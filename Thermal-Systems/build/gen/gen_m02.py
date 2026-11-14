"""m02 generator: writes data/qsrc/m02.json (originals + conceptual slide questions), data/qsrc/m02_gen.json (generated variants, fixed seed),
data/verify/m02_values.json (registry of every numeric answer + printed answers, recomputed by build/verify/verify_m02.py through a different route).
Run:  .venv/bin/python -I build/gen/gen_m02.py"""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from m02_common import *
import gen_m02_orig as O1, gen_m02_orig2 as O2, gen_m02_orig3 as O3, gen_m02_concept as CO

rng = random.Random(20261115)
GEN = lambda vi, en: B(f'Bổ sung – sinh theo dạng {vi}', f'Added – generated from the type: {en}')
TOP = dict(carnot=B('Chu trình Carnot', 'The Carnot cycle'), otto=B('Chu trình Otto', 'The Otto cycle'), diesel=B('Chu trình Diesel', 'The Diesel cycle'), bray=B('Chu trình Brayton đơn giản', 'The simple Brayton cycle'),
           real=B('Brayton thực: hiệu suất máy nén và tuabin', 'Real Brayton cycle: compressor and turbine efficiency'), regen=B('Hồi nhiệt (regeneration)', 'Regeneration'), multi=B('Làm mát trung gian và hâm nóng', 'Intercooling and reheating'),
           jet=B('Chu trình phản lực lý tưởng', 'Ideal jet-propulsion cycle'), eng=B('Động cơ piston: r, MEP', 'Reciprocating engines: r, MEP'), table=B('Bảng A-17 (nhiệt dung riêng thay đổi)', 'Table A-17 (variable specific heats)'))
G = []
def add(it): G.append(it)
def M(q, correct, wrongs, unit, nd, expl, lvl, topic, src, check='script (verify_m02: formula/model)'):
    add(mcq(q, numopts(correct, wrongs, unit, nd), 0, expl, lvl, TOP[topic], src, 'bo_sung', check))
def Tf(q, truth, expl, lvl, topic, src, check='formula + script'): add(tf(q, truth, expl, lvl, TOP[topic], src, 'bo_sung', check))
def F(name, params, out, value, tol=1e-9): reg('formula', dict(params, name=name), out, value, tol)
def pick(seq): return rng.choice(seq)

# ================================================================ Carnot
for TLc, THc in ((27, 727), (-23, 477)):
    TL, TH = TLc + 273.15, THc + 273.15; eta = 1 - TL / TH; F('carnot', dict(TL=TL, TH=TH), 'eta', eta)
    M(B(f'Chu trình Carnot hoạt động giữa nguồn nóng {THc} °C và nguồn lạnh {TLc} °C. Hiệu suất nhiệt là:', f'A Carnot cycle operates between a {THc} °C source and a {TLc} °C sink. The thermal efficiency is:'),
      eta, [1 - TLc / THc if THc else 0, 1 - TL / (TH + 273.15), TL / TH], '', 3,
      B(f'Phải đổi sang kelvin: η = 1 − T_L/T_H = 1 − {N(TL,2)}/{N(TH,2)} = {N(eta,3)}. Dùng °C trực tiếp cho {N(1-TLc/THc,3)}; cộng 273,15 hai lần cho {N(1-TL/(TH+273.15),3)}; T_L/T_H = {N(TL/TH,3)} là tỉ số nhiệt chứ không phải hiệu suất.',
        f'Convert to kelvin: η = 1 − T_L/T_H = 1 − {N(TL,2)}/{N(TH,2)} = {N(eta,3)}. Using °C directly gives {N(1-TLc/THc,3)}; adding 273.15 twice gives {N(1-TL/(TH+273.15),3)}; T_L/T_H = {N(TL/TH,3)} is the temperature ratio, not the efficiency.'), 1, 'carnot', GEN('hiệu suất Carnot', 'Carnot efficiency'))
TL, eta = 300.0, 0.6; TH = TL / (1 - eta); F('carnot_TH', dict(TL=TL, eta=eta), 'TH', TH)
M(B('Một động cơ nhiệt thuận nghịch có hiệu suất 60 % thải nhiệt ở 300 K. Nhiệt độ nguồn nóng tối thiểu (K) là:', 'A reversible heat engine of 60 % efficiency rejects heat at 300 K. The minimum source temperature (K) is:'),
  TH, [TL * (1 + eta), TL / eta, TL * (1 - eta)], 'K', 0,
  B(f'η = 1 − T_L/T_H ⇒ T_H = T_L/(1 − η) = 300/0,4 = {N(TH,0)} K. T_L(1 + η) = {N(TL*(1+eta),0)}; T_L/η = {N(TL/eta,0)}; T_L(1 − η) = {N(TL*(1-eta),0)} đều là nhầm biến đổi.',
    f'η = 1 − T_L/T_H ⇒ T_H = T_L/(1 − η) = 300/0.4 = {N(TH,0)} K. T_L(1 + η) = {N(TL*(1+eta),0)}; T_L/η = {N(TL/eta,0)}; T_L(1 − η) = {N(TL*(1-eta),0)} are algebra slips.'), 2, 'carnot', GEN('hiệu suất Carnot ngược', 'inverse Carnot efficiency'))

# ================================================================ Otto: efficiency, r from efficiency, full cycle (constant specific heats)
for r in (7, 11):
    k = 1.4; eta = 1 - r ** (1 - k); F('otto_eta', dict(r=r, k=k), 'eta', eta)
    M(B(f'Chu trình Otto khí lạnh-chuẩn có tỉ số nén r = {r}, k = 1,4. Hiệu suất nhiệt là:', f'A cold-air-standard Otto cycle has compression ratio r = {r}, k = 1.4. The thermal efficiency is:'),
      eta, [1 - 1 / r, 1 - r ** (-(k - 1) / k), r ** (1 - k)], '', 3,
      B(f'η = 1 − 1/r^(k−1) = 1 − {r}^(−0,4) = {N(eta,3)}. 1 − 1/r = {N(1-1/r,3)} quên số mũ; số mũ (k−1)/k (của Brayton) cho {N(1-r**(-(k-1)/k),3)}; r^(1−k) = {N(r**(1-k),3)} là 1 − η.',
        f'η = 1 − 1/r^(k−1) = 1 − {r}^(−0.4) = {N(eta,3)}. 1 − 1/r = {N(1-1/r,3)} forgets the exponent; the exponent (k−1)/k (Brayton\'s) gives {N(1-r**(-(k-1)/k),3)}; r^(1−k) = {N(r**(1-k),3)} is 1 − η.'), 1, 'otto', GEN('hiệu suất Otto', 'Otto efficiency'))
for eta_t in (0.55, 0.62):
    k = 1.4; r = (1 - eta_t) ** (-1 / (k - 1)); F('otto_r', dict(eta=eta_t, k=k), 'r', r)
    M(B(f'Một động cơ xăng lý tưởng (Otto, k = 1,4) cần hiệu suất nhiệt {int(eta_t*100)} %. Tỉ số nén cần có là:', f'An ideal gasoline engine (Otto, k = 1.4) needs a thermal efficiency of {int(eta_t*100)} %. The required compression ratio is:'),
      r, [1 / (1 - eta_t), (1 - eta_t) ** (-1 / k), (1 - eta_t) ** (-(1.4) / 0.4)], '', 2,
      B(f'1 − η = r^(1−k) ⇒ r = (1 − η)^(−1/(k−1)) = {N(1-eta_t,2)}^(−2,5) = {N(r,2)}. 1/(1 − η) = {N(1/(1-eta_t),2)} quên số mũ; số mũ −1/k cho {N((1-eta_t)**(-1/1.4),2)}; số mũ −k/(k−1) cho {N((1-eta_t)**(-3.5),2)}.',
        f'1 − η = r^(1−k) ⇒ r = (1 − η)^(−1/(k−1)) = {N(1-eta_t,2)}^(−2.5) = {N(r,2)}. 1/(1 − η) = {N(1/(1-eta_t),2)} forgets the exponent; exponent −1/k gives {N((1-eta_t)**(-1/1.4),2)}; exponent −k/(k−1) gives {N((1-eta_t)**(-3.5),2)}.'), 2, 'otto', GEN('tỉ số nén từ hiệu suất Otto', 'compression ratio from Otto efficiency'))
