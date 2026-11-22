# -*- coding: utf-8 -*-
"""Cau MUC 3 (nhieu buoc, tinh toan) bo sung cho Module 01 den 07 -> data/qsrc/mNN_l3.json (bo_sung). Khong cau nao la cau goc cua sach. Dap an sinh bang so nguyen/chuoi bit/Fraction;
build/verify/verify_levels.py tinh lai DOC LAP (cach khac, sympy cho toi gian Boolean) tu chinh de bai (EN). Cac lua chon cung dang so nen khong lech do dai."""
import os, sys, json, itertools, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from qdsl import Bank, OUT
TOPICS = {'binary': ('Hệ nhị phân và số học nhị phân', 'Binary numbers and arithmetic'), 'hexoct': ('Bát phân và thập lục phân', 'Octal and hexadecimal'), 'complement': ('Số có dấu, bù 1 và bù 2', 'Signed numbers, 1s and 2s complement'),
          'codes': ('Mã BCD, Gray, ASCII', 'BCD, Gray and ASCII codes'), 'base-conv': ('Đổi cơ số', 'Base conversion'), 'gates': ('Cổng logic và bảng chân trị', 'Logic gates and truth tables'), 'boolean-laws': ('Luật Boolean và De Morgan', 'Boolean laws and De Morgan'),
          'simplify': ('Tối giản: K-map, SOP, POS', 'Simplification: K-map, SOP, POS'), 'adder': ('Bộ cộng, so sánh, parity', 'Adders, comparators, parity'), 'decoder': ('Bộ giải mã và bộ mã hoá', 'Decoders and encoders'), 'mux': ('Bộ dồn kênh và phân kênh', 'Multiplexers and demultiplexers'),
          'memory': ('Bộ nhớ bán dẫn: RAM, ROM, Flash', 'Semiconductor memory: RAM, ROM, flash'), 'cycle': ('Chu trình lệnh và thời gian', 'Instruction cycle and timing'), 'arinc429': ('ARINC 429: điện, từ dữ liệu, label', 'ARINC 429: electrical, word, label'),
          'seven': ('Màn hình 7 đoạn', 'Seven-segment displays'), 'efis': ('EFIS: PFD và ND', 'EFIS: PFD and ND'), 'tech': ('Công nghệ hiển thị: CRT, LCD, LED', 'Display technology: CRT, LCD, LED'), 'integrity': ('Toàn vẹn dữ liệu: parity, checksum', 'Data integrity: parity, checksum, CRC'), 'levels': ('Mức nghiêm trọng A đến E', 'Severity levels A to E')}
NB = '̅'
B = {m: Bank(TOPICS) for m in ('m01', 'm02', 'm03', 'm04', 'm05', 'm06', 'm07')}
def X(m, tid, qv, qe, correct, wrongs, xv, xe, tagv, tage):
    ops = [correct] + [w for w in wrongs if w != correct]; seen = []; ops = [o for o in ops if not (o in seen or seen.append(o))]
    assert len(ops) >= 3, (qe, ops)
    B[m].X(tid, 3, qv, qe, ops[:4], 0, xv, xe, f'Mức 3: {tagv}', f'Level 3: {tage}')
b8 = lambda v: format(v & 0xFF, '08b')
def parity_opts(ones, odd):
    p = (1 - ones % 2) if odd else ones % 2; want = 'lẻ' if odd else 'chẵn'; wante = 'odd' if odd else 'even'; typ = lambda n, e: (('lẻ' if n % 2 else 'chẵn'), ('odd' if n % 2 else 'even'))
    mk = lambda b, tot: (f'bit = {b}; tổng số bit 1 = {tot} ({typ(tot, 0)[0]})', f'bit = {b}; total ones = {tot} ({typ(tot, 0)[1]})')
    return p, mk(p, ones + p), [mk(1 - p, ones + 1 - p), mk(p, ones + 1 - p), mk(1 - p, ones + p)], want, wante
