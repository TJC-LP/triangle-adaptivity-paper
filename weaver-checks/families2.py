import sys; sys.path.insert(0, '/workspace/review')
from lib import *
from fractions import Fraction
import random, math

print("== Theorem 5.14(1): F_a ==")
def Fa(a):
    R = [(('x', i), ('y', j)) for i in range(a) for j in range(a)]
    S = [(('y', i), ('z', i, k)) for i in range(a) for k in range(a)]
    T = [(('z', i, k), ('x', i)) for i in range(a) for k in range(a)]
    return Inst(R, S, T)
for a in (2, 3, 5):
    I = Fa(a); fwd, rev = I.moments()
    print(f"a={a}: M={I.M()} (paper a^3,a^2,a^2={a**3},{a**2},{a**2}), C={I.per_root()} (paper 2a^2={2*a*a} each), Out={I.out()} (a^2={a*a}), N={I.N} (3a^2={3*a*a}), "
          f"reduced={I.semijoin_reduced()}, fwd={fwd} rev={rev} (paper a^3,a^3,a^2 / a^3,a^2,a^3), B2^3={I.B2_cubed()} = a^8={a**8}")

print("\n== GMR(m) = E(m^3, m, m) ==")
def E(L, a, h):
    X = [('x', i) for i in range(L)]; Y = [('y', j) for j in range(a)]; Z1 = [('z1', k) for k in range(h)]
    R = [(x, y) for x in X for y in Y]; S = [(y, z) for y in Y for z in Z1]
    T = [(('z0', x, j), x) for x in X for j in range(h)]
    return Inst(R, S, T)
for m in (2, 3, 4):
    I = E(m**3, m, m); fwd, rev = I.moments()
    print(f"m={m}: M={I.M()} (paper m^5,0,0={m**5}), C={I.per_root()} -> C={I.C()} (paper 0), N={I.N} (paper 2m^4+m^2={2*m**4+m**2}), B2^3={I.B2_cubed()} vs m^12={m**12}, Out={I.out()}")
for u in (1, 2, 3):
    I = E(u**3, 6*u, 6*u); fwd, rev = I.moments(); B2 = icbrt(I.B2_cubed())
    print(f"sharp family E(u^3,6u,6u) u={u}: N={I.N} (paper {12*u**4+36*u*u}), B2={B2} (paper {36*u**4}, cube exact {B2**3 == I.B2_cubed()}), M_R={I.M()[0]} (paper {36*u**5})")

print("\n== GMIN(m) ==")
def GMIN(m):
    X0 = [('x0', i) for i in range(m**3)]; X1 = [('x1', i) for i in range(m**5)]; X2 = [('x2', i) for i in range(m**2)]; X3 = [('x3', i) for i in range(m)]
    Y0 = [('y0', i) for i in range(m)]; Y1 = [('y1', i) for i in range(m**3)]; Y2 = [('y2', i) for i in range(m**2)]; Y3 = [('y3', i) for i in range(m**5)]
    Z0 = [('z0', i) for i in range(m**5)]; Z1 = [('z1', i) for i in range(m**2)]; Z2 = [('z2', i) for i in range(m)]; Z3 = [('z3', i) for i in range(m**3)]
    R = [(x, y) for x in X0 for y in Y0] + biregular(X1, Y1, 1) + [(x, y) for x in X3 for y in Y2]
    S = [(y, z) for y in Y0 for z in Z1] + [(y, z) for y in Y1 for z in Z2] + biregular(Y3, Z3, 1)
    T = biregular(Z0, X0, 1) + [(z, x) for z in Z2 for x in X2] + [(z, x) for z in Z3 for x in X3]
    return Inst(R, S, T)
for m in (2, 3, 4):
    I = GMIN(m); fwd, rev = I.moments(); B2 = icbrt(I.B2_cubed())
    print(f"m={m}: M={I.M()} (paper m^6={m**6} each), C={I.per_root()} (paper m^5+m^3={m**5+m**3} each), N={I.N} (paper {3*(m**5+m**4+m**3)}), fwd={fwd} (paper 3m^5={3*m**5}), rev={rev}, B2={B2} exact={B2**3==I.B2_cubed()}, Out={I.out()}, "
          f"minM/(N+B2)={min(I.M())/(I.N+B2):.3f} >= m/9={m/9:.3f}")
    P, p = pad(I); B2p = icbrt(P.B2_cubed())
    print(f"   padded: reduced={P.semijoin_reduced()}, N'={P.N} (<=7N: {P.N <= 7*I.N}), Out'={P.out()}, C'={P.C()} (<= C+9N: {P.C() <= I.C() + 9*I.N}), minM'={min(P.M())} (>= m^6: {min(P.M()) >= m**6}), B2'~{B2p}; "
          f"paper Thm 5.27 padded N'={12*m**5+3*m**4+3*m**3+9*m**2}, Out'={3*m**5+3*m**2}")

print("\n== H_a ==")
def Ha(a):
    X = [('x', i) for i in range(a)]; Y1 = [('y1', i) for i in range(a)]; Y2 = [('y2', i) for i in range(a)]
    Z1 = [('z1', i, k) for i in range(a) for k in range(a)]; Z2 = [('z2', i) for i in range(a)]
    R = [(x, y) for x in X for y in Y1]
    S = [(('y1', i), ('z1', i, k)) for i in range(a) for k in range(a)] + [(y, z) for y in Y2 for z in Z2]
    T = [(z, x) for z in Z2 for x in X]
    return Inst(R, S, T)
