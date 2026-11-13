"""Build and execute the m01 notebooks (VI and EN).  Run: .venv/bin/python -I build/nb/make_m01.py
Each method section = markdown (question it answers) -> code -> markdown interpreting the REAL output (numbers in the interpretation are
computed here with the same formulas and then CHECKED against the executed output text: the build fails if they do not appear)."""
import os, sys, math, subprocess, json
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
G0 = 9.80665; R = 287.0; GAM = 1.4

def isa(z):
    T0, p0, L, Rr, g = 288.15, 101325.0, 0.0065, 287.053, 9.80665
    if z <= 11000: T = T0 - L * z; p = p0 * (T / T0) ** (g / (Rr * L))
    else: T = 216.65; p = p0 * (T / T0) ** (g / (Rr * L)) * math.exp(-g * (z - 11000) / (Rr * T))
    return T, p
def f(x, nd=2): return f'{x:.{nd}f}'

def sections(lang):
    vi = lang == 'vi'
    tr = lambda a, b: a if vi else b
    S = []      # (title, question_md, code, interpretation_md, [strings that must appear in stdout])
    # ---------------------------------------------------------------- 1 ISA
    T10, p10 = isa(10000.); T11, p11 = isa(11000.); T25, p25 = isa(25000.)
    S.append((tr('Khí quyển chuẩn ISA và kiểm số liệu slide tr.48', 'ISA and checking the numbers of slide p.48'),
              tr('**Câu hỏi:** slide Ch.1 tr.48 ghi tropopause tại −56 °C và 264 hPa. Giá trị đó ứng với độ cao nào theo khí quyển chuẩn ISA, và ISA lệch bảng Farokhi Appendix A bao nhiêu?',
                 '**Question:** slide Ch.1 p.48 labels the tropopause at −56 °C and 264 hPa. Which altitude does that correspond to in the ISA, and how far is the ISA from Farokhi Appendix A?'),
              '''import math
def isa(z):
    """ISA 0-20 km: troposphere T = 288.15 - 0.0065 z, isothermal 216.65 K above 11 km."""
    T0, p0, L, Rr, g = 288.15, 101325.0, 0.0065, 287.053, 9.80665
    if z <= 11000:
        T = T0 - L*z; p = p0*(T/T0)**(g/(Rr*L))
    else:
        T = 216.65; p = p0*(T/T0)**(g/(Rr*L))*math.exp(-g*(z-11000)/(Rr*T))
    return T, p, p/(Rr*T)
# Farokhi Appendix A (SI) typed from the page image: alt km -> (T K, p Pa)
farokhi = {0:(288.1,1.013e5), 2:(275.2,7.950e4), 4:(262.2,6.166e4), 6:(249.2,4.722e4), 8:(236.2,3.565e4), 10:(223.3,2.650e4), 12:(216.6,1.940e4), 20:(216.6,5.529e3)}
print("z km |  T ISA   T Farokhi |  p ISA (Pa)  p Farokhi (Pa) | dp %")
for z,(Tf,pf) in farokhi.items():
    T,p,rho = isa(z*1000.)
    print(f"{z:4d} | {T:7.2f} {Tf:9.1f} | {p:11.1f} {pf:14.1f} | {100*(p-pf)/pf:+.2f}")
for z in (10000., 11000., 25000.):
    T,p,rho = isa(z); print(f"z = {z/1000:.0f} km: T = {T-273.15:.2f} C, p = {p/100:.2f} hPa, rho = {rho:.4f} kg/m3")''',
              tr(f'**Đọc kết quả:** ISA cho p(10 km) = {f(p10/100,1)} hPa còn p(11 km) = {f(p11/100,1)} hPa; nhiệt độ −56 °C ({f(T11-273.15,2)} °C) là của 11 km. Vậy số "264 hPa" trên slide là áp suất ở 10 km (ghép với nhiệt độ của 11 km); đây là một lỗi của slide, không phải của OCR. Sai khác ISA so với bảng Farokhi nhỏ (≤ 0,4 % đến 12 km). Mốc 26 hPa ở ~25 km: ISA {f(p25/100,2)} hPa (làm tròn).',
                 f'**Reading the output:** the ISA gives p(10 km) = {f(p10/100,1)} hPa and p(11 km) = {f(p11/100,1)} hPa; −56 °C ({f(T11-273.15,2)} °C) belongs to 11 km. So the "264 hPa" on the slide is the pressure at 10 km paired with the temperature of 11 km; this is a slide error, not an OCR error. ISA differs little from Farokhi\'s table (≤ 0.4 % up to 12 km). The 26 hPa mark at ~25 km: ISA {f(p25/100,2)} hPa (rounded).'),
              [f'{p10/100:.2f}', f'{p11/100:.2f}']))
    # ---------------------------------------------------------------- 2 level flight
    m, CL, CD = 60000., .5, .03; Fx = CD/CL*m*G0
    S.append((tr('Bốn lực khi bay bằng đều', 'Four forces in level flight'),
              tr('**Câu hỏi:** máy bay m = 60 000 kg bay bằng đều với C_L = 0,5, C_D = 0,03. Lực đẩy cần là bao nhiêu và ở độ cao 10 km (ISA) cần bay nhanh bao nhiêu để F_z = P, nếu S = 122 m²?',
                 '**Question:** an aircraft of m = 60,000 kg in level flight with C_L = 0.5, C_D = 0.03. What thrust is needed and how fast must it fly at 10 km (ISA) so that F_z = P, if S = 122 m²?'),
              '''import math
G0 = 9.80665
m, CL, CD, S_ = 60000., 0.5, 0.03, 122.
P = m*G0
Fx = CD/CL*P                      # T_u = F_x, from F_z = P
print(f"weight P = {P/1e3:.1f} kN, required thrust T_u = {Fx/1e3:.2f} kN = {100*Fx/P:.2f} % of weight")
for z in (0., 10000.):
    T,p,rho = isa(z)
    V = math.sqrt(2*P/(rho*S_*CL))      # from F_z = CL*V^2*rho/2*S = P
    Fz = CL*V**2*rho/2*S_
    print(f"z = {z/1000:4.0f} km: rho = {rho:.4f}  V = {V:.1f} m/s = {3.6*V:.0f} km/h  (check F_z = {Fz/1e3:.1f} kN)")''',
              tr(f'**Đọc kết quả:** lực đẩy cần chỉ {f(Fx/1e3,2)} kN, khoảng {f(100*Fx/(m*G0),1)} % trọng lượng (= C_D/C_L): động cơ không nâng máy bay. Ở 10 km mật độ chỉ ≈ 1/3 mực nước biển nên vận tốc cần để giữ lực nâng tăng gấp √(ρ0/ρ) ≈ 1,7 lần.',
                 f'**Reading the output:** the required thrust is only {f(Fx/1e3,2)} kN, about {f(100*Fx/(m*G0),1)} % of the weight (= C_D/C_L): the engine does not lift the aircraft. At 10 km the density is about a third of the sea-level one, so the speed needed to keep the lift rises by √(ρ0/ρ) ≈ 1.7.'),
              [f'{Fx/1e3:.2f}']))
    # ---------------------------------------------------------------- 3 thrust equation and quadratic
    r1 = ((31*610) + math.sqrt((31*610)**2 - 4*30*1.12e6))/60; r2 = ((31*610) - math.sqrt((31*610)**2 - 4*30*1.12e6))/60
    S.append((tr('Phương trình lực đẩy: Ví dụ 2.1 và 2.2 của El-Sayed', 'The thrust equation: El-Sayed Examples 2.1 and 2.2'),
              tr('**Câu hỏi:** (a) với ṁa = 30 kg/s, ṁf = 1 kg/s, ue = 610 m/s, công suất đẩy 1,12×10⁶ W, vận tốc bay u là bao nhiêu? (b) lực đẩy tiến và khi đảo chiều lực đẩy 90° của động cơ chạy chậm lúc hạ cánh?',
                 '**Question:** (a) with ṁa = 30 kg/s, ṁf = 1 kg/s, ue = 610 m/s and a thrust power of 1.12×10⁶ W, what is the flight speed u? (b) the forward thrust and the thrust with the exhaust turned 90° of an idling engine during landing?'),
              '''import sympy as sp
u = sp.symbols('u', positive=True)
roots = sp.solve(sp.Eq((30+1)*610*u - 30*u**2, 1.12e6), u)      # thrust power = T*u = (ma+mf) ue u - ma u^2
print("Example 2.1 roots u (m/s):", [round(float(r),2) for r in roots])
# Example 2.2 (British units): ma = 100 lbm/s, U = 100 mph, Ue = 450 ft/s, gc = 32.2
U = 100*1.4667; gc = 32.2
Tf = 100/gc*(450-U); Tr = 100/gc*(0-U)
print(f"forward thrust = {Tf:.0f} lbf ; with exhaust turned 90 deg = {Tr:.1f} lbf (negative = braking)")''',
              tr(f'**Đọc kết quả:** phương trình bậc hai có hai nghiệm {f(r1,2)} và {f(r2,2)} m/s, khớp sách (564,15 và 66,17). Nghiệm lớn là chế độ bay của phản lực. Lực đẩy tiến 942 lbf; khi dòng phụt bị quay 90° thành phần ngang bằng 0 nên lực chỉ còn là −ṁa·U = {f(100/32.2*(0-146.67),1)} lbf, tức lực hãm: đó là cơ chế phanh bằng đảo chiều lực đẩy.',
                 f'**Reading the output:** the quadratic has two roots {f(r1,2)} and {f(r2,2)} m/s, matching the book (564.15 and 66.17). The larger root is the jet\'s flight state. Forward thrust is 942 lbf; with the jet turned 90° the horizontal component is zero so the force is only −ṁa·U = {f(100/32.2*(0-146.67),1)} lbf, a braking force: the mechanism of thrust-reverse braking.'),
              [f'{r1:.2f}', '942']))
    # ---------------------------------------------------------------- 4 propulsive efficiency three expressions
    u25 = .8*math.sqrt(GAM*R*223.3); st25 = (1.02*570-u25)+.006*(.67e5-.265e5)
    e1 = 2*st25*u25/(2*st25*u25+1.02*(570-u25)**2); e2 = 2*st25*u25/(1.02*570**2-u25**2); e3 = 2*u25/(570+u25)
    S.append((tr('Ba biểu thức hiệu suất đẩy (El-Sayed Ví dụ 2.5)', 'Three propulsive-efficiency expressions (El-Sayed Example 2.5)'),
              tr('**Câu hỏi:** với vòi phun nghẹt (Pe = 0,67 bar > Pa = 0,265 bar), biểu thức nào của η_p còn dùng được?',
                 '**Question:** with a choked nozzle (Pe = 0.67 bar > Pa = 0.265 bar), which expression of η_p is still usable?'),
              '''import math
gam, Rg, Ta, Ma = 1.4, 287., 223.3, 0.8
ue, pe, pa, f, Ae_over_m = 570., 0.67e5, 0.265e5, 0.02, 0.006
u = Ma*math.sqrt(gam*Rg*Ta)
st = ((1+f)*ue - u) + (pe-pa)*Ae_over_m           # specific thrust, N s/kg
e1 = 2*st*u/(2*st*u + (1+f)*(ue-u)**2)            # expression 1: thrust power / (thrust power + wake loss)
e2 = 2*st*u/((1+f)*ue**2 - u**2)                  # expression 2: / kinetic energy added
e3 = 2*u/(u+ue)                                   # expression 3: Pe = Pa and f = 0 only
print(f"u = {u:.1f} m/s, specific thrust = {st:.2f} N s/kg")
print(f"eta_p: expr1 = {e1:.4f}   expr2 = {e2:.4f}   expr3 = {e3:.4f}")
# effective (fully expanded) jet velocity ue' = ue + (pe-pa) Ae / me ; then both expressions are evaluated with it
ue_eff = ue + (pe-pa)*Ae_over_m/(1+f)
e1b = 2*st*u/(2*st*u + (1+f)*(ue_eff-u)**2)
e2b = 2*st*u/((1+f)*ue_eff**2 - u**2)
print(f"effective jet velocity {ue_eff:.1f} m/s: expr1 = {e1b:.4f}, expr2 = {e2b:.4f}")''',
              tr(f'**Đọc kết quả:** biểu thức 1 cho {f(e1*100,2)} % (khớp sách 71,56 %); biểu thức 2 cho {f(e2*100,1)} %, vượt 100 % nên vô nghĩa khi vòi nghẹt; biểu thức 3 chỉ ước lượng thô {f(e3*100,2)} %. Nếu tính cả hai biểu thức với vận tốc phụt hiệu dụng u_e′ (giãn nở hoàn toàn; dòng cuối) thì chúng gần bằng nhau (chênh nhau ở số hạng f), nhưng giá trị ≈ 0,46 thấp hơn nhiều 71,56 % của sách, vì khi đó phần năng lượng áp suất chưa giãn nở của dòng phụt được tính vào tổn thất vệt khí xả. Kết luận: chọn biểu thức và nói rõ giả thiết (u_e thật hay u_e′) trước khi so sánh các giá trị η_p.',
                 f'**Reading the output:** expression 1 gives {f(e1*100,2)} % (book 71.56 %); expression 2 gives {f(e2*100,1)} %, above 100 % and so meaningless for a choked nozzle; expression 3 is only a rough {f(e3*100,2)} %. If both expressions are evaluated with the effective jet velocity u_e′ (full expansion; last line) they nearly agree (they differ by an f term), but the value ≈ 0.46 is far below the 71.56 % of the book, because the unexpanded pressure energy of the jet is then counted as wake loss. Conclusion: state which expression and which assumption (actual u_e or u_e′) before comparing η_p values.'),
              [f'{e1:.4f}', f'{e2:.4f}', f'{2*st25*u25/(2*st25*u25+1.02*((570+.006*40500/1.02)-u25)**2):.4f}']))
    # ---------------------------------------------------------------- 5 CF6
    U7 = .8*math.sqrt(GAM*R*223.2); mh = 125/6; mc = 125*5/6; f7 = .75/mh; uec = 18000/mc+U7; ueh = (6000/mh+U7)/(1+f7)
    ke = .5*(mh*((1+f7)*ueh**2-U7**2)+mc*(uec**2-U7**2)); ep = 24000*U7/ke; eth = ke/(.75*42.8e6); eo = ep*eth
    S.append((tr('Turbofan CF6: ba hiệu suất liên tiếp (El-Sayed Ví dụ 2.7)', 'CF6 turbofan: three efficiencies in a chain (El-Sayed Example 2.7)'),
              tr('**Câu hỏi:** từ lực đẩy 24 kN (quạt 75 %), BPR = 5, ṁa = 125 kg/s, ṁf = 0,75 kg/s, Ma 0,8 ở 10 km: các vận tốc phụt, η_p, η_th, η_o là bao nhiêu và có khớp số in trong sách không?',
                 '**Question:** from a thrust of 24 kN (fan 75 %), BPR = 5, ṁa = 125 kg/s, ṁf = 0.75 kg/s, Ma 0.8 at 10 km: what are the jet speeds, η_p, η_th, η_o, and do they match the numbers printed in the book?'),
              '''import math
from scipy.optimize import brentq
T, ma, beta, mf, M, Ta, QR = 24000., 125., 5., 0.75, 0.8, 223.2, 42.8e6
U = M*math.sqrt(1.4*287*Ta)
mc, mh = ma*beta/(1+beta), ma/(1+beta); f = mf/mh
Tfan, Tcore = 0.75*T, 0.25*T
uec = brentq(lambda ue: mc*(ue-U) - Tfan, 1, 3000)                  # solve instead of rearranging
ueh = brentq(lambda ue: mh*((1+f)*ue-U) - Tcore, 1, 3000)
dKE = 0.5*(mh*((1+f)*ueh**2 - U**2) + mc*(uec**2 - U**2))          # power imparted to the airflow
eta_p, eta_th = T*U/dKE, dKE/(mf*QR)
print(f"U = {U:.1f} m/s; mc = {mc:.1f}, mh = {mh:.1f} kg/s, f = {f:.4f}")
print(f"uec = {uec:.1f} m/s (book 413), ueh = {ueh:.1f} m/s (book 510)")
print(f"dKE = {dKE/1e6:.3f} MW; eta_p = {eta_p:.4f} (book 0.712), eta_th = {eta_th:.4f} (book 0.2546), eta_o = {eta_p*eta_th:.4f} (book 0.1793)")
print(f"check eta_o = T U /(mf QR) = {T*U/(mf*QR):.4f};   specific thrust = {T/ma:.1f} N s/kg, TSFC = {mf/T*1e6:.2f} mg/(N s)")''',
              tr(f'**Đọc kết quả:** u_ec = {f(uec,1)} m/s và u_eh = {f(ueh,1)} m/s khớp 413 và 510; η_p = {f(ep,4)} khớp 0,712. Nhưng η_th = {f(eth,4)} khác 0,2546 sách in: 16,179×10⁶/(2×0,75×42,8×10⁶) = 0,2520 (tính chính xác với vận tốc không làm tròn: 0,2513), và η_o in 0,1793 chỉ khớp 0,712×0,252. Đây là lỗi số học của sách (ghi trong mục lỗi nguồn). η_o = {f(eo*100,2)} % cũng bằng F·U/(ṁf·Q).',
                 f'**Reading the output:** u_ec = {f(uec,1)} m/s and u_eh = {f(ueh,1)} m/s match 413 and 510; η_p = {f(ep,4)} matches 0.712. But η_th = {f(eth,4)} differs from the printed 0.2546: 16.179×10⁶/(2×0.75×42.8×10⁶) = 0.2520 (exactly, with unrounded speeds: 0.2513), and the printed η_o = 0.1793 matches only 0.712×0.252. This is an arithmetic slip of the book (listed in the source errors). η_o = {f(eo*100,2)} % also equals F·U/(ṁf·Q).'),
              [f'{ep:.4f}', f'{eth:.4f}']))
    # ---------------------------------------------------------------- 6 Farokhi
    V0 = 2*math.sqrt(GAM*R*223.15); Fn = 25.75*1050-25*V0; dk = .5*(25.75*1050**2-25*V0**2)
    S.append((tr('Lực đẩy tổng, lực đẩy thực và cản ram (Farokhi Problem 3.5 và 3.11)', 'Gross, net thrust and ram drag (Farokhi Problems 3.5 and 3.11)'),
              tr('**Câu hỏi:** ở Ma 2 một nửa lực đẩy tổng bị mất vào lực cản ram thế nào, và so với một turbojet bay chậm (3.11) thì sao?',
                 '**Question:** how much of the gross thrust is lost to ram drag at Mach 2, and how does that compare with a slow turbojet (3.11)?'),
              '''import math
def engine(m, f, V9, V0, QR):
    mf = f*m; Dram = m*V0; Fg = (m+mf)*V9; Fn = Fg - Dram
    dKE = 0.5*((m+mf)*V9**2 - m*V0**2)
    return dict(Dram=Dram, Fg=Fg, Fn=Fn, eth=dKE/(mf*QR), ep=Fn*V0/dKE, eo=Fn*V0/(mf*QR))
V0a = 2*math.sqrt(1.4*287*223.15)
a = engine(25, 0.03, 1050, V0a, 42.8e6)          # Farokhi 3.5 (Mach 2)
b = engine(100, 0.025, 600, 300, 42.0e6)         # Farokhi 3.11 (V0 = 300 m/s)
for name, r in (("3.5  Mach 2", a), ("3.11 300 m/s", b)):
    print(f"{name}: Dram = {r['Dram']/1e3:.2f} kN, Fg = {r['Fg']/1e3:.2f} kN, Fn = {r['Fn']/1e3:.2f} kN, ram share = {100*r['Dram']/r['Fg']:.1f} %,")
    print(f"      eta_th = {r['eth']:.4f}, eta_p = {r['ep']:.4f}, eta_o = {r['eo']:.4f}")
print(f"3.5: TSFC = {0.75/a['Fn']*3600:.4f} kg/(h N)  |  3.11: TSFC = {2.5/b['Fn']*1e6:.2f} mg/(s N)")''',
              tr(f'**Đọc kết quả:** ở Ma 2 (V0 = {f(V0,1)} m/s) lực cản ram {f(25*V0/1e3,2)} kN chiếm {f(100*25*V0/(25.75*1050),1)} % lực đẩy tổng {f(25.75*1050/1e3,2)} kN nên lực đẩy thực chỉ {f(Fn/1e3,2)} kN. Ở 300 m/s với vận tốc phụt 600 m/s ram chỉ chiếm 49 %, nhưng η_p thấp hơn nhiều khi u_e ≫ u. Đây là lý do lực đẩy thực giảm theo tốc độ bay.',
                 f'**Reading the output:** at Mach 2 (V0 = {f(V0,1)} m/s) the ram drag {f(25*V0/1e3,2)} kN takes {f(100*25*V0/(25.75*1050),1)} % of the {f(25.75*1050/1e3,2)} kN gross thrust so the net thrust is only {f(Fn/1e3,2)} kN. At 300 m/s with a 600 m/s jet the ram share is only 49 %, but η_p is much lower when u_e ≫ u. This is why net thrust falls with flight speed.'),
              [f'{Fn/1e3:.2f}']))
    # ---------------------------------------------------------------- 7 Example 2.4
    comps = [(648e3, .117, 124), (655e3, .132, 112), (641e3, .374, 94), (145e3, .310, 271), (145e3, .420, 196), (41e3, .214, 584)]
    prev = (0, 0, 0); Fs = []
    for p_, A_, U_ in comps: Fs.append(p_*A_ - prev[0]*prev[1] + 69.4*(U_-prev[2])); prev = (p_, A_, U_)
    S.append((tr('Phân bố lực đẩy theo bộ phận turbojet (El-Sayed Ví dụ 2.4)', 'Thrust distribution by turbojet component (El-Sayed Example 2.4)'),
              tr('**Câu hỏi:** mỗi bộ phận chịu lực bao nhiêu và tổng có bằng lực đẩy của cả động cơ không?', '**Question:** what force does each component carry and does the sum equal the thrust of the whole engine?'),
              '''names = ["compressor", "diffuser", "combustor", "turbine", "jet pipe", "nozzle"]
comps = [(648e3,.117,124),(655e3,.132,112),(641e3,.374,94),(145e3,.310,271),(145e3,.420,196),(41e3,.214,584)]   # gauge P (Pa), A (m2), U (m/s)
m = 69.4
prev = (0.0, 0.0, 0.0); F = []
for (p, A, U) in comps:
    F.append(p*A - prev[0]*prev[1] + m*(U - prev[2]))      # F = Pe Ae - Pi Ai + m (Ue - Ui)
    prev = (p, A, U)
for n, x in zip(names, F): print(f"{n:11s} {x:12.0f} N  {'forward' if x > 0 else 'rearward'}")
print(f"sum of components = {sum(F):.0f} N ; whole engine Pe Ae + m Ue = {41e3*.214 + m*584:.0f} N")''',
              tr(f'**Đọc kết quả:** tổng các bộ phận = {f(sum(Fs),0)} N = lực đẩy cả động cơ (sách in 49 304 N). Tuabin ({f(Fs[3],0)} N) và vòi phun ({f(Fs[5],0)} N) kéo về phía sau; máy nén, khuếch tán, buồng đốt, ống xả đẩy về phía trước. Số hiệu in trong sách có vài lỗi chép (xem mục lỗi nguồn).',
                 f'**Reading the output:** the sum of the components = {f(sum(Fs),0)} N = the thrust of the whole engine (book prints 49,304 N). The turbine ({f(Fs[3],0)} N) and nozzle ({f(Fs[5],0)} N) pull rearwards; compressor, diffuser, combustor and jet pipe push forward. The printed solution has a few typos (see the source errors).'),
              [f'{sum(Fs):.0f}']))
    # ---------------------------------------------------------------- 8 Breguet + wind
    S29 = .35*45e6/9.8*17*math.log(1/.673)
    ft = 50000*(1-math.exp(-4000e3*9.8*(.08/3600)/(300*10))); fh = 50000*(1-math.exp(-4000e3*9.8*(.08/3600)/(200*10)))
    S.append((tr('Tầm bay Breguet và ảnh hưởng của gió (El-Sayed Ví dụ 2.9 và 2.11)', 'Breguet range and the effect of wind (El-Sayed Examples 2.9 and 2.11)'),
              tr('**Câu hỏi:** tầm bay của Boeing 747 trong Ví dụ 2.9 là bao nhiêu và gió xuôi/ngược 50 m/s đổi lượng nhiên liệu cho chặng 4000 km thế nào?',
                 '**Question:** what is the range of the Boeing 747 of Example 2.9 and how does a 50 m/s tail/head wind change the fuel for a 4000 km leg?'),
              '''import math
from scipy.integrate import solve_ivp
# Example 2.9: Breguet S = eta_o QR / g * (L/D) * ln(m1/m2)
S = 0.35*45e6/9.8*17*math.log(1/0.673)
print(f"Example 2.9: S = {S/1e3:.1f} km (book 10,819 km)")
# Example 2.11: integrate dm/ds = -m * TSFC * g / (Vg L/D) over 4000 km, instead of using the closed form
def fuel(Vg, TSFC=0.08/3600, g=9.8, LD=10, s_end=4000e3, m1=50000.):
    sol = solve_ivp(lambda s, m: [-m[0]*TSFC*g/(Vg*LD)], (0, s_end), [m1], rtol=1e-11, atol=1e-9)
    return m1 - sol.y[0, -1]
for name, Vg in (("tail wind 50 m/s (Vg = 300)", 300.), ("no wind (Vg = 250)", 250.), ("head wind 50 m/s (Vg = 200)", 200.)):
    print(f"{name:30s} fuel = {fuel(Vg):8.0f} kg   time = {4000e3/Vg/3600:5.2f} h")''',
              tr(f'**Đọc kết quả:** S = {f(S29/1e3,1)} km khớp 10 819 km của sách (làm tròn ln). Gió xuôi tốn {f(ft,0)} kg và gió ngược {f(fh,0)} kg (sách 12 600 và 17 654): gió ngược làm tăng nhiên liệu ≈ {f((fh/ft-1)*100,0)} % so với gió xuôi vì tốc độ so với mặt đất giảm (tầm bay tỉ lệ với V_g/TSFC).',
                 f'**Reading the output:** S = {f(S29/1e3,1)} km matches the book\'s 10,819 km (ln rounded). The tail wind needs {f(ft,0)} kg and the head wind {f(fh,0)} kg (book 12,600 and 17,654): the head wind raises the fuel by ≈ {f((fh/ft-1)*100,0)} % relative to the tail wind because the ground speed drops (range scales with V_g/TSFC).'),
              [f'{S29/1e3:.1f}', f'{ft:.0f}']))
    # ---------------------------------------------------------------- 9 plot
    S.append((tr('Hiệu suất đẩy và lực đẩy theo vận tốc bay (hình)', 'Propulsive efficiency and thrust versus flight speed (plot)'),
              tr('**Câu hỏi:** hình dạng của η_p và T theo u/ue (El-Sayed Problem 2.7: ṁa = 50 kg/s, f = 0,015, ue = 500 m/s, Pa = 60 kPa, Pe = 120 kPa, Ae = 0,25 m²) nói gì về cất cánh và bay nhanh?',
                 '**Question:** what do the shapes of η_p and T versus u/ue (El-Sayed Problem 2.7: ṁa = 50 kg/s, f = 0.015, ue = 500 m/s, Pa = 60 kPa, Pe = 120 kPa, Ae = 0.25 m²) say about takeoff and fast flight?'),
              '''import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ma, f, ue, pa, pe, Ae = 50., 0.015, 500., 60e3, 120e3, 0.25
x = np.linspace(0, 1, 101); u = x*ue
T = ma*((1+f)*ue - u) + (pe-pa)*Ae                      # thrust
wake = 0.5*ma*(1+f)*(ue-u)**2
eta_p = T*u/(T*u + wake)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4)); a1.plot(x, T/1e3); a1.set_xlabel("u/ue"); a1.set_ylabel("T (kN)"); a1.grid(alpha=.3)
a2.plot(x, eta_p); a2.set_xlabel("u/ue"); a2.set_ylabel("eta_p"); a2.grid(alpha=.3); plt.tight_layout(); plt.savefig("problem27_check.png", dpi=80)
print(f"static thrust (u = 0): {T[0]/1e3:.2f} kN, eta_p = {eta_p[0]:.3f}")
print(f"u/ue = 0.5: T = {T[50]/1e3:.2f} kN, eta_p = {eta_p[50]:.4f};  u/ue = 0.9: T = {T[90]/1e3:.2f} kN, eta_p = {eta_p[90]:.4f}")
print(f"T = 0 would need u = {(ma*(1+f)*ue + (pe-pa)*Ae)/ma:.1f} m/s > ue because of the pressure thrust")''',
              (lambda ma=50., f_=.015, ue=500., pa=60e3, pe=120e3, Ae=.25: (lambda T0, T50, T90: tr(
                  f'**Đọc kết quả:** lực đẩy tĩnh {f(T0/1e3,2)} kN với η_p = 0 (chưa có công đẩy); khi u tăng lực đẩy giảm tuyến tính còn {f(T50/1e3,2)} kN ở u/ue = 0,5 và {f(T90/1e3,2)} kN ở 0,9 trong khi η_p tăng. Vì có lực đẩy áp suất (Pe &gt; Pa) lực đẩy chưa triệt tiêu ngay cả ở u = ue. Đây là đánh đổi cơ bản: lực đẩy lớn ở vận tốc bay nhỏ, hiệu suất lớn ở vận tốc bay gần vận tốc phụt.',
                  f'**Reading the output:** static thrust is {f(T0/1e3,2)} kN with η_p = 0 (no thrust power yet); as u rises thrust falls linearly to {f(T50/1e3,2)} kN at u/ue = 0.5 and {f(T90/1e3,2)} kN at 0.9 while η_p rises. Because of the pressure thrust (Pe &gt; Pa) the thrust does not vanish even at u = ue. This is the basic trade-off: large thrust at low flight speed, high efficiency when the flight speed approaches the jet speed.'))(
                  ma*((1+f_)*ue-0)+(pe-pa)*Ae, ma*((1+f_)*ue-.5*ue)+(pe-pa)*Ae, ma*((1+f_)*ue-.9*ue)+(pe-pa)*Ae))(),
              [f'{(50*((1+.015)*500)+(120e3-60e3)*.25)/1e3:.2f}']))
    return S

