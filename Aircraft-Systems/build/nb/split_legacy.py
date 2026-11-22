# -*- coding: utf-8 -*-
"""Tach 9 notebook cu (data/notebooks/NN_*.ipynb, mot file chung VI+EN) thanh cap notebooks/mNN_<slug>_{vi,en}.ipynb va chay lai bang nbconvert.
VI: bo doan co co cuoc EN, bo co, cat nhan 'A / B' lay phan Viet; code giu nguyen. EN: markdown lay tu build/nb/legacy_en_*.py, code thay cac doan tieng Viet khong dau bang tieng Anh.
Chay: python3 build/nb/split_legacy.py [01 02 ...]  (khong tham so = tat ca)   File cu data/notebooks/ giu nguyen de URL cu van song."""
import os, sys, json, re, copy, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'build'))
import legacy_en_b, legacy_en_c                                      # noqa: F401  (nap D)
from legacy_en_a import D
import modules as M
VI_CH = re.compile(r'[ạảãàáâậầấẩẫăặằắẳẵẹẻẽèéêệềếểễịỉĩìíọỏõòóôộồốổỗơợờớởỡụủũùúưựừứửữỵỷỹỳýđ]', re.I)
def vi_md(t):
    out = []; state = None
    for ln in t.split('\n'):
        if not ln.strip(): state = None; out.append(ln); continue
        if ln.startswith('🇬🇧'): state = 'en'
        elif ln.startswith('🇻🇳'): state = 'vi'; ln = ln[len('🇻🇳'):].lstrip()
        if state == 'en': continue
        if ln.startswith('#') and ' / ' in ln: ln = ln.rsplit(' / ', 1)[0]
        out.append(ln)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()
def lines(s): return s.split('\n')
def src(c): return ''.join(c['source'])
def setsrc(c, text): c['source'] = text.splitlines(keepends=True) if text else []
def build(num):
    mod = next(m for m in M.MODS if m['slug'].startswith(num)); legacy = os.path.join(ROOT, 'data', 'notebooks', f'{num}_{mod["slug"][3:]}.ipynb')
    base = f'{mod["id"]}_{mod["slug"][3:].replace("-", "_")}'; nb0 = json.load(open(legacy, encoding='utf-8')); res = {}
    for lg in ('vi', 'en'):
        nb = copy.deepcopy(nb0); d = D[num]
        for i, c in enumerate(nb['cells']):
            t = src(c)
            if c['cell_type'] == 'markdown':
                if lg == 'vi': setsrc(c, vi_md(t))
                else:
                    if i in d['md']: setsrc(c, d['md'][i])
                    else: assert not VI_CH.search(t) and '🇻🇳' not in t, ('md cell without EN text', num, i, t[:60])
            else:
                if lg == 'en':
                    for a, b in d['code']: t = t.replace(a, b)
                    setsrc(c, t)
                c['outputs'] = []; c['execution_count'] = None
        out = os.path.join(ROOT, 'notebooks', f'{base}_{lg}.ipynb'); json.dump(nb, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        kd = os.path.join(ROOT, 'scratch', 'jup', 'kernels', 'aircraft_venv'); os.makedirs(kd, exist_ok=True)      # nhan ipykernel cua .venv (co sympy), chi dung luc chay
        json.dump(dict(argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'], display_name='Python 3', language='python'), open(os.path.join(kd, 'kernel.json'), 'w'))
        nbk = json.load(open(out, encoding='utf-8')); nbk['metadata']['kernelspec'] = dict(name='aircraft_venv', display_name='Python 3', language='python'); json.dump(nbk, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        env = dict(os.environ, JUPYTER_PATH=os.path.join(ROOT, 'scratch', 'jup'))
        r = subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=300', out], capture_output=True, text=True, cwd=os.path.join(ROOT, 'notebooks'), env=env)
        nbk = json.load(open(out, encoding='utf-8')); nbk['metadata']['kernelspec'] = dict(name='python3', display_name='Python 3 (ipykernel)', language='python'); json.dump(nbk, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(os.path.basename(out), 'nbconvert', r.returncode, r.stderr[-300:] if r.returncode else ''); res[lg] = r.returncode
    return res
if __name__ == '__main__':
    nums = sys.argv[1:] or sorted(D)
    for n in nums: build(n)
