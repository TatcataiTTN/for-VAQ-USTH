# -*- coding: utf-8 -*-
"""Notebook module 11: tach cap VI + EN, tu chua day du (khong import code cua site), chay that bang nbconvert; moi o 'Doc ket qua' lay so tu chinh ket qua tinh (seq.py)."""
import os, sys, subprocess
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import seq as S
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
CODE = {
'latch': '''# Chot S-R NOR (tac dung muc CAO): mo phong cong lap den khi on dinh
def sr_nor(S, R, Q, Qb):
    for _ in range(10):
        q2 = int(not (R or Qb)); qb2 = int(not (S or q2))
        if (q2, qb2) == (Q, Qb): break
        Q, Qb = q2, qb2
    return Q, Qb
Q, Qb = 0, 1
for S_, R_ in [(1, 0), (0, 0), (0, 1), (0, 0), (1, 1)]:
    Q, Qb = sr_nor(S_, R_, Q, Qb); print('S R =', S_, R_, '-> Q, Qbar =', Q, Qb)
# J-K: bang so voi phuong trinh dac trung Q+ = J.Qbar + Kbar.Q
table = {(0, 0): lambda q: q, (0, 1): lambda q: 0, (1, 0): lambda q: 1, (1, 1): lambda q: 1 - q}
ok = all(table[(j, k)](q) == int((j and not q) or ((not k) and q)) for j in (0, 1) for k in (0, 1) for q in (0, 1))
print('bang J-K = phuong trinh dac trung (8 to hop):', ok)''',
'ripple': '''# Bo dem gon song n bit: moi FF lat khi FF truoc di tu 1 xuong 0
def ripple(n, pulses, start=0):
    q = [(start >> i) & 1 for i in range(n)]
    for _ in range(pulses):
        i = 0
        while i < n:
            q[i] ^= 1
            if q[i] == 1: break
            i += 1
    return sum(b << i for i, b in enumerate(q))
print([format(ripple(3, k), '03b') for k in range(9)])
n, tpd = 5, 15e-9
print('tre tong', n * tpd * 1e9, 'ns; f_max = ', round(1 / (n * tpd) / 1e6, 2), 'MHz; modulus', 2 ** n)
print('Floyd Self-Test 10: 4 FF x 12 ns =', 4 * 12, 'ns')''',
'shift': '''# Thanh ghi dich phai, bit vao o dau trai; bo dem vong va Johnson
def shift_right(reg, bits):                       # bit ngoai cung ben phai cua `bits` vao truoc
    for b in reversed(bits): reg = b + reg[:-1]
    return reg
print('Floyd Self-Test 4 (hai bit ngoai cung ben phai cua 10110101 la 0 va 1):', shift_right('11100100', '01'))
def johnson(n, k):
    r = [0] * n
    for _ in range(k): r = [1 - r[-1]] + r[:-1]
    return ''.join(map(str, r))
def ring(n, k):
    r = [1] + [0] * (n - 1)
    for _ in range(k): r = [r[-1]] + r[:-1]
    return ''.join(map(str, r))
print('Johnson 4:', [johnson(4, k) for k in range(9)]); print('Vong 4   :', [ring(4, k) for k in range(5)])
print('8 bit o 100 kHz:', 8 / 100e3 * 1e6, 'us; tre 24 us can f =', round(8 / 24e-6 / 1e3, 1), 'kHz')''',
'timer': '''# 74121 va 555
import math
tw = 10e-6; C = tw / (0.7 * 2000); print('74121, R = 2 kohm, tW = 10 us -> C =', round(C * 1e12), 'pF')
print('555 mot nhip 2,2 kohm, 0,01 uF:', round(1.1 * 2200 * 1e-8 * 1e6, 1), 'us')
R1, R2, C = 1e3, 2e3, 0.1e-6
tH, tL = 0.7 * (R1 + R2) * C, 0.7 * R2 * C; T = tH + tL
print('555 dao dong: tH, tL, T =', round(tH * 1e3, 3), round(tL * 1e3, 3), round(T * 1e3, 3), 'ms; f =', round(1 / T), 'Hz (cong thuc 1,44:', round(1.44 / ((R1 + 2 * R2) * C)), 'Hz); duty =', round(tH / T * 100, 1), '%')''',
'count': '''# Bo dem cat cut va mac tang
import math
for N in (6, 10, 12, 13, 60): print('modulus', N, '-> so FF =', math.ceil(math.log2(N)))
mods = [5, 8, 10, 10]; print('10 MHz /', math.prod(mods), '=', 10e6 / math.prod(mods) / 1e3, 'kHz (Floyd Self-Test 14)')
print('32768 Hz qua 15 tang chia doi =', 32768 / 2 ** 15, 'Hz')
print('LUT 4 ngo vao: bit =', 2 ** 4, ', so ham =', 2 ** 2 ** 4)''',
}
def text(lang):
    vi = lang == 'vi'; nb = nbf.v4.new_notebook(); c = nb.cells; T = lambda a, b: a if vi else b
    dec = (lambda x: str(x).replace('.', ',')) if vi else str
    c.append(nbf.v4.new_markdown_cell(T('# Module 11: Mạch tuần tự\nNotebook kiểm tra các con số của module (Floyd Ch.7 đến 10). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả" nêu đúng số trong đầu ra.',
                                         '# Module 11: Sequential logic\nA notebook that checks the module\'s numbers (Floyd Ch.7 to 10). Each part: a question, code, then a "Reading the result" cell quoting the numbers in the output.')))
    a5 = S.ripple_delay(5, 15)
    secs = [('latch', T('1. Chốt S-R và flip-flop J-K', '1. The S-R latch and the J-K flip-flop'), T('Chuỗi (S, R) = (1,0), (0,0), (0,1), (0,0), (1,1) cho chốt NOR, và bảng J-K có khớp phương trình đặc trưng không?', 'What does the NOR latch do for (S, R) = (1,0), (0,0), (0,1), (0,0), (1,1), and does the J-K table match the characteristic equation?'),
             T('Q = 1 (đặt), giữ 1, Q = 0 (xoá), giữ 0, rồi (1,1) làm cả hai ngõ ra bằng 0: trạng thái cấm. Bảng J-K trùng phương trình đặc trưng ở cả 8 tổ hợp.', 'Q = 1 (set), hold 1, Q = 0 (reset), hold 0, then (1,1) makes both outputs 0: the forbidden state. The J-K table equals the characteristic equation in all 8 combinations.'), {}),
            ('ripple', T('2. Bộ đếm gợn sóng', '2. The ripple counter'), T('Chuỗi đếm 3 bit, trễ tổng và tần số tối đa của bộ đếm 5 bit với trễ 15 ns.', 'The 3-bit count sequence, and the total delay and maximum frequency of a 5-bit counter with 15 ns stages.'),
             T('Chuỗi 000 đến 111 rồi về 000. Bộ đếm 5 bit: trễ {a} ns, f_max ≈ {b} MHz, modulus 32. Floyd Self-Test 10: 4 × 12 = 48 ns.', 'The sequence runs 000 to 111 then back to 000. The 5-bit counter: delay {a} ns, f_max ≈ {b} MHz, modulus 32. Floyd Self-Test 10: 4 × 12 = 48 ns.'), dict(a=a5, b=f'{1 / (a5 * 1e-9) / 1e6:.2f}')),
            ('shift', T('3. Thanh ghi dịch, vòng và Johnson', '3. Shift register, ring and Johnson'), T('Nội dung sau hai xung (Floyd Self-Test 4), hai chuỗi trạng thái, thời gian nhập nối tiếp.', 'The contents after two pulses (Floyd Self-Test 4), the two state sequences, and the serial entry time.'),
             T('Sau hai xung thanh ghi chứa 01111001. Johnson 4 FF có 8 trạng thái, vòng 4 FF có 4. Nhập 8 bit ở 100 kHz mất 80 μs; trễ 24 μs cần 333,3 kHz.', 'After two pulses the register holds 01111001. A 4-FF Johnson counter has 8 states, a 4-FF ring counter 4. Entering 8 bits at 100 kHz takes 80 μs; a 24 μs delay needs 333.3 kHz.'), {}),
            ('timer', T('4. 74121 và 555', '4. The 74121 and the 555'), T('Tụ cho xung 10 μs, xung 555 một nhịp, và tần số, duty cycle của 555 dao động.', 'The capacitor for a 10 μs pulse, the 555 monostable pulse, and the frequency and duty cycle of a 555 astable.'),
             T('C ≈ 7143 pF (trùng Floyd 7-11); 555 một nhịp 24,2 μs (trùng ví dụ Floyd); 555 dao động T = 0,35 ms, f ≈ 2857 Hz (công thức 1,44 cho 2880 Hz), duty 60 %.', 'C ≈ 7143 pF (matches Floyd 7-11); the 555 monostable gives 24.2 μs (Floyd\'s example); the astable has T = 0.35 ms, f ≈ 2857 Hz (the 1.44 formula gives 2880 Hz), duty 60 %.'), {}),
            ('count', T('5. Modulus, mắc tầng, LUT', '5. Modulus, cascading, LUT'), T('Số flip-flop cho vài modulus, tần số sau chuỗi 5, 8, 10, 10 và số hàm của LUT 4 ngõ vào.', 'Flip-flops for a few moduli, the frequency after a 5, 8, 10, 10 chain, and the function count of a 4-input LUT.'),
             T('Modulus 6, 10, 12, 13 và 60 cần 3, 4, 4, 4 và 6 flip-flop. 10 MHz chia 4000 được 2,5 kHz. LUT 4 ngõ vào lưu 16 bit và thực hiện 65 536 hàm.', 'Moduli 6, 10, 12, 13 and 60 need 3, 4, 4, 4 and 6 flip-flops. 10 MHz divided by 4000 gives 2.5 kHz. A 4-input LUT stores 16 bits and implements 65,536 functions.'), {})]
    for k, title, q, rd, vals in secs:
        c.append(nbf.v4.new_markdown_cell(f'## {title}\n{q}')); c.append(nbf.v4.new_code_cell(CODE[k]))
        c.append(nbf.v4.new_markdown_cell(T('**Đọc kết quả.** ', '**Reading the result.** ') + rd.format(**{a: dec(b) for a, b in vals.items()})))
    return nb
for lg in ('vi', 'en'):
    nb = text(lg); fn = os.path.join(OUT, f'm11_sequential_logic_{lg}.ipynb'); nbf.write(nb, fn)
    r = subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=120', fn], capture_output=True, text=True)
    print(lg, 'nbconvert', r.returncode, r.stderr[-300:] if r.returncode else '')
