# -*- coding: utf-8 -*-
"""Verify cau MUC 3 cua Module 01 den 07 (data/qsrc/mNN_l3.json): moi cau tinh lai tu de bai (EN) bang cach KHAC gen_levels.py (quy tac dau, Fraction, vong lap, sympy cho SOP toi gian).
Chay bang python cua .venv (can sympy): .venv/bin/python -I build/verify/verify_levels.py -> 'FAILS: none'."""
import sys, os, re, json, math, itertools
from fractions import Fraction as Fr
import sympy as sp
from sympy.logic import SOPform
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
fails = []; fam = {}
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
def hit(k): fam[k] = fam.get(k, 0) + 1
def ans(it): return it['opts'][it['correct']]['en']
NB = '̅'
def sign8(v): return v - 256 if v >= 128 else v
def parse_sop(expr, names):                                  # chuoi nhu "A̅B + C" -> tap minterm
    terms = [t.strip() for t in expr.split('+')]; ms = set()
    for m in range(2 ** len(names)):
        env = {n: (m >> (len(names) - 1 - i)) & 1 for i, n in enumerate(names)}; ok = False
        for t in terms:
            lits = re.findall(r'([A-D])(̅?)', t); val = all((env[l] == 0) if nb else (env[l] == 1) for l, nb in lits)
            ok = ok or val
        if ok: ms.add(m)
    return ms
