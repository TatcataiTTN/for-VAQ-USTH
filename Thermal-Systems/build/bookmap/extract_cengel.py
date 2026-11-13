"""Cengel & Boles 5e (PDF 963 pp.): numbered-section table of contents of chapters 1-17, located from the heading text in the PDF text layer.
Titles: the book's Contents pages (PDF pp.2-17, no page numbers there).  Pages: body headings (a line '9-5' followed by a line that starts with a marker glyph and the
title in capitals).  Printed page = PDF page - 26.  Also: end-of-chapter parts (Summary, References, Problems, ...) and the printed 'Answers:' counts.
Output: data/bookmap/cengel.json.   Run: python3 -I build/bookmap/extract_cengel.py"""
import os, re, json, fitz, difflib
fitz.TOOLS.mupdf_display_errors(False)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, '..', 'Michsl s.Bols - Thermodynamics_ an engineering approach-McGraw-Hill Highrr Education,2005 (2005).pdf')
OFFSET = 26
def sq(s): return re.sub(r'[^a-z0-9]', '', s.lower())
PARTS = [('SUMMARY', r'SUMMARY'), ('REFERENCES AND SUGGESTED READING', r'REFERENCES AND SUGGESTED READINGS?'), ('PROBLEMS', r'PROBLEMS\*?'),
         ('Review Problems', r'Review Problems'), ('Fundamentals of Engineering (FE) Exam Problems', r'Fundamentals of Engineering \(FE\) Exam Problems'),
         ('Design and Essay Problems', r'Design and Essay Problems'), ('TOPIC OF SPECIAL INTEREST', r'TOPICS? OF SPECIAL INTEREST\*?')]
