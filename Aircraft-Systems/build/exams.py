"""Mock-exam definitions: Midterm, Final, Speed, Custom and the mixed sets.
The syllabus (AE2.021) does not state an exam format, so the structure below is THIS SITE'S OWN DESIGN and is shown as such on the page:
  Midterm  modules 01-04 (number systems, logic, integrated circuits, computer and CPU), 30 questions, 45 minutes, forward-only, three fixed papers A/B/C and a random draw
  Final    all nine modules, 45 questions, 60 minutes, free navigation, three fixed papers A/B/C and a random draw
  Speed    20 questions drawn at random from every module, 15 minutes, free navigation
  Custom   the learner chooses modules, number of questions, minutes, forward-only or not
Quotas per module follow the amount of lecture material (number of lecturer slides per module; module 07 is a 6-page document, so it gets a small quota).
Papers are reproducible (fixed seed), the three papers of one type do not overlap, levels are mixed and textbook/lecturer originals are favoured."""
import random, collections, re

ORDER = ['m%02d' % k for k in range(1, 16)]
TYPES = {
    'midterm': dict(n=30, minutes=45, forward=True, quota=dict(m01=4, m02=9, m03=9, m04=8), levels={1: .45, 2: .40, 3: .15}, papers='ABC'),
    'final': dict(n=50, minutes=70, forward=False, quota=dict(m01=3, m02=7, m03=6, m04=6, m05=3, m06=4, m07=2, m08=3, m09=3, m10=4, m11=4, m12=2, m13=1, m14=1, m15=1), levels={1: .40, 2: .40, 3: .20}, papers='ABC'),
    'speed': dict(n=20, minutes=15, forward=False, quota=dict(m01=1, m02=2, m03=2, m04=2, m05=1, m06=1, m07=1, m08=1, m09=2, m10=2, m11=2, m12=1, m13=1, m14=1, m15=0), levels={1: .45, 2: .40, 3: .15}, papers=''),
}
for t in TYPES.values(): assert sum(t['quota'].values()) == t['n'], t
MODULE_TEST = dict(n=15, minutes=20, levels={1: .40, 2: .40, 3: .20})
HARD = dict(n=25, minutes=40, cap=4, papers='AB')
FULL = dict(n_mcq=20, mcq_minutes=30, n_ess=3, ess_marks=20, ess_minutes=60, mcq_marks=2, papers='AB', levels={1: .40, 2: .40, 3: .20})
WRITTEN = dict(n=6, minutes=60, papers='ABCD', marks={1: 5, 2: 10, 3: 15})
REV = re.compile(r'Tooley Revision Paper (\d+) Q(\d+)')
KINDS = ('mcq', 'ca')                                   # true/false items (2 options) are left out: a coin flip is not an exam question

def eligible(it): return it['kind'] in KINDS and 3 <= len(it['opts']) <= 6
def longest(it):
    """True when the correct option is strictly the longest (English text): a length tell that exams try to avoid."""
    L = [len(o['en']) for o in it['opts']]; c = L[it['correct']]; return c > max(l for i, l in enumerate(L) if i != it['correct'])

def allocate(quota, weights, rng):
    """Level targets per module so that the WHOLE paper has the requested mix (rounding per module alone gave the Final 22 % level-3 instead of 25 %).
    Global totals by largest remainder (ties go to the harder level), per-module floors, then the remaining slots are handed out by largest fractional part."""
    n = sum(quota.values()); lvs = sorted(weights)
    tot = {lv: int(n * weights[lv]) for lv in lvs}
    for lv in sorted(lvs, key=lambda lv: (-(n * weights[lv] - tot[lv]), -lv))[:n - sum(tot.values())]: tot[lv] += 1
    t = {m: {lv: int(k * weights[lv]) for lv in lvs} for m, k in quota.items()}
    need = {lv: tot[lv] - sum(t[m][lv] for m in t) for lv in lvs}; slots = {m: quota[m] - sum(t[m].values()) for m in t}
    cand = sorted(((quota[m] * weights[lv] - t[m][lv], rng.random(), m, lv) for m in t for lv in lvs), reverse=True)
    for _, _, m, lv in cand:
        if slots[m] > 0 and need[lv] > 0: t[m][lv] += 1; slots[m] -= 1; need[lv] -= 1
    for lv in lvs:                                         # leftovers (cannot happen when the totals agree, kept as a guard)
        for m in t:
            while slots[m] > 0 and need[lv] > 0: t[m][lv] += 1; slots[m] -= 1; need[lv] -= 1
    assert sum(need.values()) == 0 and sum(slots.values()) == 0, (need, slots)
    return t

