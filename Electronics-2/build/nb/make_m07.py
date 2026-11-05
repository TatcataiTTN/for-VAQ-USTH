import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 07 · Dao động và IC 555 (Floyd chương 16)', '# Module 07 · Oscillators and the 555 timer (Floyd Ch.16)'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Công thức tần số các mạch RC và LC', '## 1. Frequency formulas of the RC and LC oscillators'))
    code('print(f"Wien (6.2k, 0.02uF): {1/(2*np.pi*6.2e3*0.02e-6):.0f} Hz")\nprint(f"Phase-shift (4.7k, 0.022uF): {1/(2*np.pi*np.sqrt(6)*4.7e3*0.022e-6):.0f} Hz, Rf = {29*4.7:.1f} kOhm")\nc1, c2, L = 470e-12, 47e-12, 1e-3; ct = c1*c2/(c1+c2)\nprint(f"Colpitts: CT = {ct*1e12:.1f} pF, f = {1/(2*np.pi*np.sqrt(L*ct))/1e3:.0f} kHz, Av = {c1/c2:.0f}")')
    md(T('**Nhận xét:** 1284 Hz, 628 Hz (đúng sách) và Rf = 136,3 kΩ; mạch Colpitts có Av = 10 (đúng sách).', '**Comment:** 1284 Hz, 628 Hz (as in the book) and Rf = 136.3 kΩ; the Colpitts circuit needs Av = 10 (as in the book).'))
    md(T('## 2. Khởi động và biên độ của dao động (mô hình độ lợi vòng)', '## 2. Start-up and amplitude (loop-gain model)'))
    code('# amplitude grows by loop gain each cycle until the limiter saturates it (|v| <= 1)\nfor g in (0.9, 1.0, 1.05, 1.2):\n    v = 1e-3; n = 0\n    while abs(v) < 1 and n < 1000: v *= g; n += 1\n    print(f"loop gain {g:.2f}: {\"dies out\" if g < 1 else (\"stays at 1 mV\" if g == 1 else f\"reaches 1 V after {n} cycles\")}")')
    md(T('**Nhận xét:** độ lợi vòng nhỏ hơn 1 làm dao động tắt, bằng 1 giữ nguyên biên độ, lớn hơn 1 làm biên độ tăng dần đến khi bị giới hạn — đúng tinh thần Floyd §16–2.', '**Comment:** a loop gain below 1 makes the oscillation die out, exactly 1 holds the amplitude, above 1 makes it grow until limited — in line with Floyd §16–2.'))
    md(T('## 3. 555 phi ổn: công thức và mô phỏng tụ nạp/xả', '## 3. 555 astable: formula and capacitor charge/discharge simulation'))
    code('R1, R2, C, Vcc = 1e3, 3.3e3, 0.047e-6, 5.5\nf_formula = 1.44/((R1+2*R2)*C); duty = (R1+R2)/(R1+2*R2)\nprint(f"formula: f = {f_formula:.0f} Hz, duty = {duty*100:.1f} %")\ntH = np.log(2)*(R1+R2)*C; tL = np.log(2)*R2*C; print(f"ideal exponentials: tH = {tH*1e6:.1f} us, tL = {tL*1e6:.1f} us -> f = {1/(tH+tL):.0f} Hz")\ndt = 1e-8; v = Vcc/3; t = 0; up = True; edges = []\nwhile len(edges) < 8 and t < 5e-3:\n    if up:\n        v += (Vcc - v)/((R1+R2)*C)*dt\n        if v >= 2*Vcc/3: up = False; edges.append(t)\n    else:\n        v += (0 - v)/(R2*C)*dt\n        if v <= Vcc/3: up = True; edges.append(t)\n    t += dt\nT = (edges[-1]-edges[1])/3\nprint(f"simulated period = {T*1e6:.1f} us -> f = {1/T:.0f} Hz")')
    md(T('**Nhận xét:** công thức Floyd cho khoảng 4,03 kHz; mô hình hàm mũ lý tưởng (ln 2 = 0,693 thay cho 0,7) cho tần số rất gần đó, và mô phỏng số khớp với mô hình hàm mũ. Sai khác nhỏ giữa 1,44 và 1/(2·0,693) chỉ là do Floyd làm tròn 0,7.', '**Comment:** Floyd’s formula gives about 4.03 kHz; the ideal exponential model (ln 2 = 0.693 instead of 0.7) gives a very close value and the numerical simulation agrees with that model. The small gap between 1.44 and 1/(2·0.693) is only Floyd’s rounding of 0.7.'))
    md(T('## 4. Chu kỳ làm việc và thiết kế Cext', '## 4. Duty cycle and Cext design'))
    code('print("Cext for 25 kHz:", round(1.44/((1e3+2*3.3e3)*25e3)*1e6, 4), "uF")\nprint("R2 for 75 % duty with R1 = 3.3k:", 3.3/2, "kOhm")\nfor r1, r2 in [(1, 1), (1, 10), (10, 1)]: print(f"R1={r1}k R2={r2}k duty = {(r1+r2)/(r1+2*r2)*100:.1f} %")')
    md(T('**Nhận xét:** Cext = 0,0076 μF (đúng sách); R2 = 1,65 kΩ cho 75 %; khi R2 ≪ R1 chu kỳ tiến tới 100 %, khi R2 ≫ R1 tiến tới 50 % — không bao giờ dưới 50 % nếu không có điốt.', '**Comment:** Cext = 0.0076 μF (as in the book); R2 = 1.65 kΩ gives 75 %; as R2 ≪ R1 the duty approaches 100 %, as R2 ≫ R1 it approaches 50 % — never below 50 % without the diode.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm07_oscillators_555_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
