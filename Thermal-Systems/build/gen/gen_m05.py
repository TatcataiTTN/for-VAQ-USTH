"""Generate the m05 question bank: data/qsrc/m05.json (originals + slide-derived conceptual items), data/qsrc/m05_gen.json (generated variants, origin 'bo_sung', fixed seed),
data/verify/m05_values.json (registry of every numeric answer + printed answers) and data/verify/m05_notes.json (via notes_m05.py).
Run:  .venv/bin/python -I build/gen/gen_m05.py"""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'props'))
from m05_common import *
import gen_m05_orig as O1, gen_m05_orig2 as O2, gen_m05_orig3 as O3, gen_m05_orig4 as O4, gen_m05_concept as CO
import notes_m05 as NT
rng = random.Random(20261116)
G = []
def g(item): G.append(item); return item
GAS = {'air': (1.4, 0.287, 'không khí', 'air'), 'N2': (1.4, 0.2968, 'nitơ', 'nitrogen'), 'He': (1.667, 2.0769, 'heli', 'helium'), 'CO2': (1.289, 0.1889, 'CO₂', 'carbon dioxide'),
       'Ar': (1.667, 0.2081, 'argon', 'argon'), 'CH4': (1.3, 0.5182, 'metan', 'methane'), 'prod': (1.33, 0.287, 'sản phẩm cháy', 'combustion products')}
def gd(key): k_, R_, nv, ne = GAS[key]; return k_, R_, nv, ne
def kRs(k_, R_): return f'k = {N(k_,3).rstrip("0").rstrip(".")}; R = {N(R_,4).rstrip("0").rstrip(".")} kJ/(kg·K)'
def kR_vi(k_, R_): return kRs(k_, R_)
GS_ = lambda vi, en: GS(vi, en)

# ---------------------------------------------------------------- G1: stagnation temperature (level 1)
for T, V in ((250.0, 300.0), (288.0, 200.0), (220.0, 350.0), (300.0, 450.0), (260.0, 150.0)):
    T0 = reg('stag', dict(T=T, P=100.0, V=V, k=1.4, R=0.287, cp=1.005), 'T0', T0_of(T, V, 1.005), 1e-9, f'G1 {T} {V}')
    g(gq(f'Không khí ở {T:g} K chuyển động với vận tốc {V:g} m/s (c_p = 1,005 kJ/(kg·K)). Nhiệt độ hãm T₀ là:', f'Air at {T:g} K moves at {V:g} m/s (c_p = 1.005 kJ/(kg·K)). The stagnation temperature T₀ is:',
         T0, [(T + V**2 / 1005.0, 'quên hệ số 2', 'forgets the factor 2'), (T + V**2 / 2.01, 'quên đổi m²/s² → kJ/kg', 'forgets the m²/s² → kJ/kg conversion'), (T - V**2 / 2010.0, 'trừ thay vì cộng', 'subtracts instead of adds'), (T + V**2 / 2000.0 / 0.718, 'dùng c_v = 0,718', 'uses c_v = 0.718')],
         'K', 1, f'T₀ = T + V²/(2c_p) = {T:g} + {V:g}²/(2 × 1,005 × 1000) = {T:g} + {N(V**2/2010,1)} = {N(T0,1)} K. Các phương án còn lại:', f'T₀ = T + V²/(2c_p) = {T:g} + {V:g}²/(2 × 1.005 × 1000) = {T:g} + {N(V**2/2010,1)} = {N(T0,1)} K. The other options:',
         1, TOP['stag'], GS_('nhiệt độ hãm', 'stagnation temperature'), 'script (verify_m05: ODE + node thermo.js)'))
# ---------------------------------------------------------------- G2: stagnation pressure (level 2)
for T, P, V in ((255.0, 50.0, 260.0), (230.0, 30.0, 280.0), (288.15, 101.325, 200.0), (270.0, 70.0, 240.0)):
    T0 = T0_of(T, V, 1.005); P0 = reg('stag', dict(T=T, P=P, V=V, k=1.4, R=0.287, cp=1.005), 'P0', P0_of(P, T, T0, 1.4), 1e-9, f'G2 {T} {P} {V}')
    g(gq(f'Không khí bay ở {V:g} m/s, nhiệt độ {T:g} K và áp suất {P:g} kPa (c_p = 1,005 kJ/(kg·K); k = 1,4). Áp suất hãm P₀ (hãm đẳng entropi) là:', f'Air flies at {V:g} m/s, temperature {T:g} K and pressure {P:g} kPa (c_p = 1.005 kJ/(kg·K); k = 1.4). The stagnation pressure P₀ (isentropic stop) is:',
         P0, [(P * (T0 / T) ** (0.4 / 1.4), 'đảo mũ: (k−1)/k', 'inverts the exponent: (k−1)/k'), (P * T0 / T, 'mũ 1 (đẳng áp)', 'exponent 1 (isobaric)'), (P * ((T + V**2 / 1005.0) / T) ** 3.5, 'quên hệ số 2 trong T₀', 'forgets the factor 2 in T₀'), (P * (T0 / T) ** 1.4, 'dùng mũ k', 'uses the exponent k')],
         'kPa', 1, f'T₀ = {T:g} + {V:g}²/2010 = {N(T0,1)} K; P₀ = {P:g} × ({N(T0,1)}/{T:g})^3,5 = {N(P0,1)} kPa. Các phương án còn lại:', f'T₀ = {T:g} + {V:g}²/2010 = {N(T0,1)} K; P₀ = {P:g} × ({N(T0,1)}/{T:g})^3.5 = {N(P0,1)} kPa. The other options:',
         2, TOP['stag'], GS_('áp suất hãm', 'stagnation pressure'), 'script (verify_m05: ODE + node thermo.js)'))
