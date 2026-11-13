"""Shared helpers of the exercise scanners (P5a): paths, quantity detection, flags, class, content-hash id.
Nothing here solves a problem: it only describes what is printed."""
import re, os, json, hashlib, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))          # $P
S = os.path.abspath(os.path.join(ROOT, '..'))                                          # $S
OCR = os.path.join(S, 'OCR_output')
OUT = os.path.join(ROOT, 'data', 'numeric'); os.makedirs(OUT, exist_ok=True)
BOOKMAP = os.path.join(ROOT, 'data', 'bookmap')
CENGEL_PDF = os.path.join(S, 'Michsl s.Bols - Thermodynamics_ an engineering approach-McGraw-Hill Highrr Education,2005 (2005).pdf')
FAROKHI_PDF = os.path.join(S, 'Aircraft Propulsion (Saeed Farokhi) (z-library.sk, 1lib.sk, z-lib.sk).pdf')

def bookmap(name): return json.load(open(os.path.join(BOOKMAP, name + '.json'), encoding='utf-8'))

# ---------------------------------------------------------------- text cleaning
def tidy(t):
    t = t.replace('­', '').replace(' ', ' ').replace(' ', ' ').replace('​', '')
    t = t.replace('’', "'").replace('‘', "'")
    return re.sub(r'[ \t]+', ' ', t).strip()

# ---------------------------------------------------------------- quantities and flags
UNIT = (r'(?:[kKMGmμµ]?(?:Pa|W|J|N|m|g|s|K|V|A|Hz|bar)\b|kPa|MPa|kJ|kW|MW|GW|kg|km|cm|mm|psia|psi|atm|Btu|lbm|lbf|ft|in\.?|hp|rpm|min|h\b|hr|°\s?[CF]|◦\s?[CF]|°R|\bR\b|percent|%|kmol|mol|m/s|ft/s|mph|kg/s|kJ/kg|kW/m|Mach|deg|degrees|rad|kN|lb|liters?|L\b|ppm|kcal|cal|rev|ft3|m3|m2|cm2|in2|mi\b|knots?|kts|Pa·s|dB|s\b)')
QTY = re.compile(r'(?<![\w.^–-])[-−+]?\d[\d,]*(?:\.\d+)?(?:\s*(?:×|x)\s*10\^?\(?[−-]?\d+\)?)?\s*(?:[A-Za-z°◦%][A-Za-z0-9°◦%/·⋅\.\-\^2−]*)')
NUMTOK = re.compile(r'(?<![\w.^])[-−+]?\d[\d,]*(?:\.\d+)?(?![\w])')
UNIT_RX = re.compile(r'^(?:kPa|MPa|Pa|bar|atm|kJ|J|kW|MW|W|kg|g|lbm|lbf|Btu|psia|psi|°|◦|%|percent|K|R|m|cm|mm|km|ft|in|hp|rpm|s|min|h|hr|mol|kmol|N|kN|MN|V|A|Hz|kcal|mph|knots?|kts|deg|degrees|rad|liters?|L|m/s|ft/s|kg/s|m3|m2|cm2|in3|in2|ft3|ft2|kJ/kg|lb|Mach|Pa·s|mi|dB|s)\b', re.I)
ENG = re.compile(r'\b(?:psia|psi|Btu|lbm|lbf|ft/s|ft\^?3|ft3|ft2|mph|knots?|hp|gal|°\s?F|◦\s?F|(?:\d+(?:\.\d+)?|\))\s*R\b|rankine|\d+\s*ft\b|\d+\s*in\.|lb/|lb\b)', re.I)
FIGREF = re.compile(r'\b(?:Fig\.|Figs\.|Figure|Figures|FIGURE|F I G U R E)\s*[A-Z]?\s*\d|\b(?:shown|given|sketched|illustrated|depicted)\s+(?:in\s+(?:the\s+)?)?(?:figure|fig\.|below|schematic)|\bas shown\b|\bshown in the (?:figure|diagram|schematic)\b|\bin the figure\b|\bthe (?:figure|diagram|schematic) (?:below|shown)\b', re.I)
TABLE_RX = re.compile(r"Table[s]?\s*A\s*[–-]\s*\d|\bsteam\b|\bsaturated (?:water|liquid|vapou?r|mixture)\b|\bsuperheated\b|\bwater vapou?r\b|\bR\s?-?\s?134a\b|refrigerant\s?-?\s?134a|\bammonia\b|\brefrigerant\b|variable specific heats?|enthalpy of formation|\bcompressed liquid\b|isentropic table|normal.shock table|ISA table|standard atmosphere table|gas table", re.I)
CHART_RX = re.compile(r'psychrometric chart|psychrometric|\bMollier\b|\bh-s (?:chart|diagram)\b|compressibility chart|generalized (?:compressibility|enthalpy|entropy) chart|Fig\.?\s*A\s*[–-]\s*\d|Figs\.?\s*A\s*[–-]\s*\d|wet-bulb|\bchart\b|nomograph|generalized chart|Prandtl.Meyer table|oblique.shock chart|Carpet plot|\bthetabeta\b|θ-β-M chart|Mach chart', re.I)
DIAGRAM_RX = re.compile(r'(?:show|sketch|draw|plot|illustrate)[^.?]{0,60}(?:T-?s|P-?v|h-?s|p-?h|T-?v)\s+(?:and [A-Za-z\-]+\s+)?diagram|\bT-s diagram|\bP-v diagram', re.I)
SOFT_RX = re.compile(r'\bEES\b|\b(?:other\) software|computer|software|spreadsheet|MATLAB|numerically|parametric)\b', re.I)
REF_RX = re.compile(r'\b(?:Reconsider|Repeat|Rework|Redo|Using the (?:results|solution)|Resolve|Re-?work)\b[^.]{0,40}?\bProb(?:lem|\.)s?\s*(\d+[–-]\d+[CE]?|\d+\.\d+)', re.I)

