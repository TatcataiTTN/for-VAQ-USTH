"""Combine the four tables of contents with the module assignment and the question banks -> data/bookmap/map.json.
Role of a book section for a module:
  core        lesson text and/or questions of the module are built from it
  lab         used for the servomotor lab (m10)
  ref         reading reference named by the syllabus map; mapped but NOT quoted (all Jaeger sections, Floyd Application Activities for m09)
  cited       the lesson notes mention it although it is not declared
  optional    chapter feature (Application Activity / Programmable Analog Technology) inside a module chapter, not used by the lessons
Status of a section nobody uses:  background (prerequisite device theory) | other (same chapter, deeper than the course) | out (outside the syllabus)
Run: python3 -I build/bookmap/build_map.py   (after extract.py and easa_sv.py)"""
import os, re, sys, json, glob, importlib.util
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build'))
import hx
D = os.path.join(ROOT, 'data', 'bookmap'); PDFDIR = os.path.join(ROOT, '..', 'pdf_ocr_fixed')
MIDS = ['m01', 'm02', 'm03', 'm04', 'm05', 'm06', 'm07', 'm08', 'm09', 'm10']
PRIO = ['core', 'lab', 'ref', 'cited', 'optional']
def jl(n): return json.load(open(os.path.join(D, n), encoding='utf-8'))
def setrole(d, mid, role):
    if mid not in d or PRIO.index(role) < PRIO.index(d[mid]): d[mid] = role

# ----------------------------------------------------------------------------- declared assignments (checked against build/modules.py by verify_bookmap.py)
FLOYD_CHAPTER = {'m02': 12, 'm03': 13, 'm05': 14, 'm06': 15, 'm07': 16, 'm08': 17}
FLOYD_SECTIONS = {'m04': [('6–6', 'core'), ('7–2', 'core'), ('7–3', 'core'), ('12–3', 'core')],
                  'm10': [('9–4', 'lab'), ('16–6', 'lab')]}
JAEGER = {  # module -> {chapter: [section ranges]}   (from the syllabus map in modules.py)
 'm01': {6: ['6.1-6.4', '6.11'], 7: ['7.1-7.5'], 9: ['9.2', '9.12-9.15']},
 'm02': {10: ['10.5-10.9'], 11: ['11.2', '11.11-11.13']},
 'm03': {10: ['10.9-10.10'], 12: ['12.8-12.9']},
 'm04': {11: ['11.1', '11.10'], 12: ['12.1']},
 'm05': {12: ['12.2', '12.5-12.6']},
 'm06': {12: ['12.3']},
 'm07': {12: ['12.7', '12.9']},
}
# EASA SM01 rows by title -> [(module, role)]  (SM02 -> m09 and SM03 -> m10 wholesale)
EASA_SM1_BACKGROUND_UNTIL = 'Simple Circuits'      # everything before it: diodes, transistors, thyristors = device theory of the previous course
EASA_RULES = [
 (['Simple Circuits', 'Biasing', 'Configurations', 'Common-Emitter Configuration', 'Common-Collector Configuration', 'Common-Base Configuration'], []),   # background
 (['Basic Amplifier Circuits', 'Class A Amplifiers', 'Class AB Amplifiers', 'Class B Amplifier', 'Class C Amplifier', 'Cascade Amplifiers',
   'Feedback and Stabilization', 'Direct Coupling', 'Resistive-Capacitive Coupling', 'Impedance Coupling', 'Transformer Coupling', 'Push-Pull Amplifiers',
   'Positive and Negative Feedback'], [('m04', 'core')]),
 (['Oscillators', 'Multivibrators'], [('m04', 'core'), ('m07', 'ref')]),
 (['Flip-flop Circuits'], [('m01', 'ref')]),
 (['Integrated Circuits', 'Binary Numbering System', 'Place Values', 'Binary Number System Conversion', 'Binary-Coded Decimals', 'Logic Gates', 'NOT Gate', 'Buffer Gate',
   'AND Gate', 'OR Gate', 'NAND Gate', 'NOR Gate', 'Exclusive OR Gate', 'Exclusive NOR Gate', 'Negative Logic Gates', 'Aircraft Logic Gate Applications', 'Logic Circuits',
   'Adder Logic Circuits', 'Flip-Flop Logic Circuits', 'Comparator Logic Circuits', 'Encoder Logic Circuits', 'Decoder Logic Circuits', 'Scale of Integration', 'Questions'],
  [('m01', 'core')]),
 (['Linear Circuits and Operational Amplifiers'], [('m02', 'ref'), ('m03', 'ref')]),
 (['Voltage Follower Circuit', 'Multivibrator Circuit', 'Integrator Circuit', 'Differentiator Circuit'], [('m03', 'core')]),
]

