from collections import defaultdict
from fractions import Fraction

def profiles(R,S,T):
    def idx(E):
        f,b=defaultdict(set),defaultdict(set)
        for a,c in E: f[a].add(c); b[c].add(a)
        return f,b
    rf,rb=idx(R); sf,sb=idx(S); tf,tb=idx(T)
    norms=tuple(sum(len(v)**2 for v in d.values()) for d in (rf,sf,tf,rb,sb,tb))
    M=(sum(min(len(sf[y]),len(tb[x])) for x,y in R),
       sum(min(len(tf[z]),len(rb[y])) for y,z in S),
       sum(min(len(rf[x]),len(sb[z])) for z,x in T))
    C=(sum(min(sum(1+min(len(sf[y]),len(tb[x])) for y in rf[x]),
                   sum(1+min(len(rf[x]),len(sb[z])) for z in tb[x])) for x in rf.keys()|tb.keys()),
       sum(min(sum(1+min(len(tf[z]),len(rb[y])) for z in sf[y]),
                   sum(1+min(len(sf[y]),len(tb[x])) for x in rb[y])) for y in rb.keys()|sf.keys()),
       sum(min(sum(1+min(len(rf[x]),len(sb[z])) for x in tf[z]),
                   sum(1+min(len(tf[z]),len(rb[y])) for y in sb[z])) for z in sb.keys()|tf.keys()))
    return len(R)+len(S)+len(T),norms,M,C,(rf,rb,sf,sb,tf,tb)

def transitions(a,b):
    assert a.isdisjoint(b)
    order=sorted([(v,0) for v in a]+[(v,1) for v in b])
    return sum(order[k][1]!=order[k+1][1] for k in range(len(order)-1))

def pad(R,S,T):
    _,_,_,_,(rf,rb,sf,sb,tf,tb)=profiles(R,S,T)
    R,S,T=set(R),set(S),set(T)
    serial=0
    for typ,d1,d2 in [('x',rf,tb),('y',rb,sf),('z',sb,tf)]:
        for v in sorted(d1.keys()|d2.keys()):
            if bool(d1[v])==bool(d2[v]): continue
            fresh={t:(t,-1,serial) for t in ['x','y','z']}
            fresh[typ]=v
            R.add((fresh['x'],fresh['y']))
            S.add((fresh['y'],fresh['z']))
            T.add((fresh['z'],fresh['x']))
            serial+=1
    return R,S,T,serial

def summary(R,S,T,cert):
    N,norms,M,C,_=profiles(R,S,T)
    b2cube=min(norms[0]*norms[1]*norms[2],norms[3]*norms[4]*norms[5])
    return dict(sizes=(len(R),len(S),len(T)),N=N,norms=norms,B2cube=b2cube,M=M,C=C,cert=cert)

def cf(a):
    X=list(range(a));Y=list(range(a));Z={(i,k):k*a+i for i in range(a) for k in range(a)}
    R={(x,y) for x in X for y in Y};S={(i,Z[i,k]) for i in Y for k in range(a)};T={(Z[i,k],i) for i in X for k in range(a)}
    N,norms,M,C,ix=profiles(R,S,T);rf,rb,sf,sb,tf,tb=ix
    cert=sum(transitions(sf[y],tb[x]) for x,y in R if x!=y)
    assert cert==a*(a-1)*(2*a-1)
    assert (N,M,C)==(3*a*a,(a**3,a*a,a*a),(2*a*a,)*3)
    return a,summary(R,S,T,(cert,0,0))

def gmr(m):
    nx=m**3
    A=[k*(nx+1) for k in range(m)]
    B={x:[k*(nx+1)+1+x for k in range(m)] for x in range(nx)}
    R={(x,y) for x in range(nx) for y in range(m)}
    S={(y,z) for y in range(m) for z in A}
    T={(z,x) for x in range(nx) for z in B[x]}
    N,norms,M,C,ix=profiles(R,S,T);rf,rb,sf,sb,tf,tb=ix
    cert=sum(transitions(sf[y],tb[x]) for x,y in R)
    assert cert==m**4*(2*m-1)
    assert (N,M,min(C))==(2*m**4+m*m,(m**5,0,0),0)
    return m,summary(R,S,T,(cert,0,0))

