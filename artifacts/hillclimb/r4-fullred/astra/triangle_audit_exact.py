from fractions import Fraction as F
from itertools import product, combinations, permutations
from collections import Counter,defaultdict
from math import isqrt,prod
import random,json

def stats(E):
    ds=[]
    for e in E: ds.append((Counter(a for a,b in e),Counter(b for a,b in e)))
    sz=list(map(len,E)); m=[]; weights=[]
    for i,e in enumerate(E):
        ww={(a,b):1+min(ds[(i+1)%3][0][b],ds[(i+2)%3][1][a]) for a,b in e}
        weights.append(ww); m.append(sum(ww.values())-len(e))
    cs=[]
    for i in range(3):
        left=defaultdict(int); right=defaultdict(int)
        for (a,b),v in weights[i].items():left[a]+=v
        for (a,b),v in weights[(i+2)%3].items():right[b]+=v
        cs.append(sum(min(left[k],right[k]) for k in left.keys()|right.keys()))
    sy=defaultdict(set);tx=defaultdict(set)
    for y,z in E[1]:sy[y].add(z)
    for z,x in E[2]:tx[x].add(z)
    out=sum(len(sy[y]&tx[x]) for x,y in E[0])
    f=[sum(x*x for x in d[0].values()) for d in ds]; b=[sum(x*x for x in d[1].values()) for d in ds]
    return dict(N=sum(sz),r=sz,M=m,Cs=cs,C=min(cs),out=out,f=f,b=b,Q=min(prod(f),prod(b)))

def u9(r,s):
    v=[s[i]*r[(i+1)%3]*r[(i+2)%3] for i in range(3)]
    return v+[(r[i]*s[j])**2 for i in range(3) for j in range(3) if i!=j]
def u2(r,p,q):
    a,b,c=r
    return [p*b*c,q*a*c,(a*q)**2,(b*p)**2,(c*p)**2,(c*q)**2]
def psd(A):
    B=[list(map(F,row)) for row in A]
    for k in range(len(B)):
        if B[k][k]<0:return False
        if not B[k][k]:
            if any(B[k][j] for j in range(k+1,len(B))):return False
            continue
        for i in range(k+1,len(B)):
            for j in range(i,len(B)):
                B[j][i]=B[i][j]=B[i][j]-B[k][i]*B[k][j]/B[k][k]
    return True

def normcap(E,d,s):
    G=[[sum((k,i) in E and (k,j) in E for k in range(d)) for j in range(d)] for i in range(d)]
    return psd([[s*(i==j)-G[i][j] for j in range(d)] for i in range(d)])
def spectral_integer_cap(E,d):
    return next(s for s in range(len(E)+1) if normcap(E,d,F(s)))
def rotation(E):return [E[2],E[0],E[1]]
def reflect(E):return [{(b,a) for a,b in E[2]},{(b,a) for a,b in E[1]},{(b,a) for a,b in E[0]}]
def inequalities(E):
    d=stats(E); r=d['r']; a=d['f']; b=d['b']; Q=d['Q']; C=d['C']; N=d['N']; m=d['M']; out=d['out']
    assert out**3<=Q
    assert max(0,C-N)**8<=prod(r)*Q**2
    assert N**3*max(0,C-N)**24<=27*Q**10
    assert min(m)**5<=prod(r)*Q
    for i in range(3):
        j=(i+1)%3;k=(i+2)%3
        assert m[i]**4<=r[i]*r[k]**2*a[i]*a[j]
        assert m[i]**4<=r[i]*r[j]**2*b[i]*b[k]
    # F/B/B2 chains in the specified ordering; iterate all label symmetries.
    for E0 in (E,reflect(E)):
      for rr in range(3):
        dd=stats(E0); R,S,T=dd['r']; al,be,ga=dd['f']; ap,bp,gp=dd['b']; cc=dd['C'];nn=dd['N'];MT=dd['M'][2]
        if R>=S>=T:
            lf=al*be*ga;lb=ap*bp*gp
            assert nn*max(cc-T,0)**4<=3*lf**2
            assert nn*max(cc-S,0)**4<=3*lb**2
            assert nn*max(cc-T,0)**2<=3*T*lb
        E0=rotation(E0)
    return d