for (r, T1c, P1, q) in ((9, 20, 100, 1000), (10, 25, 95, 1200), (8.5, 15, 101, 900), (9.5, 30, 100, 1100)):
    T1 = T1c + 273.15; p = dict(r=r, T1=T1, P1=P1, k=1.4, R=0.287, cv=CV_AIR, qin=q); o = otto(r, T1, P1, qin=q)
    for k_ in ('T2', 'T3', 'T4', 'P3', 'qout', 'wnet', 'eta', 'mep'): reg('otto_k', p, k_, o[k_], 1e-6)
    if r in (9, 8.5):
        M(B(f'Chu trình Otto khí lạnh-chuẩn (k = 1,4; c_v = 0,718 kJ/kg·K): r = {r}, đầu nén {P1} kPa, {T1c} °C, nhiệt cấp đẳng tích {q} kJ/kg. Nhiệt độ cực đại T₃ (K) là:', f'Cold-air-standard Otto cycle (k = 1.4; c_v = 0.718 kJ/kg·K): r = {r}, start of compression {P1} kPa, {T1c} °C, heat added at constant volume {q} kJ/kg. The maximum temperature T₃ (K) is:'),
          o['T3'], [T1 + q / CV_AIR, o['T3'] - 273.15, o['T2'] + q / CP_AIR], 'K', 0,
          B(f'T₂ = T₁r^(k−1) = {N(T1,2)}·{r}^0,4 = {N(o["T2"],1)} K; T₃ = T₂ + q_in/c_v = {N(o["T2"],1)} + {q}/0,718 = {N(o["T3"],0)} K. Bỏ bước nén cho {N(T1+q/CV_AIR,0)}; {N(o["T3"]-273.15,0)} là °C; dùng c_p thay c_v cho {N(o["T2"]+q/CP_AIR,0)}.',
            f'T₂ = T₁r^(k−1) = {N(T1,2)}·{r}^0.4 = {N(o["T2"],1)} K; T₃ = T₂ + q_in/c_v = {N(o["T2"],1)} + {q}/0.718 = {N(o["T3"],0)} K. Skipping the compression gives {N(T1+q/CV_AIR,0)}; {N(o["T3"]-273.15,0)} is in °C; using c_p instead of c_v gives {N(o["T2"]+q/CP_AIR,0)}.'), 2, 'otto', GEN('Otto khí lạnh: T₃', 'cold-air Otto: T₃'))
    else:
        M(B(f'Chu trình Otto khí lạnh-chuẩn (k = 1,4; c_v = 0,718; R = 0,287): r = {r}, đầu nén {P1} kPa, {T1c} °C, nhiệt cấp {q} kJ/kg. Áp suất cực đại P₃ (kPa) là:', f'Cold-air-standard Otto cycle (k = 1.4; c_v = 0.718; R = 0.287): r = {r}, start of compression {P1} kPa, {T1c} °C, heat added {q} kJ/kg. The maximum pressure P₃ (kPa) is:'),
          o['P3'], [o['P2'] if 'P2' in o else P1 * r ** 1.4, P1 * r * (o['T3'] / T1) * 1.0 * 0 + P1 * r * o['T3'] / (T1 + 273.15), P1 * r ** 1.4 * (o['T3'] / o['T2']) / r], 'kPa', 0,
          B(f'T₂ = {N(o["T2"],1)} K, P₂ = P₁r^k = {N(P1*r**1.4,0)} kPa; T₃ = T₂ + q/c_v = {N(o["T3"],0)} K; đẳng tích nên P₃ = P₂T₃/T₂ = {N(o["P3"],0)} kPa. {N(P1*r**1.4,0)} là P₂ (trước cấp nhiệt); chia thêm cho r cho {N(P1*r**1.4*(o["T3"]/o["T2"])/r,0)}; dùng T₁ theo °C+273 cho {N(P1*r*o["T3"]/(T1+273.15),0)}.',
            f'T₂ = {N(o["T2"],1)} K, P₂ = P₁r^k = {N(P1*r**1.4,0)} kPa; T₃ = T₂ + q/c_v = {N(o["T3"],0)} K; constant volume so P₃ = P₂T₃/T₂ = {N(o["P3"],0)} kPa. {N(P1*r**1.4,0)} is P₂ (before heat addition); dividing again by r gives {N(P1*r**1.4*(o["T3"]/o["T2"])/r,0)}; adding 273 twice in T₁ gives {N(P1*r*o["T3"]/(T1+273.15),0)}.'), 2, 'otto', GEN('Otto khí lạnh: P₃', 'cold-air Otto: P₃'))
for (r, T1c, P1, q) in ((9, 20, 100, 1000), (10, 25, 95, 1200)):
    T1 = T1c + 273.15; o = otto(r, T1, P1, qin=q)
    v1 = o['v1']
    opts = [B(f'{N(o["wnet"],0)} kJ/kg; {N(o["mep"],0)} kPa', f'{N(o["wnet"],0)} kJ/kg; {N(o["mep"],0)} kPa'), B(f'{N(o["wnet"],0)} kJ/kg; {N(o["wnet"]/v1,0)} kPa', f'{N(o["wnet"],0)} kJ/kg; {N(o["wnet"]/v1,0)} kPa'),
            B(f'{N(o["qout"],0)} kJ/kg; {N(o["qout"]/(v1*(1-1/r)),0)} kPa', f'{N(o["qout"],0)} kJ/kg; {N(o["qout"]/(v1*(1-1/r)),0)} kPa'), B(f'{N(q*(1-r**-.4),0)} kJ/kg; {N(q*(1-r**-.4)/(v1*(1-1/r)),0)} kPa', f'{N(q*(1-r**-.4),0)} kJ/kg; {N(q*(1-r**-.4)/(v1*(1-1/r)),0)} kPa')]
    if len({x['en'] for x in opts}) == 4:
        add(mcq(B(f'Chu trình Otto khí lạnh-chuẩn (k = 1,4; c_v = 0,718; R = 0,287): r = {r}, {P1} kPa, {T1c} °C, q_in = {q} kJ/kg. Công thực riêng w_net và MEP lần lượt là:', f'Cold-air-standard Otto cycle (k = 1.4; c_v = 0.718; R = 0.287): r = {r}, {P1} kPa, {T1c} °C, q_in = {q} kJ/kg. The net work per kg and the MEP are, respectively:'), opts, 0,
                B(f'T₂ = {N(o["T2"],1)}, T₃ = {N(o["T3"],0)}, T₄ = {N(o["T4"],0)} K; q_out = c_v(T₄ − T₁) = {N(o["qout"],0)}; w_net = q_in − q_out = {N(o["wnet"],0)} kJ/kg. v₁ = RT₁/P₁ = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o["mep"],0)} kPa. Chia cho v₁ (quên v₂) cho {N(o["wnet"]/v1,0)} kPa; lấy q_out làm công thực cho {N(o["qout"],0)} kJ/kg; η khí lạnh × q_in cho {N(q*(1-r**-.4),0)} kJ/kg (lệch vì cv, k làm tròn).',
                  f'T₂ = {N(o["T2"],1)}, T₃ = {N(o["T3"],0)}, T₄ = {N(o["T4"],0)} K; q_out = c_v(T₄ − T₁) = {N(o["qout"],0)}; w_net = q_in − q_out = {N(o["wnet"],0)} kJ/kg. v₁ = RT₁/P₁ = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(o["mep"],0)} kPa. Dividing by v₁ (forgetting v₂) gives {N(o["wnet"]/v1,0)} kPa; taking q_out as the net work gives {N(o["qout"],0)} kJ/kg; cold-air η × q_in gives {N(q*(1-r**-.4),0)} kJ/kg (slightly off because c_v and k are rounded).'), 3, TOP['otto'], GEN('Otto khí lạnh: w_net và MEP', 'cold-air Otto: w_net and MEP'), 'bo_sung', 'script (verify_m02: otto_k)'))
# ================================================================ Diesel
for (r, rc) in ((16, 2.0), (18, 2.5), (20, 1.8)):
    k = 1.4; eta = 1 - r ** (1 - k) * (rc ** k - 1) / (k * (rc - 1)); F('diesel_eta', dict(r=r, rc=rc, k=k), 'eta', eta)
    M(B(f'Chu trình Diesel khí lạnh-chuẩn (k = 1,4) có tỉ số nén r = {r} và tỉ số cắt r_c = {rc}. Hiệu suất nhiệt là:', f'A cold-air-standard Diesel cycle (k = 1.4) has compression ratio r = {r} and cutoff ratio r_c = {rc}. The thermal efficiency is:'),
      eta, [1 - r ** (1 - k), 1 - r ** (1 - k) * (rc ** k - 1) / (rc - 1), 1 - r ** (1 - k) * (rc ** k - 1) / (k * rc)], '', 3,
      B(f'η = 1 − r^(1−k)(r_c^k − 1)/[k(r_c − 1)] = 1 − {r}^(−0,4)·({N(rc**k,3)} − 1)/(1,4·{N(rc-1,2)}) = {N(eta,3)}. Công thức Otto cho {N(1-r**(1-k),3)} (cao hơn); quên k trong ngoặc cho {N(1-r**(1-k)*(rc**k-1)/(rc-1),3)}; mẫu số k·r_c thay k(r_c − 1) cho {N(1-r**(1-k)*(rc**k-1)/(k*rc),3)}.',
        f'η = 1 − r^(1−k)(r_c^k − 1)/[k(r_c − 1)] = 1 − {r}^(−0.4)·({N(rc**k,3)} − 1)/(1.4·{N(rc-1,2)}) = {N(eta,3)}. The Otto formula gives {N(1-r**(1-k),3)} (too high); forgetting k in the bracket gives {N(1-r**(1-k)*(rc**k-1)/(rc-1),3)}; the denominator k·r_c instead of k(r_c − 1) gives {N(1-r**(1-k)*(rc**k-1)/(k*rc),3)}.'), 2, 'diesel', GEN('hiệu suất Diesel', 'Diesel efficiency'))