# ---------------- m01 ----------------
for a, b in ((45, 77), (100, 12), (23, 90), (-50, 20)):
    r = a - b; X('m01', 'complement', f'Dùng bù hai 8 bit để tính {a} − {b} (cộng {a} với bù hai của {b}). Kết quả viết dạng bù hai 8 bit là:', f'Use 8-bit two\'s complement to compute {a} − {b} (add {a} to the two\'s complement of {b}). The result in 8-bit two\'s complement is:',
      b8(r), [b8(-r), b8(r - 1), b8(r) if False else format((~(r & 0xFF)) & 0xFF, '08b')], f'{a} − {b} = {r}; bù hai 8 bit của {r} là {b8(r)}.', f'{a} − {b} = {r}; the 8-bit two\'s complement of {r} is {b8(r)}.', 'Phép trừ bù hai', 'Two\'s complement subtraction')
for a, b in ((100, 50), (-100, -50), (60, -90), (70, 40)):
    s = a + b; ovf = not (-128 <= s <= 127); res = f'{b8(s)}, ' + ('tràn' if ovf else 'không tràn'); rese = f'{b8(s)}, ' + ('overflow' if ovf else 'no overflow'); other = f'{b8(s)}, ' + ('không tràn' if ovf else 'tràn'); othere = f'{b8(s)}, ' + ('no overflow' if ovf else 'overflow')
    X('m01', 'complement', f'Cộng hai số bù hai 8 bit {b8(a)} ({a}) và {b8(b)} ({b}). Kết quả 8 bit và trạng thái tràn (overflow) là:', f'Two 8-bit two\'s complement numbers {b8(a)} ({a}) and {b8(b)} ({b}) are added. The 8-bit result and the overflow status are:',
      (res, rese), [(other, othere), (f'{b8(s + 1)}, ' + ('tràn' if ovf else 'không tràn'), f'{b8(s + 1)}, ' + ('overflow' if ovf else 'no overflow')), (f'{b8(a - b)}, ' + ('tràn' if ovf else 'không tràn'), f'{b8(a - b)}, ' + ('overflow' if ovf else 'no overflow'))],
      f'Tổng thật là {s}, ' + ('ngoài khoảng −128 đến 127 nên tràn; 8 bit giữ ' + b8(s) if ovf else 'trong khoảng −128 đến 127 nên không tràn') + '.', f'The true sum is {s}, ' + ('outside −128 to 127 so it overflows; 8 bits keep ' + b8(s) if ovf else 'inside −128 to 127 so there is no overflow') + '.', 'Tràn khi cộng bù hai', 'Overflow in two\'s complement addition')
for a, b in ((0x7B, 0xD5), (0xA9, 0x6C)):
    s = a + b; X('m01', 'hexoct', f'Cộng hai byte thập lục phân {a:02X}H + {b:02X}H trong thanh ghi 8 bit. Kết quả và cờ nhớ (carry) là:', f'Two hexadecimal bytes {a:02X}H + {b:02X}H are added in an 8-bit register. The result and the carry flag are:',
      f'{s & 0xFF:02X}H, carry = {s >> 8}', [f'{s & 0xFF:02X}H, carry = {1 - (s >> 8)}', f'{(s + 1) & 0xFF:02X}H, carry = {s >> 8}', f'{(a - b) & 0xFF:02X}H, carry = {s >> 8}'], f'{a:02X}H + {b:02X}H = {s:03X}H (= {s}); 8 bit giữ {s & 0xFF:02X}H, nhớ {s >> 8}.', f'{a:02X}H + {b:02X}H = {s:03X}H (= {s}); 8 bits keep {s & 0xFF:02X}H, carry {s >> 8}.', 'Cộng thập lục phân có nhớ', 'Hexadecimal addition with carry')
def bcd(n): return ' '.join(format(int(d), '04b') for d in str(n))
for a, b in ((47, 38), (59, 27), (68, 45)):
    r = a + b; naive = format(int(bcd(a).replace(' ', ''), 2) + int(bcd(b).replace(' ', ''), 2), 'b').zfill(8); nv = ' '.join(naive[i:i + 4] for i in range(0, len(naive), 4))
    X('m01', 'codes', f'Cộng hai số BCD {bcd(a)} ({a}) và {bcd(b)} ({b}) rồi hiệu chỉnh. Kết quả BCD là:', f'Two BCD numbers {bcd(a)} ({a}) and {bcd(b)} ({b}) are added and corrected. The BCD result is:', bcd(r), [nv, bcd(r + 6 if r + 6 < 200 else r - 6), bcd(int(str(r)[::-1]))], f'{a} + {b} = {r}; mỗi nhóm 4 bit chỉ dùng 0000 đến 1001 nên phải cộng 0110 vào nhóm vượt 9: kết quả {bcd(r)}.', f'{a} + {b} = {r}; each nibble may use only 0000 to 1001 so 0110 is added to a nibble above 9: the result is {bcd(r)}.', 'Cộng BCD có hiệu chỉnh', 'BCD addition with correction')
