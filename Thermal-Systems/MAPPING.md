# MAPPING.md — bản đồ nội dung sách ↔ module AE2.013 (P2)

Sinh tự động bởi `build/bookmap/build_map.py` từ `data/bookmap/*.json`; kiểm bằng `build/verify/verify_bookmap.py` (FAILS: none). Vai trò: **core** = bài giảng/câu hỏi lấy từ đây; **ref** = đọc thêm; **background** = nền AE1.030; **optional** = phần phụ; mục không có vai trò nào với module = ngoài phạm vi (`out`). Cơ sở từng mục nằm trong JSON (`mods[module].basis`).

## Bảng offset trang in ↔ trang PDF

| Sách | Quy tắc | Đo bằng | Ghi chú |
|---|---|---|---|
| Cengel & Boles 5e (PDF 963 tr.) | trang in = PDF − 26 (PDF 27–907) | 349 trang đọc được số in, đều = 26; 7 mốc: PDF 44=18, 183=157, 337=311, 488=462, 623=597, 763=737, 907=881; 10 tiêu đề mục kiểm bằng ảnh | Glossary PDF 909–963 đánh số riêng: in = PDF − 908. PDF 1–26 (Contents, Preface) không dùng số in. PDF dừng ở tr.907 (in 881) giữa phần FE của Ch.17 |
| Farokhi 2e (PDF 1048 tr.) | trang in = PDF − 34 (PDF 36–1031) | 962 trang đều = 34; 7 mốc: PDF 36=2, 199=165, 364=330, 526=492, 689=655, 853=819, 1031=997 | Chương 1 mở ở PDF 35 = in 1 |
| El-Sayed 2e (EPUB) | không có PDF: trang in lấy từ `epub:type="pagebreak"` = dấu `⟦p.N⟧` trong `OCR_output/11_*.md` | 230/230 mục trong phạm vi khớp giữa `toc.ncx` + span pagebreak của xhtml | số trang La Mã ở phần đầu; Ch.1 3–74, Ch.2 75–134, Ch.4 203–288, Ch.9 679–738, Ch.10 739–780, Ch.11 781–838 |

## Module × nguồn

### m01 — Giới thiệu, nguyên lý đẩy và phân loại động cơ

Slide: ch1 tr.5–48. Tiêu đề slide: xem `data/bookmap/slides.json`.

**Cengel & Boles**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 1–1 | Thermodynamics and Energy | background | 2–2 | 28–28 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–2 | Importance of Dimensions and Units | background | 3–9 | 29–35 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–3 | Systems and Control Volumes | background | 10–11 | 36–37 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–4 | Properties of a System | background | 12–12 | 38–38 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–5 | Density and Specific Gravity | background | 13–13 | 39–39 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–6 | State and Equilibrium | background | 14–14 | 40–40 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–7 | Processes and Cycles | background | 15–16 | 41–42 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–8 | Temperature and the Zeroth Law of Thermodynamics | background | 17–20 | 43–46 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–9 | Pressure | background | 21–25 | 47–51 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–10 | The Manometer | background | 26–28 | 52–54 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–11 | The Barometer and Atmospheric Pressure | background | 29–32 | 55–58 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 1–12 | Problem-Solving Technique | background | 33–38 | 59–64 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–1 | Introduction | background | 52–52 | 78–78 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–2 | Forms of Energy | background | 53–59 | 79–85 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–3 | Energy Transfer by Heat | background | 60–61 | 86–87 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–4 | Energy Transfer by Work | background | 62–65 | 88–91 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–5 | Mechanical Forms of Work | background | 66–69 | 92–95 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–6 | The First Law of Thermodynamics | background | 70–77 | 96–103 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–7 | Energy Conversion Efficiencies | background | 78–85 | 104–111 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 2–8 | Energy and Environment | background | 86–91 | 112–117 | AE1.030 review (modules.py: Cengel Ch.1–2) |
| 9–11 | Ideal Jet-Propulsion Cycles | ref | 521–526 | 547–552 | slide Ch.1 tr.17–42 Jet propulsion engines |

**Farokhi**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 1 | Introduction | ref | 1 | 35–54 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.1 | History of the Airbreathing Jet Engine, a Twentieth-Century Invention—The Beginning | ref | 1 | 35–37 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.2 | Innovations in Aircraft Gas Turbine Engines | ref | 4 | 38–43 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.3 | New Engine Concepts | ref | 10 | 44–49 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.4 | New Vehicles | ref | 16 | 50–50 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.5 | Summary | ref | 16 | 50–51 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| 1.6 | Roadmap for the Second Edition | ref | 18 | 52–52 | slide Ch.1 tr.5–48; Farokhi Ch.1 is history/innovations (modules.py: Ch.1) |
| Ch.1 | References | ref | 19 | 53–53 | end-of-chapter References of an assigned chapter |
| Ch.1 | Problems | ref | 20 | 54–54 | end-of-chapter Problems of an assigned chapter |
| 3.1 | Introduction | core | 113 | 147–152 | slide Ch.1 tr.7–10 Role of the engine, Principles of propulsion |
| 3.2 | Installed Thrust—Some Bookkeeping Issues on Thrust and Drag | ref | 119 | 153–157 | installed thrust: deeper than the slides |
| 3.3 | Engine Thrust Based on the Sum of Component Impulse | core | 124 | 158–161 | thrust from momentum (slide Ch.1 tr.8–10 Principles of propulsion) |
| 3.4 | Rocket Thrust | ref | 128 | 162–162 | rocket thrust: slide Ch.1 tr.14 non-airbreathing engines |
| 3.5 | Airbreathing Engine Performance Parameters | core | 129 | 163–173 | performance parameters (specific thrust, TSFC, efficiencies): slide Ch.1 tr.46–47 Definitions |
| 3.6 | Modern Engines, Their Architecture and Some Performance Characteristics | ref | 140 | 174–176 | modern engines: slide Ch.1 tr.48 |
| 3.7 | Summary | ref | 143 | 177–177 | summary |
| Ch.3 | References | ref | 144 | 178–178 | end-of-chapter References of an assigned chapter |
| Ch.3 | Problems | core | 144 | 178–184 | end-of-chapter Problems of an assigned chapter |
| App.K | 10-Minute Quiz | optional | 973 | 1007–1024 | 10-minute quiz: no answers printed; per-quiz module not assigned (? to be done in P3) |
| App.L | Some “Rules of Thumb” and Trends in Aircraft Propulsion | optional | 991 | 1025–1032 | rules of thumb (inlet loss, ambient T) vs TSFC/thrust: background to performance parameters |

**El-Sayed**

| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |
|---|---|---|---|---|---|
| 1.1 | Pre–Jet Engine History | background | 4 | chapter-1.xhtml:1596 | pre-jet history; slide Ch.1 does not cover it |
| 1.2 | Jet Engines | ref | 15 | chapter-1.xhtml:1734 | jet-engine history (Whittle, von Ohain); slide Ch.1 tr.17–42 shows the engine types |
| 1.3 | Classifications of Aerospace Engines | core | 34 | chapter-1.xhtml:1978 | classification of aerospace engines ↔ slide Ch.1 tr.11–16 Aerospace engine, Classification of aerospace engine, (non-)airbreathing engines |
| 1.4 | Classification of Jet Engines | core | 35 | chapter-1.xhtml:1990 | classification of jet engines ↔ slide Ch.1 tr.17–42 Jet propulsion engines, tr.43–45 Classification of propulsion systems |
| 1.5 | Classification of Gas Turbine Engines | core | 39 | chapter-1.xhtml:2040 | classification of gas turbine engines ↔ slide Ch.1 tr.17–42, 48 |
| 1.6 | Industrial Gas Turbines | ref | 50 | chapter-1.xhtml:2164 | industrial gas turbines |
| 1.7 | Non-Airbreathing Engines | core | 50 | chapter-1.xhtml:2172 | non-airbreathing engines ↔ slide Ch.1 tr.14 |
| 1.8 | The Future of Aircraft and Powerplant Industries | ref | 51 | chapter-1.xhtml:2180 | future of aircraft and powerplant |
| Ch.1 | Problems | core | 63 | chapter-1.xhtml:2332 | end-of-chapter Problems |
| Ch.1 | References | ref | 72 | chapter-1.xhtml:2596 | end-of-chapter References |
| 2.1 | Introduction | core | 75 | chapter-2.xhtml:2643 | performance parameters: slide Ch.1 tr.7–10, 46–47 Definitions |
| 2.2 | Thrust Force | core | 76 | chapter-2.xhtml:2655 | performance parameters: slide Ch.1 tr.7–10, 46–47 Definitions |
| 2.3 | Factors Affecting Thrust | core | 87 | chapter-2.xhtml:3056 | performance parameters: slide Ch.1 tr.7–10, 46–47 Definitions |
| 2.4 | Engine Performance Parameters | core | 90 | chapter-2.xhtml:3123 | performance parameters: slide Ch.1 tr.7–10, 46–47 Definitions |
| Ch.2 | Problems | core | 122 | chapter-2.xhtml:4392 | end-of-chapter Problems |
| Ch.2 | References | ref | 133 | chapter-2.xhtml:4821 | end-of-chapter References |

### m02 — Chu trình công suất khí: Carnot, Otto, Diesel, Brayton và chu trình phản lực

Slide: ch2 tr.3–55, tut tr.1–23, tut tr.28–29. Tiêu đề slide: xem `data/bookmap/slides.json`.

**Cengel & Boles**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 4–1 | Moving Boundary Work | background | 166–172 | 192–198 | ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030 |
| 4–2 | Energy Balance for Closed Systems | background | 173–177 | 199–203 | ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030 |
| 4–3 | Specific Heats | background | 178–179 | 204–205 | ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030 |
| 4–4 | Internal Energy, Enthalpy, and Specific Heats of Ideal Gases | background | 180–188 | 206–214 | ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030 |
| 4–5 | Internal Energy, Enthalpy, and Specific Heat of Solids and Liquids | background | 189–192 | 215–218 | ideal-gas specific heats (§4-4) used by the cycle calculations; AE1.030 |
| 6–1 | Introduction to the Second Law | background | 280–280 | 306–306 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–2 | Thermal Energy Reservoirs | background | 281–281 | 307–307 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–3 | Heat Engines | background | 282–286 | 308–312 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–4 | Refrigerators and Heat Pumps | background | 287–292 | 313–318 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–5 | Perpetual-Motion Machines | background | 293–295 | 319–321 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–6 | Reversible and Irreversible Processes | background | 296–298 | 322–324 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–7 | The Carnot Cycle | background | 299–300 | 325–326 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–8 | The Carnot Principles | background | 301–302 | 327–328 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–9 | The Thermodynamic Temperature Scale | background | 303–304 | 329–330 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–10 | The Carnot Heat Engine | background | 305–308 | 331–334 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 6–11 | The Carnot Refrigerator and Heat Pump | background | 309–310 | 335–336 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–1 | Entropy | background | 332–334 | 358–360 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–2 | The Increase of Entropy Principle | background | 335–338 | 361–364 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–3 | Entropy Change of Pure Substances | background | 339–342 | 365–368 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–4 | Isentropic Processes | background | 343–343 | 369–369 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–5 | Property Diagrams Involving Entropy | background | 344–345 | 370–371 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–6 | What Is Entropy? | background | 346–349 | 372–375 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–7 | The T ds Relations | background | 350–350 | 376–376 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–8 | Entropy Change of Liquids and Solids | background | 351–353 | 377–379 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–9 | The Entropy Change of Ideal Gases | background | 354–361 | 380–387 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–10 | Reversible Steady-Flow Work | background | 362–365 | 388–391 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–11 | Minimizing the Compressor Work | background | 366–369 | 392–395 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–12 | Isentropic Efficiencies of Steady-Flow Devices | background | 370–376 | 396–402 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 7–13 | Entropy Balance | background | 377–390 | 403–416 | modules.py: Cengel Ch.9 "nền: Ch.6–7" |
| 9–1 | Basic Considerations in the Analysis of Power Cycles | core | 488–489 | 514–515 | slide Ch.2 tr.8–10 Considerations in the analysis of power cycles, Thermal efficiency |
| 9–2 | The Carnot Cycle and Its Value in Engineering | core | 490–491 | 516–517 | slide Ch.2 tr.11–13 The Carnot Cycle |
| 9–3 | Air-Standard Assumptions | core | 492–492 | 518–518 | slide Ch.2 tr.14 Air-Standard Assumptions |
| 9–4 | An Overview of Reciprocating Engines | core | 493–493 | 519–519 | slide Ch.2 tr.15–18 Reciprocating Engines |
| 9–5 | Otto Cycle: The Ideal Cycle for Spark-Ignition Engines | core | 494–499 | 520–525 | slide Ch.2 tr.19–25 Otto Cycle; Tutorials I tr.1–6, 14–15 |
| 9–6 | Diesel Cycle: The Ideal Cycle for Compression-Ignition Engines | core | 500–502 | 526–528 | slide Ch.2 tr.26–32 Diesel cycle; Tutorials I tr.7–13, 16–17 |
| 9–7 | Stirling and Ericsson Cycles | optional | 503–506 | 529–532 | Stirling/Ericsson: no slide title mentions them |
| 9–8 | Brayton Cycle:  The Ideal Cycle for Gas-Turbine Engines | core | 507–514 | 533–540 | slide Ch.2 tr.33–41 Brayton cycle; Tutorials I tr.18–23, 28–29 |
| 9–9 | The Brayton Cycle with Regeneration | core | 515–516 | 541–542 | slide Ch.2 tr.42–45 Brayton cycle with regeneration |
| 9–10 | The Brayton Cycle with Intercooling, Reheating, and Regeneration | core | 517–520 | 543–546 | slide Ch.2 tr.46–48 Brayton cycle with intercooling, reheating |
| 9–11 | Ideal Jet-Propulsion Cycles | core | 521–526 | 547–552 | slide Ch.2 tr.49–55 Ideal jet-propulsion cycles, Modifications to turbojet engines |
| 9–12 | Second-Law Analysis of Gas Power Cycles | optional | 527–529 | 553–555 | second-law analysis: not in slide titles |
| Ch.9 | Summary | ref | 537 | 563 | summary/reading/design problems |
| Ch.9 | References And Suggested Reading | ref | 538 | 564 | summary/reading/design problems |
| Ch.9 | Problems | core | 539 | 565 | end-of-chapter problems of a chapter assigned to the module |
| Ch.9 | Review Problems | core | 546 | 572 | end-of-chapter problems of a chapter assigned to the module |
| Ch.9 | Fundamentals Of Engineering (Fe) Exam Problems | core | 549 | 575 | end-of-chapter problems of a chapter assigned to the module |
| Ch.9 | Design And Essay Problems | ref | 550 | 576 | summary/reading/design problems |

