# -*- coding: utf-8 -*-
"""Trang ban chep slide cua giang vien (slides/<deck>.html): anh slide, ban chep VI/EN, cong thuc, so lieu, loi cua slide. Du lieu: data/slides/transcript/<deck>_*.json (build/transcripts)."""
import json, os, glob
from hx import esc
from modules import DECKS, MODS, BYID
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load(deck):
    fs = glob.glob(os.path.join(ROOT, 'data', 'slides', 'transcript', f'{deck}_*.json'))
    if not fs: return None
    d = json.load(open(fs[0], encoding='utf-8')); return {s['page']: s for s in d['slides']}

def split_issues(s):
    """(loi/nghi van, da kiem): muc bat dau bang 'Đã kiểm' la phep kiem khong phai loi."""
    errs = [x for x in s['issues'] if not x.startswith('Đã kiểm')]; chk = [x for x in s['issues'] if x.startswith('Đã kiểm')]
    return errs, chk

def all_transcripts():
    return {k: load(k) for k in DECKS if load(k)}

def owner(deck):
    for m in MODS:
        if any(d == deck for d, _, _ in m['slides']): return m['id']

def deck_body(lang, deck):
    vi = lang == 'vi'; T = load(deck); info = DECKS[deck]; n = info['pages']
    h = f'<div class="crumbs"><a href="index.html">{"Slide của giảng viên" if vi else "Lecturer slides"}</a> › {esc(info[lang])}</div><h1>{esc(info[lang])}</h1>'
    own = owner(deck)
    h += '<p class="lead">' + (f'Bản chép từng slide bằng tiếng Việt và tiếng Anh, đọc trực tiếp từ ảnh ({len(T)}/{n} slide). ' if vi else f'A Vietnamese and English transcript of each slide, read directly from the image ({len(T)}/{n} slides). ') + \
         (f'Module dùng bộ này: <a href="../modules/{BYID[own]["slug"]}/index.html">{own.upper()}</a>. ' if vi else f'Module using this deck: <a href="../modules/{BYID[own]["slug"]}/index.html">{own.upper()}</a>. ') + \
         ('Chỗ slide in sai hoặc không khớp được ghi riêng ở mục "Lỗi của slide"; bản chép giữ đúng như slide in.' if vi else 'Where a slide prints something wrong or inconsistent it is listed under "Slide errors"; the transcript keeps what the slide prints.') + '</p>'
    for p in range(1, n + 1):
        s = T.get(p)
        h += f'<section class="slide-tr" id="s{p}"><h3>{"Slide" if vi else "Slide"} {p}' + (f': {esc(s["title"])}' if s and s['title'] else '') + '</h3>'
        h += f'<a href="{{R}}assets/slides/{deck}/p{p:02d}.jpg" target="_blank" rel="noopener"><img class="slide-img" loading="lazy" src="{{R}}assets/slides/{deck}/p{p:02d}.jpg" alt="slide {p}"></a>'
        if s:
            h += f'<p>{esc(s["text_vi"] if vi else s["text_en"])}</p>'
            if s.get('basis'): h += '<p class="srcnote">' + ('Bản chép dạng tóm tắt từ lượt đọc ảnh slide trước (10/2026); chưa phóng to kiểm lại từng số.' if vi else 'Summary transcript from an earlier read of the slide image (10/2026); numbers not yet rechecked at high zoom.') + '</p>'
            if s['formulas']: h += '<p class="srcnote"><b>' + ('Công thức' if vi else 'Formulas') + ':</b> ' + ' · '.join(f'<code>{esc(x)}</code>' for x in s['formulas']) + '</p>'
            if s['numbers']: h += '<p class="srcnote"><b>' + ('Số liệu' if vi else 'Numbers') + ':</b> ' + '; '.join(esc(x) for x in s['numbers']) + '</p>'
            errs, chk = split_issues(s)
            if errs: h += '<div class="callout warn"><b class="t">' + ('Lỗi của slide và nghi vấn' if vi else 'Slide errors and doubts') + '</b><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in errs) + '</ul></div>'
            if chk: h += '<p class="srcnote"><b>' + ('Đã kiểm bằng tính' if vi else 'Checked by computation') + ':</b> ' + ' '.join(esc(x.replace('Đã kiểm: ', '').replace('Đã kiểm bằng Python: ', '')) for x in chk) + '</p>'
        else:
            h += '<p class="muted">' + ('Chưa đọc slide này.' if vi else 'This slide has not been read yet.') + '</p>'
        h += '</section>'
    return h
