"""Independent recomputation of module 03 answers (parses question text)."""
import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m03_gen.json'), encoding='utf-8')); orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m03.json'), encoding='utf-8'))
def val(s):
    m = re.search(r'-?[\d,]*\.?\d+', s.replace('−', '-').replace('±', '')); return float(m.group(0).replace(',', ''))
def ok(a, b): return abs(a - b) <= 0.006 * abs(b) + 1e-9
chk = {}; fails = []
def check(it, exp, fam):
    a = val(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if not ok(a, exp): fails.append((fam, it['q']['en'][:70], a, exp))
for it in gen:
    q = it['q']['en']
    if it['kind'] != 'mcq': continue
    if (m := re.match(r'A comparator with positive feedback has R1 = ([\d.]+) kΩ, R2 = ([\d.]+) kΩ and Vout\(max\) = ±(\d+) V\. What is VUTP', q)): check(it, float(m[2]) / (float(m[1]) + float(m[2])) * float(m[3]), 'VUTP')
    elif (m := re.match(r'A comparator with positive feedback has R1 = ([\d.]+) kΩ, R2 = ([\d.]+) kΩ and Vout\(max\) = ±(\d+) V\. What is the hyst', q)): check(it, 2 * float(m[2]) / (float(m[1]) + float(m[2])) * float(m[3]), 'VHYS')
    elif (m := re.match(r'A comparator is bounded .* ([\d.]+) V zener', q)): check(it, float(m[1]) + 0.7, 'bound')
    elif (m := re.match(r'A comparator has Vin = (-?[\d.]+) V .* Vref = (-?[\d.]+) V', q)):
        exp = '+Vout(max)' if float(m[1]) > float(m[2]) else '−Vout(max)'; chk['cmp'] = chk.get('cmp', 0) + 1
        if it['opts'][it['correct']]['en'] != exp: fails.append(('cmp', q[:60]))
    elif (m := re.match(r'A summing amplifier has Ri = ([\d.]+) kΩ on every input, Rf = ([\d.]+) kΩ and inputs ([\d., ]+) V', q)): check(it, -float(m[2]) / float(m[1]) * sum(float(x) for x in m[3].split(',')), 'sum')
    elif (m := re.match(r'To average (\d+) inputs .* Ri = ([\d.]+) kΩ', q)): check(it, float(m[2]) / int(m[1]), 'avg')
    elif (m := re.match(r'In a scaling adder with Rf = ([\d.]+) kΩ, .* weight \(gain\) of (\d+)', q)): check(it, float(m[1]) / int(m[2]), 'scale')
    elif (m := re.match(r'An integrator has R = ([\d.]+) kΩ and C = ([\d.]+) μF and a (\d+) V step', q)): check(it, -float(m[3]) / (float(m[1]) * 1e3 * float(m[2]) * 1e-6) / 1e3, 'ramp')
    elif (m := re.match(r'An integrator \(R = ([\d.]+) kΩ, C = ([\d.]+) μF\) .* receives (\d+) V for (\d+) ms', q)): check(it, -float(m[3]) * float(m[4]) * 1e-3 / (float(m[1]) * 1e3 * float(m[2]) * 1e-6), 'int V')
    elif (m := re.match(r'A triangular wave of (\d+) V peak-to-peak and period (\d+) μs .* Rf = ([\d.]+) kΩ and C = ([\d.]+) μF', q)): check(it, float(m[3]) * 1e3 * float(m[4]) * 1e-6 * float(m[1]) / (float(m[2]) / 2 * 1e-6), 'diff')
# originals / book answers
get = lambda n: next(i for i in orig if i['kind'] == 'mcq' and i['src']['en'].startswith(f'Floyd 9e, Ch.13, Self-Test Q{n} '))
assert round(18 / 65 * 10, 2) == 2.77 and round(80000 * 0.15e-3 * math.sqrt(2), 1) == 17.0 and 17.0 > 12   # clipping -> 24 Vpp
assert 1 / 5 == 0.2 and get(10)['opts'][get(10)['correct']]['en'] == '0.2' and get(9)['opts'][get(9)['correct']]['en'] == '4.7 kΩ'
assert round(5 / (56e3 * 0.022e-6)) == 4058 and round(15e3 * 0.047e-6 * 4000, 2) == 2.82 and 5 / (10e3 * 10e-6) * 0.01 == 0.5
assert round(2 + 10 / 33 * 3 + 10 / 91 * 3 + 10 / 180 * 6, 3) == 3.572 and 100 / 8 == 12.5 and 10 / 8 == 1.25
assert [100 / w for w in (1, 2, 4, 8, 16, 32)] == [100, 50, 25, 12.5, 6.25, 3.125]
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('generated numeric families checked:', chk, 'total', sum(chk.values()), 'of', len(gen)); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
