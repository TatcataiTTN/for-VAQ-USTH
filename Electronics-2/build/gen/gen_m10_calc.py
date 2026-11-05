"""Numeric items for module 10, modelled on worked examples of SERVOMECHANISM (sv).pdf (pp.14, 66-72)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'author'))
from _lib import *
G = Gen('m10_calc', 'SV', 20251010, dict(sv=('Servo loops and components', 'Vòng servo và linh kiện'), sy=('Synchro systems', 'Hệ synchro')))
g, fmt, add = G.g, G.fmt, G.add
def S(p): return (f'SERVOMECHANISM (sv) p.{p}', f'SERVOMECHANISM (sv) tr.{p}')
# velocity servo: equal summing resistors, motor K rpm per volt of error, tach t volt per rpm  ->  N = K|Vin| / (2 + K t)
for vin, K, t in [(9, 10, 0.1), (6, 10, 0.1), (12, 10, 0.1), (15, 10, 0.1), (9, 20, 0.05), (8, 5, 0.2), (10, 10, 0.1)]:
    n = K * vin / (2 + K * t); e = n / K
    add('sv', f'A velocity servo has equal summing resistors R2 = R3, a motor turning {K} rpm per volt of error and a tachometer giving {t} V per rpm. The control input is −{vin} V. What is the steady-state speed?', f'Servo vận tốc có R2 = R3, động cơ quay {K} vòng/phút cho mỗi volt sai số và máy phát tốc cho {t} V mỗi vòng/phút. Ngõ vào điều khiển là −{vin} V. Tốc độ ổn định là bao nhiêu?',
        fmt(n, 'rpm'), [fmt(K * vin, 'rpm'), fmt(K * vin / 2, 'rpm'), fmt(vin / t, 'rpm'), fmt(n * 2, 'rpm')], f'At balance N = K·e and e = (Vin − Vtach)/2 with Vtach = t·N, so N = K·Vin/(2 + K·t) = {K}×{vin}/(2 + {g(K*t)}) = {g(n)} rpm (error signal {g(e)} V). (Book example: −9 V, 10 rpm/V, 0.1 V/rpm → 30 rpm, error −3 V.)',
        f'Khi cân bằng N = K·e và e = (Vin − Vtach)/2 với Vtach = t·N nên N = K·Vin/(2 + K·t) = {K}×{vin}/(2 + {g(K*t)}) = {g(n)} vòng/phút (sai số {g(e)} V). (Ví dụ sách: −9 V, 10 vòng/phút/V, 0,1 V/vòng/phút → 30 vòng/phút, sai số −3 V.)', S(71), 3)
    if vin in (9, 6, 12):
        add('sv', f'In the same velocity servo (control −{vin} V, equal R2 = R3, {K} rpm/V motor, {t} V/rpm tachometer) what is the error signal at the very first instant, before the load moves?', f'Ở servo vận tốc đó (điều khiển −{vin} V, R2 = R3, động cơ {K} vòng/phút/V, máy phát tốc {t} V/vòng/phút), tín hiệu sai số ở thời điểm đầu tiên, trước khi tải chuyển động, là bao nhiêu?',
            fmt(-vin / 2, 'V'), [fmt(-vin, 'V'), fmt(0, 'V'), fmt(-vin / 3, 'V'), fmt(vin / 2, 'V')], f'The tach output is 0, so the sum point is (−{vin} + 0)/2 = {g(-vin/2)} V. (Book: −9 V → −4.5 V.)', f'Máy phát tốc bằng 0 nên điểm cộng là (−{vin} + 0)/2 = {g(-vin/2)} V. (Sách: −9 V → −4,5 V.)', S(71), 2)
for vin, vfb in [(10, 0), (8, -2), (-6, 2), (12, -4), (5, 5), (-10, 10)]:
    e = (vin + vfb) / 2
    add('sv', f'In a dc position servo with equal summing resistors R2 = R3, the input wiper gives {vin:+d} V and the feedback wiper gives {vfb:+d} V. What is the voltage at the sum point (error signal)?'.replace('+-', '−').replace('-', '−') if False else f'In a dc position servo with equal summing resistors R2 = R3, the input wiper gives {vin} V and the feedback wiper gives {vfb} V. What is the voltage at the sum point (error signal)?', f'Ở servo vị trí một chiều có R2 = R3, chổi ngõ vào cho {vin} V và chổi hồi tiếp cho {vfb} V. Điện áp tại điểm cộng (tín hiệu sai số) là bao nhiêu?',
        fmt(e, 'V'), [fmt(vin + vfb, 'V'), fmt(vin - vfb, 'V'), fmt((vin - vfb) / 2, 'V'), fmt(vin, 'V')], f'With equal resistors the sum point is the average: ({vin} + ({vfb}))/2 = {g(e)} V. The motor stops when it reaches 0 V, i.e. feedback = −input. (Book: +10 V and 0 V give +5 V.)', f'Với điện trở bằng nhau điểm cộng là trung bình: ({vin} + ({vfb}))/2 = {g(e)} V. Động cơ dừng khi về 0 V, tức hồi tiếp = −ngõ vào. (Sách: +10 V và 0 V cho +5 V.)', S(66), 2)
for vr in [115, 26, 90, 57.5, 230]:
    v = vr / 2.2
    add('sy', f'A synchro has a 2.2:1 step-down from the rotor to a single stator coil. With {vr} V on the rotor, what is the maximum voltage induced in one stator coil?', f'Synchro có tỉ số giảm 2,2:1 từ rôto xuống một cuộn stato. Với {vr} V trên rôto, điện áp cực đại cảm ứng trong một cuộn stato là bao nhiêu?', fmt(v, 'V'), [fmt(vr * 2.2, 'V'), fmt(vr / 2.2 / 2, 'V'), fmt(vr / 2.2 * math.sqrt(3), 'V'), fmt(vr, 'V')], f'V = {vr}/2.2 = {g(v)} V at maximum magnetic coupling. (Book: 115 V → 52 V.)', f'V = {vr}/2,2 = {g(v)} V khi ghép từ cực đại. (Sách: 115 V → 52 V.)', S(14), 2)
G.write()
