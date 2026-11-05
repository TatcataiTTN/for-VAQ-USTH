import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m07_gen.json'), encoding='utf-8')); orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m07.json'), encoding='utf-8'))
def val(s):
    s = s.replace('−', '-'); m = re.search(r'-?[\d,]*\.?\d+', s); v = float(m[0].replace(',', '')); u = s[m.end():].strip()
    return v * {'MHz': 1e6, 'kHz': 1e3, 'Hz': 1, 'kΩ': 1e3, 'Ω': 1, 'ms': 1e-3, 'μs': 1e-6, '%': 1, 'V': 1}.get(u.split(' ')[0], 1) if u else v
ok = lambda a, b: abs(a - b) <= 0.007 * abs(b) + 1e-12
chk = {}; fails = []
def check(it, exp, fam):
    a = val(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if not ok(a, exp): fails.append((fam, it['q']['en'][:70], a, exp))
for it in gen:
    q = it['q']['en']
    if it['kind'] != 'mcq': continue
    if (m := re.match(r'A Wien-bridge lead-lag network has R1 = R2 = ([\d.]+) kΩ and C1 = C2 = ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * float(m[1]) * 1e3 * float(m[2]) * 1e-6), 'lead-lag fr')
    elif (m := re.match(r'What R \(R1 = R2\) gives a Wien-bridge oscillator fr = (.+?) with C1 = C2 = ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * val(m[1]) * float(m[2]) * 1e-6), 'R for fr')
    elif (m := re.match(r'A three-section RC phase-shift oscillator has R = ([\d.]+) kΩ and C = ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * math.sqrt(6) * float(m[1]) * 1e3 * float(m[2]) * 1e-6), 'PS fr')
    elif (m := re.match(r'In a phase-shift oscillator with Ri = ([\d.]+) kΩ', q)): check(it, 29 * float(m[1]) * 1e3, 'Rf=29Ri')
    elif (m := re.match(r'The amplifier of a feedback oscillator has Av = (\d+)', q)): check(it, 1 / int(m[1]), 'B')
    elif (m := re.match(r'A lead-lag circuit at its resonant frequency has an input of ([\d.]+) V', q)): check(it, float(m[1]) / 3, 'lead-lag out')
    elif (m := re.match(r'A Colpitts oscillator has C1 = (\d+) pF, C2 = (\d+) pF and L = (\d+) mH', q)):
        c1, c2, l = int(m[1]), int(m[2]), int(m[3]); check(it, 1 / (2 * math.pi * math.sqrt(l * 1e-3 * c1 * c2 / (c1 + c2) * 1e-12)), 'Colpitts f')
    elif (m := re.match(r'The feedback capacitors of a Colpitts oscillator are C1 = (\d+) pF and C2 = (\d+) pF', q)): check(it, int(m[1]) / int(m[2]), 'Colpitts gain')
    elif (m := re.match(r'A 555 astable has R1 = ([\d.]+) kΩ, R2 = ([\d.]+) kΩ and Cext = ([\d.]+) μF', q)): check(it, 1.44 / ((float(m[1]) + 2 * float(m[2])) * 1e3 * float(m[3]) * 1e-6), '555 f')
    elif (m := re.match(r'A 555 astable has R1 = ([\d.]+) kΩ and R2 = ([\d.]+) kΩ\. What is the duty', q)): check(it, (float(m[1]) + float(m[2])) / (float(m[1]) + 2 * float(m[2])) * 100, '555 duty')
    elif (m := re.match(r'A 555 monostable has Rext = ([\d.]+) kΩ and Cext = ([\d.]+) μF', q)): check(it, 1.1 * float(m[1]) * 1e3 * float(m[2]) * 1e-6, '555 tW')
    elif (m := re.match(r'What are the two comparator reference voltages in a 555 timer when VCC = (\d+) V', q)):
        lo, hi = (val(x) for x in it['opts'][it['correct']]['en'].split(' and ')); chk['555 refs'] = chk.get('555 refs', 0) + 1
        if not (ok(lo, int(m[1]) / 3) and ok(hi, 2 * int(m[1]) / 3)): fails.append(('refs', q))
    elif (m := re.match(r'A sawtooth generator has VIN = (\d+) V, R = ([\d.]+) kΩ, C = ([\d.]+) μF and a period of (\d+) μs', q)): check(it, int(m[1]) / (float(m[2]) * 1e3 * float(m[3]) * 1e-6) * int(m[4]) * 1e-6, 'saw Vpp')
assert round(1 / 75, 4) == 0.0133 and round(2.2 / 3, 3) == 0.733 and round(1 / (2 * math.pi * math.sqrt(6) * 4.7e3 * 0.022e-6)) == 628 and round(29 * 4.7, 1) == 136.3
assert round(1.44 / (7.6e3 * 25e3) * 1e6, 4) == 0.0076 and round(470 / 47) == 10 and round(3.3 / 2, 2) == 1.65 and round((3.3 + 1.65) / (3.3 + 3.3), 2) == 0.75
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts'])
print('checked', chk, 'total', sum(chk.values()), 'of', len(gen)); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
