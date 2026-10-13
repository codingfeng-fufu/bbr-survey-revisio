# 防御性写作逐处检查与改法

对象：当前修订稿正文及实际引用的实验/分析片段。这里只提供改法，不覆盖现有稿件和回复。

最强叙事：问题是高利用率掩盖带宽分配差异；缺口是跨条件比较缺乏统一、指标分开的口径；思路是明确路径/实现输入与服务要求；硬结果是E2总goodput 95.58–95.59 Mbps但BBR份额0.143–0.327，并以E3要求敏感性揭示goodput/公平性的权衡。

## 1. 摘要

原表达：conditions where queue conditioning performs worse. The results do not support a universal version ranking or suitability threshold.

问题：开场把评审风险和预测失利当主结论。

建议替换：The 340-run evaluation separates link utilization from bandwidth allocation: in BBR/CUBIC coexistence, total goodput remains at 95.58–95.59 Mbps while BBR shares span 0.143–0.327. Equal-RTT measurements further show how explicit goodput and fairness requirements lead to different deployment assessments.

处理边界：将回顾性设计和适用范围放到方法/限制；误差和基线仍在实验保留。

## 2. 摘要

原表达：document the experimental conditions and measurement limitations, and narrow conclusions

问题：摘要以“我们缩小了结论”描述修改过程，而非论文价值。

建议替换：The framework combines explicit path and implementation inputs with separate throughput, delay, fairness and retransmission requirements, giving readers a reproducible basis for interpreting BBR results.

处理边界：不要把修改动作写成学术贡献。

## 3. Highlights

原表达：Retrospective transfer tests report prediction errors and failure cases.

问题：亮点强调失败登记。

建议替换：Comparable utilization coexists with sharply different bandwidth shares.

处理边界：回顾性迁移检验仍在正文说明。

## 4. 1.2

原表达：rather than establishing that no prior work discusses a particular deployment issue

问题：替审稿人设想并反驳一个无关主张。

建议替换：Table 1 compares the scope and organizing approach of the reviewed studies.

处理边界：删除不必要的自辩。

## 5. 1.2

原表达：not a universal protocol ranking

问题：段末停在“做不到什么”。

建议替换：The framework connects each performance assessment to its path, implementation and workload conditions.

处理边界：并不恢复通用选型器主张。

## 6. 1.4

原表达：We do not claim that all scenario topics are absent from prior surveys.

问题：贡献段先撤回新颖性。

建议替换：Bringing these scenarios into a common assessment exposes which findings transfer across configurations and which require additional path or implementation information.

处理边界：明确贡献是综合视角，而非首次覆盖。

## 7. 1.4

原表达：not a new congestion-control algorithm

问题：向读者主动提出没有新算法。

建议替换：The analytical contribution is a requirement-dependent assessment that connects measured rates, share feasibility and observation windows.

处理边界：原公式来源继续引用；新算法问题在R3-3回复如实回答。

## 8. 1.4

原表达：exposes both agreement and failure of queue-only conditioning

问题：贡献段列分析成败过程。

建议替换：The controlled evaluation quantifies allocation across RTT and queue settings and tests the transfer of normalized performance estimates.

处理边界：详细胜负进入结果表。

## 9. 方法

原表达：rather than an invented database origin

问题：过度审计语言。

建议替换：The register records known acquisition routes and distinguishes exact DOI matches from title-based candidate matches.

处理边界：历史来源未知和未完成全文筛查必须在同节明确保留。

## 10. 方法

原表达：do not establish a performance guarantee

问题：把常规证据原则写成保证免责声明。

建议替换：Source assessments retain implementation, parameters and observation windows alongside each quantitative comparison.

处理边界：检索角色与排除计数不删除。

## 11. 2.1

原表达：filtering does not guarantee recovery

问题：保证型否定可以换成机制描述。

建议替换：Application limits, ACK timing, queueing and path changes affect the delivery-rate and minimum-RTT estimates.

