"""Floyd 9e 'Answers to Odd-Numbered Problems' (printed pp.931-943, PDF pp.949-961): {chapter: {problem: answer text}}.
Two columns per page: words are regrouped into lines per column by position (blocks are split by figure labels)."""
import re, os, sys, json
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from floyd_text import page_lines
FLOYD_PDF = os.path.join(PDFDIR, 'Floyd_Electronic_Devices_9e_fixed.pdf')

def column_lines(page, mid=300):
    """(column, y, text, x0) from floyd_text.page_lines: characters on the same baseline, so symbols (plus-minus, primes, minus signs, Greek) are translated
    and the narrow fragments of a line are no longer lost."""
    rows = {}
    for l in page_lines(page):
        if l['y'] < 45 or l['kind'] in ('fig', 'small') and l['size'] < 7: continue
        col = 0 if l['x0'] < mid else 1
        key = next((k for k in rows if k[0] == col and abs(k[1] - l['y']) <= 1.8), None) or (col, l['y'])
        rows.setdefault(key, []).append(l)
    out = []                                                           # the parts (a) (b) (c) of one answer stand on one baseline with wide gaps: put the pieces back together
    for (col, y), ls in rows.items():
        ls.sort(key=lambda l: l['x0']); out.append((col, y, ' '.join(l['text'] for l in ls), ls[0]['x0']))
    return sorted(out, key=lambda r: (r[0], r[1]))

def scan():
    doc = fitz.open(FLOYD_PDF); res = {}; ch = None; last = 0; cur = None; extra = 0; prev = (0, 0)
    for p in range(949, 962):
        for col, y, ln, x0 in column_lines(doc[p - 1]):
            m = re.match(r'^Chapter\s+(\d{1,2})$', ln)
            if m: ch = int(m[1]); last = 0; cur = None; res.setdefault(ch, {}); continue
            if ch is None: continue
            mi = re.match(r'^(\d{1,2})\.\s*(.*)$', ln)
            if mi and last < int(mi[1]) <= last + 4 and (int(mi[1]) % 2 == 1) and x0 < 80 + 300 * col:
                last = int(mi[1]); cur = last; extra = 0; res[ch][cur] = mi[2]; prev = (col, y); continue
            if cur and not ln.startswith(('▲', 'FIGURE', 'Figure', 'ANSWERS')) and 'See Figure' not in res[ch][cur] and len(ln) > 1 and extra < 4 and x0 < 130 + 300 * col \
                    and prev[0] == col and 0 < y - prev[1] <= 16.5:                   # the next printed line of the same column; figure labels further down are not part of the answer
                res[ch][cur] += ' ' + ln; extra += 1; prev = (col, y)
    return {c: {n: clean(t) for n, t in d.items()} for c, d in res.items()}

if __name__ == '__main__':
    r = scan(); json.dump(r, open(os.path.join(OUT, 'floyd_answers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print({c: len(d) for c, d in sorted(r.items())})
    for c, n in ((12, 5), (12, 13), (13, 7), (14, 23), (17, 15), (6, 31), (6, 35), (16, 3)): print(c, n, '|', r.get(c, {}).get(n, '?')[:110])
