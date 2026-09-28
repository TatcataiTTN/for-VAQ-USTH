# TASKS — AE2.021 Aircraft Digital Electronics & Computer Systems

Ngày khởi tạo: 2026-09-28.

## Epic 10 — Theme màu, giải thích chi tiết ẩn, chuẩn văn phong 🟢 (2026-09-28)
- [x] **Theme mặc định đổi thành SÁNG (light) thật sự**, không còn tự động chuyển tối theo hệ điều hành
  (`prefers-color-scheme`) như trước, vốn là nguyên nhân site "tự nhiên hoá tối" gây khó chịu.
- [x] Thêm 2 theme mới ngoài Light/Dark: **Sepia** (nền giấy cũ, đỡ mỏi mắt khi đọc lâu) và **Ocean**
  (xanh lam tương phản cao, hợp trình chiếu). Sửa luôn 1 bug thật trong `theme.js`: nút Sepia/Ocean
  trước đó bấm vào sẽ bị coi là giá trị lạ và tự động revert về Light do logic `if/else` chỉ nhận
  đúng 2 chuỗi 'light'/'dark'.
- [x] **Thêm cơ chế "giải thích chi tiết ẩn bên dưới"** cho quiz: sau khi trả lời, ngoài dòng giải
  thích ngắn hiện ngay (`explain`), có thêm nút `<details>` "Xem giải thích đầy đủ" mở ra đoạn giải
  thích dài hơn (`detail`), viết theo văn phong dễ hiểu, có ví dụ/mẹo/liên hệ ứng dụng thực tế.
- [x] Đã viết `detail` (song ngữ) cho **toàn bộ 62 câu MCQ gốc trích trực tiếp từ Tooley** (Ch.2: 13,
  Ch.5: 10, Ch.8+9: 16, Ch.6+7: 25) — đây là bộ câu hỏi nền tảng nhất của site. Mỗi giải thích chi
  tiết đi từ cách làm tổng quát, mẹo kiểm tra nhanh, tới liên hệ ứng dụng thực tế trên avionics khi
  phù hợp, không chỉ lặp lại phép tính đã có ở `explain`.
- [x] Đã viết `detail` (song ngữ) cho **toàn bộ 139 câu trích từ Floyd** (True/False + Self-Test trên
  cả 4 module: Ch.2 32 câu, Ch.3+4 59 câu, Ch.6 22 câu, Ch.11 26 câu). Xác nhận bằng đếm trực tiếp
  trong `floyd_quiz_source.py`: 139 `explain=` khớp đúng 139 `detail=` và 139 `detail_en=`, biên dịch
  sạch, và kiểm tra chéo qua JSON đã build (`data/quiz/*.json`): mục `floyd` có 278 item (139 câu × 2
  ngôn ngữ), cả 278 đều có trường `detail`. Đã chạy lại `build_quiz.py` (audit vị trí đáp án vẫn trong
  ngưỡng an toàn, không lệch cực đoan) → `render_site.py` → `check_links.py` (110 link nội bộ, không
  lỗi) → parse-check HTML (13 file, 0 lỗi) → serve-test cục bộ xác nhận nội dung mới hiển thị đúng.
- ⚠️ **CHƯA làm**: `detail` cho 61 câu Revision Paper (Tooley) và 42 câu tự sinh (`explain` ngắn hiện
  có vẫn đầy đủ và chính xác, chỉ chưa có bản mở rộng). Đây là việc tiếp theo hợp lý nếu muốn phủ kín
  toàn bộ ngân hàng câu hỏi.
- [x] **Quét và sửa toàn bộ 336 lần dùng dấu em-dash "—"** trên mọi file mã nguồn (`.py`, `.js`,
  `.html`, `.ipynb`) theo đúng yêu cầu của skill `viet-academic-writing`/`en-academic-writing` (cấm
  tuyệt đối em-dash/en-dash). Thay bằng dấu hai chấm, dấu phẩy, hoặc viết lại câu tuỳ ngữ cảnh; đã
  soát tay và sửa riêng 5 chỗ máy móc thay bằng dấu hai chấm tạo ra câu có 2 dấu ":" gây khó đọc
  (ví dụ phần mở đầu module 02 và module 04, tiêu đề trang chủ). Xác nhận lại bằng grep trên toàn bộ
  repo: 0 em-dash còn sót, 4 notebook chạy lại `nbconvert --execute` vẫn 0 lỗi sau khi sửa.
- **CÒN THIẾU**: chưa áp dụng đầy đủ checklist còn lại của 2 skill viết học thuật (kiểm tra từng câu
  có nghe như văn mẫu AI không, đa dạng độ dài câu...) trên toàn bộ ~40 slide/module đã viết trước đó
  — mới sửa lỗi em-dash là lỗi rõ ràng nhất, chưa đọc lại toàn văn để tinh chỉnh văn phong sâu hơn.

## Epic 1 — Hạ tầng site 🟢
- [x] Cấu trúc thư mục `vi/ en/ _shared/ data/` theo chuẩn skill `build-complete-self-study-system`.
- [x] `.nojekyll` ở gốc repo (tránh Jekyll bỏ qua `_shared/`).
- [x] `_shared/common.css`, `deck.css`, `deck.js`, `quiz.js`, `theme.js` dùng chung VI/EN.
- [x] Trang chủ mỗi ngôn ngữ dạng card, trang `chapter-mapping-{vi,en}.html`.

