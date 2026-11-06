"""Jaeger 5e chapter 7 (CMOS) problems, solved with the book's own equations; constants of Table 7.1: K'n = 100 uA/V^2, K'p = 40 uA/V^2 (checked by the book's exercises:
reference inverter tau = 3.16 ns/pF with Eq. 7.15 and peak current 42.3 uA).  Independent check: the voltage-transfer curve is simulated numerically (piecewise square-law)."""
import math
from core import *
KN, KP = 100e-6, 40e-6
EOX = 3.9 * 8.854e-14                                            # F/cm

def vsp(vdd, vtn, vtp, kr): s = math.sqrt(kr); return (vdd + vtp + vtn * s) / (1 + s)

def vtc(vi, vdd, vtn, vtp, kn, kp):
    """output voltage for input vi: solve iN(vo) = iP(vo) by bisection with the full piecewise square-law model."""
    def iN(vo):
        vgs, vds = vi, vo
        if vgs <= vtn: return 0.0
        return kn * ((vgs - vtn) * vds - vds * vds / 2) if vds < vgs - vtn else kn / 2 * (vgs - vtn) ** 2
    def iP(vo):
        vsg, vsd = vdd - vi, vdd - vo; vt = -vtp
        if vsg <= vt: return 0.0
        return kp * ((vsg - vt) * vsd - vsd * vsd / 2) if vsd < vsg - vt else kp / 2 * (vsg - vt) ** 2
    lo, hi = 0.0, vdd
    for _ in range(80):
        mid = (lo + hi) / 2
        if iN(mid) - iP(mid) > 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

def nm_closed(vdd, vtn, vtp, kr):
    VIH = 2 * kr * (vdd - vtn + vtp) / ((kr - 1) * math.sqrt(1 + 3 * kr)) - (vdd - kr * vtn + vtp) / (kr - 1) if abs(kr - 1) > 1e-9 else (5 * vdd + 3 * vtn + 5 * vtp) / 8
    VOL = ((kr + 1) * VIH - vdd - kr * vtn - vtp) / (2 * kr) if abs(kr - 1) > 1e-9 else (vdd - vtn + vtp) / 8
    VIL = 2 * math.sqrt(kr) * (vdd - vtn + vtp) / ((kr - 1) * math.sqrt(kr + 3)) - (vdd - kr * vtn + vtp) / (kr - 1) if abs(kr - 1) > 1e-9 else (3 * vdd + 5 * vtn + 3 * vtp) / 8
    VOH = ((kr + 1) * VIL + vdd - kr * vtn - vtp) / 2 if abs(kr - 1) > 1e-9 else (7 * vdd + vtn - vtp) / 8
    return VIL, VIH, VOL, VOH, VIL - VOL, VOH - VIH           # NML, NMH
def nm_numeric(vdd, vtn, vtp, kr):
    kn, kp = 1.0, 1.0 / kr; h = 1e-5; sl = lambda v: (vtc(v + h, vdd, vtn, vtp, kn, kp) - vtc(v - h, vdd, vtn, vtp, kn, kp)) / (2 * h)
    # slope -1 on both sides of the switching threshold
    vs = vsp(vdd, vtn, vtp, kr); lo, hi = vtn + 1e-3, vs
    for _ in range(60):                                       # VIL: slope crosses -1 below vs
        m = (lo + hi) / 2
        if sl(m) > -1: lo = m
        else: hi = m
    VIL = (lo + hi) / 2; lo, hi = vs, vdd + vtp - 1e-3
    for _ in range(60):
        m = (lo + hi) / 2
        if sl(m) < -1: lo = m
        else: hi = m
    VIH = (lo + hi) / 2
    VOH = vtc(VIL, vdd, vtn, vtp, kn, kp); VOL = vtc(VIH, vdd, vtn, vtp, kn, kp)
    return VIL, VIH, VOL, VOH, VIL - VOL, VOH - VIH

def delays(vdd, vtn, vtp, wn, wp, c, k=2.4):
    kn, kp = KN * wn, KP * wp
    phl = k * c / (kn * (vdd - vtn)); plh = k * c / (kp * (vdd + vtp)); return phl, plh, (phl + plh) / 2

