# -*- coding: utf-8 -*-
"""Cong cu tinh cho module 14 (VHDL). Moi ham co hai cai dat doc lap: _a tren so nguyen 4 bit (mat na 0xF), _b tren chuoi bit. build/verify/verify_m14.py doi chieu.
Quy tac uu tien theo Tooley 17.7: NOT (lop 7) > dich/xoay (lop 3) > AND/OR/XOR (lop 1). SLA o day chi dung cho vector co bit phai nhat bang 0 (khi do SLA = SLL: Tooley khong dinh nghia bit dien vao)."""
M = 0xF
EXPR = ['p AND q', 'p OR q', 'p XOR q', 'NOT p AND q', 'p AND NOT q', 'NOT (p AND q)', 'NOT p OR NOT q', 'p AND SLA q', 'NOT p AND ROR q', 'SLA p AND NOT q']
def ev_a(expr, p, q):
    nt = lambda v: ~v & M; sla = lambda v: (v << 1) & M; ror = lambda v: ((v >> 1) | ((v & 1) << 3)) & M
    return {'p AND q': p & q, 'p OR q': p | q, 'p XOR q': p ^ q, 'NOT p AND q': nt(p) & q, 'p AND NOT q': p & nt(q), 'NOT (p AND q)': nt(p & q), 'NOT p OR NOT q': nt(p) | nt(q),
            'p AND SLA q': p & sla(q), 'NOT p AND ROR q': nt(p) & ror(q), 'SLA p AND NOT q': sla(p) & nt(q)}[expr]
def ev_b(expr, p, q):
    P, Q = format(p, '04b'), format(q, '04b')
    nt = lambda s: ''.join('1' if c == '0' else '0' for c in s); sla = lambda s: s[1:] + '0'; ror = lambda s: s[-1] + s[:-1]
    f = lambda a, b, op: ''.join(str(op(int(x), int(y))) for x, y in zip(a, b))
    AND = lambda a, b: f(a, b, lambda x, y: x & y); OR = lambda a, b: f(a, b, lambda x, y: x | y); XOR = lambda a, b: f(a, b, lambda x, y: x ^ y)
    r = {'p AND q': AND(P, Q), 'p OR q': OR(P, Q), 'p XOR q': XOR(P, Q), 'NOT p AND q': AND(nt(P), Q), 'p AND NOT q': AND(P, nt(Q)), 'NOT (p AND q)': nt(AND(P, Q)), 'NOT p OR NOT q': OR(nt(P), nt(Q)),
         'p AND SLA q': AND(P, sla(Q)), 'NOT p AND ROR q': AND(nt(P), ror(Q)), 'SLA p AND NOT q': AND(sla(P), nt(Q))}[expr]
    return int(r, 2)
ev = ev_a
def half_adder_a(x, y): return x ^ y, x & y
def half_adder_b(x, y): s = (x + y) % 2; c = (x + y) // 2; return s, c
half_adder = half_adder_a
def half_adder_en_a(x, y, en): return half_adder_a(x, y) if en else (0, 0)
def half_adder_en_b(x, y, en): return ((x + y) % 2 * en, (x + y) // 2 * en)
half_adder_en = half_adder_en_a
def path_delay_a(n_gates, t): return n_gates * t
def path_delay_b(n_gates, t): return sum([t] * n_gates)
path_delay = path_delay_a
