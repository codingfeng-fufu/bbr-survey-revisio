#!/usr/bin/env python3
"""Join actual acquired PDFs to complete report groups without eligibility mutation."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def identity(doi,title):
    doi=re.sub(r'^https?://(?:dx\.)?doi\.org/','',doi.strip().lower())
    return 'doi:'+doi if doi else 'title:'+re.sub(r'[^a-z0-9]','',title.lower())

def main():
    log=json.loads((ROOT/'fulltext_acquisition_20261012/retrieval_log.json').read_text())
    acquired={}
    for record in log:
        if record.get('status')!='pdf_obtained':continue
        path=ROOT/record['file']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:
            raise ValueError('Acquired source missing/hash changed: '+str(path))
        acquired.setdefault(identity(record['doi'],record['title']),[]).append(record)
    with (ROOT/'complete_eligibility_queue_20261012.csv').open() as f:groups=list(csv.DictReader(f))
    rows=[]
    for group in groups:
        records=acquired.get(group['report_key'],[])
        rows.append({'report_key':group['report_key'],'title':group['title'],'eligibility_status':group['eligibility_status'],'inclusion_decision':group['inclusion_decision'],'acquired_file_count':len(records),'pdf_files':' | '.join(r['file'] for r in records),'retrieval_urls':' | '.join(r['url'] for r in records),'identity_review_states':' | '.join(r.get('title_identity_check','pending') for r in records),'note':'Acquisition does not change eligibility; source version and quantitative claims require separate review.'})
    with (ROOT/'complete_fulltext_access_map_20261012.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    print(json.dumps({'report_groups':len(rows),'groups_with_logged_pdf':sum(bool(r['acquired_file_count']) for r in rows),'logged_files_hash_verified':sum(len(v) for v in acquired.values()),'eligibility_mutated':False}))

if __name__=='__main__':main()