def two(x, unit): return si(x, unit)
def dly(vdd, vtn, vtp, wn, wp, c):
    a = delays(vdd, vtn, vtp, wn, wp, c, 2.4); b = delays(vdd, vtn, vtp, wn, wp, c, 1.2)
    return [('τPHL, τPLH, τP (Eq. 7.23, 2.4·Ron·C)', f'{si(a[0], "s")}, {si(a[1], "s")}, {si(a[2], "s")}'), ('tf = 2τPHL, tr = 2τPLH (Eq. 7.19)', f'{si(2 * a[0], "s")}, {si(2 * a[1], "s")}'),
            ('with the first estimate 1.2·Ron·C (Eq. 7.15/7.18)', f'τP = {si(b[2], "s")}, tf = {si(2 * b[0], "s")}, tr = {si(2 * b[1], "s")}')], a
DELAY_NOTE = 'The book gives two estimates: Eq. (7.15)/(7.18) with 1.2·Ron·C and, after the SPICE comparison of Fig. 7.15, the revised Eq. (7.23) with 2.4·Ron·C. Both are listed.'

@solve('6.33')
def _(): 
    L, W, t = 0.375, 1.5e-4, 1e-4; c1 = EOX * L * W / t; return [('Parallel-plate capacitance', si(c1, 'F')), ('Total capacitance (3 × parallel plate)', si(3 * c1, 'F'))], 'C = εox·L·W/tox with L = 3.75 mm, W = 1.5 μm, tox = 1 μm, then ×3.', []
@solve('7.1')
def _():
    r = []
    for tox in (10e-7, 5e-7):
        kn, kp = 500 * EOX / tox, 200 * EOX / tox; r.append((f'tox = {int(tox * 1e7)} nm: K′n, K′p', f'{g(kn * 1e6)} μA/V², {g(kp * 1e6)} μA/V²'))
    return r, "K′ = μ·Cox″ with Cox″ = εox/tox, εox = 3.9·8.854×10⁻¹⁴ F/cm, 1 nm = 10⁻⁷ cm.", []
@solve('7.3')
def _():
    a = 500e-12 * 0.5; per = 100e-12 * (2e-4 * 5e-4); n = 20e6
    return [('(a) n-well leakage', si(a, 'A')), ('(b) vO = 2.5 V: one reverse-biased junction per inverter (NMOS drain)', f'{si(per * n, "A")} (plus the well: {si(per * n + a, "A")})'), ('(c) vO = 0 V: the PMOS drain is the reverse-biased junction', f'{si(per * n, "A")} (plus the well: {si(per * n + a, "A")})')], 'I = J·A; per inverter one 2 μm × 5 μm drain junction is reverse biased; × 20 million inverters.', ['The n-well of part (a) is counted separately; the totals with the well are shown in brackets.']
@solve('7.4')
def _(): 
    L, W, t = 0.5, 1e-4, 1e-4; c1 = EOX * L * W / t; return [('Parallel-plate capacitance', si(c1, 'F')), ('Total capacitance (3 × parallel plate)', si(3 * c1, 'F'))], 'C = εox·L·W/tox with L = 5 mm, W = 1 μm, tox = 1 μm, then ×3.', []
def vsp_block(vdd, vtn, vtp, wn, wp_ratio_kr):
    out = []
    for kr, tag in ((1.0, 'Kn = Kp'), (2.5, 'Kn = 2.5Kp')):
        v = vsp(vdd, vtn, vtp, kr); kn = KN * 2; i = kn / 2 * (v - vtn) ** 2
        # independent check: vO = vI on the numerically simulated VTC
        kp = kn / kr; lo, hi = 0.0, vdd
        for _ in range(70):
            m = (lo + hi) / 2
            if vtc(m, vdd, vtn, vtp, kn, kp) > m: lo = m
            else: hi = m
        close(v, (lo + hi) / 2, 2e-3); out.append((f'{tag}: vO = vI at', f'{g(v)} V; IDD = {si(i, "A")} with (W/L)N = 2/1'))
    return out
