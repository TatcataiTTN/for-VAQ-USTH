# -*- coding: utf-8 -*-
"""
Cau hoi tu luan (free-response) trich tu phan "Problems" cuoi chuong sach Floyd,
Digital Fundamentals 11th ed. Sach Tooley (Aircraft Digital Electronic and Computer
Systems) CHI co muc luc "Multiple-choice questions" cuoi moi chuong, khong co phan
tu luan rieng, nen toan bo cau hoi trong file nay lay tu Floyd.

Quy tac bat buoc: chi chon cau hoi so LE (odd-numbered), vi sach chi in dap an cho
cau so le o phu luc "Answers to Odd-Numbered Problems" cuoi sach. Moi dap an la
ANH CHUP THAT tu chinh trang phu luc do (khong go lai bang tay), luu tai
OCR_output/exercise_pages/Floyd/... va copy vao assets/figures/essay_floyd_*.png
de web phuc vu duoc.

Da doi chieu tung cau: tinh lai doc lap bang tay, so voi anh dap an that. Rieng
Ch.2 Problem 5 KHONG duoc dua vao day vi da phat hien loi in an that trong sach
(101(2)=5 nhung dap an in la "3"): xem ghi chu trong lich su phien lam viec.
"""

ESSAY = {
  "01-number-systems": {
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 2 – Number Systems, Operations, and Codes, Problems (p.118-122); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-1, A-2).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 2 – Number Systems, Operations, and Codes, Problems (p.118-122); answers in the Answers to Odd-Numbered Problems appendix (p.A-1, A-2).",
    "items": [
      {
        "num": 7,
        "q_vi": "Đổi mỗi số nhị phân sau sang thập phân:<br>(a) 110011.11 &nbsp; (b) 101010.01 &nbsp; (c) 1000001.111<br>(d) 1111000.101 &nbsp; (e) 1011100.10101 &nbsp; (f) 1110001.0001<br>(g) 1011010.1010 &nbsp; (h) 1111111.11111",
        "q_en": "Convert each binary number to decimal:<br>(a) 110011.11 &nbsp; (b) 101010.01 &nbsp; (c) 1000001.111<br>(d) 1111000.101 &nbsp; (e) 1011100.10101 &nbsp; (f) 1110001.0001<br>(g) 1011010.1010 &nbsp; (h) 1111111.11111",
        "src": "Floyd Ch.2 · Problem 7",
        "img": "essay_floyd_ch02_q07.png",
      },
      {
        "num": 13,
        "q_vi": "Đổi mỗi số thập phân sau sang nhị phân bằng phương pháp chia liên tiếp cho 2:<br>(a) 13 &nbsp; (b) 17 &nbsp; (c) 23 &nbsp; (d) 30<br>(e) 35 &nbsp; (f) 40 &nbsp; (g) 49 &nbsp; (h) 60",
        "q_en": "Convert each decimal number to binary using repeated division by 2:<br>(a) 13 &nbsp; (b) 17 &nbsp; (c) 23 &nbsp; (d) 30<br>(e) 35 &nbsp; (f) 40 &nbsp; (g) 49 &nbsp; (h) 60",
        "src": "Floyd Ch.2 · Problem 13",
        "img": "essay_floyd_ch02_q13.png",
      },
      {
        "num": 21,
        "q_vi": "Xác định bù một (1's complement) của mỗi số nhị phân sau:<br>(a) 100 &nbsp; (b) 111 &nbsp; (c) 1100<br>(d) 10111011 &nbsp; (e) 1001010 &nbsp; (f) 10101010",
        "q_en": "Determine the 1's complement of each binary number:<br>(a) 100 &nbsp; (b) 111 &nbsp; (c) 1100<br>(d) 10111011 &nbsp; (e) 1001010 &nbsp; (f) 10101010",
        "src": "Floyd Ch.2 · Problem 21",
        "img": "essay_floyd_ch02_q21.png",
      },
      {
        "num": 25,
        "q_vi": "Viết mỗi số thập phân sau dưới dạng số 8-bit ở dạng bù hai (2's complement):<br>(a) +12 &nbsp; (b) -68 &nbsp; (c) +101 &nbsp; (d) -125",
        "q_en": "Express each decimal number as an 8-bit number in the 2’s complement form:<br>(a) +12 &nbsp; (b) −68 &nbsp; (c) +101 &nbsp; (d) −125",
        "src": "Floyd Ch.2 · Problem 25",
        "img": "essay_floyd_ch02_q25.png",
      },
      {
        "num": 49,
        "q_vi": "Đổi các số thập phân sau sang BCD:<br>(a) 104 &nbsp; (b) 128 &nbsp; (c) 132 &nbsp; (d) 150 &nbsp; (e) 186<br>(f) 210 &nbsp; (g) 359 &nbsp; (h) 547 &nbsp; (i) 1051",
        "q_en": "Convert the following decimal numbers to BCD:<br>(a) 104 &nbsp; (b) 128 &nbsp; (c) 132 &nbsp; (d) 150 &nbsp; (e) 186<br>(f) 210 &nbsp; (g) 359 &nbsp; (h) 547 &nbsp; (i) 1051",
        "src": "Floyd Ch.2 · Problem 49",
        "img": "essay_floyd_ch02_q49.png",
      },
      {
        "num": 63,
        "q_vi": "Xác định mã nào trong các mã kiểm tra chẵn lẻ (even parity) sau bị lỗi:<br>(a) 100110010 &nbsp; (b) 011101010 &nbsp; (c) 10111111010001010",
        "q_en": "Determine which of the following even parity codes are in error:<br>(a) 100110010 &nbsp; (b) 011101010 &nbsp; (c) 10111111010001010",
        "src": "Floyd Ch.2 · Problem 63",
        "img": "essay_floyd_ch02_q63.png",
      },
    ],
  },
  "02-logic-boolean": {
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 3 – Logic Gates và Chapter 4 – Boolean Algebra and Logic Simplification, Problems (p.180-182, p.252-253); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-3, A-4).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 3 – Logic Gates and Chapter 4 – Boolean Algebra and Logic Simplification, Problems (p.180-182, p.252-253); answers in the Answers to Odd-Numbered Problems appendix (p.A-3, A-4).",
    "items": [
      {
        "num": 25,
        "q_vi": "Cổng exclusive-OR (XOR) khác cổng OR như thế nào về mặt hoạt động logic?",
        "q_en": "How does an exclusive-OR gate differ from an OR gate in its logical operation?",
        "src": "Floyd Ch.3 · Problem 25",
        "img": "essay_floyd_ch03_q25.png",
      },
      {
        "num": 1,
        "q_vi": "Dùng ký hiệu Boolean, viết một biểu thức có giá trị 0 CHỈ KHI tất cả các biến (A, B, C, D) đều bằng 0.",
        "q_en": "Using Boolean notation, write an expression that is a 0 only when all of its variables (A, B, C, and D) are 0s.",
        "src": "Floyd Ch.4 · Problem 1",
        "img": "essay_floyd_ch04_q01.png",
      },
      {
        "num": 5,
        "q_vi": "Tìm giá trị của các biến sao cho mỗi số hạng TÍCH bằng 1 và mỗi số hạng TỔNG bằng 0:<br>(a) ABC &nbsp; (b) A + B + C &nbsp; (c) ~{A}~{B}C &nbsp; (d) ~{A} + ~{B} + C<br>(e) A + ~{B} + ~{C} &nbsp; (f) ~{A} + ~{B} + ~{C}",
        "q_en": "Find the values of the variables that make each product term 1 and each sum term 0.<br>(a) ABC &nbsp; (b) A + B + C &nbsp; (c) ~{A}~{B}C &nbsp; (d) ~{A} + ~{B} + C<br>(e) A + ~{B} + ~{C} &nbsp; (f) ~{A} + ~{B} + ~{C}",
        "src": "Floyd Ch.4 · Problem 5",
        "img": "essay_floyd_ch04_q05.png",
      },
      {
        "num": 7,
        "q_vi": "Xác định luật đại số Boole làm cơ sở cho mỗi đẳng thức sau:<br>(a) A + AB + ABC + ~{ABCD} = ~{ABCD} + ABC + AB + A<br>(b) A + ~{AB} + ABC + ~{ABCD} = ~{DCBA} + CBA + ~{BA} + A<br>(c) AB(CD + ~{CD} + EF + ~{EF}) = ABCD + AB~{CD} + ABEF + AB~{EF}",
        "q_en": "Identify the law of Boolean algebra upon which each of the following equalities is based:<br>(a) A + AB + ABC + ~{ABCD} = ~{ABCD} + ABC + AB + A<br>(b) A + ~{AB} + ABC + ~{ABCD} = ~{DCBA} + CBA + ~{BA} + A<br>(c) AB(CD + ~{CD} + EF + ~{EF}) = ABCD + AB~{CD} + ABEF + AB~{EF}",
        "src": "Floyd Ch.4 · Problem 7",
        "img": "essay_floyd_ch04_q07.png",
      },
      {
        "num": 9,
        "q_vi": "Áp dụng các định lý De Morgan cho mỗi biểu thức sau:<br>(a) ~{A + ~{B}} &nbsp; (b) ~{~{A}B} &nbsp; (c) ~{A + B + C} &nbsp; (d) ~{ABC}<br>(e) ~{A(B + C)} &nbsp; (f) ~{AB} + ~{CD} &nbsp; (g) ~{AB + CD} &nbsp; (h) ~{(A + ~{B})(~{C} + D)}",
        "q_en": "Apply DeMorgan's theorems to each expression:<br>(a) ~{A + ~{B}} &nbsp; (b) ~{~{A}B} &nbsp; (c) ~{A + B + C} &nbsp; (d) ~{ABC}<br>(e) ~{A(B + C)} &nbsp; (f) ~{AB} + ~{CD} &nbsp; (g) ~{AB + CD} &nbsp; (h) ~{(A + ~{B})(~{C} + D)}",
        "src": "Floyd Ch.4 · Problem 9",
        "img": "essay_floyd_ch04_q09.png",
      },
      {
        "num": 19,
        "q_vi": "Dùng các kỹ thuật đại số Boole, rút gọn các biểu thức sau đến mức tối đa có thể:<br>(a) A(A + B) &nbsp; (b) A(~{A} + AB) &nbsp; (c) BC + ~{B}C<br>(d) A(A + ~{A}B) &nbsp; (e) A~{B}C + ~{A}BC + ~{A}~{B}C",
        "q_en": "Using Boolean algebra techniques, simplify the following expressions as much as possible:<br>(a) A(A + B) &nbsp; (b) A(~{A} + AB) &nbsp; (c) BC + ~{B}C<br>(d) A(A + ~{A}B) &nbsp; (e) A~{B}C + ~{A}BC + ~{A}~{B}C",
        "src": "Floyd Ch.4 · Problem 19",
        "img": "essay_floyd_ch04_q19.png",
      },
    ],
  },
  "03-ic-multiplexing": {
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 6 – Functions of Combinational Logic, Problems (p.374-376); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-10, A-11).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 6 – Functions of Combinational Logic, Problems (p.374-376); answers in the Answers to Odd-Numbered Problems appendix (p.A-10, A-11).",
    "note_vi": "Chương này của Floyd còn có nhiều câu về decoder/encoder/mux nhưng hầu hết yêu cầu đọc một sơ đồ cụ thể trong sách (không thể tái hiện chính xác bằng chữ mà không có hình). Một số câu khác (Problem 25) có sự không khớp giữa đề bài in trong sách và đáp án in ở phụ lục (nghi lỗi bản in Global Edition), và Problem 9 (chuỗi bit vào bộ cộng 4-bit) vì chưa thể tái tạo đáp án in bằng bất kỳ cách đọc thứ tự bit nào, nên đã CHỦ ĐỔNG loại bỏ thay vì đưa lên site một câu không chắc chắn. Vì vậy phần này chỉ có 3 câu (thay vì 6) nhưng cả 3 đều đã tự tính lại độc lập và khớp chính xác với ảnh đáp án gốc.",
    "note_en": "This Floyd chapter has many more decoder/encoder/mux problems, but most require reading a specific figure from the book that cannot be reproduced accurately in text alone. One other problem (Problem 25) shows a mismatch between the printed question and the printed appendix answer (a suspected Global Edition printing erratum) and Problem 9 (bit sequences into a 4-bit adder), whose printed answer could not be reproduced under any bit-order reading, so it was deliberately excluded rather than publishing an uncertain answer. This section therefore has only 3 questions (instead of 6), but all three were independently recomputed by hand and matched exactly against the original answer photograph.",
    "items": [
      {
        "num": 1,
        "q_vi": "Với mạch cộng đầy đủ (full-adder) ở Hình 6–4 của sách, xác định đầu ra ứng với mỗi bộ giá trị đầu vào sau:<br>(a) A = 0, B = 1, C<sub>in</sub> = 0 &nbsp; (b) A = 1, B = 0, C<sub>in</sub> = 1<br>(c) A = 0, B = 0, C<sub>in</sub> = 0",
        "q_en": "For the full-adder of Figure 6–4, determine the outputs for each of the following inputs<br>(a) A = 0, B = 1, C<sub>in</sub> = 0 &nbsp; (b) A = 1, B = 0, C<sub>in</sub> = 1<br>(c) A = 0, B = 0, C<sub>in</sub> = 0",
        "src": "Floyd Ch.6 · Problem 1",
        "img": "essay_floyd_ch06_q01.png",
      },
      {
        "num": 3,
        "q_vi": "Xác định đầu ra của một mạch cộng đầy đủ (full-adder) ứng với mỗi bộ giá trị đầu vào sau:<br>(a) A = 1, B = 0, Cin = 0 &nbsp; (b) A = 0, B = 0, Cin = 1<br>(c) A = 0, B = 1, Cin = 1 &nbsp; (d) A = 1, B = 1, Cin = 1",
        "q_en": "Determine the outputs of a full-adder for each of the following inputs:<br>(a) A = 1, B = 0, Cin = 0 &nbsp; (b) A = 0, B = 0, Cin = 1<br>(c) A = 0, B = 1, Cin = 1 &nbsp; (d) A = 1, B = 1, Cin = 1",
        "src": "Floyd Ch.6 · Problem 3",
        "img": "essay_floyd_ch06_q03.png",
      },
      {
        "num": 15,
        "q_vi": "Với mỗi cặp số nhị phân sau, xác định trạng thái đầu ra của bộ so sánh (comparator):<br>(a) A3A2A1A0 = 1010, B3B2B1B0 = 1101<br>(b) A3A2A1A0 = 1101, B3B2B1B0 = 1101<br>(c) A3A2A1A0 = 1001, B3B2B1B0 = 1000",
        "q_en": "For each set of binary numbers, determine the output states for the comparator:<br>(a) A3A2A1A0 = 1010, B3B2B1B0 = 1101<br>(b) A3A2A1A0 = 1101, B3B2B1B0 = 1101<br>(c) A3A2A1A0 = 1001, B3B2B1B0 = 1000",
        "src": "Floyd Ch.6 · Problem 15",
        "img": "essay_floyd_ch06_q15.png",
      },
    ],
  },
  "04-computer-cpu": {
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 11 – Data Storage, Problems (p.690-693); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-24, A-25).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 11 – Data Storage, Problems (p.690-693); answers in the Answers to Odd-Numbered Problems appendix (p.A-24, A-25).",
    "items": [
      {
        "num": 3,
        "q_vi": "Hãy giải thích hai thao tác cơ bản của bộ nhớ: Write (ghi) và Read (đọc).",
        "q_en": "Explain the basic memory operations: Write and Read.",
        "src": "Floyd Ch.11 · Problem 3",
        "img": "essay_floyd_ch11_q03.png",
      },
      {
        "num": 5,
        "q_vi": "Một mảng bộ nhớ tĩnh 4 hàng, giống mảng ở Hình 11–10 của sách, ban đầu lưu toàn số 0. Nội dung của nó là gì sau các điều kiện sau? Giả sử giá trị 1 chọn hàng đó.<br>Row 0 = 1, Data in (Bit 0) = 1<br>Row 1 = 0, Data in (Bit 1) = 1<br>Row 2 = 1, Data in (Bit 2) = 0<br>Row 3 = 0, Data in (Bit 3) = 1",
        "q_en": "A static memory array with four rows similar to the one in Figure 11–10 is initially storing all 0s. What is its content after the following conditions? Assume a 1 selects a row.<br>Row 0 = 1, Data in (Bit 0) = 1<br>Row 1 = 0, Data in (Bit 1) = 1<br>Row 2 = 1, Data in (Bit 2) = 0<br>Row 3 = 0, Data in (Bit 3) = 1",
        "src": "Floyd Ch.11 · Problem 5",
        "img": "essay_floyd_ch11_q05.png",
      },
      {
        "num": 9,
        "q_vi": "Bộ nhớ đệm (cache memory) là gì?",
        "q_en": "What is cache memory?",
        "src": "Floyd Ch.11 · Problem 9",
        "img": "essay_floyd_ch11_q09.png",
      },
      {
        "num": 21,
        "q_vi": "Xét một RAM 4096 × 8, trong đó 64 địa chỉ cuối cùng được dùng làm ngăn xếp LIFO. Nếu địa chỉ đầu tiên của RAM là 000<sub>16</sub>, hãy xác định 64 địa chỉ dùng cho ngăn xếp.",
        "q_en": "Consider a 4096 × 8 RAM in which the last 64 addresses are used as a LIFO stack. If the first address in the RAM is 000<sub>16</sub>, designate the 64 addresses used for the stack.",
        "src": "Floyd Ch.11 · Problem 21",
        "img": "essay_floyd_ch11_q21.png",
      },
      {
        "num": 25,
        "q_vi": "Các thông số nào được dùng để đo hiệu năng của ổ đĩa cứng (hard disk)?",
        "q_en": "What are the parameters used to measure the performance of a hard disk?",
        "src": "Floyd Ch.11 · Problem 25",
        "img": "essay_floyd_ch11_q25.png",
      },
      {
        "num": 27,
        "q_vi": "Sự khác biệt chính giữa đĩa CD và đĩa DVD là gì?",
        "q_en": "What is the main difference between a CD and a DVD?",
        "src": "Floyd Ch.11 · Problem 27",
        "img": "essay_floyd_ch11_q27.png",
      },
    ],
  },
}
