# -*- coding: utf-8 -*-
"""Nap day du 8 Tooley Revision Papers (Appendix 2, 160 cau; khoa in o Appendix 3, doc lai tu anh quet ngay 22/11/2026).
Cau chua co trong ngan hang duoc them bang file data/qsrc/mNN_rev.json (theo module cua chu de); cau da co duoc vá (hinh, nhan nguon, 4 cau sai) bang patch_existing().
Moi cau: khoa in (printed) va dap an dung (ans). Hai chi khac nhau o cac cau khoa in sai, khi do nhan nguon ghi 'khoa in (x), dung (y)'.
Cach kiem thu thu hai (build/verify/verify_rev.py): cau tinh toan tinh lai bang chuong trinh; cau ly thuyet tim cum tu trong than sach (ev=...) va ghi so trang in; cau co hinh doc tu anh cat tu trang scan."""
import json, os, re, glob, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from qdsl import Bank, ROOT, OUT, opt

KEYS = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']
ITEMS = []          # registry for the verifier
MISS = []           # evidence phrases not found in the book text
_pages = None
def pages(ph):
    """printed page numbers of a phrase in the Tooley body text (PDF page - 14)"""
    global _pages
    if _pages is None:
        import fitz
        d = fitz.open(os.path.join(ROOT, '..', 'ocr', 'pdf', 'Aircraft Digital Electronic_OCR.pdf')); _pages = {}
        for p in range(15, 363): _pages[p - 14] = re.sub(r'\s+', ' ', d[p - 1].get_text().replace('\n', ' ')).lower()
    return [p for p, t in _pages.items() if ph.lower() in t]

def topics_of(mid):
    t = {}
    for f in glob.glob(os.path.join(OUT, f'{mid}*.json')):
        if f.endswith('_rev.json'): continue
        for it in json.load(open(f)): t[it['topic_id']] = (it['topic']['vi'], it['topic']['en'])
    return t
BANKS = {}
def bank(mid):
    if mid not in BANKS: BANKS[mid] = Bank(topics_of(mid))
    return BANKS[mid]
FIG = {}            # (paper, n) -> 'assets/figures/tooley_A2_k.png'
def R(mid, p, n, printed, ans, tid, lv, qv, qe, opts, xv, xe, fig=None, ev=(), tag=''):
    """printed: khoa in (a/b/c) doc tu Appendix 3; ans: dap an dung (khac printed chi khi khoa in sai); opts theo thu tu in."""
    assert KEYS[f'rev{p}'][n - 1] == printed, ('khoa in khac anh scan', p, n, printed, KEYS[f'rev{p}'][n - 1])
    assert len(opts) == 3 and ans in 'abc', (p, n)
    ev_pages = []
    for ph in ev:
        pg = pages(ph)
        if not pg: MISS.append((p, n, ph))
        ev_pages += pg[:2]
    pg_txt = sorted(set(ev_pages))[:3]
    if pg_txt:
        xv += ' (Tooley tr.' + ', '.join(map(str, pg_txt)) + ')'; xe += ' (Tooley p.' + ', '.join(map(str, pg_txt)) + ')'
    sv = f'Tooley Revision Paper {p} Q{n}'; se = sv
    if tag: sv += ' / ' + tag[0]; se += ' / ' + tag[1]
    if printed != ans:
        sv += f' (khoá in ({printed}), đúng ({ans}))'; se += f' (printed key ({printed}), correct ({ans}))'
        xv += f' Lưu ý: khoá in của sách ghi ({printed}); site dùng đáp án đúng theo tính toán.'; xe += f' Note: the book\'s printed key says ({printed}); the site uses the answer that follows from the calculation.'
    B = bank(mid)
    it = B._item('mcq', tid, lv, 'goc', qv, qe, opts, 'abc'.index(ans), xv, xe, sv, se)
    if fig: it['fig'] = f'assets/figures/tooley_A2_{fig}.png'; FIG[(p, n)] = it['fig']
    B.goc.append(it)
    ITEMS.append(dict(p=p, n=n, mid=mid, printed=printed, ans=ans, opts=[opt(o)[1] for o in opts], ev=list(ev), fig=fig, q=qe))

