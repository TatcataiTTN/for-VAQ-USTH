# -*- coding: utf-8 -*-
"""Trang Khai niem (Concept finder): moi chu de cua ngan hang la mot khai niem; du lieu o {lang}/data/search.json (build/tools_data.py)."""
def body(lang):
    vi = lang == 'vi'
    return (f'<h1>{"Khái niệm" if vi else "Concept finder"}</h1><p class="lead">' + ('Tìm một khái niệm của môn rồi vào thẳng phần luyện tập của chủ đề đó. Mỗi khái niệm là một chủ đề trong ngân hàng câu hỏi (module × chủ đề), kèm số câu theo mức, câu mẫu và thuật ngữ liên quan. Gõ không dấu cũng tìm được.' if vi else
            'Find a concept of the course and jump straight into practice on that topic. Each concept is a topic of the question bank (module × topic) with the number of questions by level, sample questions and related terms. Accent-free typing works.') + '</p><div id="concepts"></div>')
