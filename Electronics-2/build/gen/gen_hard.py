"""Hard (level 3) multi-step questions.  The bank had only 82 level-3 questions (module 01: one), so the Final exam could not hold 25 % hard questions.
Every question is computed by code AND its result is re-derived by a second route (an assert in the question itself: nodal solve, time stepping, exhaustive search, ...).
Wrong options are computed common mistakes.  Output: data/qsrc/mNN_zhard.json.   Run: python3 -I build/gen/gen_hard.py && python3 build/assemble.py"""
import os, sys, json, math, re, cmath, itertools, collections
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOP = {}
for i in range(1, 11):
    p = os.path.join(ROOT, 'data', 'qbank', f'm{i:02d}.json')
    if os.path.exists(p):
        for it in json.load(open(p, encoding='utf-8'))['items']: TOP[it['topic']['en']] = it['topic']
OUT = collections.defaultdict(list); KEY = {}
def vn(s): return re.sub(r'(?<=\d)\.(?=\d)', ',', s)
def bi(x): return x if isinstance(x, tuple) else (x, x)
def g(x, n=4):
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e7 or a < 1e-3: return f'{x:.{n-1}e}'.replace('e-0', 'e-').replace('e+0', 'e+')
    v = float(f'{x:.{n}g}')
    return str(int(v)) if v == int(v) else str(v)
def close(a, b, rel=1e-3, ab=1e-12): assert abs(a - b) <= rel * max(abs(a), abs(b)) + ab, (a, b)
def H(mod, topic, q, correct, wrongs, expl, src, tag):
    """q, expl: (vi, en); correct / wrongs: str or (vi, en); src: (vi, en)."""
    opts = [bi(correct)] + [bi(w) for w in wrongs]
    assert len({o[1] for o in opts}) == len(opts) >= 4, (q[1], [o[1] for o in opts])
    OUT[mod].append(dict(kind='mcq', q=dict(vi=vn(q[0]), en=q[1]), opts=[dict(vi=vn(o[0]), en=o[1]) for o in opts[:4]], correct=0, explain=dict(vi=vn(expl[0]), en=expl[1]), level=3,
                         topic=TOP[topic], src=dict(vi='Bổ sung (câu khó nhiều bước) – ' + src[0], en='Generated hard multi-step question – ' + src[1]), origin='bo_sung', fixed_order=False, check='script', tags=['hard'], concept=tag))
def S(vi, en=None): return (vi, en or vi)
# ============================================================================================ module 01
M = 'm01'; B1, G1, A1, F1, T1 = 'Binary numbers and conversion', 'Logic gates', 'Adders and combinational circuits', 'Flip-flops and sequential logic', 'ICs, TTL and CMOS'
SRC1 = S('EASA M04 SM01; Jaeger 5e Ch.7', 'EASA M04 SM01; Jaeger 5e Ch.7')
a, b = 0b101101, 0b11011; s = a + b; assert s == 72 and format(s, 'b') == '1001000'
H(M, B1, S('Giá trị thập phân của 101101₂ + 11011₂ là bao nhiêu (cộng nhị phân rồi đổi)?', 'What is the decimal value of 101101₂ + 11011₂ (add in binary, then convert)?'),
  '72', [str(a | b), str(a - b), str(int(format(a, 'b') + format(b, 'b'), 2) % 1000)],
  S('101101₂ = 45 và 11011₂ = 27; 45 + 27 = 72 = 1001000₂. (OR bit-wise cho 63; trừ cho 18.)', '101101₂ = 45 and 11011₂ = 27; 45 + 27 = 72 = 1001000₂. (A bitwise OR gives 63; subtracting gives 18.)'), SRC1, 'm01-binary')
def bcd(n): return ' '.join(format(int(d), '04b') for d in str(n))
assert bcd(59) == '0101 1001'
H(M, B1, S('Số thập phân 59 viết ở dạng BCD là', 'The decimal number 59 written in BCD is'),
  '0101 1001', [format(59, 'b'), '1001 0101', '0101 1010'],
  S('BCD mã hoá từng chữ số: 5 = 0101, 9 = 1001. Nhị phân thuần của 59 là 111011; 1010 không phải mã BCD hợp lệ.', 'BCD codes each digit: 5 = 0101, 9 = 1001. Plain binary 59 is 111011; 1010 is not a valid BCD code.'), SRC1, 'm01-binary')
def add4(x, y):
    c = 0; out = []
    for i in range(4):
        p, q = (x >> i) & 1, (y >> i) & 1; ssum = p ^ q ^ c; c = (p & q) | (c & (p ^ q)); out.append(ssum)
    return out[::-1], c
bits, cy = add4(0b1011, 0b0110); assert bits == [0, 0, 0, 1] and cy == 1 and 11 + 6 == 17
H(M, A1, S('Bộ cộng 4 bit nối chuỗi (ripple) cộng 1011₂ và 0110₂. Các bit tổng S3S2S1S0 và số nhớ ra cuối cùng là', 'A 4-bit ripple-carry adder adds 1011₂ and 0110₂. The sum bits S3S2S1S0 and the final carry out are'),
  S('S = 0001, nhớ ra = 1', 'S = 0001, carry out = 1'), [S('S = 0001, nhớ ra = 0', 'S = 0001, carry out = 0'), S('S = 1111, nhớ ra = 0', 'S = 1111, carry out = 0'), S('S = 1001, nhớ ra = 1', 'S = 1001, carry out = 1')],
  S('11 + 6 = 17 = 1 0001₂: bốn bit thấp 0001 và nhớ ra 1 (bit thứ 5).', '11 + 6 = 17 = 1 0001₂: low four bits 0001 and a carry out of 1 (the fifth bit).'), SRC1, 'm01-adders')
def jk(q, j, k): return {(0, 0): q, (0, 1): 0, (1, 0): 1, (1, 1): 1 - q}[(j, k)]
q = 0; seq = []
for j, k in ((1, 0), (1, 1), (0, 0), (1, 1)): q = jk(q, j, k); seq.append(q)
assert seq == [1, 0, 0, 1]
H(M, F1, S('JK flip-flop bắt đầu với Q = 0. Qua bốn xung nhịp liên tiếp với (J, K) = (1,0), (1,1), (0,0), (1,1), dãy Q sau mỗi xung là', 'A JK flip-flop starts with Q = 0. Over four successive clock pulses with (J, K) = (1,0), (1,1), (0,0), (1,1), the sequence of Q after each pulse is'),
  '1, 0, 0, 1', ['1, 1, 1, 0', '1, 0, 1, 0', '0, 1, 1, 0'],
  S('(1,0) đặt Q = 1; (1,1) đảo → 0; (0,0) giữ → 0; (1,1) đảo → 1.', '(1,0) sets Q = 1; (1,1) toggles → 0; (0,0) holds → 0; (1,1) toggles → 1.'), SRC1, 'm01-flipflops')
cnt = 13 % 8; assert format(cnt, '03b') == '101'
H(M, F1, S('Bộ đếm nhị phân 3 bit (các flip-flop đảo nối tầng) bắt đầu ở 000. Sau 13 xung nhịp nó ở trạng thái', 'A 3-bit binary counter (cascaded toggle flip-flops) starts at 000. After 13 clock pulses its state is'),
  '101', ['110', '111', '100'],
  S('Bộ đếm lặp lại sau 2³ = 8 xung: 13 mod 8 = 5 = 101₂ (13 = 1101₂ thì giữ ba bit thấp).', 'The counter repeats every 2³ = 8 pulses: 13 mod 8 = 5 = 101₂ (13 = 1101₂, keep the three low bits).'), SRC1, 'm01-flipflops')
fx = [1 - ((a_ & (1 - b_)) | ((1 - a_) & b_)) for a_, b_ in itertools.product((0, 1), repeat=2)]; xnor = [int(a_ == b_) for a_, b_ in itertools.product((0, 1), repeat=2)]; assert fx == xnor
H(M, G1, S('Biểu thức NOT(A·B̄ + Ā·B) tương đương với cổng nào?', 'The expression NOT(A·B̄ + Ā·B) is equivalent to which gate?'),
  'XNOR', ['XOR', 'NAND', 'NOR'],
  S('A·B̄ + Ā·B là XOR; đảo của XOR là XNOR (ngõ ra 1 khi hai ngõ vào bằng nhau). Bảng chân lý: 1, 0, 0, 1.', 'A·B̄ + Ā·B is XOR; the inverse of XOR is XNOR (output 1 when the inputs are equal). Truth table: 1, 0, 0, 1.'), SRC1, 'm01-gates')
def vsp(VDD, VTN, VTP, KR): return (VDD + VTP + VTN * math.sqrt(KR)) / (1 + math.sqrt(KR))
from scipy.optimize import brentq
VDD, VTN, VTP, Kn, Kp = 3.3, 0.6, -0.8, 225e-6, 100e-6
root = brentq(lambda v: 0.5 * Kn * (v - VTN) ** 2 - 0.5 * Kp * (VDD - v + VTP) ** 2, VTN + 1e-6, VDD + VTP - 1e-6); close(root, vsp(VDD, VTN, VTP, 2.25), 1e-6)
H(M, T1, S('Bộ đảo CMOS có VDD = 3,3 V, VTN = 0,6 V, VTP = −0,8 V, Kn = 225 μA/V², Kp = 100 μA/V². Ngưỡng chuyển mạch VSP là bao nhiêu?', 'A CMOS inverter has VDD = 3.3 V, VTN = 0.6 V, VTP = −0.8 V, Kn = 225 μA/V², Kp = 100 μA/V². What is the switching threshold VSP?'),
  f'{g(root, 3)} V', [f'{g(VDD / 2, 3)} V', f'{g((VDD + VTP + VTN * 2.25) / (1 + 2.25), 3)} V', f'{g((VDD + VTP + VTN) / 2, 3)} V'],
  S(f'KR = Kn/Kp = 2,25 nên √KR = 1,5: VSP = (3,3 − 0,8 + 0,6·1,5)/(1 + 1,5) = {g(root, 3)} V (không phải VDD/2).', f'KR = Kn/Kp = 2.25 so √KR = 1.5: VSP = (3.3 − 0.8 + 0.6·1.5)/(1 + 1.5) = {g(root, 3)} V (not VDD/2).'), S('Jaeger 5e §7.2', 'Jaeger 5e §7.2'), 'm01-cmos')
P = 0.1 * 1e4 * 2e-12 * 1.8 ** 2 * 200e6; close(P, 1.296, 1e-9)
H(M, T1, S('Một vi mạch CMOS có 10 000 cổng, mỗi cổng tải C = 2 pF, VDD = 1,8 V, xung nhịp 200 MHz, hệ số hoạt động (tỉ lệ cổng chuyển trạng thái) 10 %. Công suất động P = α·N·C·V²·f là bao nhiêu?', 'A CMOS chip has 10,000 gates, each loaded with C = 2 pF, VDD = 1.8 V, a 200 MHz clock and an activity factor (fraction of gates switching) of 10 %. What is the dynamic power P = α·N·C·V²·f?'),
  f'{g(P, 4)} W', [f'{g(P * 10, 4)} W', f'{g(P / 1.8 * 1, 4)} W', f'{g(P / 1e4 * 1e3, 3)} mW'],
  S('P = 0,1 × 10⁴ × 2·10⁻¹² × 1,8² × 2·10⁸ = 1,296 W. Bỏ hệ số hoạt động cho 12,96 W; quên bình phương V cho 0,72 W; chỉ tính một cổng cho 0,13 mW.', 'P = 0.1 × 10⁴ × 2·10⁻¹² × 1.8² × 2·10⁸ = 1.296 W. Ignoring the activity factor gives 12.96 W; forgetting to square V gives 0.72 W; counting a single gate gives 0.13 mW.'), S('Jaeger 5e §7.3', 'Jaeger 5e §7.3'), 'm01-cmos')
VOH, VOL, VIH, VIL = 4.8, 0.2, 3.2, 1.4; NMH, NML = VOH - VIH, VIL - VOL; close(NMH, 1.6); close(NML, 1.2)
H(M, T1, S('Cổng A (VOH = 4,8 V, VOL = 0,2 V) điều khiển cổng B (VIH = 3,2 V, VIL = 1,4 V). Nhiễu lớn nhất chịu được trên đường đang ở mức THẤP và ở mức CAO lần lượt là', 'Gate A (VOH = 4.8 V, VOL = 0.2 V) drives gate B (VIH = 3.2 V, VIL = 1.4 V). The largest noise tolerated on a line that is LOW and on one that is HIGH is'),
  S('1,2 V (mức thấp) và 1,6 V (mức cao)', '1.2 V (LOW) and 1.6 V (HIGH)'), [S('1,6 V (mức thấp) và 1,2 V (mức cao)', '1.6 V (LOW) and 1.2 V (HIGH)'), S('0,2 V (mức thấp) và 1,4 V (mức cao)', '0.2 V (LOW) and 1.4 V (HIGH)'), S('2,8 V (mức thấp) và 3,4 V (mức cao)', '2.8 V (LOW) and 3.4 V (HIGH)')],
  S('NML = VIL − VOL = 1,4 − 0,2 = 1,2 V; NMH = VOH − VIH = 4,8 − 3,2 = 1,6 V (lấy VO của cổng phát, VI của cổng nhận).', 'NML = VIL − VOL = 1.4 − 0.2 = 1.2 V; NMH = VOH − VIH = 4.8 − 3.2 = 1.6 V (VO of the driving gate, VI of the receiving gate).'), S('Jaeger 5e §6.2', 'Jaeger 5e §6.2'), 'm01-families')
def decode(n_in, enable, code): return [int(enable and i == code) for i in range(2 ** n_in)]
def build16(code):                                   # one 2->4 decoder on the two high bits enables four 2->4 decoders on the low bits
    hi, lo = code >> 2, code & 3; top = decode(2, 1, hi); out = []
    for d in range(4): out += decode(2, top[d], lo)
    return out
assert all(build16(c) == decode(4, 1, c) for c in range(16))
H(M, A1, S('Cần tối thiểu bao nhiêu bộ giải mã 2→4 có chân enable để tạo một bộ giải mã 4→16?', 'What is the minimum number of 2→4 decoders with an enable pin needed to build a 4→16 decoder?'),
  '5', ['4', '2', '8'],
  S('Một bộ giải mã (2 bit cao) bật một trong bốn bộ giải mã còn lại (2 bit thấp): 1 + 4 = 5 bộ, cho 4 × 4 = 16 ngõ ra.', 'One decoder (the two high bits) enables one of four more decoders (the two low bits): 1 + 4 = 5, giving 4 × 4 = 16 outputs.'), SRC1, 'm01-combinational')
# ============================================================================================ module 02
M = 'm02'; FB2, FR2, OF2, CM2, IM2, BA2 = 'Negative feedback and gain', 'Frequency response and bandwidth', 'Offset, bias and slew rate', 'Input modes and CMRR', 'Impedances and compensation', 'Op-amp basics'
SRC2 = S('Floyd 9e Ch.12; Jaeger 5e Ch.10–11', 'Floyd 9e Ch.12; Jaeger 5e Ch.10–11')
A_, B_ = 2e4, 1 / 50; acl = A_ / (1 + A_ * B_); err = (acl - 50) / 50 * 100; M2 = np.array([[1.0, A_ * B_], [0, 1.0]]); close(acl, 20000 / 401, 1e-12)
H(M, FB2, S('Mạch không đảo thiết kế độ lợi 50 (B = 1/50) dùng op-amp có Aol = 2·10⁴. Độ lợi vòng kín thực và sai số độ lợi là', 'A noninverting amplifier designed for a gain of 50 (B = 1/50) uses an op-amp with Aol = 2·10⁴. The actual closed-loop gain and the gain error are'),
  f'{g(acl, 4)}; {g(err, 3)} %', [f'50; 0 %', f'{g(50 * (1 + 1 / 400), 4)}; +0.25 %', f'{g(acl / 2, 4)}; {g(-50, 3)} %'],
  S(f'Acl = Aol/(1 + B·Aol) = 20 000/(1 + 400) = {g(acl, 4)}; sai số = (49,88 − 50)/50 = −0,25 % (vòng kín hầu như không phụ thuộc Aol).', f'Acl = Aol/(1 + B·Aol) = 20,000/(1 + 400) = {g(acl, 4)}; error = (49.88 − 50)/50 = −0.25 % (the closed loop is almost independent of Aol).'), SRC2, 'm02-feedback-gain')
