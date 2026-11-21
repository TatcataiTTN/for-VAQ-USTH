# -*- coding: utf-8 -*-
"""Ghep 2 slide thanh mot anh doc (960x1080) de doc nhanh: python3 build/stack_slides.py <deck> <tu> <den>  -> scratch/stacks/<deck>/<a>_<b>.jpg"""
import sys, os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
deck, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = os.path.join(ROOT, 'scratch', 'stacks', deck); os.makedirs(out, exist_ok=True)
for p in range(a, b + 1, 2):
    ims = [Image.open(os.path.join(ROOT, 'assets', 'slides', deck, f'p{q:02d}.jpg')) for q in (p, p + 1) if q <= b]
    W = max(i.width for i in ims); H = sum(i.height for i in ims) + 6 * (len(ims) - 1)
    s = Image.new('RGB', (W, H), (200, 0, 0)); y = 0
    for i in ims: s.paste(i, (0, y)); y += i.height + 6
    s.save(os.path.join(out, f'{p:02d}.jpg'), quality=80)
print(sorted(os.listdir(out)))
