# CONTINUE — AE2.021 Aircraft-Systems (nâng cấp site có sẵn)

Cập nhật: 21/11/2026. Mọi số dưới đây do `scratch/audit/inventory.py`, `crawl.py`, `data/audit_quiz.py`, `data/check_links.py` in ra (kết quả lưu ở `scratch/audit/`). Nguồn yêu cầu: `../ULTIMATE_PROMPT_AE2.021_Aircraft_Systems.md`.

## Quyết định (mục 4 của prompt)
Người dùng trả lời 21/11/2026:
- 4a: CHUYỂN sang pipeline mới `build/` (giữ nguyên URL `vi|en/modules/0N-<slug>/`). Site cũ không lưu tiến độ quiz, nên đổi mã câu hỏi không làm mất gì.
- 4b: THÊM cả ba hướng: (i) A/D–D/A (Tooley Ch.3, Floyd Ch.12) → module 10; (ii) mạch tuần tự Floyd Ch.7–10 (latch, flip-flop, thanh ghi dịch, bộ đếm, logic khả trình); (iii) Tooley §15.4 đến Ch.20. Các mục này KHÔNG có slide của giảng viên: dựng từ sách và ghi rõ "không có slide". Chia thành: m10 A/D–D/A (Tooley Ch.3, Floyd Ch.12) · m11 mạch tuần tự (Floyd Ch.7–10, Tooley §5.6–5.7) · m12 avionics §15.4–15.10 · m13 mạng dữ liệu, AFDX, IMA (Tooley Ch.16, 18) · m14 VHDL (Ch.17) · m15 cabin và thông tin tàu bay (Ch.19, 20). Tooley Ch.12 ESD gắn vào m09 như phần mở rộng. Cách chia là đề xuất của site, chỉnh được.
- 4c: ĐĂNG đủ 342 ảnh slide VÀ thêm ảnh trang sách. Rủi ro bản quyền cao nhất, đã cảnh báo; người dùng chọn. Cách làm: ảnh cắt theo từng bài tập/hình cần cho lời giải, không đăng nguyên cuốn sách.
- 4d: CHỈ LÀM ĐỀ (Midterm / Final / Speed / Custom, ghi rõ là thiết kế của site); BỎ trang Lab. Ba demo có sẵn (checksum/CRC, cáp quang, EMC) giữ trong module m07–m09, và các công cụ tính (đổi cơ số, bảng chân trị, ARINC 429…) nằm ở trang Bảng tra/Concept, không phải Lab.

## Giai đoạn
| Giai đoạn | Trạng thái |
|---|---|
| P0c kiểm kê site | XONG 21/11 (bảng dưới) |
| Nền pipeline mới `build/` (4a) | XONG 21/11, CHƯA push: `modules.py`, `assemble.py` (mã câu ổn định = băm nội dung), `build_site.py`, `legacy.py` (chuyển nội dung 9 module cũ), `migrate_quiz.py`, `migrate_essays.py`, `topics.py`, `mapping.py`, `bookmap_body.py`, `sources_body.py`, `exams.py`, `push.sh`; `_shared/` mới (khoá `ae2021:`); `tests/site_test.py` 11/11 PASS; quét trình duyệt 64 trang × 2 cỡ: 0 tràn, 0 ảnh hỏng, 0 lỗi console, 0 gạch ngang dài |
| Module 10 (A/D và D/A) | XONG 21/11, CHƯA push: `build/content/m10.py` (5 phần, 16 slide nội dung × 2 ngôn ngữ, 3 hình tự vẽ), `build/numlib/adda.py` (mỗi hàm có hai cách tính), `build/gen/gen_m10.py` → 109 câu trắc nghiệm (38 gốc: Tooley Ch.3 13 câu khoá đọc từ ảnh A.3, Floyd Ch.12 đúng/sai, Self-Test, Checkup; 71 bổ sung, 27 câu mức 3) + 7 tự luận, `build/verify/verify_m10.py` (FAILS: none; 58/71 câu sinh được tính lại độc lập), notebook VI và EN chạy thật (`notebooks/m10_*`), `data/verify/m10_notes.json` (13 điểm nghi vấn của nguồn) |
| P0a đọc từng slide | CHƯA LÀM. Lần giao 11 tác tử song song đã thất bại (giới hạn sử dụng 5 giờ, không file nào được ghi) và người dùng yêu cầu KHÔNG chia nhiều tác tử: đọc tuần tự trong phiên chính |
| 342 ảnh slide + chỉ mục | XONG (`build/render_slides.py`, `assets/slides/`, `data/slides/index.json`); CHƯA đọc từng slide (P0a) |
| 4a–4d hỏi người dùng | XONG 21/11 (xem Quyết định) |
| P0 kiểm và vá nguồn (slide, Tooley, Floyd) | CHƯA LÀM |
| P0b khảo sát site mẫu → FEATURES.md | CHƯA LÀM |
| P1 trở đi | CHƯA LÀM |

