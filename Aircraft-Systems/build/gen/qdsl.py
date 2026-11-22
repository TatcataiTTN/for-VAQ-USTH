# -*- coding: utf-8 -*-
"""Ham dung chung de viet cau hoi cho module 12 den 15 va cac de Tooley (ngan gon, song ngu).
  B = Bank(topics)           topics: {tid: (vi, en)}
  B.T(ch, n, key, tid, lv, qv, qe, opts, xv, xe, dv='', de='')   cau trac nghiem Tooley (khoa a/b/c doc tu anh quet App.3)
  B.R(paper, n, key, tid, lv, qv, qe, opts, xv, xe)               cau cua Revision Paper (nguon 'Tooley Revision Paper N Q M')
  B.X(tid, lv, qv, qe, opts, c, xv, xe, tagv, tage, dv='', de='') cau bo sung (muc c la chi so dap an dung tinh san)
  B.E(tid, lv, qv, qe, sv, se, tagv, tage)                        tu luan co loi giai
opts: danh sach phan tu; moi phan tu la chuoi (giong nhau o hai ngon ngu) hoac (vi, en)."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); OUT = os.path.join(ROOT, 'data', 'qsrc')
PAGE = {3: 377, 12: 380, 15: 381, 16: 381, 17: 382, 18: 382, 19: 382, 20: 383}          # trang in cua khoa App.3
def opt(x): return x if isinstance(x, tuple) else (x, x)
class Bank:
    def __init__(self, topics): self.topics = topics; self.goc = []; self.gen = []; self.ess = []
    def _item(self, kind, tid, lv, origin, qv, qe, opts, c, xv, xe, sv, se, dv='', de=''):
        d = dict(kind=kind, q=dict(vi=qv, en=qe), opts=[dict(vi=opt(o)[0], en=opt(o)[1]) for o in opts], correct=c, explain=dict(vi=xv, en=xe),
                 topic=dict(vi=self.topics[tid][0], en=self.topics[tid][1]), topic_id=tid, level=lv, origin=origin, src=dict(vi=sv, en=se))
        if dv: d['detail'] = dict(vi=dv, en=de)
        return d
    def T(self, ch, n, key, tid, lv, qv, qe, opts, xv, xe, dv='', de='', printed=None):
        """printed: khoa IN khi site dung dap an khac (vd printed='b' va key='a'): nhan nguon ghi ro."""
        assert len(opts) == 3 and key in 'abc', (ch, n)
        sv = f'Tooley Ch.{ch} · Câu {n} (khoá A.{ch}, tr.{PAGE[ch]})' if not printed else f'Tooley Ch.{ch} · Câu {n} (khoá in ({printed}), đúng ({key}); A.{ch}, tr.{PAGE[ch]})'
        se = f'Tooley Ch.{ch} · Q{n} (key A.{ch}, p.{PAGE[ch]})' if not printed else f'Tooley Ch.{ch} · Q{n} (printed key ({printed}), correct ({key}); A.{ch}, p.{PAGE[ch]})'
        self.goc.append(self._item('mcq', tid, lv, 'goc', qv, qe, opts, 'abc'.index(key), xv, xe, sv, se, dv, de))
    def R(self, paper, n, key, tid, lv, qv, qe, opts, xv, xe, dv='', de=''):
        assert len(opts) == 3 and key in 'abc', (paper, n)
        self.goc.append(self._item('mcq', tid, lv, 'goc', qv, qe, opts, 'abc'.index(key), xv, xe, f'Tooley Revision Paper {paper} Q{n}', f'Tooley Revision Paper {paper} Q{n}', dv, de))
    def X(self, tid, lv, qv, qe, opts, c, xv, xe, tagv, tage, dv='', de=''):
        assert len({opt(o)[1] for o in opts}) == len(opts) >= 3, (qe, opts)
        self.gen.append(self._item('mcq', tid, lv, 'bo_sung', qv, qe, opts, c, xv, xe, f'Bổ sung · {tagv}', f'Added · {tage}', dv, de))
    def TF(self, tid, lv, qv, qe, true, xv, xe, tagv, tage):
        self.gen.append(self._item('tf', tid, lv, 'bo_sung', qv, qe, [('Đúng', 'True'), ('Sai', 'False')], 0 if true else 1, xv, xe, f'Bổ sung · {tagv}', f'Added · {tage}'))
    def E(self, tid, lv, qv, qe, sv, se, tagv, tage):
        self.ess.append(dict(kind='ess', q=dict(vi=qv, en=qe), sol=dict(vi=sv, en=se), topic=dict(vi=self.topics[tid][0], en=self.topics[tid][1]), topic_id=tid, level=lv, origin='bo_sung', src=dict(vi=f'Bổ sung · {tagv}', en=f'Added · {tage}')))
    def write(self, mid):
        import collections
        for name, data in ((f'{mid}.json', self.goc), (f'{mid}_gen.json', self.gen), (f'{mid}_ess.json', self.ess)):
            if data or name == f'{mid}.json': json.dump(data, open(os.path.join(OUT, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(mid, 'goc', len(self.goc), dict(collections.Counter(i['level'] for i in self.goc)), '| gen', len(self.gen), dict(collections.Counter(i['level'] for i in self.gen)), '| ess', len(self.ess))