Ri, Rf, A = 10e3, 100e3, 5e3; Mx = np.array([[1 / Ri + 1 / Rf, -1 / Rf], [A, 1.0]]); v1, vo = np.linalg.solve(Mx, [1 / Ri, 0.0]); formula = -(Rf / Ri) / (1 + (1 + Rf / Ri) / A); close(vo, formula, 1e-9)
H(M, FB2, S('Mạch đảo có Ri = 10 kΩ, Rf = 100 kΩ dùng op-amp có Aol = 5000. Độ lợi vòng kín chính xác là', 'An inverting amplifier with Ri = 10 kΩ and Rf = 100 kΩ uses an op-amp with Aol = 5000. The exact closed-loop gain is'),
  g(vo, 4), [g(-Rf / Ri, 4), g(-(Rf / Ri) * (1 - 11 / 5000 * 2), 4), g(-(Rf / Ri) / (1 + 10 / 5000), 4)],
  S(f'Acl = −(Rf/Ri)/(1 + (1 + Rf/Ri)/Aol) = −10/(1 + 11/5000) = {g(vo, 4)} (nhiễu độ lợi là 1 + Rf/Ri = 11, không phải 10).', f'Acl = −(Rf/Ri)/(1 + (1 + Rf/Ri)/Aol) = −10/(1 + 11/5000) = {g(vo, 4)} (the noise gain is 1 + Rf/Ri = 11, not 10).'), SRC2, 'm02-inverting')
fT, SR, Acl, Vin = 2e6, 0.8e6, 20, 0.2; Vp = Acl * Vin; f_bw = fT / Acl; f_sr = SR / (2 * math.pi * Vp); fmax = min(f_bw, f_sr)
t = np.linspace(0, 1 / f_sr, 200001); slope = np.max(np.abs(np.gradient(Vp * np.sin(2 * math.pi * f_sr * t), t))); close(slope, SR, 1e-4)
H(M, OF2, S('Op-amp có fT = 2 MHz và slew rate 0,8 V/μs làm mạch không đảo độ lợi 20, tín hiệu vào hình sin biên độ 0,2 V. Tần số cao nhất không méo là', 'An op-amp with fT = 2 MHz and a slew rate of 0.8 V/μs is used as a noninverting amplifier of gain 20 with a 0.2 V peak sine input. The highest undistorted frequency is'),
  f'{g(fmax / 1e3, 3)} kHz', [f'{g(f_bw / 1e3, 3)} kHz', f'{g(SR / (2 * math.pi * Vin) / 1e3, 3)} kHz', f'{g(fT / 1e3, 3)} kHz'],
  S(f'Băng thông: fT/Acl = 100 kHz. Slew rate: Vp = 20 × 0,2 = 4 V nên f ≤ SR/(2π·Vp) = {g(f_sr / 1e3, 3)} kHz. Giới hạn nhỏ hơn quyết định: {g(fmax / 1e3, 3)} kHz.', f'Bandwidth: fT/Acl = 100 kHz. Slew rate: Vp = 20 × 0.2 = 4 V so f ≤ SR/(2π·Vp) = {g(f_sr / 1e3, 3)} kHz. The smaller limit decides: {g(fmax / 1e3, 3)} kHz.'), SRC2, 'm02-slew-rate')
Ri, Rf, VOS, IB = 1e3, 100e3, 2e-3, 80e-9; e_vos = VOS * (1 + Rf / Ri); e_ib = IB * Rf; tot = e_vos + e_ib; close(tot, 0.210, 1e-9)
H(M, OF2, S('Mạch đảo Ri = 1 kΩ, Rf = 100 kΩ, không có điện trở bù, op-amp có VOS = 2 mV và dòng phân cực 80 nA mỗi ngõ. Sai số một chiều ở ngõ ra, trường hợp xấu nhất (cùng dấu), xấp xỉ', 'An inverting amplifier with Ri = 1 kΩ and Rf = 100 kΩ, no compensating resistor, uses an op-amp with VOS = 2 mV and 80 nA bias current at each input. The worst-case (same sign) dc output error is about'),
  f'{g(tot * 1e3, 3)} mV', [f'{g(e_vos * 1e3, 3)} mV', f'{g(e_ib * 1e3, 3)} mV', f'{g(VOS * 1e3, 3)} mV'],
  S('VOS bị khuếch đại với độ lợi nhiễu 1 + Rf/Ri = 101: 202 mV; dòng phân cực chảy qua Rf: 80 nA × 100 kΩ = 8 mV. Tổng 210 mV.', 'VOS is amplified by the noise gain 1 + Rf/Ri = 101: 202 mV; the bias current flows through Rf: 80 nA × 100 kΩ = 8 mV. Total 210 mV.'), SRC2, 'm02-bias-offset')
Acl_d, cmrr_db, vd, vc = 100, 90, 2e-3, 1.5; Acm = Acl_d / 10 ** (cmrr_db / 20); vout = Acl_d * vd + Acm * vc; close(vout, 0.2047, 1e-3)
H(M, CM2, S('Mạch khuếch đại vi sai có độ lợi vi sai 100 và CMRR 90 dB. Ngõ vào có thành phần vi sai 2 mV và chung 1,5 V. Điện áp ra xấp xỉ', 'A differential amplifier has a differential gain of 100 and a CMRR of 90 dB. The input has a 2 mV differential and a 1.5 V common-mode component. The output is about'),
  f'{g(vout * 1e3, 4)} mV', [f'{g(Acl_d * vd * 1e3, 4)} mV', f'{g(Acl_d * (vd + vc) * 1e3, 5)} mV', f'{g((Acl_d * vd + Acl_d * vc / 90) * 1e3, 4)} mV'],
  S('CMRR 90 dB = 31 623 nên Acm = 100/31 623 = 3,16·10⁻³; Vout = 100 × 2 mV + 3,16·10⁻³ × 1,5 V = 200 + 4,74 = 204,7 mV.', 'CMRR of 90 dB = 31,623 so Acm = 100/31,623 = 3.16·10⁻³; Vout = 100 × 2 mV + 3.16·10⁻³ × 1.5 V = 200 + 4.74 = 204.7 mV.'), SRC2, 'm02-modes-cmrr')
A, Zin, Zout, Ri, Rf = 1.2e5, 2e6, 75.0, 1e3, 49e3; B = Ri / (Ri + Rf); k = 1 + A * B
V = 1.0; Iin = (V - B * (A * V / (1 + A * B))) / Zin; close(V / Iin, k * Zin, 1e-9); zout = Zout / k
H(M, IM2, S('Mạch không đảo có Ri = 1 kΩ, Rf = 49 kΩ, op-amp Aol = 120 000, Zin = 2 MΩ, Zout = 75 Ω. Trở kháng ra của mạch có hồi tiếp là', 'A noninverting amplifier has Ri = 1 kΩ and Rf = 49 kΩ with an op-amp of Aol = 120,000, Zin = 2 MΩ, Zout = 75 Ω. The output impedance with feedback is'),
  f'{g(zout * 1e3, 3)} mΩ', [f'{g(Zout / (1 + A) * 1e3, 3)} mΩ', f'{g(Zout * k, 3)} Ω', f'{g(Zout / B / 1e3, 3)} Ω'],
  S(f'B = 1/50 = 0,02; 1 + B·Aol = 2401; Zout(NI) = 75/2401 = {g(zout * 1e3, 3)} mΩ (và Zin(NI) = 2401 × 2 MΩ = {g(k * Zin / 1e9, 3)} GΩ).', f'B = 1/50 = 0.02; 1 + B·Aol = 2401; Zout(NI) = 75/2401 = {g(zout * 1e3, 3)} mΩ (and Zin(NI) = 2401 × 2 MΩ = {g(k * Zin / 1e9, 3)} GΩ).'), SRC2, 'm02-impedances')
bw1 = 1e6 / 20; both = bw1 * math.sqrt(math.sqrt(2) - 1); f = np.linspace(1e3, 200e3, 400000); hh = np.abs(1 / (1 + 1j * f / bw1)) ** 2; f3 = f[np.argmin(np.abs(hh - 1 / math.sqrt(2)))]; close(f3, both, 2e-3)
H(M, FR2, S('Hai tầng giống hệt nhau, mỗi tầng dùng op-amp fT = 1 MHz với độ lợi 20, mắc nối tiếp. Băng thông −3 dB của cả hai tầng xấp xỉ', 'Two identical stages, each an op-amp with fT = 1 MHz at a gain of 20, are cascaded. The −3 dB bandwidth of the pair is about'),
  f'{g(both / 1e3, 3)} kHz', [f'{g(bw1 / 1e3, 3)} kHz', f'{g(bw1 / 2 / 1e3, 3)} kHz', f'{g(bw1 * 2 / 1e3, 3)} kHz'],
  S(f'Mỗi tầng: BW = fT/Acl = 50 kHz (một cực). Hai cực giống nhau nối tiếp: BW = 50 kHz × √(√2 − 1) = {g(both / 1e3, 3)} kHz.', f'Each stage: BW = fT/Acl = 50 kHz (one pole). Two identical poles in cascade: BW = 50 kHz × √(√2 − 1) = {g(both / 1e3, 3)} kHz.'), SRC2, 'm02-frequency')
A0, fc0, Acl3, f = 2e5, 10.0, 40, 100e3; fTx = A0 * fc0; bwcl = fTx / Acl3; mag = Acl3 / math.sqrt(1 + (f / bwcl) ** 2); dbv = 20 * math.log10(mag)
close(abs(Acl3 / (1 + 1j * f / bwcl)), mag, 1e-9)
H(M, FR2, S('Op-amp có Aol(mid) = 200 000 và fc(ol) = 10 Hz làm mạch có độ lợi vòng kín 40 (một cực). Độ lợi tại 100 kHz là', 'An op-amp with Aol(mid) = 200,000 and fc(ol) = 10 Hz is used with a closed-loop gain of 40 (single pole). The gain at 100 kHz is'),
  f'{g(dbv, 3)} dB', [f'{g(20 * math.log10(Acl3), 3)} dB', f'{g(20 * math.log10(Acl3) - 3, 3)} dB', f'{g(20 * math.log10(Acl3 * bwcl / f), 3)} dB'],
  S(f'fT = 200 000 × 10 = 2 MHz; BWcl = 2 MHz/40 = 50 kHz. Tại 100 kHz: 40/√(1 + 2²) = {g(mag, 4)} = {g(dbv, 3)} dB (đã vượt quá băng thông).', f'fT = 200,000 × 10 = 2 MHz; BWcl = 2 MHz/40 = 50 kHz. At 100 kHz: 40/√(1 + 2²) = {g(mag, 4)} = {g(dbv, 3)} dB (already beyond the bandwidth).'), SRC2, 'm02-frequency')
Ri, Rf, IB, IOS = 10e3, 220e3, 100e-9, 10e-9; Rc = Ri * Rf / (Ri + Rf); e_c = IOS * Rf; e_n = IB * Rf
H(M, IM2, S('Mạch đảo Ri = 10 kΩ, Rf = 220 kΩ, dòng phân cực 100 nA và dòng offset 10 nA. Với điện trở bù đúng giá trị ở ngõ không đảo, sai số ngõ ra do dòng vào xấp xỉ', 'An inverting amplifier with Ri = 10 kΩ and Rf = 220 kΩ has a bias current of 100 nA and an offset current of 10 nA. With the correct compensating resistor at the noninverting input, the output error from the input currents is about'),
  f'{g(e_c * 1e3, 3)} mV', [f'{g(e_n * 1e3, 3)} mV', f'{g(IB * Rc * 1e3, 3)} mV', '0 mV'],
  S(f'Rc = Ri‖Rf = {g(Rc / 1e3, 4)} kΩ; sai số còn lại = IOS·Rf = 10 nA × 220 kΩ = 2,2 mV (không bù: IB·Rf = 22 mV).', f'Rc = Ri‖Rf = {g(Rc / 1e3, 4)} kΩ; the remaining error = IOS·Rf = 10 nA × 220 kΩ = 2.2 mV (uncompensated: IB·Rf = 22 mV).'), SRC2, 'm02-bias-offset')
fc = [1e3, 20e3, 100e3]; ph = -sum(math.degrees(math.atan(20e3 / x)) for x in fc)
H(M, FR2, S('Một op-amp có ba tầng với tần số tới hạn 1 kHz, 20 kHz và 100 kHz. Độ trễ pha tổng tại f = 20 kHz xấp xỉ', 'An op-amp has three stages with critical frequencies of 1 kHz, 20 kHz and 100 kHz. The total phase lag at f = 20 kHz is about'),
  f'{g(ph, 4)}°', [f'{g(-45, 3)}°', f'{g(-90 * 3 / 2, 3)}°', f'{g(ph + 90, 3)}°'],
  S(f'θ = −tan⁻¹(20/1) − tan⁻¹(20/20) − tan⁻¹(20/100) = −87,1° − 45° − 11,3° = {g(ph, 4)}°.', f'θ = −tan⁻¹(20/1) − tan⁻¹(20/20) − tan⁻¹(20/100) = −87.1° − 45° − 11.3° = {g(ph, 4)}°.'), SRC2, 'm02-frequency')
# ============================================================================================ module 03
M = 'm03'; CH3, SU3, IN3, DI3 = 'Comparators and hysteresis', 'Summing, averaging, scaling amplifiers', 'Integrator', 'Differentiator'
SRC3 = S('Floyd 9e Ch.13', 'Floyd 9e Ch.13')
R1, R2, Vz = 33e3, 6.8e3, 5.1; Vm = Vz + 0.7; utp = R2 / (R1 + R2) * Vm; hys = 2 * utp
H(M, CH3, S('Mạch so sánh có hysteresis, ngõ ra bị giới hạn bởi hai zener 5,1 V ngược chiều (sụt thuận 0,7 V), R1 = 33 kΩ nối từ ngõ ra về ngõ vào không đảo và R2 = 6,8 kΩ nối từ ngõ vào không đảo xuống đất (Floyd Hình 13–7). Điện áp ngưỡng trên VUTP và độ rộng vòng trễ VHYS là', 'A comparator with hysteresis has its output bounded by two back-to-back 5.1 V zeners (0.7 V forward drop), R1 = 33 kΩ from the output to the noninverting input and R2 = 6.8 kΩ from the noninverting input to ground (Floyd Fig. 13–7). The upper trigger point VUTP and the hysteresis width VHYS are'),
  f'{g(utp, 3)} V; {g(hys, 3)} V', [f'{g(R2 / (R1 + R2) * 12, 3)} V; {g(2 * R2 / (R1 + R2) * 12, 3)} V', f'{g(R1 / (R1 + R2) * Vm, 3)} V; {g(2 * R1 / (R1 + R2) * Vm, 3)} V', f'{g(R2 / (R1 + R2) * Vz, 3)} V; {g(2 * R2 / (R1 + R2) * Vz, 3)} V'],
  S(f'Biên độ ngõ ra = ±(5,1 + 0,7) = ±5,8 V; B = 6,8/(33 + 6,8) = 0,171; VUTP = 0,171 × 5,8 = {g(utp, 3)} V; VHYS = 2·VUTP = {g(hys, 3)} V.', f'Output swing = ±(5.1 + 0.7) = ±5.8 V; B = 6.8/(33 + 6.8) = 0.171; VUTP = 0.171 × 5.8 = {g(utp, 3)} V; VHYS = 2·VUTP = {g(hys, 3)} V.'), SRC3, 'm03-hysteresis')
Vin, R, C, f = 2.0, 10e3, 47e-9, 500.0; T = 1 / f; slope = Vin / (R * C); half = slope * T / 2
dt = T / 4000; vc = 0.0; ys = []
for k in range(4000 * 3):
    tt = k * dt; v = Vin if (tt % T) < T / 2 else -Vin; vc += v / (R * C) * dt; ys.append(-vc)
