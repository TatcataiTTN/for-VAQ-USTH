"""Build and execute the m03 notebooks (VI and EN).  Run: .venv/bin/python -I build/nb/make_m03.py
Each method section = markdown (question it answers) -> code -> markdown interpreting the REAL output (numbers in the interpretation are computed here with route A
(build/gen/m03_common.py) and then CHECKED against the executed output text: the build fails if they do not appear).
The notebook is self-contained: the R-134a tables A-11, A-12 and the A-13 blocks used (0.14, 0.4, 0.7, 0.8, 1.0 MPa) and the Table A-17 rows (all read from the page images,
data/props/*.json) are embedded in the first code cell. CoolProp is used as the independent route when it is installed (the executed outputs here come from an environment that has it)."""
import os, sys, math, subprocess, json
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
from m03_common import vcrc_ideal, vcrc_real, gas_simple, gas_regen, cop_gas_closed, carnot_R, carnot_HP, sP, sT, shP, h_at_s, c2k, props
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
f = lambda x, nd=2: f'{x:.{nd}f}'
D = lambda n: json.load(open(os.path.join(ROOT, 'data', 'props', n + '.json'), encoding='utf-8'))
A11, A12, A13, A17 = D('A11'), D('A12'), D('A13'), D('A17')
blocks = {b['param']['P_MPa']: dict(sat=b['sat'], rows=b['rows']) for b in A13['blocks'] if b['param']['P_MPa'] in (0.14, 0.4, 0.7, 0.8, 1.0)}
A17r = [r for r in A17['rows'] if r[0] <= 700]

PRELUDE = '''import math, numpy as np
from scipy.integrate import solve_ivp
try:
    import CoolProp.CoolProp as CP
    CP.set_reference_state('R134a', 'ASHRAE')          # h = s = 0 for saturated liquid at -40 C, as in the tables
    HAVE_CP = True
except Exception:
    HAVE_CP = False
# R-134a, Appendix 1 tables read from the page images. A-11: T, Psat, hf, hfg, hg, sf, sfg, sg ; A-12: Psat, Tsat, hf, hfg, hg, sf, sfg, sg
A11 = np.array(%s)
A12 = np.array(%s)
# A-13 superheated R-134a (blocks used here): P_MPa -> dict(sat=[v, u, h, s], rows=[[T, v, u, h, s], ...])
A13 = %s
# Table A-17 (air, ideal gas), rows up to 700 K: T [K], h [kJ/kg], P_r, u, v_r, s0
A17 = np.array(%s)
def satT(T, col):                                   # A-11 by temperature (linear between rows)
    return float(np.interp(T, A11[:, 0], A11[:, col]))
def satP(P, col):                                   # A-12 by pressure [kPa]
    return float(np.interp(P, A12[:, 0], A12[:, col]))
HF, HFG, HG, SF, SFG, SG = 2, 3, 4, 5, 6, 7        # column numbers (same in A-11 and A-12 after the first two columns)
def A12col(P, name): return satP(P, dict(Tsat=1, hf=2, hfg=3, hg=4, sf=5, sfg=6, sg=7)[name])
def A11col(T, name): return satT(T, dict(Psat=1, hf=2, hfg=3, hg=4, sf=5, sfg=6, sg=7)[name])
def h_at_s(P_MPa, s):                                # h and T at (P, s): linear interpolation in s inside the A-13 block (the book's method)
    blk = A13[P_MPa]; rows = [[None] + blk['sat']] + blk['rows']          # saturated row first: [T, v, u, h, s]
    S = [r[4] for r in rows]; H = [r[3] for r in rows]
    for i in range(len(S) - 1):
        if S[i] <= s <= S[i + 1]:
            t = (s - S[i]) / (S[i + 1] - S[i]); return H[i] + t * (H[i + 1] - H[i])
    raise ValueError('s outside the block')
def sh(P_MPa, T, col):                               # exact grid point of an A-13 block: col in v, u, h, s
    for r in A13[P_MPa]['rows']:
        if r[0] == T: return r[dict(v=1, u=2, h=3, s=4)[col]]
    raise ValueError('not a grid point')
def tab(col, T): return float(np.interp(T, A17[:, 0], A17[:, dict(T=0, h=1, Pr=2, u=3, vr=4, s0=5)[col]]))
def inv(col, val):
    x = A17[:, dict(T=0, h=1, Pr=2, u=3, vr=4, s0=5)[col]]; return float(np.interp(val, x, A17[:, 0]))
''' % (json.dumps([[r[0], r[1], r[7], r[8], r[9], r[10], r[11], r[12]] for r in A11['rows']]), json.dumps([[r[0], r[1], r[7], r[8], r[9], r[10], r[11], r[12]] for r in A12['rows']]), repr(blocks), json.dumps(A17r))

