"""Assemble data/bookmap/{cengel,farokhi,elsayed}.json: tables of contents (from extract_cengel.py, extract_farokhi.py, OCR_output/_qa/elsayed_toc.json) + role of every section
for every module (core / ref / cited / optional / background / out) with the basis.  Roles follow build/modules.py (do not edit it) and the lecturer's slide titles (slides.json).
Run: python3 -I build/bookmap/extract_cengel.py && python3 -I build/bookmap/extract_farokhi.py && python3 -I build/bookmap/slides.py && python3 -I build/bookmap/build_map.py"""
import os, re, json, sys, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build')); sys.path.insert(0, os.path.dirname(__file__))
OUT = os.path.join(ROOT, 'data', 'bookmap'); OCR = os.path.join(ROOT, '..', 'OCR_output')
J = lambda n: json.load(open(os.path.join(OUT, n), encoding='utf-8'))
def R(role, basis): return dict(role=role, basis=basis)

# ----------------------------------------------------------------------------------------------- Cengel
C_SEC = {   # (chapter, section) -> {module: (role, basis)}
 '9–1': dict(m02=('core', 'slide Ch.2 tr.8–10 Considerations in the analysis of power cycles, Thermal efficiency')),
 '9–2': dict(m02=('core', 'slide Ch.2 tr.11–13 The Carnot Cycle')),
 '9–3': dict(m02=('core', 'slide Ch.2 tr.14 Air-Standard Assumptions')),
 '9–4': dict(m02=('core', 'slide Ch.2 tr.15–18 Reciprocating Engines')),
 '9–5': dict(m02=('core', 'slide Ch.2 tr.19–25 Otto Cycle; Tutorials I tr.1–6, 14–15')),
 '9–6': dict(m02=('core', 'slide Ch.2 tr.26–32 Diesel cycle; Tutorials I tr.7–13, 16–17')),
 '9–7': dict(m02=('optional', 'Stirling/Ericsson: no slide title mentions them')),
 '9–8': dict(m02=('core', 'slide Ch.2 tr.33–41 Brayton cycle; Tutorials I tr.18–23, 28–29')),
 '9–9': dict(m02=('core', 'slide Ch.2 tr.42–45 Brayton cycle with regeneration')),
 '9–10': dict(m02=('core', 'slide Ch.2 tr.46–48 Brayton cycle with intercooling, reheating')),
 '9–11': dict(m02=('core', 'slide Ch.2 tr.49–55 Ideal jet-propulsion cycles, Modifications to turbojet engines'), m01=('ref', 'slide Ch.1 tr.17–42 Jet propulsion engines')),
 '9–12': dict(m02=('optional', 'second-law analysis: not in slide titles')),
 '11–1': dict(m03=('core', 'slide Ch.3 tr.3, 9 Refrigeration cycles')),
 '11–2': dict(m03=('core', 'slide Ch.3 tr.10–14 The (reversed) Carnot cycle')),
 '11–3': dict(m03=('core', 'slide Ch.3 tr.15–25 Ideal vapor-compression cycle; Tutorials I tr.24–27')),
 '11–4': dict(m03=('core', 'slide Ch.3 tr.26 The real refrigeration process')),
 '11–5': dict(m03=('ref', 'refrigerant choice: not a slide title (tr.27–28 Refrigerating equipment is the nearest)')),
 '11–6': dict(m03=('ref', 'heat pumps: COP of heat pump appears with slide tr.20')),
 '11–7': dict(m03=('optional', 'cascade/multistage: not in slide titles')),
 '11–8': dict(m03=('ref', 'gas (reversed Brayton) cycle = closest Cengel section to the air-cycle cooling pack of slide Ch.3 tr.29–36 (the book does not describe the aircraft pack)')),
 '11–9': dict(m03=('optional', 'absorption: not in slide titles')),
}
for i, t in enumerate(['Dry and Atmospheric Air', 'Specific and Relative Humidity', 'Dew-Point Temperature', 'Adiabatic Saturation and Wet-Bulb', 'Psychrometric Chart', 'Human Comfort', 'Air-Conditioning Processes'], 1):
    C_SEC[f'14–{i}'] = dict(m03=('ref', 'modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook)'))
