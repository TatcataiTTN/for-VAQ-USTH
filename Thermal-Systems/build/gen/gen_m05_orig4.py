"""m05 ORIGINAL items, part 4 (origin 'goc'): Cengel Example 17-7 (converging-diverging nozzle, PDF 870-871), Cengel 17-41, 17-44, 17-62, 17-63, 17-65, 17-128, 17-134 (no printed answer; method tested on the
problems of part 3 that have one) and the Fundamentals-of-Engineering items 17-151...17-158, 17-160 whose five options are the book's own (PDF 906-907).
Everything is solved by route A (closed forms) and registered for route B (verify_m05.py)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from m05_common import *
from gen_m05_orig3 import fe
ITEMS = []
def add(it): ITEMS.append(it); return it
k, R, cp = 1.4, 0.287, 1.005

def build():
    # ---------------------------------------------------------------- Example 17-7 (book §17-4)
    P0, T0, As, Mae = 1000.0, 800.0, 20.0, 2.0
    cr = crit(k); Ts = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Ts', cr['TT'] * T0, 1e-9, 'Ex17-7 T*'); Vs = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Vs', csound(k, R, Ts), 1e-9, 'Ex17-7 V*')
    rho0 = P0 / (R * T0); rhos = cr['rr'] * rho0; ms = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'mdot', mdot_choked(As * 1e-4, P0, T0, k, R), 1e-9, 'Ex17-7 mdot')
    Pe = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Pe', P0 * PP0(Mae, k), 1e-9, 'Ex17-7 Pe'); Te = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Te', T0 * TT0(Mae, k), 1e-9, 'Ex17-7 Te')
    Ae = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Ae', As * AAs(Mae, k), 1e-9, 'Ex17-7 Ae'); Ve = reg('cdexit', dict(P0=P0, T0=T0, k=k, R=R, As=As, Mae=Mae), 'Ve', Mae * csound(k, R, Te), 1e-9, 'Ex17-7 Ve')
    for nm_, pv, ov, tol in (('T*', 666.6, Ts, 2e-4), ('V*', 517.5, Vs, 2e-4), ('rho*', 2.761, rhos, 1e-3), ('mdot', 2.86, ms, 2e-3), ('Pe (kPa; the book prints 0.1278 MPa)', 127.8, Pe, 2e-4), ('Te', 444.5, Te, 2e-4), ('Ae', 33.75, Ae, 2e-4), ('Ve', 845.1, Ve, 5e-4)): prn(f'Cengel Ex 17-7 {nm_}', pv, ov, tol)
    add(ess(B('Cengel Ví dụ 17–7 (§17-4; sách in đáp án). Không khí vào vòi hội tụ–phân kỳ ở 1,0 MPa và 800 K với vận tốc không đáng kể; dòng ổn định, một chiều, đẳng entropi, k = 1,4. Với Ma ở cửa ra bằng 2 và diện tích cổ họng 20 cm², xác định (a) các điều kiện ở cổ họng, (b) các điều kiện ở mặt cắt cửa ra gồm diện tích cửa ra, (c) lưu lượng khối qua vòi phun.',
               'Cengel Example 17–7 (§17-4; the book prints the answers). Air enters a converging–diverging nozzle at 1.0 MPa and 800 K with negligible velocity; the flow is steady, one-dimensional and isentropic with k = 1.4. For an exit Mach number of 2 and a throat area of 20 cm², determine (a) the throat conditions, (b) the exit-plane conditions including the exit area, and (c) the mass flow rate through the nozzle.'),
             B(f'''Giả thiết: khí lý tưởng k = 1,4; R = 0,287 kJ/(kg·K). Vì vận tốc vào ≈ 0: P₀ = 1,0 MPa, T₀ = 800 K; ρ₀ = P₀/(RT₀) = 1000/(0.287 × 800) = {N(rho0,3)} kg/m³ (kPa/(kPa·m³/(kg·K)·K)).
(a) Cổ họng Ma = 1 (A-32: P*/P₀ = 0,5283; T*/T₀ = 0,8333; ρ*/ρ₀ = 0,6339): P* = {N(cr["PP"]*P0,1)} kPa (sách 0,5283 MPa); T* = {N(Ts,1)} K; ρ* = {N(rhos,3)} kg/m³ (sách 2,761); V* = c* = √(kRT*) = {N(Vs,1)} m/s (sách 517,5).
(b) Cửa ra Ma = 2 (A-32: P/P₀ = 0,1278; T/T₀ = 0,5556; ρ/ρ₀ = 0,2300; A/A* = 1,6875): P_e = {N(Pe,1)} kPa = 0,1278 MPa; T_e = {N(Te,1)} K; A_e = 1,6875 × 20 = {N(Ae,2)} cm² (sách 33,75); V_e = Ma √(kRT_e) = 2 × {N(csound(k,R,Te),1)} = {N(Ve,1)} m/s (sách 845,2; 845,1 theo Ma*).
(c) ṁ = ρ*A*V* = {N(rhos,3)} × 20×10⁻⁴ × {N(Vs,1)} = {N(ms,3)} kg/s (sách 2,86): đây là lưu lượng lớn nhất qua vòi với điều kiện vào đã cho (dòng nghẹt).
Lỗi in của sách (ghi trong mục lỗi nguồn): dòng "P_e = 0,1278 P₀ = (0,1278)(10 MPa) = 0,1278 MPa" ghi P₀ = 10 MPa; đề cho 1,0 MPa.
Đơn vị: cm² ↔ m² (×10⁻⁴); kPa/(kJ/kg·K · K) = kg/m³.
Hai đường: (A) công thức đóng (9)–(17) (khớp hàng in A-32 tại Ma = 1 và 2); (B) verify_m05.py: cổ họng bằng cực đại số của ρV (scipy), cửa ra bằng brentq trên A/A* (nhánh siêu âm), ṁ = ρVA tại cửa ra phải bằng ṁ cổ họng (bảo toàn khối lượng); thermo.js qua node.''',
               f'''Assumptions: ideal gas k = 1.4; R = 0.287 kJ/(kg·K). Inlet velocity ≈ 0: P₀ = 1.0 MPa, T₀ = 800 K; ρ₀ = P₀/(RT₀) = 1000/(0.287 × 800) = {N(rho0,3)} kg/m³ (kPa/(kPa·m³/(kg·K)·K)).
(a) Throat Ma = 1 (A-32: P*/P₀ = 0.5283; T*/T₀ = 0.8333; ρ*/ρ₀ = 0.6339): P* = {N(cr["PP"]*P0,1)} kPa (book 0.5283 MPa); T* = {N(Ts,1)} K; ρ* = {N(rhos,3)} kg/m³ (book 2.761); V* = c* = √(kRT*) = {N(Vs,1)} m/s (book 517.5).
(b) Exit Ma = 2 (A-32: P/P₀ = 0.1278; T/T₀ = 0.5556; ρ/ρ₀ = 0.2300; A/A* = 1.6875): P_e = {N(Pe,1)} kPa = 0.1278 MPa; T_e = {N(Te,1)} K; A_e = 1.6875 × 20 = {N(Ae,2)} cm² (book 33.75); V_e = Ma √(kRT_e) = 2 × {N(csound(k,R,Te),1)} = {N(Ve,1)} m/s (book 845.2; 845.1 via Ma*).
(c) ṁ = ρ*A*V* = {N(rhos,3)} × 20×10⁻⁴ × {N(Vs,1)} = {N(ms,3)} kg/s (book 2.86): the largest flow this nozzle can pass for the given inlet conditions (choked).
Printed error in the book (recorded in the source-errors list): the line "P_e = 0.1278 P₀ = (0.1278)(10 MPa) = 0.1278 MPa" writes P₀ = 10 MPa; the statement gives 1.0 MPa.
Units: cm² ↔ m² (×10⁻⁴); kPa/(kJ/kg·K · K) = kg/m³.
Two routes: (A) closed forms (9)–(17) (matching the printed A-32 rows at Ma = 1 and 2); (B) verify_m05.py: throat as the numerical maximum of ρV (scipy), exit by brentq on A/A* (supersonic branch), and ṁ = ρVA at the exit must equal the throat flow (mass conservation); thermo.js through node.'''),
             3, TOP['cd'], CEX('17–7'), 'goc', 'printed answers (book p.844-845) + script + node thermo.js + A-32 rows Ma=1, 2'))
    add(numq('Cengel Ví dụ 17–7 (§17-4): không khí 1,0 MPa, 800 K vào vòi hội tụ–phân kỳ với vận tốc không đáng kể; Ma cửa ra = 2; diện tích cổ họng 20 cm²; k = 1,4. Diện tích mặt cắt cửa ra là:',
             'Cengel Example 17–7 (§17-4): air at 1.0 MPa, 800 K enters a converging–diverging nozzle with negligible velocity; exit Ma = 2; throat area 20 cm²; k = 1.4. The exit-plane area is:',
             Ae, [(As * AAs(0.5, k), 'chọn nhầm nghiệm cận âm A/A* = 1,3398 (Ma = 0,5)', 'takes the subsonic root A/A* = 1.3398 (Ma = 0.5)'), (As / AAs(Mae, k), 'chia thay vì nhân cho A/A*', 'divides instead of multiplies by A/A*'), (As * PP0(Mae, k), 'dùng P/P₀ = 0,1278 thay cho A/A*', 'uses P/P₀ = 0.1278 instead of A/A*'), (As * 2.0, 'lấy A_e = Ma × A*', 'takes A_e = Ma × A*')],
             'cm²', 2, f'Ma_e = 2 siêu âm nên lấy A/A* = (1/2)[(2/2,4)(1 + 0,2 × 4)]³ = {N(AAs(Mae,k),4)} (A-32: 1,6875); A_e = 1,6875 × 20 = {N(Ae,2)} cm² (sách 33,75). Các phương án còn lại:',
             f'Ma_e = 2 is supersonic so A/A* = (1/2)[(2/2.4)(1 + 0.2 × 4)]³ = {N(AAs(Mae,k),4)} (A-32: 1.6875); A_e = 1.6875 × 20 = {N(Ae,2)} cm² (book 33.75). The other options:', 3, TOP['area'], CEX('17–7'), 'goc', 'printed answer 33.75 cm2 + script + A-32 row Ma=2'))
    add(numq('Cengel Ví dụ 17–7 (§17-4): vòi hội tụ–phân kỳ có A* = 20 cm², P₀ = 1,0 MPa, T₀ = 800 K (k = 1,4; R = 0,287 kJ/(kg·K)), dòng nghẹt. Lưu lượng khối qua vòi phun là:',
             'Cengel Example 17–7 (§17-4): a converging–diverging nozzle with A* = 20 cm², P₀ = 1.0 MPa, T₀ = 800 K (k = 1.4; R = 0.287 kJ/(kg·K)), choked flow. The mass flow rate through the nozzle is:',
             ms, [(ms * math.sqrt(1000.0), 'P₀ theo Pa và R theo J nhưng thêm √1000 thừa', 'P₀ in Pa and R in J but with an extra √1000'), (ms / math.sqrt(1000.0), 'thiếu √1000: kPa và kJ/(kg·K) thay thẳng vào căn', 'missing √1000: kPa and kJ/(kg·K) plugged straight into the root'), (ms * 0.5283 / 0.5787, 'dùng P*/P₀ thay cho (2/(k+1))^((k+1)/(2(k−1)))', 'uses P*/P₀ instead of (2/(k+1))^((k+1)/(2(k−1)))')],
             'kg/s', 2, f'ṁ = A*P₀√(k/(RT₀))(2/(k+1))³ = 20×10⁻⁴ × 10⁶ × √(1,4/(287 × 800)) × 0,5787 = {N(ms,3)} kg/s (sách 2,86 = ρ*A*V*). Các phương án còn lại:',
             f'ṁ = A*P₀√(k/(RT₀))(2/(k+1))³ = 20×10⁻⁴ × 10⁶ × √(1.4/(287 × 800)) × 0.5787 = {N(ms,3)} kg/s (book 2.86 = ρ*A*V*). The other options:', 2, TOP['unit'], CEX('17–7'), 'goc', 'printed answer 2.86 kg/s + script + node thermo.js'))
    add(numq('Cengel Ví dụ 17–7 (§17-4): trong vòi phun trên (P₀ = 1,0 MPa, T₀ = 800 K, k = 1,4, R = 0,287 kJ/(kg·K)), vận tốc ở mặt cắt cửa ra Ma = 2 là:',
             'Cengel Example 17–7 (§17-4): in the same nozzle (P₀ = 1.0 MPa, T₀ = 800 K, k = 1.4, R = 0.287 kJ/(kg·K)), the velocity at the exit plane where Ma = 2 is:',
             Ve, [(2.0 * Vs, 'lấy Ma × c* (tốc độ âm ở cổ họng)', 'takes Ma × c* (the throat speed of sound)'), (2.0 * csound(k, R, T0), 'lấy Ma × c₀ (tốc độ âm hãm)', 'takes Ma × c₀ (the stagnation speed of sound)'), (math.sqrt(2000.0 * cp * T0), 'lấy V = √(2c_pT₀) (giãn nở tới T = 0)', 'takes V = √(2c_pT₀) (expansion to T = 0)')],
             'm/s', 1, f'T_e = 0,5556 × 800 = {N(Te,1)} K; c_e = √(1,4 × 287 × {N(Te,1)}) = {N(csound(k,R,Te),1)} m/s; V_e = 2c_e = {N(Ve,1)} m/s (sách 845,2). Cách khác: V_e = Ma*_e c* = 1,6330 × 517,5 = 845,1 m/s. Các phương án còn lại:',
             f'T_e = 0.5556 × 800 = {N(Te,1)} K; c_e = √(1.4 × 287 × {N(Te,1)}) = {N(csound(k,R,Te),1)} m/s; V_e = 2c_e = {N(Ve,1)} m/s (book 845.2). Alternatively V_e = Ma*_e c* = 1.6330 × 517.5 = 845.1 m/s. The other options:', 3, TOP['cd'], CEX('17–7'), 'goc', 'printed answer 845.1-845.2 m/s + script'))
    # ---------------------------------------------------------------- 17-41 and 17-44
    st41 = {nm_: reg('stagMa', dict(T=373.15, P=200.0, Ma=0.8, k=k, R=R), nm_, v_, 1e-9, f'17-41 {nm_}') for nm_, v_ in (('V', 0.8 * csound(k, R, 373.15)), ('T0', 373.15 * (1 + 0.2 * 0.64)), ('P0', 200.0 / PP0(0.8, k)), ('rho0', (200.0 / PP0(0.8, k)) / (R * 373.15 * (1 + 0.2 * 0.64))))}
    add(numq('Cengel Bài 17–41 (§17-3): không khí ở 200 kPa, 100 °C và Ma = 0,8 chảy trong ống (k = 1,4; R = 0,287 kJ/(kg·K)). Áp suất hãm là:',
             'Cengel Problem 17–41 (§17-3): air at 200 kPa, 100°C and Ma = 0.8 flows through a duct (k = 1.4; R = 0.287 kJ/(kg·K)). The stagnation pressure is:',
             st41['P0'], [(200.0 * (1 + 0.2 * 0.8), 'quên bình phương Ma và mũ 3,5', 'forgets squaring Ma and the exponent 3.5'), (200.0 * (1 + 0.2 * 0.64), 'không có mũ 3,5 (lấy T₀/T)', 'omits the exponent 3.5 (takes T₀/T)'), (200.0 * (1 - 0.2 * 0.64) ** 3.5, 'trừ thay vì cộng 0,2Ma²', 'subtracts instead of adds 0.2Ma²'), (200.0 * (1 + 0.2 * 0.64) ** 2.5, 'dùng mũ 1/(k−1) = 2,5 (khối lượng riêng)', 'uses the exponent 1/(k−1) = 2.5 (density)')],
             'kPa', 1, f'T₀ = 373,15 × (1 + 0,2 × 0,64) = {N(st41["T0"],1)} K; P₀ = 200 × (1 + 0,2 × 0,64)^3,5 = {N(st41["P0"],1)} kPa (A-32: P/P₀ = 0,6560 tại Ma = 0,8). Cũng: V = 0,8 √(1,4 × 287 × 373,15) = {N(st41["V"],1)} m/s; ρ₀ = {N(st41["rho0"],3)} kg/m³. Không có đáp án in; phương pháp đã thử trên Bài 17–5 (đáp án in). Các phương án còn lại:',
             f'T₀ = 373.15 × (1 + 0.2 × 0.64) = {N(st41["T0"],1)} K; P₀ = 200 × (1 + 0.2 × 0.64)^3.5 = {N(st41["P0"],1)} kPa (A-32: P/P₀ = 0.6560 at Ma = 0.8). Also V = 0.8 √(1.4 × 287 × 373.15) = {N(st41["V"],1)} m/s; ρ₀ = {N(st41["rho0"],3)} kg/m³. No printed answer; the method was tested on Problem 17–5 (printed answer). The other options:', 2, TOP['rel'], CEN('17–41'), 'goc', 'script + A-32 row Ma=0.8 (no printed answer; method tested on 17-5)'))
    T44 = reg('stagMa', dict(T=236.15, P=35.0, Ma=1.2, k=k, R=R), 'T0', 236.15 * (1 + 0.2 * 1.44), 1e-9, '17-44')
    add(numq('Cengel Bài 17–44 (§17-3): máy bay thiết kế bay hành trình ở Ma = 1,2 tại độ cao 8000 m, nơi nhiệt độ khí quyển là 236,15 K. Nhiệt độ hãm ở mép trước cánh là (k = 1,4):',
             'Cengel Problem 17–44 (§17-3): an aircraft is designed to cruise at Ma = 1.2 at 8000 m where the atmospheric temperature is 236.15 K. The stagnation temperature on the leading edge of the wing is (k = 1.4):',
             T44, [(236.15 * (1 + 0.2 * 1.2), 'quên bình phương Ma', 'forgets squaring Ma'), (236.15 * (1 + 0.4 * 1.44), 'dùng (k−1) thay cho (k−1)/2', 'uses (k−1) instead of (k−1)/2'), (236.15 / (1 + 0.2 * 1.44), 'chia thay vì nhân (lấy T/T₀)', 'divides instead of multiplies (takes T/T₀)')],
             'K', 1, f'T₀ = T(1 + (k−1)Ma²/2) = 236,15 × (1 + 0,2 × 1,44) = {N(T44,1)} K ≈ 31 °C: nóng hơn môi trường 68 K. (A-32: T/T₀ = 0,7764 tại Ma = 1,2.) Không có đáp án in. Các phương án còn lại:',
             f'T₀ = T(1 + (k−1)Ma²/2) = 236.15 × (1 + 0.2 × 1.44) = {N(T44,1)} K ≈ 31 °C: 68 K hotter than the ambient air. (A-32: T/T₀ = 0.7764 at Ma = 1.2.) No printed answer. The other options:', 1, TOP['rel'], CEN('17–44'), 'goc', 'script + A-32 row Ma=1.2 (no printed answer)'))
    # ---------------------------------------------------------------- 17-62, 17-63
    kN, RN = 1.4, 0.2968; c62 = {nm_: reg('critst', dict(k=kN, P0=700.0, T0=450.0, R=RN), nm_, v_, 1e-9, f'17-62 {nm_}') for nm_, v_ in (('Ts', crit(kN)['TT'] * 450.0), ('Ps', crit(kN)['PP'] * 700.0), ('rhos', crit(kN)['PP'] * 700.0 / (RN * crit(kN)['TT'] * 450.0)), ('Vs', csound(kN, RN, crit(kN)['TT'] * 450.0)))}
    add(numq('Cengel Bài 17–62 (§17-4): nitơ (k = 1,4; R = 0,2968 kJ/(kg·K)) vào vòi hội tụ–phân kỳ ở 700 kPa và 450 K với vận tốc không đáng kể. Vận tốc tới hạn (ở cổ họng khi nghẹt) là:',
             'Cengel Problem 17–62 (§17-4): nitrogen (k = 1.4; R = 0.2968 kJ/(kg·K)) enters a converging–diverging nozzle at 700 kPa and 450 K with negligible velocity. The critical velocity (at the throat when choked) is:',
             c62['Vs'], [(csound(kN, RN, 450.0), 'tốc độ âm hãm c₀ ở 450 K', 'the stagnation speed of sound c₀ at 450 K'), (csound(1.4, 0.287, c62['Ts']), 'dùng R của không khí (0,287)', 'uses R of air (0.287)'), (csound(kN, RN, 0.5283 * 450.0), 'dùng T* = 0,5283T₀ (nhầm P*/P₀)', 'uses T* = 0.5283T₀ (mixes up P*/P₀)')],
             'm/s', 1, f'T* = 0,8333 × 450 = {N(c62["Ts"],1)} K; P* = 0,5283 × 700 = {N(c62["Ps"],1)} kPa; ρ* = P*/(RT*) = {N(c62["rhos"],3)} kg/m³; V* = c* = √(kRT*) = √(1,4 × 296,8 × {N(c62["Ts"],1)}) = {N(c62["Vs"],1)} m/s. Không có đáp án in. Các phương án còn lại:',
             f'T* = 0.8333 × 450 = {N(c62["Ts"],1)} K; P* = 0.5283 × 700 = {N(c62["Ps"],1)} kPa; ρ* = P*/(RT*) = {N(c62["rhos"],3)} kg/m³; V* = c* = √(kRT*) = √(1.4 × 296.8 × {N(c62["Ts"],1)}) = {N(c62["Vs"],1)} m/s. No printed answer. The other options:', 2, TOP['crit'], CEN('17–62'), 'goc', 'script (no printed answer; method tested on Ex 17-7 and 17-37)'))
    A63 = reg('areaMa', dict(Ma1=2.4, A1=25.0, Ma2=1.2, k=1.4), 'A2', 25.0 * AAs(1.2, 1.4) / AAs(2.4, 1.4), 1e-9, '17-63')
    add(numq('Cengel Bài 17–63 (§17-3): khí lý tưởng k = 1,4 chảy đẳng entropi trong vòi phun; tại Ma = 2,4 diện tích dòng chảy là 25 cm². Diện tích tại vị trí Ma = 1,2 (cùng nhánh siêu âm) là:',
             'Cengel Problem 17–63 (§17-3): an ideal gas with k = 1.4 flows isentropically through a nozzle; at Ma = 2.4 the flow area is 25 cm². The flow area where Ma = 1.2 (same supersonic branch) is:',
             A63, [(25.0 * AAs(2.4, 1.4) / AAs(1.2, 1.4), 'đảo tỉ số diện tích', 'inverts the area ratio'), (25.0 * 1.2 / 2.4, 'tỉ lệ A với Ma', 'takes A proportional to Ma'), (25.0 * AAs(0.8, 1.4) / AAs(2.4, 1.4), 'dùng nhánh cận âm Ma = 0,8 cho cùng A/A*', 'uses a subsonic Ma = 0.8 point'), (25.0 * AAs(1.2, 1.4), 'quên chia cho A₁/A* = 2,4031', 'forgets to divide by A₁/A* = 2.4031')],
             'cm²', 2, f'A/A* = 1,0304 tại Ma = 1,2 và 2,4031 tại Ma = 2,4 (A-32): A* = 25/2,4031 = {N(25.0/AAs(2.4,1.4),3)} cm²; A = 1,0304 × {N(25.0/AAs(2.4,1.4),3)} = {N(A63,2)} cm². Không có đáp án in. Các phương án còn lại:',
             f'A/A* = 1.0304 at Ma = 1.2 and 2.4031 at Ma = 2.4 (A-32): A* = 25/2.4031 = {N(25.0/AAs(2.4,1.4),3)} cm²; A = 1.0304 × {N(25.0/AAs(2.4,1.4),3)} = {N(A63,2)} cm². No printed answer. The other options:', 3, TOP['area'], CEN('17–63'), 'goc', 'script + A-32 rows Ma=1.2, 2.4 (no printed answer)'))
    # ---------------------------------------------------------------- 17-128 helium sonic location
    kH, RH = 1.667, 2.0769; cpH = cp_of(kH, RH); T0H = 500.0 + 120.0 ** 2 / (2000.0 * cpH); P0H = 800.0 * (T0H / 500.0) ** (kH / (kH - 1)); Ma1H = 120.0 / csound(kH, RH, 500.0)
    h128 = {nm_: reg('sonic', dict(T=500.0, P=800.0, V=120.0, k=kH, R=RH, cp=cpH), nm_, v_, 1e-9, f'17-128 {nm_}') for nm_, v_ in (('Ps', crit(kH)['PP'] * P0H), ('Ts', crit(kH)['TT'] * T0H), ('AsA1', 1.0 / AAs(Ma1H, kH)))}
    add(numq('Cengel Bài 17–128 (§17-4): heli (k = 1,667; R = 2,0769 kJ/(kg·K)) vào vòi phun ở 0,8 MPa, 500 K và vận tốc 120 m/s, dòng đẳng entropi. Tỉ số diện tích A*/A₁ giữa vị trí vận tốc bằng tốc độ âm và cửa vào là:',
             'Cengel Problem 17–128 (§17-4): helium (k = 1.667; R = 2.0769 kJ/(kg·K)) enters a nozzle at 0.8 MPa, 500 K and a velocity of 120 m/s, isentropic flow. The area ratio A*/A₁ between the location where the velocity equals the speed of sound and the entrance is:',
             h128['AsA1'], [(1.0 / AAs(Ma1H, 1.4), 'dùng công thức A/A* với k = 1,4 (không khí)', 'uses the A/A* formula with k = 1.4 (air)'), (AAs(Ma1H, kH), 'lấy A₁/A* (nghịch đảo)', 'takes A₁/A* (the inverse)'), (Ma1H, 'lấy A*/A₁ = Ma₁', 'takes A*/A₁ = Ma₁')],
             '', 3, f'c₁ = √(1,667 × 2076,9 × 500) = {N(csound(kH,RH,500.0),1)} m/s; Ma₁ = {N(Ma1H,4)}; A₁/A* = (1/Ma₁)[(2/(k+1))(1 + (k−1)Ma₁²/2)]^((k+1)/(2(k−1))) = {N(AAs(Ma1H,kH),3)}; A*/A₁ = {N(h128["AsA1"],4)}. Cũng T* = {N(h128["Ts"],1)} K, P* = {N(h128["Ps"],1)} kPa. Không có đáp án in; phương pháp đã thử trên Bài 17–58 (có đáp án in 0,629). Các phương án còn lại:',
             f'c₁ = √(1.667 × 2076.9 × 500) = {N(csound(kH,RH,500.0),1)} m/s; Ma₁ = {N(Ma1H,4)}; A₁/A* = (1/Ma₁)[(2/(k+1))(1 + (k−1)Ma₁²/2)]^((k+1)/(2(k−1))) = {N(AAs(Ma1H,kH),3)}; A*/A₁ = {N(h128["AsA1"],4)}. Also T* = {N(h128["Ts"],1)} K, P* = {N(h128["Ps"],1)} kPa. No printed answer; the method was tested on Problem 17–58 (printed 0.629). The other options:', 3, TOP['area'], CEN('17–128'), 'goc', 'script (no printed answer; method tested on 17-58)'))
    # ---------------------------------------------------------------- 17-134 diffuser (no printed answer)
    d134 = {nm_: reg('diffuser', dict(T1=242.7, P1=41.1, Ma1=0.8, Ma2=0.3, k=k, R=R, mdot=65.0), nm_, v_, 1e-9, f'17-134 {nm_}') for nm_, v_ in (('dP', 0.0), ('A2', 0.0))}
    T01 = 242.7 * (1 + 0.2 * 0.64); P01 = 41.1 / PP0(0.8, k); T2 = T01 * TT0(0.3, k); P2 = P01 * PP0(0.3, k); V2 = 0.3 * csound(k, R, T2); rho2 = P2 / (R * T2); A2 = 65.0 / (rho2 * V2)
    REG[-2]['value'] = P2 - 41.1; REG[-1]['value'] = A2
    add(ess(B('Cengel Bài 17–134 (§17-3; sách không in đáp án). Máy bay bay với Ma₁ = 0,8 ở độ cao 7000 m, nơi áp suất là 41,1 kPa và nhiệt độ là 242,7 K. Diffuser ở cửa vào động cơ có Ma ở cửa ra Ma₂ = 0,3. Với lưu lượng khối 65 kg/s, xác định độ tăng áp suất tĩnh qua diffuser và diện tích cửa ra.',
               'Cengel Problem 17–134 (§17-3; no printed answer). An aircraft flies with a Mach number Ma₁ = 0.8 at an altitude of 7000 m where the pressure is 41.1 kPa and the temperature is 242.7 K. The diffuser at the engine inlet has an exit Mach number of Ma₂ = 0.3. For a mass flow rate of 65 kg/s, determine the static pressure rise across the diffuser and the exit area.'),
             B(f'''Giả thiết: không khí k = 1,4; R = 0,287 kJ/(kg·K); diffuser đẳng entropi nên T₀, P₀ không đổi.
Bước 1 (tính chất hãm từ Ma₁, công thức (9), (10)): T₀ = 242.7 × (1 + 0.2 × 0.64) = {N(T01,2)} K; P₀ = 41.1 × (1 + 0.2 × 0.64)^3.5 = {N(P01,2)} kPa.
Bước 2 (cửa ra Ma₂ = 0,3): T₂ = T₀/(1 + 0.2 × 0.09) = {N(T2,2)} K; P₂ = P₀ (T₂/T₀)^3.5 = {N(P2,2)} kPa. Độ tăng áp: P₂ − P₁ = {N(P2-41.1,2)} kPa.
Bước 3 (diện tích): V₂ = Ma₂√(kRT₂) = 0.3 × √(1.4 × 287 × {N(T2,2)}) = {N(V2,1)} m/s; ρ₂ = P₂/(RT₂) = {N(rho2,4)} kg/m³; A₂ = ṁ/(ρ₂V₂) = 65/({N(rho2,3)} × {N(V2,1)}) = {N(A2,4)} m².
Đơn vị: kPa/(kPa·m³/(kg·K)·K) = kg/m³; kg/s ÷ (kg/m³ · m/s) = m².
Hai đường: (A) công thức đóng; (B) verify_m05.py tích phân ODE Hugoniot d ln A = (Ma² − 1)dMa/[Ma(1 + 0,2Ma²)] từ Ma = 0,8 tới 0,3 để thu A₂/A₁ rồi so với ṁ/(ρVA) — hai cách cho A₂ trùng 1e-6; (C) A-32 tại Ma = 0,3 và 0,8: P/P₀ = 0,9395 và 0,6560 (các hàng in). Phương pháp đã thử trên Bài 17–126 và 17–5 (có đáp án in).''',
               f'''Assumptions: air k = 1.4; R = 0.287 kJ/(kg·K); an isentropic diffuser, so T₀ and P₀ stay constant.
Step 1 (stagnation properties from Ma₁, equations (9), (10)): T₀ = 242.7 × (1 + 0.2 × 0.64) = {N(T01,2)} K; P₀ = 41.1 × (1 + 0.2 × 0.64)^3.5 = {N(P01,2)} kPa.
Step 2 (exit Ma₂ = 0.3): T₂ = T₀/(1 + 0.2 × 0.09) = {N(T2,2)} K; P₂ = P₀ (T₂/T₀)^3.5 = {N(P2,2)} kPa. Pressure rise: P₂ − P₁ = {N(P2-41.1,2)} kPa.
Step 3 (area): V₂ = Ma₂√(kRT₂) = 0.3 × √(1.4 × 287 × {N(T2,2)}) = {N(V2,1)} m/s; ρ₂ = P₂/(RT₂) = {N(rho2,4)} kg/m³; A₂ = ṁ/(ρ₂V₂) = 65/({N(rho2,3)} × {N(V2,1)}) = {N(A2,4)} m².
Units: kPa/(kPa·m³/(kg·K)·K) = kg/m³; kg/s ÷ (kg/m³ · m/s) = m².
Two routes: (A) closed forms; (B) verify_m05.py integrates the Hugoniot ODE d ln A = (Ma² − 1)dMa/[Ma(1 + 0.2Ma²)] from Ma = 0.8 to 0.3 to get A₂/A₁ and compares it with ṁ/(ρVA) — the two ways give the same A₂ to 1e-6; (C) A-32 at Ma = 0.3 and 0.8: P/P₀ = 0.9395 and 0.6560 (printed rows). The method was tested on Problems 17–126 and 17–5 (printed answers).'''),
             3, TOP['hug'], CEN('17–134'), 'goc', 'script + ODE + A-32 rows Ma=0.3, 0.8 (no printed answer; method tested on 17-5, 17-126)'))
    # ---------------------------------------------------------------- 17-65 converging nozzle vs back pressure
    P0n, T0n, An = 900.0, 400.0, 10e-4
    rows65 = {Pb: conv_nozzle(float(Pb), P0n, T0n, k, R, An) for Pb in (700, 500, 300, 100)}
    for Pb, r_ in rows65.items():
        for key in ('Pe', 'Ma', 'V', 'mdot'): reg('cnoz', dict(Pb=float(Pb), P0=P0n, T0=T0n, k=k, R=R, A=An), key, r_[key], 1e-9, f'17-65 Pb={Pb} {key}')
    add(ess(B('Cengel Bài 17–65 (§17-4; câu hỏi gốc yêu cầu vẽ đồ thị, ta tính 4 điểm). Không khí ở 900 kPa và 400 K vào vòi hội tụ với vận tốc không đáng kể; diện tích cổ họng 10 cm². Giả thiết dòng đẳng entropi, tính áp suất cửa ra, vận tốc cửa ra và lưu lượng khối theo áp suất ngược P_b = 700, 500, 300 và 100 kPa.',
               'Cengel Problem 17–65 (§17-4; the original asks for a plot, we compute four points). Air at 900 kPa and 400 K enters a converging nozzle with negligible velocity; the throat area is 10 cm². Assuming isentropic flow, calculate the exit pressure, the exit velocity and the mass flow rate for back pressures P_b = 700, 500, 300 and 100 kPa.'),
             B(f'''Giả thiết: không khí k = 1,4; R = 0,287; P₀ = 900 kPa, T₀ = 400 K (vận tốc vào ≈ 0). P*/P₀ = 0,5283 → P* = {N(rows65[700]["Pcrit"],1)} kPa: chia hai chế độ.
P_b = 700 kPa (> P*): không nghẹt, P_e = 700 kPa; Ma_e = √{{[(P₀/P_e)^0,2857 − 1]/0,2}} = {N(rows65[700]["Ma"],4)}; T_e = {N(rows65[700]["Te"],1)} K; V_e = {N(rows65[700]["V"],1)} m/s; ṁ = ρ_eA V_e = {N(rows65[700]["rho"],3)} × 10⁻³ × {N(rows65[700]["V"],1)} = {N(rows65[700]["mdot"],3)} kg/s.
P_b = 500 kPa (> P* = {N(rows65[500]["Pcrit"],1)} kPa): không nghẹt, Ma_e = {N(rows65[500]["Ma"],4)}; V_e = {N(rows65[500]["V"],1)} m/s; ṁ = {N(rows65[500]["mdot"],3)} kg/s.
P_b = 300 kPa (< P*): NGHẸT, P_e = P* = {N(rows65[300]["Pe"],1)} kPa (không phải 300), Ma_e = 1, V_e = {N(rows65[300]["V"],1)} m/s, ṁ = ṁ_max = {N(rows65[300]["mdot"],3)} kg/s; P_b = 100 kPa cho cùng giá trị ({N(rows65[100]["mdot"],3)} kg/s).
Đơn vị: m² (10 cm² = 10⁻³ m²); kPa/(kJ/kg·K · K) = kg/m³.
Hai đường: (A) công thức (10), (15), (16); (B) verify_m05.py: ṁ = ρVA từ năng lượng + quan hệ đẳng entropi tại P_e = max(P_b, P_max-flux), với P_max-flux tìm bằng cực đại số của ρV (không dùng (13)); thermo.js (convergingNozzle) qua node. Đồ thị ṁ theo P_b/P₀: hình trong phần 4 của bài giảng.''',
               f'''Assumptions: air k = 1.4; R = 0.287; P₀ = 900 kPa, T₀ = 400 K (inlet velocity ≈ 0). P*/P₀ = 0.5283 → P* = {N(rows65[700]["Pcrit"],1)} kPa: two regimes.
P_b = 700 kPa (> P*): not choked, P_e = 700 kPa; Ma_e = √{{[(P₀/P_e)^0.2857 − 1]/0.2}} = {N(rows65[700]["Ma"],4)}; T_e = {N(rows65[700]["Te"],1)} K; V_e = {N(rows65[700]["V"],1)} m/s; ṁ = ρ_eA V_e = {N(rows65[700]["rho"],3)} × 10⁻³ × {N(rows65[700]["V"],1)} = {N(rows65[700]["mdot"],3)} kg/s.
P_b = 500 kPa (> P* = {N(rows65[500]["Pcrit"],1)} kPa): not choked, Ma_e = {N(rows65[500]["Ma"],4)}; V_e = {N(rows65[500]["V"],1)} m/s; ṁ = {N(rows65[500]["mdot"],3)} kg/s.
P_b = 300 kPa (< P*): CHOKED, P_e = P* = {N(rows65[300]["Pe"],1)} kPa (not 300), Ma_e = 1, V_e = {N(rows65[300]["V"],1)} m/s, ṁ = ṁ_max = {N(rows65[300]["mdot"],3)} kg/s; P_b = 100 kPa gives the same value ({N(rows65[100]["mdot"],3)} kg/s).
Units: m² (10 cm² = 10⁻³ m²); kPa/(kJ/kg·K · K) = kg/m³.
Two routes: (A) equations (10), (15), (16); (B) verify_m05.py: ṁ = ρVA from energy + the isentropic relation at P_e = max(P_b, P_max-flux), where P_max-flux is found as the numerical maximum of ρV (without using (13)); thermo.js (convergingNozzle) through node. Plot of ṁ against P_b/P₀: figure in part 4 of the lesson.'''),
             3, TOP['back'], CEN('17–65'), 'goc', 'script + node thermo.js (no printed answer; method tested on Ex 17-5)'))
    # ---------------------------------------------------------------- Fundamentals of Engineering items (book options)
    r151 = reg('stag', dict(T=278.15, P=100.0, V=400.0, k=k, R=R, cp=cp), 'T0', T0_of(278.15, 400.0, cp), 1e-9, '17-151 T0 (K)') - 273.15
    add(fe('Cengel Bài 17–151 (FE): máy bay bay hành trình trong không khí lặng ở 5 °C với vận tốc 400 m/s. Nhiệt độ không khí tại mũi máy bay, nơi không khí bị hãm, là',
           'Cengel Problem 17–151 (FE): an aircraft is cruising in still air at 5°C at a velocity of 400 m/s. The air temperature at the nose of the aircraft where stagnation occurs is',
           [('5 °C', '5°C'), ('25 °C', '25°C'), ('55 °C', '55°C'), ('80 °C', '80°C'), ('85 °C', '85°C')], 4,
           f'T₀ = T + V²/(2c_p) = 278,15 + 400²/(2 × 1,005 × 1000) = 278,15 + {N(400**2/2010,1)} = {N(r151+273.15,1)} K = {N(r151,1)} °C ≈ 85 °C. 5 °C là nhiệt độ tĩnh (chưa cộng nhiệt độ động 79,6 K). Các phương án còn lại là phương án nhiễu của sách.',
           f'T₀ = T + V²/(2c_p) = 278.15 + 400²/(2 × 1.005 × 1000) = 278.15 + {N(400**2/2010,1)} = {N(r151+273.15,1)} K = {N(r151,1)}°C ≈ 85°C. 5°C is the static temperature (without the 79.6 K dynamic temperature rise). The other options are the book\'s distractors.',
           1, TOP['stag'], CEN('17–151', ' (FE)', ' (FE)'), 'script (FE item: the book prints no answer; five options are the book\'s)'))
    r152 = reg('stag', dict(T=288.15, P=80.0, V=200.0, k=k, R=R, cp=cp), 'P0', P0_of(80.0, 288.15, T0_of(288.15, 200.0, cp), k), 1e-9, '17-152 P0')
    add(fe('Cengel Bài 17–152 (FE): không khí chảy trong hầm gió ở 15 °C, 80 kPa và 200 m/s. Áp suất hãm tại đầu dò đặt trong đoạn thử là',
           'Cengel Problem 17–152 (FE): air is flowing in a wind tunnel at 15°C, 80 kPa and 200 m/s. The stagnation pressure at the probe inserted into the flow section is',
           [('82 kPa', '82 kPa'), ('91 kPa', '91 kPa'), ('96 kPa', '96 kPa'), ('101 kPa', '101 kPa'), ('114 kPa', '114 kPa')], 3,
           f'T₀ = 288,15 + 200²/2010 = {N(T0_of(288.15,200.0,cp),1)} K; P₀ = 80 × ({N(T0_of(288.15,200.0,cp),1)}/288,15)^3,5 = {N(r152,1)} kPa ≈ 101 kPa. 80 kPa là áp suất tĩnh (chưa cộng hiệu ứng động ≈ 21 kPa). Các phương án còn lại là phương án nhiễu của sách.',
           f'T₀ = 288.15 + 200²/2010 = {N(T0_of(288.15,200.0,cp),1)} K; P₀ = 80 × ({N(T0_of(288.15,200.0,cp),1)}/288.15)^3.5 = {N(r152,1)} kPa ≈ 101 kPa. 80 kPa is the static pressure (without the dynamic rise of about 21 kPa). The other options are the book\'s distractors.',
           2, TOP['stag'], CEN('17–152', ' (FE)', ' (FE)'), 'script (FE item; no printed answer)'))
    v153 = reg('sound', dict(k=k, R=R, T=253.15, Ma=0.86), 'V', 0.86 * csound(k, R, 253.15), 1e-9, '17-153 V')
    add(fe('Cengel Bài 17–153 (FE): máy bay được báo cáo bay hành trình trong không khí lặng ở −20 °C và 40 kPa với Ma = 0,86. Vận tốc của máy bay là',
           'Cengel Problem 17–153 (FE): an aircraft is reported to be cruising in still air at −20°C and 40 kPa at a Mach number of 0.86. The velocity of the aircraft is',
           [('91 m/s', '91 m/s'), ('220 m/s', '220 m/s'), ('186 m/s', '186 m/s'), ('280 m/s', '280 m/s'), ('378 m/s', '378 m/s')], 3,
           f'c = √(kRT) = √(1,4 × 287 × 253,15) = {N(csound(k,R,253.15),1)} m/s; V = 0,86 c = {N(v153,1)} m/s: phương án gần nhất là 280 m/s (lệch 2 %; đề FE chọn phương án gần nhất). Các phương án còn lại là phương án nhiễu của sách; áp suất 40 kPa không ảnh hưởng đến c.',
           f'c = √(kRT) = √(1.4 × 287 × 253.15) = {N(csound(k,R,253.15),1)} m/s; V = 0.86 c = {N(v153,1)} m/s: the nearest option is 280 m/s (2 % off; FE items ask for the closest option). The other options are the book\'s distractors; the 40 kPa pressure does not affect c.',
           2, TOP['snd'], CEN('17–153', ' (FE)', ' (FE)'), 'script (FE item; no printed answer; nearest option)'))
    m154 = reg('sound', dict(k=k, R=R, T=285.15, V=230.0), 'Ma', 230.0 / csound(k, R, 285.15), 1e-9, '17-154 Ma')
    add(fe('Cengel Bài 17–154 (FE): không khí chảy trong hầm gió ở 12 °C và 66 kPa với vận tốc 230 m/s. Số Mach của dòng là (các phương án in trong sách mang đơn vị "m/s", đó là lỗi in vì Ma không thứ nguyên)',
           'Cengel Problem 17–154 (FE): air is flowing in a wind tunnel at 12°C and 66 kPa at a velocity of 230 m/s. The Mach number of the flow is (the options are printed in the book with the unit "m/s", a misprint because Ma is dimensionless)',
           [('0,54', '0.54'), ('0,87', '0.87'), ('3,3', '3.3'), ('0,36', '0.36'), ('0,68', '0.68')], 4,
           f'c = √(1,4 × 287 × 285,15) = {N(csound(k,R,285.15),1)} m/s; Ma = 230/{N(csound(k,R,285.15),1)} = {N(m154,3)} ≈ 0,68. Các phương án còn lại là phương án nhiễu của sách; áp suất 66 kPa không ảnh hưởng đến Ma.',
           f'c = √(1.4 × 287 × 285.15) = {N(csound(k,R,285.15),1)} m/s; Ma = 230/{N(csound(k,R,285.15),1)} = {N(m154,3)} ≈ 0.68. The other options are the book\'s distractors; the 66 kPa pressure does not affect Ma.',
           1, TOP['snd'], CEN('17–154', ' (FE)', ' (FE)'), 'script (FE item; no printed answer)'))
    add(fe('Cengel Bài 17–155 (FE): vòi hội tụ có vận tốc vào thấp và vận tốc âm ở mặt cắt cửa ra. Bây giờ đường kính cửa ra giảm một nửa trong khi nhiệt độ và áp suất vào giữ nguyên. Vận tốc cửa ra của vòi phun sẽ',
           'Cengel Problem 17–155 (FE): consider a converging nozzle with a low velocity at the inlet and sonic velocity at the exit plane. Now the nozzle exit diameter is reduced by half while the nozzle inlet temperature and pressure are maintained the same. The nozzle exit velocity will',
           [('giữ nguyên', 'remain the same'), ('tăng gấp đôi', 'double'), ('tăng gấp bốn', 'quadruple'), ('giảm một nửa', 'go down by half'), ('giảm còn một phần tư', 'go down to one-fourth')], 0,
           'Tại mặt cắt cửa ra Ma = 1 nên V = c* = √(kRT*) với T* = 2T₀/(k+1): chỉ phụ thuộc T₀ và loại khí, không phụ thuộc diện tích. Giảm đường kính một nửa làm diện tích giảm 4 lần nên lưu lượng khối ṁ = A*P₀√(k/(RT₀))(…) giảm 4 lần chứ vận tốc không đổi.',
           'At the exit plane Ma = 1 so V = c* = √(kRT*) with T* = 2T₀/(k+1): it depends only on T₀ and the gas, not on the area. Halving the diameter cuts the area by 4 so the mass flow ṁ = A*P₀√(k/(RT₀))(…) falls by 4 while the velocity stays the same.',
           2, TOP['mdot'], CEN('17–155', ' (FE)', ' (FE)'), 'slide p.46 + formula (16) (FE item; no printed answer)'))
    v156 = reg('critst', dict(k=k, P0=300.0, T0=293.15, R=R), 'Vs', csound(k, R, crit(k)['TT'] * 293.15), 1e-9, '17-156 V*')
    add(fe('Cengel Bài 17–156 (FE): không khí tiến vào vòi hội tụ–phân kỳ với vận tốc thấp ở 20 °C và 300 kPa, rời vòi ở vận tốc siêu âm. Vận tốc không khí ở cổ họng của vòi là',
           'Cengel Problem 17–156 (FE): air is approaching a converging–diverging nozzle with a low velocity at 20°C and 300 kPa, and it leaves the nozzle at a supersonic velocity. The velocity of air at the throat of the nozzle is',
           [('290 m/s', '290 m/s'), ('98 m/s', '98 m/s'), ('313 m/s', '313 m/s'), ('343 m/s', '343 m/s'), ('412 m/s', '412 m/s')], 2,
           f'Ra siêu âm nghĩa là cổ họng nghẹt: V = c* = √(kRT*), T* = 0,8333 × 293,15 = {N(crit(k)["TT"]*293.15,1)} K → V = {N(v156,1)} m/s ≈ 313 m/s. 343 m/s là tốc độ âm ở T₀ = 293,15 K ({N(csound(k,R,293.15),0)} m/s); áp suất 300 kPa không ảnh hưởng đến vận tốc. Các phương án còn lại là phương án nhiễu của sách.',
           f'A supersonic exit means a choked throat: V = c* = √(kRT*), T* = 0.8333 × 293.15 = {N(crit(k)["TT"]*293.15,1)} K → V = {N(v156,1)} m/s ≈ 313 m/s. 343 m/s is the speed of sound at T₀ = 293.15 K ({N(csound(k,R,293.15),0)} m/s); the 300 kPa pressure does not affect the velocity. The other options are the book\'s distractors.',
           2, TOP['crit'], CEN('17–156', ' (FE)', ' (FE)'), 'script (FE item; no printed answer)'))
    m157 = reg('choked', dict(A=0.015, P0=120.0, T0=293.15, k=1.667, R=0.2081), 'mdot', mdot_choked(0.015, 120.0, 293.15, 1.667, 0.2081), 1e-9, '17-157 mdot')
    add(fe('Cengel Bài 17–157 (FE): khí argon tiến vào vòi hội tụ–phân kỳ với vận tốc thấp ở 20 °C và 120 kPa, rời vòi ở vận tốc siêu âm. Diện tích cổ họng là 0,015 m² (k = 1,667; R = 0,2081 kJ/(kg·K)). Lưu lượng khối của argon qua vòi là',
           'Cengel Problem 17–157 (FE): argon gas is approaching a converging–diverging nozzle with a low velocity at 20°C and 120 kPa, and it leaves the nozzle at a supersonic velocity. The cross-sectional area of the throat is 0.015 m² (k = 1.667; R = 0.2081 kJ/(kg·K)). The mass flow rate of argon through the nozzle is',
           [('0,41 kg/s', '0.41 kg/s'), ('3,4 kg/s', '3.4 kg/s'), ('5,3 kg/s', '5.3 kg/s'), ('17 kg/s', '17 kg/s'), ('22 kg/s', '22 kg/s')], 2,
           f'Dòng nghẹt: ṁ = A*P₀√(k/(RT₀))(2/(k+1))^((k+1)/(2(k−1))) = 0,015 × 120 000 Pa × √(1,667/(208,1 × 293,15)) × {N((2/2.667)**(2.667/1.334),4)} = {N(m157,3)} kg/s ≈ 5,3 kg/s. Các phương án còn lại là phương án nhiễu của sách (nhớ đổi P₀ sang Pa và R sang J/(kg·K), tức hệ số √1000).',
           f'Choked flow: ṁ = A*P₀√(k/(RT₀))(2/(k+1))^((k+1)/(2(k−1))) = 0.015 × 120,000 Pa × √(1.667/(208.1 × 293.15)) × {N((2/2.667)**(2.667/1.334),4)} = {N(m157,3)} kg/s ≈ 5.3 kg/s. The other options are the book\'s distractors (remember to convert P₀ to Pa and R to J/(kg·K), i.e. the √1000 factor).',
           3, TOP['unit'], CEN('17–157', ' (FE)', ' (FE)'), 'script + node thermo.js (FE item; no printed answer)'))
    kC, RC, cpC = 1.289, 0.1889, 0.846; T0_158 = 583.15 + 60.0 ** 2 / (2000.0 * cpC); v158 = reg('sonic', dict(T=583.15, P=300.0, V=60.0, k=kC, R=RC, cp=cpC), 'Vs', csound(kC, RC, crit(kC)['TT'] * T0_158), 1e-9, '17-158 V*')
    add(fe('Cengel Bài 17–158 (FE): CO₂ vào vòi hội tụ–phân kỳ ở 60 m/s, 310 °C và 300 kPa, rời vòi ở vận tốc siêu âm (k = 1,289; R = 0,1889; c_p = 0,846 kJ/(kg·K)). Vận tốc CO₂ tại cổ họng là',
           'Cengel Problem 17–158 (FE): carbon dioxide enters a converging–diverging nozzle at 60 m/s, 310°C and 300 kPa, and it leaves the nozzle at a supersonic velocity (k = 1.289; R = 0.1889; c_p = 0.846 kJ/(kg·K)). The velocity of carbon dioxide at the throat of the nozzle is',
           [('125 m/s', '125 m/s'), ('225 m/s', '225 m/s'), ('312 m/s', '312 m/s'), ('353 m/s', '353 m/s'), ('377 m/s', '377 m/s')], 3,
           f'Dòng nghẹt nên V = c* = √(kRT*) với T* = 2T₀/(k+1); T₀ = 583,15 + 60²/(2 × 0,846 × 1000) = {N(T0_158,1)} K; T* = {N(crit(kC)["TT"]*T0_158,1)} K; V = {N(v158,1)} m/s ≈ 353 m/s. 377 m/s là tốc độ âm ở T₀ ({N(csound(kC,RC,T0_158),0)} m/s); các phương án còn lại là phương án nhiễu của sách.',
           f'Choked flow so V = c* = √(kRT*) with T* = 2T₀/(k+1); T₀ = 583.15 + 60²/(2 × 0.846 × 1000) = {N(T0_158,1)} K; T* = {N(crit(kC)["TT"]*T0_158,1)} K; V = {N(v158,1)} m/s ≈ 353 m/s. 377 m/s is the speed of sound at T₀ ({N(csound(kC,RC,T0_158),0)} m/s); the other options are the book\'s distractors.',
           3, TOP['crit'], CEN('17–158', ' (FE)', ' (FE)'), 'script (FE item; no printed answer)'))
    P160 = reg('critst', dict(k=1.33, P0=800.0, T0=673.15, R=0.287), 'Ps', crit(1.33)['PP'] * 800.0, 1e-9, '17-160 P*')
    add(fe('Cengel Bài 17–160 (FE): khí cháy có k = 1,33 vào vòi hội tụ ở nhiệt độ hãm 400 °C và áp suất hãm 800 kPa, xả ra khí quyển ở 20 °C và 100 kPa. Áp suất thấp nhất xuất hiện trong vòi là',
           'Cengel Problem 17–160 (FE): combustion gases with k = 1.33 enter a converging nozzle at stagnation temperature and pressure of 400°C and 800 kPa, and are discharged into the atmospheric air at 20°C and 100 kPa. The lowest pressure that will occur within the nozzle is',
           [('26 kPa', '26 kPa'), ('100 kPa', '100 kPa'), ('321 kPa', '321 kPa'), ('432 kPa', '432 kPa'), ('272 kPa', '272 kPa')], 3,
           f'P*/P₀ = (2/2,33)^(1,33/0,33) = {N(crit(1.33)["PP"],4)} → P* = {N(P160,1)} kPa ≈ 432 kPa. Vì P_b = 100 kPa < P* nên dòng nghẹt và áp suất cửa ra (thấp nhất trong vòi hội tụ) là P*, không phải 100 kPa. Các phương án còn lại là phương án nhiễu của sách (với k = 1,4 sẽ được 423 kPa, không có trong các phương án).',
           f'P*/P₀ = (2/2.33)^(1.33/0.33) = {N(crit(1.33)["PP"],4)} → P* = {N(P160,1)} kPa ≈ 432 kPa. Since P_b = 100 kPa < P* the flow is choked and the exit pressure (the lowest in a converging nozzle) is P*, not 100 kPa. The other options are the book\'s distractors (with k = 1.4 one would get 423 kPa, which is not among them).',
           2, TOP['back'], CEN('17–160', ' (FE)', ' (FE)'), 'script + formula (13) (FE item; no printed answer)'))
    return ITEMS
