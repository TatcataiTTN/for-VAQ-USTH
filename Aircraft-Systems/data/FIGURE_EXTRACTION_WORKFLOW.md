# Quy trình xử lý trang "khả nghi" (câu hỏi có hình vẽ tham chiếu, bảng số, phụ lục OCR hỏng)

Áp dụng phương pháp E ("đọc trực tiếp bằng mắt") từ skill `build-complete-self-study-system`
mục 0.2.1 — dùng khi OCR/text-layer không đủ tin cậy (câu hỏi kiểu "See Figure 5.30", bảng đáp án
phụ lục bị garble khi trích xuất text).

## Quy trình 6 bước

1. **Xác định trang khả nghi** — không phải trang OCR "trông có vẻ ổn" mà là:
   - Câu hỏi có cụm "See Figure X.YY" / "shown in Figure X.YY" trong text đã trích.
   - Trang phụ lục có bảng số/đáp án mà `pdftotext -layout` cho ra ký tự xáo trộn (dấu hiệu: nhiều
     dòng toàn chữ cái viết hoa dính liền không có khoảng trắng hợp lý).

2. **Render trang gốc ở DPI cao** (400–600, ưu tiên 600 nếu chữ nhỏ hoặc có chi tiết mạch điện mảnh):
   ```bash
   pdftoppm -r 600 -f <PAGE> -l <PAGE> -png "source.pdf" /tmp/page_render/p
   ```
   Dùng file PDF **gốc** (chưa force-ocr) nếu có, vì bản OCR rasterize lại có thể giảm chất lượng ảnh.

3. **Đọc toàn trang bằng mắt (vision)** — dùng tool `Read` với `pages` trên chính PDF gốc (không cần
   qua bước 2 nếu chỉ cần đọc, không cần crop) để xem đúng bố cục, đọc chính xác câu hỏi + đáp án +
   hình minh hoạ cùng lúc, tránh sai lệch do OCR.

4. **Xác định toạ độ vùng hình cần crop** — nhìn ảnh đã render, ước lượng khung chứa hình (tính theo
   % chiều rộng/cao trang, quy đổi ra pixel theo DPI đã dùng), hoặc dùng `magick identify` để lấy kích
   thước ảnh gốc rồi tính toạ độ:
   ```bash
   magick identify /tmp/page_render/p-1.png   # ra WxH pixel
   magick /tmp/page_render/p-1.png -crop <W>x<H>+<X>+<Y> +repage assets/figures/ten_hinh.png
   ```

5. **Xác minh lại ảnh đã crop** — đọc lại bằng `Read` (vision) để chắc chắn không cắt mất chú thích/số
   thứ tự hình, không bị lệch/thiếu góc.

6. **Ghi log truy vết** — với mỗi hình crop ra, ghi trong file nguồn dữ liệu: tên sách, chương, số hình
   gốc (vd "Tooley Figure 5.30"), số trang PDF, DPI đã dùng — để tái lập lại được nếu cần chỉnh sửa.

## Khi nào KHÔNG cần crop, chỉ cần đọc bằng mắt

Nếu hình chỉ giúp NGƯỜI VIẾT hiểu câu hỏi để tự diễn giải lại bằng chữ (vd sơ đồ logic đơn giản có thể mô
tả bằng bảng chân trị/lời văn tương đương) — ưu tiên diễn giải lại bằng chữ/bảng HTML sẵn có (`<table
class="tt">`) thay vì nhúng ảnh, giữ trang nhẹ và nhất quán giao diện. Chỉ crop ảnh thật khi hình có cấu
trúc mạch/sơ đồ phức tạp không thể diễn giải chính xác bằng chữ mà không mất thông tin.

## Công cụ dùng trong dự án này

- `pdftoppm` (poppler) — render trang PDF ra PNG độ phân giải tuỳ chỉnh.
- `magick`/`convert` (ImageMagick) — crop, đo kích thước ảnh.
- `Read` tool (Claude vision) — đọc trực tiếp trang PDF hoặc ảnh đã crop, đối chiếu với text đã OCR/trích
  xuất trước đó, phát hiện chỗ sai lệch (ví dụ đã dùng để xác nhận Floyd Self-Test Ch.2 Q10/Q11 bị lỗi
  trích xuất dấu trừ: "+122"/"−34" bị đọc nhầm thành "1122"/"234").

## Script tái sử dụng

Xem `data/render_pages.sh` — hàm tiện ích render nhanh 1 hoặc nhiều trang ở DPI chỉ định từ bất kỳ PDF
nào trong thư mục nguồn, xuất vào `/tmp/page_render/` để xem/crop mà không làm bẩn repo bằng ảnh trung
gian.