C_SEC.update({
 '15–1': dict(m04=('core', 'slide Ch.4 tr.3–12 FUELS AND COMBUSTION')),
 '15–2': dict(m04=('core', 'slide Ch.4 tr.13–39 Balancing the combustion equation, THEORETICAL AND ACTUAL COMBUSTION, Dew-point temperature of products, Reverse combustion analysis')),
 '15–3': dict(m04=('core', 'slide Ch.4 tr.40–55 ENTHALPY OF FORMATION AND ENTHALPY OF COMBUSTION')),
 '15–4': dict(m04=('ref', 'CLO4 "enthalpy changes in practical combustion": first-law analysis; not a slide title')),
 '15–5': dict(m04=('optional', 'adiabatic flame temperature: not in slide titles')), '15–6': dict(m04=('optional', 'entropy of reacting systems: not in slides')),
 '15–7': dict(m04=('optional', 'second-law analysis of reacting systems: not in slides')),
 '17–1': dict(m05=('core', 'slide Ch.5 tr.3–16 STAGNATION PROPERTIES; Compression of high-speed air')),
 '17–2': dict(m05=('ref', 'speed of sound/Mach number: no slide title; Mach number used from tr.14 on (to be confirmed in P3)')),
 '17–3': dict(m05=('core', 'slide Ch.5 tr.17–38 ONE-DIMENSIONAL ISENTROPIC FLOW, converging–diverging duct, property relations, critical T and p')),
 '17–4': dict(m05=('core', 'slide Ch.5 tr.39–59 ISENTROPIC FLOW THROUGH NOZZLES, back pressure, converging nozzle')),
 '17–5': dict(m05=('ref', 'shock waves: not in slide titles (tr.3–59); Farokhi Ch.2 and El-Sayed §3.8 cover them')),
 '17–6': dict(m05=('optional', 'Rayleigh flow: not in slide titles')), '17–7': dict(m05=('optional', 'steam nozzles: not in slide titles')),
})
C_CH = {  # whole-chapter roles for chapters whose sections are not listed above
 1: dict(m01=('background', 'AE1.030 review (modules.py: Cengel Ch.1–2)')), 2: dict(m01=('background', 'AE1.030 review (modules.py: Cengel Ch.1–2)')),
 3: dict(m03=('background', 'slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030)')),
 4: dict(m02=('background', 'ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030')),
 5: dict(m05=('background', 'steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030')),
 6: dict(m02=('background', 'modules.py: Cengel Ch.9 "nền: Ch.6–7"')), 7: dict(m02=('background', 'modules.py: Cengel Ch.9 "nền: Ch.6–7"'), m05=('background', 'isentropic processes of ideal gases (§7-4, §7-9)')),
 8: {}, 10: {}, 12: {}, 13: {}, 16: {},
}
STATUS_C = {10: 'out', 12: 'out', 13: 'out', 16: 'out', 8: 'out'}
def cengel():
    B = J('cengel_raw.json'); mods_used = set()
    for c in B['chapters']:
        k = c['num']
        for s in c['sections']:
            spec = C_SEC.get(s['num'], {m: v for m, v in C_CH.get(k, {}).items()})
            s['mods'] = {m: R(*v) for m, v in spec.items()}
            if not s['mods']: s['status'] = STATUS_C.get(k, 'out')
        c['mods'] = {}
        if k in (9, 11, 14, 15, 17):          # end parts of the chapters that carry the lectures: the question source for P3
            for e in c['end_parts']:
                m = {9: 'm02', 11: 'm03', 14: 'm03', 15: 'm04', 17: 'm05'}[k]
                role = ('core' if e['name'] in ('PROBLEMS', 'Review Problems', 'Fundamentals of Engineering (FE) Exam Problems') else 'ref')
                if k == 14: role = 'ref'
                e['mods'] = {m: R(role, 'end-of-chapter problems of a chapter assigned to the module' if role == 'core' else 'summary/reading/design problems')}
        else:
            for e in c['end_parts']: e['mods'] = {}
        c['mods'] = {m: v for m, v in {x for s in c['sections'] for x in []} } if False else {}
        for s in c['sections']:
            for m in s['mods']: c['mods'][m] = True
        c['mods'] = sorted(c['mods'])
    B['answers'] = dict(kind='inline', where='right after the statement of the problem, as "Answers: ..." (some problems only)',
                        recognise=r'line starting with "Answer:" or "Answers:" inside the problem list, before the next problem number "k-n"',
                        appendix=False, per_chapter={c['num']: dict(problems=c['n_problems'], with_answer=c['n_problems_with_answer']) for c in B['chapters']},
                        note='No "Answers to selected problems" appendix in the PDF (it stops at PDF p.907 = printed 881 in the middle of the FE problems of Ch.17; PDF p.908 is blank; Glossary p.909–963). Problems marked C are concept questions (no numeric answer).')
    B['offset_note'] = 'printed = PDF - 26 for PDF 27-907; Glossary PDF 909-963 is numbered separately (printed = PDF - 908). Front matter PDF 1-26 has no printed number used here.'
    return B
