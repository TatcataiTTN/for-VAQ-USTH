# -*- coding: utf-8 -*-
"""Dung notebook VI + EN tu chua day du va chay that bang nbconvert. secs: [(code, title (vi, en), question (vi, en), reading (vi, en) co {a} {b}, vals dict)]"""
import os, sys, subprocess
import nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
def make(fname, head, secs):
    for lg in ('vi', 'en'):
        vi = lg == 'vi'; T = lambda p: p[0] if vi else p[1]; dec = (lambda x: str(x).replace('.', ',')) if vi else str
        nb = nbf.v4.new_notebook(); c = nb.cells; c.append(nbf.v4.new_markdown_cell(T(head)))
        for code, title, q, rd, vals in secs:
            c.append(nbf.v4.new_markdown_cell(f'## {T(title)}\n{T(q)}')); c.append(nbf.v4.new_code_cell(code))
            c.append(nbf.v4.new_markdown_cell(T(('**Đọc kết quả.** ', '**Reading the result.** ')) + T(rd).format(**{a: dec(b) for a, b in vals.items()})))
        fn = os.path.join(OUT, f'{fname}_{lg}.ipynb'); nbf.write(nb, fn)
        r = subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', '--ExecutePreprocessor.timeout=120', fn], capture_output=True, text=True)
        print(fname, lg, 'nbconvert', r.returncode, r.stderr[-300:] if r.returncode else '')
