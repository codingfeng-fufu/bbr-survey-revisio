# E3 回复信证据候选（F16）

## 对 R1-M3、R1-M4、R2-2、R3-3 的候选回应

我们保留了 F07-v1 的预测文件，并在查看结果前冻结了 8 个留出案例。随后在 Linux `6.13.7-bbr3` 内核中分别运行双 BBRv3 与双 CUBIC，每个案例独立重复 5 次，共 80 次。逐运行原始日志、条件汇总和预测观测对接表已保存于 `06_执行台账/formal_e3_20261011/`。

在这组等RTT条件中，归档全程吞吐接近容量，BBRv3双流Jain接近1；这些是描述性观测，后续审计不签收原自动support判定。四个50Mbps案例的实际队列/BDP比为4/16而冻结标签为1/4；原预测要求五次中位数，而历史分析采用全程均值。时延是早期顺序ping，队列计数是流结束前快照，均不覆盖所声明的共同稳态窗口。正式逐项判定因此暂为undetermined，不能把快照零drop解释为全程没有拥塞丢包。

20次随机丢包扩展在独立接入链路记录人工丢包；瓶颈计数仅能描述已有快照。缺失的结束计数不能补造。0.1%独立人工丢包与真实无线/卫星错误模式不同，随机种子也未由当时接口暴露。采集v2已准备，但目标节点补跑尚未完成。

## 证据位置

- 原始运行：`06_执行台账/formal_e3_20261011/runs/`
- 逐运行指标：`06_执行台账/formal_e3_20261011/run_metrics.csv`
- 条件汇总：`06_执行台账/formal_e3_20261011/condition_summary.csv`
- 预测观测：`06_执行台账/formal_e3_20261011/prediction_observation.csv`
- 历史判定（后续审计不签收）：`06_执行台账/formal_e3_20261011/prediction_observation_reviewed.csv`
- 验收记录：`06_执行台账/formal_e3_20261011/e3_acceptance_20261012.md`
- 随机丢包扩展：`06_执行台账/formal_random_loss_20261012/random_loss_acceptance_20261012.md`

- 当前审计判定：`06_执行台账/measurement_window_audit_20261012/prediction_observation_audited.csv`
- 测量限制：`06_执行台账/measurement_window_audit_20261012.md`

本文件是候选回复材料，不代表已写入 Overleaf 或已向期刊提交。
