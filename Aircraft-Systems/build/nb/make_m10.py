# -*- coding: utf-8 -*-
"""Notebook module 10: tach cap VI + EN, tu chua day du (khong import code cua site), chay that bang nbconvert; moi o 'Doc ket qua' lay so tu chinh ket qua tinh."""
import os, sys, subprocess
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import adda as A
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)

CODE = {
'dac': '''import numpy as np
# DAC trong so nhi phan (Tooley Hinh 3.6a): logic 1 = +5 V, Rf = R, dien tro dau vao R, 2R, 4R, 8R
def dac_weighted(code, n=4, v=5.0):
    bits = [(code >> (n - 1 - k)) & 1 for k in range(n)]
    return -sum(v * b / 2 ** k for k, b in enumerate(bits))           # cong dong dien: -Rf * sum(v*b/R_k)
for c in (0b1010, 0b1111, 0b0001):
    print(format(c, '04b'), round(dac_weighted(c), 4), 'V', '| -0.625 x code =', -0.625 * c)''',
'r2r': '''# Thang R-2R (Floyd Hinh 12-29): giai he phuong trinh nut, khong dung cong thuc dong
R = 1000.0
def r2r_nodal(code, n=4, vref=5.0):
    bits = [(code >> (n - 1 - k)) & 1 for k in range(n)]
    m = n - 1; G = np.zeros((m, m)); b = np.zeros(m)
    for k in range(m):
        G[k, k] += 1 / (2 * R); b[k] += bits[1 + k] * vref / (2 * R); G[k, k] += 1 / R
        if k > 0: G[k, k - 1] -= 1 / R
        if k < m - 1: G[k, k] += 1 / R; G[k, k + 1] -= 1 / R
        else: G[k, k] += 1 / (2 * R)
    v = np.linalg.solve(G, b)
    return -(2 * R) * (bits[0] * vref / (2 * R) + v[0] / R)
for c in (8, 4, 2, 1, 0b1010):
    print(format(c, '04b'), round(r2r_nodal(c), 4), 'V', '| cong thuc dong: ', -5 * c / 8)''',
'sar': '''# ADC xap xi lien tiep 4 bit, trong so 8, 4, 2, 1 V (Floyd Hinh 12-17, 12-18)
def sar(vin, n=4):
    code = 0; trace = []
    for k in range(n):
        trial = code | (1 << (n - 1 - k)); dac = sum(2 ** (n - 1 - j) for j in range(n) if (trial >> (n - 1 - j)) & 1)
        keep = dac <= vin; trace.append((dac, keep))
        if keep: code = trial
    return code, trace
code, trace = sar(5.1); print(format(code, '04b'), trace)
print(format(sar(11.7)[0], '04b'))''',
'flash': '''# ADC flash 3 bit (Tooley Hinh 3.9): nguong 0,5; 1,5; ...; 6,5 V, bo ma hoa uu tien
def flash(vin, n=3):
    outs = [1 if vin > k + 0.5 else 0 for k in range(2 ** n - 1)]
    return max([k + 1 for k, o in enumerate(outs) if o], default=0), outs
for v in (0.3, 2.0, 4.7, 6.9): print(v, format(flash(v)[0], '03b'))''',
'res': '''# Do phan giai, so bo so sanh, Nyquist
for n in (4, 8, 12, 16): print(n, 'bit: do phan giai', round(100 / (2 ** n - 1), 5), '%', '| flash can', 2 ** n - 1, 'bo so sanh')
fmax = 15e3; print('fs toi thieu cho', fmax / 1e3, 'kHz:', 2 * fmax / 1e3, 'kHz')
f, fs = 5.0, 8.0; print('alias cua', f, 'kHz lay mau', fs, 'kHz:', abs(f - fs * round(f / fs)), 'kHz')''',
}
def text(lang):
    vi = lang == 'vi'; nb = nbf.v4.new_notebook(); c = nb.cells
    T = lambda a, b: a if vi else b
    c.append(nbf.v4.new_markdown_cell(T('# Module 10: Chuyển đổi dữ liệu A/D và D/A\nNotebook kiểm tra các con số của module (Tooley Ch.3, Floyd Ch.12). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả" nêu đúng số trong đầu ra.',
                                         '# Module 10: Data conversion A/D and D/A\nA notebook that checks the module\'s numbers (Tooley Ch.3, Floyd Ch.12). Each part: a question, code, then a "Reading the result" cell quoting the numbers in the output.')))
    secs = [('dac', T('1. DAC trọng số nhị phân', '1. Binary-weighted DAC'), T('Điện áp ra của DAC Tooley Hình 3.6a với mã 1010, 1111, 0001?', 'What does the Tooley Figure 3.6a DAC output for codes 1010, 1111, 0001?'),
             T('Mã 1010 cho {a} V và 1111 cho {b} V, khớp Tooley (−6,25 V và −9,375 V); mỗi mã tăng thêm −0,625 V.', 'Code 1010 gives {a} V and 1111 gives {b} V, matching Tooley (−6.25 V and −9.375 V); each code adds −0.625 V.'), dict(a=A.dac_weighted_closed(0b1010), b=A.dac_weighted_closed(0b1111))),
            ('r2r', T('2. Thang R-2R', '2. The R-2R ladder'), T('Giải hệ phương trình nút của thang và so với công thức $-5\\cdot code/8$.', 'Solve the ladder\'s node equations and compare with $-5\\cdot code/8$.'),
             T('Chỉ một bit bằng 1 cho −5; −2,5; −1,25; −0,625 V (Floyd Hình 12-30) và mã 1010 cho {a} V.', 'A single bit at 1 gives −5, −2.5, −1.25, −0.625 V (Floyd Figure 12-30) and code 1010 gives {a} V.'), dict(a=A.dac_r2r_closed(0b1010))),
            ('sar', T('3. ADC xấp xỉ liên tiếp', '3. Successive-approximation ADC'), T('Các bước với 5,1 V và mã ra cho 11,7 V.', 'The steps for 5.1 V and the output code for 11.7 V.'),
             T('5,1 V: 8 V bỏ, 4 V giữ, 6 V bỏ, 5 V giữ, mã 0101 (Floyd). 11,7 V cho mã {a}.', '5.1 V: 8 V reset, 4 V kept, 6 V reset, 5 V kept, code 0101 (Floyd). 11.7 V gives code {a}.'), dict(a=format(A.sar_trace(11.7)[0], '04b'))),
            ('flash', T('4. ADC flash 3 bit', '4. 3-bit flash ADC'), T('Mã ra cho 0,3; 2,0; 4,7; 6,9 V.', 'Output codes for 0.3, 2.0, 4.7, 6.9 V.'),
             T('Vào 2 V cho 010 như Tooley; 6,9 V vượt mọi ngưỡng nên cho 111.', '2 V gives 010 as in Tooley; 6.9 V exceeds every threshold so it gives 111.'), {}),
            ('res', T('5. Độ phân giải, bộ so sánh, Nyquist', '5. Resolution, comparators, Nyquist'), T('Độ phân giải của DAC n bit và số bộ so sánh của flash.', 'Resolution of an n-bit DAC and the flash comparator count.'),
             T('8 bit: {a} % và 255 bộ so sánh; 12 bit: {b} %; 15 kHz cần ít nhất 30 kHz; sóng 5 kHz lấy mẫu 8 kHz hiện thành 3 kHz.', '8 bits: {a} % and 255 comparators; 12 bits: {b} %; 15 kHz needs at least 30 kHz; a 5 kHz wave sampled at 8 kHz appears as 3 kHz.'), dict(a=round(A.resolution_pct(8), 5), b=round(A.resolution_pct(12), 5)))]
    for k, title, q, rd, vals in secs:
        c.append(nbf.v4.new_markdown_cell(f'## {title}\n{q}')); c.append(nbf.v4.new_code_cell(CODE[k]))
        vv = {a: (str(b).replace('.', ',') if vi else b) for a, b in vals.items()}
        c.append(nbf.v4.new_markdown_cell(T('**Đọc kết quả.** ', '**Reading the result.** ') + rd.format(**vv)))
    return nb

for lg in ('vi', 'en'):
    nb = text(lg); fn = os.path.join(OUT, f'm10_data_conversion_{lg}.ipynb'); nbf.write(nb, fn)
    r = subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=120', fn], capture_output=True, text=True)
    print(lg, 'nbconvert', r.returncode, r.stderr[-200:] if r.returncode else '')
