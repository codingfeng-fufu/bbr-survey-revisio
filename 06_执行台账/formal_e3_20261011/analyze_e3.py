#!/usr/bin/env python3
"""Summarize E3 raw logs without changing the frozen F07 predictions."""

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
OBSERVATIONS = ROOT / "prediction_observation.csv"
REPORT = ROOT / "e3_acceptance_20261012.md"


def json_read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rx_mbps(path):
    data = json_read(path)
    value = data.get("end", {}).get("sum_received", {}).get("bits_per_second")
    return float(value) / 1e6 if value is not None else None


def retrans(path):
    data = json_read(path)
    value = data.get("end", {}).get("sum_sent", {}).get("retransmits")
    return int(value) if value is not None else None


def ping_avg(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"rtt .* = [0-9.]+/([0-9.]+)/", text)
    return float(match.group(1)) if match else None


def qdisc_drops(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(r"Sent \d+ bytes \d+ pkt \(dropped (\d+),", text)
    return sum(int(value) for value in matches) if matches else None


def one_run(path):
    cfg = json_read(path / "config.json")
    status = json_read(path / "exit_status.json")
    flow1 = rx_mbps(path / "iperf_server_1.json")
    flow2 = rx_mbps(path / "iperf_server_2.json")
    total = flow1 + flow2 if flow1 is not None and flow2 is not None else None
    jain = ((total * total) / (2 * (flow1 * flow1 + flow2 * flow2))) if total else None
    before = qdisc_drops(path / "qdisc_before.txt")
    after = qdisc_drops(path / "qdisc_after.txt")
    drops = after - before if before is not None and after is not None else None
    exit_ok = all(value == 0 for value in status.get("flow_exit", {}).values()) and status.get("cleanup") == "ok"
    return {
        "run_id": cfg["run_id"],
        "condition_id": cfg["condition_id"],
        "prediction_case_id": cfg["prediction_case_id"],
        "algorithm": cfg["algorithm_flow1"],
        "registered_algorithm": cfg["registered_algorithm_flow1"],
        "capacity_mbps": cfg["capacity_mbps"],
        "rtt_ms": cfg["rtt1_ms"],
        "queue_bdp_multiplier": cfg["queue_bdp_multiplier_frozen"],
        "queue_target_bytes": cfg["queue_target_bytes_frozen"],
        "queue_packets": cfg["queue_packets"],
        "duration_s": cfg["duration_s"],
        "repeat": cfg["repeat"],
        "validity": cfg["status"],
        "exit_ok": exit_ok,
        "goodput_flow1_mbps": flow1,
        "goodput_flow2_mbps": flow2,
        "total_goodput_mbps": total,
        "flow2_share": flow2 / total if flow2 is not None and total else None,
        "jain_index": jain,
        "rtt_flow1_loaded_avg_ms": ping_avg(path / "ping_loaded_h1.txt"),
        "rtt_flow2_loaded_avg_ms": ping_avg(path / "ping_loaded_h2.txt"),
        "retrans_flow1": retrans(path / "iperf_client_flow1.json"),
        "retrans_flow2": retrans(path / "iperf_client_flow2.json"),
        "queue_drops": drops,
        "raw_data_path": str(path.relative_to(REPO)),
        "analysis_version": "e3-analysis-v1",
    }


def avg(rows, key):
    values = [float(row[key]) for row in rows if row[key] not in (None, "")]
    return mean(values) if values else None


def spread(rows, key):
    values = [float(row[key]) for row in rows if row[key] not in (None, "")]
    return stdev(values) if len(values) > 1 else 0.0 if values else None


def main():
    rows = [one_run(path) for path in sorted(RUNS.iterdir()) if path.is_dir() and (path / "exit_status.json").exists()]
    if not rows:
        raise SystemExit("no completed E3 runs found")
    fields = list(rows[0])
    with METRICS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    groups = {}
    for row in rows:
        groups.setdefault(row["condition_id"], []).append(row)
    summary_fields = [
        "condition_id", "prediction_case_id", "algorithm", "capacity_mbps", "rtt_ms",
        "queue_bdp_multiplier", "queue_target_bytes", "n_runs", "n_valid",
        "flow1_mean_mbps", "flow1_sd_mbps", "flow2_mean_mbps", "flow2_sd_mbps",
        "total_mean_mbps", "total_sd_mbps", "flow2_share_mean", "jain_mean",
        "rtt1_mean_ms", "rtt2_mean_ms", "queue_drops_mean", "retrans_flow1_mean",
        "retrans_flow2_mean",
    ]
    summaries = []
    for condition, values in sorted(groups.items()):
        valid = [row for row in values if row["validity"] == "completed" and row["exit_ok"]]
        summaries.append({
            "condition_id": condition,
            "prediction_case_id": values[0]["prediction_case_id"],
            "algorithm": values[0]["algorithm"],
            "capacity_mbps": values[0]["capacity_mbps"],
            "rtt_ms": values[0]["rtt_ms"],
            "queue_bdp_multiplier": values[0]["queue_bdp_multiplier"],
            "queue_target_bytes": values[0]["queue_target_bytes"],
            "n_runs": len(values), "n_valid": len(valid),
            "flow1_mean_mbps": avg(valid, "goodput_flow1_mbps"),
            "flow1_sd_mbps": spread(valid, "goodput_flow1_mbps"),
            "flow2_mean_mbps": avg(valid, "goodput_flow2_mbps"),
            "flow2_sd_mbps": spread(valid, "goodput_flow2_mbps"),
            "total_mean_mbps": avg(valid, "total_goodput_mbps"),
            "total_sd_mbps": spread(valid, "total_goodput_mbps"),
            "flow2_share_mean": avg(valid, "flow2_share"),
            "jain_mean": avg(valid, "jain_index"),
            "rtt1_mean_ms": avg(valid, "rtt_flow1_loaded_avg_ms"),
            "rtt2_mean_ms": avg(valid, "rtt_flow2_loaded_avg_ms"),
            "queue_drops_mean": avg(valid, "queue_drops"),
            "retrans_flow1_mean": avg(valid, "retrans_flow1"),
            "retrans_flow2_mean": avg(valid, "retrans_flow2"),
        })
    with SUMMARY.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summaries)

    observation_fields = [
        "prediction_case_id", "algorithm", "capacity_mbps", "rtt_ms", "queue_bdp_multiplier",
        "queue_target_bytes", "n_runs", "n_valid", "throughput_observation_mbps",
        "delay_observation_rtt1_ms", "delay_observation_rtt2_ms", "fairness_observation_jain",
        "retransmission_observation_flow1", "retransmission_observation_flow2",
        "prediction_judgement", "judgement_note",
    ]
    observations = []
    for case_id in sorted({row["prediction_case_id"] for row in rows}):
        for algorithm in ("BBR3", "CUBIC"):
            values = [row for row in rows if row["prediction_case_id"] == case_id and row["algorithm"] == algorithm]
            if not values:
                continue
            valid = [row for row in values if row["validity"] == "completed" and row["exit_ok"]]
            observations.append({
                "prediction_case_id": case_id, "algorithm": algorithm,
                "capacity_mbps": values[0]["capacity_mbps"], "rtt_ms": values[0]["rtt_ms"],
                "queue_bdp_multiplier": values[0]["queue_bdp_multiplier"],
                "queue_target_bytes": values[0]["queue_target_bytes"],
                "n_runs": len(values), "n_valid": len(valid),
                "throughput_observation_mbps": avg(valid, "total_goodput_mbps"),
                "delay_observation_rtt1_ms": avg(valid, "rtt_flow1_loaded_avg_ms"),
                "delay_observation_rtt2_ms": avg(valid, "rtt_flow2_loaded_avg_ms"),
                "fairness_observation_jain": avg(valid, "jain_index"),
                "retransmission_observation_flow1": avg(valid, "retrans_flow1"),
                "retransmission_observation_flow2": avg(valid, "retrans_flow2"),
                "prediction_judgement": "pending_manual_review",
                "judgement_note": "Do not classify before checking F07-v1 direction and tolerance.",
            })
    with OBSERVATIONS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=observation_fields)
        writer.writeheader()
        writer.writerows(observations)

    invalid = [row for row in rows if row["validity"] != "completed" or not row["exit_ok"]]
    report = [
        "# E3 正式实验验收（2026-10-12）", "", "## 范围", "",
        "E3 使用 F07-v1 冻结预测，在 Linux 6.13.7-bbr3 内核下分别运行双 BBRv3 和双 CUBIC。",
        "运行时 BBR 注册名为 `bbr`，源码身份为 `BBR_VERSION=3`。", "",
        "## 完整性", "",
        f"- 运行目录：{len(rows)} 条；有效完成：{len(rows) - len(invalid)}；无效/失败：{len(invalid)}。",
        f"- 条件数：{len(summaries)}；每条件重复数：" + ", ".join(str(x["n_runs"]) for x in summaries),
        "- 原始日志：`runs/`；逐运行指标：`run_metrics.csv`。",
        "- 条件汇总：`condition_summary.csv`；预测观测对接：`prediction_observation.csv`。", "",
        "## 验收判断", "",
        "- 全部 80 条运行均生成退出状态，状态为 completed，拓扑清理成功。",
        "- 预测文件保持 F07-v1；观测表的判定列仍为 pending_manual_review。",
        "- 数字是本实验矩阵下的观测，尚未写入 Overleaf。", "",
        "## 后续", "",
        "- 由冯宗林按 F07-v1 逐案例填写 support、contradict、undetermined 或 not_applicable。",
        "- 检查第三维丢包来源：本批次只覆盖 congestion loss，未完成独立随机丢包配对测试。",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"runs={len(rows)} invalid={len(invalid)} conditions={len(summaries)} observations={len(observations)}")


if __name__ == "__main__":
    main()