# ---------------------------------------------------------------- G3: Mach number from V and T (level 2)
for key, T, V in (('air', 217.0, 250.0), ('He', 400.0, 900.0), ('CO2', 350.0, 280.0), ('N2', 300.0, 380.0), ('Ar', 280.0, 300.0), ('CH4', 320.0, 450.0)):
    k_, R_, nv, ne = gd(key); c = csound(k_, R_, T); Ma = reg('sound', dict(k=k_, R=R_, T=T, V=V), 'Ma', V / c, 1e-9, f'G3 {key}')
    k0, R0 = GAS['air'][:2]
    g(gq(f'{nv[0].upper()+nv[1:]} ({kR_vi(k_,R_)}) ở {T:g} K chảy với vận tốc {V:g} m/s. Số Mach là:', f'{ne[0].upper()+ne[1:]} ({kRs(k_,R_)}) at {T:g} K flows at {V:g} m/s. The Mach number is:',
         Ma, [(V / csound(1.4, 0.287, T), 'dùng tốc độ âm của không khí', 'uses the speed of sound of air'), (V / math.sqrt(k_ * R_ * T), 'quên đổi kJ → J (thiếu ×1000 trong căn)', 'forgets kJ → J (missing ×1000 inside the root)'), (c / V, 'đảo tỉ số c/V', 'inverts the ratio c/V'), (V / csound(k_, R_, T - 273.15 if T > 273.15 else T), 'dùng °C thay cho K', 'uses °C instead of K')],
         '', 3, f'c = √(kRT) = √({N(k_,3)} × {N(R_*1000,1)} × {T:g}) = {N(c,1)} m/s; Ma = V/c = {V:g}/{N(c,1)} = {N(Ma,3)} ({"siêu âm" if Ma > 1 else "cận âm"}). Các phương án còn lại:', f'c = √(kRT) = √({N(k_,3)} × {N(R_*1000,1)} × {T:g}) = {N(c,1)} m/s; Ma = V/c = {V:g}/{N(c,1)} = {N(Ma,3)} ({"supersonic" if Ma > 1 else "subsonic"}). The other options:',
         2, TOP['snd'], GS_('số Mach theo khí', 'Mach number by gas'), 'script (verify_m05: numerical dP/drho at constant s)', sep=0.02))
# ---------------------------------------------------------------- G4: static T and P from Ma (level 2)
for key, T0, P0, Ma, what in (('air', 450.0, 600.0, 0.6, 'P'), ('air', 500.0, 800.0, 1.5, 'T'), ('N2', 400.0, 500.0, 0.9, 'P'), ('CO2', 600.0, 900.0, 1.2, 'T')):
    k_, R_, nv, ne = gd(key); T = reg('stat_Ma', dict(T0=T0, P0=P0, Ma=Ma, k=k_), 'T', T0 * TT0(Ma, k_), 1e-9, f'G4 T {key} {Ma}'); P = reg('stat_Ma', dict(T0=T0, P0=P0, Ma=Ma, k=k_), 'P', P0 * PP0(Ma, k_), 1e-9, f'G4 P {key} {Ma}')
    val, nm_, nmv, unit, nd = (P, 'áp suất tĩnh P', 'static pressure P', 'kPa', 1) if what == 'P' else (T, 'nhiệt độ tĩnh T', 'static temperature T', 'K', 1)
    base = P0 if what == 'P' else T0
    wr = ([(P0 * (1 + (k_ - 1) / 2 * Ma**2) ** (-1.0), 'dùng T/T₀ mũ −1 cho áp suất', 'uses (T/T₀)^1 for the pressure'), (P0 * TT0(Ma, k_), 'dùng T/T₀ thay cho P/P₀', 'uses T/T₀ instead of P/P₀'), (P0 * (1 - (k_ - 1) / 2 * Ma**2) ** (k_ / (k_ - 1)), 'trừ thay vì cộng (k−1)Ma²/2', 'subtracts instead of adds (k−1)Ma²/2'), (P0 * PP0(Ma, 1.4 if k_ != 1.4 else 1.3), f'dùng k = {1.4 if k_ != 1.4 else 1.3:g} thay cho {k_:g}', f'uses k = {1.4 if k_ != 1.4 else 1.3:g} instead of {k_:g}')] if what == 'P'
          else [(T0 / (1 + (k_ - 1) * Ma**2), 'quên hệ số 1/2 trong (k−1)/2', 'forgets the 1/2 in (k−1)/2'), (T0 * (1 + (k_ - 1) / 2 * Ma**2), 'đảo T/T₀ thành T₀/T', 'inverts T/T₀ into T₀/T'), (T0 * (1 - (k_ - 1) / 2 * Ma**2), 'trừ thay vì cộng', 'subtracts instead of adds'), (T0 * PP0(Ma, k_), 'dùng P/P₀ cho nhiệt độ', 'uses P/P₀ for the temperature')])
    g(gq(f'{nv[0].upper()+nv[1:]} ({kR_vi(k_,R_)}) có T₀ = {T0:g} K, P₀ = {P0:g} kPa chảy đẳng entropi tới Ma = {Ma:g}. {nm_[0].upper()+nm_[1:]} là:', f'{ne[0].upper()+ne[1:]} ({kRs(k_,R_)}) with T₀ = {T0:g} K, P₀ = {P0:g} kPa flows isentropically to Ma = {Ma:g}. The {nmv} is:',
         val, wr, unit, nd, f'T/T₀ = 1/(1 + (k−1)Ma²/2) = 1/(1 + {N((k_-1)/2,4)} × {N(Ma**2,2)}) = {N(TT0(Ma,k_),4)}; P/P₀ = (T/T₀)^(k/(k−1)) = {N(PP0(Ma,k_),4)}; T = {N(T,1)} K; P = {N(P,1)} kPa. Các phương án còn lại:',
         f'T/T₀ = 1/(1 + (k−1)Ma²/2) = 1/(1 + {N((k_-1)/2,4)} × {N(Ma**2,2)}) = {N(TT0(Ma,k_),4)}; P/P₀ = (T/T₀)^(k/(k−1)) = {N(PP0(Ma,k_),4)}; T = {N(T,1)} K; P = {N(P,1)} kPa. The other options:', 2, TOP['rel'], GS_('T, P theo Ma', 'T, P from Ma'), 'script (verify_m05: energy equation + brentq)'))