处理边界：必要机制边界不丢失。

## 12. 2.1

原表达：It is not a general throughput bound for CUBIC

问题：必要纠错，但可用正面定义减少重复。

建议替换：The approximation applies to Reno-like steady-state behavior; CUBIC uses a different window-growth function.

处理边界：保留Reno-like适用范围。

## 13. 2.1

原表达：neither mechanism guarantees that a shallow queue will avoid overflow

问题：否定一个正文未承诺的保证。

建议替换：Queue overflow depends on the interaction between pacing, congestion-window limits and the available buffer.

处理边界：描述因果输入。

## 14. 2.2

原表达：a change in gain alone does not establish improved coexistence or reduced starvation

问题：机制参数段反复插入性能免责。

建议替换：The Down gain changes the drain phase; coexistence outcomes are evaluated through the per-flow measurements in Section 7.

处理边界：不要声称增益变化本身改善公平性。

## 15. 3.2–3.4

原表达：not universal physical thresholds

问题：同一限定多次重复，削弱主线。

建议替换：The buffer and BDP bins organize evidence; assessment uses the reported absolute values and implementation conditions.

处理边界：首次定义时保留一次“不构成通用阈值”。

## 16. 3.6

原表达：not an independent predictive validation

问题：必要标签多次出现。

建议替换：The Scholz measurements provide an external consistency comparison for the relationships among capacity, RTT, queue depth and allocation.

处理边界：在方法说明该材料参与了框架构建，不能改称独立验证。

## 17. 4.1

原表达：cannot establish a universal CUBIC ceiling of 15 Mbps

问题：重提已删除错误数字，像修订记录。

建议替换：WAN comparisons are interpreted jointly with receiver-window limits, RTT, loss and implementation.

处理边界：Mathis限定统一放在2.1。

## 18. 4.2

原表达：not establish a universal retransmission multiplier or a fixed suitability rating

问题：把证据价值藏在否定后。

建议替换：The queue sweeps connect buffer depth to measured flow shares and retransmission costs under each study’s configuration.

处理边界：不能补造未核实乘数。

## 19. 4.3

原表达：does not contradict potential benefits under different loss or delay conditions

问题：看到不占优结果就为BBR辩护。

建议替换：The high-capacity, low-delay hardware tests favor CUBIC throughput, whereas the loss and queue experiments examine different operating objectives. Together they distinguish raw transfer rate from congestion-response and sharing behavior.

处理边界：如实报告CUBIC更高；不能暗示它牺牲了未测量指标。

## 20. 4.4

原表达：do not establish a fixed BBRp-to-CUBIC throughput multiplier

问题：篇章结尾是不可推广免责声明。

建议替换：BBRp improves the observed throughput–latency tradeoff through pacing changes in the tested WLAN configuration.

处理边界：准确保留芯片、方向和队列配置。

## 21. 4.5

原表达：presence alone does not prove sub-RTT detection or one-RTT convergence

问题：可用机制表达替代防御句。

建议替换：After a capacity decrease, maximum-filter memory can retain earlier delivery-rate samples; assessment therefore includes recovery time and change frequency.

处理边界：不恢复一RTT保证。

## 22. 5

原表达：does not establish a universal ranking of versions or buffer sizes

问题：公平性观察后立即否定主张。

建议替换：The measured Jain values identify buffer-dependent differences among the tested versions and motivate an assessment that reports shares alongside aggregate goodput.

处理边界：报告拓扑及RTT范围。

## 23. 5.4

原表达：does not demonstrate that parameter optimization is saturated or that only two mitigation paths remain

问题：主动复述已撤回的极端结论。

建议替换：Estimator design, probing, loss responses and queue management offer complementary intervention points.

处理边界：直接删除旧极端命题。

## 24. 6.2

原表达：do not demonstrate an online BBRv3 controller or an advantage over BBR