def nlit(expr): return len(re.findall(r'[A-D]', expr))
SEG = {2: 0b1101101, 3: 0b1111001, 4: 0b0110011, 5: 0b1011011}      # abcdefg: a la bit cao nhat (cach khac voi chuoi cua gen)
def segs(code): return ', '.join(c for c, bit in zip('abcdefg', format(code, '07b')) if bit == '1')
for m in ('m01', 'm02', 'm03', 'm04', 'm05', 'm06', 'm07'):
    for it in json.load(open(os.path.join(ROOT, 'data', 'qsrc', f'{m}_l3.json'), encoding='utf-8')):
        q = it['q']['en']; a = ans(it); mm = None
        if mm := re.match(r"Use 8-bit two's complement to compute (-?\d+) − (-?\d+)", q):
            x, y = int(mm[1]), int(mm[2]); comp = (~(y & 0xFF) + 1) & 0xFF; check('sub ' + q[40:70], a == format((x + comp) & 0xFF, '08b'), (q, a)); hit('two\'s complement subtraction')
        elif mm := re.match(r"Two 8-bit two's complement numbers ([01]{8}) \((-?\d+)\) and ([01]{8}) \((-?\d+)\) are added", q):
            x, y = int(mm[1], 2), int(mm[3], 2); s = (x + y) & 0xFF; ovf = ((x >> 7) == (y >> 7)) and ((x >> 7) != (s >> 7)); exp = f'{s:08b}, ' + ('overflow' if ovf else 'no overflow')
            check('ovf ' + q[30:60], a == exp and sign8(x) == int(mm[2]), (q, a, exp)); hit('overflow')
        elif mm := re.match(r'Two hexadecimal bytes ([0-9A-F]{2})H \+ ([0-9A-F]{2})H', q):
            t = int(mm[1], 16) + int(mm[2], 16); check('hex ' + mm[1] + mm[2], a == f'{t % 256:02X}H, carry = {1 if t > 255 else 0}', (q, a)); hit('hex addition')
        elif mm := re.match(r'Two BCD numbers .* \((\d+)\) and .* \((\d+)\) are added', q):
            t = int(mm[1]) + int(mm[2]); exp = ' '.join(f'{int(c):04b}' for c in str(t)); check('bcd ' + mm[1] + mm[2], a == exp, (q, a, exp)); hit('BCD addition')
        elif mm := re.match(r'The 5-bit Gray code of the binary number ([01]{5})', q):
            b = mm[1]; g = b[0] + ''.join(str(int(b[i]) ^ int(b[i - 1])) for i in range(1, 5)); check('gray ' + b, a == g, (q, a, g)); hit('Gray code')
        elif mm := re.match(r'The binary number with a fractional part ([01]+)\.([01]+)₂', q):
            v = int(mm[1], 2) + Fr(int(mm[2], 2), 2 ** len(mm[2])); check('frac ' + mm[1], abs(float(a) - float(v)) < 1e-12, (q, a, v)); hit('binary fraction')
        elif mm := re.match(r"The range of a (\d+)-bit two's complement integer", q):
            n = int(mm[1]); check('range', a == f'{-2 ** (n - 1)} đến {2 ** (n - 1) - 1}' or a == f'{-2 ** (n - 1)} to {2 ** (n - 1) - 1}', (q, a)); hit('two\'s complement range')
        elif mm := re.match(r'The function F\(([A-D, ]+)\) = Σm\(([\d, ]+)\)', q):
            names = [n.strip() for n in mm[1].split(',')]; ms = [int(x) for x in mm[2].split(',')]
            syms = sp.symbols(names); ref = SOPform(syms, ms); ref_ms = {int(''.join(str(int(bool(b))) for b in bits), 2) for bits in itertools.product((0, 1), repeat=len(names)) if ref.subs(dict(zip(syms, [bool(b) for b in bits])))}
            check('sop equiv ' + a, parse_sop(a, names) == set(ms) == ref_ms, (q, a)); lits_ref = sum(len(t.args) if isinstance(t, sp.And) else 1 for t in (ref.args if isinstance(ref, sp.Or) else [ref]))
            check('sop minimal ' + a, nlit(a) == lits_ref, (a, nlit(a), lits_ref)); hit('minimal SOP')
        elif mm := re.match(r'How many different Boolean functions of (\d+) variables', q): check('nfunc', int(a) == len({tuple(t) for t in itertools.product((0, 1), repeat=2 ** int(mm[1]))}), (q, a)); hit('number of functions')
        elif mm := re.match(r'At least how many two-input NAND gates are needed to build a two-input (XOR|OR|AND)', q):
            nand = lambda x, y: 1 - (x & y); ok = True
            for x, y in itertools.product((0, 1), repeat=2):
                t = nand(x, y)
                if mm[1] == 'XOR': ok &= nand(nand(x, t), nand(y, t)) == (x ^ y); k = 4
                elif mm[1] == 'OR': ok &= nand(nand(x, x), nand(y, y)) == (x | y); k = 3
                else: ok &= nand(t, t) == (x & y); k = 2
            check('nand ' + mm[1], ok and a == str(k), (q, a)); hit('NAND construction')
        elif mm := re.match(r'A 4-bit parallel adder adds A = ([01]{4}), B = ([01]{4}) with carry-in Cin = (\d)', q):
            t = int(mm[1], 2) + int(mm[2], 2) + int(mm[3]); check('adder ' + q[30:60], a == f'{t & 15:04b}, Cout = {t >> 4}', (q, a)); hit('4-bit adder')
        elif mm := re.match(r'An 8-to-1 multiplexer has data inputs D0 to D7 = ([01]{8}).*CBA = ([01]{3})', q): check('mux', a == mm[1][int(mm[2], 2)], (q, a)); hit('8:1 MUX')
        elif mm := re.match(r'How many 4-to-1 multiplexers .* build a (\d+)-to-1', q):
            n = int(mm[1]); tot = 0
            while n > 1: n = -(-n // 4); tot += n
            check('mux tree ' + mm[1], a == str(tot), (q, a)); hit('MUX tree')
        elif mm := re.match(r'A 4-bit comparator receives A = ([01]{4}) and B = ([01]{4})', q):
            x, y = int(mm[1], 2), int(mm[2], 2); check('cmp', a == ('A = B' if x == y else 'A > B' if x > y else 'A < B'), (q, a)); hit('comparator')
        elif mm := re.match(r'A memory has (\d+) address lines and (\d+)-bit words', q):
            n = int(mm[1]); w = int(mm[2]); check('cap', int(a.split()[0]) == (1 << n) * w // 8, (q, a)); hit('memory capacity')
        elif mm := re.match(r'At least how many address lines are needed to address (\d+) (K|M)', q):
            n = int(mm[1]) * (1024 if mm[2] == 'K' else 1024 * 1024); check('addr lines', a == str((n - 1).bit_length()), (q, a)); hit('address lines')
        elif mm := re.match(r'How many (\d+) K × (\d+)-bit chips are needed to build a (\d+) K × (\d+)-bit', q):
            cw, cl, tw, tl = map(int, mm.groups()); check('chips', a == str(-(-tw // cw) * -(-tl // cl)), (q, a)); hit('memory chips')
        elif mm := re.match(r'A (\d+) K-cell memory block starts at address ([0-9A-F]{4})H', q):
            size = int(mm[1]) * 1024; check('block end', a == f'{int(mm[2], 16) + size - 1:04X}H', (q, a)); hit('address range')
        elif mm := re.match(r'An instruction needs (\d+) T-states and the clock is (\d+) MHz', q): check('t-state', abs(float(a.split()[0]) - int(mm[1]) / int(mm[2])) < 1e-9, (q, a)); hit('instruction time')
        elif mm := re.match(r'A 32-bit ARINC 429 word is transmitted at ([0-9.]+) kbit/s', q): check('429 time', abs(float(a.split()[0]) - 32 / (float(mm[1]) * 1e3) * 1e3) < 1e-9, (q, a)); hit('ARINC word time')
        elif mm := re.match(r'Ignoring the gap between words, how many 32-bit words per second .* at ([0-9.]+) kbit/s', q): check('429 words', abs(float(a) - float(mm[1]) * 1e3 / 32) < 0.06, (q, a)); hit('words per second')
        elif mm := re.match(r'An ARINC 429 word uses ODD parity\. The first 31 bits contain (\d+) ones', q):
            n = int(mm[1]); p = 0 if n % 2 else 1; check('429 parity', a == f'bit = {p}; total ones = {n + p} (odd)', (q, a)); hit('odd parity')
        elif mm := re.match(r'A raster display has (\d+) lines and a frame rate of (\d+) Hz', q): check('raster', abs(float(a.split()[0]) - int(mm[1]) * int(mm[2]) / 1e3) < 1e-9, (q, a)); hit('line frequency')
        elif mm := re.match(r'A common-cathode 7-segment display .* shows the digit (\d)', q): check('7seg ' + mm[1], a == segs(SEG[int(mm[1])]), (q, a)); hit('7-segment')
        elif mm := re.match(r'The frame memory for a (\d+) × (\d+) pixel display with (\d+) bits per pixel', q): check('frame mem', int(a.split()[0]) == int(mm[1]) * int(mm[2]) * int(mm[3]) // 8, (q, a)); hit('frame memory')
        elif mm := re.match(r'The checksum \(sum modulo 256\) of the bytes ([0-9A-F ]+) \(hexadecimal\)', q): check('checksum', a == f'{sum(int(b, 16) for b in mm[1].split()) % 256:02X}H', (q, a)); hit('checksum')
        elif mm := re.match(r'The 7-bit data ([01]{7}) gets an (even|odd) parity bit', q):
            n = mm[1].count('1'); p = (n % 2) if mm[2] == 'even' else 1 - (n % 2); tot = n + p; check('parity ' + mm[1] + mm[2], a == f'bit = {p}; total ones = {tot} ({"even" if tot % 2 == 0 else "odd"})', (q, a)); hit('parity bit')
        elif mm := re.match(r'The Hamming distance between the codewords ([01]{8}) and ([01]{8})', q): check('hamming', int(a) == bin(int(mm[1], 2) ^ int(mm[2], 2)).count('1'), (q, a)); hit('Hamming distance')
        elif mm := re.match(r'A code has a minimum Hamming distance of (\d+)', q): d = int(mm[1]); check('code cap', a == f'detect {d - 1}, correct {(d - 1) // 2}', (q, a)); hit('code capability')
        elif mm := re.search(r'A fleet of (\d+) aircraft each fly (\d+) hours a year', q): check('fleet', abs(float(a) - int(mm[1]) * int(mm[2]) * 1e-9) < 1e-15, (q, a)); hit('failure probability')
        else: check('khong nhan dang', False, q)
print('Cau muc 3 da tinh lai:', fam, '| tong', sum(fam.values()))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