## Hiện trạng (P0c): đã có / thiếu / lỗi
ĐÃ CÓ (đo được)
- 9 module × 2 ngôn ngữ, URL `vi|en/modules/0N-<slug>/index.html`; mỗi trang module là một deck: 60, 60, 60, 40, 38, 47, 30, 40, 41 `mdeck-slide` (gồm cả trang phân đoạn).
- 607 câu trắc nghiệm mỗi ngôn ngữ: Tooley 224, Floyd 206, tự sinh 177 (29,2 %). 86 câu đúng/sai. 511/607 có lời giải chi tiết (`detail`); m05–m09 đủ 100 %, m01–m04 từ 66 % đến 69 %.
- 129 bài tự luận Floyd/bài giảng (m01 35, m02 44, m03 11, m04 20, m06 4, m07 6, m08 7, m09 2), 186 ảnh đề và đáp án, 0 ảnh thiếu.
- 9 notebook (VI và EN cùng một file), mọi ô chạy sẵn, 0 lỗi.
- 3 demo JS: `demo_emc.js`, `demo_fibre.js`, `demo_integrity.js`. 4 giao diện. 327 ảnh trong `assets/figures`, trong đó 120 là ảnh trang slide của giảng viên (trên 342 trang, 35 %).
- 1 198 liên kết nội bộ đều tồn tại. Trình duyệt 1366 px: 0 tràn ngang, 0 ảnh hỏng, 0 lỗi KaTeX, 0 HTTP ≥ 400.
- Trang EN: không có chữ Việt lẫn vào (chỉ nhãn "Tiếng Việt" của nút đổi ngôn ngữ và tên sách tiếng Pháp). Quiz EN: 0 ký tự Việt. Trang VI: 0 số sai định dạng kiểu "60.000.0".

THIẾU (so với chuẩn mới của prompt)
- Không có `CONTINUE.md`, `AGENT_BRIEF.md`, `FEATURES.md`, `build/`, `tests/`, `verify_mNN.py`, `mNN_notes.json`.
- `_shared/` chỉ có 9 file. Không có: bank, exam, written, analyse, concepts, lab, exercises, books, sources, progress, resume.
- **Không lưu tiến độ**: chỉ `localStorage` cho giao diện (`site-theme`). Quiz không ghi gì, câu hỏi không có mã. Hệ quả: đổi mã câu hỏi KHÔNG làm mất tiến độ nào của người học (cân nhắc ở 4a).
- Câu hỏi không có mã ổn định (R6). 98/607 câu không có nguồn (`src` rỗng), đều thuộc nhóm tự sinh (R7).
- Ngân hàng không có `topic` và không có mức 1/2/3.
- Slide: 222/342 trang chưa có ảnh trên site; chưa có bản chép VI/EN theo từng slide.
- Chưa có module cho A/D–D/A (CO4), mạch tuần tự, Tooley Ch.3, 12, 16–20; Floyd Ch.1, 5, 7–10, 12–15.

