# -*- coding: utf-8 -*-
import random

def num(x, nd=2, lang="en", sci=False):
    s = f"{x:.{nd}e}" if sci else f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "vi" else s

def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table class='chapmap'><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>"

def mcq(seed, src, q, right, wrongs, explain, detail=None):
    """Tron dap an bang random.Random(seed) co dinh (cung thu tu o ca 2 ngon ngu)."""
    opts = [right] + list(wrongs)
    order = list(range(len(opts)))
    random.Random(seed).shuffle(order)
    out = {"q": q, "opts": [opts[i] for i in order], "correct": order.index(0),
           "explain": explain, "src": src}
    if detail:
        out["detail"] = detail
    return out


def sol(lang, read, idea, steps, check=None):
    """Loi giai co cau truc: De noi gi -> Y tuong -> Cac buoc -> Kiem tra. steps la list HTML, buoc cuoi nen in dam dap an."""
    h = {"vi": ("Đề nói gì", "Ý tưởng", "Các bước", "Kiểm tra"), "en": ("What the problem says", "Idea", "Steps", "Check")}[lang]
    out = f"<p><b>{h[0]}.</b> {read}</p><p><b>{h[1]}.</b> {idea}</p><p><b>{h[2]}.</b></p><ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"
    if check:
        out += f"<p class='pill'><b>{h[3]}:</b> {check}</p>"
    return out