@solve('7.10')
def _(): return vsp_block(2.5, 0.6, -0.6, 2, None), 'KR = Kn/Kp; vO = vI where both devices are saturated: vI = (VDD + VTP + VTN√KR)/(1 + √KR); IDD = (Kn/2)(vI − VTN)² with Kn = K′n·2 = 200 μA/V².', ['K′n = 100 μA/V² (Table 7.1).']
@solve('7.11')
def _(): return [('(a) VDD = 3.3 V, VTN = 0.75 V, VTP = −0.75 V', '')] + vsp_block(3.3, 0.75, -0.75, 2, None) + [('(b) VDD = 2.5 V, VTN = 0.60 V, VTP = −0.50 V', '')] + vsp_block(2.5, 0.6, -0.5, 2, None), 'Same method as Problem 7.10.', ['K′n = 100 μA/V².']
@solve('7.12')
def _(): return [('(a) VDD = 1.8 V, VT = ±0.45 V', '')] + vsp_block(1.8, 0.45, -0.45, 2, None) + [('(b) VDD = 2.5 V, VTN = 0.75 V, VTP = −0.65 V', '')] + vsp_block(2.5, 0.75, -0.65, 2, None) + [('(c) VDD = 2.5 V, VTN = 0.65 V, VTP = −0.75 V', '')] + vsp_block(2.5, 0.65, -0.75, 2, None), 'Same method as Problem 7.10.', ['K′n = 100 μA/V².']
@solve('7.15')
def _(): v = vsp(2.5, 0.6, -0.6, 2.5); return [('Switching threshold (KR = 2.5)', f'{g(v)} V')], 'W/L = 2/1 for both: Kn/Kp = K′n/K′p = 2.5, vI = (VDD + VTP + VTN√KR)/(1 + √KR).', []
@solve('7.16')
def _(): v = vsp(1.8, 0.45, -0.45, 2.5); return [('Switching threshold (KR = 2.5)', f'{g(v)} V')], 'Same method as Problem 7.15.', []
def nm_parts(vdd, vt, kr):
    c = nm_closed(vdd, vt, -vt, kr); n = nm_numeric(vdd, vt, -vt, kr)
    for a, b in zip(c, n): close(a, b, 2e-3, 2e-4)
    return [('VIL, VIH', f'{g(c[0])} V, {g(c[1])} V'), ('VOL, VOH', f'{g(c[2])} V, {g(c[3])} V'), ('NML, NMH', f'{g(c[4])} V, {g(c[5])} V')]
@solve('7.17')
def _(): return nm_parts(2.5, 0.6, 2.5), 'Eqs. (7.7)–(7.12) with KR = 2.5, checked against the simulated transfer curve (slope = −1 points).', []
@solve('7.18')
def _(): return [('(a) symmetrical (KR = 1): NML, NMH', f'{g((3.3 + 3 * .75 - .75) / 4)} V, {g((3.3 - .75 + 3 * .75) / 4)} V')] + [('(b) (W/L)N = (W/L)P → KR = 2.5', '')] + nm_parts(3.3, 0.75, 2.5), 'Eq. (7.14) for KR = 1 (checked numerically); Eqs. (7.7)–(7.12) for KR = 2.5.', []
@solve('7.23')
def _():
    vdd, vtn, vtp = 5.0, 0.6, -0.6; vl, vh = 0.6, 2.4
    kn = 1.5e-3 / ((vdd - vtn) * vl - vl * vl / 2); kp = 60e-6 / ((vdd + vtp) * (vdd - vh) - (vdd - vh) ** 2 / 2)
    # independent check: plug the sizes back into the transistor equations
    close(kn * ((vdd - vtn) * vl - vl ** 2 / 2), 1.5e-3); close(kp * ((vdd + vtp) * (vdd - vh) - (vdd - vh) ** 2 / 2), 60e-6)
    return [('Kn, (W/L)N minimum', f'{g(kn * 1e3)} mA/V², {g(kn / KN)}/1'), ('Kp, (W/L)P minimum', f'{g(kp * 1e6)} μA/V², {g(kp / KP)}/1')], 'Output low: NMOS (vGS = 5 V) in the triode region, iD = Kn[(VDD−VTN)vDS − vDS²/2] = 1.5 mA at vDS = 0.6 V. Output high: PMOS in the triode region, iD = Kp[(VDD−|VTP|)vSD − vSD²/2] = 60 μA at vSD = 2.6 V.', ['VTN = 0.6 V, VTP = −0.6 V and K′n = 100, K′p = 40 μA/V² (not given in the statement).']
