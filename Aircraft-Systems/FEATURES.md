# FEATURES — AE2.021 Aircraft-Systems

Cập nhật 21/11/2026. Trạng thái: LÀM (sẽ dựng), CHỈNH (dựng có thay đổi), BỎ (kèm lý do). Cột "Hiện có" đo trên bản làm việc `$W/Aircraft-Systems/`.
Bằng chứng khảo sát: đã ĐỌC mã engine của Thermal-Systems (`_shared/*.js`, `build/*.py`, `AGENT_BRIEF.md`). CHƯA mở bằng trình duyệt các site mẫu for-USTH/Calculus-1, for-PTIT/Discrete-Math, Electronics-2 (việc của P0b, còn LÀM). Không sao chép nội dung hay đề của site mẫu.

| ID | Tính năng (nhãn UI VI / EN) | Quyết định | Hiện có | Phụ thuộc, test |
|---|---|---|---|---|
| F01 | Trang chủ: ma trận CO/CLO × module × slide × sách, Tiến độ của bạn, Tiếp tục học | LÀM | có ma trận, tiến độ, tiếp tục | `tests/site_test.py` (tiến độ) |
| F02 | Slide của giảng viên: 342 slide, ảnh bấm phóng to, dải ảnh theo module | LÀM | có 342 ảnh (`assets/slides/`, 23 MB) và thư viện `slides/index.html`; bản chép VI/EN từng slide: 342/342 (211 chi tiết, 131 slide basis=summary chưa phóng to kiểm lại) | P0 đọc từng slide (xong phần đọc; còn kiểm lại 131 slide tóm tắt) |
| F03 | Module (9 có, 6 thêm theo 4b) | CHỈNH | 9 module chuyển bằng `build/legacy.py`; m10 đến m15 là "sắp có" | P4 |
| F04 | Quiz nhanh trong trang module (10 câu, ưu tiên câu gốc) | LÀM | có | `site_test.py` |
| F05 | Ngân hàng câu hỏi theo module (lọc nguồn/mức/chủ đề, lời giải chi tiết) | LÀM | có, 605 câu trắc nghiệm + 129 tự luận (sau khi gộp câu trùng) | `site_test.py` |
| F06 | Luyện đề: Midterm, Final, Speed, Custom, đề hỗn hợp, in A4 (thiết kế của site, ghi rõ) | LÀM | có, đề A/B/C không trùng câu | `site_test.py` |
| F07 | Viết tay (tự luận) | LÀM | CHƯA (tự luận hiện nằm trong ngân hàng, tab Tự luận) | cần bài đã giải |
| F08 | Phân tích đề | LÀM | CHƯA | cần `topic` (đã gán bằng quy tắc, chưa rà) |
| F09 | Khái niệm (Concept finder) | LÀM | CHƯA | cần `topic` |
| F10 | Lab | BỎ | người dùng chọn "chỉ làm đề, bỏ Lab" (4d, 21/11/2026) | 3 demo giữ trong m07 đến m09 |
| F11 | Bài tập có đáp án (Exercise finder) | LÀM | CHƯA | P5 |
| F12 | Bản đồ sách | CHỈNH | có cấp chương: Tooley 20 chương, Floyd 15 chương, trang in đã đo | cấp mục ở P2 |
| F13 | Nguồn, độ phủ, lỗi của nguồn | LÀM | có bản đầu (tài liệu, độ phủ đếm từ dữ liệu, lỗi gom từ module) | P0 |
| F14 | Bảng tra mã (Tooley App.5), Luyện đổi mã | CHỈNH | CHƯA | số hoá bằng script, so ảnh |
| F15 | Thuật ngữ VI–EN | LÀM | có: 130 thuật ngữ, lọc không dấu (chưa gắn số slide) | `tests/site_test.py` |
| F16 | Tóm tắt công thức | LÀM | có: 32 công thức KaTeX theo module (chưa gắn số slide) | `tests/site_test.py` |
| F17 | Kiểm tra đầu vào | LÀM | CHƯA | cần câu nền (Floyd Ch.1 đến 2, AE2.025) |
| F18 | Sổ lỗi | LÀM | CHƯA | dùng tiến độ trong localStorage |
| F19 | Cấu trúc đề | LÀM | có (khung giải thích trong trang Luyện đề) | |
| F20 | Python judge | BỎ | đề cương không có mục tiêu lập trình | |
| F21 | Mô phỏng mạch logic và bus | BỎ | thuộc Lab (4d). Ba demo (checksum/CRC, cáp quang, EMC) giữ trong module | |
| F22 | Notebook | CHỈNH | 9 file, VI+EN chung, chạy sẵn; CHƯA tách cặp | P4 |
| F23 | Giao diện | CHỈNH | có Sáng, Tối, Sepia, Ocean và 3 cỡ chữ | |

Lưu ý khoá lưu trữ: mọi khoá tiến độ có tiền tố `ae2021:` (xem `build/NAMESPACE.md`); Thermal-Systems dùng khoá không có tiền tố môn trên cùng origin, nên tiến độ giữa các môn có thể lẫn (chưa sửa, ngoài phạm vi thư mục này).
