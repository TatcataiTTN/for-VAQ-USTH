# Trạng thái & cách làm tiếp — AE2.025 Electronics 2

## Đã xong (10/10 module, song ngữ VI/EN)
| Module | Nguồn chính | Câu hỏi đóng (gốc + bổ sung) | Bài có lời giải | Cách kiểm chứng |
|---|---|---|---|---|
| m01 IC & logic | EASA M04 SM01 (Q1-23…1-46) | 79 | 24 | 57 câu đối chiếu trang EASA, 46 câu tính lại bằng script |
| m02 Op-amp | Floyd ch.12 | 165 (51 gốc) | 13 | `build/verify/verify_m02.py` (100 câu số) + đáp án lẻ của sách |
| m03 Mạch op-amp cơ bản | Floyd ch.13 | 111 (33 gốc) | 14 | `verify_m03.py` (59 câu số) |
| m04 Ghép tầng & hồi tiếp | Floyd §6-6, §7-2 + EASA SM01 tr.49-53 | 89 | 9 | `verify_m04.py` (33 chứng cứ EASA + 43 câu số) |
| m05 Op-amp chuyên dụng | Floyd ch.14 | 104 (32 gốc) | 12 | `verify_m05.py` (56 câu số) |
| m06 Bộ lọc tích cực | Floyd ch.15 | 126 (43 gốc) | 10 | `verify_m06.py` (58 câu số) |
| m07 Dao động & 555 | Floyd ch.16 | 117 (36 gốc) | 11 | `verify_m07.py` (60 câu số) |
| m08 Ổn áp | Floyd ch.17 | 103 (28 gốc) | 17 | `verify_m08.py` (54 câu số) |
| m09 PCB | EASA M04 SM02 | 89 | 13 | `verify_m09.py` (90 chứng cứ EASA + 12 câu số) |
| m10 Servo & synchro | EASA M04 SM03 + `SERVOMECHANISM (sv).pdf` | 105 | 15 | `verify_m10.py` (101 chứng cứ + 19 câu số) |

Mỗi module có: bài giảng 5 phần (VI/EN), ghi chú chi tiết với 5 ví dụ có lời giải số, ngân hàng câu hỏi (có giải thích, nguồn từng câu), luyện đề, notebook Jupyter VI+EN đã chạy sẵn, và `data/verify/mNN_notes.json` ghi lại lỗi/nghi vấn của sách (hiển thị ở trang Nguồn & đối chiếu).

## Chưa làm / hạn chế đã biết
- **Jaeger 5e** (Ch.6–7, 9 cho m01; Ch.10–12 cho m02–m07) mới chỉ được ánh xạ chương, chưa đọc để trích câu hỏi. Chỉ ghi “đọc thêm”, không trích trang.
- **Floyd không in đáp án** Self-Test, True/False, Circuit-Action: toàn bộ do ta tự giải; câu mơ hồ đã loại và ghi trong `mNN_notes.json`.
- Circuit-Action của Floyd gắn với Hình 6–34, 7–5 (m04) chưa đưa vào (cần cắt hình).
- EASA OCR không đạt 100 %: trang câu hỏi EASA đã đối chiếu bằng script; các trang khác xem `pdf_ocr_fixed/REPORT.md`.

## Quy trình
1. `python3 build/assemble.py && python3 build/build_site.py` (thêm `ONLY=mNN` để dựng một module).
2. Kiểm chứng: `python3 build/verify/verify_mNN.py` (phải in `FAILS: none`).
3. Kiểm thử trình duyệt: `python3 -m http.server 8765` ở thư mục này, rồi `python3 tests/site_test.py` (Playwright + Chrome).
4. Đẩy lên GitHub: `build/push.sh "thông điệp commit"` (đồng bộ vào bản clone `for-VAQ-USTH`, commit, push). Site: https://tatcataittn.github.io/for-VAQ-USTH/Electronics-2/
