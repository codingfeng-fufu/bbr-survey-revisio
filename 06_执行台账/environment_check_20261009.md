# 实验环境核验（2026-10-09）

> 历史快照：本文件记录 2026-10-09 节点。后续已在 `6.13.7-bbr3` 特权节点完成 BBRv1 module、BBR2、BBRv3、E1/E2/E3 和随机丢包批次；当前证据见各 formal 目录的 manifest/runtime record。

## 结论

本次现场核验节点通过了环境能力门槛，并完成一次短时 Mininet/iperf3 试跑。该试跑仅验证环境、拓扑、队列和采集链路，不是论文实验结果，不得写入正文结果、预测验证或统计汇总。

正式实验仍保持阻塞：当前能够确认的是 Ubuntu Jammy 内核自带的 `tcp_bbr.ko`，但尚未取得该云镜像对应的 BBR 上游 Git commit。正式运行前必须固定实现来源、commit、配置和分析脚本；不能用本次系统包标识或 `modinfo srcversion` 冒充 Git commit。

## 节点与工具

| 项目 | 现场值 |
|---|---|
| 虚拟化 | `kvm` |
| 云厂商/实例标识 | Tencent Cloud CVM；DMI `product_name=CVM`；实例类型元数据未返回 |
| OS | Ubuntu 22.04.5 LTS (`jammy`) |
| 内核 | `5.15.0-181-generic #191-Ubuntu SMP Fri May 22 19:09:02 UTC 2026`，x86_64 |
| 资源 | 2 vCPU；内存 3.6 GiB；无 swap；根盘 59 GiB，剩余约 50 GiB |
| Mininet | 2.3.0（本次安装） |
| iperf3 | 3.9（本次安装） |
| tc/ss | iproute2 5.15.0，libbpf 0.5.0 |
| Python | `/usr/bin/python3` |
| 安装命令 | `sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y mininet iperf3` |

## 权限与内核能力

- `sudo -n true` 成功；root 下 `CAP_NET_ADMIN` 在 bounding set 中可用。
- 临时 network namespace 创建和删除成功：`ip netns add` / `ip netns del` 返回 0。
- `sudo -n modprobe tcp_bbr`、`sch_netem`、`sch_fq` 均返回 0。
- `net.ipv4.tcp_available_congestion_control = reno cubic bbr`。
- `net.ipv4.tcp_allowed_congestion_control = reno cubic bbr`。
- 现场加载模块：`tcp_bbr`、`sch_netem`、`sch_fq`。
- `tcp_bbr` 来源可确认到 Ubuntu 5.15.0-181-generic 的 in-tree kernel module；`modinfo srcversion=3B1BCEE47503FD816689638` 仅是模块构建标识，不是上游 Git commit。上游 commit：未确认，正式实验阻塞。

## 试跑状态

- 首轮失败批次：`pilot_20261009T232438+0800`。原因是无控制器的 OVS 转发未建立，两个客户端保持 `SYN-SENT`，RTT 100% 丢包，iperf3 输出为空；拓扑已清理，原始日志保留。
- 修正后的成功批次：`pilot_20261009T232814+0800`。将交换机改为无需控制器的 `OVSBridge` 后，`pingall` 为 0% 丢包，两个 iperf3 客户端和两个服务端退出码均为 0；拓扑已清理。
- 成功批次的完整原始日志：`06_执行台账/pilot_20261009/raw_logs/pilot_20261009T232814+0800/`。
- 环境命令原始输出：`06_执行台账/pilot_20261009/environment_raw_20261009.txt`。
- 试跑说明：`06_执行台账/pilot_20261009/pilot_report.md`。
- 执行脚本：`06_执行台账/pilot_20261009/run_mininet_pilot.py`。

## 未完成与后续门槛

1. 未确认云镜像对应的 BBR 上游 Git commit，不能开始 180 秒正式运行或声称 BBRv1/v2/v3 版本实验。
2. 本次使用的是 Ubuntu 内核 in-tree BBR；没有替换为其他 BBR 实现，也没有声称其为 BBRv2/v3。
3. 试跑只验证两条同版本 BBR 流、100 Mbps、20 ms RTT、FIFO-like `tbf + netem` 队列和关闭 ECN；不覆盖论文设计矩阵。
4. 需要在正式实验前补齐固定 commit、正式配置冻结、重复数/统计窗口、采集脚本版本和失败运行处理规则。