## Epic 2 — Ánh xạ chương sách 🟢
- [x] Đọc mục lục đầy đủ của Tooley (20 chương) và Floyd (15 chương) từ bản OCR/text-layer thật.
- [x] Đối chiếu 4 bộ slide gốc với đúng chương nguồn — xem `chapter-mapping-vi.html`.
- [x] Gộp trực tiếp dòng ánh xạ (Tooley + Floyd + ghi chú) vào đầu MỖI trang module (callout "info"), không
  chỉ để ở trang riêng — người học thấy ngay ngữ cảnh mà không cần rời trang.
- ⚠️ Module 04 có độ khớp yếu với Floyd (Floyd không có chương CPU/kiến trúc máy tính) — đã ghi rõ trong
  bảng ánh xạ, không che giấu.

## Epic 8 — Tooley Appendix 2 "Revision Papers" 🟢 (mới 2026-09-28)
- [x] Đọc bằng mắt (Read tool, không OCR) toàn bộ 8 Revision Paper (160 câu, PDF trang 363-389), lọc ra
  **61 câu** thuộc đúng phạm vi 4 module (bỏ qua các câu về EMI/GPS/EFIS/ARINC data-bus... ngoài phạm vi).
- [x] Render DPI cao (400dpi, `pdftoppm`) + crop bằng ImageMagick cho **15 hình** cần thiết (mạch nhiều
  cổng, ảnh chụp chip thật, sơ đồ chân IC) — quy trình đầy đủ ghi trong `data/FIGURE_EXTRACTION_WORKFLOW.md`.
  Ảnh đã optimize (≤900px cạnh dài) và đẩy lên repo tại `assets/figures/`.
- [x] **Bắt được 1 lỗi suy luận sai thật** khi đọc nhanh: câu hỏi Hình A2.14 (mạch 3 cổng) — đọc lướt lần
  đầu nhầm hình dạng cổng OR/NAND nên tính sai đáp án; crop ảnh rõ hơn và tính lại mới ra đáp án đúng. Đây
  đúng là lý do quy trình yêu cầu xem ảnh gốc thay vì chỉ đọc mô tả — đã sửa trước khi đưa vào site.
- [x] Toàn bộ 61 câu đã gộp vào `data/build_quiz.py` (phần "Tooley"), src ghi rõ "Revision Paper N Q#".
- Tổng số câu hỏi trên site sau đợt này: **299** (từ 241).

## Epic 9 — Floyd "Problems" (bài tập tự luận cuối chương) 🟢 (2026-09-28, phần khả thi)
- [x] **Ch.2 (Number Systems) — 69/69 bài, giải TOÀN BỘ bằng code** (`data/notebooks/01_*.ipynb`,
  mục 4). Toàn bộ 12 mục (2-1 tới 2-12) đều là chuyển đổi/tính toán số → auto-solve 100%.
- [x] **Ch.4 (Boolean Algebra) — phần lớn ~45+ bài giải bằng `sympy.logic`** (`02_*.ipynb`, mục 4):
  luật Boolean, De Morgan, rút gọn, SOP/POS, bảng chân trị, Karnaugh map, Quine-McCluskey. Các bài
  cần hình mạch cụ thể (12-17, 22, 36, 45-47, 50-51) hoặc VHDL/thiết kế phần cứng (60-72) liệt kê rõ
  là CHƯA giải, không suy đoán nội dung hình.
- [x] **Ch.6, Ch.11 — giải các bài KHÔNG cần hình** (`03_*.ipynb`, `04_*.ipynb`, mục 4): Ch.6 bài
  1,2,3 (logic bộ cộng cho sẵn A,B,Cin) + bài 9 (dùng ĐÚNG 8 chuỗi bit cho sẵn trong đề, không bịa số
  liệu thay thế); Ch.11 bài 2,4,5.
- [x] Đã chạy `jupyter nbconvert --execute` cho cả 4 notebook sau khi thêm — 0 lỗi.
- ⚠️ **Phát hiện 2 lỗi thật khi đối chiếu (ghi rõ trong notebook, không giấu)**:
  1. Ch.2 câu 5(c): tính đúng theo toán học `101₂=5`, nhưng phụ lục đáp án cuối sách Floyd ghi `3` —
     nhiều khả năng là lỗi in ấn trong chính sách gốc (7/8 giá trị còn lại của câu này khớp hoàn toàn).
  2. Ch.4 câu 8(b): sách yêu cầu xác nhận đẳng thức `AAB+ABC+ABB=ABC`, nhưng `sympy` rút gọn vế trái
     ra `AB`, KHÔNG bằng `ABC` — hai vế không tương đương, đã ghi rõ thay vì khẳng định sai.
- **CÒN THIẾU (không giấu)**: Ch.3 (55 bài, hầu hết là đọc giản đồ thời gian/vẽ lại dạng sóng từ hình
  — cần trích xuất hình riêng mới giải được, bản chất khác hẳn dạng số của Ch.2/Ch.4); phần lớn Ch.6
  và Ch.11 còn lại (cần hình mạch/sơ đồ chân IC cụ thể); các bài VHDL/thiết kế phần cứng/Multisim của
  mọi chương (bài toán thực hành công cụ, không phải tính toán). Tổng cộng còn khoảng 150-200 bài tự
  luận cần hình chưa giải.

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
