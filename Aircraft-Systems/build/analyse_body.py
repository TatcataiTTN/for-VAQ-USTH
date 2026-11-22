# -*- coding: utf-8 -*-
"""Trang Phan tich de: dan de bai, tim cau tuong tu bang TF-IDF trong trinh duyet, du doan chu de va muc, bao ngoai danh muc."""
def body(lang):
    vi = lang == 'vi'
    return (f'<h1>{"Phân tích đề" if vi else "Question analyser"}</h1><p class="lead">' + ('Dán một đề bài bất kỳ (tiếng Việt hoặc tiếng Anh) để xem nó giống những câu nào của ngân hàng, thuộc module và chủ đề nào, mức khoảng bao nhiêu. Nếu đề không giống câu nào, trang báo "ngoài danh mục". Mọi phép tính chạy trong trình duyệt của bạn; đề bạn dán không được gửi đi đâu.' if vi else
            'Paste any question (Vietnamese or English) to see which bank questions it resembles, its module and topic, and a rough level. If it resembles nothing the page says "out of scope". Everything runs in your browser; the question you paste is not sent anywhere.') + '</p><div id="analyse"></div>')
