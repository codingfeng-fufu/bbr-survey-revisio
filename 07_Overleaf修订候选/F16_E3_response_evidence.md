# E3 回复信证据候选（F16）

## 对 R1-M3、R1-M4、R2-2、R3-3 的候选回应

我们保留了 F07-v1 的预测文件，并在查看结果前冻结了 8 个留出案例。随后在 Linux `6.13.7-bbr3` 内核中分别运行双 BBRv3 与双 CUBIC，每个案例独立重复 5 次，共 80 次。逐运行原始日志、条件汇总和预测观测对接表已保存于 `06_执行台账/formal_e3_20261011/`。

在这组等 RTT 留出条件中，吞吐方向性预测得到支持，BBRv3 双流 Jain 指数接近 1。部分 Q=4 的加载 RTT配对没有稳定单调增加，因此按 F07-v1 标为 `undetermined`，没有把微小差异解释成普遍深队列效应。E3 矩阵的瓶颈队列丢包计数为 0；随后完成的 20 次随机丢包扩展在独立接入链路记录到人工丢包，而瓶颈队列仍为 0。该结果支持区分两类丢包来源，但不等同于真实无线或卫星信道，随机种子也未由当前接口暴露。

## 证据位置

- 原始运行：`06_执行台账/formal_e3_20261011/runs/`
- 逐运行指标：`06_执行台账/formal_e3_20261011/run_metrics.csv`
- 条件汇总：`06_执行台账/formal_e3_20261011/condition_summary.csv`
- 预测观测：`06_执行台账/formal_e3_20261011/prediction_observation.csv`
- 人工判定：`06_执行台账/formal_e3_20261011/prediction_observation_reviewed.csv`
- 验收记录：`06_执行台账/formal_e3_20261011/e3_acceptance_20261012.md`
- 随机丢包扩展：`06_执行台账/formal_random_loss_20261012/random_loss_acceptance_20261012.md`

本文件是候选回复材料，不代表已写入 Overleaf 或已向期刊提交。
