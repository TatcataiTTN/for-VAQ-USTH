
# Tiến độ & cách làm tiếp — AE2.025 Electronics 2

## Đã xong

- **Đọc nguồn** (Drive `1Gd37QKLz37eMqwB9KT79aqZKefgr8_q4`): Floyd 9e (2012, đúng bản đề cương), Jaeger 5e (2015, có Digital ch.6–9), Jaeger 6e (chỉ analog), EASA M04 B2 (bản scan).
- **PDF chọn được chữ**: Floyd/Jaeger đã có lớp chữ ở mọi trang nội dung. EASA M04 là scan → đã OCR: `sources/easa_m04_ocr.pdf`.
  OCR lần 2 (tesseract psm 4, 300 dpi) để đối chiếu: `build/verify/ocr_easa_second_pass.sh` → `OCR_output/easa_m04/ocr_raw/psm4/` (chạy lại script nếu chưa đủ 126 trang).
- **Lỗi lớp chữ Floyd**: Ω mã hoá thành "Æ", một số dấu "=" mất → `OCR_output/floyd/text/full_layout_omega_fixed.txt`. Câu có ký hiệu: luôn đọc ảnh trang.
- **Floyd không in đáp án** Self-Test / True-False / Circuit-Action (chỉ ghi pearsonhighered.com) → phải tự giải + kiểm chứng. Đáp án bài lẻ (Problems): pdf tr.949–961. pdf = trang in + 18.
- **Bản đồ đề cương → chương** (`build/modules.py`, hiển thị ở trang `sources/`): 10 module m01–m10.
- **Khung site** song ngữ (vi/ en/), deck, quiz, ngân hàng câu hỏi có lọc/làm lại, luyện đề tính giờ, trang nguồn; theme màu USTH; `tests/site_test.js` (Playwright).
- **Quy chuẩn** cho từng module: `AGENT_BRIEF.md` (schema JSON câu hỏi, verify, notebook, chất lượng).

## Trang EASA cần dùng (số trang PDF)

SM01 IC/logic p55–75 (ghép tầng/hồi tiếp p49–54), câu hỏi p76,78,80,82,84,86 – đáp án p77…87 ·
SM02 PCB p88–97, Q p98,100 – A p99,101 · SM03 Servo p102–114, Q p116,118 – A p117,119.

## Tiến độ từng module

Xem `data/verify/PROGRESS_*.md` (mỗi nhóm module có file riêng: đã làm gì, còn thiếu gì, bước tiếp).
Bảng tổng: chạy `python3 build/assemble.py` → in số câu gốc/bổ sung mỗi module và `data/qbank/_audit.json`.

## Cách làm tiếp (mỗi module mXX)

1. Đọc `AGENT_BRIEF.md` + `data/verify/PROGRESS_*.md` của module.
2. Hoàn thiện theo đúng danh sách file:
   `build/content/mXX.py` · `data/qsrc/mXX.json` (câu gốc) · `build/gen/gen_mXX.py` → `data/qsrc/mXX_gen.json` (câu sinh) ·
   `build/verify/verify_mXX.py` (assert đáp án) · `data/verify/mXX_notes.json` (lỗi sách) · `build/nb/make_mXX.py` → `notebooks/mXX_*_{vi,en}.ipynb` (chạy `jupyter nbconvert --execute --inplace`).
3. Dựng: `ONLY=mXX python3 build/assemble.py && ONLY=mXX python3 build/build_site.py` (bỏ `ONLY` để dựng tất cả).
4. Kiểm thử: `python3 -m http.server 8765` ở thư mục này, rồi `node tests/site_test.js`.
5. Deploy: chép thư mục `Electronics-2/` vào repo `for-VAQ-USTH` (giữ `.nojekyll` ở gốc repo), push → `https://tatcataittn.github.io/for-VAQ-USTH/Electronics-2/`.

## Prompt gợi ý để tiếp tục trong phiên mới

"Giải nén Electronics-2.zip, đọc CONTINUE.md, AGENT_BRIEF.md và data/verify/PROGRESS_*.md, rồi hoàn thiện các module còn thiếu theo đúng quy chuẩn; nguồn PDF ở Drive folder 1Gd37QKLz37eMqwB9KT79aqZKefgr8_q4 (tải bằng drive.usercontent.google.com/download?id=…&export=download&confirm=t)."
