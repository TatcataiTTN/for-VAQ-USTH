"""EASA M04 (3 sub-modules) and SERVOMECHANISM (sv) tables of contents.
EASA: titles + printed page hints are transcribed from the book's own CONTENTS pages (PDF p.10-11); every heading is then LOCATED in the
page text (PDF page = printed page + offset of its sub-module) so that OCR mis-alignment of the contents columns cannot leak into the site.
SERVO: numbered headings are read from the text layer.   Output: data/bookmap/easa.json, data/bookmap/servo.json"""
import os, re, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PDFDIR = os.path.join(ROOT, '..', 'pdf_ocr_fixed'); OUT = os.path.join(ROOT, 'data', 'bookmap')
EASA_PDF = os.path.join(PDFDIR, 'EASA_M04_Electronics_Fundamentals_ocr.pdf'); SV_PDF = os.path.join(PDFDIR, 'SERVOMECHANISM_sv.pdf')

# sub-module: offset (PDF = printed + offset), first/last PDF page, qa = PDF pages of the Questions/Answers pairs (question pages and answer pages alternate)
SM = {
 1: dict(offset=11, first=12, last=87, qa=(76, 87), en='Sub-module 01 – Semiconductors', vi='Tiểu mô-đun 01 – Bán dẫn'),
 2: dict(offset=87, first=88, last=101, qa=(98, 101), en='Sub-module 02 – Printed circuit boards', vi='Tiểu mô-đun 02 – Bảng mạch in'),
 3: dict(offset=101, first=102, last=119, qa=(116, 119), en='Sub-module 03 – Servomechanisms', vi='Tiểu mô-đun 03 – Hệ servo'),
}
# (submodule, level, title, printed hint)
T = [
 (1, 1, 'Knowledge Requirements', 1), (1, 1, 'Semiconductors', 2), (1, 2, 'Characteristics and Properties', 2),
 (1, 2, 'Semiconductor Materials', 3), (1, 3, 'Electron Behavior in Valence Shells', 4), (1, 3, 'Effects of Impurities on P and N Type Materials', 5),
 (1, 3, 'Majority and Minority Carriers', 6), (1, 2, 'PN Junctions and The Basic Diode', 7), (1, 3, 'Unbiased PN Junction', 7),
 (1, 3, 'Forward-Bias PN Junction', 8), (1, 3, 'Reverse-Biased PN Junction', 9), (1, 1, 'Semiconductor Diodes', 9), (1, 2, 'Diode Parameters', 9),
 (1, 2, 'Diode Symbols', 10), (1, 2, 'Diode Identification', 11), (1, 2, 'Types of Diodes', 11), (1, 3, 'Zener Diodes', 12), (1, 3, 'Signal Diodes', 12),
 (1, 3, 'Photodiodes', 13), (1, 3, 'Light Emitting Diodes', 13), (1, 3, 'Power Rectifier Diodes', 15), (1, 3, 'Schottky Diodes', 16),
 (1, 3, 'Varistor', 16), (1, 3, 'Varactor Diodes', 17), (1, 2, 'Diode Maintenance and Testing', 19), (1, 1, 'Diodes in Series and Parallel', 21),
 (1, 2, 'Clipper Circuit', 21), (1, 2, 'Clamper Circuit', 22), (1, 2, 'Half-Wave Rectifier Circuit', 23), (1, 2, 'Full-Wave Rectifier Circuit', 23),
 (1, 2, 'Bridge Rectifier Circuit', 23), (1, 2, 'Voltage Doublers and Triplers', 24), (1, 1, 'Transistors', 25),
 (1, 2, 'Description, Characteristics, Properties and Symbols', 25), (1, 2, 'Testing of Transistors', 27), (1, 2, 'Construction and Operation of Transistors', 28),
 (1, 3, 'Bipolar Junction Transistors', 28), (1, 3, 'Unipolar Junction Transistors', 29), (1, 3, 'Field Effect Transistors', 30),
 (1, 3, 'Metal Oxide Field Effect Transistors', 30), (1, 2, 'Multi-Layer Semiconductor Devices', 31), (1, 3, 'Shockley Diodes', 31),
 (1, 3, 'Silicon Controlled Rectifiers', 32), (1, 3, 'Diacs and Triacs', 33), (1, 1, 'Simple Circuits', 34), (1, 2, 'Biasing', 34),
 (1, 2, 'Configurations', 35), (1, 3, 'Common-Emitter Configuration', 36), (1, 3, 'Common-Collector Configuration', 36), (1, 3, 'Common-Base Configuration', 36),
 (1, 2, 'Basic Amplifier Circuits', 37), (1, 3, 'Class A Amplifiers', 37), (1, 3, 'Class AB Amplifiers', 38), (1, 3, 'Class B Amplifier', 38),
 (1, 3, 'Class C Amplifier', 38), (1, 3, 'Cascade Amplifiers', 38), (1, 2, 'Feedback and Stabilization', 39), (1, 3, 'Direct Coupling', 39),
 (1, 3, 'Resistive-Capacitive Coupling', 40), (1, 3, 'Impedance Coupling', 40), (1, 3, 'Transformer Coupling', 40), (1, 2, 'Push-Pull Amplifiers', 41),
 (1, 2, 'Oscillators', 41), (1, 2, 'Multivibrators', 42), (1, 2, 'Flip-flop Circuits', 42), (1, 1, 'Integrated Circuits', 43),
 (1, 2, 'Binary Numbering System', 44), (1, 3, 'Place Values', 46), (1, 3, 'Binary Number System Conversion', 46), (1, 3, 'Binary-Coded Decimals', 47),
 (1, 2, 'Logic Gates', 48), (1, 3, 'NOT Gate', 48), (1, 3, 'Buffer Gate', 48), (1, 3, 'AND Gate', 49), (1, 3, 'OR Gate', 50), (1, 3, 'NAND Gate', 50),
 (1, 3, 'NOR Gate', 50), (1, 3, 'Exclusive OR Gate', 50), (1, 3, 'Exclusive NOR Gate', 50), (1, 3, 'Negative Logic Gates', 51),
 (1, 3, 'Aircraft Logic Gate Applications', 51), (1, 2, 'Logic Circuits', 52), (1, 3, 'Adder Logic Circuits', 52), (1, 3, 'Flip-Flop Logic Circuits', 52),
 (1, 3, 'Comparator Logic Circuits', 54), (1, 3, 'Encoder Logic Circuits', 55), (1, 3, 'Decoder Logic Circuits', 56),
 (1, 2, 'Linear Circuits and Operational Amplifiers', None), (1, 3, 'Positive and Negative Feedback', 60), (1, 3, 'Voltage Follower Circuit', 61),
 (1, 3, 'Multivibrator Circuit', 61), (1, 3, 'Integrator Circuit', 62), (1, 3, 'Differentiator Circuit', 62), (1, 2, 'Scale of Integration', 63),
 (1, 1, 'Questions', 65),
 (2, 1, 'Knowledge Requirements', 1), (2, 1, 'Printed Circuit Boards', 2), (2, 2, 'PCB Manufacturing Process', None), (2, 2, 'Single-Layer Boards', None),
 (2, 2, 'Double-Layered Boards', None), (2, 2, 'Multi-Layered Boards', None), (2, 2, 'PCB Repair', 5), (2, 3, 'Risks and Possible Damage', None),
 (2, 3, 'Anti-Static Protection', 7), (2, 3, 'Controlled Environment', 7), (2, 3, 'Static-Safe Workstation', 7), (2, 3, 'Anti-Static Wrist Straps', None),
 (2, 3, 'Grounding Test Stations', None), (2, 3, 'Ionizers', None), (2, 3, 'Special Handling', None), (2, 1, 'Questions', None),
 (3, 1, 'Knowledge Requirements', 1), (3, 1, 'Servomechanisms', 2), (3, 2, 'Feedback: Open-Loop and Closed-Loop System', None), (3, 2, 'Analog Transducers', 3),
 (3, 2, 'Synchro Systems', 4), (3, 3, 'DC Selsyn Systems', 5), (3, 3, 'AC Synchro Systems', 6), (3, 3, 'Torque Synchro Systems', 7),
 (3, 3, 'Control Synchro Systems and Synchronous Transmitters', 7), (3, 3, 'Differential Synchro Systems', 8), (3, 3, 'Resolver Synchro Systems', 9),
 (3, 2, 'E-I Inductive Transmitters', 9), (3, 2, 'Capacitance Transmitters', 10), (3, 2, 'Stability: Null Hunting, Deadband, and Damping', 10),
 (3, 2, 'Servomechanism Defects', 12), (3, 1, 'Questions', 15),
]