问题：第三方AI研究段落按“证明不了”组织。

建议替换：TCP-Drinc provides evidence on learned window control and training-condition sensitivity; its comparison set and confidence intervals define the scope of those findings.

处理边界：明确BBR不在基线、区间重叠；不能宣称优势。

## 25. 6.2

原表达：Without measured timing, we do not infer that a method can or cannot operate

问题：元评论代替研究问题。

建议替换：Deployment evaluation pairs control accuracy with measured inference latency at the intended decision frequency.

处理边界：保留需测量运行时。

## 26. E1/E2

原表达：do not establish a universal version ranking or identify unmeasured internal state

问题：结果开头否定论文可达目标。

建议替换：Across implementations, aggregate goodput stays close to the bottleneck while RTT asymmetry changes flow allocation. E1 quantifies that allocation; E2 isolates the coexistence assessment under equal RTTs.

处理边界：“isolates”只指评估场景，不能暗示版本因果隔离。

## 27. E2

原表达：does not establish an intrinsic ordering of controller versions

问题：最强结果之后机械免责。

建议替换：The twelve conditions demonstrate a consistent distinction between utilization and coexistence fairness: total goodput spans 95.58–95.59 Mbps, while BBR shares span 0.143–0.327.

处理边界：内核差异在7.1统一报告，结果表保留环境身份。

## 28. E3

原表达：rather than universal version rankings

问题：E3论证职责不突出。

建议替换：E3 extends the rate/fairness assessment across two capacities and two RTTs. BBRv3 mean Jain values are 0.995–1.000, while CUBIC means are 0.917–0.987, alongside the reported aggregate rates.

处理边界：保留CUBIC更高goodput，不能以公平性数字掩盖。

## 29. 人工丢包

原表达：not evidence that loss improves performance

问题：必要排除因果误读，可压缩成正面结果。

建议替换：At configured 0.1% access-link loss, mean goodput remains near 94 Mbps for BBRv3 and changes from 95.58 to 81.06 Mbps for CUBIC.

处理边界：小幅BBRv3上升不解释为改善；统计显著性未知。

## 30. 7.5

原表达：rather than hiding it inside a scenario rating

问题：带指责感、内部审计语气。

建议替换：The transfer test explicitly assumes that the calibrated normalized metrics can transfer across capacity and RTT.

处理边界：设计假设须保留。

## 31. 7.5

原表达：performs worse than the constant baseline

问题：写成预测器败局；但事实不可改。

建议替换：For the corrected 50-Mbps cases, Jain MAE is 0.02027 for queue interpolation and 0.01444 for the constant estimate. This comparison identifies when additional conditioning variables are needed.

处理边界：两个误差均保留；不能说插值占优或归因于未经测试机制。

## 32. 7.5

原表达：does not establish a useful universal predictor

问题：把不属于本文任务的普适预测器设成比赛。

建议替换：The transfer comparison evaluates calibration dependence, while the assessment procedure uses measured rates and explicit service requirements for its decisions.

处理边界：回顾性设计保留；该检验不包装为预测验证成功。

## 33. 7.5

原表达：not a contradiction resolved by assigning one universal suitability label

问题：修辞性争辩。

建议替换：Changing the utilization requirement from 0.90 to 0.95 shifts joint pass counts from 40/40 to 0/40 for BBRv3, with CUBIC at 27/40; the assessment therefore makes the throughput–fairness preference explicit.

处理边界：阈值为事后示例必须明确。

## 34. 结论

原表达：rather than a universal version ranking or a proof of an unmeasured internal mechanism

问题：结论仍在反驳审稿意见。

建议替换：The controlled comparison shows why flow shares must accompany aggregate goodput in BBR assessment.

处理边界：范围在方法已有定义。

## 35. 结论

原表达：performs worse than a constant predictor

问题：结论强化的是次要分析负面结果。

建议替换：The analytical assessment connects measured utilization and allocation to explicit service requirements, making the resulting deployment tradeoffs reproducible.

