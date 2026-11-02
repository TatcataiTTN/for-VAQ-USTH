# AE2.008 Aerodynamics and Flight Mechanics: ghi chú xây dựng

Trạng thái: 10 module (thêm 09 dòng thế cơ bản, Anderson ch.3; 10 cận âm nén được, Anderson ch.11). 01–04 tương ứng 4 sub-module EASA Module 08; 05 (cánh hữu hạn, Anderson ch.5), 06 (dòng nén được, ch.7–8), 07 (sóng xiên, ch.9), 08 (động lực ngang B747, Etkin 6.7) mở rộng ngoài EASA. Mỗi module có slide song ngữ kèm hình gốc EASA cắt từ scan, demo tương tác, quiz (EASA, sách, bổ sung), bài tập có lời giải và notebook chạy được. Chưa làm: Anderson ch.2, 6, 10–15 (phương trình cơ bản, dòng 3D, ống phun, lý thuyết tuyến tính, CFD, lớp biên) và Etkin ch.4, 5, 7, 8 (phương trình chuyển động, đạo hàm ổn định, đáp ứng, điều khiển vòng kín). Bài 5.x, 8.x, 9.x của Anderson chưa đối chiếu với Solution Manual.

## Cách dựng lại
```
cd data
python3 -I render.py            # sinh vi/, en/, chapter-mapping-*.html và data/quiz/*.json
python3 -I audit_quiz.py        # audit vị trí và độ dài đáp án
python3 -I build_notebooks.py   # sinh notebook; chạy bằng: jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```
Mọi số trên trang chạy ra từ `data/aero.py`; notebook cài lại độc lập (không import aero.py) và `assert` cùng các giá trị.

## Ánh xạ (đề cương docx không có bảng chương; thứ tự theo EASA Module 08)
Xem `chapter-mapping-vi.html`.

## Kiểm chứng
- `_shared/demo_aero.js`: hàm thuần đã kiểm bằng Node so với aero.py (ISA, sóng xung kích) và so với ma trận mũ của numpy (mô phỏng RK4 của B747 khớp tới 8 chữ số tại t = 20 s và 300 s).
- Module 04: ma trận A của B747 chép từ ảnh trang Etkin tr. 166; trị riêng và hệ số đa thức đặc trưng tính lại khớp số in trong sách.
- 103 câu quiz; audit: chi² vị trí đáp án 0,5, đáp án đúng là câu dài nhất ở 27%.

## Phát hiện về nguồn
- EASA cuối sub-module chỉ có câu điền khuyết: 3 + 8 + 8 = 19 câu cho sub-module 01 đến 03, không có trắc nghiệm. Đáp án in ở trang 1.8, 2.20, 3.20 (đọc từ ảnh trang). Site chuyển sang trắc nghiệm, giữ đáp án in.
- Solution Manual của Anderson là bản 4th (Fourth Edition), trong khi giáo trình là bản 6th. Bài 1.1, 1.11, 1.12 có số liệu trùng.
- Solution Manual bài 1.12 in L = 3487 N ở dòng giữa nhưng dòng sau dùng 3847 N; đáp án cuối 1,67×10^5 N đúng.
- Bài tập cuối chương Etkin ch.2 và ch.3 là bài ổn định (cần hình và dữ liệu máy bay), thuộc sub-module 04, nên chưa đưa vào.
- OCR: EASA, hai Solution Manual là ảnh scan; chữ viết tay của Solution Manual có công thức OCR sai nhiều, vì vậy đáp án trên site không lấy từ OCR mà tính lại bằng Python.
- Bài ch.3, 4, 5, 8, 11 của Anderson chưa đối chiếu với Solution Manual (chỉ ch.1 đã đối chiếu từ ảnh trang).
- EASA Sub-module 04: câu hỏi in đánh số 4-1, 4-2, 4-5, 4-6 nhưng đáp án in đánh số 4-1 đến 4-4; site ghép theo nội dung.
- Hình trên slide là các hình EASA cắt từ bản scan (không dùng cả trang) kèm số trang gốc.

## Đối chiếu Solution Manual của Anderson (bản 4th, đọc từ ảnh trang)
Khớp: 1.1, 1.11, 1.12 · 3.3, 3.4, 3.6, 3.7, 3.18 · 4.2, 4.5 · 7.1, 7.4, 7.5 · 8.1, 8.3, 8.5, 8.7, 8.8, 8.9, 8.10, 8.11, 8.13, 8.16 · 9.1, 9.2, 9.4, 9.6, 9.8, 9.13 (5°, 15°).
Khác biệt đã xử lý:
- 4.1: SM dùng c_l = 0,64, c_m = −0,036 (L' = 3,80 lb/ft, M' = −0,428); notebook 02 đã sửa theo đó.
- 1.12: SM ghi nhầm L = 3487 N ở dòng giữa (đúng 3847 N), đáp án cuối vẫn đúng.
- 9.5: bản 4th dùng nêm 22,5°, bản 6th dùng 22,2°; site theo bản 6th (β = 45,89°, p₂ = 3,592 atm).
- 9.13 ở α = 30°: SM ghi c_l = 1,19 và c_d,w = 0,687 vì bỏ cos α; đúng là 1,02 và 0,59.
- 9.8: SM đọc đồ thị nên lệch dưới 1% so với tính trực tiếp.
Không đối chiếu được: ch.5 (SM không có), 4.10–4.12, 5.4, 5.5, 9.15, 9.20, 11.4 (đánh số khác giữa các bản); các bài này kiểm bằng hai đường tính độc lập (công thức và nghiệm số, notebook).
## Kiểm tra tự động
`audit_quiz.py` kiểm: cân bằng vị trí đáp án, đáp án đúng không luôn dài nhất, không có hai phương án trùng nhau, mọi câu có giải thích. Lần kiểm này bắt được 2 câu có phương án trùng (Bài 5.4 và một câu ζ) và đã sửa.

## Bổ sung đối chiếu Solution Manual (lần 2)
Khớp thêm: 3.15, 3.16, 3.17, 3.19, 3.20 · 11.1, 11.2 (SM dùng c_l,0 = 0,75 đọc từ Hình 4.5), 11.3, 11.4, 11.5, 11.6, 11.7 (lệch nhỏ vì SM nội suy bảng). 3.21 và 3.22 không có trong SM bản 4th.
Lời giải bốn bước (Đề nói gì / Ý tưởng / Các bước / Kiểm tra): module 09, 10 và các bài chính của module 01, 02, 03. Các module 04–08 vẫn dùng lời giải ngắn hơn.
