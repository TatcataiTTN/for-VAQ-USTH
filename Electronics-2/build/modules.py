"""Single source of truth: module list + syllabus/textbook mapping (vi/en).
Page numbers: printed page numbers of each book (pdf page = printed + offset, see MAPPING.md)."""
COURSE = dict(code='AE2.025', vi='Điện tử học 2', en='Electronics 2', ects=4,
              hours=dict(lecture=30, tutorial=9, lab=24, total=63), prereq='AE1.033 Electronics 1')

BOOKS = {
    'floyd': dict(short='Floyd 9e', full='Thomas L. Floyd, Electronic Devices (Conventional Current Version), 9th ed., Pearson, 2012',
                  drive='1xGL7Uz9RKUBCTEKeVOGnU7dJ_1XDMLWy', syllabus_ref=1),
    'jaeger5': dict(short='Jaeger 5e', full='R. C. Jaeger & T. N. Blalock, Microelectronic Circuit Design, 5th ed., McGraw-Hill, 2015',
                    drive='1vGDNKiWdPEWMGyCj_tAwQPVkFPPJFf0I', syllabus_ref=2),
    'jaeger6': dict(short='Jaeger 6e', full='R. C. Jaeger & T. N. Blalock, Microelectronic Circuit Design, 6th ed., McGraw-Hill (analog-only edition)',
                    drive='19KKl2YHyI7i3kvqGhCtqdj-ZUQwPQf47', syllabus_ref=2),
    'easa': dict(short='EASA M04', full='Module 04 Electronic Fundamentals (B2), Aviation Maintenance Technician Certification Series, Aircraft Technical Book Co.',
                 drive='1OJQ8lNWcW95c4eC5-PVAMPvTILptRVcF', syllabus_ref=3),
}

# id, slug, vi title, en title, EASA item, textbook sections, CLO
MODS = [
    dict(id='m01', slug='01-ic-logic', vi='Vi mạch tích hợp và mạch logic', en='Integrated circuits and logic circuits',
         easa='4.1.3 (a)(b) logic circuits', clo='CLO1, CLO2',
         src=['Jaeger 5e Ch.6 §6.1–6.4, 6.11 · Ch.7 §7.1–7.5 · Ch.9 §9.2, 9.12–9.15', 'EASA M04 sub-module 01 (IC section)']),
    dict(id='m02', slug='02-op-amp', vi='Bộ khuếch đại thuật toán (op-amp)', en='The operational amplifier',
         easa='4.1.3 (a) linear circuits / op-amps', clo='CLO1, CLO2, CLO3',
         src=['Floyd 9e Ch.12', 'Jaeger 5e Ch.10 §10.5–10.9 · Ch.11 §11.2, 11.11–11.13']),
    dict(id='m03', slug='03-op-amp-circuits', vi='Mạch op-amp cơ bản: so sánh, cộng, tích phân, vi phân, đệm', en='Basic op-amp circuits: comparator, summer, integrator, differentiator, follower',
         easa='4.1.3 (b) integrator, differentiator, voltage follower, comparator', clo='CLO2, CLO3',
         src=['Floyd 9e Ch.13', 'Jaeger 5e Ch.10 §10.9–10.10 · Ch.12 §12.8–12.9']),
    dict(id='m04', slug='04-coupling-feedback', vi='Ghép tầng khuếch đại và hồi tiếp dương/âm', en='Amplifier stage coupling and positive/negative feedback',
         easa='4.1.3 (b) coupling methods; positive & negative feedback', clo='CLO1, CLO2',
         src=['Floyd 9e §6–6 Multistage, §7–2 Push-pull, §12–3 Negative feedback', 'Jaeger 5e Ch.11 §11.1, 11.10 · Ch.12 §12.1', 'EASA M04 sub-module 01 (amplifier coupling)']),
    dict(id='m05', slug='05-special-op-amps', vi='Mạch op-amp chuyên dụng và chuyển đổi A/D–D/A', en='Special-purpose op-amp circuits and A/D–D/A conversion',
         easa='4.1.3 linear ICs (extension)', clo='CLO2, CLO3',
         src=['Floyd 9e Ch.14', 'Jaeger 5e Ch.12 §12.2, 12.5–12.6']),
    dict(id='m06', slug='06-active-filters', vi='Bộ lọc tích cực', en='Active filters',
         easa='4.1.3 linear ICs (extension)', clo='CLO2, CLO3',
         src=['Floyd 9e Ch.15', 'Jaeger 5e Ch.12 §12.3']),
    dict(id='m07', slug='07-oscillators-555', vi='Mạch dao động và IC định thời 555', en='Oscillators and the 555 timer',
         easa='4.1.3 (b) positive feedback', clo='CLO2, CLO3, CLO4',
         src=['Floyd 9e Ch.16', 'Jaeger 5e Ch.12 §12.7, 12.9']),
    dict(id='m08', slug='08-ic-regulators', vi='Ổn áp và IC ổn áp', en='Voltage regulators and IC regulators',
         easa='4.1.3 linear ICs (extension)', clo='CLO1, CLO3',
         src=['Floyd 9e Ch.17']),
    dict(id='m09', slug='09-pcb', vi='Bảng mạch in (PCB)', en='Printed circuit boards (PCB)',
         easa='4.2 Printed circuit boards', clo='CLO1, CLO4',
         src=['EASA M04 sub-module 02', 'Floyd 9e Application Activities (circuit-board layout)']),
    dict(id='m10', slug='10-servomechanisms', vi='Hệ servo, synchro và điều khiển động cơ servo', en='Servomechanisms, synchros and servomotor control',
         easa='4.3 Servomechanisms', clo='CLO1, CLO4',
         src=['EASA M04 sub-module 03', 'Floyd 9e §16–6 (555 PWM) for the servomotor lab']),
]
BYID = {m['id']: m for m in MODS}