def block(a,b,c,m):
    E=[set(),set(),set()]
    for k in range(m):
      V=[[(k,i) for i in range(z)] for z in (a,b,c)]
      for j in range(3):E[j].update(product(V[j],V[(j+1)%3]))
    return E

def floor_sqrt(Fv):return isqrt(Fv.numerator//Fv.denominator)
def witness(r,p,q):
    v=min(u2(r,p,q))
    a,b,c=[max(1,floor_sqrt(v/F(x*x))) for x in (r[1],r[2],r[0])]
    m=min(r[0]//(a*b),r[1]//(b*c),r[2]//(c*a))
    assert a*b<=p and b*c<=q and c*a<=r[2]
    O=m*a*b*c
    assert 16*O*O>v and O*O<=v
    return (a,b,c,m),O,v

def dead(p,q,t,g,tag):
    assert p*t%g==0 and g<=p
    X=[(tag,'x',i) for i in range(p)];Y=[(tag,'y',i) for i in range(q)]
    Z=[(tag,'z',i) for i in range(t)];Z2=[(tag,'zz',i) for i in range(p*t//g)]
    R=set(product(X,Y));S=set(product(Y,Z));T=set()
    for j,z in enumerate(Z2):
      for h in range(q):S.add(((tag,'yy',j*q+h),z))
      for h in range(g):T.add((z,X[(j*g+h)%p]))
    return [R,S,T]
def deadformula(p,q,t,g):
    return dict(r=[p*q,q*t+p*q*t//g,p*t],Cs=[p*q*t+p*min(q,t),q*t,p*q*t//g],f=[p*q*q,q*t*t+p*q*t//g,p*t*g],b=[q*p*p,t*q*q+p*t*q*q//g,p*t*t],out=0)
def union(gs):
    E=[set(),set(),set()]
    for k,g in enumerate(gs):
      for i,e in enumerate(g):E[(i+k)%3].update(e)
    return E

def main():
    masks=[]
    for mask in range(16):masks.append({(i,j) for i in range(2) for j in range(2) if mask&(1<<(2*i+j))})
    caps={i:[F(k,4) for k in range(4,17) if normcap(e,2,F(k,4))] for i,e in enumerate(masks)}
    checked=0;budget=0
    for ii in product(range(16),repeat=3):
      E=[masks[i] for i in ii]; d=inequalities(E);checked+=1
      if all(d['r']):
       for p,q in product(caps[ii[0]],caps[ii[1]]):
        rr=d['r'];v=u2(rr,min(p,rr[0]),min(q,rr[1]));budget+=1
        assert d['out']**2<=min(v)
        assert d['M'][0]**2<=min(v[j] for j in (0,2,3,4))
        assert d['M'][1]**2<=min(v[j] for j in (1,2,3,5))
    print('EXHAUSTIVE_2x2',checked,'admissible_fraction_budgets',budget,'violations',0)
    rng=random.Random(1791586191); count=0;maxes=[F(0),F(0),F(0)]
    for case in range(12000):
      D=[rng.randrange(1,8) for _ in range(3)]; probs=[F(rng.randrange(1,10),10) for _ in range(3)]
      E=[]
      for i in range(3):
        if case%4==0:
          e={(a,b) for a in range(D[i]) for b in range(D[(i+1)%3]) if a==0 or (b==0 and rng.randrange(2))}
        else:e={(a,b) for a in range(D[i]) for b in range(D[(i+1)%3]) if rng.randrange(10)<probs[i]*10}
        E.append(e)
      d=inequalities(E);count+=1
      if all(d['r']):
        # all rational cap checks with actual matrix Gram certificate, size bounds actual.
        p=spectral_integer_cap(E[0],max(D));q=spectral_integer_cap(E[1],max(D));v=u2(d['r'],p,q)
        assert d['out']**2<=min(v)
        assert d['M'][0]**2<=min(v[j] for j in (0,2,3,4))
        assert d['M'][1]**2<=min(v[j] for j in (1,2,3,5))
        if d['Q']:
          maxes[0]=max(maxes[0],F(min(d['M'])**5,prod(d['r'])*d['Q']))
          maxes[1]=max(maxes[1],F(max(d['C']-d['N'],0)**8,prod(d['r'])*d['Q']**2))
    print('RANDOM_AND_STAR_ADVERSARIES',count,'violations',0,'max_best6_ratio',maxes[0],'max_perbinding_ratio',maxes[1])
    ngrid=0; worst=(F(0),None)
    for r in product(range(1,9),repeat=3):
      for p,q in product(range(1,r[0]+1),range(1,r[1]+1)):
        assert min(u2(r,p,q))==min(u9(r,[p,q,r[2]]))
        w,o,v=witness(r,p,q);ngrid+=1
        if F(v,o*o)>worst[0]:worst=(F(v,o*o),(r,p,q,w,o))
    print('COLLAPSE_AND_ROUNDING_GRID',ngrid,'violations',0,'worst_squared_U_over_Out',worst)
    six=[((4,4,4),(2,4),(1,1,1,2)),((4,4,4),(4,2),(1,1,1,2)),((2,6,6),(2,2),(0,0,2,2)),((6,2,6),(2,2),(2,0,0,2)),((6,6,2),(2,4),(0,2,0,2)),((6,6,2),(4,2),(0,2,0,2))]
    for n in (2,3,5):
      oo=[]
      for ix,(rr,ss,bl) in enumerate(six):
        r=[n**x for x in rr];p,q=[n**x for x in ss];shape=[n**x for x in bl];d=stats(block(*shape));v=u2(r,p,q)
        assert d['out']**2==v[ix]<min(v[j] for j in range(6) if j!=ix)
        assert F(min(v[j] for j in range(6) if j!=ix),v[ix])==n*n
        oo.append(d['out'])
      print('SIX_IRREDUNDANCY',n,oo,'deletion_squared_ratio',n*n)
    p,q=7,5
    for _ in range(4):
      assert p*p-2*q*q==-1;t=F(p*p,q*q);v=min(u2([t*t,t,t*t],t,1))
      assert v==t**4
      print('PELL',p,q,'t',t,'U_over_W',t*t,'W',1)
      p,q=3*p+4*q,2*p+3*q
    for k in (2,3,5,8):
      M={(i,i) for i in range(k)};E=[M,M,set(product(range(k),repeat=2))];d=stats(E)
      print('UNMEASURED_DRIVER',k,d)
    nn=0
    for p,q,t,g in product(range(1,6),repeat=4):
      if g>p or p*t%g:continue
      d=stats(dead(p,q,t,g,0));f=deadformula(p,q,t,g)
      for key in f:assert d[key]==f[key],(p,q,t,g,key,d,f)
      nn+=1
    print('DEAD_GADGET_FORMULAS',nn,'all_13_scalar_formulas_verified')
    for u in (2,3,4):
      E=union([dead(u**4,u**2,u**3,u,j) for j in range(3)])
      for tt in (8,9,10):
        M=u**tt;Ep=[set(e) for e in E];Ep[1].update(((('pad','y',j),('pad','z',j)) for j in range(M)))
        d=stats(Ep)
        assert d['N']==3*(u**8+u**7+u**6+u**5)+M
        assert d['C']==u**9+u**8+u**6+u**5
        assert d['f']==[4*u**8,4*u**8+M,4*u**8]
        print('PADDED',u,tt,d)
    for m in (2,3,4,5):
      # Three rotated E(L,a,h) components; this defines GMIN independently.
      gs=[]
      for tag in range(3):
        L,a,h=m**3,m,m*m;X=[(tag,'x',i) for i in range(L)];Y=[(tag,'y',i) for i in range(a)];Z=[(tag,'z',i) for i in range(h)]
        gs.append([set(product(X,Y)),set(product(Y,Z)),{((tag,'zz',i,j),X[i]) for i in range(L) for j in range(h)}])
      d=stats(union(gs));assert d['M']==[m**6]*3 and d['C']==m**5+m**3 and d['f']==[3*m**5]*3
      ratio5=F(prod(d['r'])*d['Q'],min(d['M'])**5)
      print('GMIN',m,d,'upper_to_actual_power5',ratio5)
if __name__=='__main__':main()