**Farokhi**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 4.1 | Introduction | core | 151 | 185–185 | cycle analysis introduction; slide Ch.2 tr.49–52 |
| 4.2 | The Gas Generator | core | 151 | 185–185 | gas generator; slide Ch.2 tr.3 (compression, combustion, expansion) |
| 4.3 | Aircraft Gas Turbine Engines | ref | 152 | 186–258 | aircraft gas turbine engines (parent of 4.3.x) |
| 4.4 | Analysis of a Mixed-Exhaust Turbofan Engine with an Afterburner | optional | 225 | 259–274 | mixed-exhaust turbofan with afterburner |
| 4.5 | The Turboprop Engine | optional | 241 | 275–293 | turboprop |
| 4.6 | Summary | ref | 260 | 294–294 | summary |
| Ch.4 | References | ref | 261 | 295–295 | end-of-chapter References of an assigned chapter |
| Ch.4 | Problems | core | 261 | 295–316 | end-of-chapter Problems of an assigned chapter |
| App.K | 10-Minute Quiz | optional | 973 | 1007–1024 | 10-minute quiz: no answers printed; per-quiz module not assigned (? to be done in P3) |

**El-Sayed**

| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |
|---|---|---|---|---|---|
| 4.1 | Introduction | core | 203 | chapter-4.xhtml:6701 | turbojet ↔ slide Ch.2 tr.49–52 |
| 4.2 | Single Spool | core | 206 | chapter-4.xhtml:6723 | single-spool turbojet thermodynamic analysis (ideal/actual) ↔ slide Ch.2 tr.49–55 |
| 4.3 | Two-Spool Engine | ref | 239 | chapter-4.xhtml:7991 | two-spool turbojet |
| 4.4 | Statistical Analysis | optional | 249 | chapter-4.xhtml:8391 | statistical analysis |
| 4.5 | Thrust Augmentation | ref | 249 | chapter-4.xhtml:8403 | thrust augmentation, afterburning ↔ slide Ch.2 tr.53–55 |
| 4.6 | Supersonic Turbojet | optional | 257 | chapter-4.xhtml:8565 | supersonic turbojet |
| 4.7 | Optimization of the Turbojet Cycle | optional | 260 | chapter-4.xhtml:8681 | optimization of the turbojet cycle |
| 4.8 | Micro Turbojet | optional | 271 | chapter-4.xhtml:8916 | micro turbojet |
| Ch.4 | Problems | core | 277 | chapter-4.xhtml:9099 | end-of-chapter Problems |
| Ch.4 | References | ref | 288 | chapter-4.xhtml:9537 | end-of-chapter References |

### m03 — Chu trình lạnh và điều hoà không khí trên tàu bay

Slide: ch3 tr.3–36, tut tr.24–27 (trống: ch3 tr.37–38). Tiêu đề slide: xem `data/bookmap/slides.json`.

**Cengel & Boles**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 3–1 | Pure Substance | background | 112–112 | 138–138 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–2 | Phases of a Pure Substance | background | 112–112 | 138–138 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–3 | Phase-Change Processes of Pure Substances | background | 113–117 | 139–143 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–4 | Property Diagrams for Phase-Change Processes | background | 118–125 | 144–151 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–5 | Property Tables | background | 126–136 | 152–162 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–6 | The Ideal-Gas Equation of State | background | 137–138 | 163–164 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–7 | Compressibility Factor—A Measure of Deviation from Ideal-Gas | background | 139–143 | 165–169 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 3–8 | Other Equations of State | background | 144–148 | 170–174 | slide Ch.3 tr.4–8 specific/latent heat, wet steam area ↔ property tables of pure substances (AE1.030) |
| 11–1 | Refrigerators and Heat Pumps | core | 608–608 | 634–634 | slide Ch.3 tr.3, 9 Refrigeration cycles |
| 11–2 | The Reversed Carnot Cycle | core | 609–609 | 635–635 | slide Ch.3 tr.10–14 The (reversed) Carnot cycle |
| 11–3 | The Ideal Vapor-Compression Refrigeration Cycle | core | 610–613 | 636–639 | slide Ch.3 tr.15–25 Ideal vapor-compression cycle; Tutorials I tr.24–27 |
| 11–4 | Actual Vapor-Compression Refrigeration Cycle | core | 614–615 | 640–641 | slide Ch.3 tr.26 The real refrigeration process |
| 11–5 | Selecting the Right Refrigerant | ref | 616–617 | 642–643 | refrigerant choice: not a slide title (tr.27–28 Refrigerating equipment is the nearest) |
| 11–6 | Heat Pump Systems | ref | 618–619 | 644–645 | heat pumps: COP of heat pump appears with slide tr.20 |
| 11–7 | Innovative Vapor-Compression Refrigeration Systems | optional | 620–627 | 646–653 | cascade/multistage: not in slide titles |
| 11–8 | Gas Refrigeration Cycles | ref | 628–630 | 654–656 | gas (reversed Brayton) cycle = closest Cengel section to the air-cycle cooling pack of slide Ch.3 tr.29–36 (the book does not describe the aircraft pack) |
| 11–9 | Absorption Refrigeration Systems | optional | 631–633 | 657–659 | absorption: not in slide titles |
| Ch.11 | Summary | ref | 636 | 662 | summary/reading/design problems |
| Ch.11 | References And Suggested Reading | ref | 637 | 663 | summary/reading/design problems |
| Ch.11 | Problems | core | 637 | 663 | end-of-chapter problems of a chapter assigned to the module |
| Ch.11 | Review Problems | core | 644 | 670 | end-of-chapter problems of a chapter assigned to the module |
| Ch.11 | Fundamentals Of Engineering (Fe) Exam Problems | core | 647 | 673 | end-of-chapter problems of a chapter assigned to the module |
| Ch.11 | Design And Essay Problems | ref | 648 | 674 | summary/reading/design problems |
| 14–1 | Dry and Atmospheric Air | ref | 718–718 | 744–744 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–2 | Specific and Relative Humidity of Air | ref | 719–720 | 745–746 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–3 | Dew-Point Temperature | ref | 721–722 | 747–748 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–4 | Adiabatic Saturation and Wet-Bulb Temperatures | ref | 723–725 | 749–751 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–5 | The Psychrometric Chart | ref | 726–726 | 752–752 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–6 | Human Comfort and Air-Conditioning | ref | 727–728 | 753–754 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| 14–7 | Air-Conditioning Processes | ref | 729–738 | 755–764 | modules.py: Cengel Ch.14 if needed (CLO3 air conditioning); no slide title covers psychrometrics (slide Ch.3 tr.29 Air conditioner in aircraft is the only hook) |
| Ch.14 | Summary | ref | 739 | 765 | summary/reading/design problems |
| Ch.14 | References And Suggested Reading | ref | 741 | 767 | summary/reading/design problems |
| Ch.14 | Problems | ref | 741 | 767 | summary/reading/design problems |
| Ch.14 | Review Problems | ref | 747 | 773 | summary/reading/design problems |
| Ch.14 | Fundamentals Of Engineering (Fe) Exam Problems | ref | 749 | 775 | summary/reading/design problems |
| Ch.14 | Design And Essay Problems | ref | 750 | 776 | summary/reading/design problems |

