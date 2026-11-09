"""Print the statement of Jaeger problems as the PDF text layer has it (the catalog keeps only the first sentences; tables and 'parameters listed below' follow in the page text).
Usage: python3 -I build/numeric/jtext.py 10.38 10.39 ..."""
import sys, re, json, os, fitz
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
cat = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'catalog.json'), encoding='utf-8'))
by = {e['number']: e for e in cat if e['book'] == 'jaeger5' and e['kind'] == 'problem'}
doc = fitz.open(os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'Jaeger_Microelectronic_Circuit_Design_5e_fixed.pdf'))
def full(n, span=1100):
    e = by[n]; out = []
    for pg in (e['pdf'], e['pdf'] + 1):
        t = doc[pg - 1].get_text('text'); i = t.find(n + '.') if pg == e['pdf'] else 0
        if i >= 0: out.append(re.sub(r'\n+', ' ', t[i:i + span])); break
    t2 = doc[e['pdf']].get_text('text')
    return out[0] if out else e['text'], re.sub(r'\n+', ' ', t2[:500])
if __name__ == '__main__':
    for n in sys.argv[1:]:
        a, b = full(n); print(n, '|', a[:1000]); print('   next page starts:', b[:300] if len(a) < 300 else ''); print()
