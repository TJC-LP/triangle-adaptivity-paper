# Editor's exact checks for revision 4 (python3 -I). Builds the live gadget from the
# paper's description, the rotated-star two-norm example, and the 4-cycle sharpness family.
from fractions import Fraction as F
from itertools import count
import sys

def stats(R, S, T):
    from collections import Counter
    dRp=Counter(x for x,y in R); dRm=Counter(y for x,y in R)
    dSp=Counter(y for y,z in S); dSm=Counter(z for y,z in S)
    dTp=Counter(z for z,x in T); dTm=Counter(x for z,x in T)
    Rout={}; Tin={}; Sout={}; Sin={}
    for x,y in R: Rout.setdefault(x,[]).append(y)
    for z,x in T: Tin.setdefault(x,[]).append(z)
    for y,z in S: Sout.setdefault(y,set()).add(z); Sin.setdefault(z,set()).add(y)
    Rin={}; Tout={}
    for x,y in R: Rin.setdefault(y,[]).append(x)
    for z,x in T: Tout.setdefault(z,[]).append(x)
    Rset=set(R); Tset=set(T)
    # costs
    def Cx():
        tot=0
        for x in set(dRp)|set(dTm):
            cR=sum(1+min(dSp[y],dTm[x]) for y in Rout.get(x,[]))
            cT=sum(1+min(dRp[x],dSm[z]) for z in Tin.get(x,[]))
            tot+=min(cR,cT)
        return tot
    def Cy():
        tot=0
        for y in set(dRm)|set(dSp):
            cR=sum(1+min(dSp[y],dTm[x]) for x in Rin.get(y,[]))
            cS=sum(1+min(dRm[y],dTp[z]) for z in Sout.get(y,[]))
            tot+=min(cR,cS)
        return tot
    def Cz():
        tot=0
        for z in set(dSm)|set(dTp):
            cS=sum(1+min(dRm[y],dTp[z]) for y in Sin.get(z,[]))
            cT=sum(1+min(dRp[x],dSm[z]) for x in Tout.get(z,[]))
            tot+=min(cS,cT)
        return tot
    out=0; supported=set()
    for x,y in R:
        for z in Sout.get(y,()):
            if (z,x) in Tset: out+=1
    # full reduction: every tuple in a triangle
    fr = all(any((z,x) in Tset for z in Sout.get(y,())) for x,y in R) and \
         all(any((x,y) in Rset for x in Tout.get(z,())) for y,z in S) and \
         all(any(z in Sout.get(y,()) for y in Rout.get(x,[])) for z,x in T)
    sq=lambda c: sum(v*v for v in c.values())
    fwd=(sq(dRp),sq(dSp),sq(dTp)); bwd=(sq(dRm),sq(dSm),sq(dTm))
    return dict(N=len(R)+len(S)+len(T), C=min(Cx(),Cy(),Cz()), Cs=(Cx(),Cy(),Cz()), Out=out,
                fwd=fwd, bwd=bwd, fr=fr)

