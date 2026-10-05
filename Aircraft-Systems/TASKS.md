# TASKS — AE2.021 Aircraft Digital Electronics & Computer Systems

Ngày khởi tạo: 2026-09-28.

## Epic 13 — Module 05: Bus dữ liệu hàng không (Data Buses) 🟢 (2026-10-04)
- [x] **Nguồn**: slide bài giảng riêng "Data buses aircraft - ver 2026 v2.pdf" (18 slide, ảnh infographic,
  không có text layer dùng được: đã render cả 18 trang ở 150 dpi vào
  `OCR_output/DataBuses_Lecture/pages/` và đọc trực tiếp bằng mắt từng trang) + Tooley Chương 4 "Data
  Buses" (tr.53-69: 4.1 Introducing bus systems, 4.2 ARINC 429, 4.3 Other bus standards, 4.4
  Multiple-Choice Questions). **Floyd KHÔNG có nội dung liên quan** (giáo trình điện tử số thuần tuý,
  không đề cập avionics bus): đây là module có độ khớp 2 sách THẤP NHẤT (thấp hơn cả Module 04), quiz chỉ
  có 2 nguồn (Tooley + câu bổ sung), không có mục Floyd.
- [x] **Phát hiện lỗi thật trong bài giảng**: slide 14 ghi mã hoá ARINC 429 là "Manchester Biphase-L",
  nhưng đối chiếu slide 3, slide 13 (cùng bài giảng) VÀ sách Tooley (mục Electrical Characteristics +
  bảng chú giải BPRZ) đều xác nhận mã hoá ĐÚNG là Bipolar Return to Zero (BPRZ). Đã đưa phát hiện này
  thành nội dung dạy (khung cảnh báo ⚠️) thay vì chỉ âm thầm sửa, vì đây là ví dụ thực tế tốt cho kỹ năng
  đối chiếu đa nguồn.
- [x] **17 câu MCQ gốc từ Tooley Ch.4** (mục 4.4, tr.67-69): đọc trực tiếp từ ảnh scan trang sách (OCR
  text-layer đọc được rõ ràng cho đề bài), đáp án đối chiếu với Appendix 3 (A.4 Chapter 4, tr.377) đọc
  trực tiếp từ ảnh scan vì bảng đáp án đa cột bị OCR text-layer xáo trộn thứ tự (bài học cũ đã ghi trong
  skill `build-complete-self-study-system`). Toàn bộ 17 câu đã tự kiểm chứng lại bằng code trong notebook
  `05_data-buses.ipynb` (chạy thật bằng `nbconvert --execute`, không chỉ viết ra). Thêm 7 câu bổ sung
  (MOD5_GEN) về ARINC 629/AFDX/MIL-STD-1553/SSM/thời gian truyền, tính từ số liệu thật trong bài giảng.
- [x] **28 slide × 2 ngôn ngữ** (5 phần: vì sao cần bus → ARINC 429 cơ bản → cấu trúc từ dữ liệu ARINC
  429 → các chuẩn bus khác → ứng dụng A320), mỗi slide có khung "Giải thích cho người mới bắt đầu". 8 ảnh
  gốc trích từ chính bài giảng (`assets/figures/databus_p02/03/06/07/10/12/13/16.jpg`, cắt nguyên trang
  infographic vì chất lượng đã đủ tốt để dùng trực tiếp, không cần crop nhỏ hơn).
- [x] **Notebook `05_data-buses.ipynb`**: mã hoá/giải mã BCD và BNR cho trường Data 19-bit, đóng gói/giải
  mã trọn 1 từ ARINC 429 32-bit (tự tính parity lẻ), kiểm chứng công thức thời gian truyền, và chạy lại
  toàn bộ 17 câu MCQ bằng code. Phát hiện 1 lỗi nhỏ khi tự viết code: hàm mã hoá BCD ban đầu mặc định 5
  chữ số (20 bit) làm tràn trường 19-bit: đã sửa về mặc định 3 chữ số (đủ cho ví dụ 250kt) và ghi chú rõ
  5 chữ số BCD không thể vừa 19 bit, một điểm cần cẩn thận khác của chính bài giảng.
- [x] Cập nhật hạ tầng dùng chung cho module không có Floyd: `FLOYD_MODULES["05-data-buses"]` để rỗng
  (`tf=[], st=[]`) thay vì bỏ qua (tránh KeyError), và `build_quiz_section()` trong `render_site.py` nay
  bỏ qua render nếu danh sách câu hỏi rỗng (không hiện khung quiz trống).
