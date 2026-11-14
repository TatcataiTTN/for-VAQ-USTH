"""m03 generator: writes data/qsrc/m03.json (originals + slide/book conceptual questions), data/qsrc/m03_gen.json (generated variants, fixed seed),
data/verify/m03_values.json (registry of every numeric answer + printed answers + FE values, recomputed by build/verify/verify_m03.py through a different route).
Run:  .venv/bin/python -I build/gen/gen_m03.py"""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from m03_common import *
import gen_m03_orig as O, gen_m03_concept as CO, notes_m03 as NT

rng = random.Random(20261115)
GEN = lambda vi, en: B(f'Bổ sung – sinh theo dạng {vi}', f'Added – generated from the type: {en}')
TOP = dict(carnot=B('Chu trình Carnot đảo ngược', 'Reversed Carnot cycle'), vcrc=B('Chu trình nén hơi lý tưởng', 'Ideal vapor-compression cycle'),
           real=B('Chu trình lạnh thực', 'Real refrigeration cycle'), gas=B('Chu trình khí lạnh', 'Gas refrigeration cycle'),
           rhp=B('Tủ lạnh, bơm nhiệt, COP', 'Refrigerators, heat pumps, COP'), pack=B('Cooling pack / ACM', 'Cooling pack / ACM'),
           units=B('Đơn vị và quy đổi', 'Units and conversions'), humid=B('Điểm sương', 'Dew point'))
G = []
def add(it): G.append(it)
def M(q, correct, wrongs, unit, nd, expl, lvl, topic, src, check='script (verify_m03: bảng ↔ CoolProp / công thức)'):
    add(mcq(q, numopts(correct, wrongs, unit, nd), 0, expl, lvl, TOP[topic], src, 'bo_sung', check))
def Tf(q, truth, expl, lvl, topic, src, check='công thức + script'): add(tf(q, truth, expl, lvl, TOP[topic], src, 'bo_sung', check))
TV = lambda: 'x'
def Rv(Pl, Ph):
    c = vcrc_ideal(Pl, Ph)
    for k in ('h1', 'h2', 'h3', 'qL', 'w', 'qH', 'cop', 'x4', 'T2'):
        reg('vcrc_ideal', dict(Pl=Pl, Ph=Ph), k, c[k], {'abs': 0.06} if k[0] in 'hqw' else ({'abs': 0.003} if k == 'x4' else ({'abs': 0.3} if k == 'T2' else 5e-3)), 'generated')
    return c

# ================================================================ Carnot (slide tr.13)
for TLc, THc in ((-10, 35), (0, 40), (-20, 30)):
    TL, TH = c2k(TLc), c2k(THc); cop = carnot_R(TL, TH); reg('carnot', dict(TL=TL, TH=TH), 'cop', cop, 3e-3, 'generated')
    M(B(f'Một tủ lạnh Carnot đảo ngược giữ không gian lạnh ở {TLc} °C và thải nhiệt ra môi trường ở {THc} °C. COP của nó là:', f'A reversed-Carnot refrigerator keeps the cold space at {TLc} °C and rejects heat to the environment at {THc} °C. Its COP is:'),
      cop, [carnot_HP(TL, TH), TH / TL - 1, TL / TH], '', 2,
      B(f'COP_R,Carnot = 1/(T_H/T_L − 1) = T_L/(T_H − T_L) = {N(TL,2)}/{N(TH-TL,0)} = {N(cop,2)} (slide tr.13; nhiệt độ đổi sang K). {N(carnot_HP(TL,TH),2)} là COP bơm nhiệt = COP_R + 1; {N(TH/TL-1,3)} là T_H/T_L − 1 chưa nghịch đảo; {N(TL/TH,3)} chỉ là tỉ số nhiệt độ.',
        f'COP_R,Carnot = 1/(T_H/T_L − 1) = T_L/(T_H − T_L) = {N(TL,2)}/{N(TH-TL,0)} = {N(cop,2)} (slide p.13; temperatures in K). {N(carnot_HP(TL,TH),2)} is the heat-pump COP = COP_R + 1; {N(TH/TL-1,3)} is T_H/T_L − 1 not yet inverted; {N(TL/TH,3)} is only the temperature ratio.'), 1, 'carnot', GEN('COP Carnot đảo ngược', 'reversed-Carnot COP'))
TL, TH = c2k(5), c2k(45); hp = carnot_HP(TL, TH); reg('carnot', dict(TL=TL, TH=TH), 'cop_hp', hp, 3e-3, 'generated')
M(B('Một bơm nhiệt Carnot lấy nhiệt từ không khí ngoài trời ở 5 °C và sưởi phòng ở 45 °C. COP của nó là:', 'A Carnot heat pump takes heat from outdoor air at 5 °C and heats a room at 45 °C. Its COP is:'),
  hp, [carnot_R(TL, TH), TL / TH, TH / TL], '', 2,
  B(f'COP_HP,Carnot = 1/(1 − T_L/T_H) = T_H/(T_H − T_L) = {N(TH,2)}/40 = {N(hp,2)} (slide tr.13). {N(carnot_R(TL,TH),2)} là COP_R = COP_HP − 1 của máy lạnh cùng hai nhiệt độ; {N(TL/TH,2)} là tỉ số nhiệt độ; {N(TH/TL,2)} là T_H/T_L chưa dùng công thức COP.',
    f'COP_HP,Carnot = 1/(1 − T_L/T_H) = T_H/(T_H − T_L) = {N(TH,2)}/40 = {N(hp,2)} (slide p.13). {N(carnot_R(TL,TH),2)} is COP_R = COP_HP − 1 of a refrigerator between the same temperatures; {N(TL/TH,2)} is the temperature ratio; {N(TH/TL,2)} is T_H/T_L, not yet the COP formula.'), 1, 'carnot', GEN('COP bơm nhiệt Carnot', 'Carnot heat-pump COP'))
cr = 3.2; M(B(f'Một tủ lạnh có COP_R = {cr}. Nếu cùng thiết bị đó chạy như bơm nhiệt (cùng Q_L, Q_H, công) thì COP_HP là:', f'A refrigerator has COP_R = {cr}. If the same machine is run as a heat pump (same Q_L, Q_H and work), its COP_HP is:'),
  cr + 1, [cr - 1, 1 / cr, cr], '', 1,
  B(f'Q_H = Q_L + W ⇒ COP_HP = Q_H/W = COP_R + 1 = {cr + 1} (Cengel Hệ thức 11–3). COP_R − 1 = {cr - 1} trừ sai dấu; 1/COP_R = {N(1/cr,2)} nghịch đảo; giữ nguyên {cr} quên rằng công cũng thành nhiệt thải.',
    f'Q_H = Q_L + W ⇒ COP_HP = Q_H/W = COP_R + 1 = {cr + 1} (Cengel Eq. 11–3). COP_R − 1 = {cr - 1} subtracts; 1/COP_R = {N(1/cr,2)} inverts; keeping {cr} forgets that the work also ends up as rejected heat.'), 1, 'rhp', GEN('COP_HP = COP_R + 1', 'COP_HP = COP_R + 1'))
reg('identity', dict(cop_r=cr), 'cop_hp', cr + 1, 1e-12, 'generated')
COPr, THK = 5.0, 310.0; TLK = COPr * THK / (1 + COPr)
M(B('Tủ lạnh Carnot có COP_R = 5,0 và thải nhiệt ở 310 K. Nhiệt độ không gian lạnh T_L (°C) là:', 'A Carnot refrigerator has COP_R = 5.0 and rejects heat at 310 K. The cold-space temperature T_L (°C) is:'),
  TLK - 273.15, [310 / (1 + 5) - 273.15, 310 * 5 - 273.15, TLK], '°C', 1,
  B(f'COP = T_L/(T_H − T_L) ⇒ T_L = COP·T_H/(1 + COP) = 5·310/6 = {N(TLK,1)} K = {N(TLK-273.15,1)} °C. T_H/(1 + COP) = {N(310/6-273.15,1)} °C là nhầm biến đổi; {N(TLK,1)} chưa đổi sang °C.',
    f'COP = T_L/(T_H − T_L) ⇒ T_L = COP·T_H/(1 + COP) = 5·310/6 = {N(TLK,1)} K = {N(TLK-273.15,1)} °C. T_H/(1 + COP) = {N(310/6-273.15,1)} °C is an algebra slip; {N(TLK,1)} is not yet converted to °C.'), 2, 'carnot', GEN('suy T_L từ COP Carnot', 'T_L from the Carnot COP'))
reg('carnot_inverse', dict(cop=5.0, TH=310.0), 'TL', TLK, 1e-9, 'generated')

# ================================================================ ideal vapor-compression cycle: Q_L, W, Q_H, COP, x4, mass flow for a table pressure pair (slides tr.19-25)
PAIRS = [(180, 900), (200, 1000), (240, 1200), (140, 1000), (320, 1400), (100, 800), (120, 900), (160, 800)]
for (Pl, Ph), m in ((PAIRS[0], 0.04), (PAIRS[1], 0.08)):
    c = Rv(Pl, Ph); QL, W, QH = m * c['qL'], m * c['w'], m * c['qH']
    M(B(f'Tủ lạnh dùng R-134a, chu trình nén hơi lý tưởng giữa {Pl} kPa và {Ph} kPa, ṁ = {m} kg/s. Nhiệt lượng lấy khỏi không gian lạnh Q̇_L (kW) là:', f'A refrigerator uses R-134a on the ideal vapor-compression cycle between {Pl} kPa and {Ph} kPa, ṁ = {m} kg/s. The refrigeration rate Q̇_L (kW) is:'),
      QL, [QH, W, c['qL']], 'kW', 2,
      B(f'h₁ = h_g@{Pl} kPa = {N(c["h1"],2)}; h₃ = h₄ = h_f@{Ph} kPa = {N(c["h4"],2)} kJ/kg ⇒ Q̇_L = ṁ(h₁ − h₄) = {m}·{N(c["qL"],2)} = {N(QL,2)} kW. {N(QH,2)} là Q̇_H; {N(W,2)} là công máy nén; {N(c["qL"],2)} quên nhân ṁ.',
        f'h₁ = h_g@{Pl} kPa = {N(c["h1"],2)}; h₃ = h₄ = h_f@{Ph} kPa = {N(c["h4"],2)} kJ/kg ⇒ Q̇_L = ṁ(h₁ − h₄) = {m}·{N(c["qL"],2)} = {N(QL,2)} kW. {N(QH,2)} is Q̇_H; {N(W,2)} is the compressor power; {N(c["qL"],2)} forgets to multiply by ṁ.'), 2, 'vcrc', GEN('công suất lạnh của chu trình nén hơi', 'refrigeration rate of the vapor-compression cycle'))
