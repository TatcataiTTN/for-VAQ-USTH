# -*- coding: utf-8 -*-
"""Chay SAU MOI LAN PUSH (build/push.sh goi tu dong): ghi lai id cac cau trac nghiem da len web vao data/published_ids.json.
assemble.py giu nguyen thu tu lua chon cua cac cau nay (de tien do luu trong trinh duyet khong bi cham sai) va chi dat cac cau MOI sao cho vi tri dap an can bang."""
import json, glob, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ids = []
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'qbank', 'm*.json'))): ids += [i['id'] for i in json.load(open(f, encoding='utf-8'))['items']]
json.dump(sorted(ids), open(os.path.join(ROOT, 'data', 'published_ids.json'), 'w')); print('published ids:', len(ids))
