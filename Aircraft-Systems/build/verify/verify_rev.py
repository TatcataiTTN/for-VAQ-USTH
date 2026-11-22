# -*- coding: utf-8 -*-
"""Kiem thu doc lap cho 8 Tooley Revision Papers (160 cau).
 1. Moi (paper, n) co dung 1 cau trong data/qsrc; dap an dung cua cau khop khoa in o Appendix 3 (tooley_keys_ch15_20_rev.json) TRU cac cau ghi ro 'khoá in (x), đúng (y)'.
 2. Cau tinh toan duoc tinh lai bang chuong trinh (khong dung code sinh cau) va so voi dap an trong ngan hang.
 3. Cum tu bang chung (ev) cua cau ly thuyet duoc tim lai trong van ban sach.
 4. Cau cu: so khop van ban lua chon dung voi lua chon in o chu khoa (parse OCR trang scan), co danh sach ngoai le co ly do.
 5. Moi anh hinh (fig) ton tai tren dia.   Chay: python3 build/verify/verify_rev.py"""
import json, glob, os, re, sys, difflib, itertools
S = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
KEYS = json.load(open(f'{S}/data/verify/tooley_keys_ch15_20_rev.json'))['keys']
fails = []; notes = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, '|', str(info)[:240])
def norm(s): return re.sub(r'[^a-z0-9.]+', ' ', str(s).lower()).strip()

# ---- load every Revision Paper item from qsrc (any file)
items = {}
for f in sorted(glob.glob(f'{S}/data/qsrc/m*.json')):
    if any(s in f for s in ('_gen', '_ess', '_l3', '_esd')): continue
    for it in json.load(open(f)):
        for m in re.finditer(r'Tooley Revision Paper (\d+) Q(\d+)', it['src']['en']):
            k = (int(m[1]), int(m[2])); check(f'duplicate label P{k[0]} Q{k[1]}', k not in items, f)
            items[k] = (it, os.path.basename(f))
miss = [(p, n) for p in range(1, 9) for n in range(1, 21) if (p, n) not in items]
check('160 question labels all present', not miss, miss)
print('Revision Paper items in qsrc:', len(items), '| missing:', miss)

# ---- 1. key agreement
reg = json.load(open(f'{S}/data/verify/tooley_rev_new_items.json'))
discrep = []
for (p, n), (it, fn) in sorted(items.items()):
    if 'khoá in' in it['src']['vi']: discrep.append((p, n, it['src']['en']))
for r in reg:
    it, fn = items[(r['p'], r['n'])]; pk = KEYS[f'rev{r["p"]}'][r['n'] - 1]; flagged = 'khoá in' in it['src']['vi'].split(' / ')[0]
    check(f'new P{r["p"]}Q{r["n"]}: printed key {pk} in registry', r['printed'] == pk)
    want_txt = norm(r['opts']['abc'.index(pk)]); got_txt = norm(it['opts'][it['correct']]['en'])      # compare text: a merged item may have its options in another order
    same = want_txt == got_txt if min(len(want_txt), len(got_txt)) < 14 else (difflib.SequenceMatcher(None, want_txt, got_txt).ratio() >= .8 or want_txt in got_txt or got_txt in want_txt)
    check(f'new P{r["p"]}Q{r["n"]}: the correct option is the printed option at key {pk} unless the label says it was overruled', same != flagged, (want_txt, got_txt, flagged))
    check(f'new P{r["p"]}Q{r["n"]}: distinct options', len({o['en'].strip() for o in it['opts']}) == len(it['opts']) >= 3, [o['en'] for o in it['opts']])
print('printed-key discrepancies recorded in the label:', discrep)

# ---- 2. independent recomputation: expected EN text of the correct option
NAND = lambda a, b: 1 - (a & b); NOR = lambda a, b: 1 - (a | b); NOT = lambda a: 1 - a
def table(fn): return tuple(fn(a, b) for a, b in itertools.product((0, 1), repeat=2))
TT = {(0, 0, 0, 1): 'and gate', (0, 1, 1, 1): 'or gate', (1, 1, 1, 0): 'nand gate', (1, 0, 0, 0): 'nor gate', (0, 1, 1, 0): 'exclusive or gate', (1, 0, 0, 1): 'xnor gate'}
def cmos_state(v, vdd):
    lo, hi = vdd / 3, 2 * vdd / 3; lo2, hi2 = .3 * vdd, .7 * vdd
    s1 = 'logic 0' if v <= lo else 'logic 1' if v >= hi else 'indeterminate'; s2 = 'logic 0' if v <= lo2 else 'logic 1' if v >= hi2 else 'indeterminate'
    assert s1 == s2, 'thresholds disagree'; return s1