for (r, T1c, P1, rc) in ((18, 27, 100, 2.2), (16, 40, 95, 2.0), (20, 20, 100, 1.9)):
    T1 = T1c + 273.15; p = dict(r=r, T1=T1, P1=P1, k=1.4, R=0.287, cp=CP_AIR, cv=CV_AIR, rc=rc); d = diesel(r, T1, P1, cp=CP_AIR, cv=CV_AIR, rc=rc)
    for k_ in ('T2', 'T3', 'T4', 'P2', 'qin', 'qout', 'wnet', 'eta', 'mep'): reg('diesel_k', p, k_, d[k_], 1e-6)
    if r != 20:
        M(B(f'Chu trình Diesel khí lạnh-chuẩn (k = 1,4; c_p = 1,005; c_v = 0,718): r = {r}, đầu nén {P1} kPa và {T1c} °C, r_c = {rc}. Nhiệt độ cuối quá trình giãn đẳng entropi T₄ (K) là:', f'Cold-air-standard Diesel cycle (k = 1.4; c_p = 1.005; c_v = 0.718): r = {r}, start of compression {P1} kPa and {T1c} °C, r_c = {rc}. The temperature at the end of isentropic expansion T₄ (K) is:'),
          d['T4'], [d['T3'] * r ** -0.4, d['T3'] / rc ** 0.4, d['T3'] * (rc / r) ** (0.4 / 1.4)], 'K', 0,
          B(f'T₂ = {N(d["T2"],0)} K; T₃ = r_cT₂ = {N(d["T3"],0)} K; V₃/V₄ = r_c/r ⇒ T₄ = T₃(r_c/r)^0,4 = {N(d["T4"],0)} K. Dùng V₃/V₄ = 1/r (quên r_c) cho {N(d["T3"]*r**-0.4,0)} K; T₃/r_c^0,4 = {N(d["T3"]/rc**0.4,0)} K (chia nhầm cho r_c thay vì nhân r_c/r); số mũ (k−1)/k thay k−1 cho {N(d["T3"]*(rc/r)**(0.4/1.4),0)} K.',
            f'T₂ = {N(d["T2"],0)} K; T₃ = r_cT₂ = {N(d["T3"],0)} K; V₃/V₄ = r_c/r ⇒ T₄ = T₃(r_c/r)^0.4 = {N(d["T4"],0)} K. Using V₃/V₄ = 1/r (forgetting r_c) gives {N(d["T3"]*r**-0.4,0)} K; T₃/r_c^0.4 = {N(d["T3"]/rc**0.4,0)} K (dividing by r_c instead of using r_c/r); the exponent (k−1)/k instead of k−1 gives {N(d["T3"]*(rc/r)**(0.4/1.4),0)} K.'), 2, 'diesel', GEN('Diesel khí lạnh: T₄', 'cold-air Diesel: T₄'))
    else:
        v1 = d['v1']
        M(B(f'Chu trình Diesel khí lạnh-chuẩn (k = 1,4; c_p = 1,005; c_v = 0,718; R = 0,287): r = {r}, {P1} kPa và {T1c} °C, r_c = {rc}. MEP (kPa) là:', f'Cold-air-standard Diesel cycle (k = 1.4; c_p = 1.005; c_v = 0.718; R = 0.287): r = {r}, {P1} kPa and {T1c} °C, r_c = {rc}. The MEP (kPa) is:'),
          d['mep'], [d['wnet'] / v1, d['qin'] / (v1 * (1 - 1 / r)), d['wnet'] / (v1 * (rc - 1))], 'kPa', 0,
          B(f'T₂ = {N(d["T2"],0)}, T₃ = {N(d["T3"],0)}, T₄ = {N(d["T4"],0)} K; q_in = c_p(T₃ − T₂) = {N(d["qin"],0)}, q_out = c_v(T₄ − T₁) = {N(d["qout"],0)}, w_net = {N(d["wnet"],0)} kJ/kg; v₁ = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(d["mep"],0)} kPa. Chia w_net cho v₁ cho {N(d["wnet"]/v1,0)}; dùng q_in thay w_net cho {N(d["qin"]/(v1*(1-1/r)),0)}; v₁(r_c − 1) thay v₁(1 − 1/r) cho {N(d["wnet"]/(v1*(rc-1)),0)}.',
            f'T₂ = {N(d["T2"],0)}, T₃ = {N(d["T3"],0)}, T₄ = {N(d["T4"],0)} K; q_in = c_p(T₃ − T₂) = {N(d["qin"],0)}, q_out = c_v(T₄ − T₁) = {N(d["qout"],0)}, w_net = {N(d["wnet"],0)} kJ/kg; v₁ = {N(v1,3)} m³/kg; MEP = w_net/[v₁(1 − 1/r)] = {N(d["mep"],0)} kPa. Dividing w_net by v₁ gives {N(d["wnet"]/v1,0)}; using q_in instead of w_net gives {N(d["qin"]/(v1*(1-1/r)),0)}; v₁(r_c − 1) instead of v₁(1 − 1/r) gives {N(d["wnet"]/(v1*(rc-1)),0)}.'), 3, 'diesel', GEN('Diesel khí lạnh: MEP', 'cold-air Diesel: MEP'))
r, rc = 16, 2.0; eo = 1 - r ** -0.4; ed = 1 - r ** -0.4 * (rc ** 1.4 - 1) / (1.4 * (rc - 1)); F('diesel_eta', dict(r=r, rc=rc, k=1.4), 'eta', ed); F('otto_eta', dict(r=r, k=1.4), 'eta', eo)
M(B('Với cùng tỉ số nén r = 16 và khí lạnh (k = 1,4), hiệu suất Otto lớn hơn hiệu suất Diesel (r_c = 2) bao nhiêu điểm phần trăm?', 'At the same compression ratio r = 16 and cold air (k = 1.4), by how many percentage points does the Otto efficiency exceed the Diesel efficiency (r_c = 2)?'),
  (eo - ed) * 100, [(1 - ed) * 100, ed * 100, (eo - ed) * 100 * 2], '', 2,
  B(f'η_Otto = 1 − 16^(−0,4) = {N(eo,4)}; η_Diesel = {N(ed,4)} ⇒ chênh {N((eo-ed)*100,2)} điểm %. Đây là hệ quả của đại lượng trong ngoặc > 1 (slide tr.31). {N((1-ed)*100,2)} là phần nhiệt thải của Diesel; {N(ed*100,2)} là chính η_Diesel.',
    f'η_Otto = 1 − 16^(−0.4) = {N(eo,4)}; η_Diesel = {N(ed,4)} ⇒ gap {N((eo-ed)*100,2)} percentage points. It follows from the bracket being > 1 (slide p.31). {N((1-ed)*100,2)} is the Diesel heat-rejection share; {N(ed*100,2)} is η_Diesel itself.'), 2, 'diesel', GEN('so sánh Otto và Diesel', 'Otto versus Diesel comparison'))

