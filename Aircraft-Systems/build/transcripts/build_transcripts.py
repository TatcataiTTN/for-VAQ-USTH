# -*- coding: utf-8 -*-
"""Ghi data/slides/transcript/<deck>_1-<N>.json tu build/transcripts/<deck>.py (danh sach S), kiem do du trang va chay check_transcripts."""
import sys, os, json, importlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import DECKS
for deck in (sys.argv[1:] or list(DECKS)):
    try: m = importlib.import_module(deck)
    except ModuleNotFoundError: continue
    S = sorted(m.S, key=lambda x: x['page']); n = DECKS[deck]['pages']; got = [x['page'] for x in S]
    if got != list(range(1, len(got) + 1)): print(deck, 'trang khong lien tuc:', got); continue
    a, b = 1, got[-1]
    fn = os.path.join(ROOT, 'data', 'slides', 'transcript', f'{deck}_{a}-{b}.json')
    for old in [f for f in os.listdir(os.path.dirname(fn)) if f.startswith(deck + '_')]: os.remove(os.path.join(os.path.dirname(fn), old))
    tmp = fn + '.tmp'; json.dump(dict(deck=deck, pdf=DECKS[deck]['pdf'], pages=n, range=[a, b], slides=S), open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(tmp, fn)
    print(deck, f'da doc {b}/{n} trang ->', os.path.basename(fn))
    subprocess.run([sys.executable, os.path.join(ROOT, 'build', 'verify', 'check_transcripts.py'), fn])
