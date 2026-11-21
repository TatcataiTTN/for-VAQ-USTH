# -*- coding: utf-8 -*-
"""Trang Nguon, do phu va loi cua nguon: tai lieu tham khao cua de cuong, bang do phu do tu du lieu, loi/nghi van cua nguon (data/verify/mNN_notes.json neu co; neu chua co thi lay truong `warn` cua module cu)."""
import os, json, sys
from hx import esc, table, callout
from modules import MODS, BOOKS, DECKS, BYID, slides_of
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'data'))

def jl(p):
    q = os.path.join(ROOT, p); return json.load(open(q, encoding='utf-8')) if os.path.exists(q) else None

def body(lang, banks):
    vi = lang == 'vi'; h = f'<h1>{"Nguồn, độ phủ và lỗi của nguồn" if vi else "Sources, coverage and source errors"}</h1>'
    h += f'<h2>{"Tài liệu tham khảo của đề cương" if vi else "References of the syllabus"}</h2>'
    rows = [[f'[{b["syllabus_ref"]}]', esc(b['full']), ('có file trong bộ nguồn' if b['pdf'] else 'KHÔNG có file: không trích, không suy đoán nội dung') if vi else ('file in the source set' if b['pdf'] else 'NO file: not quoted, content not guessed')]
            for b in sorted(BOOKS.values(), key=lambda b: b['syllabus_ref'])]
    h += table(['#', 'Tài liệu' if vi else 'Reference', 'Trạng thái' if vi else 'Status'], rows, 'left')
    h += f'<p class="srcnote">' + ('Đề cương ghi Tooley năm 2007 nhưng file trong bộ nguồn là bản Third Edition: ghi lại, không suy diễn thêm.' if vi else 'The syllabus says Tooley 2007 but the file in the source set is the Third Edition: recorded, nothing inferred.') + '</p>'
    h += f'<h2>{"Độ phủ (đếm từ dữ liệu)" if vi else "Coverage (counted from the data)"}</h2>'
    rows = []; tot = dict(s=0, q=0, g=0, e=0)
    for m in MODS:
        b = banks.get(m['id']); n = len(b['items']) if b else 0; g = sum(1 for i in b['items'] if i['origin'] == 'goc') if b else 0; e = len(b['essays']) if b else 0
        s = len(slides_of(m)); tot['s'] += s; tot['q'] += n; tot['g'] += g; tot['e'] += e
        st = ('có' if vi else 'live') if m['status'] == 'live' else ('sắp có' if vi else 'planned')
        rows.append([f'<a href="../modules/{m["slug"]}/index.html">{m["id"].upper()}</a>' if m['status'] == 'live' else m['id'].upper(), esc(m[lang]), st, str(s), str(n), str(g), str(n - g), str(e)])
    rows.append(['', '<b>' + ('Tổng' if vi else 'Total') + '</b>', '', str(tot['s']), str(tot['q']), str(tot['g']), str(tot['q'] - tot['g']), str(tot['e'])])
    h += '<div class="tablewrap">' + table(['', 'Module', 'Trạng thái' if vi else 'Status', 'Slide', 'Câu trắc nghiệm' if vi else 'MCQ', 'Gốc' if vi else 'Original', 'Bổ sung' if vi else 'Added', 'Tự luận' if vi else 'Worked'], rows, 'left') + '</div>'
    h += f'<h2>{"Lỗi và nghi vấn của nguồn" if vi else "Source errors and doubts"}</h2>'
    h += '<p class="srcnote">' + ('Gom từ ghi chú từng module. Mỗi mục nói rõ nguồn nào sai và site đã dùng giá trị nào. Chưa được kiểm lại hết bằng ảnh trang: xem CONTINUE.md.' if vi else 'Collected from the module notes. Each entry says which source is wrong and which value the site used. Not yet fully rechecked against page images: see CONTINUE.md.') + '</p>'
    try:
        from module_content import MODULES
    except Exception: MODULES = []
    for mm in MODULES:
        mid = 'm' + mm['num']; notes = (jl(f'data/verify/{mid}_notes.json') or {}).get(lang)
        h += f'<h3>{mid.upper()} · {esc(BYID[mid][lang])}</h3>'
        if notes: h += '<ul>' + ''.join(f'<li>{x}</li>' for x in notes) + '</ul>'
        else: h += '<div class="callout warn"><b class="t">' + (mm[lang]['warn_title']) + '</b><p>' + mm[lang]['warn'] + '</p></div>'
    mig = jl('data/verify/migration_notes.json') or {}
    if mig.get('source_fixes'):
        h += f'<h3>{"Sửa khi chuyển ngân hàng câu hỏi" if vi else "Fixes made while migrating the question bank"}</h3><ul>' + ''.join(f'<li><b>{esc(x["item"])}</b>: {esc(x["what"])}</li>' for x in mig['source_fixes']) + '</ul>'
    return h
