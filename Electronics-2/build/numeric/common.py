"""Shared helpers of the exercise scanner: quantity detection, figure/SPICE flags, module mapping."""
import re, json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PDFDIR = os.path.join(ROOT, '..', 'pdf_ocr_fixed')
OUT = os.path.join(ROOT, 'data', 'numeric'); os.makedirs(OUT, exist_ok=True)

_UNITS = r'(?:[kKMGmμµnpf]?(?:Ω|ohms?|V|A|W|F|H|Hz|s|J|N|C|T)|dB|°C|°|%|rad|bits?|MEG|V/μs|V/ms|V/s|ppm|µ?m|nm|mm|cm|ft)'
QTY = re.compile(r'(?<![\w.^])[-−+]?\d+(?:[.,]\d+)?(?:\s*(?:×|x|\*)\s*10\^?\(?[−-]?\d+\)?)?\s*' + _UNITS + r'(?![A-Za-z])')
NUM = re.compile(r'(?<![\w.^])[-−+]?\d+(?:[.,]\d+)?(?![\w])')
FIG = re.compile(r'\b(?:Fig\.|Figs\.|Figure|Table)\s*[A-Z]?\d', re.I)
SIM = re.compile(r'\b(?:SPICE|MATLAB|Monte Carlo|PSpice|LTspice|Excel|spreadsheet|computer-aided|simulat\w+|transient analysis)\b', re.I)

def clean(t):
    t = re.sub(r'\s+', ' ', t.replace('­', '')).strip()
    return re.sub(r'(?<=\w)- (?=[a-z])', '', t)             # join words hyphenated at the line end ("op- amp" stays: only lower-case continuations)

def analyse(text):
    """-> dict(numeric, nq, figure, sim): quantities with units, references to a figure, simulator keywords."""
    q = QTY.findall(text)
    return dict(nq=len(q), numeric=len(q) >= 1 or len(NUM.findall(text)) >= 3, figure=bool(FIG.search(text)), sim=bool(SIM.search(text)))

def load_map(): return json.load(open(os.path.join(ROOT, 'data', 'bookmap', 'map.json'), encoding='utf-8'))
