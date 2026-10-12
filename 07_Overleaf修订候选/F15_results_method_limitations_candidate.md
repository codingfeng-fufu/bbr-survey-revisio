# F15 结果、方法与限制候选稿（2026-10-12）

本文件是候选材料，供冯宗林与作者在 Overleaf 主版本中核对后合入。所有数字来自执行台账，不应脱离条件矩阵扩展为普遍版本排名。

## 方法段候选

实验节点运行 Ubuntu 22.04、Linux `6.13.7-bbr3`，2 vCPU、约 3.6 GiB RAM。BBRv3 的源码来自 `/home/ubuntu/bbr-3.tar.gz`，源码中的 `BBR_VERSION=3`，内核配置为 `CONFIG_TCP_CONG_BBR=y`，运行时注册名为 `bbr`。同一源码包中的 `tcp_bbr1.c` 以独立 `tcp_bbr1.ko` 模块加载，运行时注册名为 `bbr1`；该模块使用了针对 6.13 未导出 TSO 辅助函数的明确兼容补丁。BBR2 使用独立的 `5.13.12-bbr2alpha` 内核；Ubuntu in-tree baseline 保留为单独实现标签。Mininet、iperf3 和 tc 版本及原始命令记录在对应 manifest 和 runtime record 中。

每个正式条件建立新的 Mininet 拓扑，并在 100 Mbps 共享瓶颈上运行两条持续 TCP 流。E1 使用 20 ms、40 ms 和 80 ms 的第二流 RTT以及 0.5、2 和 10 倍冻结参考队列；E2 使用同 RTT 的 BBR/CUBIC 对照；每个条件运行 5 次，每次 180 s，前 30 s 为预热。吞吐从 iperf3 接收端 JSON 提取，公平性使用两流 Jain 指数，时延使用加载期间 ping 的 RTT 均值，重传和队列计数从客户端与 qdisc 记录提取。ECN 在本实验配置中关闭，并保留每次运行的 sysctl、qdisc、ss 和退出状态。

E3 在 F07-v1 预测冻结后执行 8 个留出网络案例：50/200 Mbps、10/60 ms、1/4 倍冻结队列，分别运行双 BBRv3 和双 CUBIC，每个条件 5 次，共 80 次。预测、原始日志、逐运行指标、条件汇总和逐案例判定分别保存在 `formal_e3_20261011/`。

## 结果段候选

在 E1/E2 的 100 Mbps 矩阵中，Ubuntu in-tree baseline、独立 BBRv1 module、BBR2 和 BBRv3 的结果随 RTT、队列和竞争协议变化。等 RTT 双流的总有效吞吐接近瓶颈容量，但流份额和 Jain 指数仍受实现、队列和启动过程影响；因此不能仅凭 RTT 与 inflight 的乘积推出带宽份额。异构 RTT条件下，长 RTT 流份额随实现和队列设置改变，结果支持条件化的 RTT 公平性表述，而不支持“长 RTT 必然占优”的普遍断言。

在 E2 的无 ECN BBR/CUBIC 对照中，BBR 流份额、CUBIC 流份额、加载 RTT、队列计数和重传计数均被分别报告。观察到的份额差异用于描述该实现和负载下的竞争结果，不能单独作为内部机制已被直接观测的证据。

E3 的 80 次留出运行全部完成。8 个案例的吞吐方向性预测得到支持；等 RTT 条件下 BBRv3 双流的 Jain 指数接近 1。部分 Q=4 条件相对于配对 Q=1 条件的加载 RTT变化不稳定，因此保留 `undetermined`，不把小幅差异解释为普遍深队列因果效应。所有 E3 条件的瓶颈 qdisc 丢包计数为 0，所以重传预测在该批次标为 `not_applicable`。

## 限制段候选

这些实验覆盖的是受控 Mininet 拓扑、指定容量、RTT、FIFO队列和关闭 ECN 的条件集合，不代表所有公网、无线或 LEO 链路。当前 Ubuntu in-tree baseline 的实现身份可以追溯到内核构建，但不能据此声称它就是独立确认的 BBRv1。E1/E2/E3 均不能替代第二台机器的独立复跑；当前结果的复现检查在同一节点完成。

本轮 E3 覆盖拥塞丢包条件，但正式 E3 矩阵没有触发瓶颈丢包。随后完成了 20 次随机丢包扩展：人工丢包施加在独立接入链路，瓶颈队列丢包保持为 0，BBRv3 与 CUBIC 的重传和吞吐变化按条件汇总。该扩展支持区分本实验中的人工接入链路丢包和瓶颈队列丢包，但 0.1% 独立随机丢包不能等同于真实无线或卫星信道；随机种子也未由当前接口暴露。框架的 working bins 和方向性判定仍应与绝对队列字节数、每流 RTT、ECN、队列管理和流数一起报告。

## 证据路径

- E1/E2 统一汇总：`06_执行台账/cross_version_20261012/`
- BBRv3 E3：`06_执行台账/formal_e3_20261011/`
- 机制与框架候选：`07_Overleaf修订候选/F05_change_log.md`、`F06_framework_change_log.md`
- F07 预测协议：`07_Overleaf修订候选/F07_validation_protocol_v1_FROZEN.md`
