"""Independent re-computation of module 02 answers. Parses each question text, recomputes, asserts against the option marked correct."""
import json, os, re, math, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m02_gen.json'), encoding='utf-8'))
orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m02.json'), encoding='utf-8'))
num = lambda s: float(s.replace(',', ''))
def val(s):
    m = re.search(r'-?[\d,]*\.?\d+', s.replace('−', '-')); return float(m.group(0).replace(',', ''))
def ok(a, b, tol=0.006): return abs(a - b) <= tol * max(1e-12, abs(b)) + 1e-9
checked = {}; fails = []
def check(it, expected, fam):
    ans = val(it['opts'][it['correct']]['en'])
    checked[fam] = checked.get(fam, 0) + 1
    if not ok(ans, expected): fails.append((fam, it['q']['en'], ans, expected))
for it in gen:
    q = it['q']['en']; m = None
    if (m := re.match(r'An op-amp has Aol = ([\d,]+) and Acm = ([\d.]+)\. What is the CMRR in decibels', q)): check(it, 20 * math.log10(num(m[1]) / float(m[2])), 'CMRR dB')
    elif (m := re.match(r'An op-amp has Aol = ([\d,]+) and CMRR = (\d+) dB', q)): check(it, num(m[1]) / 10 ** (int(m[2]) / 20), 'Acm')
    elif (m := re.match(r'The output of an op-amp changes by (\d+) V in (\d+) μs', q)): check(it, int(m[1]) / int(m[2]), 'slew')
    elif (m := re.match(r'How long .* slew rate of ([\d.]+) V/μs take to change by (\d+) V', q)): check(it, int(m[2]) / float(m[1]), 'time')
    elif (m := re.match(r'The input currents of an op-amp are ([\d.]+) μA and ([\d.]+) μA\. What is the input offset', q)): check(it, abs(float(m[1]) - float(m[2])), 'IOS')
    elif (m := re.match(r'The input currents of an op-amp are ([\d.]+) μA and ([\d.]+) μA\. What is the bias', q)): check(it, (float(m[1]) + float(m[2])) / 2, 'IBIAS')
    elif (m := re.match(r'A noninverting amplifier has Rf = ([\d.]+) kΩ and Ri = ([\d.]+) kΩ\. What is the closed', q)): check(it, 1 + float(m[1]) / float(m[2]), 'Acl NI')
    elif (m := re.match(r'An inverting amplifier has Rf = ([\d.]+) kΩ and Ri = ([\d.]+) kΩ\. What is the output for Vin = (\d+) mV', q)): check(it, -float(m[1]) / float(m[2]) * int(m[3]), 'Vout inv')
    elif (m := re.match(r'A noninverting amplifier has Rf = ([\d.]+) kΩ and Ri = ([\d.]+) kΩ\. What is the feedback fraction', q)): check(it, float(m[2]) / (float(m[1]) + float(m[2])), 'B')
    elif (m := re.match(r'Find Rf for a (inverting|noninverting) amplifier with Ri = ([\d.]+) kΩ and \|Acl\| = (\d+)', q)): check(it, float(m[3]) * float(m[2]) if m[1] == 'inverting' else (float(m[3]) - 1) * float(m[2]), 'Rf')
    elif (m := re.match(r'An op-amp has a unity-gain frequency of ([\d.]+) MHz\. .* Acl = (\d+)', q)):
        exp = float(m[1]) * 1e6 / int(m[2]); s = it['opts'][it['correct']]['en']; a = val(s) * (1e6 if 'MHz' in s else 1e3); checked['BW'] = checked.get('BW', 0) + 1
        if not ok(a, exp): fails.append(('BW', q, a, exp))
    elif (m := re.match(r'Aol = (\d+) dB, fc\(ol\) = (\d+) Hz and fc\(cl\) = ([\d,]+) Hz', q)): check(it, 20 * math.log10(10 ** (int(m[1]) / 20) / (num(m[3]) / int(m[2]))), 'Acl dB')
    elif (m := re.match(r'An RC lag circuit has fc = ([\d,]+) Hz\. What is the phase shift at ([\d,]+) Hz', q)): check(it, -math.degrees(math.atan(num(m[2]) / num(m[1]))), 'phase')
    elif (m := re.match(r'An RC lag circuit has fc = ([\d,]+) Hz\. What is Vout/Vin at ([\d,]+) Hz', q)): check(it, 1 / math.sqrt(1 + (num(m[2]) / num(m[1])) ** 2), 'atten')
    elif (m := re.match(r'.*midrange open-loop gain of (\d+) dB\. What is the gain as a plain ratio', q)): check(it, 10 ** (int(m[1]) / 20), 'dB->ratio')
    elif 'Zin(NI)' in q:
        m = re.match(r'.*Aol = ([\d,]+), Zin = ([\d.]+) MΩ.*Rf = (\d+) kΩ, Ri = ([\d.]+) kΩ', q); aol, zin, rf, ri = num(m[1]), float(m[2]) * 1e6, float(m[3]), float(m[4])
        check(it, (1 + ri / (ri + rf) * aol) * zin / 1e9, 'Zin NI')
    elif 'Zout(NI)' in q:
        m = re.match(r'Same amplifier \(Aol = ([\d,]+), Zout = (\d+) Ω, Rf = (\d+) kΩ, Ri = ([\d.]+) kΩ', q); aol, zo, rf, ri = num(m[1]), float(m[2]), float(m[3]), float(m[4])
        check(it, zo / (1 + ri / (ri + rf) * aol) * 1e3, 'Zout NI')
# original numeric MCQs
def sel(n): return next(i for i in orig if i['kind'] == 'mcq' and i['src']['en'].startswith(f'Floyd 9e, Ch.12, Self-Test Q{n} '))
assert 20 * math.log10(3500 / 0.35) == 80 and 3500 / 0.35 == 10000; assert sel(8)['correct'] == 3
assert abs((50 - 49.3) - 0.7) < 1e-9 and sel(11)['opts'][sel(11)['correct']]['en'] == '700 nA'
assert ok(8 / 12, 0.6667) and sel(12)['opts'][sel(12)['correct']]['en'] == '0.67 V/μs'
assert 1 + 100 / 1.0 == 101 and sel(16)['opts'][sel(16)['correct']]['en'] == '101'
assert 10 - 1 == 9 and sel(27)['opts'][sel(27)['correct']]['en'] == '9 kHz'
assert 20 * 10 == 200 and sel(30)['correct'] == 3
# worked problems vs. book odd answers
assert round(20 * math.log10(175000 / 0.18)) == 120 and round((8.3 + 7.9) / 2, 6) == 8.1 and round(24 / 15, 1) == 1.6
assert round(1 + 560 / 1.5) == 374 and round((1 + 560 / 1.5) * 0.01, 2) == 3.74
assert [round(49 * 1.0), round(300 * 10), round(7 * 12), round(75 * 2.2)] == [49, 3000, 84, 165]
assert round(20 * math.log10(10 ** (89 / 20) / (5500 / 750)), 1) == 71.7
assert round(20 * math.log10(250000), 1) == 108.0 and 90000 / 300000 == 0.3 and round(abs(8.3 - 7.9), 1) == 0.4 and 20 / 0.5 == 40
for it in orig + gen:   # structural sanity
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('checked generated families:', checked, '| total generated verified:', sum(checked.values()), 'of', len(gen))
print('FAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
