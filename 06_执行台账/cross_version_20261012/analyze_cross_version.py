#!/usr/bin/env python3
"""Unify the four E1/E2 condition summaries and make SVG comparison figures."""

import csv
import html
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "06_执行台账" / "cross_version_20261012"
FIGURES = OUT / "figures"
SOURCES = {
    "in_tree_baseline": REPO / "06_执行台账/formal_baseline_20261010/condition_summary.csv",
    "BBRv1_module": REPO / "06_执行台账/formal_bbr1_20261012/condition_summary.csv",
    "BBR2": REPO / "06_执行台账/formal_bbr2_20261010/condition_summary.csv",
    "BBRv3": REPO / "06_执行台账/formal_bbr3_20261011/condition_summary.csv",
}


def read_source(name, path):
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["implementation"] = name
            row["queue_bdp_multiplier"] = float(row["queue_bdp_multiplier"])
            for key in ("rtt2_ms", "n_runs", "n_valid", "flow1_mean_mbps", "flow2_mean_mbps", "total_mean_mbps", "flow2_share_mean", "jain_mean", "rtt1_mean_ms", "rtt2_mean_ms", "queue_drops_mean", "retrans_flow1_mean", "retrans_flow2_mean"):
                row[key] = float(row[key])
            yield row


def esc(text):
    return html.escape(str(text))


