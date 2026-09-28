# M02：BBR系统综述检索与筛选协议草案

状态：DRAFT，等待冯宗林确认后冻结。此文件是检索方案，不是已经执行的检索记录。

## 1. 研究问题

本轮检索服务于以下问题：

1. BBRv1、BBRv2、BBRv3的测量模型、控制机制和版本演进是什么？
2. RTT、BDP、缓冲区、丢包来源、队列管理和流数量如何影响BBR适用性与公平性？
3. BBR在有线、无线、蜂窝、卫星/LEO、QUIC及跨协议共存中的证据是什么？
4. BDP-Veno、OVeno等相关BDP型TCP与BBR有哪些可比较的设计和证据？
5. AI/学习辅助拥塞控制研究是否同时评估吞吐、时延、公平性和差异化服务？

## 2. 检索来源（待确认可访问性）

| 来源 | 用途 | 正式记录要求 |
|---|---|---|
| Scopus | 跨学科主检索 | 数据库版本/入口、完整表达式、检索日期、显示数、导出数 |
| Web of Science Core Collection | 交叉覆盖与引文追踪 | 同上 |
| IEEE Xplore | 网络与传输系统文献 | 同上 |
| ACM Digital Library | 计算机网络与系统会议/期刊 | 同上 |
| Google Scholar | 补充检索与引用追踪，不与数据库计数混合 | 精确查询、日期、筛选规则、保留记录 |
| RFC / IETF / Google BBR源码与技术资料 | 协议规范和实现证据，不作为普通数据库记录 | URL、版本/提交号、访问日期 |

正式执行前先确认作者实际拥有的数据库访问权限。没有访问权限的来源不能写成已检索；可以登记为计划来源或用可访问来源替代，并记录变化。

## 3. 分组检索概念

以下是概念块，不能直接当成所有数据库的最终语法。每个平台要保存实际执行的字段语法。

| 组 | 主题 | 候选词 |
|---|---|---|
| Q1 | BBR与版本 | `BBR`, `Bottleneck Bandwidth and Round-trip propagation time`, `BBRv1`, `BBRv2`, `BBRv3` |
| Q2 | 公平性与竞争 | `fairness`, `RTT fairness`, `RTT bias`, `CUBIC`, `coexistence`, `intra-protocol`, `inter-protocol` |
| Q3 | 缓冲区与丢包 | `buffer`, `bufferbloat`, `queue`, `BDP`, `random loss`, `ECN`, `AQM`, `CoDel`, `PIE` |
| Q4 | 网络场景 | `wireless`, `cellular`, `5G`, `satellite`, `LEO`, `QUIC`, `Wi-Fi`, `long fat network` |
| Q5 | 相关BDP型TCP | `BDP-Veno`, `BDP Veno`, `OVeno`, `O-Veno`, `bandwidth delay product TCP` |
| Q6 | AI辅助控制 | `congestion control` AND (`learning`, `reinforcement learning`, `machine learning`, `neural`) |

最低执行集合：Q1与Q2–Q4组合；Q5单独执行；Q6单独执行。每个数据库保存拆分前的完整表达式和实际运行版本，不能只保留概念词表。

## 4. 时间范围与记录单位

候选时间范围：数据库检索截至2026-09-28，覆盖数据库可追溯的最早日期至检索日；协议规范和源码资料单独记录版本/访问日期。若作者决定使用不同截止日，修改本文件版本号。

记录单位分开保存：

- `record_id`：数据库导出的单条记录；用于去重和筛选。
- `report_id`：一篇论文、报告、RFC或源码资料的具体报告。
- `study_id`：同一研究可能产生的多份报告集合。

“165篇正文引用”不是检索终点或纳入目标，也不能作为纳入标准。

## 5. 纳入标准

记录至少满足一个研究问题，并属于以下类型之一：

1. BBR版本机制、实现或协议规范的原始资料；
2. 报告BBR性能、公平性、时延、重传、缓冲区、丢包、ECN或场景行为的测量/仿真/分析研究；
3. 对BBR或相关拥塞控制进行系统综述、比较或理论分析的研究；
4. BDP-Veno、OVeno或其他明确相关的BDP型TCP研究，用于R3-2的比较背景；
5. AI/学习辅助拥塞控制研究，且能支持本文对目标函数、服务差异、公平性或实验限制的陈述；
6. 支撑网络模型、队列、AQM、BDP或可复现实验方法的规范和基础资料。

正文、官方技术资料或足以判定研究内容的公开版本必须可取得；只有摘要的记录可以作为候选或背景线索，不能直接承担定量结论。

## 6. 排除标准

排除时记录一个主要理由：

- 与研究问题无关；
- 不是网络拥塞控制/相关BDP型TCP研究；
- 重复报告（保留其与study_id的映射）；
- 只有摘要且无法取得正文，无法完成必要判断；
- 纯产品宣传或无法核查的方法/来源；
- 不属于本文所需的AI/服务/公平性证据范围；
- 语言或文献类型不符合冻结协议（必须在协议中提前写明）。

“正文中已经引用”不能作为纳入或排除理由。“缺少某个参数”通常不是全文排除理由；应在证据矩阵中标NR，并限制该来源可支持的主张范围。

## 7. 必须保存的检索日志字段

`search_id, source, platform_version, query_group, exact_query, fields, date_from, date_to, search_datetime, displayed_hits, exported_records, export_filename, access_limit, operator, notes`

导出文件必须保留原始版本。改写检索式时新建`search_id`，不覆盖旧日志。

## 8. 筛选流程

1. 导入所有原始导出，分配record_id。
2. 依据预定规则去重，保存原record_id到保留record_id的映射。
3. 标题/摘要筛选，记录纳入、排除或不确定。
4. 获取全文；未取得全文单独标记，不能记为全文排除。
5. 全文筛选，记录一个主要排除理由和执行人/日期。
6. 建立report_id与study_id关系，避免同一研究多报告重复计数。
7. 抽查纳入与排除记录；冯宗林处理争议案例并留下裁定原因。

## 9. 冻结条件

冯宗林确认以下内容后，将文件复制为`search_protocol_M02_v1_FROZEN.md`并开始正式检索：来源可访问性、最终时间范围、实际数据库语法、纳入/排除标准、筛选记录单位和争议处理方式。冻结后只能创建v2并说明原因，不能覆盖v1。

