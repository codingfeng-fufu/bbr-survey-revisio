# Song et al. BBRv2原始研究局部核验

DOI 10.1109/ACCESS.2021.3061696。实际PDF在fulltext_acquisition_20261012/openalex_Q1_0049.pdf，首页题名和DOI对应。

PDF第6页（期刊37136）Section IV.A：Mininet与物理testbed，Linux 5.4.0-rc6，BBRv2 alpha/preview更新于2019-11-22。Mininet用于低于100 Mbps案例，物理testbed用于1 Gbps。单流buffer实验另为50 Mbps、30 ms、0.1–16BDP、50 s。不能把单流时长和参数移给所有多流图。

PDF第13页（期刊37143）已视觉核验Figure 18/19及结论。Figure 18展示在2BDP buffer的BBRv2/CUBIC共存中，loss rate>2%时间点与inflight_hi限制；作者描述BBRv2的loss-driven更新。Figure 19为双BBR/双CUBIC，不能当作双流Jain表。结论限定于当时alpha实现，指出浅buffer改善但多RTT、大buffer与错峰启动公平性问题仍在。

本次没有从正文确认全部实验ECN启停配置，因此标NR。不能由“版本支持ECN”推定“实测开启/关闭ECN”，也不将该论文的机制叙述替代当前目标源码审计。未完成全篇资格审查、重复关系和逐场景字段，最终纳入仍待核验。