for (Pl, Ph), m in ((PAIRS[2], 0.06), (PAIRS[3], 0.05)):
    c = Rv(Pl, Ph); QL, W, QH = m * c['qL'], m * c['w'], m * c['qH']
    M(B(f'R-134a, chu trình nén hơi lý tưởng giữa {Pl} kPa và {Ph} kPa, ṁ = {m} kg/s. Công suất điện của máy nén Ẇ (kW) là:', f'R-134a, ideal vapor-compression cycle between {Pl} kPa and {Ph} kPa, ṁ = {m} kg/s. The compressor power Ẇ (kW) is:'),
      W, [QH, QL, c['w']], 'kW', 2,
      B(f'h₂ nội suy theo s₁ = s_g@{Pl} kPa ở {Ph} kPa: h₂ = {N(c["h2"],2)}; h₁ = {N(c["h1"],2)} kJ/kg ⇒ Ẇ = ṁ(h₂ − h₁) = {m}·{N(c["w"],2)} = {N(W,2)} kW. {N(QH,2)} là Q̇_H; {N(QL,2)} là Q̇_L; {N(c["w"],2)} quên ṁ.',
        f'h₂ interpolated at s₁ = s_g@{Pl} kPa and {Ph} kPa: h₂ = {N(c["h2"],2)}; h₁ = {N(c["h1"],2)} kJ/kg ⇒ Ẇ = ṁ(h₂ − h₁) = {m}·{N(c["w"],2)} = {N(W,2)} kW. {N(QH,2)} is Q̇_H; {N(QL,2)} is Q̇_L; {N(c["w"],2)} forgets ṁ.'), 2, 'vcrc', GEN('công suất máy nén', 'compressor power'))
for (Pl, Ph) in (PAIRS[4], PAIRS[5], PAIRS[6]):
    c = Rv(Pl, Ph)
    M(B(f'Chu trình nén hơi lý tưởng R-134a giữa {Pl} kPa (bay hơi) và {Ph} kPa (ngưng tụ). COP của tủ lạnh là:', f'Ideal vapor-compression cycle with R-134a between {Pl} kPa (evaporator) and {Ph} kPa (condenser). The COP of the refrigerator is:'),
      c['cop'], [c['cop_hp'], 1 / c['cop'], c['qH'] / c['qL']], '', 2,
      B(f'COP_R = (h₁ − h₄)/(h₂ − h₁) = {N(c["qL"],2)}/{N(c["w"],2)} = {N(c["cop"],2)}. {N(c["cop_hp"],2)} là COP bơm nhiệt = COP_R + 1; {N(1/c["cop"],2)} và {N(c["qH"]/c["qL"],2)} là các tỉ số đảo hoặc nhầm Q_H với Q_L.',
        f'COP_R = (h₁ − h₄)/(h₂ − h₁) = {N(c["qL"],2)}/{N(c["w"],2)} = {N(c["cop"],2)}. {N(c["cop_hp"],2)} is the heat-pump COP = COP_R + 1; {N(1/c["cop"],2)} and {N(c["qH"]/c["qL"],2)} are inverted ratios or Q_H mixed up with Q_L.'), 1 if Pl == 320 else 2, 'vcrc', GEN('COP của chu trình nén hơi lý tưởng', 'COP of the ideal vapor-compression cycle'))
for (Pl, Ph) in (PAIRS[7], PAIRS[1]):
    c = Rv(Pl, Ph); hfh = sP(Ph, 'hfg')
    M(B(f'Chu trình nén hơi lý tưởng R-134a giữa {Pl} kPa và {Ph} kPa. Chất lượng hơi x₄ của môi chất vào dàn bay hơi (sau tiết lưu) là:', f'Ideal vapor-compression cycle with R-134a between {Pl} kPa and {Ph} kPa. The quality x₄ of the refrigerant entering the evaporator (after throttling) is:'),
      c['x4'], [1 - c['x4'], (c['h4'] - sP(Pl, 'hf')) / hfh, (c['h4'] - sP(Pl, 'hf')) / sP(Pl, 'hg')], '', 3,
      B(f'Tiết lưu đẳng entanpi: h₄ = h₃ = h_f@{Ph} kPa = {N(c["h4"],2)} kJ/kg. Ở {Pl} kPa: h_f = {N(sP(Pl,"hf"),2)}, h_fg = {N(c["hfg_l"],2)} ⇒ x₄ = (h₄ − h_f)/h_fg = {N(c["x4"],3)}. {N(1-c["x4"],3)} là phần lỏng; dùng h_fg của áp suất cao cho {N((c["h4"]-sP(Pl,"hf"))/hfh,3)}; chia cho h_g cho {N((c["h4"]-sP(Pl,"hf"))/sP(Pl,"hg"),3)}.',
        f'Isenthalpic throttling: h₄ = h₃ = h_f@{Ph} kPa = {N(c["h4"],2)} kJ/kg. At {Pl} kPa: h_f = {N(sP(Pl,"hf"),2)}, h_fg = {N(c["hfg_l"],2)} ⇒ x₄ = (h₄ − h_f)/h_fg = {N(c["x4"],3)}. {N(1-c["x4"],3)} is the liquid fraction; using h_fg of the high pressure gives {N((c["h4"]-sP(Pl,"hf"))/hfh,3)}; dividing by h_g gives {N((c["h4"]-sP(Pl,"hf"))/sP(Pl,"hg"),3)}.'), 2, 'vcrc', GEN('chất lượng hơi sau tiết lưu', 'quality after throttling'))
for (Pl, Ph), load in ((PAIRS[0], 12.0), (PAIRS[2], 25.0)):
    c = Rv(Pl, Ph); mdot = load / c['qL']
    M(B(f'Một hệ lạnh R-134a (chu trình nén hơi lý tưởng giữa {Pl} kPa và {Ph} kPa) phải đạt công suất lạnh {int(load)} kW. Lưu lượng khối lượng cần thiết (kg/s) là:', f'An R-134a refrigeration system (ideal vapor-compression cycle between {Pl} kPa and {Ph} kPa) must deliver {int(load)} kW of cooling. The required mass flow rate (kg/s) is:'),
      mdot, [load / c['w'], load / c['qH'], load / c['hfg_l']], 'kg/s', 3,
      B(f'q_L = h₁ − h₄ = {N(c["h1"],2)} − {N(c["h4"],2)} = {N(c["qL"],2)} kJ/kg ⇒ ṁ = Q̇_L/q_L = {int(load)}/{N(c["qL"],2)} = {N(mdot,3)} kg/s. {int(load)}/w = {N(load/c["w"],3)} chia cho công nén; {int(load)}/q_H = {N(load/c["qH"],3)} chia cho nhiệt thải; {int(load)}/h_fg = {N(load/c["hfg_l"],3)} coi toàn bộ h_fg là hiệu ứng lạnh.',
        f'q_L = h₁ − h₄ = {N(c["h1"],2)} − {N(c["h4"],2)} = {N(c["qL"],2)} kJ/kg ⇒ ṁ = Q̇_L/q_L = {int(load)}/{N(c["qL"],2)} = {N(mdot,3)} kg/s. {int(load)}/w = {N(load/c["w"],3)} divides by the compressor work; {int(load)}/q_H = {N(load/c["qH"],3)} divides by the rejected heat; {int(load)}/h_fg = {N(load/c["hfg_l"],3)} treats all of h_fg as the cooling effect.'), 2, 'vcrc', GEN('lưu lượng khối lượng theo tải lạnh', 'mass flow from the cooling load'))
    reg('vcrc_mass_flow', dict(Pl=Pl, Ph=Ph, load=load), 'm', mdot, 5e-3, 'generated')
for QL, cop in ((9.0, 3.6), (15.0, 4.2)):
    QH = QL * (1 + 1 / cop)
    M(B(f'Một máy lạnh có COP = {cop} lấy {QL:.0f} kW từ không gian lạnh. Nhiệt lượng thải ra môi trường Q̇_H (kW) là:', f'A refrigerator with COP = {cop} removes {QL:.0f} kW from the cold space. The heat rejected to the environment Q̇_H (kW) is:'),
      QH, [QL * (1 + cop), QL / cop, QL * (1 - 1 / cop)], 'kW', 2,
      B(f'Ẇ = Q̇_L/COP = {QL:.0f}/{cop} = {N(QL/cop,2)} kW; Q̇_H = Q̇_L + Ẇ = {QL:.0f}·(1 + 1/{cop}) = {N(QH,2)} kW (cân bằng năng lượng quanh chu trình). {N(QL*(1+cop),2)} nhân thêm COP; {N(QL/cop,2)} chỉ là công; {N(QL*(1-1/cop),2)} trừ thay vì cộng.',
        f'Ẇ = Q̇_L/COP = {QL:.0f}/{cop} = {N(QL/cop,2)} kW; Q̇_H = Q̇_L + Ẇ = {QL:.0f}·(1 + 1/{cop}) = {N(QH,2)} kW (energy balance around the cycle). {N(QL*(1+cop),2)} multiplies by COP; {N(QL/cop,2)} is only the work; {N(QL*(1-1/cop),2)} subtracts instead of adding.'), 2, 'rhp', GEN('cân bằng năng lượng của máy lạnh', 'energy balance of a refrigerator'))
    reg('energy_balance', dict(QL=QL, cop=cop), 'QH', QH, 1e-12, 'generated')
