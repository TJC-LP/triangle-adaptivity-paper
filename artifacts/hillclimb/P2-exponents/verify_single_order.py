from collections import Counter, defaultdict
from fractions import Fraction

def evaluate(p,q,h):
    X=range(p); Y=range(q)
    R={(x,y) for x in X for y in Y}
    S={(y,('s',z)) for y in Y for z in range(h)}
    T={(('t',x,k),x) for x in X for k in range(h)}
    rp=Counter(x for x,y in R); rm=Counter(y for x,y in R)
    sp=Counter(y for y,z in S); sm=Counter(z for y,z in S)
    tp=Counter(z for z,x in T); tm=Counter(x for z,x in T)
    norms=tuple(sum(d*d for d in c.values()) for c in (rp,sp,tp,rm,sm,tm))
    MR=sum(min(sp[y],tm[x]) for x,y in R)
    MS=sum(min(tp[z],rm[y]) for y,z in S)
    MT=sum(min(rp[x],sm[z]) for z,x in T)
    costs=[defaultdict(lambda:[0,0]) for _ in range(3)]
    for x,y in R:
        v=1+min(sp[y],tm[x]); costs[0][x][0]+=v;costs[1][y][0]+=v
    for y,z in S:
        v=1+min(tp[z],rm[y]); costs[1][y][1]+=v;costs[2][z][0]+=v
    for z,x in T:
        v=1+min(rp[x],sm[z]); costs[2][z][1]+=v;costs[0][x][1]+=v
    Cs=tuple(sum(min(v) for v in c.values()) for c in costs)
    sx=defaultdict(set);tx=defaultdict(set)
    for y,z in S:sx[y].add(z)
    for z,x in T:tx[x].add(z)
    out=sum(len(sx[y]&tx[x]) for x,y in R)
    r,s,t=len(R),len(S),len(T)
    a,b,g,ap,bp,gp=norms
    assert MR**4<=r*t*t*a*b
    assert MR**4<=r*s*s*ap*gp
    return (r+s+t, norms, (MR,MS,MT), Cs, out)

print('GMR: m N B2 MR MS MT Cx Cy Cz Out ratio_M_to_NplusB')
for m in range(1,13):
    N,norms,Ms,Cs,out=evaluate(m**3,m,m)
    assert norms==(m**5,m**3,m**4,m**7,m**3,m**5)
    assert N==2*m**4+m**2 and Ms==(m**5,0,0) and Cs==(m**4,m**2,0) and out==0
    B=m**4
    assert B**3==min(norms[0]*norms[1]*norms[2],norms[3]*norms[4]*norms[5])
    print(m,N,B,*Ms,*Cs,out,Fraction(Ms[0],N+B))
print('H: u N B2 MR MS MT Cx Cy Cz Out ratio_M_to_NplusB Qf Qr')
for u in range(1,7):
    N,norms,Ms,Cs,out=evaluate(u**3,6*u,6*u)
    assert norms==(36*u**5,216*u**3,6*u**4,6*u**7,216*u**3,36*u**5)
    assert N==12*u**4+36*u**2 and Ms==(36*u**5,0,0) and Cs==(6*u**4,36*u**2,0) and out==0
    B=36*u**4
    Qf=norms[0]*norms[1]*norms[2];Qr=norms[3]*norms[4]*norms[5]
    assert B**3==min(Qf,Qr)
    assert Ms[0]**4==(6*u**4)*(6*u**4)**2*norms[0]*norms[1]
    print(u,N,B,*Ms,*Cs,out,Fraction(Ms[0],N+B),Qf,Qr)
print('All exact family checks passed.')
