# AE2.008 Aerodynamics and Flight Mechanics: ghi chú xây dựng

Trạng thái: 8 module. 01–04 tương ứng 4 sub-module EASA Module 08; 05 (cánh hữu hạn, Anderson ch.5), 06 (dòng nén được, ch.7–8), 07 (sóng xiên, ch.9), 08 (động lực ngang B747, Etkin 6.7) mở rộng ngoài EASA. Mỗi module có slide song ngữ kèm hình gốc EASA cắt từ scan, demo tương tác, quiz (EASA, sách, bổ sung), bài tập có lời giải và notebook chạy được. Chưa làm: Anderson ch.2, 6, 10–15 (phương trình cơ bản, dòng 3D, ống phun, lý thuyết tuyến tính, CFD, lớp biên) và Etkin ch.4, 5, 7, 8 (phương trình chuyển động, đạo hàm ổn định, đáp ứng, điều khiển vòng kín). Bài 5.x, 8.x, 9.x của Anderson chưa đối chiếu với Solution Manual.

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