- [x] Thêm overlay dịch tiếng Anh thủ công cho toàn bộ 24 câu quiz mới (17 Tooley + 7 bổ sung) vào
  `quiz_en_overlay.py` (`OPT_EN_BY_Q.update()`/`EXPLAIN_EN.update()`), rồi xác minh bằng script quét ký tự
  tiếng Việt trên JSON bản EN: 0 câu còn sót tiếng Việt (đúng quy trình đã rút kinh nghiệm từ lỗi ở Epic
  trước, xem `06-multilingual-workflow.md` mục 6.6bis của skill).
- [x] Cập nhật "4 module" → "5 module" ở mọi nơi hiển thị số lượng (trang chủ VI/EN, link/tiêu đề bảng
  ánh xạ chương VI/EN), thêm dòng `MAPPING_ROWS` cho module 05 trong `render_site.py`.
- [x] `render_site.py` (38 slide/ngôn ngữ sau khi thêm part-divider/formula/legend), `check_links.py`
  (330 link nội bộ, 0 lỗi), build screenshot headless xác nhận trang chủ + trang module hiển thị đúng cả
  2 ngôn ngữ, không có box quiz/ảnh vỡ.
- **CHƯA LÀM**: audit thiên lệch vị trí đáp án (position-bias) cho quiz module 05 (và thực ra cho CẢ 4
  module trước đó cũng chưa từng chạy, xem Epic 4 của skill `build-complete-self-study-system`: đây là
  khoảng trống chung của toàn site, không riêng module 05); câu hỏi tự luận (essay) không làm cho module
  này vì Tooley chỉ có "Test Your Understanding" không kèm đáp án in sẵn (không đủ điều kiện theo đúng
  tiêu chuẩn essay đã áp dụng ở Epic 12, vốn chỉ dùng câu có đáp án ẢNH CHỤP THẬT).

## Epic 14 — Mở rộng câu tự luận Floyd (đề có hình + ảnh đáp án thật) 🟡 (2026-10-05)
- [x] Hạ tầng: `qimgs` (ảnh đề cắt từ sách, giữ nguyên gạch trên) và `note_vi/note_en` từng bài trong `essay_questions.py` + `build_essay_section()`. Toàn bộ ảnh trang, ảnh cắt, script kiểm chứng nằm trong `OCR_output/Floyd/{pages,crops,scripts,text}`.
- [x] **Module 01 (Ch.2)**: đủ 35 bài lẻ; phát hiện 3 lỗi in: Bài 5(c), 29(b), 37(g).
- [x] **Module 02 (Ch.3 + Ch.4)**: Ch.3 thêm 24 bài (dạng sóng kiểm chứng bằng đọc pixel `wavetools.py`/`verify_ch3.py`); Ch.4 thêm 15 bài (sympy, `verify_ch4.py`). Lỗi in/không khớp: Ch.3 Q31 (tên entity bắt đầu bằng chữ số), Ch.4 Q21(b), Q61 (X/Y), Q3 và Q15 (đáp án in không khớp đề).
- [x] **Module 03 (Ch.6)**: thêm 8 bài (5, 7, 11, 13, 17, 19, 21, 23), tổng 11. Loại vì đáp án in không khớp đề: Q9, Q25, Q27 (Gray→nhị phân của số khác), Q29 (sóng XOR ứng với dữ liệu ngược Bài 28).
- [ ] **CHƯA LÀM**: Module 04 (Ch.11): các bài lẻ còn lại có hình hoặc cần lập bảng (1, 7, 11, 13, 15, 17, 19, 29 đến 37); Ch.3 bài 41, 49, 53, 55; Ch.4 bài 11, 17, 25 đến 29, 43, 55 đến 59; Ch.6 bài 31 đến 37.

## Epic 12 — Câu hỏi tự luận (Problems) từ Floyd, đáp án là ảnh chụp thật 🟢 (2026-09-28)
- [x] **Khảo sát cấu trúc 2 sách**: Tooley (Aircraft Digital Electronic and Computer Systems) chỉ có mục
  "Multiple-choice questions" cuối mỗi chương, KHÔNG có phần tự luận riêng (đã kiểm tra mục lục gốc, xác
  nhận qua `pdftotext`). Toàn bộ câu tự luận trong Epic này do đó lấy từ Floyd, Digital Fundamentals, phần
  "Problems" cuối chương, chỉ chọn câu SỐ LẺ vì sách chỉ in đáp án cho câu lẻ ở phụ lục "Answers to
  Odd-Numbered Problems" cuối sách.