pp = (max(ys[4000:]) - min(ys[4000:])); close(pp, half, 2e-2)
H(M, IN3, S('Sóng vuông ±2 V, 500 Hz, chu kỳ làm việc 50 % đặt vào mạch tích phân R = 10 kΩ, C = 47 nF. Biên độ đỉnh–đỉnh của sóng tam giác ở ngõ ra xấp xỉ', 'A ±2 V, 500 Hz square wave with a 50 % duty cycle drives an integrator with R = 10 kΩ and C = 47 nF. The peak-to-peak amplitude of the triangular output is about'),
  f'{g(half, 3)} V', [f'{g(2 * half, 3)} V', f'{g(half / 2, 3)} V', f'{g(Vin * R * C / (T / 2), 3)} V'],
  S(f'Độ dốc = Vin/(R·C) = 2/(10 kΩ × 47 nF) = {g(slope, 4)} V/s; nửa chu kỳ 1 ms nên ΔV = {g(half, 3)} V (đi xuống rồi lên: đỉnh–đỉnh bằng đúng ΔV này).', f'Slope = Vin/(R·C) = 2/(10 kΩ × 47 nF) = {g(slope, 4)} V/s; a half period of 1 ms gives ΔV = {g(half, 3)} V (down then up: the peak-to-peak equals this ΔV).'), SRC3, 'm03-integrator')
Vc, R, C = 1.5, 100e3, 0.1e-6; tsat = 11 * R * C / Vc; ts = 0.0; dt = 1e-5; vc = 0.0
while vc < 11 - 1e-12: vc += Vc / (R * C) * dt; ts += dt
close(ts, tsat, 2e-3)
H(M, IN3, S('Mạch tích phân R = 100 kΩ, C = 0,1 μF, op-amp bão hoà ở ±11 V, nhận bước +1,5 V không đổi. Sau bao lâu ngõ ra chạm mức bão hoà −11 V (từ 0 V)?', 'An integrator with R = 100 kΩ and C = 0.1 μF, op-amp saturating at ±11 V, receives a constant +1.5 V step. How long until the output reaches −11 V (from 0 V)?'),
  f'{g(tsat * 1e3, 3)} ms', [f'{g(11 / Vc * 1e3, 3)} ms', f'{g(Vc * R * C / 11 * 1e3, 3)} ms', f'{g(2 * tsat * 1e3, 3)} ms'],
  S(f'RC = 10 ms; độ dốc = 1,5/10 ms = 150 V/s; t = 11 V/150 V/s = {g(tsat * 1e3, 3)} ms.', f'RC = 10 ms; slope = 1.5/10 ms = 150 V/s; t = 11 V/150 V/s = {g(tsat * 1e3, 3)} ms.'), SRC3, 'm03-integrator')
Rf, C, f, pk = 10e3, 10e-9, 1e3, 1.0; slope = 2 * pk / (1 / f / 2); vo = Rf * C * slope
t = np.linspace(0, 2e-3, 400001); tri = pk * 2 / math.pi * np.arcsin(np.sin(2 * math.pi * f * t)); d = Rf * C * np.gradient(tri, t); close(np.max(np.abs(d[1000:-1000])), vo, 5e-3)
H(M, DI3, S('Sóng tam giác ±1 V, 1 kHz đặt vào mạch vi phân Rf = 10 kΩ, C = 10 nF. Biên độ đỉnh của sóng vuông ngõ ra là', 'A ±1 V, 1 kHz triangular wave drives a differentiator with Rf = 10 kΩ and C = 10 nF. The peak amplitude of the square-wave output is'),
  f'{g(vo, 3)} V', [f'{g(vo * 2, 3)} V', f'{g(vo / 2, 3)} V', f'{g(Rf * C * pk * f, 3)} V'],
  S(f'Độ dốc tam giác = 2 V/0,5 ms = 4000 V/s; |Vout| = Rf·C·độ dốc = 10⁻⁴ s × 4000 V/s = {g(vo, 3)} V (đảo dấu).', f'Triangle slope = 2 V/0.5 ms = 4000 V/s; |Vout| = Rf·C·slope = 10⁻⁴ s × 4000 V/s = {g(vo, 3)} V (inverted).'), SRC3, 'm03-differentiator')
V = [2.0, -1.0, 0.5]; Rk = [10e3, 20e3, 5e3]; Rf = 20e3; vo = -sum(v * Rf / r for v, r in zip(V, Rk)); close(vo, -5.0)
Gs = sum(1 / r for r in Rk); J = sum(v / r for v, r in zip(V, Rk)); Mx = np.array([[Gs + 1 / Rf, -1 / Rf], [1e9, 1.0]]); v2 = np.linalg.solve(Mx, [J, 0.0])[1]; close(v2, vo, 1e-6)
H(M, SU3, S('Mạch cộng đảo Rf = 20 kΩ có ba ngõ vào: +2 V qua 10 kΩ, −1 V qua 20 kΩ, +0,5 V qua 5 kΩ. Điện áp ra là', 'An inverting summer with Rf = 20 kΩ has three inputs: +2 V through 10 kΩ, −1 V through 20 kΩ, +0.5 V through 5 kΩ. The output voltage is'),
  g(vo, 3) + ' V', [g(-(sum(V)), 3) + ' V', g(+5.0, 3) + ' V', g(-(2 * 2 + 1 + 0.5 * 4), 3) + ' V'],
  S('Mỗi ngõ có độ lợi −Rf/Rk: −2, −1, −4. Vout = −(2×2) − (−1)(1) − (0,5×4) → −4 + 1 − 2 = −5 V.', 'Each input has gain −Rf/Rk: −2, −1, −4. Vout = −2·2 + (−1)(−1) + (−4)(0.5) = −4 + 1 − 2 = −5 V.'), SRC3, 'm03-summing')
Rk = [10e3, 20e3, 40e3, 80e3]; Rf = 10e3; code = 0b1011; Vh = 5.0; vo = -sum(Vh * ((code >> (3 - i)) & 1) * Rf / Rk[i] for i in range(4)); close(vo, -6.875)
H(M, SU3, S('DAC 4 bit dùng mạch cộng đảo Rf = 10 kΩ, các điện trở vào 10 kΩ (MSB), 20 kΩ, 40 kΩ, 80 kΩ (LSB), mức logic 1 = 5 V. Với mã 1011 điện áp ra là', 'A 4-bit DAC uses an inverting summer with Rf = 10 kΩ and input resistors 10 kΩ (MSB), 20 kΩ, 40 kΩ, 80 kΩ (LSB), logic 1 = 5 V. For the code 1011 the output is'),
  g(vo, 4) + ' V', [g(-5 * 11 / 16, 4) + ' V', g(-5 * 0b1101 / 8, 4) + ' V', g(5 * 1.375, 4) + ' V'],
  S('Trọng số 1, 0,5, 0,25, 0,125 (= Rf/Rk). Mã 1011: 1 + 0 + 0,25 + 0,125 = 1,375; Vout = −5 × 1,375 = −6,875 V.', 'Weights 1, 0.5, 0.25, 0.125 (= Rf/Rk). Code 1011: 1 + 0 + 0.25 + 0.125 = 1.375; Vout = −5 × 1.375 = −6.875 V.'), SRC3, 'm03-scaling')
V = [1.2, 2.4, 3.6, 4.8]; R = 10e3; Rf = R / 4; vo = -sum(V) / 4; close(vo, -3.0)
H(M, SU3, S('Mạch trung bình bốn ngõ vào dùng Ri = 10 kΩ nhận 1,2 V; 2,4 V; 3,6 V; 4,8 V. Rf phải bằng bao nhiêu và điện áp ra là', 'A four-input averaging amplifier with Ri = 10 kΩ receives 1.2 V, 2.4 V, 3.6 V, 4.8 V. What must Rf be and what is the output?'),
  S('Rf = 2,5 kΩ; Vout = −3,0 V', 'Rf = 2.5 kΩ; Vout = −3.0 V'), [S('Rf = 40 kΩ; Vout = −12 V', 'Rf = 40 kΩ; Vout = −12 V'), S('Rf = 2,5 kΩ; Vout = +3,0 V', 'Rf = 2.5 kΩ; Vout = +3.0 V'), S('Rf = 10 kΩ; Vout = −12 V', 'Rf = 10 kΩ; Vout = −12 V')],
  S('Trung bình cần Rf/Ri = 1/4 → Rf = 2,5 kΩ; tổng = 12 V; Vout = −12/4 = −3,0 V (mạch đảo nên âm).', 'Averaging needs Rf/Ri = 1/4 → Rf = 2.5 kΩ; the sum is 12 V; Vout = −12/4 = −3.0 V (negative: the circuit inverts).'), SRC3, 'm03-averaging')
Rf, Ri, C = 1e6, 10e3, 0.1e-6; fcx = 1 / (2 * math.pi * Rf * C); gdc = Rf / Ri
H(M, IN3, S('Mạch tích phân thực dùng Ri = 10 kΩ, C = 0,1 μF và điện trở Rf = 1 MΩ mắc song song với C. Độ lợi một chiều và tần số dưới đó mạch hoạt động như mạch khuếch đại đảo là', 'A practical integrator uses Ri = 10 kΩ, C = 0.1 μF and a resistor Rf = 1 MΩ in parallel with C. The dc gain and the frequency below which it behaves as an inverting amplifier are'),
  S(f'−100 (40 dB); {g(fcx, 3)} Hz', f'−100 (40 dB); {g(fcx, 3)} Hz'), [S(f'−100 (40 dB); {g(1 / (2 * math.pi * Ri * C), 3)} Hz', f'−100 (40 dB); {g(1 / (2 * math.pi * Ri * C), 3)} Hz'), S(f'−10 (20 dB); {g(fcx, 3)} Hz', f'−10 (20 dB); {g(fcx, 3)} Hz'), S(f'−1000 (60 dB); {g(fcx * 10, 3)} Hz', f'−1000 (60 dB); {g(fcx * 10, 3)} Hz')],
  S(f'Độ lợi một chiều = −Rf/Ri = −100; điểm gãy fc = 1/(2π·Rf·C) = {g(fcx, 3)} Hz; trên tần số này tụ chiếm ưu thế và mạch tích phân.', f'dc gain = −Rf/Ri = −100; the corner fc = 1/(2π·Rf·C) = {g(fcx, 3)} Hz; above it the capacitor dominates and the circuit integrates.'), SRC3, 'm03-integrator')
Rin, C, Rf = 1e3, 10e-9, 10e3; fcd = 1 / (2 * math.pi * Rin * C); gh = Rf / Rin
H(M, DI3, S('Mạch vi phân thực có Rin = 1 kΩ mắc nối tiếp với C = 10 nF, Rf = 10 kΩ. Độ lợi tần số cao tối đa và tần số tới hạn trên của vùng vi phân là', 'A practical differentiator has Rin = 1 kΩ in series with C = 10 nF and Rf = 10 kΩ. The maximum high-frequency gain and the frequency above which it stops differentiating are'),
  S(f'−10 (20 dB); {g(fcd / 1e3, 3)} kHz', f'−10 (20 dB); {g(fcd / 1e3, 3)} kHz'), [S(f'−10 (20 dB); {g(1 / (2 * math.pi * Rf * C) / 1e3, 3)} kHz', f'−10 (20 dB); {g(1 / (2 * math.pi * Rf * C) / 1e3, 3)} kHz'), S(f'−1 (0 dB); {g(fcd / 1e3, 3)} kHz', f'−1 (0 dB); {g(fcd / 1e3, 3)} kHz'), S(f'−100 (40 dB); {g(fcd / 10e3, 3)} kHz', f'−100 (40 dB); {g(fcd / 10e3, 3)} kHz')],
  S(f'Trên fc = 1/(2π·Rin·C) = {g(fcd / 1e3, 3)} kHz tụ gần như ngắn mạch, độ lợi bị giới hạn bởi Rf/Rin = 10 (nhiễu cao tần không còn tăng).', f'Above fc = 1/(2π·Rin·C) = {g(fcd / 1e3, 3)} kHz the capacitor is nearly a short and the gain is limited to Rf/Rin = 10 (high-frequency noise is no longer amplified).'), SRC3, 'm03-differentiator')
# ============================================================================================ module 04
M = 'm04'; CA4, PP4, CO4, CL4, PN4, OS4 = 'Cascade amplifiers and gain', 'Push-pull amplifiers', 'Coupling methods', 'Amplifier classes', 'Positive and negative feedback', 'Oscillation basics'
SRC4 = S('Floyd 9e §6–6, §7–2, §7–3; EASA M04 SM01', 'Floyd 9e §6–6, §7–2, §7–3; EASA M04 SM01')
A1, Ro1, Rin2, A2 = 30.0, 2e3, 6e3, 20.0; ld = A1 * Rin2 / (Ro1 + Rin2); tot = ld * A2; dbt = 20 * math.log10(tot)
H(M, CA4, S('Tầng 1 có độ lợi không tải 30 và trở kháng ra 2 kΩ, tải là tầng 2 có Rin = 6 kΩ và độ lợi 20. Độ lợi tổng (có xét tải) và giá trị dB là', 'Stage 1 has an unloaded gain of 30 and an output resistance of 2 kΩ and drives stage 2 with Rin = 6 kΩ and a gain of 20. The overall gain (loading included) and its value in dB are'),
  f'{g(tot, 3)}; {g(dbt, 3)} dB', [f'{g(A1 * A2, 3)}; {g(20 * math.log10(A1 * A2), 3)} dB', f'{g(ld, 3)}; {g(20 * math.log10(ld), 3)} dB', f'{g(A1 + A2, 3)}; {g(20 * math.log10(A1 + A2), 3)} dB'],
  S(f'Tầng 1 bị tải: 30 × 6/(2 + 6) = {g(ld, 3)}; tổng = {g(ld, 3)} × 20 = {g(tot, 3)} = {g(dbt, 3)} dB (bỏ qua tải cho 600 = 55,6 dB).', f'Stage 1 is loaded: 30 × 6/(2 + 6) = {g(ld, 3)}; total = {g(ld, 3)} × 20 = {g(tot, 3)} = {g(dbt, 3)} dB (ignoring loading gives 600 = 55.6 dB).'), SRC4, 'm04-cascade')
tot_db = 18 + 26 - 3; ratio = 10 ** (tot_db / 20); close(ratio, 10 ** (18 / 20) * 10 ** (26 / 20) * 10 ** (-3 / 20), 1e-9)          # dB add = ratios multiply
H(M, CA4, S('Ba khối nối tiếp có độ lợi 18 dB, 26 dB và −3 dB (bộ suy giảm). Độ lợi điện áp tổng dạng số lần là', 'Three blocks in cascade have gains of 18 dB, 26 dB and −3 dB (an attenuator). The overall voltage gain as a ratio is'),
  g(ratio, 4), [g(10 ** (18 / 20) + 10 ** (26 / 20) + 10 ** (-3 / 20), 4), g(10 ** (49 / 20), 4), '41'],
  S(f'18 + 26 − 3 = 41 dB → 10^(41/20) = {g(ratio, 4)} (nhân: 7,94 × 20 × 0,708 = 112,2).', f'18 + 26 − 3 = 41 dB → 10^(41/20) = {g(ratio, 4)} (multiplying: 7.94 × 20 × 0.708 = 112.2).'), SRC4, 'm04-cascade')
