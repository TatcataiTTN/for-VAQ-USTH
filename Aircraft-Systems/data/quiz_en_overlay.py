# -*- coding: utf-8 -*-
# TU DONG SINH boi build_en_overlay.py, khong sua tay.
EXPLAIN_EN = {"'A' = 65 thập phân = 41 hex (chuẩn ASCII).": "'A' = 65 decimal = 41 hex (ASCII standard).",
 "'A=A' không phải là một luật rút gọn/biến đổi: 3 luật còn lại đều là luật chuẩn (A+1=1, AA=A, A+0=A).": "'A = A' is not a simplification "
                                                                                                          'or transformation law: the '
                                                                                                          'other three are standard laws '
                                                                                                          '(A+1=1, AA=A, A+0=A).',
 "'Data distributor' là tên gọi khác của demultiplexer.": "'Data distributor' is another name for a demultiplexer.",
 "(AB)' = A' + B' theo định lý De Morgan.": "(AB)' = A' + B' by De Morgan's theorem.",
 "(AB)' = A' + B': tổng các phần bù.": "(AB)' = A' + B': the sum of the complements.",
 '0-9 (10 chữ số) + A,B,C,D,E,F (6 chữ cái) = 16 ký tự: đúng.': '0-9 (10 digits) + A, B, C, D, E, F (6 letters) = 16 characters: correct.',
 '0100₂=4 thập phân; hiển thị số 4 trên LED 7 đoạn cần sáng các đoạn b,c,f,g.': '0100₂ = 4 decimal; displaying the digit 4 on a 7-segment '
                                                                                'LED needs segments b, c, f and g lit.',
 '1 byte = 8 bit không dấu → 2⁸ = 256 giá trị, từ 0 đến 255.': '1 byte = 8 unsigned bits → 2⁸ = 256 values, from 0 to 255.',
 '1 byte = 8 bit → cần 8 đường dữ liệu ra để đọc/ghi song song 1 byte.': '1 byte = 8 bits → 8 data output lines are needed to read or '
                                                                         'write one byte in parallel.',
 '1+0+1 = 10₂ (thập phân 2) → bit tổng Σ=0, bit nhớ Cout=1.': '1+0+1 = 10₂ (decimal 2) → sum bit Σ = 0, carry Cout = 1.',
 '1+1+1=11₂ → tổng (Σ)=1, nhớ ra (Cout)=1: đúng, tổng bằng 1.': '1+1+1 = 11₂ → sum (Σ) = 1, carry out (Cout) = 1: correct, the sum is 1.',
 '10011000 có 3 bit 1 (lẻ). 01111000 có 4 bit 1 (chẵn) ✓. 11111111 có 8 bit 1 (chẵn) ✓. 11010101 có 5 bit 1 (lẻ). Vậy chỉ (b) và (c) có parity chẵn.': '10011000 '
                                                                                                                                                       'has '
                                                                                                                                                       'three '
                                                                                                                                                       '1s '
                                                                                                                                                       '(odd). '
                                                                                                                                                       '01111000 '
                                                                                                                                                       'has '
                                                                                                                                                       'four '
                                                                                                                                                       '1s '
                                                                                                                                                       '(even) '
                                                                                                                                                       '✓. '
                                                                                                                                                       '11111111 '
                                                                                                                                                       'has '
                                                                                                                                                       'eight '
                                                                                                                                                       '1s '
                                                                                                                                                       '(even) '
                                                                                                                                                       '✓. '
                                                                                                                                                       '11010101 '
                                                                                                                                                       'has '
                                                                                                                                                       'five '
                                                                                                                                                       '1s '
                                                                                                                                                       '(odd). '
                                                                                                                                                       'So '
                                                                                                                                                       'only '
                                                                                                                                                       '(b) '
                                                                                                                                                       'and '
                                                                                                                                                       '(c) '
                                                                                                                                                       'have '
                                                                                                                                                       'even '
                                                                                                                                                       'parity.',
 '12 thập phân = 1100 nhị phân.': '12 decimal = 1100 binary.',
 '122 = 64+32+16+8+2 → 01111010 (số dương giữ nguyên dạng nhị phân thường).': '122 = 64+32+16+8+2 → 01111010 (a positive number keeps its '
                                                                              'ordinary binary form).',
 '16K từ × 8 bit/từ = 16K byte = 16KB.': '16K words × 8 bits/word = 16K bytes = 16KB.',
 '1→001, 2→010, 7→111 → 001010111, bỏ số 0 thừa đầu → 1010111.': '1→001, 2→010, 7→111 → 001010111; dropping the leading zeros gives '
                                                                 '1010111.',
 '2 đầu vào chọn ra đúng 1 trong 4 đường ra (Y0-Y3): đúng cấu trúc bộ giải mã (decoder) 2-sang-4, dùng cổng NAND để tạo ngõ ra tích cực mức thấp.': '2 '
                                                                                                                                                    'input '
                                                                                                                                                    'lines '
                                                                                                                                                    'select '
                                                                                                                                                    'exactly '
                                                                                                                                                    '1 '
                                                                                                                                                    'of '
                                                                                                                                                    '4 '
                                                                                                                                                    'output '
                                                                                                                                                    'lines '
                                                                                                                                                    '(Y0-Y3): '
                                                                                                                                                    'this '
                                                                                                                                                    'is '
                                                                                                                                                    'the '
                                                                                                                                                    'structure '
                                                                                                                                                    'of '
                                                                                                                                                    'a '
                                                                                                                                                    '2-to-4 '
                                                                                                                                                    'decoder, '
                                                                                                                                                    'using '
                                                                                                                                                    'NAND '
                                                                                                                                                    'gates '
                                                                                                                                                    'to '
                                                                                                                                                    'produce '
                                                                                                                                                    'active-LOW '
                                                                                                                                                    'outputs.',
 '24 bit = 6 chữ số hex, giá trị lớn nhất toàn bit 1 → FFFFFF.': '24 bits = 6 hex digits, and the largest value is all 1s → FFFFFF.',
 '2K byte = 2048 byte; mỗi từ 32-bit = 4 byte; 2048÷4 = 512 từ.': '2K bytes = 2048 bytes; each 32-bit word = 4 bytes; 2048÷4 = 512 words.',
 '2¹⁶ = 65.536 địa chỉ khác nhau.': '2¹⁶ = 65,536 different addresses.',
 '2⁴ = 16 tổ hợp đầu vào khác nhau.': '2⁴ = 16 different input combinations.',
 '2⁴ = 16 ô.': '2⁴ = 16 cells.',
 '2⁸-1 = 255 (đáp án (c) 11111111 là dạng nhị phân chứ không phải số thập phân, dễ nhầm).': '2⁸-1 = 255 (answer (c) 11111111 is a binary '
                                                                                            'form, not a decimal number, which is easy to '
                                                                                            'confuse).',
 '2ⁿ=8 → n=3 đường chọn.': '2ⁿ = 8 → n = 3 select lines.',
 '34 = 00100010, bù một = 11011101, cộng 1 → 11011110.': "34 = 00100010, one's complement = 11011101, add 1 → 11011110.",
 "4 cổng, mỗi cổng hình OR có vòng tròn đảo ở đầu ra = NOR: đúng dạng 'quad two-input NOR gate'.": '4 gates, each an OR shape with an '
                                                                                                   'inversion bubble on the output = NOR: '
                                                                                                   "this matches 'quad two-input NOR "
                                                                                                   "gate'.",
 '4 khối chính tạo nên một hệ máy tính hoàn chỉnh: CPU (xử lý), ROM (bộ nhớ chương trình cố định), RAM (bộ nhớ tạm), I/O (vào/ra).': 'The '
                                                                                                                                     '4 '
                                                                                                                                     'main '
                                                                                                                                     'blocks '
                                                                                                                                     'of a '
                                                                                                                                     'complete '
                                                                                                                                     'computer '
                                                                                                                                     'system: '
                                                                                                                                     'CPU '
                                                                                                                                     '(processing), '
                                                                                                                                     'ROM '
                                                                                                                                     '(fixed '
                                                                                                                                     'program '
                                                                                                                                     'memory), '
                                                                                                                                     'RAM '
                                                                                                                                     '(temporary '
                                                                                                                                     'memory), '
                                                                                                                                     'I/O '
                                                                                                                                     '(input/output).',
 '4→0100, 7→0111, 3→0011 → ghép lại 010001110011, đúng phương án (c).': '4→0100, 7→0111, 3→0011 → joined together gives 010001110011, '
                                                                        'which is option (c).',
 '512=2⁹ → cần 9 đường địa chỉ để mã hoá 512 địa chỉ khác nhau.': '512 = 2⁹ → 9 address lines are needed to encode 512 different '
                                                                  'addresses.',
 '706₈ = 7·64+0·8+6 = 454₁₀ = 1C6₁₆ (1·256+12·16+6=454). Nhị phân đúng của 454 là 111000110, không phải phương án (b).': '706₈ = '
                                                                                                                         '7·64+0·8+6 = '
                                                                                                                         '454₁₀ = 1C6₁₆ '
                                                                                                                         '(1·256+12·16+6 = '
                                                                                                                         '454). The '
                                                                                                                         'correct binary '
                                                                                                                         'form of 454 is '
                                                                                                                         '111000110, not '
                                                                                                                         'option (b).',
 '8 đầu vào dữ liệu (D0-D7), 3 đường chọn (A,B,C), 1 đầu ra (Y) và đầu ra phụ đảo (W): đúng cấu trúc IC 74151, bộ dồn kênh 8-sang-1.': '8 '
                                                                                                                                       'data '
                                                                                                                                       'inputs '
                                                                                                                                       '(D0-D7), '
                                                                                                                                       '3 '
                                                                                                                                       'select '
                                                                                                                                       'lines '
                                                                                                                                       '(A, '
                                                                                                                                       'B, '
                                                                                                                                       'C), '
                                                                                                                                       '1 '
                                                                                                                                       'output '
                                                                                                                                       '(Y) '
                                                                                                                                       'and '
                                                                                                                                       'an '
                                                                                                                                       'inverted '
                                                                                                                                       'complementary '
                                                                                                                                       'output '
                                                                                                                                       '(W): '
                                                                                                                                       'this '
                                                                                                                                       'is '
                                                                                                                                       'the '
                                                                                                                                       'structure '
                                                                                                                                       'of '
                                                                                                                                       'the '
                                                                                                                                       '74151 '
                                                                                                                                       'IC, '
                                                                                                                                       'an '
                                                                                                                                       '8-to-1 '
                                                                                                                                       'multiplexer.',
 'A=8, B=10 → A<B đúng (=1), A>B sai (=0), A=B sai (=0).': 'A = 8, B = 10 → A<B is true (=1), A>B is false (=0), A=B is false (=0).',
 'ALU = Arithmetic Logic Unit, thực hiện cộng/trừ/AND/OR...': 'ALU = Arithmetic Logic Unit, which performs add/subtract/AND/OR and so on.',
 'AND ra 0 bất cứ khi nào có ÍT NHẤT MỘT đầu vào =0: cả hai trường hợp (a) và (b) đều thoả.': 'AND outputs 0 whenever AT LEAST ONE input '
                                                                                              'is 0: both cases (a) and (b) satisfy this.',
 'AND ra 1 khi tất cả đầu vào đều 1, không phải 0.': 'AND outputs 1 when all inputs are 1, not 0.',
 'AX 16-bit gồm AH (byte cao) và AL (byte thấp); 07FEh → AH=07h, AL=FEh=11111110₂.': 'The 16-bit AX consists of AH (high byte) and AL (low '
                                                                                     'byte); 07FEh → AH = 07h, AL = FEh = 11111110₂.',
 'Address bus mang địa chỉ ô nhớ/thiết bị cần truy cập.': 'The address bus carries the address of the memory location or device to be '
                                                          'accessed.',
 "Antifuse ban đầu HỞ mạch (cách điện), khi lập trình sẽ 'đánh thủng' lớp cách điện để nối 2 dây dẫn.": 'An antifuse is initially OPEN '
                                                                                                        "(insulating); programming 'breaks "
                                                                                                        "down' the insulating layer to "
                                                                                                        'connect the two conductors.',
 'A·1=A chính là luật mô tả tình huống này.': 'A·1 = A is exactly the law that describes this situation.',
 "A·A' = 0 (luôn bằng 0), không phải bằng biến A.": "A·A' = 0 (always 0), not equal to the variable A.",
 'BIOS cần giữ được khi mất điện → lưu trong ROM (thường là loại flash ROM).': 'The BIOS must survive power loss → it is stored in ROM '
                                                                               '(usually flash ROM).',
 'Bit dấu nằm ở vị trí NGOÀI CÙNG BÊN TRÁI (MSB), không phải bên phải.': 'The sign bit is at the LEFT-MOST position (MSB), not on the '
                                                                         'right.',
 'Bit dấu=1 (âm). Bù một của 10010011 = 01101100, +1 = 01101101 = 109 → giá trị gốc = −109.': "Sign bit = 1 (negative). One's complement "
                                                                                              'of 10010011 = 01101100, +1 = 01101101 = 109 '
                                                                                              '→ the original value = −109.',
 'Biến Boolean có thể đại diện cho bất kỳ đại lượng logic nào: dữ liệu, điều kiện hay hành động.': 'A Boolean variable can represent any '
                                                                                                   'logical quantity: data, a condition or '
                                                                                                   'an action.',
 'Bus arbitration quyết định thiết bị nào được quyền dùng bus tại một thời điểm, tránh nhiều thiết bị cùng truyền lúc.': 'Bus arbitration '
                                                                                                                         'decides which '
                                                                                                                         'device may use '
                                                                                                                         'the bus at any '
                                                                                                                         'one time, '
                                                                                                                         'preventing '
                                                                                                                         'several devices '
                                                                                                                         'from '
                                                                                                                         'transmitting '
                                                                                                                         'together.',
 'Bus arbitration quyết định thiết bị nào được quyền dùng bus, tránh nhiều thiết bị truyền cùng lúc gây xung đột (bus contention).': 'Bus '
                                                                                                                                     'arbitration '
                                                                                                                                     'decides '
                                                                                                                                     'which '
                                                                                                                                     'device '
                                                                                                                                     'may '
                                                                                                                                     'use '
                                                                                                                                     'the '
                                                                                                                                     'bus, '
                                                                                                                                     'preventing '
                                                                                                                                     'several '
                                                                                                                                     'devices '
                                                                                                                                     'from '
                                                                                                                                     'transmitting '
                                                                                                                                     'at '
                                                                                                                                     'once '
                                                                                                                                     'and '
                                                                                                                                     'causing '
                                                                                                                                     'a '
                                                                                                                                     'conflict '
                                                                                                                                     '(bus '
                                                                                                                                     'contention).',
 'Bát phân dùng đúng 8 chữ số (0-7), mỗi vị trí có trọng số 8ⁱ: đúng.': 'Octal uses exactly 8 digits (0-7), each position having weight '
                                                                        '8ⁱ: correct.',
 'Bìa Karnaugh n biến có 2ⁿ ô; với n=3, số ô = 2³ = 8, không phải 6.': 'An n-variable Karnaugh map has 2ⁿ cells; with n = 3, the number of '
                                                                       'cells = 2³ = 8, not 6.',
 'Bù một = 00110011, cộng 1 → 00110100.': "One's complement = 00110011, add 1 → 00110100.",
 'Bù một của 1111 là 0000, cộng thêm 1 → bù hai = 0001, không phải 0000.': "The one's complement of 1111 is 0000; adding 1 gives the two's "
                                                                           'complement = 0001, not 0000.',
 'Bước fetch đọc mã lệnh từ ô nhớ được PC trỏ tới.': 'The fetch step reads the instruction code from the memory location pointed to by the '
                                                     'PC.',
 "Bẫy từ ngữ: VHDL là 'Hardware DESCRIPTION Language' (ngôn ngữ MÔ TẢ phần cứng), không phải 'definition language' (định nghĩa): phát biểu dùng sai từ nên SAI.": 'Wording '
                                                                                                                                                                  'trap: '
                                                                                                                                                                  'VHDL '
                                                                                                                                                                  'is '
                                                                                                                                                                  'a '
                                                                                                                                                                  "'Hardware "
                                                                                                                                                                  'DESCRIPTION '
                                                                                                                                                                  "Language', "
                                                                                                                                                                  'not '
                                                                                                                                                                  'a '
                                                                                                                                                                  "'definition "
                                                                                                                                                                  "language': "
                                                                                                                                                                  'the '
                                                                                                                                                                  'statement '
                                                                                                                                                                  'uses '
                                                                                                                                                                  'the '
                                                                                                                                                                  'wrong '
                                                                                                                                                                  'word, '
                                                                                                                                                                  'so '
                                                                                                                                                                  'it '
                                                                                                                                                                  'is '
                                                                                                                                                                  'FALSE.',
 'Bộ cộng song song n-bit cộng hai số n-bit cùng lúc; với n=3 → cộng hai số 3-bit.': 'An n-bit parallel adder adds two n-bit numbers at '
                                                                                     'the same time; with n = 3 → it adds two 3-bit '
                                                                                     'numbers.',
 'CAS = Column Address Select, dùng trong DRAM để chốt phần địa chỉ cột.': 'CAS = Column Address Select, used in DRAM to latch the column '
                                                                           'address portion.',
 'CD/DVD/Blu-ray dùng tia laser để đọc/ghi dữ liệu.': 'CD/DVD/Blu-ray use a laser to read and write data.',
 'CMOS có dải điện áp ra gần sát 2 mức nguồn (rail-to-rail) nên noise margin thường lớn hơn TTL.': 'CMOS has an output voltage range close '
                                                                                                   'to both supply levels (rail-to-rail), '
                                                                                                   'so its noise margin is usually larger '
                                                                                                   "than TTL's.",
 'CMOS nổi tiếng vì dòng tĩnh cực thấp → công suất tiêu thụ thấp.': 'CMOS is well known for extremely low static current → low power '
                                                                    'consumption.',
 'CMOS tiêu thụ dòng tĩnh cực thấp, phù hợp thiết bị chạy pin/cầm tay.': 'CMOS draws extremely low static current, which suits '
                                                                         'battery-powered and handheld equipment.',
 'Ceramic DIP là kiểu đóng gói IC thương mại sớm nhất trong ba lựa chọn.': 'Ceramic DIP is the earliest commercial IC package of the three '
                                                                           'choices.',
 'Chu kỳ xung nhịp T = 1/50MHz = 20ns; 11 T-state × 20ns = 220ns.': 'Clock period T = 1/50MHz = 20ns; 11 T-states × 20ns = 220ns.',
 'Chuẩn IEEE 754 single-precision dùng 32 bit.': 'The IEEE 754 single-precision standard uses 32 bits.',
 'Chuẩn VMEbus dùng hai đầu nối DIN 41612 (P1 và P2) mỗi đầu 32 hàng chân.': 'The VMEbus standard uses two DIN 41612 connectors (P1 and '
                                                                             'P2), each with 32 rows of pins.',
 'Chuỗi cổng XOR cho phép tính tổng modulo-2 của các bit, đúng nguyên lý tính parity.': 'A chain of XOR gates lets you compute the '
                                                                                        'modulo-2 sum of the bits, which is exactly the '
                                                                                        'principle of parity generation.',
 'Chân dạng gull-wing dán bề mặt hai bên, kích thước nhỏ gọn: đặc trưng gói SOIC.': 'Gull-wing leads surface-mounted on two sides with a '
                                                                                    'compact size: characteristic of the SOIC package.',
 'Chân enable cho phép nối tầng (cascade) nhiều IC encoder để mở rộng số đầu vào mã hoá.': 'The enable pins allow several encoder ICs to '
                                                                                           'be cascaded to expand the number of encoded '
                                                                                           'inputs.',
 'Chỉ oscilloscope hiển thị được dạng sóng theo thời gian để đo chu kỳ.': 'Only an oscilloscope can display the waveform against time in '
                                                                          'order to measure the period.',
 'Chỉ ra 0 khi cả hai đầu vào đều 0 → đúng đặc trưng cổng OR.': 'Outputs 0 when both inputs are 0 → this is the characteristic of an OR '
                                                                'gate.',
 'Chỉ ra 0 khi cả hai đầu vào đều 1 → đúng đặc trưng cổng NAND.': 'Outputs 0 when both inputs are 1 → this is the characteristic of a NAND '
                                                                  'gate.',
 'Chỉ ra 1 khi cả hai đầu vào đều 0 → đúng đặc trưng cổng NOR (chỉ có 2 lựa chọn trong câu gốc).': 'Outputs 1 when both inputs are 0 → '
                                                                                                   'this is the characteristic of a NOR '
                                                                                                   'gate (only 2 choices in the original '
                                                                                                   'question).',
 'Chỉ ra 1 khi cả hai đầu vào đều 0 → đúng đặc trưng cổng NOR.': 'Outputs 1 when both inputs are 0 → this is the characteristic of a NOR '
                                                                 'gate.',
 'Clock oscillator chuẩn tạo tín hiệu sóng vuông (square wave) ổn định tần số để đồng bộ toàn hệ thống.': 'A standard clock oscillator '
                                                                                                          'produces a frequency-stable '
                                                                                                          'square wave to synchronise the '
                                                                                                          'whole system.',
 'Comparator so sánh hai số nhị phân và đưa ra tín hiệu A>B, A=B hoặc A<B.': 'A comparator compares two binary numbers and produces the '
                                                                             'A>B, A=B or A<B signal.',
 'Control bus mang các tín hiệu điều khiển/định thời (R/W, clock, interrupt...).': 'The control bus carries control/timing signals (R/W, '
                                                                                   'clock, interrupt, and so on).',
 'Các biến nhân với nhau gọi là product term.': 'Variables multiplied together form a product term.',
 'Cả 3 luật đều tồn tại và áp dụng được trong đại số Boolean.': 'All 3 laws exist and can be applied in Boolean algebra.',
 'Cả 3 đều là thuật ngữ chuẩn trong đại số Boolean.': 'All 3 are standard terms in Boolean algebra.',
 'Cả 4 loại đều là bộ nhớ bán dẫn (semiconductor memory).': 'All 4 types are semiconductor memory.',
 'Cần n đường chọn để phân biệt 2ⁿ kênh vào; với 4 kênh, n=2.': 'n select lines are needed to distinguish 2ⁿ input channels; with 4 '
                                                                'channels, n = 2.',
 'Cổng logic đơn lẻ chỉ chứa vài transistor → thuộc quy mô tích hợp nhỏ SSI.': 'A single logic gate contains only a few transistors → it '
                                                                               'belongs to the smallest integration scale, SSI.',
 'Cổng đảo (inverter) đảo dấu tín hiệu: đầu vào lên HIGH khiến đầu ra xuống LOW. Trễ từ sự kiện này chính là tPHL (trễ lan truyền khi output chuyển HIGH→LOW), không phải tPLH.': 'An '
                                                                                                                                                                                  'inverter '
                                                                                                                                                                                  'inverts '
                                                                                                                                                                                  'the '
                                                                                                                                                                                  'signal: '
                                                                                                                                                                                  'the '
                                                                                                                                                                                  'input '
                                                                                                                                                                                  'going '
                                                                                                                                                                                  'HIGH '
                                                                                                                                                                                  'makes '
                                                                                                                                                                                  'the '
                                                                                                                                                                                  'output '
                                                                                                                                                                                  'go '
                                                                                                                                                                                  'LOW. '
                                                                                                                                                                                  'The '
                                                                                                                                                                                  'delay '
                                                                                                                                                                                  'from '
                                                                                                                                                                                  'this '
                                                                                                                                                                                  'event '
                                                                                                                                                                                  'is '
                                                                                                                                                                                  'tPHL '
                                                                                                                                                                                  '(propagation '
                                                                                                                                                                                  'delay '
                                                                                                                                                                                  'when '
                                                                                                                                                                                  'the '
                                                                                                                                                                                  'output '
                                                                                                                                                                                  'goes '
                                                                                                                                                                                  'HIGH→LOW), '
                                                                                                                                                                                  'not '
                                                                                                                                                                                  'tPLH.',
 'Cộng modulo-2 chính là phép XOR: 11 XOR 10 = 01, không phải 100.': 'Modulo-2 addition is the XOR operation: 11 XOR 10 = 01, not 100.',
 'DIL = Dual-In-Line, kiểu đóng gói hai hàng chân song song.': 'DIL = Dual-In-Line, a package with two parallel rows of pins.',
 'DRAM (MOS dynamic memory) lưu dữ liệu bằng điện tích trên tụ điện của từng ô nhớ, cần refresh định kỳ.': 'DRAM (MOS dynamic memory) '
                                                                                                           'stores data as charge on the '
                                                                                                           'capacitor of each cell and '
                                                                                                           'needs periodic refresh.',
 'DRAM lưu dữ liệu dưới dạng điện tích trên một tụ điện nhỏ.': 'DRAM stores data as charge on a tiny capacitor.',
 'Data bus cần truyền dữ liệu cả hai chiều (đọc và ghi) nên buffer phải là hai chiều.': 'The data bus must carry data in both directions '
                                                                                        '(read and write), so the buffer must be '
                                                                                        'bidirectional.',
 'Decoder n-sang-2ⁿ với n=3 → 2³=8 ngõ ra.': 'An n-to-2ⁿ decoder with n = 3 → 2³ = 8 outputs.',
 'Demux đưa 1 nguồn vào ra nhiều đường, ngược với chức năng dồn nhiều vào 1 của mux.': 'A demux takes 1 input source to many lines, the '
                                                                                       'opposite of a mux, which combines many inputs into '
                                                                                       '1.',
 'Domain là tập hợp TẤT CẢ các biến xuất hiện trong biểu thức: A, B, C, D.': 'The domain is the set of ALL variables appearing in the '
                                                                             'expression: A, B, C, D.',
 'Dạng OR + vòng tròn đảo đầu ra = NOR.': 'OR shape + an inversion bubble on the output = NOR.',
 'Dạng XOR (2 đường cong đầu vào) + vòng tròn đảo đầu ra = XNOR.': 'XOR shape (2 curves at the input) + an inversion bubble on the output '
                                                                   '= XNOR.',
 'EPROM (Erasable Programmable ROM) xoá bằng tia UV và lập trình lại được nhiều lần; OTP chỉ ghi được 1 lần, Mask ROM cố định từ khi sản xuất.': 'EPROM '
                                                                                                                                                 '(Erasable '
                                                                                                                                                 'Programmable '
                                                                                                                                                 'ROM) '
                                                                                                                                                 'is '
                                                                                                                                                 'erased '
                                                                                                                                                 'with '
                                                                                                                                                 'UV '
                                                                                                                                                 'light '
                                                                                                                                                 'and '
                                                                                                                                                 'can '
                                                                                                                                                 'be '
                                                                                                                                                 'reprogrammed '
                                                                                                                                                 'many '
                                                                                                                                                 'times; '
                                                                                                                                                 'OTP '
                                                                                                                                                 'can '
                                                                                                                                                 'be '
                                                                                                                                                 'written '
                                                                                                                                                 'only '
                                                                                                                                                 'once '
                                                                                                                                                 'and '
                                                                                                                                                 'Mask '
                                                                                                                                                 'ROM '
                                                                                                                                                 'is '
                                                                                                                                                 'fixed '
                                                                                                                                                 'at '
                                                                                                                                                 'manufacture.',
 'EPROM cần thiết bị lập trình chuyên dụng (device/EPROM programmer).': 'An EPROM needs a dedicated device (EPROM) programmer.',
 'Entity khai báo giao diện (các port) của mạch, architecture mô tả hành vi bên trong.': "An entity declares the circuit's interface (its "
                                                                                         'ports), while the architecture describes the '
                                                                                         'internal behaviour.',
 'Flash memory lưu dữ liệu bằng điện tích trong cổng nổi (floating gate) bán dẫn, không liên quan tới ánh sáng.': 'Flash memory stores '
                                                                                                                  'data as charge in a '
                                                                                                                  'semiconductor floating '
                                                                                                                  'gate, unrelated to '
                                                                                                                  'light.',
 'Full adder cần kết hợp cả XOR VÀ AND/OR để tạo carry-out, không chỉ dùng XOR.': 'A full adder needs both XOR AND AND/OR to produce the '
                                                                                  'carry-out, not just XOR.',
 'Full adder cộng BA đầu vào (2 bit dữ liệu + 1 bit nhớ vào Cin), không phải chỉ 2 bit.': 'A full adder adds THREE inputs (2 data bits + 1 '
                                                                                          'carry-in Cin), not just 2 bits.',
 'Full-adder: 3 đầu vào (A,B,Cin), 2 đầu ra (Σ, Cout).': 'Full adder: 3 inputs (A, B, Cin), 2 outputs (Σ, Cout).',
 'Ghi (write) là thao tác lưu dữ liệu MỚI vào RAM.': 'Write is the operation that stores NEW data in RAM.',
 'Ghép mã ASCII 7-bit của từng ký tự S-T-O-P theo Bảng 2-7 trong sách (đáp án lấy theo answer key gốc của Floyd).': 'Concatenate the 7-bit '
                                                                                                                    'ASCII codes of the '
                                                                                                                    'characters S-T-O-P '
                                                                                                                    'from Table 2-7 in the '
                                                                                                                    'book (the answer '
                                                                                                                    "follows Floyd's own "
                                                                                                                    'answer key).',
 'Ghép tầng (cascade) bằng cách nối Carry-out của tầng thấp vào Carry-in của tầng cao: đúng nguyên lý bộ cộng gợn sóng (ripple carry).': 'Cascading '
                                                                                                                                         'by '
                                                                                                                                         'connecting '
                                                                                                                                         'the '
                                                                                                                                         'carry-out '
                                                                                                                                         'of '
                                                                                                                                         'the '
                                                                                                                                         'lower '
                                                                                                                                         'stage '
                                                                                                                                         'to '
                                                                                                                                         'the '
                                                                                                                                         'carry-in '
                                                                                                                                         'of '
                                                                                                                                         'the '
                                                                                                                                         'higher '
                                                                                                                                         'stage '
                                                                                                                                         'is '
                                                                                                                                         'the '
                                                                                                                                         'principle '
                                                                                                                                         'of '
                                                                                                                                         'the '
                                                                                                                                         'ripple-carry '
                                                                                                                                         'adder.',
 'Giao hoán cho phép đổi chỗ thứ tự nhân.': 'The commutative law allows the order of multiplication to be swapped.',
 'HLT dừng CPU, thuộc nhóm lệnh điều khiển hoạt động của bộ xử lý.': 'HLT halts the CPU and belongs to the group of instructions that '
                                                                     "control the processor's operation.",
 'Hai cách nhập thiết kế phổ biến: nhập bằng mã (HDL text) hoặc bằng sơ đồ (schematic/graphic).': 'Two common design-entry methods: text '
                                                                                                  'entry (HDL code) or graphical entry '
                                                                                                  '(schematic).',
 'Hai họ chính là bipolar (TTL) và CMOS, không phải NMOS.': 'The two main families are bipolar (TTL) and CMOS, not NMOS.',
 'Hai nhóm OR (A+B) và (C+D) được nhân (AND) với nhau.': 'The two OR groups (A+B) and (C+D) are multiplied (ANDed) together.',
 'Half-adder có 2 đầu ra: tổng (Σ) VÀ nhớ (Carry), không phải chỉ có carry.': 'A half adder has 2 outputs: sum (Σ) AND carry, not just '
                                                                              'carry.',
 'Half-adder: 2 đầu vào (A,B), 2 đầu ra (Σ, Cout).': 'Half adder: 2 inputs (A, B), 2 outputs (Σ, Cout).',
 'Hình A = dạng cong lõm không vòng tròn đảo = OR chuẩn. Hình B = dạng AND. Hình C = dạng XOR (2 đường cong ở đầu vào).': 'Shape A = a '
                                                                                                                          'concave curve '
                                                                                                                          'without an '
                                                                                                                          'inversion '
                                                                                                                          'bubble = a '
                                                                                                                          'standard OR. '
                                                                                                                          'Shape B = an '
                                                                                                                          'AND shape. '
                                                                                                                          'Shape C = an '
                                                                                                                          'XOR shape (2 '
                                                                                                                          'curves at the '
                                                                                                                          'input).',
 'Họ logic TTL chuẩn hoạt động ở nguồn 5V ±5%.': 'The standard TTL logic family operates from a 5V ±5% supply.',
 'IC1 là ký hiệu op-amp so sánh (comparator) giữa tín hiệu analog vào và sóng răng cưa từ ramp generator: cấu trúc kinh điển của ADC dốc đơn (single-slope ADC).': 'IC1 '
                                                                                                                                                                   'is '
                                                                                                                                                                   'the '
                                                                                                                                                                   'symbol '
                                                                                                                                                                   'of '
                                                                                                                                                                   'a '
                                                                                                                                                                   'comparator '
                                                                                                                                                                   'op-amp '
                                                                                                                                                                   'between '
                                                                                                                                                                   'the '
                                                                                                                                                                   'analog '
                                                                                                                                                                   'input '
                                                                                                                                                                   'signal '
                                                                                                                                                                   'and '
                                                                                                                                                                   'the '
                                                                                                                                                                   'sawtooth '
                                                                                                                                                                   'wave '
                                                                                                                                                                   'from '
                                                                                                                                                                   'the '
                                                                                                                                                                   'ramp '
                                                                                                                                                                   'generator: '
                                                                                                                                                                   'the '
                                                                                                                                                                   'classic '
                                                                                                                                                                   'structure '
                                                                                                                                                                   'of '
                                                                                                                                                                   'a '
                                                                                                                                                                   'single-slope '
                                                                                                                                                                   'ADC.',
 'IRQ (Interrupt Request) là đường tín hiệu chuẩn để thiết bị ngoại vi yêu cầu CPU phục vụ ngắt.': 'IRQ (Interrupt Request) is the '
                                                                                                   'standard signal line by which a '
                                                                                                   'peripheral asks the CPU to service an '
                                                                                                   'interrupt.',
 "ISP thường cần cả bộ tạo xung nhịp VÀ bộ xử lý nhúng điều khiển qua giao diện JTAG: đáp án đúng theo sách là 'cả (a) và (b)'.": 'ISP '
                                                                                                                                  'usually '
                                                                                                                                  'needs '
                                                                                                                                  'both a '
                                                                                                                                  'clock '
                                                                                                                                  'generator '
                                                                                                                                  'AND an '
                                                                                                                                  'embedded '
                                                                                                                                  'processor '
                                                                                                                                  'controlling '
                                                                                                                                  'through '
                                                                                                                                  'the '
                                                                                                                                  'JTAG '
                                                                                                                                  'interface: '
                                                                                                                                  'the '
                                                                                                                                  'correct '
                                                                                                                                  'answer '
                                                                                                                                  'in the '
                                                                                                                                  'book is '
                                                                                                                                  "'both "
                                                                                                                                  '(a) and '
                                                                                                                                  "(b)'.",
 'Instruction pipelining cho phép chồng lấn các giai đoạn fetch/decode/execute của nhiều lệnh, tăng thông lượng.': 'Instruction pipelining '
                                                                                                                   'overlaps the '
                                                                                                                   'fetch/decode/execute '
                                                                                                                   'stages of several '
                                                                                                                   'instructions, '
                                                                                                                   'increasing throughput.',
 'Instruction pointer/PC chứa địa chỉ lệnh kế tiếp, đưa ra address bus để CPU nạp lệnh.': 'The instruction pointer/PC holds the address of '
                                                                                          'the next instruction and places it on the '
                                                                                          'address bus so the CPU can fetch the '
                                                                                          'instruction.',
 'J=K=1 là chế độ toggle đặc trưng của JK flip-flop.': 'J = K = 1 is the characteristic toggle mode of a JK flip-flop.',
 'JTAG = Joint Test Action Group, chuẩn IEEE 1149.1.': 'JTAG = Joint Test Action Group, the IEEE 1149.1 standard.',
 "Khi hai số bằng nhau, đầu ra 'A=B' của comparator ở mức tích cực (thường là 1/HIGH), không phải 0.": 'When two numbers are equal, the '
                                                                                                       "comparator's 'A = B' output is "
                                                                                                       'active (usually 1/HIGH), not 0.',
 'Khoảng vài trăm tới ~10.000 cổng tương ứng LSI (theo phân loại dùng trong chương này).': 'From a few hundred up to about 10,000 gates '
                                                                                           'corresponds to LSI (by the classification used '
                                                                                           'in this chapter).',
 'Không có lỗi khi phép chia CRC cho số dư bằng 0.': 'There is no error when the CRC division gives a remainder of 0.',
 'Kiến trúc PLD kinh điển dùng mảng AND-OR, với mảng AND lập trình được là chính.': 'The classic PLD architecture uses an AND-OR array, '
                                                                                    'with the programmable AND array as the main feature.',
 "Ký hiệu '27xxx' là quy ước đặt tên chuẩn cho EPROM xoá bằng tia UV (UV-EPROM).": "The '27xxx' marking is the standard naming convention "
                                                                                   'for UV-erasable EPROMs (UV-EPROM).',
 "Ký hiệu '74LS' = Low-power Schottky TTL: đọc trực tiếp trên chip.": "The '74LS' marking = Low-power Schottky TTL: read directly on the "
                                                                      'chip.',
 "Ký hiệu '74LS08': 'LS' = Low-power Schottky TTL, đọc trực tiếp trên chip.": "The '74LS08' marking: 'LS' = Low-power Schottky TTL, read "
                                                                              'directly on the chip.',
 'Ký hiệu OR có vòng tròn đảo ở đầu ra = NOR.': 'An OR symbol with an inversion bubble on the output = NOR.',
 'Kỹ thuật wire-bonding gắn dây vàng/nhôm từ pad tới khung dẫn bằng hàn siêu âm/nhiệt (welded), không phải hàn thiếc thông thường.': 'Wire '
                                                                                                                                     'bonding '
                                                                                                                                     'attaches '
                                                                                                                                     'gold/aluminium '
                                                                                                                                     'wires '
                                                                                                                                     'from '
                                                                                                                                     'the '
                                                                                                                                     'pad '
                                                                                                                                     'to '
                                                                                                                                     'the '
                                                                                                                                     'lead '
                                                                                                                                     'frame '
                                                                                                                                     'by '
                                                                                                                                     'ultrasonic/thermal '
                                                                                                                                     'welding, '
                                                                                                                                     'not '
                                                                                                                                     'by '
                                                                                                                                     'ordinary '
                                                                                                                                     'soldering.',
 'Luật kết hợp cho phép nhóm lại các số hạng cộng theo thứ tự bất kỳ.': 'The associative law allows the added terms to be regrouped in any '
                                                                        'order.',
 'MOV là mã lệnh (opcode); AX là thanh ghi đích, 07FEh là toán hạng dữ liệu.': 'MOV is the operation code (opcode); AX is the destination '
                                                                               'register and 07FEh is the data operand.',
 "Multiplexer thường được gọi là 'data selector' vì chức năng chọn 1 trong nhiều nguồn dữ liệu đưa ra 1 ngõ ra.": 'A multiplexer is often '
                                                                                                                  "called a 'data "
                                                                                                                  "selector' because it "
                                                                                                                  'selects 1 of several '
                                                                                                                  'data sources for a '
                                                                                                                  'single output.',
 'Mã bootstrap phải tồn tại sẵn trước khi RAM được nạp dữ liệu → lưu trong ROM (thường là loại flash ROM/BIOS).': 'The bootstrap code must '
                                                                                                                  'exist before RAM is '
                                                                                                                  'loaded with data → it '
                                                                                                                  'is stored in ROM '
                                                                                                                  '(usually flash '
                                                                                                                  'ROM/BIOS).',
 'Mất điện (RAM volatile) HOẶC bị ghi đè bởi dữ liệu mới đều làm mất dữ liệu cũ.': 'Losing power (RAM is volatile) OR being overwritten by '
                                                                                   'new data both destroy the old data.',
 'Một ô nhớ (memory cell) chỉ lưu được 1 BIT; cần 8 ô nhớ để lưu 1 byte.': 'A memory cell stores only 1 BIT; 8 cells are needed to store 1 '
                                                                           'byte.',
 'NAND (và NOR) là cổng vạn năng; chỉ dùng NAND có thể tạo AND, OR, NOT, v.v.': 'NAND (and NOR) are universal gates; NAND alone can build '
                                                                                'AND, OR, NOT, and so on.',
 'NAND = NOT(AND): chỉ cần thêm 1 cổng đảo ở đầu ra.': 'NAND = NOT(AND): just add one inverter on the output.',
 'NAND = NOT(AND); AND=1 chỉ khi cả 2 vào đều 1, nên NAND=0 khi cả 2 vào đều 1.': 'NAND = NOT(AND); AND = 1 only when both inputs are 1, '
                                                                                  'so NAND = 0 when both inputs are 1.',
 'NAND chỉ ra LOW khi CẢ HAI đầu vào đều HIGH: khoảng chồng lấn là từ t=0.8ms đến t=1ms.': 'NAND goes LOW only when BOTH inputs are HIGH: '
                                                                                           'the overlap runs from t = 0.8ms to t = 1ms.',
 "NAND đầu tiên: (AB)'. NAND thứ 2 nhận cùng tín hiệu (AB)' ở cả 2 đầu vào → hoạt động như cổng đảo: NOT((AB)')=AB. Kết quả = hàm AND.": 'The '
                                                                                                                                         'first '
                                                                                                                                         'NAND '
                                                                                                                                         'gives '
                                                                                                                                         "(AB)'. "
                                                                                                                                         'The '
                                                                                                                                         'second '
                                                                                                                                         'NAND '
                                                                                                                                         'receives '
                                                                                                                                         'the '
                                                                                                                                         'same '
                                                                                                                                         'signal '
                                                                                                                                         "(AB)' "
                                                                                                                                         'on '
                                                                                                                                         'both '
                                                                                                                                         'inputs '
                                                                                                                                         '→ '
                                                                                                                                         'it '
                                                                                                                                         'acts '
                                                                                                                                         'as '
                                                                                                                                         'an '
                                                                                                                                         'inverter: '
                                                                                                                                         "NOT((AB)') "
                                                                                                                                         '= '
                                                                                                                                         'AB. '
                                                                                                                                         'The '
                                                                                                                                         'result '
                                                                                                                                         '= '
                                                                                                                                         'the '
                                                                                                                                         'AND '
                                                                                                                                         'function.',
 "NAND(A',B')=(A'B')'=A+B (De Morgan) = cổng OR.": "NAND(A',B') = (A'B')' = A+B (De Morgan) = an OR gate.",
 "NAND(A',B')=(A'B')'=A+B (De Morgan): cần đảo CẢ HAI đầu vào.": "NAND(A',B') = (A'B')' = A+B (De Morgan): BOTH inputs need to be "
                                                                 'inverted.',
 'NOR chỉ ra 1 khi CẢ HAI đầu vào đều ở logic 0: đây là trường hợp duy nhất.': 'NOR outputs 1 only when BOTH inputs are at logic 0: this '
                                                                               'is the only case.',
 'NOR ra HIGH chỉ khi CẢ HAI đầu vào đều LOW: chỉ đúng trước t=0 và sau t=3ms; NOR xuống LOW ngay khi có 1 xung lên HIGH (t=0) và chỉ lên lại HIGH khi cả hai đều LOW (sau t=3ms).': 'NOR '
                                                                                                                                                                                     'goes '
                                                                                                                                                                                     'HIGH '
                                                                                                                                                                                     'only '
                                                                                                                                                                                     'when '
                                                                                                                                                                                     'BOTH '
                                                                                                                                                                                     'inputs '
                                                                                                                                                                                     'are '
                                                                                                                                                                                     'LOW: '
                                                                                                                                                                                     'true '
                                                                                                                                                                                     'only '
                                                                                                                                                                                     'before '
                                                                                                                                                                                     't '
                                                                                                                                                                                     '= '
                                                                                                                                                                                     '0 '
                                                                                                                                                                                     'and '
                                                                                                                                                                                     'after '
                                                                                                                                                                                     't '
                                                                                                                                                                                     '= '
                                                                                                                                                                                     '3ms; '
                                                                                                                                                                                     'NOR '
                                                                                                                                                                                     'drops '
                                                                                                                                                                                     'LOW '
                                                                                                                                                                                     'as '
                                                                                                                                                                                     'soon '
                                                                                                                                                                                     'as '
                                                                                                                                                                                     'one '
                                                                                                                                                                                     'pulse '
                                                                                                                                                                                     'goes '
                                                                                                                                                                                     'HIGH '
                                                                                                                                                                                     '(t '
                                                                                                                                                                                     '= '
                                                                                                                                                                                     '0) '
                                                                                                                                                                                     'and '
                                                                                                                                                                                     'rises '
                                                                                                                                                                                     'HIGH '
                                                                                                                                                                                     'again '
                                                                                                                                                                                     'only '
                                                                                                                                                                                     'when '
                                                                                                                                                                                     'both '
                                                                                                                                                                                     'are '
                                                                                                                                                                                     'LOW '
                                                                                                                                                                                     '(after '
                                                                                                                                                                                     't '
                                                                                                                                                                                     '= '
                                                                                                                                                                                     '3ms).',
 "NOR(A',B')=(A'+B')'=A·B (De Morgan): chỉ cần đảo từng đầu vào, không cần đảo đầu ra.": "NOR(A',B') = (A'+B')' = A·B (De Morgan): only "
                                                                                         'each input needs inverting, not the output.',
 'NOR=NOT(OR); OR=0 chỉ khi cả hai vào đều 0, nên NOR=1 khi cả hai vào đều 0.': 'NOR = NOT(OR); OR = 0 only when both inputs are 0, so NOR '
                                                                                '= 1 when both inputs are 0.',
 'NOT là cổng đảo 1 đầu vào: đúng.': 'NOT is the single-input inverting gate: correct.',
 'Ngưỡng chuyển mức của CMOS thường ở khoảng 50% Vdd = 6V; 3V < 6V nên được coi là logic 0.': 'The CMOS switching threshold is typically '
                                                                                              'about 50% of Vdd = 6V; 3V < 6V so it is '
                                                                                              'taken as logic 0.',
 'Nhóm 3 bit từ phải (đệm trái): 011 100 101 → 3 4 5 → 345₈.': 'Group 3 bits from the right (pad on the left): 011 100 101 → 3 4 5 → 345₈.',
 'Nhóm 3 bit từ phải, đệm trái đủ nhóm, rồi đổi từng nhóm sang 1 chữ số bát phân.': 'Group 3 bits from the right, pad on the left to '
                                                                                    'complete the group, then convert each group to one '
                                                                                    'octal digit.',
 'Nhóm 3 bit từ phải: 100 010 001 → 4 2 1 → 421₈.': 'Group 3 bits from the right: 100 010 001 → 4 2 1 → 421₈.',
 'Nhóm 4 bit từ phải: 1000 1101 0100 0110 1111 → 8 D 4 6 F.': 'Group 4 bits from the right: 1000 1101 0100 0110 1111 → 8 D 4 6 F.',
 'Nhóm 4 bit: 1011=B, 0011=3 → B3.': 'Group 4 bits: 1011 = B, 0011 = 3 → B3.',
 'Nhị phân dùng 2 chữ số (0,1), trọng số 2ⁱ: đúng.': 'Binary uses 2 digits (0, 1) with weights 2ⁱ: correct.',
 'Nibble = 4 bit; 8 bit là 1 byte, không phải nibble.': 'A nibble = 4 bits; 8 bits is 1 byte, not a nibble.',
 'OR chỉ ra 0 khi TẤT CẢ đầu vào đều 0, không phải chỉ cần một đầu vào bằng 0.': 'OR outputs 0 only when ALL inputs are 0, not when just '
                                                                                 'one input is 0.',
 'OR chỉ ra 0 khi TẤT CẢ đầu vào đều 0: chỉ đúng với trường hợp (a).': 'OR outputs 0 only when ALL inputs are 0: true only for case (a).',
 'Opcode sau khi nạp được đưa vào thanh ghi lệnh (IR) để giải mã.': 'After being fetched, the opcode is placed in the instruction register '
                                                                    '(IR) to be decoded.',
 'PC luôn trỏ tới địa chỉ lệnh tiếp theo cần nạp.': 'The PC always points to the address of the next instruction to be fetched.',
 'PLCC (Plastic Leaded Chip Carrier) cho phép bố trí nhiều chân hơn trong diện tích nhỏ gọn hơn so với DIP.': 'PLCC (Plastic Leaded Chip '
                                                                                                              'Carrier) allows more pins '
                                                                                                              'in a more compact area than '
                                                                                                              'DIP.',
 'POS là tích của nhiều tổng: (A+B)(A+B+C) đúng dạng này.': 'POS is a product of several sums: (A+B)(A+B+C) has exactly this form.',
 'Phép cộng Boolean (+) tương đương hàm OR, không phải NOR.': 'Boolean addition (+) is equivalent to the OR function, not NOR.',
 'Phép đảo bit (NOT) là một phép toán logic, do ALU thực hiện.': 'Bit inversion (NOT) is a logic operation performed by the ALU.',
 "Phần bù của 0 là 1 (0'=1), không phải 0.": "The complement of 0 is 1 (0' = 1), not 0.",
 'Pipelining cho phép chồng lấn các giai đoạn xử lý lệnh, tăng thông lượng thực thi.': 'Pipelining overlaps the instruction-processing '
                                                                                       'stages, increasing execution throughput.',
 'Port khai báo các chân input/output của entity.': 'A port declares the input/output pins of the entity.',
 'Program Counter (PC) chính là tên gọi khác của instruction pointer.': 'The Program Counter (PC) is simply another name for the '
                                                                        'instruction pointer.',
 'Quine-McCluskey là phương pháp đại số thay thế K-map, đặc biệt hữu ích khi số biến ≥5 (K-map khó vẽ).': 'Quine-McCluskey is an algebraic '
                                                                                                          'method that replaces the K-map, '
                                                                                                          'especially useful when there '
                                                                                                          'are 5 or more variables (a '
                                                                                                          'K-map is hard to draw).',
 'Quy tắc chung: nhóm 2ᵏ ô loại bỏ k biến khỏi tích. Với 4 biến, nhóm 4 ô (2²) loại bỏ 2 biến, còn lại đúng 2 biến trong tích.': 'General '
                                                                                                                                 'rule: '
                                                                                                                                 'grouping '
                                                                                                                                 '2ᵏ cells '
                                                                                                                                 'removes '
                                                                                                                                 'k '
                                                                                                                                 'variables '
                                                                                                                                 'from the '
                                                                                                                                 'product. '
                                                                                                                                 'With 4 '
                                                                                                                                 'variables, '
                                                                                                                                 'a group '
                                                                                                                                 'of 4 '
                                                                                                                                 'cells '
                                                                                                                                 '(2²) '
                                                                                                                                 'removes '
                                                                                                                                 '2 '
                                                                                                                                 'variables, '
                                                                                                                                 'leaving '
                                                                                                                                 'exactly '
                                                                                                                                 '2 '
                                                                                                                                 'variables '
                                                                                                                                 'in the '
                                                                                                                                 'product.',
 'Quy ước chuẩn JEDEC: nhìn từ trên xuống, đánh số ngược chiều kim đồng hồ bắt đầu từ pin 1 (góc có khấc/chấm định vị).': 'Standard JEDEC '
                                                                                                                          'convention: '
                                                                                                                          'viewed from the '
                                                                                                                          'top, pins are '
                                                                                                                          'numbered '
                                                                                                                          'anti-clockwise '
                                                                                                                          'starting from '
                                                                                                                          'pin 1 (the '
                                                                                                                          'corner with the '
                                                                                                                          'notch/dot '
                                                                                                                          'marker).',
 "Quy ước chuẩn: '+' cho OR, '·' cho AND, dấu gạch trên cho NOT.": "Standard convention: '+' for OR, '·' for AND, and a bar over a term "
                                                                   'for NOT.',
 'Quy ước logic dương: điện áp cao hơn = 1, điện áp thấp hơn = 0.': 'Positive logic convention: the higher voltage = 1, the lower voltage '
                                                                    '= 0.',
 "Quy ước: Q=1 là trạng thái 'set', Q=0 là trạng thái 'reset'.": "Convention: Q = 1 is the 'set' state and Q = 0 is the 'reset' state.",
 "RAM = Random ACCESS Memory (truy cập ngẫu nhiên), không phải 'random address'.": "RAM = Random ACCESS Memory, not 'random address'.",
 'RAM là bộ nhớ volatile (dễ bay hơi), mất dữ liệu ngay khi ngắt điện.': 'RAM is volatile memory and loses its data as soon as power is '
                                                                         'removed.',
 'ROM giữ dữ liệu vĩnh viễn kể cả khi mất điện: nonvolatile.': 'ROM keeps its data permanently even when power is lost: it is nonvolatile.',
 'ROM là bộ nhớ chỉ đọc, không mất dữ liệu khi mất điện → lưu trữ vĩnh viễn chương trình/dữ liệu cố định.': 'ROM is read-only memory that '
                                                                                                            'keeps its data when power is '
                                                                                                            'lost → permanent storage of '
                                                                                                            'fixed programs/data.',
 'ROM là bộ nhớ non-volatile: dữ liệu vẫn còn khi mất điện.': 'ROM is non-volatile memory: its data remains when power is lost.',
 'SOIC (Small Outline IC) là gói dán bề mặt điển hình.': 'SOIC (Small Outline IC) is a typical surface-mount package.',
 'SOIC là gói dán bề mặt (surface-mount), luôn được hàn trực tiếp lên board, không dùng đế cắm như DIL/PGA.': 'SOIC is a surface-mount '
                                                                                                              'package that is always '
                                                                                                              'soldered directly to the '
                                                                                                              'board, not plugged into a '
                                                                                                              'socket like DIL/PGA.',
 'SOP là tổng của nhiều tích: AB+AC+ABC đúng dạng này; (a) không phải SOP thuần vì có ngoặc lồng.': 'SOP is a sum of several products: '
                                                                                                    'AB+AC+ABC has exactly this form; (a) '
                                                                                                    'is not a pure SOP because of the '
                                                                                                    'nested parentheses.',
 'SPLD cổ điển dùng cầu chì (fusible link) để lập trình kết nối.': 'The classic SPLD uses fusible links to program the connections.',
 "SRAM giữ dữ liệu ổn định suốt thời gian còn cấp điện, KHÔNG cần chu trình refresh như DRAM (nhưng vẫn mất dữ liệu nếu ngắt điện: đây là điểm khác 'retained indefinitely' với 'non-volatile').": 'SRAM '
                                                                                                                                                                                                   'holds '
                                                                                                                                                                                                   'its '
                                                                                                                                                                                                   'data '
                                                                                                                                                                                                   'stably '
                                                                                                                                                                                                   'for '
                                                                                                                                                                                                   'as '
                                                                                                                                                                                                   'long '
                                                                                                                                                                                                   'as '
                                                                                                                                                                                                   'power '
                                                                                                                                                                                                   'is '
                                                                                                                                                                                                   'applied '
                                                                                                                                                                                                   'and '
                                                                                                                                                                                                   'does '
                                                                                                                                                                                                   'NOT '
                                                                                                                                                                                                   'need '
                                                                                                                                                                                                   'a '
                                                                                                                                                                                                   'refresh '
                                                                                                                                                                                                   'cycle '
                                                                                                                                                                                                   'like '
                                                                                                                                                                                                   'DRAM '
                                                                                                                                                                                                   '(but '
                                                                                                                                                                                                   'it '
                                                                                                                                                                                                   'still '
                                                                                                                                                                                                   'loses '
                                                                                                                                                                                                   'data '
                                                                                                                                                                                                   'if '
                                                                                                                                                                                                   'power '
                                                                                                                                                                                                   'is '
                                                                                                                                                                                                   'removed: '
                                                                                                                                                                                                   'this '
                                                                                                                                                                                                   'is '
                                                                                                                                                                                                   'the '
                                                                                                                                                                                                   'difference '
                                                                                                                                                                                                   'between '
                                                                                                                                                                                                   "'retained "
                                                                                                                                                                                                   "indefinitely' "
                                                                                                                                                                                                   'and '
                                                                                                                                                                                                   "'non-volatile').",
 'SRAM vẫn là bộ nhớ volatile (dễ bay hơi): mất dữ liệu khi mất điện, giống DRAM.': 'SRAM is still volatile memory: it loses its data when '
                                                                                    'power is removed, just like DRAM.',
 'Segmentation kết hợp segment+offset giúp CPU 16-bit địa chỉ hoá vùng nhớ lớn hơn khả năng thanh ghi 16-bit thuần tuý.': 'Segmentation '
                                                                                                                          'combines '
                                                                                                                          'segment + '
                                                                                                                          'offset so a '
                                                                                                                          '16-bit CPU can '
                                                                                                                          'address a '
                                                                                                                          'memory area '
                                                                                                                          'larger than a '
                                                                                                                          'pure 16-bit '
                                                                                                                          'register '
                                                                                                                          'allows.',
 'Stack dùng lưu tạm địa chỉ trả về, giá trị thanh ghi khi gọi hàm/ngắt.': 'The stack temporarily stores return addresses and register '
                                                                           'values during function calls/interrupts.',
 'Stack là một vùng của bộ nhớ RAM ngoài, được quản lý bởi con trỏ stack (SP).': 'The stack is an area of external RAM managed by the '
                                                                                 'stack pointer (SP).',
 'Sơ đồ chân khớp chính xác với IC 74148: bộ mã hoá ưu tiên 8-sang-3 đường (8-to-3 priority encoder).': 'The pin layout matches the 74148 '
                                                                                                        'IC exactly: an 8-to-3 line '
                                                                                                        'priority encoder.',
 'Số bát phân chỉ dùng chữ số 0-7; 139 chứa chữ số 9 nên không hợp lệ.': 'An octal number uses only the digits 0-7; 139 contains the digit '
                                                                         '9 so it is not valid.',
 'Số tổ hợp = 2ⁿ với n=3 → 2³ = 8.': 'Number of combinations = 2ⁿ with n = 3 → 2³ = 8.',
 'TTL chuẩn (74 series) thường đạt tần số hoạt động tối đa khoảng 35MHz.': 'Standard TTL (74 series) typically reaches a maximum operating '
                                                                           'frequency of about 35MHz.',
 'TTL chuẩn có fan-out danh định là 10 (điều khiển được tối đa 10 đầu vào TTL cùng họ).': 'Standard TTL has a nominal fan-out of 10 (it '
                                                                                          'can drive up to 10 TTL inputs of the same '
                                                                                          'family).',
 'TTL chuẩn có noise margin danh định khoảng 400mV.': 'Standard TTL has a nominal noise margin of about 400mV.',
 'Theo mô tả sách, chu kỳ máy M1 là chu kỳ nạp và giải mã lệnh (opcode fetch).': 'As the book describes it, machine cycle M1 is the opcode '
                                                                                 'fetch cycle (fetch and decode of the instruction).',
 'Theo sách, ADDRESS-BURST là tên một chân/tính năng cụ thể của SRAM đồng bộ (synchronous SRAM) được trình bày trong chương này.': 'According '
                                                                                                                                   'to the '
                                                                                                                                   'book, '
                                                                                                                                   'ADDRESS-BURST '
                                                                                                                                   'is the '
                                                                                                                                   'name '
                                                                                                                                   'of a '
                                                                                                                                   'specific '
                                                                                                                                   'pin/feature '
                                                                                                                                   'of '
                                                                                                                                   'synchronous '
                                                                                                                                   'SRAM '
                                                                                                                                   'presented '
                                                                                                                                   'in '
                                                                                                                                   'this '
                                                                                                                                   'chapter.',
 'Theo định nghĩa trong sách, memory latency được tính theo góc nhìn thời gian truy cập của bộ xử lý (processor access time) tới bộ nhớ.': 'By '
                                                                                                                                           'the '
                                                                                                                                           "book's "
                                                                                                                                           'definition, '
                                                                                                                                           'memory '
                                                                                                                                           'latency '
                                                                                                                                           'is '
                                                                                                                                           'measured '
                                                                                                                                           'from '
                                                                                                                                           'the '
                                                                                                                                           'viewpoint '
                                                                                                                                           'of '
                                                                                                                                           'the '
                                                                                                                                           "processor's "
                                                                                                                                           'access '
                                                                                                                                           'time '
                                                                                                                                           'to '
                                                                                                                                           'memory.',
 "Thuật ngữ chuẩn cho một chip cắt rời từ wafer là 'die'.": "The standard term for an individual chip cut from a wafer is a 'die'.",
 "Thuật ngữ chuẩn là 'data center'.": "The standard term is 'data center'.",
 'Thập niên 1980, DIL (Dual-In-Line) là kiểu đóng gói phổ biến nhất cho IC logic chuẩn.': 'In the 1980s, DIL (Dual-In-Line) was the most '
                                                                                          'common package style for standard logic ICs.',
 'Thứ tự tăng dần mật độ: SSI < MSI < LSI < VLSI; trong 3 lựa chọn, LSI lớn nhất.': 'Order of increasing density: SSI < MSI < LSI < VLSI; '
                                                                                    'of the 3 choices, LSI is the largest.',
 'Tri-state có thêm trạng thái trở kháng cao (high-Z) ngoài 0 và 1.': 'Tri-state has a high-impedance (high-Z) state in addition to 0 and '
                                                                      '1.',
 "Trong hex, 9+1 = A (10 thập phân được viết là A trong hex), không phải '10'.": 'In hex, 9 + 1 = A (decimal 10 is written A in hex), not '
                                                                                 "'10'.",
 'Tách nhóm 4 bit: 1001=9, 0001=1 → 91.': 'Split into 4-bit groups: 1001 = 9, 0001 = 1 → 91.',
 'Tổng các biến nối bằng dấu + gọi là sum term.': 'A sum of variables joined by + is called a sum term.',
 'Vi xử lý VLSI dùng công nghệ MOS với lớp oxit cực mỏng ở cổng transistor: cực kỳ nhạy với phóng tĩnh điện (ESD) hơn hẳn linh kiện lưỡng cực (BJT/SCR).': 'A '
                                                                                                                                                           'VLSI '
                                                                                                                                                           'microprocessor '
                                                                                                                                                           'uses '
                                                                                                                                                           'MOS '
                                                                                                                                                           'technology '
                                                                                                                                                           'with '
                                                                                                                                                           'an '
                                                                                                                                                           'extremely '
                                                                                                                                                           'thin '
                                                                                                                                                           'oxide '
                                                                                                                                                           'layer '
                                                                                                                                                           'at '
                                                                                                                                                           'the '
                                                                                                                                                           'transistor '
                                                                                                                                                           'gate: '
                                                                                                                                                           'far '
                                                                                                                                                           'more '
                                                                                                                                                           'sensitive '
                                                                                                                                                           'to '
                                                                                                                                                           'electrostatic '
                                                                                                                                                           'discharge '
                                                                                                                                                           '(ESD) '
                                                                                                                                                           'than '
                                                                                                                                                           'bipolar '
                                                                                                                                                           'devices '
                                                                                                                                                           '(BJT/SCR).',
 'Vi xử lý chứa hàng triệu transistor → thuộc quy mô tích hợp rất lớn VLSI.': 'A microprocessor contains millions of transistors → it '
                                                                              'belongs to the very large scale of integration, VLSI.',
 'Vài chục tới ~100 cổng logic tương ứng quy mô tích hợp vừa MSI.': 'A few tens up to about 100 logic gates corresponds to medium-scale '
                                                                    'integration, MSI.',
 'Wafer được kiểm tra (wafer probing) ngay khi còn nguyên tấm, trước công đoạn cắt (dicing).': 'The wafer is tested (wafer probing) while '
                                                                                               'still whole, before the dicing step.',
 "X=A'+B, Y=(BC)'. Với A=B=C=0: X=1+0=1 ✓; Y=(0·0)'=1 ✓. Với B=C=1 (đáp án c): Y=(1·1)'=0, tức sai. Đáp án đúng là tất cả đầu vào ở logic 0.": 'X '
                                                                                                                                               '= '
                                                                                                                                               "A'+B, "
                                                                                                                                               'Y '
                                                                                                                                               '= '
                                                                                                                                               "(BC)'. "
                                                                                                                                               'With '
                                                                                                                                               'A '
                                                                                                                                               '= '
                                                                                                                                               'B '
                                                                                                                                               '= '
                                                                                                                                               'C '
                                                                                                                                               '= '
                                                                                                                                               '0: '
                                                                                                                                               'X '
                                                                                                                                               '= '
                                                                                                                                               '1+0 '
                                                                                                                                               '= '
                                                                                                                                               '1 '
                                                                                                                                               '✓; '
                                                                                                                                               'Y '
                                                                                                                                               '= '
                                                                                                                                               "(0·0)' "
                                                                                                                                               '= '
                                                                                                                                               '1 '
                                                                                                                                               '✓. '
                                                                                                                                               'With '
                                                                                                                                               'B '
                                                                                                                                               '= '
                                                                                                                                               'C '
                                                                                                                                               '= '
                                                                                                                                               '1 '
                                                                                                                                               '(answer '
                                                                                                                                               'c): '
                                                                                                                                               'Y '
                                                                                                                                               '= '
                                                                                                                                               "(1·1)' "
                                                                                                                                               '= '
                                                                                                                                               '0, '
                                                                                                                                               'which '
                                                                                                                                               'is '
                                                                                                                                               'wrong. '
                                                                                                                                               'The '
                                                                                                                                               'correct '
                                                                                                                                               'answer '
                                                                                                                                               'is '
                                                                                                                                               'all '
                                                                                                                                               'inputs '
                                                                                                                                               'at '
                                                                                                                                               'logic '
                                                                                                                                               '0.',
 "X=OR(A,B)=1+1=1. Y=AND(A,B,C,D')=1·1·1·0=0 (vì D'=NOT(1)=0). Vậy X=1,Y=0.": "X = OR(A,B) = 1+1 = 1. Y = AND(A,B,C,D') = 1·1·1·0 = 0 "
                                                                              "(since D' = NOT(1) = 0). So X = 1, Y = 0.",
 'XOR chỉ ra 1 khi hai đầu vào KHÁC nhau; (1,1) cho ra 0.': 'XOR outputs 1 only when the two inputs are DIFFERENT; (1,1) gives 0.',
 'XOR ra 1 khi hai đầu vào KHÁC nhau (trái dấu), ra 0 khi GIỐNG nhau: ngược với phát biểu.': 'XOR outputs 1 when the two inputs are '
                                                                                             'DIFFERENT and 0 when they are the SAME: the '
                                                                                             'opposite of the statement.',
 'XOR ra HIGH khi hai đầu vào KHÁC nhau: từ t=0-0.8ms khác nhau (HIGH), từ 0.8-1ms giống nhau (LOW), từ 1-3ms khác nhau (HIGH): khớp cả (b) và (c).': 'XOR '
                                                                                                                                                      'goes '
                                                                                                                                                      'HIGH '
                                                                                                                                                      'when '
                                                                                                                                                      'the '
                                                                                                                                                      'two '
                                                                                                                                                      'inputs '
                                                                                                                                                      'are '
                                                                                                                                                      'DIFFERENT: '
                                                                                                                                                      'from '
                                                                                                                                                      't '
                                                                                                                                                      '= '
                                                                                                                                                      '0-0.8ms '
                                                                                                                                                      'they '
                                                                                                                                                      'differ '
                                                                                                                                                      '(HIGH), '
                                                                                                                                                      'from '
                                                                                                                                                      '0.8-1ms '
                                                                                                                                                      'they '
                                                                                                                                                      'are '
                                                                                                                                                      'the '
                                                                                                                                                      'same '
                                                                                                                                                      '(LOW), '
                                                                                                                                                      'from '
                                                                                                                                                      '1-3ms '
                                                                                                                                                      'they '
                                                                                                                                                      'differ '
                                                                                                                                                      '(HIGH): '
                                                                                                                                                      'this '
                                                                                                                                                      'matches '
                                                                                                                                                      'both '
                                                                                                                                                      '(b) '
                                                                                                                                                      'and '
                                                                                                                                                      '(c).',
 "Y = A'B + AB' = A XOR B: đúng cấu trúc kinh điển dựng cổng XOR từ NOT+AND+OR.": "Y = A'B + AB' = A XOR B: exactly the classic structure "
                                                                                  'for building an XOR gate from NOT + AND + OR.',
 'f = 1/T: nghịch đảo của chu kỳ.': 'f = 1/T: the reciprocal of the period.',
 'log2(8)=3 bit đủ để mã hoá 8 trạng thái đầu vào.': 'log2(8) = 3 bits are enough to encode 8 input states.',
 'Đáp án theo sách là (c). Lưu ý: các số hạng gốc trong sách có dấu gạch trên (phần bù) ở một số biến: dấu gạch này bị mất khi trích xuất text thuần, nên không thể tự suy luận lại đầy đủ; giữ nguyên đáp án in trong sách.': 'The '
                                                                                                                                                                                                                               'answer '
                                                                                                                                                                                                                               'follows '
                                                                                                                                                                                                                               'the '
                                                                                                                                                                                                                               'book: '
                                                                                                                                                                                                                               '(c). '
                                                                                                                                                                                                                               'Note: '
                                                                                                                                                                                                                               'some '
                                                                                                                                                                                                                               'variables '
                                                                                                                                                                                                                               'in '
                                                                                                                                                                                                                               'the '
                                                                                                                                                                                                                               "book's "
                                                                                                                                                                                                                               'original '
                                                                                                                                                                                                                               'terms '
                                                                                                                                                                                                                               'carry '
                                                                                                                                                                                                                               'an '
                                                                                                                                                                                                                               'overbar '
                                                                                                                                                                                                                               '(complement), '
                                                                                                                                                                                                                               'which '
                                                                                                                                                                                                                               'is '
                                                                                                                                                                                                                               'lost '
                                                                                                                                                                                                                               'when '
                                                                                                                                                                                                                               'the '
                                                                                                                                                                                                                               'text '
                                                                                                                                                                                                                               'is '
                                                                                                                                                                                                                               'extracted '
                                                                                                                                                                                                                               'as '
                                                                                                                                                                                                                               'plain '
                                                                                                                                                                                                                               'text, '
                                                                                                                                                                                                                               'so '
                                                                                                                                                                                                                               'it '
                                                                                                                                                                                                                               'cannot '
                                                                                                                                                                                                                               'be '
                                                                                                                                                                                                                               'fully '
                                                                                                                                                                                                                               're-derived '
                                                                                                                                                                                                                               'independently; '
                                                                                                                                                                                                                               'the '
                                                                                                                                                                                                                               'answer '
                                                                                                                                                                                                                               'printed '
                                                                                                                                                                                                                               'in '
                                                                                                                                                                                                                               'the '
                                                                                                                                                                                                                               'book '
                                                                                                                                                                                                                               'is '
                                                                                                                                                                                                                               'kept.',
 "Đây chính là 1 trong 2 định lý De Morgan: (AB)'=A'+B'.": "This is exactly one of the two De Morgan theorems: (AB)' = A'+B'.",
 'Đây chính là dạng chuẩn của luật phân phối trong đại số Boolean.': 'This is the standard form of the distributive law in Boolean '
                                                                     'algebra.',
 'Đây chính là nguyên lý hoạt động của kiểm tra chẵn lẻ.': 'This is the operating principle of parity checking.',
 'Đây chính là định nghĩa của bộ nhớ truy cập ngẫu nhiên (RAM/ROM về bản chất vật lý).': 'This is the definition of random-access memory '
                                                                                         '(RAM/ROM in terms of physical nature).',
 'Đây chính là định nghĩa của fan-in.': 'This is exactly the definition of fan-in.',
 'Đây là cấu trúc bộ đếm không đồng bộ (ripple counter): mỗi tầng lấy clock từ Q của tầng trước.': 'This is the structure of an '
                                                                                                   'asynchronous (ripple) counter: each '
                                                                                                   'stage takes its clock from the Q of '
                                                                                                   'the previous stage.',
 "Đây là luật hấp thụ mở rộng: A + A'B = A + B.": "This is the extended absorption law: A + A'B = A + B.",
 'Đây là mô tả của DEMULTIPLEXER (1 vào, nhiều ra); multiplexer làm NGƯỢC LẠI: nhiều nguồn vào, chọn ra 1 đường.': 'This describes a '
                                                                                                                   'DEMULTIPLEXER (1 '
                                                                                                                   'input, many outputs); '
                                                                                                                   'a multiplexer does the '
                                                                                                                   'OPPOSITE: many input '
                                                                                                                   'sources, one selected '
                                                                                                                   'output line.',
 'Đây thực chất là CÙNG MỘT loại thiết bị được gọi theo 2 tên khác nhau, không phải hai loại khác nhau.': 'These are actually the SAME '
                                                                                                          'kind of device with two '
                                                                                                          'different names, not two '
                                                                                                          'different kinds.',
 'Đúng theo chức năng cơ bản của decoder.': 'True by the basic function of a decoder.',
 'Đúng theo định nghĩa chuẩn của fan-out.': 'True by the standard definition of fan-out.',
 'Đúng theo định nghĩa chuẩn.': 'True by the standard definition.',
 'Đúng theo định nghĩa cổng NOT.': 'True by the definition of the NOT gate.',
 'Đúng theo định nghĩa half-adder.': 'True by the definition of a half adder.',
 'Đúng theo định nghĩa.': 'True by definition.',
 'Đúng theo định nghĩa/tên gọi.': 'True by definition/name.',
 'Đúng với PLD khả trình lại (reprogrammable), như SRAM-based FPGA/CPLD.': 'True for reprogrammable PLDs, such as SRAM-based FPGAs/CPLDs.',
 'Đúng định nghĩa multiplexer: nhiều đầu vào, 1 đầu ra, chọn bằng các đường select.': 'The definition of a multiplexer: many inputs, 1 '
                                                                                      'output, selected by the select lines.',
 'Đúng: DRAM lưu dữ liệu bằng điện tích trên tụ điện, bị rò rỉ nên cần refresh.': 'True: DRAM stores data as charge on a capacitor, which '
                                                                                  'leaks, so it needs refreshing.',
 'Đúng: NAND = NOT(AND).': 'True: NAND = NOT(AND).',
 'Đúng: NOR = NOT(OR).': 'True: NOR = NOT(OR).',
 'Đúng: cache lưu tạm dữ liệu/lệnh hay dùng để tăng tốc truy cập.': 'True: cache temporarily holds frequently used data/instructions to '
                                                                    'speed up access.',
 'Đúng: data bus vừa đọc vừa ghi được, khác address bus (một chiều).': 'True: the data bus can both read and write, unlike the address bus '
                                                                       '(one-way).',
 'Đúng: encoder và decoder là hai chức năng ngược nhau.': 'True: an encoder and a decoder are two opposite functions.',
 'Đúng: phép nhân Boolean (·) chính là AND.': 'True: Boolean multiplication (·) is exactly AND.',
 'Đúng: thanh ghi nhanh nhất, nằm ngay trong CPU, đứng đầu hệ thống phân cấp bộ nhớ.': 'True: registers are the fastest, located right '
                                                                                       'inside the CPU, at the top of the memory '
                                                                                       'hierarchy.',
 'Đúng: đây chính là mục đích chính của K-map.': 'True: this is precisely the main purpose of the K-map.',
 'Đúng: đây là 2 khối cấu trúc cơ bản bắt buộc của VHDL.': 'True: these are the 2 required basic structural blocks of VHDL.',
 'Đảo bit: 01001, cộng 1 → 01010.': 'Invert the bits: 01001, add 1 → 01010.',
 'Đảo bit: 10010, cộng 1 → 10011.': 'Invert the bits: 10010, add 1 → 10011.',
 'Đảo từng bit: 1→0, 0→1 → 00001111.': 'Invert each bit: 1→0, 0→1 → 00001111.',
 'Đảo từng bit: 1→0, 0→1, 1→0, 0→1 → 0101: đúng.': 'Invert each bit: 1→0, 0→1, 1→0, 0→1 → 0101: correct.',
 'Đảo và bù là hai tên gọi tương đương của cùng phép toán NOT.': 'Inversion and complementation are two equivalent names for the same NOT '
                                                                 'operation.',
 'Đầu vào LOW(0) → đầu ra HIGH, tức mức logic 1.': 'Input LOW (0) → output HIGH, that is, logic level 1.',
 'Đếm số bit 1: 1010011→4(chẵn), 1101000→3(lẻ), 1001000→2(chẵn), 1110111→6(chẵn). Với quy ước parity chẵn, mã có SỐ BIT 1 LẺ là mã lỗi → 1101000.': 'Counting '
                                                                                                                                                    'the '
                                                                                                                                                    '1 '
                                                                                                                                                    'bits: '
                                                                                                                                                    '1010011 '
                                                                                                                                                    '→ '
                                                                                                                                                    '4 '
                                                                                                                                                    '(even), '
                                                                                                                                                    '1101000 '
                                                                                                                                                    '→ '
                                                                                                                                                    '3 '
                                                                                                                                                    '(odd), '
                                                                                                                                                    '1001000 '
                                                                                                                                                    '→ '
                                                                                                                                                    '2 '
                                                                                                                                                    '(even), '
                                                                                                                                                    '1110111 '
                                                                                                                                                    '→ '
                                                                                                                                                    '6 '
                                                                                                                                                    '(even). '
                                                                                                                                                    'With '
                                                                                                                                                    'the '
                                                                                                                                                    'even-parity '
                                                                                                                                                    'convention, '
                                                                                                                                                    'the '
                                                                                                                                                    'code '
                                                                                                                                                    'with '
                                                                                                                                                    'an '
                                                                                                                                                    'ODD '
                                                                                                                                                    'number '
                                                                                                                                                    'of '
                                                                                                                                                    '1 '
                                                                                                                                                    'bits '
                                                                                                                                                    'is '
                                                                                                                                                    'the '
                                                                                                                                                    'faulty '
                                                                                                                                                    'one '
                                                                                                                                                    '→ '
                                                                                                                                                    '1101000.',
 'Định nghĩa fan-out chính là số tải đầu vào chuẩn tối đa mà ngõ ra có thể điều khiển.': 'The definition of fan-out is the maximum number '
                                                                                         'of standard input loads an output can drive.',
 'Ưu tiên chọn đầu vào có chỉ số CAO NHẤT trong các đầu vào tích cực {0,2,5,6} → chọn 6 → mã nhị phân 110.': 'Select the input with the '
                                                                                                             'HIGHEST index among the '
                                                                                                             'active inputs {0, 2, 5, 6} → '
                                                                                                             '6 is selected → binary code '
                                                                                                             '110.'}
