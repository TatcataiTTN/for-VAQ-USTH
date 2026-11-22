# -*- coding: utf-8 -*-
"""Liet ke cac dong code (chu thich, chuoi in ra) va doan markdown tieng Viet cua 9 notebook cu, de dich (build/nb/legacy_en.json)."""
import json, glob, re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W = re.compile(r'\b(cua|va|cac|khong|nhieu|chi|duoc|cau|dap an|tinh|kiem|bieu|thuc|rut gon|bang|chan tri|ket qua|khop|hoac|voi|trong|mot|moi|tung|dung|sai|so sanh|co so|thap phan|nhi phan|bu hai|ma hoa|bo|dau vao|ngo ra|chu ky|duong|kenh|can|khi|la|tu|de bai|luat|vi du|phep|goc|ban dau|cho truoc|tuong duong|doi|thanh ghi|tin hieu|bai|giai|chuyen|tong|hieu|lon nhat|nho nhat|toi da|toi thieu|ky vong|phai|thi|nen|cung|dang|nhom|diem|so|gia tri|truong|loi|nhan|dien|ap|dong|goi|tin|ngoai|ben|trai)\b', re.I)
def vi_line(ln): return (('"' in ln or "'" in ln or '#' in ln) and len(W.findall(ln)) >= 2)
def extract():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'notebooks', '*.ipynb'))):
        nb = json.load(open(f, encoding='utf-8')); k = os.path.basename(f); out[k] = dict(code=[], md=[])
        for i, c in enumerate(nb['cells']):
            t = ''.join(c['source'])
            if c['cell_type'] == 'markdown': out[k]['md'].append((i, t))
            else:
                for j, ln in enumerate(t.split('\n')):
                    if vi_line(ln): out[k]['code'].append((i, j, ln))
    return out
if __name__ == '__main__':
    d = extract(); json.dump(d, open(os.path.join(ROOT, 'scratch', 'nb_extract.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    import sys
    for k in sys.argv[1:]:
        key = [x for x in d if x.startswith(k)][0]; print('=====', key)
        for i, j, ln in d[key]['code']: print(f'C{i}.{j}|{ln}')