def gray(n): return n ^ (n >> 1)
for v in (0b10110, 0b01101):
    X('m01', 'codes', f'Mã Gray 5 bit của số nhị phân {format(v, "05b")} là:', f'The 5-bit Gray code of the binary number {format(v, "05b")} is:', format(gray(v), '05b'), [format(v, '05b'), format(gray(v) ^ 1, '05b'), format(v ^ 0b11111, '05b')], f'Bit Gray = bit nhị phân XOR bit nhị phân bên trái nó: {format(v, "05b")} cho {format(gray(v), "05b")}.', f'Gray bit = binary bit XOR the binary bit to its left: {format(v, "05b")} gives {format(gray(v), "05b")}.', 'Đổi nhị phân sang Gray', 'Binary to Gray')
for s in ('101.101', '1101.0011'):
    ip, fp = s.split('.'); val = int(ip, 2) + sum(int(c) * Fr(1, 2 ** (i + 1)) for i, c in enumerate(fp)); f = float(val)
    X('m01', 'base-conv', f'Số nhị phân có phần thập phân {s}₂ bằng (thập phân):', f'The binary number with a fractional part {s}₂ equals (decimal):', f'{f:g}', [f'{f + 0.5:g}', f'{f * 2:g}', f'{int(ip, 2) + int(fp, 2) / 10:g}'], f'Phần nguyên {int(ip, 2)}; phần lẻ = ' + ' + '.join(f'{c}×2⁻{i + 1}' for i, c in enumerate(fp)) + f' = {float(val - int(ip, 2)):g}; tổng {f:g}.', f'Integer part {int(ip, 2)}; fraction = ' + ' + '.join(f'{c}×2⁻{i + 1}' for i, c in enumerate(fp)) + f' = {float(val - int(ip, 2)):g}; total {f:g}.', 'Phần lẻ nhị phân', 'Binary fractions')
for n in (12, 10):
    X('m01', 'complement', f'Khoảng giá trị của số nguyên có dấu {n} bit dạng bù hai là:', f'The range of a {n}-bit two\'s complement integer is:', f'{-2 ** (n - 1)} đến {2 ** (n - 1) - 1}', [f'{-2 ** (n - 1) + 1} đến {2 ** (n - 1)}', f'0 đến {2 ** n - 1}', f'{-2 ** n} đến {2 ** n - 1}'], f'$-2^{{{n - 1}}}$ đến $2^{{{n - 1}}}-1$.', f'$-2^{{{n - 1}}}$ to $2^{{{n - 1}}}-1$.', 'Khoảng số bù hai', 'Two\'s complement range')
# ---------------- m02: toi gian SOP bang Quine-McCluskey tu viet ----------------
def qm_min(ms, nv):
    imps = {(m, 0) for m in ms}                                           # (gia tri, mat na do "-")
    primes = set()
    cur = set(imps)
    while cur:
        nxt = set(); used = set(); cl = sorted(cur)
        for (a, ma), (b, mb) in itertools.combinations(cl, 2):
            if ma == mb and bin((a ^ b) & ~ma).count('1') == 1:
                nxt.add((a & b if False else a & ~(a ^ b), ma | (a ^ b))); used.add((a, ma)); used.add((b, mb))
        primes |= (cur - used); cur = nxt
    def cov(p): v, mk = p; return {m for m in ms if (m & ~mk) == (v & ~mk)}
    best = None
    pl = sorted(primes)
    for k in range(1, len(pl) + 1):
        for combo in itertools.combinations(pl, k):
            if set().union(*[cov(p) for p in combo]) == set(ms):
                cost = sum(nv - bin(mk).count('1') for v, mk in combo)
                if best is None or cost < best[0]: best = (cost, combo)
        if best: break
    return best[1]
def term(p, nv, names):
    v, mk = p; s = ''
    for i in range(nv):
        bit = 1 << (nv - 1 - i)
        if mk & bit: continue
        s += names[i] + ('' if v & bit else NB)
    return s or '1'