Pl, Ph = 140, 800; Wd = 3.0; c = Rv(Pl, Ph); QHhp = Wd * c['cop_hp']
M(B(f'Bơm nhiệt R-134a chạy chu trình nén hơi lý tưởng giữa {Pl} kPa và {Ph} kPa, công suất điện máy nén {Wd:.0f} kW. Nhiệt lượng cấp cho không gian sưởi (kW) là:', f'An R-134a heat pump runs the ideal vapor-compression cycle between {Pl} kPa and {Ph} kPa with a {Wd:.0f} kW compressor. The heat delivered to the heated space (kW) is:'),
  QHhp, [Wd * c['cop'], Wd / c['cop_hp'], Wd * (c['cop_hp'] + 1)], 'kW', 1,
  B(f'COP_HP = (h₂ − h₃)/(h₂ − h₁) = {N(c["qH"],2)}/{N(c["w"],2)} = {N(c["cop_hp"],2)} ⇒ Q̇_H = COP_HP·Ẇ = {N(c["cop_hp"],2)}·{Wd:.0f} = {N(QHhp,1)} kW. {N(Wd*c["cop"],1)} dùng COP_R (đó là Q̇_L); {N(Wd/c["cop_hp"],1)} chia thay vì nhân.',
    f'COP_HP = (h₂ − h₃)/(h₂ − h₁) = {N(c["qH"],2)}/{N(c["w"],2)} = {N(c["cop_hp"],2)} ⇒ Q̇_H = COP_HP·Ẇ = {N(c["cop_hp"],2)}·{Wd:.0f} = {N(QHhp,1)} kW. {N(Wd*c["cop"],1)} uses COP_R (that is Q̇_L); {N(Wd/c["cop_hp"],1)} divides instead of multiplying.'), 2, 'rhp', GEN('công suất sưởi của bơm nhiệt', 'heating capacity of a heat pump'))
reg('hp_heating', dict(Pl=Pl, Ph=Ph, W=Wd), 'QH', QHhp, 5e-3, 'generated')
# a higher evaporating pressure raises the COP at fixed condenser pressure (slide tr.20, Cengel rule of thumb)
ca, cb = Rv(140, 800), Rv(240, 800)
M(B('Với cùng áp suất ngưng 800 kPa, chu trình nén hơi lý tưởng R-134a có áp suất bay hơi 240 kPa so với 140 kPa. COP của chu trình bay hơi 240 kPa là:', 'At the same 800 kPa condenser pressure, an ideal R-134a vapor-compression cycle has an evaporator pressure of 240 kPa instead of 140 kPa. The COP of the 240 kPa cycle is:'),
  cb['cop'], [ca['cop'], ca['cop'] * 0.8, cb['cop'] * 0.62], '', 2,
  B(f'240 kPa: h₁ = {N(cb["h1"],2)}, h₂ = {N(cb["h2"],2)}, h₄ = {N(cb["h4"],2)} kJ/kg ⇒ COP = {N(cb["qL"],2)}/{N(cb["w"],2)} = {N(cb["cop"],2)}; ở 140 kPa COP = {N(ca["cop"],2)}. Nâng áp suất bay hơi (T_sat từ {N(ca["Tl"],1)} lên {N(cb["Tl"],1)} °C) vừa tăng q_L vừa giảm công nén nên COP tăng khoảng {N(100*(cb["cop"]/ca["cop"]-1),0)} %. Quy tắc của Cengel §11-3 (bổ sung): COP tăng 2–4 % cho mỗi °C tăng nhiệt độ bay hơi.',
    f'240 kPa: h₁ = {N(cb["h1"],2)}, h₂ = {N(cb["h2"],2)}, h₄ = {N(cb["h4"],2)} kJ/kg ⇒ COP = {N(cb["qL"],2)}/{N(cb["w"],2)} = {N(cb["cop"],2)}; at 140 kPa the COP = {N(ca["cop"],2)}. Raising the evaporator pressure (T_sat from {N(ca["Tl"],1)} to {N(cb["Tl"],1)} °C) both raises q_L and lowers the compression work, so the COP rises by about {N(100*(cb["cop"]/ca["cop"]-1),0)} %. Cengel §11-3 rule of thumb (added): the COP improves by 2–4 % for each °C the evaporating temperature is raised.'), 2, 'vcrc', GEN('ảnh hưởng áp suất bay hơi tới COP', 'effect of evaporator pressure on the COP'))
# ================================================================ actual cycle: compressor isentropic efficiency, subcooling (Cengel 11-4); table points on the A-13 grid
for (P2, etac, T3) in ((0.8, 0.8, 30), (1.0, 0.75, 28), (0.7, 0.85, 26)):
    r = vcrc_real(0.14, -10, P2, eta_c=etac, T3_C=T3)
    for k in ('h1', 'h2', 'h2s', 'h3', 'qL', 'w', 'cop'): reg('vcrc_real', dict(P1=0.14, T1=-10, P2=P2, eta_c=etac, T3=T3), k, r[k], {'abs': 0.1} if k[0] == 'h' else (0.1 if k in ('qL', 'w') else 0.012), 'generated')
    ideal = (r['h1'] - r['h3']) / (r['h2s'] - r['h1']); sat3 = (r['h1'] - sP(int(P2 * 1000), 'hf')) / (r['h2'] - r['h1'])
    M(B(f'R-134a vào máy nén là hơi quá nhiệt ở 0,14 MPa, −10 °C (h₁ = {N(r["h1"],2)} kJ/kg); nén tới {P2} MPa với hiệu suất đẳng entropi {int(etac*100)} % (h₂ₛ = {N(r["h2s"],2)} kJ/kg); môi chất ra dàn ngưng là lỏng ở {T3} °C (h₃ ≅ h_f@{T3} °C = {N(r["h3"],2)} kJ/kg). COP của tủ lạnh là:', f'R-134a enters the compressor as superheated vapor at 0.14 MPa, −10 °C (h₁ = {N(r["h1"],2)} kJ/kg); it is compressed to {P2} MPa with an isentropic efficiency of {int(etac*100)} % (h₂ₛ = {N(r["h2s"],2)} kJ/kg); the refrigerant leaves the condenser as liquid at {T3} °C (h₃ ≅ h_f@{T3} °C = {N(r["h3"],2)} kJ/kg). The COP of the refrigerator is:'),
      r['cop'], [ideal, sat3, (r['h2'] - r['h3']) / (r['h2'] - r['h1'])], '', 2,
      B(f'h₂ = h₁ + (h₂ₛ − h₁)/η_c = {N(r["h1"],2)} + ({N(r["h2s"],2)} − {N(r["h1"],2)})/{etac} = {N(r["h2"],2)} kJ/kg; q_L = h₁ − h₄ = {N(r["h1"],2)} − {N(r["h3"],2)} = {N(r["qL"],2)}; w = h₂ − h₁ = {N(r["w"],2)} ⇒ COP = {N(r["cop"],2)}. {N(ideal,2)} dùng công đẳng entropi (bỏ η_c); {N(sat3,2)} bỏ quá lạnh (h₃ = h_f ở áp suất ngưng); {N((r["h2"]-r["h3"])/(r["h2"]-r["h1"]),2)} là COP bơm nhiệt.',
        f'h₂ = h₁ + (h₂ₛ − h₁)/η_c = {N(r["h1"],2)} + ({N(r["h2s"],2)} − {N(r["h1"],2)})/{etac} = {N(r["h2"],2)} kJ/kg; q_L = h₁ − h₄ = {N(r["h1"],2)} − {N(r["h3"],2)} = {N(r["qL"],2)}; w = h₂ − h₁ = {N(r["w"],2)} ⇒ COP = {N(r["cop"],2)}. {N(ideal,2)} uses the isentropic work (drops η_c); {N(sat3,2)} ignores the subcooling (h₃ = h_f at the condenser pressure); {N((r["h2"]-r["h3"])/(r["h2"]-r["h1"]),2)} is the heat-pump COP.'), 3, 'real', GEN('chu trình thực có hiệu suất máy nén và quá lạnh', 'actual cycle with compressor efficiency and subcooling'))
# ================================================================ units: tons of refrigeration, psi, rpm
M(B('Một máy điều hoà 5 tấn lạnh (1 tấn lạnh = 211 kJ/phút theo Cengel §11-1) có COP = 3,5. Công suất điện (kW) cần cấp là:', 'An air conditioner rated 5 tons of refrigeration (1 ton = 211 kJ/min, Cengel §11-1) has COP = 3.5. The electric power required (kW) is:'),
  5 * TON / 3.5, [5 * TON, 5 * 211 / 3.5, 5 * TON * 3.5], 'kW', 2,
  B(f'Q̇_L = 5·211 kJ/phút = 1 055 kJ/phút = {N(5*TON,2)} kW; Ẇ = Q̇_L/COP = {N(5*TON,2)}/3,5 = {N(5*TON/3.5,2)} kW. {N(5*TON,2)} là tải lạnh chứ không phải công suất điện; {N(5*211/3.5,1)} quên đổi phút sang giây; nhân COP thay vì chia cho {N(5*TON*3.5,1)}.',
    f'Q̇_L = 5·211 kJ/min = 1,055 kJ/min = {N(5*TON,2)} kW; Ẇ = Q̇_L/COP = {N(5*TON,2)}/3.5 = {N(5*TON/3.5,2)} kW. {N(5*TON,2)} is the cooling load, not the electric power; {N(5*211/3.5,1)} forgets to convert minutes to seconds; multiplying by COP instead of dividing gives {N(5*TON*3.5,1)}.'), 2, 'units', GEN('tấn lạnh và công suất điện', 'tons of refrigeration and electric power'), 'Cengel §11-1 (211 kJ/min) + script')