**Farokhi**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|

**El-Sayed**

| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |
|---|---|---|---|---|---|

### m04 — Nhiên liệu và quá trình cháy

Slide: ch4 tr.3–55 (trống: ch4 tr.56–61). Tiêu đề slide: xem `data/bookmap/slides.json`.

**Cengel & Boles**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 15–1 | Fuels and Combustion | core | 752–755 | 778–781 | slide Ch.4 tr.3–12 FUELS AND COMBUSTION |
| 15–2 | Theoretical and Actual Combustion Processes | core | 756–761 | 782–787 | slide Ch.4 tr.13–39 Balancing the combustion equation, THEORETICAL AND ACTUAL COMBUSTION, Dew-point temperature of products, Reverse combustion analysis |
| 15–3 | Enthalpy of Formation and Enthalpy of Combustion | core | 762–764 | 788–790 | slide Ch.4 tr.40–55 ENTHALPY OF FORMATION AND ENTHALPY OF COMBUSTION |
| 15–4 | First-Law Analysis of Reacting Systems | ref | 765–769 | 791–795 | CLO4 "enthalpy changes in practical combustion": first-law analysis; not a slide title |
| 15–5 | Adiabatic Flame Temperature | optional | 770–772 | 796–798 | adiabatic flame temperature: not in slide titles |
| 15–6 | Entropy Change of Reacting Systems | optional | 773–774 | 799–800 | entropy of reacting systems: not in slides |
| 15–7 | Second-Law Analysis of Reacting systems | optional | 775–779 | 801–805 | second-law analysis of reacting systems: not in slides |
| Ch.15 | Summary | ref | 782 | 808 | summary/reading/design problems |
| Ch.15 | References And Suggested Reading | ref | 783 | 809 | summary/reading/design problems |
| Ch.15 | Problems | core | 783 | 809 | end-of-chapter problems of a chapter assigned to the module |
| Ch.15 | Review Problems | core | 788 | 814 | end-of-chapter problems of a chapter assigned to the module |
| Ch.15 | Fundamentals Of Engineering (Fe) Exam Problems | core | 791 | 817 | end-of-chapter problems of a chapter assigned to the module |
| Ch.15 | Design And Essay Problems | ref | 792 | 818 | summary/reading/design problems |

**Farokhi**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 7.1 | Introduction | ref | 429 | 463–464 | introduction |
| 7.2 | Laws Governing Mixture of Gases | core | 431 | 465–467 | mixture of gases ↔ slide Ch.4 tr.3–12 |
| 7.3 | Chemical Reaction and Flame Temperature | core | 434 | 468–478 | chemical reaction and flame temperature ↔ slide Ch.4 tr.13–55 |
| 7.4 | Chemical Equilibrium and Chemical Composition | optional | 445 | 479–492 | chemical equilibrium: not in slides |
| 7.5 | Chemical Kinetics | optional | 459 | 493–506 | chemical kinetics: not in slides |
| 7.6 | Combustion Chamber | optional | 473 | 507–531 | combustion chamber design |
| 7.7 | Combustion-Generated Pollutants | optional | 498 | 532–542 | pollutants |
| 7.8 | Aviation Fuels | ref | 509 | 543–546 | aviation fuels ↔ slide Ch.4 tr.3–12 FUELS |
| 7.9 | Alternative “Drop-In” Jet Fuels (AJFs) | optional | 513 | 547–548 | alternative jet fuels |
| 7.10 | Combustion Instability: Screech and Rumble | optional | 515 | 549–549 | combustion instability |
| 7.11 | Summary | ref | 516 | 550–550 | summary |
| Ch.7 | References | ref | 516 | 550–551 | end-of-chapter References of an assigned chapter |
| Ch.7 | Problems | core | 518 | 552–558 | end-of-chapter Problems of an assigned chapter |
| App.K | 10-Minute Quiz | optional | 973 | 1007–1024 | 10-minute quiz: no answers printed; per-quiz module not assigned (? to be done in P3) |

**El-Sayed**

| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |
|---|---|---|---|---|---|
| 10.1 | Introduction | ref | 739 | chapter-10.xhtml:22489 | introduction |
| 10.2 | Subsonic Combustion Chambers | optional | 740 | chapter-10.xhtml:22521 | combustor types |
| 10.3 | Supersonic Combustion Chamber | optional | 744 | chapter-10.xhtml:22627 | supersonic combustion chamber |
| 10.4 | Combustion Process | ref | 744 | chapter-10.xhtml:22631 | combustion process ↔ slide Ch.4 tr.3–12 |
| 10.5 | Components of the Combustion Chamber | optional | 746 | chapter-10.xhtml:22651 | components |
| 10.6 | Aerodynamics of the Combustion Chamber | optional | 748 | chapter-10.xhtml:22675 | aerodynamics |
| 10.7 | Chemistry of Combustion | core | 753 | chapter-10.xhtml:22859 | chemistry of combustion ↔ slide Ch.4 tr.13–39 |
| 10.8 | The First Law Analysis of Combustion | core | 757 | chapter-10.xhtml:23023 | first-law analysis of combustion ↔ slide Ch.4 tr.40–55 |
| 10.9 | Combustion Chamber Performance | optional | 759 | chapter-10.xhtml:23086 | performance |
| 10.10 | Material | optional | 766 | chapter-10.xhtml:23247 | materials |
| 10.11 | Aircraft Fuels | ref | 766 | chapter-10.xhtml:23251 | aircraft fuels ↔ slide Ch.4 tr.3–12 |
| 10.12 | Emissions and Pollutants | optional | 768 | chapter-10.xhtml:23307 | emissions |
| 10.13 | The Afterburner | optional | 770 | chapter-10.xhtml:23347 | afterburner |
| 10.14 | Supersonic Combustion System | optional | 773 | chapter-10.xhtml:23461 | supersonic combustion |
| Ch.10 | Problems | core | 776 | chapter-10.xhtml:23495 | end-of-chapter Problems |
| Ch.10 | References | ref | 778 | chapter-10.xhtml:23643 | end-of-chapter References |

