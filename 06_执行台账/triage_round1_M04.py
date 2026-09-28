import csv, re, json
from pathlib import Path

root = Path(__file__).parent
source = root / 'screening_queue_M04_MACHINE_TRIAGE.csv'
out = root / 'screening_round1_M04.csv'
rows = list(csv.DictReader(source.open(encoding='utf-8-sig')))
bbr = re.compile(r'\b(bbr|bbrv[123]|bottleneck bandwidth|bbrp)\b', re.I)
veno = re.compile(r'\b(veno|bdp[- ]?veno|oveno|o[- ]?veno)\b', re.I)
topic = re.compile(r'fair|rtt|round[- ]?trip|buffer|queue|ecn|loss|wireless|wifi|cellular|satellite|leo|quic|learning|reinforcement|congestion control|tcp', re.I)
abstract_available = 0
for row in rows:
    text = (row.get('title', '') + ' ' + row.get('abstract', '')).strip()
    if row.get('abstract'):
        abstract_available += 1
    direct = bool(bbr.search(text) or veno.search(text))
    topical = bool(topic.search(text))
    qid = row.get('query_id', '')
    if direct and topical:
        decision, reason = 'candidate_include', 'BBR/BDP-Veno/OVeno term plus a review topic'
    elif direct:
        decision, reason = 'manual_check', 'Protocol term present but topic relevance needs reading'
    elif qid == 'Q8' and topical:
        decision, reason = 'candidate_background', 'General learning congestion-control evidence; scope must be checked'
    elif not direct and qid in ('Q5', 'Q6'):
        decision, reason = 'manual_check', 'Exact supplemental query but title/abstract lacks expected protocol term'
    else:
        decision, reason = 'manual_check', 'No safe automatic exclusion from title/abstract alone'
    row['machine_round1_decision'] = decision
    row['machine_round1_reason'] = reason
    row['human_title_abstract_decision'] = 'pending'
    row['human_exclusion_reason'] = ''
    row['full_text_status'] = 'not_started'
with out.open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
counts = {}
for row in rows:
    counts[row['machine_round1_decision']] = counts.get(row['machine_round1_decision'], 0) + 1
summary = {'records': len(rows), 'abstract_available': abstract_available,
           'machine_round1_counts': counts, 'human_title_abstract_decisions_completed': 0,
           'full_text_reviews_completed': 0,
           'note': 'Machine triage is only a reading order; no record is finally included or excluded.'}
(root / 'screening_round1_M04_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