def build(lang):
    nb = nbf.v4.new_notebook(); vi = lang == 'vi'
    head = ('# m01 · Giới thiệu, nguyên lý đẩy và phân loại động cơ: tính toán kiểm chứng\n\nNotebook này tính lại bằng Python các ví dụ và công thức chính của module m01 (Slide Ch.1; El-Sayed Ch.2; Farokhi Ch.3, Appendix A). '
            'Mỗi mục có ba phần: câu hỏi mà phương pháp trả lời → mã → diễn giải số thật in ra. Chạy từ trên xuống (cần numpy, scipy, sympy, matplotlib).') if vi else \
           ('# m01 · Introduction, principles of propulsion and engine classification: verification calculations\n\nThis notebook recomputes in Python the main examples and formulas of module m01 (Slide Ch.1; El-Sayed Ch.2; Farokhi Ch.3, Appendix A). '
            'Every section has three parts: the question the method answers → code → interpretation of the real printed numbers. Run top to bottom (needs numpy, scipy, sympy, matplotlib).')
    cells = [nbf.v4.new_markdown_cell(head)]
    checks = []
    for i, (title, q, code, interp, must) in enumerate(sections(lang), 1):
        cells.append(nbf.v4.new_markdown_cell(f'## {i}. {title}\n\n{q}'))
        cells.append(nbf.v4.new_code_cell(code)); cells.append(nbf.v4.new_markdown_cell(interp)); checks.append((len(cells) - 2, must))
    nb['cells'] = cells; nb['metadata']['language_info'] = {'name': 'python'}
    # section 2 needs the isa() of section 1 in scope: it is defined in cell 1 and the notebook runs top to bottom
    fn = os.path.join(OUT, f'm01_introduction_propulsion_{lang}.ipynb')
    nbf.write(nb, fn)
    r = subprocess.run([os.path.join(ROOT, '.venv', 'bin', 'python'), '-I', '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', fn], capture_output=True, text=True, cwd=OUT)
    if r.returncode != 0: print(r.stdout[-1500:], r.stderr[-2500:]); raise SystemExit(f'nbconvert failed for {lang}')
    nb2 = nbf.read(fn, as_version=4)
    for idx, must in checks:
        out = ''.join(o.get('text', '') for o in nb2.cells[idx].get('outputs', []))
        for s in must:
            if s not in out: raise SystemExit(f'[{lang}] cell {idx}: expected "{s}" in the output but it is missing:\n{out}')
    print('executed and verified', fn, len(nb2.cells), 'cells')
    for f_ in ('problem27_check.png',):
        p = os.path.join(OUT, f_)
        if os.path.exists(p): os.remove(p)

if __name__ == '__main__':
    build('vi'); build('en')