reg('identity', dict(tons=5, cop=3.5), 'W', 5 * TON / 3.5, 1e-9, 'generated')
M(B('Slide tr.32 nói khí xả vào bộ trao đổi nhiệt sơ cấp "ở áp suất trung bình 30 đến 40 psi" nhưng không nói đó là áp suất dư (gauge) hay tuyệt đối. Nếu là áp suất dư và áp suất khí quyển 101,3 kPa, giới hạn trên 40 psi tương ứng áp suất tuyệt đối (kPa) khoảng:', 'Slide p.32 says the bleed air enters the primary heat exchanger "at an average pressure of 30 to 40 p.s.i." without saying gauge or absolute. If it is gauge and atmospheric pressure is 101.3 kPa, the upper limit of 40 psi corresponds to an absolute pressure (kPa) of about:'),
  40 * PSI + 101.325, [40 * PSI, 40 * PSI * 2, 40 / PSI + 101.325], 'kPa', 0,
  B(f'1 psi = {PSI} kPa ⇒ 40 psi = {N(40*PSI,0)} kPa (áp suất dư); áp suất tuyệt đối = dư + khí quyển = {N(40*PSI,0)} + 101,3 = {N(40*PSI+101.325,0)} kPa. Nếu 40 psi là áp suất tuyệt đối thì chỉ {N(40*PSI,0)} kPa: slide không nói rõ, ghi vào mục lỗi nguồn. {N(40/PSI+101.325,0)} chia thay vì nhân.',
    f'1 psi = {PSI} kPa ⇒ 40 psi = {N(40*PSI,0)} kPa (gauge); absolute = gauge + atmospheric = {N(40*PSI,0)} + 101.3 = {N(40*PSI+101.325,0)} kPa. If 40 psi were already absolute it would be only {N(40*PSI,0)} kPa: the slide does not say, recorded in the source-error list. {N(40/PSI+101.325,0)} divides instead of multiplying.'), 2, 'units', GEN('đổi psi sang kPa (áp suất dư/tuyệt đối)', 'psi to kPa (gauge/absolute)'), 'slide tr.32 + hệ số đổi (script)')
reg('identity', dict(psi=40), 'kPa_abs', 40 * PSI + 101.325, 1e-6, 'generated')
M(B('Slide tr.35 cho trục ACM quay 40.000 đến 50.000 vòng/phút. Tốc độ góc ở 50.000 vòng/phút (rad/s) là:', 'Slide p.35 gives the ACM shaft speed as 40.000 to 50.000 rpm. The angular speed at 50,000 rpm (rad/s) is:'),
  50000 * 2 * math.pi / 60, [50000 / 60, 50000 * 2 * math.pi, 50000 * math.pi / 60], 'rad/s', 0,
  B(f'ω = 2π·n/60 = 2π·50 000/60 = {N(50000*2*math.pi/60,0)} rad/s. {N(50000/60,0)} là số vòng/giây (chưa nhân 2π); {N(50000*2*math.pi,0)} quên chia 60; {N(50000*math.pi/60,0)} chỉ nhân π.',
    f'ω = 2π·n/60 = 2π·50,000/60 = {N(50000*2*math.pi/60,0)} rad/s. {N(50000/60,0)} is revolutions per second (2π not applied); {N(50000*2*math.pi,0)} forgets to divide by 60; {N(50000*math.pi/60,0)} multiplies by π only.'), 1, 'units', GEN('đổi vòng/phút sang rad/s', 'rpm to rad/s'), 'slide tr.35 + công thức (script)')
reg('identity', dict(rpm=50000), 'omega', 50000 * 2 * math.pi / 60, 1e-12, 'generated')
# ================================================================ cooling pack arithmetic on slide numbers (illustrative: sums of slide numbers)
M(B('Theo slide tr.32, khí xả vào pack ở khoảng 150 °C và nhiệt độ giảm khoảng 100 °C khi qua bộ trao đổi nhiệt sơ cấp. Nhiệt độ khí sau bộ sơ cấp (suy ra, minh hoạ) xấp xỉ:', 'According to slide p.32 the bleed air enters the pack at about 150 °C and drops by about 100 °C in the primary heat exchanger. The air temperature after the primary exchanger (derived, illustrative) is about:'),
  50.0, [250.0, 100.0, 15.0], '°C', 0,
  B('150 − 100 = 50 °C: giá trị suy ra bằng phép trừ hai số của slide, slide không in nhiệt độ này. 250 °C là cộng thay vì trừ; 100 °C là chính độ giảm; 15 °C là nhầm với nhiệt độ môi trường.', '150 − 100 = 50 °C: derived by subtracting two slide numbers; the slide does not print this temperature. 250 °C adds instead of subtracting; 100 °C is the drop itself; 15 °C is confused with the ambient temperature.'), 1, 'pack', B('Slide Ch.3 tr.32: nhiệt độ khí sau bộ trao đổi nhiệt sơ cấp (suy ra)', 'Slide Ch.3 p.32: air temperature after the primary heat exchanger (derived)'), 'số học trên số của slide (minh hoạ)')
lo = 150 - 100 + 30 - 70; hi = 150 - 100 + 40 - 60
M(B('Chuỗi số của slide tr.32–33: vào 150 °C, bộ sơ cấp giảm ~100 °C, máy nén ACM tăng 30–40 °C, bộ thứ cấp giảm 60–70 °C. Nhiệt độ thấp nhất có thể sau bộ thứ cấp (minh hoạ, cộng các cận) là:', 'The chain of numbers on slides p.32–33: entry 150 °C, primary exchanger −~100 °C, ACM compressor +30–40 °C, secondary exchanger −60–70 °C. The lowest possible temperature after the secondary exchanger (illustrative, combining the bounds) is:'),
  float(lo), [float(hi), 150 - 100 + 30 - 60.0, 150 - 100 - 70.0], '°C', 0,
  B(f'Cận thấp: 150 − 100 + 30 − 70 = {lo} °C (tăng ít nhất ở máy nén, giảm nhiều nhất ở bộ thứ cấp). Cận cao: 150 − 100 + 40 − 60 = {hi} °C. {N(150-100+30-60.0,0)} và {N(150-100-70.0,0)} bỏ một bước hoặc trộn lẫn các cận. Khoảng 10–30 °C khớp với "20 to 10 °C" ở tr.34 (đọc là 10–20 °C): slide không mâu thuẫn.',
    f'Lower bound: 150 − 100 + 30 − 70 = {lo} °C (smallest rise in the compressor, largest drop in the secondary exchanger). Upper bound: 150 − 100 + 40 − 60 = {hi} °C. {N(150-100+30-60.0,0)} and {N(150-100-70.0,0)} skip a step or mix the bounds. The range 10–30 °C is consistent with "20 to 10 °C" on p.34 (read as 10–20 °C): the slides do not contradict one another.'), 3, 'pack', B('Slide Ch.3 tr.32–34: chuỗi nhiệt độ qua pack (suy ra)', 'Slide Ch.3 p.32–34: temperature chain through the pack (derived)'), 'số học trên số của slide (minh hoạ)')
reg('identity', dict(chain=1), 'lo', float(lo), 1e-12, 'generated'); reg('identity', dict(chain=1), 'hi', float(hi), 1e-12, 'generated')
# ================================================================ gas refrigeration (Cengel §11-8): COP, T4, regeneration, real efficiencies
for rp in (2.0, 4.0):
    g = gas_simple(c2k(20), c2k(40), rp); cg = cop_gas_closed(rp)
    reg('gas_simple', dict(T1=c2k(20), T3=c2k(40), rp=rp), 'cop', g['cop'], 0.03, 'generated'); reg('gas_simple', dict(T1=c2k(20), T3=c2k(40), rp=rp), 'T4', g['T4'], {'abs': 1.5}, 'generated')
    M(B(f'Chu trình khí lạnh lý tưởng (Brayton ngược) dùng không khí (k = 1,4, c_p hằng) có tỉ số áp r_p = {rp:.0f}. COP của chu trình đơn giản (không hồi nhiệt) là:', f'An ideal gas refrigeration cycle (reversed Brayton) with air (k = 1.4, constant c_p) has pressure ratio r_p = {rp:.0f}. The COP of the simple cycle (no regeneration) is:'),
      cg, [rp ** (0.4 / 1.4) - 1, 1 / (1 - rp ** (-0.4 / 1.4)), 1 / (rp - 1)], '', 2,
      B(f'COP = q_L/w_net = 1/(r_p^((k−1)/k) − 1) = 1/({rp:.0f}^0,2857 − 1) = 1/{N(rp**(0.4/1.4)-1,4)} = {N(cg,2)} (Cengel §11-8, bổ sung từ sách). {N(rp**(0.4/1.4)-1,3)} chưa nghịch đảo; 1/(1 − r_p^(−0,2857)) = {N(1/(1-rp**(-0.4/1.4)),2)} là COP bơm nhiệt; 1/(r_p − 1) = {N(1/(rp-1),2)} bỏ số mũ.',
        f'COP = q_L/w_net = 1/(r_p^((k−1)/k) − 1) = 1/({rp:.0f}^0.2857 − 1) = 1/{N(rp**(0.4/1.4)-1,4)} = {N(cg,2)} (Cengel §11-8, added from the book). {N(rp**(0.4/1.4)-1,3)} is not yet inverted; 1/(1 − r_p^(−0.2857)) = {N(1/(1-rp**(-0.4/1.4)),2)} is the heat-pump COP; 1/(r_p − 1) = {N(1/(rp-1),2)} drops the exponent.'), 1, 'gas', GEN('COP chu trình khí lạnh', 'gas-cycle COP'), 'công thức đóng + sympy (verify_m03)')
