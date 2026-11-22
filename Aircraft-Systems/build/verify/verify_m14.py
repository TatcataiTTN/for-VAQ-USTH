# -*- coding: utf-8 -*-
"""Verify module 14 (VHDL): (1) vhdl.py hai cai dat khop nhau (256 cap p, q); (2) vi du Tooley 17.7 va 17.5; bang chan tri bo nua cong (Bang 17.1, 17.2); (3) moi cau so cua m14_gen.json tinh lai bang mot TRINH PHAN TICH
RIENG (leo thang uu tien) doc bieu thuc tu de bai; (4) khoa A.17 doc tu anh quet khop cau goc. Chay: python3 build/verify/verify_m14.py -> 'FAILS: none'."""
import sys, os, re, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import vhdl as V
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
for e in V.EXPR:
    for p in range(16):
        for q in range(16): check(f'ev {e},{p},{q}', V.ev_a(e, p, q) == V.ev_b(e, p, q))
for x in (0, 1):
    for y in (0, 1):
        check(f'HA {x}{y}', V.half_adder_a(x, y) == V.half_adder_b(x, y))
        for en in (0, 1): check(f'HA EN {x}{y}{en}', V.half_adder_en_a(x, y, en) == V.half_adder_en_b(x, y, en))
for n in range(1, 10): check(f'delay {n}', V.path_delay_a(n, 15) == V.path_delay_b(n, 15))
# ---- sach ----
b4 = lambda v: format(v, '04b')
T = {'p AND q': '0010', 'NOT p AND q': '0100', 'p AND NOT q': '1000', 'p AND SLA q': '1000', 'NOT p AND ROR q': '0001'}                # Tooley 17.7 (p = 1010, q = 0110)
for e, r in T.items(): check('Tooley 17.7: ' + e, b4(V.ev(e, 0b1010, 0b0110)) == r)
check('Tooley 17.5 (1): x AND y = 0000', b4(V.ev('p AND q', 3, 4)) == '0000'); check('Tooley 17.5 (2): NOT x OR NOT y = 1111', b4(V.ev('NOT p OR NOT q', 3, 4)) == '1111')
check('Tooley Ch.17 Q12: not x and y (101, 011) = 010', ((~0b101 & 0b111) & 0b011) == 0b010)
check('Bang 17.1: SUM = XOR, CARRY = AND', [V.half_adder(x, y) for x in (0, 1) for y in (0, 1)] == [(0, 0), (1, 0), (1, 0), (0, 1)])
check('Bang 17.2: EN = 0 -> (0, 0)', all(V.half_adder_en(x, y, 0) == (0, 0) for x in (0, 1) for y in (0, 1)))
check('Tooley 17.10: 3 x 15 ns = 45 ns', V.path_delay(3, 15) == 45)
# ---- trinh phan tich rieng: NOT (lop 7) > SLA/ROR (lop 3, mot ngoi) > AND/OR/XOR (lop 1), dau ngoac ----
def parse(expr, p, q):
    tok = re.findall(r'\(|\)|[A-Za-z]+', expr); pos = [0]; env = {'p': p, 'q': q}
    def peek(): return tok[pos[0]] if pos[0] < len(tok) else None
    def take(): pos[0] += 1; return tok[pos[0] - 1]
    def unary():                                           # lop cao nhat truoc: NOT, roi dich/xoay (deu mot ngoi trong cach viet cua Tooley)
        t = take()
        if t == 'NOT': return ~unary() & 0xF
        if t == 'SLA': v = unary(); return (v << 1) & 0xF
        if t == 'ROR': v = unary(); return ((v >> 1) | ((v & 1) << 3)) & 0xF
        if t == '(': v = logic(); take(); return v
        return env[t]
    def logic():
        v = unary()
        while peek() in ('AND', 'OR', 'XOR'):
            op = take(); w = unary(); v = {'AND': v & w, 'OR': v | w, 'XOR': v ^ w}[op]
        return v
    return logic()
for e in V.EXPR: check('parser = vhdl.py ' + e, all(parse(e, p, q) == V.ev(e, p, q) for p in range(16) for q in range(16)))
# ---- cau so sinh ----
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm14_gen.json'), encoding='utf-8')); fam = {}
def ans(it): return it['opts'][it['correct']]['en']
def hit(k): fam[k] = fam.get(k, 0) + 1
for it in data:
    q = it['q']['en']; a = ans(it); m = None
    if m := re.match(r'With p = ([01]{4}) and q = ([01]{4}) \(4-bit vectors\), the VHDL expression "(.+)" \(in Tooley', q):
        check('gen expr ' + q[:70], a == b4(parse(m[3], int(m[1], 2), int(m[2], 2))), (q, a)); hit('VHDL expression')
    elif m := re.match(r'A half adder with an active-high enable EN has x = (\d), y = (\d), EN = (\d)\. The pair', q):
        x, y, en = map(int, m.groups()); s, c = ((x ^ y), (x & y)) if en else (0, 0); check('gen HA ' + q[40:80], a == f'({s}, {c})', (q, a)); hit('half adder EN')
    elif m := re.match(r'A half adder built from three standard gates', q): check('gen 45ns', a == '45 ns'); hit('3-gate delay')
    elif m := re.match(r'A signal path passes through (\d+) gates in a row, each with a (\d+) ns delay', q): check('gen path ' + q[:40], a == f'{int(m[1]) * int(m[2])} ns', (q, a)); hit('path delay')
print('Ho cau so da tinh lai:', fam, '| tong', sum(fam.values()), '/', len(data))
K = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']['ch17']
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm14.json'), encoding='utf-8'))
for it in goc:
    n = int(re.search(r'Q(\d+)', it['src']['en'])[1]); check(f'Tooley Ch.17 Q{n} khoa {K[n - 1]}', it['correct'] == 'abc'.index(K[n - 1]))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
