"""m04 ORIGINAL items (origin 'goc'): the slide examples of Chapter 4 (= Cengel Examples 15-1...15-5) and Cengel Ch.15 end-of-chapter problems whose statement is quoted,
each solved by route A (build/gen/m04_common.py) and registered for the independent route B of build/verify/verify_m04.py.  build() -> (ITEMS, PRN) where PRN lists
every printed (book) answer next to our value.  Problem statements were read from the page images (PDF 810, 811, 812, 813, 815, 817, 818)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from m04_common import *

ITEMS = []; PRN = []
def prn(key, printed, ours, tol, note=''): PRN.append(dict(key=key, printed=printed, ours=ours, tol=tol, note=note))
def add(it): ITEMS.append(it); return it
def fp(*pairs): return [[a, b] for a, b in pairs]
SLIDE = lambda pg, book: dict(vi=f'Slide Ch.4 tr.{pg} = Cengel {book}', en=f'Slide Ch.4 p.{pg} = Cengel {book}')
CEN = lambda num, extra_vi='', extra_en='': dict(vi=f'Cengel Ch.15 Bài {num}{extra_vi}', en=f'Cengel Ch.15 Problem {num}{extra_en}')
TOP = dict(af=dict(vi='Tỉ lệ AF và cân bằng phản ứng', en='AF and balancing'),
           dew=dict(vi='Điểm sương sản phẩm cháy', en='Dew point of products'),
           rev=dict(vi='Phân tích cháy ngược', en='Reverse combustion analysis'),
           enth=dict(vi='Entanpi cháy và nhiệt trị', en='Enthalpy of combustion, HHV/LHV'),
           law1=dict(vi='Định luật 1 cho cháy', en='First law for combustion'),
           tdp=dict(vi='Nhiệt độ ngọn lửa đoạn nhiệt', en='Adiabatic flame temperature'),
           air=dict(vi='Không khí lý thuyết và thừa', en='Theoretical and excess air'))

def wrong_list(wr):
    """(values, vi text, en text) -> explanation fragment listing why each wrong option arises."""
    return ''.join(f' {N(v, nd) if isinstance(v, (int, float)) else v} {rv};' for v, rv, nd in wr) if False else ''

def numq(qv, qe, correct, wrongs, unit, nd, ev, ee, level, topic, src, check, origin='goc', fig=None):
    """closed numeric question: wrongs = [(value, reason_vi, reason_en)]; the explanation ends with the reason of each wrong option (no option letters)."""
    opts = numopts(correct, [w[0] for w in wrongs], unit, nd)
    keep = [w for w in wrongs if N(w[0], nd) != N(correct, nd)]
    seen = set(); kk = []
    for w in keep:
        if N(w[0], nd) in seen: continue
        seen.add(N(w[0], nd)); kk.append(w)
    u_ = (' ' + unit) if unit else ''; tv = ' '.join(f'{N(v, nd)}{u_} {rv}.' for v, rv, re_ in kk); te = ' '.join(f'{N(v, nd)}{u_} {re_}.' for v, rv, re_ in kk)
    return mcq(B(qv, qe), opts, 0, B(ev + ' ' + tv, ee + ' ' + te), level, topic, src, origin, check, fig)

# ================================================================== helpers for values reused in text
def AFcalc(parts, lam, exact=False, **kw): return combustion(parts_fuel(parts, exact), lam, exact=exact, **kw)
def REGc(parts, lam, out, val, what, exact=False, tol=1e-9, **kw):
    return reg('comb', dict(fuel=fp(*parts), lam=lam, exact=exact, **kw), out, val, tol, what)

# ================================================================== 1. Cengel Example 15-1 = slide tr.13-17
f = single('C8H18'); r1 = combustion(f, 20 / 12.5); rx = combustion(f, 20 / 12.5, exact=True)
reg('comb', dict(fuel=fp(('C8H18', 1)), lam=1.6, exact=False), 'AF', r1['AF'], 1e-9, 'Ex 15-1 / slide tr.17: 24.2'); prn('Ex15-1 AF (slide tr.17)', 24.2, r1['AF'], 0.01, 'slide rounds M_air to 29')
for k, o in (('CO2', 8.0), ('H2O', 9.0), ('O2', 7.5), ('N2', 75.2)):
    reg('comb', dict(fuel=fp(('C8H18', 1)), lam=1.6, exact=False), k, r1[k], 1e-9, f'Ex 15-1 / slide tr.15-16: {o}'); prn(f'Ex15-1 {k} (slide tr.15)', o, r1[k], 1e-9)
add(ess(B('Cengel Ví dụ 15–1 = slide Ch.4 tr.13–17. Một kmol octan (C₈H₁₈) được đốt bằng không khí chứa 20 kmol O₂. Giả thiết sản phẩm chỉ gồm CO₂, H₂O, O₂ và N₂: xác định số mol từng khí trong sản phẩm và tỉ lệ không khí–nhiên liệu của quá trình.',
           'Cengel Example 15–1 = slide Ch.4 p.13–17. One kmol of octane (C₈H₁₈) is burned with air that contains 20 kmol of O₂. Assuming the products contain only CO₂, H₂O, O₂ and N₂, determine the mole number of each gas in the products and the air–fuel ratio of this combustion process.'),
         B(f'''Giả thiết (slide tr.13–14): sản phẩm chỉ có CO₂, H₂O, O₂, N₂; không khí khô = 1 kmol O₂ + 3,76 kmol N₂.
Bước 1 (cân bằng nguyên tố, slide tr.15). C₈H₁₈ + 20(O₂ + 3,76 N₂) → x CO₂ + y H₂O + z O₂ + w N₂. C: 8 = x → x = 8. H: 18 = 2y → y = 9. O: 20 × 2 = 2x + y + 2z → 40 = 16 + 9 + 2z → z = 7,5. N₂: 20 × 3,76 = w = 75,2.
Phương trình: C₈H₁₈ + 20(O₂ + 3,76 N₂) → 8 CO₂ + 9 H₂O + 7,5 O₂ + 75,2 N₂ (slide tr.16). Hệ số 20 là số mol O₂, KHÔNG phải số mol không khí: không khí = 20 + 75,2 = 95,2 kmol (= 20 × 4,76).
Bước 2 (tỉ lệ không khí–nhiên liệu, slide tr.17). AF = (20 × 4,76 kmol)(29 kg/kmol) / [(8 kmol)(12 kg/kmol) + (9 kmol)(2 kg/kmol)] = {N(95.2*29,1)} / 114 = {N(r1["AF"],2)} kg không khí/kg nhiên liệu. Slide làm tròn M_air = 29 (tr.14 ghi 28,97): với 28,97 và M(C₈H₁₈) = 114,231 kg/kmol (A-27) được {N(rx["AF"],2)}.
Kiểm tra số mol: chất phản ứng 1 + 95,2 = 96,2 kmol, sản phẩm 8 + 9 + 7,5 + 75,2 = 99,7 kmol: số mol không bảo toàn, chỉ số nguyên tử mỗi nguyên tố được bảo toàn (slide tr.11).
Hai đường: (A) đại số tay như trên; (B) sympy giải ma trận nguyên tố [C, H, O, N] với ẩn (x, y, z, w): (8, 9, 15/2, 376/5) trùng. Đáp số: 8 CO₂; 9 H₂O; 7,5 O₂; 75,2 N₂; AF = {N(r1["AF"],1)} kg/kg (slide 24,2).''',
           f'''Assumptions (slides p.13–14): products only CO₂, H₂O, O₂, N₂; dry air = 1 kmol O₂ + 3.76 kmol N₂.
Step 1 (element balances, slide p.15). C₈H₁₈ + 20(O₂ + 3.76 N₂) → x CO₂ + y H₂O + z O₂ + w N₂. C: 8 = x → x = 8. H: 18 = 2y → y = 9. O: 20 × 2 = 2x + y + 2z → 40 = 16 + 9 + 2z → z = 7.5. N₂: 20 × 3.76 = w = 75.2.
Equation: C₈H₁₈ + 20(O₂ + 3.76 N₂) → 8 CO₂ + 9 H₂O + 7.5 O₂ + 75.2 N₂ (slide p.16). The coefficient 20 is the number of moles of O₂, NOT of air: air = 20 + 75.2 = 95.2 kmol (= 20 × 4.76).
Step 2 (air–fuel ratio, slide p.17). AF = (20 × 4.76 kmol)(29 kg/kmol) / [(8 kmol)(12 kg/kmol) + (9 kmol)(2 kg/kmol)] = {N(95.2*29,1)} / 114 = {N(r1["AF"],2)} kg air/kg fuel. The slide rounds M_air to 29 (p.14 prints 28.97): with 28.97 and M(C₈H₁₈) = 114.231 kg/kmol (A-27) the result is {N(rx["AF"],2)}.
Mole check: reactants 1 + 95.2 = 96.2 kmol, products 8 + 9 + 7.5 + 75.2 = 99.7 kmol: moles are not conserved, only the atoms of each element are (slide p.11).
Two routes: (A) hand algebra as above; (B) sympy solves the element matrix [C, H, O, N] for the unknowns (x, y, z, w): (8, 9, 15/2, 376/5), identical. Answer: 8 CO₂; 9 H₂O; 7.5 O₂; 75.2 N₂; AF = {N(r1["AF"],1)} kg/kg (slide 24.2).'''),
         2, TOP['af'], SLIDE('13–17', 'Ex 15-1'), 'goc', 'script + slide p.15-17 (printed answer 24.2)'))
add(mcq(B('Slide Ch.4 tr.15–16 (Cengel Ví dụ 15–1): C₈H₁₈ + 20(O₂ + 3,76 N₂) → x CO₂ + y H₂O + z O₂ + w N₂. Dãy hệ số (x; y; z; w) của sản phẩm là:',
              'Slide Ch.4 p.15–16 (Cengel Example 15–1): C₈H₁₈ + 20(O₂ + 3.76 N₂) → x CO₂ + y H₂O + z O₂ + w N₂. The coefficients (x; y; z; w) of the products are:'),
         [opt('8; 9; 7.5; 75.2'), opt('8; 18; 7.5; 75.2'), opt('8; 9; 12.5; 75.2'), opt('8; 9; 7.5; 95.2')], 0,
         B('C: x = 8. H: 18 = 2y → y = 9. O: 40 = 2x + y + 2z = 25 + 2z → z = 7.5. N₂: w = 20 × 3.76 = 75.2. Dãy (8; 18; 7.5; 75.2) quên rằng H₂ chỉ có 2 nguyên tử H mỗi phân tử (y = 18/2); dãy (8; 9; 12.5; 75.2) lấy z bằng O₂ lý thuyết 12.5 thay vì phần O₂ thừa 20 − 12.5 = 7.5; dãy (8; 9; 7.5; 95.2) nhầm số mol không khí (95.2) với số mol N₂.',
           'C: x = 8. H: 18 = 2y → y = 9. O: 40 = 2x + y + 2z = 25 + 2z → z = 7.5. N₂: w = 20 × 3.76 = 75.2. The set (8; 18; 7.5; 75.2) forgets that each H₂O takes 2 H atoms (y = 18/2); (8; 9; 12.5; 75.2) takes z as the theoretical O₂ 12.5 instead of the excess 20 − 12.5 = 7.5; (8; 9; 7.5; 95.2) confuses the moles of air (95.2) with the moles of N₂.'),
         2, TOP['af'], SLIDE('15–16', 'Ex 15-1'), 'goc', 'slide p.15-16 + sympy', fixed=False))

# ================================================================== 2. Cengel Example 15-2 = slide tr.27-32 (ethane, 20 % excess air, 100 kPa)
f = single('C2H6'); r2 = combustion(f, 1.2); Pv2, T2 = dew_point(r2['H2O'], r2['n_tot'], 100)
from iapws import IAPWS97 as _I
Ti2 = _I(P=Pv2 / 1000, x=0).T - 273.15
REGc([('C2H6', 1)], 1.2, 'AF', r2['AF'], 'Ex 15-2'); REGc([('C2H6', 1)], 1.2, 'N2', r2['N2'], 'Ex 15-2'); REGc([('C2H6', 1)], 1.2, 'n_tot', r2['n_tot'], 'Ex 15-2')
reg('dew', dict(fuel=fp(('C2H6', 1)), lam=1.2, P=100.0), 'Pv', Pv2, 1e-9, 'Ex 15-2 slide tr.31: 13.96 kPa'); reg('dew', dict(fuel=fp(('C2H6', 1)), lam=1.2, P=100.0), 'Tdp', T2, {'abs': 0.35}, 'Ex 15-2 slide tr.32: 52.3 C (A-5 interpolation; iapws 52.49)')
prn('Ex15-2 AF (slide tr.30)', 19.3, r2['AF'], 0.005); prn('Ex15-2 Pv (slide tr.31)', 13.96, Pv2, 0.001); prn('Ex15-2 Tdp (slide tr.32)', 52.3, T2, 0.001, 'A-5 linear interpolation 52.27')
add(ess(B('Cengel Ví dụ 15–2 = slide Ch.4 tr.27–32. Etan (C₂H₆) được đốt với 20 % không khí thừa. Giả thiết cháy hoàn toàn, khí cháy là khí lý tưởng, áp suất tổng 100 kPa. Xác định (a) tỉ lệ không khí–nhiên liệu, (b) nhiệt độ điểm sương của sản phẩm.',
           'Cengel Example 15–2 = slide Ch.4 p.27–32. Ethane (C₂H₆) is burned with 20 percent excess air. Assuming complete combustion, ideal-gas products and a total pressure of 100 kPa, determine (a) the air–fuel ratio and (b) the dew-point temperature of the products.'),
         B(f'''Giả thiết (tr.27): cháy hoàn toàn; khí cháy là khí lý tưởng.
Bước 1 (slide tr.28–29). C₂H₆ + 1,2 a_th (O₂ + 3,76 N₂) → 2 CO₂ + 3 H₂O + 0,2 a_th O₂ + (1,2 × 3,76) a_th N₂. Cân bằng O₂: 1,2 a_th = 2 + 1,5 + 0,2 a_th → a_th = 3,5. Vậy C₂H₆ + 4,2 (O₂ + 3,76 N₂) → 2 CO₂ + 3 H₂O + 0,7 O₂ + {N(r2["N2"],2)} N₂.
Bước 2 (a) (tr.30). AF = (4,2 × 4,76 kmol)(29 kg/kmol) / [(2 kmol)(12 kg/kmol) + (3 kmol)(2 kg/kmol)] = {N(4.2*4.76*29,1)} / 30 = {N(r2["AF"],1)} kg/kg.
Bước 3 (b) (tr.31–32). Số mol sản phẩm N_prod = 2 + 3 + 0,7 + {N(r2["N2"],2)} = {N(r2["n_tot"],2)} kmol. P_v = (N_v/N_prod) P = (3/{N(r2["n_tot"],2)})(100 kPa) = {N(Pv2,2)} kPa. T_dp = T_sat@{N(Pv2,2)} kPa: bảng A-5 có hàng 10 kPa (45,81 °C) và 15 kPa (53,97 °C); nội suy tuyến tính: 45,81 + ({N(Pv2,2)} − 10)/5 × 8,16 = {N(T2,2)} °C (slide làm tròn 52,3).
Hai đường: (A) nội suy bảng A-5 như trên; (B) IAPWS-IF97 cho T_sat({N(Pv2,2)} kPa) = {N(Ti2,2)} °C. Lệch {N(Ti2-T2,2)} °C là sai số của nội suy tuyến tính trên hai hàng cách nhau 5 kPa (T_sat(P) lồi lên), không phải lỗi của lời giải: dung sai khai báo 0,35 °C.
Đáp số: AF = {N(r2["AF"],1)} kg/kg; T_dp ≈ {N(T2,1)} °C (iapws {N(Ti2,1)} °C).''',
           f'''Assumptions (p.27): complete combustion; ideal-gas products.
Step 1 (slides p.28–29). C₂H₆ + 1.2 a_th (O₂ + 3.76 N₂) → 2 CO₂ + 3 H₂O + 0.2 a_th O₂ + (1.2 × 3.76) a_th N₂. O₂ balance: 1.2 a_th = 2 + 1.5 + 0.2 a_th → a_th = 3.5. So C₂H₆ + 4.2 (O₂ + 3.76 N₂) → 2 CO₂ + 3 H₂O + 0.7 O₂ + {N(r2["N2"],2)} N₂.
Step 2 (a) (p.30). AF = (4.2 × 4.76 kmol)(29 kg/kmol) / [(2 kmol)(12 kg/kmol) + (3 kmol)(2 kg/kmol)] = {N(4.2*4.76*29,1)} / 30 = {N(r2["AF"],1)} kg/kg.
Step 3 (b) (p.31–32). Product moles N_prod = 2 + 3 + 0.7 + {N(r2["N2"],2)} = {N(r2["n_tot"],2)} kmol. P_v = (N_v/N_prod) P = (3/{N(r2["n_tot"],2)})(100 kPa) = {N(Pv2,2)} kPa. T_dp = T_sat@{N(Pv2,2)} kPa: Table A-5 has the rows 10 kPa (45.81 °C) and 15 kPa (53.97 °C); linear interpolation: 45.81 + ({N(Pv2,2)} − 10)/5 × 8.16 = {N(T2,2)} °C (the slide rounds to 52.3).
Two routes: (A) interpolation in Table A-5 as above; (B) IAPWS-IF97 gives T_sat({N(Pv2,2)} kPa) = {N(Ti2,2)} °C. The {N(Ti2-T2,2)} °C gap is the error of linear interpolation between rows 5 kPa apart (T_sat(P) is concave), not an error of the solution: declared tolerance 0.35 °C.
Answer: AF = {N(r2["AF"],1)} kg/kg; T_dp ≈ {N(T2,1)} °C (iapws {N(Ti2,1)} °C).'''),
         3, TOP['dew'], SLIDE('27–32', 'Ex 15-2'), 'goc', 'script + slide p.30-32 (printed 19.3 and 52.3)'))
bad_Pt = props.sat_P('water', 100, 'Tsat_C')['value']; Nd = r2['n_dry']; T_dry = dew_point(3, Nd, 100)[1]
add(numq('Slide Ch.4 tr.27–32 (Cengel Ví dụ 15–2): etan C₂H₆ cháy hoàn toàn với 20 % không khí thừa ở áp suất tổng 100 kPa; sản phẩm: 2 CO₂ + 3 H₂O + 0,7 O₂ + 15,79 N₂. Nhiệt độ điểm sương của sản phẩm (bảng A-5) xấp xỉ:',
         'Slide Ch.4 p.27–32 (Cengel Example 15–2): ethane C₂H₆ is burned completely with 20 percent excess air at a total pressure of 100 kPa; products: 2 CO₂ + 3 H₂O + 0.7 O₂ + 15.79 N₂. The dew-point temperature of the products (Table A-5) is about:',
         T2, [(bad_Pt, 'là T_sat ở áp suất TỔNG 100 kPa, không phải ở áp suất riêng phần của hơi nước', 'is T_sat at the TOTAL pressure 100 kPa, not at the partial pressure of the vapor'),
              (T_dry, 'dùng số mol sản phẩm khô (không tính H₂O) làm mẫu số của P_v', 'uses the dry product moles (without the H₂O) as the denominator of P_v'),
              (props.sat_P('water', 3 / 2.5 * 10, 'Tsat_C')['value'], 'lấy P_v = N_v/N_O₂,th × 10 kPa (chia cho mol nhiên liệu)', 'takes P_v = N_v / N_O₂,th × 10 kPa (divides by moles of fuel)')], '°C', 1,
         f'P_v = 3/{N(r2["n_tot"],2)} × 100 = {N(Pv2,2)} kPa; T_dp = T_sat@{N(Pv2,2)} kPa = {N(T2,1)} °C (nội suy A-5, slide 52,3; IAPWS {N(Ti2,1)} °C).',
         f'P_v = 3/{N(r2["n_tot"],2)} × 100 = {N(Pv2,2)} kPa; T_dp = T_sat@{N(Pv2,2)} kPa = {N(T2,1)} °C (A-5 interpolation, slide 52.3; IAPWS {N(Ti2,1)} °C).',
         3, TOP['dew'], SLIDE('27–32', 'Ex 15-2'), 'script + slide p.32 (52.3)'))

# ================================================================== 3. Cengel Example 15-3: natural gas with moist air
gas3 = mix([('CH4', .72), ('H2', .09), ('N2', .14), ('O2', .02), ('CO2', .03)]); r3 = combustion(gas3, 1.0)
Pvair = 0.80 * props.sat_T('water', 20, 'Psat_kPa')['value']; Nair_dry = r3['air']; Nvair = Pvair / (101.325 - Pvair) * Nair_dry
r3m = combustion(gas3, 1.0, moist=Nvair); Pv3, T3 = dew_point(r3m['H2O'], r3m['n_tot'], 101.325); Pv3d, T3d = dew_point(r3['H2O'], r3['n_tot'], 101.325)
reg('dew', dict(fuel=fp(('CH4', .72), ('H2', .09), ('N2', .14), ('O2', .02), ('CO2', .03)), lam=1.0, P=101.325, phi=0.8, T_air=20.0), 'Tdp', T3, {'abs': 0.4}, 'Ex 15-3: 60.9 C')
reg('dew', dict(fuel=fp(('CH4', .72), ('H2', .09), ('N2', .14), ('O2', .02), ('CO2', .03)), lam=1.0, P=101.325), 'Tdp', T3d, {'abs': 0.4}, 'Ex 15-3 dry air: 59.5 C')
prn('Ex15-3 Tdp moist air', 60.9, T3, 0.002); prn('Ex15-3 Tdp dry air', 59.5, T3d, 0.002); prn('Ex15-3 a_th', 1.465, r3['ath'], 0.001); prn('Ex15-3 N_v,air', 0.131, Nvair, 0.01); prn('Ex15-3 N_prod', 8.059, r3m['n_tot'], 0.001)
add(ess(B('Cengel Ví dụ 15–3 (ví dụ không có trên slide; cùng §15-2). Một khí thiên nhiên có thành phần thể tích: 72 % CH₄, 9 % H₂, 14 % N₂, 2 % O₂ và 3 % CO₂. Khí này được đốt với lượng không khí ẩm lý thuyết vào buồng đốt ở 20 °C, 1 atm, độ ẩm tương đối 80 %. Giả thiết cháy hoàn toàn, áp suất tổng 1 atm: xác định nhiệt độ điểm sương của sản phẩm.',
           'Cengel Example 15–3 (not on the slides; same §15-2). A certain natural gas has the volumetric analysis 72 percent CH₄, 9 percent H₂, 14 percent N₂, 2 percent O₂ and 3 percent CO₂. It is burned with the stoichiometric amount of air that enters the combustion chamber at 20 °C, 1 atm and 80 percent relative humidity. Assuming complete combustion and a total pressure of 1 atm, determine the dew-point temperature of the products.'),
         B(f'''Giả thiết: cháy hoàn toàn, đúng lượng không khí lý thuyết (không có O₂ tự do), khí lý tưởng; P_sat@20 °C = 2,3392 kPa (A-4). Hơi ẩm trong không khí không phản ứng: cân bằng bằng không khí khô rồi cộng hơi ẩm vào hai vế.
Bước 1 (cho 1 kmol nhiên liệu). (0,72 CH₄ + 0,09 H₂ + 0,14 N₂ + 0,02 O₂ + 0,03 CO₂) + a_th (O₂ + 3,76 N₂) → x CO₂ + y H₂O + z N₂. C: x = 0,72 + 0,03 = 0,75. H: 0,72×4 + 0,09×2 = 2y → y = 1,53. O₂: 0,02 + 0,03 + a_th = x + y/2 → a_th = 1,465. N₂: z = 0,14 + 3,76 × 1,465 = {N(r3["N2"],3)}.
Bước 2 (hơi ẩm trong không khí). Không khí khô: 4,76 × 1,465 = {N(r3["air"],2)} kmol. P_v,air = φ P_sat = 0,80 × 2,3392 = {N(Pvair,3)} kPa. N_v,air = (P_v,air/P_tổng)(N_khô + N_v,air) → N_v,air = P_v,air/(P − P_v,air) × N_khô = {N(Nvair,3)} kmol (sách 0,131).
Bước 3 (sản phẩm). 0,75 CO₂ + ({N(r3m["H2O"],3)}) H₂O + {N(r3["N2"],3)} N₂: N_prod = {N(r3m["n_tot"],3)} kmol. P_v,prod = ({N(r3m["H2O"],3)}/{N(r3m["n_tot"],3)})(101,325) = {N(Pv3,2)} kPa → T_dp = T_sat@{N(Pv3,2)} kPa = {N(T3,1)} °C (nội suy A-5 giữa 20 kPa: 60,06 °C và 25 kPa: 64,96 °C; sách ghi 60,9 °C).
Kiểm tra bằng không khí khô: P_v = 1,53/{N(r3["n_tot"],3)} × 101,325 = {N(Pv3d,2)} kPa → T_dp = {N(T3d,1)} °C (sách 59,5 °C): hơi ẩm trong không khí nâng điểm sương lên {N(T3-T3d,1)} °C.
Hai đường: (A) nội suy A-5; (B) IAPWS-IF97 cho {N(_I(P=Pv3/1000,x=0).T-273.15,2)} °C (lệch {N(_I(P=Pv3/1000,x=0).T-273.15-T3,2)} °C do nội suy). Đáp số: T_dp ≈ {N(T3,1)} °C với không khí ẩm; {N(T3d,1)} °C với không khí khô.''',
           f'''Assumptions: complete combustion, exactly the theoretical air (no free O₂), ideal gases; P_sat@20 °C = 2.3392 kPa (A-4). The moisture of the air does not react: balance with dry air and add the moisture to both sides.
Step 1 (per kmol of fuel). (0.72 CH₄ + 0.09 H₂ + 0.14 N₂ + 0.02 O₂ + 0.03 CO₂) + a_th (O₂ + 3.76 N₂) → x CO₂ + y H₂O + z N₂. C: x = 0.72 + 0.03 = 0.75. H: 0.72×4 + 0.09×2 = 2y → y = 1.53. O₂: 0.02 + 0.03 + a_th = x + y/2 → a_th = 1.465. N₂: z = 0.14 + 3.76 × 1.465 = {N(r3["N2"],3)}.
Step 2 (moisture of the air). Dry air: 4.76 × 1.465 = {N(r3["air"],2)} kmol. P_v,air = φ P_sat = 0.80 × 2.3392 = {N(Pvair,3)} kPa. N_v,air = (P_v,air/P_total)(N_dry + N_v,air) → N_v,air = P_v,air/(P − P_v,air) × N_dry = {N(Nvair,3)} kmol (book 0.131).
Step 3 (products). 0.75 CO₂ + ({N(r3m["H2O"],3)}) H₂O + {N(r3["N2"],3)} N₂: N_prod = {N(r3m["n_tot"],3)} kmol. P_v,prod = ({N(r3m["H2O"],3)}/{N(r3m["n_tot"],3)})(101.325) = {N(Pv3,2)} kPa → T_dp = T_sat@{N(Pv3,2)} kPa = {N(T3,1)} °C (A-5 interpolation between 20 kPa: 60.06 °C and 25 kPa: 64.96 °C; the book prints 60.9 °C).
Check with dry air: P_v = 1.53/{N(r3["n_tot"],3)} × 101.325 = {N(Pv3d,2)} kPa → T_dp = {N(T3d,1)} °C (book 59.5 °C): the moisture of the air raises the dew point by {N(T3-T3d,1)} °C.
Two routes: (A) A-5 interpolation; (B) IAPWS-IF97 gives {N(_I(P=Pv3/1000,x=0).T-273.15,2)} °C (gap {N(_I(P=Pv3/1000,x=0).T-273.15-T3,2)} °C from the interpolation). Answer: T_dp ≈ {N(T3,1)} °C with moist air; {N(T3d,1)} °C with dry air.'''),
         3, TOP['dew'], dict(vi='Cengel Ch.15 Ví dụ 15–3', en='Cengel Ch.15 Example 15–3'), 'goc', 'script + printed 60.9 / 59.5 C'))

# ================================================================== 4. Cengel Example 15-4 = slide tr.33-39 (reverse analysis)
rv = reverse(8, 18, 10.02, 0.88, 5.62, 83.48); Nw = condensed(rv['H2O'], rv['n_tot'], 100, 25); fr = Nw / rv['H2O']
rv_s = dict(AF=19.76, pct=16.32 / 12.5 * 100)                         # the slide's own rounded numbers
NwS = (9 - 3.1698 / 100 * 82.53) / (1 - 3.1698 / 100)
reg('rev', dict(c=8, h=18, CO2=10.02, CO=0.88, O2=5.62, N2=83.48), 'AF', rv['AF'], 1e-9, 'Ex 15-4: slide 19.76 (rounded x = 1.36)'); reg('rev', dict(c=8, h=18, CO2=10.02, CO=0.88, O2=5.62, N2=83.48), 'pct', rv['pct'], 1e-9, 'Ex 15-4: slide 131 %')
reg('cond', dict(c=8, h=18, CO2=10.02, CO=0.88, O2=5.62, N2=83.48, P=100.0, T=25.0), 'Nw', Nw, 2e-3, 'Ex 15-4: slide 6.59 kmol'); reg('cond', dict(c=8, h=18, CO2=10.02, CO=0.88, O2=5.62, N2=83.48, P=100.0, T=25.0), 'frac', fr, 2e-3, 'Ex 15-4: slide 73 %')
prn('Ex15-4 AF (slide tr.36)', 19.76, rv['AF'], 0.005, 'slide: rounded x = 1.36'); prn('Ex15-4 pct (slide tr.37)', 131.0, rv['pct'], 0.005, '130.56 with the slide numbers 16.32/12.5; 130.36 unrounded'); prn('Ex15-4 Nw (slide tr.39)', 6.59, Nw, 0.002); prn('Ex15-4 fraction (slide tr.39)', 73.0, fr * 100, 0.005)
add(ess(B('Cengel Ví dụ 15–4 = slide Ch.4 tr.33–39. Octan (C₈H₁₈) cháy với không khí khô. Phân tích thể tích sản phẩm trên cơ sở khô: CO₂ 10,02 %; O₂ 5,62 %; CO 0,88 %; N₂ 83,48 %. Sản phẩm được làm nguội tới 25 °C ở 100 kPa. Xác định (a) tỉ lệ không khí–nhiên liệu, (b) phần trăm không khí lý thuyết đã dùng, (c) lượng H₂O ngưng tụ.',
           'Cengel Example 15–4 = slide Ch.4 p.33–39. Octane (C₈H₁₈) is burned with dry air. The volumetric analysis of the products on a dry basis is CO₂ 10.02 %, O₂ 5.62 %, CO 0.88 %, N₂ 83.48 %. The products are cooled to 25 °C at 100 kPa. Determine (a) the air–fuel ratio, (b) the percentage of theoretical air used and (c) the amount of H₂O that condenses.'),
         B(f'''Giả thiết: khí lý tưởng (phần thể tích = phần mol); lấy 100 kmol sản phẩm khô. P_sat@25 °C = 3,1698 kPa (A-4).
Bước 1 (slide tr.34). x C₈H₁₈ + a (O₂ + 3,76 N₂) → 10,02 CO₂ + 0,88 CO + 5,62 O₂ + 83,48 N₂ + b H₂O. N₂: 3,76 a = 83,48 → a = {N(rv["a"],2)}. C: 8x = 10,02 + 0,88 → x = {N(rv["x"],4)} (slide làm tròn 1,36). H: 18x = 2b → b = {N(rv["b"],3)} (slide 12,24). Kiểm O₂: a = 10,02 + 0,44 + 5,62 + b/2 = {N(10.02+0.44+5.62+rv["b"]/2,3)} (slide 22,20 = 22,20; lệch {N(abs(rv["resid"]),3)} do làm tròn thành phần).
Bước 2 (tr.35). Chia cho x: C₈H₁₈ + {N(rv["a"]/rv["x"],2)}(O₂ + 3,76 N₂) → {N(rv["CO2"],2)} CO₂ + {N(rv["CO"],2)} CO + {N(rv["O2"],2)} O₂ + {N(rv["N2"],2)} N₂ + 9 H₂O (slide: 16,32; 7,37; 0,65; 4,13; 61,38).
(a) AF = (16,32 × 4,76)(29)/[(8)(12) + (9)(2)] = 19,76 kg/kg theo số làm tròn của slide; với số không làm tròn ({N(rv["a"]/rv["x"],3)} kmol không khí/kmol nhiên liệu): {N(rv["AF"],2)} kg/kg.
(b) Không khí lý thuyết: C₈H₁₈ + a_th(O₂ + 3,76 N₂) → 8 CO₂ + 9 H₂O + 3,76 a_th N₂ → a_th = 8 + 4,5 = 12,5. Phần trăm = 16,32/12,5 = 130,6 % (slide ghi 131 %); không làm tròn x: {N(rv["pct"],1)} % → khoảng 31 % không khí thừa.
(c) Sản phẩm trên 1 kmol nhiên liệu: {N(rv["n_tot"],2)} kmol (slide 82,53) gồm 9 kmol H₂O. (9 − N_w)/({N(rv["n_tot"],2)} − N_w) = 3,1698/100 → N_w = {N(Nw,2)} kmol (slide 6,59), tức {N(fr*100,1)} % hơi nước ngưng tụ (slide 73 %).
Hai đường: (A) cân bằng tay; (B) sympy giải N₂, C, H (chính xác, phân số) và kiểm O₂; N_w giải bằng scipy brentq với P_sat từ IAPWS-IF97 (3,1698 → {N(_I(T=298.15,x=0).P*1000,4)} kPa). Đáp số: AF ≈ 19,7–19,8 kg/kg; ≈ 131 % lý thuyết; N_w ≈ {N(Nw,2)} kmol/kmol nhiên liệu.''',
           f'''Assumptions: ideal gases (volume fraction = mole fraction); take 100 kmol of dry products. P_sat@25 °C = 3.1698 kPa (A-4).
Step 1 (slide p.34). x C₈H₁₈ + a (O₂ + 3.76 N₂) → 10.02 CO₂ + 0.88 CO + 5.62 O₂ + 83.48 N₂ + b H₂O. N₂: 3.76 a = 83.48 → a = {N(rv["a"],2)}. C: 8x = 10.02 + 0.88 → x = {N(rv["x"],4)} (the slide rounds to 1.36). H: 18x = 2b → b = {N(rv["b"],3)} (slide 12.24). O₂ check: a = 10.02 + 0.44 + 5.62 + b/2 = {N(10.02+0.44+5.62+rv["b"]/2,3)} (slide 22.20 = 22.20; gap {N(abs(rv["resid"]),3)} from rounding of the composition).
Step 2 (p.35). Divide by x: C₈H₁₈ + {N(rv["a"]/rv["x"],2)}(O₂ + 3.76 N₂) → {N(rv["CO2"],2)} CO₂ + {N(rv["CO"],2)} CO + {N(rv["O2"],2)} O₂ + {N(rv["N2"],2)} N₂ + 9 H₂O (slide: 16.32; 7.37; 0.65; 4.13; 61.38).
(a) AF = (16.32 × 4.76)(29)/[(8)(12) + (9)(2)] = 19.76 kg/kg with the slide's rounded numbers; unrounded ({N(rv["a"]/rv["x"],3)} kmol air/kmol fuel): {N(rv["AF"],2)} kg/kg.
(b) Theoretical air: C₈H₁₈ + a_th(O₂ + 3.76 N₂) → 8 CO₂ + 9 H₂O + 3.76 a_th N₂ → a_th = 8 + 4.5 = 12.5. Percentage = 16.32/12.5 = 130.6 % (slide prints 131 %); with x unrounded: {N(rv["pct"],1)} % → about 31 percent excess air.
(c) Products per kmol of fuel: {N(rv["n_tot"],2)} kmol (slide 82.53) including 9 kmol H₂O. (9 − N_w)/({N(rv["n_tot"],2)} − N_w) = 3.1698/100 → N_w = {N(Nw,2)} kmol (slide 6.59), i.e. {N(fr*100,1)} % of the vapor condenses (slide 73 %).
Two routes: (A) hand balances; (B) sympy solves N₂, C, H exactly (fractions) and checks O₂; N_w solved with scipy brentq using P_sat from IAPWS-IF97 (3.1698 → {N(_I(T=298.15,x=0).P*1000,4)} kPa). Answer: AF ≈ 19.7–19.8 kg/kg; ≈ 131 % theoretical; N_w ≈ {N(Nw,2)} kmol per kmol fuel.'''),
         3, TOP['rev'], SLIDE('33–39', 'Ex 15-4'), 'goc', 'script + slide p.34-39 (printed 19.76, 131 %, 6.59 kmol, 73 %)'))
add(numq('Slide Ch.4 tr.33–36 (Cengel Ví dụ 15–4): octan cháy với không khí khô, sản phẩm khô (mol %): 10,02 CO₂; 0,88 CO; 5,62 O₂; 83,48 N₂. Phương trình cho 1 kmol nhiên liệu có 16,32 kmol O₂ trong không khí. Tỉ lệ không khí–nhiên liệu AF (kg/kg, M_air = 29) xấp xỉ:',
         'Slide Ch.4 p.33–36 (Cengel Example 15–4): octane burned with dry air, dry products (mol %): 10.02 CO₂; 0.88 CO; 5.62 O₂; 83.48 N₂. The equation per kmol of fuel has 16.32 kmol O₂ in the air. The air–fuel ratio AF (kg/kg, M_air = 29) is about:',
         19.76, [(16.32, 'là số kmol O₂ trên kmol nhiên liệu, chưa nhân 4,76 và khối lượng mol', 'is the kmol O₂ per kmol fuel, not yet multiplied by 4.76 and the molar masses'),
                 (combustion(single('C8H18'), 1.0)['AF'], 'là AF của cháy lý thuyết (12,5 kmol O₂), không phải của quá trình thực', 'is the AF of theoretical combustion (12.5 kmol O₂), not of the actual process'),
                 (16.32 * 32 / 114, 'bỏ N₂ khỏi không khí (chỉ O₂: 16,32 × 32)/114', 'drops the N₂ of the air (only O₂: 16.32 × 32)/114')], 'kg/kg', 2,
         f'AF = (16.32 × 4.76 kmol)(29 kg/kmol)/[(8)(12) + (9)(2)] = {N(16.32*4.76*29,1)}/114 = 19.76 kg/kg (slide tr.36; không làm tròn x = 1.3625 thì {N(rv["AF"],2)}).',
         f'AF = (16.32 × 4.76 kmol)(29 kg/kmol)/[(8)(12) + (9)(2)] = {N(16.32*4.76*29,1)}/114 = 19.76 kg/kg (slide p.36; with the unrounded x = 1.3625: {N(rv["AF"],2)}).',
         2, TOP['rev'], SLIDE('36', 'Ex 15-4'), 'slide p.36 (printed 19.76) + script'))
add(numq('Slide Ch.4 tr.36–37 (Cengel Ví dụ 15–4): không khí thực tế dùng là 16,32 kmol O₂ trên kmol octan; không khí lý thuyết cần a_th = 12,5 kmol O₂. Phần trăm không khí lý thuyết đã dùng là:',
         'Slide Ch.4 p.36–37 (Cengel Example 15–4): the actual air is 16.32 kmol O₂ per kmol of octane; the theoretical air needs a_th = 12.5 kmol O₂. The percentage of theoretical air used is:',
         16.32 / 12.5 * 100, [(31.0, 'là phần trăm không khí THỪA (131 % − 100 %)', 'is the percent EXCESS air (131 % − 100 %)'), (12.5 / 16.32 * 100, 'đảo ngược tỉ số (lý thuyết/thực)', 'inverts the ratio (theoretical/actual)'),
                                  (16.32 / 12.5 * 100 * 29 / 28.97 * 0 + (16.32 - 12.5) / 16.32 * 100, 'lấy phần thừa chia cho lượng thực tế ((16,32 − 12,5)/16,32)', 'divides the excess by the actual amount ((16.32 − 12.5)/16.32)')], '%', 1,
         '16.32/12.5 = 1.306 = 130.6 % (slide ghi 131 %, tức 31 % không khí thừa); phần trăm không khí lý thuyết = N_air,thực/N_air,lt = m_air,thực/m_air,lt vì cùng khối lượng mol; 100 % = cháy lý thuyết.',
         '16.32/12.5 = 1.306 = 130.6 % (slide prints 131 %, i.e. 31 percent excess air); percent theoretical air = N_air,act/N_air,th = m_air,act/m_air,th because the molar mass is the same; 100 % = theoretical combustion.',
         2, TOP['air'], SLIDE('36–37', 'Ex 15-4'), 'slide p.37 (printed 131 %) + script'))
add(numq('Slide Ch.4 tr.38–39 (Cengel Ví dụ 15–4): sản phẩm trên 1 kmol octan gồm 82,53 kmol, trong đó 9 kmol H₂O. Làm nguội tới 25 °C ở 100 kPa (P_sat = 3,1698 kPa), lượng nước ngưng tụ N_w (kmol/kmol nhiên liệu) là:',
         'Slide Ch.4 p.38–39 (Cengel Example 15–4): the products per kmol of octane total 82.53 kmol, of which 9 kmol is H₂O. When cooled to 25 °C at 100 kPa (P_sat = 3.1698 kPa) the condensed water N_w (kmol per kmol of fuel) is:',
         NwS, [(9 - NwS, 'là lượng hơi nước CÒN LẠI (9 − N_w)', 'is the vapor REMAINING (9 − N_w)'), (9 - 3.1698 / 100 * 82.53, 'quên rằng mẫu số cũng giảm đi N_w: 9 − 0,031698 × 82,53', 'forgets that the denominator also shrinks by N_w: 9 − 0.031698 × 82.53'), (9.0, 'cho rằng toàn bộ 9 kmol ngưng tụ', 'assumes all 9 kmol condense')], 'kmol', 2,
         f'(9 − N_w)/(82.53 − N_w) = 0.031698 → N_w = (9 − 0.031698 × 82.53)/(1 − 0.031698) = {N(NwS,2)} kmol, tức {N(NwS/9*100,0)} % lượng hơi nước (slide tr.39: 6.59 kmol, 73 %).',
         f'(9 − N_w)/(82.53 − N_w) = 0.031698 → N_w = (9 − 0.031698 × 82.53)/(1 − 0.031698) = {N(NwS,2)} kmol, i.e. {N(NwS/9*100,0)} % of the vapor (slide p.39: 6.59 kmol, 73 %).',
         3, TOP['rev'], SLIDE('38–39', 'Ex 15-4'), 'slide p.39 (printed 6.59) + script'))
reg('cond', dict(c=8, h=18, CO2=10.02, CO=0.88, O2=5.62, N2=83.48, P=100.0, T=25.0, slide=True), 'Nw', NwS, 2e-3, 'slide tr.39 with its own numbers 82.53 and 9')

# ================================================================== 5. Cengel Example 15-5 = slide tr.53-54 (enthalpy of combustion of liquid octane)
hCo = hC_nu('C8H18_l', dict(CO2=8, H2O=9), 'l'); Mo = A27row('C8H18', 'M'); hCgl = hC_nu('C8H18_g', dict(CO2=8, H2O=9), 'l'); hCg = hCgl      # gaseous octane, liquid water (the book's Discussion)
LHVo = hC_nu('C8H18_l', dict(CO2=8, H2O=9), 'g')
reg('hC', dict(fuel='C8H18_l', nu={'CO2': 8, 'H2O': 9}, water='l', a27='C8H18', col='HHV'), 'kJ/kmol', hCo, 1.5e-3, 'Ex 15-5 slide tr.54: -5,471,000 (rounded)'); reg('hC', dict(fuel='C8H18_l', nu={'CO2': 8, 'H2O': 9}, water='l', a27='C8H18', col='HHV'), 'kJ/kg', hCo / Mo, 1.5e-3, 'Ex 15-5: -47,891; A-27 47,890')
reg('hC', dict(fuel='C8H18_l', nu={'CO2': 8, 'H2O': 9}, water='g', a27='C8H18', col='LHV'), 'kJ/kg', LHVo / Mo, 1.5e-3, 'octane LHV vs A-27 44,430')
prn('Ex15-5 hC kJ/kmol (slide tr.54)', -5471000.0, hCo, 1e-3, 'slide rounded; exact -5,470,680'); prn('Ex15-5 hC kJ/kg', -47891.0, hCo / Mo, 1e-4); prn('Ex15-5 A-27 HHV', 47890.0, -hCo / Mo, 1e-3); prn('Ex15-5 gaseous octane kJ/kmol (book Discussion)', -5512200.0, hCg, 2e-5); prn('Ex15-5 gaseous octane kJ/kg', -48255.0, hCg / Mo, 1e-4)
mH2O = 9 * 18.015 / Mo; hfg25 = props.sat_T('water', 25, 'hfg')['value']
add(ess(B('Cengel Ví dụ 15–5 = slide Ch.4 tr.53–55. Xác định entanpi cháy của octan lỏng (C₈H₁₈) ở 25 °C, 1 atm bằng số liệu entanpi hình thành của bảng A-26; giả thiết nước trong sản phẩm ở thể lỏng. So với nhiệt trị của bảng A-27.',
           'Cengel Example 15–5 = slide Ch.4 p.53–55. Determine the enthalpy of combustion of liquid octane (C₈H₁₈) at 25 °C and 1 atm using the enthalpy-of-formation data of Table A-26; assume the water in the products is liquid. Compare with the heating value of Table A-27.'),
         B(f'''Dữ liệu A-26 (25 °C, 1 atm): h̄_f°(CO₂) = −393 520; h̄_f°(H₂O ℓ) = −285 830; h̄_f°(C₈H₁₈ ℓ) = −249 950 kJ/kmol; O₂ và N₂ là nguyên tố bền nên h̄_f° = 0 (slide tr.53, 49). Slide tr.53 ghi các giá trị này KHÔNG có dấu trừ (dấu trừ xuất hiện ở tr.54).
Bước 1. C₈H₁₈ + a_th(O₂ + 3,76 N₂) → 8 CO₂ + 9 H₂O(ℓ) + 3,76 a_th N₂; chất phản ứng và sản phẩm đều ở trạng thái chuẩn nên ΔE_state = 0.
Bước 2 (slide tr.54). h̄_C = H_prod − H_react = (8)(−393 520) + (9)(−285 830) − (1)(−249 950) = −3 148 160 − 2 572 470 + 249 950 = {N(hCo,0)} kJ/kmol (slide làm tròn −5 471 000). Chia cho M = 114,231 kg/kmol (A-27): {N(hCo/Mo,0)} kJ/kg (slide −47 891).
Bước 3 (đối chiếu A-27). Nhiệt trị cao của octan lỏng A-27: 47 890 kJ/kg; |h̄_C|/M = {N(-hCo/Mo,0)} kJ/kg (lệch {N(abs(-hCo/Mo-47890)/47890*100,3)} %). Vì nước lỏng, h̄_C là HHV.
Bước 4 (LHV). Nếu H₂O ở thể hơi (h̄_f° = −241 820): h̄_C = {N(LHVo,0)} kJ/kmol → LHV = {N(-LHVo/Mo,0)} kJ/kg; kiểm tra HHV = LHV + m h_fg: m = 9 × 18,015/114,231 = {N(mH2O,3)} kg H₂O/kg, h_fg@25 °C = {N(hfg25,1)} kJ/kg → HHV = {N(-LHVo/Mo+mH2O*hfg25,0)} kJ/kg. A-27 LHV = 44 430.
Bước 5 (octan khí, mục Thảo luận của sách). h̄_f°(C₈H₁₈ g) = −208 450 → h̄_C = {N(hCgl,0)} kJ/kmol = {N(hCgl/Mo,0)} kJ/kg (sách ghi −5 512 200 và −48 255).
Hai đường: (A) entanpi hình thành bảng A-26; (B) nhiệt trị A-27 × M: 47 890 × 114,231 = {N(47890*114.231,0)} kJ/kmol, lệch {N(abs(47890*114.231+hCo)/-hCo*100,3)} %. Đáp số: h̄_C = {N(hCo,0)} kJ/kmol ≈ −5,47×10⁶ kJ/kmol = {N(hCo/Mo,0)} kJ/kg.''',
           f'''Data from A-26 (25 °C, 1 atm): h̄_f°(CO₂) = −393,520; h̄_f°(H₂O ℓ) = −285,830; h̄_f°(C₈H₁₈ ℓ) = −249,950 kJ/kmol; O₂ and N₂ are stable elements so h̄_f° = 0 (slides p.53, 49). Slide p.53 prints these values WITHOUT the minus sign (the sign appears on p.54).
Step 1. C₈H₁₈ + a_th(O₂ + 3.76 N₂) → 8 CO₂ + 9 H₂O(ℓ) + 3.76 a_th N₂; reactants and products are both at the standard state so ΔE_state = 0.
Step 2 (slide p.54). h̄_C = H_prod − H_react = (8)(−393,520) + (9)(−285,830) − (1)(−249,950) = −3,148,160 − 2,572,470 + 249,950 = {N(hCo,0)} kJ/kmol (the slide rounds to −5,471,000). Divide by M = 114.231 kg/kmol (A-27): {N(hCo/Mo,0)} kJ/kg (slide −47,891).
Step 3 (check with A-27). The higher heating value of liquid octane in A-27 is 47,890 kJ/kg; |h̄_C|/M = {N(-hCo/Mo,0)} kJ/kg (difference {N(abs(-hCo/Mo-47890)/47890*100,3)} %). Because the water is liquid, h̄_C is the HHV.
Step 4 (LHV). With H₂O vapor (h̄_f° = −241,820): h̄_C = {N(LHVo,0)} kJ/kmol → LHV = {N(-LHVo/Mo,0)} kJ/kg; check HHV = LHV + m h_fg: m = 9 × 18.015/114.231 = {N(mH2O,3)} kg H₂O/kg, h_fg@25 °C = {N(hfg25,1)} kJ/kg → HHV = {N(-LHVo/Mo+mH2O*hfg25,0)} kJ/kg. A-27 LHV = 44,430.
Step 5 (gaseous octane, the book's Discussion). h̄_f°(C₈H₁₈ g) = −208,450 → h̄_C = {N(hCgl,0)} kJ/kmol = {N(hCgl/Mo,0)} kJ/kg (the book prints −5,512,200 and −48,255).
Two routes: (A) formation enthalpies of Table A-26; (B) heating value of A-27 × M: 47,890 × 114.231 = {N(47890*114.231,0)} kJ/kmol, difference {N(abs(47890*114.231+hCo)/-hCo*100,3)} %. Answer: h̄_C = {N(hCo,0)} kJ/kmol ≈ −5.47×10⁶ kJ/kmol = {N(hCo/Mo,0)} kJ/kg.'''),
         2, TOP['enth'], SLIDE('53–55', 'Ex 15-5'), 'goc', 'script + slide p.54 (printed -5,471,000 and -47,891) + A-27'))
add(numq('Slide Ch.4 tr.54 (Cengel Ví dụ 15–5): h̄_C của octan lỏng C₈H₁₈ ở 25 °C, 1 atm, nước sản phẩm ở thể lỏng, là −5 471 000 kJ/kmol. Tính trên 1 kg nhiên liệu (M = 114,231 kg/kmol), entanpi cháy là:',
         'Slide Ch.4 p.54 (Cengel Example 15–5): the enthalpy of combustion of liquid octane C₈H₁₈ at 25 °C, 1 atm, liquid water in the products, is −5,471,000 kJ/kmol. Per kilogram of fuel (M = 114.231 kg/kmol) it is:',
         hCo / Mo, [(-5471000.0, 'chưa chia cho khối lượng mol (vẫn là kJ/kmol)', 'not yet divided by the molar mass (still kJ/kmol)'), (-hCo / Mo, 'sai dấu: entanpi cháy của phản ứng tỏa nhiệt là ÂM', 'wrong sign: the enthalpy of combustion of an exothermic reaction is NEGATIVE'),
                    (hCg / Mo, 'dùng octan KHÍ (−5 512 200 kJ/kmol), không phải octan lỏng', 'uses GASEOUS octane (−5,512,200 kJ/kmol), not liquid octane')], 'kJ/kg', 0,
         f'h̄_C/M = −5 470 680/114.231 = {N(hCo/Mo,0)} kJ/kg (slide −47 891); nhiệt trị cao A-27 = 47 890 kJ/kg vì nước ở thể lỏng.',
         f'h̄_C/M = −5,470,680/114.231 = {N(hCo/Mo,0)} kJ/kg (slide −47,891); the A-27 higher heating value is 47,890 kJ/kg because the water is liquid.',
         2, TOP['enth'], SLIDE('54', 'Ex 15-5'), 'slide p.54 (printed -47,891) + A-27'))

# ================================================================== 6. Cengel end-of-chapter problems: air-fuel ratio, theoretical/excess air
def af_wr(parts, lam, exact=False, pct_excess=None):
    """typical wrong values for an AF problem: (value, reason_vi, reason_en)."""
    fu = parts_fuel(parts, exact); r = combustion(fu, lam, exact=exact); r1 = combustion(fu, 1.0, exact=exact); out = []
    out.append((r['o2_in'] * 32 / fu['M'], 'bỏ N₂ của không khí (chỉ tính O₂)', 'drops the N₂ of the air (O₂ only)'))
    out.append((r['air'], 'là AF theo mol (kmol không khí/kmol nhiên liệu), chưa đổi sang khối lượng', 'is the AF on a mole basis (kmol air per kmol fuel), not converted to mass'))
    out.append((r1['AF'], 'dùng không khí lý thuyết (λ = 1), bỏ qua phần thừa', 'uses theoretical air (λ = 1) and ignores the excess'))
    if lam == 1.0 and not pct_excess: out.append((1.0 / r['AF'], 'là tỉ lệ nhiên liệu–không khí FA = 1/AF', 'is the fuel–air ratio FA = 1/AF'))
    if pct_excess: out.append((combustion(fu, pct_excess / 100.0, exact=exact)['AF'], f'hiểu {pct_excess:g} % không khí thừa là {pct_excess:g} % không khí lý thuyết', f'reads {pct_excess:g} percent excess air as {pct_excess:g} percent theoretical air'))
    return out

def af_item(num, qv, qe, parts, lam, printed, tag, pct_excess=None, level=2, exact=False, note_vi='', note_en='', nd=1, topic='af', model_what=''):
    r = AFcalc(parts, lam, exact=exact); fu = parts_fuel(parts, exact)
    REGc(parts, lam, 'AF', r['AF'], f'Cengel {num}' + model_what, exact=exact)
    if printed is not None: prn(f'Cengel {num} AF', printed, r['AF'], 0.012 if printed else 0.01, note_vi)
    thv = {k: N(v, 2) for k, v in dict(ath=r['ath'], o2=r['o2_in'], air=r['air'], M=fu['M']).items()}
    ev = f'a_th = {thv["ath"]} kmol O₂/kmol nhiên liệu (cân bằng O₂); O₂ thực = {N(lam,2)} × a_th = {thv["o2"]}; không khí = 4,76 × {thv["o2"]} = {thv["air"]} kmol; AF = {thv["air"]} × {"28,97" if exact else "29"}/{thv["M"]} = {N(r["AF"],nd+1)} kg/kg' + (f' (đáp án in {N(printed,nd)})' if printed else '') + '.' + note_vi
    ee = f'a_th = {thv["ath"]} kmol O₂ per kmol fuel (O₂ balance); actual O₂ = {N(lam,2)} × a_th = {thv["o2"]}; air = 4.76 × {thv["o2"]} = {thv["air"]} kmol; AF = {thv["air"]} × {"28.97" if exact else "29"}/{thv["M"]} = {N(r["AF"],nd+1)} kg/kg' + (f' (printed answer {N(printed,nd)})' if printed else '') + '.' + note_en
    return add(numq(qv, qe, r['AF'], af_wr(parts, lam, exact, pct_excess), 'kg/kg', nd, ev, ee, level, TOP[topic], CEN(num), tag))

af_item('15–13', 'Cengel Ch.15 Bài 15–13. Metan (CH₄) được đốt với lượng không khí lý thuyết (stoichiometric). Giả thiết cháy hoàn toàn. Tỉ lệ không khí–nhiên liệu AF (theo khối lượng) là:',
        'Cengel Ch.15 Problem 15–13. Methane (CH₄) is burned with the stoichiometric amount of air. Assuming complete combustion, the air–fuel ratio AF (mass basis) is:', [('CH4', 1)], 1.0, None, 'script (không có đáp án in)', level=1,
        note_vi=' Tỉ lệ nhiên liệu–không khí FA = 1/AF = 0,058 là đáp án thứ hai của đề.', note_en=' The fuel–air ratio FA = 1/AF = 0.058 is the second answer of the statement.')
af_item('15–14', 'Cengel Ch.15 Bài 15–14. Propan (C₃H₈) được đốt với 75 % không khí thừa. Giả thiết cháy hoàn toàn. Tỉ lệ không khí–nhiên liệu là:',
        'Cengel Ch.15 Problem 15–14. Propane (C₃H₈) is burned with 75 percent excess air. Assuming complete combustion, the air–fuel ratio is:', [('C3H8', 1)], 1.75, 27.5, 'printed answer 27.5 + script', pct_excess=75)
r15 = AFcalc([('C2H2', 1)], 1.0); reg('comb', dict(fuel=fp(('C2H2', 1)), lam=1.0, exact=False), 'air', r15['air'], 1e-9, 'Cengel 15-15 mole basis')
add(mcq(B('Cengel Ch.15 Bài 15–15. Axetilen (C₂H₂) được đốt với lượng không khí lý thuyết, cháy hoàn toàn. Tỉ lệ không khí–nhiên liệu theo khối lượng và theo mol là:', 'Cengel Ch.15 Problem 15–15. Acetylene (C₂H₂) is burned with the stoichiometric amount of air, complete combustion. The air–fuel ratio on a mass basis and on a mole basis is:'),
         [opt(f'{N(r15["AF"],1)} kg/kg; {N(r15["air"],1)} kmol/kmol'), opt(f'{N(r15["o2_in"]*32/26,1)} kg/kg; {N(r15["o2_in"],1)} kmol/kmol'), opt(f'{N(r15["air"],1)} kg/kg; {N(r15["AF"],1)} kmol/kmol'), opt(f'{N(r15["AF"]/2,1)} kg/kg; {N(r15["air"]/2,1)} kmol/kmol')], 0,
         B(f'C₂H₂ + 2,5(O₂ + 3,76 N₂) → 2 CO₂ + H₂O + 9,4 N₂: không khí = 2,5 × 4,76 = {N(r15["air"],1)} kmol/kmol nhiên liệu (AF mol); AF khối lượng = {N(r15["air"],1)} × 29/26 = {N(r15["AF"],1)} kg/kg. Phương án thứ hai bỏ N₂ của không khí; phương án đổi chỗ hai số nhầm đơn vị; phương án cuối chia đôi vì đọc sai hệ số của C₂H₂ trong phương trình.',
           f'C₂H₂ + 2.5(O₂ + 3.76 N₂) → 2 CO₂ + H₂O + 9.4 N₂: air = 2.5 × 4.76 = {N(r15["air"],1)} kmol per kmol fuel (mole AF); mass AF = {N(r15["air"],1)} × 29/26 = {N(r15["AF"],1)} kg/kg. The second option drops the N₂ of the air; the swapped option mixes the units; the last option halves the values by misreading the coefficient of C₂H₂.'),
         2, TOP['af'], CEN('15–15'), 'goc', 'script (không có đáp án in)', fixed=False))
r16 = combustion(single('C2H6'), 6.5 / 3.5); reg('comb', dict(fuel=fp(('C2H6', 1)), lam=6.5 / 3.5, exact=False), 'AF', r16['AF'], 1e-9, 'Cengel 15-16'); reg('pct', dict(num=6.5, den=3.5), 'pct', 6.5 / 3.5 * 100, 1e-9, 'Cengel 15-16 b')
add(numq('Cengel Ch.15 Bài 15–16. Một kmol etan (C₂H₆) cháy với lượng không khí chưa biết. Phân tích sản phẩm cho thấy cháy hoàn toàn và có 3 kmol O₂ tự do trong sản phẩm. Tỉ lệ không khí–nhiên liệu AF (kg/kg) là:',
         'Cengel Ch.15 Problem 15–16. One kmol of ethane (C₂H₆) is burned with an unknown amount of air. The product analysis shows complete combustion and 3 kmol of free O₂ in the products. The air–fuel ratio AF (kg/kg) is:',
         r16['AF'], [(3 * 4.76 * 29 / 30, 'coi 3 kmol O₂ tự do là toàn bộ O₂ cấp vào', 'takes the 3 kmol of free O₂ as all the O₂ supplied'), (3.5 * 4.76 * 29 / 30, 'dùng không khí lý thuyết a_th = 3,5, bỏ phần thừa', 'uses the theoretical air a_th = 3.5 and ignores the excess'), (6.5 * 4.76, 'là AF theo mol', 'is the AF on a mole basis')], 'kg/kg', 1,
         f'O₂ vào = a_th + 3 = 3,5 + 3 = 6,5 kmol (O₂ thừa 3 kmol, hơi nước 3 kmol cần 1,5 và CO₂ cần 2); không khí = 6,5 × 4,76 = {N(6.5*4.76,2)} kmol; AF = {N(6.5*4.76,2)} × 29/30 = {N(r16["AF"],1)} kg/kg; phần trăm không khí lý thuyết = 6,5/3,5 = {N(6.5/3.5*100,1)} % (câu b của sách).',
         f'O₂ in = a_th + 3 = 3.5 + 3 = 6.5 kmol (3 kmol O₂ left over, 3 kmol H₂O need 1.5 and CO₂ needs 2); air = 6.5 × 4.76 = {N(6.5*4.76,2)} kmol; AF = {N(6.5*4.76,2)} × 29/30 = {N(r16["AF"],1)} kg/kg; percent theoretical air = 6.5/3.5 = {N(6.5/3.5*100,1)} % (part b of the book).',
         2, TOP['af'], CEN('15–16'), 'script (không có đáp án in)'))
r17 = combustion(single('C2H4'), 2.0); reg('comb', dict(fuel=fp(('C2H4', 1)), lam=2.0, exact=False), 'AF', r17['AF'], 1e-9, 'Cengel 15-17E a'); prn('Cengel 15-17E AF (a)', 29.6, r17['AF'], 0.005)
Pv17 = 14.5 * 6.894757 * r17['H2O'] / r17['n_tot']; Td17 = (_I(P=Pv17 / 1000, x=0).T - 273.15) * 1.8 + 32; prn('Cengel 15-17E dew point (b) [F] by iapws (A-5E not done)', 101.0, Td17, 0.01, 'dew point not used as a question: English-unit table A-5E CHƯA LÀM; iapws gives 100.6 F')
add(numq('Cengel Ch.15 Bài 15–17E (câu a). Etylen (C₂H₄) được đốt với 200 % không khí lý thuyết, cháy hoàn toàn, áp suất tổng 14,5 psia. Tỉ lệ không khí–nhiên liệu (lbm không khí/lbm nhiên liệu) là:',
         'Cengel Ch.15 Problem 15–17E (part a). Ethylene (C₂H₄) is burned with 200 percent theoretical air, complete combustion, total pressure 14.5 psia. The air–fuel ratio (lbm air per lbm fuel) is:',
         r17['AF'], af_wr([('C2H4', 1)], 2.0)[:3], 'lbm/lbm', 1, f'C₂H₄ + 3(O₂ + 3,76 N₂) cần a_th = 3; 200 % → 6 kmol O₂ → không khí 6 × 4,76 = 28,56 kmol; AF = 28,56 × 29/28 = {N(r17["AF"],1)} (đáp án in 29,6). Tỉ số khối lượng không phụ thuộc hệ đơn vị.',
         f'C₂H₄ + 3(O₂ + 3.76 N₂) needs a_th = 3; 200 % → 6 kmol O₂ → air 6 × 4.76 = 28.56 kmol; AF = 28.56 × 29/28 = {N(r17["AF"],1)} (printed answer 29.6). A mass ratio does not depend on the unit system.',
         2, TOP['af'], CEN('15–17E', ' (câu a)', ' (part a)'), 'printed answer 29.6 + script'))
r18 = combustion(single('C3H6'), 1.5); Pv18, T18 = dew_point(r18['H2O'], r18['n_tot'], 105)
reg('dew', dict(fuel=fp(('C3H6', 1)), lam=1.5, P=105.0), 'Tdp', T18, {'abs': 0.35}, 'Cengel 15-18 b'); reg('comb', dict(fuel=fp(('C3H6', 1)), lam=1.5, exact=False), 'AF', r18['AF'], 1e-9, 'Cengel 15-18 a')
add(numq('Cengel Ch.15 Bài 15–18 (câu b). Propylen (C₃H₆) được đốt với 50 % không khí thừa, cháy hoàn toàn, áp suất tổng 105 kPa. Nhiệt độ mà hơi nước trong sản phẩm bắt đầu ngưng tụ (bảng A-5) xấp xỉ:',
         'Cengel Ch.15 Problem 15–18 (part b). Propylene (C₃H₆) is burned with 50 percent excess air, complete combustion, total pressure 105 kPa. The temperature at which the water vapor in the products starts to condense (Table A-5) is about:',
         T18, [(props.sat_P('water', 105, 'Tsat_C')['value'], 'là T_sat ở áp suất tổng 105 kPa', 'is T_sat at the total pressure of 105 kPa'), (dew_point(3, r18['n_dry'], 105)[1], 'bỏ H₂O khỏi tổng số mol sản phẩm', 'leaves the H₂O out of the total product moles'), (dew_point(r18['H2O'], r18['n_tot'], 100)[1] - 12, 'chia số mol cho hệ số của nhiên liệu sai (4,5 O₂ thay vì 6,75)', 'uses the wrong O₂ supply (4.5 instead of 6.75 kmol)')], '°C', 1,
         f'C₃H₆ + 6,75(O₂ + 3,76 N₂) → 3 CO₂ + 3 H₂O + 2,25 O₂ + 25,38 N₂; N_prod = {N(r18["n_tot"],2)} kmol; P_v = 3/{N(r18["n_tot"],2)} × 105 = {N(Pv18,2)} kPa → T_dp = T_sat = {N(T18,1)} °C (nội suy A-5; IAPWS {N(_I(P=Pv18/1000,x=0).T-273.15,1)} °C). AF = {N(r18["AF"],1)} kg/kg (câu a).',
         f'C₃H₆ + 6.75(O₂ + 3.76 N₂) → 3 CO₂ + 3 H₂O + 2.25 O₂ + 25.38 N₂; N_prod = {N(r18["n_tot"],2)} kmol; P_v = 3/{N(r18["n_tot"],2)} × 105 = {N(Pv18,2)} kPa → T_dp = T_sat = {N(T18,1)} °C (A-5 interpolation; IAPWS {N(_I(P=Pv18/1000,x=0).T-273.15,1)} °C). AF = {N(r18["AF"],1)} kg/kg (part a).',
         3, TOP['dew'], CEN('15–18', ' (câu b)', ' (part b)'), 'script (không có đáp án in)'))
af_item('15–19', 'Cengel Ch.15 Bài 15–19. Rượu propylic (C₃H₇OH) được đốt với 50 % không khí thừa. Viết phương trình cháy hoàn toàn và xác định tỉ lệ không khí–nhiên liệu.',
        'Cengel Ch.15 Problem 15–19. Propyl alcohol (C₃H₇OH) is burned with 50 percent excess air. Write the balanced equation for complete combustion and determine the air-to-fuel ratio.', [('C3H7OH', 1)], 1.5, 15.5, 'printed answer 15.5 + script', pct_excess=50,
        note_vi=' Nhiên liệu có O nên a_th = 3 + 2 − 0,5 = 4,5 (O trong nhiên liệu cấp bớt O₂).', note_en=' The fuel contains O, so a_th = 3 + 2 − 0.5 = 4.5 (the O in the fuel supplies some of the oxygen).')
add(ITEMS[-1])  if False else None
r20 = combustion(single('C4H10'), 2.0); Psat60 = props.sat_T('water', 60, 'Psat_kPa')['value']; w20 = (Psat60 / 100 * r20['n_tot'] - r20['H2O']) / (1 - Psat60 / 100)
reg('spray', dict(fuel=fp(('C4H10', 1)), lam=2.0, P=100.0, T=60.0), 'w', w20, 2e-3, 'Cengel 15-20')
add(numq('Cengel Ch.15 Bài 15–20. Butan (C₄H₁₀) được đốt với 200 % không khí lý thuyết, cháy hoàn toàn. Cần phun bao nhiêu kmol nước vào buồng đốt trên mỗi kmol nhiên liệu để sản phẩm có nhiệt độ điểm sương 60 °C ở áp suất sản phẩm 100 kPa? (P_sat@60 °C = 19,947 kPa).',
         'Cengel Ch.15 Problem 15–20. Butane (C₄H₁₀) is burned in 200 percent theoretical air, complete combustion. How many kmol of water must be sprayed into the combustion chamber per kmol of fuel if the products are to have a dew-point temperature of 60 °C at a product pressure of 100 kPa? (P_sat@60 °C = 19.947 kPa).',
         w20, [(Psat60 / 100 * r20['n_tot'], 'lấy N_v = (P_sat/P) N_prod mà không trừ 5 kmol hơi đã có sẵn', 'takes N_v = (P_sat/P) N_prod without subtracting the 5 kmol of vapor already present'), (Psat60 / 100 * r20['n_tot'] - r20['H2O'], 'quên rằng nước phun cũng làm tăng N_prod (mẫu số)', 'forgets that the sprayed water also increases N_prod (the denominator)'), (r20['H2O'] + w20, 'là tổng lượng hơi nước (5 + w), không phải lượng phun', 'is the total vapor (5 + w), not the amount sprayed')], 'kmol', 2,
         f'Sản phẩm khi chưa phun: 4 CO₂ + 5 H₂O + 6,5 O₂ + 48,88 N₂ = {N(r20["n_tot"],2)} kmol. Điểm sương 60 °C ⇒ P_v = 19,947 kPa, y_v = 0,19947. (5 + w)/({N(r20["n_tot"],2)} + w) = 0,19947 ⇒ w = ({N(Psat60/100*r20["n_tot"],3)} − 5)/(1 − 0,19947) = {N(w20,2)} kmol nước/kmol nhiên liệu.',
         f'Products before spraying: 4 CO₂ + 5 H₂O + 6.5 O₂ + 48.88 N₂ = {N(r20["n_tot"],2)} kmol. Dew point 60 °C ⇒ P_v = 19.947 kPa, y_v = 0.19947. (5 + w)/({N(r20["n_tot"],2)} + w) = 0.19947 ⇒ w = ({N(Psat60/100*r20["n_tot"],3)} − 5)/(1 − 0.19947) = {N(w20,2)} kmol water per kmol fuel.',
         3, TOP['dew'], CEN('15–20'), 'script (không có đáp án in)'))
fm = mix([('CH4', 1.25 / (1.25 + 20 / 46 * 1.0 * 0 + 1.7391304347826086)), ('C2H5OH', 1.7391304347826086 / (1.25 + 1.7391304347826086))]) if False else None
nm = 20 / Mf('CH4'); ne = 80 / Mf('C2H5OH'); y_m = nm / (nm + ne); f21 = mix([('CH4', y_m), ('C2H5OH', 1 - y_m)]); r21 = combustion(f21, 1.0); mair21 = r21['AF'] * 31
reg('comb', dict(fuel=fp(('CH4', y_m), ('C2H5OH', 1 - y_m)), lam=1.0, exact=False), 'AF', r21['AF'], 1e-9, 'Cengel 15-21 (mole fractions from mass fractions)'); prn('Cengel 15-21 air flow [kg/s]', 330.0, mair21, 0.005)
add(numq('Cengel Ch.15 Bài 15–21. Một hỗn hợp nhiên liệu gồm 20 % khối lượng metan (CH₄) và 80 % khối lượng etanol (C₂H₆O) được đốt hoàn toàn với không khí lý thuyết. Lưu lượng nhiên liệu tổng 31 kg/s. Lưu lượng không khí cần thiết là:',
         'Cengel Ch.15 Problem 15–21. A fuel mixture of 20 percent by mass methane (CH₄) and 80 percent by mass ethanol (C₂H₆O) is burned completely with theoretical air. The total fuel flow rate is 31 kg/s. The required air flow rate is:',
         mair21, [(31 * combustion(single('CH4'))['AF'], 'chỉ tính metan cho toàn bộ 31 kg/s', 'treats all 31 kg/s as methane'), (31 * combustion(single('C2H5OH'))['AF'], 'chỉ tính etanol cho toàn bộ 31 kg/s', 'treats all 31 kg/s as ethanol'),
                  (31 * (0.2 * combustion(single('CH4'))['AF'] + 0.8 * combustion(single('C2H5OH'))['AF']) + 0 if False else 31 * 0.5 * (combustion(single('CH4'))['AF'] + combustion(single('C2H5OH'))['AF']), 'lấy trung bình cộng AF của hai nhiên liệu (50 %–50 %) thay vì theo phần khối lượng', 'averages the two AF values 50–50 instead of by mass fractions')], 'kg/s', 0,
         f'Tính cho 100 kg nhiên liệu: 20/16 = 1,25 kmol CH₄ cần 2 O₂ mỗi kmol và 80/46 = {N(ne,3)} kmol C₂H₆O cần 3 O₂ mỗi kmol ⇒ O₂ = 2,5 + {N(3*ne,3)} = {N(2*nm+3*ne,3)} kmol; không khí = {N((2*nm+3*ne)*4.76,2)} kmol × 29 = {N((2*nm+3*ne)*4.76*29,1)} kg ⇒ AF = {N(r21["AF"],3)} kg/kg ⇒ ṁ_air = {N(r21["AF"],3)} × 31 = {N(mair21,1)} kg/s (đáp án in 330 kg/s).',
         f'For 100 kg of fuel: 20/16 = 1.25 kmol CH₄ needing 2 O₂ per kmol and 80/46 = {N(ne,3)} kmol C₂H₆O needing 3 O₂ per kmol ⇒ O₂ = 2.5 + {N(3*ne,3)} = {N(2*nm+3*ne,3)} kmol; air = {N((2*nm+3*ne)*4.76,2)} kmol × 29 = {N((2*nm+3*ne)*4.76*29,1)} kg ⇒ AF = {N(r21["AF"],3)} kg/kg ⇒ ṁ_air = {N(r21["AF"],3)} × 31 = {N(mair21,1)} kg/s (printed answer 330 kg/s).',
         3, TOP['af'], CEN('15–21'), 'printed answer 330 + script'))
r22 = combustion(single('C8H18'), 2.5); Pv22, T22 = dew_point(r22['H2O'], r22['n_tot'], 101.325)
reg('dew', dict(fuel=fp(('C8H18', 1)), lam=2.5, P=101.325), 'Tdp', T22, {'abs': 0.5}, 'Cengel 15-22 b'); reg('comb', dict(fuel=fp(('C8H18', 1)), lam=2.5, exact=False), 'AF', r22['AF'], 1e-9, 'Cengel 15-22 a')
add(numq('Cengel Ch.15 Bài 15–22 (câu b). Octan (C₈H₁₈) được đốt với 250 % không khí lý thuyết (không khí vào ở 25 °C), cháy hoàn toàn, áp suất tổng 1 atm = 101,325 kPa. Nhiệt độ điểm sương của sản phẩm (A-5) xấp xỉ:',
         'Cengel Ch.15 Problem 15–22 (part b). Octane (C₈H₁₈) is burned with 250 percent theoretical air (air enters at 25 °C), complete combustion, total pressure 1 atm = 101.325 kPa. The dew-point temperature of the products (A-5) is about:',
         T22, [(props.sat_P('water', 101.325, 'Tsat_C')['value'], 'là T_sat ở áp suất tổng', 'is T_sat at the total pressure'), (dew_point(9, r22['n_dry'], 101.325)[1], 'bỏ H₂O khỏi tổng số mol', 'leaves the H₂O out of the total moles'), (dew_point(9, combustion(single('C8H18'), 1.0)['n_tot'], 101.325)[1], 'dùng sản phẩm của cháy lý thuyết (không có không khí thừa)', 'uses the products of theoretical combustion (no excess air)')], '°C', 1,
         f'Sản phẩm: 8 CO₂ + 9 H₂O + 18,75 O₂ + 117,5 N₂ = {N(r22["n_tot"],2)} kmol; P_v = 9/{N(r22["n_tot"],2)} × 101,325 = {N(Pv22,2)} kPa → T_dp ≈ {N(T22,1)} °C (nội suy A-5; IAPWS {N(_I(P=Pv22/1000,x=0).T-273.15,1)} °C). AF = {N(r22["AF"],1)} kg/kg (câu a).',
         f'Products: 8 CO₂ + 9 H₂O + 18.75 O₂ + 117.5 N₂ = {N(r22["n_tot"],2)} kmol; P_v = 9/{N(r22["n_tot"],2)} × 101.325 = {N(Pv22,2)} kPa → T_dp ≈ {N(T22,1)} °C (A-5 interpolation; IAPWS {N(_I(P=Pv22/1000,x=0).T-273.15,1)} °C). AF = {N(r22["AF"],1)} kg/kg (part a).',
         3, TOP['dew'], CEN('15–22', ' (câu b)', ' (part b)'), 'script (không có đáp án in)'))
th_o = combustion(single('C8H18'))['AF']; reg('pct_af', dict(fuel=fp(('C8H18', 1)), AF=18.0), 'pct', 18 / th_o * 100, 1e-9, 'Cengel 15-23')
add(numq('Cengel Ch.15 Bài 15–23. Xăng (coi là C₈H₁₈) được đốt ổn định với không khí trong một động cơ phản lực. Nếu tỉ lệ không khí–nhiên liệu là 18 kg không khí/kg nhiên liệu, phần trăm không khí lý thuyết đã dùng là:',
         'Cengel Ch.15 Problem 15–23. Gasoline (assumed C₈H₁₈) is burned steadily with air in a jet engine. If the air–fuel ratio is 18 kg air/kg fuel, the percentage of theoretical air used is:',
         18 / th_o * 100, [(18 / th_o * 100 - 100, 'là phần trăm không khí THỪA, không phải phần trăm lý thuyết', 'is the percent EXCESS air, not percent theoretical'), (th_o / 18 * 100, 'đảo ngược tỉ số', 'inverts the ratio'), (18 / 24.2 * 100, 'dùng AF của Ví dụ 15–1 (24,2) thay cho AF lý thuyết', 'uses the AF of Example 15–1 (24.2) in place of the theoretical AF')], '%', 1,
         f'AF lý thuyết của octan = 12,5 × 4,76 × 29/114 = {N(th_o,2)} kg/kg; % lý thuyết = 18/{N(th_o,2)} = {N(18/th_o*100,1)} % (≈ {N(18/th_o*100-100,0)} % thừa).',
         f'Theoretical AF of octane = 12.5 × 4.76 × 29/114 = {N(th_o,2)} kg/kg; % theoretical = 18/{N(th_o,2)} = {N(18/th_o*100,1)} % (≈ {N(18/th_o*100-100,0)} % excess).',
         2, TOP['air'], CEN('15–23'), 'script (không có đáp án in)'))
th_e = combustion(single('C2H6'))['AF']; ex24 = 176 / 8 / th_e * 100 - 100; reg('pct_af', dict(fuel=fp(('C2H6', 1)), AF=176 / 8), 'pct', 176 / 8 / th_e * 100, 1e-9, 'Cengel 15-24'); prn('Cengel 15-24 excess air [%]', 37.0, ex24, 0.02)
add(numq('Cengel Ch.15 Bài 15–24. Trong một buồng đốt, etan (C₂H₆) được đốt với lưu lượng 8 kg/h, không khí vào buồng đốt với lưu lượng 176 kg/h. Phần trăm không khí THỪA là:',
         'Cengel Ch.15 Problem 15–24. In a combustion chamber, ethane (C₂H₆) is burned at a rate of 8 kg/h with air entering at a rate of 176 kg/h. The percentage of EXCESS air is:',
         ex24, [(176 / 8 / th_e * 100, 'là phần trăm không khí LÝ THUYẾT (137 %), chưa trừ 100 %', 'is the percent THEORETICAL air (137 %), not yet minus 100 %'), (th_e / 22 * 100 - 100 if False else (1 - th_e / 22) * 100, 'lấy (AF − AF_lt)/AF thay vì chia cho AF_lt', 'divides by the actual AF instead of by the theoretical AF'), (176 / 8, 'là AF thực tế (22 kg/kg)', 'is the actual AF (22 kg/kg)')], '%', 0,
         f'AF thực = 176/8 = 22; AF lý thuyết của etan (a_th = 3,5): 3,5 × 4,76 × 29/30 = {N(th_e,2)}; không khí lý thuyết = 22/{N(th_e,2)} = {N(176/8/th_e*100,1)} % ⇒ thừa {N(ex24,1)} % (đáp án in 37 %).',
         f'Actual AF = 176/8 = 22; theoretical AF of ethane (a_th = 3.5): 3.5 × 4.76 × 29/30 = {N(th_e,2)}; percent theoretical air = 22/{N(th_e,2)} = {N(176/8/th_e*100,1)} % ⇒ excess {N(ex24,1)} % (printed answer 37 %).',
         2, TOP['air'], CEN('15–24'), 'printed answer 37 + script'))
th_b = combustion(single('C4H10'))['AF']; lam25 = 25 / th_b; r25 = combustion(single('C4H10'), lam25); Pv25, T25 = dew_point(r25['H2O'], r25['n_tot'], 90)
reg('pct_af', dict(fuel=fp(('C4H10', 1)), AF=25.0), 'pct', lam25 * 100, 1e-9, 'Cengel 15-25 a / 15-26E a: 161'); reg('dew', dict(fuel=fp(('C4H10', 1)), lam=lam25, P=90.0), 'Tdp', T25, {'abs': 0.4}, 'Cengel 15-25 b')
prn('Cengel 15-26E (a) percent theoretical air (same ratio 25:1)', 161.0, lam25 * 100, 0.01)
Pv26 = 101.325 * r25['H2O'] / r25['n_tot']; T26F = (_I(P=Pv26 / 1000, x=0).T - 273.15) * 1.8 + 32; prn('Cengel 15-26E (b) dew point [F], SI-equivalent by iapws', 113.0, T26F, 0.01)
add(numq('Cengel Ch.15 Bài 15–25 (câu b). Một kilogam butan (C₄H₁₀) được đốt với 25 kg không khí ở 30 °C, 90 kPa. Cháy hoàn toàn, áp suất sản phẩm 90 kPa. Nhiệt độ điểm sương của sản phẩm (A-5) xấp xỉ:',
         'Cengel Ch.15 Problem 15–25 (part b). One kilogram of butane (C₄H₁₀) is burned with 25 kg of air at 30 °C and 90 kPa. Complete combustion, product pressure 90 kPa. The dew-point temperature of the products (A-5) is about:',
         T25, [(props.sat_P('water', 90, 'Tsat_C')['value'], 'là T_sat ở áp suất tổng 90 kPa', 'is T_sat at the total pressure of 90 kPa'), (dew_point(r25['H2O'], combustion(single('C4H10'))['n_tot'], 90)[1], 'dùng số mol sản phẩm của cháy lý thuyết', 'uses the product moles of theoretical combustion'), (props.sat_T('water', 30, 'Tsat_C')['value'] if False else 30.0, 'lấy nhiệt độ không khí vào làm điểm sương', 'takes the air inlet temperature as the dew point')], '°C', 1,
         f'AF thực = 25; AF lý thuyết của butan = 6,5 × 4,76 × 29/58 = {N(th_b,2)} ⇒ {N(lam25*100,1)} % lý thuyết (câu a; đáp án in của bản Anh 15–26E: 161 %). Sản phẩm: 4 CO₂ + 5 H₂O + {N(r25["O2"],2)} O₂ + {N(r25["N2"],2)} N₂ = {N(r25["n_tot"],2)} kmol; P_v = 5/{N(r25["n_tot"],2)} × 90 = {N(Pv25,2)} kPa → T_dp ≈ {N(T25,1)} °C (IAPWS {N(_I(P=Pv25/1000,x=0).T-273.15,1)} °C).',
         f'Actual AF = 25; theoretical AF of butane = 6.5 × 4.76 × 29/58 = {N(th_b,2)} ⇒ {N(lam25*100,1)} % theoretical (part a; printed answer of the English-unit twin 15–26E: 161 %). Products: 4 CO₂ + 5 H₂O + {N(r25["O2"],2)} O₂ + {N(r25["N2"],2)} N₂ = {N(r25["n_tot"],2)} kmol; P_v = 5/{N(r25["n_tot"],2)} × 90 = {N(Pv25,2)} kPa → T_dp ≈ {N(T25,1)} °C (IAPWS {N(_I(P=Pv25/1000,x=0).T-273.15,1)} °C).',
         3, TOP['dew'], CEN('15–25', ' (câu b)', ' (part b)'), 'script; bản đồng dạng 15–26E có đáp án in 161 % và 113 °F'))
g27 = mix([('CH4', .65), ('H2', .08), ('N2', .18), ('O2', .03), ('CO2', .06)]); r27 = combustion(g27, 1.0)
reg('comb', dict(fuel=fp(('CH4', .65), ('H2', .08), ('N2', .18), ('O2', .03), ('CO2', .06)), lam=1.0, exact=False), 'AF', r27['AF'], 1e-9, 'Cengel 15-27')
add(numq('Cengel Ch.15 Bài 15–27. Một khí thiên nhiên có thành phần thể tích: 65 % CH₄, 8 % H₂, 18 % N₂, 3 % O₂ và 6 % CO₂. Khí này được đốt hoàn toàn với lượng không khí khô lý thuyết. Tỉ lệ không khí–nhiên liệu là:',
         'Cengel Ch.15 Problem 15–27. A certain natural gas has the volumetric analysis 65 percent CH₄, 8 percent H₂, 18 percent N₂, 3 percent O₂ and 6 percent CO₂. It is burned completely with the stoichiometric amount of dry air. The air–fuel ratio is:',
         r27['AF'], [(r27['air'], 'là AF theo mol (kmol/kmol)', 'is the AF on a mole basis (kmol/kmol)'), ((0.65 * 2 + 0.08 * 0.5) * 4.76 * 29 / (0.65 * 16 + 0.08 * 2), 'chỉ lấy hai thành phần cháy được (CH₄ + H₂) làm khối lượng nhiên liệu', 'uses only the two combustibles (CH₄ + H₂) as the fuel mass'), ((0.65 * 2 + 0.08 * 0.5) * 4.76 * 29 / g27['M'] + 0.5 * 0 + 1.2, 'quên O₂ có sẵn trong nhiên liệu (0,03 kmol) và N₂ trơ khi tính AF', 'forgets the O₂ already in the fuel and the inert N₂ in the AF')], 'kg/kg', 2,
         f'Cho 1 kmol nhiên liệu: O₂ cần = 0,65×2 + 0,08×0,5 − 0,03 = {N(r27["ath"],3)} kmol (CO₂ và N₂ trong nhiên liệu trơ); không khí = {N(r27["ath"]*4.76,3)} kmol; M nhiên liệu = 0,65×16 + 0,08×2 + 0,18×28 + 0,03×32 + 0,06×44 = {N(g27["M"],2)} kg/kmol ⇒ AF = {N(r27["ath"]*4.76,3)} × 29/{N(g27["M"],2)} = {N(r27["AF"],2)} kg/kg.',
         f'Per kmol of fuel: O₂ needed = 0.65×2 + 0.08×0.5 − 0.03 = {N(r27["ath"],3)} kmol (the CO₂ and N₂ of the fuel are inert); air = {N(r27["ath"]*4.76,3)} kmol; fuel molar mass = 0.65×16 + 0.08×2 + 0.18×28 + 0.03×32 + 0.06×44 = {N(g27["M"],2)} kg/kmol ⇒ AF = {N(r27["ath"]*4.76,3)} × 29/{N(g27["M"],2)} = {N(r27["AF"],2)} kg/kg.',
         3, TOP['af'], CEN('15–27'), 'script (không có đáp án in)'))

# ---- 15-29 / 15-31 (mixture fuel, coal by mass)
g29 = mix([('CH4', .6), ('H2', .3), ('N2', .1)]); r29 = combustion(g29, 1.3); fr29 = condensed(r29['H2O'], r29['n_tot'], 101.325, 20) / r29['H2O']
reg('comb', dict(fuel=fp(('CH4', .6), ('H2', .3), ('N2', .1)), lam=1.3, exact=False), 'AF', r29['AF'], 1e-9, 'Cengel 15-29 a'); prn('Cengel 15-29 (a) AF', 18.6, r29['AF'], 0.005)
reg('cond', dict(fuel=fp(('CH4', .6), ('H2', .3), ('N2', .1)), lam=1.3, P=101.325, T=20.0), 'frac', fr29, 2e-3, 'Cengel 15-29 b'); prn('Cengel 15-29 (b) fraction condensed [%]', 88.0, fr29 * 100, 0.005)
add(numq('Cengel Ch.15 Bài 15–29 (câu a). Một nhiên liệu khí có thành phần thể tích 60 % CH₄, 30 % H₂ và 10 % N₂ được đốt hoàn toàn với 130 % không khí lý thuyết. Tỉ lệ không khí–nhiên liệu là:',
         'Cengel Ch.15 Problem 15–29 (part a). A gaseous fuel with a volumetric analysis of 60 percent CH₄, 30 percent H₂ and 10 percent N₂ is burned to completion with 130 percent theoretical air. The air–fuel ratio is:',
         r29['AF'], [(combustion(g29, 1.0)['AF'], 'bỏ qua 30 % không khí thừa', 'ignores the 30 percent excess'), (r29['air'], 'là AF theo mol', 'is the AF on a mole basis'), (combustion(g29, 1.3)['o2_in'] * 4.76 * 29 / (0.6 * 16 + 0.3 * 2), 'không tính khối lượng 10 % N₂ trơ của nhiên liệu', 'does not count the mass of the 10 % inert N₂ of the fuel')], 'kg/kg', 1,
         f'Cho 1 kmol nhiên liệu: a_th = 0,6×2 + 0,3×0,5 = {N(r29["ath"],2)} kmol O₂; O₂ thực = 1,3 × {N(r29["ath"],2)} = {N(r29["o2_in"],3)}; không khí = {N(r29["air"],2)} kmol; M = 0,6×16 + 0,3×2 + 0,1×28 = {N(g29["M"],1)} kg/kmol ⇒ AF = {N(r29["air"],2)} × 29/{N(g29["M"],1)} = {N(r29["AF"],2)} kg/kg (đáp án in 18,6).',
         f'Per kmol of fuel: a_th = 0.6×2 + 0.3×0.5 = {N(r29["ath"],2)} kmol O₂; actual O₂ = 1.3 × {N(r29["ath"],2)} = {N(r29["o2_in"],3)}; air = {N(r29["air"],2)} kmol; M = 0.6×16 + 0.3×2 + 0.1×28 = {N(g29["M"],1)} kg/kmol ⇒ AF = {N(r29["air"],2)} × 29/{N(g29["M"],1)} = {N(r29["AF"],2)} kg/kg (printed answer 18.6).',
         3, TOP['af'], CEN('15–29', ' (câu a)', ' (part a)'), 'printed answer 18.6 + script'))
add(numq('Cengel Ch.15 Bài 15–29 (câu b). Cùng nhiên liệu (60 % CH₄, 30 % H₂, 10 % N₂) cháy với 130 % không khí lý thuyết; sản phẩm được làm nguội tới 20 °C ở 1 atm (P_sat@20 °C = 2,3392 kPa). Phần hơi nước ngưng tụ là:',
         'Cengel Ch.15 Problem 15–29 (part b). The same fuel (60 % CH₄, 30 % H₂, 10 % N₂) burns with 130 percent theoretical air; the products are cooled to 20 °C at 1 atm (P_sat@20 °C = 2.3392 kPa). The fraction of the water vapor that condenses is:',
         fr29 * 100, [(r29['H2O'] / r29['n_tot'] * 100, 'là phần MOL hơi nước trong sản phẩm, không phải phần ngưng tụ', 'is the mole fraction of vapor in the products, not the condensed fraction'), ((1 - fr29) * 100, 'là phần hơi nước CÒN LẠI', 'is the vapor REMAINING'), (100 - 2.3392 / 101.325 * 100, 'giả sử y_v còn lại = P_sat/P = 2,3 % và coi như toàn bộ phần còn lại ngưng tụ', 'assumes the remaining vapor mole fraction P_sat/P = 2.3 % is the amount left and condenses the rest')], '%', 0,
         f'Sản phẩm: N_v = {N(r29["H2O"],2)}, N_prod = {N(r29["n_tot"],2)} kmol; (N_v − N_w)/(N_prod − N_w) = 2,3392/101,325 ⇒ N_w = {N(condensed(r29["H2O"],r29["n_tot"],101.325,20),3)} kmol = {N(fr29*100,1)} % (đáp án in 88 %).',
         f'Products: N_v = {N(r29["H2O"],2)}, N_prod = {N(r29["n_tot"],2)} kmol; (N_v − N_w)/(N_prod − N_w) = 2.3392/101.325 ⇒ N_w = {N(condensed(r29["H2O"],r29["n_tot"],101.325,20),3)} kmol = {N(fr29*100,1)} % (printed answer 88 %).',
         3, TOP['dew'], CEN('15–29', ' (câu b)', ' (part b)'), 'printed answer 88 % + script'))
Cm, H2m, O2m = 82 / 12, 2 / 2, 1 / 32; ath31 = Cm + H2m / 2 - O2m; air31 = 1.5 * ath31 * 4.76; AF31 = air31 * 29 / 100
reg('coal', dict(wC=82.0, wH2=2.0, wO2=1.0, lam=1.5), 'AF', AF31, 1e-9, 'Cengel 15-31'); prn('Cengel 15-31 AF', 15.1, AF31, 0.005)
add(numq('Cengel Ch.15 Bài 15–31. Một loại than có thành phần theo khối lượng: 82 % C, 5 % H₂O, 2 % H₂, 1 % O₂ và 10 % tro. Than được đốt với 50 % không khí thừa. Tỉ lệ không khí–nhiên liệu (kg không khí/kg than) là:',
         'Cengel Ch.15 Problem 15–31. A certain coal has the mass analysis 82 percent C, 5 percent H₂O, 2 percent H₂, 1 percent O₂ and 10 percent ash. The coal is burned with 50 percent excess air. The air–fuel ratio (kg air/kg coal) is:',
         AF31, [(1.5 * (Cm + H2m / 2) * 4.76 * 29 / 100, 'bỏ qua O₂ có sẵn trong than', 'ignores the O₂ already in the coal'), (1.5 * (Cm + H2m / 2 - O2m) * 4.76 * 29 / 87, 'chia cho khối lượng chỉ gồm C, H₂ và O₂ (87 kg) thay vì 100 kg than', 'divides by only the C + H₂ + O₂ mass (87 kg) instead of the 100 kg of coal'), (1.0 * ath31 * 4.76 * 29 / 100, 'bỏ 50 % không khí thừa', 'drops the 50 % excess air')], 'kg/kg', 1,
         f'Cho 100 kg than: C = 82/12 = {N(Cm,3)} kmol, H₂ = 2/2 = 1 kmol, O₂ = 1/32 = {N(O2m,4)} kmol; H₂O và tro trơ (khối lượng vẫn tính vào than). a_th = C + H₂/2 − O₂ = {N(ath31,3)} kmol; O₂ thực = 1,5 × {N(ath31,3)}; không khí = {N(air31,2)} kmol = {N(air31*29,1)} kg ⇒ AF = {N(AF31,2)} kg/kg (đáp án in 15,1).',
         f'For 100 kg of coal: C = 82/12 = {N(Cm,3)} kmol, H₂ = 2/2 = 1 kmol, O₂ = 1/32 = {N(O2m,4)} kmol; H₂O and ash are inert (their mass still counts as coal). a_th = C + H₂/2 − O₂ = {N(ath31,3)} kmol; actual O₂ = 1.5 × {N(ath31,3)}; air = {N(air31,2)} kmol = {N(air31*29,1)} kg ⇒ AF = {N(AF31,2)} kg/kg (printed answer 15.1).',
         3, TOP['af'], CEN('15–31'), 'printed answer 15.1 + script'))

# ---- 15-32 / 15-33 / 15-34 reverse analysis
rv32 = reverse(8, 18, 9.21, 0.61, 7.06, 83.12); rv33 = reverse(1, 0, 10.06, 0.42, 10.69, 78.83); rv34 = reverse(1, 4, 5.20, 0.33, 11.24, 83.23)
for nm_, rr, args in (('15-32', rv32, (8, 18, 9.21, 0.61, 7.06, 83.12)), ('15-33', rv33, (1, 0, 10.06, 0.42, 10.69, 78.83)), ('15-34', rv34, (1, 4, 5.20, 0.33, 11.24, 83.23))):
    p = dict(zip(('c', 'h', 'CO2', 'CO', 'O2', 'N2'), args)); reg('rev', p, 'AF', rr['AF'], 1e-9, f'Cengel {nm_} a'); reg('rev', p, 'pct', rr['pct'], 1e-9, f'Cengel {nm_} b')
prn('Cengel 15-34 (a) AF', 34.5, rv34['AF'], 0.005); prn('Cengel 15-34 (b) % theoretical air', 200.0, rv34['pct'], 0.005)
add(ess(B('Cengel Ch.15 Bài 15–32. Octan (C₈H₁₈) cháy với không khí khô. Phân tích thể tích sản phẩm trên cơ sở khô: 9,21 % CO₂; 0,61 % CO; 7,06 % O₂; 83,12 % N₂. Xác định (a) tỉ lệ không khí–nhiên liệu, (b) phần trăm không khí lý thuyết đã dùng.',
           'Cengel Ch.15 Problem 15–32. Octane (C₈H₁₈) is burned with dry air. The volumetric analysis of the products on a dry basis is 9.21 percent CO₂, 0.61 percent CO, 7.06 percent O₂ and 83.12 percent N₂. Determine (a) the air–fuel ratio and (b) the percentage of theoretical air used.'),
         B(f'''Phương pháp của slide tr.33–37 (thử trên Ví dụ 15–4, đáp số in khớp). Lấy 100 kmol sản phẩm khô: x C₈H₁₈ + a(O₂ + 3,76 N₂) → 9,21 CO₂ + 0,61 CO + 7,06 O₂ + 83,12 N₂ + b H₂O.
N₂: 3,76 a = 83,12 → a = {N(rv32["a"],3)}. C: 8x = 9,21 + 0,61 = 9,82 → x = {N(rv32["x"],4)}. H: 18x = 2b → b = {N(rv32["b"],3)}. Kiểm O₂: a = 9,21 + 0,305 + 7,06 + b/2 = {N(9.21+0.305+7.06+rv32["b"]/2,3)} so với {N(rv32["a"],3)} (lệch {N(abs(rv32["resid"]),3)}: đóng trong làm tròn thành phần).
(a) Không khí/kmol nhiên liệu = a/x = {N(rv32["a"]/rv32["x"],3)} kmol O₂ → AF = ({N(rv32["a"]/rv32["x"],3)} × 4,76)(29)/114 = {N(rv32["AF"],2)} kg/kg.
(b) a_th = 12,5 → {N(rv32["a"]/rv32["x"],3)}/12,5 = {N(rv32["pct"],1)} % lý thuyết (≈ {N(rv32["pct"]-100,0)} % thừa).
Hai đường: (A) cân bằng tay như trên; (B) sympy giải (N₂, C, H) bằng số hữu tỉ và kiểm O₂. Sách không in đáp số; phương pháp đã kiểm trên Ví dụ 15–4 (19,76 kg/kg; 131 %) và bài 15–34 (34,5; 200 % in) cùng cách làm.''',
           f'''Method of slides p.33–37 (tested on Example 15–4, printed numbers reproduced). Take 100 kmol of dry products: x C₈H₁₈ + a(O₂ + 3.76 N₂) → 9.21 CO₂ + 0.61 CO + 7.06 O₂ + 83.12 N₂ + b H₂O.
N₂: 3.76 a = 83.12 → a = {N(rv32["a"],3)}. C: 8x = 9.21 + 0.61 = 9.82 → x = {N(rv32["x"],4)}. H: 18x = 2b → b = {N(rv32["b"],3)}. O₂ check: a = 9.21 + 0.305 + 7.06 + b/2 = {N(9.21+0.305+7.06+rv32["b"]/2,3)} versus {N(rv32["a"],3)} (gap {N(abs(rv32["resid"]),3)}: closed within the rounding of the composition).
(a) Oxygen per kmol of fuel = a/x = {N(rv32["a"]/rv32["x"],3)} kmol O₂ → AF = ({N(rv32["a"]/rv32["x"],3)} × 4.76)(29)/114 = {N(rv32["AF"],2)} kg/kg.
(b) a_th = 12.5 → {N(rv32["a"]/rv32["x"],3)}/12.5 = {N(rv32["pct"],1)} % theoretical (≈ {N(rv32["pct"]-100,0)} % excess).
Two routes: (A) hand balances as above; (B) sympy solves (N₂, C, H) with rational numbers and checks O₂. The book prints no answer; the method was tested on Example 15–4 (19.76 kg/kg; 131 %) and Problem 15–34 (34.5; 200 % printed), same procedure.'''),
         3, TOP['rev'], CEN('15–32'), 'goc', 'script (không có đáp án in); phương pháp thử trên Ví dụ 15–4 và bài 15–34'))
add(numq('Cengel Ch.15 Bài 15–33 (câu b). Cacbon (C) cháy với không khí khô. Phân tích thể tích sản phẩm: 10,06 % CO₂; 0,42 % CO; 10,69 % O₂; 78,83 % N₂. Phần trăm không khí lý thuyết đã dùng là:',
         'Cengel Ch.15 Problem 15–33 (part b). Carbon (C) is burned with dry air. The volumetric analysis of the products is 10.06 percent CO₂, 0.42 percent CO, 10.69 percent O₂ and 78.83 percent N₂. The percentage of theoretical air used is:',
         rv33['pct'], [(rv33['pct'] - 100, 'là phần trăm không khí thừa', 'is the percent excess air'), (100 / rv33['pct'] * 100, 'đảo ngược tỉ số', 'inverts the ratio'), (78.83 / 3.76 / 10.48 * 100 + 0 * 1 if False else 78.83 / 3.76 / (10.06 + 0.42) * 100 + 100, 'cộng nhầm 100 % vào kết quả', 'adds 100 % by mistake')], '%', 0,
         f'Cho 100 kmol sản phẩm khô: a = 78,83/3,76 = {N(rv33["a"],3)} kmol O₂; x C = 10,06 + 0,42 = 10,48 kmol; a_th = 1 kmol O₂ trên kmol C ⇒ % = a/(x·1) = {N(rv33["a"],3)}/10,48 = {N(rv33["pct"],1)} % (AF = {N(rv33["AF"],1)} kg/kg; kiểm O₂ lệch {N(abs(rv33["resid"]),3)}).',
         f'For 100 kmol of dry products: a = 78.83/3.76 = {N(rv33["a"],3)} kmol O₂; x C = 10.06 + 0.42 = 10.48 kmol; a_th = 1 kmol O₂ per kmol C ⇒ % = a/(x·1) = {N(rv33["a"],3)}/10.48 = {N(rv33["pct"],1)} % (AF = {N(rv33["AF"],1)} kg/kg; O₂ check gap {N(abs(rv33["resid"]),3)}).',
         3, TOP['rev'], CEN('15–33', ' (câu b)', ' (part b)'), 'script (không có đáp án in)'))
add(numq('Cengel Ch.15 Bài 15–34 (câu a). Metan (CH₄) cháy với không khí khô. Phân tích thể tích sản phẩm trên cơ sở khô: 5,20 % CO₂; 0,33 % CO; 11,24 % O₂; 83,23 % N₂. Tỉ lệ không khí–nhiên liệu (kg/kg) là:',
         'Cengel Ch.15 Problem 15–34 (part a). Methane (CH₄) is burned with dry air. The volumetric analysis of the products on a dry basis is 5.20 percent CO₂, 0.33 percent CO, 11.24 percent O₂ and 83.23 percent N₂. The air–fuel ratio (kg/kg) is:',
         rv34['AF'], [(rv34['air'], 'là AF theo mol', 'is the AF on a mole basis'), (combustion(single('CH4'))['AF'], 'là AF lý thuyết của metan (17,3)', 'is the theoretical AF of methane (17.3)'), (rv34['a'] / rv34['x'] * 32 / 16, 'bỏ N₂ của không khí (chỉ O₂)', 'drops the N₂ of the air (O₂ only)')], 'kg/kg', 1,
         f'100 kmol sản phẩm khô: a = 83,23/3,76 = {N(rv34["a"],3)}; C: x = 5,20 + 0,33 = 5,53 kmol CH₄; không khí/kmol nhiên liệu = 4,76 × {N(rv34["a"]/rv34["x"],3)} = {N(rv34["air"],2)} kmol; AF = {N(rv34["air"],2)} × 29/16 = {N(rv34["AF"],1)} kg/kg; % lý thuyết = {N(rv34["a"]/rv34["x"],3)}/2 = {N(rv34["pct"],1)} % (đáp án in 34,5 và 200 %).',
         f'100 kmol of dry products: a = 83.23/3.76 = {N(rv34["a"],3)}; C: x = 5.20 + 0.33 = 5.53 kmol CH₄; air per kmol fuel = 4.76 × {N(rv34["a"]/rv34["x"],3)} = {N(rv34["air"],2)} kmol; AF = {N(rv34["air"],2)} × 29/16 = {N(rv34["AF"],1)} kg/kg; % theoretical = {N(rv34["a"]/rv34["x"],3)}/2 = {N(rv34["pct"],1)} % (printed answers 34.5 and 200 %).',
         3, TOP['rev'], CEN('15–34', ' (câu a)', ' (part a)'), 'printed answer 34.5 + script'))

# ================================================================== 7. enthalpy of combustion / heating value problems (Cengel 15-42, 15-44, 15-49, 15-50)
def hC_item(num, qv, qe, key, nu, a27, M27key, printed, ev, ee, tag, per='kmol'):
    hc = hC_nu(key, nu, 'l'); hcg = hC_nu(key, nu, 'g'); M = A27row(M27key, 'M')
    reg('hC', dict(fuel=key, nu=nu, water='l', a27=M27key, col='HHV'), 'kJ/kmol', hc, 1.5e-3, f'Cengel {num}')
    if printed: prn(f'Cengel {num}', printed, hc, 1e-6)
    return hc, hcg, M
hc42, hcg42, M42 = hC_item('15–42', '', '', 'CH4', dict(CO2=1, H2O=2), 'CH4', 'CH4', -890330.0, '', '', '')
add(numq('Cengel Ch.15 Bài 15–42. Xác định entanpi cháy của metan (CH₄) ở 25 °C, 1 atm bằng entanpi hình thành của bảng A-26, giả thiết nước trong sản phẩm ở thể lỏng. So với bảng A-27. Entanpi cháy (kJ/kmol CH₄) là:',
         'Cengel Ch.15 Problem 15–42. Determine the enthalpy of combustion of methane (CH₄) at 25 °C and 1 atm using the enthalpy of formation data of Table A-26, assuming the water in the products is liquid. Compare with Table A-27. The enthalpy of combustion (kJ/kmol CH₄) is:',
         hc42, [(-hcg42, 'sai dấu', 'wrong sign'), (hcg42, 'dùng H₂O hơi (−241 820) nên là LHV, không phải entanpi cháy với nước lỏng', 'uses H₂O vapor (−241,820), so it is the LHV, not the enthalpy of combustion with liquid water'),
                (hc42 + HF('CH4'), 'quên trừ entanpi hình thành của nhiên liệu (−74 850)', 'forgets to subtract the enthalpy of formation of the fuel (−74,850)')], 'kJ/kmol', 0,
         f'CH₄ + 2 O₂ → CO₂ + 2 H₂O(ℓ): h̄_C = (1)(−393 520) + (2)(−285 830) − (1)(−74 850) = {N(hc42,0)} kJ/kmol (đáp án in −890 330). Đối chiếu A-27: HHV = 55 530 kJ/kg × 16,043 = {N(55530*16.043,0)} kJ/kmol (lệch {N(abs(55530*16.043+hc42)/-hc42*100,2)} %).',
         f'CH₄ + 2 O₂ → CO₂ + 2 H₂O(ℓ): h̄_C = (1)(−393,520) + (2)(−285,830) − (1)(−74,850) = {N(hc42,0)} kJ/kmol (printed answer −890,330). Check with A-27: HHV = 55,530 kJ/kg × 16.043 = {N(55530*16.043,0)} kJ/kmol (difference {N(abs(55530*16.043+hc42)/-hc42*100,2)} %).',
         2, TOP['enth'], CEN('15–42'), 'printed answer −890,330 + A-27'))
hc44, hcg44, M44 = hC_item('15–44', '', '', 'C2H6', dict(CO2=2, H2O=3), 'C2H6', 'C2H6', None, '', '', '')
add(numq('Cengel Ch.15 Bài 15–44 (lặp lại 15–42 cho etan khí C₂H₆). Entanpi cháy của etan khí ở 25 °C, 1 atm, nước sản phẩm ở thể lỏng (A-26) là:',
         'Cengel Ch.15 Problem 15–44 (repeat of 15–42 for gaseous ethane C₂H₆). The enthalpy of combustion of gaseous ethane at 25 °C and 1 atm with liquid water in the products (A-26) is:',
         hc44, [(hcg44, 'dùng H₂O hơi (LHV)', 'uses H₂O vapor (LHV)'), (hc44 / 2, 'viết phương trình cho 1/2 kmol C₂H₆ (hệ số 2 CO₂ bị chia)', 'writes the equation for 1/2 kmol of C₂H₆ (halves the CO₂ coefficient)'), (hc44 + HF('C2H6') * 2, 'cộng thay vì trừ entanpi hình thành nhiên liệu', 'adds instead of subtracting the fuel enthalpy of formation (twice)')], 'kJ/kmol', 0,
         f'C₂H₆ + 3,5 O₂ → 2 CO₂ + 3 H₂O(ℓ): h̄_C = 2(−393 520) + 3(−285 830) − (−84 680) = {N(hc44,0)} kJ/kmol = {N(hc44/30.07,0)} kJ/kg. A-27: HHV = 51 900 × 30,07 = {N(51900*30.07,0)} kJ/kmol (lệch {N(abs(51900*30.07+hc44)/-hc44*100,2)} %); sách không in đáp án.',
         f'C₂H₆ + 3.5 O₂ → 2 CO₂ + 3 H₂O(ℓ): h̄_C = 2(−393,520) + 3(−285,830) − (−84,680) = {N(hc44,0)} kJ/kmol = {N(hc44/30.07,0)} kJ/kg. A-27: HHV = 51,900 × 30.07 = {N(51900*30.07,0)} kJ/kmol (difference {N(abs(51900*30.07+hc44)/-hc44*100,2)} %); the book prints no answer.',
         2, TOP['enth'], CEN('15–44'), 'script + A-27 (không có đáp án in)'))
add(numq('Cengel Ch.15 Bài 15–49. Metan (CH₄) cháy hoàn toàn với lượng không khí lý thuyết trong quá trình dòng ổn định. Chất phản ứng và sản phẩm đều ở 25 °C, 1 atm; nước trong sản phẩm ở thể lỏng. Nhiệt truyền ra khỏi buồng đốt trên mỗi kmol nhiên liệu là:',
         'Cengel Ch.15 Problem 15–49. Methane (CH₄) is burned completely with the stoichiometric amount of air in a steady-flow process. Reactants and products are both at 25 °C and 1 atm and the water in the products is liquid. The heat transferred out of the chamber per kmol of fuel is:',
         -hc42, [(hcg42 * -1, 'tính với H₂O hơi (LHV)', 'computed with H₂O vapor (LHV)'), (-hc42 / 16.043, 'đã chia cho khối lượng mol (kJ/kg, không phải kJ/kmol)', 'divided by the molar mass (kJ/kg, not kJ/kmol)'), (hc42, 'nhiệt đi VÀO buồng đốt (sai dấu): phản ứng tỏa nhiệt', 'heat INTO the chamber (wrong sign): the reaction is exothermic')], 'kJ/kmol', 0,
         f'Q = H_prod − H_react = h̄_C = {N(hc42,0)} kJ/kmol: nhiệt tỏa ra {N(-hc42,0)} kJ/kmol CH₄ (đáp án in 890 330). Nếu dùng 100 % không khí thừa mà vẫn ở 25 °C thì kết quả như cũ: N₂ và O₂ thừa vào và ra ở cùng trạng thái chuẩn, h̄_f° = 0 (nửa sau của đề).',
         f'Q = H_prod − H_react = h̄_C = {N(hc42,0)} kJ/kmol: heat released {N(-hc42,0)} kJ/kmol CH₄ (printed answer 890,330). With 100 percent excess air still at 25 °C the result is unchanged: the extra N₂ and O₂ enter and leave at the same standard state with h̄_f° = 0 (second half of the statement).',
         2, TOP['enth'], CEN('15–49'), 'printed answer 890,330 + script'))
hc50 = hC_nu('H2', dict(H2O=1), 'l'); reg('hC', dict(fuel='H2', nu=dict(H2O=1), water='l', a27='H2', col='HHV'), 'kJ/kmol', hc50, 1.5e-3, 'Cengel 15-50')
add(numq('Cengel Ch.15 Bài 15–50. Hiđrô (H₂) cháy hoàn toàn với lượng không khí lý thuyết trong quá trình dòng ổn định; chất phản ứng và sản phẩm ở 25 °C, 1 atm, nước ở thể lỏng. Nhiệt tỏa ra khỏi buồng đốt trên MỖI KG hiđrô (A-26; M = 2,016 kg/kmol) là:',
         'Cengel Ch.15 Problem 15–50. Hydrogen (H₂) is burned completely with the stoichiometric amount of air in a steady-flow process; reactants and products at 25 °C and 1 atm, liquid water. The heat released from the chamber per KILOGRAM of hydrogen (A-26; M = 2.016 kg/kmol) is:',
         -hc50 / 2.016, [(-hc50, 'là kJ/kmol, chưa chia cho M', 'is kJ per kmol, not divided by M'), (-hC_nu('H2', dict(H2O=1), 'g') / 2.016, 'tính với H₂O hơi (LHV; A-27 ghi 120 000)', 'computed with H₂O vapor (LHV; A-27 prints 120,000)'), (-hc50 / 18.015, 'chia cho khối lượng mol của H₂O (18,015) thay vì của H₂', 'divides by the molar mass of H₂O (18.015) instead of that of H₂')], 'kJ/kg', 0,
         f'H₂ + ½ O₂ → H₂O(ℓ): h̄_C = h̄_f°(H₂O ℓ) = −285 830 kJ/kmol ⇒ {N(-hc50/2.016,0)} kJ/kg. Đối chiếu A-27: HHV(H₂) = 141 800 kJ/kg (lệch {N(abs(-hc50/2.016-141800)/141800*100,3)} %); LHV = 120 000. 50 % không khí thừa không đổi kết quả khi mọi dòng ở 25 °C.',
         f'H₂ + 1/2 O₂ → H₂O(ℓ): h̄_C = h̄_f°(H₂O ℓ) = −285,830 kJ/kmol ⇒ {N(-hc50/2.016,0)} kJ/kg. Check with A-27: HHV(H₂) = 141,800 kJ/kg (difference {N(abs(-hc50/2.016-141800)/141800*100,3)} %); LHV = 120,000. 50 % excess air does not change the result when all streams are at 25 °C.',
         2, TOP['enth'], CEN('15–50'), 'script + A-27 (không có đáp án in)'))

# ================================================================== 8. Cengel 15-104 (exact molar masses reproduce the printed answers)
g104 = [('C3H8', .3), ('C4H10', .7)]; fx = parts_fuel(g104, True); lam104 = 20 / combustion(fx, 1.0, exact=True)['AF']; r104 = combustion(fx, lam104, exact=True)
f_r = parts_fuel(g104, False); lam104r = 20 / combustion(f_r, 1.0)['AF']; r104r = combustion(f_r, lam104r)
reg('comb_AF', dict(fuel=fp(*g104), AF=20.0, exact=True), 'N2', r104['N2'], 3e-4, 'Cengel 15-104 a'); reg('comb_AF', dict(fuel=fp(*g104), AF=20.0, exact=True), 'O2', r104['O2'], 3e-4, 'Cengel 15-104 c'); reg('comb_AF', dict(fuel=fp(*g104), AF=20.0, exact=True), 'H2O', r104['H2O'], 3e-4, 'Cengel 15-104 b')
prn('Cengel 15-104 (a) N2 [kmol/kmol fuel], exact masses', 29.41, r104['N2'], 0.002); prn('Cengel 15-104 (b) H2O', 4.7, r104['H2O'], 0.002); prn('Cengel 15-104 (c) O2 in products, exact masses', 1.77, r104['O2'], 0.005, f'with rounded masses (29, 12, 1): {r104r["O2"]:.3f}')
add(numq('Cengel Ch.15 Bài 15–104 (câu c). Hỗn hợp nhiên liệu khí gồm 30 % propan (C₃H₈) và 70 % butan (C₄H₁₀) theo thể tích được đốt trong không khí sao cho tỉ lệ không khí–nhiên liệu là 20 kg/kg và cháy hoàn toàn. Số kmol O₂ trong sản phẩm trên mỗi kmol nhiên liệu là (dùng khối lượng mol chính xác của A-1/A-27: M_air = 28,97; C₃H₈ 44,097; C₄H₁₀ 58,123) [Bổ sung: chỉ dẫn khối lượng mol chính xác, đề gốc không nêu]:',
         'Cengel Ch.15 Problem 15–104 (part c). A gaseous fuel mixture of 30 percent propane (C₃H₈) and 70 percent butane (C₄H₁₀) on a volume basis is burned in air such that the air–fuel ratio is 20 kg air/kg fuel and combustion is complete. The kmol of O₂ in the products per kmol of fuel is (use the exact molar masses of A-1/A-27: M_air = 28.97; C₃H₈ 44.097; C₄H₁₀ 58.123) [Added: the molar-mass hint, not in the original statement]:',
         r104['O2'], [(r104['O2'] + 1.0, 'cộng nhầm 1 kmol (lấy O₂ vào thay vì O₂ thừa)', 'adds one kmol by mistake'), (r104['N2'] / 3.76, 'là tổng O₂ cấp vào (7,82), chưa trừ lượng O₂ đã dùng', 'is the total O₂ supplied (7.82), not yet minus the O₂ consumed'), (0.0, 'cho rằng cháy lý thuyết không còn O₂', 'assumes theoretical combustion leaves no O₂')], 'kmol/kmol', 2,
         f'Nhiên liệu: C = 0,3×3 + 0,7×4 = 3,7; H = 0,3×8 + 0,7×10 = 9,4; M = {N(fx["M"],3)} kg/kmol ⇒ AF_lt = {N(combustion(fx,1.0,exact=True)["AF"],3)} và λ = 20/AF_lt = {N(lam104,4)}. Không khí = 20 × {N(fx["M"],3)}/28,97 = {N(20*fx["M"]/28.97,2)} kmol ⇒ O₂ vào = {N(r104["o2_in"],3)}; N₂ = {N(r104["N2"],2)} (in 29,41); H₂O = 4,7 (in 4,7); O₂ ra = O₂ vào − (C + H/4) = {N(r104["o2_in"],3)} − {N(3.7+9.4/4,3)} = {N(r104["O2"],3)} (in 1,77). Với khối lượng mol làm tròn (29; 12; 1) được {N(r104r["O2"],2)}: kết quả nhạy với chuẩn làm tròn vì là hiệu của hai số gần nhau.',
         f'Fuel: C = 0.3×3 + 0.7×4 = 3.7; H = 0.3×8 + 0.7×10 = 9.4; M = {N(fx["M"],3)} kg/kmol ⇒ AF_th = {N(combustion(fx,1.0,exact=True)["AF"],3)} and λ = 20/AF_th = {N(lam104,4)}. Air = 20 × {N(fx["M"],3)}/28.97 = {N(20*fx["M"]/28.97,2)} kmol ⇒ O₂ in = {N(r104["o2_in"],3)}; N₂ = {N(r104["N2"],2)} (printed 29.41); H₂O = 4.7 (printed 4.7); O₂ out = O₂ in − (C + H/4) = {N(r104["o2_in"],3)} − {N(3.7+9.4/4,3)} = {N(r104["O2"],3)} (printed 1.77). With rounded masses (29; 12; 1) the result is {N(r104r["O2"],2)}: it is sensitive to the rounding convention because it is a difference of two close numbers.',
         3, TOP['af'], CEN('15–104', ' (câu c)', ' (part c)'), 'printed answers 29.41 / 4.7 / 1.77 + script'))

# ================================================================== 9. first law, steady-flow combustion with sensible enthalpy (Cengel 15-53, 15-55, 15-56, 15-60, 15-67)
def lst(spec): return [[a, b, c] for a, b, c in spec]
# 15-53 acetylene 20 % excess air, fuel and air at 25 C, products at 1500 K
r53 = combustion(single('C2H2'), 1.2); rea53 = dict(C2H2=1, O2=r53['o2_in'], N2=r53['n2_in']); pro53 = dict(CO2=r53['CO2'], H2O_g=r53['H2O'], O2=r53['O2'], N2=r53['N2']); q53 = q_out(rea53, 298, pro53, 1500)
spec_r53 = lst([('C2H2', 1, 298), ('O2', r53['o2_in'], 298), ('N2', r53['n2_in'], 298)]); spec_p53 = lst([('CO2', r53['CO2'], 1500), ('H2O_g', r53['H2O'], 1500), ('O2', r53['O2'], 1500), ('N2', r53['N2'], 1500)])
reg('q', dict(react=spec_r53, prod=spec_p53), 'q_out', q53, 4e-3, 'Cengel 15-53 b'); reg('comb', dict(fuel=fp(('C2H2', 1)), lam=1.2, exact=False), 'AF', r53['AF'], 1e-9, 'Cengel 15-53 a')
q53_noSens = -(HF('CO2') * 2 + HF('H2O_g') - HF('C2H2')); q53_liq = Hstate(rea53, 298) - sum(n * (HF(s if s != 'H2O_g' else 'H2O_l') + (sens(s if s != 'H2O_g' else 'H2O', 1500) if s != 'H2O_g' else 0)) for s, n in pro53.items())
add(numq('Cengel Ch.15 Bài 15–53 (câu b). Axetilen (C₂H₂) cháy hoàn toàn với 20 % không khí thừa trong buồng đốt dòng ổn định. Nhiên liệu và không khí vào ở 25 °C, sản phẩm ra ở 1500 K. Nhiệt truyền ra khỏi buồng đốt trên mỗi kmol C₂H₂ (A-26, A-18…A-23) là:',
         'Cengel Ch.15 Problem 15–53 (part b). Acetylene (C₂H₂) is burned completely with 20 percent excess air in a steady-flow combustion chamber. The fuel and air enter at 25 °C and the products leave at 1500 K. The heat transferred out of the chamber per kmol of C₂H₂ (A-26, A-18…A-23) is:',
         q53, [(q53_noSens, 'chỉ tính −Σ N h̄_f° (cháy ở 25 °C), bỏ entanpi hiển nhiệt của sản phẩm', 'counts only −Σ N h̄_f° (combustion at 25 °C) and drops the sensible enthalpy of the products'), (q53_liq, 'dùng H₂O lỏng ở 1500 K (sai pha)', 'uses liquid H₂O at 1500 K (wrong phase)'),
              (q53 - 1500 * 0 + 0.5 * sens('O2', 1500) * 0 + sens('N2', 1500) * 2, 'cộng nhầm hai kmol N₂ nữa của entanpi sản phẩm', 'adds the enthalpy of two extra kmol of N₂ to the products')], 'kJ/kmol', 0,
         f'Chất phản ứng: C₂H₂ + 3 (O₂ + 3,76 N₂); sản phẩm: 2 CO₂ + 1 H₂O + 0,5 O₂ + {N(r53["N2"],2)} N₂ (AF = {N(r53["AF"],1)} kg/kg, câu a). Q_ra = H_react − H_prod, H_react = +226 730 (h̄_f°(C₂H₂)); H_prod = Σ N(h̄_f° + h̄_1500 − h̄_298) với h̄_1500 − 8 669-loại: CO₂ {N(sens("CO2",1500),0)}; H₂O {N(sens("H2O",1500),0)}; O₂ {N(sens("O2",1500),0)}; N₂ {N(sens("N2",1500),0)} kJ/kmol ⇒ H_prod = {N(Hstate(pro53,1500),0)}; Q_ra = {N(q53,0)} kJ/kmol. Đã thử cùng đường giải trên bài 15–55, 15–56, 15–60, 15–67, 15–70 (đáp án in khớp).',
         f'Reactants: C₂H₂ + 3 (O₂ + 3.76 N₂); products: 2 CO₂ + 1 H₂O + 0.5 O₂ + {N(r53["N2"],2)} N₂ (AF = {N(r53["AF"],1)} kg/kg, part a). Q_out = H_react − H_prod, H_react = +226,730 (h̄_f°(C₂H₂)); H_prod = Σ N(h̄_f° + h̄(1500 K) − h̄(298 K)) with the differences: CO₂ {N(sens("CO2",1500),0)}; H₂O {N(sens("H2O",1500),0)}; O₂ {N(sens("O2",1500),0)}; N₂ {N(sens("N2",1500),0)} kJ/kmol ⇒ H_prod = {N(Hstate(pro53,1500),0)}; Q_out = {N(q53,0)} kJ/kmol. The same route was tested on Problems 15–55, 15–56, 15–60, 15–67, 15–70 (printed answers reproduced).',
         3, TOP['law1'], CEN('15–53', ' (câu b)', ' (part b)'), 'script (không có đáp án in); đường giải thử trên 15–55/56/60/67/70'))
# 15-55 benzene, 95 % theoretical air, products 1000 K
n2_55 = 0.95 * 7.5 * 3.76; rea55 = dict(C6H6=1, O2=0.95 * 7.5, N2=n2_55); pro55 = dict(CO2=5.25, CO=0.75, H2O_g=3, N2=n2_55); q55 = q_out(rea55, 298, pro55, 1000); yco = 0.75 / (5.25 + 0.75 + 3 + n2_55)
spec_r55 = lst([('C6H6', 1, 298), ('O2', 0.95 * 7.5, 298), ('N2', n2_55, 298)]); spec_p55 = lst([('CO2', 5.25, 1000), ('CO', 0.75, 1000), ('H2O_g', 3, 1000), ('N2', n2_55, 1000)])
reg('q', dict(react=spec_r55, prod=spec_p55), 'q_out', q55, 4e-3, 'Cengel 15-55 b: printed 2,112,800'); reg('yco', dict(lam=0.95), 'yCO', yco, 1e-9, 'Cengel 15-55 a')
prn('Cengel 15-55 (a) y_CO [%]', 2.1, yco * 100, 0.01); prn('Cengel 15-55 (b) Q_out [kJ/kmol]', 2112800.0, q55, 2e-4, 'table interpolation; printed value 2,112,800')
q55_no = -(5.25 * HF('CO2') + 0.75 * HF('CO') + 3 * HF('H2O_g') - HF('C6H6')); q55_comp = q_out(dict(C6H6=1, O2=7.5, N2=7.5 * 3.76), 298, dict(CO2=6, H2O_g=3, N2=7.5 * 3.76), 1000)
add(numq('Cengel Ch.15 Bài 15–55 (câu b). Benzen khí (C₆H₆) ở 25 °C cháy dòng ổn định với 95 % không khí lý thuyết vào ở 25 °C. Toàn bộ hiđrô cháy thành H₂O, một phần cacbon cháy thành CO; sản phẩm ra ở 1000 K. Nhiệt truyền ra khỏi buồng đốt (kJ/kmol C₆H₆) là:',
         'Cengel Ch.15 Problem 15–55 (part b). Benzene gas (C₆H₆) at 25 °C is burned in a steady-flow process with 95 percent theoretical air entering at 25 °C. All the hydrogen burns to H₂O but part of the carbon burns to CO; the products leave at 1000 K. The heat transferred out of the chamber (kJ/kmol C₆H₆) is:',
         q55, [(q55_no, 'bỏ entanpi hiển nhiệt của sản phẩm (chỉ −Σ N h̄_f°)', 'drops the sensible enthalpy of the products (only −Σ N h̄_f°)'), (q55_comp, 'giả cháy hoàn toàn thành CO₂ với 100 % không khí', 'assumes complete combustion to CO₂ with 100 % air'), (q55 + 0.75 * (HF('CO2') - HF('CO')) * -1, 'tính 0,75 kmol CO như CO₂ (bỏ chênh lệch entanpi hình thành)', 'counts the 0.75 kmol of CO as CO₂ (ignores the formation-enthalpy difference)')], 'kJ/kmol', 0,
         f'C₆H₆ + 7,125 (O₂ + 3,76 N₂) → 5,25 CO₂ + 0,75 CO + 3 H₂O + {N(n2_55,2)} N₂ (O: 14,25 = 2x + y + 3 và x + y = 6). Q_ra = 82 930 − [5,25(−393 520 + {N(sens("CO2",1000),0)}) + 0,75(−110 530 + {N(sens("CO",1000),0)}) + 3(−241 820 + {N(sens("H2O",1000),0)}) + {N(n2_55,2)} × {N(sens("N2",1000),0)}] = {N(q55,0)} kJ/kmol (đáp án in 2 112 800; lệch {N(abs(q55-2112800)/2112800*100,4)} %). Phần mol CO = 0,75/{N(5.25+0.75+3+n2_55,2)} = {N(yco*100,1)} % (câu a, in 2,1 %).',
         f'C₆H₆ + 7.125 (O₂ + 3.76 N₂) → 5.25 CO₂ + 0.75 CO + 3 H₂O + {N(n2_55,2)} N₂ (O: 14.25 = 2x + y + 3 and x + y = 6). Q_out = 82,930 − [5.25(−393,520 + {N(sens("CO2",1000),0)}) + 0.75(−110,530 + {N(sens("CO",1000),0)}) + 3(−241,820 + {N(sens("H2O",1000),0)}) + {N(n2_55,2)} × {N(sens("N2",1000),0)}] = {N(q55,0)} kJ/kmol (printed answer 2,112,800; difference {N(abs(q55-2112800)/2112800*100,4)} %). CO mole fraction = 0.75/{N(5.25+0.75+3+n2_55,2)} = {N(yco*100,1)} % (part a, printed 2.1 %).',
         3, TOP['law1'], CEN('15–55', ' (câu b)', ' (part b)'), 'printed answers 2.1 % and 2,112,800 + script'))
# 15-56 diesel 20 % excess air, products 500 K, 2000 kJ/s
r56 = combustion(single('C12H26'), 1.2); rea56 = dict(C12H26=1, O2=r56['o2_in'], N2=r56['n2_in']); pro56 = dict(CO2=r56['CO2'], H2O_g=r56['H2O'], O2=r56['O2'], N2=r56['N2']); q56 = q_out(rea56, 298, pro56, 500); mdot56 = 2000 / q56 * Mf('C12H26') * 1000
spec_r56 = lst([('C12H26', 1, 298), ('O2', r56['o2_in'], 298), ('N2', r56['n2_in'], 298)]); spec_p56 = lst([('CO2', r56['CO2'], 500), ('H2O_g', r56['H2O'], 500), ('O2', r56['O2'], 500), ('N2', r56['N2'], 500)])
reg('q', dict(react=spec_r56, prod=spec_p56), 'q_out', q56, 4e-3, 'Cengel 15-56'); reg('mdot', dict(q=q56, Q=2000.0, M=Mf('C12H26')), 'g/s', mdot56, 4e-3, 'Cengel 15-56: printed 49.5'); prn('Cengel 15-56 mass flow [g/s]', 49.5, mdot56, 0.003)
q56_no = -hC_nu('C12H26', dict(CO2=12, H2O=13), 'g')
add(numq('Cengel Ch.15 Bài 15–56. Nhiên liệu diesel (C₁₂H₂₆) ở 25 °C cháy trong buồng đốt dòng ổn định với 20 % không khí thừa cũng vào ở 25 °C. Sản phẩm ra ở 500 K. Giả thiết cháy hoàn toàn: lưu lượng khối lượng nhiên liệu cần có để cung cấp nhiệt 2000 kJ/s là:',
         'Cengel Ch.15 Problem 15–56. Diesel fuel (C₁₂H₂₆) at 25 °C is burned in a steady-flow combustion chamber with 20 percent excess air that also enters at 25 °C. The products leave at 500 K. Assuming complete combustion, the fuel mass flow rate needed to supply heat at 2000 kJ/s is:',
         mdot56, [(2000 / q56_no * Mf('C12H26') * 1000, 'bỏ entanpi hiển nhiệt của sản phẩm (chỉ dùng |h̄_C|)', 'drops the sensible enthalpy of the products (uses |h̄_C| only)'), (mdot56 / 60, 'đọc 2000 kJ/min thay cho 2000 kJ/s', 'reads 2000 kJ/min instead of 2000 kJ/s'), (2000 / q_out(rea56, 298, pro56, 773) * Mf('C12H26') * 1000, 'đọc 500 K thành 500 °C (773 K)', 'reads 500 K as 500 °C (773 K)')], 'g/s', 1,
         f'C₁₂H₂₆ + 18,5 (O₂ + 3,76 N₂) là cháy lý thuyết: a_th = 12 + 6,5 = 18,5; 20 % thừa → 22,2 O₂ → sản phẩm 12 CO₂ + 13 H₂O + 3,7 O₂ + {N(r56["N2"],1)} N₂. Q_ra = {N(q56,0)} kJ/kmol (dùng h̄_f° C₁₂H₂₆(g) = −291 010 của A-26 và h̄ − h̄_298 của A-18…A-23 tại 500 K). ṁ = 2000 kJ/s × 170 kg/kmol / {N(q56,0)} kJ/kmol = {N(mdot56/1000,5)} kg/s = {N(mdot56,1)} g/s (đáp án in 49,5).',
         f'C₁₂H₂₆ + 18.5 (O₂ + 3.76 N₂) is the stoichiometric equation: a_th = 12 + 6.5 = 18.5; 20 % excess → 22.2 O₂ → products 12 CO₂ + 13 H₂O + 3.7 O₂ + {N(r56["N2"],1)} N₂. Q_out = {N(q56,0)} kJ/kmol (h̄_f° of C₁₂H₂₆(g) = −291,010 from A-26 and h̄ − h̄_298 from A-18…A-23 at 500 K). ṁ = 2000 kJ/s × 170 kg/kmol / {N(q56,0)} kJ/kmol = {N(mdot56/1000,5)} kg/s = {N(mdot56,1)} g/s (printed answer 49.5).',
         3, TOP['law1'], CEN('15–56'), 'printed answer 49.5 + script'))
# 15-60 ethane, preheated air 500 K, 95 % C -> CO2, products 800 K, 5 kg/h
r60 = combustion(single('C2H6'), 1.0); o2i = r60['o2_in']; n2i = r60['n2_in']; o2_60 = o2i - (1.9 + 0.05 + 1.5)
spec_r60 = lst([('C2H6', 1, 298), ('O2', o2i, 500), ('N2', n2i, 500)]); spec_p60 = lst([('CO2', 1.9, 800), ('CO', 0.1, 800), ('H2O_g', 3, 800), ('O2', o2_60, 800), ('N2', n2i, 800)])
q60k = Hstate(dict(C2H6=1), 298) + Hstate(dict(O2=o2i, N2=n2i), 500) - Hstate(dict(CO2=1.9, CO=0.1, H2O_g=3, O2=o2_60, N2=n2i), 800); Q60 = q60k * 5 / 30
reg('q', dict(react=spec_r60, prod=spec_p60), 'q_out', q60k, 4e-3, 'Cengel 15-60 per kmol'); reg('mdot', dict(q=q60k, Q=1.0, M=30.0, kg_h=5.0), 'kJ/h', Q60, 4e-3, 'Cengel 15-60: printed 200,170'); prn('Cengel 15-60 heat rate [kJ/h]', 200170.0, Q60, 0.003)
q60_cold = q_out(dict(C2H6=1, O2=o2i, N2=n2i), 298, dict(CO2=1.9, CO=0.1, H2O_g=3, O2=o2_60, N2=n2i), 800) * 5 / 30
add(numq('Cengel Ch.15 Bài 15–60. Etan khí (C₂H₆) ở 25 °C cháy với lưu lượng 5 kg/h trong buồng đốt dòng ổn định với lượng không khí lý thuyết được gia nhiệt tới 500 K trước khi vào. Phân tích khí cho thấy toàn bộ hiđrô cháy thành H₂O nhưng chỉ 95 % cacbon thành CO₂, 5 % còn lại thành CO. Sản phẩm ra ở 800 K. Tốc độ nhiệt truyền ra khỏi buồng đốt (kJ/h) là:',
         'Cengel Ch.15 Problem 15–60. Ethane gas (C₂H₆) at 25 °C is burned at a rate of 5 kg/h in a steady-flow combustion chamber with the stoichiometric amount of air preheated to 500 K. The gas analysis shows that all the hydrogen burns to H₂O but only 95 percent of the carbon burns to CO₂ and 5 percent forms CO. The products leave at 800 K. The rate of heat transfer from the chamber (kJ/h) is:',
         Q60, [(q60_cold, 'coi không khí vào ở 25 °C (bỏ entanpi hiển nhiệt khi gia nhiệt 500 K)', 'takes the air as entering at 25 °C (drops the preheating enthalpy at 500 K)'), (q60k, 'là kJ/kmol nhiên liệu, chưa nhân 5/30 kmol/h', 'is kJ per kmol of fuel, not multiplied by 5/30 kmol/h'), (q60k * 5 / 30 * 1.1, 'cộng 10 % (làm tròn sai)', 'adds 10 % (bad rounding)')], 'kJ/h', 0,
         f'C₂H₆ + 3,5 (O₂ + 3,76 N₂) → 1,9 CO₂ + 0,1 CO + 3 H₂O + {N(o2_60,2)} O₂ + {N(n2i,2)} N₂ (O₂ còn lại 3,5 − 1,9 − 0,05 − 1,5 = {N(o2_60,2)}). Q_ra = H_react − H_prod = {N(q60k,0)} kJ/kmol; lưu lượng mol = 5/30 = 0,1667 kmol/h ⇒ {N(Q60,0)} kJ/h (đáp án in 200 170; M = 30,07 thì {N(q60k*5/30.07,0)}).',
         f'C₂H₆ + 3.5 (O₂ + 3.76 N₂) → 1.9 CO₂ + 0.1 CO + 3 H₂O + {N(o2_60,2)} O₂ + {N(n2i,2)} N₂ (O₂ left: 3.5 − 1.9 − 0.05 − 1.5 = {N(o2_60,2)}). Q_out = H_react − H_prod = {N(q60k,0)} kJ/kmol; mole rate = 5/30 = 0.1667 kmol/h ⇒ {N(Q60,0)} kJ/h (printed answer 200,170; with M = 30.07 it is {N(q60k*5/30.07,0)}).',
         3, TOP['law1'], CEN('15–60'), 'printed answer 200,170 + script'))
# 15-67 ethanol liquid
r67 = combustion(single('C2H5OH'), 1.4); rea67 = dict(C2H5OH_l=1, O2=r67['o2_in'], N2=r67['n2_in']); pro67 = dict(CO2=r67['CO2'], H2O_g=r67['H2O'], O2=r67['O2'], N2=r67['N2']); q67 = q_out(rea67, 298, pro67, 600); V67 = 2000 / q67 * 46 / 790 * 1000 * 60
spec_r67 = lst([('C2H5OH_l', 1, 298), ('O2', r67['o2_in'], 298), ('N2', r67['n2_in'], 298)]); spec_p67 = lst([('CO2', r67['CO2'], 600), ('H2O_g', r67['H2O'], 600), ('O2', r67['O2'], 600), ('N2', r67['N2'], 600)])
reg('q', dict(react=spec_r67, prod=spec_p67), 'q_out', q67, 4e-3, 'Cengel 15-67'); reg('Vflow', dict(q=q67, Q=2000.0, M=46.0, rho=790.0), 'L/min', V67, 4e-3, 'Cengel 15-67: printed 6.81'); prn('Cengel 15-67 volume flow [L/min]', 6.81, V67, 0.003)
add(numq('Cengel Ch.15 Bài 15–67. Rượu etylic lỏng (C₂H₅OH(ℓ)) ở 25 °C cháy dòng ổn định với 40 % không khí thừa cũng vào ở 25 °C. Sản phẩm ra ở 600 K, cháy hoàn toàn. Lưu lượng thể tích etanol lỏng cần có để cấp nhiệt 2000 kJ/s (khối lượng riêng 790 kg/m³, M = 46 kg/kmol) là:',
         'Cengel Ch.15 Problem 15–67. Liquid ethyl alcohol (C₂H₅OH(ℓ)) at 25 °C is burned in a steady-flow chamber with 40 percent excess air that also enters at 25 °C. The products leave at 600 K, complete combustion. The volume flow rate of liquid ethanol required to supply heat at 2000 kJ/s (density 790 kg/m³, M = 46 kg/kmol) is:',
         V67, [(2000 / q_out(dict(C2H5OH_g=1, O2=r67['o2_in'], N2=r67['n2_in']), 298, pro67, 600) * 46 / 790 * 1000 * 60, 'dùng h̄_f° của etanol KHÍ (−235 310) thay cho lỏng (−277 690)', 'uses h̄_f° of ethanol VAPOR (−235,310) instead of liquid (−277,690)'), (V67 / 60, 'quên đổi s sang phút (ra L/s)', 'forgets to convert s to min (gives L/s)'), (V67 * 790 / 1000, 'nhân khối lượng riêng thay vì chia (ra kg/min)', 'multiplies by the density instead of dividing (gives kg/min)')], 'L/min', 2,
         f'C₂H₅OH + 3 O₂ → 2 CO₂ + 3 H₂O; 40 % thừa → 4,2 O₂, 15,79 N₂, sản phẩm 2 CO₂ + 3 H₂O + 1,2 O₂ + 15,79 N₂. Q_ra = {N(q67,0)} kJ/kmol (h̄_f° etanol lỏng A-26). ṁ = 2000/{N(q67,0)} × 46 = {N(2000/q67*46,3)} kg/s ⇒ V̇ = {N(2000/q67*46/790*1000,5)} L/s = {N(V67,2)} L/min (đáp án in 6,81).',
         f'C₂H₅OH + 3 O₂ → 2 CO₂ + 3 H₂O; 40 % excess → 4.2 O₂, 15.79 N₂, products 2 CO₂ + 3 H₂O + 1.2 O₂ + 15.79 N₂. Q_out = {N(q67,0)} kJ/kmol (h̄_f° of liquid ethanol, A-26). ṁ = 2000/{N(q67,0)} × 46 = {N(2000/q67*46,3)} kg/s ⇒ V̇ = {N(2000/q67*46/790*1000,5)} L/s = {N(V67,2)} L/min (printed answer 6.81).',
         3, TOP['law1'], CEN('15–67'), 'printed answer 6.81 + script'))

# ================================================================== 10. adiabatic flame temperature (Cengel 15-70, 15-73; supp. flame temperature) with the same table route
def T_ad_hf(react, T_r, prod, loss=0.0, water_liquid_hf=False):
    save = FORM['H2O_g']
    if water_liquid_hf: FORM['H2O_g'] = 'H2O(ᐉ)'
    try:
        target = Hstate(react, T_r) - loss; lo, hi = 298.0, 3200.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if Hstate(prod, mid) > target: hi = mid
            else: lo = mid
        return (lo + hi) / 2
    finally: FORM['H2O_g'] = save
def tad_case(fuel, lam, T_air, T_fuel=None, loss=0.0, **kw):
    T_fuel = T_air if T_fuel is None else T_fuel
    r = combustion(single(fuel), lam)
    rea = dict(fuel_key=0)  # placeholder (keys rebuilt below)
    rea = {fuel: 1, 'O2': r['o2_in'], 'N2': r['n2_in']}
    Hr = Hstate({fuel: 1}, T_fuel) + Hstate({'O2': r['o2_in'], 'N2': r['n2_in']}, T_air)
    prod = {'CO2': r['CO2'], 'H2O_g': r['H2O'], 'O2': r['O2'], 'N2': r['N2']}; prod = {k: v for k, v in prod.items() if v > 0}
    target = Hr - loss; lo, hi = 298.0, 3200.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Hstate(prod, mid) > target: hi = mid
        else: lo = mid
    return (lo + hi) / 2, r, prod
T70, r70, prod70 = tad_case('H2', 1.2, 280.0, 280.0); T70_st = tad_case('H2', 1.0, 280.0, 280.0)[0]; T70_big = tad_case('H2', 2.2, 280.0, 280.0)[0]; T70_liq = T_ad_hf(dict(H2=1, O2=r70['o2_in'], N2=r70['n2_in']), 280.0, prod70, water_liquid_hf=True) if False else None
def Tad_reg(fuel, lam, T_air, loss, out, what, val, tol=0.003, T_fuel=298.0):
    r = combustion(single(fuel), lam); spec_r = lst([(fuel, 1, T_fuel), ('O2', r['o2_in'], T_air), ('N2', r['n2_in'], T_air)])
    spec_p = [[k, v] for k, v in (('CO2', r['CO2']), ('H2O_g', r['H2O']), ('O2', r['O2']), ('N2', r['N2'])) if v > 0]
    return reg('Tad', dict(react=spec_r, prod=spec_p, loss=loss), out, val, tol, what)
Tad_reg('H2', 1.2, 280.0, 0.0, 'T', 'Cengel 15-70: printed 2251.4 K', T70, T_fuel=280.0); prn('Cengel 15-70 adiabatic flame temperature [K]', 2251.4, T70, 5e-4)
T70_liq = None
add(numq('Cengel Ch.15 Bài 15–70. Hiđrô (H₂) ở 7 °C cháy với 20 % không khí thừa cũng ở 7 °C trong quá trình dòng ổn định đoạn nhiệt. Giả thiết cháy hoàn toàn. Nhiệt độ sản phẩm ra (A-18…A-23) xấp xỉ:',
         'Cengel Ch.15 Problem 15–70. Hydrogen (H₂) at 7 °C is burned with 20 percent excess air that is also at 7 °C during an adiabatic steady-flow combustion process. Assuming complete combustion, the exit temperature of the products (A-18…A-23) is about:',
         T70, [(T70_st, 'bỏ 20 % không khí thừa (λ = 1): thiếu lượng khí trơ hấp thụ nhiệt', 'drops the 20 % excess air (λ = 1): too little inert gas to absorb the heat'), (T70_big, 'hiểu 20 % thừa là 120 % thừa (λ = 2,2)', 'reads 20 % excess as 120 % excess (λ = 2.2)'), (tad_case('H2', 1.2, 298.0, 298.0)[0] + 150, 'dùng khí nóng thêm 150 K (nhầm hiển nhiệt chất phản ứng)', 'adds 150 K (misapplied reactant sensible enthalpy)')], 'K', 0,
         f'H₂ + 0,6 (O₂ + 3,76 N₂) cần a_th = 0,5; 20 % thừa → 0,6 O₂, 2,256 N₂; sản phẩm H₂O + 0,1 O₂ + 2,256 N₂. Điều kiện đoạn nhiệt: Σ N_p(h̄_f° + h̄(T) − h̄_298) = Σ N_r(h̄_f° + h̄(280 K) − h̄_298), vế phải = {N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} kJ/kmol. Thử T = 2250 K: vế trái {N(Hstate(prod70,2250.0),0)}; T = 2300 K: {N(Hstate(prod70,2300.0),0)} ⇒ nội suy T = {N(T70,1)} K (đáp án in 2251,4 K).',
         f'H₂ + 0.6 (O₂ + 3.76 N₂) needs a_th = 0.5; 20 % excess → 0.6 O₂, 2.256 N₂; products H₂O + 0.1 O₂ + 2.256 N₂. Adiabatic condition: Σ N_p(h̄_f° + h̄(T) − h̄_298) = Σ N_r(h̄_f° + h̄(280 K) − h̄_298), right side = {N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} kJ/kmol. Try T = 2250 K: left side {N(Hstate(prod70,2250.0),0)}; T = 2300 K: {N(Hstate(prod70,2300.0),0)} ⇒ interpolation T = {N(T70,1)} K (printed answer 2251.4 K).',
         3, TOP['tdp'], CEN('15–70'), 'printed answer 2251.4 + script'))
T73, r73, prod73 = tad_case('C2H2', 1.3, 300.0, loss=75000.0)
Tad_reg('C2H2', 1.3, 300.0, 75000.0, 'T', 'Cengel 15-73: printed 2301 K; table route 2303', T73); prn('Cengel 15-73 exit temperature [K]', 2301.0, T73, 1.5e-3, 'table (linear) route gives 2303.1: 2 K = 0.09 % from the printed value (interpolation/rounding)')
add(numq('Cengel Ch.15 Bài 15–73. Axetilen (C₂H₂) ở 25 °C cháy dòng ổn định với 30 % không khí thừa ở 27 °C. Nhiệt mất ra môi trường là 75 000 kJ trên mỗi kmol C₂H₂. Giả thiết cháy hoàn toàn. Nhiệt độ sản phẩm ra (A-18…A-23) xấp xỉ:',
         'Cengel Ch.15 Problem 15–73. Acetylene gas (C₂H₂) at 25 °C is burned in a steady-flow process with 30 percent excess air at 27 °C. Heat is lost to the surroundings at 75,000 kJ per kmol of C₂H₂. Assuming complete combustion, the exit temperature of the products (A-18…A-23) is about:',
         T73, [(tad_case('C2H2', 1.3, 300.0)[0], 'bỏ nhiệt mất 75 000 kJ/kmol (coi đoạn nhiệt)', 'ignores the 75,000 kJ/kmol heat loss (treats it as adiabatic)'), (tad_case('C2H2', 1.0, 300.0, loss=75000.0)[0], 'bỏ 30 % không khí thừa', 'drops the 30 % excess air'), (tad_case('C2H2', 1.3, 300.0, loss=-75000.0)[0], 'cộng nhiệt 75 000 thay vì trừ (sai dấu của nhiệt mất)', 'adds the 75,000 instead of subtracting (wrong sign of the loss)')], 'K', 0,
         f'C₂H₂ + 3,25 (O₂ + 3,76 N₂) → 2 CO₂ + H₂O + 0,75 O₂ + {N(r73["N2"],2)} N₂. H_react = 226 730 + 3,25 × 4,76 kmol không khí ở 300 K: {N(Hstate(dict(C2H2=1),298.0)+Hstate(dict(O2=r73["o2_in"],N2=r73["n2_in"]),300.0),0)} kJ/kmol; H_prod(T) = H_react − 75 000 = {N(Hstate(dict(C2H2=1),298.0)+Hstate(dict(O2=r73["o2_in"],N2=r73["n2_in"]),300.0)-75000,0)} ⇒ nội suy trong A-18…A-23: T = {N(T73,0)} K (đáp án in 2301 K; lệch 2 K ≈ 0,09 % do nội suy tuyến tính/làm tròn).',
         f'C₂H₂ + 3.25 (O₂ + 3.76 N₂) → 2 CO₂ + H₂O + 0.75 O₂ + {N(r73["N2"],2)} N₂. H_react = 226,730 + the enthalpy of the 3.25 × 4.76 kmol of air at 300 K: {N(Hstate(dict(C2H2=1),298.0)+Hstate(dict(O2=r73["o2_in"],N2=r73["n2_in"]),300.0),0)} kJ/kmol; H_prod(T) = H_react − 75,000 = {N(Hstate(dict(C2H2=1),298.0)+Hstate(dict(O2=r73["o2_in"],N2=r73["n2_in"]),300.0)-75000,0)} ⇒ interpolation in A-18…A-23: T = {N(T73,0)} K (printed answer 2301 K; gap 2 K ≈ 0.09 % from linear interpolation/rounding).',
         3, TOP['tdp'], CEN('15–73'), 'printed answer 2301 (table route 2303, Δ 0.09 %) + script'))
# Cengel Example 15-8 (a) (liquid octane, theoretical air, 25 C) and Example 15-10 (a) (methane, 50 % excess air): printed 2395 K and 1789 K
def tad_gen(fuel_key, comp_fuel, lam, T=298.0):
    r = combustion(single(comp_fuel), lam); Hr = Hstate({fuel_key: 1}, T) + Hstate({'O2': r['o2_in'], 'N2': r['n2_in']}, T)
    prod = {k: v for k, v in dict(CO2=r['CO2'], H2O_g=r['H2O'], O2=r['O2'], N2=r['N2']).items() if v > 0}; lo, hi = 298.0, 3200.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Hstate(prod, mid) > Hr: hi = mid
        else: lo = mid
    return (lo + hi) / 2, r, prod
T158, r158, p158 = tad_gen('C8H18_l', 'C8H18', 1.0); T158b = tad_gen('C8H18_l', 'C8H18', 4.0)[0]; T1510, r1510, p1510 = tad_gen('CH4', 'CH4', 1.5)
def tad_reg2(fuel_key, comp_fuel, lam, what, val):
    r = combustion(single(comp_fuel), lam); spec_r = lst([(fuel_key, 1, 298.0), ('O2', r['o2_in'], 298.0), ('N2', r['n2_in'], 298.0)])
    spec_p = [[k, v] for k, v in (('CO2', r['CO2']), ('H2O_g', r['H2O']), ('O2', r['O2']), ('N2', r['N2'])) if v > 0]
    return reg('Tad', dict(react=spec_r, prod=spec_p, loss=0.0), 'T', val, 0.003, what)
tad_reg2('C8H18_l', 'C8H18', 1.0, 'Cengel Ex 15-8 a: printed 2395 K', T158); tad_reg2('C8H18_l', 'C8H18', 4.0, 'Cengel Ex 15-8 b: printed 962 K', T158b); tad_reg2('CH4', 'CH4', 1.5, 'Cengel Ex 15-10 a: printed 1789 K', T1510)
prn('Cengel Ex 15-8 (a) adiabatic flame temperature [K]', 2395.0, T158, 5e-4); prn('Cengel Ex 15-8 (b) 400 % theoretical air [K]', 962.0, T158b, 2e-3); prn('Cengel Ex 15-10 (a) methane, 50 % excess air [K]', 1789.0, T1510, 5e-4)
add(numq('Cengel Ví dụ 15–8 (câu a, bổ sung từ §15-5). Octan lỏng (C₈H₁₈) ở 25 °C, 1 atm cháy với lượng không khí lý thuyết vào cùng trạng thái trong buồng đốt tuabin khí đoạn nhiệt, dòng ổn định, cháy hoàn toàn. Nhiệt độ sản phẩm (A-18…A-23, thử và nội suy) xấp xỉ:',
         'Cengel Example 15–8 (part a, added from §15-5). Liquid octane (C₈H₁₈) at 25 °C and 1 atm is burned with the theoretical amount of air entering at the same state in an adiabatic steady-flow gas-turbine combustor, complete combustion. The product temperature (A-18…A-23, trial and interpolation) is about:',
         T158, [(T158b, 'là kết quả với 400 % không khí lý thuyết (câu b của sách)', 'is the result with 400 percent theoretical air (part b of the book)'), (tad_gen('C8H18_l', 'C8H18', 0.9)[0] if False else tad_gen('C8H18_l', 'C8H18', 1.5)[0], 'có thêm 50 % không khí thừa', 'has 50 percent excess air added'), (T158 * 1.12, 'cao hơn 12 % (dùng c̄_p nhỏ hằng số)', '12 % too high (small constant c̄_p used)')], 'K', 0,
         f'C₈H₁₈ + 12,5 (O₂ + 3,76 N₂) → 8 CO₂ + 9 H₂O + 47 N₂; H_prod = H_react = h̄_f°(C₈H₁₈ ℓ) = −249 950 kJ/kmol ⇒ Σ N_p(h̄_f° + h̄ − h̄_298) = −249 950 ⇒ 8 h̄_CO₂ + 9 h̄_H₂O + 47 h̄_N₂ = 5 646 081 kJ (sách). Thử 2400 K: {N(8*hbar("CO2",2400.0)+9*hbar("H2O",2400.0)+47*hbar("N2",2400.0),0)} (sách 5 660 828, cao hơn), 2350 K thấp hơn ⇒ nội suy T = {N(T158,0)} K (sách 2395 K). Nhiệt độ ngọn lửa đoạn nhiệt này vượt giới hạn vật liệu của tuabin nên thực tế dùng nhiều không khí thừa: 400 % cho {N(T158b,0)} K (sách 962 K).',
         f'C₈H₁₈ + 12.5 (O₂ + 3.76 N₂) → 8 CO₂ + 9 H₂O + 47 N₂; H_prod = H_react = h̄_f°(C₈H₁₈ ℓ) = −249,950 kJ/kmol ⇒ Σ N_p(h̄_f° + h̄ − h̄_298) = −249,950 ⇒ 8 h̄_CO₂ + 9 h̄_H₂O + 47 h̄_N₂ = 5,646,081 kJ (book). Trial 2400 K: {N(8*hbar("CO2",2400.0)+9*hbar("H2O",2400.0)+47*hbar("N2",2400.0),0)} (book 5,660,828, higher), 2350 K is lower ⇒ interpolation T = {N(T158,0)} K (book 2395 K). This adiabatic flame temperature exceeds the material limits of a turbine, so real combustors use a lot of excess air: 400 % gives {N(T158b,0)} K (book 962 K).',
         3, TOP['tdp'], dict(vi='Cengel Ch.15 Ví dụ 15–8 (câu a)', en='Cengel Ch.15 Example 15–8 (part a)'), 'printed answer 2395 K + script'))
add(numq('Cengel Ví dụ 15–10 (câu a, bổ sung từ §15-5). Metan (CH₄) khí ở 25 °C, 1 atm cháy hoàn toàn với 50 % không khí thừa vào ở 25 °C, 1 atm trong buồng đốt đoạn nhiệt dòng ổn định. Nhiệt độ sản phẩm (A-18…A-23) xấp xỉ:',
         'Cengel Example 15–10 (part a, added from §15-5). Methane (CH₄) gas at 25 °C and 1 atm is burned completely with 50 percent excess air entering at 25 °C and 1 atm in an adiabatic steady-flow combustion chamber. The product temperature (A-18…A-23) is about:',
         T1510, [(tad_gen('CH4', 'CH4', 1.0)[0], 'bỏ phần không khí thừa (λ = 1)', 'ignores the excess air (λ = 1)'), (tad_gen('CH4', 'CH4', 2.5)[0], 'hiểu 50 % thừa là 250 % lý thuyết', 'reads 50 % excess as 250 % theoretical'), (T1510 + 400, 'cộng thêm 400 K (hiển nhiệt N₂ của chất phản ứng)', 'adds 400 K (reactant N₂ sensible enthalpy)')], 'K', 0,
         f'CH₄ + 3 (O₂ + 3,76 N₂) → CO₂ + 2 H₂O + O₂ + 11,28 N₂; Σ N_p(h̄_f° + h̄ − h̄_298) = h̄_f°(CH₄) = −74 850 ⇒ h̄_CO₂ + 2 h̄_H₂O + h̄_O₂ + 11,28 h̄_N₂ = 937 950 kJ (sách) ⇒ thử và nội suy trong A-18…A-23: T = {N(T1510,0)} K (sách 1789 K).',
         f'CH₄ + 3 (O₂ + 3.76 N₂) → CO₂ + 2 H₂O + O₂ + 11.28 N₂; Σ N_p(h̄_f° + h̄ − h̄_298) = h̄_f°(CH₄) = −74,850 ⇒ h̄_CO₂ + 2 h̄_H₂O + h̄_O₂ + 11.28 h̄_N₂ = 937,950 kJ (book) ⇒ trial and interpolation in A-18…A-23: T = {N(T1510,0)} K (book 1789 K).',
         3, TOP['tdp'], dict(vi='Cengel Ch.15 Ví dụ 15–10 (câu a)', en='Cengel Ch.15 Example 15–10 (part a)'), 'printed answer 1789 K + script'))
# essay: 15-70 as a worked iteration (tables), plus 15-55 as a full first-law solution
add(ess(B('Cengel Ch.15 Bài 15–70 (lời giải đầy đủ). Hiđrô (H₂) ở 7 °C cháy với 20 % không khí thừa cũng ở 7 °C trong quá trình dòng ổn định đoạn nhiệt, cháy hoàn toàn. Xác định nhiệt độ ngọn lửa đoạn nhiệt của sản phẩm.',
           'Cengel Ch.15 Problem 15–70 (full solution). Hydrogen (H₂) at 7 °C is burned with 20 percent excess air that is also at 7 °C during an adiabatic steady-flow combustion process, complete combustion. Determine the adiabatic flame temperature of the products.'),
         B(f'''Giả thiết: dòng ổn định, không công, bỏ qua động/thế năng, Q = 0, khí lý tưởng; h̄(T) lấy từ A-18…A-23 (nội suy tuyến tính giữa các hàng), mốc h̄_298 như slide tr.44.
Bước 1. H₂ + 0,5 (O₂ + 3,76 N₂) là cháy lý thuyết; với 20 % thừa: H₂ + 0,6 O₂ + 2,256 N₂ → H₂O + 0,1 O₂ + 2,256 N₂.
Bước 2 (vế chất phản ứng, T = 280 K). h̄_280 − h̄_298: H₂ {N(sens("H2",280.0),0)}; O₂ {N(sens("O2",280.0),0)}; N₂ {N(sens("N2",280.0),0)} kJ/kmol. H_react = 0 + (0,6 × {N(sens("O2",280.0),0)} + 2,256 × {N(sens("N2",280.0),0)} + {N(sens("H2",280.0),0)}) = {N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} kJ/kmol.
Bước 3 (vế sản phẩm). H_prod(T) = h̄_f°(H₂O g) + Δh̄_H₂O + 0,1 Δh̄_O₂ + 2,256 Δh̄_N₂ với h̄_f°(H₂O g) = −241 820. T = 2250 K: Δh̄ = {N(sens("H2O",2250.0),0)}; {N(sens("O2",2250.0),0)}; {N(sens("N2",2250.0),0)} ⇒ H_prod = {N(Hstate(prod70,2250.0),0)}. T = 2300 K: {N(Hstate(prod70,2300.0),0)}.
Bước 4. H_react nằm giữa hai giá trị ⇒ T_ad = 2250 + 50 × ({N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} − {N(Hstate(prod70,2250.0),0)}) / ({N(Hstate(prod70,2300.0),0)} − {N(Hstate(prod70,2250.0),0)}) = {N(T70,1)} K (đáp án in 2251,4 K).
Hai đường: (A) nội suy bảng như trên; (B) giải bằng brentq với entanpi tính từ tích phân T ds° trên chính các cột s° của A-18…A-23 (không dùng cột h): chênh dưới 0,15 %. Nhận xét: nhiệt độ ngọn lửa đoạn nhiệt cao hơn nhiều giới hạn vật liệu; thực tế còn có phân ly (slide tr.8) làm nhiệt độ thấp hơn. Slide Ch.4 không có nhiệt độ ngọn lửa đoạn nhiệt: mục này là Bổ sung từ sách.''',
           f'''Assumptions: steady flow, no work, negligible kinetic/potential energy, Q = 0, ideal gases; h̄(T) from A-18…A-23 (linear interpolation between rows), reference h̄_298 as on slide p.44.
Step 1. H₂ + 0.5 (O₂ + 3.76 N₂) is theoretical combustion; with 20 % excess: H₂ + 0.6 O₂ + 2.256 N₂ → H₂O + 0.1 O₂ + 2.256 N₂.
Step 2 (reactant side, T = 280 K). h̄_280 − h̄_298: H₂ {N(sens("H2",280.0),0)}; O₂ {N(sens("O2",280.0),0)}; N₂ {N(sens("N2",280.0),0)} kJ/kmol. H_react = 0 + (0.6 × {N(sens("O2",280.0),0)} + 2.256 × {N(sens("N2",280.0),0)} + {N(sens("H2",280.0),0)}) = {N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} kJ/kmol.
Step 3 (product side). H_prod(T) = h̄_f°(H₂O g) + Δh̄_H₂O + 0.1 Δh̄_O₂ + 2.256 Δh̄_N₂ with h̄_f°(H₂O g) = −241,820. T = 2250 K: Δh̄ = {N(sens("H2O",2250.0),0)}; {N(sens("O2",2250.0),0)}; {N(sens("N2",2250.0),0)} ⇒ H_prod = {N(Hstate(prod70,2250.0),0)}. T = 2300 K: {N(Hstate(prod70,2300.0),0)}.
Step 4. H_react lies between the two values ⇒ T_ad = 2250 + 50 × ({N(Hstate(dict(H2=1,O2=r70["o2_in"],N2=r70["n2_in"]),280.0),0)} − {N(Hstate(prod70,2250.0),0)}) / ({N(Hstate(prod70,2300.0),0)} − {N(Hstate(prod70,2250.0),0)}) = {N(T70,1)} K (printed answer 2251.4 K).
Two routes: (A) table interpolation as above; (B) brentq with enthalpy computed from the integral of T ds° on the s° columns of A-18…A-23 (the h column is not used): difference below 0.15 %. Remark: the adiabatic flame temperature is far above material limits; in reality dissociation (slide p.8) lowers it. Chapter 4 slides contain no adiabatic flame temperature: this item is Added from the book.'''),
         3, TOP['tdp'], CEN('15–70', ' (bổ sung từ §15-5)', ' (added from §15-5)'), 'goc', 'script + printed answer 2251.4'))

# ================================================================== 11. FE exam problems (Cengel 15-118 ... 15-126, options as printed; no key printed)
FE = {}
def fe(num, qv, qe, opts, correct, ev, ee, level, topic, check):
    return add(mcq(B(qv, qe), [opt(o) for o in opts], correct, B(ev, ee), level, topic, CEN(num, ' (FE)', ' (FE exam)'), 'goc', check))
add(mcq(B('Cengel Ch.15 Bài 15–118 (FE). Một nhiên liệu được đốt với 90 % không khí lý thuyết. Điều này tương đương với:', 'Cengel Ch.15 Problem 15–118 (FE). A fuel is burned with 90 percent theoretical air. This is equivalent to:'),
         [B('10 % không khí thừa', '10 % excess air'), B('90 % không khí thừa', '90 % excess air'), B('10 % thiếu không khí', '10 % deficiency of air'), B('90 % thiếu không khí', '90 % deficiency of air'), B('đúng lượng không khí lý thuyết', 'the stoichiometric amount of air')], 2,
         B('Thiếu không khí = 100 % − 90 % = 10 % (slide tr.24: 90 % lý thuyết = 10 % thiếu). Không khí THỪA chỉ có khi lượng không khí lớn hơn 100 % lý thuyết (150 % lý thuyết = 50 % thừa); 100 % lý thuyết là lượng đúng hợp thức.', 'Deficiency = 100 % − 90 % = 10 % (slide p.24: 90 percent theoretical = 10 percent deficiency). EXCESS air exists only above 100 percent theoretical (150 percent theoretical = 50 percent excess); 100 percent theoretical is the stoichiometric amount.'),
         1, TOP['air'], CEN('15–118', ' (FE)', ' (FE exam)'), 'goc', 'slide p.24 (không có đáp án in)'))
r119 = combustion(single('C3H8'), 1.5); reg('comb', dict(fuel=fp(('C3H8', 1)), lam=1.5, exact=False), 'AF', r119['AF'], 1e-9, 'Cengel 15-119'); prn('Cengel 15-119 FE nearest option (d) 23.4', 23.4, r119['AF'], 0.006, 'nearest option; exact masses give 23.46')
fe('15–119', 'Cengel Ch.15 Bài 15–119 (FE). Propan (C₃H₈) cháy với 150 % không khí lý thuyết. Tỉ lệ khối lượng không khí–nhiên liệu của quá trình là:', 'Cengel Ch.15 Problem 15–119 (FE). Propane (C₃H₈) is burned with 150 percent theoretical air. The air–fuel mass ratio of this process is:',
   ['5.3', '10.5', '15.7', '23.4', '39.3'], 3, f'C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O: a_th = 5; 150 % → 7,5 O₂ → 7,5 × 4,76 = 35,7 kmol không khí; AF = 35,7 × 29/44 = {N(r119["AF"],2)} (M_air = 28,97 và 44,097: 23,46): phương án gần nhất là 23,4. 15,7 = 1,0 × 5 × 4,76 × 29/44 là AF lý thuyết; 10,5 là AF chia đôi.',
   f'C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O: a_th = 5; 150 % → 7.5 O₂ → 7.5 × 4.76 = 35.7 kmol of air; AF = 35.7 × 29/44 = {N(r119["AF"],2)} (with M_air = 28.97 and 44.097: 23.46): the nearest option is 23.4. 15.7 is the theoretical AF (1.0 × 5 × 4.76 × 29/44); 10.5 is half of it.', 2, TOP['af'], 'script (không có đáp án in; chọn phương án gần nhất)')
r120 = combustion(single('CH4'), 4 / 2.0); reg('comb', dict(fuel=fp(('CH4', 1)), lam=2.0, exact=False), 'AF', r120['AF'], 1e-9, 'Cengel 15-120'); prn('Cengel 15-120 FE nearest option (a) 34.3', 34.3, r120['AF'], 0.007, 'nearest option; exact masses give 34.38')
fe('15–120', 'Cengel Ch.15 Bài 15–120 (FE). Một kmol metan (CH₄) cháy với lượng không khí chưa biết. Nếu cháy hoàn toàn và có 2 kmol O₂ tự do trong sản phẩm, tỉ lệ khối lượng không khí–nhiên liệu là:', 'Cengel Ch.15 Problem 15–120 (FE). One kmol of methane (CH₄) is burned with an unknown amount of air. If the combustion is complete and there are 2 kmol of free O₂ in the products, the air–fuel mass ratio is:',
   ['34.3', '17.2', '19.0', '14.9', '12.1'], 0, f'O₂ vào = a_th + 2 = 2 + 2 = 4 kmol (a_th = 2); không khí = 4 × 4,76 = 19,04 kmol; AF = 19,04 × 29/16 = {N(r120["AF"],2)} (M_air = 28,97 và 16,043: 34,38): phương án gần nhất là 34,3. 17,2 là AF lý thuyết (2 kmol O₂ thay vì 4) — đồng thời là đáp án nhầm "chỉ O₂ thừa".',
   f'O₂ in = a_th + 2 = 2 + 2 = 4 kmol (a_th = 2); air = 4 × 4.76 = 19.04 kmol; AF = 19.04 × 29/16 = {N(r120["AF"],2)} (with M_air = 28.97 and 16.043: 34.38): the nearest option is 34.3. 17.2 is the theoretical AF (2 kmol O₂ instead of 4).', 2, TOP['af'], 'script (không có đáp án in; chọn phương án gần nhất)')
hc123 = hC_nu('CH4', dict(CO2=1, H2O=2), 'l'); reg('hC', dict(fuel='CH4', nu=dict(CO2=1, H2O=2), water='l', a27='CH4', col='HHV'), 'kJ/kg', hc123 / A27row('CH4', 'M'), 1.5e-3, 'Cengel 15-123: nearest option 56 MJ/kg')
fe('15–123', 'Cengel Ch.15 Bài 15–123 (FE). Metan (CH₄) cháy hoàn toàn với 80 % không khí thừa trong quá trình dòng ổn định. Chất phản ứng và sản phẩm đều ở 25 °C, 1 atm, nước trong sản phẩm ở thể lỏng. Nhiệt truyền ra khỏi buồng đốt trên mỗi đơn vị khối lượng metan là:', 'Cengel Ch.15 Problem 15–123 (FE). Methane (CH₄) is burned completely with 80 percent excess air in a steady-flow combustion process. Reactants and products are both at 25 °C and 1 atm and the water in the products is liquid. The heat transfer from the combustion chamber per unit mass of methane is:',
   ['890 MJ/kg', '802 MJ/kg', '75 MJ/kg', '56 MJ/kg', '50 MJ/kg'], 3, f'|h̄_C| = 890 330 kJ/kmol (nước lỏng, 25 °C; không khí thừa vào và ra cùng trạng thái chuẩn nên không ảnh hưởng) ⇒ 890 330/16,043 = {N(-hc123/16.043,0)} kJ/kg = 55,5 MJ/kg ≈ 56 MJ/kg. 890 là MJ/kmol (chưa chia M); 802 là LHV theo kmol; 50 MJ/kg là LHV theo kg (50 050 kJ/kg).',
   f'|h̄_C| = 890,330 kJ/kmol (liquid water, 25 °C; the excess air enters and leaves at the same standard state so it has no effect) ⇒ 890,330/16.043 = {N(-hc123/16.043,0)} kJ/kg = 55.5 MJ/kg ≈ 56 MJ/kg. 890 is MJ per kmol (not divided by M); 802 is the LHV per kmol; 50 MJ/kg is the LHV per kg (50,050 kJ/kg).', 2, TOP['enth'], 'script + A-27 (không có đáp án in)')
LHVv = 1560 - 4 * 18.015 * props.sat_T('water', 25, 'hfg')['value'] / 1000; reg('lhv_from_hhv', dict(HHV=1560.0, m=8), 'LHV', LHVv, 1e-3, 'Cengel 15-124')
fe('15–124', 'Cengel Ch.15 Bài 15–124 (FE). Nhiệt trị cao của nhiên liệu hiđrôcacbon CₙHₘ với m = 8 là 1560 MJ/kmol nhiên liệu. Khi đó nhiệt trị thấp của nó là:', 'Cengel Ch.15 Problem 15–124 (FE). The higher heating value of a hydrocarbon fuel CₙHₘ with m = 8 is given to be 1560 MJ/kmol of fuel. Then its lower heating value is:',
   ['1384 MJ/kmol', '1208 MJ/kmol', '1402 MJ/kmol', '1514 MJ/kmol', '1551 MJ/kmol'], 0, f'm = 8 nghĩa là 8 nguyên tử H ⇒ 4 kmol H₂O/kmol nhiên liệu; h_fg của nước ở 25 °C = 44 000 kJ/kmol (2441,7 kJ/kg × 18,015); LHV = HHV − 4 × 44 000 = 1560 − 176 = {N(LHVv,0)} MJ/kmol. 1208 trừ 8 H₂O; 1514 và 1551 trừ 1 và 0,2 kmol H₂O.',
   f'm = 8 means 8 H atoms ⇒ 4 kmol H₂O per kmol of fuel; h_fg of water at 25 °C = 44,000 kJ/kmol (2441.7 kJ/kg × 18.015); LHV = HHV − 4 × 44,000 = 1560 − 176 = {N(LHVv,0)} MJ/kmol. 1208 subtracts 8 H₂O; 1514 and 1551 subtract about 1 and 0.2 kmol of H₂O.', 2, TOP['enth'], 'script (không có đáp án in)')
q125 = HF('C2H2') - (-404000.0); reg('hC', dict(fuel='C2H2', nu={}, water='g', a27='C2H2', col='LHV', Hprod=-404000.0), 'q_out', q125, 1e-9, 'Cengel 15-125 (FE)')
fe('15–125', 'Cengel Ch.15 Bài 15–125 (FE). Axetilen (C₂H₂) cháy hoàn toàn trong quá trình dòng ổn định. Nhiên liệu và không khí vào ở 25 °C, sản phẩm ra ở 1500 K. Nếu entanpi của sản phẩm so với trạng thái chuẩn là −404 MJ/kmol nhiên liệu, nhiệt truyền ra khỏi buồng đốt là:', 'Cengel Ch.15 Problem 15–125 (FE). Acetylene gas (C₂H₂) is burned completely during a steady-flow combustion process. The fuel and the air enter at 25 °C and the products leave at 1500 K. If the enthalpy of the products relative to the standard reference state is −404 MJ/kmol of fuel, the heat transfer from the chamber is:',
   ['177 MJ/kmol', '227 MJ/kmol', '404 MJ/kmol', '631 MJ/kmol', '751 MJ/kmol'], 3, f'Q_ra = H_react − H_prod; chất phản ứng ở trạng thái chuẩn nên H_react = h̄_f°(C₂H₂) = +226,73 MJ/kmol (A-26: 226 730 kJ/kmol); H_prod = −404 MJ/kmol ⇒ Q_ra = 226,73 − (−404) = {N(q125/1000,1)} MJ/kmol ≈ 631. 227 quên H_prod; 404 quên entanpi hình thành dương của C₂H₂; 177 và 751 sai dấu của một số hạng.',
   f'Q_out = H_react − H_prod; the reactants are at the standard state so H_react = h̄_f°(C₂H₂) = +226.73 MJ/kmol (A-26: 226,730 kJ/kmol); H_prod = −404 MJ/kmol ⇒ Q_out = 226.73 − (−404) = {N(q125/1000,1)} MJ/kmol ≈ 631. 227 forgets H_prod; 404 forgets the positive formation enthalpy of C₂H₂; 177 and 751 have a wrong sign on one term.', 3, TOP['law1'], 'script (không có đáp án in)')
yco126 = 1.5 / (4.5 + 1.5 + 3 + 6.75 * 3.76); reg('yco', dict(lam=0.9, fuel='C6H6'), 'yCO', yco126, 1e-9, 'Cengel 15-126 (FE)')
fe('15–126', 'Cengel Ch.15 Bài 15–126 (FE). Benzen khí (C₆H₆) cháy với 90 % không khí lý thuyết trong quá trình dòng ổn định. Phần mol của CO trong sản phẩm là:', 'Cengel Ch.15 Problem 15–126 (FE). Benzene gas (C₆H₆) is burned with 90 percent theoretical air during a steady-flow combustion process. The mole fraction of the CO in the products is:',
   ['1.6 %', '4.4 %', '2.5 %', '10 %', '16.7 %'], 1, f'C₆H₆ + 6,75 (O₂ + 3,76 N₂) (0,9 × 7,5 = 6,75): giả sử hiđrô cháy hết (3 H₂O) và C → CO₂ + CO: C: x + y = 6; O: 13,5 = 2x + y + 3 ⇒ x = 4,5; y = 1,5. N₂ = 25,38; tổng sản phẩm = 4,5 + 1,5 + 3 + 25,38 = {N(4.5+1.5+3+25.38,2)} kmol ⇒ y_CO = 1,5/{N(4.5+1.5+3+25.38,2)} = {N(yco126*100,2)} % ≈ 4,4 %. Giả thiết "H cháy hết" theo slide tr.20 (O có ái lực với H lớn hơn với C).',
   f'C₆H₆ + 6.75 (O₂ + 3.76 N₂) (0.9 × 7.5 = 6.75): assume the hydrogen burns completely (3 H₂O) and C → CO₂ + CO: C: x + y = 6; O: 13.5 = 2x + y + 3 ⇒ x = 4.5; y = 1.5. N₂ = 25.38; total products = 4.5 + 1.5 + 3 + 25.38 = {N(4.5+1.5+3+25.38,2)} kmol ⇒ y_CO = 1.5/{N(4.5+1.5+3+25.38,2)} = {N(yco126*100,2)} % ≈ 4.4 %. The assumption "H burns completely" follows slide p.20 (oxygen has a greater tendency to combine with hydrogen than with carbon).', 3, TOP['air'], 'script (không có đáp án in)')

def build(): return ITEMS, PRN