### m05 — Dòng chảy nén được

Slide: ch5 tr.3–59 (trống: ch5 tr.60–63). Tiêu đề slide: xem `data/bookmap/slides.json`.

**Cengel & Boles**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 5–1 | Conservation of Mass | background | 220–225 | 246–251 | steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030 |
| 5–2 | Flow Work and the Energy of a Flowing Fluid | background | 226–229 | 252–255 | steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030 |
| 5–3 | Energy Analysis of Steady-Flow Systems | background | 230–232 | 256–258 | steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030 |
| 5–4 | Some Steady-Flow Engineering Devices | background | 233–245 | 259–271 | steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030 |
| 5–5 | Energy Analysis of Unsteady-Flow Processes | background | 246–251 | 272–277 | steady-flow devices (nozzles, diffusers) ↔ slide Ch.5; AE1.030 |
| 7–1 | Entropy | background | 332–334 | 358–360 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–2 | The Increase of Entropy Principle | background | 335–338 | 361–364 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–3 | Entropy Change of Pure Substances | background | 339–342 | 365–368 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–4 | Isentropic Processes | background | 343–343 | 369–369 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–5 | Property Diagrams Involving Entropy | background | 344–345 | 370–371 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–6 | What Is Entropy? | background | 346–349 | 372–375 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–7 | The T ds Relations | background | 350–350 | 376–376 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–8 | Entropy Change of Liquids and Solids | background | 351–353 | 377–379 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–9 | The Entropy Change of Ideal Gases | background | 354–361 | 380–387 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–10 | Reversible Steady-Flow Work | background | 362–365 | 388–391 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–11 | Minimizing the Compressor Work | background | 366–369 | 392–395 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–12 | Isentropic Efficiencies of Steady-Flow Devices | background | 370–376 | 396–402 | isentropic processes of ideal gases (§7-4, §7-9) |
| 7–13 | Entropy Balance | background | 377–390 | 403–416 | isentropic processes of ideal gases (§7-4, §7-9) |
| 17–1 | Stagnation Properties | core | 824–826 | 850–852 | slide Ch.5 tr.3–16 STAGNATION PROPERTIES; Compression of high-speed air |
| 17–2 | Speed of Sound and Mach Number | ref | 827–828 | 853–854 | speed of sound/Mach number: no slide title; Mach number used from tr.14 on (to be confirmed in P3) |
| 17–3 | One-Dimensional Isentropic Flow | core | 829–835 | 855–861 | slide Ch.5 tr.17–38 ONE-DIMENSIONAL ISENTROPIC FLOW, converging–diverging duct, property relations, critical T and p |
| 17–4 | Isentropic Flow through Nozzles | core | 836–844 | 862–870 | slide Ch.5 tr.39–59 ISENTROPIC FLOW THROUGH NOZZLES, back pressure, converging nozzle |
| 17–5 | Shock Waves and Expansion | ref | 845–859 | 871–885 | shock waves: not in slide titles (tr.3–59); Farokhi Ch.2 and El-Sayed §3.8 cover them |
| 17–6 | Duct Flow with Heat Transfer and Negligible Friction (Rayleigh Flow) | optional | 860–868 | 886–894 | Rayleigh flow: not in slide titles |
| 17–7 | Steam Nozzles | optional | 869–871 | 895–897 | steam nozzles: not in slide titles |
| Ch.17 | Summary | ref | 872 | 898 | summary/reading/design problems |
| Ch.17 | References And Suggested Reading | ref | 873 | 899 | summary/reading/design problems |
| Ch.17 | Problems | core | 874 | 900 | end-of-chapter problems of a chapter assigned to the module |
| Ch.17 | Review Problems | core | 879 | 905 | end-of-chapter problems of a chapter assigned to the module |
| Ch.17 | Fundamentals Of Engineering (Fe) Exam Problems | core | 880 | 906 | end-of-chapter problems of a chapter assigned to the module |
| Ch.17 | Design And Essay Problems | ref | 881 | 907 | summary/reading/design problems |

**Farokhi**