def has_numbers(text):
    t = re.sub(r'\bProb(?:lem|\.)s?\s+\d+[–-]\d+[CE]?', ' ', text)
    t = re.sub(r'\bProb(?:lem|\.)s?\s+\d+\.\d+', ' ', t)
    t = re.sub(r'\([a-h]\)|\bEq\.\s*\S+|\bFig\.\s*\S+|\bTable\s+\S+|\bFigure\s*P?\d[\d.–-]*|\bExample\s*\d[\d.–-]*', ' ', t)
    t = re.sub(r'\b[0-9]+[–-][0-9]+[CE]?\b', ' ', t)             # section/problem references 9–14
    return t

def quantities(text):
    t = has_numbers(text)
    n = 0
    for m in NUMTOK.finditer(t):
        tail = t[m.end():m.end() + 14].lstrip()
        if UNIT_RX.match(tail) or re.match(r'^(?:[kKMG]?(?:Pa|W|J|N)|°|◦|%)', tail): n += 1
    return n, len(NUMTOK.findall(t))

def analyse(text):
    nq, nn = quantities(text)
    return dict(
        nq=nq, n_numbers=nn,
        numeric=(nq >= 1 or nn >= 3),
        mentions_figure=bool(FIGREF.search(text)),
        mentions_table=bool(TABLE_RX.search(text)),
        mentions_chart=bool(CHART_RX.search(text)),
        asks_diagram=bool(DIAGRAM_RX.search(text)),
        software=bool(SOFT_RX.search(text)),
        refers_to=sorted(set(m.group(1) for m in REF_RX.finditer(text))),
        english_units=bool(ENG.search(text)),
    )

def table_basis(text):
    return sorted(set(m.group(0).lower() for m in TABLE_RX.finditer(text)))

def chart_basis(text):
    return sorted(set(m.group(0).lower() for m in CHART_RX.finditer(text)))

# ---------------------------------------------------------------- reliability
def reliability(text, extra=()):
    """-> list of reasons why `text` may be wrong (empty = nothing suspicious found by script)."""
    why = list(extra)
    if re.search(r'[\x00-\x08\x0b-\x1f�]', text): why.append('control or replacement characters')
    if re.search(r'[˙·]\s*[A-Za-z]|[A-Za-z]\s*[˙]', text): why.append('stray dot (rate symbol?)')
    if text.count('(') != text.count(')'): why.append('unbalanced parentheses')
    if re.search(r'\b[a-zA-Z]\s?−\s?[a-zA-Z]\b', text) and re.search(r'\b(?:h|s|g|u)\s?−', text): why.append('minus sign where a molar bar (h-bar, s-bar) may stand')
    if not re.search(r'[.?!)\]:%\w]$', text) and len(text) > 20: why.append('ends without a terminator')
    return why

