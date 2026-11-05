"""Extract the real table of contents of Floyd 9e and Jaeger 5e from the PDF bookmarks (authoritative PDF page numbers),
add printed page numbers (PDF - offset) and, for Floyd, the pages of the end-of-chapter parts (Summary, True/False, ...).
Output: data/bookmap/floyd.json, data/bookmap/jaeger5.json.   Run: python3 -I build/bookmap/extract.py"""
import os, re, json, sys
import fitz
fitz.TOOLS.mupdf_display_errors(False)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PDFDIR = os.path.join(ROOT, '..', 'pdf_ocr_fixed')
OUT = os.path.join(ROOT, 'data', 'bookmap'); os.makedirs(OUT, exist_ok=True)

def clean(s):
    s = re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()
    s = s.replace('Andoscillators', 'and Oscillators')                      # glitch in the bookmark text
    return re.sub(r'(?<=[a-z])(?=[A-Z][a-z])', ' ', s)                       # 'ElectronicSystem' -> 'Electronic System'

# --------------------------------------------------------------------------- Floyd
FLOYD_OFFSET = 18        # printed page + 18 = PDF page (checked: printed p.302 Fig 6-34 is PDF p.320)
FLOYD_END = [('SUMMARY', r'^\s*SUMMARY\b'), ('KEY TERMS', r'^\s*KEY TERMS\b'), ('KEY FORMULAS', r'^\s*KEY FORMULAS\b'),
             ('TRUE/FALSE QUIZ', r'^\s*TRUE/FALSE QUIZ'), ('CIRCUIT-ACTION QUIZ', r'^\s*CIRCUIT-ACTION QUIZ|^\s*CIRCUIT.ACTION QUIZ'),
             ('SELF-TEST', r'^\s*SELF-TEST\b'), ('PROBLEMS', r'^\s*PROBLEMS\b')]

def floyd():
    d = fitz.open(os.path.join(PDFDIR, 'Floyd_Electronic_Devices_9e_fixed.pdf')); toc = d.get_toc(); n = d.page_count
    dump = open(os.path.join(PDFDIR, 'text', 'Floyd_Electronic_Devices_9e_fixed.txt'), encoding='utf-8').read().split('===== PAGE ')
    txt = {int(x.split(' =====')[0]): x.split('=====\n', 1)[-1] for x in dump[1:]}      # the per-page text dump of the repaired PDF
    def page_text(p): return txt.get(p, '')
    chapters = []; cur = None
    for lvl, title, pg in toc:
        title = clean(title)
        m = re.match(r'^(\d{1,2}) (.+)$', title)
        if lvl == 1 and m and 1 <= int(m[1]) <= 18:
            cur = dict(num=int(m[1]), title=m[2], pdf=pg, printed=pg - FLOYD_OFFSET, sections=[]); chapters.append(cur)
        elif lvl == 1: cur = None
        elif lvl == 2 and cur is not None:
            sm = re.match(r'^(\d{1,2}[–-]\d{1,2}) (.+)$', title)
            if sm: cur['sections'].append(dict(num=sm[1].replace('-', '–'), title=sm[2], pdf=pg, printed=pg - FLOYD_OFFSET, kind='section'))
            else: cur['sections'].append(dict(num='', title=title, pdf=pg, printed=pg - FLOYD_OFFSET, kind='feature'))
    # end pages
    for i, ch in enumerate(chapters):
        ch['pdf_end'] = (chapters[i + 1]['pdf'] - 1) if i + 1 < len(chapters) else next(p for l, t, p in toc if clean(t).startswith('Answers to Odd')) - 1
        secs = ch['sections']
        for j, s in enumerate(secs):
            s['pdf_end'] = (secs[j + 1]['pdf'] - 1) if j + 1 < len(secs) else ch['pdf_end']
            if s['pdf_end'] < s['pdf']: s['pdf_end'] = s['pdf']
        # the last real section runs to the start of the end-of-chapter material (summary...) – find it
        marks = []
        scan_from = secs[-1]['pdf'] if secs else ch['pdf']
        # end-of-chapter material is after the last numbered section / application activity; scan the whole chapter backwards-safe
        nums_ = [s for s in secs if s['kind'] == 'section']; floor_ = nums_[-1]['pdf'] if nums_ else ch['pdf']      # the chapter opener also has a KEY TERMS list: look only after the last numbered section
        for name, rx in FLOYD_END:
            for p in range(max(ch['pdf'], floor_), ch['pdf_end'] + 1):
                lines = page_text(p).splitlines()
                if any(re.search(rx, ln) for ln in lines):
                    # keep the last page where the heading appears as a standalone heading near end-of-chapter (avoid cross refs)
                    marks.append(dict(name=name, pdf=p, printed=p - FLOYD_OFFSET))
                    break
        ch['end_parts'] = marks
    # drop a chapter-end mark that sits before the first section ends (false hit in chapter opener): require pdf >= last numbered section start
    for ch in chapters:
        nums = [s for s in ch['sections'] if s['kind'] == 'section']
        floor = nums[-1]['pdf'] if nums else ch['pdf']
        ch['end_parts'] = [m for m in ch['end_parts'] if m['pdf'] >= floor]
    back = []
    for lvl, title, pg in toc:
        title = clean(title)
        if lvl == 1 and (title.startswith('Answers to Odd') or title in ('Glossary', 'Index')): back.append(dict(title=title, pdf=pg, printed=pg - FLOYD_OFFSET))
    json.dump(dict(book='floyd', offset=FLOYD_OFFSET, pages=n, chapters=chapters, back=back), open(os.path.join(OUT, 'floyd.json'), 'w'), ensure_ascii=False, indent=1)
    return chapters