VCC, RL = 18.0, 8.0; Pout = VCC ** 2 / (2 * RL); Pdc = 2 * VCC ** 2 / (math.pi * RL); PD = (Pdc - Pout) / 2
th = np.linspace(0, math.pi, 400001); Idc = np.trapezoid(VCC / RL * np.sin(th), th) / (2 * math.pi) if hasattr(np, 'trapezoid') else np.trapz(VCC / RL * np.sin(th), th) / (2 * math.pi); close(VCC * 2 * Idc, Pdc, 1e-6)
H(M, PP4, S('Khuếch đại đẩy kéo lớp B (hai nguồn) có VCC = 18 V, RL = 8 Ω, ngõ ra biên độ cực đại. Công suất tiêu tán trong mỗi transistor là', 'A class B push-pull amplifier (two supplies) with VCC = 18 V and RL = 8 Ω delivers its maximum output swing. The power dissipated in each transistor is'),
  f'{g(PD, 3)} W', [f'{g(Pdc - Pout, 3)} W', f'{g(Pout, 4)} W', f'{g(Pdc / 2, 3)} W'],
  S(f'Pout = VCC²/(2RL) = 20,25 W; Pdc = 2VCC²/(πRL) = {g(Pdc, 4)} W (η = 78,5 %); tiêu tán tổng = {g(Pdc - Pout, 3)} W, mỗi transistor một nửa = {g(PD, 3)} W.', f'Pout = VCC²/(2RL) = 20.25 W; Pdc = 2VCC²/(πRL) = {g(Pdc, 4)} W (η = 78.5 %); total dissipation = {g(Pdc - Pout, 3)} W, half in each transistor = {g(PD, 3)} W.'), S('Floyd 9e §7–2', 'Floyd 9e §7–2'), 'm04-push-pull')
VCC, Rc, duty, Vce, Ic = 12.0, 100.0, 0.05, 0.3, 0.5; Pout = (2 * VCC) ** 2 / (8 * Rc); PDa = duty * Vce * Ic; eta = Pout / (Pout + PDa)
H(M, CL4, S('Khuếch đại lớp C có VCC = 12 V, Rc (tank song song) = 100 Ω, Vout(pp) = 2·VCC, transistor dẫn 5 % chu kỳ với VCE(sat) = 0,3 V, IC(sat) = 0,5 A. Hiệu suất η = Pout/(Pout + PD) là', 'A class C amplifier has VCC = 12 V, tank parallel resistance Rc = 100 Ω, Vout(pp) = 2·VCC, and the transistor conducts for 5 % of the cycle with VCE(sat) = 0.3 V and IC(sat) = 0.5 A. The efficiency η = Pout/(Pout + PD) is'),
  f'{g(100 * eta, 4)} %', [f'{g(100 * PDa / Pout, 3)} %', f'{g(100 * (1 - eta), 3)} %', '78.5 %'],
  S(f'Pout = (2·VCC)²/(8·Rc) = 0,72 W; PD = duty × VCE(sat) × IC(sat) = 0,05 × 0,3 × 0,5 = 7,5 mW; η = 0,72/(0,72 + 0,0075) = {g(100 * eta, 4)} %.', f'Pout = (2·VCC)²/(8·Rc) = 0.72 W; PD = duty × VCE(sat) × IC(sat) = 0.05 × 0.3 × 0.5 = 7.5 mW; η = 0.72/(0.72 + 0.0075) = {g(100 * eta, 4)} %.'), S('Floyd 9e §7–3', 'Floyd 9e §7–3'), 'm04-classes')
Ro, Rin, C = 4.7e3, 3.3e3, 2.2e-6; fcc = 1 / (2 * math.pi * (Ro + Rin) * C); f = 5.0; mg = 1 / math.sqrt(1 + (fcc / f) ** 2); dbm = 20 * math.log10(mg)
close(abs(1j * f / fcc / (1 + 1j * f / fcc)), mg, 1e-9)
H(M, CO4, S('Tầng trước có trở kháng ra 4,7 kΩ ghép RC (C = 2,2 μF) vào tầng sau có Rin = 3,3 kΩ. Độ lợi tại 5 Hz so với dải giữa là', 'A stage with an output resistance of 4.7 kΩ is RC-coupled (C = 2.2 μF) to a stage with Rin = 3.3 kΩ. The gain at 5 Hz relative to midband is'),
  f'{g(dbm, 3)} dB', [f'{g(-3.01, 3)} dB', f'{g(20 * math.log10(1 / math.sqrt(1 + (1 / (2 * math.pi * Rin * C) / f) ** 2)), 3)} dB', f'{g(20 * math.log10(f / fcc), 3)} dB'],
  S(f'R = 4,7 + 3,3 = 8 kΩ; fc = 1/(2π·8k·2,2 μF) = {g(fcc, 3)} Hz. Tại 5 Hz: 1/√(1 + (fc/f)²) = {g(mg, 3)} = {g(dbm, 3)} dB.', f'R = 4.7 + 3.3 = 8 kΩ; fc = 1/(2π·8k·2.2 μF) = {g(fcc, 3)} Hz. At 5 Hz: 1/√(1 + (fc/f)²) = {g(mg, 3)} = {g(dbm, 3)} dB.'), SRC4, 'm04-coupling')
A, B = 1e4, 0.01; a1 = A / (1 + A * B); a2 = 0.8 * A / (1 + 0.8 * A * B); ch = (a2 - a1) / a1 * 100
H(M, PN4, S('Mạch có hồi tiếp âm với Aol = 10 000 và B = 0,01. Nếu Aol giảm 20 % (còn 8000), độ lợi vòng kín thay đổi bao nhiêu phần trăm?', 'A negative-feedback circuit has Aol = 10,000 and B = 0.01. If Aol falls by 20 % (to 8000), by how many percent does the closed-loop gain change?'),
  f'−{g(abs(ch), 3)} %', ['−20 %', '−0.5 %', '−2.0 %'],
  S(f'Acl = A/(1 + AB): 10 000/101 = {g(a1, 4)} và 8000/81 = {g(a2, 4)}; thay đổi = {g(ch, 3)} % (hồi tiếp âm làm độ lợi bền với Aol).', f'Acl = A/(1 + AB): 10,000/101 = {g(a1, 4)} and 8000/81 = {g(a2, 4)}; change = {g(ch, 3)} % (negative feedback makes the gain robust against Aol).'), SRC4, 'm04-feedback')
n = 0
while 15 ** n <= 1000: n += 1
assert n == 3 and 15 ** 2 < 1000 < 15 ** 3
H(M, CA4, S('Mỗi tầng khuếch đại cho độ lợi điện áp tối đa 15. Cần tối thiểu bao nhiêu tầng nối tiếp để có độ lợi trên 1000?', 'Each amplifier stage gives a maximum voltage gain of 15. What is the minimum number of cascaded stages for an overall gain above 1000?'),
  '3', ['2', '4', '67'],
  S('15² = 225 < 1000 còn 15³ = 3375 > 1000 nên cần 3 tầng (độ lợi nhân với nhau, không cộng).', '15² = 225 < 1000 but 15³ = 3375 > 1000, so 3 stages are needed (gains multiply, they do not add).'), SRC4, 'm04-cascade')
# ============================================================================================ module 05
M = 'm05'; IA5, OT5, LG5, IS5, CV5 = 'Instrumentation amplifiers', 'OTA', 'Log and antilog amplifiers', 'Isolation amplifiers', 'Converters and peak detector'
SRC5 = S('Floyd 9e Ch.14; Jaeger 5e §12.5–12.6', 'Floyd 9e Ch.14; Jaeger 5e §12.5–12.6')
R, RG = 25e3, 500.0; G = 1 + 2 * R / RG; v1, v2 = 3.100, 3.085; vo = G * (v1 - v2); close(vo, 1.515, 1e-9)
H(M, IA5, S('Mạch khuếch đại thiết bị có R = 25 kΩ, RG = 500 Ω nhận 3,100 V và 3,085 V ở hai ngõ vào. Điện áp ra là', 'An instrumentation amplifier with R = 25 kΩ and RG = 500 Ω receives 3.100 V and 3.085 V at its two inputs. The output is'),
  f'{g(vo, 4)} V', [f'{g(G * (v1 + v2) / 2, 4)} V', f'{g((2 * R / RG) * (v1 - v2), 4)} V', f'{g(G * (v1 - v2) / 2, 4)} V'],
  S('G = 1 + 2R/RG = 1 + 100 = 101; chỉ phần vi sai (15 mV) được khuếch đại: 101 × 15 mV = 1,515 V; thành phần chung 3,0925 V bị triệt.', 'G = 1 + 2R/RG = 1 + 100 = 101; only the difference (15 mV) is amplified: 101 × 15 mV = 1.515 V; the common-mode part 3.0925 V is rejected.'), SRC5, 'm05-instrumentation')
Rr, Gt = 47e3, 250; RGx = 2 * Rr / (Gt - 1); close(1 + 2 * Rr / RGx, Gt)
H(M, IA5, S('Cần mạch khuếch đại thiết bị có độ lợi 250 với R = 47 kΩ (G = 1 + 2R/RG). Điện trở RG phải bằng', 'An instrumentation amplifier must have a gain of 250 with R = 47 kΩ (G = 1 + 2R/RG). The gain resistor RG must be'),
  f'{g(RGx, 4)} Ω', [f'{g(2 * Rr / Gt, 4)} Ω', f'{g(Rr / (Gt - 1), 4)} Ω', f'{g(2 * Rr / (Gt + 1), 4)} Ω'],
  S('RG = 2R/(G − 1) = 94 kΩ/249 = 377,5 Ω (nhớ trừ 1; dùng 2R/G cho 376 Ω là sai nhẹ).', 'RG = 2R/(G − 1) = 94 kΩ/249 = 377.5 Ω (remember the −1; using 2R/G gives 376 Ω, slightly off).'), SRC5, 'm05-instrumentation')
K, Ib, RL, Vin = 16e-6 / 1e-6, 62.5e-6, 5e3, 50e-3; gm = K * Ib; Iout = gm * Vin; vo = Iout * RL
H(M, OT5, S('OTA có gm = K·IBIAS với K = 16 μS/μA. Với IBIAS = 62,5 μA, tải RL = 5 kΩ và Vin = 50 mV, điện áp ra và độ lợi là', 'An OTA has gm = K·IBIAS with K = 16 μS/μA. With IBIAS = 62.5 μA, a load RL = 5 kΩ and Vin = 50 mV, the output voltage and gain are'),
  f'{g(vo, 3)} V; Av = {g(gm * RL, 3)}', [f'{g(vo * 1e3, 3)} V; Av = {g(gm * RL * 1e3, 3)}', f'{g(Iout * 1e6, 3)} V; Av = {g(gm * 1e6, 3)}', f'{g(vo / 5, 3)} V; Av = {g(gm * RL / 5, 3)}'],
  S(f'gm = 16 μS/μA × 62,5 μA = 1000 μS; Iout = gm·Vin = 50 μA; Vout = Iout·RL = 0,25 V; Av = gm·RL = 5 (đổi μS, μA về đơn vị gốc).', f'gm = 16 μS/μA × 62.5 μA = 1000 μS; Iout = gm·Vin = 50 μA; Vout = Iout·RL = 0.25 V; Av = gm·RL = 5 (convert μS, μA to base units).'), S('Floyd 9e §14–3', 'Floyd 9e §14–3'), 'm05-ota')
K, I0, dI, Vin, RL = 16.0, 50.0, 20.0, 10e-3, 10e3; gmax = K * (I0 + dI) * 1e-6; gmin = K * (I0 - dI) * 1e-6; vmax = gmax * Vin * RL; vmin = gmin * Vin * RL; mi = (vmax - vmin) / (vmax + vmin)
H(M, OT5, S('OTA (K = 16 μS/μA) có dòng phân cực biến điệu IBIAS = 50 μA ± 20 μA, tải 10 kΩ, sóng mang 10 mV. Biên độ ngõ ra lớn nhất và độ sâu điều biên là', 'An OTA (K = 16 μS/μA) with a modulated bias current IBIAS = 50 μA ± 20 μA, a 10 kΩ load and a 10 mV carrier. The largest output amplitude and the modulation depth are'),
  f'{g(vmax * 1e3, 4)} mV; {g(mi * 100, 3)} %', [f'{g(vmin * 1e3, 3)} mV; {g(mi * 100, 3)} %', f'{g(vmax * 1e3, 4)} mV; {g((vmax - vmin) / vmax * 100, 3)} %', f'{g(K * I0 * 1e-6 * Vin * RL * 1e3, 3)} mV; 0 %'],
  S('gm(max) = 16 × 70 = 1120 μS → 112 mV; gm(min) = 16 × 30 = 480 μS → 48 mV; m = (112 − 48)/(112 + 48) = 0,4 = 40 %.', 'gm(max) = 16 × 70 = 1120 μS → 112 mV; gm(min) = 16 × 30 = 480 μS → 48 mV; m = (112 − 48)/(112 + 48) = 0.4 = 40 %.'), S('Floyd 9e §14–3', 'Floyd 9e §14–3'), 'm05-ota')
VT, IEBO, R1, Vin = 0.025, 30e-9, 47e3, 2.0; vo = -VT * math.log(Vin / (R1 * IEBO)); d10 = -VT * math.log(10)
Id = Vin / R1; vd = brentq(lambda v: IEBO * (math.exp(v / VT) - 1) - Id, 0, 1); close(-vd, vo, 2e-3)
H(M, LG5, S('Mạch logarit (IEBO = 30 nA, R1 = 47 kΩ) nhận Vin = 2 V. Điện áp ra là bao nhiêu và khi Vin tăng 10 lần thì ngõ ra thay đổi bao nhiêu?', 'A log amplifier (IEBO = 30 nA, R1 = 47 kΩ) receives Vin = 2 V. What is the output and by how much does it change when Vin rises tenfold?'),
  (f'{g(vo * 1e3, 4)} mV; thay đổi {g(d10 * 1e3, 3)} mV', f'{g(vo * 1e3, 4)} mV; changes by {g(d10 * 1e3, 3)} mV'),
  [S(f'{g(-VT * math.log10(Vin / (R1 * IEBO)) * 1e3, 4)} mV; thay đổi {g(-VT * 1e3, 3)} mV', f'{g(-VT * math.log10(Vin / (R1 * IEBO)) * 1e3, 4)} mV; changes by {g(-VT * 1e3, 3)} mV'), S(f'{g(-vo * 1e3, 4)} mV; thay đổi {g(-d10 * 1e3, 3)} mV', f'{g(-vo * 1e3, 4)} mV; changes by {g(-d10 * 1e3, 3)} mV'), S(f'{g(vo * 1e3 / 10, 4)} mV; thay đổi {g(d10 * 1e3 * 10, 3)} mV', f'{g(vo * 1e3 / 10, 4)} mV; changes by {g(d10 * 1e3 * 10, 3)} mV')],
  S(f'Vout = −0,025·ln(Vin/(IEBO·R1)) = −0,025·ln(1418) = {g(vo * 1e3, 4)} mV; Vin × 10 cộng thêm −0,025·ln 10 = {g(d10 * 1e3, 3)} mV (nén dải động).', f'Vout = −0.025·ln(Vin/(IEBO·R1)) = −0.025·ln(1418) = {g(vo * 1e3, 4)} mV; Vin × 10 adds −0.025·ln 10 = {g(d10 * 1e3, 3)} mV (dynamic-range compression).'), S('Floyd 9e §14–4', 'Floyd 9e §14–4'), 'm05-log')
n, VFS, vin = 12, 4.096, 2.3456; LSB = VFS / 2 ** n; code = int(round(vin / LSB)); sar = 0
for k in range(n - 1, -1, -1):
    if (sar | (1 << k)) * LSB <= vin + 1e-12: sar |= 1 << k
assert code == 2346 and sar == 2345
H(M, CV5, S('ADC SAR 12 bit có VFS = 4,096 V, đồng hồ 2 MHz nhận 2,3456 V. Một LSB, mã số nguyên gần nhất và thời gian chuyển đổi n/f_C lần lượt là', 'A 12-bit SAR ADC with VFS = 4.096 V and a 2 MHz clock receives 2.3456 V. One LSB, the nearest integer code and the conversion time n/f_C are'),
  f'1 mV; 2346; {g(n / 2e6 * 1e6, 3)} μs', [f'1 mV; 2346; {g(2 ** n / 2e6 * 1e6, 4)} μs', f'1.0005 mV; 2345; {g(n / 2e6 * 1e6, 3)} μs', f'1 mV; 2345; 1 μs'],
  S('LSB = 4,096/4096 = 1 mV; 2,3456 V/1 mV = 2345,6 → mã 2346 (làm tròn); SAR cần n = 12 chu kỳ: 12/2 MHz = 6 μs.', 'LSB = 4.096/4096 = 1 mV; 2.3456 V/1 mV = 2345.6 → code 2346 (rounded); a SAR needs n = 12 clock cycles: 12/2 MHz = 6 μs.'), S('Jaeger 5e §12.5–12.6', 'Jaeger 5e §12.5–12.6'), 'm05-adc-dac')