处理边界：误差失败项留在7.5；不把预测器列作最强贡献。

## 36. 结论末段

原表达：These issues prevent a claim ... Full-text eligibility screening also remains incomplete.

问题：突然从科学记忆点切换到任务未完成清单。

建议替换：The main result is a metric-separated assessment: near-identical utilization can coexist with sharply different shares, and explicit rate/fairness requirements expose the tradeoffs that aggregate throughput conceals.

处理边界：完整方法限制集中在1.3/7.1与补充材料；结论可保留一句范围，不删披露。

## 实验的论证职责

| 实验 | 必须证明的事情 | 推荐写法 |
|---|---|---|
| E1 | RTT异构与队列条件改变观测份额，不能靠恒等式推份额 | 用份额0.769–0.969和Jain 0.532–0.776主导讨论 |
| E2 | 高利用率与公平分配是两个评价问题 | 95.58–95.59 Mbps对比份额0.143–0.327，作为摘要最硬结果 |
| E3 | 在容量/RTT变化下展示指标与服务要求的区别 | 同时报公平性、goodput以及两套要求下的通过比例 |
| 人工丢包 | 在声明的独立丢包设置下比较goodput保持情况 | 报两算法原始值，不夸大成无线/卫星泛化 |
| 迁移检验 | 检查基于队列条件的校准依赖，回应R2-2 | 降为校准诊断；保留误差、常数基线和回顾性性质 |
| 窗口敏感性 | 说明含预热结果对窗口口径有多敏感 | 放7.1/补充材料，避免反复在结果中插入 |

## 不应删除的科学限定

检索未完成、历史来源未知、主结果含预热、RTT与队列采样窗口、E3物理比值、内核差异、回顾性设计、基线误差及未测量指标均需准确报告。可以集中、缩短和定位，不能用“目标差异”替代实测结果或暗示未经验证的原因。纠正BDP推份额、无ECN等同v1和Mathis为CUBIC上限的否定句是必要机制结论，不是自动要删的防御句。

## 全文命中位置清单

下表完整登记相关否定/限制表达的源行，供逐处定位；关键词命中不等于防御性表达。统计定义、算法输出、历史方法披露和技术纠错应保留。

| 文件 | 行 | 命中表达 |
|---|---:|---|

| cas-sc-template.tex | 117 | conditions where queue conditioning performs worse. The results do not |

| cas-sc-template.tex | 120 | conditions and measurement limitations, and narrow conclusions about |

| cas-sc-template.tex | 130 | \item Retrospective transfer tests report prediction errors and failure cases. |

| cas-sc-template.tex | 159 | CUBIC has a different window evolution, so this approximation cannot serve |

| cas-sc-template.tex | 180 | operating point and does not determine bandwidth shares. ECN availability |

| cas-sc-template.tex | 181 | changes the feedback signals available to BBRv2/v3 but does not erase their |

| cas-sc-template.tex | 183 | illustrate conditional differences among versions rather than a universal |

| cas-sc-template.tex | 190 | reported for one configuration may not answer an operator's question about |

| cas-sc-template.tex | 220 | Table~\ref{tab:survey_compare} summarizes coverage rather than establishing |

| cas-sc-template.tex | 222 | supports metric-specific assessment, not a universal protocol ranking. |

| cas-sc-template.tex | 258 | approaches rather than BBR variants. Their shared use of BDP does not |

| cas-sc-template.tex | 260 | response, and we do not infer a performance ranking without matched |

| cas-sc-template.tex | 270 | was not retained. We do not reconstruct that chain from citation presence. |

| cas-sc-template.tex | 282 | capped exports. A title candidate does not confirm identity, and absence |

| cas-sc-template.tex | 283 | from a capped search does not establish irrelevance. Each legacy reference |

| cas-sc-template.tex | 284 | retains its known acquisition route rather than an invented database origin. |

