"""Scan Floyd 9e (chapters 1-18): the worked Examples (statement), the Related Problem of every Example, the Section Checkup questions, and at the end of each chapter
True/False, Circuit-Action, Self-Test and Problems.  Text comes from floyd_text.page_lines (physical lines rebuilt from the characters), so inline symbols
such as 'VGS(off) = -6 V', primes, deltas, plus-minus and absolute-value bars are kept; figure labels, captions and sidebars are never merged into a statement."""
import re, os, sys, json
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from floyd_text import page_lines
from common import *

FLOYD_PDF = os.path.join(PDFDIR, 'Floyd_Electronic_Devices_9e_fixed.pdf')
OFFSET = 18
RX_ITEM = re.compile(r'^(\d{1,2})\.\s+(.*)$')
RX_SECTION = re.compile(r'^Section\s+(\d{1,2})\s*[–-]\s*(\d{1,2})\b\s*(.*)$')
RX_EXAMPLE = re.compile(r'^E\s?X\s?A\s?M\s?P\s?L\s?E\s+(\d{1,2})\s*[–-]\s*(\d{1,2})\b')
RX_CHECKUP = re.compile(r'^SECTION\s+(\d{1,2})\s*[–-]\s*(\d{1,2})\s+CHECKUP', re.I)
STATES = [('TRUE/FALSE QUIZ', 'truefalse'), ('CIRCUIT-ACTION QUIZ', 'circuit_action'), ('SELF-TEST', 'selftest'), ('PROBLEMS', 'problem')]
SUBPARTS = [('BASIC PROBLEMS', 'basic'), ('ADVANCED PROBLEMS', 'advanced'), ('DATA SHEET PROBLEMS', 'datasheet'), ('TROUBLESHOOTING', 'troubleshooting'), ('MULTISIM TROUBLESHOOTING', 'troubleshooting'),
            ('APPLICATION ACTIVITY', 'application')]
DROPPED = []                                                                # lines left out of every statement (for build/verify/verify_floyd_text.py)
GAP = 22.0                                                                  # a printed line is 11-14 pt below the previous one; more than this means a figure or a heading came between

def body(lines): return [l for l in lines if l['kind'] == 'body' and l['y'] > 44]
def strip_star(t): return re.sub(r'^\^?\(?\*+\)?\s*', '', t)

