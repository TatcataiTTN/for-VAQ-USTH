"""Generate the m04 question bank: data/qsrc/m04.json (originals + conceptual, written by gen_m04_orig.py / gen_m04_concept.py), data/qsrc/m04_gen.json (generated variants,
origin 'bo_sung', fixed seed), data/verify/m04_values.json (registry of every numeric answer + printed answers) and data/verify/m04_notes.json (via notes_m04.py).
Run:  .venv/bin/python -I build/gen/gen_m04.py"""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from m04_common import *
import gen_m04_orig as O, gen_m04_concept as CO, notes_m04 as NT
from iapws import IAPWS97 as _I
fp = O.fp
rng = random.Random(20261115)
G = []
TOP = O.TOP
NAME = dict(CH4=('metan', 'methane'), C2H2=('axetilen', 'acetylene'), C2H4=('etylen', 'ethylene'), C2H6=('etan', 'ethane'), C3H6=('propylen', 'propylene'), C3H8=('propan', 'propane'), C4H10=('butan', 'butane'),
            C6H6=('benzen', 'benzene'), C8H18=('octan', 'octane'), C12H26=('dodecan', 'dodecane'), H2=('hiđrô', 'hydrogen'), CH3OH=('metanol', 'methanol'), C2H5OH=('etanol', 'ethanol'), CO=('cacbon monoxit', 'carbon monoxide'))
FRM = dict(CH4='CH₄', C2H2='C₂H₂', C2H4='C₂H₄', C2H6='C₂H₆', C3H6='C₃H₆', C3H8='C₃H₈', C4H10='C₄H₁₀', C6H6='C₆H₆', C8H18='C₈H₁₈', C12H26='C₁₂H₂₆', H2='H₂', CH3OH='CH₃OH', C2H5OH='C₂H₅OH', CO='CO')
def nm(f): return f'{NAME[f][0]} ({FRM[f]})', f'{NAME[f][1]} ({FRM[f]})'
GS = lambda vi, en: dict(vi='Bổ sung – sinh theo dạng ' + vi, en='Added – generated from the type: ' + en)
def gq(qv, qe, correct, wrongs, unit, nd, ev, ee, level, topic, src, check, sep=0.03):
    """numq with distractors closer than sep (relative) to the answer or to each other dropped; at least 3 options required."""
    keep = []
    for w in wrongs:
        v = w[0]
        if abs(v - correct) < sep * max(abs(correct), 1e-9): continue
        if any(abs(v - k[0]) < sep * max(abs(k[0]), 1e-9) for k in keep): continue
        keep.append(w)
    assert len(keep) >= 2, (qv[:60], correct, [w[0] for w in wrongs])
    G.append(O.numq(qv, qe, correct, keep[:4], unit, nd, ev, ee, level, topic, src, check, origin='bo_sung'))
def lamtxt(lam):
    ex = round((lam - 1) * 100); return (f'{ex} % không khí thừa', f'{ex} percent excess air')

# ---------------------------------------------------------------- F1 stoichiometric AF (level 1)
for f in ('C2H4', 'C4H10', 'C6H6', 'CH3OH', 'C2H5OH', 'H2'):
    r = combustion(single(f), 1.0); REGc = O.REGc; REGc([(f, 1)], 1.0, 'AF', r['AF'], f'F1 {f}')
    wr = [(r['o2_in'] * 32 / single(f)['M'], 'bỏ N₂ của không khí', 'drops the N₂ of the air'), (r['air'], 'là AF theo mol (kmol/kmol)', 'is the AF on a mole basis (kmol/kmol)'),
          (r['air'] * 32 / single(f)['M'], 'dùng khối lượng mol của O₂ (32) cho cả không khí', 'uses the molar mass of O₂ (32) for the whole air'), ((single(f)['C']) * 4.76 * 29 / single(f)['M'] if single(f)['H'] else r['AF'] * 1.7, 'bỏ nhu cầu O₂ của hiđrô trong nhiên liệu' if single(f)['H'] else 'nhân sai hệ số', 'omits the O₂ demand of the fuel hydrogen' if single(f)['H'] else 'wrong factor')]
    gq(f'Đốt hoàn toàn {nm(f)[0]} với lượng không khí lý thuyết. Tỉ lệ không khí–nhiên liệu theo khối lượng (M_air = 29, C = 12, H = 1, O = 16) là:', f'Burn {nm(f)[1]} completely with the theoretical amount of air. The air–fuel ratio on a mass basis (M_air = 29, C = 12, H = 1, O = 16) is:',
       r['AF'], wr, 'kg/kg', 2, f'a_th = {N(r["ath"],2)} kmol O₂/kmol nhiên liệu; không khí = 4,76 × {N(r["ath"],2)} = {N(r["air"],2)} kmol; M nhiên liệu = {N(single(f)["M"],0)}; AF = {N(r["air"],2)} × 29/{N(single(f)["M"],0)} = {N(r["AF"],2)} kg/kg.',
       f'a_th = {N(r["ath"],2)} kmol O₂/kmol fuel; air = 4.76 × {N(r["ath"],2)} = {N(r["air"],2)} kmol; fuel molar mass = {N(single(f)["M"],0)}; AF = {N(r["air"],2)} × 29/{N(single(f)["M"],0)} = {N(r["AF"],2)} kg/kg.', 1, TOP['af'], GS('AF hợp thức', 'stoichiometric AF'), 'script (verify_m04: sympy + khối lượng mol A-1/A-27)')