g1, g2, vin = 12.0, 8.0, 15e-3; vo = g1 * g2 * vin
H(M, IS5, S('Mạch cách ly có tầng vào độ lợi 12 và tầng ra độ lợi 8, ngõ vào 15 mV rms. Điện áp ra rms là', 'An isolation amplifier has an input stage of gain 12 and an output stage of gain 8 with a 15 mV rms input. The output voltage is'),
  f'{g(vo, 4)} V rms', [f'{g((g1 + g2) * vin, 3)} V rms', f'{g(g1 * vin, 3)} V rms', f'{g(g1 * g2 * vin * 1e3, 3)} V rms'],
  S('Độ lợi tổng = tích hai tầng: 12 × 8 = 96; 96 × 15 mV = 1,44 V rms (hai tầng cách ly điện nhưng tín hiệu vẫn nhân).', 'The overall gain is the product of the two stages: 12 × 8 = 96; 96 × 15 mV = 1.44 V rms (the stages are electrically isolated but the signal is still multiplied).'), S('Floyd 9e §14–2', 'Floyd 9e §14–2'), 'm05-isolation')
Vin, R1, Vsat = 3.3, 1.5e3, 11.0; I = Vin / R1; RLmax = Vsat / I - R1
H(M, CV5, S('Nguồn dòng V–I (tải nằm trong vòng hồi tiếp) có Vin = 3,3 V, R1 = 1,5 kΩ, op-amp bão hoà ở ±11 V. Dòng tải và điện trở tải lớn nhất còn giữ dòng không đổi là', 'A V-to-I current source (load in the feedback loop) has Vin = 3.3 V, R1 = 1.5 kΩ and an op-amp that saturates at ±11 V. The load current and the largest load resistance that keeps it constant are'),
  f'{g(I * 1e3, 3)} mA; {g(RLmax / 1e3, 3)} kΩ', [f'{g(I * 1e3, 3)} mA; {g(Vsat / I / 1e3, 3)} kΩ', f'{g(Vin / 1e3 * 1e3 / 1.5 * 0.5, 3)} mA; {g(RLmax / 1e3, 3)} kΩ', f'{g(I * 1e3, 3)} mA; {g((Vsat / I - 2 * R1) / 1e3, 3)} kΩ'],
  S('I = Vin/R1 = 2,2 mA. Vout = I·(RL + R1) ≤ 11 V → RL ≤ 11/2,2 mA − 1,5 kΩ = 3,5 kΩ.', 'I = Vin/R1 = 2.2 mA. Vout = I·(RL + R1) ≤ 11 V → RL ≤ 11/2.2 mA − 1.5 kΩ = 3.5 kΩ.'), S('Floyd 9e §14–5', 'Floyd 9e §14–5'), 'm05-v-i')
# ============================================================================================ module 06
M = 'm06'; LP6, HP6, BP6, PO6, BU6 = 'Low-pass filters', 'High-pass filters', 'Band-pass and band-stop filters', 'Filter responses and poles', 'Butterworth, Chebyshev, Bessel; damping'
SRC6 = S('Floyd 9e Ch.15', 'Floyd 9e Ch.15')
def bw_sections(n):
    poles = [cmath.exp(1j * math.pi * (2 * k + n - 1) / (2 * n)) for k in range(1, n + 1)]; up = sorted(-2 * p.real for p in poles if p.imag > 1e-9); return up
d4 = bw_sections(4); close(d4[0], 0.7654, 1e-3); close(d4[1], 1.8478, 1e-3); ratio = 2 - d4[0]
H(M, BU6, S('Bộ lọc thông thấp Butterworth bậc 4 gồm hai tầng Sallen-Key có hệ số tắt dần DF = 1,848 và DF = 0,765. Tỉ số R1/R2 của tầng có DF = 0,765 là (DF = 2 − R1/R2)', 'A 4th-order Butterworth low-pass filter uses two Sallen-Key stages with damping factors DF = 1.848 and DF = 0.765. The ratio R1/R2 of the stage with DF = 0.765 is (DF = 2 − R1/R2)'),
  f'{g(ratio, 4)}', [g(2 - d4[1], 3), g(d4[0], 3), g(2 + d4[0], 4)],
  S(f'R1/R2 = 2 − DF = 2 − 0,765 = {g(ratio, 4)}; tầng DF = 1,848 cần R1/R2 = 0,152. Hai giá trị DF lấy từ các cực Butterworth bậc 4 (2 sin 22,5° và 2 sin 67,5°).', f'R1/R2 = 2 − DF = 2 − 0.765 = {g(ratio, 4)}; the DF = 1.848 stage needs R1/R2 = 0.152. The two DF values come from the 4th-order Butterworth poles (2 sin 22.5° and 2 sin 67.5°).'), SRC6, 'm06-characteristics')
n, f, fc = 3, 8e3, 1e3; att = -10 * math.log10(1 + (f / fc) ** (2 * n)); pol = np.poly1d(np.poly([cmath.exp(1j * math.pi * (2 * k + n - 1) / (2 * n)) for k in range(1, n + 1)]).real); s_ = 1j * f / fc; hh = 1 / abs(pol(s_)); close(20 * math.log10(hh), att, 1e-6)
H(M, PO6, S('Bộ lọc thông thấp Butterworth 3 cực có fc = 1 kHz. Độ suy giảm tại 8 kHz (đáp ứng Butterworth chính xác) xấp xỉ', 'A 3-pole Butterworth low-pass filter has fc = 1 kHz. The attenuation at 8 kHz (exact Butterworth response) is about'),
  f'{g(att, 3)} dB', [f'{g(-20 * math.log10(8), 3)} dB', f'{g(-40 * math.log10(8), 3)} dB', f'{g(-80 * math.log10(8), 3)} dB'],
  S(f'|H|² = 1/(1 + (f/fc)^(2n)) = 1/(1 + 8⁶): −10·log₁₀(262 145) = {g(att, 3)} dB (đoạn tiệm cận −60 dB/decade × log 8 = −54,2 dB cũng cho kết quả này vì ở xa fc).', f'|H|² = 1/(1 + (f/fc)^(2n)) = 1/(1 + 8⁶): −10·log₁₀(262,145) = {g(att, 3)} dB (the asymptote −60 dB/decade × log 8 = −54.2 dB agrees because we are far from fc).'), SRC6, 'm06-poles')
fc, C = 2.5e3, 10e-9; R = 1 / (2 * math.pi * fc * C); wn = 1 / (R * C); H1 = lambda f_: 1 / (1 + 1j * 2 * math.pi * f_ * R * C); close(abs(H1(fc)), 1 / math.sqrt(2), 1e-9)
H(M, LP6, S('Thiết kế tầng Sallen-Key thông thấp có RA = RB = R và CA = CB = 10 nF, fc = 2,5 kHz. R phải bằng', 'Design a low-pass Sallen-Key stage with RA = RB = R and CA = CB = 10 nF for fc = 2.5 kHz. R must be'),
  f'{g(R / 1e3, 3)} kΩ', [f'{g(R / 1e3 / 2, 3)} kΩ', f'{g(R / 1e3 * 2 * math.pi, 3)} kΩ', f'{g(R / 1e3 / math.sqrt(2), 3)} kΩ'],
  S(f'fc = 1/(2π·R·C) → R = 1/(2π × 2500 × 10 nF) = {g(R / 1e3, 3)} kΩ (với RA = RB, CA = CB thì căn trong công thức tổng quát bằng RC).', f'fc = 1/(2π·R·C) → R = 1/(2π × 2500 × 10 nF) = {g(R / 1e3, 3)} kΩ (with RA = RB, CA = CB the root of the general formula equals RC).'), SRC6, 'm06-sallen-key')
fl, fh = 300.0, 3400.0; f0 = math.sqrt(fl * fh); BW = fh - fl; Q = f0 / BW
H(M, BP6, S('Bộ lọc thông dải ghép từ thông cao fc = 300 Hz và thông thấp fc = 3,4 kHz. Tần số trung tâm f0 = √(f₁f₂), Q và loại (hẹp/rộng) là', 'A band-pass filter is built from a 300 Hz high-pass and a 3.4 kHz low-pass. The centre frequency f0 = √(f₁f₂), the Q and the type (narrow/wide) are'),
  S(f'{g(f0, 4)} Hz; Q = {g(Q, 3)}; dải rộng', f'{g(f0, 4)} Hz; Q = {g(Q, 3)}; wide-band'), [S(f'{g((fl + fh) / 2, 4)} Hz; Q = {g((fl + fh) / 2 / BW, 3)}; dải rộng', f'{g((fl + fh) / 2, 4)} Hz; Q = {g((fl + fh) / 2 / BW, 3)}; wide-band'), S(f'{g(f0, 4)} Hz; Q = {g(1 / Q, 3)}; dải hẹp', f'{g(f0, 4)} Hz; Q = {g(1 / Q, 3)}; narrow-band'), S(f'{g(fh, 4)} Hz; Q = {g(fh / BW, 3)}; dải hẹp', f'{g(fh, 4)} Hz; Q = {g(fh / BW, 3)}; narrow-band')],
  S(f'f0 = √(300 × 3400) = {g(f0, 4)} Hz (trung bình nhân); BW = 3400 − 300 = 3100 Hz; Q = f0/BW = {g(Q, 3)} < 1 nên là dải rộng (dải hẹp khi Q > 10).', f'f0 = √(300 × 3400) = {g(f0, 4)} Hz (geometric mean); BW = 3400 − 300 = 3100 Hz; Q = f0/BW = {g(Q, 3)} < 1 so it is wide-band (narrow-band needs Q > 10).'), SRC6, 'm06-bandpass')
f0, Q, C = 1e3, 10.0, 10e-9; BW = f0 / Q; R2 = 1 / (math.pi * BW * C)
def mfb(R1, R2, R3, C):
    def Hh(f_):
        s = 2j * math.pi * f_; G1, G2, G3 = 1 / R1, 1 / R2, 1 / R3; va = -G2 / (s * C); return 1 / ((va * (G1 + G3 + 2 * s * C) - s * C) / G1)
    return Hh
f3 = np.geomspace(500, 2000, 100001)
# choose R1, R3 so that f0 = (1/2πC)·sqrt((R1+R3)/(R1·R2·R3)) holds for the designed R2: R1 = R3 → f0 = (1/2πC)·sqrt(2/(R1·R2))
R1 = 2 / ((2 * math.pi * f0 * C) ** 2 * R2); R3 = R1; Hm = mfb(R1, R2, R3, C); mag = np.array([abs(Hm(x)) for x in f3]); pk = f3[mag.argmax()]; close(pk, f0, 5e-3)
half = mag.max() / math.sqrt(2); lo = f3[:mag.argmax()][np.argmin(np.abs(mag[:mag.argmax()] - half))]; hi = f3[mag.argmax():][np.argmin(np.abs(mag[mag.argmax():] - half))]; close(hi - lo, BW, 2e-2)
H(M, BP6, S('Bộ lọc thông dải hồi tiếp nhiều đường (hai tụ bằng nhau C = 10 nF) cần f0 = 1 kHz và Q = 10. Điện trở R2 đặt băng thông (BW = 1/(π·R2·C)) phải bằng', 'A multiple-feedback band-pass filter (two equal capacitors C = 10 nF) must have f0 = 1 kHz and Q = 10. The resistor R2 that sets the bandwidth (BW = 1/(π·R2·C)) must be'),
  f'{g(R2 / 1e3, 4)} kΩ', [f'{g(1 / (2 * math.pi * BW * C) / 1e3, 4)} kΩ', f'{g(1 / (math.pi * f0 * C) / 1e3, 4)} kΩ', f'{g(R2 * Q / 1e3, 4)} kΩ'],
  S(f'BW = f0/Q = 100 Hz; R2 = 1/(π·BW·C) = 1/(π × 100 × 10 nF) = {g(R2 / 1e3, 4)} kΩ (đã kiểm bằng đáp ứng tần số của mạch: đỉnh ở f0, băng thông 100 Hz).', f'BW = f0/Q = 100 Hz; R2 = 1/(π·BW·C) = 1/(π × 100 × 10 nF) = {g(R2 / 1e3, 4)} kΩ (checked on the circuit\'s frequency response: peak at f0, bandwidth 100 Hz).'), SRC6, 'm06-bandpass')
n4 = 4; atten = -10 * math.log10(1 + (1 / 0.1) ** (2 * n4))
H(M, HP6, S('Bộ lọc thông cao Butterworth 4 cực (hai tầng Sallen-Key). Độ suy giảm tại f = fc/10 xấp xỉ', 'A 4-pole Butterworth high-pass filter (two Sallen-Key stages). The attenuation at f = fc/10 is about'),
  f'{g(atten, 3)} dB', ['−40 dB', '−20 dB', '−60 dB'],
  S('|H|² = 1/(1 + (fc/f)^(2n)) = 1/(1 + 10⁸) → −80 dB: mỗi cực −20 dB/decade, bốn cực −80 dB/decade.', '|H|² = 1/(1 + (fc/f)^(2n)) = 1/(1 + 10⁸) → −80 dB: each pole gives −20 dB/decade, four poles −80 dB/decade.'), SRC6, 'm06-poles')
DFb = math.sqrt(3); rr = 2 - DFb
H(M, BU6, S('Tầng Sallen-Key hai cực đáp ứng Bessel có DF = 1,732. Tỉ số R1/R2 và hệ số phẩm chất tương ứng Q = 1/DF là', 'A two-pole Sallen-Key stage with a Bessel response has DF = 1.732. The ratio R1/R2 and the corresponding quality factor Q = 1/DF are'),
  S(f'{g(rr, 3)}; Q = {g(1 / DFb, 3)}', f'{g(rr, 3)}; Q = {g(1 / DFb, 3)}'), [S(f'{g(2 - 1.414, 3)}; Q = {g(1 / 1.414, 3)}', f'{g(2 - 1.414, 3)}; Q = {g(1 / 1.414, 3)}'), S(f'{g(2 + DFb, 3)}; Q = {g(DFb, 3)}', f'{g(2 + DFb, 3)}; Q = {g(DFb, 3)}'), S(f'{g(rr, 3)}; Q = {g(DFb, 3)}', f'{g(rr, 3)}; Q = {g(DFb, 3)}')],
  S(f'R1/R2 = 2 − DF = 2 − 1,732 = {g(rr, 3)}; Q = 1/DF = {g(1 / DFb, 3)} (Butterworth hai cực: DF = 1,414, Q = 0,707, R1/R2 = 0,586).', f'R1/R2 = 2 − DF = 2 − 1.732 = {g(rr, 3)}; Q = 1/DF = {g(1 / DFb, 3)} (two-pole Butterworth: DF = 1.414, Q = 0.707, R1/R2 = 0.586).'), SRC6, 'm06-characteristics')
fc1 = 10e3; both = fc1 * math.sqrt(math.sqrt(2) - 1); f = np.linspace(1e3, 20e3, 400000); mg = np.abs(1 / (1 + 1j * f / fc1)) ** 2; f3 = f[np.argmin(np.abs(mg - 1 / math.sqrt(2)))]; close(f3, both, 2e-3)
H(M, PO6, S('Hai bộ lọc thông thấp RC một cực giống nhau (mỗi bộ fc = 10 kHz) được ghép nối tiếp qua mạch đệm. Tần số −3 dB của cả hai xấp xỉ', 'Two identical single-pole RC low-pass filters (each fc = 10 kHz) are cascaded through a buffer. The −3 dB frequency of the pair is about'),
  f'{g(both / 1e3, 3)} kHz', ['10 kHz', '5 kHz', f'{g(fc1 / math.sqrt(2) / 1e3, 3)} kHz'],
  S(f'|H|² = 1/(1 + (f/fc)²)² = 1/2 → (f/fc)² = √2 − 1 → f = fc·√(√2 − 1) = {g(both / 1e3, 3)} kHz (ghép cực làm hẹp băng thông, không giữ nguyên fc).', f'|H|² = 1/(1 + (f/fc)²)² = 1/2 → (f/fc)² = √2 − 1 → f = fc·√(√2 − 1) = {g(both / 1e3, 3)} kHz (cascading poles narrows the bandwidth; fc does not stay).'), SRC6, 'm06-cascade')