| cas-sc-template.tex | 291 | These citation-level roles are not a systematic-review inclusion count.} |

| cas-sc-template.tex | 308 | Existing citation is not an eligibility criterion for the supplemental |

| cas-sc-template.tex | 316 | The search is a bounded supplement and does not establish exhaustive coverage. |

| cas-sc-template.tex | 325 | unassessed at full text. These report-level counts do not constitute a |

| cas-sc-template.tex | 337 | do not establish a performance guarantee. |

| cas-sc-template.tex | 406 | findings. Beyond data explicitly reported in the original papers, we do not |

| cas-sc-template.tex | 413 | information in relevant scenario analyses; for papers that do not report |

| cas-sc-template.tex | 461 | We do not claim that all scenario topics are absent from prior surveys. |

| cas-sc-template.tex | 467 | explicit requirement-dependent outputs including undetermined cases. |

| cas-sc-template.tex | 470 | service requirements, not a new congestion-control algorithm. |

| cas-sc-template.tex | 477 | constant baseline exposes both agreement and failure of queue-only |

| cas-sc-template.tex | 498 | network model on which its design rests---BBR's advantages and limitations both |

| cas-sc-template.tex | 508 | changes; filtering does not guarantee recovery of the true path capacity |

| cas-sc-template.tex | 510 | against the particular version and implementation rather than transferred |

| cas-sc-template.tex | 531 | approximation describes a restricted steady-state regime and does not |

| cas-sc-template.tex | 532 | account for all timeout, receiver-window or application limitations. |

| cas-sc-template.tex | 533 | It is not a general throughput bound for CUBIC, whose window evolution |

| cas-sc-template.tex | 535 | jointly; it does not predict a universal BBR/CUBIC throughput ratio. |

| cas-sc-template.tex | 558 | queue-inflated RTT sample~\citep{cardwell2017bbr}. These modes do not all |

| cas-sc-template.tex | 559 | recur periodically, and ProbeRTT does not guarantee a queue-free sample. |

| cas-sc-template.tex | 562 | configuration; support for an ECN mechanism does not prove that it was |

| cas-sc-template.tex | 568 | \caption{Simplified BBRv1 measurement and control architecture. Delivery-rate and RTT samples inform pacing and congestion-window targets. ProbeRTT entry depends on freshness and state conditions, rather than a fixed periodic timeout. Later-version ECN-bound mechanisms are not part of this BBRv1 diagram. The original figure was generated with GPT Image 2.0 and manually checked by the authors; this replacement was drawn with Python/matplotlib using AI-assisted code preparation.} |

| cas-sc-template.tex | 586 | across non-application-limited packet-timed rounds. Later versions add |

| cas-sc-template.tex | 593 | cannot be reduced to an unconditional packet-count trigger or a claim of |

| cas-sc-template.tex | 603 | 0.9 description, and a change in gain alone does not establish improved |

| cas-sc-template.tex | 608 | state conditions; a filter window is not an unconditional periodic timer. |

| cas-sc-template.tex | 611 | subject to the minimum congestion window. These parameters do not by |

| cas-sc-template.tex | 628 | \caption{Version-specific mechanisms and comparison conditions. The overview does not imply monotonic improvement in throughput, delay or fairness; source-specific parameters are reported in Table~\ref{tab:versions}. The original figure was generated with GPT Image 2.0 and manually checked by the authors; this replacement was drawn with Python/matplotlib using AI-assisted code preparation.} |

| cas-sc-template.tex | 670 | of ECN alone therefore does not imply reversion to BBRv1; parameter values and |

| cas-sc-template.tex | 687 | metric-specific assessment requirements. It does not predict bandwidth |

| cas-sc-template.tex | 694 | performance metric cannot effectively predict its behavior in unknown environments. |

| cas-sc-template.tex | 712 | is an analysis dimension rather than a universal physical boundary. The theoretical |

