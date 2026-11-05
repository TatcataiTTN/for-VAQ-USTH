"""Floyd 9e 'Answers to Odd-Numbered Problems' (printed pp.931-943, PDF pp.949-961): {chapter: {problem: answer text}}.
Two columns per page: words are regrouped into lines per column by position (blocks are split by figure labels)."""
import re, os, sys, json
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from common import *
FLOYD_PDF = os.path.join(PDFDIR, 'Floyd_Electronic_Devices_9e_fixed.pdf')

def column_lines(page, mid=300):
    words = [w for w in page.get_text('words') if w[1] > 45]
    out = []
    for col in (0, 1):
        ws = [w for w in words if (w[0] < mid) == (col == 0)]
        rows = {}
        for w in sorted(ws, key=lambda w: (w[1], w[0])):
            key = next((k for k in rows if abs(k - w[1]) <= 3.2), None)
            if key is None: key = w[1]; rows[key] = []
            rows[key].append(w)
        for k in sorted(rows): out.append((col, k, ' '.join(w[4] for w in sorted(rows[k], key=lambda w: w[0])), min(w[0] for w in rows[k])))
    return out

def scan():
    doc = fitz.open(FLOYD_PDF); res = {}; ch = None; last = 0; cur = None; extra = 0
    for p in range(949, 962):
        for col, y, ln, x0 in column_lines(doc[p - 1]):
            m = re.match(r'^Chapter\s+(\d{1,2})$', ln)
            if m: ch = int(m[1]); last = 0; cur = None; res.setdefault(ch, {}); continue
            if ch is None: continue
            mi = re.match(r'^(\d{1,2})\.\s*(.*)$', ln)
            if mi and last < int(mi[1]) <= last + 4 and (int(mi[1]) % 2 == 1) and x0 < 80 + 300 * col:
                last = int(mi[1]); cur = last; extra = 0; res[ch][cur] = mi[2]; continue
            if cur and not ln.startswith(('▲', 'FIGURE', 'Figure', 'ANSWERS')) and 'See Figure' not in res[ch][cur] and len(ln) > 1 and extra < 4 and x0 < 130 + 300 * col:
                res[ch][cur] += ' ' + ln; extra += 1
    return {c: {n: clean(t) for n, t in d.items()} for c, d in res.items()}

if __name__ == '__main__':
    r = scan(); json.dump(r, open(os.path.join(OUT, 'floyd_answers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print({c: len(d) for c, d in sorted(r.items())})
    for c, n in ((12, 5), (12, 13), (13, 7), (14, 23), (17, 15), (6, 31), (6, 35), (16, 3)): print(c, n, '|', r.get(c, {}).get(n, '?')[:110])