# ----------------------------------------------------------------------------------------------- Farokhi
F_ROLES = {   # section number or prefix -> {module: (role, basis)}
 '1': dict(m01=('ref', 'slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1)')),
 '3.1': dict(m01=('core', 'slide Ch.1 tr.7–10 Role of the engine, Principles of propulsion')), '3.2': dict(m01=('ref', 'installed thrust: deeper than the slides')),
 '3.3': dict(m01=('core', 'thrust from momentum (slide Ch.1 tr.8–10 Principles of propulsion)')), '3.4': dict(m01=('ref', 'rocket thrust: slide Ch.1 tr.14 non-airbreathing engines')),
 '3.5': dict(m01=('core', 'performance parameters (specific thrust, TSFC, efficiencies): slide Ch.1 tr.46–47 Definitions')),
 '3.6': dict(m01=('ref', 'modern engines: slide Ch.1 tr.48')), '3.7': dict(m01=('ref', 'summary')),
 '2.2': dict(m05=('background', 'thermodynamics review (AE1.030)')), '2.3': dict(m05=('core', 'isentropic relations: slide Ch.5 tr.32–35')),
 '2.4': dict(m05=('background', 'conservation laws (AE1.030)')), '2.5': dict(m05=('core', 'speed of sound and Mach number: slide Ch.5 tr.14+')),
 '2.6': dict(m05=('core', 'stagnation state: slide Ch.5 tr.3–16')), '2.7': dict(m05=('core', 'quasi-1D flow: slide Ch.5 tr.17–31')),
 '2.8': dict(m05=('core', 'area–Mach relation: slide Ch.5 tr.25–31')), '2.9': dict(m05=('core', 'sonic throat: slide Ch.5 tr.36–38')),
 '2.10': dict(m05=('ref', 'shocks: not in slide titles tr.3–59')), '2.11': dict(m05=('ref', 'normal shocks')), '2.12': dict(m05=('optional', 'oblique shocks')),
 '2.13': dict(m05=('optional', 'conical shocks')), '2.14': dict(m05=('optional', 'expansion waves')), '2.15': dict(m05=('optional', 'Rayleigh flow')),
 '2.16': dict(m05=('optional', 'Fanno flow')), '2.17': dict(m05=('optional', 'friction factor')), '2.18': dict(m05=('optional', 'dimensionless parameters')),
 '2.19': dict(m05=('optional', 'fluid impulse')), '2.20': dict(m05=('optional', 'summary of fluid impulse')), '2.1': dict(m05=('ref', 'introduction')),
 '4.1': dict(m02=('core', 'cycle analysis introduction; slide Ch.2 tr.49–52')), '4.2': dict(m02=('core', 'gas generator; slide Ch.2 tr.3 (compression, combustion, expansion)')),
 '4.3.1': dict(m02=('core', 'turbojet cycle analysis ↔ slide Ch.2 tr.49–52 Ideal jet-propulsion cycles')),
 '4.3.2': dict(m02=('ref', 'afterburner ↔ slide Ch.2 tr.53–55 Modifications to turbojet engines')), '4.3.3': dict(m02=('ref', 'turbofan ↔ slide Ch.2 tr.53–55')),
 '4.3.4': dict(m02=('optional', 'UHB turbofan')), '4.3': dict(m02=('ref', 'aircraft gas turbine engines (parent of 4.3.x)')),
 '4.4': dict(m02=('optional', 'mixed-exhaust turbofan with afterburner')), '4.5': dict(m02=('optional', 'turboprop')), '4.6': dict(m02=('ref', 'summary')),
 '6.1': dict(m05=('ref', 'inlets and nozzles')), '6.17': dict(m05=('ref', 'exhaust nozzle ↔ slide Ch.5 tr.39–49')), '6.18': dict(m05=('ref', 'gross thrust')),
 '6.19': dict(m05=('ref', 'nozzle efficiency')), '6.20': dict(m05=('ref', 'nozzle pressure ratio')),
 '6.21': dict(m05=('core', 'NPR and critical NPR ↔ slide Ch.5 tr.50–55 Effect of back pressure')), '6.22': dict(m05=('ref', 'nozzle figures of merit')),
 '6.23': dict(m05=('core', 'convergent nozzle or de Laval ↔ slide Ch.5 tr.56–59 converging nozzle')),
 '7.1': dict(m04=('ref', 'introduction')), '7.2': dict(m04=('core', 'mixture of gases ↔ slide Ch.4 tr.3–12')), '7.3': dict(m04=('core', 'chemical reaction and flame temperature ↔ slide Ch.4 tr.13–55')),
 '7.4': dict(m04=('optional', 'chemical equilibrium: not in slides')), '7.5': dict(m04=('optional', 'chemical kinetics: not in slides')), '7.6': dict(m04=('optional', 'combustion chamber design')),
 '7.7': dict(m04=('optional', 'pollutants')), '7.8': dict(m04=('ref', 'aviation fuels ↔ slide Ch.4 tr.3–12 FUELS')), '7.9': dict(m04=('optional', 'alternative jet fuels')),
 '7.10': dict(m04=('optional', 'combustion instability')), '7.11': dict(m04=('ref', 'summary')),
}
def f_role(num, chapter):
    n = num
    while n:
        if n in F_ROLES: return F_ROLES[n]
        n = n.rsplit('.', 1)[0] if '.' in n else ''
    return None
def farokhi():
    B = J('farokhi_raw.json')
    B['entries'] = [e for e in B['entries'] if e['pdf'] >= 35 or e['kind'] in ('other',)]
    for e in B['entries']:
        ch = e.get('chapter'); e['mods'] = {}
        if e['kind'] == 'chapter': e['mods'] = {m: R(*v) for m, v in F_ROLES.get(e['num'], {}).items()} if e['num'] == '1' else {}
        if e['kind'] == 'section' and e['num']:
            top = e['num'].split('.')[0]
            if top in ('1', '2', '3', '4', '6', '7'):
                r = f_role(e['num'], ch) if top != '1' else F_ROLES['1']
                if top == '6' and r is None and int(e['num'].split('.')[1]) <= 16: r = dict(m05=('ref', 'inlets (6.1–6.16): supersonic inlet shocks; not in slide titles'))
                e['mods'] = {m: R(*v) for m, v in (r or {}).items()}
            e['status'] = 'in-scope' if e['mods'] else 'out'
        if e['kind'] == 'endpart' and ch in ('1', '2', '3', '4', '6', '7'):
            m = {'1': 'm01', '2': 'm05', '3': 'm01', '4': 'm02', '6': 'm05', '7': 'm04'}[ch]
            e['mods'] = {m: R('core' if (e['title'] == 'Problems' and ch != '1') else 'ref', 'end-of-chapter ' + e['title'] + ' of an assigned chapter')}
        if e['kind'] == 'appendix':
            if e['num'] == 'App.B': e['mods'] = {'m05': R('core', 'modules.py: Appendix B Isentropic Table; slide Ch.5 uses isentropic functions (Cengel Table A-32 is the primary table)')}
            elif e['num'] in ('App.C', 'App.D', 'App.E'): e['mods'] = {'m05': R('optional', 'normal-shock/Rayleigh/Fanno tables: shocks/Rayleigh/Fanno are not in slide titles')}
            elif e['num'] == 'App.K': e['mods'] = {m: R('optional', '10-minute quiz: no answers printed; per-quiz module not assigned (? to be done in P3)') for m in ('m01', 'm02', 'm04', 'm05')}
            elif e['num'] == 'App.L': e['mods'] = {'m01': R('optional', 'rules of thumb (inlet loss, ambient T) vs TSFC/thrust: background to performance parameters')}
        e['mods'] = e['mods'] or {}
    B['answers'] = dict(appendix=False, inline=False, note='Farokhi prints neither answers to the chapter problems nor answers to the Appendix K quizzes (checked by text search for answer/solution in Problems pages and in PDF pp.1007–1024 and by image of p.1024). Companion website has instructor resources only (not available here).')
    return B
