"""Body of the Lab page (vi/lab/index.html, en/lab/index.html). Called by build_site.optional_pages: body(lang) -> html.
Static text (headings, descriptions, the NOT DONE card) is written here in both languages; the forms, results and KaTeX steps are built by _shared/lab.js on top of
_shared/thermo.js. The worked examples (inputs + reference values + sources) come from data/lab_expected.json, written by build/verify/verify_lab.py
(run it before building: a missing file is an error, never silently empty)."""
import json, os, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STYLE = """<style>
#lab{margin:0}.labcard{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:6px 16px 14px;margin:16px 0;box-shadow:var(--shadow)}
.labcard h2{border:0;margin:.7em 0 .2em;padding:0}.labcard h3{margin:1.2em 0 .1em;color:var(--accent2)}.labcard .dsc{margin:.2em 0 .6em;color:var(--muted);font-size:.93rem}
.labform{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px 16px;margin:.6em 0}.lf{display:flex;flex-direction:column;gap:3px;min-width:0;font-size:.9rem}
.lfc{color:var(--muted);font-size:.84rem;line-height:1.3}.lfb{display:flex;align-items:center;gap:6px;min-width:0}.lfu{color:var(--muted);font-size:.82rem;white-space:nowrap}
.lf input,.lf select{font:inherit;width:100%;min-width:0;box-sizing:border-box;padding:5px 8px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text)}
.lf input.bad{border-color:var(--bad);background:var(--badbg)}.lferr{color:var(--bad);font-size:.8rem;min-height:0}
.labbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:.4em 0 .8em}.exwrap{display:flex;flex-wrap:wrap;gap:8px;align-items:center;min-width:0}.exsel{max-width:100%;font:inherit;font-size:.88rem;padding:5px 6px;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--text)}
.labbtn{font:inherit;font-size:.9rem;padding:6px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}.labbtn.ex{background:var(--card);color:var(--accent);border-color:var(--accent)}.labbtn.ghost{background:none;color:var(--muted);border-color:var(--border)}
.tw{overflow-x:auto;max-width:100%}table.labres,table.refT{margin:6px 0}table.labres td.lq,table.refT td.lq{text-align:left}table.labres td.v{font-variant-numeric:tabular-nums;font-weight:600}table.labres tr.sec th{text-align:left;font-size:.82rem;color:var(--accent2)}
table.labres td.u{color:var(--muted);font-size:.86rem}
details.steps{border:1px solid var(--border);border-radius:10px;padding:4px 12px;margin:10px 0;background:var(--bg)}details.steps summary{cursor:pointer;font-weight:700;padding:4px 0}
.step{display:flex;gap:10px;align-items:flex-start;margin:6px 0;min-width:0}.step .sn{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:var(--accent2);color:#fff;font-size:.78rem;display:flex;align-items:center;justify-content:center;margin-top:2px}
.step .sb{min-width:0;flex:1;overflow-x:auto;overflow-y:hidden}.step .sb p{margin:0 0 2px;font-size:.88rem;color:var(--muted)}.step .sf{font-size:.95rem;overflow-x:auto;overflow-y:hidden;padding:2px 0}
.refs{border:2px solid var(--good);background:var(--goodbg);border-radius:10px;padding:2px 12px 8px;margin:10px 0}.refs h4{margin:.5em 0 .2em}.refsrc{font-weight:400;font-size:.82rem;color:var(--muted);display:block}
tr.refrow.ok td.mk{color:var(--good);font-weight:800}tr.refrow.bad td.mk{color:var(--bad);font-weight:800}tr.refrow.bad{background:var(--badbg)}.refnote{font-size:.88rem;margin:.4em 0 0}
.labtoc{display:flex;flex-wrap:wrap;gap:6px 14px;margin:.6em 0;padding:0;list-style:none}.labtoc a{font-size:.9rem}
.todo{border:2px dashed var(--warn);background:var(--warnbg);border-radius:12px;padding:6px 16px 10px;margin:16px 0}.todo h2{border:0;margin:.5em 0 .2em;padding:0;color:var(--warn)}.todo li{margin:.25em 0}.todo .tag{background:var(--warn);color:#fff;border-color:var(--warn)}
@media (max-width:480px){.labcard{padding:4px 10px 12px}.labform{grid-template-columns:1fr}h1{font-size:1.6rem}}
</style>"""

