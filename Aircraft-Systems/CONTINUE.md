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
| P0a đọc từng slide | XONG phần đọc (22/11/2026): 342/342 slide có bản chép VI/EN trong `data/slides/transcript/` (9 file). 211 slide chép chi tiết (num 27, bus 18, swc 6, fib 37, logic 60, icmux 54, cpu 9), 131 slide đánh dấu `basis=summary` (emc 46, disp 36 từ bản đọc 10/2026; cpu 43 và icmux 6 là infographic dày chỉ tóm tắt) và chưa phóng to kiểm lại từng số. Tổng 108 mục lỗi hoặc nghi vấn trong slide (hiện ở `slides/<deck>.html` và `sources/`), 65 mục "Đã kiểm". Cách làm: `python3 build/stack_slides.py <deck> a b` ghép 2 slide/ảnh vào `scratch/stacks/`, đọc, phóng to chỗ nghi ngờ (`assets/slides/<deck>/pNN.jpg`), ghi `build/transcripts/<deck>.py` (hàm `s(...)`; kind chỉ được là content, title, divider, blank, thanks), rồi `.venv/bin/python -I build/transcripts/build_transcripts.py <deck>` và `check_transcripts.py`. Lỗi in thật mới tìm được: logic slide 28 và 31 (NAND/NOR đảo nghĩa so với slide 18 và 25), icmux slide 9 (khoảng hở 10000 đến 100000 cổng), slide 20 (74LS283 là bộ cộng, 74LS47 ghi hai lần), cpu slide 23 (RAM ghi là Read-Only), slide 24 (hộp L2 lặp, phải là L3), slide 46 (AX, BX... là thanh ghi 8086 nhưng ghi 8085), slide 38 (mã 3E 05, 06 03, 80 là MVI A, MVI B, ADD B của 8085 nhưng ghi MOV/ADD A,B). Còn việc: phóng to kiểm lại 131 slide basis=summary nếu cần số liệu chắc. |
| 342 ảnh slide + chỉ mục | XONG (`build/render_slides.py`, `assets/slides/`, `data/slides/index.json`); bản chép từng slide 342/342 (xem P0a) |
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
- Slide: đã có ảnh và bản chép 342/342; 131 slide chỉ ở mức tóm tắt (basis=summary).
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
- Còn lại theo thứ tự giá trị trên công sức: module 11 đến 15, cân lại vị trí và độ dài đáp án m05 đến m09, mức 3 cho m01 đến m09, Written/Concept/Analyser/Exercises, kiểm tra đầu vào, sổ lỗi, tách notebook VI/EN cho m01 đến m09, FEATURES P0b (mở site mẫu bằng trình duyệt).

- 22/11/2026: đã push commit 722d83a (nền pipeline), 66d5299 (module 10 và sửa lỗi), fcf7702 (bản chép slide 88/342, thuật ngữ, công thức), 89759e9 (bản chép 342/342 slide, 108 mục lỗi hoặc nghi vấn); production sau 89759e9: 86 trang x 2 khung nhìn, 0 tràn ngang, 0 ảnh hỏng, 0 lỗi KaTeX, 0 lỗi console, 7 URL cũ vẫn 200; production mở bằng trình duyệt: 0 tràn ngang, 0 ảnh hỏng, 0 lỗi KaTeX (một lần chờ quá hạn ở lần mở đầu tiên của slides/num.html, mở lại bình thường).
- Bài học mới: KaTeX `\sqrt` trong ô bảng có thể làm tràn ngang toàn trang ở 390 px (đường SVG của dấu căn rộng 7396 px, `scrollWidth` của trang tăng dù bảng cuộn): không dùng KaTeX trong ô bảng định nghĩa; dùng ký tự Unicode (√, ², ₁).


## Cập nhật 22/11/2026 (hai đợt trong cùng phiên)
**Đợt 1 (đã push, commit 9ffedc0; kiểm production bằng trình duyệt thật: 110 trang x 2 khung nhìn sạch, URL cũ vẫn 200):** 15 module vi+en, đủ loại đề (kiểm tra đầu vào, Midterm A/B/C, Final A/B/C 50 câu, Speed, Custom, hỗn hợp, theo module, Hard mức 3, Tooley Revision Papers, tự luận, tổng hợp, ôn câu sai), 6 công cụ (Khái niệm, Phân tích đề, Bài tập, Viết tay, Sổ lỗi, Bảng tra mã), m11 đến m15, ESD trong m09, 86 câu mức 3 cho m01-m07, ghi chú slide tiếng Anh.