# ============================================================================================ module 07
M = 'm07'; RC7, FO7, LC7, RX7, T55 = 'RC oscillators', 'Feedback oscillator conditions', 'LC and crystal oscillators', 'Relaxation oscillators', 'The 555 timer'
SRC7 = S('Floyd 9e Ch.16', 'Floyd 9e Ch.16')
R, C = 8.2e3, 0.022e-6; fr = 1 / (2 * math.pi * R * C); Z1 = lambda f_: R + 1 / (2j * math.pi * f_ * C); Z2 = lambda f_: R / (1 + 2j * math.pi * f_ * R * C); Bf = lambda f_: Z2(f_) / (Z1(f_) + Z2(f_)); close(abs(Bf(fr)), 1 / 3, 1e-9); Ri = 10e3
H(M, RC7, S('Mạch dao động cầu Wien có R = 8,2 kΩ, C = 0,022 μF. Tần số dao động và điện trở hồi tiếp Rf tối thiểu để khởi động khi Ri = 10 kΩ (độ lợi > 3) là', 'A Wien-bridge oscillator has R = 8.2 kΩ and C = 0.022 μF. The oscillation frequency and the minimum feedback resistor Rf to start up with Ri = 10 kΩ (gain > 3) are'),
  S(f'{g(fr, 4)} Hz; Rf > 20 kΩ', f'{g(fr, 4)} Hz; Rf > 20 kΩ'), [S(f'{g(fr, 4)} Hz; Rf > 30 kΩ', f'{g(fr, 4)} Hz; Rf > 30 kΩ'), S(f'{g(fr / math.sqrt(6) * 1, 4)} Hz; Rf > 20 kΩ', f'{g(fr / math.sqrt(6), 4)} Hz; Rf > 20 kΩ'), S(f'{g(2 * math.pi * fr, 4)} Hz; Rf > 290 kΩ', f'{g(2 * math.pi * fr, 4)} Hz; Rf > 290 kΩ')],
  S(f'fr = 1/(2πRC) = {g(fr, 4)} Hz; B = 1/3 nên Av = 1 + Rf/Ri phải > 3 → Rf > 2·Ri = 20 kΩ.', f'fr = 1/(2πRC) = {g(fr, 4)} Hz; B = 1/3 so Av = 1 + Rf/Ri must exceed 3 → Rf > 2·Ri = 20 kΩ.'), SRC7, 'm07-wien')
R, C, Ri = 4.7e3, 0.01e-6, 4.7e3; fr = 1 / (2 * math.pi * math.sqrt(6) * R * C); w = 2 * math.pi * fr; Zc = 1 / (1j * w * C); Am = np.array([[Zc + R, -R, 0], [-R, Zc + 2 * R, -R], [0, -R, Zc + 2 * R]], dtype=complex); i = np.linalg.solve(Am, [1, 0, 0]); close(abs(i[2] * R), 1 / 29, 1e-6)
H(M, RC7, S('Mạch dao động dịch pha ba tầng RC (R = 4,7 kΩ, C = 0,01 μF) với Ri = 4,7 kΩ. Tần số dao động và Rf tối thiểu (độ lợi 29) là', 'A three-section RC phase-shift oscillator (R = 4.7 kΩ, C = 0.01 μF) with Ri = 4.7 kΩ. The oscillation frequency and the minimum Rf (gain 29) are'),
  S(f'{g(fr / 1e3, 4)} kHz; Rf = {g(29 * Ri / 1e3, 3)} kΩ', f'{g(fr / 1e3, 4)} kHz; Rf = {g(29 * Ri / 1e3, 3)} kΩ'), [S(f'{g(1 / (2 * math.pi * R * C) / 1e3, 4)} kHz; Rf = {g(29 * Ri / 1e3, 3)} kΩ', f'{g(1 / (2 * math.pi * R * C) / 1e3, 4)} kHz; Rf = {g(29 * Ri / 1e3, 3)} kΩ'), S(f'{g(fr / 1e3, 4)} kHz; Rf = {g(2 * Ri / 1e3, 3)} kΩ', f'{g(fr / 1e3, 4)} kHz; Rf = {g(2 * Ri / 1e3, 3)} kΩ'), S(f'{g(fr * math.sqrt(6) / 1e3, 4)} kHz; Rf = {g(3 * Ri / 1e3, 3)} kΩ', f'{g(fr * math.sqrt(6) / 1e3, 4)} kHz; Rf = {g(3 * Ri / 1e3, 3)} kΩ')],
  S(f'fr = 1/(2π√6·RC) = {g(fr / 1e3, 4)} kHz; B = 1/29 nên Rf = 29·Ri = {g(29 * Ri / 1e3, 3)} kΩ (đã kiểm: mạng thang ba tầng cho |B| = 1/29, pha 180°).', f'fr = 1/(2π√6·RC) = {g(fr / 1e3, 4)} kHz; B = 1/29 so Rf = 29·Ri = {g(29 * Ri / 1e3, 3)} kΩ (checked: the three-section ladder gives |B| = 1/29 at 180°).'), SRC7, 'm07-phase-shift')
L, C1, C2 = 100e-6, 470e-12, 47e-12; CT = C1 * C2 / (C1 + C2); f0 = 1 / (2 * math.pi * math.sqrt(L * CT)); Zl = lambda f_: 1j * 2 * math.pi * f_ * L + 1 / (1j * 2 * math.pi * f_ * C1) + 1 / (1j * 2 * math.pi * f_ * C2); fz = brentq(lambda f_: Zl(f_).imag, 0.1 * f0, 10 * f0); close(fz, f0, 1e-9)
H(M, LC7, S('Mạch dao động Colpitts có L = 100 μH, C1 = 470 pF, C2 = 47 pF. Tần số dao động và độ lợi tối thiểu Av > C1/C2 là', 'A Colpitts oscillator has L = 100 μH, C1 = 470 pF and C2 = 47 pF. The oscillation frequency and the minimum gain Av > C1/C2 are'),
  S(f'{g(f0 / 1e6, 3)} MHz; Av > 10', f'{g(f0 / 1e6, 3)} MHz; Av > 10'), [S(f'{g(1 / (2 * math.pi * math.sqrt(L * (C1 + C2))) / 1e6, 3)} MHz; Av > 10', f'{g(1 / (2 * math.pi * math.sqrt(L * (C1 + C2))) / 1e6, 3)} MHz; Av > 10'), S(f'{g(f0 / 1e6, 3)} MHz; Av > 0.1', f'{g(f0 / 1e6, 3)} MHz; Av > 0.1'), S(f'{g(1 / (2 * math.pi * math.sqrt(L * C2)) / 1e6, 3)} MHz; Av > 1', f'{g(1 / (2 * math.pi * math.sqrt(L * C2)) / 1e6, 3)} MHz; Av > 1')],
  S(f'CT = C1C2/(C1 + C2) = 42,7 pF (hai tụ nối tiếp nhìn từ cuộn cảm); f0 = 1/(2π√(L·CT)) = {g(f0 / 1e6, 3)} MHz; B = C2/C1 = 0,1 nên Av > 10.', f'CT = C1C2/(C1 + C2) = 42.7 pF (two capacitors in series seen by the coil); f0 = 1/(2π√(L·CT)) = {g(f0 / 1e6, 3)} MHz; B = C2/C1 = 0.1 so Av > 10.'), SRC7, 'm07-lc')
Ls, Cs = 0.1, 0.04e-12; fs = 1 / (2 * math.pi * math.sqrt(Ls * Cs)); Zx = lambda f_: 1j * 2 * math.pi * f_ * Ls + 1 / (1j * 2 * math.pi * f_ * Cs); fz = brentq(lambda f_: Zx(f_).imag, 0.5 * fs, 2 * fs); close(fz, fs, 1e-9)
H(M, LC7, S('Thạch anh có Ls = 0,1 H và Cs = 0,04 pF. Tần số cộng hưởng nối tiếp fs = 1/(2π√(Ls·Cs)) là', 'A crystal has Ls = 0.1 H and Cs = 0.04 pF. The series resonant frequency fs = 1/(2π√(Ls·Cs)) is'),
  f'{g(fs / 1e6, 4)} MHz', [f'{g(fs / 1e6 / 2 / math.pi, 4)} MHz', f'{g(fs * 2 * math.pi / 1e6, 4)} MHz', f'{g(1 / (2 * math.pi * math.sqrt(Ls * Cs * 1e6)) / 1e6, 4)} MHz'],
  S(f'√(0,1 × 0,04·10⁻¹²) = 6,32·10⁻⁸ → fs = 1/(2π × 6,32·10⁻⁸) = {g(fs / 1e6, 4)} MHz (đã kiểm: trở kháng tổng bằng thuần trở đúng tại fs).', f'√(0.1 × 0.04·10⁻¹²) = 6.32·10⁻⁸ → fs = 1/(2π × 6.32·10⁻⁸) = {g(fs / 1e6, 4)} MHz (checked: the impedance is purely resistive at fs).'), SRC7, 'm07-lc')
f, d, Ct = 2e3, 0.65, 10e-9
# solve the two equations f = 1.44/((R1 + 2R2)C), duty = (R1 + R2)/(R1 + 2R2)
tot = 1.44 / (f * Ct); R2_ = tot * (1 - d); R1_ = tot - 2 * R2_
tH = 0.693 * (R1_ + R2_) * Ct; tL = 0.693 * R2_ * Ct; close(1 / (tH + tL), f, 1.5e-2); close(tH / (tH + tL), d, 1e-3)
H(M, T55, S('Thiết kế 555 phi ổn có f = 2 kHz, chu kỳ làm việc 65 %, Cext = 10 nF (f = 1,44/((R1 + 2R2)C), duty = (R1 + R2)/(R1 + 2R2)). Giá trị R1 và R2 xấp xỉ', 'Design an astable 555 for f = 2 kHz with a 65 % duty cycle and Cext = 10 nF (f = 1.44/((R1 + 2R2)C), duty = (R1 + R2)/(R1 + 2R2)). R1 and R2 are about'),
  S(f'R1 ≈ {g(R1_ / 1e3, 3)} kΩ; R2 ≈ {g(R2_ / 1e3, 3)} kΩ', f'R1 ≈ {g(R1_ / 1e3, 3)} kΩ; R2 ≈ {g(R2_ / 1e3, 3)} kΩ'), [S(f'R1 ≈ {g(R2_ / 1e3, 3)} kΩ; R2 ≈ {g(R1_ / 1e3, 3)} kΩ', f'R1 ≈ {g(R2_ / 1e3, 3)} kΩ; R2 ≈ {g(R1_ / 1e3, 3)} kΩ'), S(f'R1 ≈ {g(tot * d / 1e3, 3)} kΩ; R2 ≈ {g(tot * (1 - d) / 1e3, 3)} kΩ', f'R1 ≈ {g(tot * d / 1e3, 3)} kΩ; R2 ≈ {g(tot * (1 - d) / 1e3, 3)} kΩ'), S(f'R1 ≈ {g(tot / 3 / 1e3, 3)} kΩ; R2 ≈ {g(tot / 3 / 1e3, 3)} kΩ', f'R1 ≈ {g(tot / 3 / 1e3, 3)} kΩ; R2 ≈ {g(tot / 3 / 1e3, 3)} kΩ')],
  S(f'R1 + 2R2 = 1,44/(f·C) = {g(tot / 1e3, 3)} kΩ; duty = 0,65 → R2 = (1 − duty)(R1 + 2R2) = {g(R2_ / 1e3, 3)} kΩ; R1 = {g(R1_ / 1e3, 3)} kΩ (kiểm: tH + tL cho {g(1 / (tH + tL), 4)} Hz, duty {g(tH / (tH + tL), 3)}).', f'R1 + 2R2 = 1.44/(f·C) = {g(tot / 1e3, 3)} kΩ; duty = 0.65 → R2 = (1 − duty)(R1 + 2R2) = {g(R2_ / 1e3, 3)} kΩ; R1 = {g(R1_ / 1e3, 3)} kΩ (check: tH + tL gives {g(1 / (tH + tL), 4)} Hz, duty {g(tH / (tH + tL), 3)}).'), SRC7, 'm07-555-astable')
tW, Cm = 250e-3, 4.7e-6; Rm = tW / (1.1 * Cm); close(1.1 * Rm * Cm, tW)
H(M, T55, S('555 đơn ổn cần độ rộng xung tW = 250 ms với C = 4,7 μF (tW = 1,1·R·C). Điện trở R phải bằng', 'A monostable 555 needs a pulse width tW = 250 ms with C = 4.7 μF (tW = 1.1·R·C). The resistor R must be'),
  f'{g(Rm / 1e3, 4)} kΩ', [f'{g(tW / (0.693 * Cm) / 1e3, 4)} kΩ', f'{g(tW / Cm / 1e3, 4)} kΩ', f'{g(1.1 * tW / Cm / 1e3, 4)} kΩ'],
  S(f'R = tW/(1,1·C) = 0,25/(1,1 × 4,7·10⁻⁶) = {g(Rm / 1e3, 4)} kΩ (hệ số 0,693 là của chế độ phi ổn).', f'R = tW/(1.1·C) = 0.25/(1.1 × 4.7·10⁻⁶) = {g(Rm / 1e3, 4)} kΩ (the factor 0.693 belongs to the astable mode).'), SRC7, 'm07-555-monostable')
Vcc, Vc, R1, R2, C = 12.0, 9.0, 10e3, 10e3, 10e-9
def sim555(Vc):
    lo, hi = Vc / 2, Vc; dt = 1e-8; v = lo; t = 0.0; hi_state = True; edges = []
    while len(edges) < 5:
        tau = (R1 + R2) * C if hi_state else R2 * C; target = Vcc if hi_state else 0.0; v += (target - v) * dt / tau; t += dt
        if hi_state and v >= hi: hi_state = False; edges.append(t)
        elif (not hi_state) and v <= lo: hi_state = True; edges.append(t)
    return 1 / (edges[-1] - edges[-3])
f_c = sim555(9.0); f_d = sim555(8.0)
tH = (R1 + R2) * C * math.log((Vcc - Vc / 2) / (Vcc - Vc)); tL = R2 * C * math.log(2); f_an = 1 / (tH + tL); close(f_c, f_an, 5e-3)
f_def = 1 / (0.693 * (R1 + 2 * R2) * C)
H(M, T55, S('555 phi ổn (Vcc = 12 V, R1 = R2 = 10 kΩ, Cext = 10 nF) có chân điều khiển (chân 5) được giữ ở 9 V thay vì 8 V mặc định (2/3 Vcc). Tần số khi đó xấp xỉ', 'An astable 555 (Vcc = 12 V, R1 = R2 = 10 kΩ, Cext = 10 nF) has its control pin (pin 5) held at 9 V instead of the default 8 V (2/3 Vcc). The frequency is then about'),
  f'{g(f_an / 1e3, 3)} kHz', [f'{g(f_def / 1e3, 3)} kHz', f'{g(f_an / 1e3 * 1.2, 3)} kHz', f'{g(f_an / 1e3 / 1.5, 3)} kHz'],
  S(f'Ngưỡng là 9 V và 4,5 V: tH = (R1 + R2)C·ln((12 − 4,5)/(12 − 9)) = {g(tH * 1e6, 4)} μs; tL = R2C·ln 2 = {g(tL * 1e6, 4)} μs; f = {g(f_an / 1e3, 3)} kHz (mặc định 4,81 kHz; đã kiểm bằng mô phỏng theo thời gian).', f'The thresholds are 9 V and 4.5 V: tH = (R1 + R2)C·ln((12 − 4.5)/(12 − 9)) = {g(tH * 1e6, 4)} μs; tL = R2C·ln 2 = {g(tL * 1e6, 4)} μs; f = {g(f_an / 1e3, 3)} kHz (default 4.81 kHz; checked by time-domain simulation).'), SRC7, 'm07-555-astable')
