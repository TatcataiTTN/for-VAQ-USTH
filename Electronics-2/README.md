# AE2.025 Electronics 2 — hệ thống tự học song ngữ (VI/EN)

Đặt thư mục `Electronics-2/` vào repo `for-VAQ-USTH/` → URL `https://tatcataittn.github.io/for-VAQ-USTH/Electronics-2/`.

| Thư mục | Nội dung |
|---|---|
| `index.html`, `vi/`, `en/` | Site tĩnh: trang chủ, 10 module, luyện tập theo module, luyện đề, nguồn & đối chiếu |
| `_shared/` | CSS/JS dùng chung (deck, quiz, ngân hàng câu hỏi, luyện đề, theme, i18n) — cần file `.nojekyll` ở gốc repo |
| `data/qsrc/` | Câu hỏi gốc (sách) + câu sinh, song ngữ; `data/qbank/` bản ghép + `_audit.json` (kiểm tra lệch đáp án) |
| `build/` | Script dựng site: `python3 build/assemble.py && python3 build/build_site.py` |
| `build/verify/` | Script kiểm chứng đáp án; `data/verify/*_notes.json` lỗi/nghi vấn tìm thấy trong sách |
| `notebooks/` | Jupyter notebook mỗi module (VI + EN), đã chạy sẵn |
| `sources/easa_m04_ocr.pdf` | Bản EASA M04 đã OCR (chọn được chữ). Floyd/Jaeger gốc đã có lớp chữ, xem trong Drive |
| `OCR_output/` | Text trích xuất: Floyd (bản sửa Ω), Jaeger 5e, EASA 2 phương pháp OCR (ocrmypdf + tesseract psm4) |
| `AGENT_BRIEF.md` | Quy chuẩn nội dung/câu hỏi dùng khi dựng các module |

Xem thử cục bộ: `python3 -m http.server` trong thư mục cha rồi mở `/Electronics-2/`.