| Mục | Tên | Vai trò | Tr. in | Tr. PDF | Cơ sở |
|---|---|---|---|---|---|
| 2.1 | Introduction | ref | 21 | 55–55 | introduction |
| 2.2 | A Brief Review of Thermodynamics | background | 22 | 56–60 | thermodynamics review (AE1.030) |
| 2.3 | Isentropic Process and Isentropic Flow | core | 27 | 61–61 | isentropic relations: slide Ch.5 tr.32–35 |
| 2.4 | Conservation Principles for Systems and Control Volumes | background | 28 | 62–68 | conservation laws (AE1.030) |
| 2.5 | Speed of Sound & Mach Number | core | 35 | 69–71 | speed of sound and Mach number: slide Ch.5 tr.14+ |
| 2.6 | Stagnation State | core | 38 | 72–74 | stagnation state: slide Ch.5 tr.3–16 |
| 2.7 | Quasi-One-Dimensional Flow | core | 41 | 75–77 | quasi-1D flow: slide Ch.5 tr.17–31 |
| 2.8 | Area–Mach Number Relationship | core | 44 | 78–78 | area–Mach relation: slide Ch.5 tr.25–31 |
| 2.9 | Sonic Throat | core | 45 | 79–82 | sonic throat: slide Ch.5 tr.36–38 |
| 2.10 | Waves in Supersonic Flow | ref | 49 | 83–83 | shocks: not in slide titles tr.3–59 |
| 2.11 | Normal Shocks | ref | 50 | 84–87 | normal shocks |
| 2.12 | Oblique Shocks | optional | 54 | 88–93 | oblique shocks |
| 2.13 | Conical Shocks | optional | 60 | 94–96 | conical shocks |
| 2.14 | Expansion Waves | optional | 63 | 97–100 | expansion waves |
| 2.15 | Frictionless, Constant-Area Duct Flow with Heat Transfer | optional | 67 | 101–110 | Rayleigh flow |
| 2.16 | Adiabatic Flow of a Calorically Perfect Gas in a Constant-Area Duct with Friction | optional | 77 | 111–124 | Fanno flow |
| 2.17 | Friction (Drag) Coefficient Cf and D'Arcy Friction Factor fD | optional | 91 | 125–125 | friction factor |
| 2.18 | Dimensionless Parameters | optional | 91 | 125–128 | dimensionless parameters |
| 2.19 | Fluid Impulse | optional | 95 | 129–135 | fluid impulse |
| 2.20 | Summary of Fluid Impulse | optional | 102 | 136–136 | summary of fluid impulse |
| Ch.2 | References | ref | 103 | 137–137 | end-of-chapter References of an assigned chapter |
| Ch.2 | Problems | core | 103 | 137–146 | end-of-chapter Problems of an assigned chapter |
| 6.1 | Introduction | ref | 327 | 361–361 | inlets and nozzles |
| 6.2 | The Flight Mach Number and Its Impact on Inlet Duct Geometry | ref | 328 | 362–362 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.3 | Diffusers | ref | 329 | 363–363 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.4 | An Ideal Diffuser | ref | 330 | 364–364 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.5 | Real Diffusers and Their Stall Characteristics | ref | 331 | 365–366 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.6 | Subsonic Diffuser Performance | ref | 333 | 367–371 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.7 | Subsonic Cruise Inlet | ref | 338 | 372–381 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.8 | Transition Ducts | ref | 348 | 382–382 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.9 | An Interim Summary for Subsonic Inlets | ref | 349 | 383–383 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.10 | Supersonic Inlets | ref | 350 | 384–392 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.11 | Normal Shock Inlets | ref | 359 | 393–395 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.12 | External Compression Inlets | ref | 362 | 396–401 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.13 | Variable Geometry—External Compression Inlets | ref | 368 | 402–402 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.14 | Mixed-Compression Inlets | ref | 368 | 402–403 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.15 | Supersonic Inlet Types and Their Performance—A Review | ref | 370 | 404–404 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.16 | Standards for Supersonic Inlet Recovery | ref | 371 | 405–406 | inlets (6.1–6.16): supersonic inlet shocks; not in slide titles |
| 6.17 | Exhaust Nozzle | ref | 373 | 407–407 | exhaust nozzle ↔ slide Ch.5 tr.39–49 |
| 6.18 | Gross Thrust | ref | 373 | 407–407 | gross thrust |
| 6.19 | Nozzle Adiabatic Efficiency | ref | 373 | 407–407 | nozzle efficiency |
| 6.20 | Nozzle Total Pressure Ratio | ref | 374 | 408–408 | nozzle pressure ratio |
| 6.21 | Nozzle Pressure Ratio (NPR) and Critical Nozzle Pressure Ratio (NPRcrit.) | core | 374 | 408–409 | NPR and critical NPR ↔ slide Ch.5 tr.50–55 Effect of back pressure |
| 6.22 | Relation Between Nozzle Figures of Merit, ηn and n | ref | 376 | 410–410 | nozzle figures of merit |
| 6.23 | A Convergent Nozzle or a De Laval? | core | 376 | 410–412 | convergent nozzle or de Laval ↔ slide Ch.5 tr.56–59 converging nozzle |
| Ch.6 | References | ref | 411 | 445–446 | end-of-chapter References of an assigned chapter |
| Ch.6 | Problems | core | 413 | 447–462 | end-of-chapter Problems of an assigned chapter |
| App.B | Isentropic Table | core | 907 | 941–957 | modules.py: Appendix B Isentropic Table; slide Ch.5 uses isentropic functions (Cengel Table A-32 is the primary table) |
| App.C | Normal Shock Table | optional | 924 | 958–970 | normal-shock/Rayleigh/Fanno tables: shocks/Rayleigh/Fanno are not in slide titles |
| App.D | Rayleigh Flow | optional | 937 | 971–979 | normal-shock/Rayleigh/Fanno tables: shocks/Rayleigh/Fanno are not in slide titles |
| App.E | Fanno Flow | optional | 946 | 980–988 | normal-shock/Rayleigh/Fanno tables: shocks/Rayleigh/Fanno are not in slide titles |
| App.K | 10-Minute Quiz | optional | 973 | 1007–1024 | 10-minute quiz: no answers printed; per-quiz module not assigned (? to be done in P3) |

**El-Sayed**

| Mục | Tên | Vai trò | Tr. in | File:dòng md | Cơ sở |
|---|---|---|---|---|---|
| 3.8 | Summary and Governing Equations for Shock Waves and Isentropic Flow | core | 194 | chapter-3.xhtml:6450 | shock waves and isentropic flow relations ↔ slide Ch.5 (modules.py: Ch.3 §3.8) |
| 9.1 | Introduction | ref | 679 | chapter-9.xhtml:21220 | intakes |
| 9.2 | Powerplant Installation | optional | 679 | chapter-9.xhtml:21232 | powerplant installation |
| 9.3 | Subsonic Aircraft | optional | 681 | chapter-9.xhtml:21238 | installation |
| 9.4 | Supersonic Aircraft | optional | 691 | chapter-9.xhtml:21426 | installation |
| 9.5 | Air Intakes or Inlets | ref | 695 | chapter-9.xhtml:21462 | air intakes ↔ slide Ch.5 tr.39–49 nozzles/diffusers |
| 9.6 | Subsonic Intakes | ref | 695 | chapter-9.xhtml:21466 | subsonic intakes |
| 9.7 | Supersonic Intakes | ref | 705 | chapter-9.xhtml:21736 | supersonic intakes: shock relations |
| 9.8 | Matching between Intake and Engine | optional | 719 | chapter-9.xhtml:22107 | intake–engine matching |
| 9.9 | Case Study | optional | 721 | chapter-9.xhtml:22133 | case study |
| Ch.9 | Problems | core | 731 | chapter-9.xhtml:22338 | end-of-chapter Problems |
| Ch.9 | References | ref | 738 | chapter-9.xhtml:22467 | end-of-chapter References |
| 11.1 | Introduction | ref | 781 | chapter-11.xhtml:23666 | introduction |
| 11.2 | Nozzle | core | 784 | chapter-11.xhtml:23690 | nozzle governing equations ↔ slide Ch.5 tr.39–59 |
| 11.3 | Calculation of the Two-Dimensional Supersonic Nozzle | ref | 795 | chapter-11.xhtml:23993 | convergent/divergent nozzle calculation ↔ slide Ch.5 tr.50–59 |
| 11.4 | Thrust Reversal | optional | 810 | chapter-11.xhtml:24343 | thrust reversal |
| 11.5 | Thrust Vectoring | optional | 819 | chapter-11.xhtml:24609 | thrust vectoring |
| 11.6 | Noise | optional | 823 | chapter-11.xhtml:24659 | noise |
| 11.7 | High-Speed Vehicles | optional | 830 | chapter-11.xhtml:24731 | high-speed nozzles |
| Ch.11 | Problems | core | 834 | chapter-11.xhtml:24845 | end-of-chapter Problems |
| Ch.11 | References | ref | 836 | chapter-11.xhtml:24917 | end-of-chapter References |