# ---------------------------------------------------------------- F2 AF with excess air (level 2)
for f, ex in (('C3H8', .20), ('C4H10', .40), ('C2H6', .50), ('CH3OH', .30), ('C2H5OH', .60), ('C8H18', .25)):
    lam = 1 + ex; r = combustion(single(f), lam); O.REGc([(f, 1)], lam, 'AF', r['AF'], f'F2 {f} {ex}')
    r1 = combustion(single(f), 1.0); rb = combustion(single(f), ex)
    wr = [(r1['AF'], 'bỏ phần không khí thừa', 'ignores the excess air'), (rb['AF'], f'hiểu {ex*100:.0f} % thừa là {ex*100:.0f} % không khí lý thuyết', f'reads {ex*100:.0f} percent excess as {ex*100:.0f} percent theoretical air'), (r['air'], 'là AF theo mol', 'is the AF on a mole basis'), (r['o2_in'] * 32 / single(f)['M'], 'bỏ N₂ của không khí', 'drops the N₂ of the air')]
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} được đốt với {ex*100:.0f} % không khí thừa, cháy hoàn toàn. Tỉ lệ không khí–nhiên liệu (kg/kg, M_air = 29) là:', f'{nm(f)[1][0].upper()+nm(f)[1][1:]} is burned with {ex*100:.0f} percent excess air, complete combustion. The air–fuel ratio (kg/kg, M_air = 29) is:',
       r['AF'], wr, 'kg/kg', 1, f'Không khí lý thuyết a_th = {N(r["ath"],2)} kmol O₂; thực tế {N(lam,2)} × a_th; AF = {N(lam,2)} × {N(r1["AF"],2)} = {N(r["AF"],2)} kg/kg (AF lý thuyết {N(r1["AF"],2)}).',
       f'Theoretical a_th = {N(r["ath"],2)} kmol O₂; actual {N(lam,2)} × a_th; AF = {N(lam,2)} × {N(r1["AF"],2)} = {N(r["AF"],2)} kg/kg (theoretical AF {N(r1["AF"],2)}).', 2, TOP['air'], GS('AF với không khí thừa', 'AF with excess air'), 'script (verify_m04)')
# ---------------------------------------------------------------- F3 percent theoretical air from a measured AF (level 2)
for f, AFm in (('C3H8', 20.0), ('CH4', 21.0), ('C2H6', 24.0), ('C8H18', 20.5), ('C4H10', 19.0)):
    th = combustion(single(f), 1.0)['AF']; p = AFm / th * 100; reg('pct_af', dict(fuel=fp((f, 1)), AF=AFm), 'pct', p, 1e-9, f'F3 {f}')
    gq(f'Một buồng đốt đốt {nm(f)[0]} với tỉ lệ không khí–nhiên liệu đo được {AFm:g} kg/kg. Phần trăm không khí lý thuyết đã dùng là:', f'A combustor burns {nm(f)[1]} with a measured air–fuel ratio of {AFm:g} kg/kg. The percentage of theoretical air used is:', p,
       [(p - 100, 'là phần trăm không khí THỪA', 'is the percent EXCESS air'), (th / AFm * 100, 'đảo ngược tỉ số', 'inverts the ratio'), (AFm / th * 100 + 100, 'cộng nhầm 100 %', 'adds 100 % by mistake'), ((AFm - th) / AFm * 100, 'chia phần thừa cho AF thực', 'divides the excess by the actual AF')], '%', 0,
       f'AF lý thuyết của {nm(f)[0]} = {N(th,2)} kg/kg; % lý thuyết = {AFm:g}/{N(th,2)} = {N(p,0)} % (tức {N(p-100,0)} % không khí thừa).', f'Theoretical AF of {nm(f)[1]} = {N(th,2)} kg/kg; percent theoretical = {AFm:g}/{N(th,2)} = {N(p,0)} % (i.e. {N(p-100,0)} % excess air).', 2, TOP['air'], GS('% không khí lý thuyết từ AF', 'percent theoretical air from AF'), 'script (verify_m04)')
# ---------------------------------------------------------------- F4 product moles (level 2)
for f, lam, what in (('C3H8', 1.4, 'O2'), ('C4H10', 1.6, 'N2'), ('CH4', 1.5, 'n_tot'), ('C2H5OH', 1.3, 'O2'), ('C8H18', 1.8, 'n_tot')):
    r = combustion(single(f), lam); O.REGc([(f, 1)], lam, what, r[what], f'F4 {f}')
    lbl = dict(O2=('O₂ tự do', 'free O₂'), N2=('N₂', 'N₂'), n_tot=('tổng số mol sản phẩm', 'total product moles')); val = r[what]
    wr = {'O2': [(r['ath'], 'là O₂ lý thuyết, không phải phần thừa', 'is the theoretical O₂, not the excess'), (r['o2_in'], 'là tổng O₂ cấp vào', 'is the total O₂ supplied'), (r['ath'] * (lam - 1) * 2, 'nhân đôi (tính theo O thay vì O₂)', 'doubled (counted as O atoms instead of O₂)')],
          'N2': [(r['air'], 'là số mol không khí (cả O₂)', 'is the moles of air (O₂ included)'), (r['ath'] * R3, 'N₂ của không khí lý thuyết (bỏ phần thừa)', 'N₂ of the theoretical air (ignores the excess)'), (r['o2_in'], 'là số mol O₂ vào', 'is the O₂ moles entering')],
          'n_tot': [(r['n_dry'], 'bỏ H₂O', 'leaves out the H₂O'), (r['n_tot'] + r['o2_in'], 'cộng thêm O₂ cấp vào', 'adds the O₂ supplied'), (r['air'] + 1, 'lấy số mol chất phản ứng (nhiên liệu + không khí)', 'takes the reactant moles (fuel + air)'), (r['n_tot'] - r['CO2'], 'bỏ CO₂', 'leaves out the CO₂'), (r['N2'] + r['O2'], 'chỉ tính N₂ + O₂', 'counts only N₂ + O₂')]}[what]
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} cháy hoàn toàn với {lam*100:.0f} % không khí lý thuyết. Số kmol {lbl[what][0]} trong sản phẩm trên mỗi kmol nhiên liệu là:', f'{nm(f)[1][0].upper()+nm(f)[1][1:]} burns completely with {lam*100:.0f} percent theoretical air. The kmol of {lbl[what][1]} in the products per kmol of fuel is:', val, wr, 'kmol', 2,
       f'a_th = {N(r["ath"],2)}; O₂ vào = {N(lam,2)} × {N(r["ath"],2)} = {N(r["o2_in"],2)}; sản phẩm: {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ (tổng {N(r["n_tot"],2)} kmol).', f'a_th = {N(r["ath"],2)}; O₂ in = {N(lam,2)} × {N(r["ath"],2)} = {N(r["o2_in"],2)}; products: {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ (total {N(r["n_tot"],2)} kmol).',
       2, TOP['af'], GS('số mol sản phẩm', 'product moles'), 'script (verify_m04: sympy)', sep=0.015)