def live(p,q,t,g,k,w, tag):
    assert p%t==0 and (p*t)%g==0 and g<=p and q%k==0
    z=p*t//g; assert z%q==0 and z%w==0
    X0=[(tag,'x',i) for i in range(p)]; Y0=[(tag,'y',i) for i in range(q)]
    Z1=[(tag,'z1',i) for i in range(t)]; Zw=[(tag,'zw',i) for i in range(t)]; Z2=[(tag,'z2',i) for i in range(z)]
    R=set(); S=set(); T=set()
    for x in X0:
        for y in Y0: R.add((x,y))
    for y in Y0:
        for zz in Z1+Zw: S.add((y,zz))
    for i,zz in enumerate(Z2): S.add((Y0[i%q],zz))          # one Y0 in-edge per z2, z/q per y0
    for i,zz in enumerate(Z2):
        for l in range(g): T.add((zz, X0[(i*g+l)%p]))       # out g, in t
    for i,zz in enumerate(Zw):
        for l in range(p//t): T.add((zz, X0[i*(p//t)+l]))    # out p/t, in 1
    for i,zz in enumerate(Z1): T.add((zz, X0[i]))           # matching into t distinct x
    for gi in range(z//w):
        W=Z2[gi*w:(gi+1)*w]; YW=[(tag,'yw',gi,i) for i in range(q)]
        for y in YW:
            for zz in W: S.add((y,zz))
        for m in range(q//k):
            h=(tag,'h',gi,m)
            for y in YW[m*k:(m+1)*k]: R.add((h,y))
            for zz in W: T.add((zz,h))
    return R,S,T

def rot_union(params3):
    R=set(); S=set(); T=set()
    for c,pr in enumerate(params3):
        r,s,t_=live(*pr, tag=c)
        # rotation c: local (R,S,T) placed as global rotated
        rels=[r,s,t_]
        R|=rels[(0-c)%3]; S|=rels[(1-c)%3]; T|=rels[(2-c)%3]
    return R,S,T

for v in (2,3):
    pr=(v**5,v**3,v**4,v**2,v**2,v)
    st=stats(*rot_union([pr,pr,pr]))
    B2c=min(st['fwd'][0]*st['fwd'][1]*st['fwd'][2], st['bwd'][0]*st['bwd'][1]*st['bwd'][2])
    fwdc=13*v**11+2*v**10+v**9+v**6+v**4
    Nc=3*(v**10+2*v**9+2*v**8+3*v**7+v**5+v**4)
    Cc=v**12+4*v**10+3*v**9+7*v**8+7*v**7+v**5+v**4
    print('L(v)',v,st['N'],st['C'],st['Cs'],st['Out'],st['fwd'],st['bwd'],st['fr'],
          'closed', st['N']==Nc, st['C']==Cc, st['fwd']==(fwdc,)*3, B2c==fwdc**3,
          'ratio', F(st['C'], st['N']+fwdc))
# general family (i,j,u)=(2,1,2)
i,j,u=2,1,2
pr=(u**(4*i),u**(4*i-2*j),u**(4*i-j),u**(4*i-3*j),u**j,1)
st=stats(*rot_union([pr,pr,pr]))
print('general (2,1,2)',st['N'],st['C'],st['Out'],st['fwd'],st['bwd'],st['fr'], st['C']>=u**(12*i-3*j))

# rotated star example for the two-norm comparator: T=K_{k,k}, R private out-stars, S private in-stars
for k in (2,3,4,8):
    X=[('x',i) for i in range(k)]; Z=[('z',i) for i in range(k)]
    T={(z,x) for z in Z for x in X}
    R={(x,('ry',x,a)) for x in X for a in range(k)}
    S={(('sy',z,a),z) for z in Z for a in range(k)}
    st=stats(R,S,T)
    from collections import Counter
    dRp=Counter(x for x,y in R); dSm=Counter(z for y,z in S)
    MT=sum(min(dRp[x],dSm[z]) for z,x in T)
    sR=F(k); sS=F(k); r=k*k
    # U2^2 terms
    U2sq=min(sR*r*r, sS*r*r, (r*sS)**2, (r*sR)**2)
    print('rotstar',k,'N',st['N'],'MT',MT,'U2^2',U2sq,'(k^5)',k**5,'Out',st['Out'])

# 4-cycle: 38 terms as (r-exps, s-exps) with rational exponents, labels 0..3 = R,S,T,Q
def terms38():
    L=range(4); opp=lambda i:(i+2)%4
    out=[]
    def add(rx, sx):
        key=(tuple(rx),tuple(sx))
        if key not in [ (tuple(a),tuple(b)) for a,b in out]: out.append((list(rx),list(sx)))
    Z=lambda: [F(0)]*4
    for i in L:                                   # A
        others=[j for j in L if j!=i]
        for a in range(3):
            for b in range(a+1,3):
                rx=Z(); sx=Z(); rx[i]=F(1); sx[others[a]]=F(1); sx[others[b]]=F(1); add(rx,sx)
        rx=Z(); sx=Z(); rx[i]=F(1)                # B
        for j in others: sx[j]=F(1,2)
        add(rx,sx)
    for i in L:
        for j in L:
            if j<=i: continue
            k,l=[m for m in L if m not in (i,j)]
            rx=Z(); sx=Z(); rx[i]=rx[j]=F(1,2); sx[k]=sx[l]=F(1,2); add(rx,sx)   # C, C'
            if j==opp(i):
                rx=Z(); sx=Z(); rx[i]=rx[j]=F(1); add(rx,sx)                      # D
                rx=Z(); sx=Z(); rx[i]=rx[j]=F(1,2); sx=[F(1,4)]*4; add(rx,sx)      # H
    for i in L:                                   # E: i,j,k consecutive
        j=(i+1)%4; k=(i+2)%4
        rx=Z(); sx=Z(); rx[i]=rx[k]=F(1,2); sx[i]=sx[j]=sx[k]=F(1,2); add(rx,sx)
    for i in L:                                   # F: (r_i r_j^2 s_i s_k s_l)^(1/3), j=opp(i)
        j=opp(i); k,l=[m for m in L if m not in (i,j)]
        rx=Z(); sx=Z(); rx[i]=F(1,3); rx[j]=F(2,3); sx[i]=sx[k]=sx[l]=F(1,3); add(rx,sx)
        # G: (r_j r_k r_l s_i s_k s_l)^(1/3): omit r_i and s_j
        rx=[F(1,3)]*4; rx[i]=F(0); sx=[F(1,3)]*4; sx[j]=F(0); add(rx,sx)
    return out
T38=terms38(); print('4-cycle terms', len(T38))
def U4pow12(r,s):
    best=None
    for rx,sx in T38:
        val=F(1)
        for e in range(4):
            for base,ex in ((r[e],rx[e]),(s[e],sx[e])):
                n=ex*12; assert n.denominator==1; val*=F(base)**int(n)
        best=val if best is None or val<best else best
    return best
for t in (F(1),F(3,2),F(7,4),F(31,16),F(255,128)):
    r=(8,t,8,8); s=(t,t,t,8)
    print('T4 t=',t,'U4==t^3:',U4pow12(r,s)==t**36)
for t,L in ((F(3,2),F(9,4)),(F(3,2),F(27,8)),(F(7,4),F(5))):
    val=U4pow12((L,t,L,L),(t,t,t,L)); print('env',t,L, val==min(t**36,(L*t**3)**6))
# adjacent-known variant r=(8,8,8,t), s=(t,t,8,t)
for t in (F(3,2),F(31,16)):
    print('adj',t,U4pow12((8,8,8,t),(t,t,8,t))==t**36)
# r3 obstruction instance r=(1,n,n,n), s=(1,n,1,n): U4 = n
for n in (2,3,5): print('obstr',n,U4pow12((1,n,n,n),(1,n,1,n))==F(n)**12)
# matching example: R,S,Q complete n x n, T perfect matching: Out=n^3; sizes (n^2,n^2,n,n^2), s=(n^2,n^2,1,n^2)
for n in (2,3,4): print('T5',n,U4pow12((n*n,n*n,n,n*n),(n*n,n*n,1,n*n))==F(n)**36)
