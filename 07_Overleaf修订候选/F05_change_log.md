# F05 已应用修改

日期：2026-09-28。候选源文件：`cas-sc-template_F05_applied.tex`。

## 已写入的修改

- Table 3：ProbeRTT目标改为 `max(4 MSS, BDP/2)`；`cwnd_gain`改为状态相关；无ECN表注改为保留loss-driven更新和状态逻辑，删除“退化为BBRv1”。
- Abstract：删除未经来源回溯的 `Jain=0.71/0.78、50×BDP` 数字，改为条件化的多RTT公平性结论。
- Section 3：把缓冲区和BDP区间称为working bins，不再声称普适物理边界；补充版本、队列管理和流数依赖。
- Section 5/公平性：明确 `BDP=BtlBw×RTprop` 不能单独决定带宽份额；补充探测动态、队列、AQM、版本和流数条件；移除“geometric fact, not a bug”等修辞。
- RTT公平性图注：从“长RTT必然获得更多份额”改为特定版本、队列和流条件下的观测关系。
- Piotrowska结果：只保留已核实的多RTT和BBRv3 Jain序列，明确其为单篇仿真研究的条件化结果。

## 未做的事情

- 没有修改Overleaf项目。
- 没有修改 `refs.bib`。
- 没有删除原始稿；修订前备份为 `cas-sc-template_preF05_20260928.tex`。
- 没有编译PDF；本机没有检测到 `pdflatex`/`latexmk`。

## 合入前检查

1. 将候选文件与Overleaf主版本比较，确认其他作者最近修改没有被覆盖。
2. 编译并检查Table 3、Figure 2、Figure 5/6及摘要分页。
3. 回溯原稿中 `0.71/0.78/50×BDP` 的真正来源；若来源不是Piotrowska，再决定是否恢复带正确引用的数字。
4. 由冯宗林确认后，才把候选稿合入Overleaf主版本。