for (T3c, rp) in ((40, 3.0), (50, 2.5)):
    g = gas_simple(c2k(10), c2k(T3c), rp); x = g['x']
    reg('gas_simple', dict(T1=c2k(10), T3=c2k(T3c), rp=rp), 'T4', g['T4'], {'abs': 1.5}, 'generated')
    M(B(f'Chu trình khí lạnh lý tưởng dùng không khí (k = 1,4): không khí vào tuabin ở {T3c} °C, tỉ số áp {rp}. Nhiệt độ không khí ra khỏi tuabin (°C) là:', f'An ideal gas refrigeration cycle with air (k = 1.4): air enters the turbine at {T3c} °C, pressure ratio {rp}. The air temperature leaving the turbine (°C) is:'),
      g['T4'] - 273.15, [T3c / x, (c2k(T3c)) / rp - 273.15, c2k(T3c) * x - 273.15], '°C', 0,
      B(f'T₄ = T₃/r_p^((k−1)/k) = {N(c2k(T3c),2)}/{rp}^0,2857 = {N(c2k(T3c),2)}/{N(x,4)} = {N(g["T4"],1)} K = {N(g["T4"]-273.15,1)} °C. Dùng °C trong công thức cho {N(T3c/x,0)}; chia T cho r_p cho {N(c2k(T3c)/rp-273.15,0)}; nhân (nén thay vì giãn) cho {N(c2k(T3c)*x-273.15,0)} °C.',
        f'T₄ = T₃/r_p^((k−1)/k) = {N(c2k(T3c),2)}/{rp}^0.2857 = {N(c2k(T3c),2)}/{N(x,4)} = {N(g["T4"],1)} K = {N(g["T4"]-273.15,1)} °C. Using °C in the formula gives {N(T3c/x,0)}; dividing T by r_p gives {N(c2k(T3c)/rp-273.15,0)}; multiplying (compression instead of expansion) gives {N(c2k(T3c)*x-273.15,0)} °C.'), 2, 'gas', GEN('nhiệt độ ra tuabin của chu trình khí lạnh', 'turbine outlet temperature of the gas cycle'))
gr = gas_regen(c2k(0), c2k(35), c2k(-10), 3.0); mgr = 15.0 / gr['qL']
for k in ('T5', 'T6', 'qL', 'w', 'cop'): reg('gas_regen', dict(T1=c2k(0), T3=c2k(35), T4=c2k(-10), rp=3.0), k, gr[k], {'abs': 1.5} if k[0] == 'T' else 0.03, 'generated')
M(B('Chu trình khí lạnh có hồi nhiệt dùng không khí (k = 1,4, c_p = 1,005): máy nén hút ở 0 °C, r_p = 3; sau tản nhiệt 35 °C, sau hồi nhiệt −10 °C (vào tuabin). Máy nén và tuabin đẳng entropi. Lưu lượng khối lượng cần cho tải lạnh 15 kW (kg/s) là:', 'A regenerative gas refrigeration cycle with air (k = 1.4, c_p = 1.005): compressor inlet 0 °C, r_p = 3; after the heat sink 35 °C, after the regenerator −10 °C (turbine inlet). Compressor and turbine are isentropic. The mass flow rate for a 15 kW refrigeration load (kg/s) is:'),
  mgr, [15.0 / (1.005 * (c2k(0) - gr['T5'])), 15.0 / gr['w'], 15.0 / (1.005 * (c2k(-10) - gr['T5']))], 'kg/s', 3,
  B(f'T₅ = T₄/3^0,2857 = {N(c2k(-10),2)}/{N(3**(0.4/1.4),4)} = {N(gr["T5"],1)} K. Hồi nhiệt: T₆ = T₁ − (T₃ − T₄) = {N(c2k(0),2)} − 45 = {N(gr["T6"],2)} K. q_L = c_p(T₆ − T₅) = 1,005·({N(gr["T6"],2)} − {N(gr["T5"],1)}) = {N(gr["qL"],2)} kJ/kg ⇒ ṁ = 15/{N(gr["qL"],2)} = {N(mgr,3)} kg/s. Dùng T₁ − T₅ (bỏ hồi nhiệt) cho {N(15.0/(1.005*(c2k(0)-gr["T5"])),3)}; chia cho công thực {N(gr["w"],1)} kJ/kg cho {N(15.0/gr["w"],3)}; dùng T₄ − T₅ thay cho T₆ − T₅ cho {N(15.0/(1.005*(c2k(-10)-gr["T5"])),3)}.',
    f'T₅ = T₄/3^0.2857 = {N(c2k(-10),2)}/{N(3**(0.4/1.4),4)} = {N(gr["T5"],1)} K. Regenerator: T₆ = T₁ − (T₃ − T₄) = {N(c2k(0),2)} − 45 = {N(gr["T6"],2)} K. q_L = c_p(T₆ − T₅) = 1.005·({N(gr["T6"],2)} − {N(gr["T5"],1)}) = {N(gr["qL"],2)} kJ/kg ⇒ ṁ = 15/{N(gr["qL"],2)} = {N(mgr,3)} kg/s. Using T₁ − T₅ (ignoring the regenerator) gives {N(15.0/(1.005*(c2k(0)-gr["T5"])),3)}; dividing by the net work {N(gr["w"],1)} kJ/kg gives {N(15.0/gr["w"],3)}; using T₄ − T₅ instead of T₆ − T₅ gives {N(15.0/(1.005*(c2k(-10)-gr["T5"])),3)}.'), 3, 'gas', GEN('chu trình khí lạnh có hồi nhiệt', 'regenerative gas refrigeration cycle'))
reg('gas_regen_mass', dict(T1=c2k(0), T3=c2k(35), T4=c2k(-10), rp=3.0, load=15.0), 'm', mgr, 0.03, 'generated')
gm = gas_simple(c2k(10), c2k(45), 3.0, etac=0.8, etat=0.85); gi = gas_simple(c2k(10), c2k(45), 3.0)
for k in ('T2', 'T4', 'qL', 'w', 'cop'): reg('gas_simple_eff', dict(T1=c2k(10), T3=c2k(45), rp=3.0, etac=0.8, etat=0.85), k, gm[k], {'abs': 2.0} if k[0] == 'T' else (0.04 if k != 'cop' else 0.05), 'generated')
M(B('Chu trình khí lạnh đơn giản dùng không khí (k = 1,4): máy nén hút ở 10 °C, vào tuabin ở 45 °C, r_p = 3, hiệu suất đẳng entropi của máy nén 80 % và của tuabin 85 %. COP của chu trình là:', 'A simple gas refrigeration cycle with air (k = 1.4): compressor inlet 10 °C, turbine inlet 45 °C, r_p = 3, isentropic efficiency 80 % for the compressor and 85 % for the turbine. The COP of the cycle is:'),
  gm['cop'], [gi['cop'], gm['qL'] / gm['wc'], gi['cop'] * 0.8 * 0.85], '', 2,
  B(f'x = 3^0,2857 = {N(gm["x"],4)}. Nén thực: T₂ = T₁ + T₁(x − 1)/η_c = {N(gm["T2"],1)} K; giãn thực: T₄ = T₃ − η_t(T₃ − T₃/x) = {N(gm["T4"],1)} K. q_L = c_p(T₁ − T₄) = {N(gm["qL"],2)}; w_c = {N(gm["wc"],2)}; w_t = {N(gm["wt"],2)}; w_net = {N(gm["w"],2)} kJ/kg ⇒ COP = {N(gm["cop"],2)}. Chu trình lý tưởng cho {N(gi["cop"],2)}; bỏ công tuabin cho {N(gm["qL"]/gm["wc"],2)}; nhân hiệu suất vào COP lý tưởng cho {N(gi["cop"]*0.8*0.85,2)} (sai: hiệu suất tác động khác nhau lên tử và mẫu).',
    f'x = 3^0.2857 = {N(gm["x"],4)}. Real compression: T₂ = T₁ + T₁(x − 1)/η_c = {N(gm["T2"],1)} K; real expansion: T₄ = T₃ − η_t(T₃ − T₃/x) = {N(gm["T4"],1)} K. q_L = c_p(T₁ − T₄) = {N(gm["qL"],2)}; w_c = {N(gm["wc"],2)}; w_t = {N(gm["wt"],2)}; w_net = {N(gm["w"],2)} kJ/kg ⇒ COP = {N(gm["cop"],2)}. The ideal cycle gives {N(gi["cop"],2)}; ignoring the turbine work gives {N(gm["qL"]/gm["wc"],2)}; multiplying the efficiencies into the ideal COP gives {N(gi["cop"]*0.8*0.85,2)} (wrong: efficiencies act differently on numerator and denominator).'), 3, 'gas', GEN('chu trình khí lạnh có hiệu suất thiết bị', 'gas cycle with component efficiencies'))
