# -*- coding: utf-8 -*-
"""Cau hoi module 11 (mach tuan tu) -> data/qsrc/m11.json (cau goc Floyd Ch.7-10 co khoa in), m11_gen.json (sinh theo dang, bo_sung), m11_ess.json (tu luan co loi giai tinh bang chuong trinh).
Dap an cua moi cau sinh tinh bang build/numlib/seq.py; verify_m11.py tinh lai doc lap tu de bai."""
import json, os, sys, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); OUT = os.path.join(ROOT, 'data', 'qsrc')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib'))
import seq as S, m11_floyd as F
QB = 'Q̅'
TOP = {'latch': ('Chốt và flip-flop', 'Latches and flip-flops'), 'timing': ('Mạch một nhịp và bộ định thời 555', 'One-shots and the 555 timer'), 'shift': ('Thanh ghi dịch', 'Shift registers'),
       'counter': ('Bộ đếm và máy trạng thái', 'Counters and state machines'), 'pld': ('Logic khả trình (PLD)', 'Programmable logic (PLD)')}
def opt(x): return x if isinstance(x, tuple) else (x, x)
def item(kind, tid, level, origin, qv, qe, opts, c, xv, xe, sv, se, dv='', de=''):
    d = dict(kind=kind, q=dict(vi=qv, en=qe), opts=[dict(vi=opt(o)[0], en=opt(o)[1]) for o in opts], correct=c, explain=dict(vi=xv, en=xe), topic=dict(vi=TOP[tid][0], en=TOP[tid][1]), topic_id=tid, level=level, origin=origin, src=dict(vi=sv, en=se))
    if dv: d['detail'] = dict(vi=dv, en=de)
    return d
TFO = [('Đúng', 'True'), ('Sai', 'False')]
goc = []
for ch, (tf, st, page) in F.CH.items():
    for (n, vi, en, key, xv, xe, lv) in tf:
        tid = ('timing' if n >= 8 else 'latch') if ch == 7 else F.TOPIC[ch][0]
        goc.append(item('tf', tid, lv, 'goc', vi, en, TFO, 0 if key == 'T' else 1, xv, xe, f'Floyd Ch.{ch} · Đúng/Sai {n} (khoá tr.{page})', f'Floyd Ch.{ch} · True/False {n} (key p.{page})'))
    for (n, vi, en, ops, c, xv, xe, lv) in st:
        tid = F.TOPIC[ch][n - 1]
        goc.append(item('mcq', tid, lv, 'goc', vi, en, ops, c, xv, xe, f'Floyd Ch.{ch} · Self-Test {n} (khoá tr.{page})', f'Floyd Ch.{ch} · Self-Test {n} (key p.{page})'))

# ---------------- cau sinh (bo_sung): moi dap an tinh bang seq.py ----------------
gen = []; rng = random.Random(11)
def uniq(lst):
    out = []
    for x in lst:
        if x not in out: out.append(x)
    return out
def mc(tid, lv, qv, qe, correct, wrongs, xv, xe, tagv, tage, dv='', de=''):
    ops = uniq([correct] + wrongs)
    assert len(ops) >= 3, (qe, ops)
    gen.append(item('mcq', tid, lv, 'bo_sung', qv, qe, ops[:4], 0, xv, xe, f'Bổ sung · {tagv}', f'Added · {tage}', dv, de))
def g(x, nd=4):                                          # so thuc -> chuoi gon (dau cham; assemble doi sang dau phay cho ban Viet)
    s = f'{x:.{nd}g}'
    return s.replace('e+0', 'e').rstrip('.') if 'e' not in s else s
def tm(t):                                               # giay -> chuoi co don vi
    for u, k in (('s', 1), ('ms', 1e-3), ('μs', 1e-6), ('ns', 1e-9)):
        if abs(t) >= k * 0.999: return f'{g(t / k)} {u}'
    return f'{g(t / 1e-9)} ns'
def exact(x):                                            # 4 chu so co nghia, hoac 5-6 neu can de giu nguyen gia tri (32,768 kHz)
    for nd in (4, 5, 6):
        t = f'{x:.{nd}g}'
        if abs(float(t) - x) <= 1e-9 * abs(x): return g(x, nd)
    return g(x, 4)
def fq(f):
    f = float(f)
    for u, k in (('MHz', 1e6), ('kHz', 1e3), ('Hz', 1)):
        if f >= k * 0.999: return f'{exact(f / k)} {u}'
    return f'{exact(f)} Hz'
def bits(v, n): return format(v, f'0{n}b')

