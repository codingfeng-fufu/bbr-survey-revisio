# E3 正式实验验收（2026-10-12）

## 范围

E3 使用 F07-v1 冻结预测，在 Linux 6.13.7-bbr3 内核下分别运行双 BBRv3 和双 CUBIC。
运行时 BBR 注册名为 `bbr`，源码身份为 `BBR_VERSION=3`。

## 完整性

- 运行目录：80 条；有效完成：80；无效/失败：0。
- 条件数：16；每条件重复数：5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
- 原始日志：`runs/`；逐运行指标：`run_metrics.csv`。
- 条件汇总：`condition_summary.csv`；预测观测对接：`prediction_observation.csv`。

## 验收判断

- 全部 80 条运行均生成退出状态，状态为 completed，拓扑清理成功。
- 预测文件保持 F07-v1；观测表的判定列仍为 pending_manual_review。
- 数字是本实验矩阵下的观测，尚未写入 Overleaf。

## 后续

- 由冯宗林按 F07-v1 逐案例填写 support、contradict、undetermined 或 not_applicable。
- 第三维随机丢包配对测试已另批次完成，见 `formal_random_loss_20261012/random_loss_acceptance_20261012.md`；该结果只支持当前人工接入链路条件，不等同真实无线信道。