# ---------------------------------------------------------------- G5: compressor power (level 3)
for T01, pr, md in ((288.0, 6.0, 0.5), (300.0, 12.0, 0.1), (250.0, 8.0, 2.0), (310.0, 4.0, 1.5)):
    T02 = T01 * pr ** (0.4 / 1.4); w = cp_of(1.4, 0.287) * (T02 - T01); Pw = reg('comp', dict(T01=T01, pr=pr, k=1.4, R=0.287, mdot=md), 'P', w * md, 1e-9, f'G5 {T01} {pr} {md}'); reg('comp', dict(T01=T01, pr=pr, k=1.4, R=0.287, mdot=md), 'T02', T02, 1e-9, f'G5 T02 {T01} {pr}')
    cp5 = cp_of(1.4, 0.287)
    g(gq(f'Máy nén đẳng entropi nhận không khí (k = 1,4; R = 0,287 kJ/(kg·K)) ở nhiệt độ hãm {T01:g} K, tỉ số áp suất hãm {pr:g}, lưu lượng {md:g} kg/s. Công suất cấp là:', f'An isentropic compressor takes air (k = 1.4; R = 0.287 kJ/(kg·K)) at stagnation temperature {T01:g} K, stagnation pressure ratio {pr:g}, flow {md:g} kg/s. The power input is:',
         Pw, [(md * cp5 * (T01 * pr ** (1 / 1.4) - T01), 'dùng mũ 1/k', 'uses the exponent 1/k'), (cp5 * (T02 - T01), 'quên nhân lưu lượng (đây là kJ/kg)', 'forgets the flow rate (this is kJ/kg)'), (md * cp5 * T02, 'lấy c_p·T₀₂ thay cho độ tăng', 'takes c_p·T₀₂ instead of the rise'), (md * 0.718 * (T02 - T01), 'dùng c_v thay cho c_p', 'uses c_v instead of c_p')],
         'kW', 0, f'T₀₂ = {T01:g} × {pr:g}^0,2857 = {N(T02,1)} K; w = c_p(T₀₂ − T₀₁) = {N(cp5,4)} × {N(T02-T01,1)} = {N(w,1)} kJ/kg; Ẇ = {md:g} × {N(w,1)} = {N(Pw,0)} kW. Các phương án còn lại:', f'T₀₂ = {T01:g} × {pr:g}^0.2857 = {N(T02,1)} K; w = c_p(T₀₂ − T₀₁) = {N(cp5,4)} × {N(T02-T01,1)} = {N(w,1)} kJ/kg; Ẇ = {md:g} × {N(w,1)} = {N(Pw,0)} kW. The other options:',
         3, TOP['comp'], GS_('công suất máy nén', 'compressor power'), 'script (verify_m05: integral of v dP)', sep=0.03))
# ---------------------------------------------------------------- G6: turbine specific work (level 3)
for T01, pr in ((1100.0, 12.0), (1300.0, 20.0), (950.0, 6.0)):
    k_, R_ = 1.33, 0.287; cp_ = cp_of(k_, R_); T02 = T01 * (1.0 / pr) ** ((k_ - 1) / k_); w = reg('comp', dict(T01=T01, pr=1.0 / pr, k=k_, R=R_), 'w', cp_ * (T01 - T02), 1e-9, f'G6 {T01} {pr}')
    g(gq(f'Sản phẩm cháy (k = 1,33; R = 0,287 kJ/(kg·K)) vào tuabin ở nhiệt độ hãm {T01:g} K và giãn nở đẳng entropi với tỉ số áp suất hãm {pr:g}. Công riêng của tuabin là:', f'Combustion products (k = 1.33; R = 0.287 kJ/(kg·K)) enter a turbine at stagnation temperature {T01:g} K and expand isentropically with a stagnation pressure ratio {pr:g}. The specific work of the turbine is:',
         w, [(cp_of(1.4, 0.287) * T01 * (1 - (1 / pr) ** (0.4 / 1.4)), 'dùng k = 1,4 của không khí', 'uses k = 1.4 of air'), (cp_ * T01 * (1 - (1 / pr) ** (1 / k_)), 'dùng mũ 1/k', 'uses the exponent 1/k'), (0.287 * T01 * (1 - (1 / pr) ** ((k_ - 1) / k_)), 'dùng R thay cho c_p', 'uses R instead of c_p'), (cp_ * T01 * (1 - pr ** ((k_ - 1) / k_)), 'đảo tỉ số áp suất (nén thay vì giãn nở)', 'inverts the pressure ratio (compression instead of expansion)')],
         'kJ/kg', 0, f'c_p = kR/(k−1) = {N(cp_,4)}; T₀₂ = {T01:g} × (1/{pr:g})^0,2481 = {N(T02,1)} K; w = c_p(T₀₁ − T₀₂) = {N(cp_,4)} × {N(T01-T02,1)} = {N(w,1)} kJ/kg. Các phương án còn lại:', f'c_p = kR/(k−1) = {N(cp_,4)}; T₀₂ = {T01:g} × (1/{pr:g})^0.2481 = {N(T02,1)} K; w = c_p(T₀₁ − T₀₂) = {N(cp_,4)} × {N(T01-T02,1)} = {N(w,1)} kJ/kg. The other options:',
         3, TOP['comp'], GS_('công tuabin', 'turbine work'), 'script (verify_m05: integral of RT dlnP)', sep=0.03))
