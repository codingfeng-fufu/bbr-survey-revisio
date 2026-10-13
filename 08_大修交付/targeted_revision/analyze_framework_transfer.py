"""Retrospective data-disjoint transfer test; no claim of preregistration."""
from pathlib import Path
import csv,json,math,statistics,hashlib
ROOT=Path(__file__).resolve().parents[2]
LEDGER=ROOT/'06_执行台账'; OUT=Path(__file__).resolve().parent
if not LEDGER.exists(): LEDGER=OUT/'data'
def read(path):return list(csv.DictReader(path.open(encoding='utf-8-sig')))
cal_path=LEDGER/'formal_bbr3_20261011/run_metrics.csv'
eval_path=LEDGER/'formal_e3_20261011/run_metrics.csv'
cal=[r for r in read(cal_path) if r['experiment']=='E1' and float(r['rtt2_ms'])==20]
evalrows=read(eval_path)
assert len(cal)==15 and len(evalrows)==80
# Fit once to E1 calibration. No E3-dependent parameter or degree selection.
# Piecewise interpolation on log queue ratio avoids fitting a capacity/RTT effect
# not identified by the single capacity and common RTT in calibration.
knots=[]
for q in [.5,2,10]:
 rs=[r for r in cal if float(r['queue_bdp_multiplier'])==q]
 knots.append((math.log(q),statistics.mean(float(r['total_goodput_mbps'])/100 for r in rs),statistics.mean(float(r['jain_index']) for r in rs)))
def predict(q,k):
 z=math.log(q)
 i=0 if z<=knots[1][0] else 1
 a,b=knots[i],knots[i+1]
 value=a[k]+(z-a[0])/(b[0]-a[0])*(b[k]-a[k])
 return min(1,max(.5 if k==2 else 0,value))
base=[statistics.mean(float(r['total_goodput_mbps'])/100 for r in cal),statistics.mean(float(r['jain_index']) for r in cal)]
conditions=[];records=[]
for case in sorted(set(r['prediction_case_id'] for r in evalrows)):
 for alg in ['BBR3','CUBIC']:
  rr=[r for r in evalrows if r['prediction_case_id']==case and r['algorithm']==alg]
  c=float(rr[0]['capacity_mbps']);rt=float(rr[0]['rtt_ms']);qbytes=float(rr[0]['queue_target_bytes']);q=qbytes/(c*1e6*rt/1000/8)
  vals=[float(r['total_goodput_mbps'])/c for r in rr];js=[float(r['jain_index']) for r in rr]
  row={'case':case,'algorithm':alg,'capacity_mbps':c,'rtt_ms':rt,'actual_q_bdp':q,'n':len(rr),'efficiency_mean':statistics.mean(vals),'efficiency_sd':statistics.stdev(vals),'jain_mean':statistics.mean(js),'jain_sd':statistics.stdev(js),'prediction_efficiency':predict(q,1) if alg=='BBR3' else '', 'prediction_jain':predict(q,2) if alg=='BBR3' else '', 'constant_efficiency':base[0] if alg=='BBR3' else '', 'constant_jain':base[1] if alg=='BBR3' else '', 'split':'matched_input' if c==200 else 'corrected_extra'}
  conditions.append(row)
  for r,u,j in zip(rr,vals,js):
   records.append(dict(case=case,algorithm=alg,run_id=r['run_id'],efficiency=u,jain=j,passes_utilization_090=int(u>=.90),passes_jain_095=int(j>=.95),passes_joint=int(u>=.90 and j>=.95)))
grid=[]
for u0 in [.90,.93,.95]:
 for j0 in [.90,.95,.99]:
  for alg in ['BBR3','CUBIC']:
   rr=[r for r in records if r['algorithm']==alg];grid.append(dict(algorithm=alg,u0=u0,j0=j0,n=len(rr),joint_passes=sum(r['efficiency']>=u0 and r['jain']>=j0 for r in rr)))
with (OUT/'assessment_threshold_sensitivity.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(grid[0]));w.writeheader();w.writerows(grid)
results={}
for split in ['matched_input','corrected_extra','all']:
 cs=[r for r in conditions if r['algorithm']=='BBR3' and (split=='all' or r['split']==split)]
 results[split]={'conditions':len(cs)}
 for label,actual,pred,constant in [('efficiency','efficiency_mean','prediction_efficiency','constant_efficiency'),('jain','jain_mean','prediction_jain','constant_jain')]:
  errs=[r[pred]-r[actual] for r in cs];berrs=[r[constant]-r[actual] for r in cs]
  results[split][label]={'mae':statistics.mean(abs(e) for e in errs),'rmse':math.sqrt(statistics.mean(e*e for e in errs)),'max_abs_error':max(abs(e) for e in errs),'constant_mae':statistics.mean(abs(e) for e in berrs)}
# Policy diagnostic is retrospective. Tolerances are illustrative, not learned or frozen.
policy={}
for alg in ['BBR3','CUBIC']:
 rr=[r for r in records if r['algorithm']==alg]
 policy[alg]={k:sum(r[k] for r in rr) for k in ['passes_utilization_090','passes_jain_095','passes_joint']};policy[alg]['runs']=len(rr)
OUT.mkdir(exist_ok=True)
for filename,rows in [('framework_transfer_conditions.csv',conditions),('assessment_run_decisions.csv',records)]:
 with (OUT/filename).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'design':'Retrospective transfer evaluation designed after archived results were available. Fits only 15 E1 equal-RTT BBRv3 calibration runs; E3 is disjoint, not an untouched preregistered test. No E3 fit or tuning.','calibration_runs':len(cal),'evaluation_runs':80,'knots_logq_efficiency_jain':knots,'constant_baseline_efficiency_jain':base,'errors_on_condition_means':results,'illustrative_policy_counts':policy,'source_sha256':{str(p.relative_to(LEDGER)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [cal_path,eval_path]}}
(OUT/'framework_transfer_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