def rng_to_set(items):
    out = set()
    for it in items:
        m = re.match(r'^(\d+)\.(\d+)(?:-(\d+)\.(\d+))?$', it); a, b = int(m[2]), int(m[4]) if m[4] else int(m[2])
        out |= {f'{m[1]}.{k}' for k in range(a, b + 1)}
    return out

# ----------------------------------------------------------------------------- lesson text (what the lessons really cite)
def flat(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from flat(v)
    elif isinstance(o, (list, tuple)):
        for v in o: yield from flat(v)
def lesson_cites():
    out = {}
    for m in MIDS:
        spec = importlib.util.spec_from_file_location(m, os.path.join(ROOT, 'build', 'content', f'{m}.py')); mod = importlib.util.module_from_spec(spec)
        hx.LANG = 'en'; spec.loader.exec_module(mod); t = ' '.join(flat(mod.module('en')))
        t = re.sub(r'(?:has no|không có) §\d+–\d+/\d+–\d+', '', t)      # a sentence that says a section does not exist is not a citation
        out[m] = sorted({x.replace('-', '–') for x in re.findall(r'Floyd\s*(?:9e\s*)?§\s*(\d{1,2}[–-]\d{1,2})', t)} | {x.replace('-', '–') for x in re.findall(r'§\s*(\d{1,2}[–-]\d{1,2})', t)})
    return out

# ----------------------------------------------------------------------------- question banks
def src_en(i): return i['src']['en'] if isinstance(i['src'], dict) else i['src']
def load_items():
    allitems = {}
    for m in MIDS:
        b = json.load(open(os.path.join(ROOT, 'data', 'qbank', f'{m}.json'), encoding='utf-8'))
        allitems[m] = b['items'] + b.get('essays', [])
    return allitems
FLOYD_KIND = {'True/False Quiz': 'TRUE/FALSE QUIZ', 'Self-Test': 'SELF-TEST', 'Circuit-Action Quiz': 'CIRCUIT-ACTION QUIZ', 'Problem': 'PROBLEMS'}
def bump(d, key, k, n=1, page=None):
    d.setdefault(key, {}); d[key][k] = d[key].get(k, 0) + n
    if page is not None: d[key].setdefault('pages', [])
    if page is not None and page not in d[key]['pages']: d[key]['pages'] = sorted(d[key]['pages'] + [page])

def main():
    floyd, jaeger, easa, servo = jl('floyd.json'), jl('jaeger5.json'), jl('easa.json'), jl('servo.json')
    cites = lesson_cites(); items = load_items()
    # ---- Floyd
    fl_text = open(os.path.join(PDFDIR, 'text', 'Floyd_Electronic_Devices_9e_fixed.txt'), encoding='utf-8').read().split('===== PAGE ')
    pages = {int(p.split(' =====')[0]): p for p in fl_text[1:]}
    for ch in floyd['chapters']:
        first_end = min((m['pdf'] for m in ch['end_parts']), default=None)
        entries = ch['sections']
        for j, e in enumerate(entries):
            end = (entries[j + 1]['pdf'] - 1) if j + 1 < len(entries) else ch['pdf_end']
            if first_end and e['pdf'] < first_end <= end: end = first_end - 1
            e['pdf_end'] = max(e['pdf'], end); e['printed_end'] = e['pdf_end'] - floyd['offset']; e['mods'] = {}; e['q'] = {}
        eps = ch['end_parts']
        for j, e in enumerate(eps):
            e['pdf_end'] = eps[j + 1]['pdf'] if j + 1 < len(eps) else max(e['pdf'], next((s['pdf'] for s in entries if s['pdf'] > e['pdf']), ch['pdf_end'] + 1) - 1)
            e['mods'] = {}; e['q'] = {}
        ch['mods'] = {}
    byname = {c['num']: c for c in floyd['chapters']}
    def fsec(num):
        for c in floyd['chapters']:
            for s in c['sections']:
                if s['num'] == num: return c, s
        raise KeyError(num)
    for mid, chn in FLOYD_CHAPTER.items():
        ch = byname[chn]
        for s in ch['sections']: setrole(s['mods'], mid, 'core' if s['kind'] == 'section' else 'optional')
        for e in ch['end_parts']: setrole(e['mods'], mid, 'core')
    for mid, lst in FLOYD_SECTIONS.items():
        for num, role in lst: setrole(fsec(num)[1]['mods'], mid, role)
    for mid, lst in cites.items():
        for num in lst:
            try: setrole(fsec(num)[1]['mods'], mid, 'cited')
            except KeyError: pass                                  # reported by verify_bookmap.py
    # m09: Floyd Application Activities that deal with a circuit board (named by the syllabus map, not read)
    for ch in floyd['chapters']:
        for s in ch['sections']:
            if s['kind'] == 'feature' and s['title'] == 'Application Activity':
                t = ' '.join(pages.get(p, '') for p in range(s['pdf'], s['pdf_end'] + 1)).lower()
                n = len(re.findall(r'pc board|circuit board|printed circuit', t)); s['pcb_mentions'] = n
                if n >= 8: setrole(s['mods'], 'm09', 'ref')
    # ---- Floyd question counts
    for mid, its in items.items():
        for i in its:
            s = src_en(i); k = 'goc' if i['origin'] == 'goc' else 'cited'
            m = re.match(r'^Floyd \d+e, Ch\.(\d+), (True/False Quiz|Self-Test|Circuit-Action Quiz|Problem) (?:Q)?(\d+) \(p\.(\d+)\)', s)
            if m:
                ch = byname[int(m[1])]; part = next((e for e in ch['end_parts'] if e['name'] == FLOYD_KIND[m[2]]), None)
                if part: bump(part['q'], mid, 'quoted'); setrole(part['mods'], mid, 'core')
                continue
            m = re.match(r'^Generated – modelled on Floyd (Self-Test Q|Problem|CA Q)(\d+)', s) or re.match(r'^Generated – conceptual variant of Floyd Ch\.(\d+) (Self-Test)', s)
            if m and mid in FLOYD_CHAPTER:
                kind = {'Self-Test Q': 'SELF-TEST', 'Problem': 'PROBLEMS', 'CA Q': 'CIRCUIT-ACTION QUIZ', 'Self-Test': 'SELF-TEST'}[m[1] if not m[1].isdigit() else m[2]]
                ch = byname[FLOYD_CHAPTER[mid]]; part = next((e for e in ch['end_parts'] if e['name'] == kind), None)
                if part: bump(part['q'], mid, 'modelled')
                continue
            m = re.match(r'^Generated – modelled on Floyd Section (\d+–\d+)', s)
            if m:
                bump(fsec(m[1])[1]['q'], mid, 'modelled')
    # ---- Jaeger (reading references only)
    jch = {c['num']: c for c in jaeger['chapters']}
    for ch in jaeger['chapters']:
        ch['mods'] = {}
        for s in ch['sections']: s['mods'] = {}; s['q'] = {}
    for mid, d in JAEGER.items():
        for chn, rngs in d.items():
            want = rng_to_set(rngs); found = set()
            for s in jch[chn]['sections']:
                if s['num'] in want: setrole(s['mods'], mid, 'ref'); found.add(s['num'])
            assert found == want, (mid, chn, want - found)
    # ---- EASA
    rows = easa['rows']
    for i, r in enumerate(rows):
        nxt = next((x for x in rows[i + 1:] if x['sm'] == r['sm'] and x['level'] <= r['level']), None)
        sm = easa['submodules'][str(r['sm'])]
        r['pdf_end'] = max(r['pdf'], nxt['pdf'] if nxt else sm['last']); r['printed'] = r['pdf'] - sm['offset']; r['mods'] = {}; r['q'] = {}
        r['printed_label'] = f"{r['sm']}.{r['printed']}"
    index_of = {(r['sm'], r['title']): r for r in rows}
    for r in rows:
        if r['sm'] == 2: setrole(r['mods'], 'm09', 'core')
        if r['sm'] == 3: setrole(r['mods'], 'm10', 'core')
    for titles, mods in EASA_RULES:
        for t in titles:
            r = index_of[(1, t)]
            for mid, role in mods: setrole(r['mods'], mid, role)
    # ---- SERVO
    srows = servo['rows']
    for i, r in enumerate(srows):
        nxt = next((x for x in srows[i + 1:] if x['level'] <= r['level']), None)
        r['pdf_end'] = max(r['pdf'], (nxt['pdf'] if nxt else servo['pages'])); r['mods'] = {'m10': 'core'}; r['q'] = {}
    # ---- EASA / SERVO question counts (page spans)
    def within(r, n): return r['pdf'] <= n <= r['pdf_end']
    for mid, its in items.items():
        for i in its:
            s = src_en(i)
            m = re.match(r'^EASA M04 SM0?(\d), p\.(\d)\.(\d+) \(PDF p\.(\d+)\)', s)
            m2 = re.match(r'^EASA M04 SM0?(\d), Question (\d+)-(\d+) \(p\.(\d)\.(\d+)\), printed answer', s)
            if m or m2:
                sm = int(m[1]) if m else int(m2[1]); n = int(m[4]) if m else int(m2[5]) + easa['submodules'][str(sm)]['offset']
                tgt = [r for r in rows if r['sm'] == sm and within(r, n) and r['title'] != 'Knowledge Requirements']
                if (m2 or (easa['submodules'][str(sm)]['qa'][0] <= n)):
                    tgt = [r for r in rows if r['sm'] == sm and r['title'] == 'Questions']
                for r in tgt:
                    bump(r['q'], mid, 'quoted' if (m2 or i['origin'] == 'goc') else 'cited', page=n); setrole(r['mods'], mid, 'cited')
                continue
            m = re.match(r'^(Generated – modelled on )?SERVOMECHANISM \(sv\),? ?p\.(\d+)', s)
            if m:
                n = int(m[2]); tgt = [r for r in srows if within(r, n) and r['level'] >= 1]
                # deepest sections only (a page can sit in a chapter, a section and a subsection)
                deep = max((r['level'] for r in tgt), default=0); tgt = [r for r in tgt if r['level'] == deep]
                for r in tgt: bump(r['q'], mid, 'modelled' if m[1] else 'cited', page=n)
    # ---- module summary
    modsum = {}
    for mid, its in items.items():
        n = len(its); goc = sum(1 for i in its if i['origin'] == 'goc'); gen = sum(1 for i in its if src_en(i).startswith('Generated'))
        modsum[mid] = dict(items=n, original=goc, generated=gen, grounded=n - goc - gen, lesson_cites=cites[mid])
    json.dump(dict(floyd=floyd, jaeger5=jaeger, easa=easa, servo=servo, modules=modsum), open(os.path.join(D, 'map.json'), 'w'), ensure_ascii=False, indent=1)
    # ---- console summary
    def used(rs): return sum(1 for r in rs if r['mods'])
    fs = [s for c in floyd['chapters'] for s in c['sections']]; js = [s for c in jaeger['chapters'] for s in c['sections']]
    print(f"Floyd entries {len(fs)} used {used(fs)} | end parts {sum(len(c['end_parts']) for c in floyd['chapters'])} | Jaeger sections {len(js)} mapped {used(js)} | EASA rows {len(rows)} used {used(rows)} | SERVO rows {len(srows)}")
    for mid in MIDS: print(' ', mid, modsum[mid])

if __name__ == '__main__': main()
