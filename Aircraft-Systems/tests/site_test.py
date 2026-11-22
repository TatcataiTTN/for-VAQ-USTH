# -*- coding: utf-8 -*-
"""Test tuong tac bang trinh duyet that tren ban dung o thu muc lam viec: ngan hang cau hoi (chon dap an, loi giai chi tiet, luu tien do voi tien to ae2021:),
quiz nhanh o trang module, de thi (so cau dung khuon), bang tien do o trang chu. Chay: python3 tests/site_test.py"""
import os, sys, threading, http.server, socketserver, functools, json
from playwright.sync_api import sync_playwright
PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=PARENT); H.log_message = lambda *a, **k: None
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True
srv = TS(("127.0.0.1", 0), H); port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{port}/Aircraft-Systems/"
fails = []
def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info) if info and not ok else ""))
    if not ok: fails.append(name)
with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 1366, "height": 900}); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:150])); pg.on("console", lambda m: errs.append(m.text[:150]) if m.type == "error" else None)
    # 1. ngan hang m05
    pg.goto(BASE + "vi/practice/m05.html"); pg.wait_for_selector(".qitem")
    n_items = pg.evaluate("document.querySelectorAll('.qitem').length")
    check("bank m05 hien cau hoi", n_items > 0, n_items)
    first_id = pg.evaluate("document.querySelector('.qitem').id")
    pg.locator(".qitem").first.locator(".opt").first.click(); pg.wait_for_selector(".qitem .explain.show")
    check("bank: loi giai chi tiet (.detail) hien sau khi chon", pg.evaluate("!!document.querySelector('.qitem .explain.show .detail')"))
    keys = pg.evaluate("Object.keys(localStorage)")
    check("bank: khoa tien do co tien to ae2021:", any(k.startswith("ae2021:prog:bank:m05") for k in keys), keys)
    check("bank: KHONG co khoa tien do khong tien to", not any(k.startswith(("prog:", "bank:", "quiz:")) for k in keys), keys)
    # 2. tai lai trang: tien do con
    pg.reload(); pg.wait_for_selector(".qitem .explain.show")
    check("bank: tien do con sau khi tai lai", pg.evaluate("document.querySelectorAll('.qitem .explain.show').length") >= 1)
    # 3. quiz nhanh o trang module
    pg.goto(BASE + "vi/modules/05-data-buses/index.html"); pg.wait_for_selector(".quiz .opt, .quiz button")
    pg.evaluate("document.querySelector('.quiz .opt, .quiz button.opt')?.click()")
    pg.wait_for_timeout(200)
    check("module: quiz nhanh co cau hoi", pg.evaluate("document.querySelectorAll('.quiz .opt').length") >= 3)
    # 4. de thi: Final A co 45 cau
    pg.goto(BASE + "vi/exam/index.html"); pg.wait_for_selector("#exam .btn, #exam a")
    data = json.loads(pg.evaluate("fetch('data.json').then(r=>r.text())"))
    fa = next(p for p in data["papers"] if p["id"] == "final-A"); ma = next(p for p in data["papers"] if p["id"] == "midterm-A")
    check("exam: Final A va Midterm A dung so cau theo khuon", len(fa["ids"]) == data["types"]["final"]["n"] and len(ma["ids"]) == data["types"]["midterm"]["n"], (len(fa["ids"]), len(ma["ids"])))
    ids = {q["id"] for q in data["pool"]}
    check("exam: moi cau trong de nam trong ngan hang", all(i in ids for p in data["papers"] + data["mixed"] for i in p["ids"]))
    abc = [set(p["ids"]) for p in data["papers"] if p["type"] == "final"]
    check("exam: 3 de Final khong trung cau", len(abc) == 3 and not (abc[0] & abc[1] or abc[0] & abc[2] or abc[1] & abc[2]))
    # 5. trang chu: bang tien do
    pg.goto(BASE + "vi/index.html"); pg.wait_for_selector("#progress")
    pg.wait_for_timeout(300)
    txt = pg.inner_text("#progress")
    check("home: bang tien do hien so cau da lam", "1" in txt and "…" not in txt.strip()[:3], txt[:80])
    # 6. thuat ngu va cong thuc
    pg.goto(BASE + "vi/glossary/index.html"); pg.wait_for_selector("#gloss")
    total = pg.evaluate("document.querySelectorAll('#gloss tr').length - 1")
    pg.fill("#gloss-q", "bo giai ma"); pg.wait_for_timeout(200)
    shown = pg.evaluate("[...document.querySelectorAll('#gloss tr')].slice(1).filter(r=>r.style.display!=='none').length")
    check("glossary: loc khong dau 'bo giai ma' con 1 den 5 dong", 1 <= shown <= 5 and total > 100, (shown, total))
    pg.goto(BASE + "vi/formulas/index.html"); pg.wait_for_selector(".pd-formula"); pg.wait_for_timeout(500)
    check("formulas: KaTeX hien thi, 0 loi", pg.evaluate("document.querySelectorAll('.katex').length") >= 30 and pg.evaluate("document.querySelectorAll('.katex-error').length") == 0)
    check("khong co loi console/pageerror", not errs, errs[:3])
    b.close()
print("\nFAILS:", fails if fails else "none"); sys.exit(1 if fails else 0)