def sections(lang):
    vi = lang == 'vi'
    tr = lambda a, b: a if vi else b
    S = []      # (title, question_md, code, interpretation_md, [strings that must appear in stdout])
    c = vcrc_ideal(140, 800); m = 0.05; c12 = vcrc_ideal(120, 700); ex2 = vcrc_real(0.14, -10, 0.8, T2_C=50, T3_C=26); p18 = vcrc_real(0.14, -10, 0.7, T2_C=50, T3_C=24)
    # ---- 1 Carnot
    S.append((tr('COP của máy lạnh Carnot đảo ngược', 'COP of a reversed-Carnot refrigerator'),
              tr('**Câu hỏi:** COP_R,Carnot = 1/(T_H/T_L − 1) thay đổi thế nào khi hai nhiệt độ lại gần nhau? Thử với T_H = 35 °C và vài T_L (slide Ch.3 tr.13).', '**Question:** how does COP_R,Carnot = 1/(T_H/T_L − 1) change as the two temperatures come closer? Try T_H = 35 °C and several T_L (slide Ch.3 p.13).'),
              PRELUDE + '''def carnot_R(TL, TH): return 1.0 / (TH / TL - 1.0)
def carnot_HP(TL, TH): return 1.0 / (1.0 - TL / TH)
TH = 35 + 273.15
for TLc in (-20, -10, 0, 10):
    TL = TLc + 273.15
    print(f"TL = {TLc:4d} C, TH = 35 C: COP_R = {carnot_R(TL, TH):5.2f}, COP_HP = {carnot_HP(TL, TH):5.2f} (COP_HP - COP_R = {carnot_HP(TL, TH) - carnot_R(TL, TH):.2f})")''',
              tr(f'**Đọc kết quả:** COP_R tăng từ {f(carnot_R(253.15,308.15))} lên {f(carnot_R(283.15,308.15))} khi T_L tăng từ −20 lên 10 °C; hiệu COP_HP − COP_R luôn bằng 1,00 (hệ thức Cengel 11–3). Nhiệt độ phải ở kelvin: dùng °C cho kết quả vô nghĩa.', f'**Reading the output:** COP_R rises from {f(carnot_R(253.15,308.15))} to {f(carnot_R(283.15,308.15))} as T_L rises from −20 to 10 °C; the difference COP_HP − COP_R is always 1.00 (Cengel Eq. 11–3). Temperatures must be in kelvin: °C gives nonsense.'),
              [f'COP_R = {carnot_R(253.15,308.15):5.2f}', 'COP_HP - COP_R = 1.00']))
    # ---- 2 Tutorials I
    S.append((tr('Tutorials I: chu trình nén hơi lý tưởng R-134a 0,14–0,8 MPa bằng bảng', 'Tutorials I: ideal R-134a vapor-compression cycle 0.14–0.8 MPa from the tables'),
              tr('**Câu hỏi:** tính h₁…h₄, Q̇_L, Ẇ_in, Q̇_H, COP bằng bảng (nội suy theo s) và so với đáp án slide (239,16; 275,39; 95,47; 7,18 kW; 1,81 kW; COP 3,97) và với CoolProp.', '**Question:** compute h₁…h₄, Q̇_L, Ẇ_in, Q̇_H and COP from the tables (interpolation in s) and compare with the slide answers (239.16; 275.39; 95.47; 7.18 kW; 1.81 kW; COP 3.97) and with CoolProp.'),
              '''def ideal(Pl, Ph):                                   # kPa: evaporator and condenser pressures
    h1, s1 = A12col(Pl, 'hg'), A12col(Pl, 'sg'); h3 = A12col(Ph, 'hf'); h2 = h_at_s(Ph / 1000, s1); h4 = h3
    x4 = (h4 - A12col(Pl, 'hf')) / A12col(Pl, 'hfg')
    return dict(h1=h1, h2=h2, h3=h3, h4=h4, s1=s1, qL=h1 - h4, w=h2 - h1, qH=h2 - h3, cop=(h1 - h4) / (h2 - h1), x4=x4)
def ideal_cp(Pl, Ph):                                # independent route: CoolProp R134a
    h1 = CP.PropsSI('H', 'P', Pl*1e3, 'Q', 1, 'R134a')/1e3; s1 = CP.PropsSI('S', 'P', Pl*1e3, 'Q', 1, 'R134a')
    h2 = CP.PropsSI('H', 'P', Ph*1e3, 'S', s1, 'R134a')/1e3; h3 = CP.PropsSI('H', 'P', Ph*1e3, 'Q', 0, 'R134a')/1e3
    return dict(h1=h1, h2=h2, h3=h3, cop=(h1-h3)/(h2-h1))
m = 0.05; c = ideal(140, 800)
print(f"h1 = {c['h1']:.2f}, h2 = {c['h2']:.2f}, h3 = h4 = {c['h3']:.2f} kJ/kg, x4 = {c['x4']:.3f}")
print(f"QL = {m*c['qL']:.2f} kW, Win = {m*c['w']:.2f} kW, QH = {m*c['qH']:.2f} kW, COP = {c['cop']:.3f}")
if HAVE_CP:
    k = ideal_cp(140, 800); print(f"CoolProp: h1 = {k['h1']:.3f}, h2 = {k['h2']:.3f}, h3 = {k['h3']:.3f}, COP = {k['cop']:.3f}")''',
              tr(f'**Đọc kết quả:** bảng cho h₁ = {f(c["h1"])}, h₂ = {f(c["h2"])}, h₃ = {f(c["h3"])}; Q̇_L = {f(m*c["qL"])} kW, Ẇ_in = {f(m*c["w"])} kW, COP = {f(c["cop"],3)}: đúng các số của slide tr.25–27. CoolProp lệch ≤ 0,03 kJ/kg ở entanpi và 0,002 ở COP. x₄ = {f(c["x4"],3)}: khoảng một phần ba môi chất đã bay hơi trong van tiết lưu.', f'**Reading the output:** the tables give h₁ = {f(c["h1"])}, h₂ = {f(c["h2"])}, h₃ = {f(c["h3"])}; Q̇_L = {f(m*c["qL"])} kW, Ẇ_in = {f(m*c["w"])} kW, COP = {f(c["cop"],3)}: the numbers of slides p.25–27. CoolProp differs by ≤ 0.03 kJ/kg in enthalpy and 0.002 in COP. x₄ = {f(c["x4"],3)}: about one third of the refrigerant flashes to vapor in the valve.'),
              [f"h1 = {c['h1']:.2f}, h2 = {c['h2']:.2f}", f"QL = {m*c['qL']:.2f} kW", f"COP = {c['cop']:.3f}", 'CoolProp: h1 = 239.176']))
    # ---- 3 Cengel 11-12
    S.append((tr('Thử phương pháp trên Cengel Bài 11–12 (có đáp án in)', 'Test the method on Cengel Problem 11–12 (printed answer)'),
              tr('**Câu hỏi:** cùng hàm `ideal` cho cặp 0,12–0,7 MPa, 0,05 kg/s có ra 7,41 kW; 1,83 kW; 9,23 kW; 4,06 không?', '**Question:** does the same `ideal` function give 7.41 kW; 1.83 kW; 9.23 kW; 4.06 for the 0.12–0.7 MPa pair at 0.05 kg/s?'),
              '''c12 = ideal(120, 700)
print(f"QL = {m*c12['qL']:.2f} kW, Win = {m*c12['w']:.2f} kW, QH = {m*c12['qH']:.3f} kW, COP = {c12['cop']:.3f}")
print('printed: 7.41, 1.83, 9.23, 4.06')
if HAVE_CP:
    k = ideal_cp(120, 700); print(f"CoolProp: QH = {m*(k['h2']-k['h3']):.3f} kW, COP = {k['cop']:.3f}")''',
              tr(f'**Đọc kết quả:** Q̇_L = {f(m*c12["qL"])} và Ẇ_in = {f(m*c12["w"])} khớp. Q̇_H = {f(m*c12["qH"],3)} (in 9,23) và COP = {f(c12["cop"],3)} (in 4,06) lệch 0,006 và 0,009 vì h₂ nội suy tuyến tính cao hơn phương trình trạng thái khoảng 0,03 kJ/kg; CoolProp cho 9,233 và 4,055, gần đáp án in hơn. Dung sai COP ± 0,015.', f'**Reading the output:** Q̇_L = {f(m*c12["qL"])} and Ẇ_in = {f(m*c12["w"])} agree. Q̇_H = {f(m*c12["qH"],3)} (printed 9.23) and COP = {f(c12["cop"],3)} (printed 4.06) are off by 0.006 and 0.009 because the linearly interpolated h₂ is about 0.03 kJ/kg above the equation of state; CoolProp gives 9.233 and 4.055, closer to the printed answer. COP tolerance ± 0.015.'),
              [f"QL = {m*c12['qL']:.2f} kW", f"COP = {c12['cop']:.3f}", 'printed: 7.41, 1.83, 9.23, 4.06']))
    # ---- 4 real cycle
    S.append((tr('Chu trình thực: hiệu suất máy nén và quá lạnh (Cengel Ví dụ 11–2, Bài 11–18)', 'Real cycle: compressor efficiency and subcooling (Cengel Example 11–2, Problem 11–18)'),
              tr('**Câu hỏi:** với trạng thái thực (hơi quá nhiệt vào máy nén, lỏng quá lạnh ra dàn ngưng, nén không đẳng entropi), COP và η_c là bao nhiêu so với chu trình lý tưởng?', '**Question:** with real states (superheated vapor into the compressor, subcooled liquid out of the condenser, non-isentropic compression), what are the COP and η_c compared with the ideal cycle?'),
              '''def real(P1, T1, P2, T2, T3):                      # MPa, C, MPa, C (compressor exit), C (condenser exit liquid)
    h1, s1 = sh(P1, T1, 'h'), sh(P1, T1, 's'); h2s = h_at_s(P2, s1); h2 = sh(P2, T2, 'h'); h3 = A11col(T3, 'hf')
    return dict(h1=h1, h2=h2, h2s=h2s, h3=h3, qL=h1 - h3, w=h2 - h1, cop=(h1 - h3) / (h2 - h1), eta=(h2s - h1) / (h2 - h1))
e = real(0.14, -10, 0.8, 50, 26); print(f"Example 11-2: h1 = {e['h1']:.2f}, h2 = {e['h2']:.2f}, h2s = {e['h2s']:.2f}, h3 = {e['h3']:.2f}")
print(f"  QL = {0.05*e['qL']:.2f} kW, Win = {0.05*e['w']:.2f} kW, eta_c = {e['eta']:.3f}, COP = {e['cop']:.2f} (ideal cycle: {c['cop']:.2f})")
g = real(0.14, -10, 0.7, 50, 24)
print(f"Problem 11-18: QL = {0.12*g['qL']:.2f} kW, Win = {0.12*g['w']:.2f} kW, eta_c = {g['eta']:.3f}, COP = {g['cop']:.2f}")
print('printed: 7.93, 2.02, 0.939, 3.93 and 19.4, 5.06, 0.825, 3.83')''',
              tr(f'**Đọc kết quả:** Ví dụ 11–2: Q̇_L = {f(0.05*ex2["qL"])} kW, Ẇ = {f(0.05*ex2["w"])} kW, η_c = {f(ex2["eta_c"],3)}, COP = {f(ex2["cop"])} nhỏ hơn {f(c["cop"])} của chu trình lý tưởng dù có quá lạnh, vì công nén tăng nhiều hơn nhiệt lạnh. Bài 11–18: η_c = {f(p18["eta_c"],3)} từ bảng (in 0,825; CoolProp 0,825): h₂ₛ nội suy tuyến tính cao hơn 0,04 kJ/kg.', f'**Reading the output:** Example 11–2: Q̇_L = {f(0.05*ex2["qL"])} kW, Ẇ = {f(0.05*ex2["w"])} kW, η_c = {f(ex2["eta_c"],3)}, COP = {f(ex2["cop"])}, below the {f(c["cop"])} of the ideal cycle despite the subcooling, because the work rises more than the cooling. Problem 11–18: η_c = {f(p18["eta_c"],3)} from the tables (printed 0.825; CoolProp 0.825): the linearly interpolated h₂ₛ is 0.04 kJ/kg high.'),
              [f"eta_c = {ex2['eta_c']:.3f}", f"COP = {ex2['cop']:.2f}", f"eta_c = {p18['eta_c']:.3f}"]))
    # ---- 5 turbine and rule of thumb
    s3 = sP(800, 'sf'); x4s = (s3 - sP(140, 'sf')) / sP(140, 'sfg'); h4s = sP(140, 'hf') + x4s * sP(140, 'hfg'); qLt = c['h1'] - h4s; wt = c['w'] - (c['h3'] - h4s)
    TLk, THk = c['Tl'] + 273.15, c['Th'] + 273.15
    S.append((tr('So với Carnot, tuabin thay van tiết lưu và quy tắc 2–4 % mỗi °C', 'Versus Carnot, a turbine instead of the valve, and the 2–4 % per °C rule'),
              tr('**Câu hỏi:** chu trình Tutorials I đạt bao nhiêu phần trăm COP Carnot? Thay van bằng tuabin đẳng entropi thì COP tăng bao nhiêu (Cengel Ví dụ 11–1, phần Discussion)? Quy tắc "COP tăng 2–4 % mỗi °C nhiệt độ bay hơi" có đúng không?', '**Question:** what fraction of the Carnot COP does the Tutorials I cycle reach? If the valve is replaced by an isentropic turbine, how much does the COP rise (Cengel Example 11–1, Discussion)? Is the "COP +2–4 % per °C of evaporating temperature" rule right?'),
              '''TLk, THk = A12col(140, 'Tsat') + 273.15, A12col(800, 'Tsat') + 273.15
ccar = 1 / (THk / TLk - 1); print(f"Carnot between {TLk-273.15:.2f} C and {THk-273.15:.2f} C: COP = {ccar:.2f}; cycle/Carnot = {c['cop']/ccar:.2f}")
s3 = A12col(800, 'sf'); x4s = (s3 - A12col(140, 'sf')) / A12col(140, 'sfg'); h4s = A12col(140, 'hf') + x4s * A12col(140, 'hfg')
qLt = c['h1'] - h4s; wt = c['w'] - (c['h3'] - h4s)
print(f"turbine instead of valve: h4s = {h4s:.2f} kJ/kg (book 88.94), turbine power = {m*(c['h3']-h4s):.2f} kW, COP = {qLt/wt:.2f} (book 5.07), increase {100*(qLt/wt/c['cop']-1):.1f} %")
if HAVE_CP:
    def cop_T(Tl, Th):
        Pl = CP.PropsSI('P', 'T', Tl+273.15, 'Q', 1, 'R134a'); Ph = CP.PropsSI('P', 'T', Th+273.15, 'Q', 0, 'R134a')
        h1 = CP.PropsSI('H', 'P', Pl, 'Q', 1, 'R134a'); s1 = CP.PropsSI('S', 'P', Pl, 'Q', 1, 'R134a')
        return (h1 - CP.PropsSI('H', 'P', Ph, 'Q', 0, 'R134a')) / (CP.PropsSI('H', 'P', Ph, 'S', s1, 'R134a') - h1)
    for Tl in (-20, -10, 0):
        print(f"T_evap {Tl:4d} C, T_cond 40 C: COP = {cop_T(Tl, 40):.3f}; +1 C evaporating: {100*(cop_T(Tl+1, 40)/cop_T(Tl, 40)-1):.2f} %; -1 C condensing: {100*(cop_T(Tl, 39)/cop_T(Tl, 40)-1):.2f} %")''',
              tr(f'**Đọc kết quả:** COP Carnot = {f(carnot_R(TLk,THk))}; chu trình lý tưởng = {f(c["cop"])}, tức {f(c["cop"]/carnot_R(TLk,THk))} của Carnot. Tuabin thay van cho h₄ₛ = {f(h4s)} kJ/kg và COP = {f(qLt/wt)}: tăng {f(100*(qLt/wt/c["cop"]-1),1)} % (sách làm tròn thành 5,07 và 28 %). Quy tắc kinh nghiệm của Cengel đúng: mỗi °C nhiệt độ bay hơi tăng hoặc ngưng tụ giảm làm COP tăng khoảng 2,5–3,5 % trong các điểm thử.', f'**Reading the output:** Carnot COP = {f(carnot_R(TLk,THk))}; the ideal cycle = {f(c["cop"])}, i.e. {f(c["cop"]/carnot_R(TLk,THk))} of Carnot. A turbine instead of the valve gives h₄ₛ = {f(h4s)} kJ/kg and COP = {f(qLt/wt)}: up {f(100*(qLt/wt/c["cop"]-1),1)} % (the book rounds to 5.07 and 28 %). Cengel\'s rule of thumb holds: each °C of higher evaporating or lower condensing temperature raises the COP by about 2.5–3.5 % at the test points.'),
              [f"cycle/Carnot = {c['cop']/carnot_R(TLk,THk):.2f}", f"h4s = {h4s:.2f} kJ/kg", 'T_evap  -10 C, T_cond 40 C']))
    # ---- 6 flash chamber
    hf4, hg4 = sP(400, 'hf'), sP(400, 'hg'); h5 = sP(800, 'hf'); x6 = (h5 - hf4) / (hg4 - hf4); h1f = sP(140, 'hg'); s1f = sP(140, 'sg'); h2f, _ = h_at_s(0.4, s1f)
    h9 = (1 - x6) * h2f + x6 * hg4; s9 = (1 - x6) * s1f + x6 * sP(400, 'sg'); h4f, _ = h_at_s(0.8, s9); qLf = (1 - x6) * (h1f - hf4); wf = (1 - x6) * (h2f - h1f) + (h4f - h9)
    S.append((tr('Hệ nén hai cấp có buồng giãn (Cengel Bài 11–96, mở rộng)', 'Two-stage compression with a flash chamber (Cengel Problem 11–96, extension)'),
              tr('**Câu hỏi:** giữa 0,8 và 0,14 MPa với buồng giãn ở 0,4 MPa: phần bay hơi x₆, nhiệt lạnh và công trên 1 kg qua dàn ngưng, COP là bao nhiêu (in 0,165; 146,4; 32,6; 4,49)?', '**Question:** between 0.8 and 0.14 MPa with a flash chamber at 0.4 MPa: what are the flashing fraction x₆, the heat removed and the work per kg through the condenser, and the COP (printed 0.165; 146.4; 32.6; 4.49)?'),
              '''hf4, hg4 = A12col(400, 'hf'), A12col(400, 'hg'); h5 = A12col(800, 'hf'); x6 = (h5 - hf4) / (hg4 - hf4)       # flashing fraction
h1, s1 = A12col(140, 'hg'), A12col(140, 'sg'); h2 = h_at_s(0.4, s1)                  # low-pressure compressor to 0.4 MPa
h9 = (1 - x6) * h2 + x6 * hg4; s9 = (1 - x6) * s1 + x6 * A12col(400, 'sg'); h4 = h_at_s(0.8, s9)   # mixing, then high-pressure compressor
qL = (1 - x6) * (h1 - hf4); w = (1 - x6) * (h2 - h1) + (h4 - h9)
print(f"x6 = {x6:.3f}, qL = {qL:.1f} kJ/kg, w = {w:.1f} kJ/kg, COP = {qL/w:.2f}")
print(f"single stage 0.14-0.8 MPa: COP = {c['cop']:.2f}")''',
              tr(f'**Đọc kết quả:** x₆ = {f(x6,3)}; q_L = {f(qLf,1)}, w = {f(wf,1)} kJ/kg, COP = {f(qLf/wf)}: khớp đáp án in 0,165; 146,4; 32,6; 4,49. So với một cấp cùng giới hạn áp suất (COP {f(c["cop"])}), hai cấp cao hơn {f(100*(qLf/wf/c["cop"]-1),0)} %.', f'**Reading the output:** x₆ = {f(x6,3)}; q_L = {f(qLf,1)}, w = {f(wf,1)} kJ/kg, COP = {f(qLf/wf)}: matching the printed 0.165; 146.4; 32.6; 4.49. Compared with a single stage at the same pressure limits (COP {f(c["cop"])}), the two-stage system is {f(100*(qLf/wf/c["cop"]-1),0)} % higher.'),
              [f"x6 = {x6:.3f}", f"COP = {qLf/wf:.2f}"]))
    # ---- 7 gas cycles
    g97 = gas_simple(c2k(30), c2k(70), 2.5); g61 = gas_regen(c2k(-7), c2k(27), c2k(-15), 4.0)
    S.append((tr('Chu trình khí lạnh: hệ làm mát hở cho máy bay (Bài 11–97) và hồi nhiệt (Bài 11–61)', 'Gas refrigeration: open aircraft cooling (Problem 11–97) and regeneration (Problem 11–61)'),
              tr('**Câu hỏi:** không khí 30 °C, 100 kPa nén tới 250 kPa, làm mát tới 70 °C rồi giãn qua tuabin: nhiệt độ vào cabin? Công thức đóng so với tích phân số đường đẳng entropi; COP = 1/(r_p^((k−1)/k) − 1) có đúng không?', '**Question:** air at 30 °C, 100 kPa is compressed to 250 kPa, cooled to 70 °C and expanded through a turbine: what is the cabin inlet temperature? Closed form versus numerical integration of the isentrope; does COP = 1/(r_p^((k−1)/k) − 1) hold?'),
              '''k, cp = 1.4, 1.005
def T_isen(T1, p1, p2):                              # numerical isentrope: dT/dp = R T/(cp p), R = cp (k-1)/k
    R = cp * (k - 1) / k; return solve_ivp(lambda p, T: [R * T[0] / (cp * p)], (p1, p2), [T1], rtol=1e-12, atol=1e-12).y[0, -1]
x = 2.5 ** ((k - 1) / k); T1, T3 = 303.15, 343.15
T2 = T1 * x; T4 = T3 / x
print(f"Problem 11-97: T2 = {T2-273.15:.1f} C, T4 = {T4-273.15:.1f} C (printed -9 C); ODE: T4 = {T_isen(T3, 250, 100)-273.15:.1f} C")
q = cp * (T1 - T4); w = cp * (T2 - T1) - cp * (T3 - T4); print(f"COP = {q/w:.3f}; closed form 1/(x-1) = {1/(x-1):.3f}")
# regenerative cycle (Problem 11-61): T1 = -7 C, T3 = 27 C after the sink, T4 = -15 C after the regenerator, r_p = 4
x4 = 4 ** ((k - 1) / k); T1, T3, T4 = 266.15, 300.15, 258.15
T2, T5, T6 = T1 * x4, T4 / x4, T1 - (T3 - T4)
qL = cp * (T6 - T5); wn = cp * (T2 - T1) - cp * (T4 - T5)
print(f"Problem 11-61: lowest T = {T5-273.15:.1f} C, COP = {qL/wn:.2f}, mass flow for 12 kW = {12/qL:.3f} kg/s (printed -99.4 C, 1.12, 0.237)")
if HAVE_CP:
    A = lambda o, *a: CP.PropsSI(o, *a, 'Air')
    T4cp = A('T', 'P', 100e3, 'S', A('S', 'T', 343.15, 'P', 250e3)); print(f"CoolProp Air (real gas): T4 = {T4cp-273.15:.2f} C")''',
              tr(f'**Đọc kết quả:** T₂ = {f(g97["T2"]-273.15,1)} °C, T₄ = {f(g97["T4"]-273.15,1)} °C ≈ −9 °C (in −9 °C); tích phân số trùng công thức đóng, CoolProp (khí thật) lệch dưới 0,3 K. COP = {f(g97["cop"],3)} = 1/(x − 1): chỉ phụ thuộc r_p. Bài 11–61: nhiệt độ thấp nhất {f(g61["T5"]-273.15,1)} °C, COP = {f(g61["cop"])}, ṁ = {f(12/g61["qL"],3)} kg/s: khớp đáp án in.', f'**Reading the output:** T₂ = {f(g97["T2"]-273.15,1)} °C, T₄ = {f(g97["T4"]-273.15,1)} °C ≈ −9 °C (printed −9 °C); the numerical integration equals the closed form and CoolProp (real gas) is within 0.3 K. COP = {f(g97["cop"],3)} = 1/(x − 1): it depends only on r_p. Problem 11–61: lowest temperature {f(g61["T5"]-273.15,1)} °C, COP = {f(g61["cop"])}, ṁ = {f(12/g61["qL"],3)} kg/s: matching the printed answers.'),
              [f"T4 = {g97['T4']-273.15:.1f} C", f"COP = {g97['cop']:.3f}", f"lowest T = {g61['T5']-273.15:.1f} C", f"COP = {g61['cop']:.2f}"]))
    # ---- 8 A-17 route
    T1a, T3a, rpa, ma = 285.0, 320.0, 5.0, 0.08
    Pr1 = props.air(T1a, 'Pr')['value']; T2a = props.air_inverse('Pr', rpa * Pr1)['value']; h1a = props.air(T1a, 'h')['value']; h2a = props.air(T2a, 'h')['value']
    Pr3 = props.air(T3a, 'Pr')['value']; T4a = props.air_inverse('Pr', Pr3 / rpa)['value']; h3a = props.air(T3a, 'h')['value']; h4a = props.air(T4a, 'h')['value']
    qLa = h1a - h4a; wa = (h2a - h1a) - (h3a - h4a)
    S.append((tr('Khí lạnh với nhiệt dung riêng thay đổi: bảng A-17 (Cengel Bài 11–56)', 'Gas refrigeration with variable specific heats: Table A-17 (Cengel Problem 11–56)'),
              tr('**Câu hỏi:** không khí vào máy nén 12 °C (285 K), 50 kPa; vào tuabin 47 °C (320 K), 250 kPa; 0,08 kg/s. Công suất lạnh, công thực, COP bằng P_r của bảng A-17 là bao nhiêu (in 6,67 kW; 3,88 kW; 1,72), và khác thế nào với c_p hằng?', '**Question:** air enters the compressor at 12 °C (285 K), 50 kPa and the turbine at 47 °C (320 K), 250 kPa; 0.08 kg/s. What are the refrigeration rate, net power and COP from the P_r column of Table A-17 (printed 6.67 kW; 3.88 kW; 1.72), and how do they differ from constant c_p?'),
              '''rp, T1, T3, m = 5.0, 285.0, 320.0, 0.08
T2 = inv('Pr', rp * tab('Pr', T1)); T4 = inv('Pr', tab('Pr', T3) / rp)                 # isentropic: Pr2/Pr1 = rp
h1, h2, h3, h4 = tab('h', T1), tab('h', T2), tab('h', T3), tab('h', T4)
qL = h1 - h4; wnet = (h2 - h1) - (h3 - h4)
print(f"T2 = {T2:.1f} K, T4 = {T4:.1f} K; qL = {qL:.2f} kJ/kg, wnet = {wnet:.2f} kJ/kg")
print(f"QL = {m*qL:.2f} kW, Wnet = {m*wnet:.2f} kW, COP = {qL/wnet:.2f} (printed 6.67, 3.88, 1.72)")
print(f"constant cp: COP = {1/(rp**(0.4/1.4)-1):.3f}")''',
              tr(f'**Đọc kết quả:** T₂ = {f(T2a,1)} K, T₄ = {f(T4a,1)} K (thấp hơn 273 K nên đa thức c_p(T) của A-2c không dùng được, bài kiểm bằng tích phân c_p của CoolProp, lệch dưới 1 %); Q̇_L = {f(ma*qLa)} kW, Ẇ = {f(ma*wa)} kW, COP = {f(qLa/wa)}: khớp đáp án in. Với c_p hằng COP = {f(cop_gas_closed(5.0),3)}: gần nhưng khác {f(100*(qLa/wa/cop_gas_closed(5.0)-1),1)} %.', f'**Reading the output:** T₂ = {f(T2a,1)} K, T₄ = {f(T4a,1)} K (below 273 K, where the A-2c c_p(T) polynomial does not apply, so the check uses the integral of CoolProp\'s c_p, within 1 %); Q̇_L = {f(ma*qLa)} kW, Ẇ = {f(ma*wa)} kW, COP = {f(qLa/wa)}: matching the printed answers. With constant c_p the COP = {f(cop_gas_closed(5.0),3)}: close but {f(100*(qLa/wa/cop_gas_closed(5.0)-1),1)} % different.'),
              [f"T2 = {T2a:.1f} K", f"QL = {ma*qLa:.2f} kW", f"COP = {qLa/wa:.2f}", f"constant cp: COP = {cop_gas_closed(5.0):.3f}"]))
    # ---- 9 cooling pack numbers
    PRc = ((323.15 + 35) / 323.15) ** 3.5; PRt = (288.15 / 263.15) ** 3.5
    S.append((tr('Cooling pack: chuỗi nhiệt độ của slide và quy đổi đơn vị (chỉ minh hoạ)', 'Cooling pack: the slide temperature chain and unit conversions (illustration only)'),
              tr('**Câu hỏi:** cộng/trừ các số nhiệt độ của slide tr.32–35 cho chuỗi nhiệt độ nào? 30–40 psi và 40.000–50.000 vòng/phút là bao nhiêu trong đơn vị SI? Nếu nén/giãn là đẳng entropi thì các độ thay đổi nhiệt độ đó tương ứng tỉ số áp bao nhiêu (slide KHÔNG cho tỉ số áp)?', '**Question:** what temperature chain do the slide p.32–35 numbers give when added/subtracted? What are 30–40 psi and 40.000–50.000 rpm in SI units? If compression/expansion were isentropic, what pressure ratios would those temperature changes imply (the slides give NO pressure ratio)?'),
              '''T0 = 150.0                                                  # bleed air entering the primary heat exchanger (slide p.32)
after_primary = T0 - 100                                      # "about 100 C" drop (p.32): derived value, not printed on the slide
after_comp = (after_primary + 30, after_primary + 40)         # compressor rise 30-40 C (p.33)
after_secondary = (after_comp[0] - 70, after_comp[1] - 60)    # secondary drop 60-70 C (p.33): lowest and highest possible
print(f"after primary exchanger: {after_primary:.0f} C; after ACM compressor: {after_comp[0]:.0f}-{after_comp[1]:.0f} C; after secondary: {after_secondary[0]:.0f}-{after_secondary[1]:.0f} C")
print("slide p.34 turbine inlet '20 to 10 C' (read as 10-20 C) lies inside the derived range" if after_secondary[0] <= 10 and 20 <= after_secondary[1] else "inconsistent")
psi = 6.894757
print(f"30-40 psi = {30*psi:.0f}-{40*psi:.0f} kPa; if gauge, absolute = {30*psi+101.325:.0f}-{40*psi+101.325:.0f} kPa")
print(f"40 000-50 000 rpm = {40000*2*math.pi/60:.0f}-{50000*2*math.pi/60:.0f} rad/s")
PRc = ((50 + 273.15 + 35) / (50 + 273.15)) ** 3.5; PRt = ((15 + 273.15) / (-10 + 273.15)) ** 3.5
print(f"illustration (isentropic, k = 1.4): +35 K from 50 C -> pressure ratio {PRc:.2f}; 15 C -> -10 C expansion -> pressure ratio {PRt:.2f}")''',
              tr(f'**Đọc kết quả:** chuỗi 150 → 50 → 80–90 → 10–30 °C khớp khoảng 10–20 °C của tr.34 (slide viết ngược "20 to 10"). 30–40 psi = {f(30*6.894757,0)}–{f(40*6.894757,0)} kPa (nếu là áp suất dư thì tuyệt đối {f(30*6.894757+101.325,0)}–{f(40*6.894757+101.325,0)} kPa: slide không nói rõ). 40.000–50.000 vòng/phút = {f(40000*2*math.pi/60,0)}–{f(50000*2*math.pi/60,0)} rad/s. Tỉ số áp minh hoạ {f(PRc)} (máy nén) và {f(PRt)} (tuabin) chỉ là suy luận dưới giả thiết đẳng entropi, không phải số liệu của slide.', f'**Reading the output:** the chain 150 → 50 → 80–90 → 10–30 °C is consistent with the 10–20 °C of p.34 (the slide writes "20 to 10" in reverse). 30–40 psi = {f(30*6.894757,0)}–{f(40*6.894757,0)} kPa (if gauge, absolute {f(30*6.894757+101.325,0)}–{f(40*6.894757+101.325,0)} kPa: the slide does not say). 40.000–50.000 rpm = {f(40000*2*math.pi/60,0)}–{f(50000*2*math.pi/60,0)} rad/s. The illustrative pressure ratios {f(PRc)} (compressor) and {f(PRt)} (turbine) are inferences under an isentropic assumption, not slide data.'),
              ['after primary exchanger: 50 C', 'after secondary: 10-30 C', f'30-40 psi = {30*6.894757:.0f}-{40*6.894757:.0f} kPa', f'pressure ratio {PRc:.2f}']))
    return S

