"""Generated questions for module 02 (origin bo_sung). Answers by formula; wrong options = typical mistakes. Seed fixed.
Run: python3 build/gen/gen_m02.py -> data/qsrc/m02_gen.json"""
import json, os, math, random
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rng = random.Random(20250217)
out, seen = [], set()
def B(en, vi=None): return dict(en=en, vi=vi if vi is not None else en)
TP = dict(mode=B('Input modes and CMRR','Chế độ ngõ vào và CMRR'), spec=B('Offset, bias and slew rate','Dòng/áp offset, dòng phân cực và slew rate'),
          fb=B('Negative feedback and gain','Hồi tiếp âm và hệ số khuếch đại'), imp=B('Impedances and compensation','Trở kháng và bù'),
          freq=B('Frequency response and bandwidth','Đáp ứng tần số và băng thông'), basic=B('Op-amp basics','Khái niệm op-amp'))
def g(x, d=3):
    x = float(f'{x:.{d}g}')
    return f'{x:,.0f}' if abs(x) >= 1e4 else f'{x:g}'
def fmt(x, unit, d=3):
    return f'{g(x, d)} {unit}'.strip()
def add(tp, qen, qvi, ans, wrongs, xen, xvi, src_en, src_vi, lvl=1, fixed=False):
    ws = []
    for w in wrongs:
        if w != ans and w not in ws: ws.append(w)
    if len(ws) < 3: return False
    k = (qen, ans)
    if k in seen: return False
    seen.add(k)
    opts = [ans] + rng.sample(ws, 3) if len(ws) > 3 else [ans] + ws[:3]
    rng.shuffle(opts)
    out.append(dict(kind='mcq', q=B(qen, qvi), opts=[B(o) for o in opts], correct=opts.index(ans), explain=B(xen, xvi), level=lvl, topic=TP[tp],
                    src=B(f'Generated – modelled on {src_en}', f'Bổ sung – sinh theo dạng {src_vi}'), origin='bo_sung', fixed_order=fixed, check='script'))
    return True
def dB(r): return 20 * math.log10(r)
S12, S8, S16 = ('Floyd Self-Test Q12', 'Floyd Self-Test câu 12'), ('Floyd Self-Test Q8', 'Floyd Self-Test câu 8'), ('Floyd Self-Test Q16', 'Floyd Self-Test câu 16')
# 1 CMRR in dB
for aol, acm in [(100000, 0.5), (200000, 2), (50000, 0.25), (150000, 1.5), (80000, 0.2), (250000, 0.05), (120000, 0.4), (300000, 0.6)]:
    r = aol / acm; a = dB(r)
    add('mode', f'An op-amp has Aol = {aol:,} and Acm = {acm}. What is the CMRR in decibels?', f'Một op-amp có Aol = {aol:,} và Acm = {acm}. CMRR là bao nhiêu dB?',
        f'{a:.1f} dB', [f'{10*math.log10(r):.1f} dB', f'{dB(acm/aol):.1f} dB', f'{dB(aol):.1f} dB', f'{a+20:.1f} dB', f'{a-20:.1f} dB'],
        f'CMRR = Aol/Acm = {r:,.0f}; CMRR(dB) = 20·log10({r:,.0f}) = {a:.1f} dB (10·log10 is the power formula; Acm/Aol inverts the ratio).',
        f'CMRR = Aol/Acm = {r:,.0f}; CMRR(dB) = 20·log10({r:,.0f}) = {a:.1f} dB (10·log10 là công thức công suất; Acm/Aol là đảo tỉ số).', *S8, 2)
# 2 CMRR dB -> Acm
for aol, cdb in [(100000, 100), (200000, 90), (50000, 80), (150000, 110), (90000, 94)]:
    r = 10 ** (cdb / 20); acm = aol / r
    add('mode', f'An op-amp has Aol = {aol:,} and CMRR = {cdb} dB. What is the common-mode gain Acm?', f'Một op-amp có Aol = {aol:,} và CMRR = {cdb} dB. Độ lợi chế độ chung Acm là bao nhiêu?',
        g(acm), [g(aol * r), g(acm * 10), g(acm / 10), g(aol / cdb), g(10 ** (cdb / 10) and aol / 10 ** (cdb / 10))],
        f'CMRR = 10^({cdb}/20) = {r:,.0f}; Acm = Aol/CMRR = {aol:,}/{r:,.0f} = {g(acm)}.', f'CMRR = 10^({cdb}/20) = {r:,.0f}; Acm = Aol/CMRR = {aol:,}/{r:,.0f} = {g(acm)}.', *S8, 2)
