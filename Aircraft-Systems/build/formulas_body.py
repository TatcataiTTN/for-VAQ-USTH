# -*- coding: utf-8 -*-
"""Trang Tom tat cong thuc: cong thuc KaTeX theo module, co loc theo module."""
import json, os
from hx import esc
from modules import BYID, MODS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LATEX_EN = [('\\text{đến}', '\\text{to}'), ('\\text{không dấu}', '\\text{unsigned}'), ('\\text{bù hai}', "\\text{two's complement}"), ('\\text{bát phân}', '\\text{octal}'), ('\\text{thập lục phân}', '\\text{hexadecimal}'), ('\\text{đầu vào}', '\\text{inputs}'),
            ('\\text{đầu ra}', '\\text{outputs}'), ('\\text{số ô}', '\\text{cells}'), ('\\text{hàm}', '\\text{functions}'), ('\\text{chu kỳ}', '\\text{cycles}'), ('0{,}7', '0.7'), ('1{,}1', '1.1'), ('1{,}44', '1.44'), ('13{,}04', '13.04'), ('12{,}5', '12.5'), ('2{,}56', '2.56'), ('0{,}32', '0.32')]
SRC_EN = [('Phương trình', 'Equation'), ('Bài giảng cáp quang', 'Optic fibre slides'), ('Bài giảng EMC', 'EMC slides'), ('bài giảng EMC', 'EMC slides'), ('bài giảng', 'lecture'), ('Bảng', 'Table'), ('slide 28 in thiếu hệ số', 'slide 28 omits the factor'),
          ('Công thức chuẩn, dùng ở Module 09', 'Standard formula used in Module 09'), ('đối chiếu', 'compared with'), ('minh hoạ của site', "the site's illustration")]
def tex(latex, lang):
    if lang == 'vi': return latex
    for a, b in LATEX_EN: latex = latex.replace(a, b)
    return latex
def en_src(t, lang):
    if lang == 'vi': return t
    for a, b in SRC_EN: t = t.replace(a, b)
    return t
def body(lang):
    vi = lang == 'vi'; fs = json.load(open(os.path.join(ROOT, 'data', 'formulas.json'), encoding='utf-8'))
    h = f'<h1>{"Tóm tắt công thức" if vi else "Formula sheet"}</h1><p class="lead">' + (f'{len(fs)} công thức theo module, mỗi công thức đã được dùng và kiểm trong module tương ứng (demo, notebook hoặc chương trình kiểm). Chưa gắn số slide.' if vi else f'{len(fs)} formulas by module, each used and checked in the matching module (demo, notebook or verification program). Slide numbers are not attached yet.') + '</p>'
    cur = None
    for f in fs:
        if f['module'] != cur:
            cur = f['module']; m = BYID[cur]; h += f'<h2 id="{cur}"><a href="../modules/{m["slug"]}/index.html">{cur.upper()}</a> · {esc(m[lang])}</h2>'
        lg = f['legend'][lang]
        h += f'<div class="pd-formula"><div class="pd-formula-label">{esc(f["name"][lang])}</div><div class="pd-formula-math">$${tex(f["latex"], lang)}$$</div></div>' + (f'<p class="srcnote">{lg}</p>' if lg else '') + f'<p class="srcnote">{"Nguồn" if vi else "Source"}: {esc(en_src(f["src"], lang))}</p>'
    return h
