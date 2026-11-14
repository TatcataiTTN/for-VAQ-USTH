"""m02 ORIGINAL questions (origin 'goc'): Tutorials I (lecturer), Cengel Ch.9 Examples and Problems with printed answers, El-Sayed Example 4.2.
Every number comes from route A (m02_common) and is registered for build/verify/verify_m02.py (route B). Printed answers are listed in PRINTED and asserted there."""
import math
from m02_common import *

ITEMS = []; PRINTED = []
T_CARNOT = B('Chu trình Carnot', 'The Carnot cycle'); T_OTTO = B('Chu trình Otto', 'The Otto cycle'); T_DIESEL = B('Chu trình Diesel', 'The Diesel cycle')
T_BRAY = B('Chu trình Brayton đơn giản', 'The simple Brayton cycle'); T_REAL = B('Brayton thực: hiệu suất máy nén và tuabin', 'Real Brayton cycle: compressor and turbine efficiency')
T_REGEN = B('Hồi nhiệt (regeneration)', 'Regeneration'); T_MULTI = B('Làm mát trung gian và hâm nóng', 'Intercooling and reheating'); T_JET = B('Chu trình phản lực lý tưởng', 'Ideal jet-propulsion cycle')
T_OTHER = B('Chu trình khí không chuẩn', 'Non-standard air-standard cycles')

def pr(name, mine, printed, tol, src): PRINTED.append(dict(name=name, mine=mine, printed=printed, tol=tol, src=src))
def srcB(vi, en=None): return B(vi, en or vi)
def ES(q, sol, lvl, topic, src, check, fig=None): ITEMS.append(ess(q, sol, lvl, topic, src, 'goc', check, fig))
def MC(q, opts, correct, expl, lvl, topic, src, check, fig=None): ITEMS.append(mcq(q, opts, correct, expl, lvl, topic, src, 'goc', check, fig))
def num(correct, wrongs, unit, nd): return numopts(correct, wrongs, unit, nd)

