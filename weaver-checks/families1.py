"""Rebuild every explicit family of Section 5 and compare with the paper's closed forms / tables."""
import sys; sys.path.insert(0, '/workspace/review')
from lib import *
from fractions import Fraction

def G8(m):
    X = [('x', i) for i in range(m**4)]
    Y0 = [('y0', i) for i in range(m**2)]
    Y2 = [('y2', i) for i in range(m**8)]
    Z0 = [('z0', i) for i in range(m**8)]
    Z1 = [('z1', i) for i in range(m**3)]
    Z2 = [('z2', i) for i in range(m**6)]
    R = [(x, y) for x in X for y in Y0]
    S = [(y, z) for y in Y0 for z in Z1] + biregular(Y2, Z2, 1)
    T = biregular(Z0, X, 1) + biregular(Z2, X, m)
    return Inst(R, S, T)

print("== Theorem 5.6 / Table 4: U(m) = G8(m) + two rotations ==")
for m in (2, 3):
    U = three_rotations(G8(m))
    Cx, Cy, Cz = U.per_root(); N = U.N; b3 = U.B2_cubed(); B2 = icbrt(b3)
    assert B2**3 == b3, "B2 not an exact cube"
    print(f"m={m}: N={N} (paper {3*(2*m**8+m**7+m**6+m**5)}), B2={B2} (paper {5*m**8}), "
          f"C=({Cx},{Cy},{Cz}) (paper {m**9+m**8+m**6+m**5}), Out={U.out()}, "
          f"C/(N+B2)={min(Cx,Cy,Cz)/(N+B2):.3f}, forward moments={U.moments()[0]}, reverse={U.moments()[1]}")
    # Theorem 5.3 bound ratio (Table 4 last column)
    import math
    r, s, t = U.sizes()
    bound = N + (r*s*t)**(1/8) * (min(U.moments()[0][0]*U.moments()[0][1]*U.moments()[0][2], U.moments()[1][0]*U.moments()[1][1]*U.moments()[1][2]))**(1/4)
    print(f"   C/bound(Thm5.3) = {min(Cx,Cy,Cz)/bound:.3f} (paper {[0.182,0.192][m-2]})")
    # single G8: C_x, C_y, C_z (Theorem 5.14(3))
    g = G8(m); print(f"   single G8: C=({g.per_root()}) paper (m^9+m^6, m^5, m^8)=({m**9+m**6},{m**5},{m**8}); sizes {g.sizes()} paper ({m**6},{m**5+m**8},{m**8+m**7})")

print("\n== Remark 5.9(a): padded U(m) ==")
for m in (2, 3):
    U = three_rotations(G8(m)); P, p = pad(U)
    assert P.semijoin_reduced()
    B2 = icbrt(P.B2_cubed())
    print(f"m={m}: padded N={P.N}, Out={P.out()}, C={P.C()} (>= m^9={m**9}: {P.C() >= m**9}), B2~{B2}, ratio C/(N+B2)={P.C()/(P.N+B2):.3f} (paper {[0.397,0.425][m-2]})")

print("\n== Theorem 5.11: F_{i,j}(u) ==")
def F(i, j, u):
    X = [('x', k) for k in range(u**(4*i))]
    Y0 = [('y0', k) for k in range(u**(4*i-2*j))]
    Y2 = [('y2', k) for k in range(u**(8*i))]
    Z1 = [('z1', k) for k in range(u**(4*i-j))]
    Z2 = [('z2', k) for k in range(u**(4*i+2*j))]
    R = [(x, y) for x in X for y in Y0]
    S = [(y, z) for y in Y0 for z in Z1] + biregular(Y2, Z2, 1)
    T = biregular(Z2, X, u**(4*i-3*j))
    return Inst(R, S, T)
for (i, j, u) in [(1, 1, 2), (1, 1, 3), (2, 1, 2)]:
    I = three_rotations(F(i, j, u)); N = I.N; B2 = icbrt(I.B2_cubed()); C = I.C()
    fwd = I.moments()[0]
    print(f"(i,j,u)=({i},{j},{u}): N={N} in [u^8i={u**(8*i)}, 12u^8i={12*u**(8*i)}]: {u**(8*i) <= N <= 12*u**(8*i)}; "
          f"C={C} >= u^(12i-3j)={u**(12*i-3*j)}: {C >= u**(12*i-3*j)}; B2={B2} <= 4u^(12i-4j)={4*u**(12*i-4*j)}: {B2 <= 4*u**(12*i-4*j)}; "
          f"fwd moments each = {fwd} (paper 3u^(12i-4j)+u^8i = {3*u**(12*i-4*j)+u**(8*i)}); "
          f"C/(N^(3/8) B2^(3/4)) = {C / (N**(3/8) * B2**0.75):.3f}")

