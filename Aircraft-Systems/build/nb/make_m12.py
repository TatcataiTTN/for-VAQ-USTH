# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'numlib'))
import nblib, avi as A
secs = [
 ("""import math
# Quy dao GPS: Kepler (hang so chuan) va ti le theo quy dao Mat Trang (khong dung mu)
R, mu = 6371e3, 3.986004418e14
r = R + 20200e3
T1 = 2 * math.pi * math.sqrt(r ** 3 / mu) / 3600
T2 = 27.321661 * 24 * (r / 384400e3) ** 1.5
print('Kepler:', round(T1, 3), 'h; ti le Mat Trang:', round(T2, 3), 'h')
print('20200 km =', round(20200 / 1.852), 'hai ly (Tooley lam tron 10900)')""",
  ('1. Quỹ đạo GPS', '1. The GPS orbit'), ('Chu kỳ quỹ đạo ở độ cao 20 200 km có khớp 12 giờ của Tooley không, và đổi 20 200 km sang hải lý?', 'Does the orbital period at 20,200 km agree with Tooley\'s 12 hours, and what is 20,200 km in nautical miles?'),
  ('Kepler cho {a} giờ, tỉ lệ theo Mặt Trăng cho {b} giờ: cả hai gần 12 giờ. 20 200 km là {c} hải lý (sách ghi 10 900).', 'Kepler gives {a} hours and scaling from the Moon gives {b} hours: both are close to 12. 20,200 km is {c} nautical miles (the book says 10,900).'),
  dict(a=f'{A.orbit_period_a(20200) / 3600:.3f}', b=f'{A.orbit_period_b(20200) / 3600:.3f}', c=round(A.km_to_nm(20200)))),
 ("""# Ma C/A va P, chu ky cap nhat FMS
print('C/A: so chip moi chu ky =', round(1.023e6 * 1e-3))
print('P: 267 ngay / 7 ngay =', 267 // 7, 'doan day du')
print('FMS: chu ky moi nam =', 365 // 28, '; 13 x 28 =', 13 * 28, 'ngay')""",
  ('2. Mã GPS và chu kỳ FMS', '2. GPS codes and the FMS cycle'), ('Một chu kỳ mã C/A có bao nhiêu chip và FMS cập nhật mấy lần mỗi năm?', 'How many chips in one C/A period, and how many FMS updates a year?'),
  ('Mã C/A có 1 023 chip. Mã P chia được 38 đoạn bảy ngày đầy đủ. FMS có 13 chu kỳ mỗi năm, tổng 364 ngày.', 'The C/A code has 1,023 chips. The P code splits into 38 full seven-day segments. The FMS has 13 cycles a year, 364 days in all.'), {}),
 ("""# IRS: tich phan gia toc khong doi; sai so cua gia toc ke
def integrate(a, t, n=100000):
    dt = t / n; v = s = 0.0
    for _ in range(n): s += v * dt + 0.5 * a * dt * dt; v += a * dt
    return v, s
print('a = 2, t = 30:', [round(x, 3) for x in integrate(2, 30)], '| cong thuc:', 2 * 30, 0.5 * 2 * 30 ** 2)
print('sai so 0,01 m/s2 sau 40 s:', [round(x, 3) for x in integrate(0.01, 40)])""",
  ('3. IRS tích phân gia tốc', '3. The IRS integrating acceleration'), ('Vận tốc và quãng đường sau 30 s với 2 m/s², và sai số khi gia tốc kế lệch 0,01 m/s².', 'The velocity and distance after 30 s at 2 m/s², and the error when the accelerometer is off by 0.01 m/s².'),
  ('Phép lấy tổng số cho 60 m/s và 900 m, khớp công thức. Sai số 0,01 m/s² sau 40 s thành {a} m/s và {b} m.', 'Numerical summation gives 60 m/s and 900 m, matching the formulas. An error of 0.01 m/s² becomes {a} m/s and {b} m after 40 s.'),
  dict(a=f'{A.speed(0.01, 40):g}', b=f'{A.dist(0.01, 40):g}')),
 ("""# TCAS: thoi gian toi diem tiep can gan nhat tau = d / v_dong
for d, v in ((10, 600), (4, 480), (6, 360), (8, 240 + 240)):
    print(d, 'NM,', v, 'kt ->', round(d / v * 3600), 's')""",
  ('4. TCAS', '4. TCAS'), ('Thời gian τ cho vài cặp (khoảng cách, tốc độ tiếp cận).', 'The time τ for a few (distance, closure rate) pairs.'),
  ('10 NM ở 600 kt là 60 s; 4 NM ở 480 kt là 30 s; hai máy bay 240 kt ngược chiều cách 8 NM có tốc độ tiếp cận 480 kt và τ = 60 s.', '10 NM at 600 kt is 60 s; 4 NM at 480 kt is 30 s; two 240 kt aircraft head-on 8 NM apart close at 480 kt and τ = 60 s.'), {}),
]
nblib.make('m12_avionic_systems', ('# Module 12: Avionics số\nNotebook kiểm tra các con số của module (Tooley 15.4 đến 15.10). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả".', '# Module 12: Digital avionics\nA notebook that checks the module\'s numbers (Tooley 15.4 to 15.10). Each part: a question, code, then a "Reading the result" cell.'), secs)