# ================================================================ dew point (slide tr.35 "due point", Cengel §14-3; water Table A-4/A-5)
for (Tc, phi) in ((25, 0.6), (30, 0.5)):
    Pg = props.sat_T('water', Tc, 'Psat_kPa')['value']; Pv = phi * Pg; Tdp = props.sat_P('water', Pv, 'Tsat_C')['value']; T85 = props.sat_P('water', phi * 100, 'Tsat_C')['value']
    reg('dew_point', dict(T=Tc, phi=phi), 'Tdp', Tdp, {'abs': 0.15}, 'generated')
    M(B(f'Không khí ở {Tc} °C, độ ẩm tương đối {int(phi*100)} %. Điểm sương (dew point) xấp xỉ (bảng A-4/A-5), °C:', f'Air at {Tc} °C and {int(phi*100)} % relative humidity. The dew point is about (Tables A-4/A-5), in °C:'),
      Tdp, [phi * Tc, float(Tc), T85], '°C', 1,
      B(f'P_g@{Tc} °C = {N(Pg,3)} kPa (A-4) ⇒ P_v = φ·P_g = {phi}·{N(Pg,3)} = {N(Pv,3)} kPa. Điểm sương = T_sat@P_v = {N(Tdp,1)} °C (A-5, nội suy tuyến tính). Nhân φ với nhiệt độ cho {N(phi*Tc,1)} (sai: φ là tỉ số áp suất); điểm sương không bằng nhiệt độ không khí khi φ < 1; coi P_v = φ·100 kPa cho {N(T85,1)} °C. Slide tr.35 viết "due point": đúng là dew point.',
        f'P_g@{Tc} °C = {N(Pg,3)} kPa (A-4) ⇒ P_v = φ·P_g = {phi}·{N(Pg,3)} = {N(Pv,3)} kPa. Dew point = T_sat@P_v = {N(Tdp,1)} °C (A-5, linear interpolation). Multiplying φ by the temperature gives {N(phi*Tc,1)} (wrong: φ is a pressure ratio); the dew point is not the air temperature when φ < 1; taking P_v = φ·100 kPa gives {N(T85,1)} °C. Slide p.35 writes "due point": dew point is meant.'), 2, 'humid', B('Slide Ch.3 tr.35 (điểm sương) + Cengel §14-3 (bổ sung từ sách)', 'Slide Ch.3 p.35 (dew point) + Cengel §14-3 (added from the book)'), 'bảng A-4/A-5 ↔ IAPWS-IF97 (verify_m03)')
# ================================================================ true/false
c = Rv(140, 800); cc = carnot_R(c['Tl'] + 273.15, c['Th'] + 273.15)
Tf(B('Chu trình nén hơi lý tưởng R-134a giữa 0,14 và 0,8 MPa (Tutorials I) có COP lớn hơn COP của chu trình Carnot đảo ngược chạy giữa hai nhiệt độ bão hòa tương ứng.', 'The ideal R-134a vapor-compression cycle between 0.14 and 0.8 MPa (Tutorials I) has a higher COP than the reversed Carnot cycle between the corresponding saturation temperatures.'), False,
   B(f'Carnot đảo ngược là chu trình lạnh có COP lớn nhất giữa hai mức nhiệt độ (slide tr.13–14). Giữa T_L = {N(c["Tl"],2)} °C và T_H = {N(c["Th"],2)} °C: COP_Carnot = {N(cc,2)}; chu trình nén hơi lý tưởng cho {N(c["cop"],2)}, tức {N(100*c["cop"]/cc,0)} % của Carnot (do tiết lưu bất thuận nghịch và nén hơi quá nhiệt).', f'The reversed Carnot cycle has the largest COP between two temperature levels (slides p.13–14). Between T_L = {N(c["Tl"],2)} °C and T_H = {N(c["Th"],2)} °C: COP_Carnot = {N(cc,2)}; the vapor-compression cycle gives {N(c["cop"],2)}, i.e. {N(100*c["cop"]/cc,0)} % of Carnot (irreversible throttling and superheated-vapor compression).'), 2, 'carnot', GEN('so sánh với Carnot', 'comparison with Carnot'))
reg('carnot', dict(TL=c['Tl'] + 273.15, TH=c['Th'] + 273.15), 'cop', cc, 4e-3, 'generated')
Tf(B('Hệ số hiệu quả của bơm nhiệt chạy theo chu trình nén hơi luôn lớn hơn 1, ngay cả khi COP của tủ lạnh cùng chu trình rất nhỏ.', 'The COP of a heat pump on the vapor-compression cycle is always above 1, even when the COP of the refrigerator on the same cycle is very small.'), True,
   B('COP_HP = COP_R + 1 (Cengel Hệ thức 11–3) và COP_R > 0, nên COP_HP > 1: bơm nhiệt, xấu nhất, cũng như lò điện trở. (Trong thực tế một phần Q_H mất qua ống nên COP_HP có thể tụt xuống dưới 1 khi nhiệt độ ngoài trời quá thấp: Cengel §11-1.)', 'COP_HP = COP_R + 1 (Cengel Eq. 11–3) and COP_R > 0, so COP_HP > 1: at worst a heat pump equals a resistance heater. (In practice part of Q_H is lost through piping, so COP_HP can drop below 1 when the outdoor temperature is too low: Cengel §11-1.)'), 2, 'rhp', GEN('COP_HP > 1', 'COP_HP > 1'), 'Cengel §11-1 + sympy')
Tf(B('Trong chu trình khí lạnh đơn giản, nếu giảm nhiệt độ vào tuabin T₃ (làm mát tốt hơn) và giữ nguyên r_p thì nhiệt độ ra tuabin T₄ giảm.', 'In the simple gas refrigeration cycle, lowering the turbine inlet temperature T₃ (better cooling) at fixed r_p lowers the turbine outlet temperature T₄.'), True,
   B('T₄ = T₃/r_p^((k−1)/k): T₄ tỉ lệ với T₃ khi r_p cố định. Vì vậy hồi nhiệt (hạ T₃ xuống dưới nhiệt độ môi trường) cho nhiệt độ rất thấp (Cengel §11-8, bổ sung).', 'T₄ = T₃/r_p^((k−1)/k): T₄ is proportional to T₃ at fixed r_p. That is why regeneration (lowering T₃ below ambient) reaches very low temperatures (Cengel §11-8, added).'), 2, 'gas', GEN('T₄ phụ thuộc T₃', 'T₄ depends on T₃'), 'công thức đóng')
Tf(B('Trong chu trình khí lạnh đơn giản với c_p và k hằng, COP phụ thuộc vào tỉ số áp r_p nhưng không phụ thuộc vào nhiệt độ T₁ và T₃.', 'In the simple gas refrigeration cycle with constant c_p and k, the COP depends on the pressure ratio r_p but not on the temperatures T₁ and T₃.'), True,
   B('COP = q_L/w_net = 1/(r_p^((k−1)/k) − 1): các c_p(T₁ − T₄) và c_p[(T₂ − T₁) − (T₃ − T₄)] đều có cùng thừa số nhiệt độ nên triệt tiêu; chỉ còn r_p. (Điều này đúng cho chu trình lý tưởng không hồi nhiệt; nhiệt độ vẫn quyết định công suất lạnh tuyệt đối.)', 'COP = q_L/w_net = 1/(r_p^((k−1)/k) − 1): c_p(T₁ − T₄) and c_p[(T₂ − T₁) − (T₃ − T₄)] share the same temperature factor and cancel; only r_p remains. (True for the ideal cycle without regeneration; the temperatures still set the absolute refrigeration rate.)'), 3, 'gas', GEN('COP khí lạnh chỉ phụ thuộc r_p', 'gas-cycle COP depends only on r_p'), 'sympy (verify_m03)')

# ================================================================ more multi-step (level 3) questions
for (Pl, Ph), load in ((PAIRS[2], 20.0), (PAIRS[4], 30.0)):
    c = Rv(Pl, Ph); mdot = load / c['qL']; QH = mdot * c['qH']
    M(B(f'Hệ lạnh R-134a, chu trình nén hơi lý tưởng giữa {Pl} kPa và {Ph} kPa, có công suất lạnh {int(load)} kW. Nhiệt lượng dàn ngưng thải ra môi trường Q̇_H (kW) là:', f'An R-134a refrigeration system on the ideal vapor-compression cycle between {Pl} kPa and {Ph} kPa has a refrigeration rate of {int(load)} kW. The heat rejected by the condenser to the environment Q̇_H (kW) is:'),
      QH, [load, load * c['cop'], mdot * c['w']], 'kW', 1,
      B(f'ṁ = Q̇_L/(h₁ − h₄) = {int(load)}/{N(c["qL"],2)} = {N(mdot,4)} kg/s; Q̇_H = ṁ(h₂ − h₃) = {N(mdot,4)}·{N(c["qH"],2)} = {N(QH,1)} kW (= Q̇_L + Ẇ = {int(load)} + {N(mdot*c["w"],1)}). {int(load)} là Q̇_L; {N(load*c["cop"],1)} nhân COP; {N(mdot*c["w"],1)} chỉ là công máy nén.',
        f'ṁ = Q̇_L/(h₁ − h₄) = {int(load)}/{N(c["qL"],2)} = {N(mdot,4)} kg/s; Q̇_H = ṁ(h₂ − h₃) = {N(mdot,4)}·{N(c["qH"],2)} = {N(QH,1)} kW (= Q̇_L + Ẇ = {int(load)} + {N(mdot*c["w"],1)}). {int(load)} is Q̇_L; {N(load*c["cop"],1)} multiplies by the COP; {N(mdot*c["w"],1)} is only the compressor power.'), 3, 'vcrc', GEN('nhiệt thải của dàn ngưng theo tải lạnh', 'condenser heat rejection from the cooling load'))
    reg('vcrc_QH_from_load', dict(Pl=Pl, Ph=Ph, load=load), 'QH', QH, 6e-3, 'generated')