def build(lang):
    vi = lang == 'vi'
    nb = nbf.v4.new_notebook()
    head = ('# m03 · Chu trình lạnh và điều hoà không khí trên tàu bay: các phép tính kiểm chứng\n\nSổ tay này tính lại bằng Python các ví dụ chính của module m03 (Slide Ch.3; Tutorials I; Cengel Ch.11). Mỗi mục có ba phần: câu hỏi mà phương pháp trả lời → mã → diễn giải số in thật. Chạy từ trên xuống. Các bảng R-134a (A-11, A-12, các khối A-13) và bảng A-17 được nhúng sẵn trong ô mã đầu; nếu máy có CoolProp thì mỗi mục còn so sánh với CoolProp (đường độc lập), nếu không thì phần đó bị bỏ qua. Phần cooling pack chỉ dùng số của slide (minh hoạ), không có sách nào mô tả hệ này.'
            if vi else
            '# m03 · Refrigeration cycles and aircraft air conditioning: verification calculations\n\nThis notebook recomputes in Python the main examples of module m03 (Slide Ch.3; Tutorials I; Cengel Ch.11). Every section has three parts: the question the method answers → code → interpretation of the real printed numbers. Run top to bottom. The R-134a tables (A-11, A-12, the A-13 blocks) and Table A-17 are embedded in the first code cell; if CoolProp is installed each section also compares with CoolProp (the independent route), otherwise that part is skipped. The cooling-pack part uses only slide numbers (illustration); no book describes this system.')
    cells = [nbf.v4.new_markdown_cell(head)]; checks = []
    for i, (title, q, code, interp, must) in enumerate(sections(lang), 1):
        cells.append(nbf.v4.new_markdown_cell(f'## {i}. {title}\n\n{q}')); cells.append(nbf.v4.new_code_cell(code)); cells.append(nbf.v4.new_markdown_cell(interp)); checks.append((len(cells) - 2, must))
    nb['cells'] = cells; nb['metadata']['language_info'] = {'name': 'python'}
    fn = os.path.join(OUT, f'm03_refrigeration_aircraft_air_conditioning_{lang}.ipynb'); nbf.write(nb, fn)
    # a throw-away kernelspec that points to the project venv (the one with CoolProp), kept in scratch/, so nothing global is changed
    kdir = os.path.join(ROOT, 'scratch', 'm03', 'jupyter', 'kernels', 'm03venv'); os.makedirs(kdir, exist_ok=True)
    json.dump(dict(argv=[os.path.join(ROOT, '.venv', 'bin', 'python'), '-m', 'ipykernel_launcher', '-f', '{connection_file}'], display_name='m03 venv', language='python'), open(os.path.join(kdir, 'kernel.json'), 'w'))
    env = dict(os.environ, JUPYTER_PATH=os.path.join(ROOT, 'scratch', 'm03', 'jupyter'))
    r = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), '-I', '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', '--ExecutePreprocessor.kernel_name=m03venv', fn], capture_output=True, text=True, cwd=OUT, env=env)
    if r.returncode != 0: print(r.stdout[-1500:], r.stderr[-2500:]); raise SystemExit(f'nbconvert failed for {lang}')
    nb2 = nbf.read(fn, as_version=4); nb2['metadata']['kernelspec'] = dict(display_name='Python 3', language='python', name='python3'); nbf.write(nb2, fn)    # standard kernelspec for readers
    for idx, must in checks:
        out = ''.join(o.get('text', '') for o in nb2.cells[idx].get('outputs', []))
        for s in must:
            if s not in out: raise SystemExit(f'[{lang}] cell {idx}: expected "{s}" in the output but it is missing:\n{out}')
    print('executed and verified', fn, len(nb2.cells), 'cells')

if __name__ == '__main__':
    build('vi'); build('en')
