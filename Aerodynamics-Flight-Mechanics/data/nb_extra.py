# -*- coding: utf-8 -*-
# exec() tu build_notebooks.py: dung nb, md, code co san. Dinh nghia n5..n8.
HDR = lambda n, t, d: md("# Module %s: %s\n**AE2.008 · USTH**\n\n%s" % (n, t, d))

COMP = """import math
g = 1.4; R = 287.0
T0T = lambda M: 1+(g-1)/2*M*M
p0p = lambda M: T0T(M)**(g/(g-1))
def bis(f, lo, hi, n=200):
    for _ in range(n):
        mid = (lo+hi)/2
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo+hi)/2
def nshock(M):
    M2 = math.sqrt(((g-1)*M**2+2)/(2*g*M**2-(g-1))); p = 1+2*g/(g+1)*(M**2-1); r = (g+1)*M**2/((g-1)*M**2+2)
    p0 = r**(g/(g-1))*((g+1)/(2*g*M**2-(g-1)))**(1/(g-1)); return M2, p, r, p/r, p0
def a_s(T, R=R): return math.sqrt(g*R*T)
"""

n5 = nb([HDR("05", "Cánh hữu hạn / Finite wings", "🇻🇳 Tích phân số Biot-Savart, giải lại Anderson 5.1, 5.2 và Ví dụ 5.1, 5.2.  🇬🇧 Numerical Biot-Savart, re-solving Anderson 5.1, 5.2 and Examples 5.1, 5.2."),
 code("import math"),
 code('''def loop_axis(R, A, G=1.0, n=20000):
    s = 0.0; d = 2*math.pi/n
    for k in range(n):
        t = (k+0.5)*d; rx, ry, rz = -R*math.cos(t), -R*math.sin(t), A
        dlx, dly = -R*math.sin(t)*d, R*math.cos(t)*d
        s += (dlx*ry - dly*rx)/(rx*rx+ry*ry+rz*rz)**1.5
    return G*s/(4*math.pi)
w1 = loop_axis(2, 0); w2 = loop_axis(2, 1.5)
print(w1, w2); assert abs(w1-1/(2*2)) < 1e-6 and abs(w2-4/(2*(4+2.25)**1.5)) < 1e-6'''),
 code('''a0 = 2*math.pi; AR, tau = 8, 0.055
a = a0/(1+a0/(math.pi*AR)*(1+tau)); CL = a*math.pi/180*5; CD = CL**2*(1+tau)/(math.pi*AR)
print(a, CL, CD); assert abs(a-4.97) < 0.01 and abs(CL-0.4335) < 1e-3 and abs(CD-0.00789) < 1e-4
CL6 = math.sqrt(math.pi*6*0.01/1.055); a6 = CL6/math.radians(5.4); a0b = a6/(1-a6*1.055/(math.pi*6))
a10 = a0b/(1+a0b*1.105/(math.pi*10)); CL10 = a10*math.radians(5.4); CD10 = CL10**2*1.105/(math.pi*10)
print(CL6, a0b, a10, CL10, CD10); assert abs(CL6-0.423) < 1e-3 and abs(a0b-5.989) < 0.02 and abs(CL10-0.464) < 3e-3 and abs(CD10-0.0076) < 2e-4'''),
 code('''CLe, ARe = 0.5, 8
assert abs(math.degrees(CLe/(math.pi*ARe))-1.1398) < 1e-3 and abs(CLe**2/(math.pi*12)/(CLe**2/(math.pi*ARe))-8/12) < 1e-12
assert abs(math.sqrt(math.pi*0.85*8/(4*0.02))-16.34) < 0.01
print("All Module 05 checks passed.")''')])

n6 = nb([HDR("06", "Dòng nén được / Compressible flow", "🇻🇳 Giải lại Anderson 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16.  🇬🇧 Re-solves Anderson 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16."),
 code(COMP),
 code('''rho71 = 7.8*2116/(1716*934); assert abs(rho71-0.010298) < 1e-5
rho74 = 4.35e4/(287*245)*(3.6e4/4.35e4)**(1/g); assert abs(rho74-0.5404) < 1e-3
Te = 500*(0.1)**((g-1)/g); assert abs(Te-258.97) < 0.01 and abs(1.01e5/(287*Te)-1.3589) < 1e-3
M = 250/a_s(300); assert abs(M-0.7201) < 1e-3 and abs(300*T0T(M)-331.11) < 0.05 and abs(1.2*p0p(M)-1.695) < 2e-3
assert abs(p0p(2)-7.8244) < 1e-3 and abs(230*T0T(2)-414) < 1e-9'''),
 code('''M88 = math.sqrt((10.33-1)*(g+1)/(2*g)+1); T1 = 1390/nshock(M88)[3]; print(M88, T1); assert abs(M88-3.0) < 1e-3 and abs(T1-519) < 1
M89 = bis(lambda m: -math.log(nshock(m)[4])-199.5/R, 1.0001, 20); print(M89); assert abs(M89-2.5) < 1e-4
M816 = bis(lambda m: nshock(m)[4]*p0p(m)-11.3, 1.0001, 30); print(M816); assert abs(M816-2.9) < 2e-3
M2, p, r, T, p0 = nshock(2.6); assert abs(M2-0.5039) < 1e-3 and abs(p-7.72) < 1e-9 and abs(p0-0.4601) < 1e-3
M2b, pb, rb, Tb, _ = nshock(3.1); V2 = M2b*math.sqrt(g*1716*480*Tb); print(M2b, V2); assert 0.45 < M2b < 0.47
print("All Module 06 checks passed.")''')])

