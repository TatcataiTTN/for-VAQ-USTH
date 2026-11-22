# -*- coding: utf-8 -*-
"""Chay: python3 build/gen/make_rev.py  -> data/qsrc/mNN_rev.json (107 cau Revision Paper con thieu) + va cac cau da co. Chay lai an toan."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import gen_rev as G
import gen_rev_a, gen_rev_b, gen_rev_c      # noqa: F401  (moi file goi G.R(...) khi import)
if G.MISS:
    print('THIEU BANG CHUNG:'); [print('  P%d Q%d: %r' % x) for x in G.MISS]; sys.exit(1)
G.write(); G.patch_existing()
json.dump(G.ITEMS, open(os.path.join(G.ROOT, 'data', 'verify', 'tooley_rev_new_items.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
