# -*- coding: utf-8 -*-
"""Gan 'detail' cho cau hien co va them cau mo rong cho cac module 05-09 (xem quiz_x05.py ... quiz_x09.py)."""
import importlib
from qx import attach
def apply(MODULES):
    for slug in MODULES:
        num = slug[:2]
        try: m = importlib.import_module("quiz_x" + num)
        except ModuleNotFoundError: continue
        d = MODULES[slug]
        for grp, dets in getattr(m, "DET", {}).items():
            attach(d[grp], dets)
        for grp, items in getattr(m, "EXTRA", {}).items():
            d.setdefault(grp, [])
            d[grp].extend(items)
