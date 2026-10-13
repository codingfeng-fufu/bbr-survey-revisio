# Jaeger et al. 2019 作者全文定位

TUM官方publication页面链接至作者PDF `https://www.net.in.tum.de/fileadmin/bibtex/publications/papers/ComCom-2019-TCP-BBR.pdf`，已实际下载。SHA256 `f54dfacb82a48900f3f61d4d16b9bd6c91aa44e5ac3bfdf29b9e82e099c812e5`。全文为16页作者排版稿，与期刊页码31–43分别记录。

本次文本定位：第4页说明Linux network namespaces与Mininet；第8页Section 5/Figure 10邻近正文明确讨论1.5倍BDP以内持续丢包、约3倍BDP附近BBR/CUBIC份额趋于公平、更大buffer下CUBIC份额增加。该页另讨论固定一流50 ms、改变另一流RTT的条件。

当前仅取得全文并完成局部文本定位；Figure 10及参数尚未完成视觉核验。原文描述和图表条件必须一起确认，不能将“3倍BDP”当作跨版本、跨拓扑普适阈值。没有完成整篇资格筛选或研究/报告重复归并，最终纳入状态保持开放。

## 2026-10-12 图文交叉核验

已视觉检查作者PDF第8、9页。Figure 10位于第9页：10a固定50 ms RTT扫描buffer；10b固定2.3 BDP同时改变两流RTT；10c固定一流50 ms、扫描另一流RTT，使用1/2.5/5 BDP。公平性纵轴为作者定义的Ftp，不能直接当作本文Jain指标。

第8页正文的1.5/3 BDP描述与第9页图的总体趋势对应；不能将其替换成“所有BBR版本在≥3BDP都会被CUBIC压制”的通用规则。第9页多流测试另为50 ms、10 Mbit/s、2.5 BDP、240 s，其参数不能直接挪给Figure 10所有面板。

此前文件将作者稿误记为13页，现用pdfinfo确认并改为16页。最终纳入仍未关闭；本次完成的是指定图文结论核验。
