from collections import Counter,defaultdict
from fractions import Fraction
from random import Random

def D(X,a,t):
    assert X>=t>=1 and a>=1 and X%t==0
    R={(x,y) for x in range(X) for y in range(a)}
    S={(y,('a',z)) for y in range(a) for z in range(t)}
    S.update({(a+j*a+k,('b',j)) for j in range(t*t) for k in range(a)})
    T={(('b',i*t+j),i*(X//t)+k) for i in range(t) for j in range(t) for k in range(X//t)}
    return R,S,T

def evaluate(rel):
    R,S,T=rel
    rp=Counter(x for x,y in R);rm=Counter(y for x,y in R)
    sp=Counter(y for y,z in S);sm=Counter(z for y,z in S)
    tp=Counter(z for z,x in T);tm=Counter(x for z,x in T)
    fw=tuple(sum(d*d for d in c.values()) for c in (rp,sp,tp))
    rv=tuple(sum(d*d for d in c.values()) for c in (rm,sm,tm))
    costs=[defaultdict(lambda:[0,0]) for _ in range(3)]
    Ms=[0,0,0]
    for x,y in R:
        v=min(sp[y],tm[x]);Ms[0]+=v;costs[0][x][0]+=1+v;costs[1][y][0]+=1+v
    for y,z in S:
        v=min(tp[z],rm[y]);Ms[1]+=v;costs[1][y][1]+=1+v;costs[2][z][0]+=1+v
    for z,x in T:
        v=min(rp[x],sm[z]);Ms[2]+=v;costs[2][z][1]+=1+v;costs[0][x][1]+=1+v
    Cs=tuple(sum(min(v) for v in c.values()) for c in costs)
    sy=defaultdict(set);tx=defaultdict(set)
    for y,z in S:sy[y].add(z)
    for z,x in T:tx[x].add(z)
    out=sum(len(sy[y]&tx[x]) for x,y in R)
    return tuple(map(len,rel)),fw,rv,tuple(Ms),Cs,out

def closed_D(X,a,t):
    return ((X*a,a*t+a*t*t,X*t),(X*a*a,2*a*t*t,X*X),
            (a*X*X,a*a*(t+t*t),X*t*t),(X*a*t,0,X*a*t),
            (X*a*t+X*min(a,t),a*t,a*t*t),0)

def union_rotated(gadgets):
    rel=[set(),set(),set()]
    for k,g in enumerate(gadgets):
        for j,edges in enumerate(g):
            rel[(j+k)%3].update({((k,j,x),(k,(j+1)%3,y)) for x,y in edges})
    return tuple(rel)

def compressed(u,p,q):
    assert u>=2 and p<=q and 10*p>=9*q
    params=[(u**(8*p-4*q),u**(6*q-4*p),u**(6*p-3*q)),
            (u**(4*q),u**(4*p-2*q),u**(6*p-3*q)),
            (u**(4*p),u**(6*p-4*q),u**(6*q-3*p))]
    pieces=[closed_D(*z) for z in params]
    sums=[[0]*3 for _ in range(5)]
    for k,piece in enumerate(pieces):
        for kind in range(5):
            for j,val in enumerate(piece[kind]):sums[kind][(j+k)%3]+=val
    sizes,fw,rv,Ms,Cs=map(tuple,sums)
    assert fw==(4*u**(8*q),4*u**(8*p),4*u**(16*p-8*q))
    assert rv==(2*u**(12*p-2*q)+u**(9*p-2*q)+u**(6*p+4*q),
                u**(9*q-2*p)+2*u**(4*p+6*q)+u**(12*q-2*p),
                2*u**(20*p-10*q)+u**(14*p-7*q)+u**(14*p-4*q))
    assert Cs==(u**(10*p-q)+u**(4*p+2*q)+u**(16*p-8*q)+u**(3*p+2*q),
                u**(10*p-q)+u**(4*p+2*q)+u**(8*q)+u**(2*p+3*q),
                u**(7*p+2*q)+u**(10*p-4*q)+u**(8*p)+u**(10*p-5*q))
    assert Cs[0]==min(Cs)
    assert all(a<=b for a,b in zip(fw,rv))
    N=sum(sizes);C=min(Cs);B=4*u**(8*p)
    assert B**3==min(fw[0]*fw[1]*fw[2],rv[0]*rv[1]*rv[2])
    N_expr=(2*u**(4*p+2*q)+u**(2*p+3*q)+u**(8*p)+u**(14*p-7*q)
            +u**(10*p-5*q)+u**(16*p-8*q)+u**(6*p+q)+u**(10*p-4*q)
            +u**(3*p+2*q)+u**(8*q)+u**(p+6*q))
    assert N==N_expr
    assert C>=u**(10*p-q) and C<=4*u**(10*p-q)
    assert u**(8*q)<=N<=12*u**(8*q)
    return params,(sizes,fw,rv,Ms,Cs,0),(N,B,C)

print('GENERIC: (X,a,t) sizes forward reverse M C Out')
cases=[(1,1,1),(2,1,2),(4,2,2),(6,3,2),(8,3,4),(12,5,3),(12,2,6)]
for z in cases:
    val=evaluate(D(*z));assert val==closed_D(*z)
    print(z,*val)
rng=Random(1739)
for _ in range(100):
    t=rng.randrange(1,7);z=(t*rng.randrange(1,8),rng.randrange(1,8),t)
    assert evaluate(D(*z))==closed_D(*z)
print('100 additional deterministic generic checks passed.')
print('MATERIALIZED SLOPE p=q=1: u sizes fw rv M Cvec Out N B C')
for u in (2,3,4):
    pars,val,summ=compressed(u,1,1)
    actual=evaluate(union_rotated([D(*z) for z in pars]))
    assert actual==val
    print(u,*actual,*summ)
print('COMPRESSED SLOPES: u p q N B C ratio C/(N+B) bit_lengths(N,B,C)')
for p,q in ((9,10),(10,11),(19,20)):
    pars,val,(N,B,C)=compressed(2,p,q)
    print(2,p,q,N,B,C,Fraction(C,N+B),(N.bit_length(),B.bit_length(),C.bit_length()))
print('All exact slope checks passed.')
