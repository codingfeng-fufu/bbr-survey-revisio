# 全文证据提取第一批

日期：2026-09-28。来源通过公开网页、作者版本或索引页面核对。字段没有在可见全文/摘要中确认的内容标为 NR；这些记录还需要写入逐条 `fulltext_queue_M04.csv` 的最终字段。

| study/report | 可核实证据 | 可支持的用途 | 不能直接支持 |
|---|---|---|---|
| Hock, Bless & Zitterbart, 2017, *Experimental evaluation of BBR congestion control*, DOI `10.1109/ICNP.2017.8117540` | 作者版本/公开页面明确讨论 BBR 的吞吐、队列、丢包和公平性；公开作者版本可获取 | RTT公平性、队列和竞争机制的原始证据 | 不能从摘要 alone 得出所有缓冲区阈值；需正文核查参数和图表 |
| Jaeger et al., 2019, *Reproducible measurements of TCP BBR congestion control*, DOI `10.1016/j.comcom.2019.05.011` | 公开PDF与摘要说明：使用 Mininet/Linux network namespaces，提供自动化、可重复的TCP拥塞控制测量框架；分析BBR与CUBIC/Reno/Vegas/Illinois竞争及BBR流公平/同步 | R3-4复现方法；R1-M5综述比较；跨协议公平性证据 | 不能把其仿真配置直接当作本文实验配置；具体数值仍需逐页提取 |
| Cao et al., 2019, *When to use and when not to use BBR*, DOI `10.1145/3355369.3355579` | 作者公开稿摘要明确覆盖 Mininet和真实网络，改变带宽、RTT和瓶颈缓冲区；报告浅缓冲、高重传、深缓冲竞争、队列和随机丢包 cliff point | R1-M3/M4适用性边界；Table 1/框架证据 | 不能把“适合”压缩成单一吞吐指标；需记录其每个场景的具体条件 |
| Piotrowska, 2024, *Performance Evaluation of TCP BBRv3 in Networks with Multiple Round Trip Times*, DOI `10.3390/app14125053` | 多RTT仿真；接入链路9条路径、100 Mbps、RTT约8–204 ms；BBRv1/v2/v3，buffer=0.5/1/2/10×BDP；表8给出BBRv3整体Jain=0.70/0.62/0.81/0.86；2×BDP时最短RTT流占25%带宽 | R1-M1 RTT公平性、R2-2框架外部证据 | 这是单篇仿真研究的条件化结果；不能把2×BDP推广成普适最优，也不能将Jain值当作本文实验结果 |
| BDP-Veno, *A bandwidth delay product based modified Veno for high-speed networks*, DOI `10.1016/j.jnca.2024.103983` | 2024 JNCA 231；公开摘要/二级开放页面显示ns-2实现，比较Reno/NewReno/BIC/CUBIC/Vegas/Veno/Compound，另用ns-3与BBR比较；Scenario 1报告相对Veno吞吐提升57% | R3-2补充相关BDP型TCP | 当前未取得出版社全文；场景带宽、RTT、队列、重复和统计不能写入正式证据表 |
| OVeno, *Optimization of Veno parameter based on stochastic approximation* | Biswal & Patel, Simulation Modelling Practice and Theory 142 (2025) 103121, DOI `10.1016/j.simpat.2025.103121`；修改Veno的乘性下降阶段，以随机近似优化参数；摘要报告相对Reno/Compound/CUBIC/Veno吞吐提升143%/131%/66%/42%，并测试无线环境 | R3-2补充相关Veno方向 | 性能数字来自摘要，不能与BBR结果横向合并；需全文核对拓扑、参数和统计设计 |

## 证据使用规则

1. 公开摘要/作者页面只能支持摘要中明确写出的范围；定量数字必须回到全文页、图或表。
2. 研究使用Mininet、ns-2、ns-3或真实网络时，分别记录平台，不能把仿真软件能力与某一研究的参数选择混为一谈。
3. `suitable`必须按吞吐、时延、公平性、重传分别提取；Cao的“when to use”不能被改写成单一高吞吐结论。
4. Piotrowska的多RTT结果可作为外部证据，但不能用来证明 `BDP = BtlBw × RTprop` 单独决定带宽分配。
5. BDP-Veno与OVeno先作为相关算法背景，待全文审查通过后再决定是否进入最终证据集。

## Piotrowska定量核查结论

