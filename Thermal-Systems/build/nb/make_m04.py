"""Build and execute the m04 notebooks (VI and EN).  Run: .venv/bin/python -I build/nb/make_m04.py
Each method section = markdown (question it answers) -> code -> markdown interpreting the REAL output (numbers in the interpretation are computed here with route A
(build/gen/m04_common.py) and then CHECKED against the executed output text: the build fails if they do not appear).
The notebook is self-contained: the property tables it uses (A-4, A-5, A-26, A-27, h and s0 columns of A-18...A-23, cp polynomials of A-2c, molar masses of A-1; all read from the page
images, data/props/*.json) are embedded in the first code cell.  The independent routes need sympy, scipy and iapws (the executed outputs here come from an environment that has them)."""
import os, sys, math, subprocess, json
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
from m04_common import *
from iapws import IAPWS97
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
D = lambda n: json.load(open(os.path.join(ROOT, 'data', 'props', n + '.json'), encoding='utf-8'))
GASN = dict(N2=18, O2=19, CO2=20, CO=21, H2=22, H2O=23)
ERR = D('book_errata')['errors']
def gastab(g):
    rows = [list(r) for r in D(f'A{GASN[g]}')['rows'] if 270 <= r[0] <= 2600]
    for e in ERR:                                       # s0 cells flagged as printed errors are replaced by their expected value (documented in the notebook)
        if e['table'] == f'A-{GASN[g]}' and e['col'] == 's0':
            for r in rows:
                if r[0] == e['key']['T_K']: r[3] = e['expected']
    return [[r[0], r[1], r[3]] for r in rows]
A5 = [[r[0], r[1]] for r in D('A5')['rows'] if r[0] <= 200]
A4 = [[r[0], r[1]] for r in D('A4')['rows'] if r[0] <= 100 and r[0] % 5 == 0]
F26 = {r[1]: r[2] for r in D('A26')['rows']}
A27 = {r[1]: dict(M=r[2], HHV=r[6], LHV=r[7]) for r in D('A27')['rows'] if r[1] in ('CH4', 'C2H6', 'C8H18', 'H2', 'C3H8')}
A2C = {r[1]: r[2:6] + [r[7]] for r in D('A2c')['rows'] if r[1] in ('N2', 'O2', 'CO2', 'CO', 'H2', 'H2O')}
HT = {g: gastab(g) for g in GASN}
f = lambda x, nd=2: f'{x:.{nd}f}'
fc = lambda x, nd=0: f'{x:,.{nd}f}'

PRELUDE = '''import math, numpy as np, sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from iapws import IAPWS97
# ---- tables read from the Appendix 1 page images (data/props/*.json), embedded so that the notebook is self-contained
A5 = np.array(%s)                      # A-5: Psat [kPa], Tsat [C]  (P <= 200 kPa)
A4 = np.array(%s)                      # A-4: T [C], Psat [kPa]     (5 C steps)
F26 = %s                               # A-26: enthalpy of formation h_f0 [kJ/kmol] at 25 C, 1 atm
A27 = %s                               # A-27: M [kg/kmol], HHV, LHV [kJ/kg]
A2C = %s                               # A-2c: cp = a + bT + cT^2 + dT^3 [kJ/(kmol K)] and Tmax
HT = %s                                # A-18..A-23: rows [T, h, s0] (h in kJ/kmol, s0 in kJ/(kmol K)), 270-2600 K; s0 cells flagged in book_errata.json replaced by the expected value
M_AIR_ROUND, M_AIR_EXACT = 29.0, 28.97 # slides round 28.97 (A-1) to 29
def Tsat_A5(P):  return float(np.interp(P, A5[:, 0], A5[:, 1]))                 # the book's method: linear interpolation
def Tsat_iapws(P): return IAPWS97(P=P / 1000.0, x=0).T - 273.15                    # independent route: IF97
def hbar(g, T):  tab = np.array(HT[g]); return float(np.interp(T, tab[:, 0], tab[:, 1]))
def sens_table(g, T): return hbar(g, T) - hbar(g, 298.0)                           # h(T) - h(298 K), table column h
_SP = {g: CubicSpline([r[0] for r in HT[g]], [r[2] for r in HT[g]]) for g in HT}
def sens_Tds(g, T): return T * float(_SP[g](T)) - 298.0 * float(_SP[g](298.0)) - quad(lambda t: float(_SP[g](t)), 298.0, T)[0]   # integral of T ds0 (s0 column)
def sens_poly(g, T):
    a, b, c, d, Tmax = A2C[g]; assert T <= Tmax; return a * (T - 298.0) + b / 2 * (T**2 - 298.0**2) + c / 3 * (T**3 - 298.0**3) + d / 4 * (T**4 - 298.0**4)
def comp_el(formula):
    import re; e = {'C': 0, 'H': 0, 'O': 0, 'N': 0}
    for el, n in re.findall(r'([A-Z])(\\d*)', formula): e[el] += int(n) if n else 1
    return e
def balance(formula, lam):
    """sympy: fuel + lam*a_th (O2 + 3.76 N2) -> nCO2 CO2 + nH2O H2O + nO2 O2 + nN2 N2 (exact rationals); returns kmol per kmol of fuel."""
    e = comp_el(formula); a, nc, nh, nn, no2 = sp.symbols('a nc nh nn no2'); r = sp.Rational(376, 100); lam = sp.nsimplify(lam)
    ath = sp.solve([sp.Eq(e['C'], nc), sp.Eq(e['H'], 2 * nh), sp.Eq(e['O'] + 2 * a, 2 * nc + nh), sp.Eq(e['N'] + 2 * r * a, 2 * nn)], [a, nc, nh, nn], dict=True)[0][a]
    s = sp.solve([sp.Eq(e['C'], nc), sp.Eq(e['H'], 2 * nh), sp.Eq(e['O'] + 2 * lam * ath, 2 * nc + nh + 2 * no2), sp.Eq(e['N'] + 2 * r * lam * ath, 2 * nn)], [nc, nh, no2, nn], dict=True)[0]
    return dict(ath=float(ath), CO2=float(s[nc]), H2O=float(s[nh]), O2=float(s[no2]), N2=float(s[nn]), air=float(lam * ath * (1 + r)))
''' % (json.dumps(A5), json.dumps(A4), json.dumps(F26), json.dumps(A27), json.dumps(A2C), json.dumps(HT))