@solve('7.24')
def _():
    out = []
    for vdd, tag in ((2.5, 'a'), (2.0, 'b'), (1.8, 'c')):
        parts, a = dly(vdd, 0.6, -0.6, 2, 5, 0.3e-12); out.append((f'({tag}) VDD = {vdd} V', '')); out += parts
    return out, 'τPHL = 2.4·Ronn·C with Ronn = 1/[Kn(VDD − VTN)], τPLH likewise with Kp(VDD + VTP); tr = 2τPLH, tf = 2τPHL, τP = average. ' + DELAY_NOTE, ['VTN = −VTP = 0.6 V for all three supplies (the statement gives no other value).']
def asym(vtn, vtp, wn, wp, c, vdds, kr):
    out = []
    for vdd in vdds:
        parts, a = dly(vdd, vtn, vtp, wn, wp, c); kn, kp = KN * wn, KP * wp; v = vsp(vdd, vtn, vtp, kn / kp)
        out.append((f'VDD = {vdd} V: switching threshold', f'{g(v)} V')); out += parts
    return out
@solve('7.25')
def _(): return asym(0.55, -0.65, 2, 5, 0.3e-12, (2.5, 1.8, 3.3), 1), 'As Problem 7.24(a) with VTN = 0.55 V, VTP = −0.65 V; threshold vI = (VDD + VTP + VTN√KR)/(1 + √KR), KR = Kn/Kp = 1. ' + DELAY_NOTE, ['C = 0.3 pF as in Problem 7.24.']
@solve('7.26')
def _(): return asym(0.65, -0.55, 2, 5, 0.3e-12, (2.5, 1.8, 3.3), 1), 'As Problem 7.25 with VTN = 0.65 V, VTP = −0.55 V. ' + DELAY_NOTE, ['C = 0.3 pF as in Problem 7.24.']
@solve('7.27')
def _(): parts, a = dly(2.5, 0.6, -0.6, 2, 2, 0.5e-12); return parts, 'Kn = 200 μA/V², Kp = 80 μA/V² (both 2/1). ' + DELAY_NOTE, ['VTN = −VTP = 0.6 V.']
@solve('7.28')
def _(): parts, a = dly(2.5, 0.65, -0.55, 2, 2, 0.5e-12); v = vsp(2.5, .65, -.55, 2.5); return parts + [('Switching threshold (KR = 2.5)', f'{g(v)} V')], 'As Problem 7.27 with VTN = 0.65 V, VTP = −0.55 V. ' + DELAY_NOTE, []
@solve('7.29')
def _(): parts, a = dly(3.3, 0.75, -0.75, 2, 5, 0.25e-12); return parts, DELAY_NOTE, []
@solve('7.30')
def _(): parts, a = dly(2.5, 0.6, -0.6, 2, 5, 0.1e-12); return parts, DELAY_NOTE, []
def design(tau, c, vdd, vtn, vtp):
    out = []
    for k, tag in ((2.4, 'Eq. 7.23 (2.4·Ron·C)'), (1.2, 'Eq. 7.15/7.18 (1.2·Ron·C)')):
        kn = k * c / (tau * (vdd - vtn)); kp = k * c / (tau * (vdd + vtp)); out.append((tag, f'(W/L)N = {g(kn / KN)}/1, (W/L)P = {g(kp / KP)}/1'))
        close(k * c / (kn * (vdd - vtn)), tau); close(k * c / (kp * (vdd + vtp)), tau)
    return out
@solve('7.31')
def _():
    out = design(3e-9, 1e-12, 2.5, 0.6, -0.6)
    wn12 = 1.2 * 1e-12 / (3e-9 * (2.5 - 0.6)) / KN          # 1.2 version solved directly
    close(wn12, 2 * (3.16e-9 / 1e-12) * 1e-12 / 3e-9, 5e-3)   # = scaling of the reference inverter (2/1, 3.16 ns per pF) by Eq. (7.20)
    return out, 'τP = k·C/[Kn(VDD − VTN)] with equal rise and fall times (Kp = Kn) solved for Kn and Kp. The 1.2 version agrees with scaling the reference inverter of Fig. 7.12 by Eq. (7.20). ' + DELAY_NOTE, []
