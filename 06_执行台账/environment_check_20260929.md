# 实验环境核查（2026-09-29）

## 已确认

- 主机：Linux `5.4.0-100-generic`，x86_64，Ubuntu 20.04 系列内核。
- 当前账号无 root 权限；运行环境为 LXC 容器，进程无 `CAP_NET_ADMIN`。
- 已发现工具：`tc`、`ss`、Mininet `2.2.2`、iperf3 `3.7`。
- 当前默认拥塞控制为 `cubic`；`tcp_available_congestion_control` 和
  `tcp_allowed_congestion_control` 在该运行环境不可见。
- `sch_netem`、`sch_fq` 的内核模块文件不存在，无法确认队列和延迟/丢包注入能力。
- 未确认：BBRv1/v2/v3 实际内核实现、内核 commit、可用队列模块、采集脚本和可复现实验命令。

## 当前状态

正式实验尚未开始，不能把设计矩阵或预测表写成实验结果。Mininet 和 iperf3
已安装，但当前内核缺少 BBR/队列能力核验所需接口和模块；在确认固定 Linux
实现、BBR commit、tc 队列模块、采集流程和配置前保持阻塞。

## 无 root 时的处理

当前账号不能安装或加载宿主内核模块，也不能授予容器网络管理能力。正式实验需要管理员在宿主机预加载 `tcp_bbr`、`sch_netem`、`sch_fq`，并提供具有 `CAP_NET_ADMIN` 的实验节点；否则改用有完整内核权限的虚拟机或远程 Linux 主机。ns-3 等用户态模拟只能作为补充，不能替代本文计划的 Linux BBR 实现验证。

## 处理边界

本次安装了 Mininet 和 iperf3，但没有启动拓扑、加载内核模块或修改系统网络。
后续环境确认由刘馨月搭建，冯宗林验收；BBR 版本和 commit 必须在 E1/E2/E3
开跑前记录。