def sections(lang):
    vi = lang == 'vi'
    tr = lambda a, b: a if vi else b
    dv = lambda s: s.replace('.', ',') if vi else s
    S = []      # (title, question_md, code, interpretation_md, [strings that must appear in stdout])
    # ---- numbers (route A)
    r1 = combustion(single('C8H18'), 20 / 12.5); AFx = 20 * 4.76 * 28.97 / 114.231
    r2 = combustion(single('C2H6'), 1.2); Pv2, T2 = dew_point(r2['H2O'], r2['n_tot'], 100.0); Ti2 = IAPWS97(P=Pv2 / 1000, x=0).T - 273.15
    import numpy as np
    amax = max(abs(float(np.interp(P, [r[0] for r in A5], [r[1] for r in A5])) - (IAPWS97(P=float(P) / 1000, x=0).T - 273.15)) for P in np.arange(7.5, 200.0, 0.25))
    rv = reverse(8, 18, 10.02, 0.88, 5.62, 83.48); Nw = condensed(rv['H2O'], rv['n_tot'], 100.0, 25.0)
    hCo = hC_nu('C8H18_l', dict(CO2=8, H2O=9), 'l'); LHVo = hC_nu('C8H18_l', dict(CO2=8, H2O=9), 'g'); Mo = A27row('C8H18', 'M'); hfg = IAPWS97(T=298.15, x=1).h - IAPWS97(T=298.15, x=0).h          # kJ/kg
    n2_55 = 0.95 * 7.5 * 3.76; q55 = q_out(dict(C6H6=1, O2=0.95 * 7.5, N2=n2_55), 298, dict(CO2=5.25, CO=0.75, H2O_g=3, N2=n2_55), 1000)
    def tad(fuel_key, comp, lam, T_r=298.0):
        r = combustion(single(comp), lam); Hr = Hstate({fuel_key: 1}, T_r) + Hstate({'O2': r['o2_in'], 'N2': r['n2_in']}, T_r); pr = {k: v for k, v in dict(CO2=r['CO2'], H2O_g=r['H2O'], O2=r['O2'], N2=r['N2']).items() if v > 0}
        lo, hi = 298.0, 3200.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if Hstate(pr, mid) > Hr: hi = mid
            else: lo = mid
        return (lo + hi) / 2
    T70 = tad('H2', 'H2', 1.2, 280.0); T1510 = tad('CH4', 'CH4', 1.5); T158 = tad('C8H18_l', 'C8H18', 1.0); Tfar = tad('CH4', 'CH4', 1.2)
    # ---- 1 balance
    S.append((tr('Cân bằng phương trình cháy bằng ma trận nguyên tố', 'Balancing the combustion equation with the element matrix'),
              tr('**Câu hỏi:** bốn cân bằng nguyên tố (C, H, O, N) cho nghiệm gì với octan cháy trong không khí chứa 20 kmol O₂ (slide tr.13–17), và AF khác nhau bao nhiêu khi M_air = 29 hay 28,97?', '**Question:** what do the four element balances (C, H, O, N) give for octane burned with air that contains 20 kmol of O₂ (slides p.13–17), and how much does AF change between M_air = 29 and 28.97?'),
              PRELUDE + '''x, y, z, w = sp.symbols('x y z w')
sol = sp.solve([sp.Eq(8, x), sp.Eq(18, 2 * y), sp.Eq(20 * 2, 2 * x + y + 2 * z), sp.Eq(20 * sp.Rational(376, 100), w)], [x, y, z, w], dict=True)[0]
print('x, y, z, w =', sol[x], sol[y], sol[z], sol[w], '| moles in:', 1 + 20 * sp.Rational(476, 100), '| moles out:', sum(sol.values()))
M_oct = A27['C8H18']['M']
AF29 = 20 * 4.76 * M_AIR_ROUND / (8 * 12 + 9 * 2); AFx = 20 * 4.76 * M_AIR_EXACT / M_oct
print(f"AF slide (29, 114) = {AF29:.2f} kg/kg; AF with 28.97 and {M_oct} = {AFx:.2f} kg/kg; difference {100 * (AF29 / AFx - 1):.2f} %")''',
              tr(f'**Đọc kết quả:** nghiệm (8; 9; 15/2; 376/5) = (8; 9; 7,5; 75,2) khớp slide tr.15–16. Số mol vào 96,2, ra 99,7: số mol không bảo toàn (tr.11). AF = {dv(f(r1["AF"]))} (slide 24,2) với 29 và 114; với 28,97 và 114,231 là {dv(f(AFx))}: slide làm tròn M_air, lệch {dv(f(100*(r1["AF"]/AFx-1)))} %.', f'**Reading the output:** the solution (8; 9; 15/2; 376/5) = (8; 9; 7.5; 75.2) matches slides p.15–16. Moles in 96.2, out 99.7: moles are not conserved (p.11). AF = {f(r1["AF"])} (slide 24.2) with 29 and 114; with 28.97 and 114.231 it is {f(AFx)}: the slide rounds M_air, a {f(100*(r1["AF"]/AFx-1))} % difference.'),
              ['x, y, z, w = 8 9 15/2 376/5', 'moles in: 481/5', 'moles out: 997/10', f'AF slide (29, 114) = {f(r1["AF"])} kg/kg', f'with 28.97 and 114.231 = {f(AFx)} kg/kg']))
    # ---- 2 AF vs excess air
    ths = {k: combustion(single(k), 1.0) for k in ('CH4', 'C3H8', 'C8H18')}
    S.append((tr('AF theo lượng không khí cho ba nhiên liệu', 'AF versus the air used for three fuels'),
              tr('**Câu hỏi:** AF thay đổi thế nào theo % không khí lý thuyết cho CH₄, C₃H₈, C₈H₁₈ (slide tr.21–25)? Dùng phép cân bằng sympy và so với công thức a_th = c + h/4.', '**Question:** how does AF change with the percent theoretical air for CH₄, C₃H₈, C₈H₁₈ (slides p.21–25)? Use the sympy balance and compare with the formula a_th = c + h/4.'),
              PRELUDE + '''M = dict(CH4=16.0, C3H8=44.0, C8H18=114.0)        # rounded masses (C = 12, H = 1) as on the slides
for fu in ('CH4', 'C3H8', 'C8H18'):
    e = comp_el(fu); line = []
    for lam in (1.0, 1.2, 1.5, 2.0):
        b = balance(fu, lam); af = b['air'] * M_AIR_ROUND / M[fu]; line.append(f"{lam * 100:.0f} %: AF {af:.2f}, O2 left {b['O2']:.2f}")
    print(fu, f"a_th = {balance(fu, 1.0)['ath']:.2f} (c + h/4 = {e['C'] + e['H'] / 4:.2f}) |", ' | '.join(line))''',
              tr(f'**Đọc kết quả:** a_th đúng bằng c + h/4 (2; 5; 12,5); AF = (% lý thuyết/100) × AF hợp thức: {dv(f(ths["CH4"]["AF"]))}; {dv(f(ths["C3H8"]["AF"]))}; {dv(f(ths["C8H18"]["AF"]))} kg/kg ở 100 %, tăng tuyến tính (hình trong module). O₂ dư bằng (λ − 1) a_th.', f'**Reading the output:** a_th equals c + h/4 (2; 5; 12.5); AF = (percent theoretical/100) × stoichiometric AF: {f(ths["CH4"]["AF"])}; {f(ths["C3H8"]["AF"])}; {f(ths["C8H18"]["AF"])} kg/kg at 100 %, growing linearly (figure in the module). The O₂ left over is (λ − 1) a_th.'),
              [f'a_th = 2.00 (c + h/4 = 2.00)', f'100 %: AF {f(ths["CH4"]["AF"])}', f'100 %: AF {f(ths["C8H18"]["AF"])}', '150 %: AF', f'a_th = 12.50']))
    # ---- 3 dew point
    S.append((tr('Điểm sương: nội suy A-5 và IAPWS (slide tr.27–32)', 'Dew point: A-5 interpolation versus IAPWS (slides p.27–32)'),
              tr('**Câu hỏi:** điểm sương của sản phẩm etan 20 % thừa ở 100 kPa là bao nhiêu, và nội suy tuyến tính bảng A-5 lệch bao nhiêu so với phương trình trạng thái?', '**Question:** what is the dew point of the products of ethane with 20 % excess air at 100 kPa, and how far does linear interpolation of Table A-5 deviate from the equation of state?'),
              PRELUDE + '''b = balance('C2H6', 1.2); n_prod = b['CO2'] + b['H2O'] + b['O2'] + b['N2']
Pv = b['H2O'] / n_prod * 100.0
print(f"N_prod = {n_prod:.2f} kmol; P_v = {Pv:.2f} kPa; T_dp (A-5 interpolation) = {Tsat_A5(Pv):.2f} C; T_dp (IAPWS) = {Tsat_iapws(Pv):.2f} C; slide 52.3")
err = max(abs(Tsat_A5(P) - Tsat_iapws(P)) for P in np.arange(7.5, 200.0, 0.25))
print(f"largest |A-5 interpolation - IAPWS| for P = 7.5...200 kPa: {err:.3f} C")''',
              tr(f'**Đọc kết quả:** N_prod = {dv(f(r2["n_tot"]))}; P_v = {dv(f(Pv2))} kPa; nội suy A-5 cho {dv(f(T2))} °C (slide làm tròn 52,3), IAPWS cho {dv(f(Ti2))} °C: lệch {dv(f(Ti2-T2))} °C là sai số nội suy tuyến tính trên hai hàng cách nhau 5 kPa. Trên 7,5–200 kPa lệch lớn nhất {dv(f(amax,3))} °C, vì vậy các câu hỏi điểm sương khai dung sai 0,5 °C.', f'**Reading the output:** N_prod = {f(r2["n_tot"])}; P_v = {f(Pv2)} kPa; A-5 interpolation gives {f(T2)} °C (slide rounds to 52.3), IAPWS gives {f(Ti2)} °C: the {f(Ti2-T2)} °C gap is the error of linear interpolation over two rows 5 kPa apart. Over 7.5–200 kPa the largest gap is {f(amax,3)} °C, so the dew-point questions declare a tolerance of 0.5 °C.'),
              [f'N_prod = {f(r2["n_tot"])} kmol', f'P_v = {f(Pv2)} kPa', f'(A-5 interpolation) = {f(T2)} C', f'(IAPWS) = {f(Ti2)} C', f'{f(amax,3)} C']))
    # ---- 4 reverse analysis
    S.append((tr('Phân tích cháy ngược từ thành phần khô (slide tr.33–39)', 'Reverse combustion analysis from the dry composition (slides p.33–39)'),
              tr('**Câu hỏi:** từ CO₂ 10,02 %, CO 0,88 %, O₂ 5,62 %, N₂ 83,48 % (khô) của octan, AF, phần trăm không khí lý thuyết và lượng nước ngưng ở 25 °C, 100 kPa là bao nhiêu? Slide làm tròn x = 1,36: ảnh hưởng gì?', '**Question:** from the dry composition CO₂ 10.02 %, CO 0.88 %, O₂ 5.62 %, N₂ 83.48 % of octane, what are the AF, the percent theoretical air and the water condensed at 25 °C, 100 kPa? The slide rounds x to 1.36: what does that change?'),
              PRELUDE + '''R = lambda v: sp.nsimplify(str(v), rational=True)
CO2, CO, O2, N2 = R(10.02), R(0.88), R(5.62), R(83.48)
x, a, b = sp.symbols('x a b')
s = sp.solve([sp.Eq(a * sp.Rational(376, 100), N2), sp.Eq(8 * x, CO2 + CO), sp.Eq(18 * x, 2 * b)], [x, a, b], dict=True)[0]
print(f"a = {float(s[a]):.4f}, x = {float(s[x]):.4f}, b = {float(s[b]):.4f}; O2 check: a - (CO2 + CO/2 + O2 + b/2) = {float(s[a] - (CO2 + CO/2 + O2 + s[b]/2)):.4f}")
air = float(s[a] / s[x]); AF = air * 4.76 * 29 / 114; pct = air / 12.5 * 100
print(f"O2 per kmol fuel = {air:.3f}; AF = {AF:.2f} kg/kg (slide 19.76); % theoretical = {pct:.1f} % (slide 131 %)")
Nv = float(s[b] / s[x]); Ntot = float((CO2 + CO + O2 + N2 + s[b]) / s[x]); y = IAPWS97(T=298.15, x=0).P * 1000 / 100.0
Nw = brentq(lambda w: (Nv - w) / (Ntot - w) - y, 0, Nv - 1e-9)
print(f"products {Ntot:.2f} kmol (slide 82.53); N_w = {Nw:.2f} kmol = {Nw / Nv * 100:.1f} % of the vapor (slide 6.59 kmol, 73 %)")''',
              tr(f'**Đọc kết quả:** a = {dv(f(rv["a"],4))}; x = {dv(f(rv["x"],4))} (slide 1,36); b = {dv(f(rv["b"],4))} (slide 12,24). Kiểm O₂ lệch {dv(f(abs(rv["resid"]),4))} do làm tròn thành phần. AF = {dv(f(rv["AF"]))} (slide 19,76), {dv(f(rv["pct"],1))} % lý thuyết (slide 131 %: 16,32/12,5 = 130,56 theo số của slide). N_w = {dv(f(Nw))} kmol ({dv(f(Nw/9*100,1))} %): khớp 6,59 kmol và 73 % của slide, giải bằng brentq với P_sat của IAPWS.', f'**Reading the output:** a = {f(rv["a"],4)}; x = {f(rv["x"],4)} (slide 1.36); b = {f(rv["b"],4)} (slide 12.24). The O₂ check is off by {f(abs(rv["resid"]),4)} because of the rounding of the composition. AF = {f(rv["AF"])} (slide 19.76), {f(rv["pct"],1)} % theoretical (slide 131 %: 16.32/12.5 = 130.56 with the slide numbers). N_w = {f(Nw)} kmol ({f(Nw/9*100,1)} %): matches the slide\'s 6.59 kmol and 73 %, solved with brentq and the IAPWS P_sat.'),
              [f'a = {f(rv["a"],4)}', f'x = {f(rv["x"],4)}', f'AF = {f(rv["AF"])} kg/kg', f'{f(rv["pct"],1)} %', f'N_w = {f(Nw)} kmol']))
    # ---- 5 enthalpy of combustion
    S.append((tr('Entanpi cháy từ entanpi hình thành, đối chiếu nhiệt trị A-27 (slide tr.53–54)', 'Enthalpy of combustion from the formation enthalpies, checked against the A-27 heating values (slides p.53–54)'),
              tr('**Câu hỏi:** h̄_C của octan lỏng (nước lỏng) là bao nhiêu, nhiệt trị cao/thấp theo kg là bao nhiêu và HHV − LHV có đúng bằng m·h_fg (h_fg từ IAPWS) không?', '**Question:** what is h̄_C of liquid octane (liquid water), what are the higher/lower heating values per kg, and is HHV − LHV exactly m·h_fg (h_fg from IAPWS)?'),
              PRELUDE + '''hf = F26
hC_l = 8 * hf['CO2(g)'] + 9 * hf['H2O(ᐉ)'] - hf['C8H18(ᐉ)']; hC_g = 8 * hf['CO2(g)'] + 9 * hf['H2O(g)'] - hf['C8H18(ᐉ)']
M = A27['C8H18']['M']
print(f"h_C (liquid H2O) = {hC_l:,.0f} kJ/kmol = {hC_l / M:,.0f} kJ/kg; A-27 HHV = {A27['C8H18']['HHV']:,.0f} kJ/kg")
print(f"h_C (H2O vapor) = {hC_g:,.0f} kJ/kmol = {hC_g / M:,.0f} kJ/kg; A-27 LHV = {A27['C8H18']['LHV']:,.0f} kJ/kg")
hfg = (IAPWS97(T=298.15, x=1).h - IAPWS97(T=298.15, x=0).h)
m_H2O = 9 * 18.015 / M
print(f"m h_fg = {m_H2O:.3f} kg/kg x {hfg:.1f} kJ/kg = {m_H2O * hfg:,.0f} kJ/kg; HHV - LHV (A-26) = {(hC_g - hC_l) / M:,.0f} kJ/kg; A-27: {A27['C8H18']['HHV'] - A27['C8H18']['LHV']:,.0f}")''',
              tr(f'**Đọc kết quả:** h̄_C = {dv(fc(hCo))} kJ/kmol (slide làm tròn −5 471 000) = {dv(fc(hCo/Mo))} kJ/kg; HHV A-27 = 47 890 (lệch 0,002 %). Với nước hơi: {dv(fc(LHVo/Mo))} kJ/kg (A-27 44 430). m·h_fg = 1,419 × {dv(f(hfg,1))} = {dv(fc(9*18.015/Mo*hfg))} kJ/kg, đúng bằng HHV − LHV của A-26 ({dv(fc((LHVo-hCo)/Mo))}).', f'**Reading the output:** h̄_C = {fc(hCo)} kJ/kmol (the slide rounds to −5,471,000) = {fc(hCo/Mo)} kJ/kg; A-27 HHV = 47,890 (0.002 % apart). With vapor water: {fc(LHVo/Mo)} kJ/kg (A-27 44,430). m·h_fg = 1.419 × {f(hfg,1)} = {fc(9*18.015/Mo*hfg)} kJ/kg, equal to HHV − LHV from A-26 ({fc((LHVo-hCo)/Mo)}).'),
              [f'h_C (liquid H2O) = {fc(hCo)} kJ/kmol = {fc(hCo/Mo)} kJ/kg', f'{fc(LHVo/Mo)} kJ/kg', f'{fc(9*18.015/Mo*hfg)} kJ/kg']))
    # ---- 6 sensible enthalpy
    d1 = sens('N2', 500.0)
    S.append((tr('Entanpi hiển nhiệt h̄(T) − h̄(298 K): bảng, tích phân T ds° và đa thức cp', 'Sensible enthalpy h̄(T) − h̄(298 K): table, integral of T ds° and cp polynomials'),
              tr('**Câu hỏi:** ví dụ tr.44 (N₂ ở 500 K: 14 581 − 8669 = 5912 kJ/kmol) có khớp tích phân T ds° trên chính các cột s° của bảng và đa thức cp của A-2c không?', '**Question:** does the example on p.44 (N₂ at 500 K: 14,581 − 8669 = 5912 kJ/kmol) agree with the integral of T ds° over the s° columns of the same tables and with the cp polynomials of A-2c?'),
              PRELUDE + '''print(f"N2 500 K: table {sens_table('N2', 500.0):.1f}; integral of T ds0 {sens_Tds('N2', 500.0):.1f}; A-2c polynomial {sens_poly('N2', 500.0):.1f} kJ/kmol")
for g, T in (('CO2', 1000.0), ('H2O', 1000.0), ('O2', 1500.0), ('N2', 1500.0)):
    t, i, p = sens_table(g, T), sens_Tds(g, T), sens_poly(g, T)
    print(f"{g:3s} {T:.0f} K: table {t:9.0f}; T ds0 {i:9.0f} ({100 * (i / t - 1):+.2f} %); polynomial {p:9.0f} ({100 * (p / t - 1):+.2f} %)")''',
              tr(f'**Đọc kết quả:** N₂ ở 500 K: bảng {dv(f(d1,1))} (slide 5912), tích phân T ds° cho giá trị gần như trùng (hai cột h và s° của bảng nhất quán), đa thức cp lệch dưới 1 % (A-2c tự khai sai số lớn nhất 0,6–1,2 %). Vì vậy đường chính dùng cột h; hai đường kia là kiểm độc lập.', f'**Reading the output:** N₂ at 500 K: table {f(d1,1)} (slide 5912), the integral of T ds° gives almost the same value (the h and s° columns of the table are consistent), the cp polynomial is within 1 % (A-2c declares a maximum error of 0.6–1.2 %). The main route therefore uses the h column; the other two are independent checks.'),
              [f'N2 500 K: table {f(d1,1)}', 'CO2 1000 K: table', 'polynomial']))
    # ---- 7 first law
    S.append((tr('Định luật 1 cho buồng đốt: Cengel 15–55 (bổ sung §15-4)', 'First law for a combustor: Cengel 15–55 (added §15-4)'),
              tr('**Câu hỏi:** benzen khí cháy với 95 % không khí lý thuyết, sản phẩm ra ở 1000 K (một phần C thành CO): nhiệt truyền ra khỏi buồng đốt là bao nhiêu và có khớp 2 112 800 kJ/kmol in của sách không?', '**Question:** gaseous benzene burns with 95 % theoretical air, the products leave at 1000 K (part of the carbon becomes CO): how much heat leaves the combustor, and does it match the printed 2,112,800 kJ/kmol of the book?'),
              PRELUDE + '''hf = F26; n2 = 0.95 * 7.5 * 3.76
# C6H6 + 7.125 (O2 + 3.76 N2) -> x CO2 + y CO + 3 H2O + n2 N2 ; O: 14.25 = 2x + y + 3, x + y = 6
x, y = sp.symbols('x y'); s = sp.solve([sp.Eq(x + y, 6), sp.Eq(2 * x + y + 3, sp.Rational(1425, 100))], [x, y], dict=True)[0]
xc, yc = float(s[x]), float(s[y]); print('x (CO2), y (CO) =', xc, yc, f'; y_CO = {yc / (xc + yc + 3 + n2) * 100:.2f} %')
prod = [('CO2', xc, 'CO2(g)'), ('CO', yc, 'CO(g)'), ('H2O', 3.0, 'H2O(g)'), ('N2', n2, 'N2(g)')]
for tag, sens in (('table h column', sens_table), ('integral of T ds0', sens_Tds)):
    Hp = sum(n * (hf[k] + sens(g, 1000.0)) for g, n, k in prod); Q = hf['C6H6(g)'] - Hp
    print(f"{tag:18s}: H_prod = {Hp:,.0f}; Q_out = {Q:,.0f} kJ/kmol  (printed 2,112,800; difference {100 * (Q / 2112800 - 1):+.4f} %)")''',
              tr(f'**Đọc kết quả:** x = 5,25; y = 0,75 ⇒ y_CO = 2,10 % (in 2,1 %). Q_ra = {dv(fc(q55))} kJ/kmol bằng cột h của bảng, chênh {dv(f(abs(q55-2112800)/2112800*100,4))} % so với 2 112 800 in; tích phân T ds° (cột s°) cho kết quả trùng trong 0,01 %. Đã thử cùng đường giải trên 15–56, 15–60, 15–67, 15–70 trước khi dùng cho 15–53 (không có đáp án in).', f'**Reading the output:** x = 5.25; y = 0.75 ⇒ y_CO = 2.10 % (printed 2.1 %). Q_out = {fc(q55)} kJ/kmol from the h column of the table, {f(abs(q55-2112800)/2112800*100,4)} % from the printed 2,112,800; the integral of T ds° (s° column) agrees within 0.01 %. The same route was tested on 15–56, 15–60, 15–67, 15–70 before being used for 15–53 (no printed answer).'),
              ['x (CO2), y (CO) = 5.25 0.75', 'y_CO = 2.10 %', f'Q_out = {fc(q55)} kJ/kmol']))
    # ---- 8 adiabatic flame temperature
    S.append((tr('Nhiệt độ ngọn lửa đoạn nhiệt: Cengel 15–70, Ví dụ 15–10 và Farokhi Ví dụ 7.5 (bổ sung)', 'Adiabatic flame temperature: Cengel 15–70, Example 15–10 and Farokhi Example 7.5 (added)'),
              tr('**Câu hỏi:** giải H_prod(T) = H_react bằng brentq với h̄(T) từ bảng (nội suy) và từ tích phân T ds°: kết quả có khớp 2251,4 K (15–70) và 1789 K (Ví dụ 15–10) in của sách không? Với c̄_p không đổi như Farokhi Ví dụ 7.5 (CH₄, 120 % không khí) thì ra bao nhiêu so với bảng?', '**Question:** solve H_prod(T) = H_react with brentq using h̄(T) from the table (interpolation) and from the integral of T ds°: do the results match the printed 2251.4 K (15–70) and 1789 K (Example 15–10)? With constant c̄_p as in Farokhi Example 7.5 (CH₄, 120 % air), what does one get compared with the tables?'),
              PRELUDE + '''hf = F26
def Tad(react, prod, sens):
    Hr = sum(n * (hf[k] + (sens(g, Tr) if g else 0.0)) for g, n, k, Tr in react)
    return brentq(lambda T: sum(n * (hf[k] + (sens(g, T) if g else 0.0)) for g, n, k in prod) - Hr, 300.0, 3200.0, xtol=1e-6)
# 15-70: H2 at 7 C (280 K) with 20 % excess air at 280 K -> H2O + 0.1 O2 + 2.256 N2
r70 = [('H2', 1.0, 'H2(g)', 280.0), ('O2', 0.6, 'O2(g)', 280.0), ('N2', 0.6 * 3.76, 'N2(g)', 280.0)]; p70 = [('H2O', 1.0, 'H2O(g)'), ('O2', 0.1, 'O2(g)'), ('N2', 0.6 * 3.76, 'N2(g)')]
# Example 15-10: CH4 + 3 (O2 + 3.76 N2) -> CO2 + 2 H2O + O2 + 11.28 N2 at 25 C
r10 = [(None, 1.0, 'CH4(g)', 298.0), ('O2', 3.0, 'O2(g)', 298.0), ('N2', 11.28, 'N2(g)', 298.0)]; p10 = [('CO2', 1.0, 'CO2(g)'), ('H2O', 2.0, 'H2O(g)'), ('O2', 1.0, 'O2(g)'), ('N2', 11.28, 'N2(g)')]
# Farokhi Example 7.5: CH4 + 2.4 (O2 + 3.76 N2) -> CO2 + 2 H2O + 0.4 O2 + 9.02 N2 at 25 C; constant cp 61.9, 52.3, 37.8, 33.6 kJ/(kmol K) and h_f(CH4) = -74,873
r75 = [(None, 1.0, 'CH4(g)', 298.0), ('O2', 2.4, 'O2(g)', 298.0), ('N2', 2.4 * 3.76, 'N2(g)', 298.0)]; p75 = [('CO2', 1.0, 'CO2(g)'), ('H2O', 2.0, 'H2O(g)'), ('O2', 0.4, 'O2(g)'), ('N2', 2.4 * 3.76, 'N2(g)')]
for tag, rr, pp, printed in (('Cengel 15-70', r70, p70, '2251.4'), ('Cengel Ex 15-10', r10, p10, '1789'), ('Farokhi Ex 7.5 (tables)', r75, p75, '1953 with constant cp')):
    print(f"{tag:24s}: table h {Tad(rr, pp, sens_table):7.1f} K | integral of T ds0 {Tad(rr, pp, sens_Tds):7.1f} K | printed {printed}")
cpsum = 61.9 + 2 * 52.3 + 0.4 * 37.8 + 9.02 * 33.6; dH = 393522 + 2 * 241827 - 74873
print(f"Farokhi constant-cp route: sum n cp = {cpsum:.1f}; T = 298 + {dH:,.0f}/{cpsum:.1f} = {298 + dH / cpsum:.0f} K")''',
              tr(f'**Đọc kết quả:** 15–70: {dv(f(T70,1))} K (in 2251,4); Ví dụ 15–10: {dv(f(T1510,0))} K (in 1789): cả hai khớp. Tích phân T ds° cho cùng nhiệt độ trong vài phần nghìn. Với CH₄, 120 % không khí, bảng cho {dv(f(Tfar,0))} K còn đường c̄_p không đổi của Farokhi cho 1953 K: c̄_p lấy gần 300 K đánh giá thấp nhiệt độ khoảng {dv(f(Tfar-1953,0))} K. Phân ly (slide tr.8) còn làm nhiệt độ thực thấp hơn nữa.', f'**Reading the output:** 15–70: {f(T70,1)} K (printed 2251.4); Example 15–10: {f(T1510,0)} K (printed 1789): both match. The integral of T ds° gives the same temperature within a few parts per thousand. For CH₄ with 120 % air the tables give {f(Tfar,0)} K while Farokhi\'s constant-c̄_p route gives 1953 K: constant c̄_p values taken near room temperature underestimate the temperature by about {f(Tfar-1953,0)} K. Dissociation (slide p.8) lowers the real temperature further.'),
              [f'Cengel 15-70', f'{f(T70,1)} K', f'{f(T1510,0)}', 'Farokhi constant-cp route: sum n cp = 484.7']))
    return S