print("\n== Section 5.3: first violation F_{1,1}(u) union, u=6,7 (closed forms) ==")
for u in (6, 7):
    C = u**9 + u**8 + u**6 + u**5; N = 3*(u**8 + u**7 + u**6 + u**5); B2 = 4*u**8
    print(f"u={u}: N={N:.3e}, C/(N+B2)={C/(N+B2):.3f}")
for m in (10, 11):
    C = m**9 + m**8 + m**6 + m**5; N = 3*(2*m**8 + m**7 + m**6 + m**5); B2 = 5*m**8
    print(f"U(m) m={m}: N={N:.3e}, C/(N+B2)={C/(N+B2):.3f}")
for m in (6, 7):
    C = m**9 + m**8 + m**6 + m**5; N = 3*(2*m**8 + m**7 + m**6 + m**5); abg = (5*m**8)**3
    print(f"U(m) cubic form m={m}: C^3/(N^3+abg) = {C**3/(N**3+abg):.3f}")

print("\n== Theorem 5.10: I_v (fully reduced) ==")
def Iv(v):
    rng = range(v)
    A3 = list(itertools.product(rng, repeat=3))
    X = [('x', A, B) for A in A3 for B in A3]
    Y0 = [('y0', t) for t in itertools.product(rng, repeat=4)]
    Z1 = [('z1', t) for t in itertools.product(rng, repeat=5)]
    Y2 = [('y2', A, B, E, e) for A in A3 for B in A3 for E in A3 for e in rng]
    Z2 = [('z2', A, E, F) for A in A3 for E in A3 for F in itertools.product(rng, repeat=2)]
    f = lambda A, B: ('z1', (A[0], A[1], A[2], B[0], B[1]))
    R = [(x, y) for x in X for y in Y0] + [(('x', A, B), ('y2', A, B, E, e)) for A in A3 for B in A3 for E in A3 for e in rng]
    S = [(y, z) for y in Y0 for z in Z1] + [(('y2', A, B, E, e), ('z2', A, E, F)) for A in A3 for B in A3 for E in A3 for e in rng for F in itertools.product(rng, repeat=2)]
    T = [(f(A, B), ('x', A, B)) for A in A3 for B in A3] + [(('z2', A, E, F), ('x', A, B)) for A in A3 for E in A3 for F in itertools.product(rng, repeat=2) for B in A3]
    return Inst(R, S, T)
for v in (1, 2):
    I = Iv(v)
    print(f"v={v}: fully reduced={I.fully_reduced()}, Out={I.out()} (paper v^10+v^12={v**10+v**12}), per-root={I.per_root()} "
          f"(paper Cx={v**15+v**11+v**10+v**6}, Cy={v**12+2*v**10+v**9}, Cz={2*v**12+v**10+v**6}), sizes={I.sizes()} (paper {(2*v**10, v**12+v**9, v**11+v**6)}), "
          f"moments={I.moments()} (paper fwd {(4*v**14, 2*v**14, v**14+v**7)}, rev {(v**16+v**10, v**16+v**13, v**16+2*v**11+v**6)})")
    U = three_rotations(I)
    print(f"   union: fully reduced={U.fully_reduced()}, N={U.N} (paper {3*(v**12+v**11+2*v**10+v**9+v**6)}), C={U.C()} (paper {v**15+3*v**12+v**11+4*v**10+v**9+2*v**6}), B2^3={U.B2_cubed()} vs (7v^14+v^7)^3={(7*v**14+v**7)**3}")
v = 8
C = v**15 + 3*v**12 + v**11 + 4*v**10 + v**9 + 2*v**6; N = 3*(v**12+v**11+2*v**10+v**9+v**6); B2 = 7*v**14 + v**7
print(f"v=8 closed form: C/(N+B2) = {C}/{N+B2} = {Fraction(C, N+B2)} (paper 45017942/39450457) -> {C/(N+B2):.4f}")

print("\n== Gadget D(L,a,h) and Theorem 5.13 ==")
def D(L, a, h):
    assert L % h == 0; b = L // h
    X = [('x', i, j) for i in range(h) for j in range(b)]
    Y0 = [('y0', k) for k in range(a)]
    Y2 = [('y2', i, j, k) for i in range(h) for j in range(h) for k in range(a)]
    Z1 = [('z1', i) for i in range(h)]
    Z2 = [('z2', i, j) for i in range(h) for j in range(h)]
    R = [(x, y) for x in X for y in Y0]
    S = [(y, z) for y in Y0 for z in Z1] + [(('y2', i, j, k), ('z2', i, j)) for i in range(h) for j in range(h) for k in range(a)]
    T = [(('z2', i, j), ('x', i, l)) for i in range(h) for j in range(h) for l in range(b)]
    return Inst(R, S, T)
