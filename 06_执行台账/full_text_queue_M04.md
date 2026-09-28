# M04：全文审查队列说明

标题/摘要筛选已由 Codex 于 2026-09-28 完成，当前结果：

- 2,618 条检索记录完成标题/摘要判断；
- 572 条标题/摘要层面候选纳入；去除初步重复后为 400 条候选报告；
- 297 条标题/摘要层面排除；去除初步重复后为 236 条；
- 1,749 条需要全文或进一步判断；去除初步重复后为 1,384 条；
- 最终纳入仍为 0，因为全文审查尚未完成。

## 全文处理顺序

1. 先处理 `include_title_abstract` 中的400个唯一候选报告。
2. 优先顺序：BBR版本/机制、RTT公平性、缓冲区/ECN、BBRv3、多场景、LEO/无线、BDP-Veno/OVeno、AI公平性。
3. 每篇先保存PDF或合法全文入口，再填写全文字段；不可取得全文记为 `full_text_unavailable`，不能直接记为研究排除。
4. 全文排除必须填写一个主要理由；全文纳入必须填写研究ID、报告ID和至少一个证据定位。
5. 同一研究的预印本、会议版、期刊扩展版建立 `study_id` 关联，不重复计算研究数。

## 需要填写的全文字段

`report_id, study_id, full_text_status, inclusion_decision, exclusion_reason, protocol_version, scenario, bandwidth, RTT, buffer, queue_management, flow_count, loss_source, ECN, metrics, result_location, evidence_strength, limitations, reviewer, review_date`

当前文件 `screening_human_round1_M04.csv` 记录了标题/摘要决定、理由和重复关系。它是全文审查的输入，不能直接改写成最终165篇证据集。
