#!/usr/bin/env python3
"""Audit explicit current TeX/bibliography inputs into a separate directory.
Static key consistency only; never infer literature screening from citations.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tex',type=Path,required=True)
    parser.add_argument('--bib',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    if not args.tex.is_file() or not args.bib.is_file():
        parser.error('Both actual TeX and bibliography files must exist; no placeholder audit')
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error('Use an empty/new output directory to preserve previous audit evidence')
    sources={}
    visited=set()
    def read(path):
        path=path.resolve()
        if path in visited:return
        visited.add(path)
        text=path.read_text(encoding='utf-8')
        text=re.sub(r'(?<!\\)%[^\n]*','',text)
        sources[path]=text
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):
            target=path.parent/child
            if not target.suffix:target=target.with_suffix('.tex')
            if not target.is_file():raise FileNotFoundError('Unresolved source input: '+str(target))
            read(target)
    read(args.tex)
    keys=set()
    pattern=r'\\cite(?:p|t|alt|alp|author|year|yearpar)?\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}'
    for source in sources.values():
        for group in re.findall(pattern,source):keys.update(k.strip() for k in group.split(',') if k.strip())
    entries=re.findall(r'^\s*@(?!(?:comment|string|preamble)\b)\w+\{\s*([^,\s]+)',args.bib.read_text(encoding='utf-8'),re.M|re.I)
    bib_keys=set(entries)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    summary={'tex_files':[str(p) for p in sources],'cited_keys':len(keys),'bibliography_entries':len(entries),'missing_keys':sorted(keys-bib_keys),'unused_keys':sorted(bib_keys-keys),'duplicate_bibliography_keys':sorted(k for k in bib_keys if entries.count(k)>1),'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*sources,args.bib.resolve()]},'scope':'Static key consistency; no full BibTeX syntax, LaTeX runtime, final PDF or systematic-review acceptance.'}
    (args.output_dir/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    with (args.output_dir/'keys.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['citation_key','cited','in_bibliography'])
        writer.writerows((k,k in keys,k in bib_keys) for k in sorted(keys|bib_keys))
    print(json.dumps(summary,ensure_ascii=False))
    if summary['missing_keys'] or summary['duplicate_bibliography_keys']:raise SystemExit(1)

if __name__=='__main__':main()
