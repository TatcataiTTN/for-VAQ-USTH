# -*- coding: utf-8 -*-
import nbformat as nbf, os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"notebooks"); os.makedirs(OUT,exist_ok=True)
md=nbf.v4.new_markdown_cell; code=nbf.v4.new_code_cell
cells=[
md("""# Module 09: EMC trên máy bay / EMC in Aircraft
**AE2.021 · USTH**

🇻🇳 Notebook tính lại mọi con số dB, dBm, nối tầng của bài giảng (slide 13 đến 21), phát hiện lỗi 10 kW so với 100 kW ở slide 21, kiểm chứng chuỗi Fourier của sóng vuông, tụ thực (ESL, ESR, f_r), các ví dụ phổ của Tooley, noise margin Floyd và khoá đáp án Tooley chương 14 (đọc từ ảnh scan A.14, tr.381).

🇬🇧 This notebook recomputes every dB, dBm and cascade number in the lecture (slides 13 to 21), catches the 10 kW versus 100 kW error on slide 21, verifies the square-wave Fourier series, the real capacitor (ESL, ESR, f_r), Tooley's spectrum examples, Floyd's noise margins and Tooley's chapter 14 key (read from the scanned image A.14, p.381)."""),
md("## 1. dB và dBm / dB and dBm"),
code("""import math
L10=math.log10
dbP=lambda p2,p1:10*L10(p2/p1); dbA=lambda a2,a1:20*L10(a2/a1)
dbm=lambda w:10*L10(w/1e-3); from_dbm=lambda d:1e-3*10**(d/10)

# slide 13: ba vi du
assert round(dbA(1,1e-3))==60 and round(dbP(1,1e-3))==30 and round(dbA(1e-3,1e-5))==40 and round(dbA(0.1,1))==-20
# slide 14-15: bang ti so
for r,pw,vo in ((0.01,-20,-40),(0.1,-10,-20),(0.5,-3,-6),(1,0,0),(2,3,6),(10,10,20),(100,20,40)):
    assert abs(dbP(r,1)-pw)<0.4 and abs(dbA(r,1)-vo)<0.8, r
# slide 17: bai tap
rows=[(dbA(200,100),6),(dbA(300,100),10),(dbA(400,100),12),(dbA(500,100),14),(dbP(2,1),3),(dbP(3,1),5),(dbP(5,1),7)]
for got,slide in rows: print(round(got,2),slide); assert abs(got-slide)<0.5
# slide 19: bang dBm
for w,d in ((0.001,0),(0.1,20),(0.5,27),(1,30),(2,33),(10,40),(1000,60)):
    print(w,round(dbm(w),2)); assert abs(dbm(w)-d)<0.1
assert from_dbm(0)==1e-3          # 0 dBm = 1 mW, khong phai 0 W"""),
md("## 2. Bài tập slide 20 và 21 / Exercises on slides 20 and 21"),
code("""# slide 20: noi tang
assert 0+10+6==16 and 0-3-10==-13
# slide 21
v1=1*10**(-2/20);          print("1) Vout =",round(v1,3)); assert abs(v1-0.794)<1e-3
p2=10*10**(40/10);         print("2) Pout =",p2,"W");      assert p2==100000          # slide in nham '10000 W (10 kW)'
p3=-20+30;                 print("3) Pout =",p3,"dBm =",from_dbm(p3)*1e3,"mW"); assert p3==10 and abs(from_dbm(p3)-0.01)<1e-12
p4=34+(-2);                print("4) Iout =",p4,"dBuA"); assert p4==32
print("Loi tren slide 21: ket qua in 10000 W khac 100000 W cua chinh phep tinh.")"""),
md("## 3. Sóng vuông và phổ / Square wave and spectrum"),
code("""import numpy as np
t=np.linspace(0,1,20001,endpoint=False)
def sq(N): return sum(np.sin(2*np.pi*n*t)/n for n in range(1,N+1,2))
# Tooley TYU 14.1: 50 V, 2 kHz -> hai bac 5
assert 50/5==10 and 5*2000==10000
# Hai bac 1 cua day V/n co bien do 4/pi * V_vuong: kiem tra gia tri tren plateau
plateau=sq(401)[len(t)//4]          # giua nua chu ky duong
print("gia tri plateau cua chuoi V/n =",round(plateau,4),"(pi/4 =",round(math.pi/4,4),")")
assert abs(plateau-math.pi/4)<0.01   # => bien do song vuong that = (pi/4) * V, nghia la hai co ban = 4V_sq/pi
# Tooley hinh 14.9: ba bac 3 thap hon co ban 70 dB
assert -20-(-90)==70"""),
md("## 4. Tụ thực / A real capacitor"),
code("""fr=lambda L,C:1/(2*math.pi*math.sqrt(L*C))
Z=lambda f,C,L,R:math.sqrt(R**2+(2*math.pi*f*L-1/(2*math.pi*f*C))**2)
C,Lh,R=100e-9,10e-9,0.05
f0=fr(Lh,C); print("f_r =",round(f0/1e6,3),"MHz"); assert abs(f0-5.033e6)<1e3
assert abs(Z(f0,C,Lh,R)-R)<1e-9                      # tai f_r: Z = ESR
assert Z(0.1*f0,C,Lh,R)>Z(f0,C,Lh,R) and Z(10*f0,C,Lh,R)>Z(f0,C,Lh,R)
# tren f_r: cam khang cua cuon cam chiem uu the
f=10*f0; assert 2*math.pi*f*Lh>1/(2*math.pi*f*C)
# tu 1 nF co f_r cao hon nhieu
assert fr(Lh,1e-9)>3*f0"""),
md("## 5. Số liệu của Tooley và Floyd / Tooley and Floyd numbers"),
code("""# Tooley hinh 14.14: san nhieu tang tu -110 den -84 dB = 26 dB; sach viet '50 lan'
d=-84-(-110); print("tang",d,"dB ->",round(10**(d/20),1),"lan bien do,",round(10**(d/10)),"lan cong suat")
assert d==26 and abs(10**(d/20)-19.95)<0.1 and round(10**(d/10))==398    # khong phai 50 lan
# Tooley 14.3: phan tich pho: bien do hai con tro -26 dBm tai 121 MHz, san nhieu -95 dBm => 69 dB tren san nhieu
assert -26-(-95)==69
# CISPR 11 (slide 26): doi dBuV/m sang uV/m
print(round(10**(30/20),1),"uV/m;",round(10**(37/20),1),"uV/m;",round(10**(7/20),2),"lan")
assert abs(10**(37/20)/10**(30/20)-2.239)<0.01
# Floyd Ch.15 Bai 3 va vi du 15-1 (CMOS 5 V)
VNH=2.4-2.25; VNL=0.65-0.4; assert abs(VNH-0.15)<1e-9 and abs(VNL-0.25)<1e-9
assert abs((4.4-3.5)-0.9)<1e-9 and abs((1.5-0.33)-1.17)<1e-9"""),
md("## 6. Khoá Tooley Ch.14 / Tooley Ch.14 key"),
code("""KEY=dict(zip(range(1,10),"a c c c c a b a c".split()))     # A.14 tr.381
assert KEY[8]=="a"          # nguon: bo loc thong thap
assert KEY[9]=="c"          # dong cat nhanh va dong lon
assert KEY[3]=="c"          # bien do theo tan so
assert KEY[6]=="a"          # < 0.005 ohm (Tooley 14.6 noi < 0.001-0.003 ohm)
# Cac nguong lien ket: slide 43 (0.001-0.003), slide 45 (<2.5 mohm, tester 0.003 ohm), Tooley Q6 (<0.005)
tester=0.003; slide45_limit=0.0025
print("tester",tester,"ohm  > gioi han slide 45",slide45_limit,"ohm ->", "KHONG DAT theo chinh slide" if tester>slide45_limit else "dat")
assert tester>slide45_limit and tester<0.005
print("Khoa 9/9 doc tu anh scan.")"""),
md("""#### 📤 Nhận xét / Takeaway
🇻🇳 Mọi con số dB khớp, trừ ô kết quả 10 kW ở slide 21 (đúng là 100 kW). Chuỗi V/n của sóng vuông phải hiểu V là biên độ hài cơ bản (biên độ sóng vuông thật là π/4 lần giá trị tổng chuỗi). Sàn nhiễu tăng 26 dB là khoảng 20 lần biên độ, không phải 50 lần. Hai ngưỡng điện trở liên kết (slide 43 và 45) mâu thuẫn và hình thiết bị đo ở slide 45 tự không đạt.

🇬🇧 Every dB figure agrees, except the 10 kW result box on slide 21 (it should be 100 kW). In the V/n series V must be read as the fundamental amplitude (the real square-wave amplitude is π/4 times the series sum). A 26 dB rise in the noise floor is about 20 times in amplitude, not 50. The two bonding resistance thresholds (slides 43 and 45) conflict and the tester picture on slide 45 itself fails."""),
]
nb=nbf.v4.new_notebook(); nb["cells"]=cells
nb["metadata"]={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3"}}
nbf.write(nb,os.path.join(OUT,"09_emc.ipynb")); print("wrote")
