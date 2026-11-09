"""Grounding check for module 09: every item's evidence regex must occur in the EASA OCR text of the cited PDF page."""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
import subprocess, functools
PDF = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'EASA_M04_Electronics_Fundamentals_ocr.pdf')
class Pages(dict):
    def get(self, n, d=''):
        if n not in self: self[n] = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), PDF, '-'], capture_output=True, text=True).stdout)   # reading order (columns kept together)
        return self[n]
pages = Pages()
ev = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm09_evidence.json'), encoding='utf-8'))
ev.update(json.load(open(os.path.join(ROOT, 'data', 'verify', 'm09_l2_evidence.json'), encoding='utf-8')))          # the 39 level-2 questions of build/gen/gen_m09_l2.py
items = json.load(open(os.path.join(ROOT, 'data/qsrc/m09.json'), encoding='utf-8')) + json.load(open(os.path.join(ROOT, 'data/qsrc/m09_gen.json'), encoding='utf-8')) + json.load(open(os.path.join(ROOT, 'data/qsrc/m09_zl2.json'), encoding='utf-8'))
calc = json.load(open(os.path.join(ROOT, 'data/qsrc/m09_calc_gen.json'), encoding='utf-8'))
fails = []; n = 0
for it in items:
    e = ev.get(it['q']['en'])
    if not e: fails.append(('no evidence', it['q']['en'][:60])); continue
    n += 1
    near = ' '.join(pages.get(p, '') for p in (e['page'] - 1, e['page'], e['page'] + 1))   # tolerate off-by-one PDF page
    if not re.search(e['rx'], pages.get(e['page'], ''), re.I): fails.append(('not on cited page' if re.search(e['rx'], near, re.I) else 'NOT FOUND', e['page'], e['rx'], it['q']['en'][:50]))
import math
RHO = 1.68e-8; EPS0 = 8.854e-12; nc = 0
def val(x): return float(re.search(r'-?[\d,]*\.?\d+(?:e-?\d+)?', x.replace('−', '-'))[0].replace(',', ''))
for it in calc:
    q = it['q']['en']; a = val(it['opts'][it['correct']]['en'])
    if (m := re.match(r'A copper trace is ([\d.]+) mm long, ([\d.]+) mm wide and ([\d.]+) μm thick', q)): e = RHO * float(m[1]) * 1e-3 / (float(m[2]) * 1e-3 * float(m[3]) * 1e-6)
    elif (m := re.match(r'A ([\d.]+) mm × ([\d.]+) mm × ([\d.]+) μm copper trace carries ([\d.]+) A', q)): e = float(m[4]) * RHO * float(m[1]) * 1e-3 / (float(m[2]) * 1e-3 * float(m[3]) * 1e-6) * 1e3
    elif (m := re.match(r'Two parallel copper areas of ([\d.]+) cm² .* ([\d.]+) mm of FR-4 \(εr = ([\d.]+)\)', q)): e = EPS0 * float(m[3]) * float(m[1]) * 1e-4 / (float(m[2]) * 1e-3) * 1e12
    else: fails.append(('unparsed calc', q[:50])); continue
    nc += 1
    if abs(a - e) > 0.01 * abs(e): fails.append(('calc', q[:50], a, e))
print('calc items verified:', nc, 'of', len(calc))
for it in items:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('items checked:', n, 'of', len(items)); print('FAILS:'); [print(' ', f) for f in fails] if fails else print('  none'); sys.exit(1 if fails else 0)
