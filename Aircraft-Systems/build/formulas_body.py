# -*- coding: utf-8 -*-
"""Trang Tom tat cong thuc: cong thuc KaTeX theo module, co loc theo module."""
import json, os
from hx import esc
from modules import BYID, MODS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def body(lang):
    vi = lang == 'vi'; fs = json.load(open(os.path.join(ROOT, 'data', 'formulas.json'), encoding='utf-8'))
    h = f'<h1>{"Tóm tắt công thức" if vi else "Formula sheet"}</h1><p class="lead">' + (f'{len(fs)} công thức theo module, mỗi công thức đã được dùng và kiểm trong module tương ứng (demo, notebook hoặc chương trình kiểm). Chưa gắn số slide.' if vi else f'{len(fs)} formulas by module, each used and checked in the matching module (demo, notebook or verification program). Slide numbers are not attached yet.') + '</p>'
    cur = None
    for f in fs:
        if f['module'] != cur:
            cur = f['module']; m = BYID[cur]; h += f'<h2 id="{cur}"><a href="../modules/{m["slug"]}/index.html">{cur.upper()}</a> · {esc(m[lang])}</h2>'
        lg = f['legend'][lang]
        h += f'<div class="pd-formula"><div class="pd-formula-label">{esc(f["name"][lang])}</div><div class="pd-formula-math">$${f["latex"]}$$</div></div>' + (f'<p class="srcnote">{lg}</p>' if lg else '') + f'<p class="srcnote">{"Nguồn" if vi else "Source"}: {esc(f["src"])}</p>'
    return h
