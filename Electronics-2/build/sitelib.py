"""Page shell (bilingual). Every page lives in vi/... or en/... with a mirror in the other language."""
import os, json
import hx
from hx import esc
from modules import COURSE, BOOKS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DRIVE = 'https://drive.google.com/drive/folders/1Gd37QKLz37eMqwB9KT79aqZKefgr8_q4'
NAV = {
    'vi': [('Trang chủ', 'index.html'), ('Lộ trình', 'index.html#modules'), ('Luyện tập', 'practice/index.html'),
           ('Luyện đề', 'exam/index.html'), ('Nguồn & đối chiếu', 'sources/index.html')],
    'en': [('Home', 'index.html'), ('Modules', 'index.html#modules'), ('Practice', 'practice/index.html'),
           ('Mock tests', 'exam/index.html'), ('Sources & mapping', 'sources/index.html')],
}
FOOT = {
    'vi': 'Tài liệu tự học không chính thức cho học phần AE2.025 Điện tử học 2 (USTH), bám đề cương chính thức và ba nguồn tham khảo của học phần. '
          'Câu hỏi gốc được trích từ sách (ghi nguồn từng câu); đáp án được giải lại và kiểm chứng bằng chương trình (sách Floyd không in đáp án Self-Test). '
          'Nội dung gốc thuộc tác giả và nhà xuất bản tương ứng.',
    'en': 'Unofficial self-study material for USTH course AE2.025 Electronics 2, following the official syllabus and its three references. '
          'Original questions are quoted from the books (source shown per question); every answer was re-solved and checked by script (Floyd does not print Self-Test answers). '
          'Original content belongs to its authors and publishers.',
}

def page(title, body, lang, relpath, desc='', scripts=()):
    """relpath: path of this page inside the language tree, e.g. 'modules/02-op-amp/index.html'."""
    depth = relpath.count('/') + 1          # +1 for the vi/ or en/ folder
    r = '../' * depth
    lr = '../' * (depth - 1)                  # root of the language tree
    other = 'en' if lang == 'vi' else 'vi'
    nav = ''.join(f'<a href="{lr}{u}">{t}</a>' for t, u in NAV[lang])
    sw = f'<a class="lang-sw" href="{r}{other}/{relpath}">{"🇬🇧 EN" if lang == "vi" else "🇻🇳 VI"}</a>'
    th = ('<button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr>'
          '<button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button>') if lang == 'vi' else \
         ('<button data-set-theme="light">Light</button><button data-set-theme="dark">Dark</button><button data-set-theme="sepia">Sepia</button><hr>'
          '<button data-set-font="14px">Small text</button><button data-set-font="16px">Medium text</button><button data-set-font="19px">Large text</button>')
    srcs = ''.join(f'<li><a href="https://drive.google.com/file/d/{b["drive"]}/view" target="_blank" rel="noopener">{esc(b["full"])}</a></li>' for b in BOOKS.values())
    sc = ''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    body = body.replace('{R}', r)
    brand = f'{COURSE["code"]} · {COURSE[lang]}'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {esc(brand)}</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="icon" href="{r}assets/images/usth_logo.png"><link rel="stylesheet" href="{r}_shared/common.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="{lr}index.html"><img src="{r}assets/images/usth_logo.png" alt="USTH">{esc(brand)}</a><nav>{nav}{sw}
<details class="menu"><summary>🎨</summary><div class="pop">{th}</div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p><b>{"Nguồn" if lang == "vi" else "Sources"}:</b> <a href="{DRIVE}" target="_blank" rel="noopener">Google Drive</a></p><ul style="margin:.3em 0 .8em;padding-left:1.2em">{srcs}</ul><p>{FOOT[lang]}</p></div></footer>
<script src="{r}_shared/i18n.js"></script><script src="{r}_shared/theme.js"></script>{sc}</body></html>'''

def write(relpath, content):
    p = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)
