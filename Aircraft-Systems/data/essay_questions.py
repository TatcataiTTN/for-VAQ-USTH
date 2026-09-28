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
        "q_en": "Express each decimal number as an 8-bit number in the 2's complement form:<br>(a) +12 &nbsp; (b) -68 &nbsp; (c) +101 &nbsp; (d) -125",
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
}
