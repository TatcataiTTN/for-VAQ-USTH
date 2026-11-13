"""Farokhi, Aircraft Propulsion 2e (PDF 1048 pp.): table of contents from the PDF bookmarks (389 entries, levels 1-3; authoritative PDF page numbers),
printed page = PDF page - 34 (chapter 1 opens on PDF p.35 = printed 1).  For the relevant chapters the worked examples ('E X A M P L E n . m' in the text) and the end-of-chapter
References / Problems pages are listed; Appendix K quiz entries are listed one by one.  Output: data/bookmap/farokhi_raw.json.   Run: python3 -I build/bookmap/extract_farokhi.py"""
import os, re, json, fitz
fitz.TOOLS.mupdf_display_errors(False)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, '..', 'Aircraft Propulsion (Saeed Farokhi) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
OFFSET = 34
def clean(s): return re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
def run():
    d = fitz.open(SRC); toc = d.get_toc(); N = d.page_count
    ents = []
    for i, (lvl, t, pg) in enumerate(toc):
        t = clean(t); m = re.match(r'^((?:\d+\.)+\d+|\d+)\s+(.*)$', t)
        if lvl == 1 and re.match(r'^\d+ ', t): num, title, kind = m[1], m[2], 'chapter'
        elif lvl == 1 and t.startswith('Appendix'): m2 = re.match(r'Appendix ([A-Z])\s+(.*)', t); num, title, kind = 'App.' + m2[1], m2[2], 'appendix'
        elif m and lvl >= 2: num, title, kind = m[1], m[2], 'section'
        else: num, title, kind = '', t, ('endpart' if t in ('References', 'Problems') else 'other')
        ents.append(dict(i=i, level=lvl, num=num, title=title, kind=kind, pdf=pg, printed=(pg - OFFSET if pg >= 35 else None)))
    # chapter context of unnumbered entries; end pages
    cur = None
    for e in ents:
        if e['kind'] in ('chapter', 'appendix'): cur = e['num']
        e['chapter'] = cur if e['level'] > 1 else (e['num'] if e['kind'] in ('chapter', 'appendix') else None)
    for k, e in enumerate(ents):
        nxt = [x['pdf'] for x in ents[k + 1:] if x['level'] <= e['level']]
        end = nxt[0] if nxt else N + 1
        e['pdf_end'] = end - 1 if end > e['pdf'] else e['pdf']
    # last page of each real chapter/appendix (Index starts at 1033)
    chap = [e for e in ents if e['kind'] in ('chapter', 'appendix')]
    ex = {}
    for c in chap:
        if c['kind'] == 'chapter' and int(c['num']) in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12):
            L = []
            for p in range(c['pdf'], c['pdf_end'] + 1):
                t = d[p - 1].get_text()
                for m in re.finditer(r'^\s*(E\s?X\s?A\s?M\s?P\s?L\s?E\s+((?:\d\s?)+\.\s*(?:\d\s?)+)[^\n]{0,60})', t, re.M):
                    L.append(dict(num=m[2].replace(' ', ''), pdf=p, printed=p - OFFSET, label=clean(m[1]).replace(' ', '') if False else clean(m[1])))
            ex[c['num']] = L
    quizzes = [e for e in ents if e['title'].startswith('Quiz No.')]
    return dict(book='farokhi', offset=OFFSET, pages=N, entries=ents, examples=ex, n_bookmarks=len(toc),
                back=dict(index_pdf=[e['pdf'] for e in ents if e['title'] == 'INDEX'][0], answers_appendix=False, quizzes=len(quizzes)))
if __name__ == '__main__':
    B = run(); out = os.path.join(ROOT, 'data', 'bookmap'); os.makedirs(out, exist_ok=True)
    json.dump(B, open(os.path.join(out, 'farokhi_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(B['n_bookmarks'], 'bookmarks;', {k: len(v) for k, v in B['examples'].items()}, 'quizzes', B['back']['quizzes'])
    for e in B['entries']:
        if e['kind'] in ('chapter', 'appendix') or (e['kind'] == 'endpart' and e['chapter'] in ('1', '2', '3', '4', '6', '7')): print(e['num'] or e['chapter'], e['title'][:40], e['pdf'], e['printed'], e['pdf_end'])