@solve('7.33')
def _(): return [('(a) VDD = 2.5 V', '')] + design(1e-9, 10e-12, 2.5, .6, -.6) + [('(b) VDD = 1.8 V, VT = ±0.45 V', '')] + design(1e-9, 10e-12, 1.8, .45, -.45), 'As Problem 7.31. ' + DELAY_NOTE, ['Part (a): VT = ±0.6 V.']
@solve('7.35')
def _(): return design(400e-12, 200e-15, 2.5, .6, -.6), 'As Problem 7.31. ' + DELAY_NOTE, []
@solve('7.37')
def _(): return design(250e-12, 120e-15, 1.5, .5, -.5), 'As Problem 7.31. ' + DELAY_NOTE, []
@solve('7.41')
def _():
    # tau ~ 1/(Kn (VDD - VTN)); sensitivities by finite differences as a check
    f = lambda kn, vt, vdd=2.5: 1 / (kn * (vdd - vt)); h = 1e-6; S_k = (1.0 / f(1, .75)) * (f(1 + h, .75) - f(1 - h, .75)) / (2 * h); close(S_k, -1.0, 1e-4)
    S_v = .75 / f(1, .75) * (f(1, .75 + h) - f(1, .75 - h)) / (2 * h); close(S_v, .75 / (2.5 - .75), 1e-4)
    return [('(a) S(Kn) = (Kn/τ)(dτ/dKn)', g(S_k)), ('(a) Kn 25 % low', f'τp increases by {g(100 * (1 / .75 - 1))} % exactly ({g(25)} % by the linearised sensitivity)'), ('(b) S(VTN) = VTN/(VDD − VTN)', g(S_v)), ('(b) VTN 0.75 V → 0.85 V', f'τp increases by {g(100 * ((2.5 - .75) / (2.5 - .85) - 1))} %')], 'τp ∝ 1/[Kn(VDD − VTN)] from Eq. (7.18); the sensitivity of a power law is its exponent.', ['VDD = 2.5 V in part (b) (not given in the statement).']
@solve('7.51')
def _(): return [('(a) average power per gate', si(100 / 500e6, 'W')), ('(b) supply current at 1.8 V', si(100 / 1.8, 'A'))], 'P/N and I = P/VDD.', []
@solve('7.52')
def _():
    p = 5 / 10e6; out = [('Power per gate', si(p, 'W'))]
    for v in (3.3, 2.5, 1.8): c = p / (v * v * 100e6); out.append((f'VDD = {v} V: C max (P = C·VDD²·f)', si(c, 'F')))
    return out, 'P = 5 W/10⁷ gates; Eq. (7.24) P = C·VDD²·f solved for C at f = 100 MHz.', []
@solve('7.53')
def _():
    a = 400e-12 * (0.5 * 1.0); per = 150e-12 * (0.5e-4 * 1.25e-4); n = 200e6
    return [('(a) n-well leakage', si(a, 'A')), ('(b) vO = 2.5 V: reverse-biased NMOS drain junctions', si(per * n, 'A')), ('(c) vO = 0 V: reverse-biased PMOS drain junctions', si(per * n, 'A'))], 'I = J·A; the well is 0.5 cm × 1 cm; each drain is 0.5 μm × 1.25 μm = 6.25×10⁻⁹ cm²; × 200 million inverters.', ['The well leakage of part (a) is not added to (b) and (c).']
@solve('7.54')
def _():
    out = []
    for v in (2.5, 3.3): p = 64 * 25e-12 * v * v * (1 / (2 * 2e-9)); out.append((f'VDD = {v} V', si(p, 'W')))
    return out, 'P = N·C·VDD²·f with f the full switching cycle rate: each line changes at every 2 ns access, so a charge-discharge cycle lasts 4 ns (f = 250 MHz).', ['If f were taken as the access rate 500 MHz the powers double.']