# ============================================================================================ module 08
M = 'm08'; IC8, SE8, RB8, SW8, SH8 = 'IC regulators', 'Series regulators and current limiting', 'Regulation and regulator blocks', 'Switching regulators', 'Shunt regulators'
SRC8 = S('Floyd 9e Ch.17', 'Floyd 9e Ch.17')
R1, R2 = 240.0, 1500.0; vo = 1.25 * (1 + R2 / R1) + 50e-6 * R2; vo0 = 1.25 * (1 + R2 / R1)
close(vo0, 1.25 * (1 + 1500 / 240))
H(M, IC8, S('Thiết kế LM317 ra 9 V với R1 = 240 Ω: R2 = (9/1,25 − 1)·240 = 1488 Ω; dùng điện trở chuẩn 1,5 kΩ. Với IADJ = 50 μA, điện áp ra thực là', 'Design an LM317 for 9 V with R1 = 240 Ω: R2 = (9/1.25 − 1)·240 = 1488 Ω; the nearest standard resistor is 1.5 kΩ. With IADJ = 50 μA the actual output is'),
  f'{g(vo, 3)} V', [f'{g(vo0, 3)} V', f'{g(1.25 * (1 + 1488 / 240), 3)} V', f'{g(1.25 * (1 + R2 / R1) - 50e-6 * R2, 3)} V'],
  S(f'VOUT = 1,25(1 + R2/R1) + IADJ·R2 = 1,25 × 7,25 + 50 μA × 1,5 kΩ = 9,0625 + 0,075 = 9,1375 ≈ {g(vo, 3)} V (bỏ IADJ cho 9,06 V).', f'VOUT = 1.25(1 + R2/R1) + IADJ·R2 = 1.25 × 7.25 + 50 μA × 1.5 kΩ = 9.0625 + 0.075 = 9.1375 ≈ {g(vo, 3)} V (ignoring IADJ gives 9.06 V).'), SRC8, 'm08-ic-regulators')
Vin, Vout, IL, Ta, thJC, thCS, thSA = 12.0, 5.0, 0.6, 40.0, 5.0, 1.0, 10.0; PD = (Vin - Vout) * IL; Tj = Ta + PD * (thJC + thCS + thSA)
H(M, IC8, S('IC 7805 nhận VIN = 12 V, cấp IL = 0,6 A. Nhiệt trở: θJC = 5 °C/W, θCS = 1 °C/W, tản nhiệt θSA = 10 °C/W, nhiệt độ môi trường 40 °C. Nhiệt độ mối nối xấp xỉ', 'A 7805 IC takes VIN = 12 V and supplies IL = 0.6 A. Thermal resistances: θJC = 5 °C/W, θCS = 1 °C/W, heat sink θSA = 10 °C/W, ambient 40 °C. The junction temperature is about'),
  f'{g(Tj, 4)} °C', [f'{g(Ta + (Vin * IL) * (thJC + thCS + thSA), 4)} °C', f'{g(Ta + PD * thJC, 4)} °C', f'{g(Ta + PD * (thJC + thSA), 4)} °C'],
  S(f'PD = (12 − 5) × 0,6 = {g(PD, 3)} W; Tj = Ta + PD·(θJC + θCS + θSA) = 40 + 4,2 × 16 = {g(Tj, 4)} °C (dùng VIN·IL = 7,2 W là sai: chỉ phần (VIN − VOUT)·IL toả nhiệt trong IC; bỏ θCS cho 103 °C).', f'PD = (12 − 5) × 0.6 = {g(PD, 3)} W; Tj = Ta + PD·(θJC + θCS + θSA) = 40 + 4.2 × 16 = {g(Tj, 4)} °C (using VIN·IL = 7.2 W is wrong: only (VIN − VOUT)·IL heats the IC; omitting θCS gives 103 °C).'), S('Floyd 9e §17–4', 'Floyd 9e §17–4'), 'm08-heat')
IL, R4 = 1.2, 0.7 / 1.2; P4 = IL ** 2 * R4
H(M, SE8, S('Bộ ổn áp nối tiếp cần giới hạn dòng ở IL(max) = 1,2 A bằng điện trở cảm biến R4 (IL(max) = 0,7 V/R4). Công suất tiêu tán tối thiểu mà R4 phải chịu là', 'A series regulator must limit the current to IL(max) = 1.2 A with a sense resistor R4 (IL(max) = 0.7 V/R4). The minimum power rating R4 must handle is'),
  f'{g(P4, 3)} W', [f'{g(0.7 ** 2 / IL, 3)} W', f'{g(IL ** 2 / R4, 3)} W', f'{g(0.7 * IL * 2, 3)} W'],
  S(f'R4 = 0,7/1,2 = {g(R4, 3)} Ω; P = I²R = 1,2² × {g(R4, 3)} = {g(P4, 3)} W (= 0,7 V × 1,2 A); chọn điện trở ≥ 1 W.', f'R4 = 0.7/1.2 = {g(R4, 3)} Ω; P = I²R = 1.2² × {g(R4, 3)} = {g(P4, 3)} W (= 0.7 V × 1.2 A); choose a resistor of at least 1 W.'), S('Floyd 9e §17–2', 'Floyd 9e §17–2'), 'm08-current-limit')
Vin, Vout, ILmax, IZmin = 20.0, 12.0, 0.100, 0.010; Rs = (Vin - Vout) / (ILmax + IZmin); Iz0 = (Vin - Vout) / Rs; Pz = Iz0 * Vout
H(M, SH8, S('Ổn áp song song VIN = 20 V, VOUT = 12 V, tải 0–100 mA, dòng tối thiểu qua phần tử shunt 10 mA. Điện trở nối tiếp R1 lớn nhất và công suất cực đại ở phần tử shunt (khi hở tải) là', 'A shunt regulator with VIN = 20 V and VOUT = 12 V serves a 0–100 mA load and needs at least 10 mA through the shunt element. The largest series resistor R1 and the maximum shunt-element power (load open) are'),
  S(f'{g(Rs, 3)} Ω; {g(Pz, 3)} W', f'{g(Rs, 3)} Ω; {g(Pz, 3)} W'), [S(f'{g(8 / 0.1, 3)} Ω; {g(0.1 * 12, 3)} W', f'{g(8 / 0.1, 3)} Ω; {g(0.1 * 12, 3)} W'), S(f'{g(Rs, 3)} Ω; {g(Iz0 * Vin, 3)} W', f'{g(Rs, 3)} Ω; {g(Iz0 * Vin, 3)} W'), S(f'{g(12 / 0.11, 3)} Ω; {g(Pz, 3)} W', f'{g(12 / 0.11, 3)} Ω; {g(Pz, 3)} W')],
  S(f'R1 = (VIN − VOUT)/(IL(max) + IZ(min)) = 8/0,11 = {g(Rs, 3)} Ω; khi hở tải toàn bộ {g(Iz0 * 1e3, 3)} mA qua phần tử shunt: P = 12 V × {g(Iz0 * 1e3, 3)} mA = {g(Pz, 3)} W.', f'R1 = (VIN − VOUT)/(IL(max) + IZ(min)) = 8/0.11 = {g(Rs, 3)} Ω; with the load open all {g(Iz0 * 1e3, 3)} mA flows in the shunt element: P = 12 V × {g(Iz0 * 1e3, 3)} mA = {g(Pz, 3)} W.'), S('Floyd 9e §17–3', 'Floyd 9e §17–3'), 'm08-shunt')
Vin, Vout, IL, eta = 24.0, 5.0, 2.0, 0.88; Pin = Vout * IL / eta; Iin = Pin / Vin; etalin = Vout / Vin; PDlin = (Vin - Vout) * IL
H(M, SW8, S('Bộ ổn áp xung giảm áp VIN = 24 V, VOUT = 5 V, IL = 2 A, hiệu suất 88 %. Dòng lấy từ nguồn vào và công suất tiêu tán của bộ ổn áp tuyến tính cùng tải là', 'A step-down switching regulator with VIN = 24 V, VOUT = 5 V, IL = 2 A and 88 % efficiency. The current drawn from the input and the dissipation of a linear regulator doing the same job are'),
  S(f'{g(Iin * 1e3, 3)} mA; {g(PDlin, 3)} W', f'{g(Iin * 1e3, 3)} mA; {g(PDlin, 3)} W'), [S(f'{g(IL * 1e3, 3)} mA; {g(PDlin, 3)} W', f'{g(IL * 1e3, 3)} mA; {g(PDlin, 3)} W'), S(f'{g(Pin / Vout * 1e3, 3)} mA; {g(Vin * IL, 3)} W', f'{g(Pin / Vout * 1e3, 3)} mA; {g(Vin * IL, 3)} W'), S(f'{g(Iin * 1e3, 3)} mA; {g(Vout * IL, 3)} W', f'{g(Iin * 1e3, 3)} mA; {g(Vout * IL, 3)} W')],
  S(f'Pout = 5 × 2 = 10 W; Pin = 10/0,88 = {g(Pin, 4)} W; Iin = Pin/24 = {g(Iin * 1e3, 3)} mA. Bộ tuyến tính: η ≈ 5/24 = {g(100 * etalin, 3)} % và tiêu tán (24 − 5) × 2 = {g(PDlin, 3)} W.', f'Pout = 5 × 2 = 10 W; Pin = 10/0.88 = {g(Pin, 4)} W; Iin = Pin/24 = {g(Iin * 1e3, 3)} mA. Linear regulator: η ≈ 5/24 = {g(100 * etalin, 3)} % and dissipation (24 − 5) × 2 = {g(PDlin, 3)} W.'), S('Floyd 9e §17–5', 'Floyd 9e §17–5'), 'm08-switching')
Vin, Vout = 5.0, 15.0; D = 1 - Vin / Vout; close(Vin / (1 - D), Vout)
H(M, SW8, S('Bộ ổn áp xung tăng áp (boost) lý tưởng có VOUT = VIN/(1 − D). Để tạo 15 V từ 5 V cần chu kỳ làm việc D bằng', 'An ideal step-up (boost) switching regulator has VOUT = VIN/(1 − D). To make 15 V from 5 V the duty cycle D must be'),
  f'{g(D, 3)}', [f'{g(Vin / Vout, 3)}', f'{g(Vout / (Vin + Vout), 3)}', f'{g(Vin / (Vin + Vout), 3)}'],
  S(f'D = 1 − VIN/VOUT = 1 − 5/15 = {g(D, 3)} (công thức giảm áp VOUT = D·VIN sẽ cho 0,333 sai).', f'D = 1 − VIN/VOUT = 1 − 5/15 = {g(D, 3)} (the step-down formula VOUT = D·VIN would give 0.333, which is wrong).'), S('Floyd 9e §17–5', 'Floyd 9e §17–5'), 'm08-switching')
v1, v2, d1, d2 = 12.00, 12.05, 15.0, 18.0; lr = ((v2 - v1) / v1 * 100) / (d2 - d1)
H(M, RB8, S('Bộ ổn áp cho 12,00 V khi VIN = 15 V và 12,05 V khi VIN = 18 V. Line regulation theo %/V là', 'A regulator gives 12.00 V at VIN = 15 V and 12.05 V at VIN = 18 V. The line regulation in %/V is'),
  f'{g(lr, 3)} %/V', [f'{g((v2 - v1) / (d2 - d1) * 100, 3)} %/V', f'{g((v2 - v1) / v1 * 100, 3)} %/V', f'{g((v2 - v1) / d2 * 100, 3)} %/V'],
  S(f'(ΔVOUT/VOUT)·100 %/ΔVIN = (0,05/12 × 100 %)/3 V = {g(lr, 3)} %/V (Floyd Eq. 17–2).', f'(ΔVOUT/VOUT)·100 %/ΔVIN = (0.05/12 × 100 %)/3 V = {g(lr, 3)} %/V (Floyd Eq. 17–2).'), SRC8, 'm08-regulation')
Vref, Vtar, R3 = 2.4, 9.0, 10e3; R2n = (Vtar / Vref - 1) * R3; Vreal = (1 + 27e3 / R3) * Vref
H(M, SE8, S('Bộ ổn áp nối tiếp có zener tham chiếu 2,4 V cần ra 9 V: R2/R3 = 9/2,4 − 1 = 2,75. Với R3 = 10 kΩ và điện trở chuẩn R2 = 27 kΩ, điện áp ra thực là', 'A series regulator with a 2.4 V reference must give 9 V: R2/R3 = 9/2.4 − 1 = 2.75. With R3 = 10 kΩ and the standard value R2 = 27 kΩ the actual output is'),
  f'{g(Vreal, 3)} V', [f'{g(Vtar, 3)} V', f'{g((1 + 10 / 27) * Vref, 3)} V', f'{g(27 / 10 * Vref, 3)} V'],
  S(f'VOUT = (1 + R2/R3)·VREF = (1 + 2,7) × 2,4 = {g(Vreal, 3)} V (R2 lý tưởng 27,5 kΩ).', f'VOUT = (1 + R2/R3)·VREF = (1 + 2.7) × 2.4 = {g(Vreal, 3)} V (the ideal R2 is 27.5 kΩ).'), S('Floyd 9e §17–2', 'Floyd 9e §17–2'), 'm08-series')
Vnl, Rout, I = 5.10, 0.1, 2.0; Vfl = Vnl - I * Rout; lrg = (Vnl - Vfl) / Vfl * 100
H(M, RB8, S('Nguồn có VNL = 5,10 V và điện trở ra tương đương 0,1 Ω cấp dòng đầy tải 2 A. Load regulation (VNL − VFL)/VFL là', 'A supply has VNL = 5.10 V and an equivalent output resistance of 0.1 Ω delivering a full-load current of 2 A. The load regulation (VNL − VFL)/VFL is'),
  f'{g(lrg, 3)} %', [f'{g((Vnl - Vfl) / Vnl * 100, 3)} %', f'{g(Rout / (Vnl - Rout) * 100, 3)} %', f'{g(Rout / Vnl * 100, 3)} %'],
  S(f'VFL = 5,10 − 2 × 0,1 = {g(Vfl, 3)} V; (5,10 − 4,90)/4,90 = {g(lrg, 3)} % (mẫu số là VFL; dùng VNL cho 3,92 %; quên nhân dòng 2 A cho 2,0 %).', f'VFL = 5.10 − 2 × 0.1 = {g(Vfl, 3)} V; (5.10 − 4.90)/4.90 = {g(lrg, 3)} % (the denominator is VFL; using VNL gives 3.92 %; forgetting the 2 A gives 2.0 %).'), S('Floyd 9e §17–1', 'Floyd 9e §17–1'), 'm08-regulation')
# ============================================================================================ module 09
M = 'm09'; TR9, ES9, ST9, ML9, PC9 = 'PCB trace physics', 'ESD protection and handling', 'Static electricity and ESD', 'Multilayer boards and vias', 'PCB construction and materials'
SRC9 = S('EASA M04 SM02', 'EASA M04 SM02')
rho, L, w, t = 1.68e-8, 0.20, 0.5e-3, 70e-6; Rt = rho * L / (w * t); I = 3.0; Vd = I * Rt; Pw = I ** 2 * Rt
H(M, TR9, S('Đường dẫn đồng dày 70 μm (2 oz), rộng 0,5 mm, dài 20 cm (ρ = 1,68·10⁻⁸ Ω·m) mang dòng 3 A. Điện áp rơi trên đường dẫn và công suất toả nhiệt là', 'A copper trace 70 μm thick (2 oz), 0.5 mm wide and 20 cm long (ρ = 1.68·10⁻⁸ Ω·m) carries 3 A. The voltage drop along it and the power dissipated are'),
  S(f'{g(Vd * 1e3, 3)} mV; {g(Pw, 3)} W', f'{g(Vd * 1e3, 3)} mV; {g(Pw, 3)} W'), [S(f'{g(Vd * 1e3 * 10, 3)} mV; {g(Pw * 10, 3)} W', f'{g(Vd * 1e3 * 10, 3)} mV; {g(Pw * 10, 3)} W'), S(f'{g(Vd * 1e3 / 2, 3)} mV; {g(Pw / 2, 3)} W', f'{g(Vd * 1e3 / 2, 3)} mV; {g(Pw / 2, 3)} W'), S(f'{g(Vd * 1e3, 3)} mV; {g(I * Rt, 3)} W', f'{g(Vd * 1e3, 3)} mV; {g(I * Rt, 3)} W')],
  S(f'R = ρL/(w·t) = 1,68·10⁻⁸ × 0,2/(0,5·10⁻³ × 70·10⁻⁶) = {g(Rt * 1e3, 3)} mΩ; V = I·R = {g(Vd * 1e3, 3)} mV; P = I²R = {g(Pw, 3)} W (quên bình phương dòng cho {g(I * Rt, 3)} W).', f'R = ρL/(w·t) = 1.68·10⁻⁸ × 0.2/(0.5·10⁻³ × 70·10⁻⁶) = {g(Rt * 1e3, 3)} mΩ; V = I·R = {g(Vd * 1e3, 3)} mV; P = I²R = {g(Pw, 3)} W (forgetting to square the current gives {g(I * Rt, 3)} W).'), S('tự thiết kế (R = ρL/A)', 'self-designed (R = ρL/A)'), 'm09-trace')
