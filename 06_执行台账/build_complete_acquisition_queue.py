#!/usr/bin/env python3
"""Attach archived index locations to pending complete report groups.
Only discovery; no accessibility, identity or eligibility claims.
"""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    raw={}
    for path in (ROOT/'raw_search_20260928').glob('*.json'):
        source,qid=path.stem.split('_',1)
        data=json.loads(path.read_text())
        items=data.get('results',[]) if source=='openalex' else data.get('message',{}).get('items',[])
        for i,item in enumerate(items,1):raw[f'{source}_{qid}_{i:04d}']=item
    with (ROOT/'complete_eligibility_queue_20261012.csv').open() as f:groups=list(csv.DictReader(f))
    rows=[]
    for group in groups:
        if group['eligibility_status']!='pending':continue
        links=[]
        for rid in group['source_record_ids'].split(';'):
            item=raw.get(rid,{})
            locations=[item.get('best_oa_location') or {},item.get('primary_location') or {},*(item.get('locations') or [])]
            for loc in locations:
                links.extend(loc[k] for k in ['pdf_url','landing_page_url'] if loc.get(k))
            oa=item.get('open_access') or {}
            if oa.get('oa_url'):links.append(oa['oa_url'])
            if item.get('URL'):links.append(item['URL'])
        rows.append({'record_id':group['canonical_record_id'],'report_key':group['report_key'],'title':group['title'],'doi':group['doi'],'full_text_status':'pending_acquisition_or_review','fulltext_url_candidates':' | '.join(dict.fromkeys(links))})
    with (ROOT/'complete_acquisition_queue_20261012.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    print(json.dumps({'pending_report_groups':len(rows),'groups_with_archived_location':sum(bool(r['fulltext_url_candidates']) for r in rows),'scope':'Archived discovery links only; missing links are not exclusion evidence.'}))

if __name__=='__main__':main()