# 3 slew rate
for dv, dt in [(10, 5), (12, 8), (20, 10), (6, 4), (15, 25), (24, 16), (9, 3), (5, 20)]:
    sr = dv / dt
    add('spec', f'The output of an op-amp changes by {dv} V in {dt} μs. What is the slew rate?', f'Ngõ ra của một op-amp thay đổi {dv} V trong {dt} μs. Slew rate là bao nhiêu?',
        fmt(sr, 'V/μs'), [fmt(dt / dv, 'V/μs'), fmt(dv * dt, 'V/μs'), fmt(sr * 1000, 'V/μs'), fmt(sr / 2, 'V/μs')],
        f'SR = ΔV/Δt = {dv} V / {dt} μs = {g(sr)} V/μs.', f'SR = ΔV/Δt = {dv} V / {dt} μs = {g(sr)} V/μs.', *S12)
# 4 time from slew rate
for dv, sr in [(20, 0.5), (24, 2), (10, 0.8), (30, 1.5), (18, 0.9), (26, 13)]:
    t = dv / sr
    add('spec', f'How long does the output of an op-amp with a slew rate of {sr} V/μs take to change by {dv} V?', f'Op-amp có slew rate {sr} V/μs cần bao lâu để ngõ ra thay đổi {dv} V?',
        fmt(t, 'μs'), [fmt(dv * sr, 'μs'), fmt(sr / dv, 'μs'), fmt(t * 1000, 'μs'), fmt(t / 2, 'μs')], f'Δt = ΔV/SR = {dv}/{sr} = {g(t)} μs.', f'Δt = ΔV/SR = {dv}/{sr} = {g(t)} μs.', *S12)
# 5 offset / bias current
for i1, i2 in [(9.2, 8.8), (12.4, 11.6), (50, 47), (105, 98), (6.5, 6.1), (80, 75.5)]:
    ios = abs(i1 - i2); ib = (i1 + i2) / 2
    add('spec', f'The input currents of an op-amp are {i1} μA and {i2} μA. What is the input offset current?', f'Hai dòng vào của một op-amp là {i1} μA và {i2} μA. Dòng offset ngõ vào là bao nhiêu?',
        fmt(ios, 'μA'), [fmt(ib, 'μA'), fmt(i1 + i2, 'μA'), fmt(ios * 1000, 'μA'), fmt(i1 * i2, 'μA')], f'IOS = |I1 − I2| = |{i1} − {i2}| = {g(ios)} μA (the average {g(ib)} μA is the bias current).',
        f'IOS = |I1 − I2| = |{i1} − {i2}| = {g(ios)} μA (trung bình {g(ib)} μA là dòng phân cực).', 'Floyd Self-Test Q11', 'Floyd Self-Test câu 11')
    add('spec', f'The input currents of an op-amp are {i1} μA and {i2} μA. What is the bias current IBIAS?', f'Hai dòng vào của một op-amp là {i1} μA và {i2} μA. Dòng phân cực IBIAS là bao nhiêu?',
        fmt(ib, 'μA'), [fmt(ios, 'μA'), fmt(i1 + i2, 'μA'), fmt(max(i1, i2), 'μA'), fmt(ib * 2.0 + ios, 'μA')], f'IBIAS = (I1 + I2)/2 = ({i1} + {i2})/2 = {g(ib)} μA.', f'IBIAS = (I1 + I2)/2 = ({i1} + {i2})/2 = {g(ib)} μA.', 'Floyd Problem 7', 'Floyd Bài 7')
