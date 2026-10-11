# E3 复现检查（F13）

- 原始运行目录：`formal_e3_20261011/runs/`
- 原始运行数：80
- 有效运行数：80
- 无效运行数：0
- 分析命令：`python3 formal_e3_20261011/analyze_e3.py`
- 图表与判定命令：`python3 formal_e3_20261011/make_e3_artifacts.py`
- 分析输出：`run_metrics.csv`、`condition_summary.csv`、`prediction_observation.csv`
- 判定输出：`prediction_observation_reviewed.csv`
- 候选图输出：`formal_e3_20261011/figures/`
- 复跑结果：分析脚本和制图脚本均返回 0；行数分别为 81、17、17、9（含表头）。
- 独立第二台机器复跑：尚未完成。
- PDF 编译复跑：尚未完成，当前主机没有 `pdflatex`/`latexmk`。
