#!/usr/bin/env python3
"""Inventory current candidate dependencies; never equate inventory with acceptance."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / '07_Overleaf修订候选'
OUT = ROOT / '06_执行台账/current_delivery_audit_20261012'


def main():
    OUT.mkdir(exist_ok=True)
    dependencies = []
    visited = set()

    def inspect(path):
        path = path.resolve()
        if path in visited:
            return
        visited.add(path)
        source = path.read_text()
        for kind, pattern in [
            ('figure', r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}'),
            ('input', r'\\input\{([^}]+)\}'),
            ('bibliography', r'\\bibliography\{([^}]+)\}')]:
            for name in re.findall(pattern, source):
                target = CANDIDATES / name
                if kind == 'bibliography': target = target.with_suffix('.bib')
                if kind == 'input' and not target.suffix: target = target.with_suffix('.tex')
                dependencies.append({'source': str(path.relative_to(ROOT)), 'kind': kind,
                                     'name': name, 'exists_in_candidate_directory': target.is_file()})
                if kind == 'input' and target.is_file(): inspect(target)

    inspect(CANDIDATES / 'cas-sc-template_F05_applied.tex')
    (OUT / 'dependencies.json').write_text(json.dumps(dependencies, ensure_ascii=False, indent=2)+'\n')
    files = set(CANDIDATES.glob('*.tex')) | set(CANDIDATES.glob('*.md'))
    files |= set((ROOT/'06_执行台账').glob('*verification_20261012.md'))
    files |= {ROOT/'06_执行台账/review_tracker.csv', ROOT/'06_执行台账/measurement_window_audit_20261012.md'}
    records = [{'file': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    (OUT / 'candidate_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    missing = [d for d in dependencies if not d['exists_in_candidate_directory']]
    print(json.dumps({'candidate_files':len(records), 'dependencies':len(dependencies),
                      'missing_dependencies':len(missing), 'acceptance':'incomplete; dependency inventory only'},ensure_ascii=False))

if __name__ == '__main__': main()