T = {
    'vi': dict(
        h1='Phòng thí nghiệm: máy tính kiểm bài làm tay',
        lead='Năm nhóm máy tính chạy hoàn toàn trong trình duyệt (không gửi dữ liệu đi đâu): chu trình Otto, Diesel, Brayton, dòng đẳng entropi và vòi phun, cân bằng phản ứng cháy. Mỗi máy hiện từng bước kèm công thức. Nút "Nạp ví dụ có lời giải" điền sẵn một bài có đáp án in hoặc đã tính lại hai đường, rồi so với giá trị tham chiếu và ghi nguồn. Ô nhập chấp nhận cả dấu phẩy lẫn dấu chấm thập phân (1,4 hoặc 1.4).',
        scope='Phạm vi và giả thiết',
        scope_b=['Khí lý tưởng, <b>tỉ số nhiệt dung k không đổi</b> (không khí-chuẩn / khí lạnh). Mặc định không khí: k = 1,4; R = 0,287 kJ/(kg·K) (Appendix 1 Table A-2 (a)); M<sub>không khí</sub> = 28,97 kg/kmol (Table A-1).',
                 'Máy tính là công cụ <b>kiểm</b> bài làm tay, không thay bài làm. Bài dùng bảng khí lý tưởng (c<sub>p</sub> biến thiên) cho số khác với k hằng: ví dụ Tutorials I bài 1 cho η = 0,523 bằng bảng nhưng 0,565 bằng khí lạnh.',
                 'Đơn vị SI: K, kPa, kJ/kg, kJ/(kg·K), m³/kg, kg/s. Đổi °C sang K bằng +273 (hoặc +273,15) trước khi nhập.'],
        todo='CHƯA LÀM trong lượt này', todo_b=['<b>Chu trình nén hơi R-134a</b> (làm lạnh): cần bộ tra thuộc tính (P3), chưa có.', '<b>Mọi bài dùng bảng khí lý tưởng với c<sub>p</sub> biến thiên</b> (Appendix 1 Table A-17, A-18…): cần bộ tra thuộc tính (P3), chưa có.', '<b>Điểm sương</b> của sản phẩm cháy: cần P<sub>sat</sub>(T) của nước từ bảng. CHƯA LÀM (cần bộ tra thuộc tính P3); không dùng công thức Antoine thay thế.',
                                          'Cháy không hoàn toàn (có CO), hỗn hợp giàu, nhiệt phản ứng và nhiệt độ ngọn lửa: ngoài phạm vi bản này.', 'Sốc thẳng, sốc xiên, dòng Fanno/Rayleigh và vòi hội tụ–phân kỳ có sóng: ngoài phạm vi (slide Chương 5 không đòi hỏi trong các ví dụ đã kiểm).'],
        c_otto='1. Chu trình Otto lý tưởng', d_otto='Nén đẳng entropi, cấp nhiệt đẳng tích, giãn nở đẳng entropi, thải nhiệt đẳng tích. Cho r, k, T₁, P₁ và một trong q_in, T₃, T₄.',
        c_diesel='2. Chu trình Diesel lý tưởng', d_diesel='Cấp nhiệt đẳng áp. Cho r, k, T₁, P₁ và một trong r_c, T₃, q_in. Hiện thêm công thức η theo r, r_c, k.',
        c_bray='3. Chu trình Brayton', d_bray='Có thể chọn hiệu suất đẳng entropi của máy nén và tuabin, hồi nhiệt (hiệu suất ε), làm mát trung gian và hâm nóng (số tầng, tỉ số áp chia đều, slide Ch.2 tr.33–48). Hiện tỉ số áp tối ưu cho w_net.',
        c_flow='4. Dòng đẳng entropi và vòi phun (Chương 5)', d_flow='Sáu máy nhỏ: (a) từ Ma, (b) từ A/A* (hai nhánh), (c) từ P/P₀, (d) tính chất hãm, (e) tỉ số tới hạn và lưu lượng nghẹt, (f) vòi hội tụ với áp suất ngược. k và R sửa được; mặc định không khí.',
        f_a='(a) Từ số Mach: T/T₀, P/P₀, ρ/ρ₀, A/A*', f_b='(b) Từ A/A*: số Mach nhánh dưới âm và trên âm; đoạn ống đổi tiết diện', f_c='(c) Từ P/P₀: số Mach (và T, c, V, diện tích nếu biết T₀, P₀, ṁ)', f_d='(d) Tính chất hãm T₀, P₀ từ T, P, V', f_e='(e) Tỉ số tới hạn và lưu lượng nghẹt tại họng', f_f='(f) Vòi hội tụ với áp suất ngược: nghẹt hay không',
        c_comb='5. Cân bằng phản ứng cháy (Chương 4)', d_comb='Nhiên liệu C<sub>a</sub>H<sub>b</sub>O<sub>c</sub>N<sub>d</sub> bất kỳ cháy hoàn toàn với không khí (3,76 N₂ cho mỗi O₂), không khí đủ hoặc thừa. Ra hệ số cân bằng, AF theo khối lượng và theo kmol, thành phần sản phẩm.',
        comb_note='<b>Nguồn khối lượng mol.</b> C = 12,011 (Appendix 1 Table A-27, dòng Carbon); H = 1,008; O = 15,999; N = 14,007. Appendix không liệt kê nguyên tử khối: ba giá trị sau là một nửa khối lượng mol phân tử ở Table A-1 (H₂ 2,016; O₂ 31,999; N₂ 28,013) làm tròn tới 0,001. Khối lượng mol tính ra vì vậy lệch bảng tới 0,001 kg/kmol (C₈H₁₈: 114,232 so với 114,231 của Table A-27). M<sub>không khí</sub> = 28,97 (Table A-1).',
        comb_todo='<span class="tag">CHƯA LÀM</span> Điểm sương: cần bộ tra thuộc tính P3 (P<sub>sat</sub>(T) của nước). Máy chỉ cho áp suất riêng phần của hơi nước P<sub>v</sub> = y<sub>H₂O</sub>·P.',
        toc='Mục lục'),
    'en': dict(
        h1='Lab: calculators to check your hand work',
        lead='Five groups of calculators run entirely in your browser (nothing is sent anywhere): Otto cycle, Diesel cycle, Brayton cycle, isentropic flow and nozzles, combustion balance. Each shows its steps with formulas. "Load worked example" fills in a problem with a printed or twice-recomputed answer, then compares with the reference values and names the source. Inputs accept a decimal comma or a decimal point (1,4 or 1.4).',
        scope='Scope and assumptions',
        scope_b=['Ideal gas with a <b>constant specific-heat ratio k</b> (air-standard / cold-air). Defaults for air: k = 1.4; R = 0.287 kJ/(kg·K) (Appendix 1 Table A-2 (a)); M<sub>air</sub> = 28.97 kg/kmol (Table A-1).',
                 'The calculators <b>check</b> a hand calculation, they do not replace it. Problems that use ideal-gas tables (variable c<sub>p</sub>) give different numbers from a constant k: Tutorials I problem 1 gives η = 0.523 with tables but 0.565 as cold-air.',
                 'SI units: K, kPa, kJ/kg, kJ/(kg·K), m³/kg, kg/s. Convert °C to K (+273 or +273.15) before typing.'],
        todo='NOT DONE in this round', todo_b=['<b>R-134a vapour-compression cycle</b> (refrigeration): needs the property library (P3), which does not exist yet.', '<b>Every problem that uses ideal-gas tables with variable c<sub>p</sub></b> (Appendix 1 Table A-17, A-18…): needs the property library (P3), not available yet.', '<b>Dew point</b> of the combustion products: needs P<sub>sat</sub>(T) of water from the tables. NOT DONE (needs the property library P3); no Antoine formula is used instead.',
                                          'Incomplete combustion (CO), rich mixtures, heat of reaction and flame temperature: outside this version.', 'Normal and oblique shocks, Fanno/Rayleigh flow and converging–diverging nozzles with shocks: outside this version (the checked Chapter 5 examples do not need them).'],
        c_otto='1. Ideal Otto cycle', d_otto='Isentropic compression, constant-volume heat addition, isentropic expansion, constant-volume heat rejection. Give r, k, T₁, P₁ and one of q_in, T₃, T₄.',
        c_diesel='2. Ideal Diesel cycle', d_diesel='Constant-pressure heat addition. Give r, k, T₁, P₁ and one of r_c, T₃, q_in. The η formula in r, r_c, k is shown too.',
        c_bray='3. Brayton cycle', d_bray='Optional isentropic efficiencies of compressor and turbine, regeneration (effectiveness ε), intercooling and reheating (number of stages, equal pressure ratio per stage, slide Ch.2 p.33–48). Shows the pressure ratio that maximises w_net.',
        c_flow='4. Isentropic flow and nozzles (Chapter 5)', d_flow='Six small tools: (a) from Ma, (b) from A/A* (both branches), (c) from P/P₀, (d) stagnation properties, (e) critical ratios and choked flow, (f) converging nozzle with back pressure. k and R are editable; defaults are for air.',
        f_a='(a) From the Mach number: T/T₀, P/P₀, ρ/ρ₀, A/A*', f_b='(b) From A/A*: subsonic and supersonic Mach numbers; duct with an area change', f_c='(c) From P/P₀: Mach number (and T, c, V, area when T₀, P₀, ṁ are known)', f_d='(d) Stagnation properties T₀, P₀ from T, P, V', f_e='(e) Critical ratios and choked flow at the throat', f_f='(f) Converging nozzle with back pressure: choked or not',
        c_comb='5. Combustion balance (Chapter 4)', d_comb='Any fuel C<sub>a</sub>H<sub>b</sub>O<sub>c</sub>N<sub>d</sub> burning completely in air (3.76 N₂ per O₂), stoichiometric or lean. Gives the balance coefficients, AF on a mass and a mole basis, and the product composition.',
        comb_note='<b>Source of the molar masses.</b> C = 12.011 (Appendix 1 Table A-27, Carbon row); H = 1.008; O = 15.999; N = 14.007. The Appendix lists no atomic masses: the last three are half the molecular masses of Table A-1 (H₂ 2.016; O₂ 31.999; N₂ 28.013) rounded to 0.001. Computed molar masses therefore differ from the tables by up to 0.001 kg/kmol (C₈H₁₈: 114.232 vs 114.231 in Table A-27). M<sub>air</sub> = 28.97 (Table A-1).',
        comb_todo='<span class="tag">NOT DONE</span> Dew point: needs the property library P3 (P<sub>sat</sub>(T) of water). The calculator only gives the partial pressure of the water vapour P<sub>v</sub> = y<sub>H₂O</sub>·P.',
        toc='Contents'),
}


