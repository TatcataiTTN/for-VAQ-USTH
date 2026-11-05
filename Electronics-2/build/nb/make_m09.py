import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 09 · PCB và ESD (EASA M04 SM02)\nPhần tính toán dùng vật lý cơ bản để minh hoạ; không nằm trong văn bản EASA.', '# Module 09 · PCBs and ESD (EASA M04 SM02)\nThe calculations use basic physics for illustration; they are not in the EASA text.'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Điện trở và sụt áp của đường dẫn đồng', '## 1. Resistance and voltage drop of a copper trace'))
    code('rho = 1.68e-8\ndef R(L_mm, w_mm, t_um): return rho*L_mm*1e-3/(w_mm*1e-3*t_um*1e-6)\nfor L, w, t in [(100, 0.25, 35), (100, 1.0, 35), (100, 0.25, 70)]:\n    r = R(L, w, t); print(f"L={L} mm w={w} mm t={t} um: R = {r*1e3:.1f} mOhm; drop at 1 A = {r*1e3:.1f} mV")\nw = np.linspace(0.1, 2, 100); plt.plot(w, R(100, w, 35)*1e3); plt.xlabel("width (mm)"); plt.ylabel("R (mOhm)"); plt.grid(alpha=.3); plt.show()')
    md(T('**Nhận xét:** đường 100 mm × 0,25 mm × 35 μm có R ≈ 192 mΩ (sụt 192 mV ở 1 A); tăng chiều rộng hoặc độ dày gấp đôi giảm R một nửa — R tỉ lệ nghịch với tiết diện.', '**Comment:** a 100 mm × 0.25 mm × 35 μm trace has R ≈ 192 mΩ (192 mV drop at 1 A); doubling the width or thickness halves R — R is inversely proportional to cross-section.'))
    md(T('## 2. Điện dung giữa hai lớp (ghép ký sinh)', '## 2. Capacitance between two layers (parasitic coupling)'))
    code('eps0 = 8.854e-12\nfor er, A, d in [(4.5, 1.0, 0.2), (4.5, 4.0, 0.1), (4.5, 1.0, 0.4)]:\n    C = eps0*er*A*1e-4/(d*1e-3); print(f"er={er} A={A} cm2 d={d} mm: C = {C*1e12:.2f} pF")\nC = eps0*4.5*1e-4/0.2e-3\nfor f in (1e6, 100e6): print(f"f = {f/1e6:.0f} MHz: |Z| = {1/(2*np.pi*f*C):.0f} ohm")')
    md(T('**Nhận xét:** 1 cm² FR-4 dày 0,2 mm cho khoảng 19,9 pF; ở 100 MHz trở kháng chỉ còn khoảng 80 Ω (ở 1 MHz khoảng 8 kΩ) nên tín hiệu cao tần ghép sang lớp bên cạnh — đúng cảnh báo của EASA về ghép ký sinh.', '**Comment:** 1 cm² of FR-4 0.2 mm thick gives about 19.9 pF; at 100 MHz the impedance is only about 80 Ω (about 8 kΩ at 1 MHz), so a high-frequency signal couples into the neighbouring layer — as the EASA text warns.'))
    md(T('## 3. Xả tĩnh điện: mô hình cơ thể người (minh hoạ)', '## 3. Electrostatic discharge: human-body model (illustrative)'))
    code('C, Rb = 100e-12, 1500.0     # common illustrative HBM values (not from EASA)\nfor V in (250, 380, 1500, 3000, 7000, 35000):\n    print(f"{V:>6} V: stored energy = {0.5*C*V**2*1e6:8.2f} uJ, peak current = {V/Rb:6.2f} A")\nt = np.linspace(0, 1e-6, 400); plt.plot(t*1e9, 1500/Rb*np.exp(-t/(Rb*C))); plt.xlabel("t (ns)"); plt.ylabel("I (A)"); plt.title("1500 V discharge"); plt.grid(alpha=.3); plt.show()\nprint("time constant =", Rb*C*1e9, "ns")')
    md(T('**Nhận xét:** với mô hình minh hoạ 100 pF/1,5 kΩ, 1 500 V tích 112,5 μJ và xả với đỉnh 1 A, hằng số thời gian 150 ns — ngắn nhưng đủ nóng cục bộ làm hỏng linh kiện CMOS (nhạy từ 250 V). Giá trị mô hình là quy ước phổ biến, không từ EASA.', '**Comment:** with the illustrative 100 pF/1.5 kΩ model, 1 500 V stores 112.5 μJ and discharges with a 1 A peak and a 150 ns time constant — brief but enough local heating to damage CMOS parts (sensitive from 250 V). The model values are a common convention, not from EASA.'))
    md(T('## 4. So sánh mức nhạy ESD (số liệu EASA)', '## 4. Comparing ESD susceptibility (EASA figures)'))
    code('dev = {"Bipolar": (380, 7000), "CMOS": (250, 3000), "EPROM": (100, 100)}\nfor k, (lo, hi) in dev.items(): print(f"{k:8s} {lo:>5} - {hi:<5} V")\nprint("walking, 65% RH: 1500 V  -> above the lower limit of CMOS and bipolar:", 1500 > 250, 1500 > 380)\nprint("walking, 20% RH: 35000 V -> above every upper limit:", all(35000 > hi for _, hi in dev.values()))')
    md(T('**Nhận xét:** 1 500 V khi đi trên thảm đã vượt ngưỡng dưới của cả CMOS (250 V) và lưỡng cực (380 V); 35 000 V ở độ ẩm 20 % vượt mọi ngưỡng trên — vì vậy cần môi trường kiểm soát.', '**Comment:** the 1 500 V from walking on carpet already exceeds the lower limit of both CMOS (250 V) and bipolar parts (380 V); 35 000 V at 20 % RH exceeds every upper limit — hence the controlled environment.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm09_pcb_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