# --------------------------------------------------------------------------- Jaeger 5e
JAEGER_OFFSET = 29
JAEGER_BRIEF = {1: 3, 2: 41, 3: 72, 4: 144, 5: 215, 6: 283, 7: 359, 8: 414, 9: 455, 10: 517, 11: 587, 12: 685, 13: 770, 14: 841, 15: 952, 16: 1031, 17: 1113, 18: 1217}
JAEGER_PARTS = {1: 'Part One – Solid-State Electronics and Devices', 6: 'Part Two – Digital Electronics', 10: 'Part Three – Analog Electronics'}

def jaeger():
    d = fitz.open(os.path.join(PDFDIR, 'Jaeger_Microelectronic_Circuit_Design_5e_fixed.pdf')); toc = d.get_toc(); n = d.page_count
    chapters = []; cur = None; app = []
    for lvl, title, pg in toc:
        title = clean(title)
        m = re.match(r'^(\d{1,2})\. (.+)$', title)
        if lvl == 2 and m:
            cur = dict(num=int(m[1]), title=m[2], pdf=pg, printed=pg - JAEGER_OFFSET, sections=[]); chapters.append(cur)
        elif lvl <= 2: cur = None
        elif lvl == 3 and cur is not None:
            sm = re.match(r'^(\d{1,2}\.\d{1,2}) (.+)$', title)
            title = re.sub(r'(?<=[a-z])(?=[A-Z][a-z])', ' ', title) if False else title
            if sm:
                ttl = sm[2][2:] if (sm[1] == '9.12' and sm[2].startswith('A ')) else sm[2]       # the book's own contents has a stray 'A' in this title; the section heading does not
                cur['sections'].append(dict(num=sm[1], title=ttl, pdf=pg, printed=pg - JAEGER_OFFSET, kind='section'))
            else: cur['sections'].append(dict(num='', title=title, pdf=pg, printed=pg - JAEGER_OFFSET, kind='end'))
        elif lvl == 4 and cur is not None and cur['sections']:
            pass
    first_after = {c['num']: c for c in chapters}
    app_pdf = next(p for l, t, p in toc if l == 1 and clean(t) == 'APPENDICES'); idx_pdf = next(p for l, t, p in toc if l == 1 and clean(t) == 'INDEX')
    for i, ch in enumerate(chapters):
        ch['part'] = next((v for k, v in sorted(JAEGER_PARTS.items(), reverse=True) if ch['num'] >= k), '')
        ch['pdf_end'] = (chapters[i + 1]['pdf'] - 1) if i + 1 < len(chapters) else app_pdf - 1
        secs = ch['sections']
        for j, s in enumerate(secs):
            s['pdf_end'] = max(s['pdf'], (secs[j + 1]['pdf'] - 1) if j + 1 < len(secs) else ch['pdf_end'])
        assert ch['printed'] == JAEGER_BRIEF[ch['num']], (ch['num'], ch['printed'], JAEGER_BRIEF[ch['num']])   # offset check against printed Brief Contents
    # appendices
    appx = [dict(title=f'Appendix {a}', name=n, printed=pr, pdf=pr + JAEGER_OFFSET) for a, n, pr in [('A', 'Standard Discrete Component Values', 1291),
            ('B', 'Solid-State Device Models and SPICE Simulation Parameters', 1294), ('C', 'Two-Port Review', 1299)]]
    assert appx[0]['pdf'] == app_pdf, (appx[0]['pdf'], app_pdf)               # printed Brief Contents agrees with the bookmark
    json.dump(dict(book='jaeger5', offset=JAEGER_OFFSET, pages=n, chapters=chapters, appendices=appx, appendices_pdf=app_pdf, index_pdf=idx_pdf), open(os.path.join(OUT, 'jaeger5.json'), 'w'), ensure_ascii=False, indent=1)
    return chapters

if __name__ == '__main__':
    f = floyd(); j = jaeger()
    print('Floyd chapters', len(f), 'sections', sum(len(c['sections']) for c in f), '| Jaeger chapters', len(j), 'sections', sum(len(c['sections']) for c in j))
    for c in f:
        if c['num'] in (6, 7, 12, 16): print(' Floyd ch', c['num'], c['pdf'], c['pdf_end'], [(m['name'], m['pdf']) for m in c['end_parts']])
