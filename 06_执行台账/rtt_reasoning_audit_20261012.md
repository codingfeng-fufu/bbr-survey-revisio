# RTT 公平性推理审计（F04）

## 审计结论

`BDP_i = BtlBw_i × RTprop_i` 只定义给定测量工作点下的在途数据量，不能单独证明竞争流的带宽份额。份额还受实现、探测周期、队列、RTT比、流数、AQM、启动顺序和损失/ECN条件影响。

## 证据

- E1 原始与汇总：`formal_baseline_20261010/`、`formal_bbr1_20261012/`、`formal_bbr2_20261010/`、`formal_bbr3_20261011/`。
- 统一比较：`cross_version_20261012/cross_version_comparison.csv`。
- 逐流指标：吞吐、加载 RTT、Jain、重传和 qdisc 计数均保留。

## 正文候选句

> The BDP identity determines the in-flight amount corresponding to a measured operating point; it is not a sufficient law for bandwidth allocation among competing flows. We therefore treat RTT-dependent unfairness as a configuration-conditioned mechanism hypothesis and report the measured share, delay, fairness, and loss counters separately.

## 未解决

- 第二台机器独立复跑尚未完成。
- 本机 qdisc/iperf3 结果不能外推到所有公网或无线路径。