for (Pl, Ph) in ((140, 800), (200, 1000)):
    t = O.turbine_case(Pl, Ph); c = t['c']
    reg('turbine_instead_of_valve', dict(Pl=Pl, Ph=Ph), 'h4s', t['h4s'], {'abs': 0.05}, 'generated'); reg('turbine_instead_of_valve', dict(Pl=Pl, Ph=Ph), 'dcop', t['dcop'], {'abs': 0.003}, 'generated')
    M(B(f'Trong chu trình nén hơi lý tưởng R-134a giữa {Pl} kPa và {Ph} kPa, thay van tiết lưu bằng một tuabin đẳng entropi (giãn lỏng bão hòa từ {Ph} kPa về {Pl} kPa, sinh công trừ vào công máy nén). COP mới lớn hơn COP cũ khoảng:', f'In the ideal R-134a vapor-compression cycle between {Pl} kPa and {Ph} kPa, the throttling valve is replaced by an isentropic turbine (expanding saturated liquid from {Ph} kPa to {Pl} kPa and delivering work that offsets the compressor). The new COP exceeds the old one by about:'),
      100 * t['dcop'], [100 * t['dq'], 100 * (c['h3'] - t['h4s']) / c['w'], 100 * (c['h4'] - t['h4s']) / c['h4']], '%', 1,
      B(f's₃ = s_f@{Ph} kPa; x₄ₛ = {N(t["x4s"],3)}; h₄ₛ = {N(t["h4s"],2)} kJ/kg (so với h₄ = {N(c["h4"],2)}). q_L mới = h₁ − h₄ₛ = {N(t["qL"],2)}; w mới = (h₂ − h₁) − (h₃ − h₄ₛ) = {N(t["w"],2)} ⇒ COP mới = {N(t["cop"],2)} so với {N(c["cop"],2)}: tăng {N(100*t["dcop"],1)} %. {N(100*t["dq"],1)} % chỉ là mức tăng q_L; {N(100*(c["h3"]-t["h4s"])/c["w"],1)} % là công tuabin trên công nén.',
        f's₃ = s_f@{Ph} kPa; x₄ₛ = {N(t["x4s"],3)}; h₄ₛ = {N(t["h4s"],2)} kJ/kg (versus h₄ = {N(c["h4"],2)}). New q_L = h₁ − h₄ₛ = {N(t["qL"],2)}; new w = (h₂ − h₁) − (h₃ − h₄ₛ) = {N(t["w"],2)} ⇒ new COP = {N(t["cop"],2)} versus {N(c["cop"],2)}: up {N(100*t["dcop"],1)} %. {N(100*t["dq"],1)} % is only the increase of q_L; {N(100*(c["h3"]-t["h4s"])/c["w"],1)} % is turbine work over compressor work.'), 3, 'vcrc', GEN('tuabin thay van tiết lưu', 'turbine instead of the throttling valve'))
for (Pl, Ph) in (PAIRS[1], PAIRS[5]):
    c = Rv(Pl, Ph); TLk, THk = c['Tl'] + 273.15, c['Th'] + 273.15; cc = carnot_R(TLk, THk); eta2 = c['cop'] / cc
    reg('carnot', dict(TL=TLk, TH=THk), 'cop', cc, 4e-3, 'generated')
    M(B(f'Chu trình nén hơi lý tưởng R-134a giữa {Pl} kPa và {Ph} kPa (T_sat tương ứng {N(c["Tl"],2)} °C và {N(c["Th"],2)} °C). Tỉ số COP của chu trình trên COP của chu trình Carnot đảo ngược giữa hai nhiệt độ bão hòa đó xấp xỉ:', f'Ideal R-134a vapor-compression cycle between {Pl} kPa and {Ph} kPa (T_sat = {N(c["Tl"],2)} °C and {N(c["Th"],2)} °C). The ratio of its COP to that of a reversed Carnot cycle between those saturation temperatures is about:'),
      eta2, [1 / eta2, c['cop'] / carnot_HP(TLk, THk), c['cop'] / (THk / TLk - 1)], '', 2,
      B(f'COP_cycle = {N(c["cop"],2)}; COP_Carnot = T_L/(T_H − T_L) = {N(TLk,2)}/{N(THk-TLk,2)} = {N(cc,2)} ⇒ tỉ số = {N(eta2,2)} (< 1 vì tiết lưu bất thuận nghịch và hơi nén quá nhiệt). {N(1/eta2,2)} là tỉ số đảo; {N(c["cop"]/carnot_HP(TLk,THk),2)} chia cho COP bơm nhiệt Carnot; {N(c["cop"]/(THk/TLk-1),2)} chia cho T_H/T_L − 1 chưa nghịch đảo.',
        f'COP_cycle = {N(c["cop"],2)}; COP_Carnot = T_L/(T_H − T_L) = {N(TLk,2)}/{N(THk-TLk,2)} = {N(cc,2)} ⇒ ratio = {N(eta2,2)} (< 1 because of irreversible throttling and superheated-vapor compression). {N(1/eta2,2)} is the inverted ratio; {N(c["cop"]/carnot_HP(TLk,THk),2)} divides by the Carnot heat-pump COP; {N(c["cop"]/(THk/TLk-1),2)} divides by T_H/T_L − 1 not yet inverted.'), 3, 'carnot', GEN('tỉ số COP thực/Carnot', 'COP ratio actual/Carnot'))
# illustrative ACM stage: what pressure ratio would a 35 K temperature rise mean if the compression were isentropic (slides give the temperature rise only, never the pressure ratio)
Tin = c2k(50.0); dT = 35.0; PRc = ((Tin + dT) / Tin) ** (1.4 / 0.4)
M(B('Slide tr.33 cho độ tăng nhiệt độ qua máy nén ACM là khoảng 30–40 °C và (suy ra từ tr.32) khí vào máy nén khoảng 50 °C; slide KHÔNG cho tỉ số nén. Minh hoạ: giả sử nén đẳng entropi, k = 1,4, độ tăng 35 K. Tỉ số áp của máy nén sẽ xấp xỉ:', 'Slide p.33 gives the temperature rise through the ACM compressor as about 30–40 °C and (derived from p.32) the air entering it as about 50 °C; the slide gives NO pressure ratio. Illustration: assume isentropic compression, k = 1.4, a 35 K rise. The compressor pressure ratio would be about:'),
  PRc, [(Tin + dT) / Tin, ((Tin + dT) / Tin) ** (0.4 / 1.4), dT / 50], '', 2,
  B(f'T₂/T₁ = (323,15 + 35)/323,15 = {N((Tin+dT)/Tin,4)}; đẳng entropi: r_p = (T₂/T₁)^(k/(k−1)) = {N((Tin+dT)/Tin,4)}^3,5 = {N(PRc,2)}. Đây chỉ là minh hoạ (nén thực có tổn thất cần tỉ số áp cao hơn cho cùng độ tăng nhiệt độ… hoặc ngược lại, tuỳ cách định nghĩa; slide không cho số). {N((Tin+dT)/Tin,3)} là tỉ số nhiệt độ; {N(((Tin+dT)/Tin)**(0.4/1.4),3)} dùng số mũ ngược (k−1)/k.',
    f'T₂/T₁ = (323.15 + 35)/323.15 = {N((Tin+dT)/Tin,4)}; isentropic: r_p = (T₂/T₁)^(k/(k−1)) = {N((Tin+dT)/Tin,4)}^3.5 = {N(PRc,2)}. This is only an illustration (the slides give no number; a real, lossy compressor needs a different pressure ratio for the same rise). {N((Tin+dT)/Tin,3)} is the temperature ratio; {N(((Tin+dT)/Tin)**(0.4/1.4),3)} uses the inverted exponent (k−1)/k.'), 3, 'pack', B('Slide Ch.3 tr.32–33 + Cengel §11-8 (minh hoạ, giả thiết đẳng entropi)', 'Slide Ch.3 p.32–33 + Cengel §11-8 (illustration, isentropic assumption)'), 'công thức đóng (verify_m03: tích phân đẳng entropi)')
reg('acm_illustration', dict(Tin=Tin, dT=dT), 'PR', PRc, 3e-4, 'generated')
Tt1, Tt2 = c2k(15.0), c2k(-10.0); PRt = (Tt1 / Tt2) ** 3.5
M(B('Slide tr.34–35: khí vào tuabin ACM khoảng 10–20 °C (lấy 15 °C) và ra ở −10 °C; slide KHÔNG cho tỉ số giãn. Minh hoạ: giả sử giãn đẳng entropi, k = 1,4. Tỉ số áp qua tuabin sẽ xấp xỉ:', 'Slides p.34–35: the air enters the ACM turbine at about 10–20 °C (take 15 °C) and leaves at −10 °C; the slides give NO expansion ratio. Illustration: assume isentropic expansion, k = 1.4. The pressure ratio across the turbine would be about:'),
  PRt, [Tt1 / Tt2, (Tt1 / Tt2) ** (0.4 / 1.4), 15 / 10.0], '', 2,
  B(f'T₁/T₂ = {N(Tt1,2)}/{N(Tt2,2)} = {N(Tt1/Tt2,4)}; r_p = (T₁/T₂)^(k/(k−1)) = {N(Tt1/Tt2,4)}^3,5 = {N(PRt,2)}. Minh hoạ giả thiết đẳng entropi: tuabin thực có tổn thất cần tỉ số lớn hơn cho cùng độ giảm nhiệt độ. {N(Tt1/Tt2,3)} là tỉ số nhiệt độ; {N((Tt1/Tt2)**(0.4/1.4),3)} dùng số mũ (k−1)/k; 1,5 dùng °C (15/10).',
    f'T₁/T₂ = {N(Tt1,2)}/{N(Tt2,2)} = {N(Tt1/Tt2,4)}; r_p = (T₁/T₂)^(k/(k−1)) = {N(Tt1/Tt2,4)}^3.5 = {N(PRt,2)}. Illustration under the isentropic assumption: a real, lossy turbine needs a larger ratio for the same temperature drop. {N(Tt1/Tt2,3)} is the temperature ratio; {N((Tt1/Tt2)**(0.4/1.4),3)} uses the exponent (k−1)/k; 1.5 uses °C (15/10).'), 3, 'pack', B('Slide Ch.3 tr.34–35 + Cengel §11-8 (minh hoạ, giả thiết đẳng entropi)', 'Slide Ch.3 p.34–35 + Cengel §11-8 (illustration, isentropic assumption)'), 'công thức đóng (verify_m03: tích phân đẳng entropi)')
