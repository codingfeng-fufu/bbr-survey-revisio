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
- 完整候选片段已独立编译；用户提供的完整项目 zip 已生成 28 页 PDF。仓库候选副本仍未合入该完整资产包。
- 随机丢包扩展：`formal_random_loss_20261012/analyze_random_loss.py` 返回 0；20/20 有效，4 个条件汇总完成。
- 跨版本汇总：`cross_version_20261012/analyze_cross_version.py` 返回 0；36 条输入条件统一为 12 条三实现对照。
- 候选片段编译：F13 E3 与 F15 跨版本片段由 `latexmk` 成功生成 1 页 PDF；最终轮无新的 Overfull/Underfull 警告。
- 完整 CAS 主稿：用户提供 zip 已成功编译；仓库候选副本仍需合入主版本后重编译，详见 `zip_full_compile_check_20261012.md`。
