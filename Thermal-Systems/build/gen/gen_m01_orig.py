"""m01: ORIGINAL questions (origin 'goc': printed Examples and end-of-chapter Problems of El-Sayed / Farokhi) and
CONCEPTUAL questions derived from the Chapter-1 slides (origin 'bo_sung', slide named).  Route A = closed forms; every number is
registered with reg() and recomputed by a different route in build/verify/verify_m01.py."""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from m01_common import *

T_THR = B('Lực đẩy và công thức lực đẩy', 'Thrust and the thrust equation')
T_EFF = B('Hiệu suất đẩy, nhiệt, tổng', 'Propulsive, thermal and overall efficiency')
T_SFC = B('Tiêu hao nhiên liệu riêng và xung riêng', 'Specific fuel consumption and specific impulse')
T_RNG = B('Tầm bay (Breguet)', 'Range (Breguet)')
T_ISA = B('Khí quyển chuẩn ISA', 'International Standard Atmosphere')
T_CLS = B('Phân loại động cơ', 'Engine classification')
T_AER = B('Khí động học và bốn lực', 'Aerodynamics and the four forces')
T_PRI = B('Nguyên lý đẩy', 'Principles of propulsion')
T_JET = B('Động cơ phản lực', 'Jet engines')
T_THM = B('Nhiệt động lực học ôn tập', 'Thermodynamics review')
T_APP = B('Phân loại theo ứng dụng', 'Classification by application')
SRC = lambda vi, en=None: B(vi, en or vi)

