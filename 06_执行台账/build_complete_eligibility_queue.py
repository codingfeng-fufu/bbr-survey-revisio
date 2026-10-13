#!/usr/bin/env python3
"""Preserve all nonexcluded screening records as normalized report groups.
Does not change screening decisions or overwrite the historical 400-row queue.
"""
import collections
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def identity(row):
    doi=re.sub(r'^https?://(?:dx\.)?doi\.org/','',row['doi'].strip().lower())
    doi=re.sub(r'^doi:\s*','',doi)
    return 'doi:'+doi if doi else 'title:'+re.sub(r'[^a-z0-9]','',row['title'].lower())

def main():
    with (ROOT/'screening_human_round1_M04.csv').open(encoding='utf-8-sig') as f:
        source=list(csv.DictReader(f))
    with (ROOT/'fulltext_queue_M04.csv').open(encoding='utf-8-sig') as f:
        old=list(csv.DictReader(f))
    completed={}
    for r in old:
        if r['full_text_status']!='eligibility_review_completed':continue
        key=identity(r)
        if key in completed and completed[key]['inclusion_decision']!=r['inclusion_decision']:
            raise ValueError('Conflicting completed eligibility decisions for '+key)
        if r['inclusion_decision'] not in ('include','exclude'):
            raise ValueError('Completed eligibility requires an explicit include/exclude decision')
        for field in ('report_id','study_id','evidence_location','reviewer','review_date','full_text_source'):
            if not r.get(field) or r[field]=='to_assign':
                raise ValueError('Completed eligibility lacks '+field+' for '+key)
        evidence=Path(r['full_text_source'])
        if not evidence.is_absolute():evidence=ROOT.parent/evidence
        if not evidence.is_file():
            raise ValueError('Completed eligibility source file missing: '+str(evidence))
        completed[key]=r
    resolutions={}
    resolution_path=ROOT/'screening_conflict_resolutions_20261012.csv'
    if resolution_path.exists():
        with resolution_path.open() as f:
            resolutions={r['report_key']:r for r in csv.DictReader(f)}
    reassessments={}
    reassessment_path=ROOT/'title_abstract_reassessment_20261012.csv'
    if reassessment_path.exists():
        with reassessment_path.open() as f:reassessments={r['report_key']:r for r in csv.DictReader(f)}
    groups=collections.defaultdict(list)
    for row in source:
        groups[identity(row)].append(row)
    fields=['report_key','canonical_record_id','title','doi','source_record_ids','screening_decisions','requires_eligibility_review','decision_conflict','eligibility_status','inclusion_decision','verified_report_id','verified_study_id','screening_conflict_resolution']
    rows=[]
    for key,values in sorted(groups.items()):
        decisions=sorted({v['human_title_abstract_decision'] for v in values})
        needs=any(x!='exclude_title_abstract' for x in decisions)
        reassessment=reassessments.get(key,{})
        if reassessment.get('decision')=='retain_for_fulltext':needs=True
        elif reassessment.get('decision')=='exclude_title_abstract':needs=False
        done=completed.get(key)
        r=values[0]
        rows.append(dict(report_key=key,canonical_record_id=r['record_id'],title=r['title'],doi=r['doi'],source_record_ids=';'.join(v['record_id'] for v in values),screening_decisions=';'.join(decisions),requires_eligibility_review=needs,decision_conflict=len(decisions)>1,eligibility_status='completed' if done else 'pending' if needs else 'reviewed_title_abstract_excluded' if reassessment.get('decision')=='exclude_title_abstract' else 'pending_title_abstract_reassessment',inclusion_decision=done['inclusion_decision'] if done else '',verified_report_id=done['report_id'] if done else '',verified_study_id=done['study_id'] if done else '',screening_conflict_resolution=resolutions.get(key,{}).get('resolved_title_abstract_decision','')))
    with (ROOT/'complete_eligibility_queue_20261012.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    summary={'exported_records':len(source),'normalized_report_groups':len(rows),'requires_fulltext_groups':sum(r['requires_eligibility_review'] for r in rows),'reviewed_title_abstract_excluded_groups':sum(r['eligibility_status']=='reviewed_title_abstract_excluded' for r in rows),'automatically_excluded_groups_pending_reassessment':sum(r['eligibility_status']=='pending_title_abstract_reassessment' for r in rows),'conflicting_screening_groups':sum(r['decision_conflict'] for r in rows),'unresolved_screening_conflict_groups':sum(r['decision_conflict'] and not r['screening_conflict_resolution'] for r in rows),'completed_eligibility_groups':sum(r['eligibility_status']=='completed' for r in rows),'included_report_groups':sum(r['eligibility_status']=='completed' and r['inclusion_decision']=='include' for r in rows),'excluded_after_eligibility_groups':sum(r['eligibility_status']=='completed' and r['inclusion_decision']=='exclude' for r in rows),'pending_eligibility_groups':sum(r['eligibility_status']=='pending' for r in rows),'rule':'Any include or uncertain record keeps the report in eligibility review, even if another source record excludes it. Identity normalization is not study-level deduplication.'}
    (ROOT/'complete_eligibility_queue_20261012_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    authority={'authority':'complete_eligibility_queue_20261012.csv and summary',
               'status':summary,
               'note':'Completed report eligibility counts, not complete-corpus inclusion or independent-study counts.'}
    (ROOT/'fulltext_current_status_20261012.json').write_text(json.dumps(authority,ensure_ascii=False,indent=2)+'\n')
    status_text=f"""# 当前资格审查权威状态

使用 `python 06_执行台账/build_complete_eligibility_queue.py` 同时重建完整队列和本状态。历史9月快照不覆盖。

- 原始检索记录：{summary['exported_records']}。
- 规范化报告组：{summary['normalized_report_groups']}。
- 需要资格审查：{summary['requires_fulltext_groups']}。
- 已完成：{summary['completed_eligibility_groups']}（纳入{summary['included_report_groups']}，全文范围排除{summary['excluded_after_eligibility_groups']}）。
- 仍待全文资格核验：{summary['pending_eligibility_groups']}。
- 独立标题摘要复核后排除：{summary['reviewed_title_abstract_excluded_groups']}（不计作全文完成）。
- 另待独立标题摘要复核：{summary['automatically_excluded_groups_pending_reassessment']}（只有自动规则排除，不能签收）。
- 历史标题摘要冲突：{summary['conflicting_screening_groups']}组；未裁决的阶段冲突：{summary['unresolved_screening_conflict_groups']}组。阶段裁决不等于全文验收。

完成标记必须有明确include/exclude决定；生成器拒绝同一报告的已完成决定冲突。下载、首页身份和局部图表核验不计为资格完成。

本表不是独立研究数或完成的综述最终纳入数。M04仍开放；获取失败应保留原因，不能补造纳入。
"""
    (ROOT/'fulltext_current_status_20261012.md').write_text(status_text)
    tex=f"""% Generated from complete_eligibility_queue_20261012_summary.json.
% Report-level working status; not final corpus or independent study counts.
At this working-draft stage, {summary['requires_fulltext_groups']:,} report groups
enter eligibility review. Of these, {summary['completed_eligibility_groups']} groups
have completed full-text eligibility assessment ({summary['included_report_groups']}
retained and {summary['excluded_after_eligibility_groups']} excluded), while
{summary['pending_eligibility_groups']:,} remain pending. A further
{summary['reviewed_title_abstract_excluded_groups']} groups have documented
title/abstract-level exclusions. These counts describe reports, not
independent studies or a completed review corpus.
"""
    (ROOT.parent/'07_Overleaf修订候选/F22_screening_status_generated.tex').write_text(tex)
    print(json.dumps(summary))

if __name__=='__main__':main()
