"""Render every page of the lecturer's slide decks to assets/slides/<deck>/pNN.jpg (960 px wide, JPEG q72) and write data/slides/index.json (deck, page, title, kind).
Run:  python3 -I build/slides/render_slides.py   (needs pdftoppm; PDFs are in the parent folder of the project)"""
import os, sys, re, json, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.abspath(os.path.join(HERE, '..', '..')); SRC = os.path.dirname(P)
sys.path.insert(0, os.path.join(P, 'build'))
from modules import DECKS
def titles(md):
    t = open(os.path.join(SRC, 'OCR_output', md), encoding='utf-8').read()
    parts = re.split(r'^## \[Trang (\d+)\]\s*$', t, flags=re.M); out = {}
    for i in range(1, len(parts), 2):
        body = parts[i + 1].strip(); title = ''
        for l in body.splitlines():
            l = l.strip()
            if l and not l.startswith('**[') and not l.startswith('---') and not l.startswith('_(không'): title = l; break
        out[int(parts[i])] = (title, len(body))
    return out
index = []
for key, info in DECKS.items():
    d = os.path.join(P, 'assets', 'slides', key); os.makedirs(d, exist_ok=True)
    pdf = os.path.join(SRC, info['pdf'])
    subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=72', '-scale-to-x', '960', '-scale-to-y', '-1', pdf, os.path.join(d, 'p')], check=True)
    for f in glob.glob(os.path.join(d, 'p-*.jpg')):                      # pdftoppm writes p-01.jpg ... ; normalise to pNN.jpg
        n = int(re.search(r'p-(\d+)\.jpg$', f).group(1)); os.replace(f, os.path.join(d, f'p{n:02d}.jpg'))
    tt = titles(info['md'])
    n_files = len(glob.glob(os.path.join(d, 'p[0-9][0-9].jpg')))
    assert n_files == info['pages'], (key, n_files, info['pages'])
    for p in range(1, info['pages'] + 1):
        title, ln = tt.get(p, ('', 0)); index.append(dict(deck=key, page=p, title=title[:120], img=f'assets/slides/{key}/p{p:02d}.jpg', chars=ln))
json.dump(index, open(os.path.join(P, 'data', 'slides', 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('rendered', len(index), 'slides;', sum(os.path.getsize(os.path.join(P, i['img'])) for i in index) // 1024, 'KB')