def examples_json():
    p = os.path.join(ROOT, 'data', 'lab_expected.json')
    if not os.path.exists(p):
        raise FileNotFoundError('data/lab_expected.json missing: run .venv/bin/python -I build/verify/verify_lab.py first')
    ex = json.load(open(p, encoding='utf-8'))['examples']
    return json.dumps({'examples': ex}, ensure_ascii=False).replace('<', '\\u003c')


def calc(cid):
    return f'<div class="calc" data-calc="{cid}"></div>'


def body(lang):
    t = T[lang]
    secs = [('lab-otto', t['c_otto']), ('lab-diesel', t['c_diesel']), ('lab-brayton', t['c_bray']), ('lab-flow', t['c_flow']), ('lab-comb', t['c_comb'])]
    h = STYLE + f'<h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p>'
    h += f'<div class="callout info"><b class="t">{t["scope"]}</b><ul style="margin:.2em 0 0;padding-left:1.2em">' + ''.join(f'<li>{x}</li>' for x in t['scope_b']) + '</ul></div>'
    h += f'<div class="todo" id="lab-todo"><h2>{t["todo"]}</h2><ul>' + ''.join(f'<li>{x}</li>' for x in t['todo_b']) + '</ul></div>'
    h += f'<nav aria-label="{t["toc"]}"><ul class="labtoc">' + ''.join(f'<li><a href="#{i}">{html.escape(x)}</a></li>' for i, x in secs) + '</ul></nav>'
    h += '<div id="lab">'
    for cid, key in (('otto', 'otto'), ('diesel', 'diesel'), ('brayton', 'bray')):
        h += f'<section class="labcard" id="lab-{cid}"><h2>{t["c_" + key]}</h2><p class="dsc">{t["d_" + key]}</p>{calc(cid)}</section>'
    h += f'<section class="labcard" id="lab-flow"><h2>{t["c_flow"]}</h2><p class="dsc">{t["d_flow"]}</p>'
    for cid, key in (('flow_ma', 'f_a'), ('flow_aas', 'f_b'), ('flow_pr', 'f_c'), ('flow_stag', 'f_d'), ('flow_crit', 'f_e'), ('flow_noz', 'f_f')):
        h += f'<h3>{t[key]}</h3>{calc(cid)}'
    h += '</section>'
    h += f'<section class="labcard" id="lab-comb"><h2>{t["c_comb"]}</h2><p class="dsc">{t["d_comb"]}</p>{calc("comb")}<div class="callout warn">{t["comb_todo"]}</div><p class="dsc">{t["comb_note"]}</p></section>'
    h += '</div>'
    h += f'<script type="application/json" id="lab-examples">{examples_json()}</script><script src="{{R}}_shared/thermo.js"></script>'
    return h