for (L, a, h) in [(4, 2, 2), (8, 3, 4), (12, 5, 3), (16, 2, 8)]:
    I = D(L, a, h)
    exp = dict(sizes=(L*a, a*h + a*h*h, L*h), fwd=(L*a*a, 2*a*h*h, L*L), rev=(a*L*L, a*a*(h+h*h), L*h*h), M=(L*a*h, 0, L*a*h), C=(L*a*h + L*min(a, h), a*h, a*h*h))
    got = dict(sizes=I.sizes(), fwd=I.moments()[0], rev=I.moments()[1], M=I.M(), C=I.per_root())
    print(f"D({L},{a},{h}): match={got == exp}; Out={I.out()}" + ("" if got == exp else f"\n   got {got}\n   exp {exp}"))

def thm513(u, p, q):
    D1 = D(u**(8*p-4*q), u**(6*q-4*p), u**(6*p-3*q))
    D2 = D(u**(4*q), u**(4*p-2*q), u**(6*p-3*q))      # local R,S,T -> global S,T,R
    D3 = D(u**(4*p), u**(6*p-4*q), u**(6*q-3*p))      # local R,S,T -> global T,R,S
    # placing local (R,S,T) as global (S,T,R): global R = local T, global S = local R, global T = local S
    D2g = Inst(D2.T, D2.R, D2.S)
    # placing local (R,S,T) as global (T,R,S): global R = local S, global S = local T, global T = local R
    D3g = Inst(D3.S, D3.T, D3.R)
    return union(D1, D2g, D3g)
for (u, p, q) in [(2, 1, 1), (2, 9, 10)]:
    if (u, p, q) == (2, 9, 10):
        # too large to materialize (u^80); evaluate closed forms only
        N_hi = 12*u**(8*q); B2 = 4*u**(8*p); C = u**(10*p-q) + u**(4*p+2*q) + u**(16*p-8*q) + u**(3*p+2*q)
        Cy = u**(10*p-q) + u**(4*p+2*q) + u**(8*q) + u**(2*p+3*q)
        print(f"(u,p,q)=({u},{p},{q}) closed forms: C_x <= 4u^(10p-q): {C <= 4*u**(10*p-q)}; C_x<=C_y termwise: {C <= Cy}; "
              f"C/(N_hi+B2) in [{C/(N_hi+B2):.3f}, {C/(u**(8*q)+B2):.3f}] (paper 0.980 with exact N)")
        # exact N: sum of the twelve sizes
        def sizesD(L, a, h): return (L*a, a*h + a*h*h, L*h)
        N = sum(sizesD(u**(8*p-4*q), u**(6*q-4*p), u**(6*p-3*q))) + sum(sizesD(u**(4*q), u**(4*p-2*q), u**(6*p-3*q))) + sum(sizesD(u**(4*p), u**(6*p-4*q), u**(6*q-3*p)))
        print(f"   exact N={N:.4e}, C/(N+B2)={C/(N+B2):.4f}; N^(-1/8) B2^(5/4) / C = {N**(-1/8)*B2**1.25/C:.3f} (<= 4^(5/4)={4**1.25:.3f})")
        continue
    I = thm513(u, p, q); Cx, Cy, Cz = I.per_root()
    fwd, rev = I.moments()
    print(f"(u,p,q)=({u},{p},{q}): fwd={fwd} (paper {(4*u**(8*q), 4*u**(8*p), 4*u**(16*p-8*q))}), rev={rev} all >= fwd: {all(r >= f for r, f in zip(rev, fwd))}; "
          f"C=({Cx},{Cy},{Cz}) paper Cx={u**(10*p-q)+u**(4*p+2*q)+u**(16*p-8*q)+u**(3*p+2*q)}, Cy={u**(10*p-q)+u**(4*p+2*q)+u**(8*q)+u**(2*p+3*q)}, Cz={u**(7*p+2*q)+u**(10*p-4*q)+u**(8*p)+u**(10*p-5*q)}; "
          f"N={I.N} in [u^8q, 12u^8q]=[{u**(8*q)},{12*u**(8*q)}]")
    # compare with F_{1,1}(2) union at p=q=1 (paper says D(u^4i,u^2i,u^3i) = F_{i,i}(u))
    J = three_rotations(F(1, 1, 2))
    print(f"   vs F_1,1(2) union: C {J.C()} vs {I.C()}, N {J.N} vs {I.N}, B2^3 {J.B2_cubed()} vs {I.B2_cubed()}")
