from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
x=np.linspace(0,2.5,500)
throughput=np.minimum(x,1)
rtt=1+np.maximum(x-1,0)
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
a2=ax.twinx()
a=ax.plot(x,throughput,color='#2459a6',label='Throughput / bottleneck capacity')[0]
b=a2.plot(x,rtt,'--',color='#b63333',label='Total RTT / propagation RTT')[0]
ax.axvline(1,color='0.45',linestyle=':',linewidth=1)
ax.scatter([1],[1],marker='*',s=140,color='#d89e00',zorder=5)
ax.annotate('Reference operating point\n(in-flight data = BDP)',(1,1),xytext=(1.25,.70),arrowprops={'arrowstyle':'->'},fontsize=10,bbox={'facecolor':'white','edgecolor':'none','alpha':0.95})
ax.set(xlim=(0,2.5),ylim=(0,1.15),xlabel='In-flight data / reference BDP',ylabel='Normalized throughput')
a2.set(ylim=(0,2.875),ylabel='Normalized total RTT')
ax.legend(handles=[a,b],loc='lower right',fontsize=9)
ax.spines['top'].set_visible(False);a2.spines['top'].set_visible(False)
fig.text(.13,.98,'Conceptual single-bottleneck model; not measured data',fontsize=9,ha='left',va='top')
base=Path(__file__).resolve().parents[1]
out=base/'revised' if (base/'revised').exists() else base
fig.savefig(out/'optimal_operating_point_corrected.pdf')
fig.savefig(out/'optimal_operating_point_corrected.png',dpi=180)
