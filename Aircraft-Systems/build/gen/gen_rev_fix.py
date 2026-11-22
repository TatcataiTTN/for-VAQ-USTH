# -*- coding: utf-8 -*-
"""Vá cac cau Revision Paper da co trong ngan hang (kiem chung bang scratch/audit_existing_rev.py + doc lai anh trang):
  FIX_FIG  : (paper, n) -> so hinh A2.k de gan anh vao cau (anh cat tu trang scan, assets/figures/tooley_A2_k.png)
  RELABEL  : cau gan nham nhan nguon (paper, n, tep) -> (paper dung, n dung)
  FIXES    : cau dap an/giai thich khong khop khoa in hoac sai (idempotent: ghi de truong, khong cong don)"""
FIX_FIG = {(2, 5): 5, (2, 6): 6, (2, 8): 7, (2, 11): 9, (2, 12): 10, (2, 14): 11, (3, 6): 13, (3, 12): 14, (4, 13): 16, (4, 18): 17, (5, 6): 19,
           (6, 4): 20, (6, 7): 21, (6, 8): 22, (6, 9): 23, (7, 5): 25, (7, 19): 27, (7, 20): 28, (8, 17): 30, (8, 20): 31}
RELABEL = {(2, 20, 'm03.json'): (4, 20)}     # 'chan IC DIL danh so nguoc chieu kim dong ho' la Paper 4 Q20 (khoa in c), khong phai Paper 2 Q20
def bi(vi, en): return dict(vi=vi, en=en)
FIXES = {
    (5, 6): dict(correct=2, explain=bi(
        'Bốn cổng có thân dạng AND (mặt vào phẳng) và vòng tròn đảo ở đầu ra: NAND. Kiểm tra sơ đồ chân: các cặp đầu vào ở chân 1-2, 4-5, 9-10, 12-13, đầu ra ở chân 3, 6, 8, 11 đúng là chip 7400 (4 cổng NAND 2 đầu vào); chip NOR 7402 có đầu ra ở chân 1, 4, 10, 13. Khoá in (b).',
        'The four gates have AND-shaped bodies (flat input side) with an output bubble: NAND. Pin-out check: input pairs on pins 1-2, 4-5, 9-10 and 12-13 and outputs on pins 3, 6, 8 and 11 is exactly the 7400 quad two-input NAND; the 7402 NOR has its outputs on pins 1, 4, 10 and 13. Printed key (b).'),
        q=bi('Thiết bị logic trong Hình A2.19 (IC 14 chân, 4 cổng 2 đầu vào có bong bóng đảo ở đầu ra) là:', 'The logic device shown in Figure A2.19 is:')),
    (4, 18): dict(correct=0, explain=bi(
        'Hai cổng đảo cho A\' và B\', rồi cổng NOR (thân dạng OR có bong bóng): NOR(A\',B\') = (A\'+B\')\' = A·B (De Morgan): cổng AND. Khoá in (b).',
        'Two inverters give A\' and B\', then a NOR gate (OR-shaped body with a bubble): NOR(A\',B\') = (A\'+B\')\' = A·B (De Morgan): an AND gate. Printed key (b).'),
        q=bi('Sắp xếp logic gồm hai cổng đảo (cho A và B) nối vào một cổng NOR (Hình A2.17) tương đương với:', 'The logic arrangement shown in Figure A2.17 (two inverters feeding a NOR gate) is equivalent to:')),
    (4, 2): dict(correct=1,
        opts=[bi('dữ liệu được giữ lại vô thời hạn', 'the memory is retained indefinitely'), bi('dữ liệu mất ngay khi ngắt điện', 'the memory is lost as soon as power is removed'), bi('dữ liệu cần được làm tươi liên tục, kể cả khi đang cấp điện', 'the memory needs to be refreshed constantly, even when power is applied')],
        explain=bi('Bộ nhớ tĩnh (ô lật) là bộ nhớ khả biến: dữ liệu mất ngay khi ngắt điện, nên phương án (b) đúng theo khoá in. Nó không cần làm tươi như RAM động (c). Phương án (a) sai vì "vô thời hạn" bỏ qua việc mất điện; chỉ nói "chừng nào còn cấp điện" mới đúng.',
                   'Static memory (flip-flop cells) is volatile: its contents are lost as soon as power is removed, so (b) is right and follows the printed key. It needs no refresh, unlike dynamic RAM (c). Option (a) is wrong because "indefinitely" ignores loss of power; it would only be true "as long as power is applied".')),
    (6, 10): dict(src=bi('Tooley Revision Paper 6 Q10 (khoá in (c), đúng (b))', 'Tooley Revision Paper 6 Q10 (printed key (c), correct (b))'),
        explain=bi('64K byte = 64K × 8 bit = 512 Kbit; mỗi chip 16K × 4 bit = 64 Kbit (8 KB). 512 ÷ 64 = 8 chip (4 chip nối theo chiều địa chỉ × 2 chip theo chiều rộng dữ liệu 8 bit). Khoá in của sách ghi (c) 16; site dùng đáp án đúng theo tính toán là 8.',
                   '64K bytes = 64K × 8 bits = 512 Kbit; each 16K × 4-bit chip is 64 Kbit (8 KB). 512 ÷ 64 = 8 chips (4 along the address depth × 2 across the 8-bit data width). The book\'s printed key says (c) 16; the site uses the calculated answer, 8.')),
}
