"""Scan Jaeger 5e: in-text EXERCISE boxes with their printed ANSWERS, worked EXAMPLEs, and the numbered end-of-chapter Problems.
Text comes from PyMuPDF blocks with superscripts kept (pdftext.py), so 10^(40 dB/20 dB) is not flattened to 1040.
Returns a list of catalogue entries (see scan_all.py for the fields)."""
import re, os, sys, json
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from pdftext import page_blocks
from common import *

JAEGER_PDF = os.path.join(PDFDIR, 'Jaeger_Microelectronic_Circuit_Design_5e_fixed.pdf')
OFFSET = 29
RX_EX = re.compile(r'^E\s?X\s?E\s?R\s?C\s?I\s?S\s?E\s?:\s*', re.I)
RX_ANS = re.compile(r'^A\s?N\s?S\s?W\s?E\s?R\s?S?\s?:\s*', re.I)
RX_EXAMPLE = re.compile(r'^E\s?X\s?A\s?M\s?P\s?L\s?E\s+(\d+\.\d+)\b\s*(.*)$', re.I)
RX_PROB = re.compile(r'^(\d{1,2}\.\d{1,3})\.?(?:\s+(.*))?$')
def norm(t): return re.sub(r'[^a-z]', '', t.lower())
RX_SECHEAD = re.compile(r'^(\d{1,2}\.\d{1,3})\s+[A-Z][^.]{3,}$')

def section_index(M):
    secs = sorted((s['pdf'], s['num']) for c in M['jaeger5']['chapters'] for s in c['sections'] if s['kind'] == 'section')
    def of(p):
        cur = None
        for pdf, num in secs:
            if pdf <= p: cur = num
            else: break
        return cur
    return of