def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
_cache = {}
def ptxt(p):
    if p not in _cache: _cache[p] = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), EASA_PDF, '-'], capture_output=True, text=True).stdout
    return _cache[p]
def heading_lines(p):
    """candidate heading lines of a page: text split into lines AND into >=3-space separated chunks (two-column layout)"""
    out = []
    for ln in ptxt(p).splitlines():
        for ch in re.split(r'\s{3,}', ln.strip()):
            n = norm(ch)
            if n: out.append(n)
    return out
def has_heading(p, title):
    t = norm(title); words = t.split()
    for n in heading_lines(p):
        if n == t or n.startswith(t + ' ') or (len(words) >= 3 and n.startswith(' '.join(words[:3])) and len(n) <= len(t) + 12): return True
    return False

def easa():
    rows = []; flags = []
    for sm, lvl, title, hint in T:
        s = SM[sm]; lo, hi = s['first'], s['last']
        guess = None
        if hint is not None:
            guess = hint + s['offset']                    # hint = printed page counter inside the sub-module (1.21 -> 21)
        found = None
        order = ([guess, guess + 1, guess - 1, guess + 2, guess - 2] if guess else []) + list(range(lo, hi + 1))
        seen = set()
        for p in order:
            if p in seen or not (lo <= p <= hi): continue
            seen.add(p)
            if has_heading(p, title): found = p; break
        if title == 'Knowledge Requirements': found = lo
        by_hint = False
        if found is None and guess:                       # OCR lost the heading itself (checked by eye on the page): keep the page printed in the book's contents
            found = guess; by_hint = True
        rows.append(dict(sm=sm, level=lvl, title=title, hint_printed=hint, pdf=found, by_hint=by_hint))
        if found is None: flags.append((sm, title, 'NOT FOUND'))
        elif by_hint: flags.append((sm, title, f'heading not in OCR text; used contents page pdf {found}'))
        elif guess and found != guess: flags.append((sm, title, f'hint pdf {guess} -> found {found}'))
    return rows, flags

