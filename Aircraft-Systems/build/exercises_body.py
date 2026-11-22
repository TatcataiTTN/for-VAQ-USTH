# -*- coding: utf-8 -*-
"""Trang Bai tap co dap an (Exercise finder) va Viet tay (Written practice); du lieu o {lang}/data/."""
def exercises_body(lang):
    vi = lang == 'vi'
    return (f'<h1>{"Tra cứu bài tập có đáp án" if vi else "Exercise finder"}</h1><p class="lead">' + ('Mọi bài tập của site trong một bảng: câu gốc của sách (có đáp án in) xếp trước, câu bổ sung sau. Lọc theo sách, module, loại, mức; bấm mũi tên để mở đúng câu trong ngân hàng. Cuối trang là số bài theo từng chương Tooley và Floyd.' if vi else
            'Every exercise of the site in one table: original book questions (with a printed answer) first, added questions after. Filter by book, module, kind and level; click the arrow to open the exact item in the bank. At the bottom: the number of exercises per Tooley and Floyd chapter.') + '</p><div id="exercises"></div>')
def written_body(lang):
    vi = lang == 'vi'
    return (f'<h1>{"Viết tay (tự luận)" if vi else "Written practice"}</h1><p class="lead">' + ('Các bài tự luận có đáp án in của sách và các bài bổ sung có lời giải tính bằng chương trình. Làm nháp ở ô ghi chú, bấm "Xem lời giải", rồi tự đánh dấu "Tôi làm được". Đề tự luận có tính giờ nằm ở trang Luyện đề thi thử.' if vi else
            'Worked problems with the printed answer of the books and added problems whose solutions were computed by program. Draft in the notes box, press "Show solution", then mark "I can do it" yourself. Timed written papers are on the Mock exams page.') + '</p><div id="written"></div>')