def pick(items, k, weights, rng, used, target=None):
    """k items of one module, stratified by level (`target` = level counts from allocate()), textbook originals favoured, none from `used`."""
    avail = collections.defaultdict(list)
    for it in items:
        if it['id'] not in used: avail[it['level']].append(it)
    for lv in avail: avail[lv].sort(key=lambda it: rng.random() + (0 if it['origin'] == 'goc' else 0.5) + (0.4 if longest(it) else 0))
    if target is None:
        target = {lv: int(k * w) for lv, w in weights.items()}; rest = k - sum(target.values())
        for lv in sorted(weights, key=lambda lv: -(k * weights[lv] - target[lv]))[:rest]: target[lv] += 1
    got = []
    for lv in sorted(weights):
        take = avail[lv][:target[lv]]; got += take; avail[lv] = avail[lv][len(take):]
    while len(got) < k:                                  # a level ran out: take from the level that has most left
        lv = max(avail, key=lambda lv: len(avail[lv]), default=None)
        if lv is None or not avail[lv]: break
        got.append(avail[lv].pop(0))
    rng.shuffle(got); return got

def fit_quota(quota, avail, need):
    """Quota per module restricted to the modules that have enough eligible questions; the freed slots go round-robin to the biggest remaining quotas, so n stays the same."""
    q = {m: k for m, k in quota.items() if m in avail and k and avail[m] >= k * 3}
    free = sum(quota.values()) - sum(q.values()); order = sorted(q, key=lambda m: -q[m]); i = 0
    while free > 0 and order:
        m = order[i % len(order)]
        if avail[m] >= (q[m] + 1) * 3: q[m] += 1; free -= 1
        i += 1
        if i > 1000: break
    return q

def essay_marks(it): return WRITTEN['marks'][it['level']]

