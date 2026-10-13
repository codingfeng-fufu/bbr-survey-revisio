# Pan et al. 2021 原始全文核验

论文：Improved RTT Fairness of BBR Congestion Control Algorithm based on Adaptive Congestion Window；Electronics 10 (2021), 615；DOI 10.3390/electronics10050615。
来源：`https://mdpi-res.com/d_attachment/electronics/electronics-10-00615/article_deploy/electronics-10-00615.pdf`。18页；SHA256 `a858ed37aa435d5613bb728905920bf5374d1af10e982f049a992b405061dbbe`。

## 本次已核实范围

第8页已视觉检查：Section 5说明使用NS3、BBR/BBQ/DA-BBR/BBR-ACW对照、DropTail；每个案例重复10次、每次300秒。同页对包大小写作“1 kb”，单位含义未进一步确认，不能自行解释成1 kB。

第8页Eq.2为 beta = Ti/(Ti+pi)，用于按队列相关量缩小较长RTT流的cwnd gain。该机制证据支持将BBR-ACW归为拥塞窗口调整方案，不能据此声称修改后的所有版本或任意网络均获得公平性。

第9页Section 5.1文本定位：随机丢包测试使用1/5倍BDP队列和0/1/3/6%丢包；仍需视觉检查结果图与所有配置字段。摘要中的“公平性提升超过50%、时延减少54%”本次没有逐图复算，不升级为已验证的定量综合结论。

PDF文本提取存在重叠重复文字层；字段核实以对应页面渲染为准。本次是局部证据核验，尚未关闭全文资格判断、研究/报告重复关系及最终纳入。