def build(lang):
    vi = lang == 'vi'
    nb = nbf.v4.new_notebook()
    head = ('# m04 · Nhiên liệu và quá trình cháy: các phép tính kiểm chứng\n\nSổ tay này tính lại bằng Python các ví dụ chính của module m04 (Slide Ch.4; Cengel Ch.15; Farokhi Ch.7; El-Sayed Ch.10). Mỗi mục có ba phần: câu hỏi mà phương pháp trả lời → mã → diễn giải số in thật. Chạy từ trên xuống. Các bảng A-4, A-5, A-26, A-27 và các cột h, s° của A-18…A-23 (đọc từ ảnh trang phụ lục) được nhúng ở ô mã đầu; đường độc lập dùng sympy, scipy và iapws. Phần định luật 1 và nhiệt độ ngọn lửa đoạn nhiệt là Bổ sung từ sách (không có trên slide).'
            if vi else
            '# m04 · Fuels and the combustion process: verification calculations\n\nThis notebook recomputes in Python the main examples of module m04 (Slide Ch.4; Cengel Ch.15; Farokhi Ch.7; El-Sayed Ch.10). Every section has three parts: the question the method answers → code → interpretation of the real printed numbers. Run from top to bottom. Tables A-4, A-5, A-26, A-27 and the h and s° columns of A-18…A-23 (read from the Appendix page images) are embedded in the first code cell; the independent routes use sympy, scipy and iapws. The first-law and adiabatic-flame-temperature parts are Added from the book (not on the slides).')
    cells = [nbf.v4.new_markdown_cell(head)]; checks = []
    for i, (title, q, code, interp, must) in enumerate(sections(lang), 1):
        cells.append(nbf.v4.new_markdown_cell(f'## {i}. {title}\n\n{q}')); cells.append(nbf.v4.new_code_cell(code)); cells.append(nbf.v4.new_markdown_cell(interp)); checks.append((len(cells) - 2, must))
    nb['cells'] = cells; nb['metadata']['language_info'] = {'name': 'python'}
    fn = os.path.join(OUT, f'm04_fuels_and_combustion_{lang}.ipynb'); nbf.write(nb, fn)
    kdir = os.path.join(ROOT, 'scratch', 'm04', 'jupyter', 'kernels', 'm04venv'); os.makedirs(kdir, exist_ok=True)
    json.dump(dict(argv=[os.path.join(ROOT, '.venv', 'bin', 'python'), '-m', 'ipykernel_launcher', '-f', '{connection_file}'], display_name='m04 venv', language='python'), open(os.path.join(kdir, 'kernel.json'), 'w'))
    env = dict(os.environ, JUPYTER_PATH=os.path.join(ROOT, 'scratch', 'm04', 'jupyter'))
    r = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), '-I', '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', '--ExecutePreprocessor.kernel_name=m04venv', fn], capture_output=True, text=True, cwd=OUT, env=env)
    if r.returncode != 0: print(r.stdout[-1500:], r.stderr[-2500:]); raise SystemExit(f'nbconvert failed for {lang}')
    nb2 = nbf.read(fn, as_version=4); nb2['metadata']['kernelspec'] = dict(display_name='Python 3', language='python', name='python3'); nbf.write(nb2, fn)
    for idx, must in checks:
        out = ''.join(o.get('text', '') for o in nb2.cells[idx].get('outputs', []))
        for s in must:
            if s not in out: raise SystemExit(f'[{lang}] cell {idx}: expected "{s}" in the output but it is missing:\n{out}')
    print('executed and verified', fn, len(nb2.cells), 'cells')

if __name__ == '__main__':
    build('vi'); build('en')
