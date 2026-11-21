# -*- coding: utf-8 -*-
"""Trang Thuat ngu VI-EN: bang co o tim kiem (JS thuan), cot module co lien ket."""
import json, os
from hx import esc
from modules import BYID
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def body(lang):
    vi = lang == 'vi'; g = json.load(open(os.path.join(ROOT, 'data', 'glossary.json'), encoding='utf-8'))
    h = f'<h1>{"Thuật ngữ VI–EN" if vi else "Glossary VI–EN"}</h1><p class="lead">' + (f'{len(g)} thuật ngữ của 10 module, tiếng Việt kèm tiếng Anh. Gõ vào ô để lọc theo bất kỳ cột nào.' if vi else f'{len(g)} terms from the 10 modules, English with Vietnamese. Type in the box to filter on any column.') + '</p>'
    h += f'<input id="gloss-q" type="search" placeholder="{"Tìm thuật ngữ..." if vi else "Search a term..."}" style="width:100%;max-width:420px;padding:8px 10px;border:1px solid var(--border);border-radius:8px;margin:6px 0 10px">'
    h += f'<div class="tablewrap"><table class="t left" id="gloss"><tr><th>English</th><th>Tiếng Việt</th><th>{"Định nghĩa" if vi else "Definition"}</th><th>Module</th></tr>'
    for t in sorted(g, key=lambda t: t['en'].lower()):
        mods = ', '.join(f'<a href="../modules/{BYID[m]["slug"]}/index.html">{m.upper()}</a>' for m in t['modules'])
        h += f'<tr><td><b>{esc(t["en"])}</b></td><td>{esc(t["vi"])}</td><td>{t["def_vi"] if vi else t["def_en"]}</td><td>{mods}</td></tr>'
    return h + '</table></div><script src="../../_shared/glossary.js"></script>'
