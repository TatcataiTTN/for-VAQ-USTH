"""Generated numeric items for module 09: physics of PCB traces (outside the EASA text; syllabus objective (c): formulas with physical laws)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'author'))
from _lib import *
G = Gen('m09_calc', 'EASA SM02', 20250909, dict(calc=('PCB trace physics', 'Vật lý đường dẫn PCB')))
g, fmt, add = G.g, G.fmt, G.add
RHO = 1.68e-8; EPS0 = 8.854e-12
S = ('PCB trace physics (R = ρL/(w·t)); not from the EASA text', 'vật lý đường dẫn PCB (R = ρL/(w·t)); không có trong văn bản EASA')
for L, w, t in [(100, 0.25, 35), (50, 0.5, 35), (200, 0.3, 70), (25, 0.15, 35), (150, 1.0, 35), (80, 0.2, 18)]:
    r = RHO * L * 1e-3 / (w * 1e-3 * t * 1e-6)
    add('calc', f'A copper trace is {L} mm long, {w} mm wide and {t} μm thick (ρ = 1.68×10⁻⁸ Ω·m). What is its resistance?', f'Một đường đồng dài {L} mm, rộng {w} mm, dày {t} μm (ρ = 1,68×10⁻⁸ Ω·m). Điện trở của nó là bao nhiêu?', fmt(r, 'Ω'), [fmt(r * 1000, 'Ω'), fmt(r / 1000, 'Ω'), fmt(r * 2, 'Ω'), fmt(RHO * L * 1e-3 / (w * 1e-3 * t * 1e-3), 'Ω')], f'R = ρL/(w·t) = 1.68e-8 × {L} mm / ({w} mm × {t} μm) = {g(r)} Ω.', f'R = ρL/(w·t) = 1,68e-8 × {L} mm / ({w} mm × {t} μm) = {g(r)} Ω.', S, 2)
for L, w, t, i in [(100, 0.25, 35, 1.0), (50, 0.5, 35, 2.0), (200, 0.3, 70, 0.5)]:
    r = RHO * L * 1e-3 / (w * 1e-3 * t * 1e-6); v = i * r * 1e3
    add('calc', f'A {L} mm × {w} mm × {t} μm copper trace carries {i} A. What is the voltage drop along it?', f'Đường đồng {L} mm × {w} mm × {t} μm mang dòng {i} A. Sụt áp dọc theo nó là bao nhiêu?', fmt(v, 'mV'), [fmt(v * 1000, 'mV'), fmt(v / 1000, 'mV'), fmt(v * 2, 'mV'), fmt(i / r * 1e3, 'mV')], f'R = {g(r)} Ω; V = I·R = {i} × {g(r)} = {g(v)} mV.', f'R = {g(r)} Ω; V = I·R = {i} × {g(r)} = {g(v)} mV.', S, 3)
for a, d, er in [(1.0, 0.2, 4.5), (4.0, 0.1, 4.5), (0.25, 0.36, 4.3)]:
    c = EPS0 * er * a * 1e-4 / (d * 1e-3) * 1e12
    add('calc', f'Two parallel copper areas of {a} cm² on adjacent layers are separated by {d} mm of FR-4 (εr = {er}). What is the capacitance between them?', f'Hai vùng đồng song song {a} cm² ở hai lớp liền kề cách nhau {d} mm FR-4 (εr = {er}). Điện dung giữa chúng là bao nhiêu?', fmt(c, 'pF'), [fmt(c * 1000, 'pF'), fmt(c / 1000, 'pF'), fmt(c / er, 'pF'), fmt(c * 2, 'pF')], f'C = ε0·εr·A/d = 8.854e-12 × {er} × {a} cm² / {d} mm = {g(c)} pF — a source of the unintended coupling the text warns about.', f'C = ε0·εr·A/d = 8,854e-12 × {er} × {a} cm² / {d} mm = {g(c)} pF — nguồn của ghép ký sinh mà sách cảnh báo.', S, 3)
G.write()
