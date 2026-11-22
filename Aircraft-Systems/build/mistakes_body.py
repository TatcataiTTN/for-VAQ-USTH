# -*- coding: utf-8 -*-
"""Trang So loi: cac cau lam sai o Ngan hang cau hoi va cac de (du lieu tu localStorage cua trinh duyet)."""
def body(lang):
    vi = lang == 'vi'
    return (f'<h1>{"Sổ lỗi" if vi else "Mistake log"}</h1><p class="lead">' + ('Các câu bạn làm sai ở lần làm gần nhất, gom từ Ngân hàng câu hỏi và các đề thi thử, nhóm theo module, kèm đáp án đúng và giải thích. Dữ liệu chỉ nằm trong trình duyệt này.' if vi else
            'The questions you got wrong at your latest attempt, gathered from the Question bank and the mock exams, grouped by module, with the correct answer and explanation. The data stays in this browser only.') + '</p><div id="mistakes"></div>')
