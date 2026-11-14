"""Build and execute the m02 notebooks (VI and EN).  Run: .venv/bin/python -I build/nb/make_m02.py
Each method section = markdown (question it answers) -> code -> markdown interpreting the REAL output (numbers in the interpretation are computed here with route A
(build/gen/m02_common.py) and then CHECKED against the executed output text: the build fails if they do not appear).
The notebook is self-contained: the Table A-17 rows (read from the page image, data/props/A17.json) are embedded in the first code cell."""
import os, sys, math, subprocess, json
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
from m02_common import (otto, otto_var, diesel, brayton, brayton_var, multistage_var, ideal_jet_k, turbojet_unchoked, rp_opt, A, CP_AIR, CV_AIR)
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
f = lambda x, nd=2: f'{x:.{nd}f}'
A17 = [r for r in json.load(open(os.path.join(ROOT, 'data', 'props', 'A17.json'), encoding='utf-8'))['rows'] if r[0] <= 1800]

PRELUDE = '''import math, numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
R = 0.287                                    # kJ/(kg K), Table A-1
# Table A-17 (air, ideal gas), rows read from the page image: T [K], h [kJ/kg], P_r, u [kJ/kg], v_r, s0
A17 = np.array(%s)
COL = dict(T=0, h=1, Pr=2, u=3, vr=4, s0=5)
def tab(col, T):                             # value of a column at temperature T (linear interpolation, as a student does)
    return float(np.interp(T, A17[:, 0], A17[:, COL[col]]))
def inv(col, val):                           # temperature at which a column has the value val
    x = A17[:, COL[col]]; T = A17[:, 0]
    return float(np.interp(val, x, T)) if x[0] < x[-1] else float(np.interp(val, x[::-1], T[::-1]))
''' % json.dumps(A17)

