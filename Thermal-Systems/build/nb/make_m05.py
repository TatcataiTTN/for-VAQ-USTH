"""Build and execute the m05 notebooks (VI and EN).  Run: .venv/bin/python -I build/nb/make_m05.py
Each method section = markdown (question it answers) -> code -> markdown interpreting the REAL output (numbers in the interpretation are computed here with route A
(build/gen/m05_common.py) and then CHECKED against the executed output text: the build fails if they do not appear).
The notebook is self-contained: the tables it uses (A-32 printed rows, A-17 air h and Pr, A-20 CO2 h; read from the Appendix page images, data/props/*.json) are embedded in the first code cell.
The independent routes need numpy and scipy (the executed outputs here come from an environment that has them)."""
import os, sys, math, subprocess, json
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
from m05_common import *
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
D = lambda n: json.load(open(os.path.join(ROOT, 'data', 'props', n + '.json'), encoding='utf-8'))
A32 = [r for r in D('A32')['rows'] if r[0] not in (None, 0)]
A17 = [[r[0], r[1], r[2]] for r in D('A17')['rows'] if 250 <= r[0] <= 800]
A20 = [[r[0], r[1]] for r in D('A20')['rows'] if 300 <= r[0] <= 1400]
f = lambda x, nd=2: f'{x:.{nd}f}'

PRELUDE = '''import math, numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar
# ---- tables read from the Appendix 1 page images (data/props/*.json), embedded so that the notebook is self-contained
A32 = np.array(%s)     # A-32 (k = 1.4) rows: Ma, Ma*, A/A*, P/P0, rho/rho0, T/T0
A17 = np.array(%s)     # A-17 air: T [K], h [kJ/kg], Pr
A20 = np.array(%s)     # A-20 CO2: T [K], h [kJ/kmol]
# ---- route A: closed forms of the slide equations (SI: P kPa, R kJ/(kg K), V m/s, A m2, mdot kg/s)
def cp_of(k, R): return k * R / (k - 1.0)
def T0_of(T, V, cp): return T + V * V / (2000.0 * cp)                         # (1)/(7): V^2/2 in J/kg -> kJ/kg
def P0_of(P, T, T0, k): return P * (T0 / T) ** (k / (k - 1.0))               # (2)
def csound(k, R, T): return math.sqrt(k * R * 1000.0 * T)
def TT0(Ma, k): return 1.0 / (1.0 + (k - 1.0) / 2.0 * Ma * Ma)               # (9)
def PP0(Ma, k): return TT0(Ma, k) ** (k / (k - 1.0))                         # (10)
def AAs(Ma, k): return (1.0 / Ma) * ((2.0 / (k + 1.0)) * (1.0 + (k - 1.0) / 2.0 * Ma * Ma)) ** ((k + 1.0) / (2.0 * (k - 1.0)))   # (17)
def crit(k): return dict(TT=2.0 / (k + 1.0), PP=(2.0 / (k + 1.0)) ** (k / (k - 1.0)))                                      # (12),(13)
def Ma_of_PP(pr, k): return math.sqrt(2.0 / (k - 1.0) * (pr ** (-(k - 1.0) / k) - 1.0))
def mdot_choked(A, P0, T0, k, R): return A * (P0 * 1000.0) * math.sqrt(k / (R * 1000.0 * T0)) * (2.0 / (k + 1.0)) ** ((k + 1.0) / (2.0 * (k - 1.0)))   # (16) with P0 in Pa, R in J/(kg K)
# ---- route B: numerical descriptions that do not use (9)-(17)
def flux_max(k):
    """x* = T/T0 maximising the mass flux rho V ~ x^(1/(k-1)) sqrt(1-x) along the isentrope (energy equation V = sqrt(2 cp (T0 - T)))."""
    r = minimize_scalar(lambda x: -(x ** (1.0 / (k - 1.0)) * math.sqrt(1.0 - x)), bounds=(1e-6, 1 - 1e-9), method='bounded', options=dict(xatol=1e-13)); return r.x, -r.fun
def isentrope_T(T, P, Pnew, k):
    s = solve_ivp(lambda x, y: [(k - 1.0) / k], [0.0, math.log(Pnew / P)], [math.log(T)], rtol=1e-11, atol=1e-13); return math.exp(s.y[0, -1])
def c_num(T, k, R):
    """speed of sound as (dP/d rho)_s by central difference on the isentrope P = C rho^k (not sqrt(kRT))."""
    P0_ = 1.0e5; rho = P0_ / (R * 1000.0 * T); C = P0_ / rho ** k; h = 1e-5 * rho; return math.sqrt((C * (rho + h) ** k - C * (rho - h) ** k) / (2 * h))
def x_of_Ma(Ma, k, R=0.287):
    cp = cp_of(k, R); return brentq(lambda T: Ma * c_num(T, k, R) - math.sqrt(max(2000.0 * cp * (1000.0 - T), 0.0)), 1.0, 1000.0 - 1e-9, xtol=1e-12) / 1000.0
''' % (json.dumps(A32), json.dumps(A17), json.dumps(A20))

