# Independent check of Theorem 1.L (G8 and its rotation union), cycle form:
# E1 ⊆ X×Y, E2 ⊆ Y×Z, E3 ⊆ Z×X ; triangle (x,y,z) needs all three.
# A_v for root class v: per vertex, min over the two incident cycle edges of
#   Σ_{u ∈ N_e(v)} (1 + min(|other edge list at v|, |third-edge list at u toward the remaining class|)).
from collections import defaultdict
import sys
def nbrs(E):
    out, inn = defaultdict(list), defaultdict(list)
    for a, b in E: out[a].append(b); inn[b].append(a)
    return out, inn
def costs(E1, E2, E3):
    o1,i1 = nbrs(E1); o2,i2 = nbrs(E2); o3,i3 = nbrs(E3)
    # root x: options via y∈o1[x] (other at x: i3[x] list of z; at y: o2[y]) or via z∈i3[x] (other at x: o1[x]; at z: i2[z])
    Ax = sum(min(sum(1+min(len(i3[x]),len(o2[y])) for y in o1[x]),
                 sum(1+min(len(o1[x]),len(i2[z])) for z in i3[x])) for x in set(o1)|set(i3))
    Ay = sum(min(sum(1+min(len(o2[y]),len(i3[x])) for x in i1[y]),
                 sum(1+min(len(i1[y]),len(o3[z])) for z in o2[y])) for y in set(i1)|set(o2))
    Az = sum(min(sum(1+min(len(o3[z]),len(i1[y])) for y in i2[z]),
                 sum(1+min(len(i2[z]),len(o1[x])) for x in o3[z])) for z in set(i2)|set(o3))
    N = len(E1)+len(E2)+len(E3)
    a = sum(len(v)**2 for v in o1.values()); b = sum(len(v)**2 for v in o2.values()); c = sum(len(v)**2 for v in o3.values())
    a_ = sum(len(v)**2 for v in i1.values()); b_ = sum(len(v)**2 for v in i2.values()); c_ = sum(len(v)**2 for v in i3.values())
    tri = sum(1 for (x,y) in E1 for z in o2[y] if x in set(o3[z]))
    return Ax, Ay, Az, N, (a,b,c), (a_,b_,c_), tri
def biregular(L, R, dout):  # |L|*dout == |R|*din, circulant
    return [(L[i], R[(i*dout + j) % len(R)]) for i in range(len(L)) for j in range(dout)]
def G8(m, tag):
    X=[f'{tag}x{i}' for i in range(m**4)]; Y0=[f'{tag}y0_{i}' for i in range(m**2)]; Y2=[f'{tag}y2_{i}' for i in range(m**8)]
    Z0=[f'{tag}z0_{i}' for i in range(m**8)]; Z1=[f'{tag}z1_{i}' for i in range(m**3)]; Z2=[f'{tag}z2_{i}' for i in range(m**6)]
    E1 = [(x,y) for x in X for y in Y0]                         # R complete X×Y0
    T  = biregular(X, Z0, m**4) + biregular(X, Z2, m**3)        # T: X→Z
    E3 = [(z,x) for (x,z) in T]                                  # cycle form z→x
    E2 = [(y,z) for y in Y0 for z in Z1] + biregular(Y2, Z2, 1)  # S
    return E1, E2, E3
for m in [2, 3]:
    E1,E2,E3 = G8(m,'g')
    Ax,Ay,Az,N,fw,rv,tri = costs(E1,E2,E3)
    assert (Ax,Ay,Az)==(m**9+m**6, m**5, m**8), (m,Ax,Ay,Az)
    assert N == 2*m**8+m**7+m**6+m**5 and fw==(m**8,2*m**8,2*m**8), (N,fw)
    # rotation union: rotate roles (E1,E2,E3)->(E2,E3,E1) with fresh labels
    F1,F2,F3 = G8(m,'h'); H1,H2,H3 = G8(m,'k')
    U1 = E1 + F3 + H2; U2 = E2 + F1 + H3; U3 = E3 + F2 + H1
    UAx,UAy,UAz,UN,ufw,urv,utri = costs(U1,U2,U3)
    want = m**9+m**8+m**6+m**5
    assert UAx==UAy==UAz==want, (UAx,UAy,UAz,want)
    L2 = (ufw[0]*ufw[1]*ufw[2])**0.5; L2r=(urv[0]*urv[1]*urv[2])**0.5; B2 = min(L2,L2r)**(2/3)
    A = min(UAx,UAy,UAz)
    print(f"m={m}: G8 A=({Ax},{Ay},{Az}) | U: N={UN} fw={ufw} B2={B2:.0f} A={A} A/(N+B2)={A/(UN+B2):.3f} thm1U={UN+(len(U1)*len(U2)*len(U3))**0.125*min(L2,L2r)**0.5:.0f} triangles={utri}")
