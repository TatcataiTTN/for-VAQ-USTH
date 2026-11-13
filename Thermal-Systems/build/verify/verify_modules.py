"""P1 gate: every slide of every deck has exactly one module, or is listed as out of scope / blank (with a reason); every CLO has a module.
Counts come from build/modules.py and the PDF page counts in DECKS (checked against pdfinfo when the PDFs are reachable)."""
import os, sys, subprocess, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from modules import MODS, DECKS, OUT_OF_SCOPE, CLO, TUT
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))      # .../USTH Thermal System
bad = []
owner = collections.defaultdict(list)
for m in MODS:
    for d, a, b in m['slides']:
        for p in range(a, b + 1): owner[(d, p)].append(m['id'])
    for d, a, b in m['blank_slides']:
        for p in range(a, b + 1): owner[(d, p)].append('blank:' + m['id'])
for d, a, b, why in OUT_OF_SCOPE:
    for p in range(a, b + 1): owner[(d, p)].append('out')
for d, info in DECKS.items():
    n = info['pages']
    pdf = os.path.join(ROOT, info['pdf'])
    if os.path.exists(pdf):
        out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
        real = int([l for l in out.splitlines() if l.startswith('Pages:')][0].split()[1])
        if real != n: bad.append(f'{d}: DECKS says {n} pages, pdfinfo says {real}')
    for p in range(1, n + 1):
        o = owner.get((d, p), [])
        if len(o) == 0: bad.append(f'{d} p{p}: no module')
        elif len(o) > 1: bad.append(f'{d} p{p}: several owners {o}')
used = set(c for m in MODS for c in m['clo'])
for c in CLO:
    if c not in used: bad.append(f'{c}: no module')
tot = sum(i['pages'] for i in DECKS.values())
by = collections.Counter(o[0].split(':')[0] for o in owner.values() if o)
print('slides total', tot, '| by owner', dict(sorted(by.items())))
for t in TUT: assert t['module'] in {m['id'] for m in MODS}
print('FAILS:', 'none' if not bad else ''); [print(' ', b) for b in bad]
sys.exit(1 if bad else 0)
