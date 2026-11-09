"""Helpers shared by the Jaeger figure solvers: page numbers of the problems and the 'circuit' description string (read by build/numeric/jfigexport.py: the figure labels in front of '(p.')."""
import json, os, math
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
_cat = None
def printed(num, book='jaeger5', kind='problem'):
    global _cat
    if _cat is None: _cat = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'catalog.json'), encoding='utf-8'))
    for e in _cat:
        if e['book'] == book and e['kind'] == kind and e['number'] == num: return e['printed']
    return '?'
def cir(num, figs, text, kind='problem'):
    """'Fig. P10.44 (p.580): text' – `figs` is the label list as printed ('Fig. P10.44' or 'Figs. P10.70 and P10.71')."""
    return f'{figs} (p.{printed(num, kind=kind)}): {text}'
def dbv(x): return 20 * math.log10(abs(x))
