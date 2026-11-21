"""Page shell (bilingual). Every page lives in vi/... or en/... with a mirror in the other language.
Navigation has four groups only (Learn / Practise / Tools / Sources): lesson from the 12-link flat bar of AE2.025 that took four rows at 390 px."""
import os, json
import hx
from hx import esc
from modules import COURSE, BOOKS, MODS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def nav_groups(lang):
    vi = lang == 'vi'
    return [
        ('Học' if vi else 'Learn', [('Trang chủ' if vi else 'Home', 'index.html')] +
            [(f'{m["id"].upper()} · {m[lang]}', f'modules/{m["slug"]}/index.html') for m in MODS]),
        ('Luyện' if vi else 'Practise', [('Ngân hàng câu hỏi' if vi else 'Question bank', 'practice/index.html'), ('Luyện đề thi thử' if vi else 'Mock exams', 'exam/index.html'),
                                          ('Viết tay (tự luận)' if vi else 'Written practice', 'written/index.html')]),
        ('Công cụ' if vi else 'Tools', [('Khái niệm' if vi else 'Concept finder', 'concepts/index.html'), ('Thuật ngữ VI-EN' if vi else 'Glossary VI-EN', 'glossary/index.html'),
                                         ('Tóm tắt công thức' if vi else 'Formula sheet', 'formulas/index.html'), ('Bài tập có đáp án' if vi else 'Exercise finder', 'exercises/index.html'),
                                         ('Phân tích đề' if vi else 'Question analyser', 'analyse/index.html')]),
        ('Nguồn' if vi else 'Sources', [('Slide của giảng viên' if vi else 'Lecturer slides', 'slides/index.html'), ('Bản đồ sách' if vi else 'Book map', 'books/index.html'),
                                         ('Nguồn, độ phủ, lỗi của nguồn' if vi else 'Sources, coverage, source errors', 'sources/index.html')]),
    ]

FOOT = {
    'vi': 'Tài liệu tự học không chính thức cho học phần AE2.021 Hệ thống điện tử: hệ thống analog và hệ thống kỹ thuật số (USTH), bám đề cương, slide của giảng viên và hai giáo trình có file (Tooley, Floyd). '
          'Câu hỏi gốc được trích từ slide và sách (ghi nguồn từng câu); đáp án được tính lại bằng chương trình. Tài liệu [3] AeroGATES và [4] VAR Part 7 của đề cương không có trong bộ nguồn nên không được trích. '
          'Nội dung gốc thuộc tác giả, nhà xuất bản và giảng viên tương ứng.',
    'en': 'Unofficial self-study material for USTH course AE2.021 Electronics Systems: Analog Systems and Digital Systems, following the syllabus, the lecturer\'s slides and the two textbooks that are available (Tooley, Floyd). '
          'Original questions are quoted from the slides and books (source shown per question); answers were recomputed by script. References [3] AeroGATES and [4] VAR Part 7 of the syllabus are not in the source set and are not quoted. '
          'Original content belongs to its authors, publishers and the lecturer.',
}

def page(title, body, lang, relpath, desc='', scripts=(), css=()):
    """relpath: path of this page inside the language tree, e.g. 'modules/02-gas-power-cycles/index.html'."""
    depth = relpath.count('/') + 1          # +1 for the vi/ or en/ folder
    r = '../' * depth
    lr = '../' * (depth - 1)                  # root of the language tree
    other = 'en' if lang == 'vi' else 'vi'
    groups = ''.join(f'<details class="navgrp"><summary>{esc(g)} ▾</summary><div class="pop">' + ''.join(f'<a href="{lr}{u}">{esc(t)}</a>' for t, u in items) + '</div></details>' for g, items in nav_groups(lang))
    sw = f'<a class="lang-sw" href="{r}{other}/{relpath}">{"🇬🇧 EN" if lang == "vi" else "🇻🇳 VI"}</a>'
    th = ('<button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><button data-set-theme="ocean">Ocean</button><hr>'
          '<button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button>') if lang == 'vi' else \
         ('<button data-set-theme="light">Light</button><button data-set-theme="dark">Dark</button><button data-set-theme="sepia">Sepia</button><button data-set-theme="ocean">Ocean</button><hr>'
          '<button data-set-font="14px">Small text</button><button data-set-font="16px">Medium text</button><button data-set-font="19px">Large text</button>')
    srcs = ''.join(f'<li>[{b["syllabus_ref"]}] {esc(b["full"])}</li>' for b in sorted(BOOKS.values(), key=lambda b: b["syllabus_ref"]))
    sc = ''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    cs = ''.join(f'<link rel="stylesheet" href="{r}_shared/{c}">' for c in css)
    body = body.replace('{R}', r)
    brand = f'{COURSE["code"]} · {COURSE["title_short_" + lang]}'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {esc(brand)}</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="icon" href="{r}assets/images/usth_logo.png"><link rel="stylesheet" href="{r}_shared/vendor/katex/katex.min.css"><link rel="stylesheet" href="{r}_shared/common.css">{cs}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{lr}index.html"><img src="{r}assets/images/usth_logo.png" alt="USTH"><span>{esc(brand)}</span></a><nav>{groups}{sw}
<details class="menu"><summary>🎨</summary><div class="pop">{th}</div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p><b>{"Tài liệu tham khảo của đề cương" if lang == "vi" else "References of the syllabus"}:</b></p><ul style="margin:.3em 0 .8em;padding-left:1.2em">{srcs}</ul><p>{FOOT[lang]}</p></div></footer>
<script src="{r}_shared/vendor/katex/katex.min.js"></script><script src="{r}_shared/vendor/katex/auto-render.min.js"></script>
<script src="{r}_shared/i18n.js"></script><script src="{r}_shared/theme.js"></script><script src="{r}_shared/nav.js"></script>{sc}<script src="{r}_shared/math.js"></script></body></html>'''

def nodash(t):
    """Quy tac noi dung: khong dung gach ngang dai/ngan. So-so (Hinh 11-78, tr.25-38) giu gach noi; dau ngang dai trong cau doi thanh dau phay."""
    return t.replace('\u2013', '-').replace(' \u2014 ', ', ').replace('\u2014', ', ')

def write(relpath, content):
    content = nodash(content)
    p = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)