# 6 noninverting gain
for rf, ri in [(47, 4.7), (100, 2.2), (220, 3.3), (68, 1.0), (330, 10), (22, 1.0), (150, 3.0), (470, 10)]:
    a = 1 + rf / ri
    add('fb', f'A noninverting amplifier has Rf = {rf} kΩ and Ri = {ri} kΩ. What is the closed-loop gain?', f'Mạch không đảo có Rf = {rf} kΩ và Ri = {ri} kΩ. Độ lợi vòng kín là bao nhiêu?',
        g(a, 4), [g(rf / ri, 4), g(-rf / ri, 4), g(1 + ri / rf, 4), g(rf / ri + 2, 4)], f'Acl(NI) = 1 + Rf/Ri = 1 + {rf}/{ri} = {g(a,4)} (the “+1” is what distinguishes it from the inverting gain).',
        f'Acl(NI) = 1 + Rf/Ri = 1 + {rf}/{ri} = {g(a,4)} (số “+1” là điểm khác với độ lợi mạch đảo).', *S16)
# 7 inverting gain & output
for rf, ri, vin in [(100, 2.2, 20), (47, 1.0, 50), (220, 10, 100), (68, 4.7, 15), (330, 3.3, 8), (150, 10, 40)]:
    a = -rf / ri; vo = a * vin
    add('fb', f'An inverting amplifier has Rf = {rf} kΩ and Ri = {ri} kΩ. What is the output for Vin = {vin} mV?', f'Mạch đảo có Rf = {rf} kΩ và Ri = {ri} kΩ. Điện áp ra khi Vin = {vin} mV là bao nhiêu?',
        fmt(vo, 'mV'), [fmt(-vo, 'mV'), fmt((1 + rf / ri) * vin, 'mV'), fmt(-(1 + rf / ri) * vin, 'mV'), fmt(vin / abs(a), 'mV')], f'Acl(I) = −Rf/Ri = −{rf}/{ri} = {g(a)}; Vout = Acl·Vin = {g(a)} × {vin} mV = {g(vo)} mV (inverted).',
        f'Acl(I) = −Rf/Ri = −{rf}/{ri} = {g(a)}; Vout = Acl·Vin = {g(a)} × {vin} mV = {g(vo)} mV (đảo pha).', 'Floyd Problem 15 / Fig. 12–22', 'Floyd Bài 15 / Hình 12–22', 2)
# 8 feedback attenuation
for rf, ri in [(100, 4.7), (47, 1.0), (220, 3.3), (68, 10), (330, 2.2), (150, 15)]:
    b = ri / (ri + rf)
    add('fb', f'A noninverting amplifier has Rf = {rf} kΩ and Ri = {ri} kΩ. What is the feedback fraction B?', f'Mạch không đảo có Rf = {rf} kΩ và Ri = {ri} kΩ. Hệ số hồi tiếp B là bao nhiêu?',
        g(b, 3), [g(rf / (ri + rf), 3), g(ri / rf, 3), g(1 / b, 3), g(rf / ri, 3)], f'B = Ri/(Ri + Rf) = {ri}/({ri}+{rf}) = {g(b)}; it is the reciprocal of the ideal gain 1/Acl.', f'B = Ri/(Ri + Rf) = {ri}/({ri}+{rf}) = {g(b)}; nó là nghịch đảo của độ lợi lý tưởng 1/Acl.', 'Floyd Problem 12', 'Floyd Bài 12', 2)
# 9 Rf for gain
for acl, ri, inv in [(50, 1.0, False), (100, 2.2, False), (25, 10, True), (75, 2.2, True), (12, 4.7, False), (150, 1.0, True), (8, 12, False), (60, 3.3, True)]:
    rf = (acl - 1) * ri if not inv else acl * ri
    wrong = [acl * ri if not inv else (acl - 1) * ri, acl / ri, rf * 10, rf / 10]
    add('fb', f'Find Rf for a {"inverting" if inv else "noninverting"} amplifier with Ri = {ri} kΩ and |Acl| = {acl}.', f'Tìm Rf cho mạch {"đảo" if inv else "không đảo"} có Ri = {ri} kΩ và |Acl| = {acl}.',
        fmt(rf, 'kΩ'), [fmt(w, 'kΩ') for w in wrong], f'{"Rf = |Acl|·Ri" if inv else "Rf = (Acl − 1)·Ri"} = {g(rf)} kΩ.', f'{"Rf = |Acl|·Ri" if inv else "Rf = (Acl − 1)·Ri"} = {g(rf)} kΩ.', 'Floyd Problem 15', 'Floyd Bài 15', 2)