n7 = nb([HDR("07", "Sóng xiên / Oblique shocks", "🇻🇳 Giải θ-β-M bằng chia đôi; Anderson 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20.  🇬🇧 θ-β-M by bisection; Anderson 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20."),
 code(COMP + """d = math.radians
def thb(M, b): return math.atan(2/math.tan(b)*(M*M*math.sin(b)**2-1)/(M*M*(g+math.cos(2*b))+2))
def thmax(M):
    mu = math.asin(1/M); return max(thb(M, mu+(math.pi/2-mu)*i/20000) for i in range(1, 20000))
def beta(M, th):
    mu = math.asin(1/M); bm = max((mu+(math.pi/2-mu)*i/20000 for i in range(1, 20000)), key=lambda b: thb(M, b))
    lo, hi = mu, bm
    for _ in range(100):
        mid = (lo+hi)/2
        if thb(M, mid) < th: lo = mid
        else: hi = mid
    return (lo+hi)/2
def obl(M, b, th):
    Mn = M*math.sin(b); M2n, p, r, T, p0 = nshock(Mn); return M2n/math.sin(b-th), p, T, p0
def pm(M):
    a = math.sqrt((g+1)/(g-1)); return a*math.atan(math.sqrt((M*M-1)/a**2))-math.atan(math.sqrt(M*M-1))
"""),
 code('''assert abs(559*math.tan(math.asin(1/1.5))-500) < 0.1
th = math.atan(2/math.tan(d(30))*(16*0.25-1)/(16*(g+math.cos(d(60)))+2)); M2, p, T, p0 = obl(4, d(30), th)
print(math.degrees(th), M2, p, T, p0); assert abs(p-4.5) < 1e-9 and abs(T-1.6875) < 1e-9 and abs(2.65e4*p-119250) < 1
b = beta(2.5, d(22.2)); M2, p, T, p0 = obl(2.5, b, d(22.2)); print(math.degrees(b), M2, p, 300*T); assert abs(math.degrees(b)-45.89) < 0.02 and abs(M2-1.5374) < 1e-3
assert abs(math.degrees(thmax(2.4))-28.68) < 0.02
assert abs(math.degrees(pm(1e7))-130.45) < 0.01'''),
 code('''p98a = nshock(4)[4]
b1 = beta(4, d(25.3)); o1 = obl(4, b1, d(25.3)); p98b = o1[3]*nshock(o1[0])[4]
b2 = beta(o1[0], d(20)); o2 = obl(o1[0], b2, d(20)); p98c = o1[3]*o2[3]*nshock(o2[0])[4]
print(p98a, p98b, p98c); assert p98a < p98b < p98c and abs(p98a-0.1388) < 1e-3 and abs(p98c-0.4201) < 2e-3
def Mpm(nu): return bis(lambda m: pm(m)-nu, 1.0, 60)
Mx = Mpm(pm(3)+d(20)); pe = p0p(3)/p0p(Mx); b = beta(Mx, d(20)); o = obl(Mx, b, d(20)); p3 = pe*o[1]
print(Mx, pe, o[0], p3); assert abs(Mx-4.318) < 2e-3 and abs(p3-0.9182) < 2e-3 and p3 < 1
print("All Module 07 checks passed.")''')])

n8 = nb([HDR("08", "Động lực ngang / Lateral dynamics", "🇻🇳 Ma trận ngang B747 từ Etkin tr. 187, trị riêng, Bảng 6.8, tiêu chí E, R, bộ giảm xoay.  🇬🇧 The B747 lateral matrix from Etkin p. 187, eigenvalues, Table 6.8, criteria E, R, yaw damper."),
 code('''import numpy as np, math
A = np.array([[-0.0558,0,-774,32.2],[-0.003865,-0.4342,0.4136,0],[0.001086,-0.006112,-0.1458,0],[0,1,0,0]])
c = np.poly(A); print(c); assert np.allclose(c, [1,0.6358,0.9388,0.5114,0.003682], rtol=2e-3, atol=1e-6)
B, C, D, E = c[1:]; R = B*C*D-D**2-B**2*E; print("R =", R); assert E > 0 and R > 0 and abs(R-0.04223) < 5e-4'''),
 code('''ev = np.linalg.eigvals(A); dr = [e for e in ev if e.imag > 0][0]; re = sorted(e.real for e in ev if abs(e.imag) < 1e-9)
print(re, dr)
assert abs(re[0]+0.56248) < 1e-4 and abs(re[1]+0.0072973) < 1e-6 and abs(dr-(-0.03301+0.94655j)) < 1e-4
T = 2*math.pi/dr.imag; th = math.log(2)/-dr.real; print(T, th, th/T, math.log(2)/-re[0], math.log(2)/-re[1])
assert abs(T-6.64) < 0.01 and abs(th-21) < 0.1 and abs(th/T-3.16) < 0.01 and abs(math.log(2)/-re[1]-95) < 0.1 and abs(math.log(2)/-re[0]-1.23) < 0.01
assert abs(-(2*dr.real+re[0]+re[1])-B) < 1e-3'''),
 code('''def zeta(dn):
    M = A.copy(); M[2,2] -= dn; e = [x for x in np.linalg.eigvals(M) if x.imag > 0][0]; return -e.real/abs(e)
print([round(zeta(x), 3) for x in (0, 0.25, 0.5, 1)])
assert abs(zeta(0)-0.0349) < 1e-3 and abs(zeta(0.5)-0.2947) < 1e-3
w, V = np.linalg.eig(A); Vi = np.linalg.inv(V)
x = (V@np.diag(np.exp(w*30))@Vi@np.array([10,0,0,0])).real; print(x); assert abs(x[0]+3.521) < 1e-3
print("All Module 08 checks passed.")''')])
