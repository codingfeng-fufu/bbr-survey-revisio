import csv, re
from pathlib import Path

tex = Path(r'D:\BBRComputerNetworks\cas-sc-template.tex')
bib = Path(r'D:\BBRComputerNetworks\refs.bib')
out = Path(__file__).parent
text = tex.read_text(encoding='utf-8')
bib_text = bib.read_text(encoding='utf-8')
keys = set()
for group in re.findall(r'\\cite(?:p|t|alt)?\{([^}]+)\}', text):
    keys.update(k.strip() for k in group.split(',') if k.strip())
bib_keys = set(re.findall(r'^\s*@\w+\{\s*([^,\s]+)', bib_text, re.M))
rows = []
for key in sorted(bib_keys | keys):
    hits = len(re.findall(r'\\cite(?:p|t|alt)?\{[^}]*\b' + re.escape(key) + r'\b[^}]*\}', text))
    rows.append({'citation_key': key, 'in_bib': 'yes' if key in bib_keys else 'no',
        'cited_in_main_text': 'yes' if key in keys else 'no', 'citation_occurrences': hits,
        'original_search_record': 'unknown',
        'screening_status': 'broken_reference' if key in keys-bib_keys else 'unknown',
        'study_id': 'to_assign',
        'notes': 'M01 audit; do not infer historical search provenance from citation presence'})
with (out / 'baseline_references_M01.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(out / 'm01_summary.md').write_text(
    '# M01：原稿引用与参考文献基线审计\n\n'
    f'- LaTeX入口：`{tex}`\n- refs.bib：`{bib}`\n'
    f'- BibTeX条目数：{len(bib_keys)}\n- 正文实际引用key数：{len(keys)}\n'
    f'- BibTeX中未在正文引用：{len(bib_keys - keys)}\n'
    f'- 正文引用但BibTeX缺失：{len(keys - bib_keys)}\n\n'
    '这份表只证明当前正文与refs.bib的静态对应关系，不能证明165篇文献的历史检索、去重或筛选过程。检索来源、筛选状态和study_id仍需通过M02–M04补齐。\n\n'
    '下一步：人工检查缺失key和未引用条目，建立原始检索记录映射，在检索协议冻结后补充检索日志与筛选记录。\n', encoding='utf-8')
print(f'bib={len(bib_keys)} cited={len(keys)} missing={len(keys-bib_keys)} unused={len(bib_keys-keys)}')
