"""Exact checks for the single-predicate section and Thm 5.3 repair. python3 -I."""
from collections import defaultdict
from fractions import Fraction as Fr
import random, math

def deg(E):
    o, i = defaultdict(int), defaultdict(int)
    for a, b in E: o[a] += 1; i[b] += 1
    return o, i

def stats(R, S, T):
    R, S, T = set(R), set(S), set(T)
    Ro, Ri = deg(R); So, Si = deg(S); To, Ti = deg(T)
    Rf = defaultdict(list); Rb = defaultdict(list)
    for x, y in R: Rf[x].append(y); Rb[y].append(x)
    Sf = defaultdict(list); Sb = defaultdict(list)
    for y, z in S: Sf[y].append(z); Sb[z].append(y)
    Tf = defaultdict(list); Tb = defaultdict(list)
    for z, x in T: Tf[z].append(x); Tb[x].append(z)
    eR = lambda x, y: 1 + min(So[y], Ti[x])
    eS = lambda y, z: 1 + min(Ri[y], To[z])
    eT = lambda z, x: 1 + min(Ro[x], Si[z])
    Cx = sum(min(sum(eR(x, y) for y in Rf[x]), sum(eT(z, x) for z in Tb[x])) for x in set(Rf) | set(Tb))
    Cy = sum(min(sum(eR(x, y) for x in Rb[y]), sum(eS(y, z) for z in Sf[y])) for y in set(Rb) | set(Sf))
    Cz = sum(min(sum(eS(y, z) for y in Sb[z]), sum(eT(z, x) for x in Tf[z])) for z in set(Sb) | set(Tf))
    MR = sum(min(So[y], Ti[x]) for x, y in R)
    MS = sum(min(To[z], Ri[y]) for y, z in S)
    MT = sum(min(Ro[x], Si[z]) for z, x in T)
    sq = lambda d: sum(v * v for v in d.values())
    fw = (sq(Ro), sq(So), sq(To)); rv = (sq(Ri), sq(Si), sq(Ti))
    out = sum(1 for x, y in R for z in Sf[y] if (z, x) in T)
    return dict(Cx=Cx, Cy=Cy, Cz=Cz, C=min(Cx, Cy, Cz), M=(MR, MS, MT), N=len(R) + len(S) + len(T),
                sizes=(len(R), len(S), len(T)), fw=fw, rv=rv, Q=min(fw[0]*fw[1]*fw[2], rv[0]*rv[1]*rv[2]), out=out)

def icbrt_exact(Q):  # B2 = Q^{1/3}; return exact if perfect cube else None
    r = round(Q ** (1/3))
    for c in (r-1, r, r+1):
        if c**3 == Q: return c
    return None

def G8(m):
    X = [('x', i) for i in range(m**4)]; Y0 = [('y0', i) for i in range(m**2)]
    Z1 = [('z1', i) for i in range(m**3)]
    Z2 = [('z2', g, t) for g in range(m**3) for t in range(m**3)]
    Xg = lambda g: [('x', g*m + h) for h in range(m)]
    R = [(x, y) for x in X for y in Y0]
    S = [(y, z) for y in Y0 for z in Z1] + [(('y2', z, k), z) for z in Z2 for k in range(m**2)]
    T = [(('z0', x, k), x) for x in X for k in range(m**4)] + [(z, x) for z in Z2 for x in Xg(z[1])]
    return R, S, T

def single(R, S, T):
    P = set(R) | set(S) | set(T)
    return P, P, P

def Fa(a):
    R = [(('x', i), ('y', j)) for i in range(a) for j in range(a)]
    S = [(('y', i), ('z', i, k)) for i in range(a) for k in range(a)]
    T = [(('z', i, k), ('x', i)) for i in range(a) for k in range(a)]
    return R, S, T

