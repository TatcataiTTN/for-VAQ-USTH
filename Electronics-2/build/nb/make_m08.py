import os, math, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 08 · Ổn áp (Floyd chương 17)', '# Module 08 · Voltage regulators (Floyd Ch.17)'))
    code('import numpy as np, matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n%matplotlib inline')
    md(T('## 1. Line và load regulation', '## 1. Line and load regulation'))
    code('print(f"Prob 1: line = {2e-3/6*100:.4f} %  ({2e-3/6*100/6:.5f} %/V)")\nprint(f"Prob 3: load = {(10-9.90)/9.90*100:.2f} %  ({(10-9.90)/9.90*100/250:.5f} %/mA)")')
    md(T('**Nhận xét:** 0,0333 % và 1,01 % trùng đáp án sách.', '**Comment:** 0.0333 % and 1.01 % match the book.'))
    md(T('## 2. Ổn áp nối tiếp với op-amp: VIN thay đổi, VOUT đứng yên', '## 2. Series regulator with op-amp: VIN changes, VOUT holds'))
    code('def series(vin, vref=5.1, r2=10e3, r3=10e3, A=1e5, vdrop=0.7):\n    # error-amplifier loop solved by iteration: Vout = A*(vref - Vout*r3/(r2+r3)) limited by VIN - vdrop\n    b = r3/(r2+r3); vo = vref/b\n    vo_open = min(A*vref/(1+A*b), vin - vdrop)\n    return vo_open\nfor vin in (13, 15, 16, 20): print(f"VIN = {vin} V -> VOUT = {series(vin):.3f} V")\nprint("ideal (1+R2/R3)*VREF =", (1+1)*5.1)')
    md(T('**Nhận xét:** với VIN = 13, 15, 16 và 20 V ngõ ra đều là 10,200 V = (1 + R2/R3)·VREF; sai số do độ lợi hữu hạn của op-amp nhỏ hơn 1 mV nên không hiện ra ở ba chữ số thập phân. Ngõ ra chỉ giảm nếu VIN rơi xuống dưới VOUT + 0,7 V (hết khoảng dropout, mô hình đơn giản). Bài 7–9 cho 8,51 V, 5,26 V (R3 = 4,7 kΩ), 9,57 V.', '**Comment:** for VIN = 13, 15, 16 and 20 V the output is 10.200 V = (1 + R2/R3)·VREF; the error from the op-amp’s finite gain is below 1 mV so it does not show at three decimals. The output would only fall if VIN dropped below VOUT + 0.7 V (out of headroom, in this simple model). Problems 7–9 give 8.51 V, 5.26 V (R3 = 4.7 kΩ) and 9.57 V.'))
    md(T('## 3. Giới hạn dòng và ổn áp song song', '## 3. Current limiting and the shunt regulator'))
    code('print("Prob 10: R4 =", 0.7/0.25, "ohm, P =", round(0.25**2*0.7/0.25, 3), "W; halving R4 ->", 0.7/1.4*1e3, "mA")\nprint("Prob 13: dIC =", 1/100*1e3, "mA;  Prob 15: IL(max) =", 25/100*1e3, "mA, PR1 =", 25**2/100, "W")\nvin = np.linspace(12, 25, 6)\nprint("shunt: R1 current with Vout = 10 V:", np.round((vin-10)/100*1e3, 1), "mA")')
    md(T('**Nhận xét:** R4 = 2,8 Ω, 0,175 W; chia đôi R4 cho 500 mA; ổn áp song song: 10 mA mỗi volt VIN, 250 mA và 6,25 W khi ngắn mạch — đều đúng sách.', '**Comment:** R4 = 2.8 Ω, 0.175 W; halving R4 gives 500 mA; shunt regulator: 10 mA per volt of VIN, 250 mA and 6.25 W when shorted — all as in the book.'))
    md(T('## 4. Ổn áp xung: chu kỳ làm việc và lọc LC', '## 4. Switching regulator: duty cycle and LC filtering'))
    code('vin, f, d, L, C, R = 12.0, 10e3, 0.4, 1e-3, 100e-6, 10.0\ndt = 1e-7; n = int(0.02/dt); i = 0.0; v = 0.0; vs = []\nfor k in range(n):\n    t = (k*dt) % (1/f); sw = vin if t < d/f else 0.0\n    i += (sw - v)/L*dt; v += (i - v/R)/C*dt; vs.append(v)\nvs = np.array(vs); tail = vs[-int(0.002/dt):]\nprint(f"duty = {d*100:.0f} %: ideal Vout = {d*vin:.2f} V; simulated mean = {tail.mean():.2f} V, ripple = {tail.max()-tail.min():.3f} V")\nprint("Prob 17: duty =", (1000/10-60)/(1000/10)*100, "%")')
    md(T('**Nhận xét:** mô phỏng LC với chu kỳ 40 % cho điện áp trung bình xấp xỉ 4,8 V = 0,4 × 12 V, gợn nhỏ; bài 17 cho 40 % như sách.', '**Comment:** the LC simulation at a 40 % duty cycle settles near 4.8 V = 0.4 × 12 V with small ripple; Problem 17 gives 40 % as in the book.'))
    md(T('## 5. LM317 và IC 78XX', '## 5. LM317 and 78XX ICs'))
    code('v = 1.25*(1+10/1) + 50e-6*10e3; print(f"Prob 21: VOUT = {v:.2f} V;  Prob 23: I = {v/11e3*1e3:.2f} mA")\nprint("Prob 25: Rext =", 0.7/0.25, "ohm;  Prob 27: Rlimit =", 0.7/2, "ohm")')
    md(T('**Nhận xét:** 14,25 V ≈ 14,3 V, 1,3 mA, 2,8 Ω và 0,35 Ω đều khớp đáp án sách.', '**Comment:** 14.25 V ≈ 14.3 V, 1.3 mA, 2.8 Ω and 0.35 Ω all match the book.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm08_voltage_regulators_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
