# -*- coding: utf-8 -*-
"""
Soat toan bo href/src noi bo trong moi file HTML da sinh ra: resolve theo dung
thu muc chua file, xac nhan file dich thuc su TON TAI tren dia. Bat loi kieu
"thieu 1 cap ../" ma soat bang mat de bo sot.
"""
import os, re, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Aircraft-Systems/

ATTR_RE = re.compile(r"""(?:href|src)=(?:"([^"]+)"|'([^']+)')""")

fails = []
checked = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    if "/.git" in dirpath: continue
    for fn in filenames:
        if not fn.endswith(".html"): continue
        fpath = os.path.join(dirpath, fn)
        html = open(fpath, encoding="utf-8").read()
        for m in ATTR_RE.finditer(html):
            url = m.group(1) or m.group(2)
            p = urlparse(url)
            if p.scheme or url.startswith("//") or url.startswith("mailto:") or url.startswith("#"):
                continue  # external or anchor, skip
            if url.startswith("?"):
                continue
            path_part = p.path
            if not path_part:
                continue
            checked += 1
            resolved = os.path.normpath(os.path.join(dirpath, path_part))
            if not os.path.exists(resolved):
                rel_file = os.path.relpath(fpath, ROOT)
                rel_resolved = os.path.relpath(resolved, ROOT)
                fails.append((rel_file, url, rel_resolved))

print(f"Checked {checked} internal href/src across all HTML files.")
if fails:
    print(f"\n{len(fails)} BROKEN LINK(S):")
    for f, url, resolved in fails:
        print(f"  {f}  ->  \"{url}\"  (resolves to missing: {resolved})")
    sys.exit(1)
else:
    print("All internal links resolve to existing files. OK.")
