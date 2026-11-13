"""Sinh tests/props_cases.json: ~400 loi goi + ket qua cua props.py (Node so sanh).  python3 -I build/props/gen_cases.py"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import props as p
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rnd = random.Random(20261113)
C = []
def add(fn, *args):
    C.append(dict(fn=fn, args=list(args)))
for sub in ('water', 'R134a'):
    for _ in range(18):
        t = p._load('A4' if sub == 'water' else 'A11'); xs = [r[0] for r in t['rows']]
        add('sat_T', sub, round(rnd.uniform(xs[0], xs[-1]), 2), rnd.choice(['hf', 'hg', 'hfg', 'vg', 'sg', 'ug', 'Psat_kPa']))
        t = p._load('A5' if sub == 'water' else 'A12'); xs = [r[0] for r in t['rows']]
        add('sat_P', sub, round(rnd.uniform(xs[0], xs[-1]), 1), rnd.choice(['hf', 'hg', 'Tsat_C', 'vf', 'sf', 'sfg']))
        add('wet_T', sub, round(rnd.uniform(xs[0] if sub == 'water' else -40, 100), 1) if sub == 'water' else round(rnd.uniform(-40, 100), 1), round(rnd.uniform(0, 1), 3), rnd.choice(['h', 'u', 's', 'v']))
    add('sat_T', sub, 100 if sub == 'water' else 0, 'hg')
    add('quality', sub, 'T', 60 if sub == 'water' else 20, 'h', 1000 if sub == 'water' else 150)
for _ in range(25):
    add('superheated', 'water', round(rnd.uniform(0.01, 60), 3), round(rnd.uniform(40, 1300), 1), rnd.choice(['v', 'u', 'h', 's']))
    add('superheated', 'R134a', round(rnd.uniform(0.06, 1.6), 3), round(rnd.uniform(-20, 180), 1), rnd.choice(['v', 'u', 'h', 's']))
    add('compressed', round(rnd.uniform(5, 50), 2), round(rnd.uniform(0, 380), 1), rnd.choice(['v', 'u', 'h', 's']))
    add('air', round(rnd.uniform(200, 2250), 2), rnd.choice(['h', 'u', 'Pr', 'vr', 's0']))
    add('air', round(rnd.uniform(360, 5300), 2), rnd.choice(['h', 'u', 'Pr', 'vr', 's0']), 'E')
    add('air_inverse', rnd.choice(['h', 'Pr', 'u', 'vr', 's0']), round(rnd.uniform(5, 300), 3))
    for g in p.GAS:
        add('gas_kmol', g, round(rnd.uniform(300, 3000), 1), rnd.choice(['h', 'u', 's0']))
    add('isentropic', round(rnd.uniform(0, 5), 3), rnd.choice(['Ma_star', 'A_Astar', 'P_P0', 'rho_rho0', 'T_T0']))
    add('isentropic_inverse', rnd.choice(['P_P0', 'T_T0', 'rho_rho0']), round(rnd.uniform(0.02, 0.99), 3))
    add('isentropic_inverse', 'A_Astar', round(rnd.uniform(1.0, 5), 3), rnd.choice(['sub', 'sup']))
for _ in range(12):
    add('superheated_inverse', 'R134a', round(rnd.uniform(0.06, 1.6), 3), 's', round(rnd.uniform(0.93, 1.3), 4))
    add('superheated_inverse', 'water', round(rnd.uniform(0.01, 30), 3), 'h', round(rnd.uniform(2600, 4500), 1))
for fn, args in [('cp_poly', ('Air', 500)), ('cp_poly', ('CO2', 1000, True)), ('cp_poly', ('Nitrogen', 2500)), ('cp_T', ('Air', 523.5, 'cp')), ('cp_T', ('H2', 275, 'k')),
                 ('cp_300', ('Air', 'cp')), ('cp_300', ('Butane', 'R')), ('critical', ('Water', 'Tcr')), ('critical', ('Nitrogen', 'M')), ('formation', ('CO2(g)', 'hf0')), ('formation', ('H2O(ᐉ)', 's0')),
                 ('fuel', ('Methane', 'LHV')), ('fuel', ('C8H18', 'HHV')), ('compressed_approx', (95.5, 'h')), ('gas_kmol_inverse', ('N2', 'h', 20000)),
                 ('air', (550, 'h')), ('air', (630, 'Pr')), ('air', (1040, 'vr')), ('air', (2150, 'Pr', 'E')), ('isentropic', (3.0, 'rho_rho0')), ('isentropic', (2.95, 'rho_rho0')),
                 ('superheated', ('water', 0.15, 115, 'h')), ('sat_T', ('water', 400, 'hg')), ('air', (100, 'h')), ('superheated', ('R134a', 0.8, 40, 'h')),
                 ('superheated', ('R134a', 0.14, 50, 'h')), ('superheated', ('R134a', 0.8, 50, 's')), ('superheated', ('water', 7.5, 500, 'h')), ('isentropic', (6, 'P_P0')), ('wet_P', ('water', 250, 1.5, 'h'))]:
    add(fn, *args)
out = []
for lang in ('vi', 'en'):
    p.set_lang(lang)
    for c in C:
        try:
            r = getattr(p, c['fn'])(*c['args'])
            out.append(dict(c, lang=lang, ok=True, result=r))
        except p.PropsRangeError as e:
            out.append(dict(c, lang=lang, ok=False, error=str(e)))
json.dump(out, open(os.path.join(P, 'tests', 'props_cases.json'), 'w'), ensure_ascii=False)
print(len(out), sum(1 for o in out if o['ok']), 'ok;', sum(1 for o in out if not o['ok']), 'range errors')
