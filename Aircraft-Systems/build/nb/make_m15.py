# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import nblib
secs = [
 ("""# Chuong cabin: 494 Hz va 587 Hz keo dai 900 ms
for f in (494, 587):
    print(f, 'Hz: chu ky', round(1000 / f, 3), 'ms; so chu ky trong 900 ms =', round(f * 0.9, 1))
print('ti so tan so 587/494 =', round(587 / 494, 3), '(gan 6/5 = 1.2, khong phai quang tam = 2)')""",
  ('1. Chuông cabin', '1. The cabin chimes'), ('Chu kỳ, số chu kỳ trong 900 ms và tỉ số tần số của hai chuông.', 'The period, the number of cycles in 900 ms and the frequency ratio of the two chimes.'),
  ('494 Hz có chu kỳ 2,024 ms và 444,6 chu kỳ; 587 Hz có chu kỳ 1,704 ms và 528,3 chu kỳ; tỉ số 1,188 gần một quãng ba thứ.', '494 Hz has a 2.024 ms period and 444.6 cycles; 587 Hz has a 1.704 ms period and 528.3 cycles; the ratio 1.188 is close to a minor third.'), {}),
 ("""# Thoi gian nap tep phuong tien vao bo nho IFE (gia dinh cua site: 1 GB = 1e9 byte, bo qua mao dau)
for size in (4.7, 20):
    for name, rate in (('100 Mbit/s', 100e6), ('1 Gbit/s', 1e9)):
        t = size * 8e9 / rate; print(size, 'GB qua', name, '->', round(t, 1), 's =', round(t / 60, 2), 'phut')""",
  ('2. Nạp phương tiện IFE', '2. IFE media loading'), ('Thời gian nạp tệp 4,7 GB và 20 GB qua 100 Mbit/s và 1 Gbit/s.', 'The loading time of a 4.7 GB and a 20 GB file over 100 Mbit/s and 1 Gbit/s.'),
  ('4,7 GB mất 376 s (6,3 phút) ở 100 Mbit/s và 37,6 s ở 1 Gbit/s; tệp 20 GB mất 1 600 s và 160 s. Gigabit nhanh gấp mười lần.', 'A 4.7 GB file takes 376 s (6.3 min) at 100 Mbit/s and 37.6 s at 1 Gbit/s; a 20 GB file takes 1,600 s and 160 s. Gigabit is ten times faster.'), {}),
 ("""# Toc do cat canh B737 dien hinh (Tooley 20.1)
v = {'V1': 124, 'VR': 125, 'V2': 136}
print(sorted(v, key=v.get), '; V2 - V1 =', v['V2'] - v['V1'], 'kt')""",
  ('3. Tốc độ cất cánh', '3. Take-off speeds'), ('Thứ tự và chênh lệch của V1, VR, V2.', 'The order and difference of V1, VR, V2.'),
  ('Thứ tự V1, VR, V2 (124, 125, 136 kt); V2 hơn V1 là 12 kt.', 'The order is V1, VR, V2 (124, 125, 136 kt); V2 exceeds V1 by 12 kt.'), {}),
]
nblib.make('m15_cabin_information', ('# Module 15: Cabin và hệ thống thông tin tàu bay\nNotebook kiểm tra các con số của module (Tooley Ch.19, 20). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả".', '# Module 15: Cabin and aircraft information systems\nA notebook that checks the module\'s numbers (Tooley Ch.19, 20). Each part: a question, code, then a "Reading the result" cell.'), secs)