# ---------------------------------------------------------------- G7: critical pressure and temperature (level 2)
for key, P0, T0 in (('He', 800.0, 500.0), ('CH4', 600.0, 700.0), ('CO2', 1000.0, 600.0), ('prod', 900.0, 1100.0)):
    k_, R_, nv, ne = gd(key); c = crit(k_); Ps = reg('critst', dict(k=k_, P0=P0, T0=T0, R=R_), 'Ps', c['PP'] * P0, 1e-9, f'G7 Ps {key}'); Ts = reg('critst', dict(k=k_, P0=P0, T0=T0, R=R_), 'Ts', c['TT'] * T0, 1e-9, f'G7 Ts {key}')
    reg('critst', dict(k=k_, P0=P0, T0=T0, R=R_), 'Vs', csound(k_, R_, Ts), 1e-9, f'G7 Vs {key}'); reg('critst', dict(k=k_, P0=P0, T0=T0, R=R_), 'rhos', Ps / (R_ * Ts), 1e-9, f'G7 rhos {key}')
    g(gq(f'{nv[0].upper()+nv[1:]} ({kR_vi(k_,R_)}) có áp suất hãm {P0:g} kPa và nhiệt độ hãm {T0:g} K đi vào vòi phun hội tụ–phân kỳ (vận tốc vào ≈ 0). Áp suất tới hạn P* là:', f'{ne[0].upper()+ne[1:]} ({kRs(k_,R_)}) with stagnation pressure {P0:g} kPa and stagnation temperature {T0:g} K enters a converging–diverging nozzle (inlet velocity ≈ 0). The critical pressure P* is:',
         Ps, [(P0 * 0.5283, 'dùng P*/P₀ = 0,5283 của không khí', 'uses P*/P₀ = 0.5283 of air'), (P0 * c['TT'], 'dùng T*/T₀ = 2/(k+1) cho áp suất', 'uses T*/T₀ = 2/(k+1) for the pressure'), (P0 * c['rr'], 'dùng ρ*/ρ₀ (mũ 1/(k−1))', 'uses ρ*/ρ₀ (exponent 1/(k−1))'), (P0 * c['TT'] ** ((k_ - 1) / k_), 'đảo mũ (k−1)/k', 'inverts the exponent (k−1)/k')],
         'kPa', 1, f'P*/P₀ = (2/(k+1))^(k/(k−1)) = (2/{N(k_+1,3)})^({N(k_,3)}/{N(k_-1,3)}) = {N(c["PP"],4)}; P* = {N(c["PP"],4)} × {P0:g} = {N(Ps,1)} kPa; T* = {N(c["TT"],4)} × {T0:g} = {N(Ts,1)} K. Các phương án còn lại:', f'P*/P₀ = (2/(k+1))^(k/(k−1)) = (2/{N(k_+1,3)})^({N(k_,3)}/{N(k_-1,3)}) = {N(c["PP"],4)}; P* = {N(c["PP"],4)} × {P0:g} = {N(Ps,1)} kPa; T* = {N(c["TT"],4)} × {T0:g} = {N(Ts,1)} K. The other options:',
         2, TOP['crit'], GS_('tính chất tới hạn theo khí', 'critical properties by gas'), 'script (verify_m05: numerical flux maximum)', sep=0.02))
# ---------------------------------------------------------------- G8: choked mass flow, unit trap (level 3)
for key, A, P0, T0 in (('air', 12.0, 800.0, 500.0), ('He', 5.0, 1200.0, 400.0), ('CO2', 20.0, 500.0, 450.0), ('N2', 8.0, 1000.0, 600.0)):
    k_, R_, nv, ne = gd(key); m = reg('choked', dict(A=A * 1e-4, P0=P0, T0=T0, k=k_, R=R_), 'mdot', mdot_choked(A * 1e-4, P0, T0, k_, R_), 1e-9, f'G8 {key}')
    lit = A * 1e-4 * P0 * math.sqrt(k_ / (R_ * T0)) * (2 / (k_ + 1)) ** ((k_ + 1) / (2 * (k_ - 1)))
    g(gq(f'Vòi phun nghẹt, diện tích cổ họng {A:g} cm². {nv[0].upper()+nv[1:]} ({kR_vi(k_,R_)}) có P₀ = {P0:g} kPa, T₀ = {T0:g} K. Lưu lượng khối ṁ_max = A*P₀√(k/(RT₀))(2/(k+1))^((k+1)/(2(k−1))) (đơn vị SI đúng) là:', f'A choked nozzle with a throat area of {A:g} cm². {ne[0].upper()+ne[1:]} ({kRs(k_,R_)}) has P₀ = {P0:g} kPa, T₀ = {T0:g} K. The mass flow ṁ_max = A*P₀√(k/(RT₀))(2/(k+1))^((k+1)/(2(k−1))) (correct SI units) is:',
         m, [(lit, 'thay thẳng kPa và kJ/(kg·K) (thiếu √1000)', 'plugs kPa and kJ/(kg·K) straight in (missing √1000)'), (m * 1000.0, 'P₀ theo Pa và R theo kJ (thừa 10³)', 'P₀ in Pa and R in kJ (extra 10³)'), (m / 10.0, 'đổi cm² → m² bằng 10⁻³ thay vì 10⁻⁴', 'converts cm² → m² with 10⁻³ instead of 10⁻⁴'), (m * math.sqrt(1000.0), 'đổi cả P₀ và R nhưng nhân √1000 lần nữa', 'converts both P₀ and R but multiplies by √1000 again')],
         'kg/s', 3, f'A* = {A:g}×10⁻⁴ m²; P₀ = {N(P0*1000,0)} Pa; R = {N(R_*1000,1)} J/(kg·K); √(k/(RT₀)) = {N(math.sqrt(k_/(R_*1000*T0)),6)} s/m; (2/(k+1))^((k+1)/(2(k−1))) = {N((2/(k_+1))**((k_+1)/(2*(k_-1))),4)}; ṁ = {N(m,3)} kg/s. Thay nguyên văn kPa và kJ/(kg·K) cho {N(lit,4)} kg/s (sai). Các phương án còn lại:',
         f'A* = {A:g}×10⁻⁴ m²; P₀ = {N(P0*1000,0)} Pa; R = {N(R_*1000,1)} J/(kg·K); √(k/(RT₀)) = {N(math.sqrt(k_/(R_*1000*T0)),6)} s/m; (2/(k+1))^((k+1)/(2(k−1))) = {N((2/(k_+1))**((k_+1)/(2*(k_-1))),4)}; ṁ = {N(m,3)} kg/s. Plugging kPa and kJ/(kg·K) literally gives {N(lit,4)} kg/s (wrong). The other options:',
         3, TOP['unit'], GS_('dòng nghẹt, bẫy đơn vị', 'choked flow, unit trap'), 'script (verify_m05: numerical flux maximum + node thermo.js)', sep=0.02))