# ================================================================ Brayton, constant cp
for (rp, T1c, T3) in ((10, 27, 1200), (8, 15, 1100), (12, 30, 1300), (16, 20, 1400)):
    T1 = T1c + 273.15; p = dict(rp=rp, T1=T1, T3=T3, k=1.4, cp=CP_AIR, etac=1.0, etat=1.0, eps=0.0); b = brayton(rp, T1, T3)
    for k_ in ('T2', 'T4', 'wc', 'wt', 'wnet', 'qin', 'bwr', 'eta'): reg('brayton_k', p, k_, b[k_], 1e-6)
    x = rp ** (.4 / 1.4)
    if rp == 10:
        opts = [B(f'{N(b["T2"],0)} K; {N(b["T4"],0)} K', f'{N(b["T2"],0)} K; {N(b["T4"],0)} K'), B(f'{N(T1*rp,0)} K; {N(T3/rp,0)} K', f'{N(T1*rp,0)} K; {N(T3/rp,0)} K'), B(f'{N(T1*rp**.4,0)} K; {N(T3/rp**.4,0)} K', f'{N(T1*rp**.4,0)} K; {N(T3/rp**.4,0)} K'), B(f'{N(b["T4"],0)} K; {N(b["T2"],0)} K', f'{N(b["T4"],0)} K; {N(b["T2"],0)} K')]
        add(mcq(B(f'Chu trình Brayton đơn giản khí lạnh (k = 1,4): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. Nhiệt độ ra máy nén T₂ và ra tuabin T₄ lần lượt là:', f'Simple cold-air Brayton cycle (k = 1.4): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. The compressor-exit T₂ and turbine-exit T₄ temperatures are, respectively:'), opts, 0,
                B(f'x = r_p^((k−1)/k) = {rp}^0,2857 = {N(x,4)}; T₂ = T₁x = {N(b["T2"],0)} K; T₄ = T₃/x = {N(b["T4"],0)} K. T₁r_p và T₃/r_p quên số mũ; số mũ k−1 = 0,4 cho {N(T1*rp**.4,0)} K và {N(T3/rp**.4,0)} K; cặp có {N(b["T4"],0)} K đứng trước đảo vị trí hai trạng thái.',
                  f'x = r_p^((k−1)/k) = {rp}^0.2857 = {N(x,4)}; T₂ = T₁x = {N(b["T2"],0)} K; T₄ = T₃/x = {N(b["T4"],0)} K. T₁r_p and T₃/r_p forget the exponent; the exponent k−1 = 0.4 gives {N(T1*rp**.4,0)} K and {N(T3/rp**.4,0)} K; the pair starting with {N(b["T4"],0)} K swaps the two states.'), 2, TOP['bray'], GEN('Brayton khí lạnh: T₂, T₄', 'cold-air Brayton: T₂, T₄'), 'bo_sung', 'script (verify_m02: brayton_k)'))
    elif rp == 8:
        M(B(f'Chu trình Brayton đơn giản khí lạnh (k = 1,4): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. Tỉ số công hồi r_bw = w_comp/w_turb là:', f'Simple cold-air Brayton cycle (k = 1.4): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. The back work ratio r_bw = w_comp/w_turb is:'),
          b['bwr'], [1 - b['bwr'], b['wc'] / b['qin'], T1 / T3], '', 3,
          B(f'Khí lạnh: w_comp = c_pT₁(x − 1) = {N(b["wc"],1)}, w_turb = c_pT₃(1 − 1/x) = {N(b["wt"],1)} ⇒ r_bw = T₁x/T₃ = {N(b["bwr"],3)}. {N(1-b["bwr"],3)} là phần công tuabin còn lại; w_comp/q_in = {N(b["wc"]/b["qin"],3)}; T₁/T₃ = {N(T1/T3,3)} bỏ thừa số x.',
            f'Cold air: w_comp = c_pT₁(x − 1) = {N(b["wc"],1)}, w_turb = c_pT₃(1 − 1/x) = {N(b["wt"],1)} ⇒ r_bw = T₁x/T₃ = {N(b["bwr"],3)}. {N(1-b["bwr"],3)} is the remaining share of the turbine work; w_comp/q_in = {N(b["wc"]/b["qin"],3)}; T₁/T₃ = {N(T1/T3,3)} drops the factor x.'), 2, 'bray', GEN('Brayton khí lạnh: tỉ số công hồi', 'cold-air Brayton: back work ratio'))
    elif rp == 12:
        opts = [B(f'{N(b["wnet"],0)} kJ/kg; {N(b["eta"],3)}', f'{N(b["wnet"],0)} kJ/kg; {N(b["eta"],3)}'), B(f'{N(b["wt"],0)} kJ/kg; {N(b["eta"],3)}', f'{N(b["wt"],0)} kJ/kg; {N(b["eta"],3)}'), B(f'{N(b["wnet"],0)} kJ/kg; {N(1-T1/T3,3)}', f'{N(b["wnet"],0)} kJ/kg; {N(1-T1/T3,3)}'), B(f'{N(b["wc"],0)} kJ/kg; {N(b["eta"],3)}', f'{N(b["wc"],0)} kJ/kg; {N(b["eta"],3)}')]
        add(mcq(B(f'Chu trình Brayton đơn giản khí lạnh (k = 1,4; c_p = 1,005): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. Công thực riêng w_net và hiệu suất lần lượt là:', f'Simple cold-air Brayton cycle (k = 1.4; c_p = 1.005): r_p = {rp}, T₁ = {T1c} °C, T₃ = {T3} K. The net work per kg and the efficiency are, respectively:'), opts, 0,
                B(f'T₂ = {N(b["T2"],0)} K, T₄ = {N(b["T4"],0)} K; w_comp = {N(b["wc"],0)}, w_turb = {N(b["wt"],0)} ⇒ w_net = {N(b["wnet"],0)} kJ/kg; q_in = c_p(T₃ − T₂) = {N(b["qin"],0)} ⇒ η = {N(b["eta"],3)} (= 1 − 1/x). w_turb ({N(b["wt"],0)}) và w_comp ({N(b["wc"],0)}) là công của từng máy chứ không phải công thực; {N(1-T1/T3,3)} là hiệu suất Carnot.',
                  f'T₂ = {N(b["T2"],0)} K, T₄ = {N(b["T4"],0)} K; w_comp = {N(b["wc"],0)}, w_turb = {N(b["wt"],0)} ⇒ w_net = {N(b["wnet"],0)} kJ/kg; q_in = c_p(T₃ − T₂) = {N(b["qin"],0)} ⇒ η = {N(b["eta"],3)} (= 1 − 1/x). w_turb ({N(b["wt"],0)}) and w_comp ({N(b["wc"],0)}) are the work of single machines, not the net work; {N(1-T1/T3,3)} is the Carnot efficiency.'), 3, TOP['bray'], GEN('Brayton khí lạnh: w_net, η', 'cold-air Brayton: w_net, η'), 'bo_sung', 'script (verify_m02: brayton_k)'))
    else:
        M(B(f'Chu trình Brayton đơn giản khí lạnh (k = 1,4): r_p = {rp}. Hiệu suất nhiệt là:', f'Simple cold-air Brayton cycle (k = 1.4): r_p = {rp}. The thermal efficiency is:'),
          b['eta'], [1 - 1 / rp, 1 - 1 / rp ** 0.4, 1 - T1 / T3], '', 3,
          B(f'η = 1 − 1/r_p^((k−1)/k) = 1 − 1/{rp}^0,2857 = {N(b["eta"],3)}. 1 − 1/r_p = {N(1-1/rp,3)} quên số mũ; số mũ k−1 cho {N(1-1/rp**.4,3)}; 1 − T₁/T₃ = {N(1-T1/T3,3)} là hiệu suất Carnot.',
            f'η = 1 − 1/r_p^((k−1)/k) = 1 − 1/{rp}^0.2857 = {N(b["eta"],3)}. 1 − 1/r_p = {N(1-1/rp,3)} forgets the exponent; the exponent k−1 gives {N(1-1/rp**.4,3)}; 1 − T₁/T₃ = {N(1-T1/T3,3)} is the Carnot efficiency.'), 1, 'bray', GEN('hiệu suất Brayton', 'Brayton efficiency'))
for (T1, T3) in ((300.0, 1000.0), (288.0, 1400.0)):
    ro = rp_opt(T3, T1); F('rp_opt', dict(T1=T1, T3=T3, k=1.4), 'rp', ro)
    M(B(f'Với T_min = {int(T1)} K, T_max = {int(T3)} K và k = 1,4, tỉ số áp r_p cho công thực cực đại của chu trình Brayton khí lạnh (slide tr.40) là:', f'With T_min = {int(T1)} K, T_max = {int(T3)} K and k = 1.4, the pressure ratio r_p giving the maximum net work of the cold-air Brayton cycle (slide p.40) is:'),
      ro, [(T3 / T1) ** (1.4 / 0.4), (T3 / T1) ** (0.4 / 1.4), (T3 / T1) ** 1.4 / 2], '', 2,
      B(f'r_p,opt = (T_max/T_min)^(k/[2(k−1)]) = {N(T3/T1,3)}^1,75 = {N(ro,2)}. Số mũ k/(k−1) = 3,5 là giá trị làm w_net = 0 ({N((T3/T1)**3.5,1)}); số mũ (k−1)/k cho {N((T3/T1)**(0.4/1.4),2)}; (T₃/T₁)^k/2 cho {N((T3/T1)**1.4/2,2)}.',
        f'r_p,opt = (T_max/T_min)^(k/[2(k−1)]) = {N(T3/T1,3)}^1.75 = {N(ro,2)}. The exponent k/(k−1) = 3.5 gives the value at which w_net = 0 ({N((T3/T1)**3.5,1)}); the exponent (k−1)/k gives {N((T3/T1)**(0.4/1.4),2)}; (T₃/T₁)^k/2 gives {N((T3/T1)**1.4/2,2)}.'), 2, 'bray', GEN('r_p tối ưu cho công', 'work-optimal r_p'))
