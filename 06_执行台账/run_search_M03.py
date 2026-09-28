import csv, json, re, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
RAW = ROOT / 'raw_search_20260928'
RAW.mkdir(exist_ok=True)
queries = {
    'Q1': 'BBR congestion control', 'Q2': 'BBRv2 BBRv3 congestion control',
    'Q3': 'BBR RTT fairness', 'Q4': 'BBR buffer loss ECN',
    'Q5': 'BDP-Veno', 'Q6': 'OVeno TCP congestion control',
    'Q7': 'BBR wireless satellite LEO', 'Q8': 'learning congestion control fairness',
}

def get_json(url):
    req = Request(url, headers={'User-Agent': 'bbr-survey-revision/1.0 (systematic-review-audit)'})
    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode('utf-8'))

def openalex_abstract(item):
    inv = item.get('abstract_inverted_index') or {}
    words = []
    for word, positions in inv.items():
        for position in positions:
            words.append((position, word))
    return ' '.join(word for _, word in sorted(words))

logs, records = [], []
for source in ('openalex', 'crossref'):
    for qid, query in queries.items():
        if source == 'openalex':
            url = 'https://api.openalex.org/works?search=' + quote(query) + '&per-page=200'
        else:
            url = 'https://api.crossref.org/works?query=' + quote(query) + '&rows=200&select=DOI,title,author,published,container-title,type'
        try:
            data = get_json(url)
            path = RAW / f'{source}_{qid}.json'
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            if source == 'openalex':
                items = data.get('results', [])
                total = data.get('meta', {}).get('count', '')
            else:
                items = data.get('message', {}).get('items', [])
                total = data.get('message', {}).get('total-results', '')
            logs.append({'search_id': f'{source}_{qid}', 'source': source, 'query_id': qid,
                         'exact_query': query, 'search_datetime': '2026-09-28',
                         'displayed_hits': total, 'exported_records': len(items),
                         'raw_file': path.name, 'status': 'success', 'error': ''})
            for i, item in enumerate(items, 1):
                title = item.get('display_name') if source == 'openalex' else ((item.get('title') or [''])[0])
                abstract = openalex_abstract(item) if source == 'openalex' else (item.get('abstract') or '')
                doi = item.get('doi') if source == 'openalex' else item.get('DOI')
                year = item.get('publication_year') if source == 'openalex' else ((item.get('published', {}).get('date-parts') or [[None]])[0][0])
                records.append({'record_id': f'{source}_{qid}_{i:04d}', 'search_id': f'{source}_{qid}',
                                'source': source, 'query_id': qid, 'title': title or '', 'abstract': abstract,
                                'year': year or '', 'doi': doi or '', 'screening_decision': 'pending',
                                'exclusion_reason': '', 'report_id': 'to_assign', 'study_id': 'to_assign'})
        except Exception as exc:
            logs.append({'search_id': f'{source}_{qid}', 'source': source, 'query_id': qid,
                         'exact_query': query, 'search_datetime': '2026-09-28',
                         'displayed_hits': '', 'exported_records': 0, 'raw_file': '',
                         'status': 'error', 'error': repr(exc)})
        time.sleep(0.2)

def write(name, rows):
    if not rows: return
    with (ROOT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
write('search_log_M03.csv', logs)
write('screening_log_M04_PENDING.csv', records)

def norm(row):
    title = re.sub(r'[^a-z0-9 ]', ' ', row['title'].lower())
    return re.sub(r'\s+', ' ', title).strip()

dedup = {}
for row in records:
    key = ('doi:' + row['doi'].lower().strip()) if row['doi'] else ('title:' + norm(row))
    keep = dedup.get(key)
    row['duplicate_key'] = key
    row['duplicate_of'] = keep or ''
    if not keep: dedup[key] = row['record_id']
write('dedup_map_M04_PENDING.csv', records)

terms = ('bbr', 'congestion control', 'tcp', 'veno', 'fairness', 'rtt', 'buffer',
         'queue', 'ecn', 'wireless', 'satellite', 'leo', 'quic', 'learning')
for row in records:
    hay = (row['title'] + ' ' + row.get('abstract', '')).lower()
    hits = [term for term in terms if term in hay]
    row['keyword_hits'] = ';'.join(hits)
    row['machine_triage'] = 'priority_review' if len(hits) >= 2 else 'low_priority_review'
write('screening_queue_M04_MACHINE_TRIAGE.csv', records)

summary = {'search_requests': len(logs), 'successful_requests': sum(x['status']=='success' for x in logs),
           'failed_requests': sum(x['status']=='error' for x in logs),
           'exported_records_before_dedup': len(records), 'unique_keys': len(dedup),
           'records_pending_screening': len(records), 'screening_completed': 0,
           'full_text_reviewed': 0, 'final_included': 0,
           'note': 'Search and deduplication exports are real records; screening remains pending until title/abstract review.'}
(ROOT / 'search_summary_M03_M04.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
