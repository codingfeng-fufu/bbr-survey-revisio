from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
base=Path(__file__).resolve().parents[1]
out=base/'revised' if (base/'revised').exists() else base
def draw(name,title,rows,note):
 fig,ax=plt.subplots(figsize=(10,4.5));ax.set(xlim=(0,10),ylim=(0,4.5));ax.axis('off')
 ax.text(.2,4.12,title,fontsize=14,weight='bold')
 for y,labels in rows:
  for j,label in enumerate(labels):
   x=.2+j*3.3
   ax.add_patch(FancyBboxPatch((x,y),2.85,.8,boxstyle='round,pad=0.06',facecolor='#f2f6fa',edgecolor='#2459a6'))
   ax.text(x+1.425,y+.4,label,ha='center',va='center',fontsize=11)
   if j<2:ax.annotate('',(x+3.22,y+.4),(x+2.94,y+.4),arrowprops={'arrowstyle':'->','color':'#555555'})
 ax.text(.2,.25,note,fontsize=10,va='bottom')
 fig.subplots_adjust(left=.015,right=.99,bottom=.03,top=.99)
 fig.savefig(out/(name+'.pdf'));fig.savefig(out/(name+'.png'),dpi=180);plt.close(fig)
draw('rtt_skew_mechanism_corrected','RTT asymmetry: model target and measured allocation',[(2.85,['Capacity and propagation RTT','Reference in-flight target\nrate × propagation RTT','Equal rates can require\ndifferent in-flight volumes']),(1.45,['Probing and recovery\n(version-dependent)','Shared queue and scheduler\n(flow count, loss, queue size)','Measure per-flow goodput\nand Jain fairness'])],'The in-flight identity alone does not determine bandwidth shares.\nArrows show assessment steps, not a proven causal allocation law.')
draw('fairness_mechanism_corrected','Fairness assessment under a shared bottleneck',[(2.85,['Same-version competition\nEqual or unequal RTTs','Version-specific probing\nand in-flight constraints','Observed shares and Jain\nunder reported conditions']),(1.45,['BBR/CUBIC competition\nLoss and ECN configuration','Recovery, queues and\ncontroller interactions','Measure goodput, delay,\nfairness and retransmissions'])],'ECN absence does not remove BBRv2/v3 loss-based logic.\nNeither RTT nor loss-response differences alone establish an inevitable unfair share.')
draw('bbr_architecture_corrected','BBRv1: measurement model and controller modes',[(2.85,['ACK delivery and RTT samples','Maximum delivery-rate filter\nMinimum RTT filter','Pacing target and\ncongestion-window target']),(1.45,['Startup → Drain → ProbeBW','Freshness and state conditions\ncan trigger ProbeRTT','RTT sampling, then return\nto bandwidth probing'])],'Simplified BBRv1 overview: TCP recovery remains active; no BBRv2/v3 ECN-bound logic is shown.\nFilter expiration is not a guaranteed periodic transition; targets are not exact instantaneous values.')
