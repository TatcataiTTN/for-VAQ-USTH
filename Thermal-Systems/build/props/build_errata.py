"""Sinh data/props/book_errata.json tu cac kiem tra noi bang (locate_errors.py) + muc da biet tu _qa/app.json.
Moi muc: table, row (khoa hang), col, printed, expected, how, seen_image (da xem anh trang chua), pdf_page, kind.
python3 -I build/props/build_errata.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locate_errors as L, consistency as C
P = L.P
# Trang da xem anh 130 dpi trong P3 (doc tay): A-17 p28,29; A-17E p76,77; A-32 p48; A-18 p31; A-19 p32,33; A-20 p34,35; A-21 p37
SEEN = {28, 29, 76, 77, 48, 31, 32, 33, 34, 35, 37, 2, 4, 5, 8, 9, 10, 11, 12, 13, 15, 16, 20, 21, 22, 23, 24}

EN = [
 ('ū khớp nội suy hàng xóm', 'ū agrees with interpolation between neighbouring rows'),
 ('h̄ khớp nội suy hàng xóm', 'h̄ agrees with interpolation between neighbouring rows'),
 ('s̄° = s̄°(hàng trước) + Δh̄/T_lm; hai hiệu liền kề lệch bằng nhau, ngược dấu', 's̄° = s̄°(previous row) + Δh̄/T_lm; the two adjacent differences are equal and of opposite sign'),
 ('(trung vị cả bảng); hàng xóm cho biết ô h lệch', '(median of the table); neighbouring rows show that the h cell is off'),
 ('(trung vị cả bảng); hàng xóm cho biết ô u lệch', '(median of the table); neighbouring rows show that the u cell is off'),
 ('P_r = P_r(hàng trước)·exp(Δs°/R); hai cặp liền kề lệch ngược dấu', 'P_r = P_r(previous row)·exp(Δs°/R); the two adjacent pairs deviate with opposite sign'),
 ('(trung vị)', '(median)'),
 ('s° = s°(hàng sau) − R·ln(P_r sau / P_r này); P_r hàng này và hàng hai bên khớp nhau', 's° = s°(next row) − R·ln(P_r next / P_r this); P_r of this row and of its neighbours are mutually consistent'),
 ('h = h(hàng trước) + Δs°·T_lm; P_r và s° ở hàng này khớp nhau nên ô h lệch (nguyên nhân chưa xác định: có thể hàng này ứng với 536,67 R)', 'h = h(previous row) + Δs°·T_lm; P_r and s° of this row agree with each other so the h cell is off (cause not determined: this row may really correspond to 536.67 R)'),
 ('u = h − R·T (R = 0,28706): u in lệch hệ thống −0,5…−0,8 kJ/kg (≈0,04 %) từ 1700 K; không rõ ô h hay u (nguồn Keenan–Kaye); coi là cảnh báo nhẹ', 'u = h − R·T (R = 0.28706): printed u is off systematically by −0.5…−0.8 kJ/kg (≈0.04 %) from 1700 K; unclear whether h or u (Keenan–Kaye source); treated as a mild warning'),
 ('ρ/ρ0 = (1+0,2·Ma²)^−2,5 tại Ma = 3,0 cho 0,0762', 'ρ/ρ0 = (1+0.2·Ma²)^−2.5 at Ma = 3.0 gives 0.0762'),
 ('cp − cv = 1,7164 − 1,5734 = 0,1430 và A-1 (n-butane) cho R = 0,1430; A-2a in 0,1433', 'cp − cv = 1.7164 − 1.5734 = 0.1430 and A-1 (n-butane) gives R = 0.1430; A-2a prints 0.1433'),
 ('với R =', 'with R ='),
]
import re as _re
VI_CH = _re.compile('[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]', _re.I)

def to_en(how):
    out = how
    for a, b in EN:
        out = out.replace(a, b)
    return out

def build():
    E = []
    air = L.air_tables(); kmol = L.kmol_tables()
    flagged_pr = {(e['table'], tuple(e['key'].items())) for e in air if e['col'] == 'Pr'}
    flagged_hu = {(e['table'], tuple(e['key'].items())) for e in air if e['col'] in ('h', 'u')}
    for e in air:
        k = (e['table'], tuple(e['key'].items()))
        if e['col'] == 'vr' and k in flagged_pr:
            continue                               # Pr la o sai (hai cap s0), vr khop hang xom
        if e['col'] == 'h|s0':
            if k in flagged_hu:
                continue                           # da co muc h (h-u)
            # s0 sai: tinh tu Pr
            import math
            t = L.load('A17E' if e['table'] == 'A-17E' else 'A17')
            e = dict(e)
            rows = t['rows']; i = [r[0] for r in rows].index(list(e['key'].values())[0])
            Rm = 0.068549 if e['table'] == 'A-17E' else 0.287057
            a, b, c = rows[i - 1], rows[i], rows[i + 1]
            e1 = math.log(b[2] / a[2]) - (b[5] - a[5]) / Rm; e2 = math.log(c[2] / b[2]) - (c[5] - b[5]) / Rm
            if abs(e1) < 0.0015 and abs(e2) < 0.0015:
                Tl = (b[0] - a[0]) / math.log(b[0] / a[0])
                e['col'] = 'h'; e['printed'] = e['printed'][0]; e['expected'] = round(a[1] + (b[5] - a[5]) * Tl, 2)
                e['how'] = 'h = h(hàng trước) + Δs°·T_lm; P_r và s° ở hàng này khớp nhau nên ô h lệch (nguyên nhân chưa xác định: có thể hàng này ứng với 536,67 R)'
                E.append(e); continue
            e['col'] = 's0'; e['printed'] = e['printed'][1]
            # Pr(i+1) dung, Pr(i-1) co the da sai: dung Pr(i+1)
            import math
            e['expected'] = round(rows[i + 1][5] - Rm * math.log(rows[i + 1][2] / rows[i][2]), 5)
            e['how'] = 's° = s°(hàng sau) − R·ln(P_r sau / P_r này); P_r hàng này và hàng hai bên khớp nhau'
        # h-u o T>=1700 K cua A-17: lech he thong, khong phai loi tung o
        if e['table'] == 'A-17' and e['col'] in ('h', 'u') and list(e['key'].values())[0] >= 1700:
            continue
        E.append(e)
    E += kmol
    # A-17 T >= 1700 K: lech he thong h-u (dung cot u theo yeu cau, kind rieng)
    t17 = L.load('A17'); Rm = 0.287057
    for r, pg in zip(t17['rows'], t17['row_pages']):
        if r[0] >= 1700 and abs(r[1] - r[3] - Rm * r[0]) > 0.25 + 1.5e-4 * r[0]:
            E.append(dict(table='A-17', key={'T_K': r[0]}, col='u', printed=r[3], expected=round(r[1] - Rm * r[0], 2), pdf_page=pg, how='u = h − R·T (R = 0,28706): u in lệch hệ thống −0,5…−0,8 kJ/kg (≈0,04 %) từ 1700 K; không rõ ô h hay u (nguồn Keenan–Kaye); coi là cảnh báo nhẹ', diff=round(r[1] - r[3] - Rm * r[0], 3), kind='systematic_offset'))
    # A-17 550 K: QA da nghi u, nhung h moi sai
    # A-32 rho/rho0 tai Ma=3.0
    for f in C.run():
        if f['table'] == 'A-32':
            E.append(dict(table='A-32', key=f['key'], col='rho_rho0', printed=f['printed'], expected=f['expected'], pdf_page=48, how='ρ/ρ0 = (1+0,2·Ma²)^−2,5 tại Ma = 3,0 cho 0,0762', diff=f['diff']))
        if f['table'] == 'A-2a' and f['check'] == 'cp-cv=R':
            E.append(dict(table='A-2a', key=f['key'], col='R', printed=0.1433, expected=0.1430, pdf_page=3, how='cp − cv = 1,7164 − 1,5734 = 0,1430 và A-1 (n-butane) cho R = 0,1430; A-2a in 0,1433', diff=-0.0003))
    for e in E:
        e['how_en'] = to_en(e['how'])
        if VI_CH.search(e['how_en']): raise SystemExit('how_en còn tiếng Việt: ' + e['how_en'])
        e['seen_image'] = e['pdf_page'] in SEEN
        e.setdefault('kind', 'book_print_error')
        e['printed_in_image'] = 'bản chữ = ảnh' if e['seen_image'] else 'chưa so ảnh'
    # ghi chu ve ket luan khac voi QA
    notes = [
        {'table': 'A-17', 'row': {'T_K': 550}, 'note': 'QA (_qa/app.json) nghi u(550 K)=396,86; kiểm nhất quán cho thấy h = 555,74 mới là ô sai (h−u = RT và Δs°=Δh/T chỉ khớp với h ≈ 554,74; u = 396,86 khớp 554,74 − 0,287·550). Giá trị u in đúng.'},
        {'table': 'A-17', 'row': {'T_K': 630}, 'note': 'QA nghi v_r(630 K)=92,84. Kiểm nhất quán: v_r khớp hàng xóm (96,92; 88,99 → 92,87); P_r = 19,84 mới lệch (≈ 19,47 theo s° và hàng xóm). Ô sai là P_r.'},
        {'table': 'A-17', 'row': {'T_K': '>=1700'}, 'note': 'Từ 1700 K h − u thấp hơn R·T (R = 0,28706) khoảng 0,5–0,7 kJ/kg (≈0,04 %) đều ở mọi hàng: lệch hệ thống của nguồn Keenan–Kaye, không phải lỗi từng ô; không đánh dấu suspect.'},
        {'table': 'A-17', 'row': {'T_K': 298}, 'note': 'v_r·P_r/T lệch 0,06 % ở hàng 298 K và h−u hơi lệch ở hàng 298 K của A-18…A-25 (≈1,3–1,9 kJ/kmol): hàng 298 K được sách thêm riêng (làm tròn khác), không coi là lỗi.'},
        {'table': 'A-2a', 'row': {'gas': 'Carbon monoxide'}, 'note': 'k = 1,400 trong khi cp/cv = 1,040/0,744 = 1,398: k tính từ giá trị chưa làm tròn của sách; không phải lỗi.'},
    ]
    return E, notes

if __name__ == '__main__':
    E, notes = build()
    out = dict(description='Lỗi in của Appendix 1 (Cengel) tìm thấy khi kiểm nhất quán nội bảng; giá trị in được trả nguyên trong thư viện nhưng đánh dấu suspect. expected = giá trị kỳ vọng suy từ quan hệ vật lý + hàng xóm (không phải số của sách).',
               n=len(E), errors=E, not_errors_or_corrections=notes)
    with open(os.path.join(L.D, 'book_errata.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(E), Counter(e['table'] for e in E))
    for e in E:
        if e['table'].startswith('A-17') or e['table'] in ('A-32', 'A-2a'): print(e['table'], e['key'], e['col'], e['printed'], '->', e['expected'])