# ---------------------------------------------------------------- F5 dew point (level 3)
for f, lam, P in (('CH4', 1.0, 101.325), ('C3H8', 1.2, 100.0), ('C2H5OH', 1.3, 101.325), ('C8H18', 1.5, 101.325), ('H2', 1.2, 101.325), ('C4H10', 1.1, 150.0)):
    r = combustion(single(f), lam); Pv, Td = dew_point(r['H2O'], r['n_tot'], P); Ti = _I(P=Pv / 1000, x=0).T - 273.15
    reg('dew', dict(fuel=fp((f, 1)), lam=lam, P=P), 'Tdp', Td, {'abs': 0.5}, f'F5 {f} {lam} {P}'); reg('dew', dict(fuel=fp((f, 1)), lam=lam, P=P), 'Pv', Pv, 1e-9, f'F5 Pv {f}')
    Tp = props.sat_P('water', P, 'Tsat_C')['value']; Tdry = dew_point(r['H2O'], r['n_dry'], P)[1]
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} cháy hoàn toàn với {lam*100:.0f} % không khí lý thuyết, áp suất tổng của sản phẩm {P:g} kPa. Nhiệt độ điểm sương của sản phẩm (nội suy A-5) xấp xỉ:', f'{nm(f)[1][0].upper()+nm(f)[1][1:]} burns completely with {lam*100:.0f} percent theoretical air; total product pressure {P:g} kPa. The dew-point temperature of the products (A-5 interpolation) is about:', Td,
       [(Tp, 'là T_sat ở áp suất TỔNG', 'is T_sat at the TOTAL pressure'), (Tdry, 'chia cho số mol sản phẩm khô (bỏ H₂O)', 'divides by the dry product moles (H₂O left out)'), (props.sat_P('water', P * r['H2O'] / (r['n_tot'] + r['air']), 'Tsat_C')['value'], 'dùng cả không khí vào trong mẫu số', 'puts the air moles in the denominator too'), (props.sat_P('water', P * r['H2O'] * 18.0 / (r['CO2'] * 44.0 + r['H2O'] * 18.0 + r['O2'] * 32.0 + r['N2'] * 28.0), 'Tsat_C')['value'], 'dùng phần KHỐI LƯỢNG của H₂O làm phần áp suất', 'uses the MASS fraction of H₂O as the pressure fraction')], '°C', 1,
       f'Sản phẩm: {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ = {N(r["n_tot"],2)} kmol; P_v = {N(r["H2O"],0)}/{N(r["n_tot"],2)} × {P:g} = {N(Pv,2)} kPa; T_dp = T_sat@{N(Pv,2)} kPa = {N(Td,1)} °C (nội suy A-5; IAPWS {N(Ti,1)} °C; dung sai ≤ 0,5 °C).',
       f'Products: {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ = {N(r["n_tot"],2)} kmol; P_v = {N(r["H2O"],0)}/{N(r["n_tot"],2)} × {P:g} = {N(Pv,2)} kPa; T_dp = T_sat@{N(Pv,2)} kPa = {N(Td,1)} °C (A-5 interpolation; IAPWS {N(Ti,1)} °C; tolerance ≤ 0.5 °C).', 3, TOP['dew'], GS('điểm sương của sản phẩm', 'dew point of products'), 'script (verify_m04: nội suy A-5 ↔ iapws)')
