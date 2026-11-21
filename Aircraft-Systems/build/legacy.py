# -*- coding: utf-8 -*-
"""Bo chuyen noi dung module CU (data/module_content.py + data/slides_NN.py) sang cau truc cua pipeline moi:
module(mid, lang) -> dict(subtitle, objectives_title, objectives, parts=[dict(title, bullets, slides=[html])], notes=html).
Nguon van la cac file cu (khong chep lai); tung module se duoc viet lai theo chuan moi o P4 va khi do tro thanh build/content/mNN.py."""
import os, sys, importlib, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'data'))
import hx
from hx import sl, callout, ul
from module_content import MODULES
from modules import BYID

NUM2ID = {m['num']: 'm' + m['num'] for m in MODULES}
BYNUM = {m['num']: m for m in MODULES}

def _load(num):
    m = BYNUM[num]
    try: sm = importlib.import_module(f'slides_{num}')
    except ModuleNotFoundError: sm = None
    if sm:
        for lang in ('vi', 'en'):
            ps = sm.SLIDES.get(lang, [])
            for i, part in enumerate(m[lang]['parts']):
                if i < len(ps): part['slides'] = ps[i]
    return m

def _slide(lang, cs, part_i, num, R):
    """Mot slide noi dung cu -> html (tieu de, than, anh slide goc neu co, giai thich cho nguoi moi)."""
    img = ''
    if cs.get('img'):
        src = f'{R}assets/figures/{cs["img"]}'
        cap = 'Bấm vào ảnh để phóng to' if lang == 'vi' else 'Click the image to enlarge'
        img = f"<figure class='slide-fig'><a href='{src}' target='_blank' rel='noopener'><img src='{src}' alt='{html.escape(cs['title'], quote=True)}' loading='lazy'/></a><figcaption>{cap}</figcaption></figure>"
    return sl(cs['body'] + img, kicker=f"{'PHẦN' if lang == 'vi' else 'PART'} {part_i}/5 · {num}", title=cs['title'], explain=cs.get('explain'))

def module(mid, lang):
    num = mid[1:]; m = _load(num); d = m[lang]; hx.LANG = lang; R = '{R}'
    t = dict(vi=dict(formula='Công thức', hist='Bối cảnh lý thuyết và lịch sử', case='Case study', warn='Bẫy hay gặp và lỗi của nguồn', part='PHẦN'),
             en=dict(formula='Formula', hist='Theory and history', case='Case study', warn='Common traps and source errors', part='PART'))[lang]
    parts = []
    for i, p in enumerate(d['parts'], 1):
        parts.append(dict(title=p['title'], bullets=p['bullets'], slides=[_slide(lang, cs, i, num, R) for cs in p.get('slides', [])]))
    # cac slide tong ket cua deck cu (cong thuc, lich su, case, bay) dua vao phan cuoi de giu nguyen noi dung
    legend = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in d['legend'])
    tail = [sl(f"<div class='pd-formula'><div class='pd-formula-label'>{d['formula_label']}</div><div class='pd-formula-math'>{d['formula_math']}</div></div><ul class='pd-legend'>{legend}</ul>",
               kicker=f"{t['part']} · {t['formula']}", title=d['formula_label']),
            sl(f"<p>{d['history']}</p>", kicker='📜 ' + t['hist'], title=d['history_title']),
            sl(f"<p>{d['case']}</p>", kicker='🔎 ' + t['case'], title=d['case_title']),
            sl(f"<p>{d['warn']}</p>", kicker='⚠️ ' + t['warn'], title=d['warn_title'])]
    parts[-1]['slides'] += tail
    notes = ''
    demo = m.get('demo')
    if demo: notes += demo['html_' + lang]
    return dict(subtitle=d['intro'], objectives_title=('Nội dung bài giảng (5 phần)' if lang == 'vi' else 'Lecture outline (5 parts)'),
                objectives=[p['title'] for p in d['parts']], parts=parts, notes=notes, notes_title=(('Demo chạy trong trình duyệt' if lang == 'vi' else 'In-browser demos') if demo else None), demo_js=(demo or {}).get('js'), notebook_desc=d.get('notebook_desc', ''))