def servo():
    txt = subprocess.run(['pdftotext', '-layout', SV_PDF, '-'], capture_output=True, text=True).stdout.split('\f')
    rows = []; chap = 0
    for i, pg in enumerate(txt, 1):
        for ln in pg.splitlines():
            s = ln.strip()
            m = re.match(r'^Chapter (\d+): (.+)$', s)
            if m: chap = int(m[1]); rows.append(dict(chapter=chap, level=0, num=f'Ch.{chap}', rel=f'Ch.{chap}', title=m[2].strip(), pdf=i)); continue
            m = re.match(r'^(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+([A-Z][^\n]{2,80})$', s)
            if m and chap and not re.search(r'\bvolts?\b|\bFigure\b|\d+\s*V\b', s):
                num = m[1]; lvl = num.count('.') + 1
                rows.append(dict(chapter=chap, level=lvl, num=f'{chap}.{num}', rel=num, title=re.sub(r'\s+', ' ', m[2]).strip(), pdf=i))
    # de-duplicate (same number repeated by page text); keep first occurrence
    seen = set(); out = []
    for r in rows:
        k = (r['chapter'], r['num'])
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    rows, flags = easa(); json.dump(dict(book='easa', submodules={str(k): v for k, v in SM.items()}, rows=rows), open(os.path.join(OUT, 'easa.json'), 'w'), ensure_ascii=False, indent=1)
    print('EASA entries', len(rows), 'flags', len(flags))
    for f in flags: print('  ', f)
    sv = servo(); json.dump(dict(book='servo', pages=99, rows=sv), open(os.path.join(OUT, 'servo.json'), 'w'), ensure_ascii=False, indent=1)
    print('SERVO entries', len(sv))
