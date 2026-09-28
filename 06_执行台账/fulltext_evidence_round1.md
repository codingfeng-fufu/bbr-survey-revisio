# 全文证据提取第一批

日期：2026-09-28。来源通过公开网页、作者版本或索引页面核对。字段没有在可见全文/摘要中确认的内容标为 NR；这些记录还需要写入逐条 `fulltext_queue_M04.csv` 的最终字段。

| study/report | 可核实证据 | 可支持的用途 | 不能直接支持 |
|---|---|---|---|
| Hock, Bless & Zitterbart, 2017, *Experimental evaluation of BBR congestion control*, DOI `10.1109/ICNP.2017.8117540` | 作者版本/公开页面明确讨论 BBR 的吞吐、队列、丢包和公平性；公开作者版本可获取 | RTT公平性、队列和竞争机制的原始证据 | 不能从摘要 alone 得出所有缓冲区阈值；需正文核查参数和图表 |
| Jaeger et al., 2019, *Reproducible measurements of TCP BBR congestion control*, DOI `10.1016/j.comcom.2019.05.011` | 公开PDF与摘要说明：使用 Mininet/Linux network namespaces，提供自动化、可重复的TCP拥塞控制测量框架；分析BBR与CUBIC/Reno/Vegas/Illinois竞争及BBR流公平/同步 | R3-4复现方法；R1-M5综述比较；跨协议公平性证据 | 不能把其仿真配置直接当作本文实验配置；具体数值仍需逐页提取 |
| Cao et al., 2019, *When to use and when not to use BBR*, DOI `10.1145/3355369.3355579` | 作者公开稿摘要明确覆盖 Mininet和真实网络，改变带宽、RTT和瓶颈缓冲区；报告浅缓冲、高重传、深缓冲竞争、队列和随机丢包 cliff point | R1-M3/M4适用性边界；Table 1/框架证据 | 不能把“适合”压缩成单一吞吐指标；需记录其每个场景的具体条件 |
| Piotrowska, 2024, *Performance Evaluation of TCP BBRv3 in Networks with Multiple Round Trip Times*, DOI `10.3390/app14125053` | 公开页面摘要明确覆盖全部BBR版本、多RTT、吞吐、丢包、同协议与跨协议公平性；摘要称2×BDP缓冲时队列稳定且较低 | R1-M1 RTT公平性、R2-2框架外部证据 | 具体Jain值、50×BDP条件及版本参数须从正文/图表核验，不能只依摘要 |
| BDP-Veno, *A bandwidth delay product based modified Veno for high-speed networks*, DOI `10.1016/j.jnca.2024.103983` | 公开索引摘要显示：在Veno基础上引入瓶颈BDP信息，使用ns-2并与多种TCP及BBR比较 | R3-2补充相关BDP型TCP | 不能把其仿真吞吐直接与本文BBR证据合并；实现、队列、RTT和统计需全文核对 |
| OVeno, *Optimization of Veno parameter based on stochastic approximation* | 公开索引显示：针对Veno参数和乘性下降阶段做随机近似优化 | R3-2补充相关Veno方向 | 书目信息、完整实现和实验条件仍待核实，暂不加入正式refs.bib |

## 证据使用规则

1. 公开摘要/作者页面只能支持摘要中明确写出的范围；定量数字必须回到全文页、图或表。
2. 研究使用Mininet、ns-2、ns-3或真实网络时，分别记录平台，不能把仿真软件能力与某一研究的参数选择混为一谈。
3. `suitable`必须按吞吐、时延、公平性、重传分别提取；Cao的“when to use”不能被改写成单一高吞吐结论。
4. Piotrowska的多RTT结果可作为外部证据，但不能用来证明 `BDP = BtlBw × RTprop` 单独决定带宽分配。
5. BDP-Veno与OVeno先作为相关算法背景，待全文审查通过后再决定是否进入最终证据集。

## 第一批全文核验状态

| report | 状态 | 下一步 |
|---|---|---|
| Hock 2017 | 已找到作者版本入口，待下载/逐页提取 | 记录实验带宽、RTT、buffer、flow count和公平性结果 |
| Jaeger 2019 | 已找到TUM公开PDF | 记录Mininet拓扑、指标、重复方式和竞争结果 |
| Cao 2019 | 已找到作者公开PDF | 记录浅/深buffer、loss cliff和适用性指标 |
| Piotrowska 2024 | 已找到MDPI页面和Semantic Scholar PDF入口 | 记录2×BDP、50×BDP、多RTT和Jain结果 |
| BDP-Veno | 已找到DOI和公开摘要；ScienceDirect全文访问受限 | 获取合法全文后核对ns-2配置和BBR比较 |
| OVeno | 仅有索引摘要和DOI候选线索 | 先补完整书目信息，再决定全文来源 |