# ----------------------------------------------------------------------------------------------- El-Sayed
E_ROLES = {
 '1.1': dict(m01=('background', 'pre-jet history; slide Ch.1 does not cover it')), '1.2': dict(m01=('ref', 'jet-engine history (Whittle, von Ohain); slide Ch.1 tr.17–42 shows the engine types')),
 '1.3': dict(m01=('core', 'classification of aerospace engines ↔ slide Ch.1 tr.11–16 Aerospace engine, Classification of aerospace engine, (non-)airbreathing engines')),
 '1.4': dict(m01=('core', 'classification of jet engines ↔ slide Ch.1 tr.17–42 Jet propulsion engines, tr.43–45 Classification of propulsion systems')),
 '1.5': dict(m01=('core', 'classification of gas turbine engines ↔ slide Ch.1 tr.17–42, 48')), '1.6': dict(m01=('ref', 'industrial gas turbines')),
 '1.7': dict(m01=('core', 'non-airbreathing engines ↔ slide Ch.1 tr.14')), '1.8': dict(m01=('ref', 'future of aircraft and powerplant')),
 '2': dict(m01=('core', 'performance parameters: slide Ch.1 tr.7–10, 46–47 Definitions')),
 '4.1': dict(m02=('core', 'turbojet ↔ slide Ch.2 tr.49–52')), '4.2': dict(m02=('core', 'single-spool turbojet thermodynamic analysis (ideal/actual) ↔ slide Ch.2 tr.49–55')),
 '4.3': dict(m02=('ref', 'two-spool turbojet')), '4.4': dict(m02=('optional', 'statistical analysis')), '4.5': dict(m02=('ref', 'thrust augmentation, afterburning ↔ slide Ch.2 tr.53–55')),
 '4.6': dict(m02=('optional', 'supersonic turbojet')), '4.7': dict(m02=('optional', 'optimization of the turbojet cycle')), '4.8': dict(m02=('optional', 'micro turbojet')),
 '3.8': dict(m05=('core', 'shock waves and isentropic flow relations ↔ slide Ch.5 (modules.py: Ch.3 §3.8)')),
 '9.1': dict(m05=('ref', 'intakes')), '9.5': dict(m05=('ref', 'air intakes ↔ slide Ch.5 tr.39–49 nozzles/diffusers')), '9.6': dict(m05=('ref', 'subsonic intakes')), '9.7': dict(m05=('ref', 'supersonic intakes: shock relations')),
 '9.2': dict(m05=('optional', 'powerplant installation')), '9.3': dict(m05=('optional', 'installation')), '9.4': dict(m05=('optional', 'installation')), '9.8': dict(m05=('optional', 'intake–engine matching')), '9.9': dict(m05=('optional', 'case study')),
 '10.1': dict(m04=('ref', 'introduction')), '10.4': dict(m04=('ref', 'combustion process ↔ slide Ch.4 tr.3–12')), '10.7': dict(m04=('core', 'chemistry of combustion ↔ slide Ch.4 tr.13–39')),
 '10.8': dict(m04=('core', 'first-law analysis of combustion ↔ slide Ch.4 tr.40–55')), '10.11': dict(m04=('ref', 'aircraft fuels ↔ slide Ch.4 tr.3–12')),
 '10.2': dict(m04=('optional', 'combustor types')), '10.3': dict(m04=('optional', 'supersonic combustion chamber')), '10.5': dict(m04=('optional', 'components')), '10.6': dict(m04=('optional', 'aerodynamics')),
 '10.9': dict(m04=('optional', 'performance')), '10.10': dict(m04=('optional', 'materials')), '10.12': dict(m04=('optional', 'emissions')), '10.13': dict(m04=('optional', 'afterburner')), '10.14': dict(m04=('optional', 'supersonic combustion')),
 '11.1': dict(m05=('ref', 'introduction')), '11.2': dict(m05=('core', 'nozzle governing equations ↔ slide Ch.5 tr.39–59')), '11.3': dict(m05=('ref', 'convergent/divergent nozzle calculation ↔ slide Ch.5 tr.50–59')),
 '11.4': dict(m05=('optional', 'thrust reversal')), '11.5': dict(m05=('optional', 'thrust vectoring')), '11.6': dict(m05=('optional', 'noise')), '11.7': dict(m05=('optional', 'high-speed nozzles')), '11.8': dict(m05=('ref', 'Problems of Ch.11')),
}
def e_role(num, ch):
    n = num
    while n:
        if n in E_ROLES: return E_ROLES[n]
        n = n.rsplit('.', 1)[0] if '.' in n else ''
    return None
