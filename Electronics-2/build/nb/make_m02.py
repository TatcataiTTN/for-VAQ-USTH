"""Build + execute notebooks m02_op_amp_{vi,en}.ipynb. Interpretations quote numbers computed here (same formulas as the code cells)."""
import os, math, nbformat as nbf, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
db = lambda r: 20 * math.log10(r)
cmrr = 175000 / 0.18; acl13 = 1 + 560 / 1.5
aol37 = 10 ** (89 / 20); acl37 = aol37 / (5500 / 750)
fmax = 0.5e6 / (2 * math.pi * 10)
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b
    nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 02 · Op-amp (Floyd chương 12)\nNotebook tái hiện các phép tính chính; mỗi mục có câu hỏi, mã, và nhận xét dựa trên kết quả thật.', '# Module 02 · The operational amplifier (Floyd Ch.12)\nThis notebook reproduces the key calculations; each section has a question, code and a comment based on the real output.'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline\ndb = lambda r: 20*np.log10(r)')
    md(T('## 1. CMRR\n**Câu hỏi:** Aol = 175 000, Acm = 0,18 thì CMRR bằng bao nhiêu dB? (Floyd Bài 5)', '## 1. CMRR\n**Question:** Aol = 175,000 and Acm = 0.18: what is the CMRR in dB? (Floyd Problem 5)'))
    code('Aol, Acm = 175000, 0.18\nCMRR = Aol/Acm\nprint(f"CMRR = {CMRR:,.0f}  ->  {db(CMRR):.2f} dB")\nprint(f"250,000 -> {db(250000):.2f} dB   (Floyd Problem 4)")')
    md(T(f'**Nhận xét:** CMRR = {cmrr:,.0f} tương ứng {db(cmrr):.2f} dB ≈ 120 dB, khớp đáp án sách (120 dB). Nhân thêm 10 lần tỉ số chỉ cộng 20 dB.', f'**Comment:** CMRR = {cmrr:,.0f} corresponds to {db(cmrr):.2f} dB ≈ 120 dB, matching the book (120 dB). Another factor of 10 only adds 20 dB.'))
    md(T('## 2. Slew rate và tần số sin tối đa\n**Câu hỏi:** Với SR = 0,5 V/μs, sin biên độ đỉnh 10 V có méo ở tần số nào?', '## 2. Slew rate and maximum sine frequency\n**Question:** With SR = 0.5 V/μs, at what frequency does a 10 V-peak sine start to distort?'))
    code('SR = 0.5e6   # V/s\nVp = 10\nfmax = SR/(2*np.pi*Vp)\nprint(f"f_max = {fmax/1e3:.2f} kHz")\nt = np.linspace(0, 3/10e3, 3000)\nfor f in (5e3, 10e3):\n    ideal = Vp*np.sin(2*np.pi*f*t); y = np.zeros_like(t)\n    for k in range(1, len(t)):\n        step = np.clip(ideal[k]-y[k-1], -SR*(t[1]-t[0]), SR*(t[1]-t[0])); y[k] = y[k-1]+step\n    plt.plot(t*1e3, y, label=f"{f/1e3:.0f} kHz")\nplt.xlabel("t (ms)"); plt.ylabel("Vout (V)"); plt.legend(); plt.grid(alpha=.3); plt.show()')
    md(T(f'**Nhận xét:** f_max = {fmax/1e3:.2f} kHz. Đường 5 kHz bám theo sin còn đường 10 kHz bị giới hạn thành dạng tam giác vì đổi mức nhanh hơn slew rate.', f'**Comment:** f_max = {fmax/1e3:.2f} kHz. The 5 kHz curve follows the sine while the 10 kHz curve becomes triangular because it changes faster than the slew rate.'))
    md(T('## 3. Độ lợi không đảo và đảo\n**Câu hỏi:** Tính độ lợi và Vout cho Floyd Bài 13 và bài 15.', '## 3. Noninverting and inverting gain\n**Question:** Compute gain and Vout for Floyd Problems 13 and 15.'))
    code('Acl = 1 + 560/1.5\nprint(f"Problem 13: Acl = {Acl:.1f}, Vout = {Acl*10e-3:.3f} V rms")\nfor lbl, acl, ri, inv in [("a",50,1.0,False),("b",300,10,True),("c",8,12,False),("d",75,2.2,True)]:\n    rf = acl*ri if inv else (acl-1)*ri\n    print(f"Problem 15({lbl}): Rf = {rf:g} kOhm")')
    md(T(f'**Nhận xét:** Acl = {acl13:.1f}, Vout = {acl13*0.01:.3f} V rms; bốn giá trị Rf là 49 kΩ, 3000 kΩ, 84 kΩ, 165 kΩ — trùng đáp án sách.', f'**Comment:** Acl = {acl13:.1f}, Vout = {acl13*0.01:.3f} V rms; the four Rf values are 49 kΩ, 3000 kΩ, 84 kΩ, 165 kΩ — identical to the book.'))
    md(T('## 4. Trở kháng với hồi tiếp\n**Câu hỏi:** Zin và Zout của mạch không đảo thay đổi thế nào?', '## 4. Impedances with feedback\n**Question:** How do Zin and Zout of the noninverting circuit change?'))
    code('Aol, Zin, Zout, Rf, Ri = 100000, 2e6, 75, 100e3, 1e3\nB = Ri/(Ri+Rf); k = 1 + B*Aol\nprint(f"B = {B:.5f}, 1+B*Aol = {k:,.1f}")\nprint(f"Zin(NI) = {k*Zin/1e9:.2f} GOhm,  Zout(NI) = {Zout/k*1e3:.1f} mOhm")')
    md(T(f'**Nhận xét:** 1 + B·Aol ≈ {1+100000/101:,.1f}; Zin từ 2 MΩ lên {(1+100000/101)*2e6/1e9:.2f} GΩ và Zout từ 75 Ω xuống {75/(1+100000/101)*1e3:.1f} mΩ.', f'**Comment:** 1 + B·Aol ≈ {1+100000/101:,.1f}; Zin rises from 2 MΩ to {(1+100000/101)*2e6/1e9:.2f} GΩ and Zout falls from 75 Ω to {75/(1+100000/101)*1e3:.1f} mΩ.'))
    md(T('## 5. Đáp ứng tần số vòng hở và vòng kín\n**Câu hỏi:** Vẽ Bode biên độ của Aol = 100 dB (fc = 10 Hz) và các độ lợi vòng kín 10, 100, 1000.', '## 5. Open- and closed-loop frequency response\n**Question:** Plot the magnitude Bode of Aol = 100 dB (fc = 10 Hz) and closed-loop gains 10, 100, 1000.'))
    code('f = np.logspace(0, 7, 600); Aol0, fc = 1e5, 10\nAol = Aol0/np.sqrt(1+(f/fc)**2)\nplt.semilogx(f, db(Aol), "k", lw=2, label="open loop")\nfor acl in (10, 100, 1000):\n    B = 1/acl; fcl = fc*(1+B*Aol0)\n    A = (Aol0/(1+B*Aol0))/np.sqrt(1+(f/fcl)**2)\n    plt.semilogx(f, db(A), label=f"Acl={acl}  BW={fcl/1e3:.0f} kHz")\n    print(f"Acl={acl}: fc(cl)={fcl/1e3:.1f} kHz, Acl*fc(cl)={acl*fcl/1e6:.2f} MHz")\nplt.axhline(0, color="gray", lw=.8); plt.xlabel("f (Hz)"); plt.ylabel("gain (dB)"); plt.legend(); plt.grid(alpha=.3, which="both"); plt.show()')
    md(T('**Nhận xét:** Tích Acl·fc(cl) xấp xỉ 1 MHz cho cả ba độ lợi (= Aol·fc(ol) = 10⁵ × 10 Hz): tăng độ lợi 10 lần thì băng thông giảm 10 lần.', '**Comment:** The product Acl·fc(cl) is ≈ 1 MHz for all three gains (= Aol·fc(ol) = 10⁵ × 10 Hz): ten times more gain gives one tenth of the bandwidth.'))
    md(T('## 6. Floyd Bài 37–38\n**Câu hỏi:** fc(ol) = 750 Hz, Aol = 89 dB, fc(cl) = 5,5 kHz. Tìm Acl (dB) và fT.', '## 6. Floyd Problems 37–38\n**Question:** fc(ol) = 750 Hz, Aol = 89 dB, fc(cl) = 5.5 kHz. Find Acl (dB) and fT.'))
    code('Aol = 10**(89/20); k = 5500/750\nAcl = Aol/k\nprint(f"Aol = {Aol:,.0f}; 1+B*Aol = {k:.3f}; Acl = {Acl:,.0f} -> {db(Acl):.1f} dB")\nprint(f"fT = Acl*fc(cl) = {Acl*5500/1e6:.1f} MHz ; Aol*fc(ol) = {Aol*750/1e6:.1f} MHz")')
    md(T(f'**Nhận xét:** Acl ≈ {acl37:,.0f} ({db(acl37):.1f} dB, sách: 71,7 dB); fT ≈ {acl37*5500/1e6:.1f} MHz và hai cách tính khớp nhau.', f'**Comment:** Acl ≈ {acl37:,.0f} ({db(acl37):.1f} dB, book: 71.7 dB); fT ≈ {acl37*5500/1e6:.1f} MHz and the two routes agree.'))
    md(T('## 7. Mạch trễ RC\n**Câu hỏi:** Biên độ và pha của mạch trễ RC theo f/fc.', '## 7. RC lag circuit\n**Question:** Magnitude and phase of an RC lag versus f/fc.'))
    code('r = np.array([0.1, 0.5, 1, 2, 10])\nfor x, a, p in zip(r, 1/np.sqrt(1+r**2), -np.degrees(np.arctan(r))):\n    print(f"f/fc={x:>4}: |Vout/Vin|={a:.3f} ({db(a):6.2f} dB), phase={p:6.1f} deg")')
    md(T('**Nhận xét:** Tại f = fc biên độ là 0,707 (−3,01 dB) và pha −45°; tại f = 10·fc pha gần −90° và biên độ ≈ 0,0995.', '**Comment:** At f = fc the magnitude is 0.707 (−3.01 dB) and the phase −45°; at f = 10·fc the phase approaches −90° and the magnitude is ≈ 0.0995.'))
    md(T('## 8. Sai số do Aol hữu hạn\n**Câu hỏi:** Acl thực khác 1/B bao nhiêu?', '## 8. Error from finite Aol\n**Question:** How far is the real Acl from 1/B?'))
    code('for Aol in (1e3, 1e4, 1e5, 2e5):\n    B = 1/101; A = Aol/(1+B*Aol)\n    print(f"Aol={Aol:>9,.0f}: Acl={A:8.3f}  error vs 101 = {(101-A)/101*100:6.3f} %")')
    md(T('**Nhận xét:** Với Aol = 10⁵ sai số ≈ 0,1 %; gấp đôi Aol thì sai số giảm còn một nửa — vì vậy Self-Test câu 18 coi độ lợi “vẫn là 25”.', '**Comment:** At Aol = 10⁵ the error is ≈ 0.1 %; doubling Aol halves it — which is why Self-Test Q18 treats the gain as “remains at 25”.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm02_op_amp_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True)
        print('executed', p)
