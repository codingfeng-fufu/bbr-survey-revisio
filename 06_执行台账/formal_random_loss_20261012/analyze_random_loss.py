#!/usr/bin/env python3
"""Summarize the separated artificial-loss and bottleneck counters."""

import csv
import json
import re
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
RUNS = ROOT / "runs"
METRICS = ROOT / "run_metrics.csv"
SUMMARY = ROOT / "condition_summary.csv"
REPORT = ROOT / "random_loss_acceptance_20261012.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rx_mbps(path):
    value = read_json(path).get("end", {}).get("sum_received", {}).get("bits_per_second")
    return float(value) / 1e6 if value is not None else None


def retrans(path):
    value = read_json(path).get("end", {}).get("sum_sent", {}).get("retransmits")
    return int(value) if value is not None else None


def ping_avg(path):
    match = re.search(r"rtt .* = [0-9.]+/([0-9.]+)/", path.read_text(encoding="utf-8", errors="replace"))
    return float(match.group(1)) if match else None


def first_drop(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Sent \d+ bytes \d+ pkt \(dropped (\d+),", text)
    return int(match.group(1)) if match else None


def one_run(path):
    cfg = read_json(path / "config.json")
    status = read_json(path / "exit_status.json")
    f1 = rx_mbps(path / "iperf_server_1.json")
    f2 = rx_mbps(path / "iperf_server_2.json")
    total = f1 + f2 if f1 is not None and f2 is not None else None
    before_art = first_drop(path / "qdisc_before_artificial_loss.txt")
    after_art = first_drop(path / "qdisc_after_artificial_loss.txt")
    before_btl = first_drop(path / "qdisc_before_bottleneck.txt")
    after_btl = first_drop(path / "qdisc_after_bottleneck.txt")
    exit_ok = all(v == 0 for v in status.get("flow_exit", {}).values()) and status.get("cleanup") == "ok"
    return {
        "run_id": cfg["run_id"], "condition_id": cfg["condition_id"],
        "algorithm": cfg["algorithm_flow1"], "artificial_loss_pct": cfg["artificial_loss_pct"],
        "capacity_mbps": cfg["capacity_mbps"], "rtt_ms": cfg["rtt1_ms"],
        "queue_bdp_multiplier": cfg["queue_bdp_multiplier"], "queue_target_bytes": cfg["queue_target_bytes"],
        "n_runs": 1, "validity": cfg["status"], "exit_ok": exit_ok,
        "goodput_flow1_mbps": f1, "goodput_flow2_mbps": f2, "total_goodput_mbps": total,
        "flow2_share": f2 / total if f2 is not None and total else None,
        "jain_index": ((total * total) / (2 * (f1 * f1 + f2 * f2))) if total else None,
        "rtt_flow1_loaded_avg_ms": ping_avg(path / "ping_loaded_h1.txt"),
        "rtt_flow2_loaded_avg_ms": ping_avg(path / "ping_loaded_h2.txt"),
        "artificial_loss_drops": after_art - before_art if before_art is not None and after_art is not None else None,
        "bottleneck_drops": after_btl - before_btl if before_btl is not None and after_btl is not None else None,
        "retrans_flow1": retrans(path / "iperf_client_flow1.json"),
        "retrans_flow2": retrans(path / "iperf_client_flow2.json"),
        "raw_data_path": str(path.relative_to(REPO)), "analysis_version": "random-loss-analysis-v1",
    }


def avg(rows, key):
    values = [float(row[key]) for row in rows if row[key] not in (None, "")]
    return mean(values) if values else None


def sd(rows, key):
    values = [float(row[key]) for row in rows if row[key] not in (None, "")]
    return stdev(values) if len(values) > 1 else 0.0 if values else None


def main():
    rows = [one_run(path) for path in sorted(RUNS.iterdir()) if path.is_dir() and (path / "exit_status.json").exists()]
    if not rows:
        raise SystemExit("no random-loss runs found")
    fields = list(rows[0])
    with METRICS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    groups = {}
    for row in rows:
        groups.setdefault((row["algorithm"], row["artificial_loss_pct"]), []).append(row)
    summary_fields = ["algorithm", "artificial_loss_pct", "n_runs", "n_valid", "total_goodput_mean_mbps", "total_goodput_sd_mbps", "jain_mean", "rtt1_mean_ms", "rtt2_mean_ms", "artificial_loss_drops_mean", "bottleneck_drops_mean", "retrans_flow1_mean", "retrans_flow2_mean"]
    summaries = []
    for (algorithm, loss), values in sorted(groups.items()):
        valid = [row for row in values if row["validity"] == "completed" and row["exit_ok"]]
        summaries.append({
            "algorithm": algorithm, "artificial_loss_pct": loss, "n_runs": len(values), "n_valid": len(valid),
            "total_goodput_mean_mbps": avg(valid, "total_goodput_mbps"), "total_goodput_sd_mbps": sd(valid, "total_goodput_mbps"),
            "jain_mean": avg(valid, "jain_index"), "rtt1_mean_ms": avg(valid, "rtt_flow1_loaded_avg_ms"),
            "rtt2_mean_ms": avg(valid, "rtt_flow2_loaded_avg_ms"), "artificial_loss_drops_mean": avg(valid, "artificial_loss_drops"),
            "bottleneck_drops_mean": avg(valid, "bottleneck_drops"), "retrans_flow1_mean": avg(valid, "retrans_flow1"),
            "retrans_flow2_mean": avg(valid, "retrans_flow2"),
        })
    with SUMMARY.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader(); writer.writerows(summaries)
    invalid = [row for row in rows if row["validity"] != "completed" or not row["exit_ok"]]
    report = [
        "# 随机丢包扩展验收（2026-10-12）", "", "## 范围", "",
        "固定 100 Mbps、20 ms、2×BDP、FIFO、ECN关闭；人工丢包施加在独立 h3 接入链路，瓶颈为 s1-eth3。BBRv3 和 CUBIC 分别运行 0% 与 0.1% 人工丢包，每条件 5 次。", "",
        f"- 运行数：{len(rows)}；有效：{len(rows)-len(invalid)}；无效：{len(invalid)}。",
        "- `artificial_loss_drops` 来自 s2-eth1；`bottleneck_drops` 来自 s1-eth3。",
        "- 随机种子未由当前 Mininet/iproute2 接口暴露，记录为 unavailable。", "",
        "## 解释边界", "",
        "人工丢包和瓶颈丢包分开记录；只有在 20 次全部验收后，才能把该扩展用于第三维丢包来源的正文结论。结果仍限于当前容量、RTT、队列和实现。",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"runs={len(rows)} invalid={len(invalid)} conditions={len(summaries)}")


if __name__ == "__main__":
    main()
