import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    v27 = -0.025 * math.log(1.5 / (47e3 * 60e-9)) * 1e3; v26 = -0.025 * math.log(3 / (82e3 * 100e-9)) * 1e3
    md(T('# Module 05 · Mạch op-amp chuyên dụng (Floyd chương 14)', '# Module 05 · Special-purpose op-amp circuits (Floyd Ch.14)'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Mạch khuếch đại thiết bị: loại bỏ nhiễu chung', '## 1. Instrumentation amplifier: rejecting common-mode noise'))
    code('R, RG = 100e3, 1e3\nAv = 1 + 2*R/RG\nv1, v2, vcm = 5e-3, 10e-3, 225e-3\nprint(f"Av = {Av:.0f};  Vout = {Av*(v2-v1):.3f} V  (common-mode {vcm*1e3:.0f} mV rejected)")\nprint(f"RG for gain 1000: {2*R/999:.0f} ohm;  AD622 with 1k: {1+50.5e3/1e3:.1f}")\nt = np.linspace(0, 2e-3, 800); sig = 5e-3*np.sin(2*np.pi*1e3*t); noise = 225e-3*np.sin(2*np.pi*50*t)\nplt.plot(t*1e3, (sig+noise)*1e3, label="Vin1 (signal+noise)"); plt.plot(t*1e3, Av*sig*1e3/20, label="amplified difference (scaled)"); plt.legend(); plt.grid(alpha=.3); plt.xlabel("ms"); plt.ylabel("mV"); plt.show()')
    md(T('**Nhận xét:** Av = 201 và Vout = 1,005 V chỉ từ hiệu 5 mV; thành phần chung 225 mV hoàn toàn bị triệt. RG = 200 Ω cho độ lợi 1000 và AD622 với 1,0 kΩ cho 51,5 — đều trùng đáp án sách.', '**Comment:** Av = 201 and Vout = 1.005 V come only from the 5 mV difference; the 225 mV common-mode part is fully rejected. RG = 200 Ω gives a gain of 1000 and the AD622 with 1.0 kΩ gives 51.5 — both match the book.'))
    md(T('## 2. Băng thông giảm khi độ lợi tăng', '## 2. Bandwidth falls as gain rises'))
    code('fT = 8e6   # AD622: 800 kHz at gain 10 -> gain-bandwidth ~ 8 MHz\nfor G in (1, 10, 100, 1000): print(f"G = {G:>4}: BW ~ {fT/G/1e3:,.0f} kHz")')
    md(T('**Nhận xét:** Với tích độ lợi–băng thông xấp xỉ 8 MHz (800 kHz tại G = 10 theo Floyd), G = 1000 chỉ còn khoảng 8 kHz.', '**Comment:** With a gain–bandwidth product of ≈ 8 MHz (800 kHz at G = 10 per Floyd), G = 1000 leaves only ≈ 8 kHz. This is an approximation from one datasheet point.'))
    md(T('## 3. OTA', '## 3. OTA'))
    code('gm, Vin, RL = 5000e-6, 0.1, 10e3\nIo = gm*Vin; print(f"Iout = {Io*1e6:.0f} uA, Vout = {Io*RL:.1f} V, Av = {gm*RL:.0f}")\nfor ib in (25, 50, 100, 200): print(f"IBIAS = {ib:>3} uA -> gm = {16*ib} uS -> Av(RL=10k) = {16*ib*1e-6*10e3:.1f}")')
    md(T('**Nhận xét:** Iout = 500 μA, Vout = 5 V (đúng sách). Gấp đôi dòng phân cực thì gấp đôi gm và độ lợi.', '**Comment:** Iout = 500 μA and Vout = 5 V (as in the book). Doubling the bias current doubles gm and the gain.'))
    md(T('## 4. Mạch logarit', '## 4. Log amplifier'))
    code('def vlog(vin, r, ir): return -0.025*np.log(vin/(r*ir))\nprint(f"Prob 27: {vlog(1.5,47e3,60e-9)*1e3:.0f} mV;  Prob 26: {vlog(3,82e3,100e-9)*1e3:.0f} mV")\nvin = np.logspace(-2, 1, 200); plt.semilogx(vin, vlog(vin, 47e3, 60e-9)*1e3); plt.xlabel("Vin (V)"); plt.ylabel("Vout (mV)"); plt.grid(alpha=.3, which="both"); plt.show()\nprint("range of Vout for Vin 0.1 V ... 1 V:", round(vlog(0.1,47e3,60e-9)*1e3), "...", round(vlog(1,47e3,60e-9)*1e3), "mV")')
    md(T(f'**Nhận xét:** Bài 27 cho {v27:.0f} mV (sách: −157 mV); bài 26 cho {v26:.0f} mV. Tín hiệu vào biến thiên 10 lần (0,1–1 V) chỉ làm ngõ ra đổi khoảng 58 mV: đó là nén dải động.', f'**Comment:** Problem 27 gives {v27:.0f} mV (book: −157 mV); Problem 26 gives {v26:.0f} mV. A tenfold input span (0.1–1 V) moves the output by only ≈ 58 mV: dynamic-range compression.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm05_special_op_amps_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
