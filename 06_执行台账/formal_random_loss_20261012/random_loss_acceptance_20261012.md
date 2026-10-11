# 随机丢包扩展验收（2026-10-12）

## 范围

固定 100 Mbps、20 ms、2×BDP、FIFO、ECN关闭；人工丢包施加在独立 h3 接入链路，瓶颈为 s1-eth3。BBRv3 和 CUBIC 分别运行 0% 与 0.1% 人工丢包，每条件 5 次。

- 运行数：20；有效：20；无效：0。
- `artificial_loss_drops` 来自 s2-eth1；`bottleneck_drops` 来自 s1-eth3。
- 随机种子未由当前 Mininet/iproute2 接口暴露，记录为 unavailable。

## 条件汇总

| Algorithm | Artificial loss | Total goodput (Mbps) | Jain | Artificial drops | Bottleneck drops | Retrans flow 1 | Retrans flow 2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BBRv3 | 0% | 93.867 | 1.000 | 0.0 | 0.0 | 0.0 | 0.8 |
| BBRv3 | 0.1% | 94.247 | 0.994 | 119.8 | 0.0 | 777.4 | 688.4 |
| CUBIC | 0% | 95.585 | 0.961 | 0.0 | 0.0 | 0.0 | 0.0 |
| CUBIC | 0.1% | 81.061 | 0.995 | 105.4 | 0.0 | 642.4 | 636.4 |

## 解释边界

人工丢包和瓶颈丢包已分开记录。该扩展支持在本矩阵中区分人工接入链路丢包与瓶颈队列丢包，但不能把 0.1% 独立随机丢包等同于真实无线或卫星信道。结果仍限于当前容量、RTT、队列和实现。
