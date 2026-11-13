"""Doc cac trang 08_*.md va tach token so (dung chung cho extract_tables)."""
import re, os
S = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
MD = os.path.join(S, 'OCR_output', '08_Appendix1_Property_Tables_and_Charts_SI.md')

def pages():
    t = open(MD, encoding='utf-8').read()
    pg = re.split(r'^## \[Trang (\d+)\][^\n]*\n', t, flags=re.M)
    return {int(pg[i]): pg[i + 1] for i in range(1, len(pg), 2)}

NUM = re.compile(r'^[-]?(\d{1,3}(,\d{3})+|\d*\.?\d+)$')

def norm(tok):
    return tok.replace('−', '-').replace('–', '-').replace('—', '-')

def tonum(tok):
    """-> (float, so chu so thap phan in) hoac None."""
    t = norm(tok)
    if not NUM.match(t):
        return None
    t = t.replace(',', '')
    dec = len(t.split('.')[1]) if '.' in t else 0
    return float(t), dec

def lines(page_text):
    return [l.strip() for l in page_text.split('\n') if l.strip()]