# ---------------------------------------------------------------- F6 reverse analysis (level 3): dry composition made from a forward model with CO
for f, lam, fco, ask in (('C3H8', 1.30, 0.10, 'AF'), ('C2H6', 1.15, 0.08, 'pct'), ('C8H18', 1.20, 0.05, 'AF'), ('CH4', 1.40, 0.06, 'pct'), ('C4H10', 1.10, 0.12, 'AF')):
    s = single(f); r = combustion(s, lam); c, h = s['C'], s['H']
    co2, co = c * (1 - fco), c * fco; o2 = r['o2_in'] - (co2 + co / 2 + h / 4); n2 = r['N2']; nd_ = co2 + co + o2 + n2
    pc = [round(100 * x / nd_, 2) for x in (co2, co, o2, n2)]; sm = round(100 - sum(pc), 2); pc[3] = round(pc[3] + sm, 2)
    rv_ = reverse(int(c), int(h), *pc); prm = dict(c=int(c), h=int(h), CO2=pc[0], CO=pc[1], O2=pc[2], N2=pc[3]); reg('rev', prm, ask, rv_[ask], 1e-9, f'F6 {f}')
    th = combustion(s, 1.0)['AF']
    if ask == 'AF':
        correct = rv_['AF']; unit = 'kg/kg'; nd = 1; wr = [(th, 'là AF lý thuyết của nhiên liệu', 'is the theoretical AF of the fuel'), (rv_['air'], 'là AF theo mol', 'is the AF on a mole basis'), (rv_['a'] * 4.76 * 29 / (c * 12 + h), 'lấy 100 kmol sản phẩm khô làm 1 kmol nhiên liệu', 'treats the 100 kmol of dry products as 1 kmol of fuel'), (rv_['a'] * 32 / ((c * 12 + h) * rv_['x']), 'bỏ N₂ của không khí', 'drops the N₂ of the air')]
        qa = ('tỉ lệ không khí–nhiên liệu (kg/kg, M_air = 29)', 'the air–fuel ratio (kg/kg, M_air = 29)')
        ev = f'N₂: a = {N(pc[3],2)}/3,76 = {N(rv_["a"],3)}; C: x = ({N(pc[0],2)} + {N(pc[1],2)})/{int(c)} = {N(rv_["x"],4)}; không khí/kmol nhiên liệu = 4,76 × a/x = {N(rv_["air"],2)} kmol; AF = {N(rv_["air"],2)} × 29/{N(c*12+h,0)} = {N(rv_["AF"],2)} kg/kg.'
        ee = f'N₂: a = {N(pc[3],2)}/3.76 = {N(rv_["a"],3)}; C: x = ({N(pc[0],2)} + {N(pc[1],2)})/{int(c)} = {N(rv_["x"],4)}; air per kmol of fuel = 4.76 × a/x = {N(rv_["air"],2)} kmol; AF = {N(rv_["air"],2)} × 29/{N(c*12+h,0)} = {N(rv_["AF"],2)} kg/kg.'
    else:
        correct = rv_['pct']; unit = '%'; nd = 0; wr = [(rv_['pct'] - 100, 'là phần trăm không khí thừa', 'is the percent excess air'), (100 / rv_['pct'] * 100, 'đảo ngược tỉ số', 'inverts the ratio'), (rv_['pct'] + 100, 'cộng nhầm 100 %', 'adds 100 % by mistake'), (rv_['a'] / (c + h / 4) / 2 * 100, 'chia cho 2 thay vì cho a_th của nhiên liệu', 'divides by 2 instead of by the fuel a_th')]
        qa = ('phần trăm không khí lý thuyết đã dùng', 'the percentage of theoretical air used')
        ev = f'a = {N(pc[3],2)}/3,76 = {N(rv_["a"],3)}; x = {N(rv_["x"],4)} kmol nhiên liệu; O₂/kmol nhiên liệu = a/x = {N(rv_["a"]/rv_["x"],3)}; a_th = {N(c + h/4,2)}; % = {N(rv_["a"]/rv_["x"],3)}/{N(c+h/4,2)} = {N(rv_["pct"],0)} %.'
        ee = f'a = {N(pc[3],2)}/3.76 = {N(rv_["a"],3)}; x = {N(rv_["x"],4)} kmol of fuel; O₂ per kmol of fuel = a/x = {N(rv_["a"]/rv_["x"],3)}; a_th = {N(c + h/4,2)}; % = {N(rv_["a"]/rv_["x"],3)}/{N(c+h/4,2)} = {N(rv_["pct"],0)} %.'
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} cháy với không khí khô; phân tích thể tích sản phẩm trên cơ sở khô: CO₂ {pc[0]:.2f} %; CO {pc[1]:.2f} %; O₂ {pc[2]:.2f} %; N₂ {pc[3]:.2f} %. Xác định {qa[0]}:', f'{nm(f)[1][0].upper()+nm(f)[1][1:]} is burned with dry air; the volumetric analysis of the products on a dry basis is CO₂ {pc[0]:.2f} %, CO {pc[1]:.2f} %, O₂ {pc[2]:.2f} %, N₂ {pc[3]:.2f} %. Determine {qa[1]}:',
       correct, wr, unit, nd, ev, ee, 3, TOP['rev'], GS('phân tích cháy ngược', 'reverse combustion analysis'), 'script (verify_m04: sympy hữu tỉ)', sep=0.04)
