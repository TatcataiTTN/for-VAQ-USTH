# -*- coding: utf-8 -*-
"""Test trinh duyet that cho cac cong cu: Khai niem, Phan tich de, Bai tap co dap an, Viet tay, So loi, Bang tra ma, va lien ket #id vao ngan hang (vi va en). Chay: python3 tests/tools_test.py"""
import os, sys, threading, http.server, socketserver, functools, json
from playwright.sync_api import sync_playwright
PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=PARENT); H.log_message = lambda *a, **k: None
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True
srv = TS(("127.0.0.1", 0), H); port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{port}/Aircraft-Systems/"
fails = []
def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:200] if info and not ok else ""))
    if not ok: fails.append(name)
with sync_playwright() as pw:
    b = pw.chromium.launch(); errs = []
    for lang in ("vi", "en"):
        ctx = b.new_context(viewport={"width": 1366, "height": 900}); pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)[:150])); pg.on("console", lambda m: errs.append(m.text[:150]) if m.type == "error" else None)
        U = BASE + lang + "/"
        S = json.loads(pg.request.get(U + "data/search.json").text()); items = S["items"]
        check(f"{lang}: search.json co du module 1 den 15", len(S["mods"]) == 15 and len(items) > 1000, (len(S["mods"]), len(items)))
        # --- Khai niem
        pg.goto(U + "concepts/index.html"); pg.wait_for_selector("#concepts .mod-card")
        n0 = pg.evaluate("document.querySelectorAll('#concepts .mod-card').length")
        check(f"{lang}: Khai niem co >= 60 khai niem", n0 >= 60, n0)
        pg.fill("#concepts input[type=search]", "AFDX"); pg.wait_for_timeout(150)
        n1 = pg.evaluate("document.querySelectorAll('#concepts .mod-card').length")
        check(f"{lang}: tim 'AFDX' con 1 den {n0 - 1} khai niem", 1 <= n1 < n0, n1)
        pg.fill("#concepts input[type=search]", "thanh ghi dich" if lang == "vi" else "shift register"); pg.wait_for_timeout(150)
        check(f"{lang}: tim khong dau 'thanh ghi dich'/'shift register' co ket qua", pg.evaluate("document.querySelectorAll('#concepts .mod-card').length") >= 1)
        href = pg.evaluate("document.querySelector('#concepts .mod-card a.btn').getAttribute('href')")
        pg.goto(U + "concepts/" + href); pg.wait_for_selector(".qitem")
        check(f"{lang}: nut Luyen chu de mo dung ngan hang da loc", pg.evaluate("document.querySelectorAll('.qitem').length") >= 1, href)
        # --- Phan tich de
        known = next(i for i in items if i["m"] == "m13" and i["o"] == "b" and i["k"] == "mcq")
        pg.goto(U + "analyse/index.html"); pg.wait_for_selector("#analyse textarea"); pg.fill("#analyse textarea", known["q"]); pg.click("#analyse button")
        pg.wait_for_selector("#analyse .qitem")
        top = pg.evaluate("document.querySelector('#analyse .qitem a').getAttribute('href')")
        check(f"{lang}: Phan tich de: dan nguyen cau {known['id']} thi cau giong nhat chinh la no", known["id"] in top, top)
        check(f"{lang}: Phan tich de du doan dung module m13", "M13" in pg.inner_text("#analyse .panel"), pg.inner_text("#analyse .panel")[:120])
        pg.fill("#analyse textarea", "how to bake a chocolate cake with butter and sugar" if lang == "en" else "cach lam banh socola voi bo va duong"); pg.click("#analyse button"); pg.wait_for_selector("#analyse .callout")
        check(f"{lang}: Phan tich de bao ngoai danh muc voi de la", pg.evaluate("!!document.querySelector('#analyse .callout.warn')"))
        # --- Bai tap co dap an
        pg.goto(U + "exercises/index.html"); pg.wait_for_selector("#exercises table.t tr:nth-child(5)")
        pg.select_option("#exercises select >> nth=0", "Tooley"); pg.wait_for_timeout(200)
        rows = pg.evaluate("document.querySelectorAll('#exercises .tablewrap table.t')[0].rows.length")
        check(f"{lang}: Bai tap loc Tooley co nhieu dong", rows > 30, rows)
        check(f"{lang}: bang do phu co Tooley Ch.16 va Ch.17 va Floyd Ch.7", all(k in pg.inner_text("#exercises") for k in ("Tooley Ch.16", "Tooley Ch.17", "Floyd Ch.7")))
        # --- Viet tay
        pg.goto(U + "written/index.html"); pg.wait_for_selector("#written .qitem")
        nq = pg.evaluate("document.querySelectorAll('#written .qitem').length"); check(f"{lang}: Viet tay co >= 100 bai", nq >= 100, nq)
        pg.click("#written .qitem >> nth=0 >> button >> nth=0"); check(f"{lang}: Viet tay xem duoc loi giai", pg.evaluate("document.querySelector('#written .qitem .explain.show') !== null"))
        pg.click("#written .qitem >> nth=0 >> button >> nth=1"); pg.wait_for_timeout(150)
        keys = pg.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('ae2021:prog:written:'))"); check(f"{lang}: Viet tay luu tien do voi tien to ae2021:", len(keys) == 1, keys)
        # --- So loi
        mm = next(i for i in items if i["m"] == "m11" and i["k"] == "mcq")
        pg.goto(U + "mistakes/index.html"); pg.wait_for_selector("#mistakes .callout")
        check(f"{lang}: So loi trong khi chua sai cau nao", pg.evaluate("document.querySelectorAll('#mistakes .qitem').length") == 0)
        pg.evaluate("(id)=>localStorage.setItem('ae2021:prog:wrong', JSON.stringify({[id]:{k:'w',n:2,t:Date.now()}}))", mm["id"]); pg.reload(); pg.wait_for_selector("#mistakes .qitem")
        check(f"{lang}: So loi hien cau sai va nut on lai", pg.evaluate("document.querySelectorAll('#mistakes .qitem').length") == 1 and pg.evaluate("!!document.querySelector('#mistakes a[href*=\"exam=review\"]')"))
        pg.click("#mistakes .qitem >> button >> nth=0"); pg.wait_for_timeout(150); check(f"{lang}: So loi an cau da hieu", pg.evaluate("document.querySelectorAll('#mistakes .qitem').length") == 0)
        # --- Bang tra ma
        pg.goto(U + "codes/index.html"); pg.wait_for_selector("#code-table")
        check(f"{lang}: Bang ma co 128 dong", pg.evaluate("document.querySelectorAll('#code-table tr').length") == 129)
        pg.fill("#conv input[data-k=dec]", "65"); pg.wait_for_timeout(100)
        got = pg.evaluate("['oct','hex','bin','chr'].map(k=>document.querySelector('#conv input[data-k='+k+']').value)")
        check(f"{lang}: may doi ma: 65 -> 101, 41, 01000001, A", got == ["101", "41", "01000001", "A"], got)
        pg.fill("#conv input[data-k=hex]", "7F"); pg.wait_for_timeout(100); check(f"{lang}: 7F -> 127 va DEL", pg.evaluate("document.querySelector('#conv input[data-k=dec]').value") == "127")
        pg.fill("#drill input", "zzz"); pg.click("#drill button >> nth=0"); check(f"{lang}: Luyen doi ma cham sai", "✘" in pg.inner_text("#drill"))
        # --- lien ket #id vao trang thu ba cua ngan hang
        far = next(i for i in items if i["m"] == "m13" and i["k"] == "mcq" and i["o"] == "b")
        pg.goto(U + f"practice/m13.html#{far['id']}"); pg.wait_for_timeout(500)
        check(f"{lang}: #id mo dung trang ngan hang chua cau {far['id']}", pg.evaluate("(id)=>!!document.getElementById(id)", far["id"]))
        ctx.close()
    check("khong co loi console/pageerror", not errs, errs[:3])
    b.close()
print("\nFAILS:", fails if fails else "none"); sys.exit(1 if fails else 0)
