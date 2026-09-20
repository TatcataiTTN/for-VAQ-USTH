# -*- coding: utf-8 -*-
# Bộ MCQ bổ sung (Set B) cho Mechanics II -- câu tính toán có đáp số tính bằng Python.
import math
g = 9.81; G = 6.674e-11; Me = 5.972e24; Re = 6.371e6
def f(x, n=4):
    return f"{x:.{n}g}"
def Q(lec, q, c, w):
    return {"lecture": lec, "q": q, "correct": c, "wrong": w}

QUESTIONS_B = []
A = QUESTIONS_B.append

# ---- L1 Equilibrium & Elasticity ----
A(Q("L1", "Ngẫu lực (couple) là gì?", "Hai lực bằng nhau, song song, ngược chiều, khác đường tác dụng: tổng lực bằng 0 nhưng có mô-men", ["Hai lực cùng chiều cùng đường", "Một lực duy nhất có mô-men", "Hai lực vuông góc nhau"]))
A(Q("L1", "Mô-đun khối (bulk modulus) $K$ đặc trưng cho:", "Khả năng chống thay đổi thể tích khi áp suất thay đổi", ["Chống biến dạng dọc trục", "Chống biến dạng cắt", "Độ dẻo của vật liệu"]))
A(Q("L1", "Mô-đun cắt $G$ liên hệ ứng suất cắt và:", "Biến dạng cắt (góc $\\gamma$)", ["Biến dạng dọc", "Thể tích", "Khối lượng"]))
A(Q("L1", "Vật đồng chất đặt lên 2 gối; gối nào chịu lực lớn hơn?", "Gối gần khối tâm (hoặc gần tải) hơn", ["Gối xa khối tâm hơn", "Hai gối luôn bằng nhau", "Gối bên trái"]))
A(Q("L1", "Giới hạn đàn hồi của vật liệu là:", "Ứng suất lớn nhất mà vật còn trở về hình dạng ban đầu khi bỏ tải", ["Ứng suất phá hủy", "Mô-đun Young", "Ứng suất bằng 0"]))
_s = 25e6/200e9
A(Q("L1", "[Tính toán] Thanh thép $E=200$~GPa chịu ứng suất $25$~MPa. Biến dạng?", "$1.25\\times10^{-4}$", ["$1.25\\times10^{-3}$", "$8\\times10^{3}$", "$5\\times10^{-6}$"]))
A(Q("L1", "[Tính toán] Dầm $6$~m hai gối ở hai đầu, tải $600$~N cách gối trái $1.5$~m (bỏ qua trọng lượng dầm). Phản lực gối phải?", "150 N", ["450 N", "300 N", "600 N"]))
A(Q("L1", "[Tính toán] Nước ($K=2.2$~GPa) chịu tăng áp $22$~MPa. Độ giảm thể tích tương đối?", "1%", ["10%", "0.1%", "22%"]))
A(Q("L1", "[Tính toán] Lực $F=1000$~N kéo thanh $A=5\\times10^{-5}$~m². Ứng suất?", "20 MPa", ["2 MPa", "200 MPa", "0.02 MPa"]))
A(Q("L1", "[Tính toán] Cân bằng mô-men: khối $4$~kg cách điểm tựa $0.6$~m. Khối cần đặt cách điểm tựa $0.3$~m ở phía kia để cân bằng có khối lượng?", "8 kg", ["2 kg", "4 kg", "16 kg"]))

