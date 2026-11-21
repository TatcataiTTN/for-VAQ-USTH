# -*- coding: utf-8 -*-
"""Anh xa MODULE <-> chuong sach o cap chuong (ban nhap tu phien truoc, da sua cac cau cu/sai: m05 Floyd Ch.13 muc 13-6..13-10; m08 Tooley Ch.10 bat dau tr.165).
SO TRANG IN: Tooley in = PDF - 14, Floyd in = PDF - 1 (do 21/11/2026 tren trang dau chuong). Kiem tra cap muc o P2."""
MAPPING_ROWS = [{'floyd': 'Ch.2 Number Systems, Operations, and Codes (p.65-124)',
  'module': '01: Number Systems',
  'note_en': 'Near 1-to-1 match: both books devote exactly one chapter to these same four number systems.',
  'note_vi': 'Khớp trực tiếp gần như 1-1: cả 2 sách đều dành nguyên 1 chương cho đúng 4 hệ đếm này.',
  'tooley': 'Ch.2 Number systems (p.25-38): decimal, binary, octal, hex, ASCII'},
 {'floyd': 'Ch.3 Logic Gates (p.125-190) + Ch.4 Boolean Algebra and Logic Simplification (p.191-260); phần bistable đối chiếu thêm Ch.7 Latches, Flip-Flops, and Timers (p.387-448)',
  'floyd_en': 'Ch.3 Logic Gates (p.125-190) + Ch.4 Boolean Algebra and Logic Simplification (p.191-260); the bistable part is cross-referenced with Ch.7 Latches, Flip-Flops, and Timers (p.387-448)',
  'module': '02: Logic Circuits & Boolean Algebra',
  'note_en': 'Tooley bundles gates + Boolean algebra + bistables into one chapter; Floyd splits this into three more detailed chapters.',
  'note_vi': 'Tooley gộp cả gate + Boolean + bistable vào 1 chương; Floyd tách thành 3 chương riêng chi tiết hơn.',
  'tooley': 'Ch.5 Logic circuits (p.70-94): gates, Boolean algebra, combinational logic, tri-state, monostable/bistable, logic families'},
 {'floyd': 'Ch.6 Functions of Combinational Logic (p.313-386): decoders, encoders, multiplexers, demultiplexers, comparators; công nghệ chế tạo IC đối chiếu thêm Ch.15 Integrated Circuit '
           'Technologies (p.855+)',
  'floyd_en': 'Ch.6 Functions of Combinational Logic (p.313-386): decoders, encoders, multiplexers, demultiplexers, comparators; IC fabrication technology is cross-referenced with Ch.15 Integrated '
              'Circuit Technologies (p.855+)',
  'module': '03: Integrated Circuits & Multiplexing',
  'note_en': "Tooley splits 'IC technology' (ch.8) and 'MSI applications' (ch.9) into two chapters; Floyd bundles all MSI applications into Ch.6 and keeps fabrication technology separate at the end "
             'of the book (Ch.15).',
  'note_vi': "Tooley tách 'công nghệ IC' (ch.8) và 'ứng dụng MSI' (ch.9) thành 2 chương; Floyd gộp toàn bộ ứng dụng MSI vào Ch.6 và để công nghệ chế tạo riêng ở cuối sách (Ch.15).",
  'tooley': 'Ch.8 Integrated circuits (p.139-148) + Ch.9 MSI logic (p.149-164): fan-in/out, decoders, encoders, multiplexers'},
 {'floyd': 'Ch.11 Data Storage (p.627-696): RAM/ROM/Flash memory. Floyd KHÔNG có chương riêng về kiến trúc CPU/vi xử lý: đây là điểm khác biệt lớn nhất giữa 2 sách cho module này.',
  'floyd_en': 'Ch.11 Data Storage (p.627-696): RAM/ROM/Flash memory. Floyd has NO dedicated chapter on CPU/microprocessor architecture: this is the biggest difference between the two books for this '
              'module.',
  'module': '04: Computers & Microprocessors',
  'note_en': 'This module has the WEAKEST match between the two books: Floyd is a pure digital-logic fundamentals text and does not cover computer/CPU architecture in depth like Tooley: the CPU '
             'content in this module relies mainly on Tooley.',
  'note_vi': 'Đây là module có độ khớp THẤP NHẤT giữa 2 sách: Floyd là sách nền tảng logic số thuần tuý, không đi sâu kiến trúc máy tính/CPU như Tooley: phần CPU trong module này chủ yếu dựa vào '
             'Tooley.',
  'tooley': 'Ch.6 Computers (p.95-115): computer systems, data storage, backplane bus + Ch.7 The CPU (p.116-138): internal architecture, x86/Pentium/AMD 29050'},
 {'floyd': 'Ch.13 Data Transmission, §13-6 Bus Basics (PDF tr.765), §13-7 Parallel Buses, §13-8 USB, §13-9 Other Serial Buses, §13-10 Bus Interfacing (PDF tr.785): bus CHUNG của máy tính, KHÔNG phải '
           'bus hàng không (ARINC 429/629, MIL-STD-1553, AFDX không có trong Floyd).',
  'floyd_en': 'Ch.13 Data Transmission, §13-6 Bus Basics (PDF p.765), §13-7 Parallel Buses, §13-8 USB, §13-9 Other Serial Buses, §13-10 Bus Interfacing (PDF p.785): GENERAL computer buses, NOT '
              'aircraft buses (ARINC 429/629, MIL-STD-1553 and AFDX are not in Floyd).',
  'module': '05: Data Buses',
  'note_en': 'Floyd matches only at the level of general buses (USB, serial, parallel, bus interfacing: Ch.13 §13-6 to 13-10; 19 Floyd questions in the bank, true/false and Self-Test); it has no '
             'aircraft buses. ARINC 429/629/AFDX rely on Tooley Ch.4 and the 18-page lecture deck.',
  'note_vi': 'Floyd khớp ở mức bus chung (USB, nối tiếp, song song, giao tiếp bus: Ch.13 §13-6 đến 13-10; 19 câu Floyd trong ngân hàng gồm đúng/sai và Self-Test), không có bus hàng không. Phần ARINC '
             '429/629/AFDX dựa vào Tooley Ch.4 và bộ slide 18 trang.',
  'tooley': 'Ch.4 Data buses (p.53-69): bus rationale, ARINC 429 (electrical/word format/BCD-BNR), other standards (ARINC 629/AFDX/MIL-STD-1553/legacy buses)'},
 {'floyd': 'Ch.4 Applied Logic: Seven-Segment Display (p.244-249; problems 62-71, p.256) + Ch.6 section 6-5 decoder/driver 74HC47 and zero suppression (p.338-340) + section 6-8 7-segment '
           'multiplexing (p.353). Floyd KHÔNG có nội dung về EFIS/ECAM/ACARS hay CRT/LCD ngoài mức 7 đoạn: phần lớn module này dựa vào Tooley và bộ slide bài giảng.',
  'floyd_en': 'Ch.4 Applied Logic: Seven-Segment Display (p.244-249; problems 62-71, p.256) + Ch.6 section 6-5 decoder/driver 74HC47 and zero suppression (p.338-340) + section 6-8 7-segment '
              'multiplexing (p.353). Floyd has NO content on EFIS/ECAM/ACARS or CRT/LCD technology beyond the 7-segment level: most of this module relies on Tooley and the lecture slides.',
  'module': '06: Electronic Displays',
  'note_en': 'This module has its own lecture deck (36 infographic slides, each read directly). Tooley matches well (three scattered chapters: Ch.1, Ch.11, Ch.15). Floyd matches only at the '
             "7-segment level (Ch.4, Ch.6), so this module's Floyd quiz is small and the essay section has only the 4 odd Applied Logic problems.",
  'note_vi': 'Đây là module có bộ slide bài giảng riêng (36 slide infographic, đọc trực tiếp từng slide). Tooley khớp tốt (3 chương rải rác: Ch.1, Ch.11, Ch.15). Floyd chỉ khớp ở phần 7 đoạn (Ch.4, '
             'Ch.6), nên quiz Floyd của module này ít và bài tự luận chỉ có 4 bài lẻ của Applied Logic.',
  'tooley': 'Ch.1 Introduction (p.1-24): flight instruments, EFIS, ECAM/EICAS, cockpit layouts + Ch.11 Displays (p.178-196): CRT, LED/7-segment, LCD + Ch.15 Avionic systems, sections 15.1 ACARS, '
            '15.2 EFIS, 15.3 EICAS/ECAM (p.238-250); 53 MCQs from Ch.1, 11, 15'},
 {'floyd': 'Ch.2 section 2-12 Error Codes (parity, CRC, Example 2-41; p.109-114) và Ch.11 section 11-11 (kiểm tra ROM bằng checksum, Hình 11-74 và 11-75). Floyd KHÔNG có nội dung về DO-178, phân '
           'loại mức phần mềm hay nạp phần mềm máy bay: chỉ khớp ở khía cạnh kiểm tra lỗi dữ liệu.',
  'floyd_en': 'Ch.2 section 2-12 Error Codes (parity, CRC, Example 2-41; p.109-114) and Ch.11 section 11-11 (ROM checksum test, Figures 11-74 and 11-75). Floyd has NO content on DO-178, software '
              'levels or loading aircraft software: it matches only on the data error checking aspect.',
  'module': '07: Software Management Control',
  'note_en': 'The main source is the 6-page EASA Part-66 Module 5.13 document (13.1 to 13.6, with Figure 13-1 and 6 questions with answers) plus Tooley ch.13. The module has 2 interactive demos '
             '(checksum versus CRC, a DAL level explorer).',
  'note_vi': 'Nguồn chính là tài liệu 6 trang EASA Part-66 Module 5.13 (13.1 đến 13.6, gồm Hình 13-1 và 6 câu hỏi có đáp án) cùng Tooley ch.13. Module có 2 demo tương tác (checksum và CRC, bộ chọn '
             'mức DAL).',
  'tooley': 'Ch.13 Software (p.207-217): 13.1 classification, 13.2 certification, 13.3 upgrading (FLS, LSAP, UMS, OSS, DFLD, EEC loading with PDL), 13.4 data verification; 7 MCQs; plus Ch.15 MCQ on '
            'navigation database update'},
 {'floyd': 'Ch.13 Data Transmission, section 13-1 Data Transmission Media (p.740-745): optical fiber cable, modes (multimode, single-mode, 50/125, 62.5/125, 8.3/125), link block diagram, connectors; '
           'Section Checkup; Problems 5 and 7 (p.793; answers A-27). Floyd KHÔNG có góc tới hạn, khẩu độ số, suy hao hay tán sắc: phần lý thuyết sâu dựa vào bài giảng và Tooley.',
  'floyd_en': 'Ch.13 Data Transmission, section 13-1 Data Transmission Media (p.740-745): optical fiber cable, modes (multimode, single-mode, 50/125, 62.5/125, 8.3/125), link block diagram, '
              'connectors; Section Checkup; Problems 5 and 7 (p.793; answers A-27). Floyd has NO critical angle, numerical aperture, attenuation or dispersion: the deeper theory relies on the '
              'lecture and Tooley.',
  'module': '08: Fibre Optics',
  'note_en': 'The 37-slide lecture has four calculation exercises (slides 20, 22, 27, 36); the module solves and verifies them, and only slide 36 has a printed answer. The module has 2 interactive '
             'demos (fibre calculator, Snell/TIR ray) and records the 7 mismatches found in the material.',
  'note_vi': 'Bộ bài giảng 37 slide có bốn bài tập tính toán (slide 20, 22, 27, 36); module giải lại và kiểm chứng, và chỉ slide 36 có đáp án in. Module có 2 demo tương tác (máy tính sợi quang, tia '
             'sáng Snell/TIR) và ghi lại 7 điểm không khớp tìm thấy trong tài liệu.',
  'tooley': 'Ch.10 Fibre optics (p.165-177): 10.1 advantages, 10.2 propagation (critical angle, numerical aperture, attenuation), 10.3 dispersion and bandwidth, 10.4 practical networks (ARINC 636, '
            'cable, connectors), 10.5 components; 20 MCQs (A.10, p.379-380)'},
 {'floyd': 'Floyd KHÔNG có chương EMC. Chỉ khớp một phần: Ch.13 mục 13-1 (cross talk, cáp xoắn đôi UTP/STP chống EMI, tr.741), Ch.6 mục 6-11 (tụ tách VCC-đất, tr.364), Ch.15 mục 15-3 (noise margin, '
           'tr.859; Bài 3 tr.887). Phần lớn module dựa vào Tooley và bài giảng.',
  'floyd_en': 'Floyd has NO EMC chapter. Only partial matches: Ch.13 section 13-1 (cross talk, UTP/STP twisted pairs against EMI, p.741), Ch.6 section 6-11 (VCC-to-ground decoupling, p.364), Ch.15 '
              'section 15-3 (noise margin, p.859; Problem 3 p.887). Most of the module relies on Tooley and the lecture.',
  'module': '09: EMC',
  'note_en': 'The 46-slide lecture (each slide read) has 3 dB exercise sets (slides 17, 19, 21); all were re-solved and the 10 kW versus 100 kW error on slide 21 was caught. The module has 3 '
             'interactive demos (dB and dBm, square-wave Fourier, a real capacitor) and records the mismatches found in the material.',
  'note_vi': 'Bài giảng 46 slide (đọc từng slide) có 3 nhóm bài tập dB (slide 17, 19, 21), đã giải lại và phát hiện lỗi 10 kW so với 100 kW ở slide 21. Module có 3 demo tương tác (dB và dBm, Fourier '
             'sóng vuông, tụ thực) và ghi lại các điểm không khớp trong tài liệu.',
  'tooley': 'Ch.14 EMC (p.218-237): 14.1 harmonics and pulse spectrum, 14.2 EMC and avionic equipment, 14.3 spectrum analysis (noise floor, Table 14.1 bands), 14.4 effects, sources and reduction of '
            'EMI, 14.5 wiring, 14.6 grounding and bonding; 9 MCQs (A.14, p.381)'}]
