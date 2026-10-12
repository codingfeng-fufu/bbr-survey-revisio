# 跨版本 E1/E2 汇总（2026-10-12）

## 数据范围

统一读取当前 Ubuntu in-tree baseline、独立 BBR2 内核和 Linux 6.13.7-bbr3 的条件汇总表。每个实现的 E1/E2 条件均为五次有效重复。

## 实现身份

- `in_tree_baseline`：Ubuntu in-tree `bbr`，不能直接标为 BBRv1。
- `BBRv1_module`：Linux 6.13.7-bbr3 上独立加载的 `tcp_bbr1.ko`，运行时注册名 `bbr1`；这是本项目单独构建的 BBRv1 module，不是 Ubuntu baseline。
- `BBR2`：`5.13.12-bbr2alpha`，运行时注册名 `bbr2`。
- `BBRv3`：`6.13.7-bbr3`，源码 `BBR_VERSION=3`，运行时注册名 `bbr`。

## 结果边界

比较表支持在本实验容量、RTT、队列和 ECN 条件下描述条件性差异；不能把 baseline 当成 BBRv1，也不能从吞吐或 Jain 差异单独推出未观测的内部机制。E1/E2 均为无人工随机丢包矩阵，丢包来源扩展另存于 `formal_random_loss_20261012/`。

输出：`cross_version_condition_summary.csv`、`cross_version_comparison.csv`，以及 `figures/` 下的 E1/E2 吞吐和公平性图。
