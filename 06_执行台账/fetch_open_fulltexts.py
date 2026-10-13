#!/usr/bin/env python3
"""Fetch indexed public PDF links; acquisition is not eligibility acceptance."""
import argparse
import concurrent.futures
import csv
import datetime
import hashlib
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'fulltext_acquisition_20261012'


def canonical(doi):
    return re.sub(r'^https?://(?:dx\.)?doi\.org/','',doi.strip().lower())


def fetch(item):
    record_id,url,doi,title=item
    record={'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_id':record_id,'url':url,'doi':doi,'title':title,'eligibility':'not_reviewed'}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (academic source verification)'})
        deadline=time.monotonic()+45
        chunks=[]
        size=0
        with urllib.request.urlopen(request,timeout=10) as response:
            record['final_url']=response.url
            while True:
                if time.monotonic()>deadline:raise TimeoutError('Total acquisition deadline exceeded')
                chunk=response.read1(65536)
                if not chunk:break
                size+=len(chunk)
                if size>25*1024*1024:raise ValueError('Exceeds25MiB acquisition limit')
                chunks.append(chunk)
        data=b''.join(chunks)
        if len(data)>25*1024*1024:raise ValueError('Exceeds 25 MiB acquisition limit')
        if not data.startswith(b'%PDF'):raise ValueError('Response is not a PDF; no fulltext accepted')
        digest=hashlib.sha256(data).hexdigest()
        path=OUT/(record_id+'.pdf')
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            path=OUT/(record_id+'_'+digest[:12]+'.pdf')
        path.write_bytes(data)
        record.update(status='pdf_obtained',file=str(path.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        diagnostic=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,timeout=15)
        record['pdfinfo_returncode']=diagnostic.returncode
        record['pdfinfo_stderr']=diagnostic.stderr
        if diagnostic.returncode!=0:
            record['status']='pdf_parse_failed'
        else:
            text_path=path.with_suffix('.txt')
            extraction=subprocess.run(['pdftotext','-layout',str(path),str(text_path)],capture_output=True,text=True,timeout=30)
            record['text_extraction_returncode']=extraction.returncode
            record['text_extraction_stderr']=extraction.stderr
            if extraction.returncode==0:record['text_file']=str(text_path.relative_to(ROOT))

    except Exception as exc:record.update(status='not_obtained',error=str(exc))
    return record


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=12);args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    log=OUT/'retrieval_log.json'
    prior=json.loads(log.read_text()) if log.exists() else []
    seen_urls={r['url'] for r in prior}
    seen_dois=set()
    for record in prior:
        if record.get('status')=='pdf_obtained':
            doi=canonical(record['doi'])
            seen_dois.add('doi:'+doi if doi else 'title:'+re.sub(r'[^a-z0-9]','',record['title'].lower()))
    jobs=[]
    with (ROOT/'complete_acquisition_queue_20261012.csv').open(encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            doi=canonical(row['doi'])
            report_key='doi:'+doi if doi else 'title:'+re.sub(r'[^a-z0-9]','',row['title'].lower())
            if report_key in seen_dois or row['full_text_status'].startswith(('obtained','eligibility_review')):continue
            for url in row['fulltext_url_candidates'].split(' | '):
                if not url.startswith(('https://','http://')) or url in seen_urls:continue
                location=urlsplit(url)
                if not ('.pdf' in location.path.lower() or location.path.lower().endswith('/pdf') or 'type=printable' in location.query.lower()):continue
                # Use the publisher's public static PDF domain for MDPI article paths.
                parsed=urlsplit(url)
                match=re.fullmatch(r'/(\d{4}-\d{4})/(\d+)/(\d+)/(\d+)/pdf',parsed.path)
                journal={'2076-3417':'applsci','2079-9292':'electronics','1424-8220':'sensors','1999-5903':'futureinternet'}.get(match.group(1)) if match else None
                if journal:
                    _,volume,issue,article=match.groups();url=f'https://mdpi-res.com/d_attachment/{journal}/{journal}-{int(volume):02d}-{int(article):05d}/article_deploy/{journal}-{int(volume):02d}-{int(article):05d}.pdf'
                if url in seen_urls:continue
                jobs.append((row['record_id'],url,doi,row['title']));seen_dois.add(report_key);break
            if len(jobs)>=args.limit:break
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(fetch,job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            temporary=log.with_suffix('.json.tmp')
            temporary.write_text(json.dumps(prior+results,ensure_ascii=False,indent=2)+'\n')
            temporary.replace(log)
    print(json.dumps({'attempted':len(results),'obtained':sum(r['status']=='pdf_obtained' for r in results),'results':results},ensure_ascii=False))

if __name__=='__main__':main()