# ---------------------------------------------------------------- F7 condensed fraction (level 3)
for f, lam, P, T in (('CH4', 1.0, 101.325, 25.0), ('C3H8', 1.2, 101.325, 30.0), ('C2H6', 1.0, 100.0, 20.0), ('C8H18', 1.3, 101.325, 40.0)):
    r = combustion(single(f), lam); Nw = condensed(r['H2O'], r['n_tot'], P, T); fr = Nw / r['H2O'] * 100; Ps = props.sat_T('water', T, 'Psat_kPa')['value']
    reg('cond', dict(fuel=fp((f, 1)), lam=lam, P=P, T=T), 'frac', fr / 100, 2e-3, f'F7 {f}')
    gq(f'Sản phẩm cháy hoàn toàn của {nm(f)[0]} với {lam*100:.0f} % không khí lý thuyết được làm nguội tới {T:g} °C ở {P:g} kPa (P_sat@{T:g} °C = {N(Ps,4)} kPa). Phần trăm hơi nước ngưng tụ là:', f'The products of complete combustion of {nm(f)[1]} with {lam*100:.0f} percent theoretical air are cooled to {T:g} °C at {P:g} kPa (P_sat@{T:g} °C = {N(Ps,4)} kPa). The percentage of the water vapor that condenses is:', fr,
       [(r['H2O'] / r['n_tot'] * 100, 'là phần mol hơi nước trong sản phẩm', 'is the mole fraction of vapor in the products'), (100 - fr, 'là phần hơi nước CÒN LẠI', 'is the vapor REMAINING'), ((r['H2O'] - Ps / P * r['n_tot']) / r['H2O'] * 100, 'quên rằng mẫu số cũng giảm đi N_w', 'forgets that the denominator also shrinks by N_w'), (100.0, 'cho rằng toàn bộ hơi nước ngưng tụ', 'assumes all the vapor condenses')], '%', 0,
       f'N_v = {N(r["H2O"],0)}, N_prod = {N(r["n_tot"],2)} kmol; (N_v − N_w)/(N_prod − N_w) = {N(Ps,4)}/{P:g} ⇒ N_w = {N(Nw,3)} kmol = {N(fr,1)} % (slide tr.38–39).', f'N_v = {N(r["H2O"],0)}, N_prod = {N(r["n_tot"],2)} kmol; (N_v − N_w)/(N_prod − N_w) = {N(Ps,4)}/{P:g} ⇒ N_w = {N(Nw,3)} kmol = {N(fr,1)} % (slide p.38–39).', 3, TOP['dew'], GS('lượng nước ngưng tụ', 'condensed water'), 'script (verify_m04: iapws + brentq)')
# ---------------------------------------------------------------- F8 enthalpy of combustion from A-26 (level 2)
MX = dict(CH4=16.043, C2H2=26.038, C2H4=28.054, C2H6=30.07, C3H8=44.097, C4H10=58.123, C6H6=78.114, CH3OH=32.042, C2H5OH=46.069, H2=2.016, CO=28.013, C8H18=114.231)
CASES = (('C2H6', 'C2H6', dict(CO2=2, H2O=3), 'g', 'kJ/kmol'), ('C3H8', 'C3H8', dict(CO2=3, H2O=4), 'l', 'kJ/kg'), ('C4H10', 'C4H10', dict(CO2=4, H2O=5), 'g', 'kJ/kg'), ('CH3OH', 'CH3OH_l', dict(CO2=1, H2O=2), 'l', 'kJ/kmol'),
         ('C2H2', 'C2H2', dict(CO2=2, H2O=1), 'g', 'kJ/kg'), ('C6H6', 'C6H6', dict(CO2=6, H2O=3), 'l', 'kJ/kmol'))
for f, key, nu, w, per in CASES:
    h = hC_nu(key, nu, w); hg = hC_nu(key, nu, 'g' if w == 'l' else 'l'); a27 = f if f in A27 else None
    val = h / MX[f] if per == 'kJ/kg' else h; unit = per
    reg('hC', dict(fuel=key, nu=nu, water=w, a27=a27, col=('HHV' if w == 'l' else 'LHV'), M=MX[f], liq_listed=f in ('C4H10', 'C6H6')), unit, val, 3e-3 if a27 else 1.5e-4, f'F8 {f} {w}')
    hs = 'HHV' if w == 'l' else 'LHV'; he = hs
    other = (hg / MX[f] if per == 'kJ/kg' else hg)
    gq(f'Dùng bảng A-26, entanpi cháy của {nm(f)[0]} ở 25 °C, 1 atm với H₂O trong sản phẩm ở thể {"lỏng" if w=="l" else "hơi"} ({hs}) tính trên {"1 kg nhiên liệu (M = " + N(MX[f],3) + " kg/kmol)" if per=="kJ/kg" else "1 kmol nhiên liệu"} là:',
       f'Using Table A-26, the enthalpy of combustion of {nm(f)[1]} at 25 °C and 1 atm with {"liquid" if w=="l" else "vapor"} H₂O in the products ({he}) per {"kg of fuel (M = " + N(MX[f],3) + " kg/kmol)" if per=="kJ/kg" else "kmol of fuel"} is:', val,
       [(-val, 'sai dấu', 'wrong sign'), (other, f'dùng H₂O {"hơi" if w=="l" else "lỏng"} thay vì {"lỏng" if w=="l" else "hơi"}', f'uses {"vapor" if w=="l" else "liquid"} H₂O instead of {"liquid" if w=="l" else "vapor"}'), (val + HF(key) * (1 / MX[f] if per == 'kJ/kg' else 1), 'quên trừ h̄_f° của nhiên liệu', 'forgets to subtract the h̄_f° of the fuel'), (val * (MX[f] if per == 'kJ/kg' else 1 / MX[f]), 'nhầm đơn vị kJ/kg ↔ kJ/kmol', 'mixes kJ/kg and kJ/kmol')], unit, 0,
       f'h̄_C = Σ N_p h̄_f°(sản phẩm) − h̄_f°(nhiên liệu) = {N(h,0)} kJ/kmol' + (f' ⇒ chia cho M = {N(MX[f],3)}: {N(val,0)} kJ/kg' if per == 'kJ/kg' else '') + (f' (A-27 {"HHV" if w=="l" else "LHV"}: {N(A27row(a27, "HHV" if w=="l" else "LHV"),0)} kJ/kg)' if a27 and per == 'kJ/kg' else '') + '.',
       f'h̄_C = Σ N_p h̄_f°(products) − h̄_f°(fuel) = {N(h,0)} kJ/kmol' + (f' ⇒ divided by M = {N(MX[f],3)}: {N(val,0)} kJ/kg' if per == 'kJ/kg' else '') + (f' (A-27 {"HHV" if w=="l" else "LHV"}: {N(A27row(a27, "HHV" if w=="l" else "LHV"),0)} kJ/kg)' if a27 and per == 'kJ/kg' else '') + '.',
       2, TOP['enth'], GS('entanpi cháy từ entanpi hình thành', 'enthalpy of combustion from formation enthalpies'), 'script (verify_m04: A-26 ↔ A-27)')
