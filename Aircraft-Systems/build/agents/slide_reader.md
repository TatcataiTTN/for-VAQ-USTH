# Brief: đọc từng slide của giảng viên và chép lại song ngữ (P0a)

Dự án: site tự học AE2.021 (USTH). Gốc: `$P = /Users/tuannghiat/Downloads/USTH - Aircraft Systems/Aircraft-Systems`. Python: `$P/.venv/bin/python -I` (có PyMuPDF `import pymupdf`, PIL, numpy). Không push GitHub, không sửa file ngoài đường dẫn ghi bên dưới, không `rm -rf`, `sudo`, `git`.

## Việc của bạn
Đọc BẰNG MẮT từng slide trong phạm vi được giao và ghi một file JSON `data/slides/transcript/<deck>_<từ>-<đến>.json`. Slide của giảng viên là infographic, `pdftotext` gần như vô dụng. Dùng tool Read trên ảnh.
- Ảnh có sẵn: `assets/slides/<deck>/pNN.jpg` (960 px). Với slide chữ nhỏ, mạch, bảng, chuỗi bit: render lại từ PDF ở độ phân giải cao hơn vào `scratch/slides_<deck>/` (ví dụ `pymupdf` zoom 2, cắt phần cần đọc). PDF nguồn: `../sources/lectures/<tên file>` (xem `build/modules.py` mục `DECKS`).
- Đọc từng slide một cách độc lập; không đoán từ slide kế bên.

## Định dạng (một phần tử trong `slides` cho mỗi trang)
```json
{"deck":"logic","range":[1,30],"slides":[
 {"page":1,"kind":"content|title|divider|blank|thanks",
  "title":"tiêu đề đúng như trên slide (tiếng Anh gốc; để rỗng nếu không có)",
  "text_en":"CHỮ trên slide (chép lại đủ ý, giữ số và đơn vị) rồi mô tả HÌNH: loại sơ đồ, nhãn, mũi tên, giá trị. 2 đến 8 câu, đủ để người học không cần mở ảnh vẫn hiểu slide nói gì.",
  "text_vi":"bản dịch tiếng Việt THẬT của text_en (dịch riêng, thuật ngữ chuẩn: hệ đếm, bù hai, đại số Boolean, bản đồ Karnaugh, bộ giải mã, bộ dồn kênh, bus dữ liệu, cáp quang, tương thích điện từ...). Dấu thập phân là dấu phẩy trong văn bản (0,7 V); chuỗi nhị phân/hex/mã/nhãn giữ nguyên.",
  "formulas":["công thức đúng như trên slide; chữ gạch trên viết \\overline{A}; chỉ số dưới A_{in}"],
  "numbers":["các số có đơn vị hoặc chuỗi bit quan trọng, ví dụ '2,0 V mức cao tối thiểu', '1011 0010'"],
  "issues":["lỗi, không khớp, chính tả, số sai, nhãn thiếu, kèm số trang và vì sao"]}
]}
```
## Luật cứng
1. Không bịa. Chỗ không đọc được: ghi `[không đọc rõ]` trong text và nêu ở `issues`. Không suy diễn nội dung từ tên slide.
2. Chuỗi nhị phân, thập lục phân, mã ASCII, nhãn bus, số hiệu: đọc từng ký tự; OCR hay nhầm 0 và O, 1 và l và I, 8 và B, 5 và S. Chữ gạch trên (NOT) hay bị mất: nhìn ảnh và ghi `\overline{...}`.
3. Không dùng gạch ngang dài hay ngắn (U+2014, U+2013) trong mọi trường văn bản: dùng dấu phẩy, hai chấm, hoặc gạch nối (-) cho khoảng số.
4. Lỗi của slide (sai chính tả, số không khớp phép tính, nhãn lệch, ví dụ đáp án sai) PHẢI vào `issues`, không sửa thầm trong `text_en`: `text_en` chép đúng như slide in.
5. Mỗi slide phải có `text_en` và `text_vi` không rỗng, kể cả slide tiêu đề (ghi tên bài giảng, tên giảng viên nếu có).
6. `kind`: `title` (bìa), `divider` (ngăn chương chỉ có tiêu đề), `blank` (trống), `thanks` (cảm ơn), còn lại `content`.
7. Ghi file bằng một lần ghi nguyên tử (viết ra `.tmp` rồi `os.replace`). Khi xong chạy kiểm: `.venv/bin/python -I build/verify/check_transcripts.py data/slides/transcript/<file>.json` phải in `OK`.

## Báo cáo cuối (tiếng Việt, tối đa 150 từ)
Số slide đã đọc/tổng, số slide có `issues`, danh sách lỗi quan trọng nhất của slide (kèm số trang), số slide bạn không đọc chắc (kèm số trang), đường dẫn file đã ghi. Không dán lại nội dung file.
