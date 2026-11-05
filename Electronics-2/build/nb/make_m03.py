"""Notebooks m03_op_amp_circuits_{vi,en}.ipynb (executed)."""
import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    ut = 18 / 65 * 10; v13 = 2 + 10 / 33 * 3 + 10 / 91 * 3 + 10 / 180 * 6; s15 = 5 / (56e3 * 0.022e-6); a18 = 15e3 * 0.047e-6 * 4000
    md(T('# Module 03 · Mạch op-amp cơ bản (Floyd chương 13)', '# Module 03 · Basic op-amp circuits (Floyd Ch.13)'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Hysteresis\n**Câu hỏi:** Hình 13–61 (R1 = 47 kΩ, R2 = 18 kΩ, Vout(max) = ±10 V) có ngưỡng nào?', '## 1. Hysteresis\n**Question:** What are the trigger points of Fig. 13–61 (R1 = 47 kΩ, R2 = 18 kΩ, Vout(max) = ±10 V)?'))
    code('R1, R2, Vm = 47, 18, 10\nUT = R2/(R1+R2)*Vm\nprint(f"VUTP = {UT:.2f} V, VLTP = {-UT:.2f} V, VHYS = {2*UT:.2f} V")\nt = np.linspace(0, 2e-3, 4000); vin = 6*np.sin(2*np.pi*1e3*t) + 0.8*np.sin(2*np.pi*40e3*t)\nout = np.zeros_like(t); s = -Vm\nfor k, v in enumerate(vin):\n    if s < 0 and v > UT: s = Vm\n    elif s > 0 and v < -UT: s = -Vm\n    out[k] = s\nplt.plot(t*1e3, vin, lw=.7, label="Vin (noisy)"); plt.plot(t*1e3, out, label="Vout"); plt.legend(); plt.grid(alpha=.3); plt.xlabel("ms"); plt.show()\nprint("transitions:", int(np.sum(np.diff(out) != 0)))')
    md(T(f'**Nhận xét:** VUTP = {ut:.2f} V đúng đáp án sách (±2,77 V). Dù nhiễu 40 kHz biên độ 0,8 V chồng lên tín hiệu, ngõ ra chỉ chuyển 4 lần trong 2 chu kỳ nhờ hysteresis {2*ut:.2f} V.', f'**Comment:** VUTP = {ut:.2f} V matches the book (±2.77 V). Despite 0.8 V of 40 kHz noise on the signal, the output flips only 4 times in 2 cycles thanks to the {2*ut:.2f} V hysteresis.'))
    md(T('## 2. Mạch cộng và cộng có trọng số', '## 2. Summing and scaling adders'))
    code('print("Prob 9b:", -22/10*(0.1+1+0.5), "V")\nRf=10; R=[10,33,91,180]; V=[2,3,3,6]\nvo=-sum(Rf/r*v for r,v in zip(R,V)); print(f"Prob 13: VOUT = {vo:.3f} V, If = {abs(vo)/10e3*1e6:.0f} uA")\nprint("Prob 14 Ri (kOhm):", [100/w for w in (1,2,4,8,16,32)])')
    md(T(f'**Nhận xét:** VOUT bài 9b = −3,52 V; bài 13 cho −{v13:.3f} V (dòng {v13/10e3*1e6:.0f} μA); sáu điện trở bài 14 giảm một nửa liên tiếp từ 100 kΩ đến 3,125 kΩ.', f'**Comment:** Problem 9b gives −3.52 V; Problem 13 gives −{v13:.3f} V ({v13/10e3*1e6:.0f} μA); the six resistors of Problem 14 halve from 100 kΩ down to 3.125 kΩ.'))
    md(T('## 3. Tích phân: bước nhảy và sóng vuông', '## 3. Integrator: step and square-wave inputs'))
    code('R, C = 56e3, 0.022e-6\nprint(f"Prob 15: dVout/dt = {-5/(R*C):.0f} V/s = {-5/(R*C)/1e3:.2f} V/ms")\nR, C, dt = 10e3, 0.01e-6, 1e-7\nt = np.arange(0, 800e-6, dt); vin = np.where((t//200e-6) % 2 == 0, 2.5, -2.5)\nvo = -np.cumsum(vin)*dt/(R*C)\nplt.plot(t*1e6, vin, label="Vin"); plt.plot(t*1e6, vo, label="Vout"); plt.legend(); plt.xlabel("us"); plt.grid(alpha=.3); plt.show()\nprint(f"peak-to-peak after 200 us: {abs(vo[int(200e-6/dt)-1]):.2f} V")')
    md(T(f'**Nhận xét:** Tốc độ bài 15 là −{s15:.0f} V/s (−{s15/1e3:.2f} V/ms). Với 2,5 V, 10 kΩ, 0,01 μF, đường dốc đạt 5 V sau 200 μs — đúng Hình 13–35(b).', f'**Comment:** Problem 15’s rate is −{s15:.0f} V/s (−{s15/1e3:.2f} V/ms). With 2.5 V, 10 kΩ and 0.01 μF the ramp reaches 5 V in 200 μs — matching Fig. 13–35(b).'))
    md(T('## 4. Vi phân: tam giác → vuông', '## 4. Differentiator: triangle → square'))
    code('Rf, C, vpp, T = 15e3, 0.047e-6, 2, 1e-3\nslope = vpp/(T/2); A = Rf*C*slope\nprint(f"Prob 18: slope = {slope:.0f} V/s, |Vout| = {A:.2f} V")\nt = np.linspace(0, 2*T, 4000); tri = vpp/2*(2*np.abs(2*((t/T)%1)-1)-1)\nd = -Rf*C*np.gradient(tri, t); plt.plot(t*1e3, tri, label="Vin"); plt.plot(t*1e3, d, label="Vout"); plt.legend(); plt.grid(alpha=.3); plt.xlabel("ms"); plt.show()')
    md(T(f'**Nhận xét:** |Vout| = {a18:.2f} V, ngõ ra là sóng vuông ±{a18:.2f} V ngược dấu với độ dốc của ngõ vào.', f'**Comment:** |Vout| = {a18:.2f} V and the output is a ±{a18:.2f} V square wave, opposite in sign to the input slope.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm03_op_amp_circuits_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
