"""Module 04 verification: EASA evidence + independent recomputation of the numeric families + Floyd answers."""
import json, os, re, math, sys, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EASA = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'EASA_M04_Electronics_Fundamentals_ocr.pdf')
cache = {}
def page(n):
    if n not in cache: cache[n] = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), EASA, '-'], capture_output=True, text=True).stdout)
    return cache[n]
ev = json.load(open(os.path.join(ROOT, 'data/verify/m04_evidence.json'), encoding='utf-8'))
orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m04.json'), encoding='utf-8')); gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m04_gen.json'), encoding='utf-8'))
fails = []; n_ev = 0; chk = {}
def val(x): return float(re.search(r'-?[\d,]*\.?\d+', x.replace('−', '-'))[0].replace(',', ''))
def check(it, e, fam, tol=0.006):
    a = val(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if abs(a - e) > tol * abs(e) + 1e-9: fails.append((fam, it['q']['en'][:60], a, e))
for it in gen:
    if it['kind'] == 'ess': continue
    q = it['q']['en']; e = ev.get(q)
    if e:
        n_ev += 1
        if not re.search(e['rx'], page(e['page']), re.I): fails.append(('evidence', e['page'], e['rx'][:50], q[:50]))
        continue
    if (m := re.match(r'A cascade has stage voltage gains of ([\d, ]+)\.', q)): check(it, math.prod(int(x) for x in m[1].split(',')), 'product')
    elif (m := re.match(r'Express a voltage gain of (\d+) in decibels', q)): check(it, 20 * math.log10(int(m[1])), 'dB')
    elif (m := re.match(r'Stages of ([\d, ]+) dB are cascaded', q)): check(it, 10 ** (sum(int(x) for x in m[1].split(',')) / 20), 'dB sum')
    elif (m := re.match(r'Two cascaded stages have Av1 = (\d+) and Av2 = (\d+).* passes ([\d.]+) of', q)): check(it, int(m[1]) * int(m[2]) * float(m[3]), 'loaded')
    elif (m := re.match(r'An amplifier has open-loop gain A = ([\d,]+) and .* B = (\d*\.?\d+)', q)): A = int(m[1].replace(',', '')); B = float(m[2]); check(it, A / (1 + A * B), 'feedback')
    elif (m := re.match(r'A feedback oscillator amplifier has Av = (\d+)', q)): check(it, 1 / int(m[1]), 'B=1/Av')
    elif (m := re.match(r'A two-supply class B push-pull amplifier has VCC = (\d+) V and RL = (\d+)', q)): check(it, int(m[1]) / int(m[2]), 'Ic(sat)')
    elif (m := re.match(r'A class C transistor is on for (\d+) % .* Vce\(sat\) = ([\d.]+) V and Ic\(sat\) = (\d+) mA', q)): check(it, int(m[1]) / 100 * float(m[2]) * int(m[3]), 'PD class C')
    elif (m := re.match(r'What is the resonant frequency of a tank circuit with L = ([\d.]+) mH and C = ([\d.]+)', q)): check(it, 1 / (2 * math.pi * math.sqrt(float(m[1]) * 1e-3 * float(m[2]) * 1e-6)) / 1e3, 'tank')
    elif (m := re.match(r'An RC-coupled stage has a total resistance of ([\d.]+) kΩ seen by a ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * float(m[1]) * 1e3 * float(m[2]) * 1e-6), 'RC fc')
    else: fails.append(('unparsed', q[:60]))
assert round(1000 ** (1 / 3)) == 10 and round(1 / 50 - 1 / 100000, 5) == 0.01999 and round(1 / (2 * math.pi * 20 * 4.7e3) * 1e6, 2) == 1.69
assert 15 ** 4 == 50625 and round(20 * math.log10(50625), 1) == 94.1 and 20 / 50 == 0.4 and round(1 / (2 * math.pi * math.sqrt(10e-3 * 0.001e-6)) / 1e3, 2) == 50.33
assert round(10 ** 1.5, 1) == 31.6 and round(0.1 * 0.18 * 25, 2) == 0.45
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('EASA-grounded items:', n_ev, '| numeric families:', chk, 'total numeric', sum(chk.values())); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
