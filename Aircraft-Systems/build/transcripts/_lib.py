# -*- coding: utf-8 -*-
"""Tien ich ghi ban chep slide: moi file build/transcripts/<deck>.py chua danh sach S gom cac dict tao bang s(...); build_transcripts.py ghi data/slides/transcript/<deck>_<a>-<b>.json."""
def s(page, kind, title, en, vi, formulas=(), numbers=(), issues=()):
    return dict(page=page, kind=kind, title=title, text_en=en, text_vi=vi, formulas=list(formulas), numbers=list(numbers), issues=list(issues))