# ---------------------------------------------------------------- G9: converging nozzle with back pressure (level 3)
for P0, T0, A, Pb, V0 in ((800.0, 500.0, 20.0, 600.0, 0.0), (800.0, 500.0, 20.0, 300.0, 0.0), (500.0, 350.0, 15.0, 350.0, 0.0), (500.0, 350.0, 15.0, 150.0, 0.0), (1000.0, 700.0, 30.0, 700.0, 0.0)):
    r_ = conv_nozzle(Pb, P0, T0, 1.4, 0.287, A * 1e-4)
    for key in ('Pe', 'Ma', 'V', 'mdot'): reg('cnoz', dict(Pb=Pb, P0=P0, T0=T0, k=1.4, R=0.287, A=A * 1e-4), key, r_[key], 1e-9, f'G9 {Pb} {key}')
    mmax = mdot_choked(A * 1e-4, P0, T0, 1.4, 0.287); Tb = T0 * (Pb / P0) ** (0.4 / 1.4); m_as_unchoked = Pb / (0.287 * Tb) * math.sqrt(2000.0 * 1.005 * (T0 - Tb)) * A * 1e-4
    st = 'nghẹt' if r_['choked'] else 'không nghẹt'; se = 'choked' if r_['choked'] else 'not choked'
    g(gq(f'Không khí (k = 1,4; R = 0,287 kJ/(kg·K)) có P₀ = {P0:g} kPa, T₀ = {T0:g} K vào vòi hội tụ có diện tích cửa ra {A:g} cm², xả vào áp suất ngược {Pb:g} kPa. Dòng đẳng entropi. Lưu lượng khối là:', f'Air (k = 1.4; R = 0.287 kJ/(kg·K)) at P₀ = {P0:g} kPa, T₀ = {T0:g} K enters a converging nozzle with an exit area of {A:g} cm² discharging against a back pressure of {Pb:g} kPa. Isentropic flow. The mass flow rate is:',
         r_['mdot'], [(mmax if not r_['choked'] else m_as_unchoked, 'bỏ qua chế độ: dùng ṁ_max (nghẹt)' if not r_['choked'] else 'coi dòng không nghẹt và dùng P_e = P_b thấp hơn P*', 'ignores the regime: uses ṁ_max (choked)' if not r_['choked'] else 'treats the flow as not choked and uses P_e = P_b below P*'),
                      (r_['mdot'] * 0.5283 / 0.6339, 'nhầm tỉ số mật độ tới hạn 0,6339 và P*/P₀', 'mixes up the critical density ratio 0.6339 with P*/P₀'), (r_['mdot'] * math.sqrt(1000.0), 'nhân thừa √1000 (đổi đơn vị hai lần)', 'an extra √1000 (units converted twice)'), (r_['mdot'] / math.sqrt(1000.0), 'thiếu √1000 (kPa và kJ thay thẳng)', 'missing √1000 (kPa and kJ plugged straight in)')],
         'kg/s', 3, f'P*/P₀ = 0,5283 → P* = {N(r_["Pcrit"],1)} kPa; P_b = {Pb:g} kPa {">" if not r_["choked"] else "<"} P* ⇒ {st}, P_e = {N(r_["Pe"],1)} kPa, Ma_e = {N(r_["Ma"],3)}; T_e = {N(r_["Te"],1)} K; V_e = {N(r_["V"],1)} m/s; ρ_e = {N(r_["rho"],3)} kg/m³; ṁ = ρ_eA V_e = {N(r_["mdot"],3)} kg/s (ṁ_max = {N(mmax,3)} kg/s). Các phương án còn lại:',
         f'P*/P₀ = 0.5283 → P* = {N(r_["Pcrit"],1)} kPa; P_b = {Pb:g} kPa {">" if not r_["choked"] else "<"} P* ⇒ {se}, P_e = {N(r_["Pe"],1)} kPa, Ma_e = {N(r_["Ma"],3)}; T_e = {N(r_["Te"],1)} K; V_e = {N(r_["V"],1)} m/s; ρ_e = {N(r_["rho"],3)} kg/m³; ṁ = ρ_eA V_e = {N(r_["mdot"],3)} kg/s (ṁ_max = {N(mmax,3)} kg/s). The other options:',
         3, TOP['back'], GS_('vòi hội tụ theo P_b', 'converging nozzle against P_b'), 'script (verify_m05: energy equation + flux maximum + node thermo.js)', sep=0.02))
