"""EASA M04: every printed Question and its Answer (sub-modules 1, 2, 3).  Pages: SM01 PDF 76-87, SM02 98-101, SM03 116-119 (question and answer pages alternate)."""
import re, os, sys, subprocess, json
sys.path.insert(0, os.path.dirname(__file__))
from common import *
EASA_PDF = os.path.join(PDFDIR, 'EASA_M04_Electronics_Fundamentals_ocr.pdf')
RANGES = {1: (76, 87), 2: (98, 101), 3: (116, 119)}; OFFSET = {1: 11, 2: 87, 3: 101}
FOOT = re.compile(r'^(Module 04 - Electronic Fundamentals|AIRCRAFT|TECHNICAL|Book Company|QUESTIONS|ANSWERS|SEMICONDUCTORS|PRINTED CIRCUIT BOARDS|SERVOMECHANISMS|ELECTRONIC|FUNDAMENTALS|\d+\.\d+|[A-Z]\.\d+)$')

def scan():
    qs, ans = {}, {}
    for sm, (a, b) in RANGES.items():
        for p in range(a, b + 1):
            raw = subprocess.run(['pdftotext', '-raw', '-f', str(p), '-l', str(p), EASA_PDF, '-'], capture_output=True, text=True).stdout
            cur = None
            for ln in raw.splitlines():
                ln = ln.strip()
                m = re.match(r'^(Question|Answer):\s*(\d)-(\d+)\b\s*(.*)$', ln)
                if m:
                    cur = (m[1], f'{m[2]}-{m[3]}', p); (qs if m[1] == 'Question' else ans)[cur[1]] = dict(pdf=p, sm=sm, text=m[4]); continue
                if cur and ln and not FOOT.match(ln) and not re.match(r'^(AIRCRAFT\s+)?\d+$', ln) and not re.match(r'^(AIRCRAFT|TECHNICAL)\b', ln):
                    (qs if cur[0] == 'Question' else ans)[cur[1]]['text'] += ' ' + ln
    out = []
    for k in sorted(qs, key=lambda x: tuple(int(v) for v in x.split('-'))):
        q = qs[k]; a = ans.get(k)
        qt = clean(q['text']); at = clean(a['text']) if a else None
        out.append(dict(book='easa', kind='question', chapter=q['sm'], section=None, number=k, pdf=q['pdf'], printed=f"{q['sm']}.{q['pdf'] - OFFSET[q['sm']]}", text=qt, answer=at, answer_pdf=a['pdf'] if a else None, **analyse(qt + ' ' + (at or ''))))
    return out

if __name__ == '__main__':
    r = scan(); json.dump(r, open(os.path.join(OUT, 'easa_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(len(r), Counter(e['chapter'] for e in r), 'with answer', sum(1 for e in r if e['answer']))
    print(r[0]['number'], r[0]['text'][:100], '=>', (r[0]['answer'] or '')[:100]); print(r[-1]['number'], r[-1]['text'][:100])
