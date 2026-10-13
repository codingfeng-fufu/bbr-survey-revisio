# BBRp WLAN定量主张核查

来源：Grazia et al., DOI 10.1109/ACCESS.2020.2977834，已取得PDF。本文的候选50/60/250Mbps表及“BBRp=4.2倍CUBIC”没有找到同一配置证据，本轮撤回该表及对应机制段倍数，不自行拼接上传/下载结果。

正文Section V报告Arch Linux 4.19三节点物理testbed，ath9k/ath10k、802.11n/ac；Algorithm 1将ProbeBW首周期gain从1.25改为1.5。Section VI下载讨论Figures 12/13明确区分两个芯片，pfifo_fast在无线瓶颈；CUBIC/NewReno接近测试容量，而BBRp提供相对于标准BBR的吞吐/时延权衡。下载时发送端在有线一侧，TSQ未作为无线本地瓶颈变量扫描。

该记录基于正文文本定位；具体曲线读数和整篇资格审查仍需完成，不将所有论文百分比标为核实。更新后的候选只保留有来源的配置和机制叙述。无线cellular证据另属其他研究，不能拼成WiFi—cellular普适差异证明。