def sections(lang):
    vi = lang == 'vi'
    tr = lambda a, b: a if vi else b
    S = []      # (title, question_md, code, interpretation_md, [strings that must appear in stdout])
    o1 = otto_var(8, 290, 100, qin=800); oc = otto(8, 290, 100, qin=800)
    S.append((tr('Otto với nhiệt dung thay đổi (Tutorials I #1)', 'Otto with variable specific heats (Tutorials I #1)'),
              tr('**Câu hỏi:** chu trình Otto r = 8, 100 kPa, 290 K, q_in = 800 kJ/kg: T₃, P₃, w_net, η, MEP tính bằng bảng A-17 khác công thức khí lạnh bao nhiêu?', '**Question:** Otto cycle r = 8, 100 kPa, 290 K, q_in = 800 kJ/kg: how far are T₃, P₃, w_net, η and MEP from the cold-air formulas when computed with Table A-17?'),
              PRELUDE + '''r, T1, P1, qin = 8.0, 290.0, 100.0, 800.0
u1, vr1 = tab('u', T1), tab('vr', T1)
T2 = inv('vr', vr1 / r); u2 = tab('u', T2)                      # isentropic compression: v_r2 = v_r1 / r
T3 = inv('u', u2 + qin); vr3 = tab('vr', T3)                    # constant volume: u3 = u2 + q_in
T4 = inv('vr', vr3 * r); u4 = tab('u', T4)                      # isentropic expansion: v_r4 = r v_r3
P3 = P1 * (T3 / T1) * r
qout = u4 - u1; wnet = qin - qout; v1 = R * T1 / P1
print(f"T2 = {T2:.1f} K, T3 = {T3:.1f} K, T4 = {T4:.1f} K, P3 = {P3:.0f} kPa")
print(f"q_out = {qout:.2f}, w_net = {wnet:.2f} kJ/kg, eta = {wnet/qin:.3f}, MEP = {wnet/(v1*(1-1/r)):.0f} kPa")
k, cv = 1.4, 0.718                                              # cold air
T3c = T1 * r**(k-1) + qin / cv
print(f"cold air: T3 = {T3c:.1f} K, eta = {1 - r**(1-k):.3f}")''',
              tr(f'**Đọc kết quả:** bảng cho T₃ = {f(o1["T3"],1)} K, P₃ = {f(o1["P3"],0)} kPa, w_net = {f(o1["wnet"],2)} kJ/kg, η = {f(o1["eta"],3)}, MEP = {f(o1["mep"],0)} kPa: đúng đáp số slide Tutorials I (1575,1 K; 4,345 MPa; 418,17; 52,3 %; 574 kPa). Khí lạnh cho T₃ = {f(oc["T3"],1)} K và η = {f(1-8**-.4,3)}: c_v thật nhỏ hơn 0,718 ở nhiệt độ thấp và lớn hơn ở nhiệt độ cao nên hiệu suất thật thấp hơn.',
                 f'**Reading the output:** the table gives T₃ = {f(o1["T3"],1)} K, P₃ = {f(o1["P3"],0)} kPa, w_net = {f(o1["wnet"],2)} kJ/kg, η = {f(o1["eta"],3)}, MEP = {f(o1["mep"],0)} kPa: the slide answers of Tutorials I (1575.1 K; 4.345 MPa; 418.17; 52.3 %; 574 kPa). Cold air gives T₃ = {f(oc["T3"],1)} K and η = {f(1-8**-.4,3)}: the real c_v is below 0.718 at low temperature and above it at high temperature, so the real efficiency is lower.'),
              [f'T3 = {o1["T3"]:.1f} K', f'eta = {o1["eta"]:.3f}', f'MEP = {o1["mep"]:.0f} kPa', f'{oc["T3"]:.1f}']))
    d6 = diesel(20, 293, 95, cp=CP_AIR, cv=CV_AIR, T3=2200)
    S.append((tr('Diesel khí lạnh: công thức đóng và tích phân ∮P dV (Tutorials I #6)', 'Cold-air Diesel: closed form versus the ∮P dV integral (Tutorials I #6)'),
              tr('**Câu hỏi:** động cơ diesel r = 20, 95 kPa, 293 K, T_max = 2200 K: r_c, η, MEP; công thức hiệu suất có khớp công thức tích phân ∮P dV không?', '**Question:** a diesel engine r = 20, 95 kPa, 293 K, T_max = 2200 K: r_c, η, MEP; does the efficiency formula agree with the ∮P dV integral?'),
              '''import math
from scipy.integrate import quad
k, R, cp, cv = 1.4, 0.287, 1.005, 0.718
r, T1, P1, T3 = 20.0, 293.0, 95.0, 2200.0
T2 = T1 * r**(k-1); rc = T3 / T2
qin = cp * (T3 - T2); T4 = T3 * (rc / r)**(k-1); qout = cv * (T4 - T1); w = qin - qout; v1 = R * T1 / P1
eta_formula = 1 - r**(1-k) * (rc**k - 1) / (k * (rc - 1))
# route B: net work from the integral of P dv along the four processes
v2 = v1 / r; v3 = rc * v2; P2 = R * T2 / v2
w12 = quad(lambda v: P1 * v1**k / v**k, v1, v2)[0]               # isentropic compression (negative)
w23 = P2 * (v3 - v2)                                              # isobaric heat addition
w34 = quad(lambda v: P2 * v3**k / v**k, v3, v1)[0]                # isentropic expansion
wint = w12 + w23 + w34
print(f"T2 = {T2:.1f} K, r_c = {rc:.3f}, T4 = {T4:.1f} K")
print(f"eta (heats) = {w/qin:.4f}, eta (r_c formula) = {eta_formula:.4f}, eta (integral) = {wint/qin:.4f}")
print(f"w_net = {w:.1f} kJ/kg (heats) vs {wint:.1f} kJ/kg (integral); MEP = {w/(v1*(1-1/r)):.1f} kPa")''',
              tr(f'**Đọc kết quả:** r_c = {f(d6["rc"],3)}; η = {f(d6["eta"],4)} theo cả ba cách (hiệu nhiệt, công thức r_c, tích phân); khác biệt nhỏ ở công thực ({f(d6["wnet"],1)} kJ/kg so với tích phân) do R/(k−1) = 0,7175 chứ không phải 0,718 (làm tròn hằng số của sách). MEP = {f(d6["mep"],1)} kPa (sách 933).',
                 f'**Reading the output:** r_c = {f(d6["rc"],3)}; η = {f(d6["eta"],4)} by all three routes (heat difference, r_c formula, integral); the small difference in the net work ({f(d6["wnet"],1)} kJ/kg versus the integral) is because R/(k−1) = 0.7175, not 0.718 (rounded book constants). MEP = {f(d6["mep"],1)} kPa (book 933).'),
              [f'r_c = {d6["rc"]:.3f}', f'eta (r_c formula) = {d6["eta_formula"]:.4f}', f'MEP = {d6["mep"]:.1f} kPa']))
    bB = brayton_var(8, 300, 1300); bK = brayton(8, 300, 1300)
    S.append((tr('Brayton lý tưởng: bảng A-17 và đa thức c_p(T) của bảng A-2c (Tutorials I)', 'Ideal Brayton: Table A-17 versus the c_p(T) polynomial of Table A-2c (Tutorials I)'),
              tr('**Câu hỏi:** r_p = 8, 300 K và 1300 K: T₂, T₄, r_bw, η tính bằng bảng A-17 so với tích phân c_p(T) của đa thức A-2c (đường độc lập), và so với khí lạnh.', '**Question:** r_p = 8, 300 K and 1300 K: T₂, T₄, r_bw and η from Table A-17 versus the integral of c_p(T) from the A-2c polynomial (an independent route), and versus cold air.'),
              PRELUDE + '''rp, T1, T3 = 8.0, 300.0, 1300.0
# route A: Table A-17
T2 = inv('Pr', rp * tab('Pr', T1)); T4 = inv('Pr', tab('Pr', T3) / rp)
wc = tab('h', T2) - tab('h', T1); wt = tab('h', T3) - tab('h', T4); qin = tab('h', T3) - tab('h', T2)
print(f"table A-17: T2 = {T2:.1f} K, T4 = {T4:.1f} K, w_comp = {wc:.2f}, w_turb = {wt:.2f}, r_bw = {wc/wt:.4f}, eta = {(wt-wc)/qin:.4f}")
# route B: cp(T) = (a + bT + cT^2 + dT^3)/M, Table A-2c (air, 273-1800 K); isentrope: int cp/T dT = R ln(rp)
a, b, c, d, M = 28.11, 0.001967, 4.802e-6, -1.966e-9, 28.97
cp = lambda T: (a + b*T + c*T**2 + d*T**3) / M
h = lambda T1_, T2_: quad(cp, T1_, T2_)[0]
phi = lambda T1_, T2_: quad(lambda T: cp(T)/T, T1_, T2_)[0]
T2p = brentq(lambda T: phi(T1, T) - R*math.log(rp), T1, 1000)
T4p = brentq(lambda T: phi(T, T3) - R*math.log(rp), 300, T3)
wcp, wtp, qinp = h(T1, T2p), h(T4p, T3), h(T2p, T3)
print(f"polynomial: T2 = {T2p:.1f} K, T4 = {T4p:.1f} K, w_comp = {wcp:.2f}, w_turb = {wtp:.2f}, r_bw = {wcp/wtp:.4f}, eta = {(wtp-wcp)/qinp:.4f}")
print(f"cold air k = 1.4: eta = {1 - rp**(-0.4/1.4):.4f}, r_bw = {T1*rp**(0.4/1.4)/T3:.4f}")''',
              tr(f'**Đọc kết quả:** bảng A-17 cho T₂ = {f(bB["T2"],1)} K, T₄ = {f(bB["T4"],1)} K, r_bw = {f(bB["bwr"],4)}, η = {f(bB["eta"],4)}; đa thức A-2c cho cùng kết quả trong khoảng 1 %. Slide làm tròn T₂ = 540 K nên in r_bw = 0,403 thay cho {f(bB["bwr"],4)}. Khí lạnh cho η = {f(bK["eta"],4)}, cao hơn khoảng 2 điểm %.',
                 f'**Reading the output:** Table A-17 gives T₂ = {f(bB["T2"],1)} K, T₄ = {f(bB["T4"],1)} K, r_bw = {f(bB["bwr"],4)}, η = {f(bB["eta"],4)}; the A-2c polynomial agrees within about 1 %. The slide rounds T₂ to 540 K and prints r_bw = 0.403 instead of {f(bB["bwr"],4)}. Cold air gives η = {f(bK["eta"],4)}, about 2 percentage points higher.'),
              [f'T2 = {bB["T2"]:.1f} K', f'r_bw = {bB["bwr"]:.4f}', f'eta = {bB["eta"]:.4f}', f'{bK["eta"]:.4f}']))
    e6 = brayton_var(8, 300, 1300, .8, .85); e7 = brayton_var(8, 300, 1300, .8, .85, .8)
    S.append((tr('Brayton thực và hồi nhiệt (Cengel Ví dụ 9–6, 9–7)', 'Real Brayton and regeneration (Cengel Examples 9–6, 9–7)'),
              tr('**Câu hỏi:** thêm η_c = 80 %, η_t = 85 % rồi bộ hồi nhiệt ε = 80 %: r_bw, η, T₄ₐ, h₅ thay đổi thế nào?', '**Question:** add η_c = 80 %, η_t = 85 % and then a regenerator ε = 80 %: how do r_bw, η, T₄ₐ and h₅ change?'),
              PRELUDE + '''rp, T1, T3, ec, et, eps = 8.0, 300.0, 1300.0, 0.80, 0.85, 0.80
h1 = tab('h', T1); T2s = inv('Pr', rp * tab('Pr', T1)); h3 = tab('h', T3); T4s = inv('Pr', tab('Pr', T3) / rp)
wc = (tab('h', T2s) - h1) / ec; wt = et * (h3 - tab('h', T4s))     # isentropic efficiencies
h2 = h1 + wc; h4 = h3 - wt; wnet = wt - wc
print(f"w_comp = {wc:.2f}, w_turb = {wt:.2f} kJ/kg, r_bw = {wc/wt:.3f}, T2a = {inv('h', h2):.0f} K, T4a = {inv('h', h4):.0f} K")
print(f"without regenerator: q_in = {h3-h2:.2f}, eta = {wnet/(h3-h2):.3f}")
h5 = h2 + eps * (h4 - h2)                                          # effectiveness: (h5 - h2)/(h4 - h2)
print(f"with regenerator: h5 = {h5:.2f}, q_in = {h3-h5:.2f}, eta = {wnet/(h3-h5):.3f}")''',
              tr(f'**Đọc kết quả:** máy nén thực ăn {f(e6["bwr"]*100,1)} % công tuabin (lý tưởng {f(bB["bwr"]*100,1)} %); η rơi từ {f(bB["eta"],3)} xuống {f(e6["eta"],3)}; T₄ₐ = {f(e6["T4"],0)} K cao hơn T₂ₐ = {f(e6["T2"],0)} K nên hồi nhiệt có ích: h₅ = {f(e7["h5"],2)} và η = {f(e7["eta"],3)} (sách: 0,592; 26,6 %; 825,37; 36,9 %).',
                 f'**Reading the output:** the real compressor takes {f(e6["bwr"]*100,1)} % of the turbine work (ideal {f(bB["bwr"]*100,1)} %); η falls from {f(bB["eta"],3)} to {f(e6["eta"],3)}; T₄ₐ = {f(e6["T4"],0)} K is above T₂ₐ = {f(e6["T2"],0)} K so regeneration helps: h₅ = {f(e7["h5"],2)} and η = {f(e7["eta"],3)} (book: 0.592; 26.6 %; 825.37; 36.9 %).'),
              [f'r_bw = {e6["bwr"]:.3f}', f'eta = {e6["eta"]:.3f}', f'h5 = {e7["h5"]:.2f}', f'eta = {e7["eta"]:.3f}']))
    ro = rp_opt(1000, 300); bo = brayton(ro, 300, 1000)
    S.append((tr('r_p cho công cực đại: công thức, tối ưu số và nhiệt dung thay đổi (slide tr.40)', 'r_p for maximum work: formula, numerical optimum and variable specific heats (slide p.40)'),
              tr('**Câu hỏi:** với T_min = 300 K, T_max = 1000 K, r_p = 8,2 của slide đúng với giả thiết nào, và công thực phẳng cỡ nào quanh cực đại?', '**Question:** with T_min = 300 K and T_max = 1000 K, under which assumption is the slide\'s r_p = 8.2 right, and how flat is the net work around the maximum?'),
              '''import math
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
k, cp, R = 1.4, 1.005, 0.287
T1, T3 = 300.0, 1000.0
wnet_k = lambda rp: cp*(T3 - T1*rp**((k-1)/k)) - cp*(T3/rp**((k-1)/k) - T1)      # w_turb - w_comp
r_formula = (T3/T1)**(k/(2*(k-1)))
r_num = minimize_scalar(lambda x: -wnet_k(x), bounds=(2, 40), method='bounded', options=dict(xatol=1e-9)).x
print(f"formula {r_formula:.3f}; numerical {r_num:.3f}; w_net,max = {wnet_k(r_num):.1f} kJ/kg; w(8.2)/w_max = {wnet_k(8.2)/wnet_k(r_num):.4f}")
# variable cp: polynomial of Table A-2c
a, b, c, d, M = 28.11, 0.001967, 4.802e-6, -1.966e-9, 28.97
cpT = lambda T: (a + b*T + c*T**2 + d*T**3) / M
h = lambda x, y: quad(cpT, x, y)[0]
phi = lambda x, y: quad(lambda T: cpT(T)/T, x, y)[0]
def wnet_v(rp):
    T2 = brentq(lambda T: phi(T1, T) - R*math.log(rp), T1, 1000); T4 = brentq(lambda T: phi(T, T3) - R*math.log(rp), 300, T3)
    return h(T4, T3) - h(T1, T2)
r_v = minimize_scalar(lambda x: -wnet_v(x), bounds=(3, 30), method='bounded', options=dict(xatol=1e-6)).x
print(f"variable c_p (polynomial): r_p,opt = {r_v:.2f}; w(8.2)/w_max = {wnet_v(8.2)/wnet_v(r_v):.4f}")
for rp in (2, 8.2, 15):
    print(f"r_p = {rp:5.1f}: eta = {1 - rp**(-(k-1)/k):.3f}, w_net = {wnet_k(rp):6.1f} kJ/kg")''',
              tr(f'**Đọc kết quả:** r_p = 8,2 của slide là nghiệm của k = 1,4 hằng ({f(ro,3)}); với c_p(T) cực đại dịch lên khoảng 9,1 nhưng công thực rất phẳng (tỉ số 0,998), nên 8,2 vẫn gần tối ưu. Ở r_p = 8,2: η = {f(bo["eta"],3)}, w_net = {f(bo["wnet"],1)} kJ/kg; hiệu suất cực đại và công cực đại không trùng nhau.',
                 f'**Reading the output:** the slide\'s r_p = 8.2 is the constant k = 1.4 optimum ({f(ro,3)}); with c_p(T) the maximum moves to about 9.1 but the net work is very flat (ratio 0.998), so 8.2 stays near-optimal. At r_p = 8.2: η = {f(bo["eta"],3)}, w_net = {f(bo["wnet"],1)} kJ/kg; the maximum efficiency and the maximum work do not coincide.'),
              [f'formula {ro:.3f}', f'w_net,max = {bo["wnet"]:.1f} kJ/kg']))
    m0 = multistage_var(8, 2, 300, 1300, 0); m1 = multistage_var(8, 2, 300, 1300, 1)
    S.append((tr('Hai cấp nén và giãn, làm mát trung gian, hâm nóng, hồi nhiệt (Cengel Ví dụ 9–8)', 'Two compression and expansion stages with intercooling, reheating and regeneration (Cengel Example 9–8)'),
              tr('**Câu hỏi:** r_p = 8 chia hai cấp (√8 mỗi cấp), 300 K và 1300 K: r_bw và η không hồi nhiệt và với hồi nhiệt lý tưởng khác chu trình một cấp thế nào?', '**Question:** r_p = 8 split into two stages (√8 each), 300 K and 1300 K: how do r_bw and η, without and with an ideal regenerator, differ from the single-stage cycle?'),
              PRELUDE + '''rp, T1, T3 = 8.0, 300.0, 1300.0; x = math.sqrt(rp)
h1 = tab('h', T1); T2 = inv('Pr', x * tab('Pr', T1)); h2 = tab('h', T2)
h6 = tab('h', T3); T7 = inv('Pr', tab('Pr', T3) / x); h7 = tab('h', T7)
wc = 2 * (h2 - h1); wt = 2 * (h6 - h7); wnet = wt - wc
q_noreg = (h6 - h2) + (h6 - h7)           # h4 = h2 (intercooled stages), reheat to T3 after the first turbine
q_idealreg = (h6 - h7) + (h6 - h7)        # ideal regenerator: h5 = h7
print(f"T2 = {T2:.1f} K, T7 = {T7:.1f} K; w_comp = {wc:.2f}, w_turb = {wt:.2f}, w_net = {wnet:.2f} kJ/kg, r_bw = {wc/wt:.3f}")
print(f"no regenerator: q_in = {q_noreg:.2f}, eta = {wnet/q_noreg:.3f}; ideal regenerator: q_in = {q_idealreg:.2f}, eta = {wnet/q_idealreg:.3f}")''',
              tr(f'**Đọc kết quả:** r_bw giảm xuống {f(m0["bwr"],3)} (một cấp {f(bB["bwr"],3)}) nhưng η không hồi nhiệt cũng giảm xuống {f(m0["eta"],3)} (một cấp {f(bB["eta"],3)}) vì nhiệt vào tăng; thêm hồi nhiệt lý tưởng đưa η lên {f(m1["eta"],3)} (sách 0,304; 35,8 %; 69,6 %).',
                 f'**Reading the output:** r_bw falls to {f(m0["bwr"],3)} (single stage {f(bB["bwr"],3)}) but η without regeneration also falls to {f(m0["eta"],3)} (single stage {f(bB["eta"],3)}) because the heat input rises; adding an ideal regenerator lifts η to {f(m1["eta"],3)} (book 0.304; 35.8 %; 69.6 %).'),
              [f'r_bw = {m0["bwr"]:.3f}', f'eta = {m0["eta"]:.3f}', f'eta = {m1["eta"]:.3f}']))
    j9 = ideal_jet_k(420, 5, 850, 10, 2460, 100, 0.240, J=25037.0); ex = turbojet_unchoked(240, 32, 310, 12, 1400, 42700)
    S.append((tr('Chu trình phản lực lý tưởng: Cengel Ví dụ 9–9 và El-Sayed Ví dụ 4.2', 'Ideal jet-propulsion cycle: Cengel Example 9–9 and El-Sayed Example 4.2'),
              tr('**Câu hỏi:** tính chuỗi khuếch tán → máy nén → buồng đốt → tuabin → vòi phun của hai ví dụ; kết quả in của El-Sayed có khớp không?', '**Question:** run the chain diffuser → compressor → burner → turbine → nozzle for both examples; do El-Sayed\'s printed results agree?'),
              '''import math
k = 1.4
# Cengel Example 9-9 (English units, cold air): 850 ft/s, 5 psia, 420 R, rp = 10, T4 = 2460 R, 100 lbm/s, cp = 0.240 Btu/lbm R, 1 Btu/lbm = 25037 ft2/s2
cp, J = 0.240, 25037.0
T1, P1, V, rp, T4, md = 420.0, 5.0, 850.0, 10.0, 2460.0, 100.0
T2 = T1 + V**2 / (2*cp*J); P2 = P1 * (T2/T1)**(k/(k-1))
T3 = T2 * rp**((k-1)/k); P3 = rp * P2
T5 = T4 - T3 + T2; P5 = P3 * (T5/T4)**(k/(k-1))                 # turbine work = compressor work
T6 = T5 * (P1/P5)**((k-1)/k); V6 = math.sqrt(2*J*cp*(T5 - T6))
Wp = md * (V6 - V) * V / J; Qin = md * cp * (T4 - T3)
print(f"9-9: T2 = {T2:.0f} R, T3 = {T3:.0f} R, T5 = {T5:.0f} R, P5 = {P5:.1f} psia, V6 = {V6:.0f} ft/s, Wp = {Wp:.0f}, Qin = {Qin:.0f} Btu/s, eta_P = {100*Wp/Qin:.1f} %")
# El-Sayed Example 4.2 (SI): 310 m/s, 240 K, 32 kPa, pi_c = 12, T04 = 1400 K, QR = 42700 kJ/kg, cp = 1.005
cp, Ta, Pa, Vf, pic, T04, QR = 1.005, 240.0, 32.0, 310.0, 12.0, 1400.0, 42700.0
T02 = Ta + Vf**2 / (2000*cp); P02 = Pa * (T02/Ta)**3.5
T03 = T02 * pic**((k-1)/k); f = cp*(T04 - T03) / (QR - cp*T04)
T05 = T04 - (T03 - T02)/(1 + f); P05 = pic*P02*(T05/T04)**3.5
T7 = T05 * (Pa/P05)**((k-1)/k); Vj = math.sqrt(2000*cp*(T05 - T7))
st = (1 + f)*Vj - Vf; eta_p = 2*Vf/(Vf + Vj)
print(f"4.2: T03 = {T03:.1f} K, f = {f:.4f}, T05 = {T05:.1f} K, T7 = {T7:.1f} K, Vj = {Vj:.1f} m/s, specific thrust = {st:.1f} N s/kg, m_a = {12120/st:.2f} kg/s")
# the book's own numbers: T03 = 587.5 K and T7 = 563.6 K (slips). Vj from the book's T05 and T7:
print(f"book: T7 = 563.6 K gives Vj = {math.sqrt(2000*cp*(1106.1 - 563.6)):.1f} m/s; correct T7 = 1106.1/1.9283 = {1106.1/1.9283:.1f} K; 287.8 x 2.035 = {287.8*2.035:.1f} K")''',
              tr(f'**Đọc kết quả:** Ví dụ 9–9 khớp sách (480; 927; 2013 R; 39,7 psia; 3288 ft/s; 22,5 %): V₆ = {f(j9["V6"],0)} ft/s, η_P = {f(j9["etaP"]*100,1)} %. Ví dụ 4.2: V_j = {f(ex["Vj"],1)} m/s, ṁ_a = {f(12120/ex["spec_thrust"],2)} kg/s, không phải 1044,34 m/s và 16,06 kg/s của sách: sách tính sai T₀₃ (587,5 thay vì 585,7 K) và T₇ (563,6 thay vì 573,6 K); với T₇ = 563,6 K đúng ra 1044 m/s. Ghi trong mục lỗi nguồn.',
                 f'**Reading the output:** Example 9–9 matches the book (480; 927; 2013 R; 39.7 psia; 3288 ft/s; 22.5 %): V₆ = {f(j9["V6"],0)} ft/s, η_P = {f(j9["etaP"]*100,1)} %. Example 4.2: V_j = {f(ex["Vj"],1)} m/s, ṁ_a = {f(12120/ex["spec_thrust"],2)} kg/s, not the printed 1044.34 m/s and 16.06 kg/s: the book miscomputes T₀₃ (587.5 instead of 585.7 K) and T₇ (563.6 instead of 573.6 K); with T₇ = 563.6 K one indeed gets 1044 m/s. Recorded in the source-error notes.'),
              [f'V6 = {j9["V6"]:.0f} ft/s', f'eta_P = {j9["etaP"]*100:.1f} %', f'Vj = {ex["Vj"]:.1f} m/s']))
    b8 = brayton_var(7, 300, None, etat=.86, T2_given=580, qin23=950)
    S.append((tr('Otto và Diesel theo r, và bài Tutorials I #8 không có lời giải', 'Otto and Diesel versus r, and Tutorials I #8 (no printed solution)'),
              tr('**Câu hỏi:** (a) với k = 1,4, Otto hơn Diesel (r_c = 2) bao nhiêu ở các r điển hình, và hình slide tr.25 lệch công thức bao nhiêu? (b) giải Tutorials I #8 bằng bảng A-17.', '**Question:** (a) with k = 1.4, how much does Otto beat Diesel (r_c = 2) at typical r, and how far is the figure of slide p.25 from the formula? (b) solve Tutorials I #8 with Table A-17.'),
              PRELUDE + '''k, rc = 1.4, 2.0
print("   r   Otto  Diesel(rc=2)  gap")
for r in (7, 10, 14, 16, 18, 24):
    eo = 1 - r**(1-k); ed = 1 - r**(1-k) * (rc**k - 1) / (k*(rc - 1))
    print(f"{r:4d}  {eo:.3f}  {ed:.3f}        {eo-ed:.3f}")
print(f"slide p.25 reads about 0.665 at r = 14; formula {1-14**(1-k):.3f}")
# Tutorials I #8: 300 K, 100 kPa -> 700 kPa and 580 K (actual state), q_in = 950, eta_t = 0.86, P3 = P2, exhaust at 100 kPa
rp = 7.0; h1 = tab('h', 300); h2 = tab('h', 580); wc = h2 - h1
h3 = h2 + 950; T3 = inv('h', h3); T4s = inv('Pr', tab('Pr', T3) / rp); wt = 0.86 * (h3 - tab('h', T4s)); wnet = wt - wc
print(f"#8: T3 = {T3:.0f} K, w_turb = {wt:.1f}, w_comp = {wc:.1f} kJ/kg, w_comp/w_turb = {wc/wt:.3f}, eta = {wnet/950:.3f}")''',
              tr(f'**Đọc kết quả:** Otto luôn hơn Diesel cùng r (ví dụ r = 16: {f(1-16**-.4,3)} so với {f(1-16**-.4*(2**1.4-1)/1.4,3)}); công thức cho {f(1-14**-.4,3)} tại r = 14 còn hình slide ≈ 0,665 (lệch 0,013, trong sai số đọc hình). Tutorials I #8: T₃ = {f(b8["T3"],0)} K, w_turb = {f(b8["wt"],1)}, w_comp = {f(b8["wc"],1)} kJ/kg, tỉ số {f(b8["bwr"],3)}, η = {f(b8["eta"],3)} (giả định P₃ = P₂ và xả ở 100 kPa).',
                 f'**Reading the output:** Otto always beats Diesel at equal r (for example r = 16: {f(1-16**-.4,3)} versus {f(1-16**-.4*(2**1.4-1)/1.4,3)}); the formula gives {f(1-14**-.4,3)} at r = 14 while the slide figure reads ≈ 0.665 (0.013 off, inside the reading error). Tutorials I #8: T₃ = {f(b8["T3"],0)} K, w_turb = {f(b8["wt"],1)}, w_comp = {f(b8["wc"],1)} kJ/kg, ratio {f(b8["bwr"],3)}, η = {f(b8["eta"],3)} (assuming P₃ = P₂ and exhaust at 100 kPa).'),
              [f'T3 = {b8["T3"]:.0f} K', f'eta = {b8["eta"]:.3f}', f'{1-14**-.4:.3f}']))
    return S