# 10 closed-loop bandwidth
for ft, acl in [(1e6, 10), (5e6, 50), (3e6, 100), (10e6, 20), (1.5e6, 25), (8e6, 40)]:
    bw = ft / acl
    f_ = lambda x: f'{x/1e3:,.0f} kHz' if x < 1e6 else f'{x/1e6:g} MHz'
    add('freq', f'An op-amp has a unity-gain frequency of {ft/1e6:g} MHz. What is the closed-loop bandwidth when Acl = {acl}?', f'Op-amp có tần số độ lợi đơn vị {ft/1e6:g} MHz. Băng thông vòng kín khi Acl = {acl} là bao nhiêu?',
        f_(bw), [f_(ft * acl), f_(ft / (acl + 1)), f_(ft), f_(bw / 10)], f'BWcl = fT/Acl = {ft/1e6:g} MHz / {acl} = {f_(bw)}.', f'BWcl = fT/Acl = {ft/1e6:g} MHz / {acl} = {f_(bw)}.', 'Floyd Self-Test Q30', 'Floyd Self-Test câu 30', 2)
# 11 closed-loop gain at given fc(ol)
for aol_db, fol, fcl in [(100, 10, 1e4), (89, 750, 5500), (106, 5, 5e4), (94, 20, 2e4)]:
    aol = 10 ** (aol_db / 20); k = fcl / fol; acl = aol / k
    add('freq', f'Aol = {aol_db} dB, fc(ol) = {fol} Hz and fc(cl) = {fcl:,.0f} Hz. What is the closed-loop gain in dB?', f'Aol = {aol_db} dB, fc(ol) = {fol} Hz và fc(cl) = {fcl:,.0f} Hz. Độ lợi vòng kín là bao nhiêu dB?',
        f'{dB(acl):.1f} dB', [f'{aol_db - dB(k)+dB(k):.1f} dB' if False else f'{aol_db - 20:.1f} dB', f'{dB(k):.1f} dB', f'{aol_db + dB(k):.1f} dB', f'{dB(acl)+6:.1f} dB'],
        f'1 + B·Aol = fc(cl)/fc(ol) = {k:g}; Acl = Aol/{k:g} = {acl:,.0f} → {dB(acl):.1f} dB (i.e. Aol(dB) − 20·log10 {k:g}).', f'1 + B·Aol = fc(cl)/fc(ol) = {k:g}; Acl = Aol/{k:g} = {acl:,.0f} → {dB(acl):.1f} dB (tức Aol(dB) − 20·log10 {k:g}).', 'Floyd Problem 37', 'Floyd Bài 37', 3)
# 12 RC lag
for fcr, f_ in [(1000, 1000), (2000, 4000), (5000, 2500), (8500, 17000), (12000, 3000), (10000, 100000)]:
    r = f_ / fcr; att = 1 / math.sqrt(1 + r * r); ph = -math.degrees(math.atan(r))
    add('freq', f'An RC lag circuit has fc = {fcr:,} Hz. What is the phase shift at {f_:,} Hz?', f'Mạch trễ RC có fc = {fcr:,} Hz. Độ lệch pha tại {f_:,} Hz là bao nhiêu?',
        f'{ph:.1f}°', [f'{-ph:.1f}°', f'{-math.degrees(math.atan(1/r)):.1f}°', f'{-math.degrees(math.atan(r))/2:.1f}°', f'{-90 if abs(ph)<89 else -45:.1f}°'],
        f'θ = −tan⁻¹(f/fc) = −tan⁻¹({r:g}) = {ph:.1f}° (the lag is negative; f = fc gives −45°).', f'θ = −tan⁻¹(f/fc) = −tan⁻¹({r:g}) = {ph:.1f}° (độ trễ mang dấu âm; f = fc cho −45°).', 'Floyd Problem 31–32', 'Floyd Bài 31–32', 2)
    add('freq', f'An RC lag circuit has fc = {fcr:,} Hz. What is Vout/Vin at {f_:,} Hz?', f'Mạch trễ RC có fc = {fcr:,} Hz. Tỉ số Vout/Vin tại {f_:,} Hz là bao nhiêu?',
        f'{att:.3f}', [f'{1/(1+r*r):.3f}', f'{math.sqrt(1+r*r):.3f}', f'{1/(1+r):.3f}', f'{0.707:.3f}'], f'Vout/Vin = 1/√(1 + (f/fc)²) = 1/√(1 + {r:g}²) = {att:.3f}.', f'Vout/Vin = 1/√(1 + (f/fc)²) = 1/√(1 + {r:g}²) = {att:.3f}.', 'Floyd Problem 29', 'Floyd Bài 29', 2)
