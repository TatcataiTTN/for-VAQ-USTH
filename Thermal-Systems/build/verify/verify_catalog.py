"""Gate of the exercise catalog (P5a). Run: python3 -I build/verify/verify_catalog.py  (after build/numeric/scan_*.py and scan_all.py). Ends with 'FAILS: none' or lists the failures.
 a  Cengel: continuous numbering per chapter, total = bookmap answers.per_chapter, printed answers = 27/22/21/32/30; Examples have a printed solution
 b  Farokhi / El-Sayed: Example counts = book map, problems continuous, no duplicate number, no empty statement; quizzes = 45; Tutorials I = 8 + 2
 c  hand check against page images (data/numeric/handcheck.json, written by reading the images/xhtml BEFORE looking at the extracted text): every token is searched in `text`;
    a mismatch is accepted only when the entry has text_reliable=false (known loss, reason printed); otherwise FAIL
 d  printed answers: each hand-read answer string equals the catalog `answer_printed` (normalised); >= 15
 e  consistency: unique ids, class in the allowed set, flags vs class, summary.json = catalog"""
import os, sys, json, re, collections, unicodedata
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'numeric'))
from common import CLASSES
D = os.path.join(ROOT, 'data')
cat = json.load(open(os.path.join(D, 'numeric', 'catalog.json'), encoding='utf-8'))
summ = json.load(open(os.path.join(D, 'numeric', 'summary.json'), encoding='utf-8'))
hand = json.load(open(os.path.join(D, 'numeric', 'handcheck.json'), encoding='utf-8'))
cm = json.load(open(os.path.join(D, 'bookmap', 'cengel.json'), encoding='utf-8'))
fm = json.load(open(os.path.join(D, 'bookmap', 'farokhi.json'), encoding='utf-8'))
em = json.load(open(os.path.join(D, 'bookmap', 'elsayed.json'), encoding='utf-8'))
FAILS = []; NOTES = []
def fail(m): FAILS.append(m)
def norm(s):
    s = unicodedata.normalize('NFKC', s).lower().replace('_', '').replace('^', '').replace('{', '').replace('}', '')
    s = s.replace('◦', '°').replace('º', '°').replace('∕', '/').replace('−', '-').replace('–', '-').replace('—', '-').replace('⋅', '').replace('·', '').replace('•', '').replace(' ', '')
    s = s.replace('$', '').replace('\\', '')
    return re.sub(r'\s+', '', s)
by = collections.defaultdict(list)
for e in cat: by[(e['source'], e['kind'])].append(e)
idx = {(e['source'], e['number'], e['kind']): e for e in cat}

# ---------------------------------------------------------------- a Cengel
print('== a Cengel')
per = cm['answers']['per_chapter']
for ch in (9, 11, 14, 15, 17):
    pr = [e for e in by[('cengel', 'problem')] if e['chapter'] == ch]
    nums = sorted(int(re.match(r'\d+–(\d+)', e['number'])[1]) for e in pr)
    miss = [n for n in range(1, max(nums) + 1) if n not in nums]; dup = [n for n, c in collections.Counter(nums).items() if c > 1]
    ans = sum(1 for e in pr if e['answer_printed'])
    want = per[str(ch)]
    ok = not miss and not dup and len(pr) == want['problems'] and ans == want['with_answer']
    print(f"  Ch.{ch}: problems {len(pr)} (book map {want['problems']}), missing {miss}, dup {dup}, printed answers {ans} (book map {want['with_answer']}) ->", 'ok' if ok else 'FAIL')
    if not ok: fail(f'a Cengel Ch.{ch} count/continuity/answers')
    suf = collections.Counter(e['suffix'] or '-' for e in pr)
    NOTES.append(f'Ch.{ch} suffix C={suf["C"]} E={suf["E"]} plain={suf["-"]}; no jump in numbering')
    exs = [e for e in by[('cengel', 'example')] if e['chapter'] == ch]
    bad = [e['number'] for e in exs if not e['has_solution_printed'] or not e['text']]
    if bad: fail(f'a Cengel examples without statement/solution {bad}')
    en = sorted(int(e['number'].split('–')[1]) for e in exs)
    if en != list(range(1, max(en) + 1)): fail(f'a Cengel Ch.{ch} example numbering {en}')
    print(f'  Ch.{ch}: examples {len(exs)} numbered 1..{max(en)}')
    # sanity: every problem has a statement
    emp = [e['number'] for e in pr if len(e['text']) < 15]
    if emp: fail(f'a Cengel empty statement {emp}')

# ---------------------------------------------------------------- b Farokhi / El-Sayed / Tut
print('== b Farokhi, El-Sayed, Tutorials I')
for ch, lst in fm['examples'].items():
    if int(ch) not in (1, 2, 3, 4, 6, 7): continue
    got = [e for e in by[('farokhi', 'example')] if e['chapter'] == int(ch)]
    ok = len(got) == len(lst) and len({e['number'] for e in got}) == len(got)
    print(f'  Farokhi Ch.{ch} examples {len(got)} (book map {len(lst)})', 'ok' if ok else 'FAIL')
    if not ok: fail(f'b Farokhi Ch.{ch} examples')
for ch in (1, 2, 3, 4, 6, 7):
    pr = [e for e in by[('farokhi', 'problem')] if e['chapter'] == ch]
    nums = sorted(int(e['number'].split('.')[1]) for e in pr)
    miss = [n for n in range(1, max(nums) + 1) if n not in nums]
    print(f'  Farokhi Ch.{ch} problems {len(pr)} 1..{max(nums)} missing {miss}')
    if miss or len(set(nums)) != len(nums): fail(f'b Farokhi Ch.{ch} problem numbering')