T1, T3 = 300.0, 1000.0; ro = rp_opt(T3, T1); bo = brayton(ro, T1, T3); F('brayton_wmax', dict(T1=T1, T3=T3, k=1.4), 'wnet', bo['wnet']); F('brayton_wmax', dict(T1=T1, T3=T3, k=1.4), 'eta', bo['eta'])
opts = [B(f'{N(bo["wnet"],0)} kJ/kg; {N(bo["eta"],3)}', f'{N(bo["wnet"],0)} kJ/kg; {N(bo["eta"],3)}'), B(f'{N(bo["wnet"],0)} kJ/kg; {N(1-T1/T3,3)}', f'{N(bo["wnet"],0)} kJ/kg; {N(1-T1/T3,3)}'), B(f'{N(brayton(15,T1,T3)["wnet"],0)} kJ/kg; {N(brayton(15,T1,T3)["eta"],3)}', f'{N(brayton(15,T1,T3)["wnet"],0)} kJ/kg; {N(brayton(15,T1,T3)["eta"],3)}'), B(f'{N(bo["wt"],0)} kJ/kg; {N(bo["eta"],3)}', f'{N(bo["wt"],0)} kJ/kg; {N(bo["eta"],3)}')]
add(mcq(B('Chu trình Brayton khí lạnh với T_min = 300 K, T_max = 1000 K (slide tr.40; k = 1,4; c_p = 1,005). Tại r_p cho công cực đại, công thực riêng và hiệu suất lần lượt là:', 'A cold-air Brayton cycle with T_min = 300 K, T_max = 1000 K (slide p.40; k = 1.4; c_p = 1.005). At the r_p of maximum work, the net work per kg and the efficiency are, respectively:'), opts, 0,
        B(f'r_p,opt = {N(ro,2)} ⇒ x = √(T₃/T₁) = {N(math.sqrt(T3/T1),4)}; T₂ = T₄ = {N(bo["T2"],1)} K; w_net = c_p(T₃ − T₂) − c_p(T₄ − T₁) = {N(bo["wnet"],1)} kJ/kg; η = 1 − 1/x = {N(bo["eta"],3)}, thấp hơn Carnot {N(1-T1/T3,3)}. Tại r_p = 15 (slide) công chỉ còn {N(brayton(15,T1,T3)["wnet"],0)} kJ/kg dù η = {N(brayton(15,T1,T3)["eta"],3)} cao hơn: công cực đại và hiệu suất cực đại không cùng điểm.',
          f'r_p,opt = {N(ro,2)} ⇒ x = √(T₃/T₁) = {N(math.sqrt(T3/T1),4)}; T₂ = T₄ = {N(bo["T2"],1)} K; w_net = c_p(T₃ − T₂) − c_p(T₄ − T₁) = {N(bo["wnet"],1)} kJ/kg; η = 1 − 1/x = {N(bo["eta"],3)}, below the Carnot value {N(1-T1/T3,3)}. At r_p = 15 (slide) the work is only {N(brayton(15,T1,T3)["wnet"],0)} kJ/kg although η = {N(brayton(15,T1,T3)["eta"],3)} is higher: maximum work and maximum efficiency do not coincide.'), 3, TOP['bray'], GEN('Brayton: công cực đại', 'Brayton at maximum work'), 'bo_sung', 'script (verify_m02: brayton_wmax)'))
# ================================================================ Brayton with efficiencies and regeneration (constant cp)
for (rp, T1, T3, ec, et) in ((10, 300.0, 1300.0, .85, .88), (8, 290.0, 1200.0, .80, .85)):
    p = dict(rp=rp, T1=T1, T3=T3, k=1.4, cp=CP_AIR, etac=ec, etat=et, eps=0.0); b = brayton(rp, T1, T3, etac=ec, etat=et); bi_ = brayton(rp, T1, T3)
    for k_ in ('T2', 'T4', 'wc', 'wt', 'wnet', 'qin', 'bwr', 'eta'): reg('brayton_k', p, k_, b[k_], 1e-6)
    M(B(f'Chu trình Brayton khí lạnh (k = 1,4; c_p = 1,005): r_p = {rp}, T₁ = {int(T1)} K, T₃ = {int(T3)} K, η_c = {int(ec*100)} %, η_t = {int(et*100)} %. Tỉ số công hồi là:', f'Cold-air Brayton cycle (k = 1.4; c_p = 1.005): r_p = {rp}, T₁ = {int(T1)} K, T₃ = {int(T3)} K, η_c = {int(ec*100)} %, η_t = {int(et*100)} %. The back work ratio is:'),
      b['bwr'], [bi_['bwr'], bi_['bwr'] * ec * et, bi_['bwr'] * ec / et], '', 3,
      B(f'w_comp = w_s/η_c = {N(bi_["wc"],1)}/{ec} = {N(b["wc"],1)}; w_turb = η_tw_s = {et}·{N(bi_["wt"],1)} = {N(b["wt"],1)} kJ/kg ⇒ r_bw = {N(b["bwr"],3)}. Lý tưởng cho {N(bi_["bwr"],3)}; nhân cả hai η cho {N(bi_["bwr"]*ec*et,3)}; nhân η_c/η_t cho {N(bi_["bwr"]*ec/et,3)} (đúng phải chia cho η_c và nhân η_t ở mẫu: r_bw = r_bw,s/(η_cη_t)).',
        f'w_comp = w_s/η_c = {N(bi_["wc"],1)}/{ec} = {N(b["wc"],1)}; w_turb = η_tw_s = {et}·{N(bi_["wt"],1)} = {N(b["wt"],1)} kJ/kg ⇒ r_bw = {N(b["bwr"],3)}. The ideal cycle gives {N(bi_["bwr"],3)}; multiplying by both η gives {N(bi_["bwr"]*ec*et,3)}; multiplying by η_c/η_t gives {N(bi_["bwr"]*ec/et,3)} (the correct factor is 1/(η_cη_t): r_bw = r_bw,s/(η_cη_t)).'), 3, 'real', GEN('Brayton thực: tỉ số công hồi', 'real Brayton: back work ratio'))
    M(B(f'Cùng chu trình (r_p = {rp}, T₁ = {int(T1)} K, T₃ = {int(T3)} K, η_c = {int(ec*100)} %, η_t = {int(et*100)} %, khí lạnh): hiệu suất nhiệt là:', f'The same cycle (r_p = {rp}, T₁ = {int(T1)} K, T₃ = {int(T3)} K, η_c = {int(ec*100)} %, η_t = {int(et*100)} %, cold air): the thermal efficiency is:'),
      b['eta'], [bi_['eta'], b['wnet'] / (b['qin'] + b['wc'] - bi_['wc']), 1 - (1 - bi_['eta']) / (ec * et)], '', 3,
      B(f'T₂ = T₁ + w_comp/c_p = {N(b["T2"],0)} K; q_in = c_p(T₃ − T₂) = {N(b["qin"],0)}; w_net = {N(b["wnet"],0)} kJ/kg ⇒ η = {N(b["eta"],3)} (lý tưởng {N(bi_["eta"],3)}). Nhiệt cấp vào tăng khi máy nén kém hiệu quả vì T₂ cao hơn nhưng công thực giảm nhiều hơn.',
        f'T₂ = T₁ + w_comp/c_p = {N(b["T2"],0)} K; q_in = c_p(T₃ − T₂) = {N(b["qin"],0)}; w_net = {N(b["wnet"],0)} kJ/kg ⇒ η = {N(b["eta"],3)} (ideal {N(bi_["eta"],3)}). Less heat is needed when the compressor is less efficient (T₂ is higher), but the net work drops even more.'), 3, 'real', GEN('Brayton thực: hiệu suất', 'real Brayton: efficiency'))
for (T1, T3, rp) in ((300.0, 1200.0, 6), (300.0, 1400.0, 8)):
    x = rp ** (.4 / 1.4); er = 1 - T1 / T3 * x; es = 1 - 1 / x; F('regen_eta', dict(T1=T1, T3=T3, rp=rp, k=1.4), 'eta', er)
    M(B(f'Chu trình Brayton khí lạnh có bộ hồi nhiệt lý tưởng (ε = 100 %): T₁ = {int(T1)} K, T₃ = {int(T3)} K, r_p = {rp}, k = 1,4. Hiệu suất nhiệt là:', f'A cold-air Brayton cycle with an ideal regenerator (ε = 100 %): T₁ = {int(T1)} K, T₃ = {int(T3)} K, r_p = {rp}, k = 1.4. The thermal efficiency is:'),
      er, [es, 1 - (T1 / T3) / x, 1 - T1 / T3], '', 3,
      B(f'η_regen = 1 − (T₁/T₃)r_p^((k−1)/k) = 1 − ({int(T1)}/{int(T3)})·{N(x,4)} = {N(er,3)} (slide tr.45). Không hồi nhiệt: {N(es,3)}; (T₁/T₃)/x thay cho (T₁/T₃)x cho {N(1-(T1/T3)/x,3)}; Carnot {N(1-T1/T3,3)}.',
        f'η_regen = 1 − (T₁/T₃)r_p^((k−1)/k) = 1 − ({int(T1)}/{int(T3)})·{N(x,4)} = {N(er,3)} (slide p.45). Without regeneration: {N(es,3)}; (T₁/T₃)/x instead of (T₁/T₃)x gives {N(1-(T1/T3)/x,3)}; Carnot {N(1-T1/T3,3)}.'), 2, 'regen', GEN('hiệu suất Brayton có hồi nhiệt', 'Brayton efficiency with regeneration'))