def sections(lang):
    vi = lang == 'vi'
    tr = lambda a, b: a if vi else b
    dv = lambda s: s.replace('.', ',') if vi else s
    S = []      # (title, question_md, code, interpretation_md, [strings that must appear in stdout])
    k, R, cp = 1.4, 0.287, 1.005
    T01 = T0_of(255.7, 250.0, cp); P01 = P0_of(54.05, 255.7, T01, k); T02 = T01 * 8 ** ((k - 1) / k); w13 = cp * (T02 - T01)
    # ---- 1 stagnation
    S.append((tr('Tính chất hãm: slide tr.10–13 (Cengel Ví dụ 17–1)', 'Stagnation properties: slides p.10–13 (Cengel Example 17–1)'),
              tr('**Câu hỏi:** không khí 250 m/s ở 5000 m (54,05 kPa; 255,7 K) bị hãm đẳng entropi trong diffuser rồi nén với tỉ số hãm 8: T₀₁, P₀₁, T₀₂ và công nén là bao nhiêu? Công thức đóng so với tích phân số dT = −V dV/c_p và w = ∫RT d ln P.', '**Question:** air at 250 m/s at 5000 m (54.05 kPa; 255.7 K) is brought to rest isentropically in the diffuser and then compressed by a stagnation ratio of 8: what are T₀₁, P₀₁, T₀₂ and the compressor work? Closed form against numerical integration of dT = −V dV/c_p and w = ∫RT d ln P.'),
              PRELUDE + '''T, P, V, cp, k, R = 255.7, 54.05, 250.0, 1.005, 1.4, 0.287
T01 = T0_of(T, V, cp); P01 = P0_of(P, T, T01, k); T02 = T01 * 8 ** ((k - 1) / k); w = cp * (T02 - T01)
print(f"route A: T01 = {T01:.2f} K; P01 = {P01:.2f} kPa; T02 = {T02:.1f} K; w = {w:.1f} kJ/kg   (slide: 286.8; 80.77; 519.5; 233.9)")
s = solve_ivp(lambda v, y: [-v / (1000.0 * cp)], [V, 0.0], [T], rtol=1e-11, atol=1e-11); T01b = s.y[0, -1]
P01b = P * math.exp(quad(lambda t: (k / (k - 1)) / t, T, T01b)[0])                       # ds = 0: d ln P = k/(k-1) d ln T
wb = abs(quad(lambda x: R * isentrope_T(T01b, 1.0, math.exp(x), k), 0.0, math.log(8.0))[0])
print(f"route B: T01 = {T01b:.2f} K; P01 = {P01b:.2f} kPa; w = {wb:.1f} kJ/kg  (cp = kR/(k-1) = {cp_of(k, R):.4f} instead of 1.005: {100 * (wb / w - 1):+.2f} %)")
print("ram rise:", f"dT = {T01 - T:.1f} K, dP = {P01 - P:.2f} kPa")
for Vp in (1, 10, 100, 1000): print(f"probe in air at 300 K, V = {Vp:4d} m/s reads {T0_of(300.0, Vp, cp):.2f} K")''',
              tr(f'**Đọc kết quả:** T₀₁ = {dv(f(T01,2))} K, P₀₁ = {dv(f(P01,2))} kPa, T₀₂ = {dv(f(T02,1))} K, công {dv(f(w13,1))} kJ/kg khớp slide (286,8; 80,77; 519,5; 233,9). Đường B (tích phân số) cho cùng T₀₁, P₀₁; công chênh {dv(f((cp_of(1.4,0.287)/1.005-1)*100,2))} % vì kR/(k−1) = 1,0045 chứ không phải 1,005. Hãm từ 250 m/s làm tăng {dv(f(T01-255.7,1))} K và {dv(f(P01-54.05,2))} kPa. Đầu dò ở 100 m/s chỉ 304,98 K, ở 1000 m/s chỉ 797,51 K (slide tr.14 không in đáp án; c_p không đổi là xấp xỉ thô ở 1000 m/s).', f'**Reading the output:** T₀₁ = {f(T01,2)} K, P₀₁ = {f(P01,2)} kPa, T₀₂ = {f(T02,1)} K, work {f(w13,1)} kJ/kg agree with the slide (286.8; 80.77; 519.5; 233.9). Route B (numerical integration) gives the same T₀₁, P₀₁; the work differs by {f((cp_of(1.4,0.287)/1.005-1)*100,2)} % because kR/(k−1) = 1.0045, not 1.005. Stopping from 250 m/s raises T by {f(T01-255.7,1)} K and P by {f(P01-54.05,2)} kPa. A probe at 100 m/s reads 304.98 K, at 1000 m/s 797.51 K (slide p.14 prints no answer; constant c_p is a rough approximation at 1000 m/s).'),
              [f'T01 = {f(T01,2)} K', f'P01 = {f(P01,2)} kPa', f'w = {f(w13,1)} kJ/kg', 'V = 1000 m/s reads 797.51 K']))
    # ---- 2 compressor 17-8
    T01c = 300.15; T02c = T01c * 9 ** ((k - 1) / k); P15 = 0.02 * cp * (T02c - T01c); w16 = cp_of(1.33, 0.287) * 1023.15 * (1 - 0.1 ** (0.33 / 1.33))
    S.append((tr('Công máy nén đẳng entropi: slide tr.15 (Cengel 17–8, đáp án in 5,27 kW) và A-17', 'Isentropic compressor power: slide p.15 (Cengel 17–8, printed 5.27 kW) and A-17'),
              tr('**Câu hỏi:** không khí vào máy nén ở T₀₁ = 27 °C, tỉ số áp suất hãm 9, 0,02 kg/s: công suất là bao nhiêu và c_p biến thiên (bảng A-17, P_r) thay đổi nó bao nhiêu? Đây là bài có đáp án in dùng để thử phương pháp trước khi áp dụng cho bài không đáp án (tr.16).', '**Question:** air enters a compressor at T₀₁ = 27 °C with a stagnation pressure ratio of 9 at 0.02 kg/s: what is the power and how much does variable c_p (Table A-17, P_r) change it? This is the problem with a printed answer used to test the method before applying it to a problem without one (p.16).'),
              PRELUDE + '''T01 = 300.15; pr = 9.0; cp, k, R, mdot = 1.005, 1.4, 0.287, 0.02
T02 = T01 * pr ** ((k - 1) / k); P_A = mdot * cp * (T02 - T01)
w_ds = abs(quad(lambda x: R * isentrope_T(T01, 1.0, math.exp(x), k), 0.0, math.log(pr))[0]); P_B = mdot * w_ds
h = lambda T: float(np.interp(T, A17[:, 0], A17[:, 1])); Pr = lambda T: float(np.interp(T, A17[:, 0], A17[:, 2]))
Pr2 = Pr(T01) * pr; T02v = float(np.interp(Pr2, A17[:, 2], A17[:, 0])); P_C = mdot * (h(T02v) - h(T01))
print(f"A closed form : T02 = {T02:.1f} K; power = {P_A:.3f} kW")
print(f"B integral    : power = {P_B:.3f} kW")
print(f"C Table A-17  : Pr(T01) = {Pr(T01):.3f} -> Pr2 = {Pr2:.3f} -> T02 = {T02v:.1f} K; power = {P_C:.3f} kW  (printed answer 5.27 kW)")
w16 = cp_of(1.33, 0.287) * 1023.15 * (1 - 0.1 ** (0.33 / 1.33)); print(f"slide p.16 (turbine, k = 1.33): w = {w16:.1f} kJ/kg")''',
              tr(f'**Đọc kết quả:** đường A cho {dv(f(P15,3))} kW và đường B cho {dv(f(0.02*cp_of(1.4,0.287)*(T02c-T01c),3))} kW (khác 0,05 % vì c_p); đường C (A-17) cho 5,258 kW: cả ba khớp đáp án in 5,27 kW trong 0,3 %. Phương pháp (A) vì thế đáng tin cho tr.14 và tr.16: bài tr.16 cho {dv(f(w16,1))} kJ/kg (không có đáp án in).', f'**Reading the output:** route A gives {f(P15,3)} kW and route B {f(0.02*cp_of(1.4,0.287)*(T02c-T01c),3)} kW (0.05 % apart because of c_p); route C (A-17) gives 5.258 kW: all three agree with the printed 5.27 kW within 0.3 %. Method (A) is therefore trustworthy for p.14 and p.16: the p.16 problem gives {f(w16,1)} kJ/kg (no printed answer).'),
              [f'power = {f(P15,3)} kW', 'power = 5.258 kW', f'w = {f(w16,1)} kJ/kg']))
    # ---- 3 CO2 duct
    kC, RC = 1.289, 0.1889
    def co2(P):
        T = 473.0 * (P / 1400.0) ** ((kC - 1) / kC); V = math.sqrt(2000.0 * cp_of(kC, RC) * (473.0 - T)); rho = P / (RC * T); return T, V, rho, csound(kC, RC, T), (3.0 / (rho * V) * 1e4 if V > 0 else float('inf')), V / csound(kC, RC, T)
    r1200, r767 = co2(1200.0), co2(767.0)
    S.append((tr('Ống CO₂: slide tr.18–24 (Cengel Ví dụ 17–3)', 'The CO₂ duct: slides p.18–24 (Cengel Example 17–3)'),
              tr('**Câu hỏi:** CO₂ 3 kg/s, T₀ = 473 K, P₀ = 1400 kPa giãn nở đẳng entropi tới 200 kPa. Bảng T, V, ρ, c, A, Ma tại mỗi bước giảm 200 kPa tính bằng công thức và bằng tích phân số có khớp bảng slide tr.22 không?', '**Question:** CO₂ at 3 kg/s, T₀ = 473 K, P₀ = 1400 kPa expands isentropically to 200 kPa. Do the table of T, V, ρ, c, A, Ma at each 200 kPa step computed by formula and by numerical integration match the slide table on p.22?'),
              PRELUDE + '''k, R, T0, P0, mdot = 1.289, 0.1889, 473.0, 1400.0, 3.0
slide = {1200: (457, 164.5, 13.9, 333.6, 13.1, 0.493), 1000: (439, 240.7, 12.1, 326.9, 10.3, 0.736), 800: (417, 306.6, 10.1, 318.8, 9.64, 0.962), 767: (413, 317.2, 9.82, 317.2, 9.63, 1.000),
         600: (391, 371.4, 8.12, 308.7, 10.0, 1.203), 400: (357, 441.9, 5.93, 295.0, 11.5, 1.498), 200: (306, 530.9, 3.46, 272.9, 16.3, 1.946)}
cpkR = cp_of(k, R); print(f"cp = kR/(k-1) = {cpkR:.4f} (the slide quotes 0.846)")
print(" P     T      V      rho     c      A(cm2)  Ma     | slide T, V, A, Ma")
for P in (1200, 1000, 800, 767, 600, 400, 200):
    T = T0 * (P / P0) ** ((k - 1) / k); V = math.sqrt(2000.0 * cpkR * (T0 - T)); rho = P / (R * T); c = csound(k, R, T); A = mdot / (rho * V) * 1e4
    Tb = isentrope_T(T0, P0, float(P), k); Vb = math.sqrt(2000.0 * quad(lambda t: cpkR, Tb, T0)[0]); cb = c_num(Tb, k, R)           # route B
    assert abs(Tb - T) < 1e-6 and abs(Vb / V - 1) < 1e-9 and abs(cb / c - 1) < 1e-6
    s = slide[P]; print(f"{P:5d} {T:6.1f} {V:7.1f} {rho:7.2f} {c:6.1f} {A:7.2f} {V / c:6.3f} | {s[0]} {s[1]} {s[4]} {s[5]}")
print("slide with cp = 0.846 at 1200 kPa: V =", round(math.sqrt(2000 * 0.846 * (T0 - T0 * (1200 / P0) ** ((k - 1) / k))), 1), "m/s")''',
              tr(f'**Đọc kết quả:** tại 1200 kPa: T = {dv(f(r1200[0],1))} K, V = {dv(f(r1200[1],1))} m/s, ρ = {dv(f(r1200[2],2))} kg/m³, A = {dv(f(r1200[4],1))} cm², Ma = {dv(f(r1200[5],3))}; tại cổ họng 767 kPa: A = {dv(f(r767[4],2))} cm² (cực tiểu) và Ma = {dv(f(r767[5],3))}. Bảng slide khớp c_p = kR/(k−1) = 0,8425 (V lệch ≤ 0,3 % so với 0,846), nên đã dùng 0,8425; c_p = 0,846 cho V = 164,9 m/s ở 1200 kPa (slide in 164,5). Đường B trùng đường A (khẳng định bằng assert).', f'**Reading the output:** at 1200 kPa: T = {f(r1200[0],1)} K, V = {f(r1200[1],1)} m/s, ρ = {f(r1200[2],2)} kg/m³, A = {f(r1200[4],1)} cm², Ma = {f(r1200[5],3)}; at the throat 767 kPa: A = {f(r767[4],2)} cm² (the minimum) and Ma = {f(r767[5],3)}. The slide table matches c_p = kR/(k−1) = 0.8425 (V within 0.3 % of using 0.846), so 0.8425 was used; c_p = 0.846 gives V = 164.9 m/s at 1200 kPa (slide prints 164.5). Route B equals route A (asserted).'),
              ['cp = kR/(k-1) = 0.8425', 'slide with cp = 0.846 at 1200 kPa: V = 164.9']))
    # ---- 4 critical ratios by flux maximum
    S.append((tr('Tính chất tới hạn: cực đại số của lưu lượng ρV so với công thức (12)–(14)', 'Critical properties: numerical maximum of the flux ρV against formulas (12)–(14)'),
              tr('**Câu hỏi:** công thức (13) P*/P₀ = (2/(k+1))^(k/(k−1)) có đúng là vị trí cực đại của khối lượng riêng nhân vận tốc ρV (lưu lượng trên đơn vị diện tích) dọc đường đẳng entropi không? Thử cho không khí, CO₂ (slide tr.36–38) và sản phẩm cháy (tr.16).', '**Question:** is formula (13) P*/P₀ = (2/(k+1))^(k/(k−1)) really where the flux ρV (mass flow per unit area) is maximum along the isentrope? Test for air, CO₂ (slides p.36–38) and combustion products (p.16).'),
              PRELUDE + '''for name, k in (('air', 1.4), ('CO2 (slide p.37)', 1.289), ('products k = 1.33', 1.33), ('helium', 1.667)):
    xs, fs = flux_max(k); c = crit(k); Pstar = math.exp(k / (k - 1.0) * math.log(xs))
    print(f"{name:20s}: numerical T*/T0 = {xs:.5f} (eq.12 {c['TT']:.5f}); numerical P*/P0 = {Pstar:.5f} (eq.13 {c['PP']:.5f}); Ma at the maximum = {math.sqrt(2/(k-1)*(1/xs-1)):.5f}")
print("slide Ex 17-4: T* =", round(crit(1.289)['TT'] * 473.0, 1), "K; P* =", round(crit(1.289)['PP'] * 1400.0, 1), "kPa")''',
              tr(f'**Đọc kết quả:** cực đại số của ρV rơi đúng tại T*/T₀ = 2/(k+1) và P*/P₀ của (13) cho cả bốn loại khí, và Ma tại cực đại bằng 1,00000: tức Ma = 1 chính là điều kiện làm lưu lượng cực đại (slide tr.45). Với CO₂: T* = {dv(f(crit(1.289)["TT"]*473,1))} K, P* = {dv(f(crit(1.289)["PP"]*1400,1))} kPa (slide 413 K; 767 kPa).', f'**Reading the output:** the numerical maximum of ρV falls exactly at T*/T₀ = 2/(k+1) and at the P*/P₀ of (13) for all four gases, and Ma at the maximum is 1.00000: i.e. Ma = 1 is the condition that makes the flow a maximum (slide p.45). For CO₂: T* = {f(crit(1.289)["TT"]*473,1)} K, P* = {f(crit(1.289)["PP"]*1400,1)} kPa (slide 413 K; 767 kPa).'),
              ['Ma at the maximum = 1.00000', f'T* = {f(crit(1.289)["TT"]*473,1)} K']))
    # ---- 5 converging nozzle Ex 17-5
    T0i = T0_of(873.0, 150.0, cp); P0i = P0_of(1000.0, 873.0, T0i, k); na = conv_nozzle(700.0, P0i, T0i, k, R, 50e-4); nb = conv_nozzle(400.0, P0i, T0i, k, R, 50e-4)
    lit = 50e-4 * 1045.0 * math.sqrt(1.4 / (0.287 * 884.0)) * (2.0 / 2.4) ** (2.4 / 0.8); mok = mdot_choked(50e-4, 1045.0, 884.0, k, R)
    S.append((tr('Vòi hội tụ và áp suất ngược: slide tr.50–55 (Cengel Ví dụ 17–5) và bẫy √1000', 'Converging nozzle and back pressure: slides p.50–55 (Cengel Example 17–5) and the √1000 trap'),
              tr('**Câu hỏi:** không khí 1 MPa, 600 °C, 150 m/s vào vòi hội tụ A_t = 50 cm². Lưu lượng khối với P_b = 0,7 MPa và 0,4 MPa là bao nhiêu? Tính bằng (15)/(16) và bằng năng lượng + đẳng entropi (không dùng (15), (16)); thử công thức (16) nguyên văn bằng kPa và kJ/(kg·K) như slide tr.55.', '**Question:** air at 1 MPa, 600 °C, 150 m/s enters a converging nozzle A_t = 50 cm². What is the mass flow for P_b = 0.7 MPa and 0.4 MPa? Compute it with (15)/(16) and with energy + isentropy (without (15), (16)); try formula (16) literally with kPa and kJ/(kg·K) as on slide p.55.'),
              PRELUDE + '''k, R, cp, A = 1.4, 0.287, 1.005, 50e-4
T0 = 873.0 + 150.0 ** 2 / (2000.0 * cp); P0 = 1000.0 * (T0 / 873.0) ** 3.5; Pc = P0 * crit(k)['PP']
print(f"T0 = {T0:.1f} K; P0 = {P0:.1f} kPa; P* = {Pc:.1f} kPa")
xs, fs = flux_max(k)
for Pb in (700.0, 400.0):
    Pe = max(Pb, P0 * math.exp(k / (k - 1) * math.log(xs)))                                  # route B: exit pressure = max(Pb, pressure at flux maximum)
    Te = T0 * (Pe / P0) ** ((k - 1) / k); V = math.sqrt(2000.0 * cp_of(k, R) * (T0 - Te)); mB = Pe / (R * Te) * V * A
    Ma = Ma_of_PP(min(Pe, P0) / P0, k); mA = mdot_choked(A, P0, T0, k, R) if Pb < Pc else (Pe / (R * T0 * TT0(Ma, k))) * A * Ma * csound(k, R, T0 * TT0(Ma, k))
    print(f"Pb = {Pb:5.0f} kPa: {'choked' if Pb < Pc else 'not choked'}; Pe = {Pe:6.1f} kPa; Ma_e = {V / csound(k, R, Te):.4f}; V = {V:6.1f} m/s; mdot A = {mA:.3f}, B = {mB:.3f} kg/s")
lit = A * 1045.0 * math.sqrt(1.4 / (0.287 * 884.0)) * (2 / 2.4) ** (2.4 / 0.8); ok = mdot_choked(A, 1045.0, 884.0, k, R)
print(f"slide p.55 literally (kPa, kJ/(kg K)): {lit:.4f} kg/s ; with P0 in Pa and R in J/(kg K): {ok:.3f} kg/s ; ratio = {ok / lit:.2f} = sqrt(1000) = {math.sqrt(1000):.2f}")''',
              tr(f'**Đọc kết quả:** T₀ = {dv(f(T0i,1))} K, P₀ = {dv(f(P0i,1))} kPa, P* = {dv(f(na["Pcrit"],1))} kPa. P_b = 700 kPa: không nghẹt, Ma_e = {dv(f(na["Ma"],4))}, ṁ = {dv(f(na["mdot"],3))} kg/s (slide 6,77 từ nội suy A-32). P_b = 400 kPa: nghẹt, P_e = P* = {dv(f(nb["Pe"],1))} kPa, ṁ = {dv(f(nb["mdot"],3))} kg/s (slide 7,10). Hai đường A, B trùng. Thay nguyên văn kPa và kJ/(kg·K) cho {dv(f(lit,4))} kg/s (sai); đổi đúng đơn vị cho {dv(f(mok,3))} kg/s: tỉ số chính là √1000 = 31,62. Đây là lỗi thiếu hệ số đổi đơn vị của slide tr.55.', f'**Reading the output:** T₀ = {f(T0i,1)} K, P₀ = {f(P0i,1)} kPa, P* = {f(na["Pcrit"],1)} kPa. P_b = 700 kPa: not choked, Ma_e = {f(na["Ma"],4)}, ṁ = {f(na["mdot"],3)} kg/s (slide 6.77 from A-32 interpolation). P_b = 400 kPa: choked, P_e = P* = {f(nb["Pe"],1)} kPa, ṁ = {f(nb["mdot"],3)} kg/s (slide 7.10). Routes A and B agree. Plugging kPa and kJ/(kg·K) literally gives {f(lit,4)} kg/s (wrong); correct units give {f(mok,3)} kg/s: the ratio is exactly √1000 = 31.62. This is the missing unit factor on slide p.55.'),
              [f'T0 = {f(T0i,1)} K', f'mdot A = {f(na["mdot"],3)}', f'slide p.55 literally (kPa, kJ/(kg K)): {f(lit,4)} kg/s', 'sqrt(1000) = 31.62']))
    # ---- 6 area ratio Ex 17-6
    A1s = AAs(0.3, k); A2s = 0.8 * A1s; M2 = Ma_of_AA(A2s, k); TT2, PP2 = TT0(M2, k), PP0(M2, k); T2n = 400 * TT2 / TT0(0.3, k); P2n = 100 * PP2 / PP0(0.3, k); Mi = 0.3 + 0.1 * (2.0351 - A2s) / (2.0351 - 1.5901)
    S.append((tr('Tỉ số diện tích A/A*: slide tr.56–59 (Cengel Ví dụ 17–6) và nội suy bảng A-32', 'Area ratio A/A*: slides p.56–59 (Cengel Example 17–6) and A-32 interpolation'),
              tr('**Câu hỏi:** N₂ (k = 1,4) ở Ma₁ = 0,3, T₁ = 400 K, P₁ = 100 kPa; diện tích giảm 20 %. Ma₂, T₂, P₂ chính xác là bao nhiêu và nội suy tuyến tính của slide sai bao nhiêu? Ba đường: brentq trên (17), tích phân ODE Hugoniot, nội suy A-32.', '**Question:** N₂ (k = 1.4) at Ma₁ = 0.3, T₁ = 400 K, P₁ = 100 kPa; the area is reduced by 20 %. What are the exact Ma₂, T₂, P₂ and how far off is the slide\'s linear interpolation? Three routes: brentq on (17), the Hugoniot ODE, A-32 interpolation.'),
              PRELUDE + '''k = 1.4
A1s = AAs(0.3, k); A2s = 0.8 * A1s
Ma2_A = brentq(lambda M: AAs(M, k) - A2s, 1e-6, 1.0)                                                # A: brentq on (17), subsonic branch
Ma2_B = solve_ivp(lambda x, y: [y[0] * (1 + (k - 1) / 2 * y[0] ** 2) / (y[0] ** 2 - 1)], [0.0, math.log(0.8)], [0.3], rtol=1e-11, atol=1e-13).y[0, -1]   # B: Hugoniot ODE in ln A
rows = A32[A32[:, 0] <= 1.0]; Ma2_C = float(np.interp(A2s, rows[::-1, 2], rows[::-1, 0]))       # C: linear interpolation in A-32 (subsonic rows)
print(f"A1/A* = {A1s:.4f} (A-32 row: {A32[2, 2]}); A2/A* = {A2s:.4f}")
print(f"Ma2: brentq {Ma2_A:.4f} | ODE {Ma2_B:.4f} | A-32 interpolation {Ma2_C:.4f} | slide prints 0.391")
T2 = 400 * TT0(Ma2_A, k) / TT0(0.3, k); P2 = 100 * PP0(Ma2_A, k) / PP0(0.3, k)
print(f"T2 = {T2:.2f} K (slide 395); P2 = {P2:.2f} kPa (slide 95.7; error of the slide {100 * (95.7 / P2 - 1):+.2f} %)")
Ma = 3.5; lin = float(np.interp(Ma, A32[:, 0], A32[:, 2])); ex = AAs(Ma, k)
print(f"sparse rows: A/A* at Ma 3.5: linear {lin:.2f}, exact {ex:.2f} ({100 * (lin / ex - 1):+.0f} %); P/P0 at Ma 4: linear {np.interp(4.0, A32[:, 0], A32[:, 3]):.5f}, exact {PP0(4.0, k):.5f} ({100 * (np.interp(4.0, A32[:, 0], A32[:, 3]) / PP0(4.0, k) - 1):+.0f} %)")''',
              tr(f'**Đọc kết quả:** A₂/A* = {dv(f(A2s,4))}; Ma₂ = {dv(f(M2,4))} (brentq và ODE trùng), nội suy A-32 cho {dv(f(Mi,4))} nên slide in 0,391. T₂ = {dv(f(T2n,2))} K (slide 395 đúng), P₂ = {dv(f(P2n,2))} kPa (slide 95,7 lệch −0,22 %). Với hàng thưa Ma 3 → 5, nội suy sai +39 % cho A/A* tại Ma = 3,5 và +121 % cho P/P₀ tại Ma = 4: chỉ dùng A-32 ở hàng in, còn lại dùng công thức.', f'**Reading the output:** A₂/A* = {f(A2s,4)}; Ma₂ = {f(M2,4)} (brentq and ODE agree), A-32 interpolation gives {f(Mi,4)} hence the slide\'s 0.391. T₂ = {f(T2n,2)} K (the slide\'s 395 is right), P₂ = {f(P2n,2)} kPa (the slide\'s 95.7 is −0.22 % off). With the sparse rows Ma 3 → 5 interpolation is +39 % off for A/A* at Ma = 3.5 and +121 % for P/P₀ at Ma = 4: use A-32 only at printed rows, otherwise the formulas.'),
              [f'A2/A* = {f(A2s,4)}', f'Ma2: brentq {f(M2,4)}', f'P2 = {f(P2n,2)} kPa', '(+39 %)', '(+121 %)']))
    # ---- 7 A-32 check
    S.append((tr('Kiểm bảng A-32: mọi hàng in so với công thức, và lỗi in ρ/ρ₀ tại Ma = 3,0', 'Checking Table A-32: every printed row against the formulas, and the printed error ρ/ρ₀ at Ma = 3.0'),
              tr('**Câu hỏi:** các hàng in của A-32 (Ma*, A/A*, P/P₀, ρ/ρ₀, T/T₀) có khớp công thức (9)–(11), (17) trong nửa đơn vị của chữ số cuối không? Ô nào sai?', '**Question:** do the printed rows of A-32 (Ma*, A/A*, P/P₀, ρ/ρ₀, T/T₀) agree with formulas (9)–(11), (17) within half a unit of the last digit? Which cell is wrong?'),
              PRELUDE + '''k = 1.4; bad = []; n = 0
for Ma, Mas, aa, pp, rr, tt in A32:
    f_ = dict(Mas=Ma * math.sqrt((k + 1) / (2 + (k - 1) * Ma ** 2)), aa=AAs(Ma, k), pp=PP0(Ma, k), rr=TT0(Ma, k) ** (1 / (k - 1)), tt=TT0(Ma, k))
    for key, val in (('Mas', Mas), ('aa', aa), ('pp', pp), ('rr', rr), ('tt', tt)):
        n += 1; tol = 5.1e-4 if (key == 'aa' and Ma == 5.0) else 5.1e-5
        if abs(val - f_[key]) > tol: bad.append((float(Ma), key, float(val), round(float(f_[key]), 5)))
print(n, "printed cells compared; outside half a unit of the last digit:", bad)''',
              tr('**Đọc kết quả:** trong 21 hàng (Ma > 0) × 5 cột = 105 ô chỉ một ô lệch: Ma = 3,0, ρ/ρ₀ in 0,0760, công thức cho 0,07623 (đúng 0,0762). Đây là lỗi in của bảng (thư viện P3 đánh dấu suspect); câu hỏi của module không dùng ô này.', f'**Reading the output:** among 21 rows (Ma > 0) × 5 columns = 105 cells only one cell is off: Ma = 3.0, ρ/ρ₀ printed 0.0760, the formula gives 0.07623 (correct 0.0762). This is a printing error of the table (the P3 library flags it as suspect); the module\'s questions do not use this cell.'),
              ["(3.0, 'rr', 0.076, 0.07623)"]))
    # ---- 8 CD nozzle and variable cp
    S.append((tr('Vòi hội tụ–phân kỳ (Cengel Ví dụ 17–7, 17–135) và c_p biến thiên (17–11, 17–20c)', 'Converging–diverging nozzle (Cengel Example 17–7, 17–135) and variable c_p (17–11, 17–20c)'),
              tr('**Câu hỏi:** (a) Ví dụ 17–7: P₀ = 1 MPa, T₀ = 800 K, A* = 20 cm², Ma_e = 2: A_e, V_e, ṁ; 17–135: heli, A* và A_e. (b) Bài 17–11: T tĩnh khi P₀ = 0,6 MPa, T₀ = 673,15 K, V = 570 m/s với c_p = 1,005 so với bảng A-17 (đáp án in 518,6 K). (c) 17–20c: V₂ của CO₂ khi c_p biến thiên (A-20).', '**Question:** (a) Example 17–7: P₀ = 1 MPa, T₀ = 800 K, A* = 20 cm², Ma_e = 2: A_e, V_e, ṁ; 17–135: helium, A* and A_e. (b) Problem 17–11: static T for P₀ = 0.6 MPa, T₀ = 673.15 K, V = 570 m/s with c_p = 1.005 against Table A-17 (printed 518.6 K). (c) 17–20c: V₂ of CO₂ with variable c_p (A-20).'),
              PRELUDE + '''k, R = 1.4, 0.287; xs, fs = flux_max(k); cp = cp_of(k, R)
# (a) Example 17-7: throat by flux maximum, exit by brentq on the energy equation (no use of eq. 17)
P0, T0, As = 1000.0, 800.0, 20.0
mdot = As * 1e-4 * (P0 / (R * T0)) * xs ** (1 / (k - 1)) * math.sqrt(2000 * cp * T0 * (1 - xs)); xe = x_of_Ma(2.0, k, R)
fe = xe ** (1 / (k - 1)) * math.sqrt(1 - xe); Ae = As * fs / fe; Ve = 2.0 * c_num(T0 * xe, k, R)
print(f"17-7: T* = {xs * T0:.1f} K; mdot = {mdot:.3f} kg/s (book 2.86); A_e = {Ae:.2f} cm2 (33.75); V_e = {Ve:.1f} m/s (845.1-845.2); closed form A_e = {As * AAs(2.0, k):.2f}")
kH, RH = 1.667, 2.0769; xsH, fsH = flux_max(kH); AsH = 0.25 / ((1000.0 / (RH * 500.0)) * xsH ** (1 / (kH - 1)) * math.sqrt(2000 * cp_of(kH, RH) * 500.0 * (1 - xsH))) * 1e4
xeH = (100.0 / 1000.0) ** ((kH - 1) / kH); AeH = AsH * fsH / (xeH ** (1 / (kH - 1)) * math.sqrt(1 - xeH)); print(f"17-135 helium: A* = {AsH:.3f} cm2 (printed 3.51); A_e = {AeH:.3f} cm2 (printed 5.84)")
# (b) 17-11
h0 = float(np.interp(673.15, A17[:, 0], A17[:, 1])); hs = h0 - 570.0 ** 2 / 2000.0; Tv = float(np.interp(hs, A17[:, 1], A17[:, 0]))
Pv = 600.0 * float(np.interp(Tv, A17[:, 0], A17[:, 2])) / float(np.interp(673.15, A17[:, 0], A17[:, 2])); Tc = 673.15 - 570.0 ** 2 / 2010.0
print(f"17-11: constant cp {Tc:.1f} K, {600 * (Tc / 673.15) ** 3.5:.1f} kPa | A-17 {Tv:.1f} K, {Pv:.1f} kPa | printed 518.6 K, 0.23 MPa")
# (c) 17-20c: CO2 1200 K -> 400 K, V1 = 50 m/s
dh = (np.interp(1200.0, A20[:, 0], A20[:, 1]) - np.interp(400.0, A20[:, 0], A20[:, 1])) / 44.01; V2c = math.sqrt(50.0 ** 2 + 2000.0 * 0.846 * 800.0); V2v = math.sqrt(50.0 ** 2 + 2000.0 * dh)
print(f"17-20c: dh = {dh:.1f} kJ/kg (constant cp 0.846 x 800 = {0.846 * 800:.1f}); V2 = {V2c:.0f} m/s (constant cp) vs {V2v:.0f} m/s (A-20): {100 * (V2v / V2c - 1):+.0f} %")''',
              tr(f'**Đọc kết quả:** (a) ṁ = 2,858 kg/s, A_e = 33,75 cm², V_e = 845,1 m/s khớp in 2,86; 33,75; 845,1–845,2; heli A* = 3,508 cm², A_e = 5,845 cm² (in 3,51; 5,84). Cực đại số của ρV và brentq trên phương trình năng lượng cho cùng kết quả với công thức (16), (17). (b) c_p = 1,005 cho 511,5 K (−1,4 %), bảng A-17 cho 518,5 K: đáp án in 518,6 K cần c_p biến thiên. (c) với A-20, V₂ lớn hơn 17 % so với c_p = 0,846 không đổi: giả thiết c_p không đổi kém khi nhiệt độ đổi 800 K.', f'**Reading the output:** (a) ṁ = 2.858 kg/s, A_e = 33.75 cm², V_e = 845.1 m/s match the printed 2.86; 33.75; 845.1–845.2; helium A* = 3.508 cm², A_e = 5.845 cm² (printed 3.51; 5.84). The numerical maximum of ρV and brentq on the energy equation reproduce formulas (16), (17). (b) c_p = 1.005 gives 511.5 K (−1.4 %), Table A-17 gives 518.5 K: the printed 518.6 K needs variable c_p. (c) with A-20, V₂ is 17 % above the constant c_p = 0.846 result: the constant-c_p assumption is poor when the temperature changes by 800 K.'),
              ['17-7: T* = 666.7 K; mdot = 2.858 kg/s', '17-135 helium: A* = 3.508', '17-11: constant cp 511.5 K', 'A-17 518.5 K', '+17 %']))
    return S

