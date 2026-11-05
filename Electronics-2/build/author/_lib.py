"""Shared helpers for module authoring (bilingual items + seeded generators)."""
import json, os, math, random
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def B(en, vi=None): return dict(en=en, vi=vi if vi is not None else en)
def O(opts): return [B(*o) if isinstance(o, tuple) else B(o) for o in opts]
def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(obj, open(path + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(path + '.tmp', path)
class Mod:
    """Original (book) items of one Floyd chapter."""
    def __init__(self, mid, ch, T): self.mid, self.ch, self.T, self.items = mid, ch, {k: B(*v) for k, v in T.items()}, []
    def _src(self, kind_en, kind_vi, n, pg): return B(f'Floyd 9e, Ch.{self.ch}, {kind_en} Q{n} (p.{pg})', f'Floyd 9e, Ch.{self.ch}, {kind_vi} câu {n} (tr.{pg})')
    def mcq(self, n, pg, en, vi, opts, c, xe, xv, topic, lvl=1, fixed=False):
        self.items.append(dict(kind='mcq', q=B(en, vi), opts=O(opts), correct=c, explain=B(xe, xv), level=lvl, topic=self.T[topic], src=self._src('Self-Test', 'Self-Test', n, pg), origin='goc', fixed_order=fixed, check='chapter text + script'))
    def tf(self, n, pg, en, vi, v, xe, xv, topic):
        self.items.append(dict(kind='tf', q=B(en, vi), opts=[B('True', 'Đúng'), B('False', 'Sai')], correct=0 if v else 1, explain=B(xe, xv), level=1, topic=self.T[topic], src=self._src('True/False Quiz', 'Đúng/Sai', n, pg), origin='goc', fixed_order=True, check='chapter text'))
    def ca(self, n, pg, en, vi, fig, c, xe, xv, topic):
        self.items.append(dict(kind='ca', q=B(en, vi), opts=[B('Increase', 'Tăng'), B('Decrease', 'Giảm'), B('Not change', 'Không đổi')], correct=c, explain=B(xe, xv), level=2, topic=self.T[topic], src=self._src('Circuit-Action Quiz', 'Circuit-Action', n, pg), origin='goc', fixed_order=True, fig=fig, check='figure + formula'))
    def ess(self, n, pg, en, vi, se, sv, topic, lvl=2, book=False):
        self.items.append(dict(kind='ess', q=B(en, vi), sol=B(se, sv), level=lvl, topic=self.T[topic], src=B(f'Floyd 9e, Ch.{self.ch}, Problem {n} (p.{pg})', f'Floyd 9e, Ch.{self.ch}, Bài tập {n} (tr.{pg})'), origin='goc', check='script + book answer' if book else 'script'))
    def write(self):
        save(os.path.join(ROOT, 'data', 'qsrc', f'{self.mid}.json'), self.items)
        from collections import Counter; print(self.mid, dict(Counter(i['kind'] for i in self.items)))
class Gen:
    """Seeded generator of origin=bo_sung items."""
    def __init__(self, mid, ch, seed, T): self.mid, self.ch, self.rng, self.T, self.out, self.seen = mid, ch, random.Random(seed), {k: B(*v) for k, v in T.items()}, [], set()
    @staticmethod
    def g(x, d=3):
        x = float(f'{x:.{d}g}'); return f'{x:,.0f}' if abs(x) >= 1e4 else f'{x:g}'
    def fmt(self, x, unit, d=3): return f'{self.g(x, d)} {unit}'.strip()
    def add(self, tp, qen, qvi, ans, wrongs, xen, xvi, srcs, lvl=1):
        ws = []
        for w in wrongs:
            if w != ans and w not in ws: ws.append(w)
        if len(ws) < 3 or (qen, ans) in self.seen: return False
        self.seen.add((qen, ans)); opts = [ans] + (self.rng.sample(ws, 3) if len(ws) > 3 else ws[:3]); self.rng.shuffle(opts)
        self.out.append(dict(kind='mcq', q=B(qen, qvi), opts=[B(o) for o in opts], correct=opts.index(ans), explain=B(xen, xvi), level=lvl, topic=self.T[tp],
                             src=B(f'Generated – modelled on {srcs[0]}', f'Bổ sung – sinh theo dạng {srcs[1]}'), origin='bo_sung', fixed_order=False, check='script')); return True
    def concept(self, tp, qe, qv, ca, ws, xe, xv):
        if (qe, ca[0]) in self.seen: return
        self.seen.add((qe, ca[0])); opts = [ca] + ws; self.rng.shuffle(opts)
        self.out.append(dict(kind='mcq', q=B(qe, qv), opts=[B(*o) for o in opts], correct=opts.index(ca), explain=B(xe, xv), level=1, topic=self.T[tp],
                             src=B(f'Generated – conceptual variant of Floyd Ch.{self.ch} Self-Test', f'Bổ sung – dạng khái niệm theo Floyd Ch.{self.ch} Self-Test'), origin='bo_sung', fixed_order=False, check='chapter text'))
    def ca(self, tp, qe, qv, fig, c, xe, xv, srcs):
        self.out.append(dict(kind='ca', q=B(qe, qv), opts=[B('Increase', 'Tăng'), B('Decrease', 'Giảm'), B('Not change', 'Không đổi')], correct=c, explain=B(xe, xv), level=2, topic=self.T[tp],
                             src=B(f'Generated – modelled on {srcs[0]}', f'Bổ sung – sinh theo dạng {srcs[1]}'), origin='bo_sung', fixed_order=True, fig=fig, check='figure + formula'))
    def write(self): save(os.path.join(ROOT, 'data', 'qsrc', f'{self.mid}_gen.json'), self.out); print(self.mid, 'generated', len(self.out))
