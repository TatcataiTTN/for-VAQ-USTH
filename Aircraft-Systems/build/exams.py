"""Mock-exam definitions: Midterm, Final, Speed, Custom and the mixed sets.
The syllabus (AE2.021) does not state an exam format, so the structure below is THIS SITE'S OWN DESIGN and is shown as such on the page:
  Midterm  modules 01-04 (number systems, logic, integrated circuits, computer and CPU), 30 questions, 45 minutes, forward-only, three fixed papers A/B/C and a random draw
  Final    all nine modules, 45 questions, 60 minutes, free navigation, three fixed papers A/B/C and a random draw
  Speed    20 questions drawn at random from every module, 15 minutes, free navigation
  Custom   the learner chooses modules, number of questions, minutes, forward-only or not
Quotas per module follow the amount of lecture material (number of lecturer slides per module; module 07 is a 6-page document, so it gets a small quota).
Papers are reproducible (fixed seed), the three papers of one type do not overlap, levels are mixed and textbook/lecturer originals are favoured."""
import random, collections

ORDER = ['m01', 'm02', 'm03', 'm04', 'm05', 'm06', 'm07', 'm08', 'm09']
TYPES = {
    'midterm': dict(n=30, minutes=45, forward=True, quota=dict(m01=4, m02=9, m03=9, m04=8), levels={1: .45, 2: .40, 3: .15}, papers='ABC'),
    'final': dict(n=45, minutes=60, forward=False, quota=dict(m01=4, m02=8, m03=8, m04=7, m05=3, m06=5, m07=2, m08=4, m09=4), levels={1: .40, 2: .40, 3: .20}, papers='ABC'),
    'speed': dict(n=20, minutes=15, forward=False, quota=dict(m01=2, m02=3, m03=3, m04=3, m05=1, m06=2, m07=1, m08=2, m09=3), levels={1: .45, 2: .40, 3: .15}, papers=''),
}
for t in TYPES.values(): assert sum(t['quota'].values()) == t['n'], t
KINDS = ('mcq', 'ca')                                   # true/false items (2 options) are left out: a coin flip is not an exam question

def eligible(it): return it['kind'] in KINDS and 3 <= len(it['opts']) <= 6

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
    for lv in avail: avail[lv].sort(key=lambda it: rng.random() + (0 if it['origin'] == 'goc' else 0.5))
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

def build(banks):
    """banks: {module id: bank dict (raw, bilingual)}.  Returns dict(papers=[...], mixed=[...], types=...) with item ids only."""
    byMod = {m: [it for it in b['items'] if eligible(it)] for m, b in banks.items() if b}
    papers = []; seed = 3100
    for tname in ('midterm', 'final'):
        t = TYPES[tname]; used = set()
        for letter in t['papers']:
            rng = random.Random(seed); seed += 17; ids = []; alloc = allocate({m: k for m, k in t['quota'].items() if m in byMod}, t['levels'], rng)
            for m in ORDER:
                k = t['quota'].get(m, 0)
                if k and m in byMod:
                    got = pick(byMod[m], k, t['levels'], rng, used, alloc[m]); assert len(got) == k, (tname, letter, m, len(got), k); ids += [it['id'] for it in got]; used.update(it['id'] for it in got)
            papers.append(dict(id=f'{tname}-{letter}', type=tname, label=letter, ids=ids, minutes=t['minutes'], forward=t['forward']))
    pool = [it for m in ORDER if m in byMod for it in byMod[m]]; rng = random.Random(2025); mixed = []
    for k in range(4):                                   # four mixed practice sets of 20 questions
        mixed.append(dict(id=f'mixed-{k + 1}', type='mixed', label=str(k + 1), ids=[it['id'] for it in rng.sample(pool, 20)], minutes=30, forward=False))
    return dict(papers=papers, mixed=mixed, types={k: {kk: vv for kk, vv in v.items() if kk != 'papers'} for k, v in TYPES.items()}, pool_ids=[it['id'] for it in pool])
