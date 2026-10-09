# 最小环境试跑报告（2026-10-09）

## 范围

这是环境试跑，不是论文实验结果。没有运行 180 秒正式配置，没有修改 Overleaf，没有写入已有 CSV、预测表或证据文件。

## 配置

- 拓扑：`h1,h2 -> s1 -> s2 -> h3`；`s1-s2` 是唯一 100 Mbps 瓶颈。
- 瓶颈方向：两端各设置 `10 ms` netem，目标 RTT 为 20 ms。
- qdisc：Mininet `TCLink` 的 `tbf + netem`；netem limit 为 83 packets，约为 `0.5 x BDP`（100 Mbps x 20 ms / 8 = 250,000 bytes；按 1500-byte packets 四舍五入）。
- ECN：各 Mininet host namespace 设置 `net.ipv4.tcp_ecn=0`。
- 拥塞控制：各 Mininet host namespace 设置 `net.ipv4.tcp_congestion_control=bbr`；实际实现为当前 Ubuntu 内核 in-tree BBR，Git commit 未确认。
- 流：两条 iperf3 TCP 流，h1/h2 分别连接 h3 的 5201/5202，运行 10 秒，间隔 1 秒。
- 原始命令入口：`sudo -n python3 06_执行台账/pilot_20261009/run_mininet_pilot.py`。

## 批次结果

| 批次 | 状态 | 原因/证据 |
|---|---|---|
| `pilot_20261009T232438+0800` | 失败，已清理 | `ping_baseline_h1.txt`/`h2.txt` 为 100% 丢包；`ss_h1.txt`/`ss_h2.txt` 为 `SYN-SENT`；iperf JSON 为空；`exit_status.json` 保留等待超时。 |
| `pilot_20261009T232814+0800` | 环境试跑成功，已清理 | `pingall.txt` 为 0% 丢包；两个客户端和两个服务端退出码均为 0；`mininet_cleanup.txt` 清理返回 0。 |

## 成功批次的观测记录

成功批次目录：`06_执行台账/pilot_20261009/raw_logs/pilot_20261009T232814+0800/`。

- RTT 基线：h1 `20.129 ms` 平均，h2 `20.136 ms` 平均。
- 负载 RTT：h1 `37.916 ms` 平均，h2 `44.925 ms` 平均。
- iperf3 客户端发送吞吐：h1 `50.744967 Mbps`，h2 `49.095149 Mbps`。
- iperf3 服务端接收吞吐：h1 `48.154300 Mbps`，h2 `46.645260 Mbps`；合计约 `94.800 Mbps`。
- 瓶颈 qdisc（s1 侧）负载快照：`Sent 45,193,108 bytes`、`29,930 packets`、`dropped 571`、`overlimits 24,558`、`backlog 77 packets`。
- 瓶颈 qdisc（s2 侧）负载快照：`Sent 488,972 bytes`、`6,634 packets`、`dropped 0`、`backlog 22 packets`。
- `ss -tin` 显示两条已建立连接均使用 `bbr`，并记录了 RTT、delivery rate、retransmission 和 BBR pacing/cwnd 字段。

以上数值只说明本次短时环境试跑的实际观测，不代表正式实验样本、预测验证或论文结论。

## 证据清单

- `environment_raw_20261009.txt`：现场环境、工具、权限、模块、qdisc 和 namespace 核验输出。
- `run_config.json`：拓扑、容量、延迟、BDP、队列上限和流数。
- `host_sysctl.txt`：各 namespace 的 BBR/ECN 配置。
- `ping_baseline_*.txt`、`ping_loaded_*.txt`、`rtt_summary.json`：RTT 原始日志与摘要。
- `iperf_client_*.json`、`iperf_server_*.json`：两条 TCP 流的原始 JSON。
- `qdisc_before_*.txt`、`qdisc_loaded_*.txt`：qdisc 配置和计数器。
- `ss_h1.txt`、`ss_h2.txt`：连接状态与 BBR 内核可观测字段。
- `exit_status.json`、`mininet_cleanup.txt`：进程和清理状态。
- 首轮失败批次的所有文件同样保留，用于解释修正原因。
