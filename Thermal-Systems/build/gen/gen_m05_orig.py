"""m05 ORIGINAL items, part 1 (origin 'goc'): the slide examples of Chapter 5 (= Cengel Examples 17-1, 17-3, 17-4, 17-5, 17-6 and Problems 17-6, 17-8, 17-10), solved by route A
(build/gen/m05_common.py) and registered for the independent route B of build/verify/verify_m05.py.  Every slide Ch.5 tr.3-59 and Cengel PDF 852-871, 900-907 was read as an image.
build() -> list of items; printed answers go into m05_common.PRN."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from m05_common import *
ITEMS = []
def add(it): ITEMS.append(it); return it

# ================================================================== numbers (route A)
# ---- Example 17-1 = slide tr.10-13
T1a, P1a, Va = 255.7, 54.05, 250.0; cpA = 1.005; kA = 1.4; RA = 0.287
T01a = reg('stag', dict(T=T1a, P=P1a, V=Va, k=kA, R=RA, cp=cpA), 'T0', T0_of(T1a, Va, cpA), 1e-9, 'Ex17-1 / slide tr.11: 286.8')
P01a = reg('stag', dict(T=T1a, P=P1a, V=Va, k=kA, R=RA, cp=cpA), 'P0', P0_of(P1a, T1a, T01a, kA), 1e-9, 'Ex17-1 / slide tr.12: 80.77')
T02a = reg('comp', dict(T01=T01a, pr=8.0, k=kA, R=RA, cp=cpA), 'T02', T01a * 8.0 ** ((kA - 1) / kA), 1e-9, 'slide tr.13: 519.5')
wa = reg('comp', dict(T01=T01a, pr=8.0, k=kA, R=RA, cp=cpA), 'w', cpA * (T02a - T01a), 1e-9, 'slide tr.13: 233.9')
prn('Ex17-1 T01 (slide tr.11)', 286.8, T01a, 2e-4); prn('Ex17-1 P01 (slide tr.12)', 80.77, P01a, 2e-4); prn('Ex17-1 T02 (slide tr.13)', 519.5, T02a, 2e-4); prn('Ex17-1 w (slide tr.13)', 233.9, wa, 2e-4)
# ---- slide tr.14 = Cengel 17-6 (probe temperatures)
probe = {V: reg('stag', dict(T=300.0, P=100.0, V=float(V), k=kA, R=RA, cp=cpA), 'T0', T0_of(300.0, V, cpA), 1e-9, f'17-6 V={V}') for V in (1, 10, 100, 1000)}
# ---- slide tr.15 = Cengel 17-8 (printed 5.27 kW)
T01c = 27.0 + 273.15; T02c = T01c * 9.0 ** ((kA - 1) / kA); wc = cpA * (T02c - T01c); Pc = reg('comp', dict(T01=T01c, pr=9.0, k=kA, R=RA, cp=cpA, mdot=0.02), 'P', wc * 0.02, 1e-9, '17-8: 5.27 kW')
prn('Cengel 17-8 power (kW)', 5.27, Pc, 2e-3, 'T01 = 300.15 K; with 300 K the result is 5.267')
# ---- slide tr.16 = Cengel 17-10 (no printed answer)
k16, R16 = 1.33, 0.287; cp16 = cp_of(k16, R16); T01d = 750.0 + 273.15; T02d = T01d * (100.0 / 1000.0) ** ((k16 - 1) / k16); w16 = reg('comp', dict(T01=T01d, pr=0.1, k=k16, R=R16), 'w', cp16 * (T01d - T02d), 1e-9, '17-10 turbine w per unit mass (no printed answer)')
# ---- Example 17-3 = slide tr.18-22 (CO2 duct)
kC, RC, cpC = 1.289, 0.1889, 0.846; T0C, P0C = 473.0, 1400.0
def co2(P, cpm='kR'):
    T = T0C * (P / P0C) ** ((kC - 1) / kC); cp_ = cp_of(kC, RC) if cpm == 'kR' else cpC
    V = math.sqrt(2000.0 * cp_ * (T0C - T)); rho = P / (RC * T); c = csound(kC, RC, T); A = 3.0 / (rho * V) * 1e4 if V > 0 else float('inf')
    return dict(T=T, V=V, rho=rho, c=c, A=A, Ma=V / c)
rc = {P: co2(P) for P in (1200, 1000, 800, 767, 600, 400, 200)}
for P, r in rc.items():
    for key in ('T', 'V', 'rho', 'c', 'A', 'Ma'): reg('isenP', dict(P=float(P), P0=P0C, T0=T0C, k=kC, R=RC, mdot=3.0, cpmode='kR'), key, r[key], 1e-9, f'Ex17-3 P={P}')
r1200 = rc[1200]
# slide tr.22 table, printed (T, V, rho, c, A, Ma)
SLC = {1200: (457, 164.5, 13.9, 333.6, 13.1, 0.493), 1000: (439, 240.7, 12.1, 326.9, 10.3, 0.736), 800: (417, 306.6, 10.1, 318.8, 9.64, 0.962), 767: (413, 317.2, 9.82, 317.2, 9.63, 1.000),
       600: (391, 371.4, 8.12, 308.7, 10.0, 1.203), 400: (357, 441.9, 5.93, 295.0, 11.5, 1.498), 200: (306, 530.9, 3.46, 272.9, 16.3, 1.946)}
for P, row in SLC.items():
    for nm_, pv, key, tol in zip(('T', 'V', 'rho', 'c', 'A', 'Ma'), row, ('T', 'V', 'rho', 'c', 'A', 'Ma'), (3e-3, 2e-3, 1e-2, 2e-3, 1e-2, 2e-3)):
        prn(f'Slide tr.22 table P={P} {nm_}', pv, rc[P][key], tol, 'slide table follows cp = kR/(k-1) = 0.8425, not the 0.846 of tr.19' if nm_ == 'V' else '')
# ---- Example 17-4 = slide tr.36-38
cC = reg('crit', dict(k=kC), 'PP', crit(kC)['PP'], 1e-9, 'Ex17-4 P*/P0'); cT = reg('crit', dict(k=kC), 'TT', crit(kC)['TT'], 1e-9, 'Ex17-4 T*/T0'); Tst = cT * T0C; Pst = cC * P0C
prn('Ex17-4 T*/T0 (slide tr.37)', 0.8737, cT, 1e-4); prn('Ex17-4 P*/P0 (slide tr.37)', 0.5477, cC, 1e-4); prn('Ex17-4 T* (slide tr.38)', 413.0, Tst, 1e-3); prn('Ex17-4 P* (slide tr.38)', 767.0, Pst, 1e-3)
# ---- Example 17-5 = slide tr.50-55
At5 = 50e-4
T0i5 = reg('stag', dict(T=873.0, P=1000.0, V=150.0, k=1.4, R=0.287, cp=1.005), 'T0', T0_of(873.0, 150.0, 1.005), 1e-9, 'Ex17-5 / slide tr.51: 884 K'); P0i5 = reg('stag', dict(T=873.0, P=1000.0, V=150.0, k=1.4, R=0.287, cp=1.005), 'P0', P0_of(1000.0, 873.0, T0i5, 1.4), 1e-9, 'Ex17-5: 1.045 MPa')
prn('Ex17-5 T0 (slide tr.51)', 884.0, T0i5, 3e-4); prn('Ex17-5 P0 (slide tr.51)', 1045.0, P0i5, 1e-3)
na = conv_nozzle(700.0, P0i5, T0i5, 1.4, 0.287, At5); nb = conv_nozzle(400.0, P0i5, T0i5, 1.4, 0.287, At5)
for key in ('Pe', 'Ma', 'V', 'mdot'): reg('cnoz', dict(Pb=700.0, P0=P0i5, T0=T0i5, k=1.4, R=0.287, A=At5), key, na[key], 1e-9, f'Ex17-5 (a) {key}'); reg('cnoz', dict(Pb=400.0, P0=P0i5, T0=T0i5, k=1.4, R=0.287, A=At5), key, nb[key], 1e-9, f'Ex17-5 (b) {key}')
m55r = reg('choked', dict(A=At5, P0=1045.0, T0=884.0, k=1.4, R=0.287), 'mdot', mdot_choked(At5, 1045.0, 884.0, 1.4, 0.287), 1e-9, 'slide tr.55 with the slide\'s rounded 1045 kPa, 884 K')
lit55 = At5 * 1045.0 * math.sqrt(1.4 / (0.287 * 884.0)) * (2.0 / 2.4) ** (2.4 / 0.8)
prn('Ex17-5 (a) mdot (slide tr.54)', 6.77, na['mdot'], 3e-3, 'slide uses Table A-32 interpolation Ma_t = 0.778 (exact 0.7794)'); prn('Ex17-5 (b) mdot (slide tr.55)', 7.10, m55r, 1e-3, 'slide prints 7.10; formula with rounded inputs 7.103'); prn('Ex17-5 P*/P0 (slide tr.52)', 0.5283, crit(1.4)['PP'], 2e-4)
# ---- Example 17-6 = slide tr.56-59
A1s = reg('isenMa', dict(Ma=0.3, k=1.4), 'AA', AAs(0.3, 1.4), 1e-9, 'Ex17-6 A1/A* = 2.0351'); A2s = 0.8 * A1s
M2 = reg('duct', dict(Ma1=0.3, A2A1=0.8, k=1.4, branch='sub'), 'Ma2', Ma_of_AA(A2s, 1.4), 1e-9, 'Ex17-6 Ma2 (slide 0.391)')
TT2 = reg('duct', dict(Ma1=0.3, A2A1=0.8, k=1.4, branch='sub'), 'TT2', TT0(M2, 1.4), 1e-9, 'T2/T0'); PP2 = reg('duct', dict(Ma1=0.3, A2A1=0.8, k=1.4, branch='sub'), 'PP2', PP0(M2, 1.4), 1e-9, 'P2/P0')
T2n = 400.0 * TT2 / TT0(0.3, 1.4); P2n = 100.0 * PP2 / PP0(0.3, 1.4); reg('duct', dict(Ma1=0.3, A2A1=0.8, k=1.4, branch='sub', T1=400.0, P1=100.0), 'T2', T2n, 1e-9, 'T2 395'); reg('duct', dict(Ma1=0.3, A2A1=0.8, k=1.4, branch='sub', T1=400.0, P1=100.0), 'P2', P2n, 1e-9, 'P2 95.91')
prn('Ex17-6 A1/A* (slide tr.57)', 2.0351, A1s, 1e-4); prn('Ex17-6 A2/A* (slide tr.57)', 1.6281, A2s, 1e-4); prn('Ex17-6 T2 (slide tr.59)', 395.0, T2n, 2e-3); prn('Ex17-6 Ma2 (slide tr.58, table interpolation)', 0.391, M2, 1e-2, 'slide 0.391, exact 0.3887 (-0.6 %)')
prn('Ex17-6 P2 (slide tr.59, table interpolation)', 95.7, P2n, 3e-3, 'slide 95.7, exact 95.91 (+0.22 %)')
# ---- Cengel Example 17-2 (book only) c at 30 C
c172 = reg('sound', dict(k=1.4, R=0.287, T=303.0, V=200.0), 'c', csound(1.4, 0.287, 303.0), 1e-9, 'Ex17-2 c'); M172 = reg('sound', dict(k=1.4, R=0.287, T=303.0, V=200.0), 'Ma', 200.0 / c172, 1e-9, 'Ex17-2 Ma')
prn('Ex17-2 c', 349.0, c172, 1e-3); prn('Ex17-2 Ma', 0.573, M172, 1e-3)

def build():
    S = ITEMS
    # ============================================================ 1. Example 17-1 = slides tr.10-13 (compression of high-speed air)
    add(ess(B('Slide Ch.5 tr.10–13 (Cengel Ví dụ 17–1). Máy bay bay ở 250 m/s tại độ cao 5000 m, nơi áp suất khí quyển là 54,05 kPa và nhiệt độ không khí là 255,7 K. Không khí được làm chậm trong diffuser trước khi vào máy nén. Giả thiết diffuser và máy nén đều đẳng entropi, không khí là khí lý tưởng với nhiệt dung riêng không đổi ở nhiệt độ phòng. Xác định (a) áp suất hãm ở cửa vào máy nén, (b) công nén riêng nếu tỉ số áp suất hãm của máy nén là 8.',
               'Slide Ch.5 p.10–13 (Cengel Example 17–1). An aircraft is flying at a cruising speed of 250 m/s at an altitude of 5000 m where the atmospheric pressure is 54.05 kPa and the ambient air temperature is 255.7 K. The ambient air is first decelerated in a diffuser before it enters the compressor. Assume both the diffuser and the compressor are isentropic and air is an ideal gas with constant specific heats at room temperature. Determine (a) the stagnation pressure at the compressor inlet, (b) the required compressor work per unit mass if the stagnation pressure ratio of the compressor is 8.'),
             B(f'''Giả thiết (slide tr.10): diffuser và máy nén đẳng entropi; khí lý tưởng, c_p = 1,005 kJ/(kg·K), k = 1,4 (A-2a; slide tr.11).
(a) Nhiệt độ hãm (tr.11, công thức (1)/(7) của slide): T₀₁ = T₁ + V₁²/(2c_p) = 255.7 K + (250 m/s)²/(2 × 1.005 kJ/(kg·K) × 1000 (m²/s²)/(kJ/kg)) = 255.7 + {N(Va**2/2010,2)} = {N(T01a,1)} K (slide 286,8 K).
Áp suất hãm (tr.12, (2)): P₀₁ = P₁(T₀₁/T₁)^(k/(k−1)) = 54.05 kPa × ({N(T01a,1)}/255.7)^3.5 = {N(P01a,2)} kPa (slide 80,77 kPa). Nhiệt độ tăng {N(T01a-T1a,1)} °C và áp suất tăng {N(P01a-P1a,2)} kPa khi không khí bị hãm từ 250 m/s về 0 (động năng → entanpi, tr.12).
(b) T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01a,1)} K × 8^(0.4/1.4) = {N(T02a,1)} K (tr.13). w_in = c_p(T₀₂ − T₀₁) = 1.005 × ({N(T02a,1)} − {N(T01a,1)}) = {N(wa,1)} kJ/kg (slide 233,9 kJ/kg). Không có nhiệt, thế năng bỏ qua (slide (5)).
Đơn vị từng dòng: m²/s² = J/kg nên chia 1000 để ra kJ/kg; kJ/kg ÷ kJ/(kg·K) = K; kPa × (không thứ nguyên) = kPa.
Hai đường: (A) công thức đóng như trên; (B) verify_m05.py tích phân số dT = −V dV/c_p từ V = 250 về 0 và d ln P = k/(k−1) d ln T (scipy solve_ivp), công nén w = ∫ v dP = ∫ RT d ln P (scipy quad): trùng đến 1e-6.''',
               f'''Assumptions (slide p.10): diffuser and compressor isentropic; ideal gas, c_p = 1.005 kJ/(kg·K), k = 1.4 (A-2a; slide p.11).
(a) Stagnation temperature (p.11, slide eq. (1)/(7)): T₀₁ = T₁ + V₁²/(2c_p) = 255.7 K + (250 m/s)²/(2 × 1.005 kJ/(kg·K) × 1000 (m²/s²)/(kJ/kg)) = 255.7 + {N(Va**2/2010,2)} = {N(T01a,1)} K (slide 286.8 K).
Stagnation pressure (p.12, (2)): P₀₁ = P₁(T₀₁/T₁)^(k/(k−1)) = 54.05 kPa × ({N(T01a,1)}/255.7)^3.5 = {N(P01a,2)} kPa (slide 80.77 kPa). The temperature rises by {N(T01a-T1a,1)} °C and the pressure by {N(P01a-P1a,2)} kPa when the air is brought from 250 m/s to rest (kinetic energy → enthalpy, p.12).
(b) T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01a,1)} K × 8^(0.4/1.4) = {N(T02a,1)} K (p.13). w_in = c_p(T₀₂ − T₀₁) = 1.005 × ({N(T02a,1)} − {N(T01a,1)}) = {N(wa,1)} kJ/kg (slide 233.9 kJ/kg). No heat, potential energy neglected (slide (5)).
Units line by line: m²/s² = J/kg so divide by 1000 to get kJ/kg; kJ/kg ÷ kJ/(kg·K) = K; kPa × (dimensionless) = kPa.
Two routes: (A) the closed forms above; (B) verify_m05.py integrates dT = −V dV/c_p from V = 250 to 0 and d ln P = k/(k−1) d ln T numerically (scipy solve_ivp) and the work w = ∫ v dP = ∫ RT d ln P (scipy quad): agreement to 1e-6.'''),
             2, TOP['stag'], SLIDE('10–13', 'Ex 17-1'), 'goc', 'script + slide p.11-13 (printed 286.8 K, 80.77 kPa, 519.5 K, 233.9 kJ/kg)'))
    add(numq('Slide Ch.5 tr.10–11 (Cengel Ví dụ 17–1): không khí ở T₁ = 255,7 K, V₁ = 250 m/s, c_p = 1,005 kJ/(kg·K). Nhiệt độ hãm T₀₁ ở cửa vào máy nén là:',
             'Slide Ch.5 p.10–11 (Cengel Example 17–1): air at T₁ = 255.7 K, V₁ = 250 m/s, c_p = 1.005 kJ/(kg·K). The stagnation temperature T₀₁ at the compressor inlet is:',
             T01a, [(T1a + Va**2 / 1005.0, 'quên hệ số 2 trong V²/(2c_p)', 'forgets the factor 2 in V²/(2c_p)'), (T1a - Va**2 / 2010.0, 'trừ thay vì cộng nhiệt độ động', 'subtracts instead of adds the dynamic temperature'),
                    (T1a + Va**2 / (2 * 0.718 * 1000.0), 'dùng c_v = 0,718 thay cho c_p', 'uses c_v = 0.718 instead of c_p'), (T1a + Va**2 / 2.01, 'quên đổi m²/s² → kJ/kg (không chia 1000)', 'forgets the m²/s² → kJ/kg conversion (no division by 1000)')],
             'K', 1, f'T₀₁ = T₁ + V₁²/(2c_p) = 255.7 + 250²/(2 × 1.005 × 1000) = 255.7 + {N(Va**2/2010,2)} = {N(T01a,1)} K (slide 286,8 K). Các phương án còn lại:',
             f'T₀₁ = T₁ + V₁²/(2c_p) = 255.7 + 250²/(2 × 1.005 × 1000) = 255.7 + {N(Va**2/2010,2)} = {N(T01a,1)} K (slide 286.8 K). The other options:', 1, TOP['stag'], SLIDE('11', 'Ex 17-1'), 'goc', 'script + slide p.11 (printed 286.8 K)'))
    add(numq('Slide Ch.5 tr.12 (Cengel Ví dụ 17–1): với T₁ = 255,7 K, P₁ = 54,05 kPa, T₀₁ = 286,8 K và k = 1,4, áp suất hãm P₀₁ ở cửa vào máy nén (dòng đẳng entropi) là:',
             'Slide Ch.5 p.12 (Cengel Example 17–1): with T₁ = 255.7 K, P₁ = 54.05 kPa, T₀₁ = 286.8 K and k = 1.4, the stagnation pressure P₀₁ at the compressor inlet (isentropic flow) is:',
             P01a, [(P1a * (T01a / T1a) ** ((kA - 1) / kA), 'đảo mũ: dùng (k−1)/k thay cho k/(k−1)', 'inverts the exponent: uses (k−1)/k instead of k/(k−1)'), (P1a * T01a / T1a, 'dùng tỉ số nhiệt độ mũ 1 (đẳng áp)', 'uses the temperature ratio to the power 1 (isobaric)'),
                    (P1a * (T01a / T1a) ** kA, 'dùng mũ k thay cho k/(k−1)', 'uses the exponent k instead of k/(k−1)'), (P1a + (T01a - T1a), 'cộng ΔT (°C) vào áp suất', 'adds ΔT (°C) to the pressure')],
             'kPa', 2, f'P₀₁ = P₁(T₀₁/T₁)^(k/(k−1)) = 54.05 × (286.8/255.7)^3.5 = {N(P01a,2)} kPa (slide 80,77 kPa); mũ k/(k−1) = 3,5. Các phương án còn lại:',
             f'P₀₁ = P₁(T₀₁/T₁)^(k/(k−1)) = 54.05 × (286.8/255.7)^3.5 = {N(P01a,2)} kPa (slide 80.77 kPa); the exponent k/(k−1) = 3.5. The other options:', 2, TOP['stag'], SLIDE('12', 'Ex 17-1'), 'goc', 'script + slide p.12 (printed 80.77 kPa)'))
    add(numq('Slide Ch.5 tr.13 (Cengel Ví dụ 17–1): không khí vào máy nén ở T₀₁ = 286,8 K; tỉ số áp suất hãm của máy nén là 8 (đẳng entropi, c_p = 1,005 kJ/(kg·K), k = 1,4). Công nén riêng là:',
             'Slide Ch.5 p.13 (Cengel Example 17–1): air enters the compressor at T₀₁ = 286.8 K; the stagnation pressure ratio of the compressor is 8 (isentropic, c_p = 1.005 kJ/(kg·K), k = 1.4). The compressor work per unit mass is:',
             wa, [(cpA * T02a, 'lấy c_p·T₀₂ thay vì c_p(T₀₂ − T₀₁)', 'takes c_p·T₀₂ instead of c_p(T₀₂ − T₀₁)'), (cpA * (T01a * 8 ** kA - T01a), 'dùng mũ k thay cho (k−1)/k cho T₀₂', 'uses the exponent k instead of (k−1)/k for T₀₂'),
                  (cpA * (T01a * 8 ** ((kA - 1) / kA) - T1a), 'lấy hiệu T₀₂ − T₁ (nhiệt độ tĩnh bay)', 'takes T₀₂ − T₁ (the static flight temperature)'), (cpA * (T01a * 8 ** (1 / kA) - T01a), 'dùng mũ 1/k', 'uses the exponent 1/k')],
             'kJ/kg', 1, f'T₀₂ = 286.8 × 8^(0.4/1.4) = {N(T02a,1)} K; w = 1.005 × ({N(T02a,1)} − 286.8) = {N(wa,1)} kJ/kg (slide 233,9). Các phương án còn lại:',
             f'T₀₂ = 286.8 × 8^(0.4/1.4) = {N(T02a,1)} K; w = 1.005 × ({N(T02a,1)} − 286.8) = {N(wa,1)} kJ/kg (slide 233.9). The other options:', 2, TOP['comp'], SLIDE('13', 'Ex 17-1'), 'goc', 'script + slide p.13 (printed 233.9 kJ/kg)'))
    # ============================================================ 2. slide tr.14 = Cengel 17-6
    add(ess(B('Slide Ch.5 tr.14 (Cengel Bài 17–6, slide không in đáp án). Không khí ở 300 K chảy trong ống với vận tốc (a) 1, (b) 10, (c) 100 và (d) 1000 m/s. Xác định nhiệt độ mà đầu dò đứng yên đặt trong ống sẽ chỉ ở mỗi trường hợp.',
               'Slide Ch.5 p.14 (Cengel Problem 17–6, no printed answer on the slide). Air at 300 K is flowing in a duct at a velocity of (a) 1, (b) 10, (c) 100 and (d) 1000 m/s. Determine the temperature that a stationary probe inserted into the duct will read for each case.'),
             B(f'''Đầu dò đứng yên làm không khí dừng đoạn nhiệt nên chỉ nhiệt độ hãm T₀ = T + V²/(2c_p) (slide tr.7). Giả thiết (slide không nêu, ta chọn theo Cengel): khí lý tưởng, c_p = 1,005 kJ/(kg·K) ở nhiệt độ phòng.
(a) V = 1 m/s: V²/(2c_p) = 1/(2 × 1.005 × 1000) = {N(1/2010,5)} K → T₀ = {N(probe[1],4)} K ≈ 300.0 K.
(b) V = 10 m/s: 100/2010 = {N(100/2010,4)} K → T₀ = {N(probe[10],3)} K ≈ 300.05 K.
(c) V = 100 m/s: 10⁴/2010 = {N(1e4/2010,3)} K → T₀ = {N(probe[100],2)} K ≈ 304.98 K (tr.7: nhiệt kế 300 → 305 K).
(d) V = 1000 m/s: 10⁶/2010 = {N(1e6/2010,1)} K → T₀ = {N(probe[1000],1)} K ≈ 797.5 K.
Đơn vị: m²/s² ÷ 1000 → kJ/kg; ÷ kJ/(kg·K) → K.
Lưu ý: ở (d) ΔT ≈ 500 K nên c_p không đổi 1,005 là xấp xỉ thô; với bảng A-17 (c_p biến thiên) T₀ ≈ 780,1 K (thấp hơn 2,2 %). Với V ≤ 100 m/s sai khác không đáng kể.
Hai đường: (A) công thức trên; (B) tích phân số dT = −V dV/c_p (scipy solve_ivp) cho cùng kết quả; (C) A-17: h₀ = h(300 K) + V²/2 rồi tìm T₀ bằng brentq (chỉ để đánh giá giả thiết c_p không đổi, xem verify_m05.py).''',
               f'''A stationary probe brings the air to rest adiabatically, so it reads the stagnation temperature T₀ = T + V²/(2c_p) (slide p.7). Assumption (not stated on the slide; we follow Cengel): ideal gas, c_p = 1.005 kJ/(kg·K) at room temperature.
(a) V = 1 m/s: V²/(2c_p) = 1/(2 × 1.005 × 1000) = {N(1/2010,5)} K → T₀ = {N(probe[1],4)} K ≈ 300.0 K.
(b) V = 10 m/s: 100/2010 = {N(100/2010,4)} K → T₀ = {N(probe[10],3)} K ≈ 300.05 K.
(c) V = 100 m/s: 10⁴/2010 = {N(1e4/2010,3)} K → T₀ = {N(probe[100],2)} K ≈ 304.98 K (p.7: the thermometer rises 300 → 305 K).
(d) V = 1000 m/s: 10⁶/2010 = {N(1e6/2010,1)} K → T₀ = {N(probe[1000],1)} K ≈ 797.5 K.
Units: m²/s² ÷ 1000 → kJ/kg; ÷ kJ/(kg·K) → K.
Note: in (d) ΔT ≈ 500 K, so a constant c_p = 1.005 is a rough approximation; with Table A-17 (variable c_p) T₀ ≈ 780.1 K (2.2 % lower). For V ≤ 100 m/s the difference is negligible.
Two routes: (A) the formula above; (B) numerical integration of dT = −V dV/c_p (scipy solve_ivp) gives the same; (C) A-17: h₀ = h(300 K) + V²/2 then brentq for T₀ (only to judge the constant-c_p assumption, see verify_m05.py).'''),
             1, TOP['stag'], SLIDE('14', 'Prob 17-6'), 'goc', 'script (no printed answer on the slide or in the book for 17-6; method tested on Cengel 17-5 and 17-8 first)'))
    add(numq('Slide Ch.5 tr.14 (Cengel Bài 17–6, câu c): không khí ở 300 K chảy với vận tốc 100 m/s. Đầu dò đứng yên chỉ nhiệt độ (c_p = 1,005 kJ/(kg·K)):',
             'Slide Ch.5 p.14 (Cengel Problem 17–6, part c): air at 300 K flows at 100 m/s. A stationary probe reads (c_p = 1.005 kJ/(kg·K)):',
             probe[100], [(300.0 + 100.0**2 / 1005.0, 'quên hệ số 2', 'forgets the factor 2'), (300.0 + 100.0**2 / 2.01, 'quên chia 1000 (m²/s² → kJ/kg)', 'forgets the division by 1000 (m²/s² → kJ/kg)'), (300.0 - 100.0**2 / 2010.0, 'trừ thay vì cộng', 'subtracts instead of adds'), (300.0 + 100.0 / 2.01 / 1000.0, 'dùng V thay cho V²', 'uses V instead of V²')],
             'K', 2, f'T₀ = T + V²/(2c_p) = 300 + 100²/(2 × 1.005 × 1000) = 300 + {N(1e4/2010,3)} = {N(probe[100],2)} K ≈ 305 K (khớp nhiệt kế slide tr.7). Các phương án còn lại:',
             f'T₀ = T + V²/(2c_p) = 300 + 100²/(2 × 1.005 × 1000) = 300 + {N(1e4/2010,3)} = {N(probe[100],2)} K ≈ 305 K (matches the thermometer on slide p.7). The other options:', 1, TOP['stag'], SLIDE('14', 'Prob 17-6'), 'goc', 'script (no printed answer; same formula as the slide example p.11)'))
    add(numq('Slide Ch.5 tr.14 (Cengel Bài 17–6, câu d): không khí ở 300 K chảy với vận tốc 1000 m/s. Giả thiết c_p = 1,005 kJ/(kg·K) không đổi: đầu dò đứng yên chỉ',
             'Slide Ch.5 p.14 (Cengel Problem 17–6, part d): air at 300 K flows at 1000 m/s. Assuming a constant c_p = 1.005 kJ/(kg·K), a stationary probe reads',
             probe[1000], [(300.0 + 1000.0**2 / 1005.0, 'quên hệ số 2', 'forgets the factor 2'), (300.0 + 1000.0**2 / 2.01, 'không đổi m²/s² → kJ/kg', 'no m²/s² → kJ/kg conversion'), (300.0 + 1000.0**2 / 2010.0 / 1.4, 'chia thêm k = 1,4', 'divides additionally by k = 1.4'), (300.0 * (1 + 0.2 * (1000.0 / csound(1.4, 0.287, 300.0))**2), 'đúng công thức Ma nhưng bỏ 1 (lấy T₀/T = 0,2Ma²)', 'right Ma formula but drops the 1 (T₀/T = 0.2 Ma²)')],
             'K', 1, f'T₀ = 300 + 1000²/(2 × 1.005 × 1000) = 300 + {N(1e6/2010,1)} = {N(probe[1000],1)} K. Đây là kết quả với c_p hằng; với c_p biến thiên (A-17) khoảng 780 K. Các phương án còn lại:',
             f'T₀ = 300 + 1000²/(2 × 1.005 × 1000) = 300 + {N(1e6/2010,1)} = {N(probe[1000],1)} K. This is the constant-c_p result; with variable c_p (A-17) it is about 780 K. The other options:', 2, TOP['stag'], SLIDE('14', 'Prob 17-6'), 'goc', 'script + A-17 cross-check (no printed answer)'))
    # ============================================================ 3. slide tr.15 = Cengel 17-8 (printed 5.27 kW)
    add(ess(B('Slide Ch.5 tr.15 (Cengel Bài 17–8, đáp án in 5,27 kW). Không khí vào máy nén với áp suất hãm 100 kPa và nhiệt độ hãm 27 °C, được nén tới áp suất hãm 900 kPa. Giả thiết quá trình nén đẳng entropi, xác định công suất cấp cho máy nén khi lưu lượng khối là 0,02 kg/s.',
               'Slide Ch.5 p.15 (Cengel Problem 17–8, printed answer 5.27 kW). Air enters a compressor with a stagnation pressure of 100 kPa and a stagnation temperature of 27°C, and it is compressed to a stagnation pressure of 900 kPa. Assuming the compression process to be isentropic, determine the power input to the compressor for a mass flow rate of 0.02 kg/s.'),
             B(f'''Giả thiết: khí lý tưởng c_p = 1,005 kJ/(kg·K), k = 1,4 (A-2a); T₀₁ = 27 + 273,15 = {N(T01c,2)} K.
T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01c,2)} × 9^(0.4/1.4) = {N(T02c,1)} K.
w = c_p(T₀₂ − T₀₁) = 1.005 × ({N(T02c,1)} − {N(T01c,2)}) = {N(wc,1)} kJ/kg. Công suất: Ẇ = ṁ w = 0.02 kg/s × {N(wc,1)} kJ/kg = {N(Pc,3)} kW ≈ 5.27 kW (đáp án in).
Đơn vị: kg/s × kJ/kg = kJ/s = kW. Nhạy cảm làm tròn: với 300 K thay cho 300,15 K được {N(0.02*cpA*300.0*(9**((kA-1)/kA)-1),3)} kW (vẫn ≈ 5,27 trong 0,1 %).
Hai đường: (A) công thức đóng; (B) w = ∫ v dP = ∫ RT d ln P (scipy quad) cho cùng kết quả; (C) bảng A-17 (P_r) cho 5,258 kW (c_p biến thiên, −0,2 %). Đường A đã được thử trên bài này (có đáp án in) trước khi dùng cho tr.16.''',
               f'''Assumptions: ideal gas, c_p = 1.005 kJ/(kg·K), k = 1.4 (A-2a); T₀₁ = 27 + 273.15 = {N(T01c,2)} K.
T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01c,2)} × 9^(0.4/1.4) = {N(T02c,1)} K.
w = c_p(T₀₂ − T₀₁) = 1.005 × ({N(T02c,1)} − {N(T01c,2)}) = {N(wc,1)} kJ/kg. Power: Ẇ = ṁ w = 0.02 kg/s × {N(wc,1)} kJ/kg = {N(Pc,3)} kW ≈ 5.27 kW (printed answer).
Units: kg/s × kJ/kg = kJ/s = kW. Rounding sensitivity: with 300 K instead of 300.15 K the result is {N(0.02*cpA*300.0*(9**((kA-1)/kA)-1),3)} kW (still ≈ 5.27 within 0.1 %).
Two routes: (A) closed form; (B) w = ∫ v dP = ∫ RT d ln P (scipy quad) gives the same; (C) Table A-17 (P_r) gives 5.258 kW (variable c_p, −0.2 %). Route A was tested on this problem (printed answer) before it was used for p.16.'''),
             2, TOP['comp'], SLIDE('15', 'Prob 17-8'), 'goc', 'printed answer 5.27 kW + script'))
    add(numq('Slide Ch.5 tr.15 (Cengel Bài 17–8): không khí vào máy nén ở T₀ = 27 °C, P₀ = 100 kPa và ra ở 900 kPa (đẳng entropi, c_p = 1,005 kJ/(kg·K), k = 1,4), lưu lượng 0,02 kg/s. Công suất máy nén là:',
             'Slide Ch.5 p.15 (Cengel Problem 17–8): air enters a compressor at T₀ = 27 °C, P₀ = 100 kPa and leaves at 900 kPa (isentropic, c_p = 1.005 kJ/(kg·K), k = 1.4), mass flow 0.02 kg/s. The compressor power is:',
             Pc, [(0.02 * cpA * (T01c * 9 ** (1 / kA) - T01c), 'dùng mũ 1/k', 'uses the exponent 1/k'), (cpA * (T02c - T01c), 'quên nhân lưu lượng 0,02 kg/s (đây là kJ/kg)', 'forgets the 0.02 kg/s flow (this is kJ/kg)'), (0.02 * cpA * (27.0 * 9 ** ((kA - 1) / kA) - 27.0), 'dùng °C trong tỉ số nhiệt độ hãm', 'uses °C in the stagnation temperature ratio'), (0.02 * cpA * T02c, 'lấy c_p·T₀₂ thay vì độ tăng', 'takes c_p·T₀₂ instead of the rise')],
             'kW', 2, f'T₀₂ = 300.15 × 9^0.2857 = {N(T02c,1)} K; w = 1.005 × ({N(T02c,1)} − 300.15) = {N(wc,1)} kJ/kg; Ẇ = 0.02 × {N(wc,1)} = {N(Pc,2)} kW (đáp án in 5,27 kW). Các phương án còn lại:',
             f'T₀₂ = 300.15 × 9^0.2857 = {N(T02c,1)} K; w = 1.005 × ({N(T02c,1)} − 300.15) = {N(wc,1)} kJ/kg; Ẇ = 0.02 × {N(wc,1)} = {N(Pc,2)} kW (printed answer 5.27 kW). The other options:', 2, TOP['comp'], SLIDE('15', 'Prob 17-8'), 'goc', 'printed answer 5.27 kW + script'))
    # ============================================================ 4. slide tr.16 = Cengel 17-10 (turbine, no printed answer)
    add(ess(B('Slide Ch.5 tr.16 (Cengel Bài 17–10, không có đáp án in). Sản phẩm cháy vào tuabin khí với áp suất hãm 1,0 MPa và nhiệt độ hãm 750 °C, giãn nở tới áp suất hãm 100 kPa. Lấy k = 1,33 và R = 0,287 kJ/(kg·K) cho sản phẩm cháy, giả thiết quá trình giãn nở đẳng entropi: xác định công suất ra của tuabin trên một đơn vị lưu lượng khối.',
               'Slide Ch.5 p.16 (Cengel Problem 17–10, no printed answer). Products of combustion enter a gas turbine with a stagnation pressure of 1.0 MPa and a stagnation temperature of 750°C, and they expand to a stagnation pressure of 100 kPa. Taking k = 1.33 and R = 0.287 kJ/(kg·K) for the products of combustion, and assuming the expansion process to be isentropic, determine the power output of the turbine per unit mass flow.'),
             B(f'''Giả thiết: khí lý tưởng, k = 1,33 và R = 0,287 kJ/(kg·K) cho trước; nhiệt dung riêng c_p = kR/(k−1) = 1.33 × 0.287/0.33 = {N(cp16,4)} kJ/(kg·K).
T₀₁ = 750 + 273,15 = {N(T01d,2)} K. T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01d,2)} × 0.1^(0.33/1.33) = {N(T02d,1)} K (0.1^0.2481 = {N(0.1**((k16-1)/k16),4)}).
w_out = c_p(T₀₁ − T₀₂) = {N(cp16,4)} × ({N(T01d,2)} − {N(T02d,1)}) = {N(cp16*(T01d-T02d),1)} kJ/kg, tức công suất ra riêng ≈ 515 kJ/(kg/s) = 515 kW trên mỗi kg/s lưu lượng.
Đơn vị: kJ/(kg·K) × K = kJ/kg; kJ/kg × (kg/s) = kW.
Hai đường: (A) công thức đóng; (B) w = −∫ v dP = ∫ RT d ln P (scipy quad) từ 100 kPa đến 1 MPa dọc đường đẳng entropi: trùng. Phương pháp (A) đã được thử trên Bài 17–8 (có đáp án in 5,27 kW) trước khi áp dụng ở đây. Không đối chiếu được đáp án in (sách và slide không in).''',
               f'''Assumptions: ideal gas, k = 1.33 and R = 0.287 kJ/(kg·K) given; specific heat c_p = kR/(k−1) = 1.33 × 0.287/0.33 = {N(cp16,4)} kJ/(kg·K).
T₀₁ = 750 + 273.15 = {N(T01d,2)} K. T₀₂ = T₀₁ (P₀₂/P₀₁)^((k−1)/k) = {N(T01d,2)} × 0.1^(0.33/1.33) = {N(T02d,1)} K (0.1^0.2481 = {N(0.1**((k16-1)/k16),4)}).
w_out = c_p(T₀₁ − T₀₂) = {N(cp16,4)} × ({N(T01d,2)} − {N(T02d,1)}) = {N(cp16*(T01d-T02d),1)} kJ/kg, i.e. a specific power of ≈ 515 kJ/(kg/s) = 515 kW per kg/s of flow.
Units: kJ/(kg·K) × K = kJ/kg; kJ/kg × (kg/s) = kW.
Two routes: (A) closed form; (B) w = −∫ v dP = ∫ RT d ln P (scipy quad) from 100 kPa to 1 MPa along the isentrope: identical. Method (A) was tested on Problem 17–8 (printed answer 5.27 kW) before use here. No printed answer to compare (neither the book nor the slide prints one).'''),
             2, TOP['comp'], SLIDE('16', 'Prob 17-10'), 'goc', 'script (no printed answer; method tested on 17-8)'))
    add(numq('Slide Ch.5 tr.16 (Cengel Bài 17–10): sản phẩm cháy (k = 1,33; R = 0,287 kJ/(kg·K)) vào tuabin ở T₀ = 750 °C, P₀ = 1,0 MPa, giãn nở đẳng entropi tới 100 kPa. Công riêng của tuabin xấp xỉ:',
             'Slide Ch.5 p.16 (Cengel Problem 17–10): combustion products (k = 1.33; R = 0.287 kJ/(kg·K)) enter a turbine at T₀ = 750 °C, P₀ = 1.0 MPa and expand isentropically to 100 kPa. The specific work of the turbine is about:',
             w16, [(cp_of(1.4, 0.287) * T01d * (1 - 0.1 ** (0.4 / 1.4)), 'dùng k = 1,4 của không khí thay cho 1,33', 'uses k = 1.4 of air instead of 1.33'), (cp_of(k16, R16) * T01d * (1 - 0.1 ** (1 / k16)), 'dùng mũ 1/k', 'uses the exponent 1/k'),
                   (0.287 * T01d * (1 - 0.1 ** ((k16 - 1) / k16)), 'dùng R thay cho c_p', 'uses R instead of c_p'), (cp_of(k16, R16) * (T01d - 273.15) * (1 - 0.1 ** ((k16 - 1) / k16)), 'dùng °C thay cho K', 'uses °C instead of K')],
             'kJ/kg', 0, f'c_p = kR/(k−1) = {N(cp16,4)}; T₀₂ = {N(T01d,2)} × 0.1^0.2481 = {N(T02d,1)} K; w = c_p(T₀₁ − T₀₂) = {N(w16,1)} kJ/kg. Các phương án còn lại:',
             f'c_p = kR/(k−1) = {N(cp16,4)}; T₀₂ = {N(T01d,2)} × 0.1^0.2481 = {N(T02d,1)} K; w = c_p(T₀₁ − T₀₂) = {N(w16,1)} kJ/kg. The other options:', 3, TOP['comp'], SLIDE('16', 'Prob 17-10'), 'goc', 'script (no printed answer; method tested on 17-8)'))
    return S