**Đợt 2 (đã dựng và test trên máy, CHƯA push; hỏi người dùng trước khi push):**
- **8 đề Tooley Revision Papers đủ 160 câu** (trước đó 54 câu, chưa có đề 1): `build/gen/make_rev.py` (dữ liệu `gen_rev_a/b/c.py`, vá câu cũ `gen_rev_fix.py`) nạp 106 câu thiếu vào `data/qsrc/mNN_rev.json` theo module; 17 câu lặp lại câu chương của Tooley được gộp (thêm nhãn `/ Tooley Revision Paper P Qn` vào câu cũ, không thêm bản sao); 32 câu có hình cắt từ trang scan (`assets/figures/tooley_A2_k.png`, trường `fig`). Khoá in đọc lại từ ảnh trang Appendix 3 (khớp `data/verify/tooley_keys_ch15_20_rev.json`). Kiểm độc lập `build/verify/verify_rev.py` (xanh): 160 nhãn đủ, 20 câu tính lại bằng chương trình (đổi cơ số, BCD, cổng, BAG, ngưỡng CMOS, từ ARINC, mô phỏng hình A2.26/A2.17, sơ đồ chân 7400), 95 cụm bằng chứng tìm lại trong thân sách, 51 câu cũ đối chiếu khoá. Ba câu chỉ có khoá in và hình, không có đường thứ hai: P3 Q2 (màu radar thời tiết), P4 Q3 (WORM), P8 Q11.
- **Lỗi khoá in của Tooley (dùng đáp án đúng, ghi trong nhãn):** Revision Paper 6 Q10 (16K×4 → 8 chip, khoá (c) 16), Paper 8 Q9 (0101 × 50 mV = 0,25 V, khoá (a) 0,15 V), Paper 8 Q11 (độ chính xác ADC xấp xỉ liên tiếp phụ thuộc độ phân giải (a), khoá (c) thời gian chuyển đổi; câu này chỉ có lý thuyết ADC, cần hỏi giảng viên), Chương 20 Q10 và Paper 8 Q8 là cùng một câu nhưng hai khoá mâu thuẫn ((b) và (a)); theo Hình 20.6 là (a) liên kết chéo hiển thị. Tooley Ch.20 Q10 nay nằm trong ngân hàng (gộp với Paper 8 Q8).
- **Sửa 4 câu cũ sai/gán nhầm** (phát hiện nhờ đối chiếu khoá): Paper 5 Q6 (hình A2.19 là chip 7400 NAND, ngân hàng ghi NOR), Paper 4 Q18 (hai cổng đảo vào NOR cho AND, ngân hàng ghi OR), Paper 4 Q2 (phương án đúng trái khoá in), câu "chân IC DIL" mang nhãn Paper 2 Q20 nhưng là Paper 4 Q20.
- **Phần vi điều khiển (CO5)**: `build/gen/gen_m04_mcu.py` + `build/content/m04_mcu.py` + hình `build/figs/make_m04_figs.py`; Floyd Ch.14 Đúng/Sai (15) và Self-Test (15), 24 câu bổ sung tính bằng `numlib/mcu.py`, 9 bài tự luận gốc (Checkup 14-8, 14-9); `verify_m04_mcu.py` đọc khoá từ văn bản sách; hai khoá in sai (Đúng/Sai 12, Self-Test 13). Floyd Ch.8 Self-Test 10 (Hình 8-36) đã đưa vào m11 (`m11_floyd.py`, hình `assets/figures/floyd_8_36.png`).
- **46 slide có số liệu/công thức** (cpu 12, disp 17, emc 14, icmux 3) đã phóng to kiểm lại, bỏ nhãn `basis='summary'`; còn 85 slide chỉ có chữ (không số, không công thức) vẫn ở mức tóm tắt.
- Cân bằng vị trí đáp án: `data/published_ids.json` (id đã lên web) giữ nguyên thứ tự lựa chọn của câu đã công bố (trình duyệt lưu CHỈ SỐ lựa chọn); câu mới được đặt để vị trí đúng phân bố đều (m07 3 lựa chọn: χ² 10,4 xuống 5,1; m13: 18/18/18). `build/push.sh` tự chạy `build/pubids.py` sau khi push.
- Sửa dấu chấm phân cách nghìn trong chữ tiếng Anh (65.536 thành 65,536; `build/gen/fix_en_thousands.py`, nhận biết đơn vị để không đụng 32.768 kHz, 1.024 MHz, 2.048 Mbit/s).
- Trang Luyện đề: văn bản mô tả đề Tooley sửa lại (8 đề đủ 20 câu).
- QA đợt 2: site_test, exam_test (thêm kiểm tra 8 đề Tooley, hình, kiểm tra đầu vào, hoán vị lựa chọn), tools_test đều PASS; 9 script verify xanh; crawl 110 trang x 2 khung nhìn: 0 tràn ngang, 0 ảnh hỏng, 0 lỗi KaTeX/console/HTTP.
- Số đo cuối: ngân hàng m01-m15: 1 370 câu trắc nghiệm/đúng-sai (751 gốc; mức 1/2/3 = 720/399/251), 165 tự luận, m00 (đầu vào) 40 câu, 190 thuật ngữ, 53 công thức; đề: 15 theo module, 8 Tooley, 4 tự luận, Midterm/Final 3+3, Hard 2, tổng hợp 2, đầu vào 1, hỗn hợp 4.