# ---------------------------------------------------------------- F9 HHV -> LHV (level 2)
hfg25 = props.sat_T('water', 25, 'hfg')['value']
for f, HHV in (('CH4', 55530.0), ('C2H6', 51900.0), ('C3H8', 50330.0), ('C8H18', 47890.0)):
    s = single(f); mH = s['H'] / 2 * 18.015 / MX[f]; LHV = HHV - mH * hfg25; reg('lhv_kg', dict(HHV=HHV, H=s['H'], M=MX[f]), 'LHV', LHV, 2e-3, f'F9 {f}: A-27 {A27row(f,"LHV")}')
    gq(f'Nhiệt trị cao của {nm(f)[0]} là {HHV:,.0f} kJ/kg. Với khối lượng H₂O sinh ra {N(mH,3)} kg/kg nhiên liệu và h_fg(25 °C) = {N(hfg25,1)} kJ/kg, nhiệt trị thấp là:', f'The higher heating value of {nm(f)[1]} is {HHV:,.0f} kJ/kg. With {N(mH,3)} kg of H₂O formed per kg of fuel and h_fg(25 °C) = {N(hfg25,1)} kJ/kg, the lower heating value is:', LHV,
       [(HHV + mH * hfg25, 'cộng thay vì trừ (LHV lớn hơn HHV)', 'adds instead of subtracts (LHV larger than HHV)'), (HHV - hfg25, 'chỉ trừ h_fg của 1 kg nước', 'subtracts the h_fg of only 1 kg of water'), (HHV - mH * hfg25 / 2, 'chỉ tính nửa lượng nước', 'counts only half the water'), (HHV - mH * hfg25 * 2, 'tính gấp đôi lượng nước', 'counts twice the water')], 'kJ/kg', 0,
       f'LHV = HHV − m h_fg = {HHV:,.0f} − {N(mH,3)} × {N(hfg25,1)} = {N(LHV,0)} kJ/kg (A-27: {A27row(f,"LHV"):,.0f}).', f'LHV = HHV − m h_fg = {HHV:,.0f} − {N(mH,3)} × {N(hfg25,1)} = {N(LHV,0)} kJ/kg (A-27: {A27row(f,"LHV"):,.0f}).', 2, TOP['enth'], GS('HHV ↔ LHV', 'HHV ↔ LHV'), 'script (verify_m04: A-27 LHV)')
# ---------------------------------------------------------------- F10 first law with sensible enthalpy (level 3)
for f, lam, Tp in (('CH4', 1.5, 1000.0), ('C3H8', 1.2, 1200.0), ('C2H2', 2.0, 800.0), ('C2H6', 1.3, 1400.0)):
    r = combustion(single(f), lam); rea = {f: 1, 'O2': r['o2_in'], 'N2': r['n2_in']}; pro = {k: v for k, v in dict(CO2=r['CO2'], H2O_g=r['H2O'], O2=r['O2'], N2=r['N2']).items() if v > 0}
    q = q_out(rea, 298, pro, Tp); qh = -hC_nu(f, {'CO2': r['CO2'], 'H2O': r['H2O']}, 'g'); ql = -hC_nu(f, {'CO2': r['CO2'], 'H2O': r['H2O']}, 'l')
    reg('q', dict(react=O.lst([(f, 1, 298.0), ('O2', r['o2_in'], 298.0), ('N2', r['n2_in'], 298.0)]), prod=O.lst([(k, v, Tp) for k, v in pro.items()])), 'q_out', q, 4e-3, f'F10 {f} {lam} {Tp}')
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} và không khí vào buồng đốt dòng ổn định ở 25 °C; cháy hoàn toàn với {lam*100:.0f} % không khí lý thuyết, sản phẩm ra ở {Tp:g} K. Nhiệt truyền ra khỏi buồng đốt trên mỗi kmol nhiên liệu (A-26, A-18…A-23) là:',
       f'{nm(f)[1][0].upper()+nm(f)[1][1:]} and air enter a steady-flow chamber at 25 °C; complete combustion with {lam*100:.0f} percent theoretical air, products leave at {Tp:g} K. The heat transferred out per kmol of fuel (A-26, A-18…A-23) is:', q,
       [(qh, 'bỏ entanpi hiển nhiệt của sản phẩm (chỉ LHV)', 'drops the sensible enthalpy of the products (LHV only)'), (ql, 'dùng nhiệt trị cao, sản phẩm ở 25 °C với nước lỏng', 'uses the HHV: products at 25 °C with liquid water'), (q_out(rea, 298, {k: v for k, v in dict(CO2=r['CO2'], H2O_g=r['H2O'], N2=r['ath'] * R3).items() if v > 0}, Tp), 'bỏ O₂ thừa và N₂ của không khí thừa khỏi sản phẩm', 'leaves the excess O₂ and the N₂ of the excess air out of the products'), (q_out(rea, 298, pro, Tp + 273.15), f'đọc {Tp:g} °C thay cho {Tp:g} K', f'reads {Tp:g} °C instead of {Tp:g} K')], 'kJ/kmol', 0,
       f'Chất phản ứng ở trạng thái chuẩn: H_react = h̄_f°(nhiên liệu) = {N(HF(f),0)}; sản phẩm {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ tại {Tp:g} K: H_prod = Σ N(h̄_f° + h̄(T) − h̄_298) = {N(Hstate(pro,Tp),0)} kJ/kmol ⇒ Q_ra = H_react − H_prod = {N(q,0)} kJ/kmol.',
       f'Reactants are at the standard state: H_react = h̄_f°(fuel) = {N(HF(f),0)}; products {N(r["CO2"],0)} CO₂ + {N(r["H2O"],0)} H₂O + {N(r["O2"],2)} O₂ + {N(r["N2"],2)} N₂ at {Tp:g} K: H_prod = Σ N(h̄_f° + h̄(T) − h̄_298) = {N(Hstate(pro,Tp),0)} kJ/kmol ⇒ Q_out = H_react − H_prod = {N(q,0)} kJ/kmol.', 3, TOP['law1'], GS('định luật 1 cho cháy', 'first law for combustion'), 'script (verify_m04: A-18…A-23 ↔ ∫T ds° ↔ A-2c)')