SCOPE = {1: (3, 74), 2: (75, 134), 3: (135, 202), 4: (203, 288), 9: (679, 738), 10: (739, 780), 11: (781, 838)}
def elsayed():
    T = json.load(open(os.path.join(OCR, '_qa', 'elsayed_toc.json'), encoding='utf-8'))
    def fl(x):
        for i in x:
            yield i
            for c in i.get('children', []): yield from fl([c])
    flat = list(fl(T['entries']))
    md = open(os.path.join(OCR, [f for f in os.listdir(OCR) if f.startswith('11_')][0]), encoding='utf-8').read().split('\n')
    pg = [None] * (len(md) + 2); cur = None
    for i, l in enumerate(md, 1):
        m = list(re.finditer(r'⟦p\.([0-9ivxlc]+)⟧', l))
        if m and not (i > 1580 and False): cur = m[0][1] if l.lstrip().startswith(('# ', '## ')) or True else cur
        pg[i] = cur
    chap = {}
    for e in flat:
        if e['depth'] and e['file'].startswith('chapter-'):
            pass
    ep = zipfile.ZipFile(os.path.join(ROOT, '..', [f for f in os.listdir(os.path.join(ROOT, '..')) if f.startswith('Aircraft Propulsion and Gas')][0]))
    names = {os.path.basename(x): x for x in ep.namelist()}; cache = {}
    def X(fn):
        if fn not in cache: cache[fn] = ep.read(names[fn]).decode('utf-8')
        return cache[fn]
    PB = r'epub:type="pagebreak"[^>]*?title="([^"]+)"'
    def epub_page(fn, anchor):
        t = X(fn); m = re.search(r'id="%s"' % re.escape(anchor), t) if anchor else None
        if not m: return None
        pb = re.findall(PB, t[:m.start()]); return pb[-1] if pb else None
    def first_page(fn):
        pb = re.findall(PB, X(fn)); return pb[0] if pb else None
    out = []; chapters = []
    for e in flat:
        m = re.match(r'^(\d+)\.\s+(.*)$', e['title']); fn = e['file']
        mm = re.match(r'^((?:\d+\.)+\d+)\s*(.*)$', e['title'])
        if not fn.startswith('chapter-'): continue
        k = int(re.match(r'chapter-(\d+)', fn)[1])
        if k not in SCOPE: continue
        if m: num, title, kind = str(k), m[2], 'chapter'
        elif mm: num, title, kind = mm[1], mm[2], 'section'
        else: num, title, kind = '', e['title'], ('endpart' if e['title'] in ('Problems', 'References') else 'other')
        printed = epub_page(fn, e['anchor']) or (first_page(fn) if kind == 'chapter' else None) or pg[e['md_line']]
        r = {}
        if kind in ('section', 'chapter') and num:
            top = num.split('.')[0]
            sp = e_role(num, k) if num != str(k) else None
            if top == '3' and not num.startswith('3.8'): sp = None
            if num == str(k) and k != 3: sp = E_ROLES.get(num) if num in E_ROLES else None
            r = {mid: R(*v) for mid, v in (sp or {}).items()}
        if kind == 'endpart' and k in SCOPE and k != 3:
            r = {{1: 'm01', 2: 'm01', 4: 'm02', 9: 'm05', 10: 'm04', 11: 'm05'}[k]: R('core' if e['title'] == 'Problems' else 'ref', 'end-of-chapter ' + e['title'])}
        out.append(dict(num=num, title=title, kind=kind, chapter=k, file=fn, anchor=e['anchor'], md_line=e['md_line'], printed=printed, depth=e['depth'], mods=r,
                        status=('in-scope' if r else 'out')))
    # examples (lines "Example n.m" alone) inside the scope chapters
    ex = []
    for i, l in enumerate(md, 1):
        m = re.fullmatch(r'Example (\d+)\.(\d+)', l.strip())
        if m and int(m[1]) in SCOPE: ex.append(dict(num=f'{m[1]}.{m[2]}', md_line=i, printed=pg[i], chapter=int(m[1])))
    # printed pages of chapters from the EPUB page-break spans
    return dict(book='elsayed', source='EPUB OPS/toc.ncx; printed pages = epub:type="pagebreak" spans = ⟦p.N⟧ in OCR_output/11_*.md', entries=out, examples=ex,
                scope=T['scope_chapters'], n_toc=T['flat_count'],
                answers=dict(appendix=False, inline=False, note='No answers/solutions to the problems anywhere in the EPUB text (no "Answer(s)" heading or Answers appendix: back matter is Appendix A Glossary, B Turbofan, C Samples of gas turbines, Index). Chapter Problems are statements only.'))