def orig():
    I = []
    # =============================================================== ESSAYS (goc) =====================================
    # --- El-Sayed Problem 2.2 / 2.20
    ma, mf, u, ue, pe, pa, Te, QR = 200, 6, 280, 600, 30e3, 26.5e3, 750, 42.6e6
    f = mf / ma; me = ma + mf; Ae = me / (pe / (R_AIR * Te) * ue)
    pt = (pe - pa) * Ae; T = ma * ((1 + f) * ue - u) + pt
    ep = T * u / (T * u + .5 * me * (ue - u) ** 2); eth = (T * u + .5 * me * (ue - u) ** 2) / (mf * QR); eo = T * u / (mf * QR)
    tsfc = mf / T; Mex = ue / math.sqrt(4 / 3 * R_AIR * Te)
    reg('p22', dict(ma=ma, mf=mf, u=u, ue=ue, pe=pe, pa=pa, Te=Te, QR=QR), dict(T=T, ep=ep, eth=eth, eo=eo, tsfc=tsfc, M=Mex, Ae=Ae))
    I.append(ess(
        B(f'Một máy bay bay ở {u} m/s tại độ cao 20 km (áp suất môi trường 26,5 kPa, nhiệt độ 223,16 K). Dòng phụt có vận tốc 600 m/s, áp suất 30 kPa, nhiệt độ 750 K. Hệ đẩy hút 200 kg/s không khí và đốt 6 kg/s nhiên liệu có nhiệt trị 42 600 kJ/kg. Tính: (1) lực đẩy riêng T/ṁa; (2) hiệu suất đẩy, hiệu suất nhiệt, hiệu suất tổng; (3) TSFC; (4) số Mach tại cửa ra (γ = 4/3, R = 287 J/kg·K).',
          f'An aircraft flies at {u} m/s at 20 km altitude (ambient pressure 26.5 kPa, temperature 223.16 K). The jet speed, pressure and temperature are 600 m/s, 30 kPa and 750 K. The propulsion system consumes 200 kg/s of air and burns 6 kg/s of fuel with heating value 42,600 kJ/kg. Calculate: (1) specific thrust T/ṁa; (2) propulsive, thermal and overall efficiency; (3) TSFC; (4) exhaust Mach number (γ = 4/3, R = 287 J/kg·K).'),
        B(f'Giả thiết: khí xả là khí lý tưởng R = 287 J/kg·K (đề cho R); diện tích cửa ra chưa cho nên suy ra từ liên tục: Ae = ṁe/(ρe·ue).\n'
          f'Bước 1. ṁe = 200 + 6 = 206 kg/s; f = 6/200 = 0.03; ρe = Pe/(R·Te) = 30 000/(287×750) = {N(30e3/(R_AIR*Te),4)} kg/m³; Ae = 206/({N(30e3/(R_AIR*Te),4)}×600) = {N(Ae,3)} m².\n'
          f'Bước 2. Lực đẩy = ṁa[(1+f)ue − u] + (Pe − Pa)Ae = 200×(1.03×600 − 280) + (30 000 − 26 500)×{N(Ae,3)} = 67,600 + {N(pt,0)} = {N(T,0)} N. Lực đẩy riêng T/ṁa = {N(T/ma,1)} N·s/kg.\n'
          f'Bước 3. Công đẩy T·u = {N(T*u/1e6,3)} MW; tổn thất vệt khí xả ½·ṁe·(ue − u)² = {N(.5*me*(ue-u)**2/1e6,3)} MW. η_p = {N(ep,4)}. Công cấp cho dòng khí = T·u + tổn thất = {N((T*u+.5*me*(ue-u)**2)/1e6,3)} MW; nhiệt cấp ṁf·QR = {N(mf*QR/1e6,1)} MW; η_th = {N(eth,4)}; η_o = T·u/(ṁf·QR) = {N(eo,4)} (= η_p·η_th = {N(ep*eth,4)}, kiểm).\n'
          f'Bước 4. TSFC = ṁf/T = 6/{N(T,0)} = {N(tsfc*1e6,1)} mg/(N·s) = {N(tsfc*3600,4)} kg/(N·h).\n'
          f'Bước 5. a_e = √(γ R Te) = √(4/3×287×750) = {N(math.sqrt(4/3*R_AIR*Te),1)} m/s; Ma_e = 600/{N(math.sqrt(4/3*R_AIR*Te),1)} = {N(Mex,3)}.\n'
          f'Kiểm hai cách: (a) công thức đóng như trên; (b) cân bằng thể tích kiểm soát giải số (xem verify_m01.py). Nhận xét: Pe > Pa nên có thành phần lực đẩy áp suất {N(pt,0)} N; dùng công thức η_p = 2u/(u+ue) = {N(2*u/(u+ue),3)} sẽ lệch vì nó chỉ đúng khi Pe = Pa và bỏ qua f.',
          f'Assumption: exhaust is an ideal gas with R = 287 J/kg·K (given); the exit area is not given, so it follows from continuity: Ae = ṁe/(ρe·ue).\n'
          f'Step 1. ṁe = 200 + 6 = 206 kg/s; f = 6/200 = 0.03; ρe = Pe/(R·Te) = 30,000/(287×750) = {N(30e3/(R_AIR*Te),4)} kg/m³; Ae = 206/({N(30e3/(R_AIR*Te),4)}×600) = {N(Ae,3)} m².\n'
          f'Step 2. Thrust = ṁa[(1+f)ue − u] + (Pe − Pa)Ae = 200×(1.03×600 − 280) + (30,000 − 26,500)×{N(Ae,3)} = 67,600 + {N(pt,0)} = {N(T,0)} N. Specific thrust T/ṁa = {N(T/ma,1)} N·s/kg.\n'
          f'Step 3. Thrust power T·u = {N(T*u/1e6,3)} MW; wake loss ½·ṁe·(ue − u)² = {N(.5*me*(ue-u)**2/1e6,3)} MW. η_p = {N(ep,4)}. Power imparted to the airflow = {N((T*u+.5*me*(ue-u)**2)/1e6,3)} MW; fuel heat rate ṁf·QR = {N(mf*QR/1e6,1)} MW; η_th = {N(eth,4)}; η_o = T·u/(ṁf·QR) = {N(eo,4)} (= η_p·η_th = {N(ep*eth,4)}, check).\n'
          f'Step 4. TSFC = ṁf/T = 6/{N(T,0)} = {N(tsfc*1e6,1)} mg/(N·s) = {N(tsfc*3600,4)} kg/(N·h).\n'
          f'Step 5. a_e = √(γ R Te) = √(4/3×287×750) = {N(math.sqrt(4/3*R_AIR*Te),1)} m/s; Ma_e = 600/{N(math.sqrt(4/3*R_AIR*Te),1)} = {N(Mex,3)}.\n'
          f'Two routes: (a) closed forms above; (b) control-volume balance solved numerically (see verify_m01.py). Remark: Pe > Pa, so there is a pressure-thrust term of {N(pt,0)} N; the shortcut η_p = 2u/(u+ue) = {N(2*u/(u+ue),3)} is off because it holds only for Pe = Pa and f ≈ 0.'),
        3, T_EFF, SRC('El-Sayed Ch.2 Problem 2.2 (cũng 2.20)', 'El-Sayed Ch.2 Problem 2.2 (also 2.20)'), 'goc', 'script (verify_m01: p22)'))

    # --- El-Sayed Problem 2.5 first part (three formulas)
    u, ue, st = 240, 560, 525
    e1 = 2*st*u/(2*st*u + (ue-u)**2); e2 = 2*st*u/(ue**2-u**2); e3 = 2*u/(u+ue)
    reg('p25a', dict(u=u, ue=ue, st=st), dict(e1=e1, e2=e2, e3=e3))
    I.append(ess(
        B('Một động cơ turbojet đẩy máy bay bay ở 240 m/s, vận tốc phụt 560 m/s, lực đẩy riêng 525 N·s/kg. Dùng ba công thức hiệu suất đẩy, tính η_p và nhận xét (bỏ qua f).',
          'A turbojet powers an aircraft flying at 240 m/s with exhaust speed 560 m/s and specific thrust 525 N·s/kg. Using the three formulae, calculate the propulsive efficiency and comment (ignore the fuel-to-air ratio).'),
        B(f'Công thức 1 (công đẩy / (công đẩy + tổn thất vệt)): η_p = 2(T/ṁ)u / [2(T/ṁ)u + (ue − u)²] = 2×525×240/(2×525×240 + 320²) = 252,000/354,400 = {N(e1,4)}.\n'
          f'Công thức 2 (động năng cấp thêm): η_p = 2(T/ṁ)u/(ue² − u²) = 252,000/{N(ue**2-u**2,0)} = {N(e2,4)}.\n'
          f'Công thức 3: η_p = 2u/(u + ue) = 480/800 = {N(e3,4)}.\n'
          f'Nhận xét: nếu Pe = Pa thì T/ṁ = ue − u = 320 N·s/kg, nhưng đề cho 525, nghĩa là có thêm {N(st-(ue-u),0)} N·s/kg lực đẩy áp suất (vòi phun nghẹt, Pe > Pa). Khi đó công thức 3 chỉ là ước lượng thô, công thức 2 cho giá trị gần 1 vô lý và không được dùng; công thức 1 là cách đúng (và nó trùng công thức 2 nếu dùng vận tốc phụt hiệu dụng).\nKiểm: công thức 1 tính lại bằng định nghĩa công đẩy/(công đẩy + ½ṁ(ue−u)²) với ṁ = 1 kg/s cho cùng kết quả.',
          f'Formula 1 (thrust power / (thrust power + wake loss)): η_p = 2(T/ṁ)u / [2(T/ṁ)u + (ue − u)²] = 2×525×240/(2×525×240 + 320²) = 252,000/354,400 = {N(e1,4)}.\n'
          f'Formula 2 (kinetic energy added): η_p = 2(T/ṁ)u/(ue² − u²) = 252,000/{N(ue**2-u**2,0)} = {N(e2,4)}.\n'
          f'Formula 3: η_p = 2u/(u + ue) = 480/800 = {N(e3,4)}.\n'
          f'Comment: if Pe = Pa then T/ṁ = ue − u = 320 N·s/kg, but 525 is given, so there is an extra {N(st-(ue-u),0)} N·s/kg of pressure thrust (choked nozzle, Pe > Pa). Then formula 3 is only a rough estimate, formula 2 gives an unphysical value near 1 and must not be used; formula 1 is the right one (and equals formula 2 if the effective jet velocity is used).\nCheck: formula 1 recomputed from the definition thrust power/(thrust power + ½ṁ(ue−u)²) with ṁ = 1 kg/s gives the same value.'),
        2, T_EFF, SRC('El-Sayed Ch.2 Problem 2.5 (phần đầu)', 'El-Sayed Ch.2 Problem 2.5 (first part)'), 'goc', 'script (verify_m01: p25a)'))

    # --- El-Sayed Problem 2.5 second part (two flight speeds)
    f, ue, ma, eo, eomax, LD, m1m2 = .02, 770, 100, .16, .18, 10, 1.2
    lam = eomax / eo; us = [(1+f)*ue/2*(1+s*math.sqrt((lam-1)/lam)) for s in (1, -1)]
    QRx = us[0]*((1+f)*ue-us[0])/(f*eo)
    S = breguet(eo, QRx, LD, m1m2); ts = [S/x for x in us]; m1s = [6*f*ma*t for t in ts]; Ts = [ma*((1+f)*ue-x) for x in us]
    reg('p25b', dict(f=f, ue=ue, ma=ma, eo=eo, eomax=eomax, LD=LD, m1m2=m1m2), dict(u1=us[0], u2=us[1], QR=QRx, S=S, t1=ts[0], t2=ts[1], m1a=m1s[0], m1b=m1s[1], T1=Ts[0], T2=Ts[1]))
    I.append(ess(
        B('Một máy bay một động cơ turbojet có: ṁa = 100 kg/s, ue = 770 m/s, η_o = 0.16, η_o,max = 0.18, f = 0.02, L/D = 10, m1/m2 = 1.2. Với λ = η_o,max/η_o thì u = (1+f)ue/2·[1 ± √((λ−1)/λ)]. Tính: (1) các vận tốc bay có thể; (2) nhiệt trị QR; (3) tầm bay; (4) thời gian bay; (5) khối lượng m1, m2; (6) lực đẩy tương ứng. (Giả thiết lưu lượng nhiên liệu không đổi ṁf = f·ṁa trong chặng bay.)',
          'A single-turbojet aircraft has ṁa = 100 kg/s, ue = 770 m/s, η_o = 0.16, η_o,max = 0.18, f = 0.02, L/D = 10, m1/m2 = 1.2. With λ = η_o,max/η_o the flight speed is u = (1+f)ue/2·[1 ± √((λ−1)/λ)]. Calculate: (1) possible flight speeds; (2) heating value QR; (3) range; (4) trip time; (5) masses m1 and m2; (6) the thrust. (Assume constant fuel flow ṁf = f·ṁa during the leg.)'),
        B(f'(1) λ = 0.18/0.16 = {N(lam,3)}; √((λ−1)/λ) = √(0.125/1.125) = 1/3. u = 1.02×770/2×(1 ± 1/3) = {N(us[0],1)} m/s hoặc {N(us[1],1)} m/s.\n'
          f'(2) η_o = T·u/(ṁf·QR) = u[(1+f)ue − u]/(f·QR) ⇒ QR = {N(us[0],1)}×{N((1+f)*ue-us[0],1)}/(0.02×0.16) = {N(QRx/1e6,2)} MJ/kg (hai vận tốc cho cùng QR vì tích u[(1+f)ue − u] đối xứng). Kiểm: η_o,max = (1+f)²ue²/(4f·QR) = {N((1+f)**2*ue**2/(4*f*QRx),4)} ✓.\n'
          f'(3) S = η_o·QR/g·(L/D)·ln(m1/m2) = 0.16×{N(QRx/1e6,2)}e6/9.80665×10×ln1.2 = {N(S/1e3,1)} km (như nhau cho cả hai vận tốc, vì tầm chỉ phụ thuộc η_o).\n'
          f'(4) t = S/u = {N(ts[0]/3600,3)} h (u lớn) hoặc {N(ts[1]/3600,3)} h (u nhỏ).\n'
          f'(5) Nhiên liệu đốt = ṁf·t = 2×t; m1 − m2 = m1(1 − 1/1.2) = m1/6 ⇒ m1 = 6·ṁf·t = {N(m1s[0],0)} kg, m2 = {N(m1s[0]/1.2,0)} kg (u lớn); m1 = {N(m1s[1],0)} kg, m2 = {N(m1s[1]/1.2,0)} kg (u nhỏ).\n'
          f'(6) T = ṁa[(1+f)ue − u] = {N(Ts[0],0)} N (u lớn) hoặc {N(Ts[1],0)} N (u nhỏ).\n'
          f'Kiểm hai cách: tầm bay cũng tính từ S = (u/g)(T/ṁf)(L/D)ln(m1/m2) cho cùng {N(S/1e3,1)} km.',
          f'(1) λ = 0.18/0.16 = {N(lam,3)}; √((λ−1)/λ) = √(0.125/1.125) = 1/3. u = 1.02×770/2×(1 ± 1/3) = {N(us[0],1)} m/s or {N(us[1],1)} m/s.\n'
          f'(2) η_o = T·u/(ṁf·QR) = u[(1+f)ue − u]/(f·QR) ⇒ QR = {N(us[0],1)}×{N((1+f)*ue-us[0],1)}/(0.02×0.16) = {N(QRx/1e6,2)} MJ/kg (both speeds give the same QR because the product u[(1+f)ue − u] is symmetric). Check: η_o,max = (1+f)²ue²/(4f·QR) = {N((1+f)**2*ue**2/(4*f*QRx),4)} ✓.\n'
          f'(3) S = η_o·QR/g·(L/D)·ln(m1/m2) = 0.16×{N(QRx/1e6,2)}e6/9.80665×10×ln1.2 = {N(S/1e3,1)} km (the same for both speeds, because range depends on η_o only).\n'
          f'(4) t = S/u = {N(ts[0]/3600,3)} h (high u) or {N(ts[1]/3600,3)} h (low u).\n'
          f'(5) Fuel burned = ṁf·t = 2×t; m1 − m2 = m1(1 − 1/1.2) = m1/6 ⇒ m1 = 6·ṁf·t = {N(m1s[0],0)} kg, m2 = {N(m1s[0]/1.2,0)} kg (high u); m1 = {N(m1s[1],0)} kg, m2 = {N(m1s[1]/1.2,0)} kg (low u).\n'
          f'(6) T = ṁa[(1+f)ue − u] = {N(Ts[0],0)} N (high u) or {N(Ts[1],0)} N (low u).\n'
          f'Two routes: range also from S = (u/g)(T/ṁf)(L/D)ln(m1/m2), giving the same {N(S/1e3,1)} km.'),
        3, T_RNG, SRC('El-Sayed Ch.2 Problem 2.5 (phần sau)', 'El-Sayed Ch.2 Problem 2.5 (second part)'), 'goc', 'script (verify_m01: p25b)'))

    # --- El-Sayed Problem 2.12 JT9D static
    mc, mh, uh, uc, mfh = 1248, 247, 1190, 885, 15570
    Tj = (mc*uc + mh*uh)/32.174; ke = .5*(mh*uh**2 + mc*uc**2)/32.174; qf = mfh/3600*18400*778.169
    eth_j = ke/qf; tsfc_j = mfh/Tj; Tsi = Tj*4.44822
    reg('p212', dict(mc=mc, mh=mh, uh=uh, uc=uc, mfh=mfh), dict(T=Tj, eth=eth_j, tsfc=tsfc_j))
    I.append(ess(
        B('Động cơ turbofan lưu lượng rẽ nhánh cao JT9D ở công suất tĩnh tối đa (V0 = 0) trên mực nước biển chuẩn có: lưu lượng khí qua lõi 247 lbm/s, qua ống rẽ nhánh 1248 lbm/s, vận tốc ra khỏi lõi 1190 ft/s, ra khỏi ống rẽ nhánh 885 ft/s, lưu lượng nhiên liệu 15 570 lbm/h. Với áp suất ra bằng áp suất môi trường, ước lượng: (1) lực đẩy; (2) hiệu suất nhiệt (nhiệt trị 18 400 Btu/lbm); (3) hiệu suất đẩy và TSFC.',
          'The JT9D high-BPR turbofan at maximum static power (V0 = 0) on a standard sea-level day has core air flow 247 lbm/s, bypass flow 1248 lbm/s, core exit velocity 1190 ft/s, bypass exit velocity 885 ft/s and fuel flow 15,570 lbm/h. With exhaust pressure equal to ambient, estimate: (1) the thrust; (2) the thermal efficiency (heating value 18,400 Btu/lbm); (3) the propulsive efficiency and TSFC.'),
        B(f'Giả thiết: bỏ qua khối lượng nhiên liệu trong dòng lõi (4.3 lbm/s so với 247 lbm/s, sai lệch 0.4 %); 1 lbf = 32.174 lbm·ft/s²; 1 Btu = 778.169 ft·lbf.\n'
          f'(1) T = (ṁc·uc + ṁh·uh)/gc = (1248×885 + 247×1190)/32.174 = {N(Tj,0)} lbf = {N(Tsi/1e3,1)} kN. (Farokhi Problem 3.4 cho lực đẩy cất cánh 43 500 lbf: khớp trong 0.1 %.)\n'
          f'(2) Công suất động năng = ½(ṁh·uh² + ṁc·uc²)/gc = {N(ke/1e6,2)}×10⁶ ft·lbf/s; nhiệt cấp = (15 570/3600)×18 400×778.169 = {N(qf/1e6,2)}×10⁶ ft·lbf/s ⇒ η_th = {N(eth_j,3)}.\n'
          f'(3) V0 = 0 nên công đẩy F·V0 = 0 ⇒ η_p = 0 và η_o = 0 (động cơ đứng yên không thực hiện công đẩy). TSFC = 15 570/{N(Tj,0)} = {N(tsfc_j,3)} lbm/(h·lbf) = {N(tsfc_j*0.453592/4.44822*1e3/3.6*1,2)} mg/(N·s)... (đổi: 1 lbm/(h·lbf) = 28.33 mg/(N·s)) = {N(tsfc_j*28.325,1)} mg/(N·s).\n'
          f'Kiểm hai cách: đổi toàn bộ sang SI (kg, m/s, N) cho T = {N(Tsi,0)} N, η_th = {N(eth_j,3)}.',
          f'Assumptions: fuel mass in the core stream neglected (4.3 lbm/s against 247 lbm/s, 0.4 % effect); 1 lbf = 32.174 lbm·ft/s²; 1 Btu = 778.169 ft·lbf.\n'
          f'(1) T = (ṁc·uc + ṁh·uh)/gc = (1248×885 + 247×1190)/32.174 = {N(Tj,0)} lbf = {N(Tsi/1e3,1)} kN. (Farokhi Problem 3.4 gives a takeoff thrust of 43,500 lbf: agreement within 0.1 %.)\n'
          f'(2) Kinetic power = ½(ṁh·uh² + ṁc·uc²)/gc = {N(ke/1e6,2)}×10⁶ ft·lbf/s; fuel heat rate = (15,570/3600)×18,400×778.169 = {N(qf/1e6,2)}×10⁶ ft·lbf/s ⇒ η_th = {N(eth_j,3)}.\n'
          f'(3) V0 = 0 so thrust power F·V0 = 0 ⇒ η_p = 0 and η_o = 0 (a stationary engine does no propulsive work). TSFC = 15,570/{N(Tj,0)} = {N(tsfc_j,3)} lbm/(h·lbf) (1 lbm/(h·lbf) = 28.33 mg/(N·s)) = {N(tsfc_j*28.325,1)} mg/(N·s).\n'
          f'Two routes: everything converted to SI (kg, m/s, N) gives T = {N(Tsi,0)} N and η_th = {N(eth_j,3)}.'),
        2, T_SFC, SRC('El-Sayed Ch.2 Problem 2.12', 'El-Sayed Ch.2 Problem 2.12'), 'goc', 'script (verify_m01: p212)'))

    # --- El-Sayed Problem 2.13 (1-4)
    ue = 2300/3.6; f = .0175; em = .15
    u13 = (1+f)*ue/2; QR13 = (1+f)**2*ue**2/(4*f*em); S13 = breguet(em, QR13, 10, 1.2); t13 = S13/u13
    reg('p213', dict(ue=ue, f=f, em=em), dict(u=u13, QR=QR13, S=S13, t=t13))
    I.append(ess(
        B('Máy bay có hai động cơ turbojet: vận tốc phụt 2300 km/h, hiệu suất tổng cực đại 0.15, f = 0.0175, L/D = 10, m1/m2 = 1.2. Tầm cực đại S = η_o,max·QR/g·(L/D)·ln(m1/m2), tại vận tốc u = (1+f)ue/2 và η_o,max = (1+f)²ue²/(4f·QR). Tính: (1) vận tốc bay; (2) nhiệt trị QR; (3) tầm bay cực đại; (4) thời gian bay.',
          'An aircraft has two turbojets: exhaust speed 2300 km/h, maximum overall efficiency 0.15, f = 0.0175, L/D = 10, m1/m2 = 1.2. The maximum range is S = η_o,max·QR/g·(L/D)·ln(m1/m2) at flight speed u = (1+f)ue/2, with η_o,max = (1+f)²ue²/(4f·QR). Calculate: (1) flight speed; (2) heating value QR; (3) maximum range; (4) trip time.'),
        B(f'ue = 2300/3.6 = {N(ue,2)} m/s.\n(1) u = (1+f)ue/2 = 1.0175×{N(ue,2)}/2 = {N(u13,1)} m/s = {N(u13*3.6,0)} km/h.\n(2) QR = (1+f)²ue²/(4f·η_o,max) = {N((1+f)**2*ue**2,0)}/(4×0.0175×0.15) = {N(QR13/1e6,2)} MJ/kg.\n(3) S = 0.15×{N(QR13/1e6,2)}e6/9.80665×10×ln1.2 = {N(S13/1e3,1)} km.\n(4) t = S/u = {N(t13,0)} s = {N(t13/3600,3)} h.\nĐề còn hỏi m1, m2 nhưng không cho lưu lượng không khí nên bỏ (xem ghi chú nguồn). Kiểm: tầm = u·t; hiệu suất tổng tại u đó tính lại = η_o = u[(1+f)ue − u]/(f·QR) = {N(u13*((1+f)*ue-u13)/(f*QR13),4)}.',
          f'ue = 2300/3.6 = {N(ue,2)} m/s.\n(1) u = (1+f)ue/2 = 1.0175×{N(ue,2)}/2 = {N(u13,1)} m/s = {N(u13*3.6,0)} km/h.\n(2) QR = (1+f)²ue²/(4f·η_o,max) = {N((1+f)**2*ue**2,0)}/(4×0.0175×0.15) = {N(QR13/1e6,2)} MJ/kg.\n(3) S = 0.15×{N(QR13/1e6,2)}e6/9.80665×10×ln1.2 = {N(S13/1e3,1)} km.\n(4) t = S/u = {N(t13,0)} s = {N(t13/3600,3)} h.\nThe problem also asks for m1 and m2, but no air flow rate is given, so this part is dropped (see source notes). Check: range = u·t; the overall efficiency recomputed at that u is η_o = u[(1+f)ue − u]/(f·QR) = {N(u13*((1+f)*ue-u13)/(f*QR13),4)}.'),
        2, T_RNG, SRC('El-Sayed Ch.2 Problem 2.13 (câu 1–4)', 'El-Sayed Ch.2 Problem 2.13 (parts 1–4)'), 'goc', 'script (verify_m01: p213)'))

    # --- Problem 2.19 ESFC
    esp = 3300 + 700*250*1.466667/550/.9; esfc = 1500/esp
    reg('p219', {}, dict(esp=esp, esfc=esfc))
    I.append(ess(
        B('ESFC của một động cơ turboprop tiêu thụ 1500 lb nhiên liệu mỗi giờ, sinh 700 lb lực đẩy khí xả và 3300 mã lực trục khi bay 250 mph? Hiệu suất cánh quạt 0.9.',
          'What is the ESFC of a turboprop engine that consumes 1500 lb of fuel per hour and produces 700 lb of exhaust thrust and 3300 shaft horsepower during flight at 250 mph? The propeller efficiency is 0.9.'),
        B(f'ESP = SP + Te·u/η_pr (El-Sayed Eq. 2.19b). 250 mph = 366.67 ft/s; Te·u = 700×366.67 = {N(700*366.667,0)} ft·lbf/s = {N(700*366.667/550,1)} hp (1 hp = 550 ft·lbf/s).\nESP = 3300 + {N(700*366.667/550,1)}/0.9 = {N(esp,1)} hp.\nESFC = 1500/{N(esp,1)} = {N(esfc,4)} lb/(h·hp) = {N(esfc*0.4535924/0.7456999,4)} kg/(kW·h).\nNhận xét: nằm dưới khoảng điển hình 0.45–0.60 lb/(h·hp) mà sách nêu (tr.104); số liệu đề là ước lượng. Kiểm: đổi sang SI: T_e·u = 3.114 kW×... cho cùng ESP = {N(esp*0.7456999,0)} kW.',
          f'ESP = SP + Te·u/η_pr (El-Sayed Eq. 2.19b). 250 mph = 366.67 ft/s; Te·u = 700×366.67 = {N(700*366.667,0)} ft·lbf/s = {N(700*366.667/550,1)} hp (1 hp = 550 ft·lbf/s).\nESP = 3300 + {N(700*366.667/550,1)}/0.9 = {N(esp,1)} hp.\nESFC = 1500/{N(esp,1)} = {N(esfc,4)} lb/(h·hp) = {N(esfc*0.4535924/0.7456999,4)} kg/(kW·h).\nRemark: this is below the typical 0.45–0.60 lb/(h·hp) quoted in the book (p.104); the problem data are an estimate. Check: in SI the same ESP is {N(esp*0.7456999,0)} kW.'),
        2, T_SFC, SRC('El-Sayed Ch.2 Problem 2.19', 'El-Sayed Ch.2 Problem 2.19'), 'goc', 'script (verify_m01: p219)'))

    # --- Problem 2.29 kinematics
    a29 = 20e3/174e3; v29 = 241.40 + a29*120; d29 = 241.40*120 + .5*a29*120**2
    reg('p229', {}, dict(a=a29, v=v29, d=d29))
    I.append(ess(
        B('Máy bay (m = 174 000 kg) đang bay ở 241.40 m/s. Bộ đốt sau được bật trong 2.00 phút, cho lực đẩy trung bình 20 kN. (1) Vận tốc sau 2.00 phút? (2) Quãng đường bay trong 2.00 phút đó? (Coi khối lượng không đổi.)',
          'An airplane (m = 174,000 kg) is cruising at 241.40 m/s. The afterburners are ignited for 2.00 min providing an average thrust of 20 kN. (1) What is the velocity after those 2.00 min? (2) How far did the airplane travel? (Assume constant mass.)'),
        B(f'Giả thiết (đề không nói): 20 kN là lực dư thực sự làm tăng tốc (đã trừ lực cản), gia tốc không đổi.\na = F/m = 20 000/174 000 = {N(a29,5)} m/s².\n(1) v = v0 + a·t = 241.40 + {N(a29,5)}×120 = {N(v29,2)} m/s.\n(2) s = v0·t + ½a·t² = 241.40×120 + 0.5×{N(a29,5)}×120² = {N(241.4*120,1)} + {N(.5*a29*120**2,1)} = {N(d29,0)} m = {N(d29/1e3,2)} km.\nKiểm: s = vtb·t = (241.40 + {N(v29,2)})/2×120 = {N((241.4+v29)/2*120,0)} m.',
          f'Assumption (not stated): the 20 kN is the net accelerating force (drag already subtracted), acceleration constant.\na = F/m = 20,000/174,000 = {N(a29,5)} m/s².\n(1) v = v0 + a·t = 241.40 + {N(a29,5)}×120 = {N(v29,2)} m/s.\n(2) s = v0·t + ½a·t² = 241.40×120 + 0.5×{N(a29,5)}×120² = {N(241.4*120,1)} + {N(.5*a29*120**2,1)} = {N(d29,0)} m = {N(d29/1e3,2)} km.\nCheck: s = mean speed × t = (241.40 + {N(v29,2)})/2×120 = {N((241.4+v29)/2*120,0)} m.'),
        1, T_THR, SRC('El-Sayed Ch.2 Problem 2.29', 'El-Sayed Ch.2 Problem 2.29'), 'goc', 'script (verify_m01: p229)'))

    # --- Farokhi 1.1-1.3
    c1 = 1-288/2000; c2 = 1-288/864; r = 2000/864; hum = 1-GAM*(288/864)*(r**(1/GAM)-1)/(r-1)
    reg('f1x', {}, dict(carnot=c1, brayton=c2, humphrey=hum))
    I.append(ess(
        B('Farokhi Problem 1.1–1.3. (1) Chu trình Carnot giữa T1 = 288 K và T2 = 2000 K có hiệu suất nhiệt bao nhiêu? (2) Chu trình Brayton lý tưởng có T1 = 288 K, T2 = 864 K (nhiệt độ cuối nén)? (3) Chu trình Humphrey (cháy đẳng tích) có cùng T1 = 288 K, T2 = 864 K và T3 = Tmax = 2000 K, γ = 1.4, cho η_th = 1 − γ(T1/T2)[(T3/T2)^(1/γ) − 1]/[(T3/T2) − 1]; so sánh với Brayton.',
          'Farokhi Problems 1.1–1.3. (1) What is the thermal efficiency of a Carnot cycle between T1 = 288 K and T2 = 2000 K? (2) Of an ideal Brayton cycle with T1 = 288 K and T2 = 864 K (end of compression)? (3) Of a Humphrey (constant-volume combustion) cycle with the same T1 = 288 K, T2 = 864 K and T3 = Tmax = 2000 K, γ = 1.4, given η_th = 1 − γ(T1/T2)[(T3/T2)^(1/γ) − 1]/[(T3/T2) − 1]; compare with Brayton.'),
        B(f'(1) η_Carnot = 1 − T1/T2 = 1 − 288/2000 = {N(c1,3)}.\n(2) Brayton: η = 1 − T1/T2 = 1 − 288/864 = {N(c2,4)} (tương đương tỉ số nén áp r_p^((γ−1)/γ) = 3; T3 không ảnh hưởng).\n(3) T3/T2 = 2000/864 = {N(r,4)}; (T3/T2)^(1/1.4) = {N(r**(1/GAM),4)}; η = 1 − 1.4×(288/864)×({N(r**(1/GAM),4)} − 1)/({N(r,4)} − 1) = {N(hum,4)}.\nSo sánh: Humphrey {N(hum*100,2)} % > Brayton {N(c2*100,2)} % (cháy đẳng tích thêm nhiệt ở thể tích nhỏ nên hiệu suất cao hơn), nhưng đều thấp hơn Carnot {N(c1*100,1)} % ở cùng giới hạn nhiệt độ.\nKiểm hai cách: Humphrey tính lại bằng q_in = cv(T3 − T2′), q_out = cp(T4 − T1) với T4 từ đoạn giãn đoạn nhiệt (xem verify).',
          f'(1) η_Carnot = 1 − T1/T2 = 1 − 288/2000 = {N(c1,3)}.\n(2) Brayton: η = 1 − T1/T2 = 1 − 288/864 = {N(c2,4)} (equivalent to pressure ratio r_p^((γ−1)/γ) = 3; T3 has no effect).\n(3) T3/T2 = 2000/864 = {N(r,4)}; (T3/T2)^(1/1.4) = {N(r**(1/GAM),4)}; η = 1 − 1.4×(288/864)×({N(r**(1/GAM),4)} − 1)/({N(r,4)} − 1) = {N(hum,4)}.\nComparison: Humphrey {N(hum*100,2)} % > Brayton {N(c2*100,2)} % (constant-volume heat addition at smaller volume gives higher efficiency) but both are below Carnot {N(c1*100,1)} % at the same temperature limits.\nTwo routes: Humphrey recomputed from q_in = cv(T3 − T2′), q_out = cp(T4 − T1) with T4 from the isentropic expansion (see verify).'),
        2, T_THM, SRC('Farokhi Ch.1 Problems 1.1–1.3', 'Farokhi Ch.1 Problems 1.1–1.3'), 'goc', 'script (verify_m01: f1x)'))

    # --- Farokhi 1.5 afterburner fuel
    ab = 1.75*21000*.5; nab = .81*13500*.5
    reg('f15', {}, dict(ab=ab, nab=nab))
    I.append(ess(
        B('Farokhi Problem 1.5. Động cơ EJ200: SFC (công suất tối đa) 0.81 lbm/h/lbf, lực đẩy mực nước biển 13 500 lbf; SFC có bộ đốt sau 1.75 lbm/h/lbf, lực đẩy khi bật bộ đốt sau 20 250–22 250 lbf. Tính lượng nhiên liệu đốt thêm trong 30 phút dùng bộ đốt sau (lực đẩy 21 000 lbf) so với 30 phút không dùng (13 500 lbf).',
          'Farokhi Problem 1.5. EJ200: SFC (max power) 0.81 lbm/h/lbf, sea-level thrust 13,500 lbf; SFC with afterburner 1.75 lbm/h/lbf, thrust with afterburner 20,250–22,250 lbf. Calculate the additional fuel burned in 30 min of afterburner use (21,000 lbf thrust) compared with 30 min without (13,500 lbf).'),
        B(f'Nhiên liệu = SFC × lực đẩy × thời gian.\nCó bộ đốt sau: 1.75 × 21 000 × 0.5 = {N(ab,1)} lbm.\nKhông: 0.81 × 13 500 × 0.5 = {N(nab,1)} lbm.\nĐốt thêm = {N(ab-nab,1)} lbm ≈ {N((ab-nab)*0.45359237,0)} kg.\nNhận xét: lực đẩy tăng 21 000/13 500 − 1 = {N(21000/13500*100-100,0)} % nhưng mức tiêu hao nhiên liệu tăng {N(ab/nab*100-100,0)} %, vì thế bộ đốt sau chỉ dùng ngắn.\nKiểm: đổi sang SI qua 1 lbm/h/lbf = 28.33 mg/(N·s) cho cùng kết quả.',
          f'Fuel = SFC × thrust × time.\nWith afterburner: 1.75 × 21,000 × 0.5 = {N(ab,1)} lbm.\nWithout: 0.81 × 13,500 × 0.5 = {N(nab,1)} lbm.\nExtra = {N(ab-nab,1)} lbm ≈ {N((ab-nab)*0.45359237,0)} kg.\nRemark: thrust rises by {N(21000/13500*100-100,0)} % but fuel flow by {N(ab/nab*100-100,0)} %, hence afterburners are used only briefly.\nCheck: conversion to SI through 1 lbm/h/lbf = 28.33 mg/(N·s) gives the same result.'),
        1, T_SFC, SRC('Farokhi Ch.1 Problem 1.5', 'Farokhi Ch.1 Problem 1.5'), 'goc', 'script (verify_m01: f15)'))

    # --- Farokhi 3.5 turbojet at Mach 2
    m_, f_, V9, QRf = 25, .03, 1050, 42.8e6; V0 = 2*math.sqrt(GAM*R_AIR*223.15)
    Dr = m_*V0; Fg = m_*(1+f_)*V9; Fn = Fg-Dr; mff = m_*f_; dke = .5*(m_*(1+f_)*V9**2 - m_*V0**2)
    ts = mff/Fn*3600; e_th = dke/(mff*QRf); e_p = Fn*V0/dke; e_o = Fn*V0/(mff*QRf)
    reg('f35', {}, dict(V0=V0, Dr=Dr, Fg=Fg, Fn=Fn, tsfc_h=ts, eth=e_th, ep=e_p, eo=e_o))
    I.append(ess(
        B('Farokhi Problem 3.5. Một động cơ hút khí bay ở Ma 2.0, nhiệt độ môi trường −50 °C, áp suất 10 kPa. Lưu lượng khí 25 kg/s, lưu lượng nhiên liệu bằng 3 % lưu lượng khí, nhiệt trị 42 800 kJ/kg. Vận tốc phụt 1050 m/s, vòi phun giãn nở hoàn toàn (p9 = p0). Tính: (a) lực cản ram (kN); (b) lực đẩy tổng (gross) (kN); (c) lực đẩy thực (kN); (d) TSFC (kg/h/N); (e) η_th; (f) η_p; (g) η_o.',
          'Farokhi Problem 3.5. An airbreathing engine flies at Mach 2.0 where T0 = −50 °C and p0 = 10 kPa. Air flow 25 kg/s, fuel flow 3 % of the air flow, heating value 42,800 kJ/kg. Exhaust speed 1050 m/s, perfectly expanded (p9 = p0). Calculate: (a) ram drag (kN); (b) gross thrust (kN); (c) net thrust (kN); (d) TSFC (kg/h/N); (e) η_th; (f) η_p; (g) η_o.'),
        B(f'Giả thiết γ = 1.4, R = 287 J/kg·K, T0 = 223.15 K.\nV0 = Ma·√(γRT0) = 2×{N(V0/2,2)} = {N(V0,1)} m/s.\n(a) Lực cản ram = ṁ0·V0 = 25×{N(V0,1)} = {N(Dr/1e3,3)} kN.\n(b) Gross = (ṁ0 + ṁf)·V9 = 25.75×1050 = {N(Fg/1e3,3)} kN (p9 = p0 nên không có lực đẩy áp suất).\n(c) Net = {N(Fg/1e3,3)} − {N(Dr/1e3,3)} = {N(Fn/1e3,3)} kN.\n(d) TSFC = 0.75/{N(Fn,1)} N = {N(mff/Fn*1e6,2)} mg/(s·N) = {N(ts,4)} kg/(h·N).\n(e) ΔKE = ½[25.75×1050² − 25×{N(V0,1)}²] = {N(dke/1e6,3)} MW; η_th = ΔKE/(ṁf·QR) = {N(dke/1e6,3)}/{N(mff*QRf/1e6,1)} = {N(e_th,4)}.\n(f) η_p = Fn·V0/ΔKE = {N(Fn*V0/1e6,3)}/{N(dke/1e6,3)} = {N(e_p,4)}.\n(g) η_o = η_th·η_p = {N(e_o,4)} (= Fn·V0/(ṁf·QR) = {N(Fn*V0/(mff*QRf),4)}, kiểm).',
          f'Assume γ = 1.4, R = 287 J/kg·K, T0 = 223.15 K.\nV0 = Ma·√(γRT0) = 2×{N(V0/2,2)} = {N(V0,1)} m/s.\n(a) Ram drag = ṁ0·V0 = 25×{N(V0,1)} = {N(Dr/1e3,3)} kN.\n(b) Gross = (ṁ0 + ṁf)·V9 = 25.75×1050 = {N(Fg/1e3,3)} kN (p9 = p0, so no pressure thrust).\n(c) Net = {N(Fg/1e3,3)} − {N(Dr/1e3,3)} = {N(Fn/1e3,3)} kN.\n(d) TSFC = 0.75/{N(Fn,1)} N = {N(mff/Fn*1e6,2)} mg/(s·N) = {N(ts,4)} kg/(h·N).\n(e) ΔKE = ½[25.75×1050² − 25×{N(V0,1)}²] = {N(dke/1e6,3)} MW; η_th = ΔKE/(ṁf·QR) = {N(dke/1e6,3)}/{N(mff*QRf/1e6,1)} = {N(e_th,4)}.\n(f) η_p = Fn·V0/ΔKE = {N(Fn*V0/1e6,3)}/{N(dke/1e6,3)} = {N(e_p,4)}.\n(g) η_o = η_th·η_p = {N(e_o,4)} (= Fn·V0/(ṁf·QR) = {N(Fn*V0/(mff*QRf),4)}, check).'),
        3, T_EFF, SRC('Farokhi Ch.3 Problem 3.5', 'Farokhi Ch.3 Problem 3.5'), 'goc', 'script (verify_m01: f35)'))

    # --- Farokhi 3.6 turboprop
    Fp, V0t, ept, mt, Fgn = 5000, 150, .75, 5, 1000
    Ps = Fp*V0t/ept; V9t = Fgn/mt; dk = .5*mt*(V9t**2 - V0t**2); Fnet = Fp + Fgn - mt*V0t
    ep6 = Fnet*V0t/(Ps+dk); ep6a = Fnet*V0t/Ps
    reg('f36', {}, dict(Ps=Ps, V9=V9t, dk=dk, ep=ep6, epa=ep6a))
    I.append(ess(
        B('Farokhi Problem 3.6. Máy bay turboprop bay ở V0 = 150 m/s, hiệu suất cánh quạt 0.75, lực đẩy cánh quạt 5000 N, lưu lượng khí qua động cơ 5 kg/s. Vòi phun giãn nở hoàn toàn và cho lực đẩy tổng 1000 N. Tính: (a) công suất trục truyền cho cánh quạt (kW); (b) vận tốc phụt (bỏ qua lưu lượng nhiên liệu); (c) chứng tỏ ΔK̇E nhỏ so với công suất trục rồi ước lượng η_p = F·V0/(℘s + ΔK̇E).',
          'Farokhi Problem 3.6. A turboprop aircraft flies at V0 = 150 m/s with propeller efficiency 0.75. Propeller thrust is 5000 N, engine air flow 5 kg/s, the nozzle is perfectly expanded and gives 1000 N gross thrust. Calculate: (a) shaft power delivered to the propeller (kW); (b) the nozzle exit velocity (neglect fuel flow); (c) show that the net kinetic power ΔK̇E is small against the shaft power, then estimate η_p = F·V0/(℘s + ΔK̇E).'),
        B(f'(a) η_prop = Fprop·V0/℘s ⇒ ℘s = 5000×150/0.75 = {N(Ps/1e3,1)} kW.\n(b) Vòi phun giãn nở hoàn toàn: Fg = ṁ·V9 ⇒ V9 = 1000/5 = {N(V9t,0)} m/s.\n(c) ΔK̇E = ½ṁ(V9² − V0²) = 0.5×5×({N(V9t**2,0)} − {N(V0t**2,0)}) = {N(dk/1e3,2)} kW, chỉ {N(dk/Ps*100,1)} % của ℘s. Lực đẩy tổng F = Fprop + (Fg − ṁV0) = 5000 + (1000 − 750) = {N(Fnet,0)} N (lực đẩy thực của ống xả chỉ 250 N vì còn trừ lực cản ram 750 N).\nη_p = F·V0/(℘s + ΔK̇E) = {N(Fnet*V0/1e3,1)}/({N(Ps/1e3,1)} + {N(dk/1e3,2)}) = {N(ep6,4)}; gần đúng η_p ≈ F·V0/℘s = {N(ep6a,4)}.\nKiểm: η_p cũng ≈ η_prop + đóng góp ống xả: ({N(Fp*V0,0)} + {N((Fgn-mt*V0t)*V0t,0)})/({N(Ps,0)} + {N(dk,0)}) = {N(ep6,4)}.',
          f'(a) η_prop = Fprop·V0/℘s ⇒ ℘s = 5000×150/0.75 = {N(Ps/1e3,1)} kW.\n(b) Perfectly expanded: Fg = ṁ·V9 ⇒ V9 = 1000/5 = {N(V9t,0)} m/s.\n(c) ΔK̇E = ½ṁ(V9² − V0²) = 0.5×5×({N(V9t**2,0)} − {N(V0t**2,0)}) = {N(dk/1e3,2)} kW, only {N(dk/Ps*100,1)} % of ℘s. Total thrust F = Fprop + (Fg − ṁV0) = 5000 + (1000 − 750) = {N(Fnet,0)} N (the exhaust net thrust is only 250 N because the 750 N ram drag must be subtracted).\nη_p = F·V0/(℘s + ΔK̇E) = {N(Fnet*V0/1e3,1)}/({N(Ps/1e3,1)} + {N(dk/1e3,2)}) = {N(ep6,4)}; approximately η_p ≈ F·V0/℘s = {N(ep6a,4)}.\nCheck: η_p as propeller plus exhaust contribution: ({N(Fp*V0,0)} + {N((Fgn-mt*V0t)*V0t,0)})/({N(Ps,0)} + {N(dk,0)}) = {N(ep6,4)}.'),
        2, T_EFF, SRC('Farokhi Ch.3 Problem 3.6', 'Farokhi Ch.3 Problem 3.6'), 'goc', 'script (verify_m01: f36)'))

    # --- Farokhi 3.9 turbofan
    cp9, g9, cp19, g19 = 1157, 1.33, 1004, 1.4
    R9 = cp9*(g9-1)/g9; T9 = 450**2/(g9*R9); V9c = 1.5*450; r9 = 15e3/(R9*T9); A9 = 10/(r9*V9c); Fg9 = 10*V9c + A9*(15e3-10e3)
    R19 = cp19*(g19-1)/g19; T19 = 310**2/(g19*R19); V19 = 1.5*310; r19 = 15e3/(R19*T19); A19 = 65/(r19*V19); Fg19 = 65*V19 + A19*5e3
    Dram = 75*.85*300; Fn9 = Fg9 + Fg19 - Dram
    reg('f39', {}, dict(Dram=Dram, Fg9=Fg9, Fg19=Fg19, Fn=Fn9, A9=A9, A19=A19))
    I.append(ess(
        B('Farokhi Problem 3.9 (câu a–d). Động cơ turbofan, p0 = 10 kPa, Ma0 = 0.85, a0 = 300 m/s, ṁ0 = 75 kg/s. Vòi phun lõi (9): ṁ9 = 10 kg/s, p9 = 15 kPa, Ma9 = 1.5, a9 = 450 m/s, γ9 = 1.33, cp9 = 1157 J/kg·K. Vòi quạt (19): ṁ19 = 65 kg/s, p19 = 15 kPa, Ma19 = 1.5, a19 = 310 m/s, γ = 1.4, cp = 1004 J/kg·K. Tính: (a) lực cản ram; (b) lực đẩy tổng vòi lõi Fg9; (c) lực đẩy tổng vòi quạt Fg19; (d) lực đẩy thực Fn. (Gợi ý: tìm diện tích vòi phun từ lưu lượng và khối lượng riêng.)',
          'Farokhi Problem 3.9 (parts a–d). Turbofan with p0 = 10 kPa, Ma0 = 0.85, a0 = 300 m/s, ṁ0 = 75 kg/s. Core nozzle (9): ṁ9 = 10 kg/s, p9 = 15 kPa, Ma9 = 1.5, a9 = 450 m/s, γ9 = 1.33, cp9 = 1157 J/kg·K. Fan nozzle (19): ṁ19 = 65 kg/s, p19 = 15 kPa, Ma19 = 1.5, a19 = 310 m/s, γ = 1.4, cp = 1004 J/kg·K. Calculate: (a) ram drag; (b) core gross thrust Fg9; (c) fan gross thrust Fg19; (d) net thrust Fn. (Hint: find the nozzle areas from mass flow and density.)'),
        B(f'(a) Dram = ṁ0·V0 = 75×(0.85×300) = {N(Dram/1e3,3)} kN.\n(b) Lõi: R = cp(γ−1)/γ = {N(R9,1)} J/kg·K; T9 = a²/(γR) = {N(T9,1)} K; V9 = 1.5×450 = {N(V9c,0)} m/s; ρ9 = p9/(R·T9) = {N(r9,4)} kg/m³; A9 = ṁ/(ρV) = {N(A9,4)} m². Fg9 = ṁ9V9 + A9(p9 − p0) = 10×{N(V9c,0)} + {N(A9,4)}×5000 = {N(Fg9/1e3,3)} kN.\n(c) Quạt: R = {N(R19,1)}; T19 = {N(T19,1)} K; V19 = {N(V19,0)} m/s; ρ19 = {N(r19,4)} kg/m³; A19 = {N(A19,4)} m². Fg19 = 65×{N(V19,0)} + {N(A19,4)}×5000 = {N(Fg19/1e3,3)} kN.\n(d) Fn = Fg9 + Fg19 − Dram = {N(Fn9/1e3,3)} kN.\nKiểm: tính ρ qua nhiệt độ tĩnh T = Tt/(1 + (γ−1)/2·Ma²) với Tt suy từ a thì cho cùng kết quả (cách khác: Fg = ṁV + A·Δp với A = ṁ/(ρ V)); xem verify.',
          f'(a) Dram = ṁ0·V0 = 75×(0.85×300) = {N(Dram/1e3,3)} kN.\n(b) Core: R = cp(γ−1)/γ = {N(R9,1)} J/kg·K; T9 = a²/(γR) = {N(T9,1)} K; V9 = 1.5×450 = {N(V9c,0)} m/s; ρ9 = p9/(R·T9) = {N(r9,4)} kg/m³; A9 = ṁ/(ρV) = {N(A9,4)} m². Fg9 = ṁ9V9 + A9(p9 − p0) = 10×{N(V9c,0)} + {N(A9,4)}×5000 = {N(Fg9/1e3,3)} kN.\n(c) Fan: R = {N(R19,1)}; T19 = {N(T19,1)} K; V19 = {N(V19,0)} m/s; ρ19 = {N(r19,4)} kg/m³; A19 = {N(A19,4)} m². Fg19 = 65×{N(V19,0)} + {N(A19,4)}×5000 = {N(Fg19/1e3,3)} kN.\n(d) Fn = Fg9 + Fg19 − Dram = {N(Fn9/1e3,3)} kN.\nCheck: density found through static temperature from Tt = T(1 + (γ−1)/2·Ma²) gives the same result (second route: Fg = ṁV + A·Δp with A = ṁ/(ρV)); see verify.'),
        3, T_THR, SRC('Farokhi Ch.3 Problem 3.9 (câu a–d)', 'Farokhi Ch.3 Problem 3.9 (parts a–d)'), 'goc', 'script (verify_m01: f39)'))

    # --- Farokhi 3.10 ramjet
    V0r = 2*math.sqrt(GAM*R_AIR*223.15); T9r = 2500/(1+.2*4); Rr = 1004*.4/1.4; V9r = 2*math.sqrt(GAM*Rr*T9r)
    Dr10 = 10*V0r; Fg10 = 10*1.04*V9r; Fn10 = Fg10-Dr10; dk10 = .5*(10.4*V9r**2 - 10*V0r**2); ep10 = Fn10*V0r/dk10
    reg('f310', {}, dict(V0=V0r, V9=V9r, Dr=Dr10, Fg=Fg10, Fn=Fn10, ep=ep10))
    I.append(ess(
        B('Farokhi Problem 3.10. Một ramjet bay ở Ma 2.0 tại độ cao có T0 = −50 °C, lưu lượng khí 10 kg/s. Số Mach phụt bằng số Mach bay (Ma9 = Ma0), vòi phun giãn nở hoàn toàn, Tt9 = 2500 K. Giả thiết γ = 1.4, cp = 1004 J/kg·K, lưu lượng nhiên liệu 4 % lưu lượng khí. Tính: (a) lực cản ram (kN); (b) lực đẩy tổng (kN); (c) lực đẩy thực (kN); (d) hiệu suất đẩy.',
          'Farokhi Problem 3.10. A ramjet flies at Mach 2.0 where T0 = −50 °C, engine air flow 10 kg/s. The exhaust Mach number equals the flight Mach number (Ma9 = Ma0), the nozzle is perfectly expanded, Tt9 = 2500 K. Assume γ = 1.4, cp = 1004 J/kg·K and fuel flow 4 % of the air flow. Calculate: (a) ram drag (kN); (b) gross thrust (kN); (c) net thrust (kN); (d) propulsive efficiency.'),
        B(f'R = cp(γ−1)/γ = {N(Rr,2)} J/kg·K. V0 = 2×√(1.4×287×223.15) = {N(V0r,1)} m/s (R khí quyển = 287).\n(a) Dram = 10×{N(V0r,1)} = {N(Dr10/1e3,3)} kN.\n(b) T9 = Tt9/(1 + 0.2×2²) = 2500/1.8 = {N(T9r,1)} K; V9 = 2×√(1.4×{N(Rr,2)}×{N(T9r,1)}) = {N(V9r,1)} m/s; Fg = 10.4×{N(V9r,1)} = {N(Fg10/1e3,3)} kN.\n(c) Fn = {N(Fg10/1e3,3)} − {N(Dr10/1e3,3)} = {N(Fn10/1e3,3)} kN.\n(d) ΔKE = ½(10.4×V9² − 10×V0²) = {N(dk10/1e6,3)} MW; η_p = Fn·V0/ΔKE = {N(ep10,4)}. (Công thức gần đúng 2/(1 + V9/V0) = {N(2/(1+V9r/V0r),4)} cao hơn vì bỏ qua lưu lượng nhiên liệu.)\nKiểm: V9 tính lại qua V9 = Ma9·a9 với a9 = √(γRT9) = {N(math.sqrt(GAM*Rr*T9r),1)} m/s.',
          f'R = cp(γ−1)/γ = {N(Rr,2)} J/kg·K. V0 = 2×√(1.4×287×223.15) = {N(V0r,1)} m/s (ambient R = 287).\n(a) Dram = 10×{N(V0r,1)} = {N(Dr10/1e3,3)} kN.\n(b) T9 = Tt9/(1 + 0.2×2²) = 2500/1.8 = {N(T9r,1)} K; V9 = 2×√(1.4×{N(Rr,2)}×{N(T9r,1)}) = {N(V9r,1)} m/s; Fg = 10.4×{N(V9r,1)} = {N(Fg10/1e3,3)} kN.\n(c) Fn = {N(Fg10/1e3,3)} − {N(Dr10/1e3,3)} = {N(Fn10/1e3,3)} kN.\n(d) ΔKE = ½(10.4×V9² − 10×V0²) = {N(dk10/1e6,3)} MW; η_p = Fn·V0/ΔKE = {N(ep10,4)}. (The approximation 2/(1 + V9/V0) = {N(2/(1+V9r/V0r),4)} is higher because it ignores the fuel flow.)\nCheck: V9 recomputed from V9 = Ma9·a9 with a9 = √(γRT9) = {N(math.sqrt(GAM*Rr*T9r),1)} m/s.'),
        3, T_THR, SRC('Farokhi Ch.3 Problem 3.10', 'Farokhi Ch.3 Problem 3.10'), 'goc', 'script (verify_m01: f310)'))

    # --- Farokhi 3.11 turbojet
    V0j, uej, mj, mfj, QRj = 300, 600, 100, 2.5, 42e6
    Drj = mj*V0j; Fgj = (mj+mfj)*uej; Fnj = Fgj-Drj; tsj = mfj/Fnj*1e6; dkj = .5*((mj+mfj)*uej**2 - mj*V0j**2)
    ethj = dkj/(mfj*QRj); epj = Fnj*V0j/dkj
    reg('f311', {}, dict(Dr=Drj, Fg=Fgj, Fn=Fnj, tsfc=tsj, eth=ethj, ep=epj))
    I.append(ess(
        B('Farokhi Problem 3.11. Máy bay turbojet bay ở V0 = 300 m/s, vận tốc phụt 600 m/s, lưu lượng khí 100 kg/s, lưu lượng nhiên liệu 2.5 kg/s, nhiệt trị 42 000 kJ/kg, vòi phun giãn nở hoàn toàn. Tính: (a) lực cản ram (kN); (b) lực đẩy tổng (kN); (c) lực đẩy thực (kN); (d) TSFC (mg/s/kN); và thêm η_th, η_p.',
          'Farokhi Problem 3.11. A turbojet cruises at V0 = 300 m/s with exhaust speed 600 m/s, air flow 100 kg/s, fuel flow 2.5 kg/s, heating value 42,000 kJ/kg, nozzle perfectly expanded. Calculate: (a) ram drag (kN); (b) gross thrust (kN); (c) net thrust (kN); (d) TSFC (mg/s/kN); and in addition η_th and η_p.'),
        B(f'(a) Dram = ṁ·V0 = 100×300 = {N(Drj/1e3,1)} kN.\n(b) Fg = (ṁ + ṁf)·V9 = 102.5×600 = {N(Fgj/1e3,1)} kN.\n(c) Fn = {N(Fgj/1e3,1)} − {N(Drj/1e3,1)} = {N(Fnj/1e3,1)} kN.\n(d) TSFC = ṁf/Fn = 2.5/{N(Fnj/1e3,1)} = {N(tsj*1e3,0)} mg/(s·kN) (= {N(tsj,2)} mg/(s·N)).\nThêm: ΔKE = ½(102.5×600² − 100×300²) = {N(dkj/1e6,2)} MW; η_th = {N(dkj/1e6,2)}/{N(mfj*QRj/1e6,0)} = {N(ethj,4)}; η_p = Fn·V0/ΔKE = {N(epj,4)}; η_o = {N(ethj*epj,4)}.\nKiểm: η_o = Fn·V0/(ṁf·QR) = {N(Fnj*V0j/(mfj*QRj),4)}.',
          f'(a) Dram = ṁ·V0 = 100×300 = {N(Drj/1e3,1)} kN.\n(b) Fg = (ṁ + ṁf)·V9 = 102.5×600 = {N(Fgj/1e3,1)} kN.\n(c) Fn = {N(Fgj/1e3,1)} − {N(Drj/1e3,1)} = {N(Fnj/1e3,1)} kN.\n(d) TSFC = ṁf/Fn = 2.5/{N(Fnj/1e3,1)} = {N(tsj*1e3,0)} mg/(s·kN) (= {N(tsj,2)} mg/(s·N)).\nExtra: ΔKE = ½(102.5×600² − 100×300²) = {N(dkj/1e6,2)} MW; η_th = {N(dkj/1e6,2)}/{N(mfj*QRj/1e6,0)} = {N(ethj,4)}; η_p = Fn·V0/ΔKE = {N(epj,4)}; η_o = {N(ethj*epj,4)}.\nCheck: η_o = Fn·V0/(ṁf·QR) = {N(Fnj*V0j/(mfj*QRj),4)}.'),
        2, T_THR, SRC('Farokhi Ch.3 Problem 3.11', 'Farokhi Ch.3 Problem 3.11'), 'goc', 'script (verify_m01: f311)'))

    # --- El-Sayed Example 2.4 (thrust distribution)
    comp = [(648e3, .117, 124, None), (655e3, .132, 112, 0), (641e3, .374, 94, 1), (145e3, .310, 271, 2), (145e3, .420, 196, 3), (41e3, .214, 584, 4)]
    names = ['Compressor', 'Diffuser', 'Combustion chamber', 'Turbine', 'Jet pipe', 'Nozzle']
    names_vi = ['Máy nén', 'Bộ khuếch tán', 'Buồng đốt', 'Tuabin', 'Ống xả', 'Vòi phun']
    Fc = []; prev = (0.0, 0.0, 0.0)
    for (p, A, U, _) in comp:
        Fc.append(p*A - prev[0]*prev[1] + 69.4*(U - prev[2])); prev = (p, A, U)
    tot = sum(Fc); Tdirect = 41e3*.214 + 69.4*584
    reg('ex24', {}, dict(F=Fc, tot=tot, direct=Tdirect))
    rows_vi = '\n'.join(f'   {names_vi[i]}: {N(Fc[i],0)} N ({"phía trước" if Fc[i] > 0 else "phía sau"})' for i in range(6))
    rows_en = '\n'.join(f'   {names[i]}: {N(Fc[i],0)} N ({"forward" if Fc[i] > 0 else "rearward"})' for i in range(6))
    I.append(ess(
        B('El-Sayed Ví dụ 2.4. Một turbojet một trục có bảng (cửa ra từng bộ phận; áp suất là áp suất dư; lưu lượng 69.4 kg/s, bỏ qua nhiên liệu): Máy nén 0.117 m², 124 m/s, 648 kPa; Khuếch tán 0.132 m², 112 m/s, 655 kPa; Buồng đốt 0.374 m², 94 m/s, 641 kPa; Tuabin 0.310 m², 271 m/s, 145 kPa; Ống xả 0.420 m², 196 m/s, 145 kPa; Vòi phun 0.214 m², 584 m/s, 41 kPa. Tính lực đẩy sinh ra ở từng bộ phận và chứng minh tổng bằng lực đẩy cả động cơ.',
          'El-Sayed Example 2.4. A single-spool turbojet has the table (outlet of each component; gauge pressure; flow 69.4 kg/s, fuel neglected): Compressor 0.117 m², 124 m/s, 648 kPa; Diffuser 0.132 m², 112 m/s, 655 kPa; Combustor 0.374 m², 94 m/s, 641 kPa; Turbine 0.310 m², 271 m/s, 145 kPa; Jet pipe 0.420 m², 196 m/s, 145 kPa; Nozzle 0.214 m², 584 m/s, 41 kPa. Calculate the thrust generated by each component and prove that the sum equals the engine thrust.'),
        B(f'Mỗi bộ phận: F = Pe·Ae − Pi·Ai + ṁ(Ue − Ui) (áp suất dư; cửa vào máy nén coi P = 0 dư, U = 0).\n{rows_vi}\nTổng = {N(tot,0)} N.\nToàn động cơ: T = Pe,dư·Ae + ṁ·Ue = 41 000×0.214 + 69.4×584 = {N(Tdirect,0)} N. Hai kết quả trùng nhau (khác biệt do làm tròn). Nhận xét: máy nén, khuếch tán, buồng đốt, ống xả đẩy về phía trước; tuabin ({N(Fc[3],0)} N) và vòi phun kéo về phía sau; hiệu số là lực đẩy {N(tot/1e3,1)} kN.\nGhi chú nguồn: lời giải in trong sách có vài lỗi chép (dòng buồng đốt, "4 × 10³" thay cho 41 × 10³, −25 118 và −25 198 cho vòi phun); các số ở đây tính lại.',
          f'Each component: F = Pe·Ae − Pi·Ai + ṁ(Ue − Ui) (gauge pressures; compressor inlet taken as 0 gauge, U = 0).\n{rows_en}\nSum = {N(tot,0)} N.\nWhole engine: T = Pe,gauge·Ae + ṁ·Ue = 41,000×0.214 + 69.4×584 = {N(Tdirect,0)} N. The two agree (differences are rounding). Remark: compressor, diffuser, combustor and jet pipe push forward; the turbine ({N(Fc[3],0)} N) and the nozzle pull rearward; the difference is the thrust of {N(tot/1e3,1)} kN.\nSource note: the printed solution contains several typos (combustor line, "4 × 10³" for 41 × 10³, −25,118 and −25,198 for the nozzle); the numbers here are recomputed.'),
        3, T_THR, SRC('El-Sayed Ch.2 Example 2.4 (tr.83–86)', 'El-Sayed Ch.2 Example 2.4 (pp.83–86)'), 'goc', 'script (verify_m01: ex24)'))

    # --- Derivation problems (El-Sayed 2.11, 2.21)
    I.append(ess(
        B('El-Sayed Problem 2.21. Chứng minh η_o/ue² = λ(1 − u/ue)(u/ue) với λ = 1/(f·QR) (vòi phun không nghẹt, bỏ qua f trong lực đẩy). Suy ra khi nào η_o/(λue²) đạt cực đại và giá trị đó.',
          'El-Sayed Problem 2.21. Prove that η_o/ue² = λ(1 − u/ue)(u/ue) with λ = 1/(f·QR) (unchoked nozzle, f neglected in the thrust). Deduce when η_o/(λue²) is maximum and its value.'),
        B('Với vòi phun không nghẹt và bỏ qua f: T = ṁa(ue − u). η_o = T·u/(ṁf·QR) = ṁa(ue − u)u/(f·ṁa·QR) = (ue − u)u/(f·QR).\nChia cho ue²: η_o/ue² = (1/(f·QR))·(1 − u/ue)(u/ue) = λ(1 − x)x với x = u/ue.\nĐặt h(x) = x(1 − x): h′(x) = 1 − 2x = 0 ⇒ x = 1/2; h″ = −2 < 0 nên là cực đại, h_max = 1/4. Vậy η_o,max = λ·ue²/4 = ue²/(4f·QR) tại u = ue/2.\nÝ nghĩa: tại u = 0 và u = ue, η_o = 0 (không có công đẩy hoặc không có lực đẩy); hiệu suất tổng tốt nhất khi bay bằng nửa vận tốc phụt. Khi giữ f trong lực đẩy, kết quả là (1+f)²ue²/(4f·QR) tại u = (1+f)ue/2 (xem Problem 2.5).\nKiểm: tính h(x) bằng số trên lưới 0–1 cho cực đại tại x = 0.5, h = 0.25.',
          'For an unchoked nozzle with f neglected: T = ṁa(ue − u). η_o = T·u/(ṁf·QR) = ṁa(ue − u)u/(f·ṁa·QR) = (ue − u)u/(f·QR).\nDivide by ue²: η_o/ue² = (1/(f·QR))·(1 − u/ue)(u/ue) = λ(1 − x)x with x = u/ue.\nLet h(x) = x(1 − x): h′(x) = 1 − 2x = 0 ⇒ x = 1/2; h″ = −2 < 0 so it is a maximum, h_max = 1/4. Hence η_o,max = λ·ue²/4 = ue²/(4f·QR) at u = ue/2.\nMeaning: at u = 0 and u = ue, η_o = 0 (no thrust power, or no thrust); the best overall efficiency occurs when flying at half the jet speed. Keeping f in the thrust gives (1+f)²ue²/(4f·QR) at u = (1+f)ue/2 (see Problem 2.5).\nCheck: evaluating h(x) numerically on a 0–1 grid gives the maximum at x = 0.5, h = 0.25.'),
        2, T_EFF, SRC('El-Sayed Ch.2 Problem 2.21', 'El-Sayed Ch.2 Problem 2.21'), 'goc', 'script (verify_m01: p221)'))
    I.append(ess(
        B('El-Sayed Problem 2.11. Chứng minh lực đẩy riêng và TSFC của turbofan: T/ṁa = [(1+f)/(1+β)]·ue,h + [β/(1+β)]·ue,c − u và TSFC = f/[(1+β)(T/ṁa)] (β = tỉ số rẽ nhánh, f = ṁf/ṁh).',
          'El-Sayed Problem 2.11. Show that the specific thrust and TSFC of a turbofan are T/ṁa = [(1+f)/(1+β)]·ue,h + [β/(1+β)]·ue,c − u and TSFC = f/[(1+β)(T/ṁa)] (β = bypass ratio, f = ṁf/ṁh).'),
        B('Dòng nóng ṁh, dòng lạnh ṁc = β·ṁh, tổng ṁa = ṁh + ṁc = (1+β)ṁh. Với vòi phun không nghẹt: T = ṁh[(1+f)ue,h − u] + ṁc(ue,c − u) (El-Sayed Eq. 2.4).\nChia cho ṁa = (1+β)ṁh: T/ṁa = [(1+f)ue,h − u]/(1+β) + β(ue,c − u)/(1+β) = (1+f)ue,h/(1+β) + β·ue,c/(1+β) − u(1+β)/(1+β) = (1+f)/(1+β)·ue,h + β/(1+β)·ue,c − u. ∎\nTSFC = ṁf/T, với ṁf = f·ṁh = f·ṁa/(1+β) ⇒ TSFC = f·ṁa/[(1+β)·T] = f/[(1+β)(T/ṁa)]. ∎\nKiểm số: ṁh = 20, β = 4, f = 0.02, ue,h = 500, ue,c = 350, u = 200: T trực tiếp = 20×(1.02×500 − 200) + 80×(350 − 200) = 6 200 + 12 000 = 18 200 N; công thức riêng: (1.02×500/5 + 4×350/5 − 200)×100 = (102 + 280 − 200)×100 = 18 200 N ✓.',
          'Hot stream ṁh, cold stream ṁc = β·ṁh, total ṁa = ṁh + ṁc = (1+β)ṁh. For unchoked nozzles: T = ṁh[(1+f)ue,h − u] + ṁc(ue,c − u) (El-Sayed Eq. 2.4).\nDivide by ṁa = (1+β)ṁh: T/ṁa = [(1+f)ue,h − u]/(1+β) + β(ue,c − u)/(1+β) = (1+f)ue,h/(1+β) + β·ue,c/(1+β) − u(1+β)/(1+β) = (1+f)/(1+β)·ue,h + β/(1+β)·ue,c − u. ∎\nTSFC = ṁf/T, with ṁf = f·ṁh = f·ṁa/(1+β) ⇒ TSFC = f·ṁa/[(1+β)·T] = f/[(1+β)(T/ṁa)]. ∎\nNumerical check: ṁh = 20, β = 4, f = 0.02, ue,h = 500, ue,c = 350, u = 200: direct T = 20×(1.02×500 − 200) + 80×(350 − 200) = 6,200 + 12,000 = 18,200 N; specific-thrust formula: (1.02×500/5 + 4×350/5 − 200)×100 = (102 + 280 − 200)×100 = 18,200 N ✓.'),
        2, T_THR, SRC('El-Sayed Ch.2 Problem 2.11', 'El-Sayed Ch.2 Problem 2.11'), 'goc', 'algebra + numeric check (verify_m01: p211)'))

    # --- Conceptual ess goc (El-Sayed Ch.1 problems): answers from the text of Ch.1
    def cess(q_vi, q_en, a_vi, a_en, num, src_slide=''):
        I.append(ess(B(q_vi, q_en), B(a_vi, a_en), 1, T_CLS, SRC(f'El-Sayed Ch.1 Problem {num}'), 'goc', f'book text El-Sayed §1.x (đối chiếu slide {src_slide})' if src_slide else 'book text'))
    cess('El-Sayed Ch.1 Problem 1.21. Những loại động cơ nào không có chi tiết chuyển động?',
         'El-Sayed Ch.1 Problem 1.21. Which engines have no moving parts?',
         'Ramjet: chỉ gồm cửa hút (khuếch tán), vùng cháy và vòi phun, không có máy nén lẫn tuabin quay (El-Sayed §1.4.1; Slide Ch.1 tr.18 "no moving mechanical parts"). Scramjet cũng vậy (không có tuabin máy). Pulsejet không van ("valveless", động cơ sóng) không có chi tiết mòn chuyển động (§1.4.2; Slide tr.21). Pulsejet có van thì có van lò xo chuyển động nên không thuộc nhóm này.',
         'Ramjet: only an inlet (diffuser), a combustion zone and a nozzle, with neither compressor nor turbine rotating (El-Sayed §1.4.1; Slide Ch.1 p.18 "no moving mechanical parts"). The scramjet is the same (no turbomachinery). The valveless pulsejet (wave engine) has no moving parts to wear out (§1.4.2; Slide p.21). The valved pulsejet has spring-loaded valves, so it is not in this group.', '1.21', 'Ch.1 tr.18, 21')
    cess('El-Sayed Ch.1 Problem 1.22. Loại động cơ nào dẫn động phần lớn máy bay chở khách hiện nay?',
         'El-Sayed Ch.1 Problem 1.22. What is the type of engine that powers most of today\'s airliners?',
         'Turbofan tỉ số rẽ nhánh cao (BPR ≥ 5:1), ví dụ JT9, CF6, CFM56, PW4000, GE90, Trent (El-Sayed §1.5.4). Ở tốc độ cận âm chúng tiết kiệm nhiên liệu và êm hơn các loại phản lực khác. Slide Ch.1 tr.41 ghi "Widely used in commercial transport aircraft" và tr.42 nêu CFM56 cho họ Airbus A320.',
         'The high-bypass-ratio turbofan (BPR ≥ 5:1), e.g. JT9, CF6, CFM56, PW4000, GE90, Trent (El-Sayed §1.5.4). At subsonic speed they are more fuel efficient and quieter than other jet engines. Slide Ch.1 p.41 says "Widely used in commercial transport aircraft" and p.42 gives the CFM56 for the Airbus A320 family.', '1.22', 'Ch.1 tr.41–42')
    cess('El-Sayed Ch.1 Problem 1.23. Loại động cơ nào được dùng trên trực thăng?',
         'El-Sayed Ch.1 Problem 1.23. What is the type of engine used in a helicopter?',
         'Động cơ trục (turboshaft): bố trí giống turboprop nhưng đưa công suất ra trục (tuabin công suất tự do), hộp số chính thuộc trực thăng chứ không thuộc động cơ, và tránh lực đẩy dư bằng giãn nở thêm trong tuabin và/hoặc quay ống xả 90° (El-Sayed §1.5.3; Slide Ch.1 tr.34–35).',
         'The turboshaft: laid out like a turboprop but delivering shaft power (free power turbine); the main gearbox belongs to the helicopter, not to the engine, and residual thrust is avoided by further expansion in the turbine and/or turning the exhaust through 90° (El-Sayed §1.5.3; Slide Ch.1 pp.34–35).', '1.23', 'Ch.1 tr.34–35')
    cess('El-Sayed Ch.1 Problem 1.24. Turboprop khác turbojet ở điểm nào?',
         'El-Sayed Ch.1 Problem 1.24. How is a turboprop different from a turbojet?',
         'Turbojet: toàn bộ năng lượng khí chủ yếu thành động năng phụt ra, lực đẩy do ống phun (phản lực trực tiếp). Turboprop: thiết kế tối ưu để sinh công suất trục quay cánh quạt qua hộp giảm tốc; lực đẩy chính do cánh quạt, ống xả chỉ cho lực đẩy dư (phản lực gián tiếp). Vì vậy turboprop hiệu quả hơn ở tốc độ dưới 400–450 mph và độ cao dưới 30 000 ft (El-Sayed §1.5.2; Slide Ch.1 tr.31–32, 44–45).',
         'Turbojet: the gas energy becomes mainly jet kinetic energy and thrust comes from the nozzle (direct reaction). Turboprop: optimised to produce shaft power that turns a propeller through a reduction gearbox; the propeller gives the main thrust and the exhaust only a residual thrust (indirect reaction). Hence the turboprop is more efficient below 400–450 mph and 30,000 ft (El-Sayed §1.5.2; Slide Ch.1 pp.31–32, 44–45).', '1.24', 'Ch.1 tr.31–32, 43–45')
    cess('El-Sayed Ch.1 Problem 1.32. So sánh ramjet và scramjet.',
         'El-Sayed Ch.1 Problem 1.32. Compare ramjet and scramjet engines.',
         'Giống nhau: không có máy nén/tuabin, nén bằng hiệu ứng ram ở cửa hút, đều cần được gia tốc ban đầu bằng nguồn ngoài. Khác nhau: ramjet làm dòng khí giảm xuống cận âm trước buồng đốt; scramjet cháy ở tốc độ khí siêu âm nên đạt tốc độ lớn hơn (dự báo Ma 12–24 theo El-Sayed §1.4.3; hydro là nhiên liệu thường dùng) nhưng phức tạp về khí động học hơn nhiều. Ramjet hiệu quả ở tốc độ cao nhưng kém ở tốc độ cận âm (§1.4.1; Slide Ch.1 tr.18, 22).',
         'Alike: no compressor or turbine, compression by the ram effect in the inlet, both need an initial boost from an external source. Different: the ramjet slows the flow to subsonic speed before the combustor; the scramjet burns at supersonic air speed, so it reaches greater speeds (projected Ma 12–24 per El-Sayed §1.4.3; hydrogen is the usual fuel) but is aerodynamically much more complex. The ramjet is efficient at high speed but poor at subsonic speed (§1.4.1; Slide Ch.1 pp.18, 22).', '1.32', 'Ch.1 tr.18, 22')
    cess('El-Sayed Ch.1 Problem 1.47. Phân loại turbojet theo (1) hệ nén, (2) số trục, (3) bộ đốt sau.',
         'El-Sayed Ch.1 Problem 1.47. Classify turbojet engines according to (1) compression system, (2) number of spools, (3) afterburning.',
         '(1) Máy nén ly tâm hoặc hướng trục (turbojet đầu tiên của Whittle W.1 và von Ohain He S-1 dùng máy nén ly tâm; Slide Ch.1 tr.28 vẽ cả hai). (2) Một trục (single spool) hoặc hai trục (double spool). (3) Có bộ đốt sau (afterburning, tăng lực đẩy, đổi lại tốn nhiên liệu; Concorde là máy bay dân dụng duy nhất có bộ đốt sau) hoặc không. Ngoài ra sách còn nêu phân loại hạt nhân/không hạt nhân (El-Sayed §1.5.1).',
         '(1) Centrifugal or axial compressor (the first turbojets, Whittle W.1 and von Ohain He S-1, used centrifugal compressors; Slide Ch.1 p.28 shows both). (2) Single spool or double spool. (3) Afterburning (extra thrust at the cost of fuel; Concorde was the only civil transport with afterburners) or non-afterburning. The book also lists nuclear/non-nuclear (El-Sayed §1.5.1).', '1.47', 'Ch.1 tr.28, 30')
    cess('El-Sayed Ch.1 Problem 1.48. Phân loại turbofan theo (1) BPR, (2) vị trí quạt, (3) số trục, (4) bộ đốt sau.',
         'El-Sayed Ch.1 Problem 1.48. Classify turbofan engines according to (1) BPR, (2) fan location, (3) number of spools, (4) afterburning.',
         '(1) BPR thấp (chủ yếu quân sự) hoặc cao (≥ 5:1, máy bay chở khách: JT9, CF6, CFM56, PW4000, GE90). (2) Quạt phía trước (forward fan) hoặc phía sau (aft fan). (3) Một, hai (GE90, CF6, PW4000, CFM56) hoặc ba trục (Rolls-Royce RB211, Trent; Slide Ch.1 tr.40 ghi Trent XWB 3 trục, tr.42 ghi CFM56 2 trục). (4) Có hoặc không có bộ đốt sau (BPR thấp quân sự, ví dụ F100). Ngoài ra: dòng trộn/không trộn, ống ngắn/dài, quạt giảm tốc/trực tiếp (El-Sayed §1.5.4).',
         '(1) Low BPR (mainly military) or high BPR (≥ 5:1, airliners: JT9, CF6, CFM56, PW4000, GE90). (2) Forward fan or aft fan. (3) One, two (GE90, CF6, PW4000, CFM56) or three spools (Rolls-Royce RB211, Trent; Slide Ch.1 p.40 gives the Trent XWB as 3-spool, p.42 the CFM56 as 2-spool). (4) Afterburning or not (low-BPR military engines such as the F100). Also: mixed/unmixed flow, short/long duct, geared/ungeared fan (El-Sayed §1.5.4).', '1.48', 'Ch.1 tr.36–42')
    return I


