# -*- coding: utf-8 -*-
"""Ghi data/slides/transcript/<deck>_1-<N>.json tu build/transcripts/<deck>.py (danh sach S), kiem do du trang va chay check_transcripts."""
import sys, os, json, importlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import DECKS
import zoom_patch as Z
ZOOM_PAIRS = []
def apply_zoom(deck, S):
    """Ap PATCH (noi dung, so lieu, loi bo sung sau khi phong to kiem) va bo co basis cho cac trang da kiem (zoom_patch.VERIFIED)."""
    ver = set(Z.VERIFIED.get(deck, []))
    for sl in S:
        pt = Z.PATCH.get((deck, sl['page']))
        if pt:
            if pt['en']: sl['text_en'] = pt['en']
            if pt['vi']: sl['text_vi'] = pt['vi']
            if pt['numbers']: sl['numbers'] = [a for a, b in pt['numbers']]; ZOOM_PAIRS.extend(pt['numbers'])
            if pt['issues_set'] is not None: sl['issues'] = [a for a, b in pt['issues_set']]; ZOOM_PAIRS.extend(pt['issues_set'])
            for a, b in pt['issues']:
                if a not in sl['issues']: sl['issues'].append(a)
                ZOOM_PAIRS.append((a, b))
        if sl['page'] in ver and sl.get('basis') == 'summary': del sl['basis']
    return S
for deck in (sys.argv[1:] or list(DECKS)):
    try: m = importlib.import_module(deck)
    except ModuleNotFoundError: continue
    S = apply_zoom(deck, sorted(m.S, key=lambda x: x['page'])); n = DECKS[deck]['pages']; got = [x['page'] for x in S]
    if got != list(range(1, len(got) + 1)): print(deck, 'trang khong lien tuc:', got); continue
    a, b = 1, got[-1]
    fn = os.path.join(ROOT, 'data', 'slides', 'transcript', f'{deck}_{a}-{b}.json')
    for old in [f for f in os.listdir(os.path.dirname(fn)) if f.startswith(deck + '_')]: os.remove(os.path.join(os.path.dirname(fn), old))
    tmp = fn + '.tmp'; json.dump(dict(deck=deck, pdf=DECKS[deck]['pdf'], pages=n, range=[a, b], slides=S), open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(tmp, fn)
    print(deck, f'da doc {b}/{n} trang ->', os.path.basename(fn))
    subprocess.run([sys.executable, os.path.join(ROOT, 'build', 'verify', 'check_transcripts.py'), fn])

if not sys.argv[1:]:                                       # ghi cap dich VI->EN cua ghi chu moi (slides_body.note_en doc them tep nay)
    seen = {}; [seen.setdefault(a, b) for a, b in ZOOM_PAIRS]
    json.dump([[a, b] for a, b in seen.items()], open(os.path.join(HERE, 'notes_en_zoom.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('notes_en_zoom.json:', len(seen), 'cap dich')