for a in (2, 4, 8):
    I = Ha(a); P, p = pad(I)
    Cx, Cy, Cz = P.per_root()
    print(f"a={a}: C={I.per_root()} (paper a^3+a^2={a**3+a**2}, a^2, a^2), Out={I.out()}, N={I.N} (4a^2={4*a*a}); padded reduced={P.semijoin_reduced()}, Cx'={Cx}>=a^3: {Cx>=a**3}, C'={P.C()}, N'={P.N}, Cx'/(C'+N')={Cx/(P.C()+P.N):.2f} (paper a=4: 0.61, a=8: 0.97)")

print("\n== Proposition 5.22: Ferrers profiles ==")
for k in (1, 2, 3):
    X = {b: [('x', b, i) for i in range(k)] for b in range(3)}; Y = {b: [('y', b, i) for i in range(k)] for b in range(3)}; Z = {b: [('z', b, i) for i in range(k)] for b in range(3)}
    blk = lambda A, B: [(u, v) for u in A for v in B]
    R = blk(X[1], Y[2]) + blk(X[2], Y[1]) + blk(X[2], Y[2])
    S = blk(Y[1], Z[1]) + blk(Y[1], Z[2]) + blk(Y[2], Z[2])
    T = blk(Z[0], X[1]) + blk(Z[1], X[1]) + blk(Z[0], X[2])
    I = Inst(R, S, T)
    print(f"k={k}: N={I.N} (9k^2={9*k*k}), Out={I.out()}, C={I.per_root()} (paper k^3+2k^2, k^3+2k^2, k^3+k^2 = {k**3+2*k*k},{k**3+2*k*k},{k**3+k*k}), M={I.M()} (paper 3k^3,k^3,k^3), moments={I.moments()} (paper 5k^3={5*k**3} each)")

print("\n== Proposition 9.1 (stride grid, 64 samples) ==")
def prop91(m, k=64):
    P = sorted({(s * m * m) // k for s in range(k)})
    J = {q % m for q in P}; j = len(J)
    live = [i for i in range(m) if i not in J]
    ZS = ['z0'] + [('z', 2*i) for i in range(1, m)]; ZT = ['z0'] + [('z', 2*i+1) for i in range(1, m)]
    R = [(('x', i), ('y', l)) for i in range(m) for l in range(m)]
    S = [(('y', l), z) for l in live for z in ZS]; S += [(('py', t), ('pz', t)) for t in range(m*m + 1 - len(S))]
    T = [(z, ('x', i)) for z in ZT for i in range(m)]; T += [(('pz2', t), ('px', t)) for t in range(m*m + 1 - len(T))]
    I = Inst(R, S, T)
    # sampled estimate for driver R: rows at positions P in (x,y) order
    rows = [(('x', q // m), ('y', q % m)) for q in P]
    Mhat = (m*m) * sum(min(I.dSp[y], I.dTm[x]) for x, y in rows) // k
    MR, MS, MT = I.M()
    return dict(j=j, Mhat_R=Mhat, M=(MR, MS, MT), Out=I.out(), N=I.N, claim2=(MR == m*m*(m-j) and MS == m*(m-j) and MT == m*(m-j) and I.out() == m*(m-j)),
                ratio=Fraction(2*m*m + MR, min(2*len(I.S)+MS, 2*len(I.T)+MT)), m_over_8=Fraction(m, 8))
for m in (65, 96, 128):
    print(f"m={m}: {prop91(m)}")

print("\n== Theorem 3.7 family and Theorem 3.1 on random regular stats (float sigma via exact-ish power iteration not needed: use block construction) ==")
def U_terms(r, s):
    rR, rS, rT = r; sR, sS, sT = s
    H = [math.sqrt(sR*rS*rT), math.sqrt(sS*rR*rT), math.sqrt(sT*rR*rS)]
    Dg = [rR*sS, rR*sT, rS*sR, rS*sT, rT*sR, rT*sS]
    return min(H + Dg)
def blk_witness(r, sig):
    rR, rS, rT = r; s = [min(x*x, y) for x, y in zip(sig, r)]
    U = U_terms(r, s)
    a = math.floor(max(1, U/rS)); b = math.floor(max(1, U/rT)); c = math.floor(max(1, U/rR))
    m = math.floor(min(rR/(a*b), rS/(b*c), rT/(c*a)))
    # admissibility: ab<=sR etc, sizes, Out
    ok = a*b <= s[0] + 1e-9 and b*c <= s[1] + 1e-9 and c*a <= s[2] + 1e-9 and m >= 1 and m*a*b <= rR and m*b*c <= rS and m*c*a <= rT
    return U, m*a*b*c, ok
random.seed(1)
worst = 10
bad = 0
for _ in range(200000):
    r = [random.choice([1, 2, 3, 5, 8, 13, 50, 100, 1000, 10**4, 10**5]) * random.uniform(1, 3) for _ in range(3)]
    sig = [random.uniform(1, math.sqrt(x)) for x in r]
    U, out, ok = blk_witness(r, sig)
    if not ok: bad += 1
    worst = min(worst, out / U)
print(f"random regular stats: block witness admissible in all cases: {bad == 0}; min Out/U over 200k = {worst:.4f} (must be > 0.25)")
for t in (1.0, 1.5, 1.9, 1.99):
    r = (t*t, t, t*t); sig = (math.sqrt(t), 1, math.sqrt(t)); s = [min(x*x, y) for x, y in zip(sig, r)]
    print(f"Thm 3.7 t={t}: U={U_terms(r, s):.4f} (t^2={t*t:.4f}), block witness Out={blk_witness(r, sig)[1]}")