def scan(M, progress=False):
    doc = fitz.open(JAEGER_PDF); sec_of = section_index(M); out = []
    chap_range = {c['num']: (c['pdf'], c['pdf_end']) for c in M['jaeger5']['chapters']}
    prob_start = {c['num']: next((s['pdf'] for s in c['sections'] if s['title'] == 'Problems'), None) for c in M['jaeger5']['chapters']}
    blocks_by_page = {}
    for p in range(1, doc.page_count + 1):
        if p < 32 or p > 1319: continue                                           # chapters 1-18 only
        blocks_by_page[p] = page_blocks(doc[p - 1])
        if progress and p % 200 == 0: print('  jaeger page', p, file=sys.stderr)
    # ---- exercises and examples (in-text)
    for p, blocks in blocks_by_page.items():
        for i, b in enumerate(blocks):
            L = b['lines']; head = L[0] if L else ''
            if RX_EX.match(head):
                q = [RX_EX.sub('', head)] + L[1:]; ans = None
                if any(RX_ANS.match(x) for x in q):                              # question and answer in the same block
                    k = next(j for j, x in enumerate(q) if RX_ANS.match(x)); ans = ' '.join([RX_ANS.sub('', q[k])] + q[k + 1:]); q = q[:k]
                else:
                    for nb in blocks[i + 1:i + 9]:
                        if not nb['lines']: continue
                        h0 = nb['lines'][0]
                        if RX_ANS.match(h0): ans = ' '.join([RX_ANS.sub('', h0)] + nb['lines'][1:]); break
                        if RX_EX.match(h0) or RX_EXAMPLE.match(h0) or (nb['bbox'][2] - nb['bbox'][0] > 300 and len(' '.join(nb['lines'])) > 140): break      # next box or body text: no answer printed
                        if nb['bbox'][1] > b['bbox'][3] + 90: break
                        q.append(' '.join(nb['lines']))                           # an equation block between the statement and the answer belongs to the statement
                qt = clean(' '.join(q)); sec = sec_of(p)
                out.append(dict(book='jaeger5', kind='exercise', chapter=int(sec.split('.')[0]) if sec else None, section=sec, number='', pdf=p, printed=p - OFFSET,
                                text=qt, answer=clean(ans) if ans else None, **analyse(qt)))
            m = None; mi = 0
            for mi, ln in enumerate(L):                                            # the header may be the 2nd line ("D E S I G N ... | EXAMPLE 10.4")
                m = RX_EXAMPLE.match(ln)
                if m: break
            if m:
                title = clean(m[2]) if m[2] else (clean(L[mi - 1]) if mi else '')
                if not title and i + 1 < len(blocks): title = clean(' '.join(blocks[i + 1]['lines']))
                stmt = ''
                for nb in [b] + blocks[i + 1:i + 7]:
                    t = ' '.join(nb['lines'])
                    mm = re.search(r'(?:^|\s)PROBLEM\s+(.*)$', t)
                    if mm: stmt = clean(mm[1]); break
                sec = sec_of(p)
                out.append(dict(book='jaeger5', kind='example', chapter=int(m[1].split('.')[0]), section=sec, number=m[1], pdf=p, printed=p - OFFSET, title=title, text=stmt, answer=None, **analyse(stmt or title)))
    # ---- end-of-chapter problems: a block may hold several problems, so split LINE by LINE on the problem numbers
    sec_titles = {c['num']: [(x['num'], x['title']) for x in c['sections'] if x['kind'] == 'section'] for c in M['jaeger5']['chapters']}
    for c in M['jaeger5']['chapters']:
        n = c['num']; ps = prob_start.get(n)
        if not ps: continue
        cur = None; last = 0; cursec = None
        def is_heading(num, rest):
            return any(num == sn and norm(rest)[:12] == norm(st)[:12] for sn, st in sec_titles[n]) or any(norm(rest)[:14] == norm(st)[:14] for sn, st in sec_titles[n] if len(norm(st)) > 14 and norm(rest) == norm(st)[:len(norm(rest))])
        for p in range(ps, c['pdf_end'] + 1):
            for b in blocks_by_page.get(p, []):
                x0, y0, x1, y1 = b['bbox']
                if y0 < 45: continue                                               # running header
                wide = (x1 - x0) > 150
                for j, ln in enumerate(b['lines']):
                    sm = re.match(r'^\^?\(?([∗*]{1,3})\)?\s*', ln); stars = len(sm[1]) if sm else 0       # difficulty marks (one or two asterisks) in front of the number
                    if sm: ln = ln[sm.end():]
                    m = RX_PROB.match(ln)
                    if m and m[1].split('.')[0] == str(n):
                        num = int(m[1].split('.')[1]); m = (m[0], m[1], m[2] or '') if False else m
                        rest = m[2] or ''
                        if rest and is_heading(m[1], rest) and not (m[1] == f'{n}.{last + 1}' and len(rest) > 60):
                            if cur: out.append(cur); cur = None
                            cursec = m[1]; continue
                        if last < num <= last + 8:
                            if cur: out.append(cur)
                            last = num; cur = dict(book='jaeger5', kind='problem', chapter=n, section=cursec, number=f'{n}.{num}', pdf=p, printed=p - OFFSET, text=rest, answer=None, stars=stars); continue
                    if ln.startswith('Figure P') or ln.startswith('Problems') or re.match(r'^P\s?R\s?O\s?B\s?L\s?E\s?M\s?S$', ln): continue
                    if re.match(r'^\d{1,2}\.\d{1,3}\s+[A-Z]', ln) and len(ln) < 70 and is_heading(ln.split()[0], ln.split(None, 1)[1]):
                        if cur: out.append(cur); cur = None
                        cursec = ln.split()[0]; continue
                    if cur and wide and len(ln) > 2: cur['text'] += ' ' + ln
        if cur: out.append(cur)
    for e in out:
        if e['kind'] == 'problem':
            e['text'] = clean(e['text']); e.update(analyse(e['text']))
    return out

if __name__ == '__main__':
    M = load_map(); r = scan(M, True)
    json.dump(r, open(os.path.join(OUT, 'jaeger_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(Counter(e['kind'] for e in r)); print('exercises with printed answer:', sum(1 for e in r if e['kind'] == 'exercise' and e['answer']))
