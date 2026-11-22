# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'numlib'))
import nblib, afdx as F
secs = [
 ("""# Bang 16.1 va chon BAG
BAGS = [1, 2, 4, 8, 16, 32, 64, 128]
print({b: 1000 / b for b in BAGS})
def max_bag(rate): return max(b for b in BAGS if 1000 / b >= rate)
print('100/s ->', max_bag(100), 'ms; 400/s ->', max_bag(400), 'ms (khoa in cua sach: 4 ms)')""",
  ('1. BAG', '1. The BAG'), ('Bảng 16.1 và BAG lớn nhất cho 100 và 400 thông điệp mỗi giây.', 'Table 16.1 and the largest BAG for 100 and 400 messages a second.'),
  ('BAG 1 đến 128 ms ứng với 1 000 đến 7,8125 Hz. 100 lần mỗi giây cho BAG 8 ms (khớp ví dụ của Tooley); 400 lần mỗi giây cho 2 ms, vì 4 ms chỉ cho 250 Hz.', 'BAGs of 1 to 128 ms give 1,000 to 7.8125 Hz. 100 a second gives 8 ms (matching Tooley\'s example); 400 a second gives 2 ms because 4 ms is only 250 Hz.'), {}),
 ("""# Toc do bit lon nhat cua VL = L * 8 * 1000 / BAG
for L, bag in ((1518, 4), (256, 128), (64, 2)): print(L, 'byte,', bag, 'ms ->', L * 8 * 1000 / bag, 'bit/s')""",
  ('2. Tốc độ bit của VL', '2. VL bit rate'), ('Tốc độ bit lớn nhất cho khung 1 518 byte với BAG 4 ms và khung 256 byte với BAG 128 ms.', 'The maximum bit rate for 1,518-byte frames with a 4 ms BAG and 256-byte frames with a 128 ms BAG.'),
  ('3 036 000 bit/s (≈ 3 Mbit/s, đúng ví dụ Tooley) và 16 000 bit/s (câu 6 Chương 16).', '3,036,000 bit/s (≈ 3 Mbit/s, Tooley\'s example) and 16,000 bit/s (Chapter 16 Q6).'), {}),
 ("""# Do dai khung AFDX tu cac truong
def frame_len(payload):
    pad = max(0, 17 - payload)
    return 6 + 6 + 2 + 20 + 8 + payload + pad + 1 + 4
print('payload 1:', frame_len(1), '| payload 17:', frame_len(17), '| payload 1471:', frame_len(1471))
for nbytes, rate in ((1518, 10e6), (1518, 100e6)): print(nbytes, 'byte o', rate / 1e6, 'Mbit/s:', nbytes * 8 / rate * 1e3, 'ms')
print('khoang cach giua khung 12 byte o 100 Mbit/s:', 12 * 8 / 100e6 * 1e6, 'us')""",
  ('3. Khung AFDX', '3. The AFDX frame'), ('Độ dài nhỏ nhất, lớn nhất và thời gian truyền.', 'The minimum and maximum length and the transmit time.'),
  ('Payload 1 (đệm 16) và payload 17 đều cho 64 byte; payload 1 471 cho 1 518 byte. Khung dài nhất mất 1,2144 ms ở 10 Mbit/s và 0,12144 ms ở 100 Mbit/s; khoảng cách 12 byte là 0,96 μs ở 100 Mbit/s.', 'A 1-byte payload (16 of padding) and a 17-byte payload both give 64 bytes; a 1,471-byte payload gives 1,518 bytes. The longest frame takes 1.2144 ms at 10 Mbit/s and 0.12144 ms at 100 Mbit/s; the 12-byte gap is 0.96 μs at 100 Mbit/s.'), {}),
 ("""# So thu tu quay vong va lui ham mu nhi phan
sn, seq = 253, []
for _ in range(5): seq.append(sn); sn = 1 if sn == 255 else sn + 1
print(seq)
print([2 ** (n - 1) for n in range(1, 6)], '(boi cua T sau lan va cham thu n)')""",
  ('4. Số thứ tự và lùi hàm mũ', '4. Sequence number and exponential back-off'), ('SN sau 255 là gì, và khoảng lùi sau 1 đến 5 va chạm?', 'What follows SN 255, and the back-off interval after 1 to 5 collisions?'),
  ('Sau 255 là 1 (không phải 0). Khoảng lùi là 1T, 2T, 4T, 8T, 16T.', 'After 255 comes 1 (not 0). The back-off intervals are 1T, 2T, 4T, 8T, 16T.'), {}),
]
nblib.make('m13_data_networks_ima', ('# Module 13: Mạng dữ liệu, AFDX và IMA\nNotebook kiểm tra các con số của module (Tooley Ch.16, 18). Mỗi phần: câu hỏi, mã, rồi ô "Đọc kết quả".', '# Module 13: Data networks, AFDX and IMA\nA notebook that checks the module\'s numbers (Tooley Ch.16, 18). Each part: a question, code, then a "Reading the result" cell.'), secs)
