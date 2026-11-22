# AGENT_BRIEF — AE2.021 Aircraft-Systems

Đọc `CONTINUE.md` trước. Prompt gốc: `../ULTIMATE_PROMPT_AE2.021_Aircraft_Systems.md` (luật R1–R13, quy trình P0–P9).

## Đường dẫn
- `$W` = `/Users/tuannghiat/Downloads/USTH - Aircraft Systems/`
- Clone git (đích push, dùng chung với Thermal-Systems, Electronics-2, Aerodynamics-Flight-Mechanics, mechanics-2): `$W/site/for-VAQ-USTH/`; chỉ sửa thư mục `Aircraft-Systems/`. Luôn `git pull --ff-only` trước khi sửa; không bao giờ `--force`.
- Bản làm việc: `$W/Aircraft-Systems/` (`scratch/`, `.venv/` không commit). Đồng bộ vào clone bằng `build/push.sh`; lần đầu `rsync -an --delete` rồi đọc danh sách.
- Pipeline cũ của site: `data/render_site.py` + `data/{module_NN,slides_NN,quiz_NN,quiz_xNN,notebook_NN}.py` → `vi|en/modules/…`, `data/quiz/*.json`, `data/notebooks/*.ipynb`. Chạy từ thư mục `data/`: `python3 build_quiz.py && python3 render_site.py && python3 check_links.py && python3 audit_quiz.py`.
- Công cụ kiểm kê: `scratch/audit/{inventory,crawl,shot}.py`.

## Quy ước cần nhớ
- Không dùng gạch ngang dài hay ngắn trong nội dung; không bịa số; ghi nguồn từng câu.
- Quiz EN phải có `opts_en`, `explain_en`, `src_en`, `detail_en` trong từng câu (cơ chế phủ ngoài từng làm lẫn chữ Việt).
- `data/qx.py` (`X`, `TF`) và `data/quiz_details.py` gắn lời giải chi tiết và câu bổ sung cho m05–m09; `balanced_seed` cân bằng vị trí đáp án đúng (m05 trở đi và nhóm tự sinh của m01–m04).
- Số Việt dùng dấu phẩy thập phân; số nhị phân, hex, mã, nhãn bus và số mục sách không bị bộ đổi số chạm vào.
- Ghi lỗi của slide/sách vào `data/verify/mNN_notes.json` (chưa tạo); hiện đang nằm rải rác trong `TASKS.md` và trường `warn` của `data/module_NN.py`.

## Lỗi/không khớp nguồn đã biết (chưa kiểm lại, theo prompt R3)
Floyd Ch.2 bài 5(c), 29(b), 37(g); Ch.3 bài 31; Ch.4 bài 21(b), 61, 67 (mã 1010); Ch.4 bài 3, 15; Ch.6 bài 25, 27, 29; Self-Test #28 Ch.13 (khoá in (b), đúng (d)); Tooley Ch.11 khoá câu 4 mâu thuẫn câu 2; slide EMC 21 (10 kW, đúng 100 kW); slide Optic_Fiber 9, 19, 24–26, 28, 30; slide Electronic displays; đề cương ghi Tooley 2007 nhưng file là Third Edition; thiếu [3] AeroGATES và [4] VAR Part 7.

## Thêm sau 22/11/2026 (đợt 2)
- Ngân hàng câu hỏi: nguồn `data/qsrc/mNN*.json` (đã là NGUỒN SỰ THẬT; `data/quiz/` chỉ lưu trữ). Sinh bằng `build/gen/*.py`; riêng 8 đề Tooley Revision Papers: `python3 build/gen/make_rev.py` (dữ liệu `gen_rev_a/b/c.py`, vá câu cũ `gen_rev_fix.py`); phần vi điều khiển: `python3 build/gen/gen_m04_mcu.py`. Sau đó `python3 build/assemble.py && python3 build/build_site.py`.
- Id câu = sha1(loại | đề tiếng Anh | đáp án đúng). Đổi chữ đề hay đáp án đúng đổi id. Trình duyệt lưu CHỈ SỐ lựa chọn, nên `data/published_ids.json` đóng băng thứ tự lựa chọn của câu đã lên web; `build/push.sh` cập nhật file này sau mỗi lần push.
- Khoá in sai của sách: dùng đáp án đúng, nhãn nguồn ghi "khoá in (x), đúng (y)", ghi trong `data/verify/mNN_notes.json`; mỗi script `build/verify/verify_*.py` phải in `FAILS: none`.
- Câu có hình: trường `fig` (đường dẫn từ gốc site). Hình Tooley Appendix 2 cắt bằng `scratch/rev_figs.py`.
- Không `sed -i` kiểu GNU trên macOS (dùng Python để sửa file).