**Đợt 3 (đã dựng và test trên máy sau commit a4edac6, CHƯA push):**
- **Notebook m01-m09 đã tách thành cặp VI/EN** (`notebooks/mNN_<slug>_{vi,en}.ipynb`, chạy lại bằng nbconvert, 0 lỗi, số liệu in ra giống hệt nhau): `build/nb/split_legacy.py` (chạy bằng `.venv/bin/python`, kernel tạm trong `scratch/jup/`), bản dịch EN trong `build/nb/legacy_en_a/b/c.py` (markdown theo chỉ số ô; code theo cặp "đoạn tiếng Việt không dấu" → "đoạn tiếng Anh"), `build/nb/check_en_residual.py` tìm chữ Việt còn sót (còn 2 dòng báo nhầm do tên biến DE). File cũ `data/notebooks/NN_*.ipynb` giữ để URL cũ sống. Bản VI giữ lời nhắn in ra bằng tiếng Việt không dấu (như bản gốc).
- 4 slide chỉ có chữ của bộ cpu (4, 7, 8, 9) kiểm thêm: khớp ảnh.

- **Sửa lỗi ký tự ở trang Viết tay (người dùng báo, ảnh chụp có `<br>` và `&nbsp;` hiện nguyên chữ):** 92 đề và 8 lời giải tự luận cũ (m01, m02, m03, m04, m08) mang HTML; `assemble.py` hàm `plain()` đổi `<br>` thành xuống dòng, `&nbsp;` thành dấu cách, `<sub>16</sub>` thành chỉ số dưới Unicode (46₁₆), bỏ thẻ `<i>`, `<b>`; thêm CSS `.xq>div{white-space:pre-line}` cho bản in. Đã quét toàn bộ dữ liệu vi/en và các trang Viết tay, Luyện sâu, Luyện đề: không còn thực thể, thẻ, ký tự lỗi hay công thức chưa vẽ. CHƯA push.

**CHƯA LÀM (nói thẳng):**
1. 81 slide chỉ có chữ (không số, không công thức) vẫn ở mức tóm tắt, chưa phóng to kiểm lại từng slide (cpu 27, disp 19, emc 32, icmux 3); mẫu kiểm 4 slide cpu không thấy sai.
2. Test Your Understanding 20.6 của Tooley (sách không in đáp án).
3. Cắt ảnh sách riêng cho từng bài tập (4c) chưa làm thêm.
4. Mã VHDL chưa biên dịch bằng công cụ thật (máy không có ghdl/nvc; cần người dùng đồng ý cài).
5. Lệch vị trí đáp án còn ở m01 (3 lựa chọn, χ² 6,5); lệch độ dài (đáp án đúng dài nhất, 3 lựa chọn): m07 63 %, m12 71 %, m13 65 %, m15 77 % là đặc điểm của câu gốc Tooley; đề Tooley tái hiện đúng sách.
6. P0b (mở site mẫu bằng trình duyệt) và P2 (bản đồ mục sách chi tiết) chưa làm; 3 câu Revision Paper chỉ có khoá in (P3 Q2, P4 Q3, P8 Q11, trong đó P8 Q11 cần hỏi giảng viên).
