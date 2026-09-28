import csv, json, re
from pathlib import Path

root = Path(__file__).parent
screen = list(csv.DictReader((root/'screening_human_round1_M04.csv').open(encoding='utf-8-sig')))
candidate = [r for r in screen if r['human_title_abstract_decision']=='include_title_abstract' and not r['duplicate_of']]
raw_dir = root/'raw_search_20260928'
openalex = {}
crossref = {}
for p in raw_dir.glob('openalex_*.json'):
    qid=p.stem.split('_',1)[1]
    data=json.loads(p.read_text(encoding='utf-8'))
    for i,item in enumerate(data.get('results',[]),1): openalex[f'openalex_{qid}_{i:04d}']=item
for p in raw_dir.glob('crossref_*.json'):
    qid=p.stem.split('_',1)[1]
    data=json.loads(p.read_text(encoding='utf-8'))
    for i,item in enumerate(data.get('message',{}).get('items',[]),1): crossref[f'crossref_{qid}_{i:04d}']=item
priority=re.compile(r'BBR(v[123])?|fair|RTT|buffer|ECN|loss|LEO|satellite|BDP[- ]?Veno|OVeno|Veno|CUBIC|wireless|WiFi|QUIC',re.I)
queue=[]
for row in candidate:
    item=openalex.get(row['record_id']) or crossref.get(row['record_id']) or {}
    loc=item.get('best_oa_location') or item.get('primary_location') or {}
    oa=item.get('open_access') or {}
    links=[]
    for key in ('pdf_url','landing_page_url','oa_url'):
        if loc.get(key): links.append(loc[key])
        if oa.get(key): links.append(oa[key])
    if item.get('URL'): links.append(item['URL'])
    links=list(dict.fromkeys(links))
    open_full=bool(loc.get('pdf_url') or oa.get('oa_url') or oa.get('any_repository_has_fulltext'))
    title=row['title']
    queue.append({**row,'priority_score':len(priority.findall(title)),'fulltext_access':'open_candidate' if open_full else 'doi_or_subscription',
        'fulltext_url_candidates':' | '.join(links),'full_text_status':'not_started','full_text_source':'','inclusion_decision':'pending_full_text',
        'report_id':'to_assign','study_id':'to_assign','evidence_location':'','reviewer':'Codex','review_date':''})
queue.sort(key=lambda r:(r['fulltext_access']!='open_candidate',-int(r['priority_score'])))
with (root/'fulltext_queue_M04.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(queue[0]));w.writeheader();w.writerows(queue)
summary={'candidate_unique_reports':len(queue),'open_candidate':sum(r['fulltext_access']=='open_candidate' for r in queue),
         'doi_or_subscription':sum(r['fulltext_access']=='doi_or_subscription' for r in queue),
         'full_text_reviews_completed':0,'final_included':0,
         'note':'Open candidate means an index exposes a possible open location; each PDF/landing page still needs manual verification.'}
(root/'fulltext_queue_M04_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