def scan(M):
    doc = fitz.open(FLOYD_PDF); out = []
    for ch in M['floyd']['chapters']:
        n = ch['num']; parts = {m['name']: m['pdf'] for m in ch['end_parts']}
        summ = parts.get('SUMMARY', ch['pdf_end']); first_q = min([parts[k] for k in ('TRUE/FALSE QUIZ', 'CIRCUIT-ACTION QUIZ', 'SELF-TEST', 'PROBLEMS') if k in parts] or [ch['pdf_end'] + 1])
        green = next((s['pdf'] for s in ch['sections'] if s['title'].startswith('GreenTech')), ch['pdf_end'] + 1)
        # ---------------- in-chapter material: Examples, Related Problems, Section Checkups.  One small state machine: mode = None | example | related | checkup
        cur_ex = None; mode = None; cur = None; chk = None; chk_last = 0; chk_x = 0; prev_y = None
        def add(kind, p, **kw):
            e = dict(book='floyd', kind=kind, chapter=n, pdf=p, printed=p - OFFSET, answer=None, **kw); out.append(e); return e
        for p in range(ch['pdf'], min(summ, first_q if first_q > ch['pdf'] else summ) + 1):
            for l in page_lines(doc[p - 1]):
                if l['y'] < 44: continue
                t = l['text']; head = l['kind'] == 'head'
                me = RX_EXAMPLE.match(t)
                if me and head:
                    cur_ex = f'{me[1]}–{me[2]}'; cur = add('example', p, section=cur_ex, number=cur_ex, text=''); mode = 'example'; prev_y = l['y']; continue
                if head and t.startswith('Related Problem'):
                    cur = add('related_problem', p, section=cur_ex, number=cur_ex or '', text=strip_star(re.sub(r'^Related Problems?', '', t).strip())); mode = 'related'; prev_y = l['y']; continue
                mc = RX_CHECKUP.match(t); mp = re.match(r'^SECTION\s+(\d{1,2})\s*[–-]\s*(\d{1,2})$', t, re.I)
                if mc: chk = f'{mc[1]}–{mc[2]}'; chk_x = l['x0']; chk_last = 0; mode = 'checkup'; cur = None; prev_y = l['y']; continue
                if mp and head: chk = f'{mp[1]}–{mp[2]}'; chk_x = l['x0']; chk_last = 0; mode = 'checkup'; cur = None; prev_y = l['y']; continue          # the box label 'SECTION 12–1' stands left of question 1 on the same line
                if mode == 'checkup' and head and l['x0'] <= chk_x + 60 and re.match(r'^(CHECKUP|Answers|pearson)', t): continue
                if mode == 'checkup' and head and l['x0'] <= chk_x + 60 and re.match(r'^\d{1,2}\s*[–-]\s*\d{1,2}\s+\S', t): mode = None; cur = None
                if mode == 'checkup' and l['kind'] in ('head', 'body') and l['x0'] > chk_x + 60:
                    mi = RX_ITEM.match(t)
                    if mi and int(mi[1]) == chk_last + 1:
                        chk_last += 1; cur = add('checkup', p, section=chk, number=f'{chk}.{chk_last}', text=mi[2], _k=l['kind'], _x=l['x0']); prev_y = l['y']; continue
                    if cur is not None and cur['kind'] == 'checkup' and cur.get('_k') == l['kind'] and cur['_x'] - 1 <= l['x0'] <= cur['_x'] + 30 and not re.search(r'[.?:]$', cur['text']) and prev_y is not None and abs(l['y'] - prev_y) <= GAP and not t.startswith(('SECTION', 'Answers', 'pearson')):
                        cur['text'] += ' ' + t; prev_y = l['y']; continue
                    continue
                if mode == 'checkup' and l['kind'] == 'body' and l['x0'] <= chk_x + 60 and prev_y is not None and l['y'] > prev_y + 5: mode = None; cur = None
                if mode in ('example', 'related') and cur is not None:
                    x_first = cur.get('_x')
                    if l['kind'] == 'body' and prev_y is not None and abs(l['y'] - prev_y) <= GAP and l['x0'] > 100 and (x_first is None or x_first - 2 <= l['x0'] <= x_first + 32 or abs(l['y'] - prev_y) < 1.6):
                        if x_first is None: cur['_x'] = l['x0']
                        cur['text'] = (cur['text'] + ' ' + (strip_star(t) if not cur['text'] else t)).strip(); prev_y = l['y']; continue
                    mode = None; cur = None                       # Solution, a figure, a heading or body text ends the statement
        # ---------------- end of chapter (below)
        if first_q > ch['pdf_end']: continue
        state = None; sub = None; sect = None; last = {}; cur = None; prev_y = None; item_x = None
        for p in range(first_q, min(ch['pdf_end'], green - 1 if green > first_q else ch['pdf_end']) + 1):
            first_body = True
            for l in page_lines(doc[p - 1]):
                if l['y'] < 44: continue
                t = l['text']; u = t.upper()
                if l['kind'] != 'body':
                    st = next((k for h, k in STATES if u.startswith(h)), None)
                    if st: state = st; sub = None; sect = None; last.setdefault(st, 0); cur = None; continue
                    sp = next((k for h, k in SUBPARTS if u.startswith(h)), None)
                    if sp and state == 'problem': sub = sp; cur = None; continue
                    if state in ('selftest', 'problem') or state is None:
                        ms = RX_SECTION.match(t)
                        if ms: sect = f'{ms[1]}–{ms[2]}'; cur = None; continue
                    if cur is not None and (re.match(r'^[▶▲◀]|^FIGURE\b|^Multisim|^These file|^file circuits|^with a logo|^folder on', t) or l['kind'] == 'head'): cur = None      # a caption, note or sidebar ends the statement
                    continue
                if state is None: continue
                mi = RX_ITEM.match(t)
                if mi and last[state] < int(mi[1]) <= last[state] + 4 and (l['bold'] or item_x is None or abs(l['x0'] - item_x) < 8):
                    last[state] = int(mi[1]); cur = dict(book='floyd', kind=state, chapter=n, section=sect, number=str(last[state]), sub=sub, pdf=p, printed=p - OFFSET, text=mi[2], answer=None); out.append(cur); item_x = l['x0']; prev_y = l['y']; first_body = False; continue
                if cur is not None and cur['chapter'] == n and cur['kind'] == state and not t.startswith(('Answers', 'Section ', 'SECTION')) and len(t) > 1 and l['x0'] > (item_x or 0) + 6 \
                        and ((prev_y is not None and abs(l['y'] - prev_y) <= GAP and l['y'] > prev_y - 1) or (first_body and l['y'] < 110)):
                    cur['text'] += ' ' + t; prev_y = l['y']
                else:
                    DROPPED.append(dict(chapter=n, pdf=p, y=round(l['y']), x0=round(l['x0']), item_x=round(item_x or 0), text=t[:140], after=(cur or {}).get('number'), gap=None if prev_y is None else round(l['y'] - prev_y, 1)))      # body text on a statement page that no statement took: the verifier reviews these
                    if cur is not None and not (first_body and l['y'] < 110): cur = None
                first_body = False
    for e in out:
        e.pop('_k', None); e.pop('_x', None); e['text'] = clean(e['text']); e.update(analyse(e['text']))
    return out

if __name__ == '__main__':
    M = load_map(); r = scan(M)
    json.dump(r, open(os.path.join(OUT, 'floyd_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(DROPPED, open(os.path.join(OUT, 'floyd_dropped.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(Counter(e['kind'] for e in r))
    c = Counter((e['chapter'], e['kind']) for e in r)
    for ch in (6, 7, 12, 13, 14, 15, 16, 17): print(ch, {k: c[(ch, k)] for k in ('example', 'truefalse', 'circuit_action', 'selftest', 'problem', 'related_problem', 'checkup')})