reg('acm_illustration', dict(Tin=Tt1, Tout=Tt2), 'PRt', PRt, 3e-4, 'generated')
QLt = 3.5 * TON; Wt = QLt / 4.0; QHt = QLt + Wt
M(B('Một máy điều hoà 3,5 tấn lạnh (1 tấn = 211 kJ/phút) có COP = 4,0 chạy liên tục để giữ nhiệt độ phòng không đổi. Nhiệt lượng nó thải ra ngoài trời Q̇_H (kW) là:', 'An air conditioner of 3.5 tons (1 ton = 211 kJ/min) with COP = 4.0 runs continuously to hold a constant room temperature. The heat it rejects outdoors Q̇_H (kW) is:'),
  QHt, [QLt, Wt, QLt * 4.0], 'kW', 2,
  B(f'Q̇_L = 3,5·211/60 = {N(QLt,2)} kW (bằng nhiệt xâm nhập phòng khi nhiệt độ không đổi); Ẇ = Q̇_L/COP = {N(Wt,2)} kW; Q̇_H = Q̇_L + Ẇ = {N(QHt,2)} kW. {N(QLt,2)} chỉ là tải lạnh; {N(Wt,2)} chỉ là công suất điện; {N(QLt*4,1)} nhân COP.',
    f'Q̇_L = 3.5·211/60 = {N(QLt,2)} kW (equal to the heat leaking into the room at constant temperature); Ẇ = Q̇_L/COP = {N(Wt,2)} kW; Q̇_H = Q̇_L + Ẇ = {N(QHt,2)} kW. {N(QLt,2)} is only the cooling load; {N(Wt,2)} is only the electric power; {N(QLt*4,1)} multiplies by COP.'), 3, 'units', GEN('tấn lạnh, COP và nhiệt thải', 'tons, COP and rejected heat'), 'Cengel §11-1 (211 kJ/min) + Bài 11–101 (dạng) + script')
reg('identity', dict(tons=3.5, cop=4.0), 'QH', QHt, 1e-9, 'generated')

for (P2, etac, T3, m_) in ((0.8, 0.8, 30, 0.05), (1.0, 0.75, 28, 0.04)):
    r = vcrc_real(0.14, -10, P2, eta_c=etac, T3_C=T3); QHa = m_ * r['qH']
    reg('vcrc_real', dict(P1=0.14, T1=-10, P2=P2, eta_c=etac, T3=T3), 'qH', r['qH'], 0.1, 'generated')
    M(B(f'R-134a vào máy nén ở 0,14 MPa, −10 °C (h₁ = {N(r["h1"],2)} kJ/kg), nén tới {P2} MPa với η_c = {int(etac*100)} % (h₂ₛ = {N(r["h2s"],2)} kJ/kg); ra dàn ngưng là lỏng ở {T3} °C (h₃ ≅ {N(r["h3"],2)} kJ/kg); ṁ = {m_} kg/s. Nhiệt lượng thải ra ở dàn ngưng Q̇_H (kW) là:', f'R-134a enters the compressor at 0.14 MPa, −10 °C (h₁ = {N(r["h1"],2)} kJ/kg), is compressed to {P2} MPa with η_c = {int(etac*100)} % (h₂ₛ = {N(r["h2s"],2)} kJ/kg); it leaves the condenser as liquid at {T3} °C (h₃ ≅ {N(r["h3"],2)} kJ/kg); ṁ = {m_} kg/s. The heat rejected in the condenser Q̇_H (kW) is:'),
      QHa, [m_ * (r['h2s'] - r['h3']), m_ * r['qL'], m_ * (r['h2'] - r['h1'])], 'kW', 2,
      B(f'h₂ = h₁ + (h₂ₛ − h₁)/η_c = {N(r["h2"],2)} kJ/kg (trạng thái thật, không phải h₂ₛ); Q̇_H = ṁ(h₂ − h₃) = {m_}·({N(r["h2"],2)} − {N(r["h3"],2)}) = {N(QHa,2)} kW (= Q̇_L + Ẇ = {N(m_*r["qL"],2)} + {N(m_*r["w"],2)}). {N(m_*(r["h2s"]-r["h3"]),2)} dùng h₂ₛ; {N(m_*r["qL"],2)} là Q̇_L; {N(m_*r["w"],2)} là công máy nén.',
        f'h₂ = h₁ + (h₂ₛ − h₁)/η_c = {N(r["h2"],2)} kJ/kg (the real state, not h₂ₛ); Q̇_H = ṁ(h₂ − h₃) = {m_}·({N(r["h2"],2)} − {N(r["h3"],2)}) = {N(QHa,2)} kW (= Q̇_L + Ẇ = {N(m_*r["qL"],2)} + {N(m_*r["w"],2)}). {N(m_*(r["h2s"]-r["h3"]),2)} uses h₂ₛ; {N(m_*r["qL"],2)} is Q̇_L; {N(m_*r["w"],2)} is the compressor power.'), 3, 'real', GEN('nhiệt thải của chu trình thực', 'heat rejection of the actual cycle'))
cA, cB = Rv(140, 800), Rv(200, 800); dTs = cB['Tl'] - cA['Tl']; pct = 100 * (cB['cop'] / cA['cop'] - 1) / dTs
reg('cop_per_degree', dict(Pl1=140, Pl2=200, Ph=800), 'pct', pct, {'abs': 0.15}, 'generated')
M(B(f'Chu trình nén hơi lý tưởng R-134a có áp suất ngưng 800 kPa. Khi áp suất bay hơi tăng từ 140 lên 200 kPa (nhiệt độ bão hòa tăng từ {N(cA["Tl"],2)} lên {N(cB["Tl"],2)} °C), COP tăng trung bình bao nhiêu phần trăm cho mỗi °C?', f'An ideal R-134a vapor-compression cycle has a 800 kPa condenser pressure. When the evaporator pressure rises from 140 to 200 kPa (saturation temperature from {N(cA["Tl"],2)} to {N(cB["Tl"],2)} °C), by how many percent does the COP rise on average per °C?'),
  pct, [100 * (cB['cop'] / cA['cop'] - 1), (cB['cop'] - cA['cop']) / dTs, 100 * (cB['cop'] - cA['cop']) / dTs], '%', 1,
  B(f'COP(140 kPa) = {N(cA["cop"],3)}, COP(200 kPa) = {N(cB["cop"],3)}: tăng {N(100*(cB["cop"]/cA["cop"]-1),1)} % trên {N(dTs,2)} °C ⇒ {N(pct,1)} %/°C: nằm trong khoảng 2–4 % mỗi °C mà Cengel §11-3 nêu như quy tắc kinh nghiệm (bổ sung). {N(100*(cB["cop"]/cA["cop"]-1),1)} là tổng mức tăng, chưa chia cho số °C; {N((cB["cop"]-cA["cop"])/dTs,3)} là mức tăng tuyệt đối mỗi °C; {N(100*(cB["cop"]-cA["cop"])/dTs,1)} nhầm đơn vị.',
    f'COP(140 kPa) = {N(cA["cop"],3)}, COP(200 kPa) = {N(cB["cop"],3)}: up {N(100*(cB["cop"]/cA["cop"]-1),1)} % over {N(dTs,2)} °C ⇒ {N(pct,1)} %/°C: inside the 2–4 % per °C that Cengel §11-3 gives as a rule of thumb (added). {N(100*(cB["cop"]/cA["cop"]-1),1)} is the total rise, not yet divided by the number of °C; {N((cB["cop"]-cA["cop"])/dTs,3)} is the absolute rise per °C; {N(100*(cB["cop"]-cA["cop"])/dTs,1)} mixes the units.'), 3, 'vcrc', GEN('mức tăng COP theo nhiệt độ bay hơi', 'COP gain per degree of evaporating temperature'))

def main():
    orig, prn = O.build(); conc, FE = CO.build()
    items_src = list(orig) + list(conc)
    sa = os.path.join(ROOT, 'data', 'qsrc'); os.makedirs(sa, exist_ok=True)
    dump(os.path.join(sa, 'm03.json'), items_src); dump(os.path.join(sa, 'm03_gen.json'), G)
    os.makedirs(os.path.join(ROOT, 'data', 'verify'), exist_ok=True)
    dump(os.path.join(ROOT, 'data', 'verify', 'm03_values.json'), dict(registry=REG, printed=prn, fe=FE, cp=O.CPN))
    notes = NT.build(); dump(os.path.join(ROOT, 'data', 'verify', 'm03_notes.json'), notes)
    closed = [i for i in items_src + G if i['kind'] != 'ess']; l3 = [i for i in closed if i['level'] == 3]
    print(f'originals+concept {len(items_src)} (ess {sum(1 for i in items_src if i["kind"]=="ess")}, goc closed {sum(1 for i in items_src if i["kind"]!="ess" and i["origin"]=="goc")}) | generated {len(G)} | closed {len(closed)} | level 3: {len(l3)} ({100*len(l3)/len(closed):.0f} %) | registry {len(REG)} | printed {len(prn)} | FE {len(FE)} | notes vi/en {len(notes["vi"])}/{len(notes["en"])}')

if __name__ == '__main__':
    main()
