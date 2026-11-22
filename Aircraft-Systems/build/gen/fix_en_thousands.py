# -*- coding: utf-8 -*-
"""Idempotent: in the ENGLISH fields of data/qsrc/*.json a dot used as the thousands separator (65.536, 100.000.000) is rewritten with a comma.
Only numbers that cannot be decimals are touched: two or more dot groups, or the known powers of two / ten written with a dot."""
import json, glob, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
KNOWN = {'1.024', '2.048', '4.096', '8.192', '16.384', '32.768', '65.536', '131.072', '262.144', '524.288', '10.000', '100.000', '1.000.000'}
PAT = re.compile(r'(?<![\d.,])(\d{1,3}(?:\.\d{3})+)(?![\d]|\.\d)(?!\s*(?:[kMG]?Hz|[kMG]?bit|[kMG]?bps|m?V|[nµm]?s\b|nm|µm|kg|km|m\b))')
def fix(t):
    def rep(m):
        s = m.group(1)
        return s.replace('.', ',') if (s.count('.') >= 2 or s in KNOWN) else s
    return PAT.sub(rep, t)
def walk(o, path=()):
    ch = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'en' and isinstance(v, str):
                nv = fix(v)
                if nv != v: o[k] = nv; ch += 1
            else: ch += walk(v, path + (k,))
    elif isinstance(o, list):
        for v in o: ch += walk(v, path)
    return ch
tot = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'qsrc', 'm*.json'))):
    d = json.load(open(f, encoding='utf-8')); n = walk(d)
    if n: json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(os.path.basename(f), n); tot += n
print('EN fields changed:', tot)