def build():
    # =========================================================================== Tutorials I #1  (= Cengel Example 9-2)
    S1 = srcB('Tutorials I tr.1–6 (= Cengel Ví dụ 9–2)', 'Tutorials I p.1–6 (= Cengel Example 9–2)')
    o = otto_var(8, 290, 100, qin=800); oc = otto(8, 290, 100, qin=800)
    for k_, v_ in o.items():
        if k_ in ('T2', 'T3', 'T4', 'P3', 'qout', 'wnet', 'eta', 'mep'): reg('otto_v', dict(r=8, T1=290, P1=100, qin=800), k_, v_, 0.012)
    pr('Tut1 T3', o['T3'], 1575.1, 2e-4, 'Tutorials I tr.3'); pr('Tut1 P3', o['P3'], 4345, 3e-4, 'Tutorials I tr.4'); pr('Tut1 wnet', o['wnet'], 418.17, 1e-4, 'Tutorials I tr.5')
    pr('Tut1 eta', o['eta'], 0.523, 1e-3, 'Tutorials I tr.5'); pr('Tut1 eta cold-air', 1 - 8 ** -0.4, 0.565, 1e-3, 'Tutorials I tr.6'); pr('Tut1 MEP', o['mep'], 574, 1e-3, 'Tutorials I tr.6')
    MC(B('Chu trình Otto lý tưởng có r = 8; đầu quá trình nén không khí ở 100 kPa, 17 °C; nhiệt cấp đẳng tích 800 kJ/kg; tính đến sự thay đổi nhiệt dung riêng theo nhiệt độ (bảng A-17, lấy T₁ = 290 K). Nhiệt độ cực đại trong chu trình là:',
          'An ideal Otto cycle has r = 8; at the start of compression the air is at 100 kPa and 17 °C; 800 kJ/kg of heat is added at constant volume; account for the variation of specific heats with temperature (Table A-17, take T₁ = 290 K). The maximum temperature in the cycle is:'),
       num(o['T3'], [oc['T3'], 290 + 800 / CV_AIR, o['T3'] - 273.15], 'K', 1), 0,
       B(f'T₂: v_r2 = v_r1/r = 676,1/8 = 84,51 ⇒ T₂ = {N(o["T2"],1)} K, u₂ = {N(o["u2"],2)} kJ/kg; u₃ = u₂ + q_in = {N(o["u3"],2)} kJ/kg ⇒ T₃ = {N(o["T3"],1)} K (slide tr.3). Dùng cv hằng (nén T₂ = 290·8^0,4) cho {N(oc["T3"],1)} K; bỏ bước nén cho {N(290+800/CV_AIR,1)} K; {N(o["T3"]-273.15,1)} là °C.',
         f'T₂: v_r2 = v_r1/r = 676.1/8 = 84.51 ⇒ T₂ = {N(o["T2"],1)} K, u₂ = {N(o["u2"],2)} kJ/kg; u₃ = u₂ + q_in = {N(o["u3"],2)} kJ/kg ⇒ T₃ = {N(o["T3"],1)} K (slide p.3). Constant cv (T₂ = 290·8^0.4) gives {N(oc["T3"],1)} K; skipping the compression step gives {N(290+800/CV_AIR,1)} K; {N(o["T3"]-273.15,1)} is in °C.'),
       2, T_OTTO, S1, 'slide tr.3 + script')
    MC(B('Cùng bài (Tutorials I #1): hiệu suất nhiệt của chu trình, tính từ w_net/q_in với nhiệt dung riêng thay đổi, là:', 'Same problem (Tutorials I #1): the thermal efficiency from w_net/q_in with variable specific heats is:'),
       num(o['eta'], [1 - 8 ** -0.4, o['qout'] / o['qin'], 1 - 1 / 8], '', 3), 0,
       B(f'u₄ = {N(o["u4"],2)} kJ/kg (v_r4 = r·v_r3 = {N(8*o["vr3"],3)}), q_out = u₄ − u₁ = {N(o["qout"],2)} kJ/kg, w_net = {N(o["wnet"],2)} kJ/kg, η = {N(o["eta"],3)}. Công thức khí lạnh 1 − r^(1−k) cho {N(1-8**-.4,3)} (cao hơn vì cv thật tăng theo T); {N(o["qout"]/o["qin"],3)} là q_out/q_in; 1 − 1/r cho {N(1-1/8,3)}.',
         f'u₄ = {N(o["u4"],2)} kJ/kg (v_r4 = r·v_r3 = {N(8*o["vr3"],3)}), q_out = u₄ − u₁ = {N(o["qout"],2)} kJ/kg, w_net = {N(o["wnet"],2)} kJ/kg, η = {N(o["eta"],3)}. The cold-air formula 1 − r^(1−k) gives {N(1-8**-.4,3)} (higher, because the real cv rises with T); {N(o["qout"]/o["qin"],3)} is q_out/q_in; 1 − 1/r gives {N(1-1/8,3)}.'),
       2, T_OTTO, S1, 'slide tr.5 + script')
    v1 = o['v1']
    MC(B('Cùng bài (Tutorials I #1): áp suất có ích trung bình MEP = w_net/(v₁ − v₂) là:', 'Same problem (Tutorials I #1): the mean effective pressure MEP = w_net/(v₁ − v₂) is:'),
       num(o['mep'], [o['wnet'] / v1, o['qin'] / (v1 * (1 - 1 / 8)), o['wnet'] / (0.287 * 17 / 100 * (1 - 1 / 8))], 'kPa', 0), 0,
       B(f'v₁ = RT₁/P₁ = 0,287·290/100 = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o["wnet"],2)}/({N(v1,3)}·0,875) = {N(o["mep"],0)} kPa. Chia cho v₁ (quên v₂) cho {N(o["wnet"]/v1,0)}; dùng q_in thay w_net cho {N(o["qin"]/(v1*0.875),0)}; dùng 17 (°C) thay T₁ cho {N(o["wnet"]/(0.287*17/100*.875),0)}.',
         f'v₁ = RT₁/P₁ = 0.287·290/100 = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o["wnet"],2)}/({N(v1,3)}·0.875) = {N(o["mep"],0)} kPa. Dividing by v₁ (forgetting v₂) gives {N(o["wnet"]/v1,0)}; using q_in instead of w_net gives {N(o["qin"]/(v1*0.875),0)}; using 17 (°C) for T₁ gives {N(o["wnet"]/(0.287*17/100*.875),0)}.'),
       3, T_OTTO, S1, 'slide tr.6 + script')
    ES(B('Tutorials I #1. Chu trình Otto lý tưởng có tỉ số nén 8. Đầu quá trình nén không khí ở 100 kPa, 17 °C; nhiệt cấp trong quá trình đẳng tích 800 kJ/kg. Tính đến sự thay đổi nhiệt dung riêng theo nhiệt độ, tính (a) nhiệt độ và áp suất cực đại, (b) công thực, (c) hiệu suất nhiệt, (d) MEP.',
         'Tutorials I #1. An ideal Otto cycle has a compression ratio of 8. At the beginning of compression the air is at 100 kPa and 17 °C; 800 kJ/kg of heat is added at constant volume. Accounting for the variation of specific heats with temperature, determine (a) the maximum temperature and pressure, (b) the net work, (c) the thermal efficiency, (d) the MEP.'),
       B(f'Giả thiết (slide tr.2): không khí-chuẩn, bỏ qua động năng/thế năng, nhiệt dung riêng thay đổi: dùng bảng A-17 (nội suy tuyến tính). 17 °C lấy 290 K như slide (290,15 K chỉ đổi T₃ +0,3 K); R = 0,287 kJ/(kg·K).\n'
         f'Bước 1 (1→2 đẳng entropi). T₁ = 290 K ⇒ u₁ = 206,91 kJ/kg, v_r1 = 676,1. v_r2 = v_r1/r = 84,51 ⇒ T₂ = {N(o["T2"],1)} K, u₂ = {N(o["u2"],2)} kJ/kg. P₂ = P₁(T₂/T₁)·r = 100·({N(o["T2"],1)}/290)·8 = {N(o["P2"],1)} kPa.\n'
         f'Bước 2 (2→3 đẳng tích). u₃ = u₂ + q_in = {N(o["u2"],2)} + 800 = {N(o["u3"],2)} kJ/kg ⇒ T₃ = {N(o["T3"],1)} K, v_r3 = {N(o["vr3"],3)}. P₃ = P₂·T₃/T₂ = {N(o["P3"],0)} kPa. Vậy (a) T_max = {N(o["T3"],1)} K, P_max = {N(o["P3"]/1000,3)} MPa.\n'
         f'Bước 3 (3→4 đẳng entropi). v_r4 = r·v_r3 = {N(8*o["vr3"],2)} ⇒ T₄ = {N(o["T4"],1)} K, u₄ = {N(o["u4"],2)} kJ/kg. q_out = u₄ − u₁ = {N(o["qout"],2)} kJ/kg.\n'
         f'Bước 4. (b) w_net = q_in − q_out = 800 − {N(o["qout"],2)} = {N(o["wnet"],2)} kJ/kg. (c) η = w_net/q_in = {N(o["eta"],3)} (khí lạnh: 1 − 8^(−0,4) = {N(1-8**-.4,3)}). (d) v₁ = 0,287·290/100 = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/8)] = {N(o["mep"],0)} kPa.\n'
         'Hai đường: (A) bảng A-17 như trên; (B) tích phân số cp(T) đa thức A-2c và CoolProp (verify_m02.py), lệch ≤ 1 %. Đáp số slide: 1575,1 K; 4,345 MPa; 418,17 kJ/kg; 52,3 %; 574 kPa.',
         f'Assumptions (slide p.2): air-standard, negligible kinetic/potential energy, variable specific heats: Table A-17 with linear interpolation. 17 °C is taken as 290 K as on the slide (290.15 K changes T₃ by +0.3 K only); R = 0.287 kJ/(kg·K).\n'
         f'Step 1 (1→2 isentropic). T₁ = 290 K ⇒ u₁ = 206.91 kJ/kg, v_r1 = 676.1. v_r2 = v_r1/r = 84.51 ⇒ T₂ = {N(o["T2"],1)} K, u₂ = {N(o["u2"],2)} kJ/kg. P₂ = P₁(T₂/T₁)·r = 100·({N(o["T2"],1)}/290)·8 = {N(o["P2"],1)} kPa.\n'
         f'Step 2 (2→3 constant volume). u₃ = u₂ + q_in = {N(o["u2"],2)} + 800 = {N(o["u3"],2)} kJ/kg ⇒ T₃ = {N(o["T3"],1)} K, v_r3 = {N(o["vr3"],3)}. P₃ = P₂·T₃/T₂ = {N(o["P3"],0)} kPa. So (a) T_max = {N(o["T3"],1)} K, P_max = {N(o["P3"]/1000,3)} MPa.\n'
         f'Step 3 (3→4 isentropic). v_r4 = r·v_r3 = {N(8*o["vr3"],2)} ⇒ T₄ = {N(o["T4"],1)} K, u₄ = {N(o["u4"],2)} kJ/kg. q_out = u₄ − u₁ = {N(o["qout"],2)} kJ/kg.\n'
         f'Step 4. (b) w_net = q_in − q_out = 800 − {N(o["qout"],2)} = {N(o["wnet"],2)} kJ/kg. (c) η = w_net/q_in = {N(o["eta"],3)} (cold air: 1 − 8^(−0.4) = {N(1-8**-.4,3)}). (d) v₁ = 0.287·290/100 = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/8)] = {N(o["mep"],0)} kPa.\n'
         'Two routes: (A) Table A-17 as above; (B) numerical integration of cp(T) from the A-2c polynomial and from CoolProp (verify_m02.py), within 1 %. Slide results: 1575.1 K; 4.345 MPa; 418.17 kJ/kg; 52.3 %; 574 kPa.'),
       3, T_OTTO, S1, 'slide + script')

    # =========================================================================== Tutorials I #2 (= Cengel Example 9-3), English units, cp, cv constant
    S2 = srcB('Tutorials I tr.7–13 (= Cengel Ví dụ 9–3)', 'Tutorials I p.7–13 (= Cengel Example 9–3)')
    RE = 0.3704; cpE, cvE = 0.240, 0.171; V1 = 117.0 / 1728.0                      # ft3
    d = diesel(18, 540, 14.7, k=1.4, R=RE, cp=cpE, cv=cvE, rc=2)                   # R in psia ft3/(lbm R)  -> v in ft3/lbm
    m_ = 14.7 * 117 / (RE * 540 * 1728)
    Qin = m_ * d['qin']; Qout = m_ * d['qout']; W = Qin - Qout; mepE = W * 778.17 * 12 / (117 - 117 / 18)
    reg('diesel_E', dict(r=18, rc=2, T1=540, P1=14.7, V1_in3=117, k=1.4, R=RE, cp=cpE, cv=cvE), 'T2', d['T2'], 1e-3); reg('diesel_E', dict(r=18, rc=2, T1=540, P1=14.7, V1_in3=117, k=1.4, R=RE, cp=cpE, cv=cvE), 'P2', d['P2'], 1e-3)
    for nm_, val_ in (('T3', d['T3']), ('T4', d['T4']), ('P4', d['P4']), ('m', m_), ('Qin', Qin), ('Qout', Qout), ('W', W), ('eta', W / Qin), ('mep', mepE)):
        reg('diesel_E', dict(r=18, rc=2, T1=540, P1=14.7, V1_in3=117, k=1.4, R=RE, cp=cpE, cv=cvE), nm_, val_, 2e-3)
    pr('Tut2 T2', d['T2'], 1716, 2e-3, 'Tutorials I tr.9'); pr('Tut2 P2', d['P2'], 841, 2e-3, 'tr.9'); pr('Tut2 T3', d['T3'], 3432, 2e-3, 'tr.9'); pr('Tut2 T4', d['T4'], 1425, 2e-3, 'tr.10'); pr('Tut2 P4', d['P4'], 38.8, 3e-3, 'tr.10')
    pr('Tut2 m', m_, 0.00498, 2e-3, 'tr.10'); pr('Tut2 Qin', Qin, 2.051, 2e-3, 'tr.11'); pr('Tut2 Qout', Qout, 0.754, 2e-3, 'tr.11'); pr('Tut2 W', W, 1.297, 3e-3, 'tr.12'); pr('Tut2 eta', W / Qin, 0.632, 2e-3, 'tr.12'); pr('Tut2 MEP', mepE, 110, 6e-3, 'tr.13 (rounded from 109.5)')
    MC(B('Chu trình Diesel lý tưởng, không khí, r = 18, r_c = 2; đầu nén: 14,7 psia, 80 °F (= 540 R), 117 in³. Giả thiết khí lạnh (k = 1,4). Nhiệt độ sau quá trình cấp nhiệt đẳng áp (T₃) là:',
          'Ideal Diesel cycle, air, r = 18, r_c = 2; start of compression 14.7 psia, 80 °F (= 540 R), 117 in³. Cold-air-standard (k = 1.4). The temperature after the constant-pressure heat addition (T₃) is:'),
       num(d['T3'], [d['T2'], d['T2'] * 2 ** 2, 540 * 2], 'R', 0), 0,
       B(f'T₂ = T₁ r^(k−1) = 540·18^0,4 = {N(d["T2"],0)} R; quá trình 2→3 đẳng áp nên T₃ = T₂·V₃/V₂ = r_c T₂ = {N(d["T3"],0)} R. Quên r_c cho {N(d["T2"],0)}; nhân r_c hai lần cho {N(d["T2"]*4,0)}; T₁·r_c cho {N(1080,0)} (bỏ nén).',
         f'T₂ = T₁ r^(k−1) = 540·18^0.4 = {N(d["T2"],0)} R; process 2→3 is isobaric so T₃ = T₂·V₃/V₂ = r_c T₂ = {N(d["T3"],0)} R. Forgetting r_c gives {N(d["T2"],0)}; applying r_c twice gives {N(d["T2"]*4,0)}; T₁·r_c gives {N(1080,0)} (no compression).'),
       2, T_DIESEL, S2, 'slide tr.9 + script')
    MC(B('Cùng bài (Tutorials I #2): hiệu suất nhiệt từ W_net/Q_in (c_p = 0,240; c_v = 0,171 Btu/lbm·R) là:', 'Same problem (Tutorials I #2): the thermal efficiency from W_net/Q_in (c_p = 0.240; c_v = 0.171 Btu/lbm·R) is:'),
       num(W / Qin, [1 - 18 ** -0.4, 1 - 18 ** -0.4 * (2 ** 1.4 - 1) / (2 - 1), Qout / Qin], '', 3), 0,
       B(f'm = P₁V₁/(RT₁) = {N(m_,5)} lbm; Q_in = m c_p(T₃ − T₂) = {N(Qin,3)} Btu; Q_out = m c_v(T₄ − T₁) = {N(Qout,3)} Btu; W_net = {N(W,3)} Btu; η = {N(W/Qin,3)}. Công thức Otto cho {N(1-18**-.4,3)} (sai: bỏ ngoặc r_c); quên k ở mẫu số ngoặc cho {N(1-18**-.4*(2**1.4-1),3)}; Q_out/Q_in = {N(Qout/Qin,3)}. Slide dùng k = 1,4 cho nhiệt độ nhưng c_p/c_v = {N(.24/.171,4)} cho nhiệt lượng; công thức chính xác với k = 1,4 cho {N(1-18**-.4*(2**1.4-1)/1.4,4)}.',
         f'm = P₁V₁/(RT₁) = {N(m_,5)} lbm; Q_in = m c_p(T₃ − T₂) = {N(Qin,3)} Btu; Q_out = m c_v(T₄ − T₁) = {N(Qout,3)} Btu; W_net = {N(W,3)} Btu; η = {N(W/Qin,3)}. The Otto formula gives {N(1-18**-.4,3)} (wrong: drops the r_c bracket); forgetting k in the bracket denominator gives {N(1-18**-.4*(2**1.4-1),3)}; Q_out/Q_in = {N(Qout/Qin,3)}. The slide uses k = 1.4 for temperatures but c_p/c_v = {N(.24/.171,4)} for the heats; the exact formula with k = 1.4 gives {N(1-18**-.4*(2**1.4-1)/1.4,4)}.'),
       3, T_DIESEL, S2, 'slide tr.12 + script')
    MC(B('Cùng bài (Tutorials I #2): MEP = W_net/(V₁ − V₂) là:', 'Same problem (Tutorials I #2): the MEP = W_net/(V₁ − V₂) is:'),
       num(mepE, [W * 778.17 * 12 / 117, d['P2'], d['P4']], 'psia', 1), 0,
       B(f'W_net = {N(W,3)} Btu = {N(W*778.17*12,1)} lbf·in; V₁ − V₂ = 117 − 6,5 = 110,5 in³ ⇒ MEP = {N(mepE,1)} psia (slide làm tròn 110). Chia cho V₁ cho {N(W*778.17*12/117,1)}; {N(d["P2"],0)} là P₂ và {N(d["P4"],1)} là P₄.',
         f'W_net = {N(W,3)} Btu = {N(W*778.17*12,1)} lbf·in; V₁ − V₂ = 117 − 6.5 = 110.5 in³ ⇒ MEP = {N(mepE,1)} psia (the slide rounds to 110). Dividing by V₁ gives {N(W*778.17*12/117,1)}; {N(d["P2"],0)} is P₂ and {N(d["P4"],1)} is P₄.'),
       3, T_DIESEL, S2, 'slide tr.13 + script')
    ES(B('Tutorials I #2. Chu trình Diesel lý tưởng, không khí, r = 18, r_c = 2; đầu nén: 14,7 psia, 80 °F, 117 in³. Giả thiết khí lạnh. Tính (a) T và P ở cuối mỗi quá trình, (b) công thực và hiệu suất, (c) MEP.',
         'Tutorials I #2. Ideal Diesel cycle with air, r = 18, r_c = 2; at the start of compression 14.7 psia, 80 °F, 117 in³. Cold-air-standard. Determine (a) T and P at the end of each process, (b) the net work and thermal efficiency, (c) the MEP.'),
       B(f'Giả thiết: khí lạnh; R = 0,3704 psia·ft³/(lbm·R); c_p = 0,240; c_v = 0,171 Btu/(lbm·R); 80 °F = 540 R; nhiệt độ/áp suất dùng k = 1,4 (như slide), nhiệt lượng dùng c_p, c_v (tỉ số {N(.24/.171,4)}).\n'
         f'(a) V₂ = V₁/18 = 6,5 in³; V₃ = r_c V₂ = 13 in³. T₂ = 540·18^0,4 = {N(d["T2"],0)} R; P₂ = 14,7·18^1,4 = {N(d["P2"],0)} psia = P₃; T₃ = T₂·r_c = {N(d["T3"],0)} R; T₄ = T₃(V₃/V₄)^0,4 = {N(d["T4"],0)} R; P₄ = P₃(V₃/V₄)^1,4 = {N(d["P4"],1)} psia.\n'
         f'(b) m = P₁V₁/(RT₁) = (14,7·117)/(0,3704·540·1728) = {N(m_,5)} lbm. Q_in = m c_p(T₃ − T₂) = {N(Qin,3)} Btu; Q_out = m c_v(T₄ − T₁) = {N(Qout,3)} Btu; W_net = {N(W,3)} Btu; η = {N(W/Qin,3)}.\n'
         f'(c) MEP = W_net/(V₁ − V₂) = {N(W,3)}·778,17·12/110,5 = {N(mepE,1)} psia (slide: 110).\n'
         f'Hai đường: (A) công thức đóng như trên; (B) đổi sang SI và dựng chu trình bằng tích phân ∮P dV (verify_m02.py). Ghi chú nguồn: slide nói hằng số "ở 25 °C/77 °F" nhưng dùng 80 °F; dẫn "Table A–2a" (bảng đúng là A-2E(a)); η chính xác với k = 1,4 là {N(1-18**-.4*(2**1.4-1)/1.4,4)}.',
         f'Assumptions: cold air; R = 0.3704 psia·ft³/(lbm·R); c_p = 0.240; c_v = 0.171 Btu/(lbm·R); 80 °F = 540 R; temperatures/pressures use k = 1.4 (as on the slide), heats use c_p, c_v (ratio {N(.24/.171,4)}).\n'
         f'(a) V₂ = V₁/18 = 6.5 in³; V₃ = r_c V₂ = 13 in³. T₂ = 540·18^0.4 = {N(d["T2"],0)} R; P₂ = 14.7·18^1.4 = {N(d["P2"],0)} psia = P₃; T₃ = T₂·r_c = {N(d["T3"],0)} R; T₄ = T₃(V₃/V₄)^0.4 = {N(d["T4"],0)} R; P₄ = P₃(V₃/V₄)^1.4 = {N(d["P4"],1)} psia.\n'
         f'(b) m = P₁V₁/(RT₁) = (14.7·117)/(0.3704·540·1728) = {N(m_,5)} lbm. Q_in = m c_p(T₃ − T₂) = {N(Qin,3)} Btu; Q_out = m c_v(T₄ − T₁) = {N(Qout,3)} Btu; W_net = {N(W,3)} Btu; η = {N(W/Qin,3)}.\n'
         f'(c) MEP = W_net/(V₁ − V₂) = {N(W,3)}·778.17·12/110.5 = {N(mepE,1)} psia (slide: 110).\n'
         f'Two routes: (A) closed forms as above; (B) convert to SI and build the cycle by integrating ∮P dV (verify_m02.py). Source notes: the slide says the constants are "at 25 °C/77 °F" but uses 80 °F; it cites "Table A–2a" (the table is A-2E(a)); the exact η with k = 1.4 is {N(1-18**-.4*(2**1.4-1)/1.4,4)}.'),
       3, T_DIESEL, S2, 'slide + script')

    # =========================================================================== Tutorials I #3 (= Cengel 9-37): Otto 9.5, T4 = 800 K, constant specific heats
    S3 = srcB('Tutorials I tr.14 (= Cengel Bài 9–37)', 'Tutorials I p.14 (= Cengel Problem 9–37)')
    p3 = dict(r=9.5, T1=308, P1=100, T4=800, k=1.4, R=0.287, cv=0.718); o3 = otto(9.5, 308, 100, T4=800); m3 = 100 * 600e-6 / (0.287 * 308); Q3 = m3 * o3['qin']
    o3b = otto(9.5, 308.15, 100, T4=800)
    for k_ in ('T3', 'T2', 'P3', 'qin', 'qout', 'wnet', 'eta', 'mep'): reg('otto_k', p3, k_, o3[k_], 1e-6)
    reg('otto_k', dict(p3, T1=308.15), 'P3', o3b['P3'], 1e-6)
    pr('9-37 T3', o3['T3'], 1969, 3e-4, 'Cengel 9–37 (ans.)'); pr('9-37 P3', o3['P3'], 6072, 1e-4, 'Cengel 9–37'); pr('9-37 Qin', Q3, 0.59, 2e-3, 'Cengel 9–37'); pr('9-37 eta', o3['eta'], 0.594, 1e-3, 'Cengel 9–37'); pr('9-37 MEP', o3['mep'], 652, 1e-3, 'Cengel 9–37')
    MC(B('Chu trình Otto khí-chuẩn có r = 9,5; trước nén không khí ở 100 kPa, 35 °C, 600 cm³; nhiệt độ cuối quá trình giãn đẳng entropi là 800 K. Dùng nhiệt dung riêng ở nhiệt độ phòng (k = 1,4; c_v = 0,718 kJ/kg·K). Nhiệt độ cao nhất của chu trình là:',
          'An air-standard Otto cycle has r = 9.5; before compression the air is at 100 kPa, 35 °C, 600 cm³; the temperature at the end of the isentropic expansion is 800 K. Use room-temperature specific heats (k = 1.4; c_v = 0.718 kJ/kg·K). The highest temperature of the cycle is:'),
       num(o3['T3'], [800, 800 / 9.5 ** 0.4, 800 * 9.5 ** (0.4 / 1.4)], 'K', 0), 0,
       B(f'3→4 là đẳng entropi: T₃ = T₄ r^(k−1) = 800·9,5^0,4 = {N(o3["T3"],1)} K. T₃ = T₄ là nhầm giãn nở với đẳng nhiệt; chia cho r^(k−1) cho {N(800/9.5**.4,1)}; dùng số mũ (k−1)/k thay k−1 cho {N(800*9.5**(.4/1.4),1)}.',
         f'3→4 is isentropic: T₃ = T₄ r^(k−1) = 800·9.5^0.4 = {N(o3["T3"],1)} K. T₃ = T₄ treats the expansion as isothermal; dividing by r^(k−1) gives {N(800/9.5**.4,1)}; using the exponent (k−1)/k instead of k−1 gives {N(800*9.5**(.4/1.4),1)}.'),
       2, T_OTTO, S3, 'printed answer Cengel 9–37 + script')
    MC(B('Cùng bài (Tutorials I #3): nhiệt lượng cấp vào chu trình Q_in (kJ) với khối lượng khí m = P₁V₁/(RT₁) là:', 'Same problem (Tutorials I #3): the heat added Q_in (kJ) with the air mass m = P₁V₁/(RT₁) is:'),
       num(Q3, [m3 * CP_AIR * (o3['T3'] - o3['T2']), m3 * o3['wnet'], m3 * o3['qout']], 'kJ', 3), 0,
       B(f'm = 100·0,0006/(0,287·308) = {N(m3,6)} kg; T₂ = 308·9,5^0,4 = {N(o3["T2"],1)} K; Q_in = m c_v(T₃ − T₂) = {N(m3,6)}·0,718·{N(o3["T3"]-o3["T2"],1)} = {N(Q3,3)} kJ (đáp án in 0,59). Dùng c_p thay c_v cho {N(m3*CP_AIR*(o3["T3"]-o3["T2"]),3)} (đẳng tích phải dùng c_v); {N(m3*o3["wnet"],3)} là công thực; {N(m3*o3["qout"],3)} là nhiệt thải.',
         f'm = 100·0.0006/(0.287·308) = {N(m3,6)} kg; T₂ = 308·9.5^0.4 = {N(o3["T2"],1)} K; Q_in = m c_v(T₃ − T₂) = {N(m3,6)}·0.718·{N(o3["T3"]-o3["T2"],1)} = {N(Q3,3)} kJ (printed answer 0.59). Using c_p instead of c_v gives {N(m3*CP_AIR*(o3["T3"]-o3["T2"]),3)} (constant-volume heating needs c_v); {N(m3*o3["wnet"],3)} is the net work; {N(m3*o3["qout"],3)} is the heat rejected.'),
       3, T_OTTO, S3, 'printed answer Cengel 9–37 + script')
    ES(B('Tutorials I #3. Chu trình Otto khí-chuẩn có r = 9,5. Trước nén: 100 kPa, 35 °C, 600 cm³. Nhiệt độ cuối giãn đẳng entropi 800 K. Dùng nhiệt dung riêng ở nhiệt độ phòng, tính (a) nhiệt độ và áp suất cực đại, (b) nhiệt cấp vào (kJ), (c) hiệu suất, (d) MEP.',
         'Tutorials I #3. An air-standard Otto cycle has r = 9.5. Before compression: 100 kPa, 35 °C, 600 cm³. The temperature at the end of the isentropic expansion is 800 K. Using room-temperature specific heats determine (a) the highest temperature and pressure, (b) the heat added (kJ), (c) the thermal efficiency, (d) the MEP.'),
       B(f'(Slide không có lời giải; đề không in c_v, R: lấy A-2a: c_v = 0,718 kJ/(kg·K), R = 0,287, k = 1,4. 35 °C = 308 K; nếu 308,15 K thì P₃ = {N(o3b["P3"],0)} kPa, MEP = {N(o3b["mep"],1)} kPa.)\n'
         f'(a) T₃ = T₄ r^(k−1) = 800·9,5^0,4 = {N(o3["T3"],1)} K. T₂ = 308·9,5^0,4 = {N(o3["T2"],1)} K; P₂ = 100·9,5^1,4 = {N(o3["P2"] if "P2" in o3 else 100*9.5**1.4,1)} kPa; P₃ = P₂T₃/T₂ = {N(o3["P3"],0)} kPa.\n'
         f'(b) m = {N(m3,6)} kg; q_in = c_v(T₃ − T₂) = {N(o3["qin"],1)} kJ/kg; Q_in = {N(Q3,3)} kJ.\n'
         f'(c) η = 1 − 9,5^(−0,4) = {N(o3["eta"],4)} (kiểm: w_net/q_in = ({N(o3["qin"],1)} − {N(o3["qout"],1)})/{N(o3["qin"],1)}).\n'
         f'(d) v₁ = 0,287·308/100 = {N(o3["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o3["wnet"],1)}/({N(o3["v1"],4)}·0,8947) = {N(o3["mep"],1)} kPa.\n'
         'Đáp án in (Cengel 9–37): 1969 K, 6072 kPa; 0,59 kJ; 59,4 %; 652 kPa: khớp. Hai đường: công thức đóng, và tích phân ∮P dV số (verify_m02.py).',
         f'(The slide has no solution; the statement prints neither c_v nor R: take A-2a: c_v = 0.718 kJ/(kg·K), R = 0.287, k = 1.4. 35 °C = 308 K; with 308.15 K, P₃ = {N(o3b["P3"],0)} kPa and MEP = {N(o3b["mep"],1)} kPa.)\n'
         f'(a) T₃ = T₄ r^(k−1) = 800·9.5^0.4 = {N(o3["T3"],1)} K. T₂ = 308·9.5^0.4 = {N(o3["T2"],1)} K; P₂ = 100·9.5^1.4 = {N(100*9.5**1.4,1)} kPa; P₃ = P₂T₃/T₂ = {N(o3["P3"],0)} kPa.\n'
         f'(b) m = {N(m3,6)} kg; q_in = c_v(T₃ − T₂) = {N(o3["qin"],1)} kJ/kg; Q_in = {N(Q3,3)} kJ.\n'
         f'(c) η = 1 − 9.5^(−0.4) = {N(o3["eta"],4)} (check: w_net/q_in = ({N(o3["qin"],1)} − {N(o3["qout"],1)})/{N(o3["qin"],1)}).\n'
         f'(d) v₁ = 0.287·308/100 = {N(o3["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o3["wnet"],1)}/({N(o3["v1"],4)}·0.8947) = {N(o3["mep"],1)} kPa.\n'
         'Printed answer (Cengel 9–37): 1969 K, 6072 kPa; 0.59 kJ; 59.4 %; 652 kPa: matches. Two routes: closed forms, and numerical ∮P dV integration (verify_m02.py).'),
       3, T_OTTO, S3, 'printed answer Cengel 9–37 + script')

    # =========================================================================== Tutorials I #4 (English units, A-17E), Otto r = 8, 540-2400 R
    S4 = srcB('Tutorials I tr.15 (= Cengel Bài 9–35E)', 'Tutorials I p.15 (= Cengel Problem 9–35E)')
    o4 = otto_var(8, 540, None, T3=2400, E=True); oc4 = 1 - 540 / 2400
    for k_ in ('T2', 'T4', 'qin', 'qout', 'wnet', 'eta'): reg('otto_v', dict(r=8, T1=540, T3=2400, E=True), k_, o4[k_], 0.012)
    cold4 = 1 - 8 ** -0.4
    MC(B('Chu trình Otto lý tưởng có r = 8, T_min = 540 R, T_max = 2400 R; tính đến nhiệt dung riêng thay đổi (bảng A-17E). Nhiệt cấp vào (Btu/lbm) là:', 'An ideal Otto cycle has r = 8, T_min = 540 R, T_max = 2400 R; account for variable specific heats (Table A-17E). The heat added (Btu/lbm) is:'),
       num(o4['qin'], [0.171 * (2400 - 540 * 8 ** 0.4), 0.240 * (2400 - 540 * 8 ** 0.4), A(2400, 'h', True) - A(540, 'h', True)], 'Btu/lbm', 1), 0,
       B(f'T₂ từ v_r: v_r2 = v_r1/8 ⇒ T₂ = {N(o4["T2"],1)} R, u₂ = {N(o4["u2"],2)} Btu/lbm; u₃(2400 R) = {N(o4["u3"],2)}; q_in = u₃ − u₂ = {N(o4["qin"],1)} Btu/lbm. Cold-air với c_v = 0,171 cho {N(0.171*(2400-540*8**.4),1)}; với c_p = 0,240 cho {N(0.240*(2400-540*8**.4),1)}; h₃ − h₁ cho {N(A(2400,"h",True)-A(540,"h",True),1)} (bỏ nén).',
         f'T₂ from v_r: v_r2 = v_r1/8 ⇒ T₂ = {N(o4["T2"],1)} R, u₂ = {N(o4["u2"],2)} Btu/lbm; u₃(2400 R) = {N(o4["u3"],2)}; q_in = u₃ − u₂ = {N(o4["qin"],1)} Btu/lbm. Cold air with c_v = 0.171 gives {N(0.171*(2400-540*8**.4),1)}; with c_p = 0.240 gives {N(0.240*(2400-540*8**.4),1)}; h₃ − h₁ gives {N(A(2400,"h",True)-A(540,"h",True),1)} (skipping the compression).'),
       2, T_OTTO, S4, 'script (A-17E) + QA tut')
    MC(B('Cùng bài (Tutorials I #4): hiệu suất nhiệt của chu trình Otto (A-17E) và hiệu suất Carnot giữa cùng hai giới hạn nhiệt độ lần lượt là:', 'Same problem (Tutorials I #4): the thermal efficiency of the Otto cycle (A-17E) and the Carnot efficiency between the same temperature limits are, respectively:'),
       [B(f'{N(o4["eta"],3)} và {N(oc4,3)}', f'{N(o4["eta"],3)} and {N(oc4,3)}'), B(f'{N(cold4,3)} và {N(oc4,3)}', f'{N(cold4,3)} and {N(oc4,3)}'), B(f'{N(o4["eta"],3)} và {N(1-540/2400*8**0.4,3)}', f'{N(o4["eta"],3)} and {N(1-540/2400*8**0.4,3)}'), B(f'{N(oc4,3)} và {N(o4["eta"],3)}', f'{N(oc4,3)} and {N(o4["eta"],3)}')], 0,
       B(f'η = 1 − q_out/q_in = 1 − {N(o4["qout"],1)}/{N(o4["qin"],1)} = {N(o4["eta"],3)}; Carnot = 1 − T_L/T_H = 1 − 540/2400 = {N(oc4,3)}. Hiệu suất Otto luôn thấp hơn Carnot; cặp có {N(cold4,3)} dùng công thức khí lạnh (k = 1,4); cặp có {N(1-540/2400*8**0.4,3)} tính nhầm Carnot với T₂ thay T₁; cặp có {N(oc4,3)} đứng trước đảo thứ tự hai giá trị.',
         f'η = 1 − q_out/q_in = 1 − {N(o4["qout"],1)}/{N(o4["qin"],1)} = {N(o4["eta"],3)}; Carnot = 1 − T_L/T_H = 1 − 540/2400 = {N(oc4,3)}. The Otto efficiency is always below the Carnot value; the pair with {N(cold4,3)} uses the cold-air formula (k = 1.4); the pair with {N(1-540/2400*8**0.4,3)} mistakes T₂ for T₁ in the Carnot value; the pair starting with {N(oc4,3)} swaps the two values.'),
       3, T_OTTO, S4, 'script (A-17E) + QA tut', fig=None)
    ES(B('Tutorials I #4. Chu trình Otto lý tưởng, không khí, r = 8; T_min = 540 R, T_max = 2400 R. Tính đến nhiệt dung riêng thay đổi, tính (a) nhiệt cấp vào, (b) hiệu suất, (c) hiệu suất Carnot giữa cùng hai nhiệt độ.',
         'Tutorials I #4. Ideal Otto cycle with air, r = 8; T_min = 540 R, T_max = 2400 R. Accounting for variable specific heats, determine (a) the heat added, (b) the thermal efficiency, (c) the Carnot efficiency between the same limits.'),
       B(f'(Slide không có lời giải; đề không nêu bảng và P₁: dùng A-17E (đơn vị R), không tính MEP.)\n'
         f'(a) T₁ = 540 R ⇒ u₁ = {N(o4["u1"],2)} Btu/lbm, v_r1 = {N(A(540,"vr",True),2)}; v_r2 = v_r1/8 ⇒ T₂ = {N(o4["T2"],1)} R, u₂ = {N(o4["u2"],2)}. T₃ = 2400 R ⇒ u₃ = {N(o4["u3"],2)}, v_r3 = {N(o4["vr3"],3)}. q_in = u₃ − u₂ = {N(o4["qin"],1)} Btu/lbm.\n'
         f'(b) v_r4 = 8·v_r3 = {N(8*o4["vr3"],2)} ⇒ T₄ = {N(o4["T4"],1)} R, u₄ = {N(o4["u4"],2)}; q_out = u₄ − u₁ = {N(o4["qout"],1)}; w_net = {N(o4["wnet"],1)} Btu/lbm; η = {N(o4["eta"],3)} (khí lạnh {N(cold4,3)}).\n'
         f'(c) η_Carnot = 1 − 540/2400 = {N(oc4,3)} (nhiệt độ tuyệt đối R).\nHai đường: bảng A-17E và tích phân số cp(T) (verify_m02.py).',
         f'(The slide has no solution; the statement names no table and gives no P₁: use A-17E (R units); MEP is not asked.)\n'
         f'(a) T₁ = 540 R ⇒ u₁ = {N(o4["u1"],2)} Btu/lbm, v_r1 = {N(A(540,"vr",True),2)}; v_r2 = v_r1/8 ⇒ T₂ = {N(o4["T2"],1)} R, u₂ = {N(o4["u2"],2)}. T₃ = 2400 R ⇒ u₃ = {N(o4["u3"],2)}, v_r3 = {N(o4["vr3"],3)}. q_in = u₃ − u₂ = {N(o4["qin"],1)} Btu/lbm.\n'
         f'(b) v_r4 = 8·v_r3 = {N(8*o4["vr3"],2)} ⇒ T₄ = {N(o4["T4"],1)} R, u₄ = {N(o4["u4"],2)}; q_out = u₄ − u₁ = {N(o4["qout"],1)}; w_net = {N(o4["wnet"],1)} Btu/lbm; η = {N(o4["eta"],3)} (cold air {N(cold4,3)}).\n'
         f'(c) η_Carnot = 1 − 540/2400 = {N(oc4,3)} (absolute temperatures in R).\nTwo routes: Table A-17E and numerical integration of cp(T) (verify_m02.py).'),
       2, T_OTTO, S4, 'script (A-17E)')

    # =========================================================================== Tutorials I #5 (= Cengel 9-47) Diesel r = 16, rc = 2, variable cp; #6 (= Cengel 9-51)
    S5 = srcB('Tutorials I tr.16 (= Cengel Bài 9–47)', 'Tutorials I p.16 (= Cengel Problem 9–47)')
    d5 = diesel_var(16, 300, 95, rc=2); d5c = diesel(16, 300, 95, rc=2)
    for k_ in ('T2', 'T3', 'T4', 'qin', 'qout', 'wnet', 'eta', 'mep'): reg('diesel_v', dict(r=16, rc=2, T1=300, P1=95), k_, d5[k_], 0.012)
    pr('9-47 T3', d5['T3'], 1724.8, 1e-4, 'Cengel 9–47 (ans.)'); pr('9-47 eta', d5['eta'], 0.563, 1e-3, 'Cengel 9–47'); pr('9-47 MEP', d5['mep'], 675.9, 6e-4, 'Cengel 9–47')
    MC(B('Chu trình Diesel khí-chuẩn: r = 16, r_c = 2; đầu nén 95 kPa, 27 °C; tính đến nhiệt dung riêng thay đổi (A-17). Nhiệt độ sau cấp nhiệt T₃ là:', 'Air-standard Diesel cycle: r = 16, r_c = 2; start of compression 95 kPa, 27 °C; accounting for variable specific heats (A-17). The temperature after heat addition T₃ is:'),
       num(d5['T3'], [d5c['T3'], 2 * 300, d5['T2']], 'K', 1), 0,
       B(f'v_r2 = v_r1/16 ⇒ T₂ = {N(d5["T2"],1)} K; 2→3 đẳng áp: T₃ = r_c T₂ = {N(d5["T3"],1)} K (đáp án in 1724,8 K). Khí lạnh (T₂ = 300·16^0,4) cho {N(d5c["T3"],1)} K; r_c·T₁ cho 600 K; {N(d5["T2"],1)} K là T₂.',
         f'v_r2 = v_r1/16 ⇒ T₂ = {N(d5["T2"],1)} K; 2→3 isobaric: T₃ = r_c T₂ = {N(d5["T3"],1)} K (printed answer 1724.8 K). Cold air (T₂ = 300·16^0.4) gives {N(d5c["T3"],1)} K; r_c·T₁ gives 600 K; {N(d5["T2"],1)} K is T₂.'),
       2, T_DIESEL, S5, 'printed answer Cengel 9–47 + script')
    MC(B('Cùng bài (Tutorials I #5): hiệu suất nhiệt của chu trình (nhiệt dung riêng thay đổi) là:', 'Same problem (Tutorials I #5): the thermal efficiency of the cycle (variable specific heats) is:'),
       num(d5['eta'], [d5c['eta'], 1 - 16 ** -0.4, d5['qout'] / d5['qin']], '', 3), 0,
       B(f'q_in = h₃ − h₂ = {N(d5["h3"],1)} − {N(d5["h2"],1)} = {N(d5["qin"],1)} kJ/kg; v_r4 = v_r3·r/r_c ⇒ T₄ = {N(d5["T4"],1)} K, q_out = u₄ − u₁ = {N(d5["qout"],1)} kJ/kg; η = {N(d5["eta"],3)} (đáp án in 56,3 %). Công thức khí lạnh cho {N(d5c["eta"],3)}; công thức Otto cho {N(1-16**-.4,3)}; q_out/q_in = {N(d5["qout"]/d5["qin"],3)}.',
         f'q_in = h₃ − h₂ = {N(d5["h3"],1)} − {N(d5["h2"],1)} = {N(d5["qin"],1)} kJ/kg; v_r4 = v_r3·r/r_c ⇒ T₄ = {N(d5["T4"],1)} K, q_out = u₄ − u₁ = {N(d5["qout"],1)} kJ/kg; η = {N(d5["eta"],3)} (printed answer 56.3 %). The cold-air formula gives {N(d5c["eta"],3)}; the Otto formula gives {N(1-16**-.4,3)}; q_out/q_in = {N(d5["qout"]/d5["qin"],3)}.'),
       3, T_DIESEL, S5, 'printed answer Cengel 9–47 + script')
    ES(B('Tutorials I #5. Chu trình Diesel khí-chuẩn có r = 16, r_c = 2. Đầu nén: 95 kPa, 27 °C. Tính đến nhiệt dung riêng thay đổi, tính (a) nhiệt độ sau cấp nhiệt, (b) hiệu suất nhiệt, (c) MEP.',
         'Tutorials I #5. An air-standard Diesel cycle has r = 16, r_c = 2. Start of compression: 95 kPa, 27 °C. Accounting for variable specific heats, determine (a) the temperature after heat addition, (b) the thermal efficiency, (c) the MEP.'),
       B(f'(Slide không có lời giải; đề không nêu bảng: dùng A-17; 27 °C = 300 K.)\n'
         f'T₁ = 300 K ⇒ u₁ = {N(A(300,"u"),2)} kJ/kg, v_r1 = {N(A(300,"vr"),1)}. 1→2: v_r2 = v_r1/16 ⇒ T₂ = {N(d5["T2"],1)} K, h₂ = {N(d5["h2"],2)} kJ/kg.\n'
         f'2→3 (P = const): T₃ = r_c T₂ = {N(d5["T3"],1)} K ⇒ h₃ = {N(d5["h3"],2)}, v_r3 = {N(A(d5["T3"],"vr"),2)}; q_in = h₃ − h₂ = {N(d5["qin"],1)} kJ/kg.\n'
         f'3→4: v₄/v₃ = r/r_c = 8 ⇒ v_r4 = 8v_r3 = {N(8*A(d5["T3"],"vr"),1)} ⇒ T₄ = {N(d5["T4"],1)} K, u₄ = {N(d5["u4"],2)}; q_out = u₄ − u₁ = {N(d5["qout"],1)} kJ/kg.\n'
         f'(b) w_net = {N(d5["wnet"],1)} kJ/kg; η = {N(d5["eta"],3)}. (c) v₁ = 0,287·300/95 = {N(d5["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/16)] = {N(d5["mep"],1)} kPa.\n'
         'Đáp án in (Cengel 9–47): 1724,8 K; 56,3 %; 675,9 kPa. Khác nhau nhỏ (1724,7; 675,6) do nội suy tuyến tính. Hai đường: A-17 và tích phân số cp(T) (verify_m02.py).',
         f'(The slide has no solution; the statement names no table: use A-17; 27 °C = 300 K.)\n'
         f'T₁ = 300 K ⇒ u₁ = {N(A(300,"u"),2)} kJ/kg, v_r1 = {N(A(300,"vr"),1)}. 1→2: v_r2 = v_r1/16 ⇒ T₂ = {N(d5["T2"],1)} K, h₂ = {N(d5["h2"],2)} kJ/kg.\n'
         f'2→3 (P = const): T₃ = r_c T₂ = {N(d5["T3"],1)} K ⇒ h₃ = {N(d5["h3"],2)}, v_r3 = {N(A(d5["T3"],"vr"),2)}; q_in = h₃ − h₂ = {N(d5["qin"],1)} kJ/kg.\n'
         f'3→4: v₄/v₃ = r/r_c = 8 ⇒ v_r4 = 8v_r3 = {N(8*A(d5["T3"],"vr"),1)} ⇒ T₄ = {N(d5["T4"],1)} K, u₄ = {N(d5["u4"],2)}; q_out = u₄ − u₁ = {N(d5["qout"],1)} kJ/kg.\n'
         f'(b) w_net = {N(d5["wnet"],1)} kJ/kg; η = {N(d5["eta"],3)}. (c) v₁ = 0.287·300/95 = {N(d5["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/16)] = {N(d5["mep"],1)} kPa.\n'
         'Printed answers (Cengel 9–47): 1724.8 K; 56.3 %; 675.9 kPa. Small differences (1724.7; 675.6) come from linear interpolation. Two routes: A-17 and numerical integration of cp(T) (verify_m02.py).'),
       3, T_DIESEL, S5, 'printed answer Cengel 9–47 + script')

    S6 = srcB('Tutorials I tr.17 (= Cengel Bài 9–51)', 'Tutorials I p.17 (= Cengel Problem 9–51)')
    d6 = diesel(20, 293, 95, cp=CP_AIR, cv=CV_AIR, T3=2200); p6 = dict(r=20, T1=293, P1=95, k=1.4, R=0.287, cp=CP_AIR, cv=CV_AIR, T3=2200)
    for k_ in ('T2', 'rc', 'T4', 'qin', 'qout', 'wnet', 'eta', 'mep'): reg('diesel_k', p6, k_, d6[k_], 1e-6)
    pr('9-51 eta', d6['eta'], 0.635, 2e-3, 'Cengel 9–51 (ans.)'); pr('9-51 MEP', d6['mep'], 933, 1e-3, 'Cengel 9–51')
    MC(B('Động cơ Diesel lý tưởng có r = 20, không khí đầu nén ở 95 kPa, 20 °C; nhiệt độ cực đại không quá 2200 K; nhiệt dung riêng hằng (c_p = 1,005; c_v = 0,718 kJ/kg·K). Tỉ số cắt r_c = T₃/T₂ là:', 'An ideal diesel engine has r = 20, the air at the start of compression is at 95 kPa, 20 °C; the maximum temperature must not exceed 2200 K; constant specific heats (c_p = 1.005; c_v = 0.718 kJ/kg·K). The cutoff ratio r_c = T₃/T₂ is:'),
       num(d6['rc'], [2200 / 293, 2200 / (293 * 20), 2200 / (293 * 20 ** 0.4) * 1.4], '', 3), 0,
       B(f'T₂ = 293·20^0,4 = {N(d6["T2"],1)} K; r_c = T₃/T₂ = 2200/{N(d6["T2"],1)} = {N(d6["rc"],3)}. 2200/293 = {N(2200/293,2)} quên nén; 2200/(293·20) = {N(2200/(293*20),3)} lấy T₂ = r·T₁; thêm hệ số k cho {N(2200/(293*20**.4)*1.4,3)}.',
         f'T₂ = 293·20^0.4 = {N(d6["T2"],1)} K; r_c = T₃/T₂ = 2200/{N(d6["T2"],1)} = {N(d6["rc"],3)}. 2200/293 = {N(2200/293,2)} forgets the compression; 2200/(293·20) = {N(2200/(293*20),3)} takes T₂ = r·T₁; an extra factor k gives {N(2200/(293*20**.4)*1.4,3)}.'),
       2, T_DIESEL, S6, 'printed answer Cengel 9–51 + script')
    MC(B('Cùng bài (Tutorials I #6): hiệu suất nhiệt và MEP lần lượt là:', 'Same problem (Tutorials I #6): the thermal efficiency and the MEP are, respectively:'),
       [B(f'{N(d6["eta"],4)} và {N(d6["mep"],1)} kPa', f'{N(d6["eta"],4)} and {N(d6["mep"],1)} kPa'), B(f'{N(1-20**-.4,4)} và {N(d6["mep"],1)} kPa', f'{N(1-20**-.4,4)} and {N(d6["mep"],1)} kPa'),
        B(f'{N(d6["eta"],4)} và {N(d6["wnet"]/d6["v1"],1)} kPa', f'{N(d6["eta"],4)} and {N(d6["wnet"]/d6["v1"],1)} kPa'), B(f'{N(1-20**-.4*(d6["rc"]**1.4-1)/(d6["rc"]-1),4)} và {N(d6["mep"],1)} kPa', f'{N(1-20**-.4*(d6["rc"]**1.4-1)/(d6["rc"]-1),4)} and {N(d6["mep"],1)} kPa')], 0,
       B(f'η = 1 − r^(1−k)(r_c^k − 1)/[k(r_c − 1)] = 1 − 20^(−0,4)({N(d6["rc"]**1.4,3)} − 1)/(1,4·{N(d6["rc"]-1,3)}) = {N(d6["eta"],4)}; q_in = {N(d6["qin"],1)}, q_out = {N(d6["qout"],1)}, w_net = {N(d6["wnet"],1)} kJ/kg; v₁ = {N(d6["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/20)] = {N(d6["mep"],1)} kPa. Công thức Otto cho {N(1-20**-.4,4)}; chia w_net cho v₁ cho {N(d6["wnet"]/d6["v1"],1)} kPa; quên k trong ngoặc cho {N(1-20**-.4*(d6["rc"]**1.4-1)/(d6["rc"]-1),4)}.',
         f'η = 1 − r^(1−k)(r_c^k − 1)/[k(r_c − 1)] = 1 − 20^(−0.4)({N(d6["rc"]**1.4,3)} − 1)/(1.4·{N(d6["rc"]-1,3)}) = {N(d6["eta"],4)}; q_in = {N(d6["qin"],1)}, q_out = {N(d6["qout"],1)}, w_net = {N(d6["wnet"],1)} kJ/kg; v₁ = {N(d6["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/20)] = {N(d6["mep"],1)} kPa. The Otto formula gives {N(1-20**-.4,4)}; dividing w_net by v₁ gives {N(d6["wnet"]/d6["v1"],1)} kPa; forgetting k in the bracket gives {N(1-20**-.4*(d6["rc"]**1.4-1)/(d6["rc"]-1),4)}.'),
       3, T_DIESEL, S6, 'printed answer Cengel 9–51 + script', fig=None)
    ES(B('Tutorials I #6. Động cơ Diesel lý tưởng có r = 20, không khí. Đầu nén: 95 kPa, 20 °C. Nhiệt độ cực đại không vượt quá 2200 K. Giả thiết nhiệt dung riêng hằng ở nhiệt độ phòng. Tính (a) hiệu suất nhiệt, (b) MEP.',
         'Tutorials I #6. An ideal diesel engine has r = 20 and uses air. Start of compression: 95 kPa, 20 °C. The maximum temperature must not exceed 2200 K. Assume constant specific heats at room temperature. Determine (a) the thermal efficiency, (b) the MEP.'),
       B(f'(Slide không có lời giải; đề không in c_p, c_v, R, k: A-2a (c_p = 1,005; c_v = 0,718; R = 0,287; k = 1,4); 20 °C = 293 K.)\n'
         f'T₂ = 293·20^0,4 = {N(d6["T2"],1)} K; T₃ = 2200 K ⇒ r_c = T₃/T₂ = {N(d6["rc"],3)}. T₄ = T₃(r_c/r)^(k−1) = {N(d6["T4"],1)} K.\n'
         f'q_in = c_p(T₃ − T₂) = {N(d6["qin"],1)} kJ/kg; q_out = c_v(T₄ − T₁) = {N(d6["qout"],1)} kJ/kg; w_net = {N(d6["wnet"],1)} kJ/kg. (a) η = {N(d6["eta"],4)} (kiểm bằng công thức r_c: {N(d6["eta_formula"],4)}).\n'
         f'(b) v₁ = 0,287·293/95 = {N(d6["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(d6["mep"],1)} kPa.\nĐáp án in (Cengel 9–51): 63,5 %; 933 kPa. Hai đường: công thức đóng và tích phân số ∮P dV (verify_m02.py).',
         f'(The slide has no solution; the statement prints no c_p, c_v, R, k: A-2a (c_p = 1.005; c_v = 0.718; R = 0.287; k = 1.4); 20 °C = 293 K.)\n'
         f'T₂ = 293·20^0.4 = {N(d6["T2"],1)} K; T₃ = 2200 K ⇒ r_c = T₃/T₂ = {N(d6["rc"],3)}. T₄ = T₃(r_c/r)^(k−1) = {N(d6["T4"],1)} K.\n'
         f'q_in = c_p(T₃ − T₂) = {N(d6["qin"],1)} kJ/kg; q_out = c_v(T₄ − T₁) = {N(d6["qout"],1)} kJ/kg; w_net = {N(d6["wnet"],1)} kJ/kg. (a) η = {N(d6["eta"],4)} (check with the r_c formula: {N(d6["eta_formula"],4)}).\n'
         f'(b) v₁ = 0.287·293/95 = {N(d6["v1"],4)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(d6["mep"],1)} kPa.\nPrinted answers (Cengel 9–51): 63.5 %; 933 kPa. Two routes: closed forms and numerical ∮P dV integration (verify_m02.py).'),
       3, T_DIESEL, S6, 'printed answer Cengel 9–51 + script')
    return ITEMS, PRINTED
