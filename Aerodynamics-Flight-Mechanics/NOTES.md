# AE2.008 Aerodynamics and Flight Mechanics: ghi chú xây dựng

Trạng thái: 3 module đầu (EASA Module 08 sub-module 01 đến 03). Sub-module 04 (Flight Stability and Dynamics, ánh xạ Etkin ch.2 đến 8) chưa làm.

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

## Phát hiện về nguồn
- EASA cuối sub-module chỉ có câu điền khuyết: 3 + 8 + 8 = 19 câu cho sub-module 01 đến 03, không có trắc nghiệm. Đáp án in ở trang 1.8, 2.20, 3.20 (đọc từ ảnh trang). Site chuyển sang trắc nghiệm, giữ đáp án in.
- Solution Manual của Anderson là bản 4th (Fourth Edition), trong khi giáo trình là bản 6th. Bài 1.1, 1.11, 1.12 có số liệu trùng.
- Solution Manual bài 1.12 in L = 3487 N ở dòng giữa nhưng dòng sau dùng 3847 N; đáp án cuối 1,67×10^5 N đúng.
- Bài tập cuối chương Etkin ch.2 và ch.3 là bài ổn định (cần hình và dữ liệu máy bay), thuộc sub-module 04, nên chưa đưa vào.
- OCR: EASA, hai Solution Manual là ảnh scan; chữ viết tay của Solution Manual có công thức OCR sai nhiều, vì vậy đáp án trên site không lấy từ OCR mà tính lại bằng Python.
- Bài ch.3, 4, 5, 8, 11 của Anderson chưa đối chiếu với Solution Manual (chỉ ch.1 đã đối chiếu từ ảnh trang).
