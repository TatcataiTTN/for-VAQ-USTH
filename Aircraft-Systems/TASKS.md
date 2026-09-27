# TASKS — AE2.021 Aircraft Digital Electronics & Computer Systems

Ngày khởi tạo: 2026-09-28.

## Epic 1 — Hạ tầng site 🟢
- [x] Cấu trúc thư mục `vi/ en/ _shared/ data/` theo chuẩn skill `build-complete-self-study-system`.
- [x] `.nojekyll` ở gốc repo (tránh Jekyll bỏ qua `_shared/`).
- [x] `_shared/common.css`, `deck.css`, `deck.js`, `quiz.js`, `theme.js` dùng chung VI/EN.
- [x] Trang chủ mỗi ngôn ngữ dạng card, trang `chapter-mapping-{vi,en}.html`.

## Epic 2 — Ánh xạ chương sách 🟢
- [x] Đọc mục lục đầy đủ của Tooley (20 chương) và Floyd (15 chương) từ bản OCR/text-layer thật.
- [x] Đối chiếu 4 bộ slide gốc với đúng chương nguồn — xem `chapter-mapping-vi.html`.
- ⚠️ Module 04 có độ khớp yếu với Floyd (Floyd không có chương CPU/kiến trúc máy tính) — đã ghi rõ trong
  bảng ánh xạ, không che giấu.

## Epic 3 — Nội dung 4 module (VI+EN) 🟢
- [x] 01 Number Systems, 02 Logic & Boolean, 03 IC & Multiplexing, 04 Computers & CPU.
- [x] Mỗi module: mini slide-deck 5 phần, công thức đóng khung, hộp lịch sử, case study A320/AIMS thật
  (trích từ nội dung sách/slide đã đọc, không bịa), cảnh báo bẫy, quiz.

## Epic 4 — Câu hỏi trắc nghiệm 🟢
- [x] Trích 62 câu MCQ gốc từ Tooley (ch.2, ch.5, ch.6, ch.7, ch.8, ch.9) — loại bỏ các câu phụ thuộc hình
  vẽ gốc (không thể hiển thị lại chính xác từ OCR).
- [x] Mỗi câu được **tính toán lại độc lập** để xác minh đáp án (không đọc Appendix 3 vì trang đó OCR bị
  lỗi/không đọc rõ được — xem ghi chú trong `data/build_quiz.py`).
- [x] 42 câu luyện tập bổ sung do AI biên soạn cùng dạng, đáp án tự kiểm chứng bằng tính toán.
- [x] Audit position-bias bằng script `data/build_quiz.py` (seed cố định 2026/2027) — vị trí đáp án đúng
  rải tương đối đều qua 3 vị trí.
- ⚠️ Length-bias KHÔNG đạt ngưỡng <5% chuẩn của skill — đây là quyết định có chủ đích: các câu hỏi trong
  module này chủ yếu là chuyển đổi số/tính toán kỹ thuật, độ dài đáp án phản ánh ĐÚNG số chữ số/bit của
  giá trị đúng (không phải "văn phong dài dòng" như quiz trắc nghiệm khái niệm) — không thể "đệm chữ" vào
  một chuỗi nhị phân/hex mà không làm sai nội dung. Xem ghi chú đầy đủ trong báo cáo bàn giao.

## Epic 5 — Notebook Python 🟢
- [x] 4 notebook (`data/notebooks/0N_*.ipynb`), mỗi notebook tự kiểm tra lại các câu hỏi gốc bằng code.
- [x] Đã chạy `jupyter nbconvert --execute` thành công cho cả 4 file, không lỗi.

## Epic 6 — Đa ngôn ngữ 🟢
- [x] VI và EN đầy đủ cho cả 4 module + trang chủ + trang ánh xạ.
- ⚠️ Notebook chỉ có 1 bản (song ngữ VI+EN trộn trong cùng file markdown), CHƯA tách 2 file riêng theo
  đúng quy ước `0N_ten[_en].ipynb` của skill — ghi nhận là việc CÒN THIẾU, không phải đã làm xong.

## Epic 7 — Deploy & kiểm thử 🟢
- [x] Serve-test cục bộ: 23/23 file mới trả HTTP 200.
- [x] Parse-check HTML: 0 lỗi cấu trúc trên 12 file HTML mới.
- [ ] Xác nhận URL production (`gh api .../pages/builds/latest`, `curl` domain thật) — làm ngay sau khi
  push, xem log trong báo cáo bàn giao.

## Còn thiếu / việc tiếp theo (không im lặng bỏ sót)
- Sơ đồ drawio minh hoạ (mux, decoder, kiến trúc CPU) — CHƯA làm, module hiện chỉ dùng chữ + bảng.
- Data explorer tương tác — không áp dụng cho môn này (không có bộ dữ liệu dạng bản ghi từng cá thể).
- Bản dịch tiếng Trung (zh) — KHÔNG nằm trong yêu cầu ban đầu, không làm.
- Notebook riêng theo từng ngôn ngữ — chưa tách, xem Epic 6.
