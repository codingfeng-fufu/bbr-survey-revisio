# BBRv3 正式实验验收（2026-10-11）

## 范围

独立启动的 Linux 6.13.7-bbr3 内核，源码 `BBR_VERSION=3`，`CONFIG_TCP_CONG_BBR=y`；运行时注册名为 `bbr`，实验标签为 BBRv3。

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
- 这些是 BBRv3 内核下的正式条件化结果，不替代 E3 跨版本结论。

## 后续

- E3 已在独立批次 `formal_e3_20261011` 完成；随机丢包扩展另有独立批次。
- 实测数字尚未合入 Overleaf 主版本。
