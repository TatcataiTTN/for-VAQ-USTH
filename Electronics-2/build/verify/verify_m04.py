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
# ---- Floyd answers printed at the back of the book (odd problems, pp.935-937) vs the worked solutions
sol = {i['src']['en']: i['sol']['en'] for i in orig if i['kind'] == 'ess'}
s35 = sol['Floyd 9e, Ch.6, Problem 35 (p.331)']
assert all(x in s35 for x in ('1.413', '1.995', '3.162', '(d) 10 ', '(e) 100')) and [round(10 ** (d / 20), 2) for d in (3, 6, 10, 20, 40)] == [1.41, 2.0, 3.16, 10.0, 100.0]      # book: 1.41, 2.00, 3.16, 10.0, 100
assert '0.45 mW' in sol['Floyd 9e, Ch.7, Problem 19 (p.379)'] and round(0.10 * 0.18 * 25e-3 * 1e6) == 450                                                                      # book: 450 uW
assert '24 V' in sol['Floyd 9e, Ch.7, Problem 21 (p.379)'] and 2 * 12 == 24                                                                                                    # book: 24 V
# ---- Circuit-Action items: independent circuit models (exact Thevenin bias, no book shortcuts); only the DIRECTION of change is asserted
def sgn(a, b, rel=1e-3): return 0 if abs(b - a) <= rel * abs(a) else (1 if b > a else -1)       # 1 = increase, -1 = decrease, 0 = no change
def f634(r4):                       # Fig 6-34, beta = 150, VCC = 10 V: |overall gain|
    b = 150; vth = 10 * 10e3 / 57e3; rth = 1 / (1 / 47e3 + 1 / 10e3)
    ie = (b + 1) * (vth - 0.7) / (rth + (b + 1) * r4); re = 0.025 / ie
    rc1 = 1 / (1 / 4.7e3 + 1 / 47e3 + 1 / 10e3 + 1 / (b * re)); return (rc1 / re) * (4.7e3 / re)
def f75(r3=5.6e3, re2=560.0, r4=22e3, c2=True):   # Fig 7-5, beta_ac = 200: (|Av1|, dc emitter voltage of Q1, dc base voltage of Q3)
    b = 200; vth = 12 * 10e3 / 66e3; rth = 1 / (1 / 56e3 + 1 / 10e3)
    ie1 = (b + 1) * (vth - 0.7) / (rth + (b + 1) * (68 + re2)); ve1 = ie1 * (68 + re2)      # dc: every capacitor (C2 included) is an open circuit, so c2 does not enter
    re = 0.025 / ie1; rin2 = b * b * (33 * 8 / 41); rc1 = 1 / (1 / 4.7e3 + 1 / r3 + 1 / r4 + 1 / rin2)
    vt2 = 12 * r4 / (r3 + r4); rt2 = 1 / (1 / r3 + 1 / r4); vb2 = vt2
    for _ in range(60): ie3 = (vb2 - 1.4) / 33; vb2 = vt2 - rt2 * ie3 / (b + 1) ** 2      # Darlington base current = IE3/(beta+1)^2
    return rc1 / (68 + re), ve1, vb2 - 0.7
fr = lambda c: 1 / (2 * math.pi * math.sqrt(10e-3 * c))
expect = {   # (chapter, question) -> sign of the change the book asks about
 (6, 9): 0, (6, 10): sgn(f634(1000), f634(500)),
 (7, 1): sgn(f75()[0], f75(r3=2.7e3)[0]), (7, 2): sgn(f75()[0], f75(re2=1000)[0]), (7, 3): sgn(f75()[1], f75(c2=False)[1]), (7, 4): sgn(f75()[2], f75(r4=33e3)[2]),
 (7, 5): sgn(20 / 2, 24 / 2), (7, 6): sgn(20 ** 2 / (8 * 8), 20 ** 2 / (8 * 16)), (7, 7): sgn(8 / (8 + 1), 4 / (4 + 1)), (7, 8): sgn(20 ** 2 / (8 * 8), 24 ** 2 / (8 * 8)), (7, 10): sgn(fr(0.001e-6), fr(0.0005e-6))}
# calibration: the exact model also counts the base currents the book neglects, so it sits a few % below the book (13,495 / 27.9 / VE1 = 1.12 V / VB(Q2) = 9.57 V)
assert 12100 < f634(1000) < 14300 and abs(f75()[0] - 27.9) < 0.8 and abs(f75()[2] + 0.7 - 9.57) < 0.1 and abs(f75()[1] - 1.12) < 0.1
ca = [i for i in orig if i['kind'] == 'ca']; seen = set()
for it in ca:
    m = re.match(r'Floyd 9e, Ch\.(\d+), Circuit-Action Quiz Q(\d+) \(p\.(\d+)\)', it['src']['en']); key = (int(m[1]), int(m[2])); seen.add(key)
    want = {1: 0, -1: 1, 0: 2}[expect[key]]                     # option order is Increase / Decrease / Not change
    if it['correct'] != want: fails.append(('circuit-action', key, 'item says', it['correct'], 'model says', want))
    if not os.path.exists(os.path.join(ROOT, it['fig'])): fails.append(('circuit-action figure missing', it['fig']))
if seen != set(expect): fails.append(('circuit-action set', sorted(seen ^ set(expect))))
print('Circuit-Action items checked against the circuit model:', len(ca), '| directions:', {k: v for k, v in sorted(expect.items())})
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('EASA-grounded items:', n_ev, '| numeric families:', chk, 'total numeric', sum(chk.values())); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
