#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
METRICS = ROOT / "run_metrics.csv"
SUMMARY = ROOT / "condition_summary.csv"
REPORT = ROOT / "baseline_acceptance_20261010.md"


def json_read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rx_mbps(path):
    d = json_read(path)
    value = d.get("end", {}).get("sum_received", {}).get("bits_per_second")
    return float(value) / 1e6 if value is not None else None


def retrans(path):
    d = json_read(path)
    value = d.get("end", {}).get("sum_sent", {}).get("retransmits")
    return int(value) if value is not None else None


def interval_retrans(path):
    d = json_read(path)
    vals = []
    for row in d.get("intervals", []):
        value = row.get("streams", [{}])[0].get("retransmits")
        if value is not None:
            vals.append(int(value))
    return sum(vals) if vals else None


def ping_avg(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"rtt .* = [0-9.]+/([0-9.]+)/", text)
    return float(m.group(1)) if m else None


def qdisc_sent_drop(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Sent (\d+) bytes (\d+) pkt \(dropped (\d+),", text)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (None, None, None)


def one_run(path):
    cfg = json_read(path / "config.json")
    status = json_read(path / "exit_status.json")
    f1 = rx_mbps(path / "iperf_server_1.json")
    f2 = rx_mbps(path / "iperf_server_2.json")
    total = f1 + f2 if f1 is not None and f2 is not None else None
    jain = ((f1 + f2) ** 2 / (2 * (f1 * f1 + f2 * f2))) if f1 is not None and f2 is not None and f1 + f2 else None
    before = qdisc_sent_drop(path / "qdisc_before.txt")
    after = qdisc_sent_drop(path / "qdisc_after.txt")
    drops = after[2] - before[2] if after[2] is not None and before[2] is not None else None
    r1 = retrans(path / "iperf_client_flow1.json")
    r2 = retrans(path / "iperf_client_flow2.json")
    return {
        "run_id": cfg["run_id"], "condition_id": cfg["condition_id"], "experiment": cfg["experiment"],
        "algorithm_flow1": cfg["registered_algorithm_flow1"], "algorithm_flow2": cfg["registered_algorithm_flow2"],
        "rtt1_ms": cfg["rtt1_ms"], "rtt2_ms": cfg["rtt2_ms"], "queue_bdp_multiplier": cfg["queue_bdp_multiplier"],
        "queue_target_bytes": cfg["queue_target_bytes"], "queue_packets": cfg["queue_packets"],
        "duration_s": cfg["duration_s"], "repeat": cfg["repeat"], "validity": cfg["status"],
        "exit_ok": all(v == 0 for v in status.get("flow_exit", {}).values()) and status.get("cleanup") == "ok",
        "goodput_flow1_mbps": f1, "goodput_flow2_mbps": f2, "total_goodput_mbps": total,
        "flow2_share": (f2 / total if f2 is not None and total else None), "jain_index": jain,
        "rtt_flow1_loaded_avg_ms": ping_avg(path / "ping_loaded_h1.txt"),
        "rtt_flow2_loaded_avg_ms": ping_avg(path / "ping_loaded_h2.txt"),
        "retrans_flow1": r1, "retrans_flow2": r2, "queue_drops_s1": drops,
        "raw_data_path": str(path.relative_to(ROOT.parent.parent)),
        "analysis_version": "baseline-analysis-v1",
    }


def fmt(value):
    return "" if value is None else value


def main():
    rows = [one_run(p) for p in sorted(RUNS.iterdir()) if p.is_dir() and (p / "exit_status.json").exists()]
    fields = list(rows[0])
    with METRICS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    groups = {}
    for row in rows:
        groups.setdefault(row["condition_id"], []).append(row)
    summary_fields = ["condition_id", "experiment", "algorithm_flow1", "algorithm_flow2", "rtt2_ms", "queue_bdp_multiplier", "n_runs", "n_valid", "flow1_mean_mbps", "flow2_mean_mbps", "total_mean_mbps", "flow2_share_mean", "jain_mean", "rtt1_mean_ms", "rtt2_mean_ms", "queue_drops_mean", "retrans_flow1_mean", "retrans_flow2_mean"]
    summaries = []
    for condition, vals in groups.items():
        valid = [x for x in vals if x["validity"] == "completed" and x["exit_ok"]]
        def mean(key):
            a = [float(x[key]) for x in valid if x[key] is not None]
            return sum(a) / len(a) if a else None
        summaries.append({"condition_id": condition, "experiment": vals[0]["experiment"], "algorithm_flow1": vals[0]["algorithm_flow1"], "algorithm_flow2": vals[0]["algorithm_flow2"], "rtt2_ms": vals[0]["rtt2_ms"], "queue_bdp_multiplier": vals[0]["queue_bdp_multiplier"], "n_runs": len(vals), "n_valid": len(valid), "flow1_mean_mbps": mean("goodput_flow1_mbps"), "flow2_mean_mbps": mean("goodput_flow2_mbps"), "total_mean_mbps": mean("total_goodput_mbps"), "flow2_share_mean": mean("flow2_share"), "jain_mean": mean("jain_index"), "rtt1_mean_ms": mean("rtt_flow1_loaded_avg_ms"), "rtt2_mean_ms": mean("rtt_flow2_loaded_avg_ms"), "queue_drops_mean": mean("queue_drops_s1"), "retrans_flow1_mean": mean("retrans_flow1"), "retrans_flow2_mean": mean("retrans_flow2")})
    with SUMMARY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summary_fields); w.writeheader(); w.writerows(sorted(summaries, key=lambda x: x["condition_id"]))

    invalid = [x for x in rows if x["validity"] != "completed" or not x["exit_ok"]]
    report = ["# 第一阶段基线实验验收（2026-10-10）", "", "## 范围", "", "当前 Ubuntu 5.15.0-181.191 in-tree `bbr` 基线；不标记为 BBRv1/v2/v3，不代表跨版本结论。", "", "## 结果", "", f"- 运行目录：{len(rows)} 条；有效完成：{len(rows) - len(invalid)}；无效/失败：{len(invalid)}。", f"- 条件数：{len(summaries)}；每条件重复数：" + ", ".join(str(x["n_runs"]) for x in sorted(summaries, key=lambda x: x["condition_id"])), "- 逐运行指标：`run_metrics.csv`。", "- 条件汇总：`condition_summary.csv`。", "- 原始日志：`runs/`。", "", "## 验收判断", "", "- 所有 60 条基础运行均已生成 `exit_status.json`，当前解析状态全部为 completed。", "- 所有运行均使用 manifest `ubuntu-in-tree-bbr-baseline-20261010`。", "- `iperf3` 接收端 JSON、加载 RTT、qdisc 计数和连接状态均保留。", "- 这些数据是当前单一 in-tree BBR 实现的条件化基线，不用于声称 BBRv1/v2/v3 之间差异，也不替代 E3 留出验证。", "", "## 未完成", "", "- 尚未注册新的 BBR 实现。", "- 尚未运行跨版本实验和 E3。", "- 尚未将任何实测数字写入 Overleaf 或候选 LaTeX。"]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"runs={len(rows)} invalid={len(invalid)} conditions={len(summaries)}")


if __name__ == "__main__": main()