# G1 tre lan truyen cua bo dem gon song; G2 tan so clock toi da
for n, tpd in ((5, 15), (6, 10), (8, 12), (3, 20)):
    mc('counter', 2, f'Một bộ đếm gợn sóng gồm {n} flip-flop, mỗi flip-flop có trễ lan truyền {tpd} ns. Thời gian để mọi ngõ ra ổn định sau khi quay vòng (trường hợp xấu nhất) là:',
       f'A ripple counter has {n} flip-flops, each with a propagation delay of {tpd} ns. The worst-case time for all outputs to settle after it recycles is:',
       f'{S.ripple_delay(n, tpd)} ns', [f'{tpd} ns', f'{(n - 1) * tpd} ns', f'{2 * n * tpd} ns'], f'Các tầng đổi lần lượt nên trễ cộng dồn: {n} × {tpd} ns = {S.ripple_delay(n, tpd)} ns.',
       f'The stages change in turn so the delays add: {n} × {tpd} ns = {S.ripple_delay(n, tpd)} ns.', f'Bộ đếm gợn sóng {n} FF, {tpd} ns', f'Ripple counter, {n} FFs, {tpd} ns')
for n, tpd in ((4, 12), (5, 16), (8, 10)):
    t = S.ripple_delay(n, tpd) * 1e-9; fmax = 1 / t
    mc('counter', 3, f'Bộ đếm gợn sóng {n} bit dùng flip-flop có trễ {tpd} ns. Tần số clock lớn nhất để các ngõ ra kịp ổn định trước xung kế tiếp xấp xỉ:',
       f'A {n}-bit ripple counter uses flip-flops with a {tpd} ns delay. The highest clock frequency that still lets the outputs settle before the next pulse is about:',
       fq(fmax), [fq(1 / (tpd * 1e-9)), fq(1 / (2 ** n * tpd * 1e-9)), fq(1 / ((n - 1) * tpd * 1e-9))],
       f'Chu kỳ phải lớn hơn {n} × {tpd} ns = {g(t * 1e9)} ns nên $f_{{max}}\\approx 1/{g(t * 1e9)}\\text{{ ns}}$ = {fq(fmax)}.', f'The period must exceed {n} × {tpd} ns = {g(t * 1e9)} ns, so $f_{{max}}\\approx 1/{g(t * 1e9)}\\text{{ ns}}$ = {fq(fmax)}.',
       f'Tần số clock tối đa, {n} FF', f'Maximum clock frequency, {n} FFs',
       '<p>Điều kiện của Floyd 9-2: trễ tích luỹ lớn nhất phải nhỏ hơn chu kỳ clock. Bộ đếm đồng bộ không bị giới hạn này vì mọi flip-flop dùng chung clock.</p>',
       '<p>Floyd 9-2: the maximum cumulative delay must be less than the clock period. A synchronous counter has no such limit because all flip-flops share the clock.</p>')
# G3 so flip-flop cho modulus N
for N in (6, 10, 20, 50, 100):
    n = S.ffs_for_mod(N); mc('counter', 2, f'Số flip-flop tối thiểu cho một bộ đếm modulus {N} là:', f'The minimum number of flip-flops for a modulus-{N} counter is:', str(n), [str(n - 1), str(n + 1), str(N)],
       f'Cần $2^n\\ge {N}$: $2^{n - 1}={2 ** (n - 1)}<{N}\\le 2^{n}={2 ** n}$ nên $n={n}$.', f'We need $2^n\\ge {N}$: $2^{n - 1}={2 ** (n - 1)}<{N}\\le 2^{n}={2 ** n}$, so $n={n}$.', f'Modulus {N}', f'Modulus {N}')
# G4 dem len nhi phan; G5 dem xuong; G6 modulus N
for n, start, k in ((4, 0b0110, 13), (4, 0b1011, 9), (5, 0b10101, 20), (3, 0b101, 6)):
    r = S.ripple(n, k, start); wrong = [bits((start + k) % (1 << n) ^ 1, n), bits((start + k + 1) % (1 << n), n), bits((start + k - 1) % (1 << n), n)]
    mc('counter', 2, f'Bộ đếm nhị phân lên {n} bit đang ở {bits(start, n)}. Sau {k} xung clock, trạng thái là:', f'A {n}-bit binary up counter is at {bits(start, n)}. After {k} clock pulses its state is:', bits(r, n), wrong,
       f'{start} + {k} = {start + k}; modulo $2^{n}={1 << n}$ ta được {r} = {bits(r, n)}.', f'{start} + {k} = {start + k}; modulo $2^{n}={1 << n}$ gives {r} = {bits(r, n)}.', f'Đếm lên {n} bit', f'{n}-bit up count')
for start, k in ((3, 5), (2, 9), (0, 3)):
    r = S.down(4, k, start); mc('counter', 2, f'Bộ đếm xuống nhị phân 4 bit đang ở {bits(start, 4)}. Sau {k} xung clock trạng thái là:', f'A 4-bit binary down counter is at {bits(start, 4)}. After {k} clock pulses its state is:', bits(r, 4),
       [bits((start + k) % 16, 4), bits((r + 1) % 16, 4), bits((r - 1) % 16, 4)], f'{start} − {k} = {start - k}; quay vòng modulo 16 cho {r} = {bits(r, 4)}.', f'{start} − {k} = {start - k}; wrapping modulo 16 gives {r} = {bits(r, 4)}.', 'Đếm xuống 4 bit', '4-bit down count')
