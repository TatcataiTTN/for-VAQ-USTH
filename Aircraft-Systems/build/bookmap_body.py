# -*- coding: utf-8 -*-
"""Trang Ban do sach (cap chuong): Tooley 20 chuong + 5 phu luc, Floyd 15 chuong; moi chuong thuoc module nao hoac 'ngoai pham vi'.
So trang in do ngay 21/11/2026: Tooley in = PDF - 14 (muc luc in, xac nhan tren trang dau chuong 3, 10, 13, 14, 15, 16); Floyd in = PDF - 1 (bookmark + so trang tren dau trang)."""
import json
from hx import esc, table, callout
from modules import MODS, BYID

# (so chuong, tieu de VI, tieu de EN, trang in dau, trang in cuoi, [module], ghi chu VI, ghi chu EN)
TOOLEY = [
 (1, 'Giới thiệu: dụng cụ bay, bố trí buồng lái', 'Introduction: flight instruments, cockpit layouts', 1, 24, ['m06'], '', ''),
 (2, 'Hệ đếm', 'Number systems', 25, 38, ['m01'], '', ''),
 (3, 'Chuyển đổi dữ liệu', 'Data conversion', 39, 52, ['m10'], 'Chưa có module (sắp có)', 'No module yet (planned)'),
 (4, 'Bus dữ liệu', 'Data buses', 53, 69, ['m05'], '', ''),
 (5, 'Mạch logic', 'Logic circuits', 70, 94, ['m02', 'm11'], '§5.1-5.5, 5.8 ở m02; §5.6-5.7 (đơn ổn, song ổn) ở m11 (sắp có)', '§5.1-5.5, 5.8 in m02; §5.6-5.7 (monostable, bistable) in m11 (planned)'),
 (6, 'Máy tính', 'Computers', 95, 115, ['m04'], '', ''),
 (7, 'CPU', 'The CPU', 116, 138, ['m04'], '', ''),
 (8, 'Mạch tích hợp', 'Integrated circuits', 139, 148, ['m03'], '', ''),
 (9, 'Logic MSI', 'MSI logic', 149, 164, ['m03'], '', ''),
 (10, 'Cáp quang', 'Fibre optics', 165, 177, ['m08'], 'Module cũ ghi tr.162; chương bắt đầu ở tr.165 (PDF 179)', 'The old module said p.162; the chapter starts on p.165 (PDF 179)'),
 (11, 'Màn hình', 'Displays', 178, 196, ['m06'], '', ''),
 (12, 'ESD (phóng tĩnh điện)', 'ESD', 197, 206, ['m09'], 'Sắp gắn vào m09 như phần mở rộng', 'To be added to m09 as an extension'),
 (13, 'Phần mềm', 'Software', 207, 217, ['m07'], '', ''),
 (14, 'EMC', 'EMC', 218, 237, ['m09'], '', ''),
 (15, 'Hệ thống avionics', 'Avionic systems', 238, 260, ['m06', 'm12'], '§15.1-15.3 (ACARS, EFIS, EICAS/ECAM) ở m06; §15.4-15.10 ở m12 (sắp có)', '§15.1-15.3 (ACARS, EFIS, EICAS/ECAM) in m06; §15.4-15.10 in m12 (planned)'),
 (16, 'Mạng dữ liệu tàu bay và AFDX', 'Aircraft data networks and AFDX', 261, 275, ['m13'], 'Sắp có', 'Planned'),
 (17, 'Hệ logic cỡ lớn và VHDL', 'Large-scale logic systems and VHDL', 277, 293, ['m14'], 'Sắp có', 'Planned'),
 (18, 'IMA (avionics mô-đun tích hợp)', 'Integrated modular avionics (IMA)', 294, 306, ['m13'], 'Sắp có', 'Planned'),
 (19, 'Hệ thống cabin', 'Cabin systems', 307, 316, ['m15'], 'Sắp có', 'Planned'),
 (20, 'Hệ thống thông tin tàu bay', 'Aircraft information systems', 317, 335, ['m15'], 'Sắp có', 'Planned'),
]
TOOLEY_APP = [('Phụ lục 1 Từ viết tắt', 'Appendix 1 Abbreviations', 336, 348), ('Phụ lục 2 Đề ôn tập (Revision papers)', 'Appendix 2 Revision papers', 349, 375), ('Phụ lục 3 Đáp án (ảnh quét)', 'Appendix 3 Answers (scanned image)', 376, 386),
              ('Phụ lục 4 Truyền nối tiếp RS-232', 'Appendix 4 Serial data: RS-232', 387, 390), ('Phụ lục 5 Bảng mã thập phân, bát phân, hex, nhị phân, ASCII', 'Appendix 5 Decimal/octal/hex/binary/ASCII values', 391, 393)]