# ---- L2 Gravitation ----
A(Q("L2", "Định luật Kepler II (diện tích) phát biểu rằng:", "Đường nối hành tinh với Mặt Trời quét diện tích bằng nhau trong thời gian bằng nhau", ["Quỹ đạo là đường tròn", "$T^2\\propto a^3$", "Hành tinh chuyển động đều"]))
A(Q("L2", "Vận tốc thoát khỏi hành tinh KHÔNG phụ thuộc vào:", "Khối lượng vật thoát", ["Khối lượng hành tinh", "Bán kính hành tinh", "$G$"]))
A(Q("L2", "Khi bán kính quỹ đạo tròn tăng gấp 4, chu kỳ tăng gấp:", "8 lần", ["4 lần", "16 lần", "2 lần"]))
A(Q("L2", "Vệ tinh địa tĩnh có đặc điểm:", "Chu kỳ 1 ngày thiên văn, quỹ đạo xích đạo", ["Chu kỳ 90 phút", "Quỹ đạo qua 2 cực", "Độ cao 400 km"]))
A(Q("L2", "Thế năng hấp dẫn của 2 khối $-GMm/r$ có giá trị:", "Âm, tiến về 0 khi $r\\to\\infty$", ["Dương luôn", "Bằng $mgh$ luôn", "Không đổi"]))
A(Q("L2", "[Tính toán] $g$ ở độ cao bằng $R_E$ (cách tâm $2R_E$) so với mặt đất?", "1/4 lần", ["1/2 lần", "2 lần", "1/9 lần"]))
A(Q("L2", "[Tính toán] Vận tốc thoát Trái Đất xấp xỉ?", f"≈ {f(math.sqrt(2*G*Me/Re)/1e3)} km/s", [f"≈ {f(math.sqrt(G*Me/Re)/1e3)} km/s (vận tốc quỹ đạo sát mặt đất)", "≈ 3.9 km/s", "≈ 22.4 km/s"]))
A(Q("L2", "[Tính toán] Hành tinh có $T=8$ năm. Bán trục lớn?", "4 AU", ["2 AU", "8 AU", "16 AU"]))
A(Q("L2", "[Tính toán] Hai khối $10$~kg cách nhau $1$~m. Lực hấp dẫn?", f"≈ {G*100:.3g} N", [f"≈ {G*10:.3g} N", f"≈ {G*1000:.3g} N", f"≈ {G*100/2:.3g} N"]))
A(Q("L2", "[Tính toán] Vệ tinh quỹ đạo tròn cách tâm $8\\times10^6$~m. Tốc độ?", f"≈ {f(math.sqrt(G*Me/8e6)/1e3)} km/s", [f"≈ {f(G*Me/8e6/1e3)} km/s (quên căn)", f"≈ {f(math.sqrt(2*G*Me/8e6)/1e3)} km/s", "≈ 3.5 km/s"]))

# ---- L4 Oscillations ----
A(Q("L4", "Trong dao động điều hòa, gia tốc luôn:", "Ngược pha với li độ (tỉ lệ $-x$)", ["Cùng pha với vận tốc", "Bằng 0 ở biên", "Không đổi"]))
A(Q("L4", "Cơ năng của dao động điều hòa tỉ lệ với:", "Bình phương biên độ", ["Biên độ", "Chu kỳ", "Pha ban đầu"]))
A(Q("L4", "Hai lò xo NỐI TIẾP có độ cứng tương đương:", "Nhỏ hơn cả hai lò xo thành phần", ["Bằng tổng", "Lớn hơn cả hai", "Bằng trung bình"]))
A(Q("L4", "Dao động tắt dần yếu: biên độ giảm theo:", "Hàm mũ $e^{-bt/2m}$", ["Tuyến tính", "Bậc hai", "Không giảm"]))
A(Q("L4", "Cộng hưởng xảy ra khi tần số ngoại lực:", "Xấp xỉ bằng tần số riêng của hệ", ["Bằng 0", "Rất lớn", "Gấp đôi tần số riêng"]))
A(Q("L4", "[Tính toán] $m=2$~kg, $k=800$~N/m. Tần số góc?", "20 rad/s", ["400 rad/s", "0.05 rad/s", "40 rad/s"]))
A(Q("L4", "[Tính toán] Con lắc đơn $L=1$~m. Chu kỳ?", f"≈ {f(2*math.pi*math.sqrt(1/g))} s", [f"≈ {f(2*math.pi*math.sqrt(g))} s", f"≈ {f(math.sqrt(1/g))} s", "≈ 1 s"]))
A(Q("L4", "[Tính toán] Biên độ $0.2$~m, $k=100$~N/m. Cơ năng?", "2 J", ["4 J", "20 J", "1 J"]))
A(Q("L4", "[Tính toán] $x=0.05\\cos(10t)$. Tốc độ cực đại?", "0.5 m/s", ["5 m/s", "0.005 m/s", "50 m/s"]))
A(Q("L4", "[Tính toán] Con lắc xoắn $I=0.08$, $\\kappa=2$. Chu kỳ?", f"≈ {f(2*math.pi*math.sqrt(0.08/2))} s", [f"≈ {f(2*math.pi*math.sqrt(2/0.08))} s", f"≈ {f(math.sqrt(0.04))} s", "≈ 0.5 s"]))