# ---------------------------------------------------------------- G10: converging-diverging nozzle areas (level 3)
for key, P0, T0, md, Pe in (('air', 1000.0, 600.0, 2.0, 100.0), ('N2', 800.0, 500.0, 1.5, 100.0), ('air', 1500.0, 700.0, 3.0, 200.0)):
    k_, R_, nv, ne = gd(key); As = md / mdot_choked(1.0, P0, T0, k_, R_) * 1e4; Mae = Ma_of_PP(Pe / P0, k_); Ae = As * AAs(Mae, k_)
    pr_ = dict(P0=P0, T0=T0, k=k_, R=R_, mdot=md, Pe=Pe); reg('cdexit', pr_, 'As', As, 1e-9, f'G10 As {key} {P0}'); reg('cdexit', pr_, 'Mae', Mae, 1e-9, f'G10 Mae'); reg('cdexit', pr_, 'Ae', Ae, 1e-9, f'G10 Ae')
    g(gq(f'{nv[0].upper()+nv[1:]} ({kR_vi(k_,R_)}) có P₀ = {P0:g} kPa, T₀ = {T0:g} K (vận tốc vào ≈ 0) giãn nở đẳng entropi trong vòi hội tụ–phân kỳ tới áp suất cửa ra {Pe:g} kPa, lưu lượng khối {md:g} kg/s. Diện tích cửa ra A_e là:', f'{ne[0].upper()+ne[1:]} ({kRs(k_,R_)}) with P₀ = {P0:g} kPa, T₀ = {T0:g} K (inlet velocity ≈ 0) expands isentropically in a converging–diverging nozzle to an exit pressure of {Pe:g} kPa at a mass flow of {md:g} kg/s. The exit area A_e is:',
         Ae, [(As, 'lấy diện tích cổ họng A* thay cho A_e', 'takes the throat area A* instead of A_e'), (As * crit(k_)['rr'] / (Pe / P0) ** (1.0 / k_), 'quên tỉ số vận tốc, chỉ dùng tỉ số khối lượng riêng ρ*/ρ_e', 'forgets the velocity ratio, uses only the density ratio ρ*/ρ_e'), (As / AAs(Mae, k_), 'chia thay vì nhân cho A/A*', 'divides instead of multiplies by A/A*'), (As * Pe / P0 * 10.0, 'tính A_e theo tỉ lệ P_e/P₀', 'scales A_e by P_e/P₀')],
         'cm²', 2, f'P*/P₀ = {N(crit(k_)["PP"],4)} > P_e/P₀ = {N(Pe/P0,3)} ⇒ cửa ra siêu âm. A* = ṁ/[P₀√(k/(RT₀))(…)] = {N(As,3)} cm²; Ma_e = √({{[(P₀/P_e)^((k−1)/k) − 1]·2/(k−1)}}) = {N(Mae,3)}; A_e/A* = {N(AAs(Mae,k_),3)}; A_e = {N(Ae,2)} cm². Các phương án còn lại:',
         f'P*/P₀ = {N(crit(k_)["PP"],4)} > P_e/P₀ = {N(Pe/P0,3)} ⇒ supersonic exit. A* = ṁ/[P₀√(k/(RT₀))(…)] = {N(As,3)} cm²; Ma_e = √({{[(P₀/P_e)^((k−1)/k) − 1]·2/(k−1)}}) = {N(Mae,3)}; A_e/A* = {N(AAs(Mae,k_),3)}; A_e = {N(Ae,2)} cm². The other options:', 3, TOP['cd'], GS_('diện tích vòi hội tụ–phân kỳ', 'converging–diverging areas'), 'script (verify_m05: flux maximum + brentq on A/A*)', sep=0.02))
# ---------------------------------------------------------------- G11: A/A* (level 2)
for Ma_, k_ in ((0.5, 1.4), (2.5, 1.4), (1.5, 1.33), (3.0, 1.4)):
    a = reg('isenMa', dict(Ma=Ma_, k=k_), 'AA', AAs(Ma_, k_), 1e-9, f'G11 {Ma_} {k_}')
    g(gq(f'Khí lý tưởng k = {k_:g} chảy đẳng entropi qua ống có Ma = {Ma_:g}. Tỉ số diện tích A/A* (A* là diện tích tại Ma = 1) là:', f'An ideal gas with k = {k_:g} flows isentropically through a duct at Ma = {Ma_:g}. The area ratio A/A* (A* the area where Ma = 1) is:',
         a, [(1.0 / a, 'lấy A*/A', 'takes A*/A'), (AAs(Ma_, 1.4 if k_ != 1.4 else 1.3), f'dùng k = {1.4 if k_ != 1.4 else 1.3:g} thay cho {k_:g}', f'uses k = {1.4 if k_ != 1.4 else 1.3:g} instead of {k_:g}'), ((1.0 / Ma_) * ((2 / (k_ + 1)) * (1 + (k_ - 1) / 2 * Ma_ ** 2)) ** ((k_ + 1) / (k_ - 1)), 'dùng mũ (k+1)/(k−1) thay cho (k+1)/(2(k−1))', 'uses the exponent (k+1)/(k−1) instead of (k+1)/(2(k−1))'), (Ma_, 'lấy A/A* = Ma', 'takes A/A* = Ma')],
         '', 3, f'A/A* = (1/Ma)[(2/(k+1))(1 + (k−1)Ma²/2)]^((k+1)/(2(k−1))) = (1/{Ma_:g})[{N(2/(k_+1),4)} × {N(1+(k_-1)/2*Ma_**2,4)}]^{N((k_+1)/(2*(k_-1)),3)} = {N(a,4)}' + (' (A-32 hàng in: ' + {0.5: '1,3398', 2.5: 'không có hàng Ma = 2,5', 3.0: '4,2346'}.get(Ma_, 'k khác 1,4 nên không dùng A-32') + ')') + '. Các phương án còn lại:',
         f'A/A* = (1/Ma)[(2/(k+1))(1 + (k−1)Ma²/2)]^((k+1)/(2(k−1))) = (1/{Ma_:g})[{N(2/(k_+1),4)} × {N(1+(k_-1)/2*Ma_**2,4)}]^{N((k_+1)/(2*(k_-1)),3)} = {N(a,4)}' + (' (A-32 printed row: ' + {0.5: '1.3398', 2.5: 'no row at Ma = 2.5', 3.0: '4.2346'}.get(Ma_, 'k differs from 1.4 so A-32 does not apply') + ')') + '. The other options:', 2, TOP['area'], GS_('A/A* theo Ma', 'A/A* from Ma'), 'script (verify_m05: flux ratio; A-32 printed rows)', sep=0.02))