| cas-sc-template.tex | 727 | approximation in Eq.~(\ref{eq:mathis}) therefore does not establish a BDP-only |

| cas-sc-template.tex | 731 | packet loss alone does not identify its cause. BBRv1 primarily regulates |

| cas-sc-template.tex | 739 | do not establish that all BBR versions ignore loss or that parameter and |

| cas-sc-template.tex | 740 | queue-management changes cannot improve a particular configuration. |

| cas-sc-template.tex | 744 | theoretical reasoning, rather than universal cutoffs. The buffer-depth bins |

| cas-sc-template.tex | 782 | The framework is used as a conditional screening procedure rather than an |

| cas-sc-template.tex | 788 | or insufficient evidence produces ``undetermined'' rather than a forced rating. |

| cas-sc-template.tex | 828 | 802.11 frame aggregation is a protocol-layer constraint that cannot be mapped to the |

| cas-sc-template.tex | 841 | This is a qualitative consistency check, not an independent predictive |

| cas-sc-template.tex | 848 | and changing capacity and RTT can alter the comparison. We do not require |

| cas-sc-template.tex | 855 | together. This provides an external consistency comparison, not a held-out |

| cas-sc-template.tex | 886 | receiver-window limits and implementation, rather than BDP alone. |

| cas-sc-template.tex | 889 | host conditions; Eq.~(\ref{eq:mathis}) cannot establish a universal CUBIC |

| cas-sc-template.tex | 895 | limited, BBR's algorithmic advantage is masked by the receiver bottleneck and |

| cas-sc-template.tex | 903 | kilobytes cannot be compared across studies without those conditions. |

| cas-sc-template.tex | 911 | not establish a universal retransmission multiplier or a fixed suitability |

| cas-sc-template.tex | 920 | source-specific loss sweep does not establish that BBR is generally |

| cas-sc-template.tex | 938 | 1\%; this does not imply full throughput at 1\% loss. These approximate |

| cas-sc-template.tex | 939 | source-reported values describe that configuration rather than universal |

| cas-sc-template.tex | 947 | high-capacity, low-delay setup and does not contradict potential benefits |

| cas-sc-template.tex | 954 | comparison does not isolate the effect of CoDel alone or establish |

| cas-sc-template.tex | 960 | reported in one experiment is not a universal suitability zone, and a BDP |

| cas-sc-template.tex | 961 | identity does not prove that AQM cannot improve the observed RTT fairness. |

| cas-sc-template.tex | 992 | queue policy and TSQ configuration; they do not establish a fixed |

| cas-sc-template.tex | 1003 | rather than inferred from a static buffer category. A maximum delivery-rate |

| cas-sc-template.tex | 1005 | presence alone does not prove sub-RTT detection or one-RTT convergence. |

| cas-sc-template.tex | 1007 | rather than an unconditional ten-second schedule. For this scenario, |

| cas-sc-template.tex | 1009 | inputs; the framework does not assign a validated ``medium'' rating. |

| cas-sc-template.tex | 1016 | particular direction and observation period, rather than assigned a fixed |

| cas-sc-template.tex | 1025 | reported improvement in one setup is not a deployment guarantee for another. |

| cas-sc-template.tex | 1028 | missing, the BDP classification and suitability remain undetermined. |

| cas-sc-template.tex | 1075 | simulation's topology and RTT distribution. This finding does not establish a |

| cas-sc-template.tex | 1078 | in-flight amount associated with a measured operating point, but does not by |

| cas-sc-template.tex | 1138 | conditions, but the equation alone is not a proof of inevitable long-RTT |

| cas-sc-template.tex | 1157 | limitation, not a universal claim that one version always dominates another. |

| cas-sc-template.tex | 1211 | buffer effect. They do not establish a universal 1.5- or 3-BDP threshold |

| cas-sc-template.tex | 1240 | and network conditions. Equation~\ref{eq:bdp} alone does not establish an |