# ---------------------------------------------------------------- F11 adiabatic flame temperature (level 3)
for f, lam in (('C3H8', 1.6), ('CH4', 1.7)):
    Tf, r, pro = O.tad_case(f, lam, 298.0, 298.0); O.Tad_reg(f, lam, 298.0, 0.0, 'T', f'F11 {f} {lam}', Tf)
    gq(f'{nm(f)[0][0].upper()+nm(f)[0][1:]} và không khí ở 25 °C cháy hoàn toàn đoạn nhiệt trong dòng ổn định với {lam*100:.0f} % không khí lý thuyết. Nhiệt độ sản phẩm (A-18…A-23) xấp xỉ:', f'{nm(f)[1][0].upper()+nm(f)[1][1:]} and air at 25 °C burn completely and adiabatically in steady flow with {lam*100:.0f} percent theoretical air. The product temperature (A-18…A-23) is about:', Tf,
       [(O.tad_case(f, 1.0, 298.0, 298.0)[0], 'bỏ phần không khí thừa (λ = 1)', 'ignores the excess air (λ = 1)'), (O.tad_case(f, lam + 1.0, 298.0, 298.0)[0], 'hiểu thành thừa thêm 100 % không khí nữa', 'adds another 100 % of air by mistake'), (O.T_ad_hf({f: 1, 'O2': r['o2_in'], 'N2': r['n2_in']}, 298.0, pro, water_liquid_hf=True), 'dùng h̄_f° của H₂O lỏng cho hơi nước ở nhiệt độ cao', 'uses the h̄_f° of liquid H₂O for the hot vapor'), (298.0 + (-hC_nu(f, {'CO2': r['CO2'], 'H2O': r['H2O']}, 'g')) / (sum(pro.values()) * 33.0), 'dùng c̄_p = 33 kJ/(kmol·K) không đổi', 'uses a constant c̄_p = 33 kJ/(kmol·K)')], 'K', 0,
       f'Cân bằng H_prod(T) = H_react = {N(HF(f),0)} kJ/kmol (mọi chất ở 25 °C). Nội suy trong A-18…A-23: T_ad = {N(Tf,0)} K. Thực tế phân ly làm nhiệt độ thấp hơn (slide tr.8); slide Ch.4 không có nhiệt độ ngọn lửa đoạn nhiệt: đây là Bổ sung từ sách (Cengel §15-5).',
       f'Balance H_prod(T) = H_react = {N(HF(f),0)} kJ/kmol (everything at 25 °C). Interpolating A-18…A-23: T_ad = {N(Tf,0)} K. In reality dissociation lowers it (slide p.8); the Chapter 4 slides have no adiabatic flame temperature: this is Added from the book (Cengel §15-5).', 3, TOP['tdp'], GS('nhiệt độ ngọn lửa đoạn nhiệt', 'adiabatic flame temperature'), 'script (verify_m04: brentq trên ∫T ds°)', sep=0.05)
# ---------------------------------------------------------------- F12 equivalence ratio (level 2)
for f, AFm in (('C8H18', 40.0), ('CH4', 13.0), ('C3H8', 25.0)):
    th = combustion(single(f), 1.0)['AF']; phi = th / AFm; reg('phi', dict(fuel=fp((f, 1)), AF=AFm), 'phi', phi, 1e-9, f'F12 {f}')
    gq(f'Một buồng đốt đốt {nm(f)[0]} với tỉ lệ không khí–nhiên liệu thực {AFm:g} kg/kg (AF hợp thức {N(th,2)} kg/kg). Hệ số tương đương φ = (F/A)thực/(F/A)hợp thức là:', f'A combustor burns {nm(f)[1]} with an actual air–fuel ratio of {AFm:g} kg/kg (stoichiometric AF {N(th,2)} kg/kg). The equivalence ratio φ = (F/A)act/(F/A)st is:', phi,
       [(AFm / th, 'là nghịch đảo (tỉ lệ không khí thực/lý thuyết)', 'is the inverse (actual/theoretical air ratio)'), (abs(1 - phi), 'là |1 − φ|, độ lệch so với hợp thức', 'is |1 − φ|, the deviation from stoichiometric'), (th / (AFm + th), 'chia cho tổng AF thực và AF hợp thức', 'divides by the sum of actual and stoichiometric AF'), (AFm / (AFm + th), 'chia AF thực cho tổng hai AF', 'divides the actual AF by the sum of the two AF')], '', 2,
       f'φ = (A/F)hợp thức/(A/F)thực = {N(th,2)}/{AFm:g} = {N(phi,2)} ' + ('< 1: hỗn hợp nghèo (thừa không khí).' if phi < 1 else '> 1: hỗn hợp giàu.'), f'φ = (A/F)st/(A/F)act = {N(th,2)}/{AFm:g} = {N(phi,2)} ' + ('< 1: a lean mixture (excess air).' if phi < 1 else '> 1: a rich mixture.'), 2, TOP['air'], GS('hệ số tương đương', 'equivalence ratio'), 'script (verify_m04)')
