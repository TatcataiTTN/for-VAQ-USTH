# -*- coding: utf-8 -*-
"""Du lieu cho cac cong cu (Khai niem, Phan tich de, Bai tap co dap an, Viet tay): moi ngon ngu mot bo trong {lang}/data/.
  search.json    moi cau trac nghiem va tu luan: id, module, loai, muc, chu de, nguon, de bai rut gon, dap an dung rut gon
  essays.json    toan van cac bai tu luan (de, hinh, loi giai, hinh dap an)
  glossary.json  thuat ngu VI-EN (de Khai niem noi thuat ngu lien quan)"""
import json, os, re
from sitelib import write, ROOT
from modules import MODS

def loc(v, lang): return v.get(lang, v.get('en', '')) if isinstance(v, dict) else v
def strip_html(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s or '')).strip()
def clip(s, n): s = strip_html(s); return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'

def write_tool_data(lang, banks):
    items = []; essays = []
    for m in MODS:
        b = banks.get(m['id'])
        if not b: continue
        for it in b['items']:
            ans = loc(it['opts'][it['correct']], lang) if it['kind'] != 'ess' else ''
            items.append(dict(id=it['id'], m=m['id'], k=it['kind'], l=it['level'], t=loc(it['topic'], lang), ti=it.get('topic_id', ''), o='g' if it['origin'] == 'goc' else 'b', s=loc(it['src'], lang), q=clip(loc(it['q'], lang), 260), a=clip(ans, 90), f=int(bool(it.get('fig')))))
        for e in b['essays']:
            items.append(dict(id=e['id'], m=m['id'], k='ess', l=e['level'], t=loc(e['topic'], lang), ti=e.get('topic_id', ''), o='g' if e['origin'] == 'goc' else 'b', s=loc(e['src'], lang), q=clip(loc(e['q'], lang), 260), a=clip(loc(e['sol'], lang), 90), f=int(bool(e.get('figs')))))
            essays.append(dict(id=e['id'], m=m['id'], l=e['level'], t=loc(e['topic'], lang), o='g' if e['origin'] == 'goc' else 'b', s=loc(e['src'], lang), q=loc(e['q'], lang), sol=loc(e['sol'], lang),
                               figs=['../../' + f for f in e.get('figs', [])], af=('../../' + e['afig']) if e.get('afig') else ''))
    write(f'{lang}/data/search.json', json.dumps(dict(lang=lang, mods={m['id']: m[lang] for m in MODS if banks.get(m['id'])}, items=items), ensure_ascii=False, separators=(',', ':')))
    write(f'{lang}/data/essays.json', json.dumps(dict(lang=lang, mods={m['id']: m[lang] for m in MODS if banks.get(m['id'])}, essays=essays), ensure_ascii=False, separators=(',', ':')))
    g = json.load(open(os.path.join(ROOT, 'data', 'glossary.json'), encoding='utf-8'))
    write(f'{lang}/data/glossary.json', json.dumps([dict(en=t['en'], vi=t['vi'], m=t['modules'], d=t['def_vi'] if lang == 'vi' else t['def_en']) for t in g], ensure_ascii=False, separators=(',', ':')))
    return len(items), len(essays)