def clean(s): return re.sub(r'\s+', ' ', s.replace('\x01', '').replace('■', '')).strip()
def run():
    d = fitz.open(SRC); toc = d.get_toc(); chs = [p for l, t, p in toc if t.startswith('Chapter')]; gloss = [p for l, t, p in toc if t == 'Glossary'][0]
    L = []
    for p in range(2, 18): L += [l.strip() for l in d[p - 1].get_text().splitlines() if l.strip()]
    toc_ch = []; cur = None
    for l in L:
        m = re.fullmatch(r'Chapter (\d+)', l)
        if m: cur = dict(num=int(m[1]), title=None, items=[]); toc_ch.append(cur); continue
        if cur is not None:
            if cur['title'] is None: cur['title'] = l
            else: cur['items'].append(l)
    chapters = []; ans_total = 0
    for c in toc_ch:
        k = c['num']
        if not 1 <= k <= 17: continue
        p0 = chs[k - 1]; p1 = (chs[k] - 1 if k < 17 else 907)       # chapter 17 ends at PDF p.907 (printed 881, mid-list of FE problems: the PDF is truncated); p.908 is blank (checked)
        tsecs = []
        for it in c['items']:
            m = re.fullmatch(r'(\d+)[–-](\d+)\s+(.*)', it)
            if m and int(m[1]) == k: tsecs.append(dict(toc_num=f'{k}–{m[2]}', title=m[3].strip(), subs=[]))
            elif tsecs and not re.match(r'(Summary|References|Problems|Topics? of Special)', it) and not (it[:1].islower() and 'Special' in tsecs[-1].get('_t', '')):
                tsecs[-1]['subs'].append(it)
        heads = []; parts = []; nans = 0
        for p in range(p0, p1 + 1):
            Lp = [x.strip() for x in d[p - 1].get_text().splitlines() if x.strip()]
            for i, x in enumerate(Lp):
                m = re.fullmatch(r'(\d+)[–-](\d+)', x)
                if m and int(m[1]) == k and i + 1 < len(Lp) and not Lp[i + 1][:1].isalnum() and Lp[i + 1][:1] not in '(':
                    ttl = [Lp[i + 1]]
                    for y in Lp[i + 2:i + 4]:
                        if y.upper() == y and re.search(r'[A-Z]', y) and len(y) < 60 and not re.match(r'\d', y): ttl.append(y)
                        else: break
                    heads.append((f'{k}–{m[2]}', p, clean(' '.join(ttl))))
                for name, rx in PARTS:
                    if re.fullmatch(r'[^\w]*' + rx, x) and p > p0:
                        parts.append(dict(name=name, pdf=p))
            nans += len(re.findall(r'Answers?:', d[p - 1].get_text()))
        ans_total += nans
        pr = [e for e in parts if e['name'] == 'PROBLEMS']
        npb = nap = 0
        if pr:
            Lq = []
            for p in range(pr[0]['pdf'], p1 + 1): Lq += [x.strip() for x in d[p - 1].get_text().splitlines()]
            ix = [i for i, x in enumerate(Lq) if re.fullmatch(rf'{k}[–-]\d+[A-Z]*', x)]
            npb = len(ix)
            for j, i in enumerate(ix):
                if any(re.search(r'Answers?:', y) for y in Lq[i:(ix[j + 1] if j + 1 < len(ix) else len(Lq))]): nap += 1
        secs = []
        for n, p, t in heads:
            if any(s['num'] == n for s in secs): continue
            sc = sorted(((difflib.SequenceMatcher(None, sq(s['title']), sq(t)).ratio() + (0.15 if sq(s['title']).startswith(sq(t)) and len(sq(t)) >= 12 else 0), i) for i, s in enumerate(tsecs)), reverse=True)
            ts = tsecs[sc[0][1]] if sc and sc[0][0] >= 0.85 else None
            secs.append(dict(num=n, title=ts['title'] if ts else t.title(), pdf=p, printed=p - OFFSET, kind='section', subs=ts['subs'] if ts else [],
                             toc_num=ts['toc_num'] if ts else None, title_source='contents' if ts else 'body-heading'))
        # end of each section = page before next section / first end part
        seen = set(); ep = []
        for x in sorted(parts, key=lambda z: z['pdf']):
            if x['name'] in seen: continue
            seen.add(x['name']); ep.append(x)
        for i, s in enumerate(secs):
            nxt = [z['pdf'] for z in secs[i + 1:]] + [z['pdf'] for z in ep if z['pdf'] > s['pdf']]
            s['pdf_end'] = (min(nxt) if nxt else p1 + 1) - 1 if (min(nxt) if nxt else p1 + 1) > s['pdf'] else s['pdf']
        for e in ep: e['printed'] = e['pdf'] - OFFSET
        # topic of special interest is a feature, put it in sections list as kind=feature
        chapters.append(dict(num=k, title=c['title'], pdf=p0, printed=p0 - OFFSET, pdf_end=p1, sections=secs, end_parts=[e for e in ep if e['name'] != 'TOPIC OF SPECIAL INTEREST'],
                             features=[e for e in ep if e['name'] == 'TOPIC OF SPECIAL INTEREST'], toc_sections=[dict(num=t['toc_num'], title=t['title']) for t in tsecs],
                             answers_printed=nans, n_problems=npb, n_problems_with_answer=nap))
    return dict(book='cengel', offset=OFFSET, pages=d.page_count, chapters=chapters, back=dict(glossary_pdf=gloss, last_chapter_pdf=907, answers_appendix=False, answers_total=ans_total))
if __name__ == '__main__':
    B = run(); os.makedirs(os.path.join(ROOT, 'data', 'bookmap'), exist_ok=True)
    json.dump(B, open(os.path.join(ROOT, 'data', 'bookmap', 'cengel_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for c in B['chapters']:
        print(c['num'], c['title'], c['pdf'], len(c['sections']), 'toc', len(c['toc_sections']), 'ans', c['answers_printed'], [(e['name'][:12], e['pdf']) for e in c['end_parts']], [f['pdf'] for f in c['features']])
        for s in c['sections']:
            if s['toc_num'] != s['num']: print('   DIFF', s['num'], s['toc_num'], s['title'], s['title_source'])
