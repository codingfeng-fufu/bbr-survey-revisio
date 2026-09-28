# F06 框架判定规则修改

日期：2026-09-28。候选文件：`cas-sc-template_F05_applied.tex`。

## 已写入

- 明确框架输入：瓶颈容量、参考RTT、绝对缓冲区、丢包来源、BBR版本、队列管理和流数。
- 明确异构流的BDP口径：报告参考RTT和每流RTT，不能只给一个无条件的BDP倍数。
- 将 `suitable` 拆成吞吐、时延、公平性和重传四个输出。
- 增加 `undetermined` 状态，避免输入缺失时强行给High/Medium/Low。
- 将缓冲区和BDP边界明确称为working bins，不再声称普适物理阈值。
- 将场景表改成条件性预期，减少把单篇研究的数字写成部署保证。
- 将“Independent Validation”改为external consistency check，并明确外部数据没有严格留出，因此不声称预测验证。

## 仍需后续处理

1. `Table 5`及其他场景表中的缓冲区边界还要逐处搜索并统一。
2. 旧的“High/Medium/Low suitability”列需要在正文和表格中增加具体指标解释，或改成条件性描述。
3. Framework rules中的数字型例子要逐一回溯证据来源，尤其是BBR/CUBIC吞吐倍数、Jain值和重传倍数。
4. 编译PDF后检查表格宽度和换行。