# ---------------------------------------------------------------- G12: Ma2, P2 in a varying-area duct (level 3)
for Ma1, red, T1, P1, kind in ((0.4, 0.8, 350.0, 200.0, 'sub'), (0.5, 0.85, 300.0, 150.0, 'sub'), (2.0, 1.2, 300.0, 100.0, 'sup'), (1.5, 0.9, 400.0, 250.0, 'sup')):
    k_ = 1.4; M2 = Ma_of_AA(AAs(Ma1, k_) * red, k_, kind); P2 = P1 * PP0(M2, k_) / PP0(Ma1, k_); T2 = T1 * TT0(M2, k_) / TT0(Ma1, k_)
    pr_ = dict(Ma1=Ma1, A2A1=red, k=k_, branch=kind, T1=T1, P1=P1); reg('duct', pr_, 'Ma2', M2, 1e-9, f'G12 Ma2 {Ma1} {red}'); reg('duct', pr_, 'P2', P2, 1e-9, f'G12 P2 {Ma1} {red}'); reg('duct', pr_, 'T2', T2, 1e-9, f'G12 T2 {Ma1} {red}')
    other = 'sup' if kind == 'sub' else 'sub'; Mo = Ma_of_AA(AAs(Ma1, k_) * red, k_, other); Po = P1 * PP0(Mo, k_) / PP0(Ma1, k_)
    cvg = red < 1
    g(gq(f'Không khí (k = 1,4) chảy đẳng entropi vào ống tại Ma₁ = {Ma1:g}, P₁ = {P1:g} kPa, T₁ = {T1:g} K. Diện tích dòng chảy {"giảm" if cvg else "tăng"} còn A₂ = {red:g}A₁ ({"ống hội tụ" if cvg else "ống phân kỳ"}). Áp suất P₂ là:', f'Air (k = 1.4) flows isentropically into a duct at Ma₁ = {Ma1:g}, P₁ = {P1:g} kPa, T₁ = {T1:g} K. The flow area {"decreases" if cvg else "increases"} to A₂ = {red:g}A₁ ({"converging duct" if cvg else "diverging duct"}). The pressure P₂ is:',
         P2, [(Po, f'chọn nhầm nghiệm {"siêu âm" if kind == "sub" else "cận âm"} của A₂/A*', f'takes the {"supersonic" if kind == "sub" else "subsonic"} root of A₂/A* by mistake'), (P1 * PP0(M2, k_), 'quên chia cho P₁/P₀ (lấy P₂/P₀ nhân P₁)', 'forgets to divide by P₁/P₀ (takes P₂/P₀ times P₁)'), (P1 * red, 'lấy P tỉ lệ với A', 'takes P proportional to A'), (P1 * TT0(M2, k_) / TT0(Ma1, k_), 'dùng T₂/T₁ thay cho P₂/P₁', 'uses T₂/T₁ instead of P₂/P₁')],
         'kPa', 1, f'A₁/A* = {N(AAs(Ma1,k_),4)}; A₂/A* = {red:g} × {N(AAs(Ma1,k_),4)} = {N(AAs(Ma1,k_)*red,4)}; nhánh {"cận âm" if kind=="sub" else "siêu âm"} (dòng đầu {"cận âm" if kind=="sub" else "siêu âm"}): Ma₂ = {N(M2,4)}. P₂ = P₁(P₂/P₀)/(P₁/P₀) = {P1:g} × {N(PP0(M2,k_),4)}/{N(PP0(Ma1,k_),4)} = {N(P2,1)} kPa (T₂ = {N(T2,1)} K). Các phương án còn lại:',
         f'A₁/A* = {N(AAs(Ma1,k_),4)}; A₂/A* = {red:g} × {N(AAs(Ma1,k_),4)} = {N(AAs(Ma1,k_)*red,4)}; {"subsonic" if kind=="sub" else "supersonic"} branch (the flow starts {"subsonic" if kind=="sub" else "supersonic"}): Ma₂ = {N(M2,4)}. P₂ = P₁(P₂/P₀)/(P₁/P₀) = {P1:g} × {N(PP0(M2,k_),4)}/{N(PP0(Ma1,k_),4)} = {N(P2,1)} kPa (T₂ = {N(T2,1)} K). The other options:', 3, TOP['area'], GS_('Ma₂, P₂ khi diện tích đổi', 'Ma₂, P₂ with an area change'), 'script (verify_m05: Hugoniot ODE + brentq)', sep=0.02))