OPT_EN_BY_Q = {'ADDRESS-BURST là một tính năng của:': {'DRAM fast page mode': 'fast page mode DRAM',
                                         'DRAM đồng bộ': 'synchronous DRAM',
                                         'SRAM không đồng bộ': 'asynchronous SRAM',
                                         'SRAM đồng bộ': 'synchronous SRAM'},
 'Antifuse được tạo thành từ:': {'hai dây dẫn ngăn cách bởi một lớp cách điện': 'two conductors separated by an insulator',
                                 'hai dây dẫn nối tiếp': 'two conductors connected in a series',
                                 'hai lớp cách điện ngăn cách bởi một dây dẫn': 'two insulators separated by a conductor',
                                 'một lớp cách điện đặt cạnh một dây dẫn': 'an insulator packed beside a conductor'},
 'Biểu thức Boolean A + B + C là:': {'một literal': 'a literal term',
                                     'một số hạng đảo (inverse term)': 'an inverse term',
                                     'một tích (product term)': 'a product term',
                                     'một tổng (sum term)': 'a sum term'},
 'Biểu thức Boolean ABCD là:': {'một literal': 'a literal term',
                                'một số hạng đảo (inverse term)': 'an inverse term',
                                'một tích (product term)': 'a product term',
                                'một tổng (sum term)': 'a sum term'},
 'Bìa Karnaugh 4 biến có:': {'16 ô': 'sixteen cells', '32 ô': 'thirty-two cells', '4 ô': 'four cells', '8 ô': 'eight cells'},
 "Bù hai (2's complement) của 11001100 là:": {'00110011': '00110011',
                                              '00110100': '00110100',
                                              '00110101': '00110101',
                                              '00110110': '00110110'},
 "Bù một (1's complement) của 11110000 là:": {'00001111': '00001111',
                                              '10000001': '10000001',
                                              '11111110': '11111110',
                                              '11111111': '11111111'},
 'Bộ cộng bán phần (half-adder) được đặc trưng bởi:': {'2 đầu vào và 1 đầu ra': 'two inputs and one output',
                                                       '2 đầu vào và 2 đầu ra': 'two inputs and two outputs',
                                                       '2 đầu vào và 3 đầu ra': 'two inputs and three outputs',
                                                       '3 đầu vào và 2 đầu ra': 'three inputs and two outputs'},
 'Bộ cộng toàn phần (full-adder) được đặc trưng bởi:': {'2 đầu vào và 1 đầu ra': 'two inputs and one output',
                                                        '2 đầu vào và 2 đầu ra': 'two inputs and two outputs',
                                                        '2 đầu vào và 3 đầu ra': 'two inputs and three outputs',
                                                        '3 đầu vào và 2 đầu ra': 'three inputs and two outputs'},
 'Bộ giải mã BCD-sang-7-đoạn có đầu vào 0100. Các đầu ra tích cực là:': {'a,c,f,g': 'a, c, f, g',
                                                                         'b,c,e,f': 'b, c, e, f',
                                                                         'b,c,f,g': 'b, c, f, g',
                                                                         'b,d,e,g': 'b, d, e, g'},
 'Bộ phân phối dữ liệu (data distributor) về cơ bản giống với:': {'bộ dồn kênh (multiplexer)': 'multiplexers',
                                                                  'bộ giải dồn kênh (demultiplexer)': 'demultiplexers',
                                                                  'bộ giải mã (decoder)': 'decoders',
                                                                  'bộ mã hoá (encoder)': 'encoders'},
 'Các hàng và cột của ma trận kết nối trong SPLD được nối với nhau bằng:': {'công tắc (switches)': 'switches',
                                                                            'cầu chì (fuses)': 'fuses',
                                                                            'cổng logic (gates)': 'gates',
                                                                            'transistor': 'transistors'},
 'Cổng đảo thực hiện phép toán gọi là:': {'bù (complementation)': 'complementation',
                                          'cả (a) và (c)': 'both answers (a) and (c)',
                                          'khẳng định (assertion)': 'assertion',
                                          'đảo (inversion)': 'inversion'},
 'Dung lượng bit của một bộ nhớ có 512 địa chỉ, mỗi địa chỉ lưu 8 bit là:': {'1024': '1024', '2048': '2048', '4096': '4096', '512': '512'},
 'Dữ liệu lưu tại một địa chỉ trong RAM sẽ bị mất khi:': {'cả (a) và (c)': 'answers (a) and (c)',
                                                          'dữ liệu mới được ghi vào địa chỉ đó': 'new data are written at the address',
                                                          'dữ liệu được đọc ra từ địa chỉ đó': 'the data are read from the address',
                                                          'mất điện': 'power goes off'},
 'Dữ liệu được lưu vào bộ nhớ truy cập ngẫu nhiên (RAM) trong quá trình:': {'thao tác enable': 'enable operation',
                                                                            'thao tác ghi': 'write operation',
                                                                            'thao tác định địa chỉ': 'addressing operation',
                                                                            'thao tác đọc': 'read operation'},
 'EPROM có thể được lập trình bằng:': {'bộ lập trình thiết bị (device programmer)': 'a device programmer',
                                       'bộ lập trình đa năng (multiprogrammer)': 'a multiprogrammer',
                                       'diode': 'diodes',
                                       'transistor': 'transistors'},
 'Giá trị thập phân của số nhị phân 1000 là:': {'2': '2', '4': '4', '6': '6', '8': '8'},
 'Hai cách nhập thiết kế logic bằng phần mềm PLD là:': {'biên dịch và sắp xếp (compile and sort)': 'compile and sort',
                                                        'văn bản và số (text and numeric)': 'text and numeric',
                                                        'văn bản và đồ hoạ (text and graphic)': 'text and graphic',
                                                        'đồ hoạ và mã hoá (graphic and coded)': 'graphic and coded'},
 'Hai xung được đưa vào cổng NAND 2 đầu vào: xung 1 lên HIGH tại t=0, xuống LOW tại t=1ms; xung 2 lên HIGH tại t=0.8ms, xuống LOW tại t=3ms. Đầu ra:': {'xuống LOW tại t=0, lên lại HIGH tại t=3ms': 'It '
                                                                                                                                                                                                     'goes '
                                                                                                                                                                                                     'LOW '
                                                                                                                                                                                                     'at '
                                                                                                                                                                                                     't '
                                                                                                                                                                                                     '= '
                                                                                                                                                                                                     '0 '
                                                                                                                                                                                                     'and '
                                                                                                                                                                                                     'back '
                                                                                                                                                                                                     'HIGH '
                                                                                                                                                                                                     'at '
                                                                                                                                                                                                     't '
                                                                                                                                                                                                     '= '
                                                                                                                                                                                                     '3 '
                                                                                                                                                                                                     'ms.',
                                                                                                                                                        'xuống LOW tại t=0.8ms, lên lại HIGH tại t=1ms': 'It '
                                                                                                                                                                                                         'goes '
                                                                                                                                                                                                         'LOW '
                                                                                                                                                                                                         'at '
                                                                                                                                                                                                         't '
                                                                                                                                                                                                         '= '
                                                                                                                                                                                                         '0.8 '
                                                                                                                                                                                                         'ms '
                                                                                                                                                                                                         'and '
                                                                                                                                                                                                         'back '
                                                                                                                                                                                                         'HIGH '
                                                                                                                                                                                                         'at '
                                                                                                                                                                                                         't '
                                                                                                                                                                                                         '= '
                                                                                                                                                                                                         '1 '
                                                                                                                                                                                                         'ms.',
                                                                                                                                                        'xuống LOW tại t=0.8ms, lên lại HIGH tại t=3ms': 'It '
                                                                                                                                                                                                         'goes '
                                                                                                                                                                                                         'LOW '
                                                                                                                                                                                                         'at '
                                                                                                                                                                                                         't '
                                                                                                                                                                                                         '= '
                                                                                                                                                                                                         '0.8 '
                                                                                                                                                                                                         'ms '
                                                                                                                                                                                                         'and '
                                                                                                                                                                                                         'back '
                                                                                                                                                                                                         'HIGH '
                                                                                                                                                                                                         'at '
                                                                                                                                                                                                         't '
                                                                                                                                                                                                         '= '
                                                                                                                                                                                                         '3 '
                                                                                                                                                                                                         'ms.',
                                                                                                                                                        'xuống LOW tại t=0.8ms, xuống LOW tại t=1ms': 'It '
                                                                                                                                                                                                      'goes '
                                                                                                                                                                                                      'LOW '
                                                                                                                                                                                                      'at '
                                                                                                                                                                                                      't '
                                                                                                                                                                                                      '= '
                                                                                                                                                                                                      '0.8 '
                                                                                                                                                                                                      'ms '
                                                                                                                                                                                                      'and '
                                                                                                                                                                                                      'back '
                                                                                                                                                                                                      'LOW '
                                                                                                                                                                                                      'at '
                                                                                                                                                                                                      't '
                                                                                                                                                                                                      '= '
                                                                                                                                                                                                      '1 '
                                                                                                                                                                                                      'ms.'},
 'Hầu hết PLD sử dụng một mảng (array) các cổng:': {'cổng AND': 'AND gates',
                                                    'cổng NOR': 'NOR gates',
                                                    'cổng NOT': 'NOT gates',
                                                    'cổng OR': 'OR gates'},
 'Khi đầu vào của một cổng đảo ở mức LOW (0), đầu ra là:': {'HIGH hoặc 0': 'HIGH or 0',
                                                            'HIGH hoặc 1': 'HIGH or 1',
                                                            'LOW hoặc 0': 'LOW or 0',
                                                            'LOW hoặc 1': 'LOW or 1'},
 'Miền xác định (domain) của biểu thức ABCD + AB + CD + B là:': {'A và D': 'A and D',
                                                                 'A, B, C, và D': 'A, B, C, and D',
                                                                 'chỉ B': 'B only',
                                                                 'không phải các đáp án trên': 'none of these'},
 'Mã BCD của số thập phân 473 là:': {'010001110011': '010001110011',
                                     '010011110011': '010011110011',
                                     '110001110011': '110001110011',
                                     '111011010': '111011010'},
 'Mã nào sau đây có lỗi chẵn lẻ (even-parity error)?': {'1001000': '1001000',
                                                        '1010011': '1010011',
                                                        '1101000': '1101000',
                                                        '1110111': '1110111'},
 'Một biến trong đại số Boolean là ký hiệu dùng để biểu diễn:': {'cả (a),(b),(c)': 'answers (a), (b), and (c)',
                                                                 'dữ liệu': 'data',
                                                                 'một hành động': 'an action',
                                                                 'một điều kiện': 'a condition'},
 'Một bộ cộng song song 3-bit có thể cộng:': {'ba bit cùng lúc': 'three bits at a time',
                                              'ba bit tuần tự': 'three bits in sequence',
                                              'ba số nhị phân 2-bit': 'three 2-bit binary numbers',
                                              'hai số nhị phân 3-bit': 'two 3-bit binary numbers'},
 'Một bộ nhớ có 512 địa chỉ có:': {'1 đường địa chỉ': '1 address line',
                                   '12 đường địa chỉ': '12 address lines',
                                   '512 đường địa chỉ': '512 address lines',
                                   '9 đường địa chỉ': '9 address lines'},
 'Một bộ nhớ tổ chức theo byte (byte-organized) có:': {'1 đường dữ liệu ra': '1 data output line',
                                                       '16 đường dữ liệu ra': '16 data output lines',
                                                       '4 đường dữ liệu ra': '4 data output lines',
                                                       '8 đường dữ liệu ra': '8 data output lines'},
 'Một cơ sở chứa hệ thống lưu trữ đám mây được gọi là:': {'nhà mây (cloud house)': 'cloud house',
                                                          'server': 'server',
                                                          'trung tâm dữ liệu (data center)': 'data center',
                                                          'trung tâm máy tính': 'computer center'},
 'Một số nhị phân dấu phẩy động độ chính xác đơn (single-precision) có tổng cộng:': {'16 bit': '16 bits',
                                                                                     '24 bit': '24 bits',
                                                                                     '32 bit': '32 bits',
                                                                                     '8 bit': '8 bits'},
 'Một từ (word) 16-bit gồm:': {'3 byte': '3 bytes',
                               '3 byte và 1 nibble': '3 bytes and 1 nibble',
                               '4 byte': '4 bytes',
                               '4 nibble': '4 nibbles'},
 'Một xung dương được đưa vào cổng đảo. Khoảng thời gian từ cạnh lên đầu vào tới cạnh lên đầu ra là 7ns. Đây là tham số:': {'trễ lan truyền tPHL': 'propagation '
                                                                                                                                                   'delay, '
                                                                                                                                                   'tPHL',
                                                                                                                            'trễ lan truyền tPLH': 'propagation '
                                                                                                                                                   'delay, '
                                                                                                                                                   'tPLH',
                                                                                                                            'tích công suất-tốc độ (speed-power product)': 'speed-power '
                                                                                                                                                                           'product',
                                                                                                                            'độ rộng xung': 'pulse '
                                                                                                                                            'width'},
 'Nói chung, một bộ dồn kênh (multiplexer) có:': {'1 đầu vào dữ liệu, 1 đầu ra dữ liệu, 1 đầu vào chọn': 'one data input, one data output, '
                                                                                                         'and one selection input',
                                                  '1 đầu vào dữ liệu, nhiều đầu ra dữ liệu, và các đầu vào chọn': 'one data input, several '
                                                                                                                  'data outputs, and '
                                                                                                                  'selection inputs',
                                                  'nhiều đầu vào dữ liệu, 1 đầu ra dữ liệu, và các đầu vào chọn': 'several data inputs, '
                                                                                                                  'one data output, and '
                                                                                                                  'selection inputs',
                                                  'nhiều đầu vào dữ liệu, nhiều đầu ra dữ liệu, và các đầu vào chọn': 'several data '
                                                                                                                      'inputs, several '
                                                                                                                      'data outputs, and '
                                                                                                                      'selection inputs'},
 'Nếu bộ giải mã 1-trong-16 với đầu ra tích cực mức thấp có đầu ra decimal 12 ở mức LOW, đầu vào là:': {'A3A2A1A0=0100': 'A3A2A1A0 = 0100',
                                                                                                        'A3A2A1A0=1010': 'A3A2A1A0 = 1010',
                                                                                                        'A3A2A1A0=1100': 'A3A2A1A0 = 1100',
                                                                                                        'A3A2A1A0=1110': 'A3A2A1A0 = 1110'},
 'Nếu bộ mã hoá ưu tiên bát phân-sang-nhị phân có các đầu vào 0,2,5,6 ở mức tích cực, đầu ra nhị phân tích cực mức cao là:': {'000': '000',
                                                                                                                              '010': '010',
                                                                                                                              '101': '101',
                                                                                                                              '110': '110'},
 'Phương pháp Quine-McCluskey có thể dùng để:': {'cả (a) và (b)': 'both (a) and (b)',
                                                 'không đáp án nào': 'none of the above',
                                                 'rút gọn biểu thức từ 5 biến trở lên': 'simplify expressions with 5 or more variables',
                                                 'thay thế phương pháp bìa Karnaugh': 'replace the Karnaugh map method'},
 'Phần tử lưu trữ của DRAM là:': {'diode': 'diode', 'transistor': 'transistor', 'tụ điện': 'capacitor', 'điện trở': 'resistor'},
 'ROM là một loại bộ nhớ:': {'không mất dữ liệu khi mất điện (nonvolatile)': 'nonvolatile memory',
                             'mất dữ liệu khi mất điện (volatile)': 'volatile memory',
                             'tổ chức theo byte': 'byte-organized memory',
                             'đọc/ghi được': 'read/write memory'},
 'SRAM, DRAM, flash, và EEPROM đều là:': {'thiết bị lưu trữ bán dẫn': 'semiconductor storage devices',
                                          'thiết bị lưu trữ quang học': 'optical storage devices',
                                          'thiết bị lưu trữ từ tính': 'magnetic storage devices',
                                          'thiết bị lưu trữ từ-quang': 'magneto-optical storage devices'},
 'Sau khi đo được chu kỳ của dạng sóng xung, tần số được tính bằng cách:': {'dùng loại thiết bị đo khác': 'using another type of '
                                                                                                          'instrument',
                                                                            'dùng thang đo khác': 'using another setting',
                                                                            'lấy nghịch đảo của chu kỳ': 'finding the reciprocal of the '
                                                                                                         'period',
                                                                            'đo duty cycle': 'measuring the duty cycle'},
 'Số nhị phân 10001101010001101111 viết dưới dạng thập lục phân là:': {'8C46F₁₆': '8C46F16',
                                                                       '8D46F₁₆': '8D46F16',
                                                                       'AD467₁₆': 'AD46716',
                                                                       'AE46F₁₆': 'AE46F16'},
 'Số nhị phân 101100111001010100001 viết dưới dạng bát phân là:': {'2316250₈': '231625018',
                                                                   '2634521₈': '26345218',
                                                                   '5471230₈': '54712308',
                                                                   '5471241₈': '54712418'},
 'Số nhị phân 11011101 tương ứng với số thập phân:': {'121': '121', '221': '221', '256': '256', '441': '441'},
 'Số thập phân 21 tương ứng với số nhị phân:': {'10000': '10000', '10001': '10001', '10101': '10101', '11111': '11111'},
 'Số thập phân 250 tương ứng với số nhị phân:': {'11110110': '11110110',
                                                 '11111000': '11111000',
                                                 '11111010': '11111010',
                                                 '11111011': '11111011'},
 'Theo luật kết hợp của phép cộng:': {'(A+B)+C=A+(B+C)': '(A + B) + C = A + (B + C )',
                                      'A+0=A': 'A + 0 = A',
                                      'A+B=B+A': 'A + B = B + A',
                                      'A=A+A': 'A = A + A'},
 'Theo luật phân phối:': {'A(A+1)=A': 'A(A + 1) = A',
                          'A(B+C)=AB+AC': 'A(B + C) = AB + AC',
                          'A(BC)=ABC': 'A(BC) = ABC',
                          'A+AB=A': 'A + AB = A'},
 'Thiết bị lưu trữ quang học sử dụng:': {'bộ ghép quang': 'optical couplers',
                                         'tia laser': 'lasers',
                                         'trường điện từ': 'electromagnetic fields',
                                         'ánh sáng cực tím': 'ultraviolet light'},
 "Trong VHDL, một 'port' là:": {'một loại architecture': 'a type of architecture',
                                'một loại biến': 'a type of variable',
                                'một loại entity': 'a type of entity',
                                'một đầu vào hoặc đầu ra': 'an input or output'},
 'Trong bìa Karnaugh 4 biến, một tích 2 biến được tạo bởi:': {'nhóm 2 ô': 'a 2-cell group of 1s',
                                                              'nhóm 4 ô': 'a 4-cell group of 1s',
                                                              'nhóm 4 ô số 0': 'a 4-cell group of 0s',
                                                              'nhóm 8 ô': 'an 8-cell group of 1s'},
 'Trong kiểm tra dư thừa vòng (CRC), việc không có lỗi được thể hiện bằng:': {'Số dư = 0': 'Remainder = 0',
                                                                              'Số dư = 1': 'Remainder = 1',
                                                                              'Số dư = mã sinh (generator code)': 'Remainder = generator '
                                                                                                                  'code',
                                                                              'Thương số = 0': 'Quotient = 0'},
 'Trong máy tính, chương trình BIOS được lưu trong:': {'DRAM': 'DRAM', 'RAM': 'RAM', 'ROM': 'ROM', 'SRAM': 'SRAM'},
 'VHDL là một loại:': {'logic khả trình': 'data',
                       'mảng khả trình': 'an action',
                       'ngôn ngữ mô tả phần cứng': 'a condition',
                       'toán logic': 'answers (a), (b), and (c)'},
 'Ví dụ của biểu thức SOP chuẩn (standard SOP) là:': {'AB+AB+AB': 'AB + AB + AB',
                                                      'AB+ABC+ABD': 'AB + ABC + ABD',
                                                      'ABC+ACD': 'ABC + ACD',
                                                      'ABCD+AB+A': 'ABCD + AB + A'},
 'Ví dụ của biểu thức tích-các-tổng (POS) là:': {'(A+B)(A+B+C)': '(A + B)(A + B + C)',
                                                 'A(B+C)+AC': 'A(B + C) + AC',
                                                 'A+B+BC': 'A + B + BC',
                                                 'cả (a) và (b)': 'both answers (a) and (b)'},
 'Ví dụ của biểu thức tổng-các-tích (SOP) là:': {'(A+B+C)(A+B+C)': '(A + B + C)(A + B + C)',
                                                 'A+B(C+D)': 'A + B(C + D)',
                                                 'AB+AC+ABC': 'AB + AC + ABC',
                                                 'cả (a) và (b)': 'both answers (a) and (b)'},
 'Đâu KHÔNG phải là một luật hợp lệ của đại số Boolean?': {'A+0=A': 'A + 0 = A', 'A+1=1': 'A + 1 = 1', 'A=A': 'A = A', 'AA=A': 'AA = A'},
 'Để mở rộng bộ cộng song song 2-bit thành 4-bit, bạn phải:': {'dùng 2 bộ cộng 2-bit không kết nối': 'use two 2-bit adders with no '
                                                                                                     'interconnections',
                                                               'dùng 2 bộ cộng 2-bit, nối đầu ra nhớ (carry) của bộ này vào đầu vào nhớ của bộ kia': 'use '
                                                                                                                                                     'two '
                                                                                                                                                     '2-bit '
                                                                                                                                                     'adders '
                                                                                                                                                     'with '
                                                                                                                                                     'the '
                                                                                                                                                     'carry '
                                                                                                                                                     'output '
                                                                                                                                                     'of '
                                                                                                                                                     'one '
                                                                                                                                                     'connected '
                                                                                                                                                     'to '
                                                                                                                                                     'the '
                                                                                                                                                     'carry '
                                                                                                                                                     'input '
                                                                                                                                                     'of '
                                                                                                                                                     'the '
                                                                                                                                                     'other',
                                                               'dùng 2 bộ cộng 2-bit, nối đầu ra tổng của bộ này vào đầu vào bit của bộ kia': 'use '
                                                                                                                                              'two '
                                                                                                                                              '2-bit '
                                                                                                                                              'adders '
                                                                                                                                              'and '
                                                                                                                                              'connect '
                                                                                                                                              'the '
                                                                                                                                              'sum '
                                                                                                                                              'outputs '
                                                                                                                                              'of '
                                                                                                                                              'one '
                                                                                                                                              'to '
                                                                                                                                              'the '
                                                                                                                                              'bit '
                                                                                                                                              'inputs '
                                                                                                                                              'of '
                                                                                                                                              'the '
                                                                                                                                              'other',
                                                               'dùng 4 bộ cộng 2-bit không kết nối': 'use four 2-bit adders with no '
                                                                                                     'interconnections'},
 'Để đo chu kỳ của dạng sóng xung, bạn phải dùng:': {'bút thử logic (logic probe)': 'a logic probe',
                                                     'bút xung logic (logic pulser)': 'a logic pulser',
                                                     'dao động ký (oscilloscope)': 'an oscilloscope',
                                                     'đồng hồ vạn năng số (DMM)': 'a DMM'},
 'Độ trễ bộ nhớ (memory latency) là:': {'thời gian ngừng hoạt động trung bình': 'average down time',
                                        'thời gian truy cập của bộ xử lý': 'processor access time',
                                        'thời gian để tham chiếu một khối dữ liệu': 'time to reference a block of data',
                                        'tỉ lệ hit (hit rate)': 'the hit rate'},
 'Ở dạng bù hai, số nhị phân 10010011 tương ứng với số thập phân:': {'+109': '+ 109', '+91': '+ 91', '−109': '2109', '−19': '219'}}