Rv, N = 1.2e-3, 5
H(M, ML9, S('Mỗi via có điện trở 1,2 mΩ. Dùng 5 via song song để nối hai lớp thì điện trở tương đương là', 'Each via has a resistance of 1.2 mΩ. Five vias in parallel joining two layers give an equivalent resistance of'),
  f'{g(Rv / N * 1e3, 3)} mΩ', [f'{g(Rv * N * 1e3, 3)} mΩ', f'{g(Rv * 1e3, 3)} mΩ', f'{g(Rv / N / N * 1e3, 3)} mΩ'],
  S('Điện trở song song = R/N = 1,2 mΩ/5 = 0,24 mΩ (thêm via vừa giảm điện trở vừa tăng khả năng tải dòng và dẫn nhiệt).', 'Parallel resistance = R/N = 1.2 mΩ/5 = 0.24 mΩ (more vias lower the resistance and raise the current and heat capacity).'), SRC9, 'm09-vias')
rng = {'bipolar': (380, 7000), 'CMOS': (250, 3000), 'EPROM': (100, 3000)}   # EASA M04 §2.7: bipolar 380-7000 V, CMOS 250-3000 V, EPROM "as low as 100 V" (upper end not given; irrelevant at 300 V)
risk = sorted(k for k, (lo, hi) in rng.items() if lo <= 300); assert risk == ['CMOS', 'EPROM']
H(M, ST9, S('Theo EASA M04, ngưỡng ESD thấp nhất làm hỏng: transistor lưỡng cực 380 V, CMOS 250 V, EPROM 100 V. Một kỹ thuật viên đã tích tĩnh điện 300 V chạm vào bảng mạch. Loại linh kiện nào có nguy cơ hỏng?', 'According to EASA M04 the lowest ESD voltage that can damage a part is 380 V for bipolar transistors, 250 V for CMOS and 100 V for EPROMs. A technician carrying 300 V of static charge touches a circuit board. Which device types are at risk?'),
  S('CMOS và EPROM, không phải transistor lưỡng cực', 'CMOS and EPROM, but not bipolar transistors'), [S('Cả ba loại', 'All three types'), S('Chỉ EPROM', 'Only EPROM'), S('Transistor lưỡng cực và CMOS', 'Bipolar transistors and CMOS')],
  S('So 300 V với ngưỡng thấp nhất: 300 ≥ 250 (CMOS) và 300 ≥ 100 (EPROM) nên cả hai có nguy cơ; 300 < 380 nên transistor lưỡng cực chưa tới ngưỡng. (Khoảng nhạy cảm là khoảng giữa các linh kiện cùng loại, nên "có nguy cơ" chứ chưa chắc hỏng.)', 'Compare 300 V with the lowest thresholds: 300 ≥ 250 (CMOS) and 300 ≥ 100 (EPROM) so both are at risk; 300 < 380 so bipolar transistors are below their threshold. (The ranges span different parts of one family, so "at risk" does not mean "certain to fail".)'), S('EASA M04 SM02 §2.7 (ESD-sensitive items)', 'EASA M04 SM02 §2.7 (ESD-sensitive items)'), 'm09-esd-physics')
Vm, Rs = 230.0, 1e6; Ig = Vm / Rs
H(M, ES9, S('Dây đeo cổ tay nối đất qua điện trở 1 MΩ. Nếu đất bất ngờ mang điện 230 V, dòng tối đa qua người (bỏ qua điện trở cơ thể) xấp xỉ', 'A wrist strap is grounded through 1 MΩ. If the ground suddenly becomes live at 230 V, the maximum current through the person (body resistance neglected) is about'),
  f'{g(Ig * 1e6, 3)} μA', [f'{g(Vm / (Rs / 1e3) * 1e3, 3)} mA', f'{g(Vm / (Rs * 10) * 1e6, 3)} μA', f'{g(Vm / (Rs / 100) * 1e3, 3)} mA'],
  S('I = V/R = 230 V/1 MΩ = 230 μA: điện trở 1 MΩ giữ dòng ở mức thấp, đó là lý do dây đeo không nối thẳng xuống đất.', 'I = V/R = 230 V/1 MΩ = 230 μA: the 1 MΩ resistor keeps the current low, which is why the strap is never wired straight to ground.'), SRC9, 'm09-esd-protection')
# ============================================================================================ module 10
M = 'm10'; SY10, SV10, DC10, ST10, OC10, TD10 = 'Synchro systems', 'Servo loops and components', 'Differential, control synchros and resolvers', 'Stability, hunting and damping', 'Open/closed loop and the follow-up', 'Transducers: LVDT, RVDT, inductive, capacitive'
SRC10 = S('EASA M04 SM03; SERVOMECHANISM (sv)', 'EASA M04 SM03; SERVOMECHANISM (sv)')
Vc, kt, km = 15.0, 0.05, 20.0; w = 0.0
for _ in range(500): e = (Vc - kt * w) / 2; w = km * e
close(w, 100, 1e-6); err = (Vc - kt * w) / 2
H(M, ST10, S('Servo vận tốc: điện áp điều khiển 15 V, hai điện trở cộng bằng nhau (điện áp ở điểm cộng = trung bình của điện áp điều khiển và điện áp máy phát tốc, e = (Vc − Vt)/2), động cơ 20 vòng/phút mỗi volt, máy phát tốc 0,05 V mỗi vòng/phút. Tốc độ cân bằng và điện áp sai số ở điểm cộng là', 'A velocity servo has a 15 V control voltage and two equal summing resistors (the summing-point voltage is the average of the control and tachometer voltages, e = (Vc − Vt)/2), a motor of 20 rpm per volt and a tachometer of 0.05 V per rpm. The steady speed and the error voltage at the summing point are'),
  S(f'{g(w, 3)} vòng/phút; {g(err, 3)} V', f'{g(w, 3)} rpm; {g(err, 3)} V'), [S(f'{g(Vc * km / 2, 3)} vòng/phút; {g(Vc / 2, 3)} V', f'{g(Vc * km / 2, 3)} rpm; {g(Vc / 2, 3)} V'), S(f'{g(Vc * km, 3)} vòng/phút; {g(Vc, 3)} V', f'{g(Vc * km, 3)} rpm; {g(Vc, 3)} V'), S(f'{g(w / 2, 3)} vòng/phút; {g(err, 3)} V', f'{g(w / 2, 3)} rpm; {g(err, 3)} V')],
  S('Cân bằng: ω = km·e và e = (Vc − kt·ω)/2 → ω = 20 × (15 − 0,05ω)/2 = 150 − 0,5ω → ω = 100 vòng/phút; e = (15 − 5)/2 = 5 V (sai số không bằng 0 vì servo vận tốc cần một sai số để quay).', 'Balance: ω = km·e and e = (Vc − kt·ω)/2 → ω = 20 × (15 − 0.05ω)/2 = 150 − 0.5ω → ω = 100 rpm; e = (15 − 5)/2 = 5 V (the error is not zero because a velocity servo needs an error to keep turning).'), SRC10, 'm10-stability')
Vm, Av, k = 2.0, 40.0, 0.15; e = Vm / (Av * k)
H(M, OC10, S('Servomotor cần tối thiểu 2 V để thắng ma sát tĩnh. Máy biến áp điều khiển có độ nhạy 0,15 V/° và bộ khuếch đại có độ lợi 40. Sai số góc tĩnh nhỏ nhất của vòng servo là', 'The servomotor needs at least 2 V to overcome static friction. The control transformer has a sensitivity of 0.15 V/° and the amplifier a gain of 40. The smallest static angular error of the servo loop is'),
  f'{g(e, 3)}°', [f'{g(Vm / k, 3)}°', f'{g(Vm * Av / k, 3)}°', f'{g(Vm / Av, 3)}°'],
  S(f'Điện áp sai số cần thiết = 2 V/40 = 0,05 V; góc = 0,05/0,15 = {g(e, 3)}° (cũng là lý do vùng chết quyết định độ chính xác).', f'The error voltage needed = 2 V/40 = 0.05 V; angle = 0.05/0.15 = {g(e, 3)}° (this is also why the deadband decides the accuracy).'), SRC10, 'm10-control-synchro')
a1, a2 = 135, 60; plain = (a1 + a2) % 360; rev = (-a1 + a2) % 360
# SERVOMECHANISM_sv §3.7-3.9: S2 is the electrical zero, S1 and S3 sit at -/+120 deg; interchanging S1 and S3 reverses the sense of rotation (negates the angle) with no offset
stator = lambda a: np.array([math.cos(math.radians(a + 120)), math.cos(math.radians(a)), math.cos(math.radians(a - 120))])
assert np.allclose(stator(a1)[::-1], stator(-a1)) and plain == 195 and rev == 285
H(M, DC10, S('Synchro vi sai TDX được nối để góc ra = θ₁ + θ₂, với θ₁ = 135° là góc của máy phát TX nối vào stato TDX và θ₂ = 60° là góc cơ khí của rôto TDX. Nếu đổi chỗ hai dây S1 và S3 giữa TX và TDX (θ₂ giữ nguyên), góc ra trở thành', 'A differential synchro TDX is connected so that its output angle = θ₁ + θ₂, where θ₁ = 135° is the angle of the transmitter TX feeding the TDX stator and θ₂ = 60° is the mechanical angle of the TDX rotor. If the S1 and S3 leads between the TX and the TDX are interchanged (θ₂ unchanged), the output angle becomes'),
  S('−75° (= 285°)', '−75° (= 285°)'), [S('75°', '75°'), S(f'{plain}°', f'{plain}°'), S('−195° (= 165°)', '−195° (= 165°)')],
  S('Đổi S1–S3 đảo chiều quay, tức đổi dấu θ₁ (đã kiểm bằng điện áp stato, S2 là điểm không): góc ra = −135° + 60° = −75° = 285°. 75° có độ lớn đúng nhưng sai chiều; 195° là khi chưa đổi dây; −195° là khi đổi dấu cả θ₂.', 'Interchanging S1–S3 reverses the sense of rotation, i.e. it changes the sign of θ₁ (checked with the stator voltages, S2 being the zero): output = −135° + 60° = −75° = 285°. 75° has the right size but the wrong sense; 195° is the unmodified wiring; −195° negates θ₂ as well.'), S('SERVOMECHANISM §3.7–3.9 (đảo S1–S3; TDX cộng/trừ tuỳ cách nối)', 'SERVOMECHANISM §3.7–3.9 (S1–S3 reversal; TDX adds or subtracts by wiring)'), 'm10-control-synchro')
Vr, ratio, th = 115.0, 2.2, 60.0; Vmax = Vr / ratio; vcoil = Vmax * math.cos(math.radians(th))
H(M, SY10, S('Synchro có rôto 115 V qua tỉ số hạ áp 2,2:1 vào mỗi cuộn stato. Khi trục rôto lệch 60° so với trục cuộn stato S1 (điện áp cuộn ∝ cos của góc lệch), điện áp hiệu dụng trên cuộn S1 là', 'A synchro has a 115 V rotor with a 2.2:1 step-down to each stator coil. With the rotor shaft 60° from the axis of stator coil S1 (coil voltage ∝ cos of the offset), the rms voltage on coil S1 is'),
  f'{g(vcoil, 3)} V', [f'{g(Vmax, 3)} V', f'{g(Vmax * math.sin(math.radians(th)), 3)} V', f'{g(Vr * math.cos(math.radians(th)), 3)} V'],
  S(f'Cực đại = 115/2,2 = {g(Vmax, 3)} V (sách SERVOMECHANISM dùng 52 V); V = Vmax·cos 60° = {g(vcoil, 3)} V (cos 60° = 0,5).', f'Maximum = 115/2.2 = {g(Vmax, 3)} V (the SERVOMECHANISM text uses 52 V); V = Vmax·cos 60° = {g(vcoil, 3)} V (cos 60° = 0.5).'), SRC10, 'm10-synchro')
mot, gear = 3000.0, 60.0; out = mot / gear
H(M, SV10, S('Servomotor quay 3000 vòng/phút qua hộp số giảm tốc 60:1 (bỏ qua tổn hao). Tốc độ trục tải và hệ số nhân mô-men là', 'A servomotor turns at 3000 rpm through a 60:1 reduction gear train (losses neglected). The load-shaft speed and the torque multiplication are'),
  S(f'{g(out, 3)} vòng/phút; ×60', f'{g(out, 3)} rpm; ×60'), [S(f'{g(mot * gear, 6)} vòng/phút; ×60', f'{g(mot * gear, 6)} rpm; ×60'), S(f'{g(out, 3)} vòng/phút; ÷60', f'{g(out, 3)} rpm; ÷60'), S(f'{g(out, 3)} vòng/phút; ×1', f'{g(out, 3)} rpm; ×1')],
  S('Giảm tốc 60:1 chia tốc độ cho 60 (3000/60 = 50 vòng/phút) và nhân mô-men với 60 (công suất không đổi nếu bỏ qua tổn hao): đó là vai trò của hộp số trong servo.', 'A 60:1 reduction divides the speed by 60 (3000/60 = 50 rpm) and multiplies the torque by 60 (power unchanged if losses are neglected): this is the gear train\'s job in a servo.'), SRC10, 'm10-servo-loop')
C0, eps_f, h = 100.0, 2.1, 0.6; Cx = C0 * ((1 - h) + eps_f * h); close(Cx, C0 * (1 + (eps_f - 1) * h), 1e-12)
H(M, TD10, S('Đầu dò dung kháng trong bình nhiên liệu gồm hai bản trụ đồng tâm cố định, điện dung khi rỗng C0 = 100 pF, hằng số điện môi nhiên liệu 2,1 (không khí 1,0). Khi bình đầy 60 % chiều cao, điện dung xấp xỉ', 'A fuel-tank capacitance probe has two fixed concentric cylindrical plates, an empty capacitance C0 = 100 pF, and a fuel dielectric constant of 2.1 (air 1.0). With the tank 60 % full by height the capacitance is about'),
  f'{g(Cx, 3)} pF', [f'{g(C0 * eps_f, 3)} pF', f'{g(C0 * (1 + h), 3)} pF', f'{g(C0 * eps_f * h, 3)} pF'],
  S(f'Phần ngập nhiên liệu và phần còn không khí là hai tụ song song: C = C0·[(1 − h) + εr·h] = 100 × (0,4 + 2,1 × 0,6) = {g(Cx, 3)} pF (diện tích và khoảng cách bản không đổi, chỉ điện môi đổi).', f'The fuel-covered and the air-filled parts are two capacitors in parallel: C = C0·[(1 − h) + εr·h] = 100 × (0.4 + 2.1 × 0.6) = {g(Cx, 3)} pF (plate area and spacing are fixed, only the dielectric changes).'), SRC10, 'm10-lvdt')
# ============================================================================================ write
if __name__ == '__main__' or True:
    tot = 0
    for mod, items in sorted(OUT.items()):
        json.dump(items, open(os.path.join(ROOT, 'data', 'qsrc', f'{mod}_zhard.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0); tot += len(items)
    print({m: len(v) for m, v in sorted(OUT.items())}, 'total', tot)