原稿中“BBRv3在50×BDP时Jain约0.71、BBRv2约0.78”的表述不能由目前核对到的Piotrowska表3/表8直接支持：表3是不同buffer和RTT ratio下各版本Jain值，表8是接入链路场景BBRv3的0.70/0.62/0.81/0.86序列；50×BDP与0.71/0.78的对应关系需要回到原稿所引用的具体来源，不能继续不核对来源就归给Piotrowska。

## 第一批全文核验状态

| report | 状态 | 下一步 |
|---|---|---|
| Hock 2017 | 已找到作者版本入口，待下载/逐页提取 | 记录实验带宽、RTT、buffer、flow count和公平性结果 |
| Jaeger 2019 | 已找到TUM公开PDF | 记录Mininet拓扑、指标、重复方式和竞争结果 |
| Cao 2019 | 已找到作者公开PDF | 记录浅/深buffer、loss cliff和适用性指标 |
| Piotrowska 2024 | 已核对MDPI页面和公开PDF片段 | 已记录2×BDP、RTT表和BBRv3 Jain序列；50×BDP归属待回溯 |
| BDP-Veno | DOI和候选书目信息核实；ScienceDirect全文访问受限 | 取得合法全文后核对ns-2配置和BBR比较 |
| OVeno | 卷、期、文章号和DOI已核实；全文仍不可得 | 取得全文后核对仿真配置和性能数字 |

## 定量字段补充（公开全文定位）

| 研究 | 平台/配置 | 关键结果 | 定位 |
|---|---|---|---|
| Hock et al. 2017 | Linux kernel 4.9 BBR；瓶颈10 Gbit/s与1 Gbit/s；六流图中RTT min=20 ms，并含20/40/80 ms多RTT图 | 结论明确覆盖单流、多流、不同RTT及BBR/CUBIC竞争；作者报告高带宽下多流行为偏离公平目标 | 作者PDF p.1实验概述；Fig. 7 p.6；Fig. 14 p.8；结论 p.10 |
| Jaeger et al. 2019 | Mininet作为网络仿真后端，Linux network namespaces；BBR与CUBIC/Reno/Vegas/Illinois交互 | 不同瓶颈buffer下：约1.5 BDP以内BBR持续丢包并压制CUBIC；到约3 BDP两者接近公平；更大buffer时CUBIC份额增加。作者也指出改变两流共同RTT影响较小，固定一流50 ms并改变另一流时大buffer下RTT影响明显 | 公开PDF p.8 Fig. 10及正文；Mininet说明 p.13 |
| Cao et al. 2019 | Mininet：1 Gbps、20 ms RTT，buffer从10 KB到100 MB；另有100 Mbps、25 ms RTT、10 MB buffer的loss实验 | 与CUBIC共存时，100 KB buffer下BBR重传305,029、CUBIC 1,398；10 MB时BBR 204、CUBIC 794；loss实验中BBR在约20% loss附近goodput出现cliff；论文明确区分Mininet与WAN结果 | 作者PDF p.5 Table 1；p.4 Fig. 7/8及正文 |
| Ma et al. 2017 | 100 Mbps瓶颈、两流10 ms/50 ms RTT；另扫10 Mbps到1 Gbps带宽；改变竞争流数 | 50 ms流加入后10 ms流稳定goodput约6.3 Mbps；论文将偏差与较长RTT流的探测inflight和队列占用联系起来；还指出流数会改变长RTT优势 | arXiv HTML，Fig. 1及相关段落；全文字段仍需归档PDF页码 |
| Piotrowska 2024 | 多RTT、BBRv1/v2/v3、吞吐/丢包/公平性；公开页面摘要可见 | 摘要明确报告2×BDP缓冲时BBRv3保持稳定低队列；具体Jain值和50×BDP结果需PDF逐页核对 | MDPI/公开摘要；正式定量引用前待PDF核验 |

## 对正文的直接影响

1. Jaeger的公开全文支持“buffer depth、AQM和RTT组合影响公平性”，不支持把RTT恒等式单独写成带宽分配证明。
2. Cao的实验条件可用于说明 `suitable` 必须分吞吐、重传、队列和公平性；其Mininet与WAN结果不同，正文要保留平台边界。
3. Ma的10/50 ms、100 Mbps案例可作为RTT公平性机制证据，但应写成特定实验条件下的观测；其结果不能替代多版本、多个队列的独立验证。
4. Hock的高带宽实验不能直接作为本文100 Mbps候选实验的数值基准，只能用于跨研究条件比较。