- [x] **Module 01 (Floyd Ch.2, 6 câu)**: Problem 7, 13, 21, 25, 49, 63. Mỗi câu đã tính lại độc lập bằng
  tay, đối chiếu ảnh chụp thật trang phụ lục (p.A-1, A-2) ở DPI 400 trước khi đưa vào site.
  Phát hiện quan trọng: **Problem 5(c)** (101₂ đổi thập phân) có lỗi in ấn thật trong sách, đáp án in là
  "3" nhưng giá trị đúng là "5": đã loại bỏ câu này khỏi danh sách, không dùng để tránh gây hiểu nhầm.
- [x] Hạ tầng mới: `data/essay_questions.py` (câu hỏi gõ tay bằng HTML, song ngữ) + `build_essay_section()`
  trong `render_site.py`, hiển thị dưới quiz mỗi trang module. Mỗi câu có khung `<details>` "Xem đáp án gốc
  trong sách", mở ra hiện ẢNH CHỤP THẬT (không gõ lại) từ đúng trang phụ lục, crop tại
  `OCR_output/exercise_pages/Floyd/ch02_number_systems_essay/answers/`, copy vào `assets/figures/essay_floyd_*`.
- [x] **Module 02 (Floyd Ch.3+4, 6 câu)**: Ch.3 Problem 25; Ch.4 Problem 1, 5, 7, 9, 19. Riêng câu 9 (De Morgan)
  đề bài in dấu gạch ngang trên rất nhỏ nên không đọc trực tiếp bằng mắt; đã suy ngược từng biểu thức từ
  đáp án in rồi kiểm tra xuôi lại bằng De Morgan, cả 8 ý khớp. Bỏ qua Ch.4 Problem 3 (đề ghi 3 biến A,B,C nhưng
  đáp án in "ABCD") và Problem 21 (đáp án in có gạch trên biến E, còn text trích từ PDF mất dấu gạch nên chưa thể tự kiểm tra lại, không dùng khi chưa chắc).
- [x] **Module 03 (Floyd Ch.6, 3 câu)**: Problem 1, 3, 15. Cố ý chỉ 3 câu thay vì 6: các câu còn lại hoặc cần
  đọc sơ đồ cụ thể trong sách, hoặc lệch đề/đáp án (Problem 25: đề hỏi 4,7,12,23,34 nhưng đáp án in cho
  2,8,13,26,33; Problem 9 chưa kịp đối chiếu lại dữ liệu bit với notebook 03 nên chưa đưa lên). Ưu tiên đúng hơn đủ số lượng.
- [x] **Module 04 (Floyd Ch.11, 6 câu)**: Problem 3, 5, 9, 21, 25, 27. Câu 21 (ngăn xếp LIFO 4096x8) tính tay ra
  FC0h..FFFh, khớp đáp án in.
- [x] Kiểm tra toàn bộ 21 ảnh đáp án bằng bảng tổng hợp: phát hiện và sửa 8 ảnh bị cắt sai lần đầu (Q13 và Q49
  Ch.2 thiếu dòng, Ch.3 Q25 mất dấu gạch trên, Ch.4 Q7 thiếu (a), Ch.6 Q3 mất (a), bảng Ch.11 Q5 mất dòng
  tiêu đề...). Bài học: luôn xem ảnh crop cuối cùng, không chỉ xem lúc cắt thử.
- Tổng: 21 câu tự luận, song ngữ, đáp án là ảnh chụp thật, đã trên site.

## Epic 11 — Giải thích "cho người mới bắt đầu" dưới từng slide + ảnh gốc bài giảng 🟢 (2026-09-28)
- [x] **Module 01 (pilot, chờ duyệt phong cách)**: cả 50 slide nội dung × 2 ngôn ngữ đều có khung
  `<details>` thu gọn "Giải thích cho người mới bắt đầu" (nguồn: `data/explain01/{vi,en}_p0..p4.py`,
  gộp vào `slides_01.py` qua trường `explain`).
- [x] Trích 8 hình gốc từ `Number system.pdf` (bài giảng của giảng viên, chưa từng có trên site) vào
  `assets/figures/numsys_*`: 6 infographic "Applications of ... in A320" (tổng quan, thập phân, nhị phân,
  hex, bát phân, BCD), sơ đồ chuyển đổi 4 hệ đếm, mạch half adder. Gắn vào 8 slide phù hợp qua trường `img`,
  bấm vào ảnh để mở bản đầy đủ.