| cas-sc-template.tex | 1251 | throughput---complementary to, rather than a replacement for, end-side algorithm |

| cas-sc-template.tex | 1255 | and reported fairness limitations. It does not demonstrate that parameter |

| cas-sc-template.tex | 1282 | Reported fairness limitations require their tested implementation and queue conditions \\ |

| cas-sc-template.tex | 1300 | explicit conditions; the surveyed observations do not prove that all |

| cas-sc-template.tex | 1321 | measured; absence of ECN does not establish reversion to BBRv1 or a fixed |

| cas-sc-template.tex | 1332 | Bandwidth fairness alone does not establish latency or reliability guarantees |

| cas-sc-template.tex | 1335 | a bulk two-flow result does not supply those guarantees. |

| cas-sc-template.tex | 1345 | and the table alone does not establish statistically superior fairness. |

| cas-sc-template.tex | 1348 | inference cost; they do not demonstrate an online BBRv3 controller or |

| cas-sc-template.tex | 1391 | fixed heuristics and broader policy changes; the BDP identity does not |

| cas-sc-template.tex | 1392 | prove that such learning cannot improve a measured fairness outcome. |

| cas-sc-template.tex | 1400 | \citep{bernardez2025graphcc,huang2024llm}. Without measured timing, we do not |

| cas-sc-template.tex | 1401 | infer that a method can or cannot operate within a sub-RTT control loop. |

| cas-sc-template.tex | 1409 | baseline intervals overlap and its evaluation does not include BBR. |

| cas-sc-template.tex | 1417 | justifies deployment. Third, an evaluation in ns-3 or Mininet is limited |

| cas-sc-template.tex | 1425 | not a proof of a universal ceiling on learning-assisted control. |

| cas-sc-template.tex | 1431 | without excluding other designs. The near-term path is a ``model-driven + limited data-driven'' hybrid |

| cas-sc-template.tex | 1437 | and improves fairness must be evaluated; L4S support alone does not |

| cas-sc-template.tex | 1440 | not alternatives. |

| cas-sc-template.tex | 1454 | categories. The working bins summarize available evidence; they do not |

| cas-sc-template.tex | 1459 | in-flight operating point but does not determine the division of bandwidth |

| cas-sc-template.tex | 1462 | comparison supports condition-specific observations rather than a universal |

| cas-sc-template.tex | 1469 | performs worse than a constant predictor. |

| cas-sc-template.tex | 1472 | measurement limitations: full-run averages differ from the planned post-warmup |

| cas-sc-template.tex | 1473 | window, queue snapshots do not cover complete transfers, and some frozen E3 |

| cas-sc-template.tex | 1474 | queue labels do not match the physical reference BDP. These issues prevent a |

| F13_E3_results_candidate.tex | 8 | are retained; the affected cases do not validate the intended buffer bins. We ran two BBRv3 flows |

| F13_E3_results_candidate.tex | 13 | The values are condition-specific observations rather than universal |

| F13_E3_results_candidate.tex | 15 | RTT cases, while CUBIC showed more variation. The queue snapshots do not cover the complete measurement window; |

| F13_E3_results_candidate.tex | 16 | this experiment therefore does not establish full-run bottleneck |

| F13_E3_results_candidate.tex | 18 | separately and do not substitute for complete bottleneck loss accounting. |

| F13_E3_results_candidate.tex | 21 | the table does not report warmup-excluded steady-state estimates. |

| F15_cross_version_results_candidate.tex | 6 | conditional comparison over the tested matrix; they do not establish a |

| F15_cross_version_results_candidate.tex | 23 | Table~\ref{tab:e2_results} shows that similar total goodput does not imply |

| F15_cross_version_results_candidate.tex | 28 | is restricted to the tested no-ECN environments and does not establish |

| F15_cross_version_results_candidate.tex | 37 | than infer it from the in-flight identity; they do not show that the RTT |

