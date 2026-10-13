from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,4.8));ax.axis('off')
rows=[['Path model','Delivery-rate and minimum-RTT estimates','Delivery-rate and minimum-RTT estimates','Delivery-rate and minimum-RTT estimates'],['Probing','Eight-phase ProbeBW sequence','Refill / Up / Down / Cruise','Revised four-phase probing'],['Congestion feedback','Model-based rate control;\nTCP recovery remains active','Loss-based bounds;\nECN response when enabled/eligible','Loss-based bounds;\nECN response when eligible'],['Parameters','Reference Linux v5.4 design','Defaults depend on alpha revision\nand runtime module settings','Defaults depend on source revision\nand eligibility conditions'],['Performance','Evaluate under matched conditions','No universal fairness ranking','No universal fairness ranking']]
import textwrap
rows=[[textwrap.fill(v,width=20 if j==0 else 29) for j,v in enumerate(row)] for row in rows]
t=ax.table(cellText=rows,colLabels=['Aspect','BBRv1','BBRv2','BBRv3'],colWidths=[.16,.28,.28,.28],cellLoc='left',loc='center');t.auto_set_font_size(False);t.set_fontsize(9);t.scale(1,3.2)
for (r,c),cell in t.get_celld().items():
 cell.set_edgecolor('#cccccc')
 if r==0:cell.set_facecolor('#e9eff7');cell.set_text_props(weight='bold')
ax.set_title('Version mechanisms and conditions for comparison',fontsize=14,weight='bold',pad=12)
fig.text(.05,.035,'Mechanism overview; not a measured performance ranking. Exact parameters are reported in the manuscript version-parameter table.',fontsize=10)
fig.subplots_adjust(left=.025,right=.975,top=.88,bottom=.12)
base=Path(__file__).resolve().parents[1]
out=base/'revised' if (base/'revised').exists() else base
fig.savefig(out/'version_comparison_corrected.pdf');fig.savefig(out/'version_comparison_corrected.png',dpi=160)
