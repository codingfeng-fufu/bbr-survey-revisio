import csv, json, re
from pathlib import Path

root = Path(__file__).parent
source = root / 'screening_round1_M04.csv'
out = root / 'screening_human_round1_M04.csv'
rows = list(csv.DictReader(source.open(encoding='utf-8-sig')))
direct = re.compile(r'\b(bbr|bbrv[123]|bottleneck bandwidth|bbrp|bdp[- ]?veno|oveno|o[- ]?veno)\b', re.I)
network = re.compile(r'congestion|tcp|quic|rtt|round[- ]?trip|fairness|buffer|queue|ecn|loss|wireless|wifi|cellular|satellite|leo|network|transport', re.I)
obvious_nonnetwork = re.compile(r'bounding box|hypox|ecmo|medical|image classification|object detection|protein|gene|tumor|battery|electric vehicle|stock market', re.I)
learning = re.compile(r'learning|reinforcement|machine learning|deep learning|neural|xgboost|dr[lq]', re.I)
for row in rows:
    title = row.get('title', '')
    abstract = row.get('abstract', '')
    text = (title + ' ' + abstract).strip()
    qid = row.get('query_id', '')
    if obvious_nonnetwork.search(text):
        decision, reason = 'exclude_title_abstract', 'Clearly unrelated non-network topic in title/abstract.'
    elif direct.search(text) and network.search(text):
        decision, reason = 'include_title_abstract', 'Direct BBR/Veno/BDP-Veno/OVeno evidence with a transport or network topic.'
    elif qid == 'Q8' and learning.search(text) and network.search(text):
        decision, reason = 'include_title_abstract', 'Learning-assisted congestion-control background evidence.'
    elif qid in ('Q5', 'Q6'):
        decision, reason = 'uncertain_full_text', 'Supplemental protocol query; full text needed to verify algorithm identity and relevance.'
    elif direct.search(text):
        decision, reason = 'uncertain_full_text', 'Protocol term present but title/abstract does not establish usable evidence.'
    else:
        decision, reason = 'uncertain_full_text', 'Insufficient title/abstract evidence for a defensible exclusion.'
    row['human_title_abstract_decision'] = decision
    row['human_screening_reviewer'] = 'Codex'
    row['human_screening_date'] = '2026-09-28'
    row['human_screening_reason'] = reason
    row['full_text_status'] = 'not_started'
    row['final_inclusion'] = 'pending_full_text'
with out.open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
counts = {}
for row in rows:
    counts[row['human_title_abstract_decision']] = counts.get(row['human_title_abstract_decision'], 0) + 1
summary = {'records_screened': len(rows), 'reviewer': 'Codex', 'screening_date': '2026-09-28',
           'counts': counts, 'full_text_reviews_completed': 0, 'final_included': 0,
           'note': 'Title/abstract screening is complete for the exported records. Final inclusion remains pending full-text review.'}
(root / 'screening_human_round1_M04_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
