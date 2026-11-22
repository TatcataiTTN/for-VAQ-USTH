# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import nblib
secs = [
 ("""# Toan tu VHDL theo thu tu uu tien (NOT > dich/xoay > AND/OR/XOR) tren vector 4 bit
M = 0xF
nt = lambda v: ~v & M
sla = lambda v: (v << 1) & M
ror = lambda v: ((v >> 1) | ((v & 1) << 3)) & M
p, q = 0b1010, 0b0110
for name, val in (('p AND q', p & q), ('NOT p AND q', nt(p) & q), ('p AND NOT q', p & nt(q)), ('p AND SLA q', p & sla(q)), ('NOT p AND ROR q', nt(p) & ror(q))):
    print(f'{name:18s}', format(val, '04b'))
print('NOT (p AND q) =', format(nt(p & q), '04b'), '(dau ngoac doi thu tu)')""",
  ('1. Toán tử và độ ưu tiên', '1. Operators and precedence'), ('Năm biểu thức của Tooley 17.7 với p = 1010 và q = 0110.', 'Tooley\'s five expressions of 17.7 with p = 1010 and q = 0110.'),
  ('Kết quả 0010, 0100, 1000, 1000, 0001 khớp sách. NOT (p AND q) = 1101 khác NOT p AND q = 0100 vì dấu ngoặc đổi thứ tự.', 'The results 0010, 0100, 1000, 1000, 0001 match the book. NOT (p AND q) = 1101 differs from NOT p AND q = 0100 because the brackets change the order.'), {}),
 ("""# Bo nua cong: bang chan tri hanh vi (XOR, AND) so voi phep cong so hoc; va ban co EN
for x in (0, 1):
    for y in (0, 1):
        s, c = x ^ y, x & y
        assert (s, c) == ((x + y) % 2, (x + y) // 2)
        print(x, y, '->', s, c, '| EN = 0:', 0, 0)""",
  ('2. Bộ nửa cộng', '2. The half adder'), ('Bảng chân trị của bộ nửa cộng và bản có EN.', 'The truth table of the half adder and the version with EN.'),
  ('Sum là XOR, carry là AND; trùng phép cộng số học. Khi EN = 0 cả hai ngõ ra bằng 0.', 'Sum is the XOR and carry the AND, equal to arithmetic addition. With EN = 0 both outputs are 0.'), {}),
 ("""# Tre lan truyen cong don
for n, t in ((3, 15), (4, 15), (5, 12)): print(n, 'cong x', t, 'ns =', n * t, 'ns')
print('XOR 15 ns: a doi tai 100 ns -> c doi tai', 100 + 15, 'ns')""",
  ('3. Trễ lan truyền', '3. Propagation delay'), ('Trễ tổng của vài đường tín hiệu và thời điểm c đổi.', 'The total delay of a few signal paths and when c changes.'),
  ('Ba cổng 15 ns trễ 45 ns (như bộ nửa cộng của Tooley); c đổi tại 115 ns khi a đổi tại 100 ns.', 'Three 15 ns gates delay 45 ns (like Tooley\'s half adder); c changes at 115 ns when a changes at 100 ns.'), {}),
]
nblib.make('m14_vhdl', ('# Module 14: VHDL\nNotebook kiểm tra các con số của module (Tooley Ch.17). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả".', '# Module 14: VHDL\nA notebook that checks the module\'s numbers (Tooley Ch.17). Each part: a question, code, then a "Reading the result" cell.'), secs)