T1, T3 = 300.0, 1200.0; rc_ = (T3 / T1) ** (1.4 / (2 * 0.4)); F('regen_cross', dict(T1=T1, T3=T3, k=1.4), 'rp', rc_)
M(B('Với T₁ = 300 K, T₃ = 1200 K, k = 1,4 (khí lạnh), hồi nhiệt lý tưởng chỉ có lợi (η_regen > η không hồi nhiệt) khi r_p nhỏ hơn giá trị nào?', 'With T₁ = 300 K, T₃ = 1200 K, k = 1.4 (cold air), an ideal regenerator helps (η_regen > η without regeneration) only when r_p is below which value?'),
  rc_, [(T3 / T1) ** 3.5, (T3 / T1) ** (0.4 / 1.4), (T3 / T1) ** (1.4 / 0.8) / 2], '', 2,
  B(f'η_regen = η_simple ⇔ (T₁/T₃)x = 1/x ⇔ x² = T₃/T₁ ⇒ r_p = (T₃/T₁)^(k/[2(k−1)]) = 4^1,75 = {N(rc_,2)}: cũng là r_p cho công cực đại. Dưới giá trị này T₄ > T₂ nên khí xả còn nóng hơn khí nén và hồi nhiệt có ích. Số mũ k/(k−1) cho {N((T3/T1)**3.5,1)}; (k−1)/k cho {N((T3/T1)**(0.4/1.4),2)}.',
    f'η_regen = η_simple ⇔ (T₁/T₃)x = 1/x ⇔ x² = T₃/T₁ ⇒ r_p = (T₃/T₁)^(k/[2(k−1)]) = 4^1.75 = {N(rc_,2)}: also the r_p of maximum work. Below it T₄ > T₂ so the exhaust is hotter than the compressed air and regeneration helps. The exponent k/(k−1) gives {N((T3/T1)**3.5,1)}; (k−1)/k gives {N((T3/T1)**(0.4/1.4),2)}.'), 3, 'regen', GEN('r_p giao điểm hồi nhiệt', 'regeneration cross-over r_p'))
for (T2, T4, eps) in ((520.0, 780.0, 0.7), (600.0, 900.0, 0.8)):
    T5 = T2 + eps * (T4 - T2); F('regen_T5', dict(T2=T2, T4=T4, eps=eps), 'T5', T5)
    M(B(f'Bộ hồi nhiệt có hiệu quả ε = {eps} (khí lạnh): khí nén ra máy nén ở T₂ = {int(T2)} K, khí xả tuabin vào bộ hồi nhiệt ở T₄ = {int(T4)} K. Nhiệt độ khí nén sau bộ hồi nhiệt T₅ (K) là:', f'A regenerator of effectiveness ε = {eps} (cold air): compressed air leaves the compressor at T₂ = {int(T2)} K, turbine exhaust enters the regenerator at T₄ = {int(T4)} K. The compressed-air temperature after the regenerator T₅ (K) is:'),
      T5, [T4 - eps * (T4 - T2), eps * T4, T2 + (T4 - T2) / eps], 'K', 0,
      B(f'ε = (T₅ − T₂)/(T₄ − T₂) ⇒ T₅ = T₂ + ε(T₄ − T₂) = {int(T2)} + {eps}·{int(T4-T2)} = {N(T5,0)} K. T₄ − ε(T₄ − T₂) = {N(T4-eps*(T4-T2),0)} là nhiệt độ khí xả ra khỏi bộ hồi nhiệt (T₆); εT₄ = {N(eps*T4,0)}; chia cho ε cho {N(T2+(T4-T2)/eps,0)}.',
        f'ε = (T₅ − T₂)/(T₄ − T₂) ⇒ T₅ = T₂ + ε(T₄ − T₂) = {int(T2)} + {eps}·{int(T4-T2)} = {N(T5,0)} K. T₄ − ε(T₄ − T₂) = {N(T4-eps*(T4-T2),0)} is the temperature of the exhaust leaving the regenerator (T₆); εT₄ = {N(eps*T4,0)}; dividing by ε gives {N(T2+(T4-T2)/eps,0)}.'), 2, 'regen', GEN('hiệu quả bộ hồi nhiệt', 'regenerator effectiveness'))
p = dict(rp=9, T1=300.0, T3=1200.0, k=1.4, cp=CP_AIR, etac=.85, etat=.88, eps=.75); br = brayton(9, 300.0, 1200.0, etac=.85, etat=.88, eps=.75); bn = brayton(9, 300.0, 1200.0, etac=.85, etat=.88)
for k_ in ('T4', 'T5', 'wnet', 'qin', 'eta'): reg('brayton_k', p, k_, br[k_], 1e-6)
M(B('Chu trình Brayton khí lạnh (k = 1,4; c_p = 1,005): r_p = 9, T₁ = 300 K, T₃ = 1200 K, η_c = 85 %, η_t = 88 %, bộ hồi nhiệt ε = 75 %. Hiệu suất nhiệt là:', 'A cold-air Brayton cycle (k = 1.4; c_p = 1.005): r_p = 9, T₁ = 300 K, T₃ = 1200 K, η_c = 85 %, η_t = 88 %, regenerator ε = 75 %. The thermal efficiency is:'),
  br['eta'], [bn['eta'], brayton(9, 300.0, 1200.0)['eta'], br['wnet'] / (CP_AIR * (1200 - br['T4']))], '', 3,
  B(f'T₂ = {N(br["T2"],0)} K, T₄ = {N(br["T4"],0)} K; T₅ = T₂ + ε(T₄ − T₂) = {N(br["T5"],0)} K; q_in = c_p(T₃ − T₅) = {N(br["qin"],0)}; w_net = {N(br["wnet"],0)} kJ/kg (hồi nhiệt không đổi công) ⇒ η = {N(br["eta"],3)}. Không hồi nhiệt: {N(bn["eta"],3)}; chu trình lý tưởng: {N(brayton(9,300.0,1200.0)["eta"],3)}; {N(br["wnet"]/(CP_AIR*(1200-br["T4"])),3)} dùng T₄ thay T₅ trong q_in (ε = 100 %).',
    f'T₂ = {N(br["T2"],0)} K, T₄ = {N(br["T4"],0)} K; T₅ = T₂ + ε(T₄ − T₂) = {N(br["T5"],0)} K; q_in = c_p(T₃ − T₅) = {N(br["qin"],0)}; w_net = {N(br["wnet"],0)} kJ/kg (regeneration does not change the work) ⇒ η = {N(br["eta"],3)}. Without regeneration: {N(bn["eta"],3)}; ideal cycle: {N(brayton(9,300.0,1200.0)["eta"],3)}; {N(br["wnet"]/(CP_AIR*(1200-br["T4"])),3)} uses T₄ instead of T₅ in q_in (ε = 100 %).'), 3, 'regen', GEN('Brayton thực có hồi nhiệt', 'real Brayton with regeneration'))
# ================================================================ multistage compression (cold air)
for (T1, rp) in ((300.0, 12.0), (290.0, 16.0)):
    x = rp ** (.4 / 1.4); w1 = CP_AIR * T1 * (x - 1); w2 = 2 * CP_AIR * T1 * (math.sqrt(rp) ** (.4 / 1.4) - 1); F('w_comp_stages', dict(T1=T1, rp=rp, k=1.4), 'w1', w1); F('w_comp_stages', dict(T1=T1, rp=rp, k=1.4), 'w2', w2)
    M(B(f'Nén không khí (khí lạnh, c_p = 1,005) từ {int(T1)} K với tỉ số áp {int(rp)}: tiết kiệm công nén (kJ/kg) khi dùng hai cấp có làm mát trung gian về {int(T1)} K, tỉ số áp mỗi cấp bằng nhau, so với một cấp là:', f'Compressing air (cold air, c_p = 1.005) from {int(T1)} K with a pressure ratio of {int(rp)}: the compression work saved (kJ/kg) by two stages with intercooling back to {int(T1)} K and equal stage pressure ratios, compared with one stage, is:'),
      w1 - w2, [w2, w1 / 2, w1 - w2 / 2], 'kJ/kg', 1,
      B(f'Một cấp: w₁ = c_pT₁(r_p^0,2857 − 1) = {N(w1,1)} kJ/kg. Hai cấp: mỗi cấp r_p = √{int(rp)} = {N(math.sqrt(rp),3)}, w₂ = 2c_pT₁(r_p^0,1429 − 1) = {N(w2,1)}. Tiết kiệm = {N(w1-w2,1)} kJ/kg (vùng hồng slide tr.46). {N(w2,1)} là công hai cấp; {N(w1/2,1)} chia đôi công một cấp.',
        f'One stage: w₁ = c_pT₁(r_p^0.2857 − 1) = {N(w1,1)} kJ/kg. Two stages: each r_p = √{int(rp)} = {N(math.sqrt(rp),3)}, w₂ = 2c_pT₁(r_p^0.1429 − 1) = {N(w2,1)}. Saving = {N(w1-w2,1)} kJ/kg (pink area of slide p.46). {N(w2,1)} is the two-stage work; {N(w1/2,1)} halves the one-stage work.'), 3, 'multi', GEN('tiết kiệm công nén nhờ làm mát trung gian', 'compression work saved by intercooling'))
