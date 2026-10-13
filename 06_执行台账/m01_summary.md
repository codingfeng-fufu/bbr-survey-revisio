# M01：原稿引用与参考文献基线审计

- LaTeX入口：`D:\BBRComputerNetworks\cas-sc-template.tex`
- refs.bib：`D:\BBRComputerNetworks\refs.bib`
- BibTeX条目数：165
- 正文实际引用key数：165
- BibTeX中未在正文引用：0
- 正文引用但BibTeX缺失：0

这份表只证明当前正文与refs.bib的静态对应关系，不能证明165篇文献的历史检索、去重或筛选过程。检索来源、筛选状态和study_id仍需通过M02–M04补齐。

下一步：人工检查缺失key和未引用条目，建立原始检索记录映射，在检索协议冻结后补充检索日志与筛选记录。

## 当前项目复核入口

旧build_m01_audit.py保留历史Windows路径及产物。当前可使用独立脚本：

```bash
python 06_执行台账/audit_current_references.py --tex /实际项目/main.tex --bib /实际项目/refs.bib --output-dir /新建或空审计目录
```

新脚本递归读取input/include、检查缺key/重复key并保存输入哈希；缺少真实文件会拒绝生成验收结果。当前候选refs.bib缺失，实际执行返回2，没有生成假的通过记录。它只做静态key检查，不替代BibTeX语法、完整编译或全文筛选。

当前引用审计器已用临时合成项目验证：递归input中的真实引用会计入，带可选参数的citep可识别，注释中的假引用不计；缺失key及重复BibTeX key会返回失败。合成输入不作为本论文参考文献证据，实际refs.bib仍缺失。