# 13 noninverting impedances
for aol, zin, zout, rf, ri in [(100000, 2e6, 75, 100, 1.0), (200000, 1e6, 60, 47, 4.7), (150000, 5e6, 100, 220, 3.3)]:
    b = ri / (ri + rf); k = 1 + b * aol; zi = k * zin; zo = zout / k
    add('imp', f'A noninverting amplifier uses an op-amp with Aol = {aol:,}, Zin = {zin/1e6:g} MΩ and Zout = {zout} Ω; Rf = {rf} kΩ, Ri = {ri} kΩ. What is Zin(NI)?', f'Mạch không đảo dùng op-amp có Aol = {aol:,}, Zin = {zin/1e6:g} MΩ, Zout = {zout} Ω; Rf = {rf} kΩ, Ri = {ri} kΩ. Zin(NI) là bao nhiêu?',
        f'{g(zi/1e9)} GΩ', [f'{g(zin*(1+aol)/1e9)} GΩ', f'{g(zin/k/1e9)} GΩ', f'{g(zin/1e9)} GΩ', f'{g(zin*b/1e9)} GΩ'], f'B = {ri}/({ri}+{rf}) = {b:.5f}; 1 + B·Aol = {k:,.1f}; Zin(NI) = (1 + B·Aol)·Zin = {g(zi/1e9)} GΩ.', f'B = {ri}/({ri}+{rf}) = {b:.5f}; 1 + B·Aol = {k:,.1f}; Zin(NI) = (1 + B·Aol)·Zin = {g(zi/1e9)} GΩ.', 'Floyd Problem 19', 'Floyd Bài 19', 3)
    add('imp', f'Same amplifier (Aol = {aol:,}, Zout = {zout} Ω, Rf = {rf} kΩ, Ri = {ri} kΩ). What is Zout(NI)?', f'Cùng mạch (Aol = {aol:,}, Zout = {zout} Ω, Rf = {rf} kΩ, Ri = {ri} kΩ). Zout(NI) là bao nhiêu?',
        f'{g(zo*1e3)} mΩ', [f'{g(zout*k*1e3)} mΩ', f'{g(zout/(1+aol)*1e3)} mΩ', f'{g(zout*1e3)} mΩ', f'{g(zo*1e3*10)} mΩ'], f'Zout(NI) = Zout/(1 + B·Aol) = {zout}/{k:,.1f} = {g(zo*1e3)} mΩ.', f'Zout(NI) = Zout/(1 + B·Aol) = {zout}/{k:,.1f} = {g(zo*1e3)} mΩ.', 'Floyd Problem 19', 'Floyd Bài 19', 3)
# 14 dB <-> ratio
for db in [40, 60, 80, 100, 106, 120]:
    r = 10 ** (db / 20)
    add('basic', f'An op-amp has a midrange open-loop gain of {db} dB. What is the gain as a plain ratio?', f'Op-amp có độ lợi vòng hở vùng giữa {db} dB. Giá trị tỉ số tương ứng là bao nhiêu?',
        g(r, 3), [g(10 ** (db / 10), 3), g(db * 10, 3), g(db / 20, 3), g(r * 10, 3)], f'Aol = 10^({db}/20) = {g(r)} (20·log is for voltage ratios).', f'Aol = 10^({db}/20) = {g(r)} (20·log dùng cho tỉ số điện áp).', 'Floyd Self-Test Q10', 'Floyd Self-Test câu 10', 2)
