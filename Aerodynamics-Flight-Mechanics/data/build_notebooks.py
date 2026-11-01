# -*- coding: utf-8 -*-
"""Sinh 3 notebook tu chua (khong import aero.py) va co assert cho moi dap an. Chay: python3 -I build_notebooks.py"""
import os
import nbformat as nbf

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "notebooks")
os.makedirs(OUT, exist_ok=True)


def nb(cells):
    n = nbf.v4.new_notebook()
    n["cells"] = cells
    n["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}}
    return n


md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

ISA = '''import math
G0, R_AIR, GAMMA = 9.80665, 287.05287, 1.4
P0, T0, RHO0 = 101325.0, 288.15, 1.225
FT, PSI = 0.3048, 6894.757

def isa(h_m):
    """ISA 0-20 km: (T [K], p [Pa], rho [kg/m3]). Troposphere lapse -6.5 K/km, isothermal 216.65 K above 11 km."""
    if h_m <= 11000:
        L = -0.0065; T = T0 + L*h_m; p = P0*(T/T0)**(-G0/(L*R_AIR))
    else:
        T = 216.65; p11 = P0*(T/T0)**(-G0/(-0.0065*R_AIR)); p = p11*math.exp(-G0*(h_m-11000)/(R_AIR*T))
    return T, p, p/(R_AIR*T)

def isa_ft(h_ft): return isa(h_ft*FT)
'''

# ===================================================================== 01
n1 = nb([
    md("""# Module 01: Khí quyển chuẩn ISA / The International Standard Atmosphere
**AE2.008 · USTH: Aerodynamics and Flight Mechanics**

🇻🇳 Notebook cài đặt ISA bằng code, đối chiếu các con số trong **EASA Module 08** (Hình 1-3, 1-4, 1-7), giải lại các bài **Anderson 1.1, 1.11, 1.12** và dùng `assert` để tự kiểm các đáp án quiz của module.

🇬🇧 This notebook implements ISA in code, checks the numbers in **EASA Module 08** (Figures 1-3, 1-4, 1-7), re-solves **Anderson 1.1, 1.11, 1.12** and uses `assert` to self-check the module's quiz answers."""),
    code(ISA),
    md("## 1. Đơn vị áp suất / Pressure units (EASA Fig. 1-3)"),
    code('''atm = P0
print(f"1 atm = {atm/PSI:.2f} psi = {atm/3386.389:.2f} inHg = {atm/100:.1f} hPa = {atm/133.322:.0f} mmHg")
assert abs(atm/PSI - 14.7) < 0.01 and abs(atm/3386.389 - 29.92) < 0.01 and abs(atm/133.322 - 760) < 0.5'''),
    md("## 2. Áp suất ở 40 000 ft / Pressure at 40 000 ft (EASA Fig. 1-4: 2.72 psi)"),
    code('''T, p, rho = isa_ft(40000)
print(f"40 000 ft: T = {T-273.15:.1f} C, p = {p/PSI:.3f} psi = {p/P0*100:.1f}% of sea level")
assert abs(p/PSI - 2.72) < 0.01'''),
    md("## 3. Bảng ISA / ISA table (EASA Fig. 1-7)"),
    code('''print(f"{'h [ft]':>8} {'T [C]':>8} {'p [hPa]':>9} {'p [psi]':>8} {'rho [kg/m3]':>12}")
for h in (0, 5000, 10000, 20000, 30000, 36089, 40000):
    T, p, rho = isa_ft(h)
    print(f"{h:>8} {T-273.15:>8.1f} {p/100:>9.1f} {p/PSI:>8.2f} {rho:>12.4f}")
# EASA Fig. 1-7: sea level 14.67 psi, 1013.53 hPa, 1.23 kg/m3; 5000 ft 12.05 psi, 5.1 C
T, p, rho = isa_ft(5000); assert abs(T-273.15-5.1) < 0.2
T, p, rho = isa(11000); assert abs(T-273.15+56.5) < 1e-6 and abs(rho/RHO0 - 0.2971) < 0.001'''),
    md("## 4. Anderson 1.1 / 1.11 / 1.12"),
    code('''# 1.1a
rho_a = 1.9e4/(287*203); print("1.1a rho =", round(rho_a, 3), "kg/m3"); assert abs(rho_a-0.326) < 5e-4
# 1.1b
T_b = 1058/(1.23e-3*1716); print("1.1b T =", round(T_b), "R"); assert round(T_b) == 501
# 1.11  U-tube: high column on model side -> lower pressure
p_model = 1.01e5 - 1.36e4*9.8*0.2; print("1.11 p =", round(p_model), "N/m2"); assert abs(p_model-7.43e4) < 50
# 1.12  Zeppelin: W = buoyancy + aerodynamic lift
rho1000 = isa(1000)[2]; B = 15000*rho1000*9.8
S = math.pi*14**2/4; q = 0.5*rho1000*30**2; Lift = q*S*0.05
print(f"1.12 rho(1000 m) = {rho1000:.4f}, B = {B:.0f} N, q = {q:.1f}, S = {S:.1f}, L = {Lift:.0f} N, W = {B+Lift:.0f} N")
assert abs(rho1000-1.1117) < 5e-4 and abs(Lift-3847) < 5 and abs((B+Lift)-1.67e5) < 1e3
# The Solution Manual (4th ed.) prints L = 3487 N on one line but uses 3847 N in the next: typo, final answer correct.'''),
    md("## 5. Độ cao mật độ / Density altitude (ví dụ minh họa / illustrative example)"),
    code('''T5, p5, _ = isa_ft(5000)
rho_hot = p5/(R_AIR*(30+273.15))
lo, hi = 0.0, 15000.0
for _ in range(80):
    mid = (lo+hi)/2
    if isa(mid)[2] > rho_hot: lo = mid
    else: hi = mid
print(f"5000 ft, 30 C: rho = {rho_hot:.3f} kg/m3 = {rho_hot/RHO0*100:.0f}% of sea level, density altitude = {lo/FT:.0f} ft")
assert 7000 < lo/FT < 9000'''),
    md("## 6. Kiểm quiz / Quiz self-check"),
    code('''assert abs(isa(1000)[2]-1.1117) < 5e-4            # Anderson 1.12
assert abs(isa(3000)[2]-0.9093) < 5e-4            # used in module 02 (Anderson 4.11)
assert round((P0/100),2) == 1013.25               # 1 atm in hPa
assert abs(isa(11000)[0]-273.15 - (-56.5)) < 1e-6  # ISA tropopause temperature
assert abs((isa_ft(36089)[2]/RHO0) - 0.30) < 0.005 # density ratio at tropopause
print("All Module 01 checks passed.")'''),
])

# ===================================================================== 02
n2 = nb([
    md("""# Module 02: Khí động lực học / Aerodynamics
**AE2.008 · USTH: Aerodynamics and Flight Mechanics**

🇻🇳 Giải lại các bài **Anderson 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10, 4.11, 4.12**, vẽ đường cong C_L theo góc tấn của NACA 2412 (số liệu từ bài 1.6) và đường cực lý thuyết, rồi `assert` các đáp án quiz.

🇬🇧 Re-solves **Anderson 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10, 4.11, 4.12**, plots the NACA 2412 C_L-versus-angle curve (data from Problem 1.6) and a theoretical polar, then asserts the quiz answers."""),
    code(ISA + "\nimport numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n"),
    md("## 1. Hệ số lực / Force coefficients (Anderson 1.5)"),
    code('''a = math.radians(12); cn, ca = 1.2, 0.03
cl = cn*math.cos(a) - ca*math.sin(a); cd = cn*math.sin(a) + ca*math.cos(a)
print(f"1.5: cl = {cl:.4f}, cd = {cd:.4f}"); assert abs(cl-1.1675) < 5e-4 and abs(cd-0.2788) < 5e-4'''),
    md("## 2. Bernoulli: Venturi, hầm gió, Pitot (Anderson 3.3, 3.4, 3.6, 3.7)"),
    code('''rho = 1.23
vac = 0.5*rho*90**2*(1/0.85**2 - 1);                 print("3.3 vacuum =", round(vac), "N/m2"); assert abs(vac-1913) < 2
dp = 1.36e4*9.81*0.10; V = math.sqrt(2*dp/(rho*(1-1/144))); print("3.4 V =", round(V, 1), "m/s"); assert abs(V-147.8) < 0.1
V6 = math.sqrt(2*(1.07e5-1.01e5)/rho);               print("3.6 V =", round(V6, 1), "m/s"); assert abs(V6-98.8) < 0.1
cp = 1 - (130/V6)**2;                                print("3.7 Cp =", round(cp, 3));     assert abs(cp+0.732) < 1e-3
G = 6/(rho*30);                                       print("3.18 Gamma =", round(G, 4), "m2/s"); assert abs(G-0.1626) < 1e-3'''),
    md("## 3. Biên dạng NACA 2412 (Anderson 1.6, 4.1, 4.2, 4.10, 4.11, 4.12)"),
    code('''# Table from Problem 1.6
alpha = np.array([-2, 0, 2, 4, 6, 8, 10, 12, 14.0])
cl_t  = np.array([0.05, 0.25, 0.44, 0.64, 0.85, 1.08, 1.26, 1.43, 1.56])
cd_t  = np.array([0.006, 0.006, 0.006, 0.007, 0.0075, 0.0092, 0.0115, 0.0150, 0.0186])
cm_t  = np.array([-0.042, -0.040, -0.038, -0.036, -0.036, -0.036, -0.034, -0.030, -0.025])
slope = np.polyfit(alpha[:6], cl_t[:6], 1); print("lift slope = %.4f /deg (2*pi/rad = %.4f /deg)" % (slope[0], 2*math.pi*math.pi/180))
# 4.2
c = 2.0; q = 0.5*1.23*50**2; cl42 = 1353/(q*c); print("4.2 cl =", round(cl42, 3)); assert abs(cl42-0.44) < 1e-9
assert alpha[np.argmin(abs(cl_t-cl42))] == 2          # alpha = 2 deg
# 4.1 (cl and cm at 4 deg from Problem 4.10)
q1 = 0.5*0.002377*50**2; L1 = q1*2*0.65; M1 = q1*4*(-0.037); print(f"4.1 L' = {L1:.3f} lb/ft, M'c/4 = {M1:.4f} ft lb/ft"); assert abs(L1-3.863) < 0.01
# 4.5 thin symmetric airfoil
cl45 = 2*math.pi*math.radians(1.5); cm45 = -cl45/4; print(f"4.5 cl = {cl45:.4f}, cm,LE = {cm45:.4f}"); assert abs(cl45-0.1645) < 1e-4
# 4.10 aerodynamic centre
hac = 0.25 - (-0.037-(-0.045))/(0.65-(-0.39)); print("4.10 x_ac/c =", round(hac, 4)); assert abs(hac-0.2423) < 1e-4
# 4.11, 4.12
r3 = isa(3000)[2]; q3 = 0.5*r3*60**2; Lp = q3*2*0.65; Gam = Lp/(r3*60)
print(f"4.11 rho = {r3:.4f}, L' = {Lp:.0f} N/m; 4.12 Gamma = {Gam:.1f} m2/s"); assert abs(Lp-2127) < 2 and abs(Gam-39.0) < 0.1'''),
    md("## 4. Đồ thị / Plots"),
    code('''fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(alpha, cl_t, "o-"); ax[0].set(xlabel="alpha [deg]", ylabel="c_l", title="NACA 2412: c_l vs alpha"); ax[0].grid(True)
ax[1].plot(cd_t, cl_t, "s-"); ax[1].set(xlabel="c_d", ylabel="c_l", title="NACA 2412: drag polar (section)"); ax[1].grid(True)
fig.tight_layout(); fig.savefig("naca2412_curves.png", dpi=100); print("saved naca2412_curves.png")
best = np.argmax(cl_t/cd_t); print(f"max section c_l/c_d = {cl_t[best]/cd_t[best]:.0f} at alpha = {alpha[best]} deg")'''),
    md("## 5. Kiểm quiz / Quiz self-check"),
    code('''AR = 12**2/20; assert AR == 7.2                         # generated question
assert abs((1-(math.sqrt(2))**2)+1) < 1e-12              # Cp = -1 at V = sqrt(2) V_inf
assert abs(4 - (200/100)**2) < 1e-12                     # lift x4 when speed x2
print("All Module 02 checks passed.")'''),
])

# ===================================================================== 03
n3 = nb([
    md("""# Module 03: Lý thuyết bay / Theory of Flight
**AE2.008 · USTH: Aerodynamics and Flight Mechanics**

🇻🇳 Giải lại **Anderson 5.4, 5.5, 8.1, 8.7, 8.11, 11.4**, tính bảng hệ số tải và tốc độ thất tốc trong vòng bay, kiểm tốc độ âm thanh của EASA (661 kt và 574 kt) rồi `assert` các đáp án quiz.

🇬🇧 Re-solves **Anderson 5.4, 5.5, 8.1, 8.7, 8.11, 11.4**, builds the load-factor and turn-stall table, checks the EASA speeds of sound (661 kt and 574 kt) and asserts the quiz answers."""),
    code(ISA + '''
def a_sound(T, R=R_AIR, g=GAMMA): return math.sqrt(g*R*T)
def pitot_ratio(M, g=GAMMA): return (1+(g-1)/2*M*M)**(g/(g-1))
def bisect(f, lo, hi, n=200):
    for _ in range(n):
        mid = (lo+hi)/2
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo+hi)/2
'''),
    md("## 1. Piper Cherokee (Anderson 5.4, 5.5)"),
    code('''S, b, W = 170.0, 32.0, 2450.0; AR = b*b/S
V = 120*5280/3600; q = 0.5*0.002377*V**2; CL = W/(q*S)
a0, tau, aL0 = 0.1033, 0.12, -3.0
a = a0/(1 + 57.3*a0/(math.pi*AR)*(1+tau)); alpha = CL/a + aL0
e = 0.64; CDi = CL**2/(math.pi*e*AR); Di = CDi*q*S
print(f"AR = {AR:.3f}, V = {V:.0f} ft/s, q = {q:.2f}, CL = {CL:.4f}, a = {a:.4f}/deg, alpha = {alpha:.2f} deg, CDi = {CDi:.5f}, Di = {Di:.1f} lb")
assert abs(CL-0.3915) < 5e-4 and abs(alpha-2.12) < 0.01 and abs(Di-79.2) < 0.2'''),
    md("## 2. Tốc độ âm thanh và Mach / Speed of sound and Mach number"),
    code('''kt = 0.514444
a_sl = a_sound(T0)/kt; a_40 = a_sound(isa_ft(40000)[0])/kt
print(f"a(sea level) = {a_sl:.1f} kt (EASA: 661), a(40 000 ft) = {a_40:.1f} kt (EASA: 574)")
assert abs(a_sl-661) < 1 and abs(a_40-574) < 1
a81 = a_sound(230, 287); print("8.1 a =", round(a81, 1), "m/s"); assert abs(a81-304.0) < 0.1
M = bisect(lambda m: pitot_ratio(m)-1.555, 0.0, 1.0); V811 = M*a_sound(288, 287)
print(f"8.11 M = {M:.4f}, V = {V811:.1f} m/s"); assert abs(M-0.8199) < 1e-3 and abs(V811-278.9) < 0.2
V_bern = math.sqrt(2*0.555*101325/1.225); print(f"Bernoulli (wrong) V = {V_bern:.1f} m/s, error {abs(V_bern-V811)/V811*100:.1f}%")'''),
    md("## 3. Sóng xung kích thẳng / Normal shock (Anderson 8.7)"),
    code('''g = GAMMA; M1 = 2.6
M2 = math.sqrt(((g-1)*M1**2+2)/(2*g*M1**2-(g-1))); p = 1+2*g/(g+1)*(M1**2-1)
rho = (g+1)*M1**2/((g-1)*M1**2+2); T = p/rho
print(f"M2 = {M2:.4f}, p2/p1 = {p:.3f}, rho2/rho1 = {rho:.3f}, T2/T1 = {T:.3f}, T2 = {T*288:.1f} K")
assert abs(M2-0.5039) < 1e-3 and abs(p-7.72) < 1e-3 and M2 < 1'''),
    md("## 4. Số Mach tới hạn / Critical Mach number (Anderson 11.4)"),
    code('''def cp_crit(M, g=GAMMA): return 2/(g*M*M)*(((1+(g-1)/2*M*M)/((g+1)/2))**(g/(g-1))-1)
Mcr = bisect(lambda m: -0.41/math.sqrt(1-m*m)-cp_crit(m), 0.3, 0.99)
print("Prandtl-Glauert Mcr =", round(Mcr, 4)); assert abs(Mcr-0.7436) < 1e-3'''),
    md("## 5. Hệ số tải trong vòng bay / Load factor in a level turn"),
    code('''print("bank  n     sqrt(n)  stall-speed increase")
for phi in (0, 30, 45, 60, 70):
    n = 1/math.cos(math.radians(phi)); print(f"{phi:>3}  {n:5.2f}  {math.sqrt(n):6.3f}  {(math.sqrt(n)-1)*100:5.0f}%")
assert abs(1/math.cos(math.radians(60))-2) < 1e-12
assert abs(60*math.sqrt(2)-84.85) < 0.01               # quiz: 60 kt stall -> ~85 kt at 60 deg bank
assert abs(3.8*1.5-5.7) < 1e-12                        # ultimate = 1.5 x limit (EASA p. 3.9)
assert abs(0.8*a_40-459) < 1                           # M 0.8 at 40 000 ft ~ 459 kt TAS
assert 36000/3000 == 12                                # glide ratio quiz'''),
    md("## 6. Kiểm quiz / Quiz self-check"),
    code('print("All Module 03 checks passed.")'),
])

for name, n in (("01_atmosphere", n1), ("02_aerodynamics", n2), ("03_theory-of-flight", n3)):
    with open(os.path.join(OUT, name + ".ipynb"), "w", encoding="utf-8") as f:
        nbf.write(n, f)
    print("wrote", name)
