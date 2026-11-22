# -*- coding: utf-8 -*-
"""Khung chung dung module 12 den 15: gom cac phan (part) -> trang module. Moi slide la bo 6 chuoi (tieu de vi, en, than vi, en, giai thich vi, en).
parts: [(title (vi, en), bullets [(vi, en)], slides [(tv, te, bv, be, ev, ee)])]; exs: [((tieu de vi, en), (noi dung vi, en), ket qua)]."""
from hx import *
def build(parts, exs, subtitle, objectives, srcnote, warns=None):
    out = []
    for (t, bl, slides) in parts:
        out.append(dict(title=tr(*t), bullets=[tr(*b) for b in bl], slides=[sl(tr(bv, be), title=tr(tv, te), explain=tr(ev, ee)) for (tv, te, bv, be, ev, ee) in slides]))
    notes = '<h3>' + tr('Năm ví dụ có số', 'Five worked examples') + '</h3>' + ''.join(ex(tr(*a), '<p>' + tr(*b) + '</p><p><b>' + tr('Kết quả (kiểm bằng chương trình)', 'Result (checked by program)') + f':</b> {r}</p>') for a, b, r in exs)
    notes += callout('info', tr('Ánh xạ nguồn', 'Source mapping'), '<p>' + tr(*srcnote) + '</p>')
    if warns: notes += callout('warn', tr('Điểm cần lưu ý của nguồn', 'Points to note in the sources'), ul([tr(*w) for w in warns]))
    return dict(subtitle=tr(*subtitle), objectives_title=tr('Sau module này bạn sẽ', 'After this module you will'), objectives=[tr(*o) for o in objectives], parts=out, notes=notes, notes_title=tr('Ghi chú chi tiết', 'Detailed notes'))