def build(banks):
    """banks: {module id: bank dict (raw, bilingual)}.  Returns dict(papers, wpapers, wpool_ids, mixed, types, ...) with item ids only.
    Exam families: midterm A/B/C, final A/B/C, speed, custom (drawn in the browser), mixed sets, one test per module, hard (level 3) A/B,
    Tooley Revision Papers (grouped by the source label of each item), written A-D (worked problems, self-marked), full paper A/B (multiple choice + written)."""
    byMod = {m: [it for it in b['items'] if eligible(it)] for m, b in banks.items() if b}
    avail = {m: len(v) for m, v in byMod.items()}
    papers = []; seed = 3100; types = {}
    for tname in ('midterm', 'final'):
        t = TYPES[tname]; used = set(); quota = fit_quota(t['quota'], avail, t['n']); types[tname] = dict(t, quota=quota)
        for letter in t['papers']:
            rng = random.Random(seed); seed += 17; ids = []; alloc = allocate(quota, t['levels'], rng)
            for m in ORDER:
                k = quota.get(m, 0)
                if k and m in byMod:
                    got = pick(byMod[m], k, t['levels'], rng, used, alloc[m]); assert len(got) == k, (tname, letter, m, len(got), k); ids += [it['id'] for it in got]; used.update(it['id'] for it in got)
            papers.append(dict(id=f'{tname}-{letter}', type=tname, label=letter, ids=ids, minutes=t['minutes'], forward=t['forward']))
    types['speed'] = dict(TYPES['speed'], quota=fit_quota(TYPES['speed']['quota'], avail, TYPES['speed']['n']))
    pool = [it for m in ORDER if m in byMod for it in byMod[m]]; rng = random.Random(2025); mixed = []
    for k in range(4):                                   # four mixed practice sets of 20 questions
        mixed.append(dict(id=f'mixed-{k + 1}', type='mixed', label=str(k + 1), ids=[it['id'] for it in rng.sample(pool, 20)], minutes=30, forward=False))
    # ---- one test per module
    for m in ORDER:
        if m in byMod and avail[m] >= 24:
            rng = random.Random(7000 + int(m[1:])); got = pick(byMod[m], MODULE_TEST['n'], MODULE_TEST['levels'], rng, set())
            papers.append(dict(id=f'module-{m}', type='module', label=m.upper(), module=m, ids=[it['id'] for it in got], minutes=MODULE_TEST['minutes'], forward=False))
    # ---- hard exams: level 3 only, at most `cap` questions of one module per paper, two papers that share no question
    lv3 = {m: [it for it in byMod[m] if it['level'] == 3] for m in byMod}; used = set()
    for letter in HARD['papers']:
        rng = random.Random(9100 + ord(letter)); got = []; mods = [m for m in ORDER if lv3.get(m)]; taken = collections.Counter()
        for m in mods: lv3[m].sort(key=lambda it: rng.random() + (0 if it['origin'] == 'goc' else .5))
        while len(got) < HARD['n']:
            progress = False; rng.shuffle(mods)
            for m in mods:
                if len(got) >= HARD['n']: break
                cand = [it for it in lv3[m] if it['id'] not in used]
                if cand and taken[m] < HARD['cap']: it = cand[0]; got.append(it); used.add(it['id']); taken[m] += 1; progress = True
            if not progress: break
        rng.shuffle(got)
        if len(got) >= 10: papers.append(dict(id=f'hard-{letter}', type='hard', label=letter, ids=[it['id'] for it in got], minutes=HARD['minutes'] if len(got) >= HARD['n'] else max(15, len(got) * 1.6 // 1), forward=False))
    # ---- entry test: 20 questions of the entry bank (Floyd Chapter 1 + numeric basics), mixed levels, 25 minutes
    if byMod.get('m00') and len(byMod['m00']) >= 20:
        got = pick(byMod['m00'], 20, {1: .7, 2: .25, 3: .05}, random.Random(8100), set())
        papers.append(dict(id='entry', type='entry', label='1', ids=[it['id'] for it in got], minutes=25, forward=False))
    # ---- Tooley Revision Papers (Appendix 2): 20 questions, 25 minutes each in the book; shown with the number of questions the bank holds
    rev = collections.defaultdict(dict)
    for it in pool:
        for mm in REV.finditer(it['src']['en']): rev[int(mm.group(1))][int(mm.group(2))] = it['id']
    for n in sorted(rev):
        ids = [rev[n][q] for q in sorted(rev[n])]
        papers.append(dict(id=f'rev-{n}', type='tooley', label=str(n), ids=ids, minutes=25, forward=False, book_n=20, qnums=sorted(rev[n])))
    # ---- written papers (worked problems with the printed answer, self-marked) and full papers
    ess = {m: [e for e in b['essays']] for m, b in banks.items() if b and b['essays']}
    wused = set(); wpapers = []
    def wpick(rng, n, avoid):
        mods = [m for m in ORDER if ess.get(m)]; rng.shuffle(mods); got = []; i = 0
        for m in mods: ess[m].sort(key=lambda e: (rng.random() + (0 if e['origin'] == 'goc' else .5)) - (e['level'] - 2) * .3)
        guard = 0
        while len(got) < n and guard < 400:
            m = mods[i % len(mods)]; i += 1; guard += 1
            cand = [e for e in ess[m] if e['id'] not in avoid and e['id'] not in {g['id'] for g in got}]
            if cand: got.append(cand[0])
        return got
    for letter in WRITTEN['papers']:
        rng = random.Random(5100 + ord(letter)); got = wpick(rng, WRITTEN['n'], wused)
        if len(got) < 4: continue
        wused.update(e['id'] for e in got)
        wpapers.append(dict(id=f'written-{letter}', type='written', label=letter, ids=[], wids=[e['id'] for e in got], minutes=0, wminutes=WRITTEN['minutes'], forward=False,
                            wmarks={e['id']: essay_marks(e) for e in got}))
    fused = set(); fpool_used = set()
    for letter in FULL['papers']:
        t = dict(n=FULL['n_mcq'], levels=FULL['levels']); rng = random.Random(6100 + ord(letter)); quota = {}
        mods = [m for m in ORDER if m in byMod]; per, extra = divmod(FULL['n_mcq'], len(mods))
        for j, m in enumerate(mods): quota[m] = per + (1 if j < extra else 0)
        alloc = allocate(quota, FULL['levels'], rng); ids = []
        for m in ORDER:
            if quota.get(m): got = pick(byMod[m], quota[m], FULL['levels'], rng, fpool_used, alloc[m]); ids += [it['id'] for it in got]; fpool_used.update(it['id'] for it in got)
        w = wpick(random.Random(6200 + ord(letter)), FULL['n_ess'], wused | fused); fused.update(e['id'] for e in w)
        if len(w) == FULL['n_ess']:
            papers.append(dict(id=f'full-{letter}', type='full', label=letter, ids=ids, wids=[e['id'] for e in w], minutes=FULL['mcq_minutes'], wminutes=FULL['ess_minutes'], forward=False,
                               mcq_marks=FULL['mcq_marks'], wmarks={e['id']: FULL['ess_marks'] for e in w}))
    meta = dict(types=types, module_test=MODULE_TEST, hard={k: v for k, v in HARD.items() if k != 'papers'}, full={k: v for k, v in FULL.items() if k != 'papers'},
                written={k: v for k, v in WRITTEN.items() if k != 'papers'})
    byid = {it['id']: it for v in byMod.values() for it in v}; audit = {p['id']: dict(n=len(p['ids']), longest=sum(1 for i in p['ids'] if longest(byid[i]))) for p in papers if p['ids']}
    wids = [i for p in wpapers + [p for p in papers if p['type'] == 'full'] for i in p.get('wids', [])]
    meta['audit'] = audit
    return dict(papers=papers + wpapers, mixed=mixed, types=types, meta=meta, pool_ids=[it['id'] for it in pool], wids=wids)
