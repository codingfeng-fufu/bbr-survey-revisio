"""Design expansion only. No traffic and no invented measurements."""
import csv
import json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
rows = []

def add(exp, alg, peer, c, r1, r2, q, ref, owner):
    cid=f'{exp}_{alg}_{peer}_C{c}_R{r1}-{r2}_Q{str(q).replace(".", "p")}'
    bdp=round(c*1_000_000*ref/1000/8)
    for rep in range(1,6):
        rows.append(dict(run_id=f'{cid}_rep{rep:02d}',condition_id=cid,
            experiment=exp,owner=owner,algorithm_flow1=alg,algorithm_flow2=peer,
            capacity_mbps=c,rtt1_ms=r1,rtt2_ms=r2,queue_bdp_multiplier=q,
            bdp_reference_rtt_ms=ref,bdp_reference_bytes=bdp,queue_target_bytes=round(bdp*q),
            queue_policy='FIFO_DRAFT',queue_effective_bytes='UNRESOLVED',
            ecn_target='off',injected_loss_probability=0,
            duration_s=180,warmup_s=30,analysis_start_s=30,analysis_end_s=180,repeat=rep,
            implementation_manifest_id='UNRESOLVED',environment_id='UNRESOLVED',
            actual_run_order='UNASSIGNED',
            prediction_id=f'E3_C{c}_R{r1}_Q{q}' if exp=='E3' else 'NA',
            design_state='DRAFT_NOT_FROZEN',execution_state='NOT_RUN'))

for v in ('BBRv1','BBRv2','BBRv3'):
    for r in (20,40,80):
        for q in (0.5,2,10):
            add('E1',v,v,100,20,r,q,20,'冯宗林' if q==2 else '刘馨月')
    for q in (0.5,2,10):
        add('E2',v,'CUBIC',100,20,20,q,20,'冯宗林' if q==2 else '刘馨月')
for c in (50,200):
    for r in (10,60):
        for q in (1,4):
            for v in ('BBRv3','CUBIC'):
                add('E3',v,v,c,r,r,q,r,'冯宗林' if c==50 else '刘馨月')

def write_csv(name, data, fields=None):
    with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(data[0]))
        w.writeheader()
        w.writerows(data)

assert len(rows)==260 and len({r['run_id'] for r in rows})==260
assert Counter(r['experiment'] for r in rows)=={'E1':135,'E2':45,'E3':80}
assert Counter(r['owner'] for r in rows)=={'冯宗林':100,'刘馨月':160}
assert len({r['condition_id'] for r in rows})==52
assert set(Counter(r['condition_id'] for r in rows).values())=={5}
assert all(r['analysis_end_s']-r['analysis_start_s']==150 for r in rows)
for r in rows:
    assert r['queue_target_bytes']>0
    if r['experiment'] in ('E1','E2'):
        assert r['capacity_mbps']==100 and r['bdp_reference_bytes']==250000
    if r['experiment']=='E1':
        assert r['algorithm_flow1']==r['algorithm_flow2']
    if r['experiment']=='E2':
        assert r['algorithm_flow2']=='CUBIC' and r['rtt1_ms']==r['rtt2_ms']==20
write_csv('design_matrix_all_DRAFT.csv',rows)
write_csv('design_matrix_liuxinyue_DRAFT.csv',[r for r in rows if r['owner']=='刘馨月'])
cases={}
for r in rows:
    if r['experiment']=='E3':
        cases[r['prediction_id']]=dict(case_id=r['prediction_id'],capacity_mbps=r['capacity_mbps'],
            rtt_ms=r['rtt1_ms'],queue_target_bytes=r['queue_target_bytes'],
            throughput_prediction='NOT_PROVIDED',rtt_prediction='NOT_PROVIDED',
            fairness_prediction='NOT_PROVIDED',tolerance_and_basis='NOT_PROVIDED',
            framework_version='NOT_PROVIDED',frozen_at='NOT_FROZEN')
assert len(cases)==8
for cid in cases:
    rr=[r for r in rows if r['prediction_id']==cid]
    assert len(rr)==10 and {r['algorithm_flow1'] for r in rr}=={'BBRv3','CUBIC'}
write_csv('E3_predictions_TO_FILL.csv',list(cases.values()))
example=next(r for r in rows if r['owner']=='刘馨月')
(ROOT/'example_config_DRAFT.json').write_text(json.dumps(example,ensure_ascii=False,indent=2),encoding='utf-8')
write_csv('run_metrics_EMPTY.csv',[],['run_id','validity','goodput_flow1_mbps','goodput_flow2_mbps',
    'target_share','jain_index','rtt_flow1_median_ms','rtt_flow2_median_ms',
    'retransmissions_window','queue_drops_window','raw_data_path','analysis_version'])
report=dict(check='PASS_DESIGN_STRUCTURE_ONLY',runs=260,conditions=52,
    assigned_liuxinyue=160,assigned_fengzonglin=100,traffic_hours_all=13,
    real_experiments_executed=0,formal_run_ready=False,
    checks=['unique_ids','counts_and_ownership','five_repeats_per_condition','bdp_arithmetic',
            'protocol_pairing','analysis_window','E3_prediction_pairing'],
    blockers=['no_installed_WSL_distribution_observed','Linux_host_and_permissions_unconfirmed',
        'implementation_commits_unconfirmed','queue_realization_unconfirmed',
        'preflight_tolerances_unfrozen','scripts_not_implemented','E3_predictions_not_supplied'])
(ROOT/'design_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