# 15 conceptual variants (bilingual, fixed order False)
C = [
 ('fb','The closed-loop gain of an inverting amplifier is set mainly by','Độ lợi vòng kín của mạch khuếch đại đảo chủ yếu được quyết định bởi',('the ratio of two external resistors','tỉ số hai điện trở ngoài'),[('the open-loop gain of the op-amp','độ lợi vòng hở của op-amp'),('the supply voltage','điện áp nguồn cấp'),('the slew rate','slew rate')],'With a large Aol, Acl ≈ −Rf/Ri, set by external components.','Với Aol lớn, Acl ≈ −Rf/Ri do linh kiện ngoài quyết định.'),
 ('fb','The inverting input of an op-amp in a negative-feedback amplifier is at approximately the same voltage as the noninverting input. This is called','Ở mạch khuếch đại hồi tiếp âm, ngõ vào đảo có điện áp xấp xỉ ngõ vào không đảo. Hiện tượng này gọi là',('a virtual short (virtual ground when Vin+ = 0)','đoản mạch ảo (đất ảo khi Vin+ = 0)'),[('common-mode rejection','triệt tín hiệu chung'),('slew-rate limiting','giới hạn slew rate'),('offset nulling','chỉnh null offset')],'High Aol forces the differential input to ≈ 0 V.','Aol lớn buộc điện áp vi sai ngõ vào ≈ 0 V.'),
 ('mode','A large CMRR means the op-amp','CMRR lớn nghĩa là op-amp',('amplifies the difference signal far more than the common signal','khuếch đại tín hiệu hiệu lớn hơn nhiều so với tín hiệu chung'),[('amplifies noise common to both inputs','khuếch đại nhiễu chung ở hai ngõ vào'),('has a low open-loop gain','có độ lợi vòng hở thấp'),('has a small bandwidth','có băng thông nhỏ')],'CMRR = Aol/Acm; larger means better rejection of common-mode noise.','CMRR = Aol/Acm; càng lớn thì triệt nhiễu chung càng tốt.'),
 ('spec','If an op-amp output cannot follow a fast input step, the limiting parameter is','Khi ngõ ra op-amp không theo kịp bước nhảy nhanh ở ngõ vào, tham số giới hạn là',('slew rate','slew rate'),[('CMRR','CMRR'),('input offset current','dòng offset ngõ vào'),('output impedance','trở kháng ra')],'Slew rate limits the maximum dV/dt of the output.','Slew rate giới hạn dV/dt cực đại của ngõ ra.'),
 ('imp','In a noninverting amplifier with negative feedback, the output impedance','Ở mạch không đảo có hồi tiếp âm, trở kháng ra',('decreases','giảm'),[('increases','tăng'),('is unchanged','không đổi'),('becomes infinite','trở thành vô cùng')],'Zout(NI) = Zout/(1 + B·Aol), far below the open-loop Zout.','Zout(NI) = Zout/(1 + B·Aol), nhỏ hơn nhiều Zout vòng hở.'),
 ('imp','In a voltage-follower, the input impedance is','Ở mạch lặp điện áp, trở kháng vào',('extremely high','cực kỳ cao'),[('equal to Ri','bằng Ri'),('very low','rất thấp'),('equal to Rf','bằng Rf')],'Zin(VF) = (1 + Aol)·Zin, which is enormous.','Zin(VF) = (1 + Aol)·Zin, rất lớn.'),
 ('freq','The unity-gain frequency of an op-amp is the frequency where','Tần số độ lợi đơn vị của op-amp là tần số tại đó',('the open-loop gain falls to 1 (0 dB)','độ lợi vòng hở giảm xuống 1 (0 dB)'),[('the gain falls by 3 dB','độ lợi giảm 3 dB'),('the phase shift is 0°','độ lệch pha bằng 0°'),('the output saturates','ngõ ra bão hòa')],'fT is where |Aol| = 1.','fT là điểm có |Aol| = 1.'),
 ('freq','Above the critical frequency, a single-pole compensated op-amp gain falls at','Phía trên tần số tới hạn, độ lợi của op-amp bù một cực suy giảm với tốc độ',('20 dB per decade','20 dB mỗi decade'),[('3 dB per decade','3 dB mỗi decade'),('40 dB per decade','40 dB mỗi decade'),('it stays constant','giữ nguyên')],'One RC lag stage gives −20 dB/decade (−6 dB/octave).','Một tầng trễ RC cho −20 dB/decade (−6 dB/octave).'),
 ('freq','The phase shift of an RC lag circuit at its critical frequency is','Độ lệch pha của mạch trễ RC tại tần số tới hạn là',('−45°','−45°'),[('0°','0°'),('−90°','−90°'),('−180°','−180°')],'θ = −tan⁻¹(1) = −45° at f = fc.','θ = −tan⁻¹(1) = −45° tại f = fc.'),
 ('spec','The purpose of a compensating resistor at the noninverting input of an inverting amplifier is to','Điện trở bù ở ngõ vào không đảo của mạch đảo dùng để',('cancel the output error caused by the bias currents','triệt sai số ngõ ra do dòng phân cực'),[('increase the voltage gain','tăng độ lợi điện áp'),('increase the bandwidth','tăng băng thông'),('reduce the slew rate','giảm slew rate')],'Rc = Ri‖Rf makes both bias-current voltage drops equal.','Rc = Ri‖Rf làm hai sụt áp do dòng phân cực bằng nhau.'),
 ('basic','Which input of an op-amp is marked “+”?','Ngõ vào nào của op-amp được ký hiệu “+”?',('the noninverting input','ngõ vào không đảo'),[('the inverting input','ngõ vào đảo'),('the output','ngõ ra'),('the supply input','chân nguồn')],'A signal at “+” appears at the output in phase.','Tín hiệu ở “+” xuất hiện ở ngõ ra cùng pha.'),
 ('fb','An op-amp circuit has Rf open and Vin applied. The output most likely','Mạch op-amp bị hở Rf và có tín hiệu Vin. Ngõ ra nhiều khả năng',('saturates at a supply rail','bão hòa ở mức nguồn'),[('equals Vin','bằng Vin'),('is exactly zero','bằng đúng không'),('becomes a pure sine of unity gain','trở thành sin với độ lợi bằng 1')],'No feedback → open-loop gain → tiny inputs drive the output to the rail.','Không hồi tiếp → độ lợi vòng hở → tín hiệu nhỏ cũng đẩy ngõ ra tới mức nguồn.'),
 ('fb','The voltage-follower is mainly used as','Mạch lặp điện áp chủ yếu dùng làm',('a buffer isolating a high-impedance source from a load','mạch đệm cách ly nguồn trở kháng cao với tải'),[('a high-gain amplifier','bộ khuếch đại độ lợi cao'),('a phase inverter','mạch đảo pha'),('an oscillator','mạch dao động')],'Gain 1, very high Zin and very low Zout make an ideal buffer.','Độ lợi 1, Zin rất cao, Zout rất thấp tạo nên mạch đệm lý tưởng.'),
 ('mode','If the same 5 mV signal is applied to both inputs of an ideal op-amp, the output is','Nếu cùng tín hiệu 5 mV đặt vào cả hai ngõ vào của op-amp lý tưởng, ngõ ra là',('0 V','0 V'),[('5 mV','5 mV'),('10 mV','10 mV'),('the supply voltage','điện áp nguồn')],'The differential input is 0 V, so the ideal output is 0 V.','Điện áp vi sai ngõ vào bằng 0 nên ngõ ra lý tưởng bằng 0 V.'),
]
for tp, qe, qv, ca, ws, xe, xv in C:
    k = (qe, ca[0])
    if k in seen: continue
    seen.add(k); opts = [ca] + ws; rng.shuffle(opts)
    out.append(dict(kind='mcq', q=B(qe, qv), opts=[B(*o) for o in opts], correct=opts.index(ca), explain=B(xe, xv), level=1, topic=TP[tp],
                    src=B('Generated – conceptual variant of Floyd Ch.12 Self-Test', 'Bổ sung – dạng khái niệm theo Floyd Ch.12 Self-Test'), origin='bo_sung', fixed_order=False, check='chapter text'))
p = os.path.join(ROOT, 'data', 'qsrc', 'm02_gen.json'); json.dump(out, open(p + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(p + '.tmp', p)
print('generated', len(out))