- [x] `check_links.py` nay nhận cả thuộc tính dùng dấu nháy đơn (trước đó bỏ sót ảnh mới): 110 → 142 link, 0 lỗi.
- [x] Sau khi duyệt Module 01: deck tự co giãn cỡ chữ (`_shared/deck.js` hàm `fit()`), cả ở chế độ xem
  thường lẫn toàn màn hình, co nhỏ khi mở khung giải thích. Thêm cache-busting theo hash nội dung cho
  mọi file `_shared/*.css|js` (`render_site.py` biến `VER`) để tránh trình duyệt giữ bản cache cũ.
- [x] **Module 02 (Cổng logic & Đại số Boolean)**: cả 50 slide nội dung × 2 ngôn ngữ có khung giải thích
  (nguồn: `data/explain02/{vi,en}_p0..p4.py`, gộp vào `slides_02.py`). Trích 8 hình gốc từ
  `logic circuit_version 2026.pdf` vào `assets/figures/logic_*`: 6 infographic "Applications of ... gate
  in A320" (AND, NOT, NAND, XOR, OR, tổng quan 6 cổng), 1 infographic ứng dụng đại số Boolean trong A320,
  1 sơ đồ tương đương NAND = Negative-OR minh hoạ De Morgan (crop riêng từ trang 51, bỏ phần chữ lý thuyết).
- [x] **Module 03 (Mạch tích hợp & Kỹ thuật dồn kênh)**: cả 50 slide nội dung × 2 ngôn ngữ có khung giải
  thích (nguồn: `data/explain03/{vi,en}_p0..p4.py`, gộp vào `slides_03.py`). Trích 8 hình gốc từ
  `integrated circuit and multiplexing version 2026.pdf` vào `assets/figures/icmux_*`: sơ đồ 5 mức quy mô
  tích hợp SSI→ULSI, sơ đồ đóng gói IC (SIP/DIP/ZIP/QFP/PGA), infographic ứng dụng IC trong A320, bảng chân
  trị decoder 4-bit (1-of-16) thật, sơ đồ logic bộ mã hoá decimal-to-BCD, sơ đồ tổng hợp mạch tổ hợp
  (adder/mux/code converter), ký hiệu và bảng chân trị multiplexer 1-of-4, sơ đồ mạch demultiplexer 1-to-4.
- [x] **Module 04 (Cấu trúc máy tính & Vi xử lý)**: cả 30 slide nội dung × 2 ngôn ngữ có khung giải thích
  (nguồn: `data/explain04/{vi,en}_p0..p4.py`, gộp vào `slides_04.py`). Trích 8 hình gốc từ
  `Basic computer structure and microprocessor PDA version 2026.pdf` vào `assets/figures/cpu_*`: sơ đồ
  kiến trúc hệ thống máy tính (CPU+bộ nhớ+bus), ví dụ address bus 32-bit thật, IPO Principle áp dụng cho
  A320, sơ đồ RAM/ROM primary/secondary storage, bảng phân loại volatile/non-volatile memory (ROM/EPROM/
  EEPROM/SSD), sơ đồ thanh ghi vi xử lý (PC/IR/ACC/SP), sơ đồ chu trình Fetch-Decode-Execute đầy đủ, bảng
  so sánh kiến trúc Von Neumann và Harvard.
- ⚠️ **Epic 11 hoàn tất cho cả 4 module** (160 slide × 2 ngôn ngữ = 320 khung giải thích, 32 hình gốc trích
  từ 4 bài giảng). Còn tồn đọng: một vài `body` cũ của Module 01 còn câu lủng củng (ví dụ slide "10.000 ft"
  có đoạn "10000×2=...").

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

### Epic 12 addendum: language and verbatim fixes
- [x] EN site no longer mixes Vietnamese into quiz options or explanations (overlay files, commit 6a6777c).
- [x] Essay questions re-checked against the book at 300-600 dpi; Ch.4 Q7, Q9 (was mis-transcribed, (f)-(h)) and Ch.11 Q5, Q21, Ch.6 Q1 now match the book's English wording; overlines are real (`~{...}` markup rendered as `.ov`); VI pages also show the original English line.
- [x] Excluded after verification: Ch.6 Q9 (printed answer Σ1..Σ5 not reproducible under any bit-order/LSB-MSB reading; all 8 readings tested), Ch.4 Q21 (ambiguous overlines in (e)/(b) and printed (b) differs from independent simplification B'C').
- [ ] Waveform/figure problems (Ch.3, most of Ch.6) still not added: they need question figures (qimg support) and programmatic waveform checks.
