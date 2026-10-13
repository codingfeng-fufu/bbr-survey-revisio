from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[2]
source=root/'06_执行台账/cross_version_20261012/cross_version_condition_summary.csv'
base=Path(__file__).resolve().parents[1]
if not source.exists(): source=base/'experiment_data/cross_version_condition_summary.csv'
rows=list(csv.DictReader(source.open()));out=base/'revised' if (base/'revised').exists() else base
impl=['in_tree_baseline','BBRv1_module','BBR2','BBRv3'];names=['In-tree baseline','BBRv1 module','BBR2','BBRv3'];colors=['#777777','#2459a6','#cb7724','#318446']
fig,axes=plt.subplots(2,3,figsize=(10,6),sharex=True)
for col,q in enumerate([.5,2,10]):
 for k in range(4):
  rr=sorted([r for r in rows if r['experiment']=='E1' and r['implementation']==impl[k] and float(r['queue_bdp_multiplier'])==q],key=lambda r:float(r['rtt2_ms']))
  axes[0,col].plot([float(r['rtt2_ms']) for r in rr],[float(r['jain_mean']) for r in rr],'o-',color=colors[k],label=names[k])
  axes[1,col].plot([float(r['rtt2_ms']) for r in rr],[float(r['flow2_share_mean']) for r in rr],'o-',color=colors[k])
 axes[0,col].set_title(f'Queue target: {q:g} BDP');axes[1,col].set_xlabel('Second-flow RTT (ms)')
 for ax in axes[:,col]:ax.set_xticks([20,40,80]);ax.grid(alpha=.2)
axes[0,0].set_ylabel('Mean run-level Jain index');axes[1,0].set_ylabel('Mean second-flow share')
axes[0,0].legend(fontsize=8);fig.tight_layout();fig.savefig(out/'e1_results.pdf');fig.savefig(out/'e1_results.png',dpi=160)
lines=[r'\begin{table}[htbp]',r'\centering',r'\caption{E2 competition with CUBIC at 100 Mbps and equal 20-ms RTTs, with ECN disabled. Each cell summarizes five full-run receiver measurements. Share denotes the BBR flow; Jain is the mean of per-run indices. Different implementation environments limit causal version attribution.}',r'\label{tab:e2_results}',r'\small',r'\begin{tabular}{lrrrr}',r'\toprule',r'Implementation & Q/BDP & Total (Mbps) & BBR share & Jain \\',r'\midrule']
for imp,name in zip(impl,names):
 for r in sorted([r for r in rows if r['experiment']=='E2' and r['implementation']==imp],key=lambda r:float(r['queue_bdp_multiplier'])):
  share=float(r['flow1_mean_mbps'])/(float(r['flow1_mean_mbps'])+float(r['flow2_mean_mbps']))
  # Mean run share is supplied for flow2; BBR is flow1.
  share=1-float(r['flow2_share_mean'])
  lines.append(f"{name} & {float(r['queue_bdp_multiplier']):g} & {float(r['total_mean_mbps']):.2f} & {share:.3f} & {float(r['jain_mean']):.3f} "+r'\\')
lines +=[r'\bottomrule',r'\end{tabular}',r'\end{table}']
(out/'E2_results_table.tex').write_text('\n'.join(lines)+'\n')
