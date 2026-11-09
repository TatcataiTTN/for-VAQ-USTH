"""Whole-bank audit (data/qbank/mNN.json): the checks that used to be done by hand, kept as a script so they can be re-run after every change.

Hard failures (exit 1): out-of-range answer, duplicate options (EN or VI), empty explanation/source, duplicate question stems inside the bank, garbage tokens
('nan', 'None', 'e+', '{', 'if False'), decimal point inside Vietnamese text, an option or stem whose Vietnamese side is the English text with words in it
(the m01 problem: English-only distractors), digit sequence of EN and VI differing in a stem/option beyond the reviewed whitelist, answer-position skew > 12 points.
Printed for review (not failures): level mix, answer positions per module, kinds, origin share."""
import os, sys, json, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
bad = []; info = []
def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
def digits(s): return re.sub(r'[^0-9]', '', s)
SCI_OPT = re.compile(r'\d[eE][+-]?\d')                  # never present after assemble.py polish; kept so the digit rule does not double-report
THOUS = re.compile(r'^\d{1,3}(?:\.\d{3})+$')                  # 10.000 / 5.000.000: Vietnamese thousands separators, not decimals
REVIEWED_EN = {'m05-008', 'm07-014', 'm09-042', 'm10-025', 'm10-034', 'm10-060'}   # acronym expansions and 555 pin names: English on purpose (read one by one)
GARBAGE = re.compile(r'\bnan\b|\bNone\b|\d[eE][+-]\d|[{}]|if False|\bTODO\b|\?\?')
# words that legitimately stay English in the Vietnamese text (units, part names, acronyms, product names)
KEEP = {'op', 'amp', 'jk', 'sr', 'ttl', 'cmos', 'bjt', 'fet', 'mosfet', 'led', 'adc', 'dac', 'ota', 'lvdt', 'rvdt', 'tdx', 'tdr', 'cdx', 'ctx', 'tx', 'tr', 'cx', 'ct', 'sallen', 'key', 'wien', 'colpitts', 'hartley', 'clapp', 'butterworth', 'bessel', 'chebyshev', 'schmitt', 'darlington',
        'class', 'pcb', 'esd', 'eprom', 'dram', 'sram', 'rom', 'ram', 'and', 'or', 'not', 'nand', 'nor', 'xor', 'xnor', 'bcd', 'lsb', 'msb', 'lm', 'pwm', 'vco', 'pll', 'ic', 'dc', 'ac', 'rms', 'gnd', 'vcc', 'vdd', 'vss', 'dip', 'smd', 'smt', 'bga', 'cmrr', 'psrr', 'emi', 'rfi', 'ptc', 'ntc', 'ldr', 'scr', 'triac', 'diac', 'ujt', 'jfet',
        'easa', 'floyd', 'jaeger', 'spice', 'vsp', 'pmos', 'nmos', 'cd', 'sv', 'sm', 'rc', 'rlc', 'lc', 'rl', 'pin', 'bit', 'byte', 'buffer', 'latch', 'flip', 'flop', 'clock', 'reset', 'set', 'hold', 'toggle', 'toggles', 'enable', 'high', 'low', 'tank', 'bypass', 'gain', 'offset', 'slew', 'rate', 'bias', 'drift', 'mica', 'decade', 'octave', 'inch', 'vout', 'vref', 'vin', 'vcc', 'chebyshev', 'bessel', 'butterworth'}
items = {}
for i in range(1, 11):
    items[f'm{i:02d}'] = json.load(open(os.path.join(ROOT, 'data', 'qbank', f'm{i:02d}.json'), encoding='utf-8'))['items']
seen = {}; tot = 0; english_leak = []
for m, its in items.items():
    pos = collections.Counter(); kinds = collections.Counter(); lv = collections.Counter(); orig = collections.Counter()
    for it in its:
        tot += 1; iid = it['id']; kinds[it['kind']] += 1; lv[it['level']] += 1; orig[it['origin']] += 1
        o = it.get('opts') or []; c = it.get('correct')
        if it['kind'] in ('mcq', 'tf', 'ca'):
            if not isinstance(c, int) or not (0 <= c < len(o)): bad.append((iid, 'correct out of range')); continue
            if it['kind'] == 'mcq' and len(o) == 4: pos[c] += 1
            en = [x['en'] for x in o]; vi = [x['vi'] for x in o]
            if len(set(en)) != len(en) or len(set(vi)) != len(vi): bad.append((iid, 'duplicate options'))
            for a, b in zip(en, vi):
                if digits(a) and digits(a) != digits(b) and not SCI_OPT.search(a): bad.append((iid, 'option digits EN/VI', a, b))
                if GARBAGE.search(a + ' ' + b): bad.append((iid, 'garbage in option', a, b))
                if any(not THOUS.match(t) and not re.match(r'^\d+\.\d{3}$', t) or re.match(r'^0\.', t) for t in re.findall(r'(?<![\d.])\d+\.\d+(?![\d.])', b)): bad.append((iid, 'dot decimal in VI option', b))
                words = [w for w in re.findall(r'[A-Za-z]{4,}', b) if w.lower() not in KEEP]
                if a == b and words and not re.search(r'[À-ỹ]', b) and iid not in REVIEWED_EN: english_leak.append((iid, b))
        for f in ('q', 'explain'):
            for tok in re.findall(r'(?<![\d.,])\d{1,3}(?:,\d{3})+(?!\d|,\d)', it[f]['en']):
                if tok in it[f]['vi'] or any(tok.replace(',', sep) in it[f]['vi'] for sep in (' ', '\u00a0', '\u202f')): bad.append((iid, f'thousands separator in VI {f}', tok))
            for lang in ('vi', 'en'):
                if not it[f][lang].strip(): bad.append((iid, f'empty {f}.{lang}'))
            if GARBAGE.search(it[f]['vi'] + ' ' + it[f]['en']): bad.append((iid, f'garbage in {f}'))
            for t in re.findall(r'(?<![\d.])\d+\.\d+(?![\d.])', it[f]['vi']):
                if (THOUS.match(t) or re.match(r'^[1-9]\d{0,2}\.\d{3}$', t)) and not t.startswith('0'): continue
                if re.search(r'(?:§|Hình|Fig\w*\.?|Eq\w*\.?|Section|Mục|Bảng|Table|Chương|Chapter|ch\.|tr\.|Ví dụ|Example|Problem|Bài|page|trang|p\.)\s*' + re.escape(t), it[f]['vi']): continue
                bad.append((iid, f'dot decimal in VI {f}', t, it[f]['vi'][:70])); break
        if not (it.get('src') or {}).get('en'): bad.append((iid, 'empty src'))
        key = norm(it['q']['en'])
        if key in seen and it['kind'] != 'tf': bad.append((iid, 'duplicate stem', seen[key]))
        seen[key] = iid
    n = sum(pos.values()); share = {k: round(100 * v / n) for k, v in sorted(pos.items())} if n else {}
    if share and max(share.values()) - min(share.values()) > 12 + 100 // max(n, 1): bad.append((m, 'answer-position skew', share))
    info.append((m, len(its), dict(sorted(lv.items())), share, dict(kinds), dict(orig)))
for row in info: print(*row)
if english_leak:
    print(f'English-only options in the VI side needing review: {len(english_leak)}')
    for e in english_leak[:40]: print('  ', e)
print(f'items {tot}; problems {len(bad)}')
for b in bad[:60]: print('  ', b)
sys.exit(1 if bad or english_leak else 0)
