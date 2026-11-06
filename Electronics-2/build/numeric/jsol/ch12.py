"""Jaeger 5e chapter 12 (op-amp applications, data converters).  Conventions taken from the book: an n-bit ADC with full scale VFS has LSB = VFS/2^n and code N means
(N − ½)LSB ≤ vX ≤ (N + ½)LSB (Fig. 12.28 and Eq. 12.53); DAC step size and differential error in LSB, integral error = running sum of the differential errors (exercise of Section 12.5.2);
single-ramp/counting converters: TT = N/fC; successive approximation: TT = n/fC; dual ramp: timing error ΔT < 0.1·T1/2^n for 0.1 LSB."""
import math
from core import *
@solve('12.25')
def _():
    n = math.ceil(math.log(5000, 50)); per = 5000 ** (1 / n); two = 50 ** 2
    return [('Maximum gain with 2 stages (≤ 50 each)', g(two) + ' < 5000'), ('Stages needed', f'{n} (≈ {g(per)} = {g(20 * math.log10(per))} dB each, or 50 × 50 × 2 = 5000)')], 'Total gain is the product of the stage gains: 50ⁿ ≥ 5000 gives n ≥ 2.2 → 3 stages. The Rin and Rout requirements need the op-amp table that the statement refers to (not reproduced in the text).', ['Only the gain constraint is evaluated here.']
@solve('12.69')
def _():
    v = [0.0, 0.1, 0.3, 0.35, 0.475, 0.63, 0.725, 0.875]; lsb = (v[-1] - v[0]) / 7
    step = [(v[k] - v[k - 1]) / lsb for k in range(1, 8)]; dnl = [s - 1 for s in step]
    inl = [(v[k] - k * lsb) / lsb for k in range(8)]
    cs = 0.0
    for k in range(1, 8): cs += dnl[k - 1]; close(inl[k], cs, 1e-9, 1e-9)                      # integral error = running sum of the differential errors
    rows = [f'{format(k, "03b")}: step {g(step[k - 1])} LSB, DNL {g(dnl[k - 1])} LSB, INL {g(inl[k])} LSB' for k in range(1, 8)]
    return [('Ideal LSB', f'{g(lsb)} VFS (endpoints 0 and 0.875 VFS)')] + [(r.split(':')[0], r.split(': ')[1]) for r in rows] + [('Largest errors', f'differential {g(max(abs(x) for x in dnl))} LSB, integral {g(max(abs(x) for x in inl))} LSB')], 'Step size = ΔVout/LSB, differential error = step − 1 LSB, integral error = actual output − ideal line through the end points, in LSB; the sum of the differential errors reproduces the integral error.', []
@solve('12.83')
def _():
    n = 14; code = int('10101110110010', 2); lsb = 5.12 / 2 ** n; lo, hi = (code - .5) * lsb, (code + .5) * lsb
    close(hi - lo, lsb); return [('Code (decimal)', str(code)), ('LSB = VFS/2¹⁴', si(lsb, 'V')), ('Input range', f'{g(lo)} V ≤ vX ≤ {g(hi)} V (N·LSB ± ½ LSB, N·LSB = {g(code * lsb)} V)')], 'Eq. (12.53) and Fig. 12.28: the quantization error of an ideal ADC is at most ½ LSB.', ['Range taken as (N ± ½)·LSB as in Fig. 12.28.']
@solve('12.84')
def _():
    n = 20; lsb = 2 / 2 ** n
    def code(v): N = round(v / lsb); return N, format(N, '020b')
    out = [('(a) LSB = VFS/2²⁰', si(lsb, 'V'))]
    for tag, v in (('(b) 1.630500 V', 1.6305), ('(c) 0.997030 V', 0.99703)):
        N, b = code(v); assert abs(N * lsb - v) <= lsb / 2 + 1e-15; out.append((tag, f'N = {N}, code {b} (back-converted {g(N * lsb)} V)'))
    return out, 'Code = nearest integer to vX/LSB (quantization error ≤ ½ LSB).', []
@solve('12.86')
def _():
    out = []
    for vx in (3.760, 4.333):
        N = int(vx / 5 * 4096); out.append((f'vX = {vx} V', f'code {format(N, "012b")} ({N}); TT = N/fC = {si(N / 1e6, "s")}'))
    return out, 'The counter runs until the DAC output reaches vX: N clock periods, with N = vX/VFS·2¹² truncated (the DAC output must not exceed vX).', ['Code obtained by truncation (counting converter stops when the DAC output first exceeds vX).']
@solve('12.92')
def _(): t1 = 0.2; lsb = t1 / 2 ** 20; return [('LSB time T1/2²⁰', si(lsb, 's')), ('Switch timing error allowed (< 0.1 LSB)', si(0.1 * lsb, 's'))], 'A timing error ΔT in T1 is a fractional error ΔT/T1 of full scale; 0.1 LSB = 0.1/2²⁰ of full scale.', []
