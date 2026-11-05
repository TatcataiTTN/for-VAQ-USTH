"""Grounding check for module 10: each item's evidence regex must occur in the cited source page (EASA OCR PDF or SERVOMECHANISM (sv).pdf)."""
import json, os, re, sys, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EASA = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'EASA_M04_Electronics_Fundamentals_ocr.pdf'); SV = os.path.join(ROOT, '..', 'SERVOMECHANISM (sv).pdf')
import fitz; fitz.TOOLS.mupdf_display_errors(False); svdoc = fitz.open(SV)
cache = {}
def page(src, n):
    k = (src, n)
    if k not in cache:
        cache[k] = re.sub(r'\s+', ' ', svdoc[n - 1].get_text('text') if src == 'SV' else subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), EASA, '-'], capture_output=True, text=True).stdout)
    return cache[k]
ev = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm10_evidence.json'), encoding='utf-8'))
items = json.load(open(os.path.join(ROOT, 'data/qsrc/m10.json'), encoding='utf-8')) + json.load(open(os.path.join(ROOT, 'data/qsrc/m10_gen.json'), encoding='utf-8'))
fails = []; n = 0
calc = json.load(open(os.path.join(ROOT, 'data/qsrc/m10_calc_gen.json'), encoding='utf-8'))
for it in items:
    e = ev.get(it['q']['en'])
    if not e: fails.append(('no evidence', it['q']['en'][:60])); continue
    n += 1
    if not re.search(e['rx'], page(e['src'], e['page']), re.I):
        near = ' '.join(page(e['src'], p) for p in (e['page'] - 1, e['page'] + 1) if 1 <= p)
        fails.append(('adjacent page' if re.search(e['rx'], near, re.I) else 'NOT FOUND', e['src'], e['page'], e['rx'][:60], it['q']['en'][:45]))
def val(x): return float(re.search(r'-?[\d,]*\.?\d+', x.replace('−', '-'))[0].replace(',', ''))
nc = 0
for it in calc:
    q = it['q']['en']; a = val(it['opts'][it['correct']]['en'])
    if (m := re.match(r'A velocity servo has equal summing resistors R2 = R3, a motor turning ([\d.]+) rpm per volt of error and a tachometer giving ([\d.]+) V per rpm. The control input is −([\d.]+) V', q)):
        K, t, v = (float(m[i]) for i in (1, 2, 3)); e = K * v / (2 + K * t)
    elif (m := re.match(r'In the same velocity servo \(control −([\d.]+) V', q)): e = -float(m[1]) / 2
    elif (m := re.match(r'In a dc position servo with equal summing resistors R2 = R3, the input wiper gives (-?\d+) V and the feedback wiper gives (-?\d+) V', q)): e = (int(m[1]) + int(m[2])) / 2
    elif (m := re.match(r'A synchro has a 2.2:1 step-down .* With ([\d.]+) V on the rotor', q)): e = float(m[1]) / 2.2
    else: fails.append(('unparsed', q[:50])); continue
    nc += 1
    if abs(a - e) > 0.01 * abs(e) + 1e-9: fails.append(('calc', q[:60], a, e))
assert abs(10 * 9 / (2 + 10 * 0.1) - 30) < 1e-9 and abs((10 + 0) / 2 - 5) < 1e-9 and abs(115 / 2.2 - 52.27) < 0.01
print('calc items verified:', nc, 'of', len(calc))
for it in items:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('items checked:', n, 'of', len(items)); print('FAILS:'); [print(' ', f) for f in fails] if fails else print('  none'); sys.exit(1 if fails else 0)