FLOYD = [  # PDF page of the bookmark; printed = PDF - 1
 (1, 'Khái niệm mở đầu', 'Introductory Concepts', 16, 65, [], 'Ngoài phạm vi hiện tại (nền cho kiểm tra đầu vào)', 'Outside the current scope (prerequisite review)'),
 (2, 'Hệ đếm, phép tính và mã', 'Number Systems, Operations, and Codes', 66, 125, ['m01', 'm07'], '§2-12 mã lỗi ở m07', '§2-12 error codes in m07'),
 (3, 'Cổng logic', 'Logic Gates', 126, 191, ['m02'], '', ''),
 (4, 'Đại số Boolean và tối giản logic', 'Boolean Algebra and Logic Simplification', 192, 261, ['m02', 'm06'], 'Applied Logic (7 đoạn) ở m06', 'Applied Logic (seven-segment) in m06'),
 (5, 'Phân tích logic tổ hợp', 'Combinational Logic Analysis', 262, 313, ['m02'], '', ''),
 (6, 'Chức năng của logic tổ hợp', 'Functions of Combinational Logic', 314, 387, ['m03', 'm06', 'm09'], '§6-5, 6-8 ở m06; §6-11 ở m09', '§6-5, 6-8 in m06; §6-11 in m09'),
 (7, 'Latch, flip-flop và bộ định thời', 'Latches, Flip-Flops, and Timers', 388, 449, ['m11'], 'Sắp có', 'Planned'),
 (8, 'Thanh ghi dịch', 'Shift Registers', 450, 497, ['m11'], 'Sắp có', 'Planned'),
 (9, 'Bộ đếm', 'Counters', 498, 561, ['m11'], 'Sắp có', 'Planned'),
 (10, 'Logic khả trình', 'Programmable Logic', 562, 627, ['m11', 'm14'], 'Sắp có', 'Planned'),
 (11, 'Lưu trữ dữ liệu', 'Data Storage', 628, 697, ['m04', 'm07'], '§11-11 checksum ở m07', '§11-11 checksum in m07'),
 (12, 'Chuyển đổi và xử lý tín hiệu', 'Signal Conversion and Processing', 698, 739, ['m10'], 'Sắp có', 'Planned'),
 (13, 'Truyền dữ liệu', 'Data transmission', 740, 801, ['m05', 'm08', 'm09'], '§13-1 ở m08/m09; §13-6 đến 13-10 ở m05', '§13-1 in m08/m09; §13-6 to 13-10 in m05'),
 (14, 'Xử lý dữ liệu và điều khiển', 'Data Processing and Control', 802, 855, [], 'Chưa gán module (chưa kiểm xem có liên quan CO5)', 'Not assigned to a module (not yet checked against CO5)'),
 (15, 'Công nghệ mạch tích hợp', 'Integrated Circuit Technologies', 856, 895, ['m03', 'm09'], '§15-3 noise margin ở m09', '§15-3 noise margin in m09'),
]
def modlist(ids, lang):
    out = []
    for i in ids:
        m = BYID[i]; tag = '' if m['status'] == 'live' else (' (sắp có)' if lang == 'vi' else ' (planned)')
        out.append(f'<a href="../modules/{m["slug"]}/index.html">{i.upper()}</a>{tag}' if m['status'] == 'live' else f'{i.upper()}{tag}')
    return ', '.join(out) if out else ('ngoài phạm vi' if lang == 'vi' else 'out of scope')

def body(lang):
    vi = lang == 'vi'; h = f'<h1>{"Bản đồ sách" if vi else "Book map"}</h1>'
    h += '<p class="lead">' + ('Mỗi chương của hai giáo trình có file thuộc module nào. Cấp chương; cấp mục sẽ bổ sung ở P2. Số trang là TRANG IN của sách (Tooley: trang PDF trừ 14; Floyd: trang PDF trừ 1, đã đo trên đầu trang).' if vi else
        'Which module each chapter of the two available textbooks belongs to. Chapter level; section level comes later. Page numbers are the PRINTED pages (Tooley: PDF page minus 14; Floyd: PDF page minus 1, measured on page headers).') + '</p>'
    h += f'<h2 id="overview">{"Module ↔ chương sách" if vi else "Module ↔ book chapters"}</h2>'
    from mapping import MAPPING_ROWS
    rows = []
    for r in MAPPING_ROWS:
        mid = 'm' + r['module'].split(':')[0].strip()
        m = BYID[mid]
        rows.append([f'<b><a href="../modules/{m["slug"]}/index.html">{r["module"]}</a></b>', r['tooley'], (r.get('floyd_en', r['floyd']) if not vi else r['floyd']), r['note_vi'] if vi else r['note_en']])
    h += '<div class="tablewrap">' + table(['Module', 'Tooley (3rd ed.)', 'Floyd (11e)', 'Ghi chú' if vi else 'Note'], rows, 'left') + '</div>'
    h += f'<h2 id="tooley">Tooley, Aircraft Digital Electronic and Computer Systems (3rd ed.)</h2>'
    rows = [[str(n), esc(v if vi else e), f'{a}-{b}', modlist(ms, lang), esc(nv if vi else ne)] for n, v, e, a, b, ms, nv, ne in TOOLEY]
    rows += [['-', esc(v if vi else e), f'{a}-{b}', '-', ''] for v, e, a, b in TOOLEY_APP]
    h += '<div class="tablewrap">' + table(['Ch.', 'Tên' if vi else 'Title', 'Trang in' if vi else 'Printed pages', 'Module', 'Ghi chú' if vi else 'Note'], rows, 'left') + '</div>'
    h += '<h2 id="floyd">Floyd, Digital Fundamentals (11th ed.)</h2>'
    rows = [[str(n), esc(v if vi else e), f'{a - 1}-{b - 1}', modlist(ms, lang), esc(nv if vi else ne)] for n, v, e, a, b, ms, nv, ne in FLOYD]
    h += '<div class="tablewrap">' + table(['Ch.', 'Tên' if vi else 'Title', 'Trang in' if vi else 'Printed pages', 'Module', 'Ghi chú' if vi else 'Note'], rows, 'left') + '</div>'
    h += '<p class="srcnote">' + ('Đề cương liệt kê thêm [3] AeroGATES Module 05 và [4] VAR Part 7 M13.04: hai tài liệu này không có trong bộ nguồn nên không được ánh xạ hay trích dẫn.' if vi else 'The syllabus also lists [3] AeroGATES Module 05 and [4] VAR Part 7 M13.04: neither is in the source set, so neither is mapped or quoted.') + '</p>'
    return h