# ====================================================================================================================
def closed_orig():
    """printed Examples / Problems as single-answer closed questions (origin goc) + conceptual questions from slides (bo_sung)."""
    Q = []
    def mc(q, correct, wrongs, unit, nd, expl, level, topic, src, check, fig=None):
        o = numopts(correct, wrongs, unit, nd)
        Q.append(mcq(q, o, 0, expl, level, topic, src, 'goc', check, fig))
    # ----- El-Sayed Example 2.1: two flight speeds
    ma_, mf_, ue_, P = 30, 1, 610, 1.12e6
    disc = ((ma_+mf_)*ue_)**2 - 4*ma_*P; r1 = ((ma_+mf_)*ue_ + math.sqrt(disc))/(2*ma_); r2 = ((ma_+mf_)*ue_ - math.sqrt(disc))/(2*ma_)
    wr = lambda a, c: ((a*ue_) + math.sqrt((a*ue_)**2 - 4*ma_*c))/(2*ma_)
    reg('ex21', {}, dict(r1=r1, r2=r2))
    o = [opt(f'{N(r1,1)} m/s hoặc {N(r2,1)} m/s'), opt(f'{N(wr(30,P),1)} m/s hoặc {N((30*ue_-math.sqrt((30*ue_)**2-4*30*P))/60,1)} m/s'),
         opt(f'{N(wr(31,P*1e-3*1e3/1),1) if False else N(P/((ma_+mf_)*ue_),1)} m/s (bỏ qua số hạng bậc hai)'), opt(f'{N(math.sqrt(P/ma_),1)} m/s')]
    o = [dict(vi=x['vi'], en=x['en'].replace('hoặc', 'or').replace('bỏ qua số hạng bậc hai', 'dropping the quadratic term')) for x in o]
    Q.append(mcq(B('Không khí chảy qua động cơ phản lực với lưu lượng 30 kg/s, nhiên liệu 1 kg/s; khí xả rời vòi phun với vận tốc tương đối 610 m/s, áp suất cân bằng ở cửa ra. Công suất đẩy (thrust power) là 1.12×10⁶ W. Phương trình T·u = (ṁa+ṁf)ue·u − ṁa·u² cho vận tốc máy bay u là:',
                    'Air flows through a jet engine at 30 kg/s and the fuel flow is 1 kg/s. The exhaust gases leave the nozzle at a relative velocity of 610 m/s with pressure equilibrium at the exit plane. The thrust power is 1.12×10⁶ W. The equation T·u = (ṁa+ṁf)ue·u − ṁa·u² gives the flight speed u as:'),
                 o, 0, B(f'Công suất đẩy = (31×610)u − 30u² = 1.12×10⁶ ⇒ 30u² − 18 910u + 1.12×10⁶ = 0, hai nghiệm {N(r1,2)} và {N(r2,2)} m/s (sách in 564.15 và 66.17). Nghiệm lớn là chế độ bay thực tế của động cơ phản lực; nghiệm nhỏ là chế độ bay chậm với cùng công suất đẩy.',
                         f'Thrust power = (31×610)u − 30u² = 1.12×10⁶ ⇒ 30u² − 18,910u + 1.12×10⁶ = 0, two roots {N(r1,2)} and {N(r2,2)} m/s (the book prints 564.15 and 66.17). The larger root is the realistic jet cruise; the smaller one is a slow flight state with the same thrust power.'),
                 2, T_THR, SRC('El-Sayed Ch.2 Example 2.1 (tr.79)', 'El-Sayed Ch.2 Example 2.1 (p.79)'), 'goc', 'printed answer + script (ex21)'))
    # ----- Example 2.2 (thrust reversal)
    Ff = 100/32.2*(450-146.67); Fr = 100/32.2*(0-146.67)
    reg('ex22', {}, dict(Ff=Ff, Fr=Fr))
    mc(B('Máy bay hạ cánh lăn trên đường băng ở 100 mph; động cơ ở chế độ chạy chậm hút 100 lbm/s không khí và phụt với vận tốc 450 ft/s. Lực đẩy tiến của động cơ là bao nhiêu? (1 mph = 1.4667 ft/s)',
          'A landing aircraft rolls at 100 mph; the idling engine consumes air at 100 lbm/s and produces an exhaust velocity of 450 ft/s. What is the forward thrust of the engine? (1 mph = 1.4667 ft/s)'),
       Ff, [100/32.2*450, 100/32.2*(450+146.67), Ff/1.4667], 'lbf', 0,
       B(f'T = ṁa(Ue − U)/gc = (100/32.2)×(450 − 146.67) = {N(Ff,0)} lbf. Quên trừ vận tốc bay cho {N(100/32.2*450,0)} lbf; cộng thay vì trừ cho {N(100/32.2*(450+146.67),0)} lbf.',
         f'T = ṁa(Ue − U)/gc = (100/32.2)×(450 − 146.67) = {N(Ff,0)} lbf. Forgetting the flight speed gives {N(100/32.2*450,0)} lbf; adding instead of subtracting gives {N(100/32.2*(450+146.67),0)} lbf.'),
       1, T_THR, SRC('El-Sayed Ch.2 Example 2.2a (tr.80)', 'El-Sayed Ch.2 Example 2.2a (p.80)'), 'printed answer 942 lbf + script (ex22)')
    mc(B('Cũng trong tình huống trên (100 mph, 100 lbm/s), nếu dòng phụt bị làm lệch 90° (thành phần ngang của vận tốc phụt bằng 0) và lưu lượng giữ nguyên, lực đẩy theo phương chuyển động là:',
          'In the same situation (100 mph, 100 lbm/s), if the exhaust is deflected 90° (zero horizontal exhaust velocity) with the mass flow kept constant, the thrust along the flight direction is:'),
       Fr, [-Ff, 0.0, Fr*-1], 'lbf', 1,
       B(f'Thành phần ngang của Ue bằng 0: T = (100/32.2)×(0 − 146.67) = {N(Fr,1)} lbf, âm nghĩa là lực hãm (đẩy ngược): chính là lý do bộ đảo chiều lực đẩy giúp phanh. Chú ý dấu: lực đẩy tiến dương, ngược là âm.',
         f'Horizontal Ue = 0: T = (100/32.2)×(0 − 146.67) = {N(Fr,1)} lbf; the negative sign means a braking (reverse) force, which is why thrust reversers help to brake. Mind the sign: forward thrust positive, reverse negative.'),
       2, T_THR, SRC('El-Sayed Ch.2 Example 2.2b (tr.80)', 'El-Sayed Ch.2 Example 2.2b (p.80)'), 'printed answer −455.5 lbf + script (ex22)')
    # ----- Example 2.3
    rho = 30.8e3/(R_AIR*229.74); Uk = 1000/3.6; mdot = rho*Uk*.235; Tm = mdot*1.02*600; Dm = mdot*Uk; Tp = .25*(200-30.8)*1e3; Tn2 = Tm + Tp - Dm
    reg('ex23', {}, dict(Tmom1=40*1.02*600, Tp=Tp, Tn2=Tn2))
    mc(B('Turbojet bay ở độ cao 9 km (Ta = 229.74 K, Pa = 30.8 kPa), Ai = 0.235 m², Ae = 0.25 m², f = 0.02, Pe = 200 kPa, Ue = 600 m/s. Với lưu lượng khí không đổi 40 kg/s, lực đẩy áp suất (Pe − Pa)·Ae bằng:',
          'A turbojet flies at 9 km (Ta = 229.74 K, Pa = 30.8 kPa) with Ai = 0.235 m², Ae = 0.25 m², f = 0.02, Pe = 200 kPa, Ue = 600 m/s. With a constant air flow of 40 kg/s, the pressure thrust (Pe − Pa)·Ae equals:'),
       Tp, [.235*(200-30.8)*1e3, .25*200e3, .25*(200-30.8)], 'N', 0,
       B(f'Lực đẩy áp suất = Ae(Pe − Pa) = 0.25×(200 − 30.8)×10³ = {N(Tp,0)} N, không phụ thuộc vận tốc bay. Nhầm Ai thay cho Ae cho {N(.235*(200-30.8)*1e3,0)} N; dùng Pe thay cho (Pe − Pa) cho 50 000 N; quên đổi kPa sang Pa cho 42.3 (kN, không phải N).',
         f'Pressure thrust = Ae(Pe − Pa) = 0.25×(200 − 30.8)×10³ = {N(Tp,0)} N, independent of flight speed. Using Ai instead of Ae gives {N(.235*(200-30.8)*1e3,0)} N; using Pe instead of (Pe − Pa) gives 50,000 N; forgetting kPa → Pa gives 42.3 (kN, not N).'),
       2, T_THR, SRC('El-Sayed Ch.2 Example 2.3 (tr.81)', 'El-Sayed Ch.2 Example 2.3 (p.81)'), 'printed answer 42,300 N + script (ex23)')
    mc(B('Cùng động cơ (Ví dụ 2.3, trường hợp lưu lượng khí tỉ lệ với vận tốc bay: ṁa = ρ·U·Ai), lực đẩy thực khi bay ở 1000 km/h gần nhất với:',
          'Same engine (Example 2.3, case where the air flow follows the flight speed: ṁa = ρ·U·Ai), the net thrust at 1000 km/h is closest to:'),
       Tn2, [Tm + Tp, 66780 - 11.11*1000, Tn2 - Tp], 'N', 0,
       B(f'ρ = Pa/(R·Ta) = {N(rho,4)} kg/m³; U = 277.78 m/s; ṁa = ρ·U·Ai = {N(mdot,2)} kg/s. Thrust động lượng = ṁa(1+f)Ue = {N(Tm,0)} N; áp suất = {N(Tp,0)} N; cản động lượng = ṁa·U = {N(Dm,0)} N. Lực đẩy thực = {N(Tn2,0)} N (khớp công thức sách 42 300 + 18.66U − 8.47×10⁻³U² tại U = 1000). Chọn giá trị lưu lượng cố định 40 kg/s sẽ cho 66 780 − 11.11U = 55 670 N, sai vì lưu lượng thực giảm ở độ cao.',
         f'ρ = Pa/(R·Ta) = {N(rho,4)} kg/m³; U = 277.78 m/s; ṁa = ρ·U·Ai = {N(mdot,2)} kg/s. Momentum thrust = ṁa(1+f)Ue = {N(Tm,0)} N; pressure thrust = {N(Tp,0)} N; momentum drag = ṁa·U = {N(Dm,0)} N. Net thrust = {N(Tn2,0)} N (agrees with the book formula 42,300 + 18.66U − 8.47×10⁻³U² at U = 1000). Using the fixed 40 kg/s case would give 66,780 − 11.11U = 55,670 N, wrong because the real flow is lower at altitude.'),
       3, T_THR, SRC('El-Sayed Ch.2 Example 2.3 case 2 (tr.81–83)', 'El-Sayed Ch.2 Example 2.3 case 2 (pp.81–83)'), 'formula printed in book + script (ex23)')
    # ----- Example 2.4 total
    mc(B('Turbojet một trục: Pe,dư = 41 kPa, Ae = 0.214 m², Ue = 584 m/s, ṁ = 69.4 kg/s (bỏ qua nhiên liệu), cửa vào ở áp suất khí quyển với U = 0. Lực đẩy của động cơ là:',
          'Single-spool turbojet: exit gauge pressure 41 kPa, Ae = 0.214 m², Ue = 584 m/s, ṁ = 69.4 kg/s (fuel neglected), inlet at atmospheric pressure with U = 0. The engine thrust is:'),
       41e3*.214 + 69.4*584, [69.4*584, 41e3*.214, (41e3+101.325e3)*.214 + 69.4*584], 'N', 0,
       B(f'T = (Pe − Pa)Ae + ṁUe = 41 000×0.214 + 69.4×584 = {N(41e3*.214,0)} + {N(69.4*584,0)} = {N(41e3*.214+69.4*584,0)} N (sách in 49 304 N). Hai thành phần đều phải có mặt: chỉ động lượng cho {N(69.4*584,0)} N, chỉ áp suất cho {N(41e3*.214,0)} N; dùng áp suất tuyệt đối thay cho áp suất dư cho {N((41e3+101.325e3)*.214+69.4*584,0)} N.',
         f'T = (Pe − Pa)Ae + ṁUe = 41,000×0.214 + 69.4×584 = {N(41e3*.214,0)} + {N(69.4*584,0)} = {N(41e3*.214+69.4*584,0)} N (the book prints 49,304 N). Both terms must be present: momentum alone gives {N(69.4*584,0)} N, pressure alone {N(41e3*.214,0)} N; using absolute instead of gauge pressure gives {N((41e3+101.325e3)*.214+69.4*584,0)} N.'),
       1, T_THR, SRC('El-Sayed Ch.2 Example 2.4 (tr.86)', 'El-Sayed Ch.2 Example 2.4 (p.86)'), 'printed answer 49,304 N + script (ex24)')
    # ----- Example 2.5 (turbojet, M 0.8, 10 km)
    a10 = 223.3; u25 = .8*math.sqrt(1.4*287*a10); st25 = (1.02*570-u25) + .006*(.67e5-.265e5)
    e25 = 2*st25*u25/(2*st25*u25 + 1.02*(570-u25)**2); e25b = 2*st25*u25/(1.02*570**2-u25**2); e25c = 2*u25/(570+u25)
    reg('ex25', {}, dict(u=u25, st=st25, e1=e25, e2=e25b, e3=e25c))
    mc(B('Turbojet chiến đấu bay ở 10 km (Ta = 223.3 K, Pa = 0.265 bar), Ma 0.8; khí xả rời vòi phun ở 570 m/s, 0.67 bar; Ae/ṁa = 0.006 m²·s/kg; f = 0.02. Lực đẩy riêng T/ṁa (N·s/kg) là:',
          'A turbojet powers a fighter at 10 km (Ta = 223.3 K, Pa = 0.265 bar) and Ma 0.8; the exhaust leaves the nozzle at 570 m/s and 0.67 bar; Ae/ṁa = 0.006 m²·s/kg; f = 0.02. The specific thrust T/ṁa (N·s/kg) is:'),
       st25, [1.02*570-u25, st25 - .006*(.67e5), (570-u25) + .006*(.67e5-.265e5)], 'N·s/kg', 1,
       B(f'u = Ma·√(γRTa) = 0.8×√(1.4×287×223.3) = {N(u25,1)} m/s. T/ṁa = [(1+f)ue − u] + (Pe − Pa)·Ae/ṁa = (1.02×570 − {N(u25,1)}) + 0.006×(0.67 − 0.265)×10⁵ = {N(1.02*570-u25,1)} + {N(.006*(.67e5-.265e5),0)} = {N(st25,2)} N·s/kg (sách: 584.77). Nếu bỏ lực đẩy áp suất chỉ còn {N(1.02*570-u25,1)}.',
         f'u = Ma·√(γRTa) = 0.8×√(1.4×287×223.3) = {N(u25,1)} m/s. T/ṁa = [(1+f)ue − u] + (Pe − Pa)·Ae/ṁa = (1.02×570 − {N(u25,1)}) + 0.006×(0.67 − 0.265)×10⁵ = {N(1.02*570-u25,1)} + {N(.006*(.67e5-.265e5),0)} = {N(st25,2)} N·s/kg (book: 584.77). Dropping the pressure thrust leaves only {N(1.02*570-u25,1)}.'),
       3, T_THR, SRC('El-Sayed Ch.2 Example 2.5 (tr.94)', 'El-Sayed Ch.2 Example 2.5 (p.94)'), 'printed answer 584.77 + script (ex25)')
    mc(B('Với số liệu của Ví dụ 2.5 (T/ṁa = 584.77 N·s/kg, u = 239.6 m/s, ue = 570 m/s, f = 0.02), hiệu suất đẩy theo biểu thức thứ nhất (công đẩy chia công đẩy cộng tổn thất vệt khí xả) là:',
          'With the data of Example 2.5 (T/ṁa = 584.77 N·s/kg, u = 239.6 m/s, ue = 570 m/s, f = 0.02), the propulsive efficiency by the first expression (thrust power over thrust power plus wake loss) is:'),
       e25*100, [e25b*100, e25c*100, 100*2*u25/(2*u25+(570-u25))], '%', 1,
       B(f'η_p = 2(T/ṁ)u/[2(T/ṁ)u + (1+f)(ue − u)²] = {N(e25*100,2)} %. Biểu thức thứ hai cho {N(e25b*100,1)} % (> 100 %: vô lý vì vòi phun nghẹt, Pe ≠ Pa), biểu thức thứ ba 2u/(u+ue) chỉ ước lượng thô {N(e25c*100,2)} %.',
         f'η_p = 2(T/ṁ)u/[2(T/ṁ)u + (1+f)(ue − u)²] = {N(e25*100,2)} %. The second expression gives {N(e25b*100,1)} % (> 100 %: unphysical because the nozzle is choked, Pe ≠ Pa); the third, 2u/(u+ue), is only a rough {N(e25c*100,2)} %.'),
       2, T_EFF, SRC('El-Sayed Ch.2 Example 2.5 (tr.95)', 'El-Sayed Ch.2 Example 2.5 (p.95)'), 'printed answer 71.56 % + script (ex25)')
    # ----- Example 2.6 turbofan thrust (our recomputation with unrounded data)
    u26 = .9*math.sqrt(1.4*287*(273.15-50.4)); mh26 = 22.7; mc26 = 68.1; f26 = .015
    T26 = mh26*((1+f26)*452-u26) + mc26*(339.7-u26) + .229*(32.56-26.2)*1e3 + .299*(55.26-26.2)*1e3
    wk = .5*(mh26*(1+f26)*(452-u26)**2 + mc26*(339.7-u26)**2); e26 = T26*u26/(T26*u26+wk)
    reg('ex26', {}, dict(u=u26, T=T26, ep=e26))
    mc(B('Turbofan bay Ma 0.9 ở 33 000 ft (Ta = −50.4 °C, Pa = 26.2 kPa), BPR = 3, dòng lõi 22.7 kg/s, f = 0.015. Vòi lạnh: Pec = 55.26 kPa, uec = 339.7 m/s, Aec = 0.299 m². Vòi nóng: Peh = 32.56 kPa, ueh = 452 m/s, Aeh = 0.229 m². Lực đẩy của động cơ là:',
          'A turbofan flies at Ma 0.9 at 33,000 ft (Ta = −50.4 °C, Pa = 26.2 kPa), BPR = 3, core flow 22.7 kg/s, f = 0.015. Cold nozzle: Pec = 55.26 kPa, uec = 339.7 m/s, Aec = 0.299 m². Hot nozzle: Peh = 32.56 kPa, ueh = 452 m/s, Aeh = 0.229 m². The engine thrust is:'),
       T26/1e3, [T26/1e3 - (.229*6.36+.299*29.06), (T26 - .299*29.06e3)/1e3, (T26 - (.229*6.36+.299*29.06)*1e3 + .229*32.56e3 + .299*55.26e3)/1e3], 'kN', 2,
       B(f'u = 0.9×√(1.4×287×222.75) = {N(u26,1)} m/s. T = ṁh[(1+f)ueh − u] + ṁc(uec − u) + Aeh(Peh − Pa) + Aec(Pec − Pa) = {N(mh26*((1+f26)*452-u26),0)} + {N(mc26*(339.7-u26),0)} + {N(.229*6.36e3,0)} + {N(.299*29.06e3,0)} = {N(T26,0)} N = {N(T26/1e3,2)} kN (sách in 19.257 kN, chênh do làm tròn). Cả hai vòi đều nghẹt (Pe > Pa) nên có lực đẩy áp suất, ≈ {N((.229*6.36+.299*29.06),2)} kN; dùng Pe thay cho (Pe − Pa) sẽ cho {N((T26 - (.229*6.36+.299*29.06)*1e3 + .229*32.56e3 + .299*55.26e3)/1e3,2)} kN.',
         f'u = 0.9×√(1.4×287×222.75) = {N(u26,1)} m/s. T = ṁh[(1+f)ueh − u] + ṁc(uec − u) + Aeh(Peh − Pa) + Aec(Pec − Pa) = {N(mh26*((1+f26)*452-u26),0)} + {N(mc26*(339.7-u26),0)} + {N(.229*6.36e3,0)} + {N(.299*29.06e3,0)} = {N(T26,0)} N = {N(T26/1e3,2)} kN (the book prints 19.257 kN, rounding). Both nozzles are choked (Pe > Pa), so there is a pressure thrust of ≈ {N((.229*6.36+.299*29.06),2)} kN; using Pe instead of (Pe − Pa) would give {N((T26 - (.229*6.36+.299*29.06)*1e3 + .229*32.56e3 + .299*55.26e3)/1e3,2)} kN.'),
       3, T_THR, SRC('El-Sayed Ch.2 Example 2.6 (tr.95–96)', 'El-Sayed Ch.2 Example 2.6 (pp.95–96)'), 'printed answer 19.257 kN + script (ex26)')
    # ----- Example 2.7 CF6 (printed answers 413, 510, 71.2, 25.46, 17.93)
    U7 = .8*math.sqrt(1.4*287*223.2); m7 = 125; beta = 5; mc7 = m7*beta/(beta+1); mh7 = m7/(beta+1); f7 = .75/mh7
    uec7 = 18000/mc7 + U7; ueh7 = (6000/mh7 + U7)/(1+f7)
    ke7 = .5*(mh7*((1+f7)*ueh7**2 - U7**2) + mc7*(uec7**2 - U7**2)); e_p7 = 24000*U7/ke7; e_th7 = ke7/(.75*42.8e6); e_o7 = e_p7*e_th7
    reg('ex27', {}, dict(U=U7, uec=uec7, ueh=ueh7, ep=e_p7, eth=e_th7, eo=e_o7, tsfc=.75/24))
    mc(B('Boeing 747 dùng 4 động cơ CF6, mỗi động cơ: lực đẩy 24.0 kN, lưu lượng khí 125 kg/s, BPR 5.0, nhiên liệu 0.75 kg/s, Ma 0.8, độ cao 10 km (Ta = 223.2 K), nhiệt trị 42 800 kJ/kg. Quạt cho 75 % lực đẩy; các vòi giãn nở hoàn toàn. Vận tốc ra khỏi vòi quạt (dòng lạnh) là:',
          'The Boeing 747 has four CF6 turbofans, each with thrust 24.0 kN, air flow 125 kg/s, BPR 5.0, fuel flow 0.75 kg/s, Ma 0.8, altitude 10 km (Ta = 223.2 K), heating value 42,800 kJ/kg. The fan gives 75 % of the thrust; the nozzles expand fully. The fan (cold) exit velocity is:'),
       uec7, [uec7 - U7, 18000/mh7 + U7, U7 + 24000/m7], 'm/s', 0,
       B(f'U = 0.8×√(1.4×287×223.2) = {N(U7,1)} m/s. ṁc = 5/6×125 = {N(mc7,1)} kg/s. T_fan = 0.75×24 = 18 kN = ṁc(uec − U) ⇒ uec = 18 000/{N(mc7,1)} + {N(U7,1)} = {N(uec7,0)} m/s (sách: 413). Lỗi hay gặp: chia cho dòng lõi hay cho dòng tổng.',
         f'U = 0.8×√(1.4×287×223.2) = {N(U7,1)} m/s. ṁc = 5/6×125 = {N(mc7,1)} kg/s. T_fan = 0.75×24 = 18 kN = ṁc(uec − U) ⇒ uec = 18,000/{N(mc7,1)} + {N(U7,1)} = {N(uec7,0)} m/s (book: 413). Typical slips: dividing by the core flow or by the total flow.'),
       2, T_THR, SRC('El-Sayed Ch.2 Example 2.7 (tr.99–100)', 'El-Sayed Ch.2 Example 2.7 (pp.99–100)'), 'printed answer 413 m/s + script (ex27)')
    mc(B('Với động cơ CF6 trên (Ví dụ 2.7; uec ≈ 413 m/s, ueh ≈ 510 m/s, U ≈ 240 m/s, ṁh = 20.8 kg/s, ṁc = 104.2 kg/s), hiệu suất đẩy là:',
          'For the CF6 engine above (Example 2.7; uec ≈ 413 m/s, ueh ≈ 510 m/s, U ≈ 240 m/s, ṁh = 20.8 kg/s, ṁc = 104.2 kg/s), the propulsive efficiency is:'),
       e_p7*100, [e_th7*100, 2*U7/(U7+ueh7)*100, 100*2*U7/(U7+uec7)], '%', 1,
       B(f'η_p = F·U/[F·U + ½(ṁeh(ueh − U)² + ṁc(uec − U)²)] = ΔK̇E-cơ sở: F·U = {N(24000*U7/1e6,2)} MW, công cấp cho dòng khí ΔK̇E = {N(ke7/1e6,2)} MW ⇒ η_p = {N(e_p7*100,1)} % (sách 71.2 %). Lấy 2U/(U + ueh) = {N(2*U7/(U7+ueh7)*100,1)} % là nhầm công thức một dòng cho turbofan; η_th = {N(e_th7*100,2)} % là hiệu suất nhiệt, không phải η_p.',
         f'η_p = F·U/ΔK̇E with F·U = {N(24000*U7/1e6,2)} MW and the power imparted to the airflow ΔK̇E = {N(ke7/1e6,2)} MW ⇒ η_p = {N(e_p7*100,1)} % (book 71.2 %). Taking 2U/(U + ueh) = {N(2*U7/(U7+ueh7)*100,1)} % wrongly applies the single-stream formula to a turbofan; η_th = {N(e_th7*100,2)} % is the thermal efficiency, not η_p.'),
       3, T_EFF, SRC('El-Sayed Ch.2 Example 2.7 (tr.100)', 'El-Sayed Ch.2 Example 2.7 (p.100)'), 'printed answer 71.2 % + script (ex27)')
    mc(B('Cũng với động cơ CF6 (Ví dụ 2.7), hiệu suất tổng η_o = η_p·η_th bằng:',
          'Also for the CF6 engine (Example 2.7), the overall efficiency η_o = η_p·η_th is:'),
       e_o7*100, [e_th7*100, e_p7*100, (e_o7+e_th7)*50], '%', 1,
       B(f'η_th = ΔK̇E/(ṁf·QR) = {N(ke7/1e6,2)}/{N(.75*42.8,1)} = {N(e_th7*100,2)} %; η_o = {N(e_p7*100,1)} % × {N(e_th7*100,2)} % = {N(e_o7*100,2)} % (sách 17.93 %). Kiểm: η_o = F·U/(ṁf·QR) = {N(24000*U7/(.75*42.8e6)*100,2)} %.',
         f'η_th = ΔK̇E/(ṁf·QR) = {N(ke7/1e6,2)}/{N(.75*42.8,1)} = {N(e_th7*100,2)} %; η_o = {N(e_p7*100,1)} % × {N(e_th7*100,2)} % = {N(e_o7*100,2)} % (book 17.93 %). Check: η_o = F·U/(ṁf·QR) = {N(24000*U7/(.75*42.8e6)*100,2)} %.'),
       3, T_EFF, SRC('El-Sayed Ch.2 Example 2.7 (tr.101)', 'El-Sayed Ch.2 Example 2.7 (p.101)'), 'printed answer 17.93 % + script (ex27)')
    # ----- Example 2.9 range
    S29 = breguet(.35, 45e6, 17, 1/.673, 9.8)
    reg('ex29', {}, dict(S=S29))
    mc(B('Boeing 747 có L/D = 17, nhiệt trị 45 000 kJ/kg, tỉ số khối lượng cuối/đầu chặng bay là 0.673, hiệu suất tổng 0.35. Tầm bay theo phương trình Breguet (g = 9.8 m/s²) là:',
          'A Boeing 747 has L/D = 17, fuel heating value 45,000 kJ/kg, a weight ratio at the end/start of cruise of 0.673 and overall efficiency 0.35. The Breguet range (g = 9.8 m/s²) is:'),
       S29/1e3, [S29/1e3*math.log(1/.673)/(1-.673), S29/1e3/math.log(1/.673), S29/1e3*9.8/9.81*0.35], 'km', 0,
       B(f'S = η_o·QR/g·(L/D)·ln(m1/m2) = 0.35×45×10⁶/9.8×17×ln(1/0.673) = {N(S29/1e3,0)} km (sách 10 819 km, làm tròn ln = 0.396). Lỗi hay gặp: dùng (1 − 0.673) thay cho ln(1/0.673) hoặc quên nhân L/D.',
         f'S = η_o·QR/g·(L/D)·ln(m1/m2) = 0.35×45×10⁶/9.8×17×ln(1/0.673) = {N(S29/1e3,0)} km (book 10,819 km, ln rounded to 0.396). Typical slips: using (1 − 0.673) instead of ln(1/0.673) or forgetting L/D.'),
       2, T_RNG, SRC('El-Sayed Ch.2 Example 2.9 (tr.107)', 'El-Sayed Ch.2 Example 2.9 (p.107)'), 'printed answer 10,819 km + script (ex29)')
    # ----- Example 2.11 wind
    def fuel_wind(Vg): L_ = 4000e3*9.8*(.08/3600)/(Vg*10); return 50000*(1-math.exp(-L_)), L_
    ft, lt = fuel_wind(300); fh, lh = fuel_wind(200)
    reg('ex211', {}, dict(ft=ft, fh=fh))
    mc(B('Máy bay bay 4000 km, tốc độ không khí 250 m/s, L/D = 10, TSFC = 0.08 kg/N/h, m1 = 50 000 kg. Với gió xuôi 50 m/s (Vg = 300 m/s), lượng nhiên liệu tiêu thụ là:',
          'An aircraft flies 4000 km at an airspeed of 250 m/s, L/D = 10, TSFC = 0.08 kg/N/h, m1 = 50,000 kg. With a 50 m/s tail wind (Vg = 300 m/s) the fuel consumed is:'),
       ft, [fh, 50000*(1-math.exp(-4000e3*9.8*(.08/3600)/(250*10))), ft*300/250], 'kg', 0,
       B(f'ln(m1/m2) = S·g·TSFC/(Vg·L/D) = 4×10⁶×9.8×(0.08/3600)/(300×10) = {N(lt,4)} ⇒ m1/m2 = {N(math.exp(lt),4)}; nhiên liệu = m1(1 − m2/m1) = {N(ft,0)} kg (sách ≈ 12 600). Gió ngược 50 m/s (Vg = 200 m/s) cho {N(fh,0)} kg (sách 17 654): gió ngược làm tăng lượng nhiên liệu cho cùng quãng đường.',
         f'ln(m1/m2) = S·g·TSFC/(Vg·L/D) = 4×10⁶×9.8×(0.08/3600)/(300×10) = {N(lt,4)} ⇒ m1/m2 = {N(math.exp(lt),4)}; fuel = m1(1 − m2/m1) = {N(ft,0)} kg (book ≈ 12,600). A 50 m/s head wind (Vg = 200 m/s) gives {N(fh,0)} kg (book 17,654): a head wind raises the fuel needed for the same distance.'),
       3, T_RNG, SRC('El-Sayed Ch.2 Example 2.11 (tr.110–112)', 'El-Sayed Ch.2 Example 2.11 (pp.110–112)'), 'printed answers 12,600 / 17,654 kg + script (ex211)')
    # ----- Problem 2.4 reverse thrust
    Trev = 40*(1.025*500 + 80)
    reg('p24', {}, dict(Trev=Trev))
    mc(B('Sau khi chạm bánh, phi công dùng đảo chiều lực đẩy. Động cơ hút 40 kg/s không khí, f = 2.5 %, tốc độ máy bay 80 m/s, vận tốc khí xả 500 m/s, áp suất xả bằng áp suất môi trường. Giả thiết dòng phụt hoàn toàn quay ngược về phía trước. Độ lớn lực đẩy ngược là:',
          'After touchdown the pilot applies thrust reverse. Air is sucked into the engine at 40 kg/s, f = 2.5 %, aircraft speed 80 m/s, exhaust gas speed 500 m/s, exhaust pressure equal to ambient. Assume the jet is turned fully forward. The magnitude of the reverse thrust is:'),
       Trev, [40*(1.025*500 - 80), 40*1.025*500, 40*(500+80)], 'N', 0,
       B(f'Giả thiết của site (đề không nêu góc đảo): đảo hoàn toàn 180°, nên T = ṁa[(1+f)(−ue) − u]. Độ lớn = 40×(1.025×500 + 80) = {N(Trev,0)} N: cả hai thành phần cùng hướng hãm (động lượng của dòng phụt đảo chiều và lực cản ram). Nếu trừ vận tốc bay như lực đẩy tiến sẽ ra {N(40*(1.025*500-80),0)} N (sai dấu).',
         f'Site assumption (the problem gives no reverser angle): full 180° reversal, so T = ṁa[(1+f)(−ue) − u]. Magnitude = 40×(1.025×500 + 80) = {N(Trev,0)} N: both terms brake (reversed jet momentum and ram drag). Subtracting the flight speed as for forward thrust gives {N(40*(1.025*500-80),0)} N (wrong sign).'),
       2, T_THR, SRC('El-Sayed Ch.2 Problem 2.4 (giả thiết đảo 180°)', 'El-Sayed Ch.2 Problem 2.4 (180° reversal assumed)'), 'script (p24); no printed answer')
    # ----- Problem 2.28
    a28 = (560-475)/20*0.44704; d28 = (475+560)/2*0.44704*20
    reg('p228', {}, dict(a=a28, d=d28))
    mc(B('Trước khi bật bộ đốt sau, máy bay bay ở 475 mph; 20 giây sau khi bật, bay ở 560 mph. Gia tốc trung bình trong 20 giây (m/s²) là: (1 mph = 0.44704 m/s)',
          'Before the afterburners are turned on, an airplane is traveling at 475 mph. Twenty seconds after, it is traveling at 560 mph. The average acceleration over those 20 s (m/s²) is: (1 mph = 0.44704 m/s)'),
       a28, [(560-475)/20, a28*2, 560*0.44704/20], 'm/s²', 3,
       B(f'Δv = 85 mph = 85×0.44704 = {N(85*.44704,3)} m/s; a = Δv/Δt = {N(a28,3)} m/s². Quên đổi mph sang m/s cho {N(85/20,2)}; chia nhầm cho vận tốc cuối cho {N(560*.44704/20,2)}.',
         f'Δv = 85 mph = 85×0.44704 = {N(85*.44704,3)} m/s; a = Δv/Δt = {N(a28,3)} m/s². Forgetting the mph → m/s conversion gives {N(85/20,2)}; using the final speed instead of Δv gives {N(560*.44704/20,2)}.'),
       1, T_THR, SRC('El-Sayed Ch.2 Problem 2.28(1)', 'El-Sayed Ch.2 Problem 2.28(1)'), 'script (p228)')
    mc(B('Cùng bài toán (475 → 560 mph trong 20 s, gia tốc không đổi), quãng đường máy bay đi được trong 20 s là:',
          'Same problem (475 → 560 mph in 20 s, constant acceleration): the distance the plane travels in those 20 s is:'),
       d28, [560*.44704*20, 475*.44704*20, d28/2], 'm', 0,
       B(f'Gia tốc không đổi ⇒ vận tốc trung bình = (475 + 560)/2 = 517.5 mph = {N(517.5*.44704,2)} m/s; s = v_tb·t = {N(d28,0)} m ≈ {N(d28/1609.344,2)} dặm. Dùng vận tốc cuối (560 mph) cho {N(560*.44704*20,0)} m, vận tốc đầu cho {N(475*.44704*20,0)} m.',
         f'Constant acceleration ⇒ mean speed = (475 + 560)/2 = 517.5 mph = {N(517.5*.44704,2)} m/s; s = v_mean·t = {N(d28,0)} m ≈ {N(d28/1609.344,2)} mi. Using the final speed (560 mph) gives {N(560*.44704*20,0)} m, the initial speed {N(475*.44704*20,0)} m.'),
       1, T_THR, SRC('El-Sayed Ch.2 Problem 2.28(2)', 'El-Sayed Ch.2 Problem 2.28(2)'), 'script (p228)')
    # ----- Farokhi Ch.1
    mc(B('Farokhi Problem 1.1. Hiệu suất nhiệt của chu trình Carnot giữa T1 = 288 K và T2 = 2000 K là:', 'Farokhi Problem 1.1. The thermal efficiency of a Carnot cycle between T1 = 288 K and T2 = 2000 K is:'),
       (1-288/2000)*100, [288/2000*100, (1-288/864)*100, (1-math.sqrt(288/2000))*100], '%', 1,
       B('η = 1 − T1/T2 = 1 − 288/2000 = 85.6 %. Nhầm cho T1/T2 = 14.4 % (đó là phần nhiệt thải); dùng T2 = 864 K (nhiệt độ cuối nén Brayton) cho 66.7 %.',
         'η = 1 − T1/T2 = 1 − 288/2000 = 85.6 %. Using T1/T2 = 14.4 % is the heat rejected fraction; using T2 = 864 K (end of Brayton compression) gives 66.7 %.'),
       1, T_THM, SRC('Farokhi Ch.1 Problem 1.1', 'Farokhi Ch.1 Problem 1.1'), 'script (f1x)')
    mc(B('Farokhi Problem 1.2. Chu trình Brayton lý tưởng có T1 = 288 K, T2 = 864 K (T3 không ảnh hưởng đến hiệu suất). Hiệu suất nhiệt là:',
          'Farokhi Problem 1.2. An ideal Brayton cycle has T1 = 288 K and T2 = 864 K (T3 has no effect on efficiency). The thermal efficiency is:'),
       (1-288/864)*100, [(1-288/2000)*100, (1-864/2000)*100, 288/864*100], '%', 1,
       B('η = 1 − T1/T2 = 1 − 288/864 = 66.67 %, tương đương 1 − r_p^(−(γ−1)/γ) với r_p^((γ−1)/γ) = 3 (r_p = 46.8). Lấy T3 vào công thức là sai.',
         'η = 1 − T1/T2 = 1 − 288/864 = 66.67 %, equivalent to 1 − r_p^(−(γ−1)/γ) with r_p^((γ−1)/γ) = 3 (r_p = 46.8). Putting T3 into the formula is wrong.'),
       1, T_THM, SRC('Farokhi Ch.1 Problem 1.2', 'Farokhi Ch.1 Problem 1.2'), 'script (f1x)')
    r_ = 2000/864; hum = 1-1.4*(288/864)*(r_**(1/1.4)-1)/(r_-1)
    mc(B('Farokhi Problem 1.3. Chu trình Humphrey (cháy đẳng tích) với T1 = 288 K, T2 = 864 K, T3 = 2000 K, γ = 1.4, η = 1 − γ(T1/T2)[(T3/T2)^(1/γ) − 1]/[(T3/T2) − 1]. So với Brayton 66.67 % cùng T1, T2, hiệu suất Humphrey là:',
          'Farokhi Problem 1.3. The Humphrey (constant-volume combustion) cycle with T1 = 288 K, T2 = 864 K, T3 = 2000 K, γ = 1.4, η = 1 − γ(T1/T2)[(T3/T2)^(1/γ) − 1]/[(T3/T2) − 1]. Compared with Brayton (66.67 %) at the same T1 and T2, the Humphrey efficiency is:'),
       hum*100, [(1-288/864)*100, (1-288/2000)*100, (1-1.4*(288/864)*(r_**(1.4)-1)/(r_-1))*100], '%', 2,
       B(f'T3/T2 = {N(r_,4)}; (T3/T2)^(1/γ) = {N(r_**(1/1.4),4)}; η = 1 − 1.4×0.3333×{N(r_**(1/1.4)-1,4)}/{N(r_-1,4)} = {N(hum*100,2)} %, cao hơn Brayton 66.67 % và thấp hơn Carnot 85.6 %. Lỗi: dùng mũ γ thay cho 1/γ.',
         f'T3/T2 = {N(r_,4)}; (T3/T2)^(1/γ) = {N(r_**(1/1.4),4)}; η = 1 − 1.4×0.3333×{N(r_**(1/1.4)-1,4)}/{N(r_-1,4)} = {N(hum*100,2)} %, above Brayton 66.67 % and below Carnot 85.6 %. Slip: using exponent γ instead of 1/γ.'),
       2, T_THM, SRC('Farokhi Ch.1 Problem 1.3', 'Farokhi Ch.1 Problem 1.3'), 'script (f1x), Humphrey recomputed from cv/cp heat balance')
    rpm = 340/1e-3*60/(2*math.pi)
    reg('f14', {}, dict(rpm=rpm))
    mc(B('Farokhi Problem 1.4. Rôto của động cơ tuabin khí cỡ milimét có bán kính 1 mm, cần tốc độ đỉnh cánh gần bằng tốc độ âm (340 m/s). Tốc độ quay là:',
          'Farokhi Problem 1.4. The rotor of a millimetre-scale gas turbine has a radius of 1 mm and must reach a tip speed near the speed of sound (340 m/s). The rotational speed is:'),
       rpm/1e6, [340/1e-3/1e6, rpm/1e6/2, rpm/1e6*2*math.pi], '×10⁶ vòng/phút' if False else '×10⁶ rpm', 3,
       B(f'ω = V/r = 340/0.001 = 340 000 rad/s; n = ω·60/(2π) = {N(rpm,0)} vòng/phút = {N(rpm/1e6,3)}×10⁶ rpm. Nhầm đơn vị rad/s với vòng/phút cho 0.34×10⁶; quên chia 2π cho {N(rpm/1e6*2*math.pi,2)}×10⁶.',
         f'ω = V/r = 340/0.001 = 340,000 rad/s; n = ω·60/(2π) = {N(rpm,0)} rpm = {N(rpm/1e6,3)}×10⁶ rpm. Confusing rad/s with rpm gives 0.34×10⁶; forgetting 2π gives {N(rpm/1e6*2*math.pi,2)}×10⁶.'),
       1, T_THM, SRC('Farokhi Ch.1 Problem 1.4', 'Farokhi Ch.1 Problem 1.4'), 'script (f14)')
    # ----- Farokhi examples 3.3, 3.4, 3.5, 3.6
    pt3 = (200-100)*1e3*math.pi
    mc(B('Farokhi Example 3.3. Tên lửa nhiên liệu lỏng tiêu thụ 200 kg/s chất oxy hoá và 50 kg/s nhiên liệu; khí tăng tốc trong vòi phun đến V9 = 4000 m/s, p9 = 200 kPa ở mực nước biển (p0 = 100 kPa), đường kính cửa ra 2 m. Lực đẩy tổng (gross) của tên lửa là:',
          'Farokhi Example 3.3. A liquid-propellant rocket consumes 200 kg/s of oxidiser and 50 kg/s of fuel; the gas leaves the nozzle at V9 = 4000 m/s and p9 = 200 kPa at sea level (p0 = 100 kPa) with an exit diameter of 2 m. The rocket gross thrust is:'),
       (1e6+pt3)/1e3, [1e6/1e3, pt3/1e3, (1e6+200e3*math.pi)/1e3], 'kN', 0,
       B(f'Lực đẩy động lượng = ṁ·V9 = 250×4000 = 1000 kN; lực đẩy áp suất = (p9 − p0)·A9 = 100 kPa×π×2²/4 = {N(pt3/1e3,2)} kN; Fg = {N((1e6+pt3)/1e3,0)} kN (sách 1314 kN). Thiếu lực đẩy áp suất cho 1000 kN; dùng p9 thay cho (p9 − p0) cho {N((1e6+200e3*math.pi)/1e3,0)} kN.',
         f'Momentum thrust = ṁ·V9 = 250×4000 = 1000 kN; pressure thrust = (p9 − p0)·A9 = 100 kPa×π×2²/4 = {N(pt3/1e3,2)} kN; Fg = {N((1e6+pt3)/1e3,0)} kN (book 1314 kN). Omitting the pressure thrust gives 1000 kN; using p9 instead of (p9 − p0) gives {N((1e6+200e3*math.pi)/1e3,0)} kN.'),
       1, T_THR, SRC('Farokhi Ch.3 Example 3.3 (tr.129)', 'Farokhi Ch.3 Example 3.3 (p.129)'), 'printed answer 1314 kN + script (f33)')
    eth34 = 102*900**2/(2*2*42000e3); Fn34 = 102*900
    mc(B('Farokhi Example 3.4. Turbojet cất cánh (V0 ≈ 0): ṁ0 = 100 kg/s, ṁf = 2 kg/s, QR = 42 000 kJ/kg, V9 = 900 m/s. Hiệu suất nhiệt η_th = (ṁ0 + ṁf)V9²/(2ṁf·QR) bằng:',
          'Farokhi Example 3.4. A turbojet at takeoff (V0 ≈ 0): ṁ0 = 100 kg/s, ṁf = 2 kg/s, QR = 42,000 kJ/kg, V9 = 900 m/s. The thermal efficiency η_th = (ṁ0 + ṁf)V9²/(2ṁf·QR) is:'),
       eth34*100, [100*900**2/(2*2*42000e3)*100, eth34*50, 102*900/(2*42000e3/1e3)], '%', 1,
       B(f'η_th = 102×900²/(2×2×42 000×10³) = {N(eth34*100,1)} % (sách 49.2 %), nghĩa là ~51 % năng lượng nhiên liệu còn nằm trong khí xả. Lực đẩy lúc cất cánh F ≈ ṁ9·V9 = 102×900 = {N(Fn34/1e3,1)} kN. Lỗi: dùng ṁ0 thay cho ṁ0 + ṁf, quên hệ số 2.',
         f'η_th = 102×900²/(2×2×42,000×10³) = {N(eth34*100,1)} % (book 49.2 %), i.e. ~51 % of the fuel energy stays in the exhaust. Takeoff thrust F ≈ ṁ9·V9 = 102×900 = {N(Fn34/1e3,1)} kN. Slips: using ṁ0 instead of ṁ0 + ṁf, forgetting the factor 2.'),
       1, T_EFF, SRC('Farokhi Ch.3 Example 3.4 (tr.132)', 'Farokhi Ch.3 Example 3.4 (p.132)'), 'printed answer 49.2 % + script (f34)')
    mc(B('Farokhi Example 3.5. Turbojet bay 200 m/s, vận tốc khí xả 900 m/s. Ước lượng hiệu suất đẩy bằng η_p ≈ 2/(1 + V9/V0):',
          'Farokhi Example 3.5. A turbojet flies at 200 m/s and the exhaust velocity is 900 m/s. Estimate the propulsive efficiency by η_p ≈ 2/(1 + V9/V0):'),
       2/(1+900/200)*100, [2*200/900*100, 200/900*100, 2/(900/200)*100*1.0 + 0.0], '%', 1,
       B('V9/V0 = 4.5; η_p = 2/(1 + 4.5) = 36.36 % (sách ghi 36.3 %: cắt bớt, không làm tròn). Thấp vì tốc độ phụt vượt xa tốc độ bay.',
         'V9/V0 = 4.5; η_p = 2/(1 + 4.5) = 36.36 % (the book prints 36.3 %: truncated, not rounded). Low because the jet speed far exceeds the flight speed.'),
       1, T_EFF, SRC('Farokhi Ch.3 Example 3.5 (tr.136)', 'Farokhi Ch.3 Example 3.5 (p.136)'), 'printed answer 36.3 % + script')
    Q.append(mcq(B('Farokhi Example 3.6. Turbofan bay 200 m/s, vận tốc phụt cả hai vòi 250 m/s. Hiệu suất đẩy ước lượng 2/(1 + V9/V0) là:',
                    'Farokhi Example 3.6. A turbofan flies at 200 m/s with a 250 m/s exhaust speed in both nozzles. The propulsive efficiency estimated by 2/(1 + V9/V0) is:'),
                 numopts(88.89, [100*250/200/(1+250/200), 36.36, 100*200/250], '%', 2), 0,
                 B('η_p = 2/(1 + 1.25) = 88.89 % (sách 88.9 %). So với turbojet 36.36 %, tăng 52.5 điểm phần trăm; sách ghi "52.6 % increase" nhưng tăng tương đối thực là 144 %. Quên hệ số 2 ở tử số cho 55.6 %; lấy V0/V9 cho 80 %.',
                   'η_p = 2/(1 + 1.25) = 88.89 % (book 88.9 %). Against the turbojet 36.36 % that is +52.5 percentage points; the book says "52.6 % increase" but the true relative rise is 144 %. Forgetting the factor 2 in the numerator gives 55.6 %; taking V0/V9 gives 80 %.'),
                 1, T_EFF, SRC('Farokhi Ch.3 Example 3.6 (tr.136)', 'Farokhi Ch.3 Example 3.6 (p.136)'), 'goc', 'printed answer 88.9 % + script'))
    # ----- Farokhi Problems 3.7, 3.8, 3.13, 3.17
    p1 = 100e3 + .5*1*(10**2-100**2)
    mc(B('Farokhi Problem 3.7. Ống dòng hút khí của động cơ lúc cất cánh: tốc độ 10 m/s ở diện tích A0 và 100 m/s ở A1; p0 = 100 kPa, ρ0 = 1 kg/m³. Dùng phương trình Bernoulli (dòng không nén được), tỉ số p1/p0 là:',
          'Farokhi Problem 3.7. The capture streamtube of an engine at takeoff: speed 10 m/s at area A0 and 100 m/s at A1; p0 = 100 kPa, ρ0 = 1 kg/m³. Using the Bernoulli equation (incompressible flow), the ratio p1/p0 is:'),
       p1/100e3, [100e3/p1, (100e3-.5*1*10**2)/100e3, 1-.5*(100**2)/100e3*2], '', 4,
       B(f'p1 = p0 + ½ρ(V0² − V1²) = 100 000 + 0.5×1×(10² − 100²) = {N(p1,0)} Pa ⇒ p1/p0 = {N(p1/100e3,4)}. (Tỉ số diện tích bắt dòng A0/A1 = V1/V0 = 10 theo liên tục.) Đảo dấu cho {N(100e3/p1,4)}.',
         f'p1 = p0 + ½ρ(V0² − V1²) = 100,000 + 0.5×1×(10² − 100²) = {N(p1,0)} Pa ⇒ p1/p0 = {N(p1/100e3,4)}. (The capture area ratio A0/A1 = V1/V0 = 10 by continuity.) Reversing the sign gives {N(100e3/p1,4)}.'),
       1, T_THR, SRC('Farokhi Ch.3 Problem 3.7(b)', 'Farokhi Ch.3 Problem 3.7(b)'), 'script (analytic)')
    mc(B('Farokhi Problem 3.8. Động cơ tên lửa đốt 50 kg/s thuốc phóng, vận tốc phụt 3500 m/s, vòi phun giãn nở hoàn toàn. Xung riêng Is (s) là:',
          'Farokhi Problem 3.8. A rocket motor burns propellant at 50 kg/s with an exhaust speed of 3500 m/s, the nozzle perfectly expanded. The specific impulse Is (s) is:'),
       3500/G0, [3500/9.0, 3500*50/G0/1e3, 3500/G0/50], 's', 1,
       B(f'F = ṁp·V9 = 50×3500 = 175 kN; Is = F/(ṁp·g0) = V9/g0 = 3500/9.80665 = {N(3500/G0,1)} s (với g0 = 9.8: 357,1 s). Is có đơn vị giây, không phải m/s; chia cho 9 hoặc quên g0 đều sai.',
         f'F = ṁp·V9 = 50×3500 = 175 kN; Is = F/(ṁp·g0) = V9/g0 = 3500/9.80665 = {N(3500/G0,1)} s (with g0 = 9.8: 357.1 s). Is is in seconds, not m/s.'),
       1, T_SFC, SRC('Farokhi Ch.3 Problem 3.8', 'Farokhi Ch.3 Problem 3.8'), 'script (analytic)')
    mc(B('Farokhi Problem 3.13. Động cơ turboshaft đốt 1 kg/s nhiên liệu nhiệt trị 42 000 kJ/kg, hiệu suất nhiệt 0.333. Công suất trục là:',
          'Farokhi Problem 3.13. A turboshaft engine burns fuel of heating value 42,000 kJ/kg at 1 kg/s with a thermal efficiency of 0.333. The shaft power is:'),
       .333*42e3, [42e3, .333*42e3*1e3, 42e3/.333], 'kW', 0,
       B('℘s = η_th·ṁf·QR = 0.333×1×42 000 kJ/s = 13 986 kW ≈ 14 MW. Với turboshaft, hiệu suất nhiệt định nghĩa theo công suất trục (El-Sayed Eq. 2.17), không phải động năng dòng khí.',
         '℘s = η_th·ṁf·QR = 0.333×1×42,000 kJ/s = 13,986 kW ≈ 14 MW. For a turboshaft the thermal efficiency is defined on shaft power (El-Sayed Eq. 2.17), not on jet kinetic energy.'),
       1, T_EFF, SRC('Farokhi Ch.3 Problem 3.13', 'Farokhi Ch.3 Problem 3.13'), 'script (analytic)')
    fn = lambda M, g=1.33: M*(1+(g-1)/2*M*M)**(-(g+1)/(2*(g-1)))
    A7 = .5*.98*fn(1)/fn(.5)
    reg('f317', {}, dict(A7=A7))
    mc(B('Farokhi Problem 3.17(a). Vòi phun hội tụ giãn nở hoàn toàn: Ma cửa ra M8 = 1.0, áp suất toàn phần cửa ra bằng 98 % cửa vào, Ma cửa vào M7 = 0.5, A8 = 0.5 m², γ = 1.33, dòng đoạn nhiệt. Diện tích cửa vào A7 là:',
          'Farokhi Problem 3.17(a). A convergent nozzle is perfectly expanded with exit Mach number M8 = 1.0, exit total pressure 98 % of the inlet total pressure, inlet Mach number M7 = 0.5, A8 = 0.5 m², γ = 1.33, adiabatic flow. The inlet area A7 is:'),
       A7, [.5*fn(1)/fn(.5), .5*.98*fn(.5)/fn(1), A7*.98], 'm²', 4,
       B(f'Liên tục với Tt không đổi: ṁ ∝ A·pt·f(M), f(M) = M(1 + (γ−1)M²/2)^(−(γ+1)/(2(γ−1))). f(1) = {N(fn(1),4)}, f(0.5) = {N(fn(.5),4)}. A7 = A8·(pt8/pt7)·f(1)/f(0.5) = 0.5×0.98×{N(fn(1),4)}/{N(fn(.5),4)} = {N(A7,4)} m². Bỏ tổn thất áp suất toàn phần cho {N(.5*fn(1)/fn(.5),4)} m².',
         f'Continuity with constant Tt: ṁ ∝ A·pt·f(M), f(M) = M(1 + (γ−1)M²/2)^(−(γ+1)/(2(γ−1))). f(1) = {N(fn(1),4)}, f(0.5) = {N(fn(.5),4)}. A7 = A8·(pt8/pt7)·f(1)/f(0.5) = 0.5×0.98×{N(fn(1),4)}/{N(fn(.5),4)} = {N(A7,4)} m². Ignoring the total-pressure loss gives {N(.5*fn(1)/fn(.5),4)} m².'),
       3, T_THR, SRC('Farokhi Ch.3 Problem 3.17(a)', 'Farokhi Ch.3 Problem 3.17(a)'), 'script (f317); mass-flow function recomputed by sympy-free numeric route')
    return Q
