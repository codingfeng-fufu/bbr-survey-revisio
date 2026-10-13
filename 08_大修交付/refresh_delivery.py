from pathlib import Path
import csv,re,zipfile,shutil,hashlib,json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from xml.sax.saxutils import escape
root=Path(__file__).resolve().parent;rev=root/'revised'
labels={m[0]:(m[1],m[2]) for m in re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}", (rev/'cas-sc-template.aux').read_text())}
rows=list(csv.DictReader((root/'reviewer_change_locations.csv').open()))
for row in rows:
 if row['label'] in labels:
  row['number'],row['printed_page']=labels[row['label']];row['status']='integrated'
# Extend experiment result locations and search figure mapping.
for key,label in [('R2-1','fig:prisma'),('R1-M3','tab:e3_candidate'),('R1-M4','sec:controlled_experiments'),('R2-2','tab:e3_candidate'),('R3-4','tab:e3_candidate')]:
 if not any(x['review_id']==key and x['label']==label for x in rows):
  number,page=labels[label];rows.append(dict(review_id=key,label=label,number=number,printed_page=page,status='integrated'))
with (root/'reviewer_change_locations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['review_id','label','number','printed_page','status']);w.writeheader();w.writerows(rows)
p=root/'response_to_reviewers.md';s=p.read_text().split('\n## Compiled revision index')[0]
# Replace vague location sentences with compiled, exact locations for each response.
for key in dict.fromkeys(r['review_id'] for r in rows):
 rr=[r for r in rows if r['review_id']==key and r['number']]
 loc=['{} {} (p. {})'.format('Figure' if r['label'].startswith('fig:') else 'Table' if r['label'].startswith('tab:') else 'Section',r['number'],r['printed_page']) for r in rr]
 if loc:
  pattern=r'(### '+re.escape(key)+r':.*?)(?=\n### |\n## |\Z)'
  def replace(m):
   body=re.sub(r'(?:Revised locations?|Manuscript locations):[^\n]*', '',m.group(1)).rstrip()
   body=re.sub(r'\n{3,}', '\n\n',body)
   return body+'\n\nManuscript locations: '+('; '.join(loc))+'.\n'
  s=re.sub(pattern,replace,s,flags=re.S)
import fitz
man=fitz.open(rev/'cas-sc-template.pdf')
declaration_page=next(i for i,p in enumerate(man) if 'Declaration of generative AI and AI-assisted technologies' in p.get_text())
s=s.replace('Manuscript locations: Figure 3', 'Manuscript locations: Declaration of generative AI (p. '+str(declaration_page)+'); Figure 3')
s+='\n## Compiled revision index\n\nPage numbers refer to the printed manuscript pages, excluding the separate Highlights sheet. Reviewer comments above are faithful summaries; the original review text is supplied separately.\n\n'
for key in dict.fromkeys(r['review_id'] for r in rows):
 rr=[r for r in rows if r['review_id']==key and r['number']]
 loc=['{} {} (p. {})'.format('Figure' if r['label'].startswith('fig:') else 'Table' if r['label'].startswith('tab:') else 'Section',r['number'],r['printed_page']) for r in rr]
 s+=key+': '+('; '.join(loc) if loc else 'Abstract/Highlights (unnumbered) or acknowledgement of positive comment')+'.\n\n'
p.write_text(s)
for reviewer in (1,2,3):
 part=s.split('## Reviewer '+str(reviewer)+'\n',1)[1]
 part=part.split('## Reviewer '+str(reviewer+1),1)[0] if reviewer<3 else part.split('## Compiled revision index',1)[0]
 part=re.sub(r'^### ', '',part.strip(),flags=re.M)
 intro='Response to Reviewer '+str(reviewer)+'\n\nThank you for reading the manuscript carefully. We respond to each comment below. Page numbers refer to the printed revised manuscript pages.\n\n'
 (root/('Reviewer_'+str(reviewer)+'_response.txt')).write_text(intro+part+'\n',encoding='utf-8')
styles=getSampleStyleSheet();styles['BodyText'].leading=14
styles['BodyText'].spaceAfter=5
styles['Heading2'].keepWithNext=True

def pdf(name,text):
 story=[]
 for b in text.split('\n\n'):
  b=b.strip()
  if not b:continue
  n=len(b)-len(b.lstrip('#'));style=styles['Title' if n==1 else 'Heading1' if n==2 else 'Heading2' if n==3 else 'BodyText']
  story.extend([Paragraph(escape(b.lstrip('# ').replace('`','')).replace('\n','<br/>'),style),Spacer(1,7)])
 def footer(canvas,doc):
  canvas.saveState();canvas.setFont('Helvetica',8);canvas.setFillColor(colors.grey);canvas.drawString(45,25,'COMNET-D-26-03761');canvas.drawRightString(550,25,str(doc.page));canvas.restoreState()
 SimpleDocTemplate(str(root/name),leftMargin=45,rightMargin=45,topMargin=45,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
pdf('response_to_reviewers.pdf',s)
pdf('cover_letter.pdf',(root/'cover_letter.md').read_text())
pdf('highlights.pdf','# Highlights\n\n'+'\n\n'.join((root/'highlights.txt').read_text().splitlines()))
pdf('experimental_supplement.pdf',(root/'experimental_supplement.md').read_text())
pdf('search_supplement.pdf',(root/'search_supplement.md').read_text())
shutil.copy2(rev/'cas-sc-template.pdf',root/'BBR_revised_manuscript.pdf')
with zipfile.ZipFile(root/'BBR_revised_source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in rev.iterdir():
  if (p.suffix in {'.tex','.bib','.png','.cls','.sty','.bst'} and p.name!='cas-sc-template_F05_applied.tex') or (p.suffix=='.pdf' and p.name!='cas-sc-template.pdf'):z.write(p,p.name)
 for p in (root/'figure_sources').glob('*.py'):z.write(p,'figure_sources/'+p.name)
 for p in (root/'targeted_revision').rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(root))
 source=root.parent/'06_执行台账/cross_version_20261012/cross_version_condition_summary.csv'
 z.write(source,'experiment_data/cross_version_condition_summary.csv')
 z.writestr('README.md','Compile: pdflatex cas-sc-template.tex; bibtex cas-sc-template; pdflatex cas-sc-template.tex until label-change warnings disappear. Figures are supplied. Plot scripts use Python/matplotlib; E1/E2 inputs are in experiment_data. The full experiment archive is delivered separately.\n')
files=['BBR_revised_manuscript.pdf','response_to_reviewers.md','response_to_reviewers.pdf','BBR_revised_source.zip','cover_letter.md','cover_letter.pdf','highlights.txt','highlights.pdf','experimental_supplement.zip','experimental_supplement.pdf','search_supplement.zip','search_supplement.pdf']
(root/'delivery_hashes.json').write_text(json.dumps({f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n')
print('Refreshed final delivery and compiled locations')
