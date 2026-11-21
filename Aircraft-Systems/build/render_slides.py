# -*- coding: utf-8 -*-
"""Render moi trang slide cua giang vien thanh JPEG 960 px + chi muc data/slides/index.json (deck, page, title tu bookmark neu co, chars)."""
import os, json, sys
import pymupdf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.abspath(os.path.join(ROOT, "..", "sources", "lectures"))
DECKS = [("num", "Number system.pdf"), ("logic", "logic circuit_version 2026.pdf"), ("icmux", "integrated circuit and multiplexing version 2026.pdf"),
         ("cpu", "Basic computer structure and microprocessor PDA version 2026.pdf"), ("bus", "Data buses aircraft - ver 2026 v2.pdf"),
         ("disp", "Electronic displays - ver 2026.pdf"), ("fib", "Optic_Fiber_ver 2026.pdf"), ("emc", "Cours_EMC_Aircraft_ver2026.pdf"),
         ("swc", "software management control.pdf")]
idx = []
for key, fn in DECKS:
    doc = pymupdf.open(os.path.join(SRC, fn)); toc = {p: t for _, t, p in doc.get_toc()}
    out = os.path.join(ROOT, "assets", "slides", key); os.makedirs(out, exist_ok=True)
    for i, pg in enumerate(doc, 1):
        z = 960 / pg.rect.width
        pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False)
        pix.save(os.path.join(out, f"p{i:02d}.jpg"), jpg_quality=72)
        t = toc.get(i, "")
        if t.lower().startswith("slide "): t = t.split(":", 1)[1].strip() if ":" in t else ""
        idx.append(dict(deck=key, page=i, title=t, img=f"assets/slides/{key}/p{i:02d}.jpg", chars=len(pg.get_text().strip()), w=pix.width, h=pix.height))
    print(key, len(doc), "trang")
json.dump(idx, open(os.path.join(ROOT, "data", "slides", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("tong", len(idx))
