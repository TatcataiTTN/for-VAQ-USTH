import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m06_gen.json'), encoding='utf-8')); orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m06.json'), encoding='utf-8'))
def hzv(s):
    m = re.search(r'([\d.,]+)\s*(kHz|Hz|kΩ|Ω)', s.replace('−', '-')); v = float(m[1].replace(',', '')); return v * (1e3 if m[2] in ('kHz', 'kΩ') else 1)
def num(s): return float(re.search(r'-?[\d,]*\.?\d+', s.replace('−', '-'))[0].replace(',', ''))
ok = lambda a, b: abs(a - b) <= 0.006 * abs(b) + 1e-9
chk = {}; fails = []
def check(it, exp, fam, fn=num):
    a = fn(it['opts'][it['correct']]['en']); chk[fam] = chk.get(fam, 0) + 1
    if not ok(a, exp): fails.append((fam, it['q']['en'][:70], a, exp))
for it in gen:
    q = it['q']['en']
    if it['kind'] != 'mcq': continue
    if (m := re.match(r'A single-pole RC filter has R = ([\d.]+) kΩ and C = ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * float(m[1]) * 1e3 * float(m[2]) * 1e-6), 'fc', hzv)
    elif (m := re.match(r'An equal-value low-pass RC section needs fc = (.+?) with C = ([\d.]+) μF', q)): check(it, 1 / (2 * math.pi * hzv(m[1]) * float(m[2]) * 1e-6), 'R', hzv)
    elif (m := re.match(r'A band-pass filter has critical frequencies (.+?) and (.+?)\. What is its bandwidth', q)): check(it, hzv(m[2]) - hzv(m[1]), 'BW', hzv)
    elif (m := re.match(r'A band-pass filter has critical frequencies (.+?) and (.+?)\. What is its Q', q)): check(it, math.sqrt(hzv(m[1]) * hzv(m[2])) / (hzv(m[2]) - hzv(m[1])), 'Q')
    elif (m := re.match(r'A filter has Q = (\d+) and a bandwidth of (.+?)\. What is the center', q)): check(it, int(m[1]) * hzv(m[2]), 'f0', hzv)
    elif (m := re.match(r'What is the roll-off rate of an (\d)-pole', q)): check(it, -20 * int(m[1]), 'roll')
    elif (m := re.match(r'How many poles are needed for a roll-off of −(\d+)', q)): check(it, int(m[1]) / 20, 'poles')
    elif (m := re.match(r'For a Sallen-Key stage, what R1/R2 gives a damping factor of ([\d.]+)', q)): check(it, 2 - float(m[1]), 'R1/R2')
    elif (m := re.match(r'A Sallen-Key stage has R1 = ([\d.]+) kΩ and R2 = ([\d.]+) kΩ', q)): check(it, 2 - float(m[1]) / float(m[2]), 'DF')
    elif (m := re.match(r'A multiple-feedback band-pass filter has R1 = ([\d.]+) kΩ, R2 = ([\d.]+) kΩ, R3 = ([\d.]+) kΩ and C1 = C2 = ([\d.]+) μF. What is its (bandwidth|center)', q)):
        r1, r2, r3, c = (float(m[i]) for i in (1, 2, 3, 4)); c *= 1e-6
        if m[5] == 'bandwidth': check(it, 1 / (math.pi * r2 * 1e3 * c), 'MFB BW', hzv)
        else: check(it, 1 / (2 * math.pi * c) * math.sqrt((r1 + r3) * 1e3 / (r1 * 1e3 * r2 * 1e3 * r3 * 1e3)), 'MFB f0', hzv)
    elif (m := re.match(r'A high-pass filter \(fc = (.+?)\) is cascaded with a low-pass filter \(fc = (.+?)\)', q)): check(it, hzv(m[2]) - hzv(m[1]), 'cascade BW', hzv)
assert round(1 / (2 * math.pi * 2.2e3 * 0.0015e-6) / 1e3, 1) == 48.2 and round(math.sqrt(3.2e3 * 3.9e3) / 700, 2) == 5.05
f19 = 1 / (2 * math.pi * 0.022e-6) * math.sqrt((47e3 + 1.8e3) / (47e3 * 150e3 * 1.8e3)); b19 = 1 / (math.pi * 150e3 * 0.022e-6)
assert round(f19) == 449 and abs(b19 - 96.4) < 0.1 and [round(2 - d, 3) for d in (1.932, 1.414, 0.518)] == [0.068, 0.586, 1.482]
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts'])
print('checked', chk, 'total', sum(chk.values()), 'of', len(gen)); print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