# ---- L9 Impulse & Momentum ----
A(Q("L9", "Hệ số phục hồi $e=1$ ứng với:", "Va chạm đàn hồi hoàn toàn", ["Va chạm mềm hoàn toàn", "Không có lực", "Mất toàn bộ động năng"]))
A(Q("L9", "Khối tâm của hệ không chịu ngoại lực ngang sẽ:", "Không dịch chuyển theo phương ngang (nếu ban đầu đứng yên)", ["Luôn chuyển động", "Dịch chuyển theo trọng lực", "Quay quanh vật nặng nhất"]))
A(Q("L9", "Xung lượng góc bằng:", "Tích phân mô-men lực theo thời gian", ["Tích phân lực theo thời gian", "Động năng quay", "Vận tốc góc"]))
A(Q("L9", "Lực phi xung lượng trong va chạm là lực:", "Đủ nhỏ để xung lượng của nó trong thời gian va chạm có thể bỏ qua", ["Bằng 0 luôn", "Lực gây va chạm", "Lực lớn nhất"]))
A(Q("L9", "Trong va chạm xiên giữa 2 đĩa trơn, thành phần động lượng không đổi cho MỖI đĩa là theo phương:", "Tiếp tuyến với mặt tiếp xúc (vuông góc đường va chạm)", ["Dọc đường va chạm", "Cả hai", "Không có"]))
A(Q("L9", "[Tính toán] Lực $50$~N trong $0.2$~s tác dụng lên vật $2$~kg từ nghỉ. Tốc độ?", "5 m/s", ["50 m/s", "20 m/s", "0.5 m/s"]))
A(Q("L9", "[Tính toán] Va chạm mềm $3$~kg ($6$~m/s) và $3$~kg đứng yên. Vận tốc chung?", "3 m/s", ["6 m/s", "0 m/s", "2 m/s"]))
A(Q("L9", "[Tính toán] Bóng thả $4$~m, $e=0.5$. Độ cao nảy?", "1 m", ["2 m", "0.5 m", "4 m"]))
A(Q("L9", "[Tính toán] Người $60$~kg đi $5$~m trên thuyền $140$~kg đứng yên (không cản). Thuyền dịch?", "1.5 m", ["3.5 m", "5 m", "0.6 m"]))
A(Q("L9", "[Tính toán] Chất điểm $2$~kg, $4$~m/s, cánh tay đòn $3$~m. Động lượng góc?", "24 kg·m²/s", ["8 kg·m²/s", "6 kg·m²/s", "12 kg·m²/s"]))

# ---- L10 Planar kinematics ----
A(Q("L10", "Tâm vận tốc tức thời (IC) của bánh lăn không trượt nằm ở:", "Điểm tiếp xúc với mặt đất", ["Tâm bánh xe", "Điểm trên cùng", "Vô cực"]))
A(Q("L10", "Vật rắn chuyển động tịnh tiến thì:", "Mọi điểm có cùng vận tốc và gia tốc", ["Có $\\omega\\ne0$", "Chỉ khối tâm chuyển động", "Vận tốc mỗi điểm khác nhau"]))
A(Q("L10", "Công thức vận tốc tương đối 2 điểm trên vật rắn:", "$\\vec v_B=\\vec v_A+\\vec\\omega\\times\\vec r_{B/A}$", ["$\\vec v_B=\\vec v_A-\\vec\\omega r$", "$\\vec v_B=\\vec\\omega r$ (bỏ $\\vec v_A$)", "$\\vec v_B=\\vec v_A$"]))
A(Q("L10", "Điểm tiếp xúc của bánh lăn không trượt (vận tốc bằng 0) có gia tốc:", "Khác 0, hướng về tâm bánh ($\\omega^2r$)", ["Bằng 0", "Hướng ngang", "Vô cùng"]))
A(Q("L10", "Gia tốc góc $\\alpha$ đặc trưng cho sự thay đổi của:", "Vận tốc góc", ["Vị trí góc", "Bán kính", "Khối lượng"]))
A(Q("L10", "[Tính toán] $\\omega=12$~rad/s, $r=0.25$~m. Vận tốc dài?", "3 m/s", ["48 m/s", "0.02 m/s", "12.25 m/s"]))
A(Q("L10", "[Tính toán] Bánh lăn không trượt $v_G=6$~m/s, $r=0.3$~m. Tốc độ điểm trên cùng?", "12 m/s", ["6 m/s", "20 m/s", "0 m/s"]))
A(Q("L10", "[Tính toán] $\\omega_0=4$, $\\alpha=3$~rad/s² không đổi, $t=2$~s. $\\omega$?", "10 rad/s", ["6 rad/s", "14 rad/s", "12 rad/s"]))
A(Q("L10", "[Tính toán] Điểm cách trục $0.5$~m, $\\omega=6$. Gia tốc pháp tuyến?", "18 m/s²", ["3 m/s²", "36 m/s²", "6 m/s²"]))
A(Q("L10", "[Tính toán] Bánh răng $r_A=0.2$ ($\\omega_A=15$) ăn khớp $r_B=0.5$. $\\omega_B$?", "6 rad/s", ["37.5 rad/s", "15 rad/s", "3 rad/s"]))
