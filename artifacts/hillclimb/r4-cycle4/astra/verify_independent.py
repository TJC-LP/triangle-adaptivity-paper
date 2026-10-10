"""Independent exact checks. No solver code or nonstandard packages imported.
Run: python3 -I verify_independent.py
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd, prod
from functools import lru_cache
import random
import json

def transpose(a): return tuple(zip(*a))
def mm(a,b): return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)
def size(a): return sum(map(sum,a))
def out(a):
    p=mm(mm(a[0],a[1]),mm(a[2],a[3]))
    return sum(p[i][i] for i in range(len(p)))
def brute(a):
    return sum(a[0][x][y]*a[1][y][z]*a[2][z][w]*a[3][w][x]
               for x,y,z,w in product(*(range(len(m)) for m in a)))

@lru_cache(maxsize=20000)
def norm_bounds(a,steps=16):
    # A^T A has nonnegative entries: Rayleigh <= lambda <= Collatz.
    # Integer power vectors avoid any rounded arithmetic.
    if len(a)<len(a[0]): a=transpose(a)
    g=mm(transpose(a),a)
    if not size(a): return F(0),F(0)
    unseen={i for i in range(len(g)) if g[i][i]}
    bounds=[]
    while unseen:
        todo=[unseen.pop()]; comp=[]
        while todo:
            i=todo.pop();comp.append(i)
            neighbors={j for j in unseen if g[i][j]}
            unseen-=neighbors;todo.extend(neighbors)
        block=[[g[i][j] for j in comp] for i in comp]
        v=[1]*len(block)
        lo=F(max(g[i][i] for i in comp));hi=F(max(map(sum,block)))
        for _ in range(steps):
            w=[sum(x*y for x,y in zip(row,v)) for row in block]
            lo=max(lo,F(sum(x*y for x,y in zip(v,w)),sum(x*x for x in v)))
            hi=min(hi,max(F(wi,vi) for wi,vi in zip(w,v)))
            if lo==hi: break
            div=gcd(*w)
            v=[x//div for x in w]
        bounds.append((lo,hi))
    return max(x[0] for x in bounds),max(x[1] for x in bounds)

def monomials():
    terms=[]
    def add(name,den,r,s):
        a=[0]*4;b=[0]*4
        for i,p in r: a[i]+=p
        for i,p in s: b[i]+=p
        terms.append((name,den,tuple(a),tuple(b)))
    for i in range(4):
        other=[j for j in range(4) if j!=i]
        for j,k in combinations(other,2): add('A'+str((i,j,k)),1,[(i,1)],[(j,1),(k,1)])
        add('B'+str(i),2,[(i,2)],[(j,1) for j in other])
    for i,j in combinations(range(4),2):
        add('C'+str((i,j)),2,[(i,1),(j,1)],[(k,1) for k in range(4) if k not in (i,j)])
    for i in range(2): add('D'+str(i),1,[(i,1),(i+2,1)],[])
    for j in range(4):
        i,k=(j-1)%4,(j+1)%4
        add('E'+str(j),2,[(i,1),(k,1)],[(i,1),(j,1),(k,1)])
    for i in range(4):
        j=(i+2)%4
        add('F'+str(i),3,[(i,1),(j,2)],[(k,1) for k in range(4) if k!=j])
        add('G'+str(i),3,[(k,1) for k in range(4) if k!=i],[(k,1) for k in range(4) if k!=j])
    for i in range(2): add('H'+str(i),4,[(i,2),(i+2,2)],[(j,1) for j in range(4)])
    assert len(terms)==38 and len({(d,r,s) for _,d,r,s in terms})==38
    return terms

TERMS=monomials()
def power_value(term,r,s):
    _,d,a,b=term
    return prod(F(x)**p for x,p in zip(r,a))*prod(F(x)**p for x,p in zip(s,b))
def u12(r,s): return min(power_value(t,r,s)**(12//t[1]) for t in TERMS)

def certify(a,extra=False):
    o=out(a); r=tuple(map(size,a))
    assert o==brute(a)
    if not o: return {'output':0,'decided':True,'tight':False,'extra_checked':False}
    slo,shi=zip(*(norm_bounds(m) for m in a))
    for t in TERMS:
        if o**t[1]>power_value(t,r,slo):
            slo,shi=zip(*(norm_bounds(m,80) for m in a))
            break
    failures=[t[0] for t in TERMS if o**t[1]>power_value(t,r,shi)]
    undecided=[t[0] for t in TERMS if o**t[1]>power_value(t,r,slo)]
    assert not failures, (a,o,r,failures)
    assert not undecided,(a,o,r,undecided)
    result={'output':o,'decided':True,'tight':any(slo==shi and o**t[1]==power_value(t,r,slo) for t in TERMS),'extra_checked':extra}
    if extra:
        f=mm(mm(a[0],a[1]),a[2])
        f3=sum(x**3 for row in f for x in row)
        assert f3<=r[1]*prod(slo[:3]),('F2',a,f3)
        ss=[(y,z) for y,row in enumerate(a[1]) for z,v in enumerate(row) if v]
        qq=[(w,x) for w,row in enumerate(a[3]) for x,v in enumerate(row) if v]
        b=tuple(tuple(a[0][x][y]*a[2][z][w] for w,x in qq) for y,z in ss)
        blo,bhi=norm_bounds(b,32)
        if bhi*bhi>prod(slo):
            blo,bhi=norm_bounds(b,100)
        assert bhi*bhi<=prod(slo),('H3 unresolved',a,blo,bhi)
    return result

def random_matrix(rng,m,n,kind):
    if kind==0: return tuple(tuple(int(rng.randrange(7)<rng.randrange(1,7)) for j in range(n)) for i in range(m))
    if kind==1: return tuple(tuple(int(i==0 or j==0) for j in range(n)) for i in range(m))
    if kind==2: return tuple(tuple(int(i==j or rng.randrange(12)==0) for j in range(n)) for i in range(m))
    if kind==3:
        rr=[rng.randrange(3) for _ in range(m)];cc=[rng.randrange(3) for _ in range(n)]
        return tuple(tuple(int(rr[i]==cc[j]) for j in range(n)) for i in range(m))
    if kind==4: return tuple(tuple(int(j<=i) for j in range(n)) for i in range(m))
    if kind==5: return tuple(tuple(int(rng.randrange(8)>0) for j in range(n)) for i in range(m))
    return tuple(tuple(int((i+j)%2==0) for j in range(n)) for i in range(m))

def main():
    mats=[tuple(tuple((mask>>(i*2+j))&1 for j in range(2)) for i in range(2)) for mask in range(16)]
    groups={};total=positive=0
    for ids in product(range(16),repeat=4):
        a=tuple(mats[i] for i in ids);o=out(a)
        assert o==brute(a)
        key=tuple((size(m),norm_bounds(m)) for m in a)
        if key not in groups or o>groups[key][0]: groups[key]=(o,a)
        total+=1;positive+=o>0
    for o,a in groups.values(): certify(a)
    print(json.dumps({'exhaustive_2x2':total,'positive':positive,'statistics_groups':len(groups),'violations':0,'undecided':0}),flush=True)
    fcount=0
    for a,b,c in product(mats,repeat=3):
        m=mm(mm(a,b),c);lhs=sum(x**3 for row in m for x in row)
        rhs=size(b)*prod(norm_bounds(x)[0] for x in (a,b,c))
        assert lhs<=rhs
        fcount+=1
    print(json.dumps({'F2_exhaustive_triples':fcount,'violations':0}),flush=True)
    rng=random.Random(931407);positives=tight=extras=0
    for k in range(1800):
        dims=[rng.randrange(1,7) for _ in range(4)]
        a=tuple(random_matrix(rng,dims[i],dims[(i+1)%4],rng.randrange(7)) for i in range(4))
        v=certify(a,extra=(k<240))
        positives+=v['output']>0;tight+=v['tight'];extras+=v['extra_checked']
    print(json.dumps({'random_adversarial':1800,'positive':positives,'tight':tight,'F2_H3_additional_checked':extras,'violations':0,'undecided':0}),flush=True)
    arcs=[frozenset((i+j)%4 for j in range(k)) for k in range(1,4) for i in range(4)]+[frozenset(range(4))]
    positives=tight=0
    for sample in range(320):
        chosen=rng.sample(arcs,rng.randrange(1,4))
        ids=[[j for j,a in enumerate(chosen) if i in a] for i in range(4)]
        vertices=[list(product([0,1],repeat=len(js))) for js in ids]
        mats=[]
        for i in range(4):
            j=(i+1)%4
            common=[(ids[i].index(k),ids[j].index(k)) for k in ids[i] if k in ids[j]]
            mats.append([[int(all(u[x]==v[y] for x,y in common)) for v in vertices[j]] for u in vertices[i]])
        for _ in range(rng.randrange(1,5)):
            e=rng.randrange(4);i=rng.randrange(len(mats[e]));j=rng.randrange(len(mats[e][0]))
            mats[e][i][j]^=1
        a=tuple(tuple(tuple(row) for row in mat) for mat in mats)
        v=certify(a);positives+=v['output']>0;tight+=v['tight']
    print(json.dumps({'arc_plus_flips':320,'positive':positives,'tight':tight,'violations':0,'undecided':0}),flush=True)
    dims=[2,1,7,2]
    a=tuple(tuple(tuple(1 for _ in range(dims[(i+1)%4])) for _ in range(dims[i])) for i in range(4))
    r=list(map(size,a));s=[norm_bounds(m)[0] for m in a];o=out(a)
    assert certify(a)['tight'] and o==28 and u12(r,s)==28**12
    print(json.dumps({'misnamed_tight_example':{'dimensions':dims,'r':r,'s':list(map(str,s)),
        'Out':o,'U12':str(u12(r,s)),'r_Q_s_R_s_T':str(r[3]*s[0]*s[2]),
        'r_R_r_T':r[0]*r[2],'r_S_r_Q':r[1]*r[3]}}),flush=True)
    # Every relation is a double star. Delta+Delta- incorrectly substitutes for norm².
    for n in [2,3,5,8]:
        a=tuple(tuple(int(i==0 or j==0) for j in range(n)) for i in range(n))
        lo,hi=norm_bounds(a,12)
        assert hi<n*n
        print(json.dumps({'double_star_n':n,'degree_product':n*n,'sigma2_lower':str(lo),'sigma2_upper':str(hi)}),flush=True)

if __name__=='__main__': main()