def _norm(t): return re.sub(r'[^a-z0-9.]+', ' ', str(t).lower()).strip()
MERGED = []         # (paper, n, label of the existing item it was merged into)
def merge_duplicates():
    """A Revision Paper question that repeats a chapter question already in the bank (Tooley reuses questions) is NOT added twice:
    its label is appended to the existing item (' / Tooley Revision Paper P Qn') and the new item is dropped, so a mixed exam can never contain both."""
    import difflib
    pool = []
    for f in sorted(glob.glob(os.path.join(OUT, 'm*.json'))):
        if any(s in f for s in ('_ess', '_rev', '_l3', '_esd')): continue
        data = json.load(open(f, encoding='utf-8'))
        for it in data:
            if it['kind'] == 'mcq': pool.append((f, data, it))
    changed = set()
    for mid, B in BANKS.items():
        keep = []
        for it in B.goc:
            m = re.match(r'Tooley Revision Paper (\d+) Q(\d+)', it['src']['en']); lab_en = m.group(0); lab_vi = lab_en
            q, c = _norm(it['q']['en']), _norm(it['opts'][it['correct']]['en']); oset = {_norm(o['en']) for o in it['opts']}
            hit = None
            for f, data, ex in pool:
                if re.search(re.escape(lab_en) + r'(?!\d)', ex['src']['en']): hit = (f, data, ex); break           # already merged on an earlier run
                if _norm(ex['opts'][ex['correct']]['en']) != c: continue
                if len(oset & {_norm(o['en']) for o in ex['opts']}) < 2: continue
                if difflib.SequenceMatcher(None, q, _norm(ex['q']['en'])).ratio() >= .88: hit = (f, data, ex); break
            if not hit: keep.append(it); continue
            f, data, ex = hit
            if not re.search(re.escape(lab_en) + r'(?!\d)', ex['src']['en']):
                ex['src']['en'] += ' / ' + lab_en; ex['src']['vi'] += ' / ' + lab_vi; changed.add(f)
                if it.get('fig') and not ex.get('fig'): ex['fig'] = it['fig']
            MERGED.append((int(m.group(1)), int(m.group(2)), ex['src']['en']))
        B.goc = keep
    for f in changed:
        data = next(d for ff, d, _ in pool if ff == f); json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return changed

def write():
    merge_duplicates()
    for mid, B in BANKS.items():
        fn = os.path.join(OUT, f'{mid}_rev.json'); json.dump(B.goc, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    c = collections.Counter(i['mid'] for i in ITEMS)
    print('rev items', len(ITEMS), dict(sorted(c.items())), '| merged into existing items:', len(MERGED))
    for p, n, lab in MERGED: print('   merged P%d Q%d -> %s' % (p, n, lab[:90]))

def patch_existing():
    """Vá cac cau Revision Paper da co: them hinh, sua nhan nguon sai, sua 4 cau sai/khong khop khoa in. Chay lai nhieu lan khong doi ket qua."""
    from gen_rev_fix import FIX_FIG, FIXES, RELABEL
    n_fig = n_fix = 0
    for f in sorted(glob.glob(os.path.join(OUT, 'm*.json'))):
        if any(s in f for s in ('_gen', '_ess', '_l3', '_esd', '_rev')): continue
        data = json.load(open(f)); ch = False
        for it in data:
            m = re.match(r'Tooley Revision Paper (\d+) Q(\d+)', it['src']['en'])
            if not m: continue
            key = (int(m[1]), int(m[2]), os.path.basename(f))
            key2 = (int(m[1]), int(m[2]))
            if key in RELABEL:
                np_, nn_ = RELABEL[key]; it['src'] = dict(vi=f'Tooley Revision Paper {np_} Q{nn_}', en=f'Tooley Revision Paper {np_} Q{nn_}'); key2 = (np_, nn_); ch = True; n_fix += 1
            if key2 in FIXES:
                for k, v in FIXES[key2].items():
                    if it.get(k) != v: it[k] = v; ch = True; n_fix += 1
            fg = FIX_FIG.get(key2)
            if fg and it.get('fig') != f'assets/figures/tooley_A2_{fg}.png': it['fig'] = f'assets/figures/tooley_A2_{fg}.png'; ch = True; n_fig += 1
        if ch: json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('patched existing: fig', n_fig, 'fixes', n_fix)
