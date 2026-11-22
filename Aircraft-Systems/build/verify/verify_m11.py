# -*- coding: utf-8 -*-
"""Verify module 11 (mach tuan tu): (1) moi ham cua seq.py co hai cai dat khop nhau; (2) so lieu va quy tac trong sach; (3) MOI cau sinh tinh lai tu de bai (EN) bang cach doc lap voi gen_m11.py/seq.py
(so nguyen, Fraction, bang chan tri); (4) khoa in cua Floyd tinh duoc bang chuong trinh thi phai khop.
Chay: python3 build/verify/verify_m11.py   -> cuoi cung in 'FAILS: none'."""
import sys, os, re, json, math, itertools
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
import seq as S
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
# ---- 1. hai cai dat ----
for s_, r_, q, qb in itertools.product((0, 1), (0, 1), (0, 1), (0, 1)):
    if q == qb: continue                                   # chi xet trang thai bu nhau (Q, Qb) ban dau
    check(f'sr_nor {s_}{r_}{q}', S.sr_nor_a(s_, r_, q, qb) == S.sr_nor_b(s_, r_, q, qb) if (s_, r_) != (1, 1) else S.sr_nor_a(1, 1, q, qb) == (0, 0))
    check(f'sr_nand {s_}{r_}{q}', S.sr_nand_a(s_, r_, q, qb) == S.sr_nand_b(s_, r_, q, qb) if (s_, r_) != (0, 0) else S.sr_nand_a(0, 0, q, qb) == (1, 1))
for j, k, q in itertools.product((0, 1), repeat=3): check(f'jk {j}{k}{q}', S.jk_a(j, k, q) == S.jk_b(j, k, q))
for t, q in itertools.product((0, 1), repeat=2): check(f't {t}{q}', S.t_ff_a(t, q) == S.t_ff_b(t, q))
for n in range(1, 9):
    for k in range(0, 300, 7):
        for start in (0, 1, (1 << n) - 1, 5 % (1 << n)): check(f'ripple {n},{k},{start}', S.ripple_a(n, k, start) == S.ripple_b(n, k, start) == (start + k) % (1 << n) and S.down_a(n, k, start) == S.down_b(n, k, start))
for N in range(2, 200):
    check(f'ffs {N}', S.ffs_for_mod_a(N) == S.ffs_for_mod_b(N) == (N - 1).bit_length())
    check(f'mod_n {N}', all(S.mod_n_a(N, k) == S.mod_n_b(N, k) for k in (0, 1, N - 1, N, N + 3, 3 * N + 2)))
for n in range(1, 9):
    for k in range(0, 40): check(f'ring/johnson {n},{k}', S.ring_a(n, k) == S.ring_b(n, k) and S.johnson_a(n, k) == S.johnson_b(n, k))
for reg, data in (('1010', '1101'), ('11100100', '10110101'), ('00001111', '101')):
    for side in ('right', 'left'): check(f'shift {reg},{data},{side}', S.shift_right_a(reg, data, side) == S.shift_right_b(reg, data, side))
for R, C in ((2000, 7.143e-9), (10e3, 1e-6), (2200, 1e-8)):
    check(f'one-shot {R},{C}', abs(S.one_shot_a(R, C) / S.one_shot_b(R, C) - 1) < 0.011); check(f'555 mono {R},{C}', abs(S.t555_mono_a(R, C) / S.t555_mono_b(R, C) - 1) < 0.011)
for R1, R2, C in ((1e3, 2e3, 1e-7), (4.7e3, 47e3, 1e-6), (2.2e3, 6.8e3, 1e-7)):
    a, b = S.t555_astable_a(R1, R2, C), S.t555_astable_b(R1, R2, C)
    check(f'555 astable {R1},{R2}', abs(a['duty'] - b['duty']) < 1e-12 and abs(a['f'] / b['f'] - 1) < 0.011 and abs(a['tH'] / b['tH'] - 1) < 0.011)