## Phần cuối chương và ví dụ (cho quét bài tập ở giai đoạn sau)

### Cengel (tr. PDF; tr. in = PDF − 26)

| Ch. | Summary | References | Problems | Review Problems | FE Exam | Design & Essay | Topic of Special Interest | #bài | #bài có "Answers:" |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 65 | 65 | 66 | 72 | 76 | — | — | 129 | 19 |
| 2 | 122 | 123 | 124 | 131 | 134 | 135 | 118 | 148 | 13 |
| 3 | 179 | 180 | 180 | 186 | 190 | — | 175 | 145 | 24 |
| 4 | 226 | 227 | 227 | 236 | 241 | — | 219 | 180 | 38 |
| 5 | 281 | 282 | 282 | 296 | 303 | 304 | 278 | 217 | 57 |
| 6 | 341 | 342 | 342 | 350 | 355 | 356 | 337 | 172 | 30 |
| 7 | 426 | 427 | 428 | 440 | 447 | 448 | 417 | 241 | 39 |
| 8 | 495 | 496 | 496 | 505 | 511 | 511 | 491 | 158 | 41 |
| 9 | 563 | 564 | 565 | 572 | 575 | 576 | 556 | 191 | 27 |
| 10 | 615 | 615 | 616 | 625 | 628 | 629 | 612 | 133 | 28 |
| 11 | 662 | 663 | 663 | 670 | 673 | 674 | 660 | 129 | 22 |
| 12 | 700 | 701 | 701 | 704 | 705 | 706 | — | 98 | 16 |
| 13 | 734 | 735 | 735 | 739 | 740 | — | 723 | 105 | 10 |
| 14 | 765 | 767 | 767 | 773 | 775 | 776 | — | 157 | 21 |
| 15 | 808 | 809 | 809 | 814 | 817 | 818 | 806 | 133 | 32 |
| 16 | 841 | 842 | 843 | 846 | 847 | 848 | — | 111 | 22 |
| 17 | 898 | 899 | 900 | 905 | 906 | 907 | — | 163 | 30 |

**Đáp án in của Cengel:** right after the statement of the problem, as "Answers: ..." (some problems only). Nhận biết: line starting with "Answer:" or "Answers:" inside the problem list, before the next problem number "k-n". No "Answers to selected problems" appendix in the PDF (it stops at PDF p.907 = printed 881 in the middle of the FE problems of Ch.17; PDF p.908 is blank; Glossary p.909–963). Problems marked C are concept questions (no numeric answer). Tổng: 469 trong 2610 bài (đếm bằng script, `verify_bookmap.py`).

### Farokhi (tr. PDF; in = PDF − 34)

| Ch. | PDF đầu–cuối | References | Problems (đầu–cuối) | Ví dụ (E X A M P L E) |
|---|---|---|---|---|
| 1 | 35–54 | 53 | 54–54 | không có ví dụ đánh số |
| 2 | 55–146 | 137 | 137–146 | 2.1
@57, 2.2
@62, 2.3
@64, 2.4
@66, 2.5
@68, 2.6
@108, 2.7
@109, 2.8
@110, 2.9
@122, 2.10
@122, 2.11
@123, 2.12@130, 2.13@131, 2.14@134, 2.15@135, 2.16@135 |
| 3 | 147–184 | 178 | 178–184 | 3.1
@152, 3.2
@153, 3.3
@163, 3.4
@166, 3.5
@170, 3.6
@170 |
| 4 | 185–316 | 295 | 295–316 | 4.1
@191, 4.2
@197, 4.3
@202, 4.4
@210, 4.5
@210, 4.6
@211, 4.7
@218, 4.8
@227, 4.9
@227, 4.10
@229, 4.11
@240, 4.12
@242, 4.13
@251, 4.14
@254, 4.15
@257, 4.16
@270, 4.17
@272, 4.18
@280, 4.19
@281, 4.20
@290, 4.21
@292 |
| 6 | 361–462 | 445 | 447–462 | 6.1
@389, 6.2
@391, 6.3
@392, 6.4
@395, 6.5
@397, 6.6
@412, 6.7
@414, 6.8
@417, 6.9
@418, 6.10
@424, 6.11
@431, 6.12
@436, 6.13
@439 |
| 7 | 463–558 | 550 | 552–558 | 7.1
@464, 7.2
@472, 7.3
@474, 7.4
@477, 7.5
@478, 7.6
@481, 7.7
@489 |
| App.B Isentropic Table | 941–957 | — | — | — |
| App.K 10-Minute Quiz | 1007–1024 | — | — | — |
| App.L Some “Rules of Thumb” and Trends in Aircraft Propulsion | 1025–1032 | — | — | — |

Appendix K: 45 bài quiz 10 phút (mỗi quiz một bookmark, PDF 1007–1024), **không in đáp án** (kiểm bằng text và ảnh tr.1024). Bài tập cuối chương Farokhi **không in đáp án**. Appendix L (PDF 1025–1032) là bảng quy tắc ngón tay cái (thay đổi % lực đẩy/TSFC), không có bài tập. Chưa gán quiz nào cho module cụ thể (`?`, để P3).

### El-Sayed (tr. in; dòng trong 11_*.md)

| Ch. | Trang in | Problems (tr. in : dòng) | References | Số ví dụ "Example n.m" |
|---|---|---|---|---|
| 1 History and Classifications of Aeroengines | 3–74 | 63 : 2332 | 72 | 0 |
| 2 Performance Parameters of Jet Engines | 75–134 | 122 : 4392 | 133 | 16 |
| 3 Pulsejet and Ramjet Engines | 135–202 | 196 : 6509 | 200 | 9 |
| 4 Turbojet Engine | 203–288 | 277 : 9099 | 288 | 11 |
| 9 Powerplant Installation and Intakes | 679–738 | 731 : 22338 | 738 | 7 |
| 10 Combustion Systems | 739–780 | 776 : 23495 | 778 | 6 |
| 11 Exhaust System | 781–838 | 834 : 24845 | 836 | 6 |

**Đáp án in của El-Sayed:** không. No answers/solutions to the problems anywhere in the EPUB text (no "Answer(s)" heading or Answers appendix: back matter is Appendix A Glossary, B Turbofan, C Samples of gas turbines, Index). Chapter Problems are statements only.

## CLO3 — tìm ECS / cooling pack / air cycle machine / bleed air