Pm = math.sqrt(100 * 1600); F('p_inter', dict(P1=100, P3=1600), 'Pm', Pm)
M(B('Nén hai cấp từ 100 kPa tới 1600 kPa có làm mát trung gian về nhiệt độ đầu vào. Áp suất trung gian làm tổng công nén nhỏ nhất (kPa) là:', 'Two-stage compression from 100 kPa to 1600 kPa with intercooling back to the inlet temperature. The intermediate pressure that minimises the total compression work (kPa) is:'),
  Pm, [(100 + 1600) / 2, 1600 / 100, 100 * 1600 ** 0.5], 'kPa', 0,
  B(f'Công nhỏ nhất khi tỉ số áp hai cấp bằng nhau: P_m = √(P₁P₃) = √(100·1600) = {N(Pm,0)} kPa (tỉ số 4 mỗi cấp). Trung bình cộng cho {N(850,0)}; 1600/100 = 16 là tỉ số tổng; 100√1600 = {N(100*1600**.5,0)} lẫn đơn vị.',
    f'Work is smallest when both stages have the same pressure ratio: P_m = √(P₁P₃) = √(100·1600) = {N(Pm,0)} kPa (ratio 4 per stage). The arithmetic mean gives {N(850,0)}; 1600/100 = 16 is the overall ratio; 100√1600 = {N(100*1600**.5,0)} mixes units.'), 2, 'multi', GEN('áp suất trung gian tối ưu', 'optimal intermediate pressure'))
# ================================================================ ideal jet cycle
for (m_, Ve, Vi) in ((50.0, 600.0, 200.0), (120.0, 450.0, 250.0)):
    Fth = m_ * (Ve - Vi); F('thrust', dict(m=m_, Ve=Ve, Vi=Vi), 'F', Fth)
    M(B(f'Turbojet lý tưởng, áp suất cửa vào và cửa ra bằng áp suất môi trường: lưu lượng khí {int(m_)} kg/s, vận tốc khí thải {int(Ve)} m/s, vận tốc bay {int(Vi)} m/s (bỏ qua lượng nhiên liệu). Lực đẩy thực (kN) là:', f'An ideal turbojet with inlet and exit pressures equal to ambient: air flow {int(m_)} kg/s, exhaust velocity {int(Ve)} m/s, flight speed {int(Vi)} m/s (fuel mass neglected). The net thrust (kN) is:'),
      Fth / 1e3, [m_ * Ve / 1e3, m_ * (Ve + Vi) / 1e3, m_ * (Ve ** 2 - Vi ** 2) / 2e3], 'kN', 1,
      B(f'F = ṁ(V_exit − V_inlet) = {int(m_)}·({int(Ve)} − {int(Vi)}) = {N(Fth,0)} N = {N(Fth/1e3,1)} kN (slide tr.52). ṁV_exit = {N(m_*Ve/1e3,1)} kN là lực đẩy tổng (chưa trừ lực cản ram); cộng V_inlet cho {N(m_*(Ve+Vi)/1e3,1)}; ṁ(V₂² − V₁²)/2 = {N(m_*(Ve**2-Vi**2)/2e3,1)} kW là độ tăng động năng.',
        f'F = ṁ(V_exit − V_inlet) = {int(m_)}·({int(Ve)} − {int(Vi)}) = {N(Fth,0)} N = {N(Fth/1e3,1)} kN (slide p.52). ṁV_exit = {N(m_*Ve/1e3,1)} kN is the gross thrust (ram drag not subtracted); adding V_inlet gives {N(m_*(Ve+Vi)/1e3,1)}; ṁ(V₂² − V₁²)/2 = {N(m_*(Ve**2-Vi**2)/2e3,1)} kW is the kinetic-energy rise.'), 1, 'jet', GEN('lực đẩy turbojet', 'turbojet thrust'))
for (Ta, V) in ((250.0, 250.0), (216.65, 300.0)):
    T2 = Ta + V ** 2 / (2 * CP_AIR * 1000); F('diffuser_T', dict(Ta=Ta, V=V, cp=CP_AIR), 'T2', T2)
    M(B(f'Không khí ở {Ta} K đi vào bộ khuếch tán lý tưởng của máy bay bay {int(V)} m/s (c_p = 1,005 kJ/kg·K), ra với vận tốc coi như bằng 0. Nhiệt độ ra T₂ (K) là:', f'Air at {Ta} K enters the ideal diffuser of an aircraft flying at {int(V)} m/s (c_p = 1.005 kJ/kg·K) and leaves at essentially zero velocity. The exit temperature T₂ (K) is:'),
      T2, [Ta - V ** 2 / (2 * CP_AIR * 1000), Ta + V ** 2 / (2 * CP_AIR), Ta + V ** 2 / (CP_AIR * 1000)], 'K', 1,
      B(f'h₂ = h₁ + V²/2 ⇒ T₂ = T₁ + V²/(2c_p) = {Ta} + {int(V)}²/(2·1005) = {N(T2,1)} K (slide tr.49–51, Cengel Ví dụ 9–9). Dấu − cho {N(Ta-V**2/(2*CP_AIR*1000),1)}; quên đổi kJ→J cho {N(Ta+V**2/(2*CP_AIR),0)}; quên hệ số 2 cho {N(Ta+V**2/(CP_AIR*1000),1)}.',
        f'h₂ = h₁ + V²/2 ⇒ T₂ = T₁ + V²/(2c_p) = {Ta} + {int(V)}²/(2·1005) = {N(T2,1)} K (slide pp.49–51, Cengel Example 9–9). A minus sign gives {N(Ta-V**2/(2*CP_AIR*1000),1)}; forgetting the kJ→J conversion gives {N(Ta+V**2/(2*CP_AIR),0)}; forgetting the factor 2 gives {N(Ta+V**2/(CP_AIR*1000),1)}.'), 2, 'jet', GEN('nhiệt độ ra bộ khuếch tán', 'diffuser exit temperature'))
for (Ta, Pa, V, rp, T4, md) in ((220.0, 25.0, 250.0, 12, 1400.0, 40.0), (230.0, 30.0, 200.0, 10, 1300.0, 30.0)):
    j = ideal_jet_k(Ta, Pa, V, rp, T4, md, CP_AIR, J=1000.0); p = dict(Ta=Ta, Pa=Pa, V=V, rp=rp, T4=T4, mdot=md, cp=CP_AIR, k=1.4, J=1000.0)
    for k_ in ('T2', 'T3', 'T5', 'T6', 'V6', 'Wp', 'Qin', 'etaP'): reg('jet_k', p, k_, j[k_], 1e-6)
    if V == 250.0:
        M(B(f'Turbojet lý tưởng khí lạnh (k = 1,4; c_p = 1,005): bay {int(V)} m/s ở độ cao có {int(Ta)} K, {int(Pa)} kPa; r_p máy nén = {rp}; nhiệt độ vào tuabin {int(T4)} K; công tuabin = công máy nén. Nhiệt độ ra tuabin T₅ (K) là:', f'An ideal cold-air turbojet (k = 1.4; c_p = 1.005): flight {int(V)} m/s where the air is {int(Ta)} K, {int(Pa)} kPa; compressor r_p = {rp}; turbine inlet {int(T4)} K; turbine work = compressor work. The turbine exit temperature T₅ (K) is:'),
          j['T5'], [T4 - j['T3'], T4 * rp ** -(.4 / 1.4), T4 - j['T3'] + Ta], 'K', 0,
          B(f'T₂ = {N(j["T2"],1)} K (khuếch tán); T₃ = T₂·{rp}^0,2857 = {N(j["T3"],1)} K; T₃ − T₂ = T₄ − T₅ ⇒ T₅ = T₄ − T₃ + T₂ = {N(j["T5"],1)} K. Quên + T₂ cho {N(T4-j["T3"],0)}; giãn nở cả r_p cho {N(T4*rp**-(.4/1.4),0)}; dùng T_a thay T₂ cho {N(T4-j["T3"]+Ta,0)}.',
            f'T₂ = {N(j["T2"],1)} K (diffuser); T₃ = T₂·{rp}^0.2857 = {N(j["T3"],1)} K; T₃ − T₂ = T₄ − T₅ ⇒ T₅ = T₄ − T₃ + T₂ = {N(j["T5"],1)} K. Forgetting + T₂ gives {N(T4-j["T3"],0)}; expanding through the whole r_p gives {N(T4*rp**-(.4/1.4),0)}; using T_a instead of T₂ gives {N(T4-j["T3"]+Ta,0)}.'), 3, 'jet', GEN('turbojet lý tưởng: T₅', 'ideal turbojet: T₅'))
    else:
        M(B(f'Turbojet lý tưởng khí lạnh (k = 1,4; c_p = 1,005): bay {int(V)} m/s ở {int(Ta)} K, {int(Pa)} kPa; r_p = {rp}; T₄ = {int(T4)} K; ṁ = {int(md)} kg/s. Hiệu suất "đẩy" của slide η_P = Ẇ_p/Q̇_in (%) là:', f'An ideal cold-air turbojet (k = 1.4; c_p = 1.005): flight {int(V)} m/s at {int(Ta)} K, {int(Pa)} kPa; r_p = {rp}; T₄ = {int(T4)} K; ṁ = {int(md)} kg/s. The slide\'s "propulsive" efficiency η_P = Ẇ_p/Q̇_in (%) is:'),
          j['etaP'] * 100, [2 * V / (V + j['V6']) * 100, j['Wp'] / (md * CP_AIR * (T4 - j['T2'])) * 100, (j['V6'] - V) / j['V6'] * 100], '', 1,
          B(f'T₂ = {N(j["T2"],1)}, T₃ = {N(j["T3"],1)}, T₅ = T₄ − T₃ + T₂ = {N(j["T5"],1)} K; P₅ = P₄(T₅/T₄)^3,5; nhiệt độ ra vòi T₆ = T₅(P_a/P₅)^0,2857 = {N(j["T6"],1)} K; V₆ = √[2c_p(T₅ − T₆)] = {N(j["V6"],0)} m/s. Ẇ_p = ṁ(V₆ − V)V = {N(j["Wp"]/1e3,2)} MW; Q̇_in = ṁc_p(T₄ − T₃) = {N(j["Qin"]/1e3,2)} MW ⇒ η_P = {N(j["etaP"]*100,1)} %. 2V/(V + V₆) = {N(2*V/(V+j["V6"])*100,1)} % là hiệu suất đẩy kiểu Farokhi; dùng T₄ − T₂ trong Q̇_in cho {N(j["Wp"]/(md*CP_AIR*(T4-j["T2"]))*100,1)} %; (V₆ − V)/V₆ = {N((j["V6"]-V)/j["V6"]*100,1)} % không có ý nghĩa vật lý.',
            f'T₂ = {N(j["T2"],1)}, T₃ = {N(j["T3"],1)}, T₅ = T₄ − T₃ + T₂ = {N(j["T5"],1)} K; P₅ = P₄(T₅/T₄)^3.5; nozzle-exit temperature T₆ = T₅(P_a/P₅)^0.2857 = {N(j["T6"],1)} K; V₆ = √[2c_p(T₅ − T₆)] = {N(j["V6"],0)} m/s. Ẇ_p = ṁ(V₆ − V)V = {N(j["Wp"]/1e3,2)} MW; Q̇_in = ṁc_p(T₄ − T₃) = {N(j["Qin"]/1e3,2)} MW ⇒ η_P = {N(j["etaP"]*100,1)} %. 2V/(V + V₆) = {N(2*V/(V+j["V6"])*100,1)} % is Farokhi\'s propulsive efficiency; using T₄ − T₂ in Q̇_in gives {N(j["Wp"]/(md*CP_AIR*(T4-j["T2"]))*100,1)} %; (V₆ − V)/V₆ = {N((j["V6"]-V)/j["V6"]*100,1)} % has no physical meaning.'), 3, 'jet', GEN('turbojet lý tưởng: hiệu suất η_P', 'ideal turbojet: η_P'))
