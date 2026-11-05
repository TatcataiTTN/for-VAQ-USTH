import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m08_gen.json'), encoding='utf-8')); orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m08.json'), encoding='utf-8'))
def val(s): return float(re.search(r'-?[\d,]*\.?\d+(?:e-?\d+)?', s.replace('−', '-'))[0].replace(',', ''))
ok = lambda a, b: abs(a - b) <= 0.01 * abs(b) + 1e-9
chk = {}; fails = []
def check(it, exp, fam):
    a = val(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if not ok(a, exp): fails.append((fam, it['q']['en'][:70], a, exp))
for it in gen:
    q = it['q']['en']
    if it['kind'] != 'mcq': continue
    if (m := re.match(r'A regulator \(nominal output (\d+) V\) changes ([\d.]+) mV when VIN goes from (\d+) V to (\d+) V', q)): check(it, float(m[2]) * 1e-3 / (int(m[4]) - int(m[3])) * 100 / (int(m[4]) - int(m[3])), 'line %/V')
    elif (m := re.match(r'A regulator has VNL = ([\d.]+) V and VFL = ([\d.]+) V', q)): check(it, (float(m[1]) - float(m[2])) / float(m[2]) * 100, 'load %')
    elif (m := re.match(r'A series regulator has R2 = ([\d.]+) kΩ, R3 = ([\d.]+) kΩ and a reference of ([\d.]+) V', q)): check(it, (1 + float(m[1]) / float(m[2])) * float(m[3]), 'VOUT series')
    elif (m := re.match(r'A series regulator with VREF = ([\d.]+) V and R3 = ([\d.]+) kΩ must give VOUT = (\d+) V', q)): check(it, (int(m[3]) / float(m[1]) - 1) * float(m[2]), 'R2 design')
    elif (m := re.match(r'A current-limiting resistor must hold the load current to (\d+) mA', q)): check(it, 0.7 / (int(m[1]) * 1e-3), 'Rlimit')
    elif (m := re.match(r'In a shunt regulator with series resistor R1 = (\d+) Ω, VIN changes by ([\d.]+) V', q)): check(it, float(m[2]) / int(m[1]) * 1e3, 'shunt dI')
    elif (m := re.match(r'A shunt regulator has R1 = (\d+) Ω and VIN\(max\) = (\d+) V', q)): check(it, int(m[2]) ** 2 / int(m[1]), 'shunt P')
    elif (m := re.match(r'A switching regulator transistor runs at (\d+) kHz with an off-time of (\d+) μs', q)): t = 1000 / int(m[1]); check(it, (t - int(m[2])) / t * 100, 'duty')
    elif (m := re.match(r'A step-down switching regulator with VIN = (\d+) V runs at a duty cycle of ([\d.]+) %', q)): check(it, int(m[1]) * float(m[2]) / 100, 'buck VOUT')
    elif (m := re.match(r'An LM317 has R1 = ([\d.]+) (kΩ|Ω) and R2 = ([\d.]+) (kΩ|Ω)', q)):
        r1, r2 = float(m[1]), float(m[3]); k = 1e3 if m[4] == 'kΩ' else 1; check(it, 1.25 * (1 + r2 / r1) + 50e-6 * r2 * k, 'LM317')
    elif (m := re.match(r'What is the output voltage of a (\d{4}) IC regulator', q)):
        exp = ('+' if m[1][1] == '8' else '−') + str(int(m[1][2:])) + ' V'; chk['78/79'] = chk.get('78/79', 0) + 1
        if it['opts'][it['correct']]['en'] != exp: fails.append(('78/79', q, exp))
    elif (m := re.match(r'In a 78XX circuit with an external pass transistor, what Rext limits the internal regulator current to (\d+) mA', q)): check(it, 0.7 / (int(m[1]) * 1e-3), 'Rext')
assert round(2e-3 / 6 * 100, 4) == 0.0333 and round(0.1 / 9.9 * 100, 2) == 1.01 and round((1 + 5.6 / 2.2) * 2.4, 2) == 8.51 and round((1 + 5.6 / 2.2) * 2.7, 2) == 9.57
assert round(0.7 / 1.4 * 1e3) == 500 and round(1 / 100 * 1e3) == 10 and 25 ** 2 / 100 == 6.25 and round(1.25 * 11 + 0.5, 2) == 14.25 and round(14.25 / 11e3 * 1e3, 1) == 1.3 and round(0.7 / 0.25, 1) == 2.8 and 0.7 / 2 == 0.35
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts'])
print('checked', chk, 'total', sum(chk.values()), 'of', len(gen)); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
