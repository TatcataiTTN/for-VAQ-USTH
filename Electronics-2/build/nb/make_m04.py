import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 04 · Ghép tầng và hồi tiếp', '# Module 04 · Stage coupling and feedback'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Tích độ lợi và dB', '## 1. Gain product and decibels'))
    code('A = 15**4; print(f"15^4 = {A:,}  -> {20*np.log10(A):.1f} dB  (= 4 x {20*np.log10(15):.2f} dB)")\nprint("3 stages of 10 dB: gain =", round(10**(30/20), 1))\nfor av in (12, 50, 100, 2500): print(av, "->", round(20*np.log10(av), 2), "dB")')
    md(T('**Nhận xét:** 15⁴ = 50 625 ứng với 94,1 dB = 4 × 23,52 dB; ba tầng 10 dB cho 31,6 lần — dB cộng, tỉ số nhân.', '**Comment:** 15⁴ = 50,625 corresponds to 94.1 dB = 4 × 23.52 dB; three 10 dB stages give 31.6 — dB add while ratios multiply.'))
    md(T('## 2. Hồi tiếp âm giảm độ nhạy với độ lợi vòng hở', '## 2. Negative feedback desensitises the gain to the open-loop gain'))
    code('B = 0.02\nfor A in (50000, 100000, 200000):\n    print(f"A = {A:>7,}: Acl = {A/(1+A*B):.4f}")\nA1, A2 = 100000, 120000\nc1, c2 = A1/(1+A1*B), A2/(1+A2*B)\nprint(f"A changes +{(A2/A1-1)*100:.0f} % -> Acl changes +{(c2/c1-1)*100:.4f} %")')
    md(T('**Nhận xét:** khi A tăng 20 %, Acl chỉ đổi khoảng 0,0083 % quanh 49,98 — hồi tiếp âm làm độ lợi vòng kín gần như chỉ phụ thuộc B (≈ 1/B = 50).', '**Comment:** when A rises 20 %, Acl changes only about 0.0083 % around 49.98 — negative feedback makes the closed-loop gain depend almost only on B (≈ 1/B = 50).'))
    md(T('## 3. Ghép RC: đáp ứng tần số thấp', '## 3. RC coupling: low-frequency response'))
    code('R, C = 4.7e3, 2.2e-6\nfc = 1/(2*np.pi*R*C); print(f"fc = {fc:.1f} Hz;  C for fc=20 Hz: {1/(2*np.pi*20*R)*1e6:.2f} uF")\nf = np.logspace(0, 3, 300); H = 1/np.sqrt(1+(fc/f)**2)\nfor ff in (fc/10, fc, 10*fc): print(f"f = {ff:7.2f} Hz: |H| = {1/np.sqrt(1+(fc/ff)**2):.3f} ({20*np.log10(1/np.sqrt(1+(fc/ff)**2)):.2f} dB)")\nplt.semilogx(f, 20*np.log10(H)); plt.axvline(fc, color="gray", lw=.8); plt.xlabel("Hz"); plt.ylabel("dB"); plt.grid(alpha=.3, which="both"); plt.show()')
    md(T('**Nhận xét:** với 4,7 kΩ và 2,2 μF, fc ≈ 15,4 Hz; tại fc biên độ giảm 3 dB (0,707), ở fc/10 chỉ còn 0,0995 — tụ ghép chặn tín hiệu thấp hơn fc nhiều.', '**Comment:** with 4.7 kΩ and 2.2 μF, fc ≈ 15.4 Hz; at fc the gain is down 3 dB (0.707) and at fc/10 only 0.0995 remains — the coupling capacitor blocks signals well below fc.'))
    md(T('## 4. Hiệu suất lớp A và lớp B theo biên độ', '## 4. Class A and class B efficiency versus amplitude'))
    code('# class B push-pull: eta = (pi/4)*(Vp/VCC);  class A (series-fed, Q at VCC/2): eta = 0.25*(Vp/(VCC/2))**2\nfor x in (0.25, 0.5, 0.75, 1.0):\n    etaB = np.pi/4*x; etaA = 0.25*x**2\n    print(f"Vp/VCC = {x:4.2f}: class B eta = {etaB*100:5.1f} %, class A eta (Vp/(VCC/2)={x:.2f}) = {etaA*100:5.1f} %")\nprint("class B maximum:", round(np.pi/4*100, 1), "%; class A series-fed maximum: 25.0 %")')
    md(T('**Nhận xét:** lớp B đạt tối đa π/4 ≈ 78,5 % khi biên độ bằng VCC; lớp A ghép nối tiếp tối đa 25 % — đúng Floyd (79 %, 25 %) và EASA (lớp B hiệu quả gấp khoảng hai lần lớp A, ở đây còn hơn thế khi so tối đa).', '**Comment:** class B reaches a maximum of π/4 ≈ 78.5 % when the amplitude equals VCC; the series-fed class A reaches at most 25 % — consistent with Floyd (79 %, 25 %); EASA’s “about twice as efficient” is a rough statement, and the maximum figures give a larger ratio.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm04_coupling_feedback_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
