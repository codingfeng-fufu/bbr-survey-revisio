"""Retrospective reference identity/role register, not historical screening reconstruction."""
from pathlib import Path
import re,csv,json,collections,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
ORIG=ROOT/'08_大修交付/original_overleaf/refs.bib';QUEUE=ROOT/'06_执行台账/complete_eligibility_queue_20261012.csv';LOG=ROOT/'06_执行台账/search_log_M03.csv'
if not ORIG.exists():
 ORIG=OUT/'data/refs_original.bib';QUEUE=OUT/'data/complete_eligibility_queue_20261012.csv';LOG=OUT/'data/search_log_M03.csv'
def entries(text):
 # Preserve nested braced fields and strings; do not split BibTeX on commas.
 for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),',text):
  i=m.end();depth=1;j=i
  while j<len(text) and depth:
   if text[j]=='{' and (j==0 or text[j-1]!='\\'):depth+=1
   if text[j]=='}' and (j==0 or text[j-1]!='\\'):depth-=1
   j+=1
  body=text[i:j-1];fields={}
  for f in re.finditer(r'(\w+)\s*=\s*',body):
   k=f.group(1).lower();v=f.end()
   if body[v:v+1]=='{':
    level=1;u=v+1;start=u
    while u<len(body) and level:
     if body[u]=='{' and body[u-1]!='\\':level+=1
     if body[u]=='}' and body[u-1]!='\\':level-=1
     u+=1
    value=body[start:u-1]
   elif body[v:v+1]=='"':
    end=body.find('"',v+1);value=body[v+1:end]
   else:value=body[v:].split(',')[0].strip()
   fields[k]=re.sub(r'\s+',' ',value.replace('{','').replace('}','')).strip()
  yield {'key':m[2].strip(),'type':m[1].lower(),**fields}
def doi(s):return re.sub(r'^(?:https?://(?:dx\.)?doi.org/|doi:\s*)','',s.strip().lower()).rstrip(' .')
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
queue=list(csv.DictReader(QUEUE.open(encoding='utf-8-sig')));logs=list(csv.DictReader(LOG.open(encoding='utf-8-sig')))
refs=list(entries(ORIG.read_text()));assert len(refs)==165
roles={};register=[]
mechanism={'cardwell2017bbr','cardwell2016bbrqueue','cardwell2019bbrv2','cardwell2023bbrv3','ietf_ccwg_bbr'}
survey={'abrol2026bbr','al2019survey'}
# These specific non-BBR titles are directly about BBR/path comparison in the text.
core_nonbbr={'ma2017fairness','deutschmann2023starlink'}
learning={'winstein2013remy','pappone2025mutant','ketabi2023drl','kim2020ml','sharan2022symbolic','galliera2023marlin','bernardez2025graphcc','huang2024llm','jiang2021mlcc','boutaba2018ml','dong2018vivace','jay2019aurora','zeng2025alibaba','abbasloo2020orca','dong2015pcc','meng2020proteus'}
for r in refs:
 key=r['key'];title=r.get('title','')
 if key in mechanism:role='BBR mechanism/version material';reason='Direct description of controller model, version or specification'
 elif key in survey:role='Related survey';reason='Comparison of coverage and organization; not a primary BBR result'
 elif 'bbr' in title.lower() or key in core_nonbbr:role='Direct BBR evaluation/analysis';reason='Title identifies BBR or an explicitly discussed BBR comparison'
 elif key in learning:role='Learning/control comparator';reason='Method or survey context for learning-assisted congestion control'
 else:role='Supporting transport/network context';reason='Protocol, queue, measurement, transport or network-design context; not counted as primary BBR evidence'
 d=doi(r.get('doi',''));matches=[x for x in queue if d and doi(x['doi'])==d];kind='DOI exact'
 if not matches:
  matches=[x for x in queue if norm(x['title'])==norm(title) and len(norm(title))>15];kind='Exact normalized title candidate'
 register.append({'citation_key':key,'title':title,'year':r.get('year',''),'bibtex_type':r['type'],'doi':d,'url':r.get('url',''),'evidence_role':role,'role_basis':'Retrospective title/metadata and manuscript-use assessment; not full-text eligibility','role_reason':reason,'acquisition_route':'Legacy citation baseline; historical retrieval route not recorded','supplemental_match_rule':kind if matches else 'Not located by exact DOI/title in capped exports','matched_report_groups':';'.join(x['report_key'] for x in matches),'matched_source_records':';'.join(sorted(set(y for x in matches for y in x['source_record_ids'].split(';')))),'matched_current_eligibility':';'.join(sorted(set(x['eligibility_status'] for x in matches))),'fulltext_inclusion_claim':'Not established by this register'})
with (OUT/'reference_traceability_165.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(register[0]));w.writeheader();w.writerows(register)
db={}
for source in sorted(set(x['source'] for x in logs)):
 rr=[x for x in logs if x['source']==source];db[source]={'queries':len(rr),'exported_records':sum(int(x['exported_records']) for x in rr),'displayed_hit_counts_are_not_relevant_study_counts':True}
byrole=dict(collections.Counter(x['evidence_role'] for x in register))
result={'register_type':'Retrospective citation-level identity and role register; not a completed systematic-review included-study set','references':165,'roles':byrole,'exact_doi_matches':sum(x['supplemental_match_rule']=='DOI exact' for x in register),'exact_title_candidates':sum(x['supplemental_match_rule']=='Exact normalized title candidate' for x in register),'not_located_in_capped_exports':sum(x['matched_report_groups']=='' for x in register),'database_export_counts':db,'historical_retrieval_not_reconstructed':True,'sources_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ORIG,QUEUE,LOG]}}
(OUT/'reference_traceability_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