# ---------------------------------------------------------------- F13 air flow rate (level 2)
for f, lam, mf in (('C8H18', 1.5, 0.020), ('C3H8', 1.3, 0.050), ('C2H6', 1.1, 0.100)):
    r = combustion(single(f), lam); ma = r['AF'] * mf; reg('airflow', dict(fuel=fp((f, 1)), lam=lam, mf=mf), 'kg/s', ma, 1e-9, f'F13 {f}')
    gq(f'Lưu lượng khối lượng nhiên liệu {nm(f)[0]} là {mf:g} kg/s, đốt với {lam*100:.0f} % không khí lý thuyết. Lưu lượng không khí cần cấp (kg/s, M_air = 29) là:', f'The fuel mass flow of {nm(f)[1]} is {mf:g} kg/s, burned with {lam*100:.0f} percent theoretical air. The required air flow (kg/s, M_air = 29) is:', ma,
       [(combustion(single(f), 1.0)['AF'] * mf, 'dùng không khí lý thuyết', 'uses the theoretical air'), (r['air'] * mf, 'dùng AF theo mol', 'uses the mole-basis AF'), (combustion(single(f), 1.0)['AF'] * mf / lam, 'chia thay vì nhân cho hệ số không khí thừa', 'divides instead of multiplies by the excess-air factor'), (r['o2_in'] * 32 * mf / single(f)['M'], 'bỏ N₂ của không khí', 'drops the N₂ of the air')], 'kg/s', 3,
       f'AF = {N(r["AF"],2)} kg/kg ({N(lam,2)} × AF lý thuyết); ṁ_air = AF × ṁ_fuel = {N(r["AF"],2)} × {mf:g} = {N(ma,3)} kg/s.', f'AF = {N(r["AF"],2)} kg/kg ({N(lam,2)} × the theoretical AF); ṁ_air = AF × ṁ_fuel = {N(r["AF"],2)} × {mf:g} = {N(ma,3)} kg/s.', 2, TOP['af'], GS('lưu lượng không khí', 'air flow rate'), 'script (verify_m04)')

# ================================================================== write everything
def main():
    orig, prn = O.build(); conc = CO.build(); items_src = orig + conc
    closed = [i for i in items_src + G if i['kind'] != 'ess']; l3 = [i for i in closed if i['level'] == 3]
    sa = os.path.join(ROOT, 'data', 'qsrc'); os.makedirs(sa, exist_ok=True)
    dump(os.path.join(sa, 'm04.json'), items_src); dump(os.path.join(sa, 'm04_gen.json'), G)
    r2 = combustion(single('C2H6'), 1.2); Pv2, T2 = dew_point(r2['H2O'], r2['n_tot'], 100.0)
    gas3 = mix([('CH4', .72), ('H2', .09), ('N2', .14), ('O2', .02), ('CO2', .03)]); r3 = combustion(gas3, 1.0); Pva = 0.8 * props.sat_T('water', 20, 'Psat_kPa')['value']; Nva = Pva / (101.325 - Pva) * r3['air']
    r3m = combustion(gas3, 1.0, moist=Nva); Pv3 = r3m['H2O'] / r3m['n_tot'] * 101.325
    extra = dict(Ti_ex152=_I(P=Pv2 / 1000, x=0).T - 273.15, Ti_ex153=_I(P=Pv3 / 1000, x=0).T - 273.15, hfg25=(_I(T=298.15, x=1).h - _I(T=298.15, x=0).h) * 18.015, Psat25_iapws=_I(T=298.15, x=0).P * 1000,
                 A5_maxerr=max(abs(props.sat_P('water', float(P), 'Tsat_C')['value'] - (_I(P=float(P) / 1000, x=0).T - 273.15)) for P in [7.5 + 0.25 * k for k in range(0, 770)]))
    dump(os.path.join(ROOT, 'data', 'verify', 'm04_values.json'), dict(registry=REG, printed=prn, extra=extra))
    notes = NT.build(); dump(os.path.join(ROOT, 'data', 'verify', 'm04_notes.json'), notes)
    print(f'originals+conceptual {len(items_src)} (ess {sum(1 for i in items_src if i["kind"]=="ess")}, goc closed {sum(1 for i in items_src if i["kind"]!="ess" and i["origin"]=="goc")}) | generated {len(G)} | closed {len(closed)} | level 3: {len(l3)} ({100*len(l3)/len(closed):.0f} %) | registry {len(REG)} | printed {len(prn)} | notes vi/en {len(notes["vi"])}/{len(notes["en"])}')
if __name__ == '__main__': main()
