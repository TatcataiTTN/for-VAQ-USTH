# -*- coding: utf-8 -*-
"""Module 01: Vat ly khi quyen. Nguon: EASA M08 Sub-module 01 (tr.1.1-1.8), Anderson 6th Ch.1 (muc 1.4, Bai 1.1, 1.11, 1.12; Phu luc D),
Etkin & Reid 3rd Phu luc D (The Standard Atmosphere). Moi con so tinh bang aero.py."""
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    # ---- so lieu da tinh ----
    isa_rows = []
    for h in (0, 10000, 20000, 30000, 36089, 40000):
        T_, p_, r_ = isa_ft(h)
        isa_rows.append((f"{h:,}".replace(",", " "), N(T_ - 273.15, 1), N(p_ / 100, 1), N(p_ / PSI, 2), N(r_, 4)))
    _, p40, _ = isa_ft(40000)
    rho_11a = 1.9e4 / (R_ANDERSON * 203)
    T_11b = 1058 / (1.23e-3 * 1716)
    p_11 = 1.01e5 - 1.36e4 * 9.8 * 0.2
    rho1000 = isa(1000)[2]
    B = 15000 * rho1000 * 9.8
    S = math.pi * 14 ** 2 / 4
    q = 0.5 * rho1000 * 30 ** 2
    Lz = q * S * 0.05
    W = B + Lz
    T5, p5, _r = isa_ft(5000)
    rho_hot = p5 / (R_AIR * (30 + 273.15))
    ratio = rho_hot / RHO0
    isa_dev = 30 - (T5 - 273.15)
    lo, hi = 0.0, 15000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if isa(mid)[2] > rho_hot:
            lo = mid
        else:
            hi = mid
    dens_alt_ft = lo / FT

    m = {"num": "01", "slug": "01-atmosphere", "tag": L("Khí quyển", "Atmosphere")}
    m["title"] = L("Vật lý khí quyển và khí quyển chuẩn quốc tế (ISA)", "Physics of the Atmosphere and the International Standard Atmosphere (ISA)")
    m["src"] = L("EASA Module 08, Sub-module 01 (tr. 1.1–1.8) · Anderson ch.1 mục 1.4 và Phụ lục D · Etkin &amp; Reid Phụ lục D",
                 "EASA Module 08, Sub-module 01 (pp. 1.1–1.8) · Anderson ch.1 sec. 1.4 and Appendix D · Etkin &amp; Reid Appendix D")
    m["intro"] = L("Máy bay hoạt động trong không khí, nên mọi lực khí động đều phụ thuộc vào ba đại lượng của không khí: áp suất, mật độ và nhiệt độ. Module này đi từ áp suất và các đơn vị của nó, qua mật độ và độ ẩm, đến sự thay đổi theo độ cao và mô hình khí quyển chuẩn ISA, rồi áp dụng vào bài toán thật: mật độ không khí trên cánh Boeing 727, khí cầu Zeppelin và sân bay cao nguyên nóng.",
                   "An aircraft operates in air, so every aerodynamic force depends on three properties of that air: pressure, density and temperature. This module goes from pressure and its units, through density and humidity, to the change with altitude and the International Standard Atmosphere (ISA), then applies it to real problems: air density on a Boeing 727 wing, a World War I Zeppelin and a hot high-altitude airport.")
    m["mapping"] = {
        "easa": L("Sub-module 01 Physics of the Atmosphere (tr. 1.1–1.8): áp suất, mật độ, độ ẩm, nhiệt độ và độ cao, ISA; 3 câu hỏi cuối chương (Q1-1 đến Q1-3)",
                  "Sub-module 01 Physics of the Atmosphere (pp. 1.1–1.8): pressure, density, humidity, temperature and altitude, ISA; 3 end-of-chapter questions (Q1-1 to Q1-3)"),
        "anderson": L("Ch.1 mục 1.4 (các đại lượng cơ bản: áp suất, mật độ, nhiệt độ), mục 1.9 (tĩnh học chất lưu), Phụ lục D/E (bảng khí quyển chuẩn); Bài 1.1, 1.11, 1.12 (mục 1.17 Problems)",
                      "Ch.1 sec. 1.4 (basic quantities: pressure, density, temperature), sec. 1.9 (fluid statics), Appendices D/E (standard atmosphere tables); Problems 1.1, 1.11, 1.12 (sec. 1.17)"),
        "etkin": L("Phụ lục D The Standard Atmosphere and Other Data (tr. 364–368); Ch.1 mục 1.1 (lực khí động là một trong các trường lực chính của cơ học bay)",
                   "Appendix D The Standard Atmosphere and Other Data (pp. 364–368); Ch.1 sec. 1.1 (the aerodynamic force field is one of the strong fields in flight dynamics)"),
        "note": L("EASA chỉ giới thiệu định tính và đưa bảng ISA; Anderson cho phương trình trạng thái p = ρRT và các bài tính; Etkin cho bảng ISA đầy đủ dùng trong ví dụ Boeing 747. Solution Manual của Anderson là bản 4th; bài 1.1, 1.11, 1.12 có số liệu trùng bản 6th.",
                  "EASA only introduces the topic qualitatively with an ISA table; Anderson gives the equation of state p = ρRT and numeric problems; Etkin gives the full ISA table used in the Boeing 747 examples. Anderson's Solution Manual is the 4th edition; problems 1.1, 1.11 and 1.12 carry the same numbers as in the 6th."),
    }

    parts = []
    parts.append({"title": L("Không khí là một chất lưu", "Air is a fluid"),
                  "bullets": [L("Không khí gồm chủ yếu nitơ và oxy, là chất lưu vì có thể chảy và nhận hình dạng bình chứa", "Air is mostly nitrogen and oxygen, and is a fluid because it can flow and take the shape of its container"),
                              L("Khác nước ở chỗ không khí nén được", "Unlike water, air is compressible"),
                              L("Khí động lực học nghiên cứu vật chuyển động trong không khí và các lực sinh ra", "Aerodynamics studies bodies moving through air and the forces produced")],
                  "slides": [
                      {"title": L("Aerodynamics là gì và vì sao kỹ thuật viên cần biết", "What aerodynamics is and why a technician needs it"),
                       "body": ul(L("\"aero\" là không khí, \"dyne\" là lực: khí động lực học nghiên cứu vật chuyển động trong không khí và các lực gây ra hoặc thay đổi chuyển động đó", "\"aero\" means air and \"dyne\" means force: aerodynamics studies objects moving through air and the forces that produce or change that motion"),
                                  L("Hiểu vì sao bề mặt phải trơn khí động và vì sao có điều khiển chính, phụ là điều kiện để bảo dưỡng đúng máy bay hiện đại", "Knowing why surfaces must be aerodynamically smooth and why primary and secondary controls exist is essential to maintain modern aircraft"),
                                  L("Về khí động học, máy bay là một vật đi qua không gian và chịu ảnh hưởng của thay đổi điều kiện khí quyển", "Aerodynamically, an aircraft is an object travelling through space and affected by changes in atmospheric conditions")),
                       "explain": L("Hình dung bạn thò tay ra ngoài cửa xe đang chạy: tay chịu lực dù không chạm vật rắn nào. Không khí chuyển động tương đối so với vật tạo ra lực, và đó là điều toàn bộ môn học này mô tả.", "Imagine putting your hand out of a moving car window: it feels a force although it touches nothing solid. Air moving relative to a body produces force, and that is what this whole course describes.")},
                      {"title": L("Ba đại lượng của không khí: p, ρ, T", "Three air properties: p, ρ, T"),
                       "body": ul(L("Áp suất p (N/m² hay Pa): lực trên một đơn vị diện tích", "Pressure p (N/m² or Pa): force per unit area"),
                                  L("Mật độ ρ (kg/m³): khối lượng trên một đơn vị thể tích", "Density ρ (kg/m³): mass per unit volume"),
                                  L("Nhiệt độ T (kelvin): đo năng lượng chuyển động nhiệt của phân tử", "Temperature T (kelvin): a measure of the thermal motion of the molecules"),
                                  L("Ở điều kiện gần chuẩn, ba đại lượng liên hệ bằng phương trình trạng thái khí lý tưởng p = ρRT với R = 287 J/(kg·K) (Anderson 1.1)", "At near-standard conditions the three are linked by the perfect-gas equation of state p = ρRT with R = 287 J/(kg·K) (Anderson 1.1)")),
                       "explain": L("Biết hai trong ba đại lượng là tính được đại lượng còn lại. Nhớ đổi nhiệt độ sang kelvin: K = °C + 273,15.", "Knowing two of the three gives the third. Remember to convert temperature to kelvin: K = °C + 273.15.")}]})
    parts.append({"title": L("Áp suất khí quyển và đơn vị", "Atmospheric pressure and its units"),
                  "bullets": [L("Áp suất khí quyển là trọng lượng cột không khí phía trên chia cho diện tích", "Atmospheric pressure is the weight of the air column above divided by the area"),
                              L("Mức biển chuẩn: 1 atm = 14,7 psi = 29,92 inHg = 1013,2 mb (hPa) = 760 mmHg", "Standard sea level: 1 atm = 14.7 psi = 29.92 inHg = 1013.2 mb (hPa) = 760 mmHg"),
                              L("Áp suất giảm nhanh theo độ cao", "Pressure falls quickly with altitude")],
                  "slides": [
                      {"title": L("P = F/A và khí áp kế", "P = F/A and the barometer"),
                       "body": ul(L("Lực F = diện tích A × áp suất P, nên P = F/A", "Force F = area A × pressure P, so P = F/A"),
                                  L("Cột không khí 1 inch vuông từ mực biển lên đỉnh khí quyển nặng khoảng 14,7 lb, nên áp suất mực biển là 14,7 psi", "A one-square-inch column of air from sea level to the top of the atmosphere weighs about 14.7 lb, so sea-level pressure is 14.7 psi"),
                                  L("Khí áp kế (barometer) dùng cột thủy ngân đo áp suất theo inch thủy ngân (inHg)", "A barometer uses a mercury column and reads pressure in inches of mercury (inHg)"),
                                  L("Khí tượng hiện nay dùng hectopascal: 1 hPa = 100 Pa", "Meteorology now uses the hectopascal: 1 hPa = 100 Pa")),
                       "explain": L("Áp suất không phải một lực riêng: nó là lực phân bố trên diện tích, giống như cùng một vật nặng ấn sâu hơn qua gót giày nhọn so với đế bằng.", "Pressure is not a separate force: it is force spread over an area, just as the same weight presses deeper through a stiletto heel than through a flat sole.")},
                      {"title": L("Bảng quy đổi đơn vị tại mực biển chuẩn", "Unit conversion at standard sea level"),
                       "body": table([L("Đơn vị", "Unit"), L("Giá trị của 1 atm", "Value of 1 atm")],
                                     [["psi", N(P0 / PSI, 2)], ["inHg", N(P0 / 3386.389, 2)], ["hPa = mb", N(P0 / 100, 1)], ["mmHg", N(P0 / 133.322, 0)], ["Pa", N(P0, 0)]]) +
                       f"<p class='pill'>{L('Tính từ 101 325 Pa; EASA Hình 1-3 ghi 14,7 psi, 29,92 inHg, 1013,2 mb, 760 mmHg', 'Computed from 101 325 Pa; EASA Figure 1-3 gives 14.7 psi, 29.92 inHg, 1013.2 mb, 760 mmHg')}</p>"},
                      {"title": L("Áp suất giảm theo độ cao", "Pressure decreases with altitude"),
                       "body": ul(L("Cột không khí phía trên ngắn hơn nên nhẹ hơn, áp suất giảm", "The air column above is shorter and lighter, so pressure drops"),
                                  L(f"Ở 40 000 ft áp suất chỉ còn {N(p40 / PSI, 2)} psi (EASA Hình 1-4 ghi 2,72 psi), khoảng một phần sáu giá trị mực biển", f"At 40 000 ft pressure is only {N(p40 / PSI, 2)} psi (EASA Figure 1-4 gives 2.72 psi), about one sixth of the sea-level value"),
                                  L("Ở 50 000 ft áp suất gần bằng một phần mười giá trị mực biển (EASA)", "At 50 000 ft pressure is almost one tenth of sea level (EASA)"),
                                  L("Khi lên cao, áp suất, lượng oxy và nhiệt độ đều giảm, ảnh hưởng đến lực nâng và công suất động cơ", "As an aircraft climbs, pressure, oxygen and temperature all drop, affecting lift and engine power")),
                       "explain": L("Con số 2,72 psi ở 40 000 ft được kiểm bằng công thức ISA bên dưới, khớp tới hai chữ số thập phân.", "The 2.72 psi at 40 000 ft is checked with the ISA formula below and agrees to two decimals.")}]})
    parts.append({"title": L("Mật độ và độ ẩm", "Density and humidity"),
                  "bullets": [L("Mật độ tỉ lệ thuận với áp suất và tỉ lệ nghịch với nhiệt độ", "Density is proportional to pressure and inversely proportional to temperature"),
                              L("Không khí ẩm nhẹ hơn không khí khô", "Humid air is lighter than dry air"),
                              L("Mật độ thấp làm giảm lực nâng, lực đẩy và kéo dài quãng đường cất cánh", "Low density reduces lift and thrust and lengthens the take-off run")],
                  "slides": [
                      {"title": L("Hai quy tắc về mật độ", "Two rules for density"),
                       "body": ul(L("Mật độ biến thiên tỉ lệ thuận với áp suất", "Density varies directly with pressure"),
                                  L("Mật độ biến thiên tỉ lệ nghịch với nhiệt độ", "Density varies inversely with temperature"),
                                  L("Vì vậy không khí trên cao loãng hơn dưới thấp, và khối khí nóng loãng hơn khối khí lạnh", "So high-altitude air is thinner than low-altitude air, and a hot air mass is thinner than a cold one"),
                                  L("Máy bay bay nhanh hơn ở độ cao lớn vì ít hạt khí trên mỗi đơn vị thể tích nên lực cản nhỏ hơn", "An aircraft can fly faster at high altitude because there are fewer air particles per unit volume, so less resistance")),
                       "explain": L("Cả hai quy tắc là hệ quả của p = ρRT: giữ T không đổi thì ρ tăng theo p; giữ p không đổi thì ρ giảm khi T tăng.", "Both rules follow from p = ρRT: at constant T density rises with p; at constant p density falls as T rises.")},
                      {"title": L("Độ ẩm làm không khí nhẹ hơn", "Humidity makes air lighter"),
                       "body": ul(L("Độ ẩm tuyệt đối: khối lượng hơi nước trên một đơn vị thể tích không khí", "Absolute humidity: mass of water vapour per unit volume of air"),
                                  L("Độ ẩm tương đối: tỉ số phần trăm giữa lượng hơi nước hiện có và lượng hơi nước khi bão hòa ở cùng nhiệt độ và áp suất", "Relative humidity: the percentage ratio of the water vapour present to the amount at saturation at the same temperature and pressure"),
                                  L("Hơi nước nặng khoảng 5/8 không khí khô cùng thể tích, nên không khí ẩm có mật độ thấp hơn", "Water vapour weighs about 5/8 as much as the same volume of dry air, so humid air has lower density"),
                                  L("Ngày ẩm, máy bay cần đường băng cất cánh dài hơn ngày khô", "On damp days an aircraft needs a longer take-off runway than on dry days")),
                       "explain": L("Nhiều người nghĩ không khí ẩm \"nặng\" hơn. Thực ra phân tử nước (khối lượng 18) thay chỗ phân tử nitơ hay oxy (28 và 32), nên hỗn hợp nhẹ đi.", "Many people think humid air is \"heavy\". In fact a water molecule (mass 18) replaces a nitrogen or oxygen molecule (28 and 32), so the mixture gets lighter.")}]})
    parts.append({"title": L("Nhiệt độ và các tầng khí quyển", "Temperature and the atmospheric layers"),
                  "bullets": [L("Tầng đối lưu (troposphere): nhiệt độ giảm khoảng 2 °C mỗi 1 000 ft", "Troposphere: temperature falls about 2 °C per 1 000 ft"),
                              L("Đỉnh tầng đối lưu (tropopause) khoảng −57 °C", "The tropopause is about −57 °C"),
                              L("Phần lớn hàng không dân dụng bay trong tầng đối lưu", "Most civil aviation takes place in the troposphere")],
                  "slides": [
                      {"title": L("Tầng đối lưu và tropopause", "Troposphere and tropopause"),
                       "body": ul(L("Trung bình tầng đối lưu từ mặt đất lên khoảng 38 000 ft; trên hai cực chỉ 25 000 đến 30 000 ft, trên xích đạo tới khoảng 60 000 ft", "On average the troposphere reaches about 38 000 ft; over the poles only 25 000–30 000 ft, at the equator about 60 000 ft"),
                                  L("Nhiệt độ giảm gần như đều, khoảng −2 °C hay −3,5 °F mỗi 1 000 ft", "Temperature falls almost steadily, about −2 °C or −3.5 °F per 1 000 ft"),
                                  L("Biên trên là tropopause, vùng nhiệt độ gần như không đổi −57 °C (−69 °F)", "The upper boundary is the tropopause, a zone of nearly constant −57 °C (−69 °F)")),
                       "explain": L("−2 °C mỗi 1 000 ft tương đương khoảng −6,5 °C mỗi km, đúng bằng gradient 0,0065 K/m dùng trong ISA bên dưới.", "−2 °C per 1 000 ft is about −6.5 °C per km, exactly the 0.0065 K/m gradient used in ISA below.")},
                      {"title": L("Các tầng phía trên", "The layers above"),
                       "body": ul(L("Stratosphere (tầng bình lưu): nhiệt độ tăng theo độ cao, tới gần 0 °C; chứa tầng ôzôn chắn tia cực tím", "Stratosphere: temperature rises with altitude to near 0 °C; it holds the ozone layer that blocks ultraviolet rays"),
                                  L("Mesosphere (tầng trung quyển): nhiệt độ lại giảm", "Mesosphere: temperature falls again"),
                                  L("Thermosphere (tầng nhiệt quyển) nằm trên cùng", "The thermosphere lies above"),
                                  L("Một số chuyến bay dân dụng và nhiều chuyến bay quân sự diễn ra trong tầng bình lưu", "Some civil and many military flights take place in the stratosphere")),
                       "explain": L("Nhiệt độ không giảm mãi theo độ cao: trong tầng bình lưu ôzôn hấp thụ tia cực tím nên không khí nóng lên. Lưu ý: mô hình ISA giữ nhiệt độ không đổi từ 11 đến 20 km, nên bảng ISA không thể hiện phần nóng lên này.", "Temperature does not fall forever with height: in the stratosphere ozone absorbs ultraviolet and the air warms. Note that ISA holds temperature constant from 11 to 20 km, so the ISA table does not show this warming.")}]})
    parts.append({"title": L("Khí quyển chuẩn quốc tế ISA", "The International Standard Atmosphere (ISA)"),
                  "bullets": [L("Khí quyển thật luôn thay đổi, nên cần một mô hình chuẩn để so sánh và hiệu chuẩn", "The real atmosphere always changes, so a standard model is needed for comparison and calibration"),
                              L("ISA mực biển: 15 °C, 1013,25 hPa, mật độ 1,225 kg/m³", "ISA at sea level: 15 °C, 1013.25 hPa, density 1.225 kg/m³"),
                              L("Do ICAO, ISO và các chính phủ ban hành", "Published by ICAO, ISO and governments")],
                  "slides": [
                      {"title": L("Bảng ISA tính lại", "ISA table recomputed"),
                       "body": table([L("Độ cao (ft)", "Altitude (ft)"), L("Nhiệt độ (°C)", "Temp (°C)"), "p (hPa)", "p (psi)", "ρ (kg/m³)"], isa_rows) +
                       f"<p class='pill'>{L('Tính từ gradient −6,5 K/km tới 11 km, đẳng nhiệt 216,65 K trên đó (aero.py). EASA Hình 1-7 ghi mực biển 14,67 psi, 1013,53 hPa, 1,23 kg/m³ và các bước 1 000 ft: khớp với giá trị tính tới làm tròn.', 'Computed with −6.5 K/km up to 11 km and isothermal 216.65 K above (aero.py). EASA Figure 1-7 lists sea level 14.67 psi, 1013.53 hPa, 1.23 kg/m³ and 1 000 ft steps: they agree to rounding.')}</p>",
                       "explain": L("11 000 m tương ứng 36 089 ft: đây là đỉnh tầng đối lưu của ISA. Mật độ ở đó chỉ còn khoảng 30% mực biển.", "11 000 m is 36 089 ft: the ISA tropopause. Density there is only about 30% of sea level.")},
                      {"title": L("Ứng dụng: độ cao mật độ", "Application: density altitude"),
                       "body": ul(L("ISA là cơ sở của đồng hồ độ cao, tính năng máy bay và so sánh giữa các hãng", "ISA underlies the altimeter, aircraft performance figures and comparisons between manufacturers"),
                                  L(f"Ví dụ minh họa: sân bay ở 5 000 ft, nhiệt độ 30 °C (cao hơn ISA khoảng {N(isa_dev, 0)} °C). Mật độ thật {N(rho_hot, 3)} kg/m³ chỉ bằng {N(ratio * 100, 0)}% mực biển chuẩn, tương đương độ cao mật độ khoảng {N(dens_alt_ft, 0)} ft", f"Illustrative example: an airport at 5 000 ft and 30 °C (about {N(isa_dev, 0)} °C above ISA). The real density {N(rho_hot, 3)} kg/m³ is only {N(ratio * 100, 0)}% of standard sea level, equivalent to a density altitude of about {N(dens_alt_ft, 0)} ft"),
                                  L("Vì vậy ngày nóng, sân bay cao, máy bay cất cánh kém hơn", "That is why take-off performance suffers on hot days at high airports")),
                       "explain": L("Độ cao mật độ là độ cao trong ISA có cùng mật độ với không khí thực tế. Nó cho biết máy bay \"cảm thấy\" mình đang ở độ cao nào.", "Density altitude is the altitude in ISA that has the same density as the actual air. It tells how high the aircraft effectively \"feels\" it is.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Phương trình trạng thái và khí quyển chuẩn", "Equation of state and the standard atmosphere")
    m["formula_math"] = ("p = F/A  ·  p = ρ R T  ·  R = 287 J/(kg·K)<br>T = T₀ + λh  (λ = −0,0065 K/m)  ·  p = p₀ (T/T₀)^(−g/λR)  ·  ρ = p/RT" if lang == "vi" else
                         "p = F/A  ·  p = ρ R T  ·  R = 287 J/(kg·K)<br>T = T₀ + λh  (λ = −0.0065 K/m)  ·  p = p₀ (T/T₀)^(−g/λR)  ·  ρ = p/RT")
    m["legend"] = [("p", L("áp suất (Pa)", "pressure (Pa)")), ("ρ", L("mật độ (kg/m³)", "density (kg/m³)")), ("T", L("nhiệt độ tuyệt đối (K)", "absolute temperature (K)")),
                   ("λ", L("gradient nhiệt độ tầng đối lưu", "tropospheric lapse rate")), ("h", L("độ cao (m)", "altitude (m)")), ("g", "9,80665 m/s²" if lang == "vi" else "9.80665 m/s²")]
    m["history_title"] = L("Từ ống Torricelli đến ISA", "From Torricelli's tube to ISA")
    m["history"] = L("Năm 1643, Evangelista Torricelli chế tạo khí áp kế thủy ngân đầu tiên và chứng minh không khí có trọng lượng. Năm 1648 Florin Périer, theo yêu cầu của Blaise Pascal, mang khí áp kế lên núi Puy de Dôme và thấy cột thủy ngân thấp hơn ở trên cao, xác nhận áp suất giảm theo độ cao. Về sau ICAO, ISO và các chính phủ thống nhất khí quyển chuẩn để mọi đồng hồ độ cao và bảng tính năng dùng chung một nền (EASA, tr. 1.5).",
                     "In 1643 Evangelista Torricelli built the first mercury barometer and showed that air has weight. In 1648 Florin Périer, at Blaise Pascal's request, carried a barometer up the Puy de Dôme and saw the mercury column fall at height, confirming that pressure drops with altitude. Later ICAO, ISO and governments agreed one standard atmosphere so that every altimeter and performance table share a common baseline (EASA, p. 1.5).")
    m["case_title"] = L("Tình huống: Zeppelin và cánh Boeing 727", "Case: a Zeppelin and a Boeing 727 wing")
    m["case"] = L(f"Anderson 1.1: tại một điểm trên cánh Boeing 727, p = 1,9×10⁴ N/m² và T = 203 K, nên ρ = p/RT = {N(rho_11a, 3)} kg/m³, chỉ khoảng một phần ba mật độ mực biển. Anderson 1.12: Zeppelin thể tích 15 000 m³ bay ở 1 000 m (ρ ISA = {N(rho1000, 4)} kg/m³) chịu lực đẩy Archimedes {N(B / 1e5, 3)}×10⁵ N cộng lực nâng khí động {N(Lz, 0)} N, nên tổng trọng lượng là {N(W / 1e5, 3)}×10⁵ N. Lực đẩy Archimedes gánh gần hết trọng lượng; lực nâng khí động chỉ chiếm {N(Lz / W * 100, 1)}%.",
                  f"Anderson 1.1: at a point on a Boeing 727 wing, p = 1.9×10⁴ N/m² and T = 203 K, so ρ = p/RT = {N(rho_11a, 3)} kg/m³, about a third of sea-level density. Anderson 1.12: a 15 000 m³ Zeppelin flying at 1 000 m (ISA ρ = {N(rho1000, 4)} kg/m³) is supported by Archimedes buoyancy of {N(B / 1e5, 3)}×10⁵ N plus aerodynamic lift of {N(Lz, 0)} N, so the total weight is {N(W / 1e5, 3)}×10⁵ N. Buoyancy carries almost all the weight; aerodynamic lift is only {N(Lz / W * 100, 1)}%.")
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L("(1) Không khí ẩm nhẹ hơn, không nặng hơn, không khí khô. (2) Áp suất không giảm tuyến tính theo độ cao mà giảm gần như theo hàm mũ, nên ở 40 000 ft còn khoảng 1/6 chứ không phải 1/3. (3) Gradient −2 °C mỗi 1 000 ft chỉ đúng trong tầng đối lưu; trên tropopause nhiệt độ ISA không đổi. (4) Bài Anderson 1.12 có lực đẩy Archimedes: quên nó thì trọng lượng sai gấp hàng chục lần. (5) Solution Manual (bản 4th, đã kiểm trên ảnh trang 12) in L = 3487 N ở dòng tính lực nâng, nhưng 500 × 153,9 × 0,05 = 3847 N và dòng ngay sau lại dùng 3847 N để ra W = 1,67×10⁵ N: đáp án cuối đúng, chỉ có một lỗi đánh máy ở dòng giữa.",
                  "(1) Humid air is lighter, not heavier, than dry air. (2) Pressure does not fall linearly with altitude but roughly exponentially, so at 40 000 ft about 1/6 remains, not 1/3. (3) The −2 °C per 1 000 ft gradient holds only in the troposphere; above the tropopause ISA temperature is constant. (4) Anderson 1.12 includes Archimedes buoyancy: forgetting it makes the weight wrong by a large factor. (5) The Solution Manual (4th ed., checked on the page image, p. 12) prints L = 3487 N on the lift line, but 500 × 153.9 × 0.05 = 3847 N and the very next line uses 3847 N to reach W = 1.67×10⁵ N: the final answer is right and only the middle line has a typo.")
    m["nb_desc"] = L("Notebook cài đặt ISA bằng code, đối chiếu EASA Hình 1-4 và 1-7, giải lại các bài Anderson 1.1, 1.11, 1.12 và tự kiểm mọi đáp án quiz bằng assert.",
                     "The notebook implements ISA in code, checks it against EASA Figures 1-4 and 1-7, re-solves Anderson 1.1, 1.11 and 1.12 and self-checks every quiz answer with assert.")

    # ---------------- Quiz ----------------
    SD = lambda i: 100 + i
    easa = [
        mcq(SD(1), L("EASA M08 Q1-1 (tr. 1.7, đáp án tr. 1.8)", "EASA M08 Q1-1 (p. 1.7, answer p. 1.8)"),
            L("Áp suất khí quyển được đo bằng dụng cụ gọi là:", "Atmospheric pressure is measured with an instrument called a:"),
            L("khí áp kế (barometer)", "barometer"), [L("nhiệt kế (thermometer)", "thermometer"), L("ẩm kế (hygrometer)", "hygrometer"), L("tốc kế (tachometer)", "tachometer")],
            L("Khí áp kế thủy ngân đo áp suất theo inch thủy ngân (EASA tr. 1.2).", "A mercury barometer records pressure in inches of mercury (EASA p. 1.2).")),
        mcq(SD(2), L("EASA M08 Q1-2 (tr. 1.7, đáp án tr. 1.8)", "EASA M08 Q1-2 (p. 1.7, answer p. 1.8)"),
            L("Máy bay có thể bay ____ ở độ cao lớn, nơi mật độ không khí thấp, so với độ cao thấp nơi mật độ lớn hơn.", "An aircraft can fly ____ at a high altitude where the air density is low than at a low altitude where the air density is greater."),
            L("nhanh hơn", "faster"), [L("chậm hơn", "slower"), L("cao hơn", "higher"), L("lâu hơn", "longer")],
            L("Ít hạt khí hơn trên mỗi đơn vị thể tích nên lực cản nhỏ hơn (EASA tr. 1.4).", "Fewer particles per unit volume means less resistance (EASA p. 1.4).")),
        mcq(SD(3), L("EASA M08 Q1-3 (tr. 1.7, đáp án tr. 1.8)", "EASA M08 Q1-3 (p. 1.7, answer p. 1.8)"),
            L("Phần lớn hàng không dân dụng diễn ra ở tầng nào của khí quyển?", "In which layer of the atmosphere does most civilian aviation take place?"),
            L("Tầng đối lưu (troposphere)", "Troposphere"), [L("Tầng bình lưu (stratosphere)", "Stratosphere"), L("Tầng trung quyển (mesosphere)", "Mesosphere"), L("Tầng nhiệt quyển (thermosphere)", "Thermosphere")],
            L("Nhiệt độ giảm theo độ cao trong tầng đối lưu, nơi diễn ra hầu hết hàng không dân dụng (EASA tr. 1.5).", "Temperature falls with height in the troposphere, where most civil aviation takes place (EASA p. 1.5).")),
    ]
    book = [
        mcq(SD(11), "Anderson 6th, Problem 1.1a",
            L("Tại một điểm trên cánh Boeing 727, áp suất 1,9×10⁴ N/m² và nhiệt độ 203 K. Mật độ không khí tại điểm này (R = 287 J/(kg·K)) là:", "At a point on the wing of a Boeing 727 the pressure is 1.9×10⁴ N/m² and the temperature 203 K. The air density there (R = 287 J/(kg·K)) is:"),
            f"{N(rho_11a, 3)} kg/m³", [f"{N(rho_11a * 1.9, 3)} kg/m³", f"{N(rho_11a / 2.2, 3)} kg/m³", f"{N(1 / rho_11a, 2)} kg/m³"],
            L("ρ = p/(RT) = 1,9×10⁴/(287 × 203).", "ρ = p/(RT) = 1.9×10⁴/(287 × 203)."),
            L("<p>ρ = 1,9×10⁴/(287 × 203) = 1,9×10⁴/58 261 = 0,326 kg/m³. Solution Manual in cùng giá trị 0,326.</p>", "<p>ρ = 1.9×10⁴/(287 × 203) = 1.9×10⁴/58 261 = 0.326 kg/m³. The Solution Manual prints the same 0.326.</p>")),
        mcq(SD(12), "Anderson 6th, Problem 1.1b",
            L("Trong buồng thử của hầm gió siêu âm, p = 1058 lb/ft² và ρ = 1,23×10⁻³ slug/ft³. Nhiệt độ tại đó (R = 1716 ft·lb/(slug·°R)) là:", "In the test section of a supersonic wind tunnel p = 1058 lb/ft² and ρ = 1.23×10⁻³ slug/ft³. The temperature there (R = 1716 ft·lb/(slug·°R)) is:"),
            f"{N(T_11b, 0)} °R", [f"{N(T_11b * 0.62, 0)} °R", f"{N(T_11b * 1.7, 0)} °R", f"{N(T_11b - 460, 0)} °R"],
            L("T = p/(ρR) = 1058/(1,23×10⁻³ × 1716).", "T = p/(ρR) = 1058/(1.23×10⁻³ × 1716)."),
            L("<p>T = 1058/2,1107 = 501 °R, khoảng 41 °F hay 278 K. Rankine là thang nhiệt độ tuyệt đối.</p>", "<p>T = 1058/2.1107 = 501 °R, about 41 °F or 278 K. Rankine is an absolute scale.</p>")),
        mcq(SD(13), "Anderson 6th, Problem 1.11",
            L("Áp kế chữ U thủy ngân nối với mô hình hầm gió; phía kia thông khí quyển (1,01×10⁵ N/m²). Hai cột thủy ngân chênh 20 cm, cột cao ở phía mô hình. Áp suất trên cánh là (ρ_Hg = 1,36×10⁴ kg/m³, g = 9,8 m/s²):", "A mercury U-tube manometer connects the wind-tunnel model to the atmosphere (1.01×10⁵ N/m²). The two mercury columns differ by 20 cm, with the high column on the model side. The pressure on the wing is (ρ_Hg = 1.36×10⁴ kg/m³, g = 9.8 m/s²):"),
            f"{N(p_11 / 1e4, 2)}×10⁴ N/m²", [f"{N((1.01e5 + 1.36e4 * 9.8 * 0.2) / 1e4, 2)}×10⁴ N/m²", f"{N(1.36e4 * 9.8 * 0.2 / 1e4, 2)}×10⁴ N/m²", f"{N(1.01e5 / 1e4, 2)}×10⁴ N/m²"],
            L("Cột thủy ngân cao hơn nằm ở phía áp suất thấp hơn, nên p_mô hình = p_khí quyển − ρgh.", "The higher mercury column sits on the lower-pressure side, so p_model = p_atm − ρgh."),
            L(f"<p>p = 1,01×10⁵ − (1,36×10⁴)(9,8)(0,2) = 1,01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = {N(p_11, 0)} N/m². Khớp đáp án 7,43×10⁴ trong Solution Manual. Sai lầm phổ biến là cộng thay vì trừ.</p>", f"<p>p = 1.01×10⁵ − (1.36×10⁴)(9.8)(0.2) = 1.01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = {N(p_11, 0)} N/m². Matches the 7.43×10⁴ in the Solution Manual. The common slip is adding instead of subtracting.</p>")),
        mcq(SD(14), "Anderson 6th, Problem 1.12",
            L("Zeppelin thể tích 15 000 m³, đường kính lớn nhất 14 m, bay thẳng đều 30 m/s ở độ cao chuẩn 1 000 m (ρ = 1,1117 kg/m³) với C_L = 0,05 (tính theo tiết diện ngang lớn nhất). Tổng trọng lượng là:", "A Zeppelin of 15 000 m³ and 14 m maximum diameter flies straight and level at 30 m/s at a standard altitude of 1 000 m (ρ = 1.1117 kg/m³) with C_L = 0.05 (based on maximum cross-section). Its total weight is:"),
            f"{N(W / 1e5, 3)}×10⁵ N", [f"{N(Lz, 0)} N", f"{N((B - Lz) / 1e5, 3)}×10⁵ N", f"{N(B * 2 / 1e5, 3)}×10⁵ N"],
            L("W = lực đẩy Archimedes B + lực nâng khí động L.", "W = Archimedes buoyancy B + aerodynamic lift L."),
            L(f"<p>B = 15 000 × 1,1117 × 9,8 = {N(B, 0)} N; q = ½ρV² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m²; L = qSC_L = {N(Lz, 0)} N; W = B + L = {N(W, 0)} N. Chỉ tính lực nâng khí động sẽ ra đáp án sai ({N(Lz, 0)} N).</p>", f"<p>B = 15 000 × 1.1117 × 9.8 = {N(B, 0)} N; q = ½ρV² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m²; L = qSC_L = {N(Lz, 0)} N; W = B + L = {N(W, 0)} N. Counting only aerodynamic lift gives the wrong answer ({N(Lz, 0)} N).</p>")),
    ]
    T11 = isa(11000)[0] - 273.15
    T30 = isa_ft(30000)[0] - 273.15
    rho_ratio = isa_ft(36089)[2] / RHO0
    SUP = L("Bổ sung (biên soạn)", "Supplementary (authored)")
    gen = [
        mcq(SD(21), SUP, L("Tại 40 000 ft theo ISA, áp suất còn khoảng bao nhiêu so với mực biển?", "At 40 000 ft in ISA, roughly what fraction of the sea-level pressure remains?"),
            f"{N(p40 / P0 * 100, 0)}% ({N(p40 / PSI, 2)} psi)", [f"33% ({N(4.9, 1)} psi)", f"50% ({N(7.3, 1)} psi)", f"2% ({N(0.3, 1)} psi)"],
            L("Áp suất giảm theo hàm mũ chứ không tuyến tính; công thức ISA cho 2,72 psi.", "Pressure falls exponentially, not linearly; the ISA formula gives 2.72 psi.")),
        mcq(SD(22), SUP, L("Nhiệt độ ISA ở tropopause (11 000 m) là:", "The ISA temperature at the tropopause (11 000 m) is:"),
            f"{N(T11, 1)} °C", ["−40 °C", "0 °C", "−90 °C"],
            L("15 − 6,5 × 11 = −56,5 °C, EASA làm tròn −57 °C.", "15 − 6.5 × 11 = −56.5 °C, which EASA rounds to −57 °C.")),
        mcq(SD(23), SUP, L("Nhiệt độ ISA ở 30 000 ft (tầng đối lưu) xấp xỉ:", "The ISA temperature at 30 000 ft (troposphere) is approximately:"),
            f"{N(T30, 1)} °C", [f"{N(T30 + 25, 1)} °C", f"{N(T30 - 25, 1)} °C", "15 °C"],
            L("15 °C − 6,5 K/km × 9,144 km ≈ −44,4 °C, tương đương −2 °C mỗi 1 000 ft.", "15 °C − 6.5 K/km × 9.144 km ≈ −44.4 °C, i.e. −2 °C per 1 000 ft.")),
        mcq(SD(24), SUP, L("Giữ áp suất không đổi và tăng nhiệt độ tuyệt đối gấp đôi thì mật độ:", "At constant pressure, doubling the absolute temperature makes the density:"),
            L("giảm một nửa", "halve"), [L("tăng gấp đôi", "double"), L("không đổi", "stay the same"), L("giảm còn một phần tư", "fall to one quarter")],
            L("ρ = p/(RT): T gấp đôi thì ρ giảm một nửa.", "ρ = p/(RT): doubling T halves ρ.")),
        mcq(SD(25), SUP, L("Vì sao không khí ẩm có mật độ thấp hơn không khí khô ở cùng p và T?", "Why is humid air less dense than dry air at the same p and T?"),
            L("Phân tử nước nhẹ hơn phân tử N₂ và O₂ mà nó thay thế", "A water molecule is lighter than the N₂ and O₂ molecules it replaces"),
            [L("Hơi nước làm tăng nhiệt độ không khí", "Water vapour raises the air temperature"), L("Hơi nước làm tăng áp suất khí quyển", "Water vapour raises the atmospheric pressure"), L("Hơi nước nặng hơn nhưng nở ra nhiều hơn", "Water vapour is heavier but expands more")],
            L("EASA: hơi nước nặng khoảng 5/8 không khí khô cùng thể tích.", "EASA: water vapour weighs about 5/8 as much as the same volume of dry air.")),
        mcq(SD(26), SUP, L("Tại tropopause ISA (36 089 ft), mật độ so với mực biển xấp xỉ:", "At the ISA tropopause (36 089 ft), density relative to sea level is about:"),
            f"{N(rho_ratio, 2)}", [N(0.70, 2), N(0.50, 2), N(0.10, 2)],
            L("σ = 0,3639/1,225 ≈ 0,30.", "σ = 0.3639/1.225 ≈ 0.30.")),
        mcq(SD(27), SUP, L("1 atm bằng bao nhiêu hPa?", "1 atm equals how many hPa?"),
            N(1013.25, 2), ["760", N(14.7, 1), N(29.92, 2)],
            L("760 là mmHg, 14,7 là psi, 29,92 là inHg: cùng áp suất, khác đơn vị.", "760 is mmHg, 14.7 is psi, 29.92 is inHg: same pressure, different units.")),
        mcq(SD(28), SUP, L("Ngày nóng và ẩm tại sân bay cao thì quãng đường cất cánh:", "On a hot, humid day at a high-altitude airport, the take-off run is:"),
            L("dài hơn vì mật độ thấp", "longer because density is low"), [L("ngắn hơn vì không khí nhẹ", "shorter because the air is light"), L("không đổi vì ISA cố định", "unchanged because ISA is fixed"), L("ngắn hơn vì lực cản giảm", "shorter because drag falls")],
            L("Mật độ thấp giảm lực nâng và lực đẩy; lực cản giảm nhưng không bù được.", "Low density reduces lift and thrust; drag falls too but does not compensate.")),
    ]
    m["quiz_sets"] = [
        {"key": "easa", "title": L("Sách 1: EASA Module 08, câu hỏi cuối Sub-module 01 (3 câu, đã chuyển từ điền khuyết sang trắc nghiệm)", "Book 1: EASA Module 08, end of Sub-module 01 (3 questions, converted from fill-in to multiple choice)"),
         "intro": L("Đề gốc là điền khuyết; đáp án đúng giữ nguyên như bản in (tr. 1.8), ba phương án sai do module biên soạn.", "The originals are fill-in-the-blank; the right answer is exactly the printed one (p. 1.8) and the three wrong options are authored by this module."), "items": easa},
        {"key": "anderson", "title": L("Sách 2: Anderson, bài tập cuối chương 1 (mục 1.17), đáp án tính lại bằng Python", "Book 2: Anderson, end-of-chapter 1 problems (sec. 1.17), answers recomputed in Python"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập bổ sung (biên soạn thêm, đáp án tự kiểm chứng bằng tính toán)", "Additional practice (authored, answers self-verified by computation)"), "items": gen},
    ]
    m["problems_intro"] = L("Ba bài của Anderson (cuối chương 1) giải từng bước. Số liệu lấy từ bản 6th; lời giải được tính lại và đối chiếu Solution Manual (bản 4th, chữ viết tay).",
                            "Three Anderson end-of-chapter-1 problems solved step by step. Data are from the 6th edition; solutions are recomputed here and cross-checked against the Solution Manual (4th edition, handwritten).")
    m["problems"] = [
        {"num": "1.1", "src": "Anderson 6th, Problem 1.1", "q": L("(a) p = 1,9×10⁴ N/m², T = 203 K: tính ρ. (b) p = 1058 lb/ft², ρ = 1,23×10⁻³ slug/ft³: tính T.", "(a) p = 1.9×10⁴ N/m², T = 203 K: find ρ. (b) p = 1058 lb/ft², ρ = 1.23×10⁻³ slug/ft³: find T."),
         "ans": L(f"<p>(a) ρ = p/(RT) = 1,9×10⁴/(287×203) = <b>{N(rho_11a, 3)} kg/m³</b>.</p><p>(b) T = p/(ρR) = 1058/(1,23×10⁻³×1716) = <b>{N(T_11b, 0)} °R</b>.</p><p class='pill'>Khớp Solution Manual.</p>", f"<p>(a) ρ = p/(RT) = 1.9×10⁴/(287×203) = <b>{N(rho_11a, 3)} kg/m³</b>.</p><p>(b) T = p/(ρR) = 1058/(1.23×10⁻³×1716) = <b>{N(T_11b, 0)} °R</b>.</p><p class='pill'>Matches the Solution Manual.</p>")},
        {"num": "1.11", "src": "Anderson 6th, Problem 1.11", "q": L("Áp kế chữ U thủy ngân: chênh 20 cm, cột cao ở phía mô hình, p_atm = 1,01×10⁵ N/m². Tính áp suất trên cánh mô hình.", "U-tube mercury manometer: 20 cm difference, high column on the model side, p_atm = 1.01×10⁵ N/m². Find the pressure on the model wing."),
         "ans": L(f"<p>Cột cao ở phía áp suất thấp: p = p_atm − ρ_Hg g h = 1,01×10⁵ − (1,36×10⁴)(9,8)(0,2) = <b>{N(p_11, 0)} N/m²</b> (7,43×10⁴).</p>", f"<p>The high column is on the low-pressure side: p = p_atm − ρ_Hg g h = 1.01×10⁵ − (1.36×10⁴)(9.8)(0.2) = <b>{N(p_11, 0)} N/m²</b> (7.43×10⁴).</p>")},
        {"num": "1.12", "src": "Anderson 6th, Problem 1.12", "q": L("Zeppelin: thể tích 15 000 m³, d_max = 14 m, V = 30 m/s ở 1 000 m chuẩn, C_L = 0,05. Tính tổng trọng lượng.", "Zeppelin: volume 15 000 m³, d_max = 14 m, V = 30 m/s at a standard 1 000 m, C_L = 0.05. Find the total weight."),
         "ans": L(f"<p>Cân bằng: W = B + L.</p><p>B = ρVg = 1,1117×15 000×9,8 = {N(B, 0)} N. q = ½ρV² = {N(q, 1)} Pa. S = π·14²/4 = {N(S, 1)} m². L = qSC_L = {N(Lz, 0)} N.</p><p><b>W = {N(W, 0)} N</b> (≈ {N(W / 1e5, 3)}×10⁵ N).</p><p class='pill'>Solution Manual in nhầm L = 3487 N ở dòng giữa (làm tròn q = 500 Pa cho 3847 N, không làm tròn cho 3850 N); đáp án cuối 1,67×10⁵ N vẫn đúng.</p>", f"<p>Equilibrium: W = B + L.</p><p>B = ρVg = 1.1117×15 000×9.8 = {N(B, 0)} N. q = ½ρV² = {N(q, 1)} Pa. S = π·14²/4 = {N(S, 1)} m². L = qSC_L = {N(Lz, 0)} N.</p><p><b>W = {N(W, 0)} N</b> (≈ {N(W / 1e5, 3)}×10⁵ N).</p><p class='pill'>The Solution Manual misprints L = 3487 N on the middle line (rounding q to 500 Pa gives 3847 N, unrounded gives 3850 N); its final 1.67×10⁵ N is right.</p>")},
    ]
    return m