q = by[('farokhi', 'quiz')]
if len(q) != fm['back']['quizzes'] or any(not e['text'] for e in q): fail('b Farokhi quizzes')
print(f'  Farokhi Appendix K quizzes {len(q)} (book map {fm["back"]["quizzes"]}), questions {sum(e["n_questions"] for e in q)}')
for ch in (1, 2, 3, 4, 9, 10, 11):
    want = [x for x in em['examples'] if x['chapter'] == ch]
    got = [e for e in by[('elsayed', 'example')] if e['chapter'] == ch]
    pr = [e for e in by[('elsayed', 'problem')] if e['chapter'] == ch]
    nums = sorted(int(e['number'].split('.')[1]) for e in pr); miss = [n for n in range(1, max(nums) + 1) if n not in nums]
    ok = len(got) == len(want) and sorted(e['number'] for e in got) == sorted(x['num'] for x in want) and not miss and len(set(nums)) == len(nums) and all(e['text'] for e in got + pr)
    print(f'  El-Sayed Ch.{ch}: examples {len(got)} (book map {len(want)}), problems {len(pr)} 1..{max(nums)} missing {miss}', 'ok' if ok else 'FAIL')
    if not ok: fail(f'b El-Sayed Ch.{ch}')
if len(by[('elsayed', 'example')]) != 55: fail('b El-Sayed examples != 55')
tp = by[('tut', 'problem')]; te = by[('tut', 'example')]
print(f'  Tutorials I: problems {len(tp)}, examples {len(te)}')
if len(tp) != 8 or len(te) != 2: fail('b Tutorials I 8 + 2')
for e in cat:
    if not e['text'].strip(): fail(f"b empty text {e['source']} {e['number']}")

# ---------------------------------------------------------------- c hand check
print('== c hand check against images / original xhtml')
tot_items = 0; ok_items = 0; tok_tot = 0; tok_ok = 0; mism = []
by_src = collections.Counter(); ok_src = collections.Counter()
for h in hand:
    e = idx.get((h['source'], h['number'], 'problem'))
    if e is None: fail(f"c hand-check item not in catalog {h['source']} {h['number']}"); continue
    t = norm(e['text']); miss = [k for k in h['read_text'] if norm(k) not in t]
    tot_items += 1; by_src[h['source']] += 1; tok_tot += len(h['read_text']); tok_ok += len(h['read_text']) - len(miss)
    if not miss: ok_items += 1; ok_src[h['source']] += 1
    else:
        mism.append((h['source'], h['number'], miss, e['text_reliable']))
        if e['text_reliable']: fail(f"c mismatch on a text_reliable=true entry {h['source']} {h['number']}: {miss}")
print(f'  items read from images: {tot_items} (cengel {by_src["cengel"]}, farokhi {by_src["farokhi"]}, elsayed {by_src["elsayed"]}); fully matching: {ok_items}/{tot_items}; tokens {tok_ok}/{tok_tot}')
for s in ('cengel', 'farokhi', 'elsayed'): print(f'    {s}: {ok_src[s]}/{by_src[s]} items exact')
for m in mism: print('    MISMATCH', m[0], m[1], m[2], '| text_reliable =', m[3])
if by_src['cengel'] < 12 or by_src['farokhi'] < 8 or by_src['elsayed'] < 6 or tot_items < 30: fail('c fewer hand-checked items than required')

# ---------------------------------------------------------------- d printed answers
print('== d printed answers vs image')
na = 0
for h in hand:
    if not h['read_answer']: continue
    e = idx[(h['source'], h['number'], 'problem')]; na += 1
    if norm(h['read_answer']) != norm(e['answer_printed'] or ''): fail(f"d answer differs {h['number']}: read '{h['read_answer']}' vs catalog '{e['answer_printed']}'")
print(f'  answers read from images and equal to catalog: {na}', '(>= 15 required)')
if na < 15: fail('d fewer than 15 answers checked')

# ---------------------------------------------------------------- e consistency
print('== e consistency')
ids = [e['id'] for e in cat]
if len(ids) != len(set(ids)): fail('e duplicate ids')
for e in cat:
    if e['class'] not in CLASSES: fail(f"e bad class {e['class']}")
    if e['class'] == 'printed_answer' and not e['answer_printed']: fail(f"e printed_answer without answer {e['number']}")
    if e['answer_printed'] and e['class'] not in ('printed_answer', 'outside'): fail(f"e answer but class {e['class']} {e['number']}")
    if e['class'] == 'ready' and (e['needs_figure'] or e['needs_table'] or e['needs_chart'] or not e['numeric'] or not e['text_reliable']): fail(f"e ready with a blocker {e['source']} {e['number']}")
    if e['kind'] == 'example' and e['class'] != 'solved_example' and e['source'] != 'elsayed': fail(f"e example not solved_example {e['source']} {e['number']}")
    if e['module'] is None: fail('e module None')
n = sum(1 for _ in cat)
if summ['total'] != n or sum(summ['by_source'].values()) != n: fail('e summary.json != catalog')
cnt = collections.Counter(e['class'] for e in cat)
if dict(cnt) != summ['by_class']: fail('e summary by_class != catalog')
print(f'  entries {n}; classes {dict(cnt)}')
for s in NOTES: pass
print('FAILS:', 'none' if not FAILS else '')
for f in FAILS: print('  FAIL', f)
sys.exit(1 if FAILS else 0)
