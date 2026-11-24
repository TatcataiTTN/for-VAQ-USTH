# -*- coding: utf-8 -*-
"""Bai tap cuoi chuong GOC cua Floyd (Digital Fundamentals 11e) co dap an in o phu luc, ve m11 (Ch.7 den Ch.9) va m10 (Ch.12), chon cac bai CHI CAN CHU VA SO (khong phu thuoc hinh)
de TU TINH LAI duoc (R1: moi dap an qua hai duong: dap an in cua sach va phep tinh cua site; build/verify/verify_floyd_ex.py).
Moi bai co anh de bai (cat tu PDF goc) va anh dap an in; anh cat tu dong bang build/gen/floyd_crop.py -> assets/figures/floyd_ex_chNN_{q,a}N.png.
Ket qua: data/qsrc/m11_fex.json, m10_fex.json (kind 'ess', origin 'goc') va data/verify/floyd_ex_meta.json. Cac chenh lech dap an in so voi de bai duoc ghi trong nhan nguon va trong notes."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'numlib'))
import floyd_crop as FC, seq as S
ROOT = FC.ROOT; FIG = os.path.join(ROOT, 'assets', 'figures')
TOP = {'latch': ('Chốt và flip-flop', 'Latches and flip-flops'), 'timing': ('Mạch một nhịp và bộ định thời 555', 'One-shots and the 555 timer'), 'shift': ('Thanh ghi dịch', 'Shift registers'), 'counter': ('Bộ đếm và máy trạng thái', 'Counters and state machines'),
       'specs': ('Độ phân giải, độ chính xác, lỗi chuyển đổi', 'Resolution, accuracy, conversion errors'), 'opamp': ('Op-amp trong bộ chuyển đổi', 'Op-amps in converters')}
# ---- phep tinh (cai dat thu nhat, dung seq.py); verify_floyd_ex.py tinh lai bang cach khac
f21 = 1 / (20e-9 + 40e-9); i23 = 16 * 8e-3; p23 = 4 * i23; tw27 = S.one_shot(1e3, 1e-12); r29 = 0.5 / (1.1 * 1e-6); t29 = S.t555_mono(430e3, 1e-6)
c31 = 0.004e-6; s31 = 1.44 / (10e3 * c31); r2_31 = s31 - 0.8 * s31; r1_31 = 0.8 * s31 - r2_31
fd = lambda r1, r2, c: 1.44 / ((r1 + 2 * r2) * c); dd = lambda r1, r2: (r1 + r2) / (r1 + 2 * r2)
f31_e24 = fd(22e3, 7.5e3, c31); d31_e24 = dd(22e3, 7.5e3); f31_pr = fd(9.1e3, 4.3e3, c31); d31_pr = dd(9.1e3, 4.3e3); c31_pr = 1.44 / ((9.1e3 + 8.6e3) * 10e3)
def d1(x): return f'{x:.1f}'.replace('.', ',')
def vi(x, nd=2): return f'{x:.{nd}f}'.replace('.', ',')
def en(x, nd=2): return f'{x:.{nd}f}'
RES = lambda n: 100 / (2 ** n - 1)
ITEMS = [
 dict(m='m11', ch=7, n=21, page=443, ans_page=910, tid='latch', lv=2, printed='16.66 MHz', mismatch=False,
      qv='Bảng dữ liệu của một flip-flop ghi thời gian mức CAO tối thiểu của xung clock là 20 ns và thời gian mức THẤP tối thiểu là 40 ns. Tần số hoạt động tối đa là bao nhiêu?',
      qe='The datasheet of a certain flip-flop specified that the minimum HIGH time for the clock pulse is 20 ns and the minimum LOW time is 40 ns. What is the maximum operating frequency?',
      sv=f'Chu kỳ clock tối thiểu bằng thời gian mức CAO tối thiểu cộng thời gian mức THẤP tối thiểu: 20 ns + 40 ns = 60 ns. Vậy $f_{{max}}=1/T_{{min}}=1/60\\text{{ ns}}$ = {vi(f21 / 1e6)} MHz. Đáp án in ghi 16,66 MHz (cắt bớt chữ số, không làm tròn).',
      se=f'The minimum clock period is the minimum HIGH time plus the minimum LOW time: 20 ns + 40 ns = 60 ns. So $f_{{max}}=1/T_{{min}}=1/60\\text{{ ns}}$ = {en(f21 / 1e6)} MHz. The printed answer reads 16.66 MHz (truncated, not rounded).'),
 dict(m='m11', ch=7, n=23, page=443, ans_page=910, tid='latch', lv=2, printed='128 mA, 512 mW', mismatch=False,
      qv='Dòng một chiều mà một flip-flop làm việc với nguồn +4 V DC cần là 8 mA. Một thiết bị số dùng 16 flip-flop loại này. Xác định dung lượng dòng cần có của nguồn +4 V DC và công suất tiêu tán tổng của hệ thống.',
      qe='The direct current required by a particular flip-flop that operates on a +4 V dc source is found to be 8 mA. A certain digital device uses 16 of these flip-flops. Determine the current capacity required for the +4 V dc supply and the total power dissipation of the system.',
      sv=f'Dòng tổng = 16 × 8 mA = {i23 * 1e3:.0f} mA. Công suất tổng $P=V\\cdot I$ = 4 V × {i23 * 1e3:.0f} mA = {p23 * 1e3:.0f} mW. Khớp đáp án in (128 mA, 512 mW).',
      se=f'Total current = 16 × 8 mA = {i23 * 1e3:.0f} mA. Total power $P=V\\cdot I$ = 4 V × {i23 * 1e3:.0f} mA = {p23 * 1e3:.0f} mW. This agrees with the printed answer (128 mA, 512 mW).'),
 dict(m='m11', ch=7, n=27, page=444, ans_page=910, tid='timing', lv=2, printed='0.07 µs', mismatch=True,
      qv='Xác định độ rộng xung của mạch một nhịp 74121 nếu điện trở ngoài là 1 kΩ và tụ ngoài là 1 pF.', qe='Determine the pulse width of a 74121 one-shot if the external resistor is 1 kΩ and the external capacitor is 1 pF.',
      sv='Theo Floyd 7-5, độ rộng xung của 74121 là $t_W=0{,}7\\,R_{ext}C_{ext}$ = 0,7 × 1 kΩ × 1 pF = 0,7 ns. Đáp án in ghi 0,07 µs (70 ns): giá trị đó ứng với C = 100 pF (0,7 × 1 kΩ × 100 pF = 70 ns), gấp 100 lần 1 pF của đề. Đề in và đáp án in mâu thuẫn nhau; site giữ giá trị tính từ đề (0,7 ns) và ghi lại chênh lệch.',
      se='By Floyd 7-5 the pulse width of a 74121 is $t_W=0.7\\,R_{ext}C_{ext}$ = 0.7 × 1 kΩ × 1 pF = 0.7 ns. The printed answer reads 0.07 µs (70 ns): that value belongs to C = 100 pF (0.7 × 1 kΩ × 100 pF = 70 ns), 100 times the 1 pF of the statement. The printed statement and the printed answer contradict each other; the site keeps the value computed from the statement (0.7 ns) and records the difference.'),
 dict(m='m11', ch=7, n=29, page=444, ans_page=910, tid='timing', lv=3, printed='C1 = 1 µF, R1 = 454 kΩ (use 430 kΩ)', mismatch=False,
      qv='Tạo một mạch một nhịp dùng bộ định thời 555 cho xung ra rộng 0,5 s.', qe='Create a one-shot using a 555 timer that will produce a 0.5 s output pulse.',
      sv=f'Bộ 555 đơn ổn: $t_W=1{{,}}1\\,R_1C_1$. Chọn $C_1=1\\,\\mu$F thì $R_1=0{{,}}5\\text{{ s}}/(1{{,}}1\\times 1\\,\\mu\\text{{F}})$ = {r29 / 1e3:.1f} kΩ. Dùng điện trở chuẩn 430 kΩ cho $t_W$ = 1,1 × 430 kΩ × 1 µF = {vi(t29, 3)} s (xấp xỉ 0,5 s). Khớp đáp án in (C1 = 1 µF, R1 = 454 kΩ, dùng 430 kΩ); mạch: R1 nối Vcc với chân DISCH và THRESH, C1 nối chân THRESH xuống đất, xung kích vào chân TRIG (xem hình đáp án).'.replace('454.5', '454,5'),
      se=f'555 monostable: $t_W=1.1\\,R_1C_1$. Choosing $C_1=1\\,\\mu$F gives $R_1=0.5\\text{{ s}}/(1.1\\times 1\\,\\mu\\text{{F}})$ = {r29 / 1e3:.1f} kΩ. With the standard 430 kΩ resistor $t_W$ = 1.1 × 430 kΩ × 1 µF = {en(t29, 3)} s (about 0.5 s). This agrees with the printed answer (C1 = 1 µF, R1 = 454 kΩ, use 430 kΩ); circuit: R1 from Vcc to the DISCH and THRESH pins, C1 from THRESH to ground, trigger pulse on TRIG (see the answer figure).'),
 dict(m='m11', ch=7, n=31, page=445, ans_page=910, tid='timing', lv=3, printed='R1 = 9.1 kΩ, R2 = 4.3 kΩ', mismatch=True,
      qv='Xác định giá trị các điện trở ngoài của bộ định thời 555 dùng làm đa hài không ổn định có tần số ra 10 kHz, nếu tụ ngoài C là 0,004 µF và chu kỳ làm việc xấp xỉ 80 %.',
      qe='Determine the values of the external resistors for a 555 timer used as an astable multivibrator with an output frequency of 10 kHz, if the external capacitor C is 0.004 µF and the duty cycle is to be approximately 80%.',
      sv=f'Floyd 7-6: $f=\\dfrac{{1{{,}}44}}{{(R_1+2R_2)C}}$ và $D=\\dfrac{{R_1+R_2}}{{R_1+2R_2}}$. $R_1+2R_2=1{{,}}44/(10\\text{{ kHz}}\\times 0{{,}}004\\,\\mu\\text{{F}})$ = {s31 / 1e3:.0f} kΩ; $R_1+R_2=0{{,}}8\\times 36$ = {0.8 * s31 / 1e3:.1f} kΩ, nên $R_2$ = {r2_31 / 1e3:.1f} kΩ và $R_1$ = {r1_31 / 1e3:.1f} kΩ. Với giá trị chuẩn E24 $R_1$ = 22 kΩ, $R_2$ = 7,5 kΩ: $f$ = {vi(f31_e24 / 1e3)} kHz, $D$ = {vi(d31_e24 * 100, 1)} %. Đáp án in R1 = 9,1 kΩ, R2 = 4,3 kΩ cho $f$ = {vi(f31_pr / 1e3, 1)} kHz và $D$ = {vi(d31_pr * 100, 1)} % với C = 0,004 µF; chúng chỉ cho 10 kHz nếu C ≈ {vi(c31_pr * 1e6, 3)} µF. Đề in và đáp án in mâu thuẫn; site dùng giá trị tính từ đề.'.replace('7.2 kΩ', '7,2 kΩ').replace('28.8', '28,8').replace('21.6', '21,6'),
      se=f'Floyd 7-6: $f=\\dfrac{{1.44}}{{(R_1+2R_2)C}}$ and $D=\\dfrac{{R_1+R_2}}{{R_1+2R_2}}$. $R_1+2R_2=1.44/(10\\text{{ kHz}}\\times 0.004\\,\\mu\\text{{F}})$ = {s31 / 1e3:.0f} kΩ; $R_1+R_2=0.8\\times 36$ = {0.8 * s31 / 1e3:.1f} kΩ, so $R_2$ = {r2_31 / 1e3:.1f} kΩ and $R_1$ = {r1_31 / 1e3:.1f} kΩ. With standard E24 values $R_1$ = 22 kΩ, $R_2$ = 7.5 kΩ: $f$ = {en(f31_e24 / 1e3)} kHz, $D$ = {en(d31_e24 * 100, 1)} %. The printed answer R1 = 9.1 kΩ, R2 = 4.3 kΩ gives $f$ = {en(f31_pr / 1e3, 1)} kHz and $D$ = {en(d31_pr * 100, 1)} % with C = 0.004 µF; they give 10 kHz only if C ≈ {en(c31_pr * 1e6, 3)} µF. The printed statement and the printed answer contradict each other; the site uses the values computed from the statement.'),
 dict(m='m11', ch=8, n=25, page=492, ans_page=913, tid='shift', lv=1, printed='(a) 2 (b) 4 (c) 6 (d) 9', mismatch=False,
      qv='Cần bao nhiêu flip-flop để thực hiện mỗi bộ đếm Johnson sau: (a) modulus 4, (b) modulus 8, (c) modulus 12, (d) modulus 18?', qe='How many flip-flops are required to implement each of the following in a Johnson counter configuration: (a) modulus-4 (b) modulus-8 (c) modulus-12 (d) modulus-18?',
      sv='Bộ đếm Johnson có n flip-flop đi qua 2n trạng thái nên modulus = 2n và số flip-flop = modulus / 2: (a) 4/2 = 2, (b) 8/2 = 4, (c) 12/2 = 6, (d) 18/2 = 9. Khớp đáp án in.',
      se='A Johnson counter of n flip-flops steps through 2n states, so modulus = 2n and the number of flip-flops = modulus / 2: (a) 4/2 = 2, (b) 8/2 = 4, (c) 12/2 = 6, (d) 18/2 = 9. This agrees with the printed answer.'),
 dict(m='m11', ch=9, n=5, page=553, ans_page=914, first=4, tid='counter', lv=3, printed='Worst-case delay is 24 ns; it occurs when all flip-flops change state from 011 to 100 or from 111 to 000', mismatch=False,
      qv='Trong bộ đếm của Bài 4 (bộ đếm gợn sóng 3 bit, Hình 9–66), giả sử mỗi flip-flop có trễ lan truyền 8 ns từ sườn kích của xung clock đến lúc ngõ ra Q đổi. Xác định thời gian trễ xấu nhất (dài nhất) từ một xung clock đến khi bộ đếm tới một trạng thái nào đó. Chỉ rõ trạng thái hoặc các trạng thái có trễ xấu nhất này.',
      qe='In the counter of Problem 4, assume that each flip-flop has a propagation delay from the triggering edge of the clock to a change in the Q output of 8 ns. Determine the worst-case (longest) delay time from a clock pulse to the arrival of the counter in a given state. Specify the state or states for which this worst-case delay occurs.',
      sv='Trong bộ đếm gợn sóng, mỗi tầng chỉ đổi sau khi tầng trước đổi, nên thời gian ổn định của một lần chuyển bằng 8 ns nhân số thứ tự của tầng cao nhất bị đổi. Trường hợp xấu nhất là khi cả ba tầng cùng đổi: 011 → 100 và 111 → 000, tức 3 × 8 ns = 24 ns (đến trạng thái 100 và 000). Khớp đáp án in.',
      se='In a ripple counter each stage changes only after the previous one has changed, so the settling time of a transition is 8 ns times the position of the highest stage that toggles. The worst case is when all three stages change: 011 → 100 and 111 → 000, i.e. 3 × 8 ns = 24 ns (arriving at states 100 and 000). This agrees with the printed answer.'),
 dict(m='m11', ch=9, n=7, page=553, ans_page=914, tid='counter', lv=2, printed='8 ns', mismatch=False,
      qv='Nếu bộ đếm của Bài 5 là đồng bộ thay vì không đồng bộ thì thời gian trễ dài nhất là bao nhiêu?', qe='If the counter of Problem 5 were synchronous rather than asynchronous, what would be the longest delay time?',
      sv='Ở bộ đếm đồng bộ mọi flip-flop nhận clock cùng lúc nên các ngõ ra cùng đổi sau một trễ lan truyền: thời gian dài nhất chỉ là 8 ns (thay vì 24 ns). Khớp đáp án in.',
      se='In a synchronous counter all flip-flops receive the clock together, so the outputs change after a single propagation delay: the longest time is only 8 ns (instead of 24 ns). This agrees with the printed answer.'),
 dict(m='m10', ch=12, n=7, page=735, ans_page=921, tid='opamp', lv=1, printed='200', mismatch=False, sign_note=True,
      qv='Điện áp vào của một bộ khuếch đại đảo dùng op-amp là 5 mV và điện áp ra là 1 V. Độ lợi điện áp vòng kín là bao nhiêu?', qe='The input voltage to a certain op-amp inverting amplifier is 5 mV, and the output is 1 V. What is the closed-loop voltage gain?',
      sv='$|A_{cl}|=V_{out}/V_{in}$ = 1 V / 5 mV = 200. Bộ khuếch đại đảo đảo pha nên với ngõ vào +5 mV ngõ ra là −1 V và độ lợi có dấu là −200; đáp án in 200 là độ lớn (Bài 9 ngay sau đó in −33 có dấu). Khớp về độ lớn.',
      se='$|A_{cl}|=V_{out}/V_{in}$ = 1 V / 5 mV = 200. An inverting amplifier inverts the signal, so for a +5 mV input the output is −1 V and the signed gain is −200; the printed answer 200 is the magnitude (Problem 9 right after prints −33 with its sign). It agrees in magnitude.'),
 dict(m='m10', ch=12, n=9, page=735, ans_page=921, tid='opamp', lv=1, printed='-33', mismatch=False,
      qv='Độ lợi của bộ khuếch đại đảo dùng điện trở hồi tiếp 33 kΩ là bao nhiêu nếu điện trở ngõ vào là 1 kΩ?', qe='What is the gain of an inverting amplifier that uses a 33 kΩ feedback resistor if the input resistor is 1 kΩ?',
      sv='$A_{cl}=-R_f/R_i=-33\\text{ k}\\Omega/1\\text{ k}\\Omega=-33$. Khớp đáp án in (−33).', se='$A_{cl}=-R_f/R_i=-33\\text{ k}\\Omega/1\\text{ k}\\Omega=-33$. This agrees with the printed answer (−33).'),
 dict(m='m10', ch=12, n=19, page=737, ans_page=921, tid='specs', lv=2, printed='(a) 33.33% (b) 3.22% (c) 0.024%', mismatch=False,
      qv='Xác định độ phân giải, tính theo phần trăm, của mỗi DAC sau: (a) 2 bit (b) 5 bit (c) 12 bit.', qe='Determine the resolution expressed as a percentage, for each of the following DACs: (a) 2-bit (b) 5-bit (c) 12-bit.',
      sv=f'Độ phân giải theo phần trăm của DAC n bit là $\\dfrac{{1}}{{2^n-1}}\\times 100\\,\\%$: (a) 1/3 = {vi(RES(2))} %; (b) 1/31 = {vi(RES(5), 3)} % (làm tròn 3,23 %); (c) 1/4095 = {vi(RES(12), 4)} % (làm tròn 0,024 %). Khớp đáp án in (33,33 %, 3,22 %, 0,024 %); 3,22 % là số cắt bớt của 3,226 %.',
      se=f'The percentage resolution of an n-bit DAC is $\\dfrac{{1}}{{2^n-1}}\\times 100\\,\\%$: (a) 1/3 = {en(RES(2))} %; (b) 1/31 = {en(RES(5), 3)} % (rounded 3.23 %); (c) 1/4095 = {en(RES(12), 4)} % (rounded 0.024 %). This agrees with the printed answer (33.33 %, 3.22 %, 0.024 %); 3.22 % is 3.226 % truncated.'),
]
def main():
    out = {'m10': [], 'm11': []}; meta = []
    for it in ITEMS:
        ch, n = it['ch'], it['n']; qf = f'floyd_ex_ch{ch:02d}_q{n}.png'; af = f'floyd_ex_ch{ch:02d}_a{n}.png'
        qp = FC.question_png(ch, n, it['page'], os.path.join(FIG, qf), first=it.get('first')); ap = FC.answer_png(it['ans_page'], n, os.path.join(FIG, af))
        lab_v = f'Floyd Ch.{ch} · Problem {n}' + (' (đáp án in lệch đề, xem lời giải)' if it['mismatch'] else ''); lab_e = f'Floyd Ch.{ch} · Problem {n}' + (' (printed answer disagrees with the statement, see the solution)' if it['mismatch'] else '')
        d = dict(kind='ess', q=dict(vi=it['qv'], en=it['qe']), sol=dict(vi=it['sv'], en=it['se']), topic=dict(vi=TOP[it['tid']][0], en=TOP[it['tid']][1]), topic_id=it['tid'], level=it['lv'], origin='goc',
                 src=dict(vi=lab_v, en=lab_e), figs=['assets/figures/' + qf], afig='assets/figures/' + af)
        out[it['m']].append(d); meta.append(dict(m=it['m'], ch=ch, n=n, q_page=it['page'], ans_page=it['ans_page'], printed=it['printed'], mismatch=it['mismatch'], q_png=qf, a_png=af, first=it.get('first')))
    for mid, items in out.items():
        json.dump(items, open(os.path.join(ROOT, 'data', 'qsrc', f'{mid}_fex.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(meta, open(os.path.join(ROOT, 'data', 'verify', 'floyd_ex_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('floyd exercises:', {k: len(v) for k, v in out.items()}, '| printed answer disagrees with the statement:', [(m['ch'], m['n']) for m in meta if m['mismatch']])
NOTES = {
 'm11': dict(vi=['Floyd Chương 7 Problem 27: đề in 1 kΩ và 1 pF cho độ rộng xung 0,7 ns ($t_W=0{,}7RC$), nhưng đáp án in là 0,07 µs (70 ns), ứng với C = 100 pF. Site dùng giá trị tính từ đề và ghi chú chênh lệch.',
                'Floyd Chương 7 Problem 31: đề in C = 0,004 µF, 10 kHz, chu kỳ làm việc 80 % cho R1 = 21,6 kΩ và R2 = 7,2 kΩ; đáp án in R1 = 9,1 kΩ, R2 = 4,3 kΩ cho 20,3 kHz và 75,7 % (chỉ cho 10 kHz nếu C khoảng 0,008 µF). Site dùng giá trị tính từ đề.',
                'Floyd Chương 7 Problem 21: đáp án in 16,66 MHz là số cắt bớt của 16,67 MHz.'],
              en=['Floyd Chapter 7 Problem 27: the printed statement (1 kΩ and 1 pF) gives a pulse width of 0.7 ns ($t_W=0.7RC$) but the printed answer is 0.07 µs (70 ns), which belongs to C = 100 pF. The site uses the value computed from the statement and records the difference.',
                'Floyd Chapter 7 Problem 31: the printed statement (C = 0.004 µF, 10 kHz, 80 % duty cycle) gives R1 = 21.6 kΩ and R2 = 7.2 kΩ; the printed answer R1 = 9.1 kΩ, R2 = 4.3 kΩ gives 20.3 kHz and 75.7 % (10 kHz only if C is about 0.008 µF). The site uses the values computed from the statement.',
                'Floyd Chapter 7 Problem 21: the printed answer 16.66 MHz is the truncated value of 16.67 MHz.']),
 'm10': dict(vi=['Floyd Chương 12 Problem 19: đáp án in 3,22 % là số cắt bớt của 3,226 % (làm tròn 3,23 %).',
                'Floyd Chương 12 Problem 7: đáp án in 200 là độ lớn của độ lợi; bộ khuếch đại đảo có độ lợi −200 (Problem 9 ngay sau đó in −33 có dấu).',
                'Floyd Chương 12 Problem 27 (mục 12-5, ngoài phạm vi module 10 nên không có trong ngân hàng): đáp án in 18,75 triệu lệnh/s không khớp văn bản 12-5 (tám lệnh 32 bit mỗi chu kỳ ở 600 MHz là 4,8 tỉ lệnh/s); 18,75 triệu là 600 MHz chia 32.'],
              en=['Floyd Chapter 12 Problem 19: the printed answer 3.22 % is 3.226 % truncated (rounded 3.23 %).',
                'Floyd Chapter 12 Problem 7: the printed answer 200 is the magnitude of the gain; an inverting amplifier has a gain of −200 (Problem 9 right after prints −33 with its sign).',
                'Floyd Chapter 12 Problem 27 (section 12-5, outside module 10 so not in the bank): the printed answer 18.75 million instructions/s disagrees with the text of 12-5 (eight 32-bit instructions per clock cycle at 600 MHz is 4.8 billion instructions/s); 18.75 million is 600 MHz divided by 32.']),
}
def write_notes():
    for mid, nt in NOTES.items():
        fn = os.path.join(ROOT, 'data', 'verify', f'{mid}_notes.json'); d = json.load(open(fn, encoding='utf-8'))
        for lg in ('vi', 'en'):
            for x in nt[lg]:
                if x not in d[lg]: d[lg].append(x)
        json.dump(d, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if __name__ == '__main__': main(); write_notes()