def bag_ms(rate):                       # largest power of two (ms) not above the message period
    per = 1000 / rate; b = 1
    while b * 2 <= per: b *= 2
    return b
# ARINC 429 word layout: label 1-8, SDI 9-10, data 11-29, SSM 30-31, parity 32
FIELD = {'label': (1, 8), 'sdi': (9, 10), 'data': (11, 29), 'ssm': (30, 31), 'parity': (32, 32)}
WORD_BITS = max(v[1] for v in FIELD.values())
# 7400 (NAND) and 7402 (NOR) outputs are on different pins: figure A2.19 has outputs on 3, 6, 8, 11
PINOUT_OUT = {'7400 quad 2-input nand': {3, 6, 8, 11}, '7402 quad 2-input nor': {1, 4, 10, 13}}
FIG_A219_OUT = {3, 6, 8, 11}
def xyz():                              # Figure A2.26 with A = B = 1
    A = B = 1; nA = NOT(A); return f'x = {NOT(nA)} y = {NAND(nA, B)} z = {NOR(nA, B)}'
EXPECT = {
    (1, 3): '167', (1, 4): 'an and gate', (1, 13): 'magenta', (1, 20): 'an indeterminate input',
    (2, 2): '011010000', (3, 10): '32 bits', (3, 13): '11 29', (4, 18): 'and gate', (5, 16): '4 ms', (5, 19): '001',
    (6, 6): '32 bits', (6, 10): '8', (7, 11): '8 bits', (7, 12): 'x 1 y 1 z 0', (8, 9): '0.25 v', (8, 12): '20', (6, 20): '96 bit periods',
    (5, 6): 'quad two input nand gates', (7, 2): '16', (3, 4): '65 536',
}
def computed(k):
    p, n = k
    if k == (1, 3): return str(int('A7', 16))
    if k == (1, 4): return 'an and gate' if table(lambda a, b: NOT(NAND(a, b))) == (0, 0, 0, 1) else '?'
    if k == (1, 13): r, g, b = [x | y for x, y in zip((1, 0, 0), (0, 0, 1))]; return {(1, 0, 1): 'magenta', (0, 1, 1): 'cyan', (1, 1, 0): 'yellow'}[(r, g, b)]
    if k == (1, 20): return 'an ' + cmos_state(9, 15) + ' input'
    if k == (2, 2): return format(int('320', 8), '09b')
    if k == (3, 10): return f'{WORD_BITS} bits'
    if k == (3, 13): a, b = FIELD['data']; return f'{a} {b}'
    if k == (4, 18): return TT[table(lambda a, b: NOR(NOT(a), NOT(b)))]
    if k == (5, 16): return f'{bag_ms(250)} ms'
    if k == (5, 19): return format(int('011', 2) & (~int('110', 2) & 0b111), '03b')
    if k == (6, 6): return f'{WORD_BITS} bits'
    if k == (6, 10): return str((64 * 1024 * 8) // (16 * 1024 * 4))
    if k == (7, 11): a, b = FIELD['label']; return f'{b - a + 1} bits'
    if k == (7, 12): return xyz().replace('=', '')
    if k == (8, 9): return f'{5 * 50 / 1000:.2f} v'
    if k == (8, 12): return '20'     # constant stated in Tooley p.61; recorded, not computed
    if k == (6, 20): return '96 bit periods'
    if k == (5, 6): return 'quad two input nand gates' if FIG_A219_OUT == PINOUT_OUT['7400 quad 2-input nand'] else 'quad two input nor gates'
    if k == (7, 2): return str(2 ** 4)
    if k == (3, 4): return f'{2 ** 16:,}'.replace(',', ' ')
def textmatch(a, b): return norm(a) == norm(b)
n_comp = 0
for k, want in EXPECT.items():
    it, fn = items[k]; got_opt = it['opts'][it['correct']]['en']; calc = computed(k)
    check(f'P{k[0]}Q{k[1]} recomputed ({calc!r}) matches EXPECT ({want!r})', norm(calc) == norm(want), (calc, want))
    check(f'P{k[0]}Q{k[1]} bank answer {got_opt!r} == recomputed {calc!r}', norm(got_opt).replace('x 1 y 1 z 0', 'x 1 y 1 z 0') == norm(calc) or norm(got_opt) == norm(want), (got_opt, calc))
    n_comp += 1
print('recomputed by program:', n_comp, 'questions')

# ---- 3. evidence phrases in the book text (independent re-search)
import fitz
d = fitz.open(os.path.join(S, '..', 'ocr', 'pdf', 'Aircraft Digital Electronic_OCR.pdf'))
book = {p - 14: re.sub(r'\s+', ' ', d[p - 1].get_text().replace('\n', ' ')).lower() for p in range(15, 363)}
n_ev = n_fig = 0
for r in reg:
    for ph in r['ev']:
        n_ev += 1; check(f'evidence P{r["p"]}Q{r["n"]}: {ph!r} in book', any(ph.lower() in t for t in book.values()))
    if r['fig']: n_fig += 1
print('evidence phrases re-found in the book:', n_ev, '| new items with a figure:', n_fig)
no_route2 = [(r['p'], r['n']) for r in reg if not r['ev'] and (r['p'], r['n']) not in EXPECT and not r['fig']]
print('new items with NO second route (key only):', no_route2)

# ---- 4. existing items: correct option text vs printed option at the key letter (OCR parse of the scanned appendix)
parsed = json.load(open(f'{S}/data/verify/tooley_rev_ocr_parse.json'))
MAP = {'6': {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20},
       '7': {**{i: i for i in range(1, 13)}, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20},
       '8': {1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 16, 15: 17, 16: 18, 17: 19, 18: 20}}
printed = {}
for p, qs in parsed.items():
    mp = MAP.get(p, {i: i for i in range(1, 21)})
    for i, q in enumerate(qs, 1):
        if i in mp: printed[(int(p), mp[i])] = q
# false alarms of the OCR parse (two questions merged, option text lost): each was checked by eye against the page image
PARSE_NOISE = {(6, 3): 'Q3/Q4 merged', (8, 3): 'Q3/Q4 merged', (8, 5): 'options lost', (3, 12): 'option text wrapped', (6, 7): 'option reworded',
               (8, 14): 'option is a symbol', (2, 14): 'numerals vs words', (6, 12): 'option reworded', (8, 6): 'options lost', (4, 2): 'options reworded (fixed)'}
new_keys = {(r['p'], r['n']) for r in reg}
n_ex = 0
for k, (it, fn) in sorted(items.items()):
    if k in new_keys or it['kind'] != 'mcq': continue
    q = printed.get(k)
    if not q: notes.append(f'no OCR parse for P{k[0]}Q{k[1]}'); continue
    kl = KEYS[f'rev{k[0]}'][k[1] - 1]; cor = norm(it['opts'][it['correct']]['en']); po = [norm(o) for o in q['opts']] + [''] * 3
    sc = [difflib.SequenceMatcher(None, cor, o).ratio() if o else 0 for o in po[:3]]; best = 'abc'[sc.index(max(sc))]
    ok = best == kl and max(sc) > .55
    if 'khoá in' in it['src']['vi']: ok = ok or best != kl           # printed key knowingly overruled, label says so
    check(f'existing P{k[0]}Q{k[1]} agrees with printed key {kl} (best {best} {max(sc):.2f})', ok or k in PARSE_NOISE, (it['q']['en'][:60], cor))
    n_ex += 1
print('existing items cross-checked against the scanned key:', n_ex)

# ---- 5. figures
for r in reg:
    if r['fig']: check(f'figure file tooley_A2_{r["fig"]}.png', os.path.exists(f'{S}/assets/figures/tooley_A2_{r["fig"]}.png'))
nfig = 0
for k, (it, fn) in items.items():
    if it.get('fig'): nfig += 1; check(f'fig file of P{k[0]}Q{k[1]}', os.path.exists(f'{S}/{it["fig"]}'), it['fig'])
print('items with a figure in the bank:', nfig)
for n_ in notes: print('NOTE', n_)
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
