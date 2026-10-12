# 第一阶段基线实验验收（2026-10-10）

## 范围

当前 Ubuntu 5.15.0-181.191 in-tree `bbr` 基线；不标记为 BBRv1/v2/v3，不代表跨版本结论。

## 结果

- 运行目录：60 条；有效完成：60；无效/失败：0。
- 条件数：12；每条件重复数：5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
- 逐运行指标：`run_metrics.csv`。
- 条件汇总：`condition_summary.csv`。
- 原始日志：`runs/`。

## 验收判断

- 所有 60 条基础运行均已生成 `exit_status.json`，当前解析状态全部为 completed。
- 所有运行均使用 manifest `ubuntu-in-tree-bbr-baseline-20261010`。
- `iperf3` 接收端 JSON、加载 RTT、qdisc 计数和连接状态均保留。
- 这些数据是当前单一 in-tree BBR 实现的条件化基线，不用于声称 BBRv1/v2/v3 之间差异，也不替代 E3 留出验证。

## 后续

- 新实现、跨版本和 E3 已在后续独立目录完成；本文件只记录 baseline 批次。
- 实测数字尚未合入 Overleaf 主版本。