def build(lang):
    vi = lang == 'vi'
    nb = nbf.v4.new_notebook()
    head = ('# m05 · Dòng chảy nén được: các phép tính kiểm chứng\n\nSổ tay này tính lại bằng Python các ví dụ chính của module m05 (Slide Ch.5; Cengel Ch.17 §17-1…17-4). Mỗi mục có ba phần: câu hỏi mà phương pháp trả lời → mã → diễn giải kết quả THẬT. Các bảng cần dùng (A-32, A-17, A-20) nhúng trong ô mã đầu tiên. Đường A là công thức đóng của slide; đường B là cách số độc lập (cực đại số của ρV, ODE Hugoniot, đạo hàm số của P(ρ), nội suy bảng). Slide Ch.5 dừng ở vòi hội tụ: sóng xung kích, Fanno, Rayleigh CHƯA LÀM.'
            if vi else
            '# m05 · Compressible flow: verification calculations\n\nThis notebook recomputes in Python the main examples of module m05 (Slide Ch.5; Cengel Ch.17 §17-1…17-4). Every section has three parts: the question the method answers → code → interpretation of the REAL output. The tables used (A-32, A-17, A-20) are embedded in the first code cell. Route A is the slides\' closed form; route B is an independent numerical way (numerical maximum of ρV, the Hugoniot ODE, the numerical derivative of P(ρ), table interpolation). The Ch.5 slides stop at the converging nozzle: shock waves, Fanno, Rayleigh are NOT DONE.')
    cells = [nbf.v4.new_markdown_cell(head)]; checks = []
    for i, (title, q, code, interp, must) in enumerate(sections(lang), 1):
        cells.append(nbf.v4.new_markdown_cell(f'## {i}. {title}\n\n{q}')); cells.append(nbf.v4.new_code_cell(code)); cells.append(nbf.v4.new_markdown_cell(interp)); checks.append((len(cells) - 2, must))
    nb['cells'] = cells; nb['metadata']['language_info'] = {'name': 'python'}
    fn = os.path.join(OUT, f'm05_compressible_flow_{lang}.ipynb'); nbf.write(nb, fn)
    kdir = os.path.join(ROOT, 'scratch', 'm05', 'jupyter', 'kernels', 'm05venv'); os.makedirs(kdir, exist_ok=True)
    json.dump(dict(argv=[os.path.join(ROOT, '.venv', 'bin', 'python'), '-m', 'ipykernel_launcher', '-f', '{connection_file}'], display_name='m05 venv', language='python'), open(os.path.join(kdir, 'kernel.json'), 'w'))
    env = dict(os.environ, JUPYTER_PATH=os.path.join(ROOT, 'scratch', 'm05', 'jupyter'))
    r = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), '-I', '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', '--ExecutePreprocessor.kernel_name=m05venv', fn], capture_output=True, text=True, cwd=OUT, env=env)
    if r.returncode != 0: print(r.stdout[-1500:], r.stderr[-2500:]); raise SystemExit(f'nbconvert failed for {lang}')
    nb2 = nbf.read(fn, as_version=4); nb2['metadata']['kernelspec'] = dict(display_name='Python 3', language='python', name='python3'); nbf.write(nb2, fn)
    for idx, must in checks:
        out = ''.join(o.get('text', '') for o in nb2.cells[idx].get('outputs', []))
        for s in must:
            if s not in out: raise SystemExit(f'[{lang}] cell {idx}: expected "{s}" in the output but it is missing:\n{out}')
    print('executed and verified', fn, len(nb2.cells), 'cells')

if __name__ == '__main__':
    build('vi'); build('en')