# ---------------------------------------------------------------- G13: Pitot, flight speed (level 3)
for P, T, dP in ((54.05, 255.7, 20.0), (26.5, 223.3, 30.0), (101.325, 288.15, 15.0)):
    P0 = P + dP; Ma = reg('pitot', dict(P=P, T=T, dP=dP, k=1.4, R=0.287), 'Ma', Ma_of_PP(P / P0, 1.4), 1e-9, f'G13 Ma {P}'); V = reg('pitot', dict(P=P, T=T, dP=dP, k=1.4, R=0.287), 'V', Ma * csound(1.4, 0.287, T), 1e-9, f'G13 V {P}')
    g(gq(f'Máy bay cận âm bay ở độ cao có P = {P:g} kPa, T = {T:g} K (k = 1,4; R = 0,287). Ống Pitot đo P₀ − P = {dP:g} kPa. Tốc độ bay là:', f'A subsonic aircraft flies where P = {P:g} kPa, T = {T:g} K (k = 1.4; R = 0.287). A Pitot probe measures P₀ − P = {dP:g} kPa. The flight speed is:',
         V, [(csound(1.4, 0.287, T) * math.sqrt((P0 / P) ** (0.4 / 1.4) - 1.0), 'quên hệ số 2/(k−1) = 5 trong biểu thức Ma', 'forgets the factor 2/(k−1) = 5 in the Ma expression'), (csound(1.4, 0.287, T) * math.sqrt(5.0 * ((P0 / P) ** (1.4 / 0.4) - 1.0)), 'dùng mũ k/(k−1) thay cho (k−1)/k', 'uses the exponent k/(k−1) instead of (k−1)/k'),
              (Ma * 340.0, 'dùng c = 340 m/s mặc định', 'uses the default c = 340 m/s'), (math.sqrt(2.0 * dP * 1000.0 / (P / (0.287 * T))), 'Bernoulli không nén được V = √(2ΔP/ρ)', 'incompressible Bernoulli V = √(2ΔP/ρ)')],
         'm/s', 0, f'P₀ = {N(P0,2)} kPa; P/P₀ = {N(P/P0,4)} ⇒ Ma = √({{[(P₀/P)^0,2857 − 1]/0,2}}) = {N(Ma,3)}; c = √(1,4 × 287 × {T:g}) = {N(csound(1.4,0.287,T),1)} m/s; V = Ma·c = {N(V,0)} m/s. Các phương án còn lại:', f'P₀ = {N(P0,2)} kPa; P/P₀ = {N(P/P0,4)} ⇒ Ma = √({{[(P₀/P)^0.2857 − 1]/0.2}}) = {N(Ma,3)}; c = √(1.4 × 287 × {T:g}) = {N(csound(1.4,0.287,T),1)} m/s; V = Ma·c = {N(V,0)} m/s. The other options:',
         3, TOP['stag'], GS_('ống Pitot', 'Pitot probe'), 'script (verify_m05: energy equation + brentq)', sep=0.02))
# ---------------------------------------------------------------- G14: area at another Mach number (level 3)
for Ma1, A1, Ma2 in ((0.5, 30.0, 0.8), (2.0, 10.0, 3.0), (0.3, 40.0, 0.7)):
    A2 = reg('areaMa', dict(Ma1=Ma1, A1=A1, Ma2=Ma2, k=1.4), 'A2', A1 * AAs(Ma2, 1.4) / AAs(Ma1, 1.4), 1e-9, f'G14 {Ma1} {Ma2}')
    g(gq(f'Dòng không khí đẳng entropi (k = 1,4) trong ống thu–giãn có diện tích {A1:g} cm² tại Ma = {Ma1:g}. Diện tích tại vị trí Ma = {Ma2:g} (cùng nhánh {"cận âm" if Ma1 < 1 else "siêu âm"}) là:', f'Isentropic airflow (k = 1.4) in a converging–diverging duct has an area of {A1:g} cm² at Ma = {Ma1:g}. The area where Ma = {Ma2:g} (same {"subsonic" if Ma1 < 1 else "supersonic"} branch) is:',
         A2, [(A1 * AAs(Ma1, 1.4) / AAs(Ma2, 1.4), 'đảo tỉ số diện tích', 'inverts the area ratio'), (A1 * Ma1 / Ma2, 'giả thiết A tỉ lệ nghịch với Ma', 'assumes A inversely proportional to Ma'), (A1 * AAs(Ma2, 1.4), 'quên chia cho A₁/A*', 'forgets to divide by A₁/A*'), (A1 * (AAs(Ma2, 1.4) - AAs(Ma1, 1.4)), 'lấy hiệu A/A* thay cho tỉ số', 'takes the difference of A/A* instead of the ratio')],
         'cm²', 2, f'A/A* = {N(AAs(Ma1,1.4),4)} tại Ma = {Ma1:g} và {N(AAs(Ma2,1.4),4)} tại Ma = {Ma2:g}: A₂ = {A1:g} × {N(AAs(Ma2,1.4),4)}/{N(AAs(Ma1,1.4),4)} = {N(A2,2)} cm². Các phương án còn lại:', f'A/A* = {N(AAs(Ma1,1.4),4)} at Ma = {Ma1:g} and {N(AAs(Ma2,1.4),4)} at Ma = {Ma2:g}: A₂ = {A1:g} × {N(AAs(Ma2,1.4),4)}/{N(AAs(Ma1,1.4),4)} = {N(A2,2)} cm². The other options:',
         3, TOP['area'], GS_('diện tích theo Ma', 'area against Ma'), 'script (verify_m05: flux ratio)', sep=0.02))

# ================================================================== write everything
def main():
    orig = O1.build() + O2.build() + O3.build() + O4.build(); conc = CO.build(); items_src = orig + conc
    closed = [i for i in items_src + G if i['kind'] != 'ess']; l3 = [i for i in closed if i['level'] == 3]
    sa = os.path.join(ROOT, 'data', 'qsrc'); os.makedirs(sa, exist_ok=True)
    dump(os.path.join(sa, 'm05.json'), items_src); dump(os.path.join(sa, 'm05_gen.json'), G)
    dump(os.path.join(ROOT, 'data', 'verify', 'm05_values.json'), dict(registry=REG, printed=PRN))
    notes = NT.build(); dump(os.path.join(ROOT, 'data', 'verify', 'm05_notes.json'), notes)
    print(f'originals+conceptual {len(items_src)} (ess {sum(1 for i in items_src if i["kind"]=="ess")}, goc closed {sum(1 for i in items_src if i["kind"]!="ess" and i["origin"]=="goc")}) | generated {len(G)} | closed {len(closed)} | level 3: {len(l3)} ({100*len(l3)/len(closed):.0f} %) | registry {len(REG)} | printed {len(PRN)} | notes vi {len(notes["vi"])} en {len(notes["en"])}')
if __name__ == '__main__': main()
