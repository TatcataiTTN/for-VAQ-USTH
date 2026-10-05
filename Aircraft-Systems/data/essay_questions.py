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
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 2 – Number Systems, Operations, and Codes, Problems (p.117-121); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-1, A-2).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 2 – Number Systems, Operations, and Codes, Problems (p.117-121); answers in the Answers to Odd-Numbered Problems appendix (p.A-1, A-2).",
    "items": [
      {
        "num": 1,
        "q_vi": "Trọng số (weight) của chữ số 7 trong mỗi số thập phân sau là bao nhiêu?<br>(a) 1947 &nbsp; (b) 1799 &nbsp; (c) 1979",
        "q_en": "What is the weight of 7 in each of the following decimal numbers?<br>(a) 1947 &nbsp; (b) 1799 &nbsp; (c) 1979",
        "src": "Floyd Ch.2 · Problem 1",
        "img": "essay_floyd_ch02_q01.png",
        "note_vi": "Tự kiểm tra: 7 ở hàng đơn vị (1), hàng trăm (100), hàng chục (10), khớp đáp án in.",
        "note_en": "Self-check: 7 is in the units (1), hundreds (100) and tens (10) positions respectively, matching the printed answer."
      },
      {
        "num": 3,
        "q_vi": "Cho biết giá trị của từng chữ số trong các số thập phân sau:<br>(a) 263 &nbsp; (b) 5436 &nbsp; (c) 234543",
        "q_en": "Give the value of each digit in the following decimal numbers:<br>(a) 263 &nbsp; (b) 5436 &nbsp; (c) 234543",
        "src": "Floyd Ch.2 · Problem 3",
        "img": "essay_floyd_ch02_q03.png",
        "note_vi": "Tự kiểm tra từng chữ số nhân với trọng số của vị trí, khớp đáp án in.",
        "note_en": "Self-check: each digit times its positional weight, matching the printed answer."
      },
      {
        "num": 5,
        "q_vi": "Đổi các số nhị phân sau sang thập phân:<br>(a) 001 &nbsp; (b) 010 &nbsp; (c) 101 &nbsp; (d) 110<br>(e) 1010 &nbsp; (f) 1011 &nbsp; (g) 1110 &nbsp; (h) 1111",
        "q_en": "Convert the following binary numbers to decimal:<br>(a) 001 &nbsp; (b) 010 &nbsp; (c) 101 &nbsp; (d) 110<br>(e) 1010 &nbsp; (f) 1011 &nbsp; (g) 1110 &nbsp; (h) 1111",
        "src": "Floyd Ch.2 · Problem 5",
        "img": "essay_floyd_ch02_q05.png",
        "note_vi": "LỖI IN THẬT trong sách: ý (c) 101₂ = 4+0+1 = 5, nhưng đáp án in ghi 3. Các ý còn lại (1, 2, 6, 10, 11, 14, 15) đều đúng. Đừng học thuộc con số 3.",
        "note_en": "A REAL PRINTING ERROR in the book: item (c) 101₂ = 4+0+1 = 5, but the printed answer says 3. All other items (1, 2, 6, 10, 11, 14, 15) are correct. Do not memorise the 3."
      },
      {
        "num": 7,
        "q_vi": "Đổi mỗi số nhị phân sau sang thập phân:<br>(a) 110011.11 &nbsp; (b) 101010.01 &nbsp; (c) 1000001.111<br>(d) 1111000.101 &nbsp; (e) 1011100.10101 &nbsp; (f) 1110001.0001<br>(g) 1011010.1010 &nbsp; (h) 1111111.11111",
        "q_en": "Convert each binary number to decimal:<br>(a) 110011.11 &nbsp; (b) 101010.01 &nbsp; (c) 1000001.111<br>(d) 1111000.101 &nbsp; (e) 1011100.10101 &nbsp; (f) 1110001.0001<br>(g) 1011010.1010 &nbsp; (h) 1111111.11111",
        "src": "Floyd Ch.2 · Problem 7",
        "img": "essay_floyd_ch02_q07.png"
      },
      {
        "num": 9,
        "q_vi": "Cần bao nhiêu bit để biểu diễn các số thập phân sau?<br>(a) 5 &nbsp; (b) 10 &nbsp; (c) 15 &nbsp; (d) 20<br>(e) 100 &nbsp; (f) 120 &nbsp; (g) 140 &nbsp; (h) 160",
        "q_en": "How many bits are required to represent the following decimal numbers?<br>(a) 5 &nbsp; (b) 10 &nbsp; (c) 15 &nbsp; (d) 20<br>(e) 100 &nbsp; (f) 120 &nbsp; (g) 140 &nbsp; (h) 160",
        "src": "Floyd Ch.2 · Problem 9",
        "img": "essay_floyd_ch02_q09.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. (số bit tối thiểu = độ dài nhị phân của số đó).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. (minimum bits = binary length of the number)."
      },
      {
        "num": 11,
        "q_vi": "Đổi mỗi số thập phân sau sang nhị phân bằng phương pháp tổng các trọng số (sum-of-weights):<br>(a) 12 &nbsp; (b) 15 &nbsp; (c) 25 &nbsp; (d) 50<br>(e) 65 &nbsp; (f) 97 &nbsp; (g) 127 &nbsp; (h) 198",
        "q_en": "Convert each decimal number to binary by using the sum-of-weights method:<br>(a) 12 &nbsp; (b) 15 &nbsp; (c) 25 &nbsp; (d) 50<br>(e) 65 &nbsp; (f) 97 &nbsp; (g) 127 &nbsp; (h) 198",
        "src": "Floyd Ch.2 · Problem 11",
        "img": "essay_floyd_ch02_q11.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 13,
        "q_vi": "Đổi mỗi số thập phân sau sang nhị phân bằng phương pháp chia liên tiếp cho 2:<br>(a) 13 &nbsp; (b) 17 &nbsp; (c) 23 &nbsp; (d) 30<br>(e) 35 &nbsp; (f) 40 &nbsp; (g) 49 &nbsp; (h) 60",
        "q_en": "Convert each decimal number to binary using repeated division by 2:<br>(a) 13 &nbsp; (b) 17 &nbsp; (c) 23 &nbsp; (d) 30<br>(e) 35 &nbsp; (f) 40 &nbsp; (g) 49 &nbsp; (h) 60",
        "src": "Floyd Ch.2 · Problem 13",
        "img": "essay_floyd_ch02_q13.png"
      },
      {
        "num": 15,
        "q_vi": "Cộng các số nhị phân:<br>(a) 10 + 10 &nbsp; (b) 10 + 11 &nbsp; (c) 100 + 11<br>(d) 111 + 101 &nbsp; (e) 1111 + 111 &nbsp; (f) 1111 + 1111",
        "q_en": "Add the binary numbers:<br>(a) 10 + 10 &nbsp; (b) 10 + 11 &nbsp; (c) 100 + 11<br>(d) 111 + 101 &nbsp; (e) 1111 + 111 &nbsp; (f) 1111 + 1111",
        "src": "Floyd Ch.2 · Problem 15",
        "img": "essay_floyd_ch02_q15.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 17,
        "q_vi": "Thực hiện các phép nhân nhị phân sau:<br>(a) 11 × 10 &nbsp; (b) 101 × 11 &nbsp; (c) 111 × 110<br>(d) 1100 × 101 &nbsp; (e) 1110 × 1110 &nbsp; (f) 1111 × 1100",
        "q_en": "Perform the following binary multiplications:<br>(a) 11 × 10 &nbsp; (b) 101 × 11 &nbsp; (c) 111 × 110<br>(d) 1100 × 101 &nbsp; (e) 1110 × 1110 &nbsp; (f) 1111 × 1100",
        "src": "Floyd Ch.2 · Problem 17",
        "img": "essay_floyd_ch02_q17.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 19,
        "q_vi": "Có hai cách biểu diễn số không (zero) ở dạng bù một (1's complement) là gì?",
        "q_en": "What are two ways of representing zero in 1's complement form?",
        "src": "Floyd Ch.2 · Problem 19",
        "img": "essay_floyd_ch02_q19.png",
        "note_vi": "Kiểm tra bằng định nghĩa: 00000000 và đảo bit của nó là 11111111 (\"âm không\"), cả hai đều biểu diễn 0.",
        "note_en": "Check by definition: 00000000 and its bit-inversion 11111111 (\"negative zero\") both represent 0."
      },
      {
        "num": 21,
        "q_vi": "Xác định bù một (1's complement) của mỗi số nhị phân sau:<br>(a) 100 &nbsp; (b) 111 &nbsp; (c) 1100<br>(d) 10111011 &nbsp; (e) 1001010 &nbsp; (f) 10101010",
        "q_en": "Determine the 1's complement of each binary number:<br>(a) 100 &nbsp; (b) 111 &nbsp; (c) 1100<br>(d) 10111011 &nbsp; (e) 1001010 &nbsp; (f) 10101010",
        "src": "Floyd Ch.2 · Problem 21",
        "img": "essay_floyd_ch02_q21.png"
      },
      {
        "num": 23,
        "q_vi": "Biểu diễn mỗi số thập phân sau thành số 8 bit dạng dấu-độ lớn (sign-magnitude):<br>(a) +29 &nbsp; (b) −85 &nbsp; (c) +100 &nbsp; (d) −123",
        "q_en": "Express each decimal number in binary as an 8-bit sign-magnitude number:<br>(a) +29 &nbsp; (b) −85 &nbsp; (c) +100 &nbsp; (d) −123",
        "src": "Floyd Ch.2 · Problem 23",
        "img": "essay_floyd_ch02_q23.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 25,
        "q_vi": "Viết mỗi số thập phân sau dưới dạng số 8-bit ở dạng bù hai (2's complement):<br>(a) +12 &nbsp; (b) -68 &nbsp; (c) +101 &nbsp; (d) -125",
        "q_en": "Express each decimal number as an 8-bit number in the 2’s complement form:<br>(a) +12 &nbsp; (b) −68 &nbsp; (c) +101 &nbsp; (d) −125",
        "src": "Floyd Ch.2 · Problem 25",
        "img": "essay_floyd_ch02_q25.png"
      },
      {
        "num": 27,
        "q_vi": "Xác định giá trị thập phân của mỗi số nhị phân có dấu ở dạng bù một (1's complement):<br>(a) 10011001 &nbsp; (b) 01110100 &nbsp; (c) 10111111",
        "q_en": "Determine the decimal value of each signed binary number in the 1's complement form:<br>(a) 10011001 &nbsp; (b) 01110100 &nbsp; (c) 10111111",
        "src": "Floyd Ch.2 · Problem 27",
        "img": "essay_floyd_ch02_q27.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 29,
        "q_vi": "Biểu diễn mỗi số nhị phân dạng dấu-độ lớn sau ở định dạng dấu phẩy động độ chính xác đơn (single-precision floating-point):<br>(a) 0111110000101011 &nbsp; (b) 100110000011000",
        "q_en": "Express each of the following sign-magnitude binary numbers in single-precision floating-point format:<br>(a) 0111110000101011 &nbsp; (b) 100110000011000",
        "src": "Floyd Ch.2 · Problem 29",
        "img": "essay_floyd_ch02_q29.png",
        "note_vi": "LỖI IN trong ý (b): theo IEEE 754, số −3096 có phần định trị 10000011000 theo sau các số 0 (xác nhận bằng struct.pack của Python), nhưng đáp án in là 11000001100... (lệch một bước và thừa một bit 1). Phần dấu và phần mũ 10001010 trong đáp án in là đúng. Ý (a) hoàn toàn đúng.",
        "note_en": "PRINTING ERROR in item (b): by IEEE 754 the value −3096 has mantissa 10000011000 followed by zeros (confirmed with Python's struct.pack), but the printed answer shows 11000001100... (shifted by one place with an extra leading 1). The sign and the exponent 10001010 in the printed answer are correct. Item (a) is fully correct."
      },
      {
        "num": 31,
        "q_vi": "Đổi mỗi cặp số thập phân sang nhị phân rồi cộng bằng dạng bù hai (2's complement):<br>(a) 33 và 15 &nbsp; (b) 56 và −27 &nbsp; (c) −46 và 25 &nbsp; (d) −110 và −84",
        "q_en": "Convert each pair of decimal numbers to binary and add using the 2's complement form:<br>(a) 33 and 15 &nbsp; (b) 56 and −27 &nbsp; (c) −46 and 25 &nbsp; (d) −110 and −84",
        "src": "Floyd Ch.2 · Problem 31",
        "img": "essay_floyd_ch02_q31.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. Ý (d) cần 9 bit vì tổng −194 không vừa 8 bit.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. Item (d) needs 9 bits because −194 does not fit in 8 bits."
      },
      {
        "num": 33,
        "q_vi": "Thực hiện mỗi phép cộng ở dạng bù hai:<br>(a) 10001100 + 00111001 &nbsp; (b) 11011001 + 11100111",
        "q_en": "Perform each addition in the 2's complement form:<br>(a) 10001100 + 00111001 &nbsp; (b) 11011001 + 11100111",
        "src": "Floyd Ch.2 · Problem 33",
        "img": "essay_floyd_ch02_q33.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. (bỏ bit nhớ tràn ở ý b).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. (the overflow carry is discarded in item b)."
      },
      {
        "num": 35,
        "q_vi": "Nhân 01101010 với 11110001 ở dạng bù hai.",
        "q_en": "Multiply 01101010 by 11110001 in the 2's complement form.",
        "src": "Floyd Ch.2 · Problem 35",
        "img": "essay_floyd_ch02_q35.png",
        "note_vi": "Tự tính: 106 × (−15) = −1590; biểu diễn bù hai 12 bit là 100111001010, khớp đáp án in.",
        "note_en": "Own calculation: 106 × (−15) = −1590; its 12-bit two's complement is 100111001010, matching the printed answer."
      },
      {
        "num": 37,
        "q_vi": "Đổi mỗi số thập lục phân sau sang nhị phân:<br>(a) 46<sub>16</sub> &nbsp; (b) 54<sub>16</sub> &nbsp; (c) B4<sub>16</sub> &nbsp; (d) 1A3<sub>16</sub><br>(e) FA<sub>16</sub> &nbsp; (f) ABC<sub>16</sub> &nbsp; (g) ABCD<sub>16</sub>",
        "q_en": "Convert each hexadecimal number to binary:<br>(a) 46<sub>16</sub> &nbsp; (b) 54<sub>16</sub> &nbsp; (c) B4<sub>16</sub> &nbsp; (d) 1A3<sub>16</sub><br>(e) FA<sub>16</sub> &nbsp; (f) ABC<sub>16</sub> &nbsp; (g) ABCD<sub>16</sub>",
        "src": "Floyd Ch.2 · Problem 37",
        "img": "essay_floyd_ch02_q37.png",
        "note_vi": "LỖI IN trong ý (g): ABCD₁₆ = 1010 1011 1100 1101 = 1010101111001101, nhưng đáp án in là 1010110010111101 (tức ACBD₁₆, hai nhóm giữa bị đổi chỗ). Các ý còn lại đúng.",
        "note_en": "PRINTING ERROR in item (g): ABCD₁₆ = 1010 1011 1100 1101 = 1010101111001101, but the printed answer is 1010110010111101 (that is ACBD₁₆, with the two middle groups swapped). All other items are correct."
      },
      {
        "num": 39,
        "q_vi": "Đổi mỗi số thập lục phân sau sang thập phân:<br>(a) 42<sub>16</sub> &nbsp; (b) 64<sub>16</sub> &nbsp; (c) 2B<sub>16</sub> &nbsp; (d) 4D<sub>16</sub><br>(e) FF<sub>16</sub> &nbsp; (f) BC<sub>16</sub> &nbsp; (g) 6F1<sub>16</sub> &nbsp; (h) ABC<sub>16</sub>",
        "q_en": "Convert each hexadecimal number to decimal:<br>(a) 42<sub>16</sub> &nbsp; (b) 64<sub>16</sub> &nbsp; (c) 2B<sub>16</sub> &nbsp; (d) 4D<sub>16</sub><br>(e) FF<sub>16</sub> &nbsp; (f) BC<sub>16</sub> &nbsp; (g) 6F1<sub>16</sub> &nbsp; (h) ABC<sub>16</sub>",
        "src": "Floyd Ch.2 · Problem 39",
        "img": "essay_floyd_ch02_q39.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 41,
        "q_vi": "Thực hiện các phép cộng sau (số thập lục phân):<br>(a) 25<sub>16</sub> + 33<sub>16</sub> &nbsp; (b) 43<sub>16</sub> + 62<sub>16</sub> &nbsp; (c) A4<sub>16</sub> + F5<sub>16</sub> &nbsp; (d) FC<sub>16</sub> + AE<sub>16</sub>",
        "q_en": "Perform the following additions:<br>(a) 25<sub>16</sub> + 33<sub>16</sub> &nbsp; (b) 43<sub>16</sub> + 62<sub>16</sub> &nbsp; (c) A4<sub>16</sub> + F5<sub>16</sub> &nbsp; (d) FC<sub>16</sub> + AE<sub>16</sub>",
        "src": "Floyd Ch.2 · Problem 41",
        "img": "essay_floyd_ch02_q41.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 43,
        "q_vi": "Đổi mỗi số bát phân sau sang thập phân:<br>(a) 14<sub>8</sub> &nbsp; (b) 53<sub>8</sub> &nbsp; (c) 67<sub>8</sub> &nbsp; (d) 174<sub>8</sub><br>(e) 635<sub>8</sub> &nbsp; (f) 254<sub>8</sub> &nbsp; (g) 2673<sub>8</sub> &nbsp; (h) 7777<sub>8</sub>",
        "q_en": "Convert each octal number to decimal:<br>(a) 14<sub>8</sub> &nbsp; (b) 53<sub>8</sub> &nbsp; (c) 67<sub>8</sub> &nbsp; (d) 174<sub>8</sub><br>(e) 635<sub>8</sub> &nbsp; (f) 254<sub>8</sub> &nbsp; (g) 2673<sub>8</sub> &nbsp; (h) 7777<sub>8</sub>",
        "src": "Floyd Ch.2 · Problem 43",
        "img": "essay_floyd_ch02_q43.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 45,
        "q_vi": "Đổi mỗi số bát phân sau sang nhị phân:<br>(a) 17<sub>8</sub> &nbsp; (b) 26<sub>8</sub> &nbsp; (c) 145<sub>8</sub><br>(d) 456<sub>8</sub> &nbsp; (e) 653<sub>8</sub> &nbsp; (f) 777<sub>8</sub>",
        "q_en": "Convert each octal number into binary:<br>(a) 17<sub>8</sub> &nbsp; (b) 26<sub>8</sub> &nbsp; (c) 145<sub>8</sub><br>(d) 456<sub>8</sub> &nbsp; (e) 653<sub>8</sub> &nbsp; (f) 777<sub>8</sub>",
        "src": "Floyd Ch.2 · Problem 45",
        "img": "essay_floyd_ch02_q45.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 47,
        "q_vi": "Đổi mỗi số thập phân sau sang BCD 8421:<br>(a) 10 &nbsp; (b) 13 &nbsp; (c) 18 &nbsp; (d) 21 &nbsp; (e) 25 &nbsp; (f) 36<br>(g) 44 &nbsp; (h) 57 &nbsp; (i) 69 &nbsp; (j) 98 &nbsp; (k) 125 &nbsp; (l) 156",
        "q_en": "Convert each of the following decimal numbers to 8421 BCD:<br>(a) 10 &nbsp; (b) 13 &nbsp; (c) 18 &nbsp; (d) 21 &nbsp; (e) 25 &nbsp; (f) 36<br>(g) 44 &nbsp; (h) 57 &nbsp; (i) 69 &nbsp; (j) 98 &nbsp; (k) 125 &nbsp; (l) 156",
        "src": "Floyd Ch.2 · Problem 47",
        "img": "essay_floyd_ch02_q47.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. Đáp án in nằm trên hai trang (ảnh ghép hai phần: cuối trang A-1 và đầu trang A-2).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. The printed answer spans two pages (the image stitches the end of page A-1 and the top of page A-2)."
      },
      {
        "num": 49,
        "q_vi": "Đổi các số thập phân sau sang BCD:<br>(a) 104 &nbsp; (b) 128 &nbsp; (c) 132 &nbsp; (d) 150 &nbsp; (e) 186<br>(f) 210 &nbsp; (g) 359 &nbsp; (h) 547 &nbsp; (i) 1051",
        "q_en": "Convert the following decimal numbers to BCD:<br>(a) 104 &nbsp; (b) 128 &nbsp; (c) 132 &nbsp; (d) 150 &nbsp; (e) 186<br>(f) 210 &nbsp; (g) 359 &nbsp; (h) 547 &nbsp; (i) 1051",
        "src": "Floyd Ch.2 · Problem 49",
        "img": "essay_floyd_ch02_q49.png"
      },
      {
        "num": 51,
        "q_vi": "Đổi mỗi số BCD sau sang thập phân:<br>(a) 10000000 &nbsp; (b) 001000110111<br>(c) 001101000110 &nbsp; (d) 010000100001<br>(e) 011101010100 &nbsp; (f) 100000000000<br>(g) 100101111000 &nbsp; (h) 0001011010000011<br>(i) 1001000000011000 &nbsp; (j) 0110011001100111",
        "q_en": "Convert each of the BCD numbers to decimal:<br>(a) 10000000 &nbsp; (b) 001000110111<br>(c) 001101000110 &nbsp; (d) 010000100001<br>(e) 011101010100 &nbsp; (f) 100000000000<br>(g) 100101111000 &nbsp; (h) 0001011010000011<br>(i) 1001000000011000 &nbsp; (j) 0110011001100111",
        "src": "Floyd Ch.2 · Problem 51",
        "img": "essay_floyd_ch02_q51.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in.",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer."
      },
      {
        "num": 53,
        "q_vi": "Cộng các số BCD sau:<br>(a) 1000 + 0110 &nbsp; (b) 0111 + 0101<br>(c) 1001 + 1000 &nbsp; (d) 1001 + 0111<br>(e) 00100101 + 00100111 &nbsp; (f) 01010001 + 01011000<br>(g) 10011000 + 10010111 &nbsp; (h) 010101100001 + 011100001000",
        "q_en": "Add the following BCD numbers:<br>(a) 1000 + 0110 &nbsp; (b) 0111 + 0101<br>(c) 1001 + 1000 &nbsp; (d) 1001 + 0111<br>(e) 00100101 + 00100111 &nbsp; (f) 01010001 + 01011000<br>(g) 10011000 + 10010111 &nbsp; (h) 010101100001 + 011100001000",
        "src": "Floyd Ch.2 · Problem 53",
        "img": "essay_floyd_ch02_q53.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. (cộng theo số thập phân rồi mã hoá lại BCD).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. (add as decimal values, then re-encode as BCD)."
      },
      {
        "num": 55,
        "q_vi": "Trong một ứng dụng, dãy nhị phân 4 bit quay vòng định kỳ từ 1111 về 0000. Có bốn bit thay đổi và do trễ mạch, các thay đổi này có thể không xảy ra cùng lúc. Ví dụ, nếu LSB đổi trước thì số sẽ xuất hiện là 1110 trong lúc chuyển từ 1111 sang 0000 và có thể bị hệ thống hiểu nhầm. Hãy minh hoạ cách mã Gray tránh được vấn đề này.",
        "q_en": "In a certain application a 4-bit binary sequence cycles from 1111 to 0000 periodically. There are four bit changes, and because of circuit delays, these changes may not occur at the same instant. For example, if the LSB changes first, the number will appear as 1110 during the transition from 1111 to 0000 and may be misinterpreted by the system. Illustrate how the Gray code avoids this problem.",
        "src": "Floyd Ch.2 · Problem 55",
        "img": "essay_floyd_ch02_q55.png",
        "note_vi": "Tự kiểm tra: trong mã Gray 4 bit, 1000 (15 ở Gray) chuyển về 0000 chỉ đổi đúng 1 bit, nên không có trạng thái trung gian sai.",
        "note_en": "Self-check: in 4-bit Gray code the last code 1000 returns to 0000 by changing exactly one bit, so there is no wrong intermediate state."
      },
      {
        "num": 57,
        "q_vi": "Đổi mỗi mã Gray sau sang nhị phân:<br>(a) 1010 &nbsp; (b) 00010 &nbsp; (c) 11000010001",
        "q_en": "Convert each Gray code to binary:<br>(a) 1010 &nbsp; (b) 00010 &nbsp; (c) 11000010001",
        "src": "Floyd Ch.2 · Problem 57",
        "img": "essay_floyd_ch02_q57.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. (bit MSB giữ nguyên, các bit sau XOR dồn với bit nhị phân trước đó).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. (MSB kept, each following bit is XORed with the previous binary bit)."
      },
      {
        "num": 59,
        "q_vi": "Xác định mỗi ký tự ASCII (xem Bảng 2–7 của sách):<br>(a) 0011000 &nbsp; (b) 1001010 &nbsp; (c) 0111101<br>(d) 0100011 &nbsp; (e) 0111110 &nbsp; (f) 1000010",
        "q_en": "Determine each ASCII character. Refer to Table 2–7.<br>(a) 0011000 &nbsp; (b) 1001010 &nbsp; (c) 0111101<br>(d) 0100011 &nbsp; (e) 0111110 &nbsp; (f) 1000010",
        "src": "Floyd Ch.2 · Problem 59",
        "img": "essay_floyd_ch02_q59.png",
        "note_vi": "Đã tự tính lại bằng Python (script verify_ch2.py trong OCR_output/Floyd/scripts), khớp đáp án in. 0011000 = 24 thập phân là ký tự điều khiển CAN (Cancel).",
        "note_en": "Recomputed independently in Python (verify_ch2.py in OCR_output/Floyd/scripts); matches the printed answer. 0011000 = decimal 24 is the control character CAN (Cancel)."
      },
      {
        "num": 61,
        "q_vi": "Viết thông điệp ở Bài 60 dưới dạng thập lục phân.<br><i>Bài 60: Giải mã thông điệp mã ASCII sau: 1001000 1100101 1101100 1101100 1101111 0101110 0100000 1001000 1101111 1110111 0100000 1100001 1110010 1100101 0100000 1111001 1101111 1110101 0111111</i>",
        "q_en": "Write the message in Problem 60 in hexadecimal.<br><i>Problem 60: Decode the following ASCII coded message: 1001000 1100101 1101100 1101100 1101111 0101110 0100000 1001000 1101111 1110111 0100000 1100001 1110010 1100101 0100000 1111001 1101111 1110101 0111111</i>",
        "src": "Floyd Ch.2 · Problem 61",
        "img": "essay_floyd_ch02_q61.png",
        "note_vi": "Thông điệp giải mã được là \"Hello. How are you?\" (tự giải mã bằng Python), đổi từng ký tự sang hex cho đúng 19 byte như đáp án in.",
        "note_en": "The decoded message is \"Hello. How are you?\" (decoded in Python); converting each character to hex gives the same 19 bytes as the printed answer."
      },
      {
        "num": 63,
        "q_vi": "Xác định mã nào trong các mã kiểm tra chẵn lẻ (even parity) sau bị lỗi:<br>(a) 100110010 &nbsp; (b) 011101010 &nbsp; (c) 10111111010001010",
        "q_en": "Determine which of the following even parity codes are in error:<br>(a) 100110010 &nbsp; (b) 011101010 &nbsp; (c) 10111111010001010",
        "src": "Floyd Ch.2 · Problem 63",
        "img": "essay_floyd_ch02_q63.png"
      },
      {
        "num": 65,
        "q_vi": "Gắn bit chẵn (even parity) thích hợp vào mỗi byte dữ liệu sau:<br>(a) 10100100 &nbsp; (b) 00001001 &nbsp; (c) 11111110",
        "q_en": "Attach the proper even parity bit to each of the following bytes of data:<br>(a) 10100100 &nbsp; (b) 00001001 &nbsp; (c) 11111110",
        "src": "Floyd Ch.2 · Problem 65",
        "img": "essay_floyd_ch02_q65.png",
        "note_vi": "Tự kiểm tra: đếm số bit 1 (3, 2, 7); bit parity được đặt ở đầu byte (1, 0, 1) để tổng số bit 1 chẵn, đúng như đáp án in.",
        "note_en": "Self-check: count the 1s (3, 2, 7); the parity bit is placed in front of the byte (1, 0, 1) so the total number of 1s is even, as in the printed answer."
      },
      {
        "num": 67,
        "q_vi": "Kiểm chứng rằng phép trừ modulo-2 giống phép cộng modulo-2, bằng cách cộng kết quả của mỗi phép tính ở Bài 66 với một trong hai số ban đầu để thu được số còn lại.<br><i>Bài 66: Áp dụng modulo-2 cho: (a) 1100 + 1011 &nbsp; (b) 1111 + 0100 &nbsp; (c) 10011001 + 100011100</i>",
        "q_en": "Verify that modulo-2 subtraction is the same as modulo-2 addition by adding the result of each operation in problem 66 to either of the original numbers to get the other number. This will show that the result is the same as the difference of the two numbers.<br><i>Problem 66: Apply modulo-2 to the following: (a) 1100 + 1011 &nbsp; (b) 1111 + 0100 &nbsp; (c) 10011001 + 100011100</i>",
        "src": "Floyd Ch.2 · Problem 67",
        "img": "essay_floyd_ch02_q67.png",
        "note_vi": "Tự tính bằng XOR: 1100⊕1011 = 0111; 1111⊕0100 = 1011; 10011001⊕100011100 = 110000101; XOR kết quả với một số ban đầu cho ra đúng số còn lại.",
        "note_en": "Own XOR calculation: 1100⊕1011 = 0111; 1111⊕0100 = 1011; 10011001⊕100011100 = 110000101; XORing each result with one original number returns the other."
      },
      {
        "num": 69,
        "q_vi": "Giả sử mã tạo ra ở Bài 68 bị lỗi ở bit có trọng số lớn nhất (MSB) trong lúc truyền. Hãy áp dụng CRC để phát hiện lỗi.<br><i>Bài 68: Áp dụng CRC cho các bit dữ liệu 10110010 với mã sinh (generator) 1010 để tạo mã CRC được truyền.</i>",
        "q_en": "Assume that the code produced in problem 68 incurs an error in the most significant bit during transmission. Apply CRC to detect the error.<br><i>Problem 68: Apply CRC to the data bits 10110010 using the generator code 1010 to produce the transmitted CRC code.</i>",
        "src": "Floyd Ch.2 · Problem 69",
        "img": "essay_floyd_ch02_q69.png",
        "note_vi": "Tự tính (sách không in đáp án Bài 68): CRC của 10110010 với 1010 là 110, mã truyền 10110010110. Lỗi ở MSB cho 00110010110, chia cho 1010 dư 100 (viết 4 bit là 0100) khác 0 nên phát hiện lỗi, khớp đáp án in.",
        "note_en": "Own calculation (the book prints no answer for Problem 68): the CRC of 10110010 with 1010 is 110, so the transmitted code is 10110010110. An MSB error gives 00110010110, whose remainder on division by 1010 is 100 (4 bits: 0100), non-zero, so the error is detected, matching the printed answer."
      }
    ],
    "note_vi": "Chương 2 có 69 bài; chỉ bài SỐ LẺ có đáp án in. Phần này đã đưa đủ 35 bài lẻ, mỗi bài kèm ảnh đáp án thật; toàn bộ đáp án số đã được tự tính lại bằng Python. Quá trình đối chiếu phát hiện 3 LỖI IN THẬT trong đáp án của sách: Bài 5(c), Bài 29(b) và Bài 37(g), đã ghi chú rõ ngay dưới từng bài. Bài chẵn không có đáp án in nên không đưa.",
    "note_en": "Chapter 2 has 69 problems; only the ODD-numbered ones have printed answers. All 35 odd problems are included here, each with the real answer image; every numeric answer was recomputed in Python. The cross-check found 3 REAL PRINTING ERRORS in the book's answers: Problems 5(c), 29(b) and 37(g), flagged directly under each problem. Even-numbered problems have no printed answer and are omitted."
  },
  "02-logic-boolean": {
    "src_book": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 3 – Logic Gates và Chapter 4 – Boolean Algebra and Logic Simplification, Problems (Ch.3 p.179-186, Ch.4 p.252-253); đáp án ở phụ lục Answers to Odd-Numbered Problems (p.A-2, A-3, A-3 đến A-4).",
    "src_book_en": "Thomas L. Floyd, Digital Fundamentals, 11th ed., Chapter 3 – Logic Gates and Chapter 4 – Boolean Algebra and Logic Simplification, Problems (Ch.3 p.179-186, Ch.4 p.252-253); answers in the Answers to Odd-Numbered Problems appendix (p.A-2, A-3, A-3 to A-4).",
    "items": [
      {
        "num": 1,
        "q_vi": "Dạng sóng đầu vào ở Hình 3–76 được đưa vào một hệ thống gồm hai cổng đảo (inverter) nối tiếp. Hãy vẽ dạng sóng ngõ ra trên mỗi cổng đảo, đúng tương quan với đầu vào.",
        "q_en": "The input waveform shown in Figure 3–76 is applied to a system of two inverters connected in series. Draw the output waveform across each inverter in proper relation to the input.",
        "src": "Floyd Ch.3 · Problem 1",
        "img": "essay_floyd_ch03_q01.png",
        "qimgs": [
          "essay_floyd_fig03_76.png"
        ],
        "note_vi": "Hai cổng đảo liên tiếp trả lại đúng dạng sóng ban đầu: ngõ ra cuối trùng ngõ vào.",
        "note_en": "Two inverters in a row return the original waveform: the final output equals the input."
      },
      {
        "num": 3,
        "q_vi": "Nếu đưa dạng sóng của Hình 3–76 vào điểm A của mạch Hình 3–77, hãy xác định dạng sóng tại các điểm B đến F.",
        "q_en": "If the waveform in Figure 3–76 is applied to point A in Figure 3–77, determine the waveforms at points B through F.",
        "src": "Floyd Ch.3 · Problem 3",
        "img": "essay_floyd_ch03_q03.png",
        "qimgs": [
          "essay_floyd_fig03_76.png",
          "essay_floyd_fig03_77.png"
        ],
        "note_vi": "Kiểm chứng: B = Ā, C = A, D = Ā, E = A, F = Ā (C đi qua hai cổng đảo, F lấy từ C qua một cổng đảo).",
        "note_en": "Check: B = A′, C = A, D = A′, E = A, F = A′ (C passes through two inverters, F is taken from C through one inverter)."
      },
      {
        "num": 5,
        "q_vi": "Hãy xác định ngõ ra X của cổng AND 2 ngõ vào với các dạng sóng đầu vào ở Hình 3–78. Trình bày tương quan giữa ngõ ra và các ngõ vào bằng giản đồ thời gian.",
        "q_en": "Determine the output, X, for a 2-input AND gate with the input waveforms shown in Figure 3–78. Show the proper relationship of output to inputs with a timing diagram.",
        "src": "Floyd Ch.3 · Problem 5",
        "img": "essay_floyd_ch03_q05.png",
        "qimgs": [
          "essay_floyd_fig03_78.png"
        ],
        "note_vi": "Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 7,
        "q_vi": "Các dạng sóng đầu vào của cổng AND 3 ngõ vào được cho ở Hình 3–80. Hãy vẽ dạng sóng ngõ ra tương quan đúng với các đầu vào bằng giản đồ thời gian.",
        "q_en": "The input waveforms applied to a 3-input AND gate are as indicated in Figure 3–80. Show the output waveform in proper relation to the inputs with a timing diagram.",
        "src": "Floyd Ch.3 · Problem 7",
        "img": "essay_floyd_ch03_q07.png",
        "qimgs": [
          "essay_floyd_fig03_80.png"
        ],
        "note_vi": "Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 9,
        "q_vi": "Hãy vẽ ký hiệu hình chữ nhật (rectangular outline) cho cổng OR 3 ngõ vào.",
        "q_en": "Draw the rectangular outline symbol for a 3-input OR gate.",
        "src": "Floyd Ch.3 · Problem 9",
        "img": "essay_floyd_ch03_q09.png"
      },
      {
        "num": 11,
        "q_vi": "Hãy xác định ngõ ra của cổng OR 2 ngõ vào khi các dạng sóng đầu vào như ở Hình 3–79 và vẽ giản đồ thời gian.",
        "q_en": "Determine the output for a 2-input OR gate when the input waveforms are as in Figure 3–79 and draw a timing diagram.",
        "src": "Floyd Ch.3 · Problem 11",
        "img": "essay_floyd_ch03_q11.png",
        "qimgs": [
          "essay_floyd_fig03_79.png"
        ],
        "note_vi": "Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 13,
        "q_vi": "Lặp lại Bài 8 cho cổng OR 4 ngõ vào.<br><i>Bài 8: Các dạng sóng đầu vào của cổng AND 4 ngõ vào được cho ở Hình 3–81. Ngõ ra cổng AND được đưa vào một cổng đảo. Hãy vẽ dạng sóng ngõ ra tổng của hệ thống.</i>",
        "q_en": "Repeat Problem 8 for a 4-input OR gate.<br><i>Problem 8: The input waveforms applied to a 4-input AND gate are as indicated in Figure 3–81. The output of the AND gate is fed to an inverter. Draw the net output waveform of this system.</i>",
        "src": "Floyd Ch.3 · Problem 13",
        "img": "essay_floyd_ch03_q13.png",
        "qimgs": [
          "essay_floyd_fig03_81.png"
        ],
        "note_vi": "Vì \"lặp lại Bài 8\" bao gồm cả cổng đảo ở ngõ ra, đáp án in là NOR (OR rồi đảo): ngõ ra chỉ lên mức cao khi cả 4 đầu vào cùng thấp. Đã kiểm chứng đúng như vậy trên toàn bộ các khoảng. Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Because \"repeat Problem 8\" includes the inverter at the output, the printed answer is a NOR (OR followed by inversion): the output is HIGH only when all four inputs are LOW. This was verified across all intervals. Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 15,
        "q_vi": "Hãy vẽ ký hiệu hình chữ nhật (rectangular outline) cho cổng OR 4 ngõ vào.",
        "q_en": "Draw the rectangular outline symbol for a 4-input OR gate.",
        "src": "Floyd Ch.3 · Problem 15",
        "img": "essay_floyd_ch03_q15.png"
      },
      {
        "num": 17,
        "q_vi": "Với tập dạng sóng đầu vào ở Hình 3–83, hãy xác định ngõ ra của cổng được vẽ (NAND) và vẽ giản đồ thời gian.",
        "q_en": "For the set of input waveforms in Figure 3–83, determine the output for the gate shown and draw the timing diagram.",
        "src": "Floyd Ch.3 · Problem 17",
        "img": "essay_floyd_ch03_q17.png",
        "qimgs": [
          "essay_floyd_fig03_83.png"
        ],
        "note_vi": "Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 19,
        "q_vi": "Hãy xác định dạng sóng ngõ ra trong Hình 3–85 (cổng NAND 4 ngõ vào).",
        "q_en": "Determine the output waveform in Figure 3–85.",
        "src": "Floyd Ch.3 · Problem 19",
        "img": "essay_floyd_ch03_q19.png",
        "qimgs": [
          "essay_floyd_fig03_85.png"
        ],
        "note_vi": "Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 21,
        "q_vi": "Lặp lại Bài 17 cho cổng NOR 2 ngõ vào.<br><i>Bài 17: Với tập dạng sóng đầu vào ở Hình 3–83, hãy xác định ngõ ra của cổng được vẽ và vẽ giản đồ thời gian.</i>",
        "q_en": "Repeat Problem 17 for a 2-input NOR gate.<br><i>Problem 17: For the set of input waveforms in Figure 3–83, determine the output for the gate shown and draw the timing diagram.</i>",
        "src": "Floyd Ch.3 · Problem 21",
        "img": "essay_floyd_ch03_q21.png",
        "qimgs": [
          "essay_floyd_fig03_83.png"
        ],
        "note_vi": "Chỉ dùng dạng sóng đầu vào của hình; bỏ qua ký hiệu cổng vẽ trong hình vì bài yêu cầu loại cổng khác. Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Use only the input waveforms of the figure; ignore the gate symbol drawn in it, since the problem asks for a different gate. Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 23,
        "q_vi": "Lặp lại Bài 19 cho cổng NOR 4 ngõ vào.<br><i>Bài 19: Hãy xác định dạng sóng ngõ ra trong Hình 3–85.</i>",
        "q_en": "Repeat Problem 19 for a 4-input NOR gate.<br><i>Problem 19: Determine the output waveform in Figure 3–85.</i>",
        "src": "Floyd Ch.3 · Problem 23",
        "img": "essay_floyd_ch03_q23.png",
        "qimgs": [
          "essay_floyd_fig03_85.png"
        ],
        "note_vi": "Chỉ dùng dạng sóng đầu vào của hình; bỏ qua ký hiệu cổng vẽ trong hình vì bài yêu cầu loại cổng khác. Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Use only the input waveforms of the figure; ignore the gate symbol drawn in it, since the problem asks for a different gate. Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 25,
        "q_vi": "Cổng exclusive-OR (XOR) khác cổng OR như thế nào về mặt hoạt động logic?",
        "q_en": "How does an exclusive-OR gate differ from an OR gate in its logical operation?",
        "src": "Floyd Ch.3 · Problem 25",
        "img": "essay_floyd_ch03_q25.png"
      },
      {
        "num": 27,
        "q_vi": "Lặp lại Bài 17 cho cổng exclusive-NOR.<br><i>Bài 17: Với tập dạng sóng đầu vào ở Hình 3–83, hãy xác định ngõ ra của cổng được vẽ và vẽ giản đồ thời gian.</i>",
        "q_en": "Repeat Problem 17 for an exclusive-NOR gate.<br><i>Problem 17: For the set of input waveforms in Figure 3–83, determine the output for the gate shown and draw the timing diagram.</i>",
        "src": "Floyd Ch.3 · Problem 27",
        "img": "essay_floyd_ch03_q27.png",
        "qimgs": [
          "essay_floyd_fig03_83.png"
        ],
        "note_vi": "Chỉ dùng dạng sóng đầu vào của hình; bỏ qua ký hiệu cổng vẽ trong hình vì bài yêu cầu loại cổng khác. Đáp án in đã kiểm chứng: đọc mức logic từng khoảng thời gian trực tiếp từ pixel hình đề và hình đáp án, tính lại ngõ ra bằng cổng tương ứng, khớp 100% mọi khoảng; đầu vào trong hình đáp án trùng hình đề.",
        "note_en": "Use only the input waveforms of the figure; ignore the gate symbol drawn in it, since the problem asks for a different gate. Printed answer verified: logic levels in every time interval were read directly from the pixels of the question and answer figures, the output was recomputed with the matching gate, and all intervals agree; the inputs in the answer figure match the question figure."
      },
      {
        "num": 29,
        "q_vi": "Trong mảng AND lập trình được với các liên kết (link) lập trình được ở Hình 3–89, hãy xác định các biểu thức Boole ở ngõ ra.",
        "q_en": "In the simple programmed AND array with programmable links in Figure 3–89, determine the Boolean output expressions.",
        "src": "Floyd Ch.3 · Problem 29",
        "img": "essay_floyd_ch03_q29.png",
        "qimgs": [
          "essay_floyd_fig03_89.png"
        ],
        "note_vi": "Tự kiểm chứng: đọc từng liên kết còn nguyên trong hình, cổng X1 nhận Ā và B, cổng X2 nhận Ā và B̄, cổng X3 nhận A và B̄, khớp đáp án in.",
        "note_en": "Self-check: reading every intact link in the figure, gate X1 receives A′ and B, gate X2 receives A′ and B′, gate X3 receives A and B′, matching the printed answer."
      },
      {
        "num": 31,
        "q_vi": "Hãy mô tả cổng AND 4 ngõ vào bằng VHDL.",
        "q_en": "Describe a 4-input AND gate using VHDL.",
        "src": "Floyd Ch.3 · Problem 31",
        "img": "essay_floyd_ch03_q31.png",
        "note_vi": "Lưu ý lỗi trong đáp án in: tên entity \"4InputAND\" bắt đầu bằng chữ số nên KHÔNG hợp lệ trong VHDL (định danh phải bắt đầu bằng chữ cái), và dòng end entity ghi \"4Input AND\" có khoảng trắng. Phần logic X <= A and B and C and D là đúng.",
        "note_en": "Note on errors in the printed answer: the entity name \"4InputAND\" starts with a digit, so it is NOT a legal VHDL identifier (identifiers must start with a letter), and the end entity line reads \"4Input AND\" with a space. The logic X <= A and B and C and D is correct."
      },
      {
        "num": 33,
        "q_vi": "Khi so sánh một số loại linh kiện logic, người ta thấy công suất tiêu thụ của một loại tăng lên khi tần số tăng. Linh kiện đó là lưỡng cực (bipolar) hay CMOS?",
        "q_en": "In the comparison of certain logic devices, it is noted that the power dissipation for one particular type increases as the frequency increases. Is the device bipolar or CMOS?",
        "src": "Floyd Ch.3 · Problem 33",
        "img": "essay_floyd_ch03_q33.png",
        "note_vi": "Lý do: công suất động của CMOS tỉ lệ với tần số (mỗi lần chuyển mức phải nạp/xả điện dung), còn mạch lưỡng cực tiêu thụ gần như không đổi theo tần số.",
        "note_en": "Reason: CMOS dynamic power grows with frequency (each transition charges/discharges capacitance), while bipolar logic draws nearly constant power regardless of frequency."
      },
      {
        "num": 35,
        "q_vi": "Hãy xác định tPLH và tPHL từ màn hình dao động ký ở Hình 3–91. Các số đọc cho biết volt/vạch và giây/vạch của từng kênh.",
        "q_en": "Determine tPLH and tPHL from the oscilloscope display in Figure 3–91. The readings indicate volts/div and sec/div for each channel.",
        "src": "Floyd Ch.3 · Problem 35",
        "img": "essay_floyd_ch03_q35.png",
        "qimgs": [
          "essay_floyd_fig03_91.png"
        ],
        "note_vi": "Tự đo trên ảnh: tại mức 50%, tPLH ≈ 4,1 ns và tPHL ≈ 11,1 ns (5 ns/vạch). Gần với đáp án in 4,3 ns và 10,5 ns; chênh lệch nhỏ do cách ước lượng điểm 50% trên màn hình, đúng bậc đại lượng và đúng quan hệ tPHL > tPLH.",
        "note_en": "Own measurement on the image: at the 50% level, tPLH ≈ 4.1 ns and tPHL ≈ 11.1 ns (5 ns/div). Close to the printed 4.3 ns and 10.5 ns; the small difference comes from how the 50% point is estimated on screen. The order of magnitude and the relation tPHL > tPLH both agree."
      },
      {
        "num": 37,
        "q_vi": "Nếu một cổng logic hoạt động với nguồn một chiều +5 V và tiêu thụ dòng trung bình 4 mA, công suất tiêu tán của nó là bao nhiêu?",
        "q_en": "If a logic gate operates on a dc supply voltage of +5 V and draws an average current of 4 mA, what is its power dissipation?",
        "src": "Floyd Ch.3 · Problem 37",
        "img": "essay_floyd_ch03_q37.png",
        "note_vi": "Tự tính: P = V × I = 5 V × 4 mA = 20 mW, khớp đáp án in.",
        "note_en": "Own calculation: P = V × I = 5 V × 4 mA = 20 mW, matching the printed answer."
      },
      {
        "num": 39,
        "q_vi": "Hãy xét các điều kiện nêu trong Hình 3–92 và xác định các cổng bị hỏng.",
        "q_en": "Examine the conditions indicated in Figure 3–92, and identify the faulty gates.",
        "src": "Floyd Ch.3 · Problem 39",
        "img": "essay_floyd_ch03_q39.png",
        "qimgs": [
          "essay_floyd_fig03_92.png"
        ],
        "note_vi": "Tự kiểm tra từng cổng: (a) NAND(1,1)=0 đúng; (b) AND(1,1,0) phải bằng 0 nhưng ra 1, HỎNG; (c) cổng OR có hai đầu vào đảo, 0,0 thành 1,1 nên ngõ ra phải là 1 nhưng ra 0, HỎNG; (d) NOR(0,0,0,1)=0 đúng; (e) XOR(1,0) phải bằng 1 nhưng ra 0, HỎNG; (f) XOR(1,1)=0 đúng. Kết quả (b), (c), (e) khớp đáp án in.",
        "note_en": "Gate-by-gate check: (a) NAND(1,1)=0 correct; (b) AND(1,1,0) must be 0 but shows 1, FAULTY; (c) an OR gate with inverted inputs turns 0,0 into 1,1, so the output must be 1 but shows 0, FAULTY; (d) NOR(0,0,0,1)=0 correct; (e) XOR(1,0) must be 1 but shows 0, FAULTY; (f) XOR(1,1)=0 correct. (b), (c), (e) match the printed answer."
      },
      {
        "num": 43,
        "q_vi": "Mỗi lần bật công tắc đánh lửa trong mạch Hình 3–17, còi báo động kêu trong ba mươi giây, kể cả khi đã cài dây an toàn. Nguyên nhân khả dĩ nhất của sự cố này là gì?",
        "q_en": "Every time the ignition switch is turned on in the circuit of Figure 3–17, the alarm comes on for thirty seconds, even when the seat belt is buckled. What is the most probable cause of this malfunction?",
        "src": "Floyd Ch.3 · Problem 43",
        "img": "essay_floyd_ch03_q43.png",
        "qimgs": [
          "essay_floyd_fig03_17.png"
        ],
        "note_vi": "Suy luận: còi = A·B·C. Khi đã cài dây an toàn thì B phải THẤP, còi không thể kêu; nó vẫn kêu trong lúc bộ định thời (C) đang CAO nghĩa là ngõ vào B của cổng AND luôn bị đọc là CAO, tức dây ngõ vào đó bị hở (ngõ vào TTL để hở trôi lên mức cao). Khớp đáp án in.",
        "note_en": "Reasoning: alarm = A·B·C. With the belt buckled B must be LOW and the alarm cannot sound; if it still sounds while the timer (C) is HIGH, the AND gate's B input must always be read as HIGH, i.e. that input wire is open (an open TTL input floats HIGH). Matches the printed answer."
      },
      {
        "num": 45,
        "q_vi": "Hãy sửa bộ đếm tần số ở Hình 3–16 để hoạt động với xung cho phép (enable) tích cực mức THẤP thay vì mức CAO trong khoảng 1 ms.",
        "q_en": "Modify the frequency counter in Figure 3–16 to operate with an enable pulse that is active-LOW rather than HIGH during the 1 ms interval.",
        "src": "Floyd Ch.3 · Problem 45",
        "img": "essay_floyd_ch03_q45.png",
        "qimgs": [
          "essay_floyd_fig03_16.png"
        ],
        "note_vi": "Suy luận: cổng AND chỉ cho xung đi qua khi chân enable ở mức CAO; nếu enable tích cực mức THẤP thì phải đảo nó trước khi vào cổng AND, đúng như đáp án in.",
        "note_en": "Reasoning: the AND gate only passes pulses while its enable pin is HIGH; with an active-LOW enable it must be inverted before reaching the AND gate, as in the printed answer."
      },
      {
        "num": 47,
        "q_vi": "Hãy thiết kế một mạch đặt vào khối màu be ở Hình 3–96 sao cho đèn pha ô tô tự động tắt sau 15 s kể từ khi công tắc đánh lửa tắt, nếu công tắc đèn vẫn đang bật. Giả sử cần mức THẤP để tắt đèn.",
        "q_en": "Design a circuit to fit in the beige block of Figure 3–96 that will cause the headlights of an automobile to be turned off automatically 15 s after the ignition switch is turned off, if the light switch is left on. Assume that a LOW is required to turn the lights off.",
        "src": "Floyd Ch.3 · Problem 47",
        "img": "essay_floyd_ch03_q47.png",
        "qimgs": [
          "essay_floyd_fig03_96.png"
        ],
        "note_vi": "Kiểm chứng logic của đáp án in: đảo công tắc đánh lửa rồi AND với công tắc đèn, ngõ ra chỉ lên CAO khi đánh lửa TẮT và đèn BẬT; khi đó bộ định thời đếm 15 s rồi xuất mức THẤP để tắt đèn.",
        "note_en": "Logic check of the printed answer: invert the ignition switch and AND it with the light switch; the output goes HIGH only when the ignition is OFF and the lights are ON, after which the timer counts 15 s and outputs a LOW to turn the lights off."
      },
      {
        "num": 51,
        "q_vi": "Trong một quy trình sản xuất tự động, linh kiện điện tử được tự động cắm vào bo mạch in (PCB). Trước khi kích hoạt dụng cụ cắm, PCB phải được định vị đúng và linh kiện cần cắm phải nằm trong buồng. Mỗi điều kiện tiên quyết này được báo bằng một mức điện áp CAO. Dụng cụ cắm cần mức điện áp THẤP để kích hoạt. Hãy thiết kế mạch thực hiện quy trình này.",
        "q_en": "In a certain automated manufacturing process, electrical components are automatically inserted in a PCB. Before the insertion tool is activated, the PCB must be properly positioned, and the component to be inserted must be in the chamber. Each of these prerequisite conditions is indicated by a HIGH voltage. The insertion tool requires a LOW voltage to activate it. Design a circuit to implement this process.",
        "src": "Floyd Ch.3 · Problem 51",
        "img": "essay_floyd_ch03_q51.png",
        "note_vi": "Kiểm chứng: cần \"cả hai điều kiện CAO thì ngõ ra THẤP\", đó chính là cổng NAND, đúng như đáp án in.",
        "note_en": "Check: the requirement \"both conditions HIGH gives a LOW output\" is exactly a NAND gate, as in the printed answer."
      },
      {
        "num": 1,
        "q_vi": "Dùng ký hiệu Boolean, viết một biểu thức có giá trị 0 CHỈ KHI tất cả các biến (A, B, C, D) đều bằng 0.",
        "q_en": "Using Boolean notation, write an expression that is a 0 only when all of its variables (A, B, C, and D) are 0s.",
        "src": "Floyd Ch.4 · Problem 1",
        "img": "essay_floyd_ch04_q01.png"
      },
      {
        "num": 5,
        "q_vi": "Tìm giá trị của các biến sao cho mỗi số hạng TÍCH bằng 1 và mỗi số hạng TỔNG bằng 0:<br>(a) ABC &nbsp; (b) A + B + C &nbsp; (c) ~{A}~{B}C &nbsp; (d) ~{A} + ~{B} + C<br>(e) A + ~{B} + ~{C} &nbsp; (f) ~{A} + ~{B} + ~{C}",
        "q_en": "Find the values of the variables that make each product term 1 and each sum term 0.<br>(a) ABC &nbsp; (b) A + B + C &nbsp; (c) ~{A}~{B}C &nbsp; (d) ~{A} + ~{B} + C<br>(e) A + ~{B} + ~{C} &nbsp; (f) ~{A} + ~{B} + ~{C}",
        "src": "Floyd Ch.4 · Problem 5",
        "img": "essay_floyd_ch04_q05.png"
      },
      {
        "num": 7,
        "q_vi": "Xác định luật đại số Boole làm cơ sở cho mỗi đẳng thức sau:<br>(a) A + AB + ABC + ~{ABCD} = ~{ABCD} + ABC + AB + A<br>(b) A + ~{AB} + ABC + ~{ABCD} = ~{DCBA} + CBA + ~{BA} + A<br>(c) AB(CD + ~{CD} + EF + ~{EF}) = ABCD + AB~{CD} + ABEF + AB~{EF}",
        "q_en": "Identify the law of Boolean algebra upon which each of the following equalities is based:<br>(a) A + AB + ABC + ~{ABCD} = ~{ABCD} + ABC + AB + A<br>(b) A + ~{AB} + ABC + ~{ABCD} = ~{DCBA} + CBA + ~{BA} + A<br>(c) AB(CD + ~{CD} + EF + ~{EF}) = ABCD + AB~{CD} + ABEF + AB~{EF}",
        "src": "Floyd Ch.4 · Problem 7",
        "img": "essay_floyd_ch04_q07.png"
      },
      {
        "num": 9,
        "q_vi": "Áp dụng các định lý De Morgan cho mỗi biểu thức sau:<br>(a) ~{A + ~{B}} &nbsp; (b) ~{~{A}B} &nbsp; (c) ~{A + B + C} &nbsp; (d) ~{ABC}<br>(e) ~{A(B + C)} &nbsp; (f) ~{AB} + ~{CD} &nbsp; (g) ~{AB + CD} &nbsp; (h) ~{(A + ~{B})(~{C} + D)}",
        "q_en": "Apply DeMorgan's theorems to each expression:<br>(a) ~{A + ~{B}} &nbsp; (b) ~{~{A}B} &nbsp; (c) ~{A + B + C} &nbsp; (d) ~{ABC}<br>(e) ~{A(B + C)} &nbsp; (f) ~{AB} + ~{CD} &nbsp; (g) ~{AB + CD} &nbsp; (h) ~{(A + ~{B})(~{C} + D)}",
        "src": "Floyd Ch.4 · Problem 9",
        "img": "essay_floyd_ch04_q09.png"
      },
      {
        "num": 13,
        "q_vi": "Viết biểu thức Boole cho mỗi mạch logic ở Hình 4–57.",
        "q_en": "Write the Boolean expression for each of the logic circuits in Figure 4–57.",
        "src": "Floyd Ch.4 · Problem 13",
        "img": "essay_floyd_ch04_q13.png",
        "note_vi": "Tự kiểm tra bằng cách đọc mạch: (a) AND 4 ngõ vào, X = ABCD; (b) AND(A,B) rồi OR với C, X = AB + C; (c) đảo A, AND với B, rồi đảo ngõ ra, X = (Ā·B)‾ = A + B̄; (d) OR(A,B) rồi AND với C, X = (A + B)C. Khớp đáp án in.",
        "note_en": "Self-check by reading each circuit: (a) 4-input AND, X = ABCD; (b) AND(A,B) then OR with C, X = AB + C; (c) invert A, AND with B, then invert the output, X = (A′·B)′ = A + B′; (d) OR(A,B) then AND with C, X = (A + B)C. Matches the printed answer.",
        "qimgs": [
          "essay_floyd_ch04_qq13.png"
        ]
      },
      {
        "num": 19,
        "q_vi": "Dùng các kỹ thuật đại số Boole, rút gọn các biểu thức sau đến mức tối đa có thể:<br>(a) A(A + B) &nbsp; (b) A(~{A} + AB) &nbsp; (c) BC + ~{B}C<br>(d) A(A + ~{A}B) &nbsp; (e) A~{B}C + ~{A}BC + ~{A}~{B}C",
        "q_en": "Using Boolean algebra techniques, simplify the following expressions as much as possible:<br>(a) A(A + B) &nbsp; (b) A(~{A} + AB) &nbsp; (c) BC + ~{B}C<br>(d) A(A + ~{A}B) &nbsp; (e) A~{B}C + ~{A}BC + ~{A}~{B}C",
        "src": "Floyd Ch.4 · Problem 19",
        "img": "essay_floyd_ch04_q19.png"
      },
      {
        "num": 21,
        "q_vi": "Dùng đại số Boole, rút gọn các biểu thức sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Using Boolean algebra, simplify the following expressions. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 21",
        "img": "essay_floyd_ch04_q21.png",
        "note_vi": "Kiểm chứng bằng sympy: (a), (c), (d), (e) khớp đáp án in. RIÊNG ý (b) KHÔNG khớp: đọc ở độ phân giải 1200 dpi, đề là B̄C̄D + (B+C+D)‾ + B̄C̄D̄E, trong đó thanh gạch dài phủ lên cả tổng (B+C+D) và không có gạch phụ nào trên D; biểu thức này rút gọn đúng thành B̄C̄, còn đáp án in là B̄C̄D + B̄C̄E. Nghi lỗi in của sách (đáp án in chỉ khớp nếu D trong tổng bị đảo, điều mà ảnh quét không cho thấy).",
        "note_en": "Verified with sympy: (a), (c), (d), (e) match the printed answer. Item (b) does NOT: read at 1200 dpi, the problem is B′C′D + (B+C+D)′ + B′C′D′E, where the long bar spans the whole sum (B+C+D) with no extra bar on D; this simplifies exactly to B′C′, while the printed answer is B′C′D + B′C′E. A likely printing error in the book (the printed answer only fits if D inside the sum were complemented, which the scan does not show).",
        "qimgs": [
          "essay_floyd_ch04_qq21.png"
        ]
      },
      {
        "num": 23,
        "q_vi": "Chuyển các biểu thức sau sang dạng tổng các tích (SOP). Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Convert the following expressions to sum-of-product (SOP) forms. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 23",
        "img": "essay_floyd_ch04_q23.png",
        "note_vi": "Đã tự kiểm chứng bằng sympy (OCR_output/Floyd/scripts/verify_ch4.py): biểu thức trong đề và kết quả in là tương đương logic.",
        "note_en": "Verified with sympy (OCR_output/Floyd/scripts/verify_ch4.py): the expression in the problem and the printed result are logically equivalent.",
        "qimgs": [
          "essay_floyd_ch04_qq23.png"
        ]
      },
      {
        "num": 31,
        "q_vi": "Lập bảng chân trị cho mỗi biểu thức SOP chuẩn sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Develop a truth table for each of the following standard SOP expressions. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 31",
        "img": "essay_floyd_ch04_q31.png",
        "note_vi": "Tự kiểm tra: (a) có giá trị 1 đúng ở các dòng 001, 110, 111; (b) có giá trị 1 ở 000, 010, 011, 101, 110; khớp Bảng P–3 và P–4 trong đáp án in.",
        "note_en": "Self-check: (a) is 1 exactly on rows 001, 110, 111; (b) is 1 on 000, 010, 011, 101, 110; matches Tables P–3 and P–4 in the printed answer.",
        "qimgs": [
          "essay_floyd_ch04_qq31.png"
        ]
      },
      {
        "num": 33,
        "q_vi": "Lập bảng chân trị cho mỗi biểu thức SOP sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Develop a truth table for each of the SOP expressions. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 33",
        "img": "essay_floyd_ch04_q33.png",
        "note_vi": "Tự kiểm tra: (a) bằng 1 ở 000, 010, 011, 101, 110; (b) bằng 0 chỉ ở 0100, 0111, 1100 (còn lại bằng 1); khớp Bảng P–5 và P–6.",
        "note_en": "Self-check: (a) is 1 on 000, 010, 011, 101, 110; (b) is 0 only on 0100, 0111, 1100 (1 elsewhere); matches Tables P–5 and P–6.",
        "qimgs": [
          "essay_floyd_ch04_qq33.png"
        ]
      },
      {
        "num": 35,
        "q_vi": "Lập bảng chân trị cho mỗi biểu thức POS chuẩn sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Develop a truth table for each of the standard POS expressions. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 35",
        "img": "essay_floyd_ch04_q35.png",
        "note_vi": "Tự kiểm tra ý (a): bằng 1 ở 011, 100, 101, 110, 111, khớp Bảng P–7. Ý (b) có bảng 16 dòng, đối chiếu bằng mắt từng dòng với Bảng P–8 trong ảnh đáp án.",
        "note_en": "Self-check for (a): 1 on 011, 100, 101, 110, 111, matching Table P–7. Item (b) has a 16-row table, compared row by row by eye against Table P–8 in the answer image.",
        "qimgs": [
          "essay_floyd_ch04_qq35.png"
        ]
      },
      {
        "num": 37,
        "q_vi": "Vẽ bản đồ Karnaugh 3 biến và ghi nhãn mỗi ô theo giá trị nhị phân của nó.",
        "q_en": "Draw a 3-variable Karnaugh map and label each cell according to its binary value.",
        "src": "Floyd Ch.4 · Problem 37",
        "img": "essay_floyd_ch04_q37.png",
        "note_vi": "Thứ tự hàng AB là 00, 01, 11, 10 (mã Gray), cột C là 0, 1; mỗi ô được ghi bằng ABC tương ứng.",
        "note_en": "Rows AB run 00, 01, 11, 10 (Gray order), columns C run 0, 1; each cell is labelled with its ABC value."
      },
      {
        "num": 39,
        "q_vi": "Viết số hạng tích chuẩn cho từng ô của bản đồ Karnaugh 3 biến.",
        "q_en": "Write the standard product term for each cell in a 3-variable Karnaugh map.",
        "src": "Floyd Ch.4 · Problem 39",
        "img": "essay_floyd_ch04_q39.png",
        "note_vi": "Ví dụ ô 000 là ĀB̄C̄, ô 101 là AB̄C; mỗi ô là một minterm với biến bằng 0 được đảo.",
        "note_en": "For example cell 000 is A′B′C′ and cell 101 is AB′C; each cell is a minterm with the 0-valued variables complemented."
      },
      {
        "num": 41,
        "q_vi": "Dùng bản đồ Karnaugh rút gọn mỗi biểu thức về dạng SOP tối thiểu. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Use a Karnaugh map to simplify each expression to a minimum SOP form. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 41",
        "img": "essay_floyd_ch04_q41.png",
        "note_vi": "Kiểm chứng: (a) bốn minterm 000, 101, 011, 110 không có hai ô kề nhau nên không rút gọn được; (b) AC[B̄ + B(B + C̄)] = AC; (c) = DF̄ + ĒF̄. Đều khớp đáp án in.",
        "note_en": "Check: (a) the four minterms 000, 101, 011, 110 have no adjacent pair, so nothing simplifies; (b) AC[B′ + B(B + C′)] = AC; (c) = DF′ + E′F′. All match the printed answer.",
        "qimgs": [
          "essay_floyd_ch04_qq41.png"
        ]
      },
      {
        "num": 45,
        "q_vi": "Dùng bản đồ Karnaugh rút gọn hàm cho bởi Bảng 4–16 về dạng SOP tối thiểu.",
        "q_en": "Reduce the function specified in truth Table 4–16 to its minimum SOP form by using a Karnaugh map.",
        "src": "Floyd Ch.4 · Problem 45",
        "img": "essay_floyd_ch04_q45.png",
        "note_vi": "Bảng 4–16 có X = 0 chỉ ở các dòng 010 và 110 (tức B = 1, C = 0), nên X = B̄ + C. Tự tính bằng sympy, khớp đáp án in.",
        "note_en": "Table 4–16 has X = 0 only on rows 010 and 110 (B = 1, C = 0), so X = B′ + C. Computed with sympy, matches the printed answer.",
        "qimgs": [
          "essay_floyd_tab4_16.png"
        ]
      },
      {
        "num": 47,
        "q_vi": "Giải Bài 46 trong trường hợp sáu tổ hợp nhị phân cuối (1010 đến 1111) không được phép xuất hiện (don't care).<br><i>Bài 46: dùng bản đồ Karnaugh để thực hiện biểu thức SOP tối thiểu cho hàm ở Bảng 4–17.</i>",
        "q_en": "Solve Problem 46 for a situation in which the last six binary combinations are not allowed.<br><i>Problem 46: Use the Karnaugh map method to implement the minimum SOP expression for the logic function specified in truth Table 4–17.</i>",
        "src": "Floyd Ch.4 · Problem 47",
        "img": "essay_floyd_ch04_q47.png",
        "note_vi": "Tự tính bằng sympy với 1010 đến 1111 là don't care: SOP tối thiểu = ĀB̄C̄D + BC + AD̄ + CD̄, khớp đáp án in.",
        "note_en": "Computed with sympy with 1010 to 1111 as don't-cares: minimum SOP = A′B′C′D + BC + AD′ + CD′, matching the printed answer.",
        "qimgs": [
          "essay_floyd_tab4_17.png"
        ]
      },
      {
        "num": 49,
        "q_vi": "Dùng bản đồ Karnaugh rút gọn mỗi biểu thức về dạng POS tối thiểu. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Use a Karnaugh map to simplify each expression to minimum POS form. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 49",
        "img": "essay_floyd_ch04_q49.png",
        "note_vi": "Tự kiểm chứng: (a) ba thừa số tổng (maxterm) không có hai thừa số kề nhau nên không rút gọn được; (b) sympy cho (W+X)(W+Z̄)(X+Ȳ)(Ȳ+Z̄), tương đương logic với đáp án in (W+X)(W+Z̄)(X+Ȳ)(W̄+X̄+Ȳ+Z̄) (cả hai đều là dạng POS của cùng một hàm).",
        "note_en": "Self-check: (a) the three maxterms have no adjacent pair so nothing reduces; (b) sympy gives (W+X)(W+Z′)(X+Y′)(Y′+Z′), logically equivalent to the printed answer (W+X)(W+Z′)(X+Y′)(W′+X′+Y′+Z′) (both are POS forms of the same function).",
        "qimgs": [
          "essay_floyd_ch04_qq49.png"
        ]
      },
      {
        "num": 51,
        "q_vi": "Xác định biểu thức POS tối thiểu cho hàm ở Bảng 4–17.",
        "q_en": "Determine the minimum POS expression for the function in Table 4–17.",
        "src": "Floyd Ch.4 · Problem 51",
        "img": "essay_floyd_ch04_q51.png",
        "note_vi": "Tự tính bằng sympy (POSform trên các dòng có X = 0): kết quả có đúng 5 thừa số tổng giống đáp án in.",
        "note_en": "Computed with sympy (POSform over the rows where X = 0): the result has exactly the same 5 sum factors as the printed answer.",
        "qimgs": [
          "essay_floyd_tab4_17.png"
        ]
      },
      {
        "num": 53,
        "q_vi": "Liệt kê các minterm của biểu thức sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "List the minterms in the expression. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 53",
        "img": "essay_floyd_ch04_q53.png",
        "note_vi": "Tự tính: các số hạng tương ứng 111, 001, 110, 101, 011 nên các minterm là 1, 3, 5, 6, 7, khớp đáp án in.",
        "note_en": "Own calculation: the terms are 111, 001, 110, 101, 011, so the minterms are 1, 3, 5, 6, 7, matching the printed answer.",
        "qimgs": [
          "essay_floyd_ch04_qq53.png"
        ]
      },
      {
        "num": 61,
        "q_vi": "Viết chương trình VHDL cho biểu thức sau. Đề gốc (có gạch trên đúng như sách) nằm trong ảnh bên dưới.",
        "q_en": "Write a program in VHDL for the expression. The original problem (with overlines exactly as in the book) is shown in the image below.",
        "src": "Floyd Ch.4 · Problem 61",
        "img": "essay_floyd_ch04_q61.png",
        "note_vi": "Phần logic Y <= (A and not B and C) or ... khớp biểu thức đề. Lưu ý lỗi nhỏ trong đáp án in: cổng ra được khai báo là X (X: out bit) nhưng phép gán dùng Y, nên chương trình in không biên dịch được nếu giữ nguyên.",
        "note_en": "The logic Y <= (A and not B and C) or ... matches the problem's expression. Note a small error in the printed answer: the output port is declared as X (X: out bit) but the assignment uses Y, so the printed program would not compile as written.",
        "qimgs": [
          "essay_floyd_ch04_qq61.png"
        ]
      }
    ],
    "note_vi": "Chương 3 có 55 bài; chỉ các bài SỐ LẺ có đáp án in. Đã đưa lên các bài dạng sóng và ký hiệu (1 đến 27), bài mạng lập trình/VHDL/tham số (29 đến 37), bài tìm cổng hỏng và thiết kế (39 đến 51), mỗi bài kèm ảnh đề và ảnh đáp án thật. Chương 4 (72 bài): đã đưa các bài 1, 5, 7, 9, 13, 19 đến 23, 31 đến 41, 45 đến 53, 61, kèm ảnh đề gốc (giữ nguyên gạch trên của sách) và ảnh đáp án thật. Chưa đưa các bài 3, 11, 15, 17, 25 đến 29, 43, 55 đến 59 vì: bài 3 và bài 15 có đáp án in KHÔNG khớp đề (bài 3 hỏi 3 biến A, B, C nhưng đáp án là ABCD; bài 15 đề là AB+(AB)‾, ABCD, A+BC, ABC+D còn hình đáp án vẽ các mạch khác hẳn), bài 11 có gạch trên lồng nhiều tầng không đọc chắc được, các bài 17, 25 đến 29, 43, 55 đến 59 phụ thuộc đọc mạch hoặc các bài trước mà chưa tự kiểm chứng độc lập được. Với Chương 3, chưa đưa: bài 41 (đọc sơ đồ chân IC trên bo mạch, chưa tự kiểm chứng độc lập được), bài 49 (phụ thuộc bài 48 và Hình 3–25), bài 53, 55 (cần file Multisim không có trong sách). Bài chẵn không có đáp án in nên không đưa.",
    "note_en": "Chapter 3 has 55 problems; only the ODD-numbered ones have printed answers. Added here: waveform and symbol problems (1 to 27), programmable-array/VHDL/parameter problems (29 to 37), faulty-gate and design problems (39 to 51), each with the question figure and the real answer image. Chapter 4 (72 problems): included are 1, 5, 7, 9, 13, 19 to 23, 31 to 41, 45 to 53 and 61, with the original question image (book overlines preserved) and the real answer image. Not included: 3, 11, 15, 17, 25 to 29, 43, 55 to 59, because problems 3 and 15 have printed answers that do NOT match the question (3 asks about 3 variables A, B, C but the answer is ABCD; 15 asks for AB+(AB)′, ABCD, A+BC, ABC+D but the answer figure draws entirely different circuits), problem 11 has multi-level overlines that cannot be read reliably, and 17, 25 to 29, 43, 55 to 59 depend on reading circuits or earlier problems that could not be independently verified. For Chapter 3, not included: problem 41 (reading IC pin diagrams on a board, could not be independently verified), problem 49 (depends on problem 48 and Figure 3–25), problems 53 and 55 (need Multisim files not in the book). Even-numbered problems have no printed answer and are omitted."
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
        "img": "essay_floyd_ch06_q01.png"
      },
      {
        "num": 3,
        "q_vi": "Xác định đầu ra của một mạch cộng đầy đủ (full-adder) ứng với mỗi bộ giá trị đầu vào sau:<br>(a) A = 1, B = 0, Cin = 0 &nbsp; (b) A = 0, B = 0, Cin = 1<br>(c) A = 0, B = 1, Cin = 1 &nbsp; (d) A = 1, B = 1, Cin = 1",
        "q_en": "Determine the outputs of a full-adder for each of the following inputs:<br>(a) A = 1, B = 0, Cin = 0 &nbsp; (b) A = 0, B = 0, Cin = 1<br>(c) A = 0, B = 1, Cin = 1 &nbsp; (d) A = 1, B = 1, Cin = 1",
        "src": "Floyd Ch.6 · Problem 3",
        "img": "essay_floyd_ch06_q03.png"
      },
      {
        "num": 15,
        "q_vi": "Với mỗi cặp số nhị phân sau, xác định trạng thái đầu ra của bộ so sánh (comparator):<br>(a) A3A2A1A0 = 1010, B3B2B1B0 = 1101<br>(b) A3A2A1A0 = 1101, B3B2B1B0 = 1101<br>(c) A3A2A1A0 = 1001, B3B2B1B0 = 1000",
        "q_en": "For each set of binary numbers, determine the output states for the comparator:<br>(a) A3A2A1A0 = 1010, B3B2B1B0 = 1101<br>(b) A3A2A1A0 = 1101, B3B2B1B0 = 1101<br>(c) A3A2A1A0 = 1001, B3B2B1B0 = 1000",
        "src": "Floyd Ch.6 · Problem 15",
        "img": "essay_floyd_ch06_q15.png"
      }
    ]
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
        "img": "essay_floyd_ch11_q03.png"
      },
      {
        "num": 5,
        "q_vi": "Một mảng bộ nhớ tĩnh 4 hàng, giống mảng ở Hình 11–10 của sách, ban đầu lưu toàn số 0. Nội dung của nó là gì sau các điều kiện sau? Giả sử giá trị 1 chọn hàng đó.<br>Row 0 = 1, Data in (Bit 0) = 1<br>Row 1 = 0, Data in (Bit 1) = 1<br>Row 2 = 1, Data in (Bit 2) = 0<br>Row 3 = 0, Data in (Bit 3) = 1",
        "q_en": "A static memory array with four rows similar to the one in Figure 11–10 is initially storing all 0s. What is its content after the following conditions? Assume a 1 selects a row.<br>Row 0 = 1, Data in (Bit 0) = 1<br>Row 1 = 0, Data in (Bit 1) = 1<br>Row 2 = 1, Data in (Bit 2) = 0<br>Row 3 = 0, Data in (Bit 3) = 1",
        "src": "Floyd Ch.11 · Problem 5",
        "img": "essay_floyd_ch11_q05.png"
      },
      {
        "num": 9,
        "q_vi": "Bộ nhớ đệm (cache memory) là gì?",
        "q_en": "What is cache memory?",
        "src": "Floyd Ch.11 · Problem 9",
        "img": "essay_floyd_ch11_q09.png"
      },
      {
        "num": 21,
        "q_vi": "Xét một RAM 4096 × 8, trong đó 64 địa chỉ cuối cùng được dùng làm ngăn xếp LIFO. Nếu địa chỉ đầu tiên của RAM là 000<sub>16</sub>, hãy xác định 64 địa chỉ dùng cho ngăn xếp.",
        "q_en": "Consider a 4096 × 8 RAM in which the last 64 addresses are used as a LIFO stack. If the first address in the RAM is 000<sub>16</sub>, designate the 64 addresses used for the stack.",
        "src": "Floyd Ch.11 · Problem 21",
        "img": "essay_floyd_ch11_q21.png"
      },
      {
        "num": 25,
        "q_vi": "Các thông số nào được dùng để đo hiệu năng của ổ đĩa cứng (hard disk)?",
        "q_en": "What are the parameters used to measure the performance of a hard disk?",
        "src": "Floyd Ch.11 · Problem 25",
        "img": "essay_floyd_ch11_q25.png"
      },
      {
        "num": 27,
        "q_vi": "Sự khác biệt chính giữa đĩa CD và đĩa DVD là gì?",
        "q_en": "What is the main difference between a CD and a DVD?",
        "src": "Floyd Ch.11 · Problem 27",
        "img": "essay_floyd_ch11_q27.png"
      }
    ]
  }
}
