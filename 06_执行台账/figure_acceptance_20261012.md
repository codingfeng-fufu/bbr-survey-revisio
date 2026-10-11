# E3 图表验收记录（F13/F14候选）

- 生成日期：2026-10-12
- 输入：`formal_e3_20261011/condition_summary.csv`
- 生成脚本：`formal_e3_20261011/make_e3_artifacts.py`
- 图表：
  - `formal_e3_20261011/figures/e3_total_throughput.svg`
  - `formal_e3_20261011/figures/e3_jain_fairness.svg`
  - `formal_e3_20261011/figures/e3_loaded_rtt_flow1.svg`

## 检查结果

- 三张图均由条件汇总表重新生成，未手工录入观测数字。
- 图中区分 BBRv3 与 CUBIC，并标出容量、RTT 和冻结队列比。
- 单位分别为 Mbps、Jain 指数和 ms。
- 图表只覆盖 E3 等 RTT 留出条件，不表示所有网络场景。
- SVG 可审阅；TeX Live/`latexmk` 已安装，候选片段已完成 PDF 编译检查；完整 CAS 稿件仍缺 `cas-sc.cls`、图片和 `refs.bib`。
- 候选图尚未复制到 Overleaf 主版本。

## 待复核

- 与 Overleaf 当前图号、图注和排版宽度对齐。
- 由冯宗林确认 `undetermined` 时延案例的正文措辞。
- 如果投稿版本只接受 PDF/PNG，需在有对应转换工具的环境中转换并重新检查。
