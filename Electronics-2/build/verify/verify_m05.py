import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m05_gen.json'), encoding='utf-8')); orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m05.json'), encoding='utf-8'))
def val(s):
    m = re.search(r'-?[\d,]*\.?\d+', s.replace('−', '-')); return float(m.group(0).replace(',', ''))
ok = lambda a, b: abs(a - b) <= 0.006 * abs(b) + 1e-9
chk = {}; fails = []
def check(it, exp, fam):
    a = val(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if not ok(a, exp): fails.append((fam, it['q']['en'][:70], a, exp))
for it in gen:
    q = it['q']['en']
    if it['kind'] != 'mcq': continue
    if (m := re.match(r'An AD622 .* has RG = ([\d.]+) kΩ', q)): check(it, 1 + 50.5 / float(m[1]), 'AD622 G')
    elif (m := re.match(r'What RG must an AD622 use for a gain of (\d+)', q)): check(it, 50.5e3 / (int(m[1]) - 1), 'RG')
    elif (m := re.match(r'A three-op-amp .* R1 = R2 = (\d+) kΩ, RG = ([\d.]+) kΩ', q)): check(it, 1 + 2 * float(m[1]) / float(m[2]), 'IA gain')
    elif (m := re.match(r'An instrumentation amplifier \(gain ([\d.]+)\) has Vin1 = ([\d.]+) mV, Vin2 = ([\d.]+) mV', q)): check(it, float(m[1]) * (float(m[3]) - float(m[2])) * 1e-3, 'IA vout')
    elif (m := re.match(r'An isolation amplifier has an input-stage gain of (\d+) and an output-stage gain of (\d+)', q)): check(it, int(m[1]) * int(m[2]), 'iso')
    elif (m := re.match(r'An OTA has an input of (\d+) mV and an output current of (\d+) μA', q)): check(it, int(m[2]) / int(m[1]) * 1000, 'gm')
    elif (m := re.match(r'An OTA has gm = (\d+) μS, RL = ([\d.]+) kΩ and Vin = (\d+) mV', q)): check(it, float(m[1]) * 1e-6 * float(m[3]) * 1e-3 * float(m[2]) * 1e3, 'OTA Vout')
    elif (m := re.match(r'An OTA has K = (\d+) μS/μA and a bias current of (\d+) μA', q)): check(it, int(m[1]) * int(m[2]), 'K*I')
    elif (m := re.match(r'A log amplifier .* Vin = ([\d.]+) V, R = (\d+) kΩ and IR = (\d+) nA', q)): check(it, -0.025 * math.log(float(m[1]) / (float(m[2]) * 1e3 * float(m[3]) * 1e-9)) * 1e3, 'log amp')
    elif (m := re.match(r'What is log₁₀ of ([\d.]+)\?', q)): check(it, math.log10(float(m[1])), 'log10')
assert (1 + 2 * 100e3 / 1e3) == 201 and round(201 * 5e-3, 6) == 1.005 and 1 + 50.5 == 51.5 and 30 * 10 == 300 and round(5000e-6 * 0.1, 9) == 5e-4 and round(5e-4 * 10e3, 6) == 5
assert round(200e3 / 999) == 200 and round(-0.025 * math.log(1.5 / (47e3 * 60e-9)) * 1e3) == -157 and [round(math.log10(x), 3) for x in (0.5, 2)] == [-0.301, 0.301]
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts'])
print('checked', chk, 'total', sum(chk.values()), 'of', len(gen)); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
