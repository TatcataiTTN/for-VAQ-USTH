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
- [x] Mở rộng slide-deck theo yêu cầu người dùng: module có nội dung TRÙNG giữa Tooley và Floyd (01, 02,
  03) → 60 slide/trang; module 04 (khớp yếu, chỉ dựa chính vào Tooley) → 40 slide/trang. Nội dung slide
  mở rộng nằm ở `data/slides_0N.py` (song ngữ, mỗi phần 10 slide cho module 60-slide hoặc 6 slide cho
  module 40-slide), `render_site.py` tự động ghép vào và tự in cảnh báo nếu số slide sinh ra lệch target.

## Epic 4 — Câu hỏi trắc nghiệm 🟢 (mở rộng 2026-09-28)
- [x] **Tooley**: 62 câu MCQ cuối chương (ch.2,5,6,7,8,9) — loại các câu phụ thuộc hình vẽ gốc không hiển
  thị lại được từ OCR. Mỗi câu tự tính lại độc lập để xác minh (Appendix 3 gốc bị OCR hỏng không đọc được).
- [x] **Floyd** (MỚI): trích đủ **139 câu** (56 True/False + 83 Self-Test, 4 lựa chọn) từ cuối các chương
  2,3,4,6,11 — dùng trực tiếp `pdftotext` trên PDF text-layer thật (không OCR, độ chính xác cao) và cắt
  đúng theo mốc trang in sẵn trong tên file nhúng (`M0N_..._C0N.indd Page NNN`). Nguồn trong
  `data/floyd_quiz_source.py`.
- [x] **Kiểm chứng tự động 100%**: viết script đối chiếu TỪNG câu Floyd với đúng thứ tự đáp án in sẵn ở
  cuối mỗi chương ("True/False Quiz"/"Self-Test" answer key) — phát hiện và sửa **11 lỗi thật** (gõ sai
  index đáp án khi soạn tay), bao gồm 1 bẫy từ vựng có chủ đích của sách (VHDL "definition" vs
  "description" language) và 2 câu có lỗi trích xuất dấu trừ (`+122`/`-34` bị đọc thành `1122`/`234`) đã
  xác nhận lại bằng cách đọc ẢNH GỐC trang 118 (Read tool, không đoán). Sau sửa: **0 sai lệch** trên 139/139
  câu.
- [x] 42 câu luyện tập bổ sung do AI biên soạn cùng dạng, đáp án tự kiểm chứng bằng tính toán.
- [x] Trang mỗi module giờ có **3 mục quiz tách riêng theo đúng yêu cầu người dùng**: "Sách 1 — Tooley",
  "Sách 2 — Floyd", "Câu luyện tập bổ sung" — không gộp lẫn nguồn.
- [x] Audit position-bias bằng script `data/build_quiz.py` (seed cố định 2026/2027/2028) cho cả 3 nguồn.
- ⚠️ Length-bias KHÔNG đạt ngưỡng <5% chuẩn của skill cho các câu số học/kỹ thuật — quyết định có chủ đích:
  độ dài đáp án phản ánh ĐÚNG số chữ số/bit của giá trị đúng, không phải văn phong dài dòng — không thể
  "đệm chữ" vào một chuỗi nhị phân/hex mà không làm sai nội dung.
- **Tổng số câu hỏi trên toàn site: 241** (13+32+10=55 ở M01, 6+59+10=75 ở M02, 16+22+10=48 ở M03,
  25+26+12=63 ở M04) — tăng từ 104 câu ở phiên bản trước.
- **CÒN THIẾU (chưa làm, không giấu)**: câu hỏi dạng hình vẽ trong Tooley (~28 câu, cần xem hình gốc để trả
  lời chính xác), Tooley Appendix 2 "Revision papers" (bài ôn tập tổng hợp nhiều chương), và phần "Problems"
  (bài tập tự luận, không phải MCQ) của Floyd cho mỗi chương — đây là khối lượng rất lớn (hàng trăm bài tự
  luận cần lời giải từng bước), chưa đưa vào site.

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
