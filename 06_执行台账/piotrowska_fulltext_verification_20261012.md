# Piotrowska 2024 全文定量核验

来源：公开 PDF `https://mdpi-res.com/d_attachment/applsci/applsci-14-05053/article_deploy/applsci-14-05053.pdf`。
本地 SHA256：`76b2421e972e25184fe957b47c97c6f6a0418cdede433c01de8720b5934cb1d0`。共 21 页。已提取文本并视觉检查第 15 页 Table 7/8；第 13 页参数和 Table 3 通过文本定位。核验范围为下列特定结论，不声称完成整篇全文资格判断或最终纳入。

## 可支持的结论

- 第 13 页 Section 5.3 / Table 4：接入链路场景为九条路径，链路速率均为 100 Mbps，RTT 为 8、32、58、78、102、128、154、178、204 ms；缓冲区 BDP 以平均 RTT 100 ms 为参考。
- 第 15 页 Table 8：BBRv3 在 0.5、1、2、10 倍 BDP 缓冲区的整体 Jain 指数为 0.70、0.62、0.81、0.86。
- 第 15 页 Table 7：同场景 BBRv2 指数为 0.51、0.54、0.70、0.80。
- 第 15 页 Table 8：2 倍 BDP 时 8 ms 流的吞吐为 24 Mbps；邻近正文将其表述为约 25% 带宽。应区分表格吞吐值与正文近似比例，不能写成精确 25 Mbps。

## 不支持的结论

这两张表没有 50 倍 BDP 条件，也不支持将 BBRv3 0.71、BBRv2 0.78 归属于该接入链路场景。2 倍 BDP 结果不是普适最优阈值，且该实验不等同于本仓库双流验证。

## 核验后可用句子

In Piotrowska's nine-path simulation, with link rates of 100 Mbps and RTTs ranging from 8 to 204 ms, BBRv3 achieved overall Jain indices of 0.70, 0.62, 0.81, and 0.86 at buffer sizes of 0.5, 1, 2, and 10 times the BDP referenced to the mean RTT. At twice the BDP, the shortest-RTT flow achieved 24 Mbps. These observations illustrate a dependence on buffer size and path configuration rather than a universal fairness threshold.

## 全文资格筛选完成（2026-10-12）

已阅读研究目标、实现说明、实验设置、各场景结果与限制，并视觉核验第9页设置表及第15页主要公平性表。按M02冻结标准纳入，理由为直接相关的多版本、多RTT、队列与协议竞争原始研究。研究ID为 `ST_PIOTROWSKA_2024_MULTIRTT`，报告ID为 `RPT_PIOTROWSKA_2024_APP14125053`。逐场景提取与限制见 `piotrowska_evidence_extraction_20261012.json`。

最终纳入字段在当前队列回填为include；这是一篇报告的完成，不是整个400报告队列验收。只有本次明确提取的字段被核验；没有复跑作者代码，也没有把全部正文机制参数升级为已独立验证。重复次数在本文核阅部分未明确报告，记NR，不从随机启动时间推定多次重复。
