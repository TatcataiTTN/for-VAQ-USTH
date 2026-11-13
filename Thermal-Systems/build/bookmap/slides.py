"""Slide titles of the lecturer's decks: first non-empty text line after '## [Trang N]' in OCR_output/02..07_*.md (not a title in the strict sense: the decks carry no
title placeholders, so this is the first line of the slide).  Output: data/bookmap/slides.json.   Run: python3 -I build/bookmap/slides.py"""
import os, re, json, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import DECKS, MODS, OUT_OF_SCOPE
OCR = os.path.join(ROOT, '..', 'OCR_output')
def run():
    owner = {}
    for m in MODS:
        for d, a, b in m['slides']:
            for p in range(a, b + 1): owner[(d, p)] = (m['id'], 'content')
        for d, a, b in m['blank_slides']:
            for p in range(a, b + 1): owner[(d, p)] = (m['id'], 'blank')
    for d, a, b, why in OUT_OF_SCOPE:
        for p in range(a, b + 1): owner.setdefault((d, p), (None, 'title' if 'title' in why or 'Thank' in why else 'out'))
    decks = {}
    for k, info in DECKS.items():
        txt = open(os.path.join(OCR, info['md']), encoding='utf-8').read()
        parts = re.split(r'^## \[Trang (\d+)\]\s*$', txt, flags=re.M)
        pages = []
        for i in range(1, len(parts), 2):
            n = int(parts[i]); body = parts[i + 1]
            lines = [l.strip() for l in body.splitlines() if l.strip() and l.strip() != '---' and not l.strip().startswith('**[') and not l.startswith('_(')]
            first = lines[0] if lines else ''
            mod, kind = owner.get((k, n), (None, '?'))
            if not lines and kind == 'content': kind = 'content'  # image-only slide kept as content (listed by module)
            pages.append(dict(page=n, title=first[:110], module=mod, kind=kind, empty=not lines))
        assert [p['page'] for p in pages] == list(range(1, info['pages'] + 1)), k
        decks[k] = dict(pdf=info['pdf'], pages=info['pages'], slides=pages)
    return decks
if __name__ == '__main__':
    D = run(); os.makedirs(os.path.join(ROOT, 'data', 'bookmap'), exist_ok=True)
    json.dump(D, open(os.path.join(ROOT, 'data', 'bookmap', 'slides.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in D.items():
        print('==', k, v['pages'])
        for s in v['slides']: print(s['page'], s['module'], s['kind'], s['title'][:70])