def sop(ms, nv):
    names = 'ABCD'[:nv]; ps = qm_min(ms, nv); return ' + '.join(sorted(term(p, nv, names) for p in ps))
for nv, ms in ((3, [1, 3, 5, 7, 6]), (3, [0, 1, 2, 5, 6, 7]), (4, [0, 2, 5, 7, 8, 10, 13, 15]), (4, [1, 3, 4, 5, 7, 9, 11, 12, 13, 15])):
    names = 'ABCD'[:nv]; correct = sop(ms, nv); wrongs = []
    for flip in (ms[0], ms[-1], ms[len(ms) // 2]):
        alt = sorted(set(ms) ^ {flip}) if len(set(ms) ^ {flip}) else ms
        if alt: w = sop(alt, nv); wrongs.append(w)
    wrongs.append(sop(sorted(set(range(2 ** nv)) - set(ms)), nv))
    X('m02', 'simplify', f'Hàm F({", ".join(names)}) = Σm({", ".join(map(str, ms))}) ({nv} biến). Biểu thức SOP tối giản của F là (A̅ nghĩa là NOT A):', f'The function F({", ".join(names)}) = Σm({", ".join(map(str, ms))}) ({nv} variables). The minimal SOP expression of F is (A̅ means NOT A):', correct, wrongs,
      f'Gom nhóm trên bản đồ Karnaugh các ô 1 lớn nhất rồi cộng các nhóm: F = {correct}.', f'Group the largest blocks of 1s on the Karnaugh map and add the groups: F = {correct}.', 'Tối giản SOP', 'Minimal SOP')
for n in (2, 3, 4):
    X('m02', 'gates', f'Có bao nhiêu hàm Boolean khác nhau của {n} biến?', f'How many different Boolean functions of {n} variables are there?', str(2 ** (2 ** n)), [str(2 ** n), str(n * n), str(2 ** (2 ** n) - 1)], f'Bảng chân trị có $2^{n}={2 ** n}$ hàng, mỗi hàng chọn 0 hoặc 1 nên có $2^{{2^{n}}}={2 ** (2 ** n)}$ hàm.', f'The truth table has $2^{n}={2 ** n}$ rows, each free to be 0 or 1, so there are $2^{{2^{n}}}={2 ** (2 ** n)}$ functions.', 'Số hàm Boolean', 'Number of Boolean functions')
for what, k, vi_, en_ in (('XOR', 4, 'XOR hai ngõ vào', 'a two-input XOR'), ('OR', 3, 'OR hai ngõ vào', 'a two-input OR'), ('AND', 2, 'AND hai ngõ vào', 'a two-input AND')):
    X('m02', 'gates', f'Cần ít nhất bao nhiêu cổng NAND hai ngõ vào để thực hiện {vi_}?', f'At least how many two-input NAND gates are needed to build {en_}?', str(k), [str(k + 1), str(k - 1) if k > 2 else '5', str(k + 3), '1'], f'Cách xây chuẩn dùng {k} cổng NAND (kiểm bằng bảng chân trị).', f'The standard construction uses {k} NAND gates (checked by truth table).', 'Thực hiện bằng NAND', 'Building with NAND')
# ---------------- m03 ----------------
for a, b, c in ((0b1011, 0b0110, 1), (0b1111, 0b0001, 0), (0b0111, 0b1001, 1)):
    s = a + b + c; X('m03', 'adder', f'Bộ cộng song song 4 bit cộng A = {a:04b}, B = {b:04b} với nhớ vào Cin = {c}. Tổng 4 bit và nhớ ra Cout là:', f'A 4-bit parallel adder adds A = {a:04b}, B = {b:04b} with carry-in Cin = {c}. The 4-bit sum and the carry-out Cout are:',
      f'{s & 15:04b}, Cout = {s >> 4}', [f'{s & 15:04b}, Cout = {1 - (s >> 4)}', f'{(s - c) & 15:04b}, Cout = {s >> 4}', f'{(s + 1) & 15:04b}, Cout = {s >> 4}'], f'{a} + {b} + {c} = {s} = {s:05b}: tổng {s & 15:04b}, Cout {s >> 4}.', f'{a} + {b} + {c} = {s} = {s:05b}: sum {s & 15:04b}, Cout {s >> 4}.', 'Bộ cộng 4 bit', '4-bit adder')
for data, sel in (('10010110', 5), ('01101001', 2), ('11000101', 7)):
    out = data[sel]; X('m03', 'mux', f'Bộ dồn kênh 8 sang 1 có các ngõ vào dữ liệu D0 đến D7 = {data} (D0 ngoài cùng bên trái) và đường chọn CBA = {sel:03b} (C là MSB). Ngõ ra là:', f'An 8-to-1 multiplexer has data inputs D0 to D7 = {data} (D0 at the far left) and select lines CBA = {sel:03b} (C is the MSB). The output is:',
      out, [str(1 - int(out)), data[(sel + 1) % 8] if data[(sel + 1) % 8] != out else str(1 - int(out)), 'Z'], f'CBA = {sel:03b} chọn D{sel} = {out}.', f'CBA = {sel:03b} selects D{sel} = {out}.', 'Chọn kênh của MUX 8:1', 'Channel select of an 8:1 MUX')
def tree(n, k):
    c = 0
    while n > 1: g = math.ceil(n / k); c += g; n = g
    return c
for n in (16, 32, 64):
    X('m03', 'mux', f'Cần bao nhiêu bộ dồn kênh 4 sang 1 (ghép dạng cây) để xây một bộ dồn kênh {n} sang 1?', f'How many 4-to-1 multiplexers (arranged as a tree) are needed to build a {n}-to-1 multiplexer?', str(tree(n, 4)), [str(tree(n, 4) - 1), str(tree(n, 4) + 1), str(n // 4)], f'{n} → ' + ' → '.join(str(math.ceil(n / 4 ** i)) for i in range(1, 4) if math.ceil(n / 4 ** (i - 1)) > 1) + f': tổng {tree(n, 4)} bộ.', f'{n} → ' + ' → '.join(str(math.ceil(n / 4 ** i)) for i in range(1, 4) if math.ceil(n / 4 ** (i - 1)) > 1) + f': {tree(n, 4)} multiplexers in all.', 'Ghép MUX dạng cây', 'MUX trees')
for a, b in ((0b1011, 0b1100), (0b0101, 0b0101), (0b1110, 0b0111)):
    r = '=' if a == b else ('>' if a > b else '<')
    X('m03', 'adder', f'Bộ so sánh 4 bit nhận A = {a:04b} và B = {b:04b}. Ngõ ra đang ở mức tích cực là:', f'A 4-bit comparator receives A = {a:04b} and B = {b:04b}. The active output is:', f'A {r} B', [f'A {x} B' for x in ('<', '=', '>') if x != r] + ['không ngõ ra nào' if False else 'A ≠ B và A = B'], f'{a} {r} {b} (so từ MSB).', f'{a} {r} {b} (compared from the MSB).', 'Bộ so sánh 4 bit', '4-bit comparator')
# ---------------- m04 ----------------
for a, w in ((12, 8), (16, 8), (10, 16)):
    n = 2 ** a; bits = n * w; X('m04', 'memory', f'Một bộ nhớ có {a} đường địa chỉ và từ dài {w} bit. Dung lượng toàn bộ là:', f'A memory has {a} address lines and {w}-bit words. Its total capacity is:', f'{bits // 8:,} byte'.replace(',', ' ') if False else (f'{bits // 8} byte', f'{bits // 8} bytes'), [(f'{bits} byte', f'{bits} bytes'), (f'{n} byte', f'{n} bytes'), (f'{bits // 16} byte', f'{bits // 16} bytes')], f'$2^{{{a}}}={n}$ ô × {w} bit = {bits} bit = {bits // 8} byte.', f'$2^{{{a}}}={n}$ cells × {w} bits = {bits} bits = {bits // 8} bytes.', 'Dung lượng bộ nhớ', 'Memory capacity')
for cap, nm in ((8 * 1024, '8 K'), (64 * 1024, '64 K'), (1024 * 1024, '1 M')):
    a = int(math.log2(cap)); X('m04', 'memory', f'Cần ít nhất bao nhiêu đường địa chỉ để định vị {nm} ô nhớ (mỗi ô một địa chỉ)?', f'At least how many address lines are needed to address {nm} memory cells (one address per cell)?', str(a), [str(a - 1), str(a + 1), str(cap // 1024 if cap < 2 ** 20 else 1024)], f'$2^{{{a}}}={cap}$ nên cần {a} đường.', f'$2^{{{a}}}={cap}$ so {a} lines are needed.', 'Số đường địa chỉ', 'Address lines')
for tw, tl, cw, cl in ((16384, 8, 4096, 4), (32768, 8, 8192, 8), (8192, 16, 2048, 8)):
    n = math.ceil(tw / cw) * math.ceil(tl / cl); X('m04', 'memory', f'Cần bao nhiêu vi mạch {cw // 1024} K × {cl} bit để xây bộ nhớ {tw // 1024} K × {tl} bit?', f'How many {cw // 1024} K × {cl}-bit chips are needed to build a {tw // 1024} K × {tl}-bit memory?', str(n), [str(n * 2), str(n // 2), str(math.ceil(tw / cw))], f'Theo chiều từ: {math.ceil(tl / cl)} cột; theo chiều ô: {math.ceil(tw / cw)} hàng; tổng {n} vi mạch.', f'Word width: {math.ceil(tl / cl)} columns; depth: {math.ceil(tw / cw)} rows; {n} chips in all.', 'Ghép vi mạch nhớ', 'Combining memory chips')
for start, size, nm in ((0x2000, 0x1000, '4 K'), (0xC000, 0x4000, '16 K'), (0x8000, 0x0800, '2 K')):
    end = start + size - 1; X('m04', 'memory', f'Một khối nhớ {nm} ô bắt đầu ở địa chỉ {start:04X}H. Địa chỉ ô cuối cùng của khối là:', f'A {nm}-cell memory block starts at address {start:04X}H. The address of its last cell is:', f'{end:04X}H', [f'{end + 1:04X}H', f'{end - 0x100:04X}H', f'{(start + size // 2):04X}H'], f'{start:04X}H + {size:04X}H − 1 = {end:04X}H.', f'{start:04X}H + {size:04X}H − 1 = {end:04X}H.', 'Dải địa chỉ khối nhớ', 'Address range of a memory block')
for ts, mhz in ((18, 3), (10, 5), (24, 6)):
    t = Fr(ts) / mhz; X('m04', 'cycle', f'Một lệnh cần {ts} T-state, clock {mhz} MHz. Thời gian thực thi lệnh là:', f'An instruction needs {ts} T-states and the clock is {mhz} MHz. The instruction execution time is:', f'{float(t):g} μs', [f'{float(t * 2):g} μs', f'{float(t / 2):g} μs', f'{ts * mhz:g} μs'], f'$t=n_T/f={ts}/{mhz}$ μs = {float(t):g} μs.', f'$t=n_T/f={ts}/{mhz}$ μs = {float(t):g} μs.', 'Thời gian lệnh', 'Instruction time')
# ---------------- m05 ----------------
for r, nm in ((12.5e3, '12,5 kbit/s'), (100e3, '100 kbit/s')):
    t = 32 / r; X('m05', 'arinc429', f'Một từ ARINC 429 dài 32 bit được truyền ở tốc độ {nm}. Thời gian truyền một từ là:', f'A 32-bit ARINC 429 word is transmitted at {nm.replace(",", ".")}. The transmission time of one word is:', f'{t * 1e3:g} ms', [f'{t * 1e3 * 2:g} ms', f'{t * 1e3 / 2:g} ms', f'{t * 1e3 * 10:g} ms'], f'$t=32/R=32/{r:g}$ s = {t * 1e3:g} ms.', f'$t=32/R=32/{r:g}$ s = {t * 1e3:g} ms.', 'Thời gian một từ ARINC 429', 'ARINC 429 word time')
for r, nm in ((12.5e3, '12,5 kbit/s'), (100e3, '100 kbit/s')):
    w = r / 32; X('m05', 'arinc429', f'Bỏ qua khoảng nghỉ giữa các từ, bus ARINC 429 tốc độ {nm} truyền tối đa bao nhiêu từ 32 bit mỗi giây?', f'Ignoring the gap between words, how many 32-bit words per second can an ARINC 429 bus at {nm.replace(",", ".")} carry at most?', f'{w:.1f}'.rstrip('0').rstrip('.'), [f'{w * 2:.1f}'.rstrip('0').rstrip('.'), f'{w / 2:.1f}'.rstrip('0').rstrip('.'), f'{r / 8:.1f}'.rstrip('0').rstrip('.')], f'$R/32={r:g}/32={w:.1f}$ từ/giây.', f'$R/32={r:g}/32={w:.1f}$ words/s.', 'Số từ mỗi giây', 'Words per second')
for ones in (14, 17, 22):
    p, ok, wr, want, wante = parity_opts(ones, True)
    X('m05', 'arinc429', f'Một từ ARINC 429 dùng chẵn lẻ LẺ (odd parity). 31 bit đầu có {ones} bit 1. Bit chẵn lẻ (bit 32) và tổng số bit 1 của cả từ là:', f'An ARINC 429 word uses ODD parity. The first 31 bits contain {ones} ones. The parity bit (bit 32) and the total number of ones of the whole word are:', ok, wr, f'Tổng số bit 1 phải lẻ: {ones} là {"chẵn" if ones % 2 == 0 else "lẻ"} nên bit chẵn lẻ = {p}.', f'The total number of ones must be odd: {ones} is {"even" if ones % 2 == 0 else "odd"} so the parity bit = {p}.', 'Parity lẻ của từ 429', 'Odd parity of a 429 word')
# ---------------- m06 ----------------
for nl, fr in ((525, 30), (625, 25), (1125, 30)):
    f = nl * fr; X('m06', 'tech', f'Màn hình raster có {nl} dòng và tần số quét khung {fr} Hz. Tần số quét dòng là:', f'A raster display has {nl} lines and a frame rate of {fr} Hz. The line frequency is:', f'{f / 1e3:g} kHz', [f'{f / 2e3:g} kHz', f'{f / 1e3 * 2:g} kHz', f'{nl / fr:g} kHz'], f'$f_X=N_{{line}}\\,f_Y={nl}\\times{fr}$ = {f} Hz.', f'$f_X=N_{{line}}\\,f_Y={nl}\\times{fr}$ = {f} Hz.', 'Tần số quét dòng', 'Line frequency')
SEG = {2: 'abdeg', 3: 'abcdg', 4: 'bcfg', 5: 'acdfg'}
for d in (2, 3, 4, 5):
    s = SEG[d]; fmt = lambda t: ', '.join(sorted(t)); alt = [x for x in SEG if x != d]
    X('m06', 'seven', f'Màn hình 7 đoạn catốt chung (a, b, c, d, e, f, g) hiển thị chữ số {d}. Các đoạn sáng là:', f'A common-cathode 7-segment display (a, b, c, d, e, f, g) shows the digit {d}. The lit segments are:', fmt(s), [fmt(SEG[alt[0]]), fmt(SEG[alt[1]]), fmt(set('abcdefg') - set(s))], f'Chữ số {d} dùng các đoạn {fmt(s)}.', f'The digit {d} uses segments {fmt(s)}.', 'Đoạn sáng của chữ số', 'Lit segments of a digit')
for wpx, hpx, bpp in ((1024, 768, 8), (640, 480, 24)):
    byt = wpx * hpx * bpp // 8; X('m06', 'tech', f'Bộ nhớ khung hình cho màn hình {wpx} × {hpx} điểm ảnh, {bpp} bit mỗi điểm ảnh, cần tối thiểu:', f'The frame memory for a {wpx} × {hpx} pixel display with {bpp} bits per pixel needs at least:', f'{byt} byte', [f'{byt * 8} byte', f'{byt // 8} byte', f'{wpx * hpx} byte' if bpp != 8 else f'{byt + wpx} byte'], f'{wpx} × {hpx} × {bpp} / 8 = {byt} byte.', f'{wpx} × {hpx} × {bpp} / 8 = {byt} bytes.', 'Bộ nhớ khung hình', 'Frame memory')
# ---------------- m07 ----------------
for bs in ([0x3A, 0x7F, 0xC4, 0x91], [0x5E, 0xA7, 0x39], [0xFF, 0x02, 0x80, 0x81]):
    s = sum(bs) % 256; hs = ' '.join(f'{b:02X}' for b in bs); X('m07', 'integrity', f'Checksum (tổng modulo 256) của các byte {hs} (thập lục phân) là:', f'The checksum (sum modulo 256) of the bytes {hs} (hexadecimal) is:', f'{s:02X}H', [f'{(256 - s) % 256:02X}H', f'{(s + 1) % 256:02X}H', f'{sum(bs) // 256:02X}H'], f'Tổng = {sum(bs):X}H; modulo 256 giữ hai chữ số cuối: {s:02X}H.', f'Sum = {sum(bs):X}H; modulo 256 keeps the last two digits: {s:02X}H.', 'Checksum modulo 256', 'Modulo-256 checksum')
for data, kind in (('1011001', 'chẵn'), ('1011001', 'lẻ'), ('0110111', 'chẵn')):
    ones = data.count('1'); p, ok, wr, want, wante = parity_opts(ones, kind == 'lẻ')
    X('m07', 'integrity', f'Dữ liệu 7 bit {data} được thêm một bit chẵn lẻ {kind}. Bit chẵn lẻ và tổng số bit 1 của từ 8 bit là:', f'The 7-bit data {data} gets an {wante} parity bit. The parity bit and the total number of ones of the 8-bit word are:', ok, wr, f'Có {ones} bit 1; để tổng số bit 1 {want} cần bit = {p}.', f'There are {ones} ones; for an {wante} total the bit must be {p}.', 'Bit chẵn lẻ', 'Parity bit')
for x, y in (('10110100', '10011110'), ('11110000', '00111100'), ('01010101', '01010101'[::-1] if False else '01111101')):
    d = sum(a != b for a, b in zip(x, y)); X('m07', 'integrity', f'Khoảng cách Hamming giữa hai từ mã {x} và {y} là:', f'The Hamming distance between the codewords {x} and {y} is:', str(d), [str(d + 1), str(max(d - 1, 0)) if d > 1 else '8', str(8 - d), str(d + 2)], f'Số vị trí bit khác nhau: {d}.', f'Number of differing bit positions: {d}.', 'Khoảng cách Hamming', 'Hamming distance')
for dmin in (3, 4, 5):
    X('m07', 'integrity', f'Một mã có khoảng cách Hamming nhỏ nhất {dmin}. Nó phát hiện được tối đa bao nhiêu bit lỗi và sửa được tối đa bao nhiêu bit?', f'A code has a minimum Hamming distance of {dmin}. At most how many bit errors can it detect and correct?', (f'phát hiện {dmin - 1}, sửa {(dmin - 1) // 2}', f'detect {dmin - 1}, correct {(dmin - 1) // 2}'), [(f'phát hiện {dmin}, sửa {dmin // 2}', f'detect {dmin}, correct {dmin // 2}'), (f'phát hiện {dmin - 1}, sửa {dmin - 1}', f'detect {dmin - 1}, correct {dmin - 1}'), (f'phát hiện {(dmin - 1) // 2}, sửa {dmin - 1}', f'detect {(dmin - 1) // 2}, correct {dmin - 1}')], f'Phát hiện $d-1={dmin - 1}$; sửa $\\lfloor(d-1)/2\\rfloor={(dmin - 1) // 2}$.', f'Detect $d-1={dmin - 1}$; correct $\\lfloor(d-1)/2\\rfloor={(dmin - 1) // 2}$.', 'Khả năng của mã', 'Code capability')
for fleet, hours, rate in ((1000, 3000, '10⁻⁹'), (200, 4000, '10⁻⁹')):
    tot = fleet * hours; exp = tot * 1e-9; X('m07', 'levels', f'Một lỗi mức A phải có xác suất dưới {rate} mỗi giờ bay. Đội {fleet} máy bay bay mỗi chiếc {hours} giờ mỗi năm. Số lỗi mức A kỳ vọng tối đa mỗi năm là:', f'A level A failure must have a probability below {rate} per flight hour. A fleet of {fleet} aircraft each fly {hours} hours a year. The maximum expected number of level A failures a year is:', f'{exp:g}'.replace('e-0', 'e-'), [f'{exp * 1000:g}'.replace('e-0', 'e-'), f'{exp / 1000:g}'.replace('e-0', 'e-'), f'{exp * 10:g}'.replace('e-0', 'e-')], f'{fleet} × {hours} = {tot} giờ; {tot} × 10⁻⁹ = {exp:g}.', f'{fleet} × {hours} = {tot} hours; {tot} × 10⁻⁹ = {exp:g}.', 'Xác suất theo mức hỏng', 'Failure probability by level')
if __name__ == '__main__':
    import collections
    for m, bk in B.items():
        if bk.gen: json.dump(bk.gen, open(os.path.join(OUT, f'{m}_l3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(m, len(bk.gen))
