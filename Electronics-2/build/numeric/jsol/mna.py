"""A small modified-nodal-analysis solver (numpy) used as the independent route of the figure problems of Jaeger 5e: build the circuit of the figure element by element and solve it
exactly, instead of using the closed formulas the textbook (and the first route of each solver) uses.
Elements: R, C, L, independent V and I sources, VCVS (gain E), and opamp() = input resistance Rid between the inputs + gain A behind output resistance Ro (A = 1e12, Rid = 1e15 Ω,
Ro = 0 give the ideal op-amp).  solve(s) with s = 0 for dc or s = j·2πf for ac returns {node: voltage} and {source name: current}."""
import numpy as np
class Ckt:
    def __init__(self): self.el = []; self.nodes = {'0': 0}; self.nv = 0; self.vs = []
    def n(self, name):
        name = str(name)
        if name not in self.nodes: self.nodes[name] = len(self.nodes)
        return self.nodes[name]
    def R(self, a, b, r): self.el.append(('Y', self.n(a), self.n(b), 1 / r)); return self
    def G(self, a, b, g): self.el.append(('Y', self.n(a), self.n(b), g)); return self
    def C(self, a, b, c): self.el.append(('C', self.n(a), self.n(b), c)); return self
    def L(self, a, b, l): self.el.append(('L', self.n(a), self.n(b), l)); return self
    def I(self, a, b, i): self.el.append(('I', self.n(a), self.n(b), i)); return self            # current i flows from a through the source to b
    def V(self, name, p, m, v): self.vs.append((name, 'V', self.n(p), self.n(m), v)); return self
    def E(self, name, p, m, cp, cm, gain): self.vs.append((name, 'E', self.n(p), self.n(m), (self.n(cp), self.n(cm), gain))); return self
    def opamp(self, plus, minus, out, A=1e12, Rid=1e15, Ro=0.0, tag='op'):
        if Rid < 1e14: self.R(plus, minus, Rid)
        if Ro > 0: self.E(f'{tag}_E', f'{tag}_int', '0', plus, minus, A); self.R(f'{tag}_int', out, Ro)
        else: self.E(f'{tag}_E', out, '0', plus, minus, A)
        return self
    def solve(self, s=0.0):
        N = len(self.nodes) - 1; M = len(self.vs); A = np.zeros((N + M, N + M), complex); z = np.zeros(N + M, complex)
        def add(i, j, v):
            if i > 0 and j > 0: A[i - 1, j - 1] += v
        for k, a, b, v in self.el:
            if k == 'I':
                if a > 0: z[a - 1] -= v
                if b > 0: z[b - 1] += v
                continue
            y = v if k == 'Y' else s * v if k == 'C' else 1 / (s * v) if s != 0 else 1e12
            add(a, a, y); add(b, b, y); add(a, b, -y); add(b, a, -y)
        for m, (name, k, p, q, v) in enumerate(self.vs):
            r = N + m
            if p > 0: A[p - 1, r] += 1; A[r, p - 1] += 1
            if q > 0: A[q - 1, r] -= 1; A[r, q - 1] -= 1
            if k == 'V': z[r] = v
            else:
                cp, cm, gain = v
                if cp > 0: A[r, cp - 1] -= gain
                if cm > 0: A[r, cm - 1] += gain
        x = np.linalg.solve(A, z); volts = {nm: (x[i - 1] if i > 0 else 0j) for nm, i in self.nodes.items()}; amps = {name: x[N + m] for m, (name, *_r) in enumerate(self.vs)}
        return volts, amps
def dc(ckt): v, i = ckt.solve(0.0); return {k: x.real for k, x in v.items()}, {k: x.real for k, x in i.items()}
