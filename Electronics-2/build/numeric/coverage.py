"""How many of the calculation exercises of the books that belong to the ten modules does the site cover?  Writes data/numeric/coverage.json (shown on the Exercise finder page).
status of a numeric exercise mapped to a module (first match wins):
  printed   the book prints the answer (Written Practice paper)        solved   the site solved and checked it (Written Practice paper)
  bank      a question of the practice bank is built on it             figure   needs a figure of the book, no answer available (listed with its page)
  sim       needs a simulator (SPICE/MATLAB)                           skipped  not solved, reason given in the finder     open    nothing yet (should be 0)"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import *
cat = json.load(open(os.path.join(OUT, 'catalog.json'), encoding='utf-8'))
def status(e):
    if e.get('skip') and 'Figure ANS' in (e.get('answer') or ''): return 'skipped'          # the printed answer is a circuit figure of the appendix: not usable as a worked answer
    if e.get('ans_kind') == 'printed': return 'printed'
    if e.get('ans_kind') == 'computed': return 'solved'
    if e['in_site']: return 'bank'
    if e.get('sim'): return 'sim'
    if e.get('skip'): return 'skipped'
    if e.get('figure'): return 'figure'
    return 'open'
ORDER = ['printed', 'solved', 'bank', 'figure', 'sim', 'skipped', 'open']
mods = collections.defaultdict(collections.Counter); books = collections.defaultdict(collections.Counter); seen = set(); openlist = []
for e in cat:
    if not e.get('numeric') or not e['modules']: continue
    st = status(e)
    for m in e['modules']: mods[m][st] += 1; mods[m]['total'] += 1
    if e['id'] not in seen: seen.add(e['id']); books[f"{e['book']}/{e['kind']}"][st] += 1; books[f"{e['book']}/{e['kind']}"]['total'] += 1
    if st == 'open': openlist.append((e['book'], e['kind'], e['chapter'], e['number'], e['text'][:80]))
tot = collections.Counter()
for e in cat:
    if e.get('numeric') and e['modules'] and e['id'] not in tot: tot[e['id']] = 1
unique = collections.Counter(status(e) for e in cat if e.get('numeric') and e['modules'])
json.dump(dict(order=ORDER, per_module={m: dict(v) for m, v in sorted(mods.items())}, per_kind={k: dict(v) for k, v in sorted(books.items())}, unique=dict(unique), unique_total=sum(unique.values()), open=openlist),
          open(os.path.join(OUT, 'coverage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('unique numeric exercises of the modules:', sum(unique.values()), dict(unique))
for m, v in sorted(mods.items()): print(m, dict(v))
print('open:', openlist)