| F20_controlled_experiments_candidate.tex | 10 | framework's assessment dimensions under stated conditions, rather than |

| F20_controlled_experiments_candidate.tex | 48 | these run-level quantities, rather than values calculated from mean rates. |

| F20_controlled_experiments_candidate.tex | 56 | analysis does not exclude it. A separate sensitivity analysis uses |

| F20_controlled_experiments_candidate.tex | 61 | respectively. These are sensitivity results rather than revised |

| F20_controlled_experiments_candidate.tex | 66 | They therefore do not share the goodput observation window, and a zero |

| F20_controlled_experiments_candidate.tex | 67 | counter in a saved snapshot does not establish zero drops over 180 s. |

| F20_controlled_experiments_candidate.tex | 68 | The experiment records cannot reconstruct the missing end-of-run |

| F20_controlled_experiments_candidate.tex | 74 | \subsection{Artificial loss and experimental limitations} |

| F20_controlled_experiments_candidate.tex | 83 | seed was not exposed in the retained configuration; this setup does not |

| F20_controlled_experiments_candidate.tex | 90 | rather than as a validation of the original buffer-category predictions. |

| F20_controlled_experiments_candidate.tex | 92 | conditions; they do not establish universal suitability thresholds or |

| F24_analytical_assessment.tex | 11 | analysis shows why they cannot determine bandwidth allocation by themselves. |

| F24_analytical_assessment.tex | 19 | a longer propagation RTT does not algebraically force a larger share. |

| F24_analytical_assessment.tex | 20 | This is an identifiability result about the equations, not a claim that all |

| F24_analytical_assessment.tex | 50 | \emph{does not meet}, or \emph{undetermined}. A missing or incompatible |

| F24_analytical_assessment.tex | 51 | measurement window yields \emph{undetermined}, rather than an inferred pass. |

| F24_analytical_assessment.tex | 53 | meets its own limit. An observed violation yields a failure for that |

| F24_analytical_assessment.tex | 55 | missing, the joint result remains undetermined. A zero-goodput run has $u=0$ and undefined Jain fairness; it cannot pass |

| F24_analytical_assessment.tex | 69 | within each run. In general, substituting an averaged share does not recover |

| F24_analytical_assessment.tex | 70 | the mean Jain index. Queue bins and BDP bins do not set $u_0,j_0,D_0,H_0$: |

| F24_analytical_assessment.tex | 73 | and its transfer limitations using the archived measurements. |

| F25_framework_transfer.tex | 8 | retrospective and is not a preregistered or untouched validation dataset. |

| F25_framework_transfer.tex | 10 | comparison, including conditions where queue conditioning performs worse. |

| F25_framework_transfer.tex | 19 | RTT effects cannot be estimated from this single-capacity, equal-RTT |

| F25_framework_transfer.tex | 21 | simplifying assumption, rather than hiding it inside a scenario rating. |

| F25_framework_transfer.tex | 55 | corrected 50-Mbps cases, queue-conditioned Jain prediction performs worse |

| F25_framework_transfer.tex | 56 | than the constant baseline. Queue conditioning alone therefore does not |

| F25_framework_transfer.tex | 68 | to equal-RTT same-algorithm competition; it does not establish BBR/CUBIC |

| F25_framework_transfer.tex | 70 | run-level decisions and a threshold sensitivity grid. Delay suitability remains undetermined because the receiver-goodput and |

| F25_framework_transfer.tex | 71 | early-ping windows do not align. Sender retransmission totals are supplied |

| F25_framework_transfer.tex | 72 | separately, but queue snapshots cannot attribute all retransmissions to |

| F25_framework_transfer.tex | 97 | throughput--allocation tradeoff under equal RTTs, not a contradiction |

| F25_framework_transfer.tex | 103 | numerical acceptance margins, and request medians rather than the reported |

| F25_framework_transfer.tex | 105 | We therefore do not convert that historical prediction sheet into a formal |