def GMIN(m):
    def part(n, p, k): return [(n, p, i) for i in range(k)]
    X0, X1, X2, X3 = part('x',0,m**3), part('x',1,m**5), part('x',2,m**2), part('x',3,m)
    Y0, Y1, Y2, Y3 = part('y',0,m), part('y',1,m**3), part('y',2,m**2), part('y',3,m**5)
    Z0, Z1, Z2, Z3 = part('z',0,m**5), part('z',1,m**2), part('z',2,m), part('z',3,m**3)
    R = [(x, y) for x in X0 for y in Y0] + [(X1[i], Y1[i // m**2]) for i in range(m**5)] + [(x, y) for x in X3 for y in Y2]
    S = [(y, z) for y in Y0 for z in Z1] + [(y, z) for y in Y1 for z in Z2] + [(Y3[i], Z3[i // m**2]) for i in range(m**5)]
    T = [(Z0[i], X0[i // m**2]) for i in range(m**5)] + [(z, x) for z in Z2 for x in X2] + [(z, x) for z in Z3 for x in X3]
    return R, S, T

def main():
    print("== single predicate, one G8(m)")
    for m in (2, 3):
        R, S, T = G8(m); g = stats(R, S, T); p = stats(*single(R, S, T))
        assert p['Cx'] == p['Cy'] == p['Cz'] == g['Cx'] + g['Cy'] + g['Cz'] == m**9 + m**8 + m**6 + m**5
        assert p['N'] == 3 * g['N'] == 3 * (2*m**8 + m**7 + m**6 + m**5)
        assert p['fw'] == (sum(g['fw']),) * 3 and p['rv'] == (sum(g['rv']),) * 3
        assert sum(g['fw']) == 5 * m**8 and sum(g['rv']) == m**12 + 2*m**11 + 3*m**10 + m**7
        assert p['M'] == (sum(g['M']),) * 3 and p['out'] == 3 * g['out'] == 0
        print(f"m={m}: N_P={p['N']} B2_P={5*m**8} C_P={p['C']} M_P={p['M'][0]}")

    print("== single predicate, F_a")
    for a in (2, 3, 4, 5, 8):
        R, S, T = Fa(a); g = stats(R, S, T); p = stats(*single(R, S, T))
        assert p['N'] == 9 * a * a and p['C'] == 6 * a * a and p['out'] == 3 * a * a
        assert all(len(set(R) | set(S) | set(T)) + mm == a**3 + 5*a*a for mm in p['M'])
        print(f"a={a}: N_P={p['N']} C_P={p['C']} every GAO={3*a*a + p['M'][0]} Out_P={p['out']}")

    print("== single predicate, GMIN(m)")
    for m in (2, 3, 4):
        R, S, T = GMIN(m); g = stats(R, S, T); p = stats(*single(R, S, T))
        assert g['M'] == (m**6,) * 3 and g['C'] == m**5 + m**3
        assert p['M'] == (3 * m**6,) * 3 and p['N'] == 9 * (m**5 + m**4 + m**3)
        assert p['fw'] == (9 * m**5,) * 3 and p['rv'][0] >= p['fw'][0]
        print(f"m={m}: N_P={p['N']} B2_P={9*m**5} M_P={p['M'][0]} C_P={p['C']} ratio GAO/(N+B2)={Fr(p['M'][0] + p['N']//3, p['N'] + 9*m**5)}")

    print("== symmetric predicate: C <= |P| + sum d^2, equality structure")
    rng = random.Random(3313); worst = Fr(0)
    for it in range(4000):
        n = rng.randint(2, 10); E = set()
        for _ in range(rng.randint(1, n * n)):
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b: E.add((a, b)); E.add((b, a))
        if not E: continue
        st = stats(E, E, E)
        o, _ = deg(E); B2 = sum(v * v for v in o.values())
        assert st['fw'] == st['rv'] == (B2,) * 3
        assert st['Cx'] == st['Cy'] == st['Cz'] <= len(E) + B2
        worst = max(worst, Fr(st['C'], len(E) + B2))
    print("max C/(|P|+B2) =", worst)

    print("== Theorem 5.3 repair: referee counterexample K_{2,3,3} + 10 stray R-edges")
    X = [('x', i) for i in range(2)]; Y = [('y', i) for i in range(3)]; Z = [('z', i) for i in range(3)]
    R = [(x, y) for x in X for y in Y] + [(('xs', i), ('ys', i)) for i in range(10)]
    S = [(y, z) for y in Y for z in Z]; T = [(z, x) for z in Z for x in X]
    st = stats(R, S, T)
    print(st['sizes'], (st['Cx'], st['Cy'], st['Cz']))
    Hx = st['Cx'] - st['sizes'][0] - st['sizes'][2]; Hy = st['Cy'] - st['sizes'][0] - st['sizes'][1]; Hz = st['Cz'] - st['sizes'][1] - st['sizes'][2]
    print("signed H =", (Hx, Hy, Hz), "product", Hx*Hy*Hz)
    assert (Hx, Hy, Hz) == (2, -1, 9)


if __name__ == "__main__":
    main()
