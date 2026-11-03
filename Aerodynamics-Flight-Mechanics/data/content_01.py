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
        isa_rows.append((f"{h:,}".replace(",", " "), N(T_ - 273.15, 1).replace("-", "−"), N(p_ / 100, 1), N(p_ / PSI, 2), N(r_, 4)))
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
    m["intro"] = L("Mọi lực khí động đều đến từ không khí, nên trước hết phải biết không khí đang ở trạng thái nào: áp suất, mật độ và nhiệt độ bao nhiêu. Module này đi qua ba đại lượng đó, cách chúng đổi theo độ cao và khí quyển chuẩn ISA, rồi dùng vào ba tình huống cụ thể: cánh Boeing 727 ở độ cao lớn, khí cầu Zeppelin và sân bay cao nguyên vào ngày nóng.",
                   "Every aerodynamic force comes from the air, so the first thing to know is the state of that air: its pressure, density and temperature. This module covers those three quantities, how they change with height and the International Standard Atmosphere (ISA), then puts them to work in three concrete cases: a Boeing 727 wing at altitude, a Zeppelin airship and a high-altitude airport on a hot day.")
    m["mapping"] = {
        "easa": L("Sub-module 01 Physics of the Atmosphere (tr. 1.1–1.8): áp suất, mật độ, độ ẩm, nhiệt độ và độ cao, ISA; 3 câu hỏi cuối chương (Q1-1 đến Q1-3)",
                  "Sub-module 01 Physics of the Atmosphere (pp. 1.1–1.8): pressure, density, humidity, temperature and altitude, ISA; 3 end-of-chapter questions (Q1-1 to Q1-3)"),
        "anderson": L("Ch.1 mục 1.4 (các đại lượng cơ bản: áp suất, mật độ, nhiệt độ), mục 1.9 (tĩnh học chất lưu), Phụ lục D/E (bảng khí quyển chuẩn); Bài 1.1, 1.11, 1.12 (mục 1.17 Problems)",
                      "Ch.1 sec. 1.4 (basic quantities: pressure, density, temperature), sec. 1.9 (fluid statics), Appendices D/E (standard atmosphere tables); Problems 1.1, 1.11, 1.12 (sec. 1.17)"),
        "etkin": L("Phụ lục D The Standard Atmosphere and Other Data (tr. 364–368); Ch.1 mục 1.1 (lực khí động là một trong các trường lực chính của cơ học bay)",
                   "Appendix D The Standard Atmosphere and Other Data (pp. 364–368); Ch.1 sec. 1.1 (the aerodynamic force field is one of the strong fields in flight dynamics)"),
        "note": L("EASA giải thích định tính và cho bảng ISA. Anderson có phương trình trạng thái p = ρRT cùng các bài tính. Etkin có bảng ISA đầy đủ, dùng trong các ví dụ Boeing 747. Solution Manual của Anderson là bản 4; ba bài 1.1, 1.11, 1.12 có số liệu giống bản 6.",
                  "EASA explains the topic qualitatively and gives an ISA table. Anderson gives the equation of state p = ρRT and the numeric problems. Etkin gives the full ISA table used in its Boeing 747 examples. Anderson's Solution Manual is the 4th edition; problems 1.1, 1.11 and 1.12 use the same numbers as the 6th."),
    }

    parts = []
    parts.append({"title": L("Không khí là một chất lưu", "Air is a fluid"),
                  "bullets": [L("Không khí chủ yếu là nitơ và oxy; nó là chất lưu vì chảy được và lấy hình dạng của bình chứa", "Air is mostly nitrogen and oxygen, and is a fluid because it can flow and take the shape of its container"),
                              L("Khác nước, không khí nén được", "Unlike water, air is compressible"),
                              L("Khí động lực học nghiên cứu vật chuyển động trong không khí và các lực sinh ra", "Aerodynamics studies bodies moving through air and the forces produced")],
                  "slides": [
                      {"title": L("Khí động lực học (aerodynamics) là gì và học để làm gì", "What aerodynamics is and why it matters"),
                       "body": ul(L("\"aero\" nghĩa là không khí, \"dyne\" nghĩa là lực. Khí động lực học nghiên cứu vật chuyển động trong không khí và những lực sinh ra hoặc làm thay đổi chuyển động đó", "\"aero\" means air and \"dyne\" means force. Aerodynamics studies objects moving through air and the forces that produce or change that motion"),
                                  L("Muốn bảo dưỡng đúng một máy bay hiện đại, phải hiểu vì sao bề mặt của nó cần nhẵn khí động và vì sao có cả điều khiển chính lẫn điều khiển phụ", "To maintain a modern aircraft properly you need to know why its surfaces must be aerodynamically smooth and why it has both primary and secondary controls"),
                                  L("Với khí động học, máy bay là một vật chuyển động trong không gian, chịu ảnh hưởng khi điều kiện khí quyển thay đổi", "Aerodynamically, an aircraft is an object travelling through space and affected by changes in atmospheric conditions")),
                       "explain": L("Thử thò tay ra ngoài cửa xe đang chạy: tay bị đẩy dù không chạm vào vật rắn nào. Không khí chuyển động so với một vật thì tạo ra lực lên vật đó, và cả môn học này là để mô tả lực ấy.", "Hold your hand out of a moving car window: it is pushed even though it touches nothing solid. Air moving relative to a body puts a force on it, and this whole course is about describing that force.")},
                      {"title": L("Ba đại lượng của không khí: p, ρ, T", "Three air properties: p, ρ, T"),
                       "body": ul(L("Áp suất p (N/m² hay Pa): lực trên một đơn vị diện tích", "Pressure p (N/m² or Pa): force per unit area"),
                                  L("Mật độ ρ (kg/m³): khối lượng trên một đơn vị thể tích", "Density ρ (kg/m³): mass per unit volume"),
                                  L("Nhiệt độ T (kelvin): đo năng lượng chuyển động nhiệt của phân tử", "Temperature T (kelvin): a measure of the thermal motion of the molecules"),
                                  L("Với không khí ở điều kiện thông thường, ba đại lượng nối với nhau bằng phương trình trạng thái khí lý tưởng p = ρRT, R = 287 J/(kg·K) (Anderson 1.1)", "At near-standard conditions the three are linked by the perfect-gas equation of state p = ρRT with R = 287 J/(kg·K) (Anderson 1.1)")),
                       "explain": L("Biết hai trong ba đại lượng là tính được đại lượng còn lại. Nhớ đổi nhiệt độ sang kelvin trước khi thay vào: K = °C + 273,15.", "Knowing two of the three gives the third. Remember to convert temperature to kelvin: K = °C + 273.15.")}]})
    parts.append({"title": L("Áp suất khí quyển và đơn vị", "Atmospheric pressure and its units"),
                  "bullets": [L("Áp suất khí quyển là trọng lượng cột không khí phía trên chia cho diện tích", "Atmospheric pressure is the weight of the air column above divided by the area"),
                              L("Mức biển chuẩn: 1 atm = 14,7 psi = 29,92 inHg = 1013,2 mb (hPa) = 760 mmHg", "Standard sea level: 1 atm = 14.7 psi = 29.92 inHg = 1013.2 mb (hPa) = 760 mmHg"),
                              L("Áp suất giảm nhanh theo độ cao", "Pressure falls quickly with altitude")],
                  "slides": [
                      {"title": L("P = F/A và khí áp kế", "P = F/A and the barometer"),
                       "body": ul(L("Lực F = diện tích A × áp suất P, nên P = F/A", "Force F = area A × pressure P, so P = F/A"),
                                  L("Cột không khí tiết diện 1 inch vuông, từ mực biển lên hết khí quyển, nặng khoảng 14,7 lb, nên áp suất mực biển là 14,7 psi", "A one-square-inch column of air from sea level to the top of the atmosphere weighs about 14.7 lb, so sea-level pressure is 14.7 psi"),
                                  L("Khí áp kế (barometer) dùng một cột thủy ngân và đọc áp suất bằng chiều cao cột đó, tính theo inch thủy ngân (inHg)", "A barometer uses a mercury column and reads pressure in inches of mercury (inHg)"),
                                  L("Ngành khí tượng ngày nay dùng hectopascal: 1 hPa = 100 Pa", "Meteorology now uses the hectopascal: 1 hPa = 100 Pa")),
                       "explain": L("Áp suất là lực chia đều trên một diện tích. Cùng một người nặng, đứng bằng gót giày nhọn thì lún sâu hơn đứng bằng đế bằng, vì lực dồn vào diện tích nhỏ hơn.", "Pressure is force spread over an area. The same person sinks deeper in a stiletto heel than in a flat sole because the force is concentrated on a smaller area.")},
                      {"title": L("Bảng quy đổi đơn vị tại mực biển chuẩn", "Unit conversion at standard sea level"),
                       "body": table([L("Đơn vị", "Unit"), L("Giá trị của 1 atm", "Value of 1 atm")],
                                     [["psi", N(P0 / PSI, 2)], ["inHg", N(P0 / 3386.389, 2)], ["hPa = mb", N(P0 / 100, 1)], ["mmHg", N(P0 / 133.322, 0)], ["Pa", N(P0, 0)]]) +
                       f"<p class='pill'>{L('Tính từ 101 325 Pa. EASA Hình 1-3 ghi 14,7 psi, 29,92 inHg, 1013,2 mb và 760 mmHg.', 'Computed from 101 325 Pa. EASA Figure 1-3 gives 14.7 psi, 29.92 inHg, 1013.2 mb and 760 mmHg.')}</p>"},
                      {"title": L("Áp suất giảm theo độ cao", "Pressure decreases with altitude"),
                       "body": ul(L("Lên cao thì cột không khí phía trên ngắn và nhẹ hơn, nên áp suất giảm", "The air column above is shorter and lighter, so pressure drops"),
                                  L(f"Ở 40 000 ft áp suất chỉ còn {N(p40 / PSI, 2)} psi (EASA Hình 1-4 cũng ghi 2,72 psi), chưa đến một phần năm giá trị ở mực biển", f"At 40 000 ft pressure is only {N(p40 / PSI, 2)} psi (EASA Figure 1-4 also gives 2.72 psi), less than a fifth of the sea-level value"),
                                  L("Ở 50 000 ft, theo EASA, áp suất chỉ còn gần một phần mười giá trị mực biển", "At 50 000 ft pressure is almost one tenth of sea level (EASA)"),
                                  L("Càng lên cao, áp suất, lượng oxy và nhiệt độ đều giảm, và điều đó ảnh hưởng đến lực nâng và công suất động cơ", "As an aircraft climbs, pressure, oxygen and temperature all drop, affecting lift and engine power")),
                       "explain": L("Áp suất giảm theo kiểu nhân chứ không giảm đều: cứ lên thêm khoảng 5,5 km là áp suất mất đi một nửa. Vì vậy ở 40 000 ft (khoảng 12 km) đã mất hơn 80%.", "Pressure falls by a constant factor, not a constant amount: it halves for roughly every 5.5 km of climb. So by 40 000 ft (about 12 km) more than 80% of it is gone.")}]})
    parts.append({"title": L("Mật độ và độ ẩm", "Density and humidity"),
                  "bullets": [L("Mật độ tỉ lệ thuận với áp suất và tỉ lệ nghịch với nhiệt độ", "Density is proportional to pressure and inversely proportional to temperature"),
                              L("Không khí ẩm nhẹ hơn không khí khô", "Humid air is lighter than dry air"),
                              L("Mật độ thấp làm giảm lực nâng, lực đẩy và kéo dài quãng đường cất cánh", "Low density reduces lift and thrust and lengthens the take-off run")],
                  "slides": [
                      {"title": L("Hai quy tắc về mật độ", "Two rules for density"),
                       "body": ul(L("Mật độ biến thiên tỉ lệ thuận với áp suất", "Density varies directly with pressure"),
                                  L("Mật độ biến thiên tỉ lệ nghịch với nhiệt độ", "Density varies inversely with temperature"),
                                  L("Nên không khí trên cao loãng hơn dưới thấp, và khối khí nóng loãng hơn khối khí lạnh", "So high-altitude air is thinner than low-altitude air, and a hot air mass is thinner than a cold one"),
                                  L("Ở độ cao lớn máy bay bay nhanh hơn được, vì mỗi đơn vị thể tích có ít hạt khí hơn nên lực cản nhỏ hơn", "An aircraft can fly faster at high altitude because there are fewer air particles per unit volume, so less resistance")),
                       "explain": L("Cả hai quy tắc đều suy ra từ p = ρRT. Giữ T không đổi thì ρ tăng theo p; giữ p không đổi thì ρ giảm khi T tăng.", "Both rules follow from p = ρRT. At constant T, density rises with p; at constant p, density falls as T rises.")},
                      {"title": L("Độ ẩm làm không khí nhẹ hơn", "Humidity makes air lighter"),
                       "body": ul(L("Độ ẩm tuyệt đối: khối lượng hơi nước trên một đơn vị thể tích không khí", "Absolute humidity: mass of water vapour per unit volume of air"),
                                  L("Độ ẩm tương đối: lượng hơi nước đang có, tính theo phần trăm của lượng hơi nước tối đa (bão hòa) ở cùng nhiệt độ và áp suất", "Relative humidity: the percentage ratio of the water vapour present to the amount at saturation at the same temperature and pressure"),
                                  L("Hơi nước nặng khoảng 5/8 không khí khô cùng thể tích, nên không khí ẩm có mật độ thấp hơn", "Water vapour weighs about 5/8 as much as the same volume of dry air, so humid air has lower density"),
                                  L("Ngày ẩm, máy bay cần đường băng dài hơn để cất cánh", "On damp days an aircraft needs a longer take-off runway than on dry days")),
                       "explain": L("Ngày ẩm có cảm giác \"nặng nề\", nên dễ nghĩ không khí ẩm nặng hơn, nhưng thực tế ngược lại. Phân tử nước (khối lượng phân tử 18) thế chỗ phân tử nitơ hay oxy (28 và 32), nên hỗn hợp nhẹ đi.", "A muggy day feels \"heavy\", so it is natural to think humid air weighs more. It is the other way round: a water molecule (mass 18) takes the place of a nitrogen or oxygen molecule (28 or 32), so the mixture gets lighter.")}]})
    parts.append({"title": L("Nhiệt độ và các tầng khí quyển", "Temperature and the atmospheric layers"),
                  "bullets": [L("Tầng đối lưu (troposphere): nhiệt độ giảm khoảng 2 °C mỗi 1000 ft", "Troposphere: temperature falls about 2 °C per 1000 ft"),
                              L("Đỉnh tầng đối lưu (tropopause) khoảng −57 °C", "The tropopause is about −57 °C"),
                              L("Phần lớn hàng không dân dụng bay trong tầng đối lưu", "Most civil aviation takes place in the troposphere")],
                  "slides": [
                      {"title": L("Tầng đối lưu và tropopause", "Troposphere and tropopause"),
                       "body": ul(L("Trung bình tầng đối lưu cao tới khoảng 38 000 ft; ở hai cực chỉ 25 000 đến 30 000 ft, ở xích đạo tới khoảng 60 000 ft", "On average the troposphere reaches about 38 000 ft; over the poles only 25 000–30 000 ft, at the equator about 60 000 ft"),
                                  L("Nhiệt độ giảm gần như đều, khoảng −2 °C hay −3,5 °F mỗi 1000 ft", "Temperature falls almost steadily, about −2 °C or −3.5 °F per 1000 ft"),
                                  L("Biên trên là tropopause, vùng nhiệt độ gần như không đổi −57 °C (−69 °F)", "The upper boundary is the tropopause, a zone of nearly constant −57 °C (−69 °F)")),
                       "explain": L("−2 °C mỗi 1000 ft xấp xỉ −6,5 °C mỗi km, tức gradient 0,0065 K/m mà ISA dùng ở các slide sau.", "−2 °C per 1000 ft is about −6.5 °C per km, which is the 0.0065 K/m gradient the ISA uses on the next slides.")},
                      {"title": L("Các tầng phía trên", "The layers above"),
                       "body": ul(L("Tầng bình lưu (stratosphere): nhiệt độ tăng dần theo độ cao, tới gần 0 °C; chứa tầng ôzôn chắn tia cực tím", "Stratosphere: temperature rises with altitude to near 0 °C; it holds the ozone layer that blocks ultraviolet rays"),
                                  L("Tầng trung quyển (mesosphere): nhiệt độ lại giảm", "Mesosphere: temperature falls again"),
                                  L("Tầng nhiệt quyển (thermosphere) nằm trên cùng", "The thermosphere lies above"),
                                  L("Một số chuyến bay dân dụng và nhiều chuyến bay quân sự diễn ra trong tầng bình lưu", "Some civil and many military flights take place in the stratosphere")),
                       "explain": L("Nhiệt độ không giảm mãi theo độ cao: trong tầng bình lưu, ôzôn hấp thụ tia cực tím nên không khí nóng lên. Riêng mô hình ISA giữ nhiệt độ không đổi từ 11 đến 20 km, nên bảng ISA không cho thấy sự nóng lên này.", "Temperature does not fall forever with height: in the stratosphere ozone absorbs ultraviolet and the air warms. The ISA model, however, holds temperature constant from 11 to 20 km, so the ISA table does not show this warming.")}]})
    parts.append({"title": L("Khí quyển chuẩn quốc tế ISA", "The International Standard Atmosphere (ISA)"),
                  "bullets": [L("Khí quyển thật luôn thay đổi, nên cần một mô hình chuẩn để so sánh và hiệu chuẩn", "The real atmosphere always changes, so a standard model is needed for comparison and calibration"),
                              L("ISA mực biển: 15 °C, 1013,25 hPa, mật độ 1,225 kg/m³", "ISA at sea level: 15 °C, 1013.25 hPa, density 1.225 kg/m³"),
                              L("Được ICAO, ISO và các chính phủ thống nhất sử dụng", "Agreed and used by ICAO, ISO and governments")],
                  "slides": [
                      {"title": L("Bảng ISA (tính lại)", "ISA table (recomputed)"),
                       "body": table([L("Độ cao (ft)", "Altitude (ft)"), L("Nhiệt độ (°C)", "Temp (°C)"), "p (hPa)", "p (psi)", "ρ (kg/m³)"], isa_rows) +
                       f"<p class='pill'>{L('Tính theo ISA: nhiệt độ giảm 6,5 K mỗi km tới 11 km, trên đó giữ 216,65 K. EASA Hình 1-7 ghi 14,67 psi, 1013,53 hPa và 1,23 kg/m³ ở mực biển, kèm các bước 1000 ft: khớp với bảng này tới làm tròn.', 'Computed from the ISA: temperature falls 6.5 K per km up to 11 km and stays at 216.65 K above. EASA Figure 1-7 lists 14.67 psi, 1013.53 hPa and 1.23 kg/m³ at sea level, plus 1000 ft steps: they agree with this table to rounding.')}</p>",
                       "explain": L("11 000 m bằng 36 089 ft, là đỉnh tầng đối lưu trong ISA. Mật độ ở đó chỉ còn khoảng 30% so với mực biển.", "11 000 m is 36 089 ft: the ISA tropopause. Density there is only about 30% of sea level.")},
                      {"title": L("Ứng dụng: độ cao mật độ", "Application: density altitude"),
                       "body": ul(L("ISA là mốc chung cho đồng hồ độ cao, bảng tính năng máy bay và việc so sánh giữa các hãng", "ISA underlies the altimeter, aircraft performance figures and comparisons between manufacturers"),
                                  L(f"Ví dụ: sân bay ở độ cao 5000 ft, nhiệt độ 30 °C (nóng hơn ISA khoảng {N(isa_dev, 0)} °C). Mật độ thực là {N(rho_hot, 3)} kg/m³, chỉ bằng {N(ratio * 100, 0)}% mật độ mực biển chuẩn, ứng với độ cao mật độ khoảng {N(dens_alt_ft, 0)} ft", f"Example: an airport at 5000 ft and 30 °C (about {N(isa_dev, 0)} °C above ISA). The real density, {N(rho_hot, 3)} kg/m³, is only {N(ratio * 100, 0)}% of standard sea level, which corresponds to a density altitude of about {N(dens_alt_ft, 0)} ft"),
                                  L("Vì thế ở sân bay cao vào ngày nóng, máy bay cất cánh kém hơn", "That is why take-off performance suffers at high airports on hot days")),
                       "explain": L("Độ cao mật độ là độ cao mà trong khí quyển ISA có cùng mật độ với không khí thực tế lúc đó. Máy bay sẽ hoạt động như thể đang ở độ cao ấy.", "Density altitude is the height in the ISA at which the air has the same density as the air actually around you. The aircraft performs as if it were at that height.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Phương trình trạng thái và khí quyển chuẩn", "Equation of state and the standard atmosphere")
    m["formula_math"] = ("p = F/A  ·  p = ρ R T  ·  R = 287 J/(kg·K)<br>T = T₀ + λh  (λ = −0,0065 K/m)  ·  p = p₀ (T/T₀)^(−g/λR)  ·  ρ = p/RT" if lang == "vi" else
                         "p = F/A  ·  p = ρ R T  ·  R = 287 J/(kg·K)<br>T = T₀ + λh  (λ = −0.0065 K/m)  ·  p = p₀ (T/T₀)^(−g/λR)  ·  ρ = p/RT")
    m["legend"] = [("p", L("áp suất (Pa)", "pressure (Pa)")), ("ρ", L("mật độ (kg/m³)", "density (kg/m³)")), ("T", L("nhiệt độ tuyệt đối (K)", "absolute temperature (K)")),
                   ("λ", L("gradient nhiệt độ tầng đối lưu", "tropospheric lapse rate")), ("h", L("độ cao (m)", "altitude (m)")), ("g", "9,80665 m/s²" if lang == "vi" else "9.80665 m/s²")]
    m["history_title"] = L("Từ ống Torricelli đến ISA", "From Torricelli's tube to ISA")
    m["history"] = L("Năm 1643, Evangelista Torricelli chế tạo khí áp kế thủy ngân đầu tiên và chứng minh không khí có trọng lượng. Năm 1648, theo yêu cầu của Blaise Pascal, Florin Périer mang khí áp kế lên núi Puy de Dôme và thấy cột thủy ngân tụt xuống khi lên cao: áp suất giảm theo độ cao. Về sau, ICAO, ISO và các chính phủ thống nhất một khí quyển chuẩn, để đồng hồ độ cao và bảng tính năng máy bay cùng dựa trên một mốc chung (EASA, tr. 1.5).",
                     "In 1643 Evangelista Torricelli built the first mercury barometer and showed that air has weight. In 1648, at Blaise Pascal's request, Florin Périer carried a barometer up the Puy de Dôme and saw the mercury column fall as he climbed: pressure drops with altitude. Later ICAO, ISO and governments agreed on one standard atmosphere, so that altimeters and aircraft performance tables share a common baseline (EASA, p. 1.5).")
    m["case_title"] = L("Tình huống: Zeppelin và cánh Boeing 727", "Case: a Zeppelin and a Boeing 727 wing")
    m["case"] = L(ul(f"<b>Anderson 1.1, cánh Boeing 727.</b> Tại một điểm trên cánh, p = 1,9×10⁴ N/m² và T = 203 K, nên ρ = p/RT = {N(rho_11a, 3)} kg/m³, chỉ khoảng một phần ba mật độ mực biển.",
                  f"<b>Anderson 1.12, Zeppelin.</b> Khí cầu thể tích 15 000 m³ bay ở độ cao 1000 m (ρ theo ISA = {N(rho1000, 4)} kg/m³). Lực đẩy Archimedes là {N(B / 1e5, 3)}×10⁵ N, lực nâng khí động là {N(Lz, 0)} N, nên tổng trọng lượng là {N(W / 1e5, 3)}×10⁵ N. Lực đẩy Archimedes gánh gần hết trọng lượng; lực nâng khí động chỉ chiếm {N(Lz / W * 100, 1)}%."),
                  ul(f"<b>Anderson 1.1, Boeing 727 wing.</b> At a point on the wing p = 1.9×10⁴ N/m² and T = 203 K, so ρ = p/RT = {N(rho_11a, 3)} kg/m³, about a third of sea-level density.",
                  f"<b>Anderson 1.12, Zeppelin.</b> A 15 000 m³ airship flies at 1000 m (ISA ρ = {N(rho1000, 4)} kg/m³). Archimedes buoyancy is {N(B / 1e5, 3)}×10⁵ N and aerodynamic lift is {N(Lz, 0)} N, so the total weight is {N(W / 1e5, 3)}×10⁵ N. Buoyancy carries almost all of it; aerodynamic lift is only {N(Lz / W * 100, 1)}%."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("Không khí ẩm nhẹ hơn không khí khô, không phải nặng hơn.",
                  "Áp suất không giảm đều theo độ cao mà giảm gần như theo hàm mũ: ở 40 000 ft chỉ còn khoảng 18% giá trị ở mực biển.",
                  "Gradient −2 °C mỗi 1000 ft chỉ đúng trong tầng đối lưu. Trên tropopause, nhiệt độ ISA không đổi.",
                  "Bài Anderson 1.12 có lực đẩy Archimedes. Quên nó thì trọng lượng sai gấp hàng chục lần.",
                  "Solution Manual (bản 4, đã đối chiếu với ảnh trang 12) in L = 3487 N ở dòng tính lực nâng, nhưng 500 × 153,9 × 0,05 = 3847 N, và dòng kế tiếp lại dùng đúng 3847 N để ra W = 1,67×10⁵ N. Đáp án cuối đúng; chỉ có một lỗi đánh máy ở dòng giữa."),
                  ul("Humid air is lighter than dry air, not heavier.",
                  "Pressure does not fall evenly with height but roughly exponentially: at 40 000 ft only about 18% of the sea-level value is left.",
                  "The −2 °C per 1000 ft gradient holds only in the troposphere. Above the tropopause the ISA temperature is constant.",
                  "Anderson 1.12 includes Archimedes buoyancy. Forget it and the weight is off by a factor of dozens.",
                  "The Solution Manual (4th ed., checked against the page image, p. 12) prints L = 3487 N on the lift line, but 500 × 153.9 × 0.05 = 3847 N, and the very next line uses 3847 N to reach W = 1.67×10⁵ N. The final answer is right; only the middle line has a typo."))
    m["nb_desc"] = L("Notebook viết lại ISA bằng code, so với EASA Hình 1-4 và 1-7, giải lại các bài Anderson 1.1, 1.11, 1.12 và dùng assert để kiểm mọi đáp án quiz.",
                     "The notebook codes up the ISA, compares it with EASA Figures 1-4 and 1-7, re-solves Anderson 1.1, 1.11 and 1.12 and uses assert to check every quiz answer.")

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
            L("<p>ρ = 1,9×10⁴/(287 × 203) = 1,9×10⁴/58 261 = 0,326 kg/m³. Solution Manual cho cùng giá trị 0,326.</p>", "<p>ρ = 1.9×10⁴/(287 × 203) = 1.9×10⁴/58 261 = 0.326 kg/m³. The Solution Manual gives the same 0.326.</p>")),
        mcq(SD(12), "Anderson 6th, Problem 1.1b",
            L("Trong buồng thử của hầm gió siêu âm, p = 1058 lb/ft² và ρ = 1,23×10⁻³ slug/ft³. Nhiệt độ tại đó (R = 1716 ft·lb/(slug·°R)) là:", "In the test section of a supersonic wind tunnel p = 1058 lb/ft² and ρ = 1.23×10⁻³ slug/ft³. The temperature there (R = 1716 ft·lb/(slug·°R)) is:"),
            f"{N(T_11b, 0)} °R", [f"{N(T_11b * 0.62, 0)} °R", f"{N(T_11b * 1.7, 0)} °R", f"{N(T_11b - 460, 0)} °R"],
            L("T = p/(ρR) = 1058/(1,23×10⁻³ × 1716).", "T = p/(ρR) = 1058/(1.23×10⁻³ × 1716)."),
            L("<p>T = 1058/2,1107 = 501 °R, khoảng 41 °F hay 278 K. Rankine là thang nhiệt độ tuyệt đối.</p>", "<p>T = 1058/2.1107 = 501 °R, about 41 °F or 278 K. Rankine is an absolute scale.</p>")),
        mcq(SD(13), "Anderson 6th, Problem 1.11",
            L("Áp kế chữ U thủy ngân nối với mô hình hầm gió; phía kia thông khí quyển (1,01×10⁵ N/m²). Hai cột thủy ngân chênh 20 cm, cột cao ở phía mô hình. Áp suất trên cánh là (ρ_Hg = 1,36×10⁴ kg/m³, g = 9,8 m/s²):", "A mercury U-tube manometer connects the wind-tunnel model to the atmosphere (1.01×10⁵ N/m²). The two mercury columns differ by 20 cm, with the high column on the model side. The pressure on the wing is (ρ_Hg = 1.36×10⁴ kg/m³, g = 9.8 m/s²):"),
            f"{N(p_11 / 1e4, 2)}×10⁴ N/m²", [f"{N((1.01e5 + 1.36e4 * 9.8 * 0.2) / 1e4, 2)}×10⁴ N/m²", f"{N(1.36e4 * 9.8 * 0.2 / 1e4, 2)}×10⁴ N/m²", f"{N(1.01e5 / 1e4, 2)}×10⁴ N/m²"],
            L("Cột thủy ngân cao hơn nằm ở phía áp suất thấp hơn, nên p_mô hình = p_khí quyển − ρgh.", "The higher mercury column sits on the lower-pressure side, so p_model = p_atm − ρgh."),
            L(f"<p>p = 1,01×10⁵ − (1,36×10⁴)(9,8)(0,2) = 1,01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = {N(p_11, 0)} N/m². Khớp đáp án 7,43×10⁴ trong Solution Manual. Lỗi hay gặp là cộng thay vì trừ.</p>", f"<p>p = 1.01×10⁵ − (1.36×10⁴)(9.8)(0.2) = 1.01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = {N(p_11, 0)} N/m². Matches the 7.43×10⁴ in the Solution Manual. A common slip is adding instead of subtracting.</p>")),
        mcq(SD(14), "Anderson 6th, Problem 1.12",
            L("Zeppelin thể tích 15 000 m³, đường kính lớn nhất 14 m, bay thẳng đều 30 m/s ở độ cao chuẩn 1000 m (ρ ≈ 1,112 kg/m³) với C_L = 0,05 (tính theo tiết diện ngang lớn nhất). Tổng trọng lượng là:", "A Zeppelin of 15 000 m³ and 14 m maximum diameter flies straight and level at 30 m/s at a standard altitude of 1000 m (ρ ≈ 1.112 kg/m³) with C_L = 0.05 (based on maximum cross-section). Its total weight is:"),
            f"{N(W / 1e5, 3)}×10⁵ N", [f"{N(Lz, 0)} N", f"{N((B - Lz) / 1e5, 3)}×10⁵ N", f"{N(B * 2 / 1e5, 3)}×10⁵ N"],
            L("W = lực đẩy Archimedes B + lực nâng khí động L.", "W = Archimedes buoyancy B + aerodynamic lift L."),
            L(f"<p>Mật độ ISA ở 1000 m là 1,1116 kg/m³. B = ρVg = 1,1116 × 15 000 × 9,8 ≈ {N(B / 1e5, 3)}×10⁵ N; q = ½ρV² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m²; L = qSC_L = {N(Lz, 0)} N; W = B + L ≈ {N(W / 1e5, 3)}×10⁵ N. Nếu chỉ tính lực nâng khí động thì được {N(Lz, 0)} N: sai.</p>", f"<p>The ISA density at 1000 m is 1.1116 kg/m³. B = ρVg = 1.1116 × 15 000 × 9.8 ≈ {N(B / 1e5, 3)}×10⁵ N; q = ½ρV² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m²; L = qSC_L = {N(Lz, 0)} N; W = B + L ≈ {N(W / 1e5, 3)}×10⁵ N. Counting only aerodynamic lift gives {N(Lz, 0)} N, which is wrong.</p>")),
    ]
    T11 = isa(11000)[0] - 273.15
    T30 = isa_ft(30000)[0] - 273.15
    rho_ratio = isa_ft(36089)[2] / RHO0
    SUP = L("Câu luyện thêm", "Extra practice")
    gen = [
        mcq(SD(21), SUP, L("Tại 40 000 ft theo ISA, áp suất còn khoảng bao nhiêu so với mực biển?", "At 40 000 ft in ISA, roughly what fraction of the sea-level pressure remains?"),
            f"{N(p40 / P0 * 100, 0)}% ({N(p40 / PSI, 2)} psi)", [f"33% ({N(4.9, 1)} psi)", f"50% ({N(7.3, 1)} psi)", f"2% ({N(0.3, 1)} psi)"],
            L("Áp suất giảm theo hàm mũ chứ không tuyến tính; công thức ISA cho 2,72 psi.", "Pressure falls exponentially, not linearly; the ISA formula gives 2.72 psi.")),
        mcq(SD(22), SUP, L("Nhiệt độ ISA ở tropopause (11 000 m) là:", "The ISA temperature at the tropopause (11 000 m) is:"),
            f"{N(T11, 1)} °C", ["−40 °C", "0 °C", "−90 °C"],
            L("15 − 6,5 × 11 = −56,5 °C, EASA làm tròn −57 °C.", "15 − 6.5 × 11 = −56.5 °C, which EASA rounds to −57 °C.")),
        mcq(SD(23), SUP, L("Nhiệt độ ISA ở 30 000 ft (tầng đối lưu) xấp xỉ:", "The ISA temperature at 30 000 ft (troposphere) is approximately:"),
            f"{N(T30, 1)} °C", [f"{N(T30 + 25, 1)} °C", f"{N(T30 - 25, 1)} °C", "15 °C"],
            L("15 °C − 6,5 K/km × 9,144 km ≈ −44,4 °C, tương đương −2 °C mỗi 1000 ft.", "15 °C − 6.5 K/km × 9.144 km ≈ −44.4 °C, i.e. −2 °C per 1000 ft.")),
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
        {"key": "easa", "title": L("Sách 1, EASA Module 08: câu hỏi cuối Sub-module 01 (3 câu, đổi từ điền khuyết sang trắc nghiệm)", "Book 1, EASA Module 08: end of Sub-module 01 (3 questions, converted from fill-in to multiple choice)"),
         "intro": L("Đề gốc là điền khuyết. Đáp án đúng giữ nguyên như bản in (tr. 1.8); ba phương án sai được viết thêm.", "The originals are fill-in-the-blank. The correct answer is the printed one (p. 1.8); the three wrong options were added for this quiz."), "items": easa},
        {"key": "anderson", "title": L("Sách 2, Anderson: bài tập cuối chương 1 (mục 1.17), đáp án đã tính lại", "Book 2, Anderson: end-of-chapter 1 problems (sec. 1.17), answers recomputed"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Ba bài cuối chương 1 của Anderson, giải từng bước. Đề lấy từ bản 6; lời giải được tính lại và đối chiếu với Solution Manual (bản 4, chữ viết tay).",
                            "Three end-of-chapter 1 problems from Anderson, solved step by step. The problems come from the 6th edition; each solution was recomputed and compared with the Solution Manual (4th edition, handwritten).")
    m["problems"] = [
        {"num": "1.1", "src": "Anderson 6th, Problem 1.1", "q": L("(a) Tại một điểm trên cánh Boeing 727, p = 1,9×10⁴ N/m² và T = 203 K. Tính ρ. (b) Trong buồng thử của hầm gió siêu âm, p = 1058 lb/ft² và ρ = 1,23×10⁻³ slug/ft³. Tính T.", "(a) At a point on a Boeing 727 wing, p = 1.9×10⁴ N/m² and T = 203 K. Find ρ. (b) In the test section of a supersonic wind tunnel, p = 1058 lb/ft² and ρ = 1.23×10⁻³ slug/ft³. Find T."),
         "ans": L(f"<p>(a) ρ = p/(RT) = 1,9×10⁴/(287×203) = <b>{N(rho_11a, 3)} kg/m³</b>.</p><p>(b) T = p/(ρR) = 1058/(1,23×10⁻³×1716) = <b>{N(T_11b, 0)} °R</b>.</p><p class='pill'>Khớp Solution Manual.</p>", f"<p>(a) ρ = p/(RT) = 1.9×10⁴/(287×203) = <b>{N(rho_11a, 3)} kg/m³</b>.</p><p>(b) T = p/(ρR) = 1058/(1.23×10⁻³×1716) = <b>{N(T_11b, 0)} °R</b>.</p><p class='pill'>Matches the Solution Manual.</p>")},
        {"num": "1.11", "src": "Anderson 6th, Problem 1.11", "q": L("Một áp kế chữ U thủy ngân nối mô hình trong hầm gió với khí quyển (p_atm = 1,01×10⁵ N/m²). Hai mực thủy ngân chênh nhau 20 cm, mực cao ở phía mô hình. Tính áp suất trên cánh mô hình.", "A mercury U-tube manometer connects a wind-tunnel model to the atmosphere (p_atm = 1.01×10⁵ N/m²). The two mercury levels differ by 20 cm, with the higher level on the model side. Find the pressure on the model wing."),
         "ans": L(f"<p>Cột cao ở phía áp suất thấp: p = p_atm − ρ_Hg g h = 1,01×10⁵ − (1,36×10⁴)(9,8)(0,2) = <b>{N(p_11, 0)} N/m²</b> (7,43×10⁴).</p>", f"<p>The high column is on the low-pressure side: p = p_atm − ρ_Hg g h = 1.01×10⁵ − (1.36×10⁴)(9.8)(0.2) = <b>{N(p_11, 0)} N/m²</b> (7.43×10⁴).</p>")},
        {"num": "1.12", "src": "Anderson 6th, Problem 1.12", "q": L("Khí cầu Zeppelin thể tích 15 000 m³, đường kính lớn nhất 14 m, bay thẳng đều với V = 30 m/s ở độ cao chuẩn 1000 m, C_L = 0,05 (tính theo tiết diện ngang lớn nhất). Tính tổng trọng lượng.", "A Zeppelin of volume 15 000 m³ and maximum diameter 14 m flies straight and level at V = 30 m/s at a standard altitude of 1000 m, with C_L = 0.05 (based on maximum cross-section). Find the total weight."),
         "ans": L(f"<p>Cân bằng: W = B + L.</p><p>B = ρVg = 1,1117×15 000×9,8 = {N(B, 0)} N. q = ½ρV² = {N(q, 1)} Pa. S = π·14²/4 = {N(S, 1)} m². L = qSC_L = {N(Lz, 0)} N.</p><p><b>W = {N(W, 0)} N</b> (≈ {N(W / 1e5, 3)}×10⁵ N).</p><p class='pill'>Solution Manual in nhầm L = 3487 N ở dòng giữa (làm tròn q = 500 Pa cho 3847 N, không làm tròn cho 3850 N); đáp án cuối 1,67×10⁵ N vẫn đúng.</p>", f"<p>Equilibrium: W = B + L.</p><p>B = ρVg = 1.1117×15 000×9.8 = {N(B, 0)} N. q = ½ρV² = {N(q, 1)} Pa. S = π·14²/4 = {N(S, 1)} m². L = qSC_L = {N(Lz, 0)} N.</p><p><b>W = {N(W, 0)} N</b> (≈ {N(W / 1e5, 3)}×10⁵ N).</p><p class='pill'>The Solution Manual misprints L = 3487 N on the middle line (rounding q to 500 Pa gives 3847 N, unrounded gives 3850 N); its final 1.67×10⁵ N is right.</p>")},
    ]
    return m
