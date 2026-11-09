# AE2.025 Electronics 2 — hệ thống tự học song ngữ (VI/EN)

Site: https://tatcataittn.github.io/for-VAQ-USTH/Electronics-2/  ·  10 module, 1.251 câu hỏi (gốc từ sách + bổ sung, trong đó 161 câu mức 3), notebook Jupyter, luyện đề tính giờ.

| Thư mục | Nội dung |
|---|---|
| `index.html`, `vi/`, `en/` | Site tĩnh: trang chủ, 10 module, luyện tập theo module, luyện đề, bản đồ nội dung sách (`books/`), nguồn & đối chiếu |
| `_shared/` | CSS/JS dùng chung (deck, quiz, ngân hàng câu hỏi, luyện đề, theme, i18n); cần `.nojekyll` ở gốc repo |
| `data/qsrc/` | Câu hỏi gốc + câu bổ sung (song ngữ); `data/qbank/` bản ghép + `_audit.json` (kiểm tra lệch đáp án) |
| `data/numeric/` | Catalog 5.636 bài tập của 4 quyển (`catalog.json`, `summary.json`), dựng bởi `build/numeric/`; `jaeger_solved.json` = 122 problem Jaeger không có đáp án in mà site đã giải và kiểm (21 bài giữ lại kèm lý do), từ `build/numeric/jsol/` và `solve_all.py`; kiểm bằng `build/verify/verify_jaeger_solved.py` |
| `exercises/`, `written/`, `concepts/` | Dữ liệu cho trang Tra cứu bài tập, Written Practice và Concept finder (`concepts/data.json`, dựng bởi `build/concepts_data.py` từ `build/concepts/`) |
| `data/bookmap/` | Mục lục 4 quyển + bản đồ module→sách (`map.json`), dựng bởi `build/bookmap/` |
| `data/verify/` | Ghi chú lỗi/nghi vấn của sách (`mNN_notes.json`) và chứng cứ trích dẫn (`mNN_evidence.json`) |
| `build/` | Script dựng site, `author/` (dữ liệu câu hỏi), `gen/` (bộ sinh), `verify/` (kiểm chứng), `nb/` (notebook), `content/` (bài giảng), `push.sh` |
| `notebooks/` | Jupyter notebook mỗi module (VI + EN), đã chạy sẵn |
| `tests/` | `site_test.py`, `books_test.py`, `tools_test.py`, `concepts_test.py`, `exam_test.py` (Playwright), `check_deck.py` |
| `CONTINUE.md` | Trạng thái, hạn chế và quy trình làm tiếp |

PDF nguồn đã được sửa lớp chữ nằm ngoài thư mục này (`../pdf_ocr_fixed/`); `OCR_output/` và `sources/` (nặng) không được đẩy lên GitHub.
Xem thử cục bộ: `python3 -m http.server` trong thư mục này rồi mở `/vi/`.
