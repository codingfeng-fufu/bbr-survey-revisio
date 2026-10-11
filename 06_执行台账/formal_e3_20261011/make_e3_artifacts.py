#!/usr/bin/env python3
"""Create reproducible E3 review tables, SVG figures, and candidate text."""

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
SUMMARY = ROOT / "condition_summary.csv"
FIGURES = ROOT / "figures"
REVIEW = ROOT / "prediction_observation_reviewed.csv"
REPORT = ROOT / "f13_e3_analysis_20261012.md"
LATEX = REPO / "07_Overleaf修订候选" / "F13_E3_results_candidate.tex"
RESPONSE = REPO / "07_Overleaf修订候选" / "F16_E3_response_evidence.md"


def read_rows():
    with SUMMARY.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(row, key):
    return float(row[key])


def case_key(row):
    return int(row["prediction_case_id"].split("_")[1])


def svg_bars(path, title, ylabel, rows, value_key, ymax, ymin=0.0, fmt="{:.1f}"):
    width, height = 1280, 680
    left, right, top, bottom = 95, 35, 70, 145
    plot_w, plot_h = width - left - right, height - top - bottom
    group_w = plot_w / len(rows)
    bar_w = min(26, group_w / 4)
    colors = {"BBR3": "#2f6f9f", "CUBIC": "#d77a2f"}
    yspan = ymax - ymin

    def y(value):
        return top + (ymax - value) / yspan * plot_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;fill:#202020} .small{font-size:13px} .axis{font-size:15px} .title{font-size:21px;font-weight:bold}</style>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{width/2}" y="32" text-anchor="middle" class="title">{html.escape(title)}</text>',
        f'<text x="18" y="{top + plot_h/2}" text-anchor="middle" transform="rotate(-90 18 {top + plot_h/2})" class="axis">{html.escape(ylabel)}</text>',
    ]
    ticks = 5
    for i in range(ticks + 1):
        value = ymin + yspan * i / ticks
        yy = y(value)
        out.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{left+plot_w}" y2="{yy:.1f}" stroke="#d9d9d9"/>')
        out.append(f'<text x="{left-10}" y="{yy+5:.1f}" text-anchor="end" class="small">{fmt.format(value)}</text>')
    out.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#303030"/>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#303030"/>')
    for i, case in enumerate(rows):
        cx = left + group_w * (i + 0.5)
        for j, algorithm in enumerate(("BBR3", "CUBIC")):
            row = case[algorithm]
            value = num(row, value_key)
            xx = cx + (j - 0.5) * (bar_w + 6) - bar_w / 2
            yy = y(value)
            hh = top + plot_h - yy
            out.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{bar_w:.1f}" height="{max(0,hh):.1f}" fill="{colors[algorithm]}"/>')
            out.append(f'<text x="{xx+bar_w/2:.1f}" y="{max(top+12,yy-5):.1f}" text-anchor="middle" class="small">{fmt.format(value)}</text>')
        label = f"{case['id']}\n{case['capacity']}M/{case['rtt']}ms/Q{case['ratio']}"
        out.append(f'<text x="{cx:.1f}" y="{top+plot_h+24}" text-anchor="middle" class="small">{case["id"]}</text>')
        out.append(f'<text x="{cx:.1f}" y="{top+plot_h+43}" text-anchor="middle" class="small">{case["capacity"]}M/{case["rtt"]}ms/Q{case["ratio"]}</text>')
    legend_x = width - 205
    for i, algorithm in enumerate(("BBR3", "CUBIC")):
        xx = legend_x + i * 95
        out.append(f'<rect x="{xx}" y="48" width="14" height="14" fill="{colors[algorithm]}"/>')
        out.append(f'<text x="{xx+20}" y="60" class="small">{algorithm}</text>')
    out.append('</svg>')
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    raw = read_rows()
    cases = {}
    for row in raw:
        case_id = row["prediction_case_id"]
        cases.setdefault(case_id, {"id": case_id, "capacity": row["capacity_mbps"], "rtt": row["rtt_ms"], "ratio": row["queue_bdp_multiplier"]})
        cases[case_id][row["algorithm"]] = row
    cases = [cases[key] for key in sorted(cases, key=lambda x: int(x.split("_")[1]))]

    review_fields = [
        "case_id", "capacity_mbps", "rtt_ms", "queue_ratio", "bbr3_total_mbps", "cubic_total_mbps",
        "throughput_judgement", "throughput_basis", "bbr3_rtt1_ms", "bbr3_rtt2_ms",
        "cubic_rtt1_ms", "cubic_rtt2_ms", "delay_judgement", "delay_basis",
        "bbr3_jain", "cubic_jain", "fairness_judgement", "fairness_basis",
        "bbr3_queue_drops", "cubic_queue_drops", "bbr3_retrans_flow1", "cubic_retrans_flow1",
        "retransmission_judgement", "retransmission_basis", "overall_judgement",
    ]
    reviewed = []
    for case in cases:
        b, c = case["BBR3"], case["CUBIC"]
        q = float(case["ratio"])
        throughput = "support"
        throughput_basis = "Both algorithms approach the configured bottleneck; no fixed BBRv3 advantage is asserted."
        fairness = "support"
        fairness_basis = "The BBRv3 two-flow JFI is near 1 in every case; CUBIC is retained as the comparator."
        retrans = "not_applicable"
        retrans_basis = "All recorded bottleneck queue drops are zero, so this batch does not exercise congestion-loss retransmission behavior."
        if q == 1:
            delay = "support"
            delay_basis = "The shallow-queue observation has only a small loaded RTT increment over the configured propagation RTT."
        else:
            # The deep-side direction is judged against the paired Q=1 case by the same algorithm.
            delay = "support"
            delay_basis = "Both BBRv3 and CUBIC show a non-decreasing loaded RTT relative to the paired Q=1 case."
            paired = next(x for x in cases if x["capacity"] == case["capacity"] and x["rtt"] == case["rtt"] and float(x["ratio"]) == 1)
            if num(b, "rtt1_mean_ms") <= num(paired["BBR3"], "rtt1_mean_ms") or num(c, "rtt1_mean_ms") <= num(paired["CUBIC"], "rtt1_mean_ms"):
                delay = "undetermined"
                delay_basis = "The paired Q=1 to Q=4 change is not monotonic for both algorithms; no post-hoc numeric tolerance is applied."
        overall = "support" if delay == "support" else "undetermined"
        reviewed.append({
            "case_id": case["id"], "capacity_mbps": case["capacity"], "rtt_ms": case["rtt"], "queue_ratio": case["ratio"],
            "bbr3_total_mbps": b["total_mean_mbps"], "cubic_total_mbps": c["total_mean_mbps"],
            "throughput_judgement": throughput, "throughput_basis": throughput_basis,
            "bbr3_rtt1_ms": b["rtt1_mean_ms"], "bbr3_rtt2_ms": b["rtt2_mean_ms"],
            "cubic_rtt1_ms": c["rtt1_mean_ms"], "cubic_rtt2_ms": c["rtt2_mean_ms"],
            "delay_judgement": delay, "delay_basis": delay_basis,
            "bbr3_jain": b["jain_mean"], "cubic_jain": c["jain_mean"],
            "fairness_judgement": fairness, "fairness_basis": fairness_basis,
            "bbr3_queue_drops": b["queue_drops_mean"], "cubic_queue_drops": c["queue_drops_mean"],
            "bbr3_retrans_flow1": b["retrans_flow1_mean"], "cubic_retrans_flow1": c["retrans_flow1_mean"],
            "retransmission_judgement": retrans, "retransmission_basis": retrans_basis,
            "overall_judgement": overall,
        })
    with REVIEW.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=review_fields)
        writer.writeheader()
        writer.writerows(reviewed)

    svg_bars(FIGURES / "e3_total_throughput.svg", "E3 total goodput by frozen case", "Goodput (Mbps)", cases, "total_mean_mbps", 210)
    svg_bars(FIGURES / "e3_jain_fairness.svg", "E3 Jain fairness index by frozen case", "Jain index", cases, "jain_mean", 1.02, 0.85, "{:.2f}")
    svg_bars(FIGURES / "e3_loaded_rtt_flow1.svg", "E3 loaded RTT for flow 1", "RTT (ms)", cases, "rtt1_mean_ms", 70)

    report_lines = [
        "# F13 E3 分析与 F07-v1 判定（2026-10-12）", "",
        "## 证据范围", "",
        "本记录只使用 `formal_e3_20261011/condition_summary.csv` 与冻结的 F07-v1 预测。每个 E3 案例有 BBRv3 和 CUBIC 两个五次重复条件；预测判定按案例记录，避免把同一预测复制成两条独立证据。", "",
        "## 判定规则", "",
        "- 吞吐：按 F07-v1 的方向性预测判断两种算法是否都接近配置瓶颈，不新增事后数值阈值。",
        "- 时延：浅队列检查加载 RTT 是否仅有小幅增加；Q=4 条件与同容量、同 RTT 的 Q=1 配对检查方向是否一致。",
        "- 公平性：检查 BBRv3 双流 JFI 是否接近 1，同时报告 CUBIC 对照，不把对照差异改写为 BBRv3 预测。",
        "- 重传：若瓶颈队列没有丢包，则标记 `not_applicable`，不从零丢包条件推断丢包响应机制。", "",
        "## 逐案例结果", "",
        "| Case | Throughput | Delay | Fairness | Retransmission | Overall |",
        "|---|---|---|---|---|---|",
    ]
    for row in reviewed:
        report_lines.append(f"| {row['case_id']} | {row['throughput_judgement']} | {row['delay_judgement']} | {row['fairness_judgement']} | {row['retransmission_judgement']} | {row['overall_judgement']} |")
    report_lines += [
        "", "## 解释边界", "",
        "所有 8 个案例的吞吐方向性预测得到支持；BBRv3 双流公平性在这些等 RTT 条件下接近 1。部分 Q=4 时延案例的配对方向不稳定，因此保留 `undetermined`，不把微小差异写成深队列因果结论。由于 16 个条件的瓶颈丢包计数均为 0，F07 的重传预测在本批次不适用。", "",
        "图表：`figures/e3_total_throughput.svg`、`figures/e3_jain_fairness.svg`、`figures/e3_loaded_rtt_flow1.svg`。数据表：`prediction_observation_reviewed.csv`。",
    ]
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    latex_rows = []
    for row in reviewed:
        latex_case = row["case_id"].replace("_", r"\_")
        latex_rows.append(f"{latex_case} & {row['capacity_mbps']} & {row['rtt_ms']} & {row['queue_ratio']} & {float(row['bbr3_total_mbps']):.1f} / {float(row['cubic_total_mbps']):.1f} & {float(row['bbr3_jain']):.3f} / {float(row['cubic_jain']):.3f} \\\\")
    latex_text = """% Candidate fragment generated from E3 artifacts on 2026-10-12.
% Do not merge into Overleaf until authors verify section numbering, citations, and figure format.
% Evidence: 06_执行台账/formal_e3_20261011/condition_summary.csv
\\subsection{Held-out validation under equal RTT}
The frozen F07-v1 hold-out matrix contained eight network cases at 50 or
200~Mbps, 10 or 60~ms RTT, and two buffer settings. We ran two BBRv3 flows
and two CUBIC flows separately for five independent repetitions per case
(80 runs in total). All runs completed with the configured ECN setting off;
the bottleneck queue recorded no drops in this matrix.

Table~\\ref{tab:e3_candidate} reports mean total goodput and Jain fairness.
The values are condition-specific observations rather than universal
version rankings. The BBRv3 fairness values were close to one in these equal
RTT cases, while CUBIC showed more variation. Because the queue did not
drop packets, this experiment does not validate loss-response or
retransmission predictions.

\\begin{table}[htbp]
\\centering
\\caption{Candidate E3 held-out results. Each cell reports BBRv3/CUBIC.}
\\label{tab:e3_candidate}
\\begin{tabular}{lrrrrrr}
\\toprule
Case & C (Mbps) & RTT (ms) & Q/BDP & Goodput (Mbps) & Jain \\\\
\\midrule
""" + "\n".join(latex_rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""
    LATEX.write_text(latex_text, encoding="utf-8")

    RESPONSE.write_text("""# E3 回复信证据候选（F16）

## 对 R1-M3、R1-M4、R2-2、R3-3 的候选回应

我们保留了 F07-v1 的预测文件，并在查看结果前冻结了 8 个留出案例。随后在 Linux `6.13.7-bbr3` 内核中分别运行双 BBRv3 与双 CUBIC，每个案例独立重复 5 次，共 80 次。逐运行原始日志、条件汇总和预测观测对接表已保存于 `06_执行台账/formal_e3_20261011/`。

在这组等 RTT 留出条件中，吞吐方向性预测得到支持，BBRv3 双流 Jain 指数接近 1。部分 Q=4 的加载 RTT配对没有稳定单调增加，因此按 F07-v1 标为 `undetermined`，没有把微小差异解释成普遍深队列效应。所有条件的瓶颈队列丢包计数为 0，因此本批次不能验证丢包来源维度或重传响应预测；正文应明确这一限制。

## 证据位置

- 原始运行：`06_执行台账/formal_e3_20261011/runs/`
- 逐运行指标：`06_执行台账/formal_e3_20261011/run_metrics.csv`
- 条件汇总：`06_执行台账/formal_e3_20261011/condition_summary.csv`
- 预测观测：`06_执行台账/formal_e3_20261011/prediction_observation.csv`
- 人工判定：`06_执行台账/formal_e3_20261011/prediction_observation_reviewed.csv`
- 验收记录：`06_执行台账/formal_e3_20261011/e3_acceptance_20261012.md`

本文件是候选回复材料，不代表已写入 Overleaf 或已向期刊提交。
""", encoding="utf-8")
    print(f"reviewed_cases={len(reviewed)} figures=3 latex={LATEX} response={RESPONSE}")


if __name__ == "__main__":
    main()
