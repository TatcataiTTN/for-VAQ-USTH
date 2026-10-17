# -*- coding: utf-8 -*-
"""Helper cho cac bo cau hoi mo rong (module 05-09): moi cau co dap an, giai thich ngan va 'detail' song ngu."""
def _p(s): return "".join(f"<p>{x.strip()}</p>" for x in s.strip().split("\n") if x.strip())
def X(q, en, ov, oe, c, ev, ee, dv, de, src, src_en=None):
    return dict(q=q, en=en, opts=list(ov), opts_en=list(oe), correct=c, explain=ev, explain_en=ee,
                detail=_p(dv), detail_en=_p(de), src=src, src_en=src_en or src)
def TF(q, en, truth, ev, ee, dv, de, src, src_en=None):
    return dict(q=q, en=en, opts=["Đúng", "Sai"], opts_en=["True", "False"], correct=0 if truth else 1, explain=ev, explain_en=ee,
                detail=_p(dv), detail_en=_p(de), src=src, src_en=src_en or src)
def attach(items, dets):
    """Gan detail (vi,en) theo thu tu cho danh sach cau co san."""
    assert len(items) == len(dets), (len(items), len(dets))
    for it, (v, e) in zip(items, dets):
        it["detail"] = _p(v); it["detail_en"] = _p(e)