ECS = dict(
 question='CLO3: air conditioning / ECS / cooling pack / air cycle machine / bleed air in Farokhi and El-Sayed (slide Ch.3 tr.29-36 = "Air conditioner in aircraft", "AIR CYCLE COOLING PACK", "Operation of the Cooling Pack")',
 commands=["grep -n -i -E 'air.?condition|air cycle|cooling pack|environmental control|\\bECS\\b|customer bleed|cabin|pressuriz|refrigerat|\\bECU\\b' OCR_output/10_Farokhi_Aircraft_Propulsion.md",
           "grep -n -i -E 'air.?condition|air cycle|cooling pack|environmental control|\\bECS\\b|cabin|pressuriz|refrigerat|passenger|compressor bleed|customer' OCR_output/11_ElSayed_Aircraft_Propulsion_and_Gas_Turbine_Engines.md"],
 farokhi=dict(found=False, note='No hit for air conditioning, ECS, cooling pack, air cycle, customer bleed, cabin, refrigeration. The only hits are rocket propellant tank pressurization (Ch.12), turbine-cooling bleed and inlet boundary-layer bleed (not cabin air). So: không có.'),
 elsayed=dict(found='one sentence only', hits=[
   dict(printed=301, chapter=5, md_line=9970, text='Comment on a bleed ratio: "bleeding has its applications for cabin-air conditioning as well as other anti-icing functions." (turbofan Ch.5, outside the scope chapters; the sentence names the use, no ECS description, no air-cycle machine, no cooling pack)'),
   dict(printed=13, chapter=1, md_line=1698, text='history: "enclosed cabin airplane became the standard" (no ECS)'),
   dict(printed=500, chapter=6, md_line=16136, text='"Engine noise in the cabin area is reduced" (propfan; no ECS)')],
   note='Turbine-cooling bleed (Ch.5 Examples, Ch.14) and bleed valves of compressors (Ch.13) are not air-conditioning content.'),
 conclusion='Neither book describes the aircraft ECS / air cycle machine / cooling pack. Best textbook anchors for CLO3 stay Cengel Ch.11 (esp. §11-8 gas refrigeration = reversed Brayton) and Ch.14 §14-7 (air-conditioning processes); the cooling-pack slides tr.29-36 have no book counterpart.')
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    json.dump(ECS, open(os.path.join(OUT, 'ecs_search.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for name, fn in (('cengel', cengel), ('farokhi', farokhi), ('elsayed', elsayed)):
        B = fn(); json.dump(B, open(os.path.join(OUT, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(name, 'written')

# ----------------------------------------------------------------------------------------------- MAPPING.md
def mapping_md():
    from modules import MODS
    C, F, E, S, X = J('cengel.json'), J('farokhi.json'), J('elsayed.json'), J('slides.json'), J('ecs_search.json')
    o = ['# MAPPING.md — bản đồ nội dung sách ↔ module AE2.013 (P2)', '',
         'Sinh tự động bởi `build/bookmap/build_map.py` từ `data/bookmap/*.json`; kiểm bằng `build/verify/verify_bookmap.py` (FAILS: none). Vai trò: **core** = bài giảng/câu hỏi lấy từ đây; **ref** = đọc thêm; **background** = nền AE1.030; **optional** = phần phụ; mục không có vai trò nào với module = ngoài phạm vi (`out`). Cơ sở từng mục nằm trong JSON (`mods[module].basis`).', '',
         '## Bảng offset trang in ↔ trang PDF', '', '| Sách | Quy tắc | Đo bằng | Ghi chú |', '|---|---|---|---|',
         '| Cengel & Boles 5e (PDF 963 tr.) | trang in = PDF − 26 (PDF 27–907) | 349 trang đọc được số in, đều = 26; 7 mốc: PDF 44=18, 183=157, 337=311, 488=462, 623=597, 763=737, 907=881; 10 tiêu đề mục kiểm bằng ảnh | Glossary PDF 909–963 đánh số riêng: in = PDF − 908. PDF 1–26 (Contents, Preface) không dùng số in. PDF dừng ở tr.907 (in 881) giữa phần FE của Ch.17 |',
         '| Farokhi 2e (PDF 1048 tr.) | trang in = PDF − 34 (PDF 36–1031) | 962 trang đều = 34; 7 mốc: PDF 36=2, 199=165, 364=330, 526=492, 689=655, 853=819, 1031=997 | Chương 1 mở ở PDF 35 = in 1 |',
         '| El-Sayed 2e (EPUB) | không có PDF: trang in lấy từ `epub:type="pagebreak"` = dấu `⟦p.N⟧` trong `OCR_output/11_*.md` | 230/230 mục trong phạm vi khớp giữa `toc.ncx` + span pagebreak của xhtml | số trang La Mã ở phần đầu; Ch.1 3–74, Ch.2 75–134, Ch.4 203–288, Ch.9 679–738, Ch.10 739–780, Ch.11 781–838 |', '']
    def sec_lines(entries, mid, pdfkey=True, roles=('core', 'ref', 'background')):
        L = []
        for e in entries:
            v = e['mods'].get(mid)
            if v and v['role'] in roles:
                num = e.get('num') or ''
                L.append((e, v))
        return L
    o += ['## Module × nguồn', '']
    for m in MODS:
        mid = m['id']; o += [f'### {mid} — {m["vi"]}', '']
        sl = ', '.join(f'{d} tr.{a}–{b}' for d, a, b in m['slides'])
        o.append(f'Slide: {sl}' + (f' (trống: ' + ', '.join(f'{d} tr.{a}–{b}' for d, a, b in m['blank_slides']) + ')' if m['blank_slides'] else '') + '. Tiêu đề slide: xem `data/bookmap/slides.json`.'); o.append('')
        o += ['**Cengel & Boles**', '', '| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |', '|---|---|---|---|---|---|']
        for c in C['chapters']:
            for s in c['sections']:
                v = s['mods'].get(mid)
                if v: o.append(f'| {s["num"]} | {s["title"]} | {v["role"]} | {s["printed"]}–{s["pdf_end"] - 26} | {s["pdf"]}–{s["pdf_end"]} | {v["basis"]} |')
            for e in c['end_parts']:
                v = e.get('mods', {}).get(mid)
                if v: o.append(f'| Ch.{c["num"]} | {e["name"].title()} | {v["role"]} | {e["printed"]} | {e["pdf"]} | {v["basis"]} |')
        o += ['', '**Farokhi**', '', '| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |', '|---|---|---|---|---|---|']
        for e in F['entries']:
            v = e['mods'].get(mid)
            if v and (e['kind'] != 'section' or e['level'] == 2): o.append(f'| {e["num"] or "Ch." + str(e.get("chapter"))} | {e["title"]} | {v["role"]} | {e["printed"]} | {e["pdf"]}–{e["pdf_end"]} | {v["basis"]} |')
        o += ['', '**El-Sayed**', '', '| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |', '|---|---|---|---|---|---|']
        for e in E['entries']:
            v = e['mods'].get(mid)
            if v and e['depth'] <= 2 and (e['kind'] != 'chapter'): o.append(f'| {e["num"] or "Ch." + str(e["chapter"])} | {e["title"]} | {v["role"]} | {e["printed"]} | {e["file"]}:{e["md_line"]} | {v["basis"]} |')
        o.append('')
    o += ['## Phần cuối chương và ví dụ (cho quét bài tập ở giai đoạn sau)', '', '### Cengel (tr. PDF; tr. in = PDF − 26)', '', '| Ch. | Summary | References | Problems | Review Problems | FE Exam | Design & Essay | Topic of Special Interest | #bài | #bài có "Answers:" |', '|---|---|---|---|---|---|---|---|---|---|']
    for c in C['chapters']:
        g = {e['name']: e['pdf'] for e in c['end_parts']}
        o.append(f'| {c["num"]} | {g.get("SUMMARY", "—")} | {g.get("REFERENCES AND SUGGESTED READING", "—")} | {g.get("PROBLEMS", "—")} | {g.get("Review Problems", "—")} | {g.get("Fundamentals of Engineering (FE) Exam Problems", "—")} | {g.get("Design and Essay Problems", "—")} | {c["features"][0]["pdf"] if c["features"] else "—"} | {c["n_problems"]} | {c["n_problems_with_answer"]} |')
    o += ['', f'**Đáp án in của Cengel:** {C["answers"]["where"]}. Nhận biết: {C["answers"]["recognise"]}. {C["answers"]["note"]} Tổng: 469 trong 2610 bài (đếm bằng script, `verify_bookmap.py`).', '',
          '### Farokhi (tr. PDF; in = PDF − 34)', '', '| Ch. | PDF đầu–cuối | References | Problems (đầu–cuối) | Ví dụ (E X A M P L E) |', '|---|---|---|---|---|']
    ents = F['entries']
    for ch in ('1', '2', '3', '4', '6', '7'):
        c = next(e for e in ents if e['kind'] == 'chapter' and e['num'] == ch)
        rf = next((e for e in ents if e['kind'] == 'endpart' and e['chapter'] == ch and e['title'] == 'References'), None); pb = next((e for e in ents if e['kind'] == 'endpart' and e['chapter'] == ch and e['title'] == 'Problems'), None)
        exs = F['examples'].get(ch, []); es = ', '.join(f'{x["num"]}@{x["pdf"]}' for x in exs) or ('không có ví dụ đánh số' if ch == '1' else '—')
        o.append(f'| {ch} | {c["pdf"]}–{c["pdf_end"]} | {rf["pdf"] if rf else "—"} | {pb["pdf"] if pb else "—"}–{pb["pdf_end"] if pb else "—"} | {es} |')
    for ap in ('App.B', 'App.K', 'App.L'):
        e = next(x for x in ents if x['kind'] == 'appendix' and x['num'] == ap)
        o.append(f'| {ap} {e["title"]} | {e["pdf"]}–{e["pdf_end"]} | — | — | — |')
    o += ['', f'Appendix K: 45 bài quiz 10 phút (mỗi quiz một bookmark, PDF 1007–1024), **không in đáp án** (kiểm bằng text và ảnh tr.1024). Bài tập cuối chương Farokhi **không in đáp án**. Appendix L (PDF 1025–1032) là bảng quy tắc ngón tay cái (thay đổi % lực đẩy/TSFC), không có bài tập. Chưa gán quiz nào cho module cụ thể (`?`, để P3).', '',
          '### El-Sayed (tr. in; dòng trong 11_*.md)', '', '| Ch. | Trang in | Problems (tr. in : dòng) | References | Số ví dụ "Example n.m" |', '|---|---|---|---|---|']
    for k in (1, 2, 3, 4, 9, 10, 11):
        ch = [e for e in E['entries'] if e['chapter'] == k]; c0 = next(e for e in ch if e['kind'] == 'chapter')
        pb = next((e for e in ch if e['kind'] == 'endpart' and e['title'] == 'Problems'), None); rf = next((e for e in ch if e['kind'] == 'endpart' and e['title'] == 'References'), None)
        ne = sum(1 for x in E['examples'] if x['chapter'] == k)
        o.append(f'| {k} {c0["title"]} | {SCOPE[k][0]}–{SCOPE[k][1]} | {pb["printed"] if pb else "—"} : {pb["md_line"] if pb else ""} | {rf["printed"] if rf else "—"} | {ne} |')
    o += ['', f'**Đáp án in của El-Sayed:** không. {E["answers"]["note"]}', '', '## CLO3 — tìm ECS / cooling pack / air cycle machine / bleed air', '', f'- Câu hỏi: {X["question"]}', '- Lệnh grep đã dùng:'] + [f'  - `{c}`' for c in X['commands']] + ['',
          f'- **Farokhi:** KHÔNG CÓ. {X["farokhi"]["note"]}', '- **El-Sayed:** gần như không có; chỉ có các câu sau:'] + [f'  - tr. in {h["printed"]} (Ch.{h["chapter"]}, dòng {h["md_line"]}): {h["text"]}' for h in X['elsayed']['hits']] + [f'  - {X["elsayed"]["note"]}', f'- Kết luận: {X["conclusion"]}', '',
          '## Slide (tiêu đề từng trang: `data/bookmap/slides.json`)', '', '| Deck | Tổng trang | content | blank | title/out |', '|---|---|---|---|---|']
    for k, v in S.items():
        sl = v['slides']; o.append(f'| {k} | {v["pages"]} | {sum(1 for s in sl if s["kind"] == "content")} | {sum(1 for s in sl if s["kind"] == "blank")} | {sum(1 for s in sl if s["kind"] in ("title", "out"))} |')
    o += ['', 'Ghi chú: các deck không có tiêu đề slide dạng placeholder; "tiêu đề" = dòng chữ đầu tiên của trang trong `OCR_output/02…07_*.md`. Ch.1 tr.17–42 đều mang tên "Jet propulsion engines" (26 trang).', '',
          '## Lỗi / lệch tìm thấy', '',
          '- Cengel, trang Contents (PDF 2–17) đánh số lệch ở Ch.6: bỏ qua 6–4, các mục 6–5…6–12 trong Contents tương ứng 6–4…6–11 trong thân sách (mục cuối "The Carnot Refrigerator and Heat Pump" là 6–11 ở tr. in 309/PDF 335 — xem ảnh). Bản đồ dùng số trong thân sách. Ch.7: Contents ghi mục "Entropy Balance" là 7–13 (khớp thân sách), Ch.12: mục 12–4 "General Relations" có trong thân sách nhưng thiếu ở Contents (tên lấy từ tiêu đề thân sách).',
          '- Cengel, mục tên trong Contents đôi chỗ khác chữ hoa/thường so với thân sách ("Brayton Cycle:  The Ideal…"); dùng tên trong Contents.',
          '- Cengel PDF dừng ở PDF 907 (in 881) giữa các bài FE của Ch.17: không có phần còn lại và không có phụ lục đáp án.',
          '- Cengel text layer mất ký hiệu (=, −, Hy Lạp) nên khớp tiêu đề chỉ theo chữ/số; 10 tiêu đề kiểm bằng ảnh: 6–11, 9–8, 9–9, 9–10, 9–11, 11–3, 11–8, 14–7, 15–3, 17–4 (trang và số in đúng).',
          '- El-Sayed: dấu `⟦p.N⟧` trong bản chữ đôi khi đặt trễ vài dòng so với span pagebreak của EPUB (9.3, 11.2…); bản đồ dùng span trong xhtml (verify 230/230).',
          '- El-Sayed Ch.1 trong `modules.py` ghi "Ch.1 History and Classifications" và Ch.2 "Performance Parameters": đúng. Ch.4 là Turbojet; slide Ch.2 (Brayton, jet-propulsion cycle) khớp §4.2 hơn là phần turbofan (Ch.5, ngoài `modules.py`).', '',
          '## Đề xuất sửa `build/modules.py` (không tự sửa)', '',
          '1. m03: ghi rõ Farokhi/El-Sayed = "không có mục về ECS/cooling pack (đã grep, xem phần CLO3)"; thay "chưa tìm thấy" bằng kết luận chắc. Cân nhắc thêm Cengel §11-8 (gas refrigeration) làm mục gần nhất với air cycle cooling pack và §14-7.',
          '2. m01: Cengel Ch.1–2 chỉ có vai trò `background`; Farokhi Ch.1 là `ref` (lịch sử), Ch.3 mới là `core`. Có thể thêm Cengel §9-11 (jet-propulsion) và El-Sayed §1.3–1.5 (phân loại) vào danh sách sách của m01.',
          '3. m02: thêm Farokhi §4.3.1 (turbojet) và El-Sayed §4.2 làm `core`; phần còn lại Ch.4 là `ref`/`optional`.',
          '4. m05: slide Ch.5 tr.3–59 chỉ tới converging nozzle (Cengel §17-1…17-4); Cengel §17-5 (sóng xung kích), Farokhi §2.10–2.14 và El-Sayed §3.8 là phần sách rộng hơn slide (`ref`).',
          '5. m04: Cengel §15-2 (balancing, dew point, reverse analysis) và §15-3 là phần lõi; thêm Farokhi §7.2–7.3 và El-Sayed §10.7–10.8 làm `core` thay vì cả chương.', '',
          '## Chưa làm', '', '- Gán từng bài Quiz Appendix K (45) cho module.', '- Phân loại chi tiết tiểu mục (subsection) Cengel (có trong `subs` nhưng chưa có trang riêng).', '- Chưa xác nhận Cengel §17-2 (speed of sound) có nằm trong slide Ch.5 hay không (không có tiêu đề riêng).', '- `build/bookmap_body.py`/`_shared/bookmap.js` (trang HTML) chưa chỉnh cho dữ liệu mới: ngoài phạm vi P2 này.']
    open(os.path.join(ROOT, 'MAPPING.md'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
if __name__ == '__main__':
    mapping_md(); print('MAPPING.md written')