def bars(path, title, ylabel, groups, metrics, ymin, ymax, fmt="{:.1f}"):
    width, height = 1380, 700
    left, right, top, bottom = 100, 30, 72, 150
    pw, ph = width - left - right, height - top - bottom
    group_w = pw / len(groups)
    bar_w = min(22, group_w / 5)
    colors = {"in_tree_baseline": "#777777", "BBRv1_module": "#4c956c", "BBR2": "#2f6f9f", "BBRv3": "#c0517e"}
    yspan = ymax - ymin

    def y(v):
        return top + (ymax - v) / yspan * ph

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;fill:#202020}.small{font-size:12px}.axis{font-size:15px}.title{font-size:21px;font-weight:bold}</style>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{width/2}" y="32" text-anchor="middle" class="title">{esc(title)}</text>',
        f'<text x="18" y="{top+ph/2}" text-anchor="middle" transform="rotate(-90 18 {top+ph/2})" class="axis">{esc(ylabel)}</text>',
    ]
    for i in range(6):
        value = ymin + yspan * i / 5
        yy = y(value)
        out.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{left+pw}" y2="{yy:.1f}" stroke="#dddddd"/>')
        out.append(f'<text x="{left-10}" y="{yy+5:.1f}" text-anchor="end" class="small">{fmt.format(value)}</text>')
    out.append(f'<line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#333"/>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#333"/>')
    for i, group in enumerate(groups):
        cx = left + group_w * (i + 0.5)
        for j, implementation in enumerate(("in_tree_baseline", "BBRv1_module", "BBR2", "BBRv3")):
            row = group[implementation]
            value = float(row[metrics])
            xx = cx + (j - 1) * (bar_w + 5) - bar_w / 2
            yy = y(value)
            out.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{bar_w:.1f}" height="{max(0, top+ph-yy):.1f}" fill="{colors[implementation]}"/>')
            out.append(f'<text x="{xx+bar_w/2:.1f}" y="{max(top+12,yy-4):.1f}" text-anchor="middle" class="small">{fmt.format(value)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{top+ph+24}" text-anchor="middle" class="small">{esc(group["label"])}</text>')
    for i, implementation in enumerate(("in_tree_baseline", "BBRv1_module", "BBR2", "BBRv3")):
        xx = width - 470 + i * 115
        out.append(f'<rect x="{xx}" y="48" width="14" height="14" fill="{colors[implementation]}"/>')
        out.append(f'<text x="{xx+19}" y="60" class="small">{esc(implementation)}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    rows = [row for name, path in SOURCES.items() for row in read_source(name, path)]
    fields = ["implementation", "condition_id", "experiment", "algorithm_flow1", "algorithm_flow2", "rtt2_ms", "queue_bdp_multiplier", "n_runs", "n_valid", "flow1_mean_mbps", "flow2_mean_mbps", "total_mean_mbps", "flow2_share_mean", "jain_mean", "rtt1_mean_ms", "rtt2_mean_ms", "queue_drops_mean", "retrans_flow1_mean", "retrans_flow2_mean"]
    with (OUT / "cross_version_condition_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    keyed = {}
    for row in rows:
        pair = "same_protocol" if row["experiment"] == "E1" else "bbr_cubic"
        key = (row["experiment"], pair, row["rtt2_ms"], row["queue_bdp_multiplier"])
        keyed.setdefault(key, {})[row["implementation"]] = row
    comparison_fields = ["scenario_id", "experiment", "algorithm_pair", "rtt2_ms", "queue_bdp_multiplier"]
    for implementation in ("in_tree_baseline", "BBRv1_module", "BBR2", "BBRv3"):
        for metric in ("total_mean_mbps", "flow2_share_mean", "jain_mean", "rtt1_mean_ms", "rtt2_mean_ms", "queue_drops_mean", "retrans_flow1_mean", "retrans_flow2_mean"):
            comparison_fields.append(f"{implementation}_{metric}")
    comparisons = []
    for index, (key, values) in enumerate(sorted(keyed.items(), key=lambda item: (item[0][0], item[0][2], item[0][3], item[0][1])) , 1):
        if len(values) != 4:
            continue
        experiment, pair, rtt, ratio = key
        row = {"scenario_id": f"{experiment}_{index:02d}", "experiment": experiment, "algorithm_pair": pair, "rtt2_ms": rtt, "queue_bdp_multiplier": ratio}
        for implementation in ("in_tree_baseline", "BBRv1_module", "BBR2", "BBRv3"):
            source = values[implementation]
            for metric in comparison_fields[5:]:
                if metric.startswith(implementation + "_"):
                    row[metric] = source[metric[len(implementation)+1:]]
        comparisons.append(row)
    with (OUT / "cross_version_comparison.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=comparison_fields)
        writer.writeheader()
        writer.writerows(comparisons)

    for experiment in ("E1", "E2"):
        groups = []
        for row in comparisons:
            if row["experiment"] != experiment:
                continue
            group = {"label": f"R{row['rtt2_ms']}/Q{row['queue_bdp_multiplier']}"}
            for implementation in ("in_tree_baseline", "BBRv1_module", "BBR2", "BBRv3"):
                group[implementation] = {"total_mean_mbps": row[f"{implementation}_total_mean_mbps"], "jain_mean": row[f"{implementation}_jain_mean"]}
            groups.append(group)
        if groups:
            bars(FIGURES / f"{experiment.lower()}_total_goodput.svg", f"{experiment} total goodput across implementations", "Goodput (Mbps)", groups, "total_mean_mbps", 0, 105)
            bars(FIGURES / f"{experiment.lower()}_jain.svg", f"{experiment} Jain fairness across implementations", "Jain index", groups, "jain_mean", 0.45, 1.02, "{:.2f}")

    report = [
        "# 跨版本 E1/E2 汇总（2026-10-12）", "",
        "## 数据范围", "",
        "统一读取当前 Ubuntu in-tree baseline、独立 BBR2 内核和 Linux 6.13.7-bbr3 的条件汇总表。每个实现的 E1/E2 条件均为五次有效重复。", "",
        "## 实现身份", "",
        "- `in_tree_baseline`：Ubuntu in-tree `bbr`，不能直接标为 BBRv1。",
        "- `BBRv1_module`：Linux 6.13.7-bbr3 上独立加载的 `tcp_bbr1.ko`，运行时注册名 `bbr1`；这是本项目单独构建的 BBRv1 module，不是 Ubuntu baseline。",
        "- `BBR2`：`5.13.12-bbr2alpha`，运行时注册名 `bbr2`。",
        "- `BBRv3`：`6.13.7-bbr3`，源码 `BBR_VERSION=3`，运行时注册名 `bbr`。", "",
        "## 结果边界", "",
        "比较表支持在本实验容量、RTT、队列和 ECN 条件下描述条件性差异；不能把 baseline 当成 BBRv1，也不能从吞吐或 Jain 差异单独推出未观测的内部机制。E1/E2 均为无人工随机丢包矩阵，丢包来源扩展另存于 `formal_random_loss_20261012/`。", "",
        "输出：`cross_version_condition_summary.csv`、`cross_version_comparison.csv`，以及 `figures/` 下的 E1/E2 吞吐和公平性图。",
    ]
    (OUT / "cross_version_report_20261012.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"condition_rows={len(rows)} comparison_rows={len(comparisons)}")


if __name__ == "__main__":
    main()