@solve('7.55')
def _():
    r = 0.1 / 4; kn = 1 / (r * (2.5 - 0.6)); wl = kn / KN; area = wl * 1e-6 * 1e-6
    close(1 / (kn * 1.9), 0.025)
    return [('On-resistance allowed', si(r, 'Ω')), ('Kn needed', f'{g(kn)} A/V²'), ('W/L', f'{g(wl)}'), ('Area W·L (L = 1 μm)', f'{g(wl)} μm² = {g(wl * 1e-6)} mm²')], 'Deep triode: R = 1/[Kn(VGS − VTN)] with VGS = 2.5 V.', ['VTN = 0.6 V and K′n = 100 μA/V² (not given in the statement).']
@solve('7.56')
def _(): t = 0.2 * 100e6 * 50e-15 / 40; return [('Minimum gate delay', si(t, 's'))], 'Each switching gate dissipates PDP/τ; 0.2 × 10⁸ gates × PDP/τ ≤ 40 W.', []
def peak(vdd, vtn, vtp, wn, wp):
    kn, kp = KN * wn, KP * wp; kr = kn / kp; v = vsp(vdd, vtn, vtp, kr); i = kn / 2 * (v - vtn) ** 2
    close(i, kp / 2 * (vdd - v + vtp) ** 2)                  # the PMOS carries the same current at that input
    return v, i
@solve('7.57')
def _():
    out = []
    for vdd in (3.3, 2.5): v, i = peak(vdd, .6, -.6, 15, 15); out.append((f'VDD = {vdd} V', f'peak IDD = {si(i, "A")} at vI = {g(v)} V'))
    return out, 'Both devices saturated at vI = switching threshold: IDD,max = (Kn/2)(vI − VTN)², Kn = 15·K′n.', ['VTN = −VTP = 0.6 V, K′n = 100, K′p = 40 μA/V².']
@solve('7.58')
def _():
    v1, i1 = peak(1.8, .6, -.6, 15, 15); v2, i2 = peak(2.5, .55, -.65, 15, 15)
    return [('(a) VDD = 1.8 V', f'peak IDD = {si(i1, "A")} at vI = {g(v1)} V'), ('(b) VDD = 2.5 V, VTN = 0.55 V, VTP = −0.65 V', f'peak IDD = {si(i2, "A")} at vI = {g(v2)} V')], 'As Problem 7.57.', ['Part (a) keeps VT = ±0.6 V (not restated).']
@solve('7.59')
def _():
    a = peak(3.3, .8, -.8, 2, 5); b = peak(2.0, .5, -.5, 2, 5)
    return [('(a) VDD = 3.3 V, VT = ±0.8 V', f'peak IDD = {si(a[1], "A")} at vI = {g(a[0])} V'), ('(b) VDD = 2.0 V, VT = ±0.5 V', f'peak IDD = {si(b[1], "A")} at vI = {g(b[0])} V')], 'Symmetrical inverter: Kn = Kp = 200 μA/V², vI = VDD/2.', []
@solve('7.60')
def _():
    a = peak(2.0, .45, -.55, 2, 5); b = peak(2.0, .55, -.45, 2, 5)
    return [('(a) VTN = 0.45 V, VTP = −0.55 V', f'peak IDD = {si(a[1], "A")} at vI = {g(a[0])} V'), ('(b) VTN = 0.55 V, VTP = −0.45 V', f'peak IDD = {si(b[1], "A")} at vI = {g(b[0])} V')], 'As Problem 7.59(a) with (W/L)N = 2/1, (W/L)P = 5/1, VDD = 2.0 V.', []
@solve('7.61')
def _():
    c, v = 0.3e-12, 2.5; pdp = c * v * v / 5; p = c * v * v * 100e6; a = delays(2.5, .6, -.6, 2, 5, c, 2.4)[2]
    return [('PDP ≥ C·VDD²/5 (Eq. 7.28)', si(pdp, 'J')), ('Power at 100 MHz (P = C·VDD²·f)', si(p, 'W')), ('Check with PDP = Pav·τP using τP of Problem 7.24(a)', si(p * a, 'J'))], 'Eq. (7.28) is the lower bound of the PDP; the last line is the same quantity from Pav·τP (about 5 % lower because Eq. 7.28 assumes the 80 % transition-time rule).', ['C = 0.3 pF, VDD = 2.5 V as in Problem 7.24(a).']
