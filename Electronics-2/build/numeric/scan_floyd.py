"""Scan Floyd 9e (chapters 1-18): True/False, Circuit-Action, Self-Test and Problems at the end of every chapter, the Related Problem of every Example,
and the Section Checkup questions.  A block may hold several numbered items, so items are split LINE by LINE; numbers must follow each other."""
import re, os, sys, json
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from pdftext import page_blocks
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

def scan(M):
    doc = fitz.open(FLOYD_PDF); out = []
    for ch in M['floyd']['chapters']:
        n = ch['num']; parts = {m['name']: m['pdf'] for m in ch['end_parts']}
        summ = parts.get('SUMMARY', ch['pdf_end']); first_q = min([parts[k] for k in ('TRUE/FALSE QUIZ', 'CIRCUIT-ACTION QUIZ', 'SELF-TEST', 'PROBLEMS') if k in parts] or [ch['pdf_end'] + 1])
        green = next((s['pdf'] for s in ch['sections'] if s['title'].startswith('GreenTech')), ch['pdf_end'] + 1)
        # ---------------- in-chapter material: Related Problems and Section Checkups
        cur_ex = None; cur_chk = None; chk_last = 0
        for p in range(ch['pdf'], min(summ, first_q if first_q > ch['pdf'] else summ) + 1):
            blocks = page_blocks(doc[p - 1])
            for i, b in enumerate(blocks):
                t = ' '.join(b['lines']); L = b['lines']
                for ln in L:
                    me = RX_EXAMPLE.match(ln)
                    if me: cur_ex = f'{me[1]}–{me[2]}'
                if t.startswith('Related Problem'):
                    txt = clean(re.sub(r'^Related Problem\^?\(?\*?\)?\s*', '', t))
                    if not txt and i + 1 < len(blocks): txt = clean(' '.join(blocks[i + 1]['lines']))
                    out.append(dict(book='floyd', kind='related_problem', chapter=n, section=cur_ex, number=cur_ex or '', pdf=p, printed=p - OFFSET, text=txt, answer=None, **analyse(txt)))
                mc = RX_CHECKUP.match(t)
                if mc:
                    cur_chk = f'{mc[1]}–{mc[2]}'; chk_last = 0
                    for nb in blocks[i + 1:i + 4]:
                        for ln in nb['lines']:
                            mi = RX_ITEM.match(ln)
                            if mi and int(mi[1]) == chk_last + 1:
                                chk_last += 1; out.append(dict(book='floyd', kind='checkup', chapter=n, section=cur_chk, number=f'{cur_chk}.{chk_last}', pdf=p, printed=p - OFFSET, text=clean(mi[2]), answer=None))
                            elif mi is None and out and out[-1]['kind'] == 'checkup' and out[-1]['section'] == cur_chk and not ln.startswith(('SECTION', 'Answers')) and len(ln) > 3 and chk_last:
                                out[-1]['text'] = clean(out[-1]['text'] + ' ' + ln)
        # ---------------- end of chapter
        if first_q > ch['pdf_end']: continue
        state = None; sub = None; sect = None; last = {}
        for p in range(first_q, min(ch['pdf_end'], green - 1 if green > first_q else ch['pdf_end']) + 1):
            for b in sorted(page_blocks(doc[p - 1]), key=lambda b: (round(b['bbox'][1] / 4), b['bbox'][0])):          # Floyd pages are single-column: read them top to bottom
                x0, y0, x1, y1 = b['bbox']
                if y0 < 42: continue                                                   # running header
                for ln in b['lines']:
                    u = ln.upper()
                    st = next((k for h, k in STATES if u.startswith(h)), None)
                    if st:
                        state = st; sub = None; sect = None; last.setdefault(st, 0); continue
                    sp = next((k for h, k in SUBPARTS if u.startswith(h)), None)
                    if sp and state == 'problem': sub = sp; continue
                    if state in ('selftest', 'problem') or state is None:
                        ms = RX_SECTION.match(ln)
                        if ms: sect = f'{ms[1]}–{ms[2]}'; continue
                    if state is None: continue
                    mi = RX_ITEM.match(ln)
                    if mi and last[state] < int(mi[1]) <= last[state] + 4:
                        last[state] = int(mi[1]); text = mi[2]
                        out.append(dict(book='floyd', kind=state, chapter=n, section=sect, number=str(last[state]), sub=sub, pdf=p, printed=p - OFFSET, text=text, answer=None))
                        continue
                    if out and out[-1]['kind'] == state and out[-1]['chapter'] == n and len(ln) > 1 and not ln.startswith(('Answers', 'Section ', 'SECTION')) and (x1 - x0) > 60:
                        out[-1]['text'] += ' ' + ln
    for e in out:
        e['text'] = clean(e['text'])
        if e['kind'] != 'related_problem': e.update(analyse(e['text']))
    return out

if __name__ == '__main__':
    M = load_map(); r = scan(M)
    json.dump(r, open(os.path.join(OUT, 'floyd_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(Counter(e['kind'] for e in r))
    c = Counter((e['chapter'], e['kind']) for e in r)
    for ch in (6, 7, 12, 13, 14, 15, 16, 17): print(ch, {k: c[(ch, k)] for k in ('truefalse', 'circuit_action', 'selftest', 'problem', 'related_problem', 'checkup')})
