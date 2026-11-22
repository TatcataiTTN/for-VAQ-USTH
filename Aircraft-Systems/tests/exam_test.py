# -*- coding: utf-8 -*-
"""Test trinh duyet that cho MOI loai de thi (vi va en): trang chu de co du cac loai, lam de trac nghiem (theo module, kho, Tooley), de tu luan (lam, nop, tu cham),
de tong hop (trac nghiem roi tu luan), on lai cau sai, ban in A4 co dap an, ket qua luu voi tien to ae2021:. Chay: python3 tests/exam_test.py"""
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

def run_mcq(pg, url, pick_first=True):
    """Open run.html, start, answer every question with option A, submit; return the result text."""
    pg.goto(url); pg.wait_for_selector("#exam .btn")
    pg.click("#exam .panel .btn")                                      # Bat dau
    pg.wait_for_selector(".exambar"); n = int(pg.inner_text(".exambar .prog").split("/")[-1])
    for i in range(n):
        pg.keyboard.press("a"); pg.keyboard.press("ArrowRight")
        pg.on("dialog", lambda d: d.accept())
    pg.wait_for_selector("text=/Kết quả|Result/", timeout=8000)
    return n

with sync_playwright() as pw:
    b = pw.chromium.launch(); errs = []
    for lang in ("vi", "en"):
        ctx = b.new_context(viewport={"width": 1366, "height": 900}); pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)[:150])); pg.on("console", lambda m: errs.append(m.text[:150]) if m.type == "error" else None)
        pg.on("dialog", lambda d: d.accept())
        pg.goto(BASE + f"{lang}/exam/index.html"); pg.wait_for_selector("#exam h2")
        data = json.loads(pg.evaluate("fetch('data.json').then(r=>r.text())"))
        types = {p["type"] for p in data["papers"]}
        need = {"entry", "midterm", "final", "module", "hard", "tooley", "written", "full"}
        check(f"{lang}: de co du loai {sorted(need)}", need <= types and len(data["mixed"]) >= 4, types)
        heads = pg.evaluate("[...document.querySelectorAll('#exam h2')].map(h=>h.textContent)")
        check(f"{lang}: trang chu de co >= 10 muc", len(heads) >= 10, heads)
        pool = {q["id"] for q in data["pool"]}; wp = {w["id"] for w in data["wpool"]}
        check(f"{lang}: moi cau (trac nghiem va tu luan) cua moi de co trong du lieu", all(i in pool for p in data["papers"] + data["mixed"] for i in p["ids"]) and all(i in wp for p in data["papers"] for i in p.get("wids", [])))
        mod = next(p for p in data["papers"] if p["type"] == "module"); hard = next(p for p in data["papers"] if p["type"] == "hard")
        lv = {q["id"]: q["l"] for q in data["pool"]}
        check(f"{lang}: de Hard chi gom cau muc 3", all(lv[i] == 3 for i in hard["ids"]), hard["id"])
        wA = next(p for p in data["papers"] if p["id"] == "written-A"); fA = next(p for p in data["papers"] if p["id"] == "full-A")
        # --- de theo module
        n = run_mcq(pg, BASE + f"{lang}/exam/run.html?exam={mod['id']}")
        check(f"{lang}: de {mod['id']} lam xong, {n} cau", n == len(mod["ids"]), n)
        check(f"{lang}: ket qua luu khoa ae2021:prog:exam:{mod['id']}", pg.evaluate(f"!!localStorage.getItem('ae2021:prog:exam:{mod['id']}')"))
        # --- on lai cau sai: sau khi lam de, so cau sai > 0 va de review rut duoc cau
        pg.goto(BASE + f"{lang}/exam/index.html"); pg.wait_for_selector("#exam h2")
        has_review = pg.evaluate("!!document.querySelector('a[href*=\"exam=review\"]')")
        check(f"{lang}: co nut on lai cau sai sau khi lam sai", has_review)
        if has_review:
            n2 = run_mcq(pg, BASE + f"{lang}/exam/run.html?exam=review")
            check(f"{lang}: de on lai cau sai chay duoc ({n2} cau)", n2 >= 1)
        # --- kiem tra dau vao: 20 cau tu ngan hang m00; thu tu lua chon duoc xao moi lan lam
        ent = next(p for p in data["papers"] if p["id"] == "entry"); n3 = run_mcq(pg, BASE + f"{lang}/exam/run.html?exam=entry")
        check(f"{lang}: kiem tra dau vao {n3} cau, nam trong ngan hang", n3 == len(ent["ids"]) == 20 and all(i.startswith("m00-") for i in ent["ids"]))
        pg.goto(BASE + f"{lang}/exam/run.html?exam=module-m11"); pg.wait_for_selector("#exam .panel .btn"); pg.click("#exam .panel .btn"); pg.wait_for_selector(".opt")
        o1 = pg.evaluate("[...document.querySelectorAll('.opt')].map(b=>b.textContent).join('|')"); st = pg.evaluate("JSON.parse(sessionStorage.getItem(Object.keys(sessionStorage).find(k=>k.startsWith('examrun:')))).perm.length")
        check(f"{lang}: moi lan lam co hoan vi lua chon luu theo cau ({st} cau)", st == 15 and "|" in o1)
        # --- de tu luan
        pg.goto(BASE + f"{lang}/exam/run.html?exam=written-A"); pg.wait_for_selector("#exam .panel .btn"); pg.click("#exam .panel .btn")
        pg.wait_for_selector("textarea"); nw = pg.evaluate("document.querySelectorAll('textarea').length")
        check(f"{lang}: de tu luan hien {nw} bai co o ghi chu", nw == len(wA["wids"]), nw)
        pg.fill("textarea >> nth=0", "ghi chu thu"); pg.click(".exambar .btn")
        pg.wait_for_selector("select"); ns = pg.evaluate("document.querySelectorAll('select').length")
        check(f"{lang}: sau khi nop hien loi giai va {ns} o tu cham", ns == nw and pg.evaluate("document.querySelectorAll('.explain.show').length") == nw)
        pg.select_option("select >> nth=0", index=1); pg.click("text=/Xong, tính điểm|Done, compute the score/")
        pg.wait_for_selector("text=/Kết quả|Result/")
        check(f"{lang}: ket qua tu luan luu khoa ae2021:prog:exam:written-A", pg.evaluate("!!localStorage.getItem('ae2021:prog:exam:written-A')"))
        # --- de tong hop: phan trac nghiem roi phan tu luan
        pg.goto(BASE + f"{lang}/exam/run.html?exam=full-A"); pg.wait_for_selector("#exam .panel .btn"); pg.click("#exam .panel .btn"); pg.wait_for_selector(".exambar")
        for i in range(len(fA["ids"])): pg.keyboard.press("b"); pg.keyboard.press("ArrowRight")
        pg.wait_for_selector("text=/Kết quả|Result/")
        pg.click("text=/Sang phần II|Go to part II/"); pg.wait_for_selector("#exam .panel .btn"); pg.click("#exam .panel .btn"); pg.wait_for_selector("textarea")
        pg.click(".exambar .btn"); pg.wait_for_selector("select"); pg.click("text=/Xong, tính điểm|Done, compute the score/"); pg.wait_for_selector("text=/Tổng cộng|Total/")
        rec = json.loads(pg.evaluate("localStorage.getItem('ae2021:prog:exam:full-A')"))
        check(f"{lang}: de tong hop tinh gop diem /100", rec["n"] == len(fA["ids"]) * fA["mcq_marks"] + sum(fA["wmarks"].values()) == 100, rec)
        # --- ban in
        for pid in (mod["id"], "rev-2", "written-B", "full-B", "hard-A"):
            pg.goto(BASE + f"{lang}/exam/print.html?exam={pid}"); pg.wait_for_selector(".xprint h1")
            body = pg.inner_text(".xprint"); pd = next(p for p in data["papers"] if p["id"] == pid)
            exp_q = len(pd["ids"]); got_q = pg.evaluate("document.querySelectorAll('.xprint .xq').length")
            check(f"{lang}: ban in {pid}: {exp_q} cau trac nghiem + {len(pd.get('wids', []))} bai tu luan (khung .xq tong {got_q})", got_q >= exp_q + len(pd.get("wids", [])) and ("Đáp án" in body or "Answer key" in body), (exp_q, got_q))
        ctx.close()
    check("khong co loi console/pageerror", not errs, errs[:3])
    b.close()
print("\nFAILS:", fails if fails else "none"); sys.exit(1 if fails else 0)