def build(lang):
    vi = lang == 'vi'
    nb = nbf.v4.new_notebook()
    head = ('# m02 · Chu trình công suất khí: các phép tính kiểm chứng\n\nSổ tay này tính lại bằng Python các ví dụ chính của module m02 (Slide Ch.2; Tutorials I; Cengel Ch.9; El-Sayed Ví dụ 4.2). Mỗi mục có ba phần: câu hỏi mà phương pháp trả lời → mã → diễn giải số in thật. Chạy từ trên xuống (cần numpy, scipy). Bảng A-17 được nhúng sẵn trong ô mã đầu tiên.'
            if vi else
            '# m02 · Gas power cycles: verification calculations\n\nThis notebook recomputes in Python the main examples of module m02 (Slide Ch.2; Tutorials I; Cengel Ch.9; El-Sayed Example 4.2). Every section has three parts: the question the method answers → code → interpretation of the real printed numbers. Run top to bottom (needs numpy, scipy). Table A-17 is embedded in the first code cell.')
    cells = [nbf.v4.new_markdown_cell(head)]; checks = []
    for i, (title, q, code, interp, must) in enumerate(sections(lang), 1):
        cells.append(nbf.v4.new_markdown_cell(f'## {i}. {title}\n\n{q}')); cells.append(nbf.v4.new_code_cell(code)); cells.append(nbf.v4.new_markdown_cell(interp)); checks.append((len(cells) - 2, must))
    nb['cells'] = cells; nb['metadata']['language_info'] = {'name': 'python'}
    fn = os.path.join(OUT, f'm02_gas_power_cycles_{lang}.ipynb'); nbf.write(nb, fn)
    r = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), '-I', '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', fn], capture_output=True, text=True, cwd=OUT)
    if r.returncode != 0: print(r.stdout[-1500:], r.stderr[-2500:]); raise SystemExit(f'nbconvert failed for {lang}')
    nb2 = nbf.read(fn, as_version=4)
    for idx, must in checks:
        out = ''.join(o.get('text', '') for o in nb2.cells[idx].get('outputs', []))
        for s in must:
            if s not in out: raise SystemExit(f'[{lang}] cell {idx}: expected "{s}" in the output but it is missing:\n{out}')
    print('executed and verified', fn, len(nb2.cells), 'cells')

if __name__ == '__main__':
    build('vi'); build('en')
