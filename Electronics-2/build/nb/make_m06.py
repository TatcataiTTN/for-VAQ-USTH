import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    f3 = 1 / (2 * math.pi * 2.2e3 * 0.0015e-6)
    md(T('# Module 06 · Bộ lọc tích cực (Floyd chương 15)', '# Module 06 · Active filters (Floyd Ch.15)'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline\ndb = lambda x: 20*np.log10(np.abs(x))')
    md(T('## 1. Tần số tới hạn và băng thông', '## 1. Critical frequency and bandwidth'))
    code('fc = 1/(2*np.pi*2.2e3*0.0015e-6); print(f"Prob 3: fc = {fc/1e3:.1f} kHz")\nf1, f2 = 3.2e3, 3.9e3; f0 = np.sqrt(f1*f2); print(f"Prob 5: BW = {f2-f1:.0f} Hz, f0 = {f0:.0f} Hz, Q = {f0/(f2-f1):.2f}")\nprint("Prob 6: f0 =", 15*1e3, "Hz")')
    md(T(f'**Nhận xét:** fc = {f3/1e3:.1f} kHz đúng sách (48,2 kHz); BW = 700 Hz; Q = 5,05 (sách in 5,04).', f'**Comment:** fc = {f3/1e3:.1f} kHz matches the book (48.2 kHz); BW = 700 Hz; Q = 5.05 (book prints 5.04).'))
    md(T('## 2. Butterworth, Chebyshev (1 dB), Bessel bậc 2', '## 2. Second-order Butterworth, Chebyshev (1 dB) and Bessel'))
    code('from scipy import signal\nf = np.logspace(2, 4.2, 400); w = 2*np.pi*f; wc = 2*np.pi*1e3\nfor name, (b, a) in {"Butterworth": signal.butter(2, wc, analog=True), "Chebyshev 1 dB": signal.cheby1(2, 1, wc, analog=True), "Bessel": signal.bessel(2, wc, analog=True, norm="mag")}.items():\n    _, h = signal.freqs(b, a, w); plt.semilogx(f, db(h), label=name)\n    print(f"{name:15s} gain at 3 kHz = {db(signal.freqs(b,a,[2*np.pi*3e3])[1][0]):6.2f} dB, gain variation below 500 Hz = {np.ptp(db(h[f<500])):.2f} dB, gain at 1 kHz = {db(signal.freqs(b,a,[2*np.pi*1e3])[1][0]):.2f} dB")\nplt.ylim(-40, 3); plt.legend(); plt.grid(alpha=.3, which="both"); plt.xlabel("Hz"); plt.ylabel("dB"); plt.show()')
    md(T('**Nhận xét:** Tại 1 kHz Butterworth và Bessel đều −3,01 dB còn Chebyshev −1,00 dB vì thiết kế theo mép gợn 1 dB (tần số −3 dB của nó cao hơn 1 kHz). Tại 3 kHz suy giảm là −19,1 dB (Butterworth), −18,8 dB (Chebyshev) và −15,7 dB (Bessel): Bessel có độ suy giảm chậm nhất. Muốn thấy Chebyshev dốc hơn phải so sánh ở cùng tần số −3 dB.', '**Comment:** At 1 kHz Butterworth and Bessel are both −3.01 dB while Chebyshev is −1.00 dB because it is designed to the 1 dB ripple edge (its −3 dB frequency lies above 1 kHz). At 3 kHz the attenuation is −19.1 dB (Butterworth), −18.8 dB (Chebyshev) and −15.7 dB (Bessel): Bessel rolls off slowest. To see Chebyshev’s steeper skirt, compare at the same −3 dB frequency.'))
    md(T('## 3. Hệ số tắt dần và R1/R2', '## 3. Damping factor and R1/R2'))
    code('for n, dfs in {2: [1.414], 4: [1.848, 0.765], 6: [1.932, 1.414, 0.518]}.items():\n    print(n, "poles:", [round(2-d, 3) for d in dfs])')
    md(T('**Nhận xét:** sáu cực cho 0,068; 0,586; 1,482 trùng đáp án Bài 13 của sách.', '**Comment:** six poles give 0.068, 0.586, 1.482, identical to the book answer of Problem 13.'))
    md(T('## 4. Thông dải hồi tiếp nhiều đường (Floyd Bài 19b)', '## 4. Multiple-feedback band-pass (Floyd Problem 19b)'))
    code('R1, R2, R3, C = 47e3, 150e3, 1.8e3, 0.022e-6\nf0 = 1/(2*np.pi*C)*np.sqrt((R1+R3)/(R1*R2*R3)); BW = 1/(np.pi*R2*C)\nprint(f"f0 = {f0:.0f} Hz, BW = {BW:.1f} Hz, Q = {f0/BW:.2f}")\nf = np.logspace(1, 4, 600); s = 2j*np.pi*f; w0 = 2*np.pi*f0; Q = f0/BW\nH = (s*w0/Q)/(s**2 + s*w0/Q + w0**2); plt.semilogx(f, db(H)); plt.axvline(f0, color="gray", lw=.8); plt.grid(alpha=.3, which="both"); plt.xlabel("Hz"); plt.ylabel("dB"); plt.show()\nidx = np.where(db(H) >= -3.01)[0]; print(f"-3 dB band: {f[idx[0]]:.0f} .. {f[idx[-1]]:.0f} Hz -> width {f[idx[-1]]-f[idx[0]]:.0f} Hz")')
    md(T('**Nhận xét:** f0 = 449 Hz, BW = 96,5 Hz (sách: 96,4 Hz); đồ thị mô hình bậc hai cho dải −3 dB rộng xấp xỉ BW.', '**Comment:** f0 = 449 Hz, BW = 96.5 Hz (book: 96.4 Hz); the second-order model plot gives a −3 dB width close to BW.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm06_active_filters_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
