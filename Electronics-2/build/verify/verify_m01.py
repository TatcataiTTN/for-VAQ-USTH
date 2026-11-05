"""Module 01 verification: EASA printed-answer evidence + independent recomputation of every computed item."""
import json, os, re, sys, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EASA = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'EASA_M04_Electronics_Fundamentals_ocr.pdf'); cache = {}
def page(n):
    if n not in cache: cache[n] = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), EASA, '-'], capture_output=True, text=True).stdout)
    return cache[n]
ev = json.load(open(os.path.join(ROOT, 'data/verify/m01_evidence.json'), encoding='utf-8'))
orig = json.load(open(os.path.join(ROOT, 'data/qsrc/m01.json'), encoding='utf-8')); gen = json.load(open(os.path.join(ROOT, 'data/qsrc/m01_gen.json'), encoding='utf-8'))
G = {'AND': lambda a, b: a & b, 'OR': lambda a, b: a | b, 'NAND': lambda a, b: 1 - (a & b), 'NOR': lambda a, b: 1 - (a | b), 'XOR': lambda a, b: a ^ b}
def jk(q, j, k): return {(0, 0): q, (0, 1): 0, (1, 0): 1, (1, 1): 1 - q}[(j, k)]
fails = []; n_ev = 0; chk = {}
def ok(fam, cond, info):
    chk[fam] = chk.get(fam, 0) + 1
    if not cond: fails.append((fam, info))
for it in orig + gen:
    q = it['q']['en']; e = ev.get(q)
    if e:
        n_ev += 1
        if not re.search(e['rx'], page(e['page']), re.I): fails.append(('evidence', e['page'], e['rx'], q[:50]))
        if it['kind'] == 'ess': continue
    if it['kind'] == 'ess' or e: continue
    a = it['opts'][it['correct']]['en']
    if (m := re.match(r'Convert decimal (\d+) to binary', q)): ok('dec->bin', a == format(int(m[1]), 'b'), q)
    elif (m := re.match(r'Convert binary (\d+) to decimal', q)): ok('bin->dec', a == str(int(m[1], 2)), q)
    elif (m := re.match(r'Add the binary numbers (\d+) and (\d+)', q)): ok('bin add', a == format(int(m[1], 2) + int(m[2], 2), 'b'), q)
    elif (m := re.match(r'What is the output of a (\w+) gate for inputs A = (\d), B = (\d)', q)): ok('gate', a == str(G[m[1]](int(m[2]), int(m[3]))), q)
    elif (m := re.match(r'A half-adder has inputs A = (\d) and B = (\d)', q)): ok('half-adder', a == f'({int(m[1])^int(m[2])}, {int(m[1])&int(m[2])})', q)
    elif (m := re.match(r'A JK flip-flop currently has Q = (\d). After a clock pulse with J = (\d), K = (\d)', q)): ok('JK', a == str(jk(int(m[1]), int(m[2]), int(m[3]))), q)
    elif (m := re.match(r'A 2-to-4 decoder has its enable line (LOW|HIGH)', q)): ok('decoder', (a == 'all outputs LOW') == (m[1] == 'LOW'), q)
    else: fails.append(('unparsed', q[:60]))
assert format(13, 'b') == '1101' and int('1011', 2) == 11 and format(5 + 3, 'b') == '1000' and jk(1, 1, 1) == 0
for it in orig + gen:
    if it['kind'] != 'ess': assert len({o['en'] for o in it['opts']}) == len(it['opts']) and 0 <= it['correct'] < len(it['opts'])
print('EASA-grounded items:', n_ev, '| computed:', chk, 'total computed', sum(chk.values())); print('FAILS:'); [print(' ', f) for f in fails] if fails else print('  none'); sys.exit(1 if fails else 0)