for N, k in ((10, 23), (12, 30), (60, 125)):
    r = S.mod_n(N, k); mc('counter', 2, f'Một bộ đếm modulus {N} đếm lên từ 0. Sau {k} xung clock, giá trị đếm (thập phân) là:', f'A modulus-{N} counter counts up from 0. After {k} clock pulses the count (decimal) is:', str(r),
       [str(k % (N + 1)), str(r + 1 if r + 1 < N else r - 1), str(k)], f'{k} mod {N} = {r}.', f'{k} mod {N} = {r}.', f'Modulus {N}', f'Modulus {N}')
# G7 chia tan so
for f, ms in ((12e6, (6, 10, 10)), (1e6, (10, 10, 10)), (2.4e6, (4, 6, 10)), (32768, (2,) * 15)):
    out = S.freq_div(f, ms); prod = S.cascade_mod(ms)
    desc_v = ' và '.join(f'modulus {m}' for m in sorted(set(ms))) if len(set(ms)) > 1 else f'{len(ms)} tầng modulus {ms[0]}'
    desc_e = ' and '.join(f'modulus {m}' for m in sorted(set(ms))) if len(set(ms)) > 1 else f'{len(ms)} stages of modulus {ms[0]}'
    qv = f'Clock {fq(f)} đưa vào chuỗi bộ đếm mắc tầng gồm các tầng ' + ', '.join(str(m) for m in ms) + ' (modulus). Tần số ra cuối cùng là:' if len(ms) <= 4 else f'Clock {fq(f)} đưa vào {len(ms)} tầng chia đôi mắc tầng. Tần số ra cuối cùng là:'
    qe = f'A {fq(f)} clock drives a cascade of counters with moduli ' + ', '.join(str(m) for m in ms) + '. The final output frequency is:' if len(ms) <= 4 else f'A {fq(f)} clock drives {len(ms)} cascaded divide-by-2 stages. The final output frequency is:'
    mc('counter', 3, qv, qe, fq(out), [fq(Fr(f) / sum(ms)), fq(Fr(f) / (prod * 2)), fq(Fr(f) / (prod // ms[0]))],
       f'Modulus tổng = {" × ".join(map(str, ms)) if len(ms) <= 4 else "2^" + str(len(ms))} = {prod}; $f_{{out}}=f/{prod}$ = {fq(out)}.', f'Overall modulus = {" × ".join(map(str, ms)) if len(ms) <= 4 else "2^" + str(len(ms))} = {prod}; $f_{{out}}=f/{prod}$ = {fq(out)}.', 'Chia tần số bằng bộ đếm mắc tầng', 'Frequency division by cascaded counters')
# G8 thoi gian nhap noi tiep; G9 duong tre
for nb, f in ((16, 2e6), (32, 4e6), (12, 250e3), (10, 50e3)):
    t = S.serial_time(nb, f); mc('shift', 2, f'Clock {fq(f)}. Nhập nối tiếp {nb} bit vào một thanh ghi dịch mất:', f'With a {fq(f)} clock, entering {nb} bits serially into a shift register takes:', tm(float(t)),
       [tm(float(t) / nb), tm(float(t) * (nb - 1) / nb if nb > 1 else float(t)), tm(float(t) * 2)], f'{nb} bit × chu kỳ {tm(1 / f)} = {tm(float(t))}.', f'{nb} bits × a period of {tm(1 / f)} = {tm(float(t))}.', 'Thời gian nhập nối tiếp', 'Serial entry time')
for nb, t in ((16, 40e-6), (64, 16e-6), (8, 2e-3), (32, 12.8e-6)):
    f = S.delay_clock(nb, Fr(str(t))); mc('shift', 3, f'Một thanh ghi dịch vào nối tiếp/ra nối tiếp {nb} bit dùng làm đường trễ {tm(t)}. Tần số clock cần dùng là:', f'A {nb}-bit serial in/serial out shift register is used as a {tm(t)} delay line. The clock frequency needed is:', fq(f),
       [fq(Fr(1) / Fr(str(t))), fq(f / nb), fq(f * 2)], f'Trễ = số bit / tần số nên $f=N/t={nb}/{tm(t)}$ = {fq(f)}.', f'Delay = bits / frequency, so $f=N/t={nb}/{tm(t)}$ = {fq(f)}.', 'Đường trễ bằng thanh ghi dịch', 'Shift-register delay line')
# G10 noi dung thanh ghi sau khi dich
for reg, data in (('1010', '1101'), ('10110011', '0110'), ('00001111', '101'), ('11001', '011')):
    r = S.shift_right(reg, data, 'right'); wrong = [S.shift_right(reg, data, 'left'), reg, ''.join(reversed(r))]
    if wrong[2] == r: wrong[2] = reg[1:] + reg[0]
    mc('shift', 2, f'Thanh ghi dịch phải {len(reg)} bit chứa {reg}. Chuỗi {data} được nhập nối tiếp (bit ngoài cùng bên phải vào trước) ở đầu trái, {len(data)} xung clock. Thanh ghi chứa:',
       f'A {len(reg)}-bit shift-right register holds {reg}. The bits {data} are entered serially at the left end (right-most bit first) over {len(data)} clock pulses. The register then holds:', r, wrong,
       f'Mỗi xung dịch phải một vị trí và bit mới vào bên trái; sau {len(data)} xung: {r}.', f'Each pulse shifts one place right and a new bit enters on the left; after {len(data)} pulses: {r}.', 'Dịch bit nối tiếp', 'Serial shifting')
# G11 vong / Johnson
for n, k in ((4, 3), (4, 5), (5, 7)):
    r = S.johnson(n, k); mc('shift', 3, f'Bộ đếm Johnson {n} flip-flop khởi đầu ở {"0" * n} (ngõ ra đảo của tầng cuối nối về ngõ vào, dịch phải). Sau {k} xung clock trạng thái là:',
       f'A {n}-flip-flop Johnson counter starts at {"0" * n} (the inverted last output feeds the first input, shifting right). After {k} clock pulses its state is:', r, [S.ring(n, k), S.johnson(n, k + 1), S.johnson(n, k - 1)],
       f'Chuỗi Johnson: ' + ' → '.join(S.johnson(n, j) for j in range(0, k + 1)) + '.', 'Johnson sequence: ' + ' → '.join(S.johnson(n, j) for j in range(0, k + 1)) + '.', 'Bộ đếm Johnson', 'Johnson counter')
for N in (10, 16):
    mc('shift', 2, f'Cần bao nhiêu flip-flop để làm bộ đếm vòng và bộ đếm Johnson modulus {N}?', f'How many flip-flops are needed for a ring counter and for a Johnson counter of modulus {N}?', f'vòng {N}, Johnson {N // 2}'.replace('vòng', 'vòng') if False else (f'vòng: {N}, Johnson: {N // 2}', f'ring: {N}, Johnson: {N // 2}'),
       [(f'vòng: {N // 2}, Johnson: {N}', f'ring: {N // 2}, Johnson: {N}'), (f'vòng: {N}, Johnson: {N}', f'ring: {N}, Johnson: {N}'), (f'vòng: {N // 2}, Johnson: {N // 2}', f'ring: {N // 2}, Johnson: {N // 2}')],
       f'Vòng: modulus = số FF = {N}. Johnson: modulus = 2 × số FF nên {N // 2} FF.', f'Ring: modulus = number of FFs = {N}. Johnson: modulus = 2 × FFs so {N // 2} FFs.', 'Số FF của bộ đếm vòng và Johnson', 'FFs in ring and Johnson counters')
# G12 J-K; G13 chot S-R; G14 chia tan so bang T
for q0, steps in ((0, [(1, 0), (1, 1), (0, 0), (1, 1)]), (1, [(0, 1), (1, 1), (1, 1), (0, 0)]), (0, [(1, 1), (1, 1), (0, 1), (1, 0)]), (1, [(1, 0), (0, 0), (1, 1)])):
    qs = []; q = q0
    for j, k in steps: q = S.jk(j, k, q); qs.append(q)
    fmt = lambda l: ','.join(map(str, l)); wrong = [fmt([1 - x for x in qs]), fmt([S.t_ff(1, q0)] + qs[:-1]), fmt([q0] * len(qs))]
    mc('latch', 2, f'Flip-flop J-K kích sườn có Q = {q0}. Các cặp (J, K) trước mỗi xung clock là ' + ' ; '.join(f'({j},{k})' for j, k in steps) + '. Chuỗi Q sau từng xung là:',
       f'An edge-triggered J-K flip-flop starts with Q = {q0}. The (J, K) pairs before each clock pulse are ' + ' ; '.join(f'({j},{k})' for j, k in steps) + '. The sequence of Q after each pulse is:', fmt(qs), wrong,
       'Dùng bảng J-K: 00 giữ, 01 xoá, 10 đặt, 11 lật. Kết quả: ' + fmt(qs) + '.', 'Using the J-K table: 00 hold, 01 reset, 10 set, 11 toggle. Result: ' + fmt(qs) + '.', 'Dãy trạng thái J-K', 'J-K state sequence')
for kind, seqs, q0 in (('NOR', [(1, 0), (0, 0)], 0), ('NOR', [(0, 1), (0, 0)], 1), ('NAND', [(0, 1), (1, 1)], 0), ('NAND', [(1, 0), (1, 1)], 1)):
    Q, Qb = (q0, 1 - q0)
    for a, b in seqs: Q, Qb = (S.sr_nor(a, b, Q, Qb) if kind == 'NOR' else S.sr_nand(a, b, Q, Qb))
    lab = lambda q, qb: f'Q = {q}, {QB} = {qb}'
    act_v, act_e = ('mức CAO', 'active-HIGH') if kind == 'NOR' else ('mức THẤP', 'active-LOW')
    mc('latch', 2, f'Chốt S-R tác dụng {act_v} (hai cổng {kind}) đang ở Q = {q0}. Đặt lần lượt (S, R) = ' + ' rồi '.join(f'({a},{b})' for a, b in seqs) + '. Trạng thái cuối là:',
       f'An {act_e} S-R latch ({kind} gates) starts with Q = {q0}. The inputs (S, R) are applied in turn: ' + ' then '.join(f'({a},{b})' for a, b in seqs) + '. The final state is:', lab(Q, Qb),
       [lab(1 - Q, 1 - Qb), lab(0, 0), lab(1, 1)], f'Bước cuối giữ trạng thái do bước trước đặt: {lab(Q, Qb)}.' if seqs[-1] in ((0, 0), (1, 1)) else f'Kết quả: {lab(Q, Qb)}.',
       f'The final step holds the state set by the previous one: {lab(Q, Qb)}.' if seqs[-1] in ((0, 0), (1, 1)) else f'Result: {lab(Q, Qb)}.', f'Chốt S-R {kind}', f'{kind} S-R latch')
for n, f in ((3, 8e3), (5, 640e3), (8, 2.56e6), (10, 1.024e6)):
    mc('latch', 2, f'{n} flip-flop J-K, mỗi cái có J = K = 1, mắc nối tiếp (gợn sóng). Clock {fq(f)}. Tần số của ngõ ra tầng cuối là:', f'{n} J-K flip-flops, each with J = K = 1, are cascaded as a ripple chain. The clock is {fq(f)}. The output frequency of the last stage is:',
       fq(f / 2 ** n), [fq(f / n), fq(f / 2 ** (n - 1)), fq(f / (2 ** n - 1))], f'Mỗi tầng chia đôi tần số nên $f/2^{n}$ = {fq(f / 2 ** n)}.', f'Each stage halves the frequency so $f/2^{n}$ = {fq(f / 2 ** n)}.', 'Chia tần số bằng flip-flop lật', 'Frequency division with toggling flip-flops')
# G15 74121; G16 555 mot nhip; G17 555 dao dong
for tw in (10e-6, 20e-6, 5e-6):
    C = tw / (0.7 * 2000); show = lambda c: (f'{g(c * 1e12)} pF' if c < 1e-9 else f'{g(c * 1e9)} nF')
    mc('timing', 2, f'Mạch một nhịp 74121 dùng điện trở trong 2 kΩ. Muốn xung ra rộng {tm(tw)} ($t_W=0{{,}}7\\,R\\,C_{{EXT}}$) cần tụ ngoài xấp xỉ:', f'A 74121 one-shot uses its internal 2 kΩ resistor. For an output pulse {tm(tw)} wide ($t_W=0.7\\,R\\,C_{{EXT}}$) the external capacitor must be about:',
       show(C), [show(C * 0.7), show(C / 0.7), show(C * 2)], f'$C=t_W/(0{{,}}7R)={tm(tw)}/(0{{,}}7\\times 2\\text{{ k}}\\Omega)$ = {show(C)}.', f'$C=t_W/(0.7R)={tm(tw)}/(0.7\\times 2\\text{{ k}}\\Omega)$ = {show(C)}.', 'Tụ cho 74121', 'Capacitor for a 74121')
for R, C in ((10e3, 1e-6), (47e3, 0.1e-6), (100e3, 10e-9)):
    tw = S.t555_mono(R, C); mc('timing', 2, f'Bộ định thời 555 ở chế độ một nhịp có R = {g(R / 1e3)} kΩ và C = {tm(C).replace(" s", " F") if False else (g(C * 1e6) + " μF" if C >= 1e-7 else g(C * 1e9) + " nF")}. Độ rộng xung ra ($t_W=1{{,}}1RC$) là:',
       f'A 555 timer in monostable mode has R = {g(R / 1e3)} kΩ and C = {(g(C * 1e6) + " μF") if C >= 1e-7 else (g(C * 1e9) + " nF")}. The output pulse width ($t_W=1.1RC$) is:', tm(tw), [tm(S.one_shot(R, C)), tm(R * C), tm(2.2 * R * C)],
       f'$t_W=1{{,}}1RC$ = {tm(tw)}.', f'$t_W=1.1RC$ = {tm(tw)}.', '555 một nhịp', '555 monostable')
for R1, R2, C in ((1e3, 2e3, 0.1e-6), (10e3, 10e3, 0.01e-6), (4.7e3, 47e3, 1e-6), (2.2e3, 6.8e3, 0.1e-6)):
    a = S.t555_astable(R1, R2, C); Cs = (g(C * 1e6) + ' μF') if C >= 1e-7 else (g(C * 1e9) + ' nF')
    ctx_v = f'Bộ định thời 555 mạch dao động có R1 = {g(R1 / 1e3)} kΩ, R2 = {g(R2 / 1e3)} kΩ, C = {Cs}.'; ctx_e = f'A 555 astable has R1 = {g(R1 / 1e3)} kΩ, R2 = {g(R2 / 1e3)} kΩ, C = {Cs}.'
    mc('timing', 3, ctx_v + ' Tần số ngõ ra $f=1{,}44/((R_1+2R_2)C)$ xấp xỉ:', ctx_e + ' The output frequency $f=1.44/((R_1+2R_2)C)$ is about:', fq(a['f']), [fq(1.44 / ((R1 + R2) * C)), fq(1.44 / (R2 * C)), fq(1 / ((R1 + 2 * R2) * C))],
       f'$T=0{{,}}7(R_1+2R_2)C$ = {tm(a["T"])} nên $f$ = {fq(a["f"])}.', f'$T=0.7(R_1+2R_2)C$ = {tm(a["T"])} so $f$ = {fq(a["f"])}.', '555 dao động: tần số', '555 astable: frequency')
    mc('timing', 3, ctx_v + ' Chu kỳ làm việc (duty cycle) của ngõ ra là:', ctx_e + ' The duty cycle of the output is:', f'{g(a["duty"] * 100, 3)} %', [f'{g(R2 / (R1 + 2 * R2) * 100, 3)} %', '50 %', f'{g((R1 + R2) / (R1 + R2 + R2) * 100 + 0 if False else R1 / (R1 + 2 * R2) * 100, 3)} %'],
       f'duty = $(R_1+R_2)/(R_1+2R_2)$ = {g(a["duty"] * 100, 3)} %: lớn hơn 50 % vì tụ nạp qua R1 + R2 nhưng xả chỉ qua R2.', f'duty = $(R_1+R_2)/(R_1+2R_2)$ = {g(a["duty"] * 100, 3)} %: above 50 % because C charges through R1 + R2 but discharges only through R2.', '555 dao động: chu kỳ làm việc', '555 astable: duty cycle')
# G18 LUT; G19 bo dem BCD reset
for n in (3, 4, 5):
    mc('pld', 3, f'Một bảng tra (LUT) có {n} ngõ vào lưu bao nhiêu bit, và có thể thực hiện bao nhiêu hàm logic khác nhau của {n} biến?', f'A {n}-input look-up table (LUT) stores how many bits, and can implement how many different logic functions of {n} variables?',
       (f'{2 ** n} bit; {2 ** (2 ** n)} hàm', f'{2 ** n} bits; {2 ** (2 ** n)} functions'), [(f'{n} bit; {2 ** n} hàm', f'{n} bits; {2 ** n} functions'), (f'{2 ** n} bit; {2 ** n} hàm', f'{2 ** n} bits; {2 ** n} functions'), (f'{2 ** n - 1} bit; {2 ** (2 ** n - 1)} hàm', f'{2 ** n - 1} bits; {2 ** (2 ** n - 1)} functions')],
       f'Một ô cho mỗi tổ hợp ngõ vào: $2^{n}={2 ** n}$ bit; mỗi bit chọn tự do 0 hoặc 1 nên có $2^{{2^{n}}}={2 ** (2 ** n)}$ hàm.', f'One cell per input combination: $2^{n}={2 ** n}$ bits; each bit is free to be 0 or 1 so there are $2^{{2^{n}}}={2 ** (2 ** n)}$ functions.', 'LUT', 'LUT')
for N in (10, 12, 6):
    s = bits(N, 4); mc('counter', 2, f'Bộ đếm gợn sóng 4 bit được cắt cụt thành modulus {N} bằng cách reset không đồng bộ. Trạng thái nào phải được giải mã để kích reset?', f'A 4-bit ripple counter is truncated to modulus {N} with an asynchronous reset. Which state must be decoded to trigger the reset?', s,
       [bits(N - 1, 4), bits(N + 1, 4), '1111'], f'Bộ đếm phải đếm 0 đến {N - 1}; khi đạt {N} = {s} nó bị reset ngay về 0000, nên trạng thái {s} chỉ tồn tại thoáng qua.', f'The counter must count 0 to {N - 1}; on reaching {N} = {s} it is reset to 0000 at once, so {s} exists only for an instant.', f'Cắt cụt về modulus {N}', f'Truncating to modulus {N}')

# ---------------- tu luan co loi giai (bo_sung, tinh bang chuong trinh) ----------------
ess = []
def E(tid, lv, qv, qe, sv, se, tagv, tage): ess.append(dict(kind='ess', q=dict(vi=qv, en=qe), sol=dict(vi=sv, en=se), topic=dict(vi=TOP[tid][0], en=TOP[tid][1]), topic_id=tid, level=lv, origin='bo_sung', src=dict(vi=f'Bổ sung · {tagv}', en=f'Added · {tage}')))
n, tpd, f = 4, 15, 1e6
E('counter', 3, f'Bộ đếm gợn sóng 4 bit dùng flip-flop J-K có trễ lan truyền 15 ns, clock 1 MHz. (a) Modulus? (b) Tổng thời gian ổn định khi quay vòng? (c) Tần số clock tối đa? (d) Tần số của ngõ ra tầng cuối?',
  f'A 4-bit ripple counter uses J-K flip-flops with a 15 ns propagation delay and a 1 MHz clock. (a) Modulus? (b) Total settling time when it recycles? (c) Maximum clock frequency? (d) Frequency of the last-stage output?',
  f'(a) $2^4$ = 16. (b) 4 × 15 ns = {S.ripple_delay(4, 15)} ns. (c) $f_{{max}}=1/60\\text{{ ns}}$ = {fq(1 / (S.ripple_delay(4, 15) * 1e-9))}. (d) 1 MHz / 16 = {fq(1e6 / 16)}. Chu kỳ clock 1 μs lớn hơn 60 ns nên bộ đếm làm việc đúng.',
  f'(a) $2^4$ = 16. (b) 4 × 15 ns = {S.ripple_delay(4, 15)} ns. (c) $f_{{max}}=1/60\\text{{ ns}}$ = {fq(1 / (S.ripple_delay(4, 15) * 1e-9))}. (d) 1 MHz / 16 = {fq(1e6 / 16)}. The 1 μs clock period exceeds 60 ns so the counter works correctly.', 'Bộ đếm gợn sóng 4 bit', '4-bit ripple counter')
E('counter', 3, 'Thiết kế bộ đếm BCD (modulus 10) bằng bộ đếm nhị phân 4 bit có reset không đồng bộ: (a) cần mấy flip-flop? (b) trạng thái nào kích reset? (c) trạng thái 1010 tồn tại bao lâu? (d) clock 100 kHz thì tần số ngõ ra của tầng cuối bộ đếm modulus 10 là bao nhiêu?',
  'Design a BCD (modulus-10) counter from a 4-bit binary counter with asynchronous reset: (a) how many flip-flops? (b) which state triggers the reset? (c) how long does state 1010 exist? (d) with a 100 kHz clock, what is the output frequency of the last stage of the modulus-10 counter?',
  '(a) $2^3=8<10\\le 2^4$ nên 4 flip-flop. (b) Giải mã 1010 (số 10) bằng cổng NAND hai ngõ vào Q1 và Q3 (các bit 1 của 1010) rồi nối vào ngõ vào CLR của mọi flip-flop. (c) Chỉ thoáng qua, cỡ trễ của cổng NAND cộng thời gian xoá của flip-flop (vài chục ns): đó là gai (glitch) cần lưu ý. (d) Chu kỳ ra của chuỗi 10 trạng thái là 10 xung clock: 100 kHz / 10 = 10 kHz (Q3 không đối xứng: mức cao 2 xung, thấp 8 xung).',
  '(a) $2^3=8<10\\le 2^4$ so 4 flip-flops. (b) Decode 1010 (ten) with a two-input NAND on Q1 and Q3 (the 1s of 1010) and connect it to the CLR inputs of all flip-flops. (c) Only a glitch, about a NAND-gate delay plus the clear time of the flip-flop (tens of ns): a hazard to be aware of. (d) The output period of the 10-state sequence is 10 clock pulses: 100 kHz / 10 = 10 kHz (Q3 is not symmetric: HIGH for 2 pulses, LOW for 8).', 'Bộ đếm BCD từ bộ đếm nhị phân', 'BCD counter from a binary counter')
E('timing', 3, 'Bộ định thời 555 mạch dao động có R1 = 1 kΩ, R2 = 2 kΩ, C = 0,1 μF. Tính $t_H$, $t_L$, chu kỳ, tần số và duty cycle. Cần thay đổi gì để duty cycle nhỏ hơn 50 %?',
  'A 555 astable has R1 = 1 kΩ, R2 = 2 kΩ, C = 0.1 μF. Find $t_H$, $t_L$, the period, the frequency and the duty cycle. What must change to get a duty cycle below 50 %?',
  (lambda a: f'$t_H=0{{,}}7(R_1+R_2)C$ = {tm(a["tH"])}; $t_L=0{{,}}7R_2C$ = {tm(a["tL"])}; $T$ = {tm(a["T"])}; $f$ = {fq(a["f"])}; duty = {g(a["duty"] * 100, 3)} %. Để duty cycle dưới 50 % mắc thêm diode song song với R2 (Floyd Hình 7-59) để tụ nạp chỉ qua R1 và xả qua R2, với R1 nhỏ hơn R2.')(S.t555_astable(1e3, 2e3, 0.1e-6)),
  (lambda a: f'$t_H=0.7(R_1+R_2)C$ = {tm(a["tH"])}; $t_L=0.7R_2C$ = {tm(a["tL"])}; $T$ = {tm(a["T"])}; $f$ = {fq(a["f"])}; duty = {g(a["duty"] * 100, 3)} %. For a duty cycle below 50 % add a diode across R2 (Floyd Figure 7-59) so that C charges through R1 only and discharges through R2, with R1 smaller than R2.')(S.t555_astable(1e3, 2e3, 0.1e-6)),
  '555 dao động đầy đủ', 'Full 555 astable')
E('shift', 2, 'Thanh ghi dịch phải 8 bit chứa 00000000. Nhập nối tiếp dãy 11010010 (bit ngoài cùng bên phải vào trước) ở đầu trái với clock 250 kHz. (a) Nội dung sau từng xung (liệt kê). (b) Thời gian nhập. (c) Nếu dùng thanh ghi này làm đường trễ cho tín hiệu nối tiếp, trễ là bao nhiêu?',
  'An 8-bit shift-right register holds 00000000. The sequence 11010010 is entered serially (right-most bit first) at the left end with a 250 kHz clock. (a) The contents after each pulse (list them). (b) The entry time. (c) If this register is used as a delay line for a serial signal, what is the delay?',
  (lambda rows: '(a) ' + '; '.join(rows) + f'. (b) 8 × 4 μs = {tm(float(S.serial_time(8, 250e3)))}. (c) Mỗi bit đi qua 8 tầng nên trễ bằng đúng thời gian nhập = {tm(float(S.serial_time(8, 250e3)))}.')([S.shift_right('00000000', '11010010'[::-1][:k][::-1] if False else '11010010'[8 - k:], 'right') for k in range(1, 9)]),
  (lambda rows: '(a) ' + '; '.join(rows) + f'. (b) 8 × 4 μs = {tm(float(S.serial_time(8, 250e3)))}. (c) Each bit passes through 8 stages so the delay equals the entry time = {tm(float(S.serial_time(8, 250e3)))}.')([S.shift_right('00000000', '11010010'[8 - k:], 'right') for k in range(1, 9)]),
  'Nhập nối tiếp 8 bit', '8-bit serial entry')
E('shift', 2, 'Lập bảng trạng thái 8 xung đầu của bộ đếm Johnson 4 flip-flop khởi đầu 0000 và của bộ đếm vòng 4 flip-flop khởi đầu 1000. So sánh modulus và số cổng giải mã cần thiết để nhận biết từng trạng thái.',
  'Tabulate the first 8 pulses of a 4-flip-flop Johnson counter starting at 0000 and of a 4-flip-flop ring counter starting at 1000. Compare their moduli and the number of gates needed to decode each state.',
  'Johnson: ' + ' → '.join(S.johnson(4, k) for k in range(9)) + '. Vòng: ' + ' → '.join(S.ring(4, k) for k in range(9)) + '. Modulus Johnson = 8 (2n), vòng = 4 (n). Mỗi trạng thái Johnson giải mã bằng một cổng AND hai ngõ vào (chỉ cần xét hai tầng kề nhau); trạng thái vòng đọc trực tiếp từ một ngõ ra, không cần cổng.',
  'Johnson: ' + ' → '.join(S.johnson(4, k) for k in range(9)) + '. Ring: ' + ' → '.join(S.ring(4, k) for k in range(9)) + '. Johnson modulus = 8 (2n), ring = 4 (n). Each Johnson state decodes with one two-input AND gate (only two adjacent stages matter); a ring state is read directly from one output, no gate.', 'Johnson so với vòng', 'Johnson versus ring')
E('pld', 2, 'Một hàm $F=\\overline{A}B+A\\overline{B}$ (XOR) cần thực hiện bằng PAL. (a) Có bao nhiêu số hạng tích? (b) Bảng cầu chì (fuse map) cần giữ lại những liên kết nào? (c) Một LUT 2 ngõ vào chứa nội dung gì để thực hiện cùng hàm?',
  'A function $F=\\overline{A}B+A\\overline{B}$ (XOR) is to be built in a PAL. (a) How many product terms? (b) Which links must the fuse map keep? (c) What does a 2-input LUT hold to implement the same function?',
  '(a) Hai số hạng tích: $\\overline{A}B$ và $A\\overline{B}$, đưa vào một cổng OR cố định. (b) Số hạng 1 giữ liên kết từ $\\overline{A}$ và $B$ (đốt các cầu chì còn lại); số hạng 2 giữ liên kết từ $A$ và $\\overline{B}$. (c) LUT 4 ô theo thứ tự AB = 00, 01, 10, 11 chứa 0, 1, 1, 0.',
  '(a) Two product terms, $\\overline{A}B$ and $A\\overline{B}$, feeding a fixed OR gate. (b) Term 1 keeps the links from $\\overline{A}$ and $B$ (the other fuses are blown); term 2 keeps those from $A$ and $\\overline{B}$. (c) A 4-cell LUT for AB = 00, 01, 10, 11 holds 0, 1, 1, 0.', 'XOR trên PAL và LUT', 'XOR in a PAL and a LUT')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, data in (('m11.json', goc), ('m11_gen.json', gen), ('m11_ess.json', ess)):
        json.dump(data, open(os.path.join(OUT, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import collections
    print('goc', len(goc), collections.Counter(i['level'] for i in goc), '| gen', len(gen), collections.Counter(i['level'] for i in gen), '| ess', len(ess))
