"""Cross-check every odd-numbered Floyd problem we solved against "Answers to Odd-Numbered Problems" printed at the back of Floyd 9e (printed pp.935-943,
PDF pp.953-961).  BOOK holds the numeric answers transcribed from those pages.  For each problem the solution text (with every "(book ...)" remark removed, so
the check cannot be circular) must contain each book value, compared by absolute value with 0.6 % tolerance (printed answers are rounded).
Exit code 1 on any mismatch.   Run: python3 -I build/verify/verify_floyd_odd.py"""
import os, re, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOK = {   # (module, Floyd problem) -> numbers printed in the book's answer (units dropped; 450 uW is written 0.45 mW)
 ('m02', 5): [120], ('m02', 7): [8.1], ('m02', 9): [1.6], ('m02', 13): [374, 3.74, 9.99], ('m02', 15): [49, 3, 84, 165], ('m02', 37): [71.7],
 ('m03', 1): [24], ('m03', 3): [2.77], ('m03', 7): [8.57, 0.968], ('m03', 9): [2.5, 3.52], ('m03', 11): [110], ('m03', 13): [3.57, 357], ('m03', 15): [4.06],
 ('m04', 31): [93.6, 303, 28361, 39.4, 49.6, 89.1], ('m04', 33): [2.16, 1.46, 5.16, 4.46, 7.54, 66, 179, 11814], ('m04', 35): [1.41, 2.00, 3.16, 10.0, 100], ('m04', 19): [0.45], ('m04', 21): [24],
 ('m05', 1): [101], ('m05', 3): [1.005], ('m05', 5): [51.5], ('m05', 9): [300], ('m05', 15): [500, 5], ('m05', 23): [0.301, 1.70, 2.11], ('m05', 27): [157],
 ('m06', 3): [48.2], ('m06', 5): [700, 5.04], ('m06', 13): [0.068, 0.586, 1.482], ('m06', 19): [449, 96.4],
 ('m07', 3): [0.0133], ('m07', 5): [733], ('m07', 7): [50], ('m07', 11): [136, 628], ('m07', 13): [10], ('m07', 19): [3.33, 6.67], ('m07', 21): [0.0076],
 ('m08', 1): [0.0333], ('m08', 3): [1.01], ('m08', 7): [8.51], ('m08', 9): [9.57], ('m08', 11): [500], ('m08', 13): [10], ('m08', 15): [250, 6.25], ('m08', 17): [40],
 ('m08', 21): [14.3], ('m08', 23): [1.3], ('m08', 25): [2.8], ('m08', 27): [0.35],
}
def numbers(t):
    t = t.replace('−', '-').replace('−', '-')
    return [abs(float(x.replace(',', ''))) for x in re.findall(r'\d[\d,]*\.?\d*', t) if re.search(r'\d', x) and not x.endswith(',')]
fails = []; checked = 0
for (mid, n), want in BOOK.items():
    items = json.load(open(os.path.join(ROOT, 'data', 'qsrc', f'{mid}.json'), encoding='utf-8'))
    sol = [i for i in items if i['kind'] == 'ess' and re.search(rf'Problem {n} \(', i['src']['en'])]
    if not sol: fails.append((mid, n, 'worked problem missing')); continue
    txt = re.sub(r'\((?:the )?book[^)]*\)|\(All match[^)]*\)|\(book[^)]*$', '', sol[0]['sol']['en'], flags=re.I)
    have = numbers(txt); checked += 1
    for w in want:
        if not any(abs(h - w) <= 0.006 * w + 1e-12 for h in have): fails.append((mid, n, 'book value not in solution', w, [h for h in have if 0.3 * w < h < 3 * w][:6]))
print('odd Floyd problems checked against the printed answers:', checked, 'of', len(BOOK))
print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