LỖI (đã thấy, chưa sửa)
1. `chapter-mapping-vi.html` và `-en.html` tràn ngang ở 390 px: 161 px và 193 px (bảng 5 cột không cuộn).
2. Trang module 05 (VI) ghi "Floyd KHÔNG CÓ chương nào về bus dữ liệu" và "17-question MCQ bank". Sai: Floyd Ch.13 §13-6 đến 13-10 có bus chung (USB, SPI, I²C…) và đã có 19 câu Floyd; ngân hàng hiện 62 câu. Mô tả "4 bộ slide" trong bảng ánh xạ cũng cũ (hiện 9 bộ).
3. Trang module rất dài: tối đa 46 498 px ở 1366 px và 57 173 px ở 390 px (m02). Cần mục lục dính và phân trang.
4. Lệch độ dài lựa chọn (đáp án đúng thường dài nhất), p < 0,05: m01 Tooley (0,0006), m01 Floyd (0,0005), m01 tự sinh (0,037), m02 Floyd (0,035), m05 tự sinh (0,036), m07 tự sinh (0,003), m08 Floyd (0,008). Lệch vị trí: không nhóm nào p < 0,05.
5. `README.md` ở `$W` đã lỗi thời (ghi 6 bộ slide, 6 module).
6. `PROBLEMS_STATUS.md` tự mâu thuẫn ở Floyd Ch.11 (19 hay 20 bài lẻ).
7. `TASKS.md` có thể cũ: m05–m09 đã mở rộng quiz (commit 245450d) nhưng Epic chưa cập nhật.

Chưa đo được ở P0c (cần P0/P8): đọc đủ từng trang của 9 bộ slide; chất lượng OCR Tooley; offset trang in ↔ PDF; Floyd A-1 ở PDF trang 896; trạng thái production sau commit 245450d (chưa mở trang production).

## Việc kế tiếp
1. (xong) Ghi trả lời 4a–4d. (xong) Dựng `$W/Aircraft-Systems/`, `.venv` có sympy, `build/push.sh`; dry-run: 507 file thêm/đổi, 1 file xoá (`_shared/deck.css` → đã thay bằng `aircraft.css`).
2. Chờ người dùng xác nhận push hợp phần "nền pipeline" (prompt mục 0: hỏi sau MỖI hợp phần).
3. P0 (đọc từng slide, OCR Tooley, Floyd A-1), P0b (khảo sát site mẫu bằng trình duyệt), P2 (cấp mục sách), P3 (bộ công cụ số/logic), P4 (viết lại từng module, thêm m10 đến m15), P5 (quét bài tập), P6 (Written, Concept, Analyser, Exercises, Glossary, Formulas, Kiểm tra đầu vào, Sổ lỗi).

Các lỗi đã phát hiện khi chuyển (xem `data/verify/migration_notes.json`): Tooley Revision Paper 6 Q2 in hai lựa chọn giống nhau (tr.366), đã thay (c) và ghi chú; hai câu bị trùng nội dung và được gộp (m01, m04); Tooley Ch.10 bắt đầu tr.165 chứ không phải 162; m05 từng ghi sai "Floyd không có bus"; khoá localStorage của Thermal không có tiền tố môn.
Số đo mức độ: level 3 chỉ có ở một phần ngân hàng (m07 không có câu mức 3; m02 7/102); topic gán bằng từ khoá (m04 memory 57/73, m02 gates 51/102): cần rà ở P4. Vị trí đáp án sau khi xáo theo băm nội dung: m07 3 lựa chọn [23, 8, 16] (chi bình phương 7,19, p ≈ 0,03); lệch độ dài: m05 51 %, m07 61 %, m09 51 % (đáp án đúng là dài nhất): cần cân lại.


## Cập nhật cuối phiên 21/11/2026 (sau commit 722d83a)
- Chưa push: sửa tràn ngang ở thư viện slide (390 px, production báo thất thường), demo hiện dấu phẩy thập phân ở trang Việt, giao diện Ocean, module 10. Cần xác nhận push (prompt mục 0).
- Số đo hiện tại (bản làm việc): 20 trang module (vi, en), ngân hàng 714 câu trắc nghiệm (605 + 109), 136 tự luận. Ghi chú: `data/qbank/_audit.json` có chi bình phương vị trí và tỉ lệ đáp án dài nhất theo từng nhóm.
- Còn lại theo thứ tự giá trị trên công sức: P0a đọc slide (tuần tự, ghi từng cụm 5 đến 10 slide vào `data/slides/transcript/` ngay), glossary và tóm tắt công thức (F15, F16), module 11 đến 15, cân lại vị trí và độ dài đáp án m05 đến m09, mức 3 cho m01 đến m09, Written/Concept/Analyser/Exercises, kiểm tra đầu vào, sổ lỗi, tách notebook VI/EN cho m01 đến m09, FEATURES P0b (mở site mẫu bằng trình duyệt).