- Câu hỏi: CLO3: air conditioning / ECS / cooling pack / air cycle machine / bleed air in Farokhi and El-Sayed (slide Ch.3 tr.29-36 = "Air conditioner in aircraft", "AIR CYCLE COOLING PACK", "Operation of the Cooling Pack")
- Lệnh grep đã dùng:
  - `grep -n -i -E 'air.?condition|air cycle|cooling pack|environmental control|\bECS\b|customer bleed|cabin|pressuriz|refrigerat|\bECU\b' OCR_output/10_Farokhi_Aircraft_Propulsion.md`
  - `grep -n -i -E 'air.?condition|air cycle|cooling pack|environmental control|\bECS\b|cabin|pressuriz|refrigerat|passenger|compressor bleed|customer' OCR_output/11_ElSayed_Aircraft_Propulsion_and_Gas_Turbine_Engines.md`

- **Farokhi:** KHÔNG CÓ. No hit for air conditioning, ECS, cooling pack, air cycle, customer bleed, cabin, refrigeration. The only hits are rocket propellant tank pressurization (Ch.12), turbine-cooling bleed and inlet boundary-layer bleed (not cabin air). So: không có.
- **El-Sayed:** gần như không có; chỉ có các câu sau:
  - tr. in 301 (Ch.5, dòng 9970): Comment on a bleed ratio: "bleeding has its applications for cabin-air conditioning as well as other anti-icing functions." (turbofan Ch.5, outside the scope chapters; the sentence names the use, no ECS description, no air-cycle machine, no cooling pack)
  - tr. in 13 (Ch.1, dòng 1698): history: "enclosed cabin airplane became the standard" (no ECS)
  - tr. in 500 (Ch.6, dòng 16136): "Engine noise in the cabin area is reduced" (propfan; no ECS)
  - Turbine-cooling bleed (Ch.5 Examples, Ch.14) and bleed valves of compressors (Ch.13) are not air-conditioning content.
- Kết luận: Neither book describes the aircraft ECS / air cycle machine / cooling pack. Best textbook anchors for CLO3 stay Cengel Ch.11 (esp. §11-8 gas refrigeration = reversed Brayton) and Ch.14 §14-7 (air-conditioning processes); the cooling-pack slides tr.29-36 have no book counterpart.

## Slide (tiêu đề từng trang: `data/bookmap/slides.json`)

| Deck | Tổng trang | content | blank | title/out |
|---|---|---|---|---|
| ch1 | 49 | 44 | 0 | 5 |
| ch2 | 56 | 53 | 0 | 3 |
| ch3 | 38 | 34 | 2 | 2 |
| ch4 | 61 | 53 | 6 | 2 |
| ch5 | 63 | 57 | 4 | 2 |
| tut | 29 | 29 | 0 | 0 |

Ghi chú: các deck không có tiêu đề slide dạng placeholder; "tiêu đề" = dòng chữ đầu tiên của trang trong `OCR_output/02…07_*.md`. Ch.1 tr.17–42 đều mang tên "Jet propulsion engines" (26 trang).

## Lỗi / lệch tìm thấy

- Cengel, trang Contents (PDF 2–17) đánh số lệch ở Ch.6: bỏ qua 6–4, các mục 6–5…6–12 trong Contents tương ứng 6–4…6–11 trong thân sách (mục cuối "The Carnot Refrigerator and Heat Pump" là 6–11 ở tr. in 309/PDF 335 — xem ảnh). Bản đồ dùng số trong thân sách. Ch.7: Contents ghi mục "Entropy Balance" là 7–13 (khớp thân sách), Ch.12: mục 12–4 "General Relations" có trong thân sách nhưng thiếu ở Contents (tên lấy từ tiêu đề thân sách).
- Cengel, mục tên trong Contents đôi chỗ khác chữ hoa/thường so với thân sách ("Brayton Cycle:  The Ideal…"); dùng tên trong Contents.
- Cengel PDF dừng ở PDF 907 (in 881) giữa các bài FE của Ch.17: không có phần còn lại và không có phụ lục đáp án.
- Cengel text layer mất ký hiệu (=, −, Hy Lạp) nên khớp tiêu đề chỉ theo chữ/số; 10 tiêu đề kiểm bằng ảnh: 6–11, 9–8, 9–9, 9–10, 9–11, 11–3, 11–8, 14–7, 15–3, 17–4 (trang và số in đúng).
- El-Sayed: dấu `⟦p.N⟧` trong bản chữ đôi khi đặt trễ vài dòng so với span pagebreak của EPUB (9.3, 11.2…); bản đồ dùng span trong xhtml (verify 230/230).
- El-Sayed Ch.1 trong `modules.py` ghi "Ch.1 History and Classifications" và Ch.2 "Performance Parameters": đúng. Ch.4 là Turbojet; slide Ch.2 (Brayton, jet-propulsion cycle) khớp §4.2 hơn là phần turbofan (Ch.5, ngoài `modules.py`).

## Đề xuất sửa `build/modules.py` (không tự sửa)

1. m03: ghi rõ Farokhi/El-Sayed = "không có mục về ECS/cooling pack (đã grep, xem phần CLO3)"; thay "chưa tìm thấy" bằng kết luận chắc. Cân nhắc thêm Cengel §11-8 (gas refrigeration) làm mục gần nhất với air cycle cooling pack và §14-7.
2. m01: Cengel Ch.1–2 chỉ có vai trò `background`; Farokhi Ch.1 là `ref` (lịch sử), Ch.3 mới là `core`. Có thể thêm Cengel §9-11 (jet-propulsion) và El-Sayed §1.3–1.5 (phân loại) vào danh sách sách của m01.
3. m02: thêm Farokhi §4.3.1 (turbojet) và El-Sayed §4.2 làm `core`; phần còn lại Ch.4 là `ref`/`optional`.
4. m05: slide Ch.5 tr.3–59 chỉ tới converging nozzle (Cengel §17-1…17-4); Cengel §17-5 (sóng xung kích), Farokhi §2.10–2.14 và El-Sayed §3.8 là phần sách rộng hơn slide (`ref`).
5. m04: Cengel §15-2 (balancing, dew point, reverse analysis) và §15-3 là phần lõi; thêm Farokhi §7.2–7.3 và El-Sayed §10.7–10.8 làm `core` thay vì cả chương.

## Chưa làm

- Gán từng bài Quiz Appendix K (45) cho module.
- Phân loại chi tiết tiểu mục (subsection) Cengel (có trong `subs` nhưng chưa có trang riêng).
- Chưa xác nhận Cengel §17-2 (speed of sound) có nằm trong slide Ch.5 hay không (không có tiêu đề riêng).
- `build/bookmap_body.py`/`_shared/bookmap.js` (trang HTML) chưa chỉnh cho dữ liệu mới: ngoài phạm vi P2 này.