# ================================================================ reciprocating engines: geometry, MEP, power
for (Vd, Vc) in ((0.5, 0.0625), (0.4, 0.04)):
    r = (Vd + Vc) / Vc; F('r_from_V', dict(Vd=Vd, Vc=Vc), 'r', r)
    M(B(f'Một xi-lanh có thể tích làm việc V_d = {Vd} L và thể tích chết V_c = {Vc} L. Tỉ số nén là:', f'A cylinder has displacement volume V_d = {Vd} L and clearance volume V_c = {Vc} L. The compression ratio is:'),
      r, [Vd / Vc, (Vd + Vc) / Vd, Vd * Vc], '', 1,
      B(f'r = V_max/V_min = V_BDC/V_TDC = (V_d + V_c)/V_c = ({Vd} + {Vc})/{Vc} = {N(r,1)} (slide tr.15). V_d/V_c = {N(Vd/Vc,1)} quên cộng V_c (bằng r − 1); (V_d + V_c)/V_d = {N((Vd+Vc)/Vd,2)} đảo tỉ số.',
        f'r = V_max/V_min = V_BDC/V_TDC = (V_d + V_c)/V_c = ({Vd} + {Vc})/{Vc} = {N(r,1)} (slide p.15). V_d/V_c = {N(Vd/Vc,1)} forgets to add V_c (it equals r − 1); (V_d + V_c)/V_d = {N((Vd+Vc)/Vd,2)} inverts the ratio.'), 1, 'eng', GEN('tỉ số nén từ thể tích', 'compression ratio from volumes'))
for (mep, Vd, N_, ncyl) in ((900.0, 2.4e-3, 3000, 4), (1100.0, 4.5e-3, 2400, 6)):
    P = mep * Vd * N_ / 60 / 2; F('engine_power', dict(mep=mep, Vd=Vd, N=N_), 'P', P)
    M(B(f'Động cơ bốn kỳ {ncyl} xi-lanh, tổng thể tích làm việc {Vd*1000:.1f} L, MEP = {int(mep)} kPa, tốc độ {N_} vòng/phút. Công suất thực (kW) là:', f'A {ncyl}-cylinder four-stroke engine, total displacement {Vd*1000:.1f} L, MEP = {int(mep)} kPa, speed {N_} rev/min. The net power (kW) is:'),
      P, [2 * P, P / ncyl, P * 60], 'kW', 1,
      B(f'W_cycle = MEP·V_d = {int(mep)}·{Vd} = {N(mep*Vd,2)} kJ; bốn kỳ: một chu trình mỗi hai vòng ⇒ P = W_cycle·N/(2·60) = {N(mep*Vd,2)}·{N_}/120 = {N(P,1)} kW. Coi mỗi vòng một chu trình (hai kỳ) cho {N(2*P,1)} kW; chia cho số xi-lanh (đã nằm trong V_d tổng) cho {N(P/ncyl,1)}; nhân 60 thay vì chia cho {N(P*60,0)}.',
        f'W_cycle = MEP·V_d = {int(mep)}·{Vd} = {N(mep*Vd,2)} kJ; four-stroke: one cycle per two revolutions ⇒ P = W_cycle·N/(2·60) = {N(mep*Vd,2)}·{N_}/120 = {N(P,1)} kW. Counting one cycle per revolution (two-stroke) gives {N(2*P,1)} kW; dividing by the number of cylinders (already included in the total V_d) gives {N(P/ncyl,1)}; multiplying by 60 instead of dividing gives {N(P*60,0)}.'), 2, 'eng', GEN('công suất từ MEP', 'power from MEP'))
# ================================================================ table route (A-17)
for (T1, rp) in ((300.0, 10.0), (320.0, 12.0)):
    Pr1 = A(T1, 'Pr'); T2s = Ainv('Pr', rp * Pr1)['value']; Tc = T1 * rp ** (.4 / 1.4); reg('table_Pr', dict(T1=T1, rp=rp), 'T2s', T2s, 0.012)
    M(B(f'Dùng bảng A-17 (nhiệt dung riêng thay đổi): không khí nén đẳng entropi từ {int(T1)} K với tỉ số áp {int(rp)}. Nhiệt độ cuối T₂s (K) là:', f'Using Table A-17 (variable specific heats): air compressed isentropically from {int(T1)} K with a pressure ratio of {int(rp)}. The final temperature T₂s (K) is:'),
      T2s, [T1 * rp, T1 * rp ** 0.4, T2s + 0 + (T2s - Tc) * 3], 'K', 0,
      B(f'P_r1 = {N(Pr1,3)} ⇒ P_r2 = {int(rp)}·P_r1 = {N(rp*Pr1,2)} ⇒ T₂s = {N(T2s,1)} K (nội suy tuyến tính). Khí lạnh k = 1,4 cho {N(Tc,1)} K (lệch vì c_p tăng theo T). T₁r_p và T₁r_p^0,4 là sai công thức.',
        f'P_r1 = {N(Pr1,3)} ⇒ P_r2 = {int(rp)}·P_r1 = {N(rp*Pr1,2)} ⇒ T₂s = {N(T2s,1)} K (linear interpolation). Cold air k = 1.4 gives {N(Tc,1)} K (different because c_p rises with T). T₁r_p and T₁r_p^0.4 are wrong formulas.'), 2, 'table', GEN('tra bảng A-17 theo P_r', 'A-17 look-up by P_r'), 'bảng A-17 (props) + verify_m02: table_Pr')

def main():
    global G
    O1.build(); O2.build(); orig, printed = O3.build()
    conc = CO.build()
    items_src = list(orig) + conc
    sa = os.path.join(ROOT, 'data', 'qsrc'); os.makedirs(sa, exist_ok=True)
    dump(os.path.join(sa, 'm02.json'), items_src); dump(os.path.join(sa, 'm02_gen.json'), G)
    os.makedirs(os.path.join(ROOT, 'data', 'verify'), exist_ok=True)
    dump(os.path.join(ROOT, 'data', 'verify', 'm02_values.json'), dict(registry=REG, printed=printed))
    closed = [i for i in items_src + G if i['kind'] != 'ess']; l3 = [i for i in closed if i['level'] == 3]
    print(f'originals+concept {len(items_src)} (ess {sum(1 for i in items_src if i["kind"]=="ess")}) | generated {len(G)} | closed {len(closed)} | level 3: {len(l3)} ({100*len(l3)/len(closed):.0f} %) | registry {len(REG)} | printed {len(printed)}')

if __name__ == '__main__':
    main()
