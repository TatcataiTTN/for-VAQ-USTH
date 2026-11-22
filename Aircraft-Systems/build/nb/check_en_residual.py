# -*- coding: utf-8 -*-
"""Tim chu tieng Viet con sot trong notebook EN (nguon va dau ra): co dau, hoac tu vung khong dau thuong gap. In ra de dich them."""
import json, glob, re, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
VI = re.compile(r'[ạảãàáâậầấẩẫăặằắẳẵẹẻẽèéêệềếểễịỉĩìíọỏõòóôộồốổỗơợờớởỡụủũùúưựừứửữỵỷỹỳýđ]', re.I)
W = re.compile(r'\b(cua|khong|nhieu|duoc|cau|dap an|tinh|kiem|bieu thuc|rut gon|chan tri|ket qua|khop|hoac|voi|trong|mot|moi|tung|dung|so sanh|co so|thap phan|nhi phan|bu hai|ma hoa|dau vao|ngo ra|chu ky|duong|kenh|khi|vi du|phep|ban dau|tuong duong|thanh ghi|tin hieu|giai|chuyen|tong|toi da|toi thieu|ky vong|phai|nen|cung|nhom|diem|gia tri|loi|nhan|ngoai|ben|trai|tren|duoi|bang|cac|hay|nay|cho|chi|va|la|tu|do|bo|bai|goc|ra|vao|de|thi)\b', re.I)
bad = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'notebooks', 'm0*_en.ipynb'))):
    nb = json.load(open(f, encoding='utf-8')); n = 0
    for i, c in enumerate(nb['cells']):
        texts = [(f'C{i}', ''.join(c['source']))]
        for o in c.get('outputs', []): texts.append((f'O{i}', ''.join(o.get('text', '')) or json.dumps(o.get('data', {}), ensure_ascii=False)))
        for tag, t in texts:
            for ln in t.split('\n'):
                if VI.search(ln) or (len(W.findall(ln)) >= 2 and not re.match(r'\s*(import|from)\b', ln)):
                    n += 1; print(f'{os.path.basename(f)} {tag}|{ln[:170]}')
    bad += n
print('residual lines:', bad)