def gmin(m,padded=False):
    # Each sort is a distinct opaque-key type, which may be concatenated.
    # Common size-m^2 group is first in each layer, then m^3 fibers.
    n=m**3;p=m*m
    Z1=[('z',0,k*(n+1)) for k in range(p)]
    Z0={x:[('z',0,k*(n+1)+x+1) for k in range(p)] for x in range(n)}
    X2=[('x',0,k*(n+1)) for k in range(p)]
    X1={y:[('x',0,k*(n+1)+y+1) for k in range(p)] for y in range(n)}
    Y2=[('y',0,k*(n+1)) for k in range(p)]
    Y3={z:[('y',0,k*(n+1)+z+1) for k in range(p)] for z in range(n)}
    X0=[('x',1,x) for x in range(n)]; X3=[('x',2,x) for x in range(m)]
    Y0=[('y',1,y) for y in range(m)]; Y1=[('y',2,y) for y in range(n)]
    Z2=[('z',1,z) for z in range(m)]; Z3=[('z',2,z) for z in range(n)]
    R={(x,y) for x in X0 for y in Y0}|{(x,Y1[y]) for y in range(n) for x in X1[y]}|{(x,y) for x in X3 for y in Y2}
    S={(y,z) for y in Y0 for z in Z1}|{(y,z) for y in Y1 for z in Z2}|{(y,Z3[z]) for z in range(n) for y in Y3[z]}
    T={(z,X0[x]) for x in range(n) for z in Z0[x]}|{(z,x) for z in Z2 for x in X2}|{(z,x) for z in Z3 for x in X3}
    if padded:
        R,S,T,padcount=pad(R,S,T)
        assert padcount==3*m**5+3*m*m
        N,norms,M,C,ix=profiles(R,S,T);rf,rb,sf,sb,tf,tb=ix
        cert=(sum(transitions(sf[y],tb[x]) for x in X0 for y in Y0),
              sum(transitions(tf[z],rb[y]) for y in Y1 for z in Z2),
              sum(transitions(rf[x],sb[z]) for z in Z3 for x in X3))
        assert cert==(m**4*(2*m*m-1),)*3
        assert N==12*m**5+3*m**4+3*m**3+9*m*m
        assert norms==(8*m**5+3*m*m,)*3+(2*m**7+m**4+3*m**5+2*m**3+3*m*m,)*3
        assert M==(m**6+4*m**5+m**3+3*m*m,)*3
        assert C==(8*m**5+2*m**3+6*m*m,)*3
        assert all(bool(rf[x])==bool(tb[x]) for x in rf.keys()|tb.keys())
        assert all(bool(rb[y])==bool(sf[y]) for y in rb.keys()|sf.keys())
        assert all(bool(sb[z])==bool(tf[z]) for z in sb.keys()|tf.keys())
        out=sum(len(sf[y]&tb[x]) for x,y in R)
        assert out==padcount
        return m,summary(R,S,T,cert),dict(padcount=padcount,Out=out)
    N,norms,M,C,ix=profiles(R,S,T);rf,rb,sf,sb,tf,tb=ix
    cert=(sum(transitions(sf[y],tb[x]) for x,y in R if sf[y] and tb[x]),
          sum(transitions(tf[z],rb[y]) for y,z in S if tf[z] and rb[y]),
          sum(transitions(rf[x],sb[z]) for z,x in T if rf[x] and sb[z]))
    assert cert==(m**4*(2*m*m-1),)*3
    assert (N,M,C)==(3*(m**5+m**4+m**3),(m**6,)*3,(m**5+m**3,)*3)
    assert norms[:3]==(3*m**5,)*3
    assert Fraction(m**6,N+3*m**5)>=Fraction(m,9)
    return m,summary(R,S,T,cert),Fraction(cert[0],N+3*m**5)

def ch(a,padded=False):
    X=[('x',0,i) for i in range(a)]
    Y1=[('y',0,2*i) for i in range(a)]
    Y2=[('y',0,2*i+1) for i in range(a)]
    Z2=[('z',0,k*(a+1)) for k in range(a)]
    Z1={i:[('z',0,k*(a+1)+i+1) for k in range(a)] for i in range(a)}
    R={(x,y) for x in X for y in Y1}
    S={(Y1[i],z) for i in range(a) for z in Z1[i]}|{(y,z) for y in Y2 for z in Z2}
    T={(z,x) for z in Z2 for x in X}
    if padded:R,S,T,padcount=pad(R,S,T)
    N,norms,M,C,ix=profiles(R,S,T);rf,rb,sf,sb,tf,tb=ix
    root_R=sum(transitions(sf[y],tb[x]) for x in X for y in Y1)
    root_T=sum(transitions(rf[x],sb[z]) for x in X for z in Z2)
    assert root_R==root_T==a*a*(2*a-1)
    if not padded:
        assert (N,C)==(4*a*a,(a**3+a*a,a*a,a*a))
    else:
        assert N==7*a*a+3*a
        assert C==(a**3+3*a*a+2*a,4*a*a+2*a,4*a*a+2*a)
    return a,summary(R,S,T,(root_R,0,root_T))

if __name__=='__main__':
    for name,fn in [('CF',cf),('GMR',gmr),('GMIN',gmin),('GMIN_PAD',lambda m:gmin(m,True)),('CH',ch),('CH_PAD',lambda a:ch(a,True))]:
        for m in range(2,6): print(name,fn(m))