# ---- 2. so lieu va quy tac trong sach ----
check('JK: phuong trinh dac trung = bang J-K', all(S.jk_b(j, k, q) == {(0, 0): q, (0, 1): 0, (1, 0): 1, (1, 1): 1 - q}[(j, k)] for j, k, q in itertools.product((0, 1), repeat=3)))
EXC = {(0, 0): (0, None), (0, 1): (1, None), (1, 0): (None, 1), (1, 1): (None, 0)}          # bang kich J-K: dung mot cach hoan toan khac (thu mot J,K de tim Q+)
for (q, q2), (j, k) in EXC.items():
    ok = all(S.jk_b(jj, kk, q) == q2 for jj in ((j,) if j is not None else (0, 1)) for kk in ((k,) if k is not None else (0, 1)))
    check(f'bang kich J-K {q}->{q2}', ok)
check('Floyd Ch.8 Self-Test 4: 11100100, hai bit ngoai cung ben phai cua 10110101 vao truoc (1 roi 0) -> 01111001', S.shift_right('11100100', '10110101'[-2:], 'right') == '01111001')
reg = '11100100'; reg = '1' + reg[:-1]; reg = '0' + reg[:-1]; check('Floyd Ch.8 Self-Test 4 (tu tay): bit 1 roi bit 0 vao ben trai', reg == '01111001')
check('Floyd Ch.8 Self-Test 5: 8 bit, 100 kHz = 80 us', S.serial_time(8, 100e3) == Fr(80, 10 ** 6)); check('Floyd Ch.8 Self-Test 9: 8 bit / 24 us = 333,3 kHz', abs(float(S.delay_clock(8, Fr(24, 10 ** 6))) - 333333.33) < 1)
check('Floyd Ch.8 Self-Test 7, 8: Johnson mod 8 = 4 FF, vong mod 8 = 8 FF', len(S.johnson(4, 1)) == 4 and len({S.johnson(4, k) for k in range(20)}) == 8 and len({S.ring(8, k) for k in range(20)}) == 8)
st_ = [1] * 7 + [0]; low_ = []
for _ in range(16): low_.append(st_.index(0)); st_ = st_[-1:] + st_[:-1]
check('Floyd Ch.8 Self-Test 10 (Hinh 8-36): bo dem vong bay bit 1 mot bit 0: moi xung dung mot hang THAP, du 8 hang roi lap lai', sorted(low_[:8]) == list(range(8)) and low_[:8] == low_[8:])
check('Floyd Ch.8 Checkup 8-5: 5 kHz / 8 hang = 625 lan quet moi giay', 5000 // 8 == 625)
check('Floyd Ch.9 Self-Test 10: 4 x 12 ns = 48 ns', S.ripple_delay(4, 12) == 48); check('Floyd Ch.9 Self-Test 14: 10 MHz / (5.8.10.10) = 2,5 kHz', S.freq_div(10e6, (5, 8, 10, 10)) == Fr(2500))
check('Floyd Ch.9 Self-Test 15: xuong tu 0000 = 1111', S.down(4, 1, 0) == 15); check('Floyd Ch.9 Dung/Sai 7: 1000 -> 0111 khi dem xuong', S.down(4, 1, 8) == 7)
check('Floyd Ch.9 Self-Test 13: 10^3 = 1000', S.cascade_mod((10, 10, 10)) == 1000); check('Floyd Ch.9 Self-Test 8: mod 12 can 4 FF', S.ffs_for_mod(12) == 4); check('Floyd Ch.9 Dung/Sai 6: mod 32 can 5 tang', S.ffs_for_mod(32) == 5)
check('Floyd Ch.7 Self-Test 9: J=K=1, 10 kHz -> 5 kHz', 10e3 / 2 == 5e3 and all(S.jk(1, 1, q) == 1 - q for q in (0, 1)))
check('Floyd Ch.7 7-11: 74121 tW = 10 us, R = 2 kohm -> C = 7143 pF', abs(10e-6 / (0.7 * 2000) * 1e12 - 7142.857) < 0.01)
check('Floyd Ch.7 Example 555: 1,1 x 2,2 kohm x 0,01 uF = 24,2 us', abs(S.t555_mono(2200, 1e-8) * 1e6 - 24.2) < 1e-9)
check('Hinh 555 dao dong (R1 1k, R2 2k, C 0,1 uF): T = 0,35 ms, duty 60 %', abs(S.t555_astable(1e3, 2e3, 1e-7)['T'] - 0.35e-3) < 1e-12 and abs(S.t555_astable(1e3, 2e3, 1e-7)['duty'] - 0.6) < 1e-12)
check('2^15 = 32768 (dong ho)', 2 ** 15 == 32768 and Fr(32768, 2 ** 15) == 1)
# 0111 -> 1000 qua cac ma trung gian trong bo dem gon song: mo phong tung FF, ghi lai moi lan mot bit doi
q = [1, 1, 1, 0]; hist = ['0111']; i = 0                                   # q[i] = Qi, q[3] la MSB
while i < 4:
    q[i] ^= 1; hist.append(''.join(str(b) for b in reversed(q)))
    if q[i] == 1: break
    i += 1
check('bo dem gon song 0111 -> 1000 qua 0110, 0100, 0000', hist == ['0111', '0110', '0100', '0000', '1000'], hist)
check('LUT 4 ngo vao: 16 bit, 65536 ham', 2 ** 4 == 16 and 2 ** 16 == 65536)
check('XOR = hai so hang tich A\'B + AB\'', all((((not a) and b) or (a and (not b))) == (a != b) for a in (0, 1) for b in (0, 1)))
# ---- 3. moi cau sinh tinh lai tu de bai ----
UN = {'': 1, 'k': 1e3, 'M': 1e6, 'm': 1e-3, 'μ': 1e-6, 'n': 1e-9, 'p': 1e-12}
def val(s):
    m = re.match(r'\s*([0-9.]+)\s*([kMmμnp]?)(Hz|s|F)\b', s)
    if not m: raise ValueError(s)
    return float(m.group(1)) * UN[m.group(2)]
def close(a, b, tol=0.006): return abs(a / b - 1) < tol
def ans(it): return it['opts'][it['correct']]['en']
def bn(s): return int(s, 2)
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm11_gen.json'), encoding='utf-8')); fam = {}
def hit(name): fam[name] = fam.get(name, 0) + 1
for it in data:
    q = it['q']['en']; a = ans(it); src = it['src']['en']; m = None
    if m := re.match(r'A ripple counter has (\d+) flip-flops, each with a propagation delay of (\d+) ns', q):
        n, t = int(m[1]), int(m[2]); check('gen ripple delay ' + q[:30], a == f'{n * t} ns', (q, a)); hit('ripple delay')
    elif m := re.match(r'A (\d+)-bit ripple counter uses flip-flops with a (\d+) ns delay', q):
        n, t = int(m[1]), int(m[2]); check('gen fmax ' + q[:30], close(val(a), 1 / (n * t * 1e-9)), (q, a)); hit('fmax')
    elif m := re.match(r'The minimum number of flip-flops for a modulus-(\d+) counter', q):
        check('gen ffs ' + q[:40], a == str((int(m[1]) - 1).bit_length()), (q, a)); hit('ffs for mod')
    elif m := re.match(r'A (\d+)-bit binary up counter is at ([01]+)\. After (\d+) clock pulses', q):
        n, st, k = int(m[1]), bn(m[2]), int(m[3]); check('gen up ' + q[:40], a == format((st + k) % 2 ** n, f'0{n}b'), (q, a)); hit('up count')
    elif m := re.match(r'A 4-bit binary down counter is at ([01]+)\. After (\d+) clock pulses', q):
        st, k = bn(m[1]), int(m[2]); check('gen down ' + q[:40], a == format((st - k) % 16, '04b'), (q, a)); hit('down count')
    elif m := re.match(r'A modulus-(\d+) counter counts up from 0\. After (\d+) clock pulses', q):
        check('gen mod ' + q[:40], a == str(int(m[2]) % int(m[1])), (q, a)); hit('mod count')
    elif m := re.match(r'A (.+) clock drives (.+)\. The final output frequency is', q):
        f0 = val(m[1].replace(' ', '')) if True else 0; txt = m[2]
        ms = [int(x) for x in re.findall(r'\d+', txt.split('moduli')[1])] if 'moduli' in txt else [2] * int(re.match(r'(\d+) cascaded', txt)[1])
        check('gen chain ' + q[:40], close(val(a.replace(' ', '')), f0 / math.prod(ms)), (q, a)); hit('cascade freq')
    elif m := re.match(r'With a (.+) clock, entering (\d+) bits serially', q):
        check('gen serial time ' + q[:40], close(val(a.replace(' ', '')), int(m[2]) / val(m[1].replace(' ', ''))), (q, a)); hit('serial time')
    elif m := re.match(r'A (\d+)-bit serial in/serial out shift register is used as a (.+) delay line', q):
        check('gen delay clock ' + q[:40], close(val(a.replace(' ', '')), int(m[1]) / val(m[2].replace(' ', ''))), (q, a)); hit('delay clock')
    elif m := re.match(r'A (\d+)-bit shift-right register holds ([01]+)\. The bits ([01]+) are entered serially at the left end \(right-most bit first\)', q):
        reg, data_ = m[2], m[3]; r_ = reg
        for b in reversed(data_): r_ = b + r_[:-1]                              # dich phai, bit phai nhat vao truoc
        check('gen shift ' + q[:40], a == r_, (q, a)); hit('shift contents')
    elif m := re.match(r'A (\d+)-flip-flop Johnson counter starts at 0+ .* After (\d+) clock pulses', q):
        n, k = int(m[1]), int(m[2]); r_ = [0] * n
        for _ in range(k): r_ = [1 - r_[-1]] + r_[:-1]
        check('gen johnson ' + q[:40], a == ''.join(map(str, r_)), (q, a)); hit('johnson')
    elif m := re.match(r'How many flip-flops are needed for a ring counter and for a Johnson counter of modulus (\d+)', q):
        N = int(m[1]); check('gen ring/johnson FFs', a == f'ring: {N}, Johnson: {N // 2}', (q, a)); hit('ring-johnson ffs')
    elif m := re.match(r'An edge-triggered J-K flip-flop starts with Q = (\d)\. The \(J, K\) pairs before each clock pulse are (.+)\. The sequence of Q', q):
        qq = int(m[1]); out = []
        for j, k in re.findall(r'\((\d),(\d)\)', m[2]):
            j, k = int(j), int(k); qq = int((j and not qq) or ((not k) and qq)); out.append(qq)       # phuong trinh dac trung (cach khac voi bang)
        check('gen jk ' + q[:50], a == ','.join(map(str, out)), (q, a)); hit('jk sequence')
    elif m := re.match(r'An (active-HIGH|active-LOW) S-R latch \((NOR|NAND) gates\) starts with Q = (\d)\. The inputs \(S, R\) are applied in turn: (.+)\. The final state', q):
        Q = int(m[3]); Qb = 1 - Q
        for s_, r_ in re.findall(r'\((\d),(\d)\)', m[4]):
            s_, r_ = int(s_), int(r_)
            if m[2] == 'NOR': table = {(0, 0): (Q, Qb), (1, 0): (1, 0), (0, 1): (0, 1), (1, 1): (0, 0)}
            else: table = {(1, 1): (Q, Qb), (0, 1): (1, 0), (1, 0): (0, 1), (0, 0): (1, 1)}
            Q, Qb = table[(s_, r_)]
        check('gen latch ' + q[:50], a == f'Q = {Q}, Q̅ = {Qb}', (q, a)); hit('SR latch')
    elif m := re.match(r'(\d+) J-K flip-flops, each with J = K = 1.*The clock is (.+)\. The output frequency', q):
        check('gen divide ' + q[:40], close(val(a.replace(' ', '')), val(m[2].replace(' ', '')) / 2 ** int(m[1])), (q, a)); hit('divide by 2^n')
    elif m := re.match(r'A 74121 one-shot uses its internal 2 kΩ resistor\. For an output pulse (.+) wide', q):
        tw = val(m[1].replace(' ', '')); C = tw / (0.7 * 2000); got = re.match(r'([0-9.]+) (pF|nF)', a); gv = float(got[1]) * (1e-12 if got[2] == 'pF' else 1e-9)
        check('gen 74121 ' + q[:40], close(gv, C), (q, a)); hit('74121')
    elif m := re.match(r'A 555 timer in monostable mode has R = ([0-9.]+) kΩ and C = ([0-9.]+) (μF|nF)\. The output pulse width', q):
        R = float(m[1]) * 1e3; C = float(m[2]) * (1e-6 if m[3] == 'μF' else 1e-9); check('gen 555 mono ' + q[:40], close(val(a.replace(' ', '')), 1.1 * R * C), (q, a)); hit('555 monostable')
    elif m := re.match(r'A 555 astable has R1 = ([0-9.]+) kΩ, R2 = ([0-9.]+) kΩ, C = ([0-9.]+) (μF|nF)\. The output frequency', q):
        R1, R2 = float(m[1]) * 1e3, float(m[2]) * 1e3; C = float(m[3]) * (1e-6 if m[4] == 'μF' else 1e-9); check('gen 555 f ' + q[:40], close(val(a.replace(' ', '')), 1.44 / ((R1 + 2 * R2) * C), 0.012), (q, a)); hit('555 astable f')
    elif m := re.match(r'A 555 astable has R1 = ([0-9.]+) kΩ, R2 = ([0-9.]+) kΩ, C = .*The duty cycle', q):
        R1, R2 = float(m[1]), float(m[2]); check('gen 555 duty ' + q[:40], close(float(a.split()[0]), 100 * (R1 + R2) / (R1 + 2 * R2), 0.006), (q, a)); hit('555 astable duty')
    elif m := re.match(r'A (\d+)-input look-up table', q):
        n = int(m[1]); check('gen LUT ' + q[:30], a == f'{2 ** n} bits; {2 ** (2 ** n)} functions', (q, a)); hit('LUT')
    elif m := re.match(r'A 4-bit ripple counter is truncated to modulus (\d+) with an asynchronous reset', q):
        check('gen truncation ' + q[:40], a == format(int(m[1]), '04b'), (q, a)); hit('truncation')
    else: check('gen: de bai khong nhan dang duoc', False, q)
# ---- 4. khoa in cua Floyd tinh duoc bang chuong trinh ----
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm11.json'), encoding='utf-8'))
def g(ch, n, kind): return next(x for x in goc if x['src']['en'].startswith(f'Floyd Ch.{ch} · {kind} {n} '))
check('Ch.8 ST4 khoa (c)', ans(g(8, 4, 'Self-Test')) == '01111001'); check('Ch.8 ST5 khoa (a) 80 μs', ans(g(8, 5, 'Self-Test')) == '80 μs'); check('Ch.8 ST9 khoa (b) 333 kHz', ans(g(8, 9, 'Self-Test')) == '333 kHz')
check('Ch.9 ST10 khoa (c) 48 ns', ans(g(9, 10, 'Self-Test')) == '48 ns'); check('Ch.9 ST14 khoa (b) 2.5 kHz', ans(g(9, 14, 'Self-Test')) == '2.5 kHz'); check('Ch.9 ST15 khoa (b) 1111', ans(g(9, 15, 'Self-Test')) == '1111')
check('Ch.9 ST13 khoa (c) 1000', ans(g(9, 13, 'Self-Test')) == '1000'); check('Ch.9 ST8 khoa (c) 4 FF', 'four' in ans(g(9, 8, 'Self-Test')) or '4' in ans(g(9, 8, 'Self-Test')))
check('Ch.9 Dung/Sai 6, 8, 10 la Sai', all(g(9, n, 'True/False')['correct'] == 1 for n in (6, 8, 10))); check('Ch.9 Dung/Sai 7 la Dung', g(9, 7, 'True/False')['correct'] == 0)
check('Ch.8 Dung/Sai 8 la Sai (Johnson 8 bit co modulus 16)', g(8, 8, 'True/False')['correct'] == 1 and 2 * 8 == 16)
tfkeys = {7: 'FTFTFTTFTF', 8: 'TFTFTTTFTF', 9: 'TFTFTFTFTF', 10: 'FTFTTTTTTT'}                        # khoa in; Ch.10 muc 7 da sua F -> T (xem notes)
for ch, k in tfkeys.items():
    for n, key in enumerate(k, 1): check(f'Dung/Sai Ch.{ch} muc {n}', g(ch, n, 'True/False')['correct'] == (0 if key == 'T' else 1), (ch, n, key))
stkeys = {7: 'a c b d d d a c d d c f', 8: 'd d a c a d b a b', 9: 'c d b c b c d c b c d d c b b a', 10: 'c a d d b b c c a d b a d d c a d c b b d'}   # Ch.9 muc 2 sua a -> d; Ch.10 muc 9 sua b -> a
for ch, k in stkeys.items():
    for n, key in enumerate(k.split(), 1): check(f'Self-Test Ch.{ch} muc {n}', g(ch, n, 'Self-Test')['correct'] == 'abcdef'.index(key), (ch, n, key))
print('Ho cau sinh da tinh lai:', fam, '| tong', sum(fam.values()), '/', len(data))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
