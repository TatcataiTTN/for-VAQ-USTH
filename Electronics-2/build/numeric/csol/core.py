"""Registry for the calculation exercises of the books that have neither a printed answer nor a solver yet: Floyd Section Checkups, Examples, Related Problems and even-numbered
Problems, and Jaeger Examples.  @solve('floyd', 'checkup', 12, '12–7.4') functions return (parts, how, assume);  parts = [(label, value)].
Every solver runs an independent check before it returns (an assert), and for the Examples the numbers printed in the book's own worked solution are looked for in the
book text (must_in_book), so a result that disagrees with the book stops the build."""
import math, os, re
REG = {}
HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'pdf_ocr_fixed', 'text'))
_book = {}
def solve(book, kind, chapter, number):
    def deco(f): REG[(book, kind, str(chapter), str(number))] = f; return f
    return deco
def g(x, n=4):
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e5 or a < 1e-3: return f'{x:.{n-1}e}'.replace('e-0', 'e-').replace('e+0', 'e+')
    return str(float(f'{x:.{n}g}'))
def si(x, unit, n=4):
    if x == 0: return f'0 {unit}'
    a = abs(x)
    for f, p in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1, ''), (1e-3, 'm'), (1e-6, 'μ'), (1e-9, 'n'), (1e-12, 'p'), (1e-15, 'f')):
        if a >= f * 0.99995: return f'{float(f"{x / f:.{n}g}")} {p}{unit}'
    return f'{x:.3e} {unit}'
def close(a, b, rel=1e-3, ab=1e-12): assert abs(a - b) <= rel * max(abs(a), abs(b)) + ab, (a, b)
def db(x): return 20 * math.log10(abs(x))
def book_text(name):
    if name not in _book:
        f = {'floyd': 'Floyd_Electronic_Devices_9e_fixed.txt', 'jaeger': 'Jaeger_Microelectronic_Circuit_Design_5e_fixed.txt'}[name]
        _book[name] = open(os.path.join(TEXT, f), encoding='utf-8', errors='ignore').read()
    return _book[name]
def worked(book, tag, span=3200):
    """Text of the worked Example `tag` (e.g. 'EXAMPLE 17–1' or '10.3') as printed in the book: from the last heading that is followed by a solution."""
    t = book_text(book)
    rx = re.escape(tag).replace('EXAMPLE', 'EXAMPLE') if book == 'floyd' else r'E\s?X\s?A\s?M\s?P\s?L\s?E\s+' + re.escape(tag) + r'\b'
    idx = [m.start() for m in re.finditer(rx + (r'(?![\d–])' if book == 'floyd' else ''), t)]
    for i in idx[::-1]:
        seg = t[i:i + span]
        if book == 'floyd' and 'Solution' in seg[:1200]: return re.sub(r'\s+', ' ', seg)
        if book == 'jaeger' and 'SOLUTION' in seg[:1500]: return re.sub(r'\s+', ' ', seg)
    raise AssertionError('worked example not found: ' + tag)
def must_in_book(book, tag, needles, span=3200):
    seg = worked(book, tag, span); seg2 = seg.replace('−', '-').replace('–', '-')
    for n in needles:
        assert n in seg or n.replace('−', '-') in seg2, (tag, n)
