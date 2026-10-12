# BBRv1 正式实验验收（2026-10-12）

## 范围

Linux 6.13.7-bbr3 内核加载独立 `tcp_bbr1.ko` 模块；源码来自 BBR archive 的 `tcp_bbr1.c`，运行时注册名为 `bbr1`，实验标签为 BBRv1 module. The module uses the documented 6.13 compatibility patch for the unexported TSO helper.

## 结果

- 运行目录：60 条；有效完成：60；无效/失败：0。
- 条件数：12；每条件重复数：5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
- 逐运行指标：`run_metrics.csv`。
- 条件汇总：`condition_summary.csv`。
- 原始日志：`runs/`。

## 验收判断

- 全部 60 条运行均生成 `exit_status.json`，解析状态全部为 completed。
- 全部流退出码为 0，拓扑清理状态为 ok。
- `iperf3` 接收端 JSON、加载 RTT、qdisc 计数和连接状态均保留。
- 这些是 BBRv1 module 在本内核上的正式条件化结果；实现身份与 Ubuntu in-tree baseline 分开报告，不把本模块替换成其他 BBRv1 来源。

## 未完成

- E3 跨版本实验已在独立批次完成。
- 尚未将任何实测数字写入 Overleaf。