# ---------------------------------------------------------------- id
def make_id(source, kind, chapter, number, text):
    norm = re.sub(r'[^a-z0-9]+', '', text.lower())[:400]
    h = hashlib.sha1(f'{source}|{kind}|{chapter}|{number}|{norm}'.encode()).hexdigest()[:12]
    return f'{source[:2]}-{h}'

# ---------------------------------------------------------------- class
CLASSES = ('printed_answer', 'solved_example', 'ready', 'needs_figure', 'needs_table', 'needs_chart', 'conceptual', 'outside', 'unclear')

def classify(e):
    """Order of decision (first that fires). Returns (class, reason)."""
    if e['kind'] == 'example':
        return ('solved_example', 'worked example printed with its solution') if e.get('has_solution_printed') else ('unclear', 'example without a printed solution')
    if e['kind'] == 'quiz':
        return ('conceptual', 'quiz question (answer not printed)')
    if e['module'] in ('out', None):
        return 'outside', 'chapter/section not mapped to any module'
    if e.get('answer_printed'):
        return 'printed_answer', 'book prints the answer'
    if e.get('suffix') == 'C':
        return 'conceptual', 'concept question (suffix C)'
    if not e['text_reliable']:
        return 'unclear', 'text not reliable: ' + '; '.join(e.get('unreliable_why', []))
    if e['concept'] and not e['numeric']:
        return 'conceptual', 'no numeric data in the statement'
    if e['refers_to']:
        return 'unclear', 'refers to another problem (' + ', '.join(e['refers_to']) + '): needs that statement'
    if e['software'] and not e['numeric']:
        return 'unclear', 'software/EES parametric study without data in statement'
    if e['needs_figure']:
        return 'needs_figure', e.get('figure_basis', 'figure referenced')
    if e['needs_chart']:
        return 'needs_chart', 'chart: ' + ', '.join(e.get('chart_basis', []))
    if e['needs_table']:
        return 'needs_table', 'property table: ' + ', '.join(e.get('table_basis', []))
    if e['concept'] or not e['numeric']:
        return 'conceptual', 'no numeric data' if not e['numeric'] else 'concept question'
    if e['software']:
        return 'unclear', 'asks for software/parametric plot; closed answer unlikely'
    return 'ready', 'numeric, no figure/table/chart, no printed answer'

def finalize(e):
    """Fill derived flags, class, id. `e` has: source, chapter, number, kind, text, pdf_page, printed_page, module, ..."""
    a = analyse(e['text'])
    e['text_reliable'] = e.get('text_reliable', True)
    e['unreliable_why'] = list(e.get('unreliable_why', []))
    why = reliability(e['text'])
    if e.get('kind') == 'quiz': why = [w for w in why if 'terminator' not in w]
    if why:
        e['unreliable_why'] += [w for w in why if w not in e['unreliable_why']]
        if any(w for w in why if not w.startswith('ends without')) or e.get('strict_end'): e['text_reliable'] = False
    e['numeric'] = a['numeric']; e['nq'] = a['nq']; e['n_numbers'] = a['n_numbers']
    e['needs_figure'] = bool(e.get('fig_caption')) or a['mentions_figure']
    e['figure_basis'] = ('printed FIGURE caption' if e.get('fig_caption') else 'text mentions a figure')
    e['needs_table'] = a['mentions_table']; e['table_basis'] = table_basis(e['text'])
    e['needs_chart'] = a['mentions_chart']; e['chart_basis'] = chart_basis(e['text'])
    e['asks_diagram'] = a['asks_diagram']; e['software'] = a['software']; e['refers_to'] = a['refers_to']
    e['english_units'] = bool(e.get('suffix') == 'E') or a['english_units']
    e['concept'] = (e.get('suffix') == 'C') or (not a['numeric'])
    e['answer_printed'] = e.get('answer_printed')
    cls, why = classify(e)
    e['class'] = cls; e['class_reason'] = why
    e['id'] = make_id(e['source'], e['kind'], e['chapter'], e['number'], e['text'])
    return e
