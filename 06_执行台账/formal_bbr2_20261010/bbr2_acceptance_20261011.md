# BBR2 正式实验验收（2026-10-11）

## 范围

独立启动的 Linux 5.13.12 `bbr2alpha` 内核，`CONFIG_TCP_CONG_BBR2=y`；实验标签为 BBR2，不将其等同于其他 BBR 版本。

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
- 这些是 BBR2 内核下的正式条件化结果，不替代 BBRv3 或 E3 跨版本结论。

## 未完成

- BBRv3 尚未注册和验证。
- E3 跨版本实验尚未运行。
- 尚未将任何实测数字写入 Overleaf 或候选 LaTeX。
