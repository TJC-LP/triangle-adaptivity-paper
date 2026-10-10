"""Independent exact four-cycle auditor. No solver code is imported or executed."""
from fractions import Fraction as F
from itertools import combinations, product
from math import prod, gcd, isqrt
from functools import lru_cache
from random import Random
import json, sys

EDGES=[{i,(i+1)%4} for i in range(4)]
ARCS=[{(i+j)%4 for j in range(n)} for n in (1,2,3) for i in range(4)]+[set(range(4))]
ROWS=[tuple(int(bool(a&e)) for e in EDGES)+tuple(int(len(a&e)==1) for e in EDGES) for a in ARCS]

def listed_terms():
    terms={}
    def put(name,d):
        t=tuple(d.get(i,F(0)) for i in range(8)); terms[t]=name
    for i in range(4):
        other=[j for j in range(4) if j!=i]
        for j,k in combinations(other,2): put('A',{i:F(1),j+4:F(1),k+4:F(1)})
        put('B',{i:F(1),**{j+4:F(1,2) for j in other}})
    for i,j in combinations(range(4),2):
        put('C' if (i-j)%2==0 else "Cprime",{i:F(1,2),j:F(1,2),**{k+4:F(1,2) for k in range(4) if k not in (i,j)}})
        if (i-j)%2==0:
            put('D',{i:F(1),j:F(1)})
            put('H',{i:F(1,2),j:F(1,2),**{k+4:F(1,4) for k in range(4)}})
    for i in range(4):
        j,k,l=(i+1)%4,(i+2)%4,(i+3)%4
        put('E',{i:F(1,2),k:F(1,2),i+4:F(1,2),j+4:F(1,2),k+4:F(1,2)})
        put('F',{i:F(1,3),k:F(2,3),**{h+4:F(1,3) for h in range(4) if h!=k}})
        put('G',{**{h:F(1,3) for h in range(4) if h!=i},**{h+4:F(1,3) for h in range(4) if h!=k}})
    assert len(terms)==38
    return terms
TERMS=listed_terms()
POWERS={t:tuple(int(12*x) for x in t) for t in TERMS}

def bareiss_solve(rows):
    n=len(rows); a=[list(row)+[1] for row in rows]; prev=1
    for k in range(n-1):
        p=next((j for j in range(k,n) if a[j][k]),None)
        if p is None:return None
        a[p],a[k]=a[k],a[p]; pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n+1):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator%prev==0
                a[i][j]=numerator//prev
            a[i][k]=0
        prev=pivot
    if not a[-1][n-1]:return None
    x=[F(0)]*n
    for i in range(n-1,-1,-1):x[i]=F(a[i][n]-sum(a[i][j]*x[j] for j in range(i+1,n)))/a[i][i]
    return x

def vertices(rows):
    out=set(); count=0
    # Every vertex has a positive support; active nonnegativity eliminates other coordinates.
    for size in range(1,9):
        for support in combinations(range(8),size):
            restrict=[tuple(row[i] for i in support) for row in rows]
            for act in combinations(range(len(rows)),size):
                count+=1; sol=bareiss_solve([restrict[j] for j in act])
                if sol is None or min(sol)<=0:continue
                if any(sum(a*b for a,b in zip(row,sol))<1 for row in restrict):continue
                v=[F(0)]*8
                for i,x in zip(support,sol):v[i]=x
                out.add(tuple(v))
    return out,count

def verify_dual():
    vfull,nfull=vertices(ROWS); vred,nred=vertices(ROWS[:8]+ROWS[12:])
    assert vfull==vred
    redundant={v:next((u for u in vfull if u!=v and all(v[i]>=u[i] and v[i]+v[i+4]>=u[i]+u[i+4] for i in range(4))),None) for v in vfull}
    needed={v for v in vfull if redundant[v] is None}
    assert needed==set(TERMS)
    vint={v:tuple(int(12*x) for x in v) for v in vfull}; witness={}; rng=Random(765121)
    for k in range(200000):
        # Independent integer cost search, not imported rational certificates.
        s=[rng.randrange(0,10) for _ in range(4)]; r=[a+rng.randrange(0,10) for a in s]; cost=r+s
        score={v:sum(a*b for a,b in zip(t,cost)) for v,t in vint.items()}; best=min(score.values()); win=[v for v,z in score.items() if z==best]
        if len(win)==1 and win[0] not in witness:witness[win[0]]=cost
        if len(witness)==38:break
    assert len(witness)==38,(len(witness),set(TERMS)-set(witness))
    print('DUAL',len(vfull),len(vred),'bases',nfull,nred,'needed',len(needed),'redundant',len(vfull-needed),'strict_witness_samples',k+1,flush=True)
    data={','.join(map(str,v)):w for v,w in witness.items()}
    with open('fourcycle_dual_certificates.json','w') as f:json.dump(data,f,indent=2)
    return vfull

# Q(sqrt(5)) with exact rational coordinates.
def mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def powq(a,n):
    out=(F(1),F(0))
    while n:
        if n&1:out=mul(out,a)
        a=mul(a,a);n//=2
    return out

def nonnegative(a):
    x,y=a
    if x>=0 and y>=0:return True
    if x<0 and y<0:return False
    return x*x>=5*y*y if x>=0 else 5*y*y>=x*x

def matrix(mask,rows=2,cols=2):return [[(mask>>(i*cols+j))&1 for j in range(cols)] for i in range(rows)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def cycle_count(ms):
    a=ms[0]
    for b in ms[1:]:a=mm(a,b)
    return sum(a[i][i] for i in range(len(a)))
def spectrum22(a):
    n=sum(map(sum,a)); det=a[0][0]*a[1][1]-a[0][1]*a[1][0]; d=n*n-4*det*det
    if isqrt(d)**2==d:return (F(n+isqrt(d),2),F(0))
    assert d==5
    return(F(n,2),F(1,2))

@lru_cache(None)
def minimum22(stats):
    values=[]
    for powers in POWERS.values():
        val=(F(1),F(0))
        for i,(r,s) in enumerate(stats):val=mul(val,mul((F(r**powers[i]),F(0)),powq(s,powers[i+4])))
        values.append(val)
    m=values[0]
    for v in values[1:]:
        if nonnegative((m[0]-v[0],m[1]-v[1])):m=v
    return m

def exhaustive22():
    mats=[matrix(i) for i in range(16)]; stats=[(sum(map(sum,a)),spectrum22(a)) for a in mats]
    total=positive=tight=0; maxout=0
    for ids in product(range(16),repeat=4):
        total+=1; out=cycle_count([mats[i] for i in ids]); maxout=max(maxout,out)
        if not out:continue
        positive+=1; b=minimum22(tuple(stats[i] for i in ids)); delta=(b[0]-out**12,b[1])
        assert nonnegative(delta),(ids,out,b)
        tight+=delta==(0,0)
    print('EXHAUSTIVE_2x2',total,'positive',positive,'tight',tight,'maximum_output',maxout,'distinct_statistics',minimum22.cache_info(),flush=True)

def gram(a):return mm([list(z) for z in zip(*a)],a)
def lowernorm2(a,steps=20):
    g=gram(a); x=[1]*len(g)
    for _ in range(steps):
        y=[sum(t*v for t,v in zip(row,x)) for row in g]
        if not any(y):return F(0)
        z=0
        for v in y:z=gcd(z,v)
        x=[v//z for v in y]
    y=[sum(t*v for t,v in zip(row,x)) for row in g]
    return F(sum(a*b for a,b in zip(x,y)),sum(v*v for v in x))

def val12(r,s,p):return prod(F(x)**n for x,n in zip(r+s,p))
def u12(r,s):return min(val12(r,s,p) for p in POWERS.values())
def random_checks():
    rng=Random(709); tested=positive=undecided=0; equal=0
    for k in range(1200):
        dims=[rng.randrange(1,7) for _ in range(4)]; threshold=rng.randrange(1,10)
        mats=[[[int(rng.randrange(10)<threshold) for j in range(dims[(i+1)%4])] for z in range(dims[i])] for i in range(4)]
        # Adversarial modes: unions, nearly dense, diagonals, degree imbalance.
        if k%4==0:
            mats[2]=[[int(i==j) for j in range(dims[3])] for i in range(dims[2])]
        if k%4==1:
            mats[0]=[[int(i==0 or j==0) for j in range(dims[1])] for i in range(dims[0])]
        out=cycle_count(mats); tested+=1
        if not out:continue
        positive+=1;r=[sum(map(sum,m)) for m in mats];s=[lowernorm2(m) for m in mats]; bound=u12(r,s)
        if bound<out**12:
            s=[lowernorm2(m,120) for m in mats];bound=u12(r,s)
        if bound<out**12:undecided+=1;print('UNDECIDED',dims,r,out)
        equal+=bound==out**12
        # F2 is stronger than the F counting bound and can be checked separately.
        path=mm(mm(mats[0],mats[1]),mats[2]); cubes=sum(v**3 for row in path for v in row)
        assert cubes<=r[1]*s[0]*s[1]*s[2],('F2',k)
    print('RANDOM_ADVERSARIAL',tested,'positive',positive,'undecided',undecided,'tight',equal,flush=True)

def arc_stats(ns):
    return tuple(prod(n for n,row in zip(ns,ROWS) if row[i]) for i in range(8))
def arc_matrices(ns):
    coordinates=[[i for i,a in enumerate(ARCS) if v in a] for v in range(4)]
    domains=[list(product(*(range(ns[i]) for i in ids))) for ids in coordinates]
    mats=[]
    for e in range(4):
        f=(e+1)%4; shared=set(coordinates[e])&set(coordinates[f]); indices=[(coordinates[e].index(i),coordinates[f].index(i)) for i in shared]
        mats.append([[int(all(x[i]==y[j] for i,j in indices)) for y in domains[f]] for x in domains[e]])
    return mats

def arc_tests():
    # Supporting each term only on tight arcs gives equality by direct integer products.
    rebuilt=0; outs=[]
    for term in TERMS:
        ns=[2 if sum(a*b for a,b in zip(row,term))==1 else 1 for row in ROWS]
        st=arc_stats(ns); out=prod(ns);assert val12(st[:4],st[4:],POWERS[term])==out**12
        # Reduce matrix dimensions while retaining a literal witness for every term.
        eligible=[i for i,n in enumerate(ns) if n==2]
        ns=[2 if i in eligible[:3] else 1 for i in range(13)]
        mats=arc_matrices(ns);st=arc_stats(ns);out=cycle_count(mats)
        assert out==prod(ns)
        assert tuple(sum(map(sum,m)) for m in mats)==st[:4]
        # Arc matrices are biregular on each nontrivial connected component; Rayleigh exact.
        assert tuple(lowernorm2(m,3) for m in mats)==st[4:]
        assert val12(st[:4],st[4:],POWERS[term])==out**12
        rebuilt+=1;outs.append(out)
    print('ARCS_TERMS_REBUILT',rebuilt,'output_counts',dict((o,outs.count(o)) for o in sorted(set(outs))),flush=True)
    # Explicit obstruction examples.
    for n in (2,3,5,7):
        allones=[[1]*n for _ in range(n)];ident=[[int(i==j) for j in range(n)] for i in range(n)]
        mats=[allones,allones,ident,allones];r=[n*n,n*n,n,n*n];s=[n*n,n*n,1,n*n]
        assert u12(r,s)==n**36
        print('BLOCK_OBSTRUCTION',n,'Out',cycle_count(mats),'block_max',n*n,'U12',u12(r,s),flush=True)
        assert u12([1,n,n,n],[1,n,1,n])==n**12
    for t in (F(3,2),F(7,4),F(15,8),F(31,16),F(63,32)):
        L=1
        while u12([L,t,L,L],[t,t,t,L])!=t**36:L+=1
        print('CONSTANT8',str(t),'smallest_integer_L',L,'U12',str(t**36),'W',1,'W_over_U',str(1/t**3),flush=True)
    # All values rational: exact rounding check on feasible real arc optima identified by tightness.
    rng=Random(8903); worst=F(1); cnt=0
    for term in TERMS:
        for _ in range(40):
            ns=[F(rng.randrange(16,130),16) if sum(a*b for a,b in zip(row,term))==1 else F(1) for row in ROWS]
            st=arc_stats(ns); target=prod(ns);assert u12(st[:4],st[4:])==target**12
            rounded=[F(n.numerator//n.denominator) for n in ns];rounded[-1]=F(1)
            part=arc_stats(rounded);mstar=min(st[i]/part[i] for i in range(4));rounded[-1]=F(mstar.numerator//mstar.denominator)
            final=arc_stats(rounded);integerout=prod(rounded)
            assert all(a<=b for a,b in zip(final,st));assert 16*integerout>target
            worst=max(worst,target/integerout);cnt+=1
    print('RATIONAL_OPTIMUM_ROUNDINGS',cnt,'worst_U_over_Out',str(worst),flush=True)

def integer_arc_grid(M):
    # Enumerate all integer arc instances bounded by r_e<=M once, then query every budget.
    # Triple arcs can be replaced by complementary singletons, so nine arcs suffice.
    chosen=list(range(8))+[12]; states={}
    def visit(j,st,out):
        if j==len(chosen):states[st]=max(states.get(st,0),out);return
        row=ROWS[chosen[j]];cap=min(M//st[i] for i in range(4) if row[i])
        for n in range(1,cap+1):visit(j+1,tuple(st[i]*(n if row[i] else 1) for i in range(8)),out*n)
    visit(0,(1,)*8,1)
    candidates=list(states.items());worst=F(0);arg=None;cnt=0
    pairs=[(r,s) for r in range(1,M+1) for s in range(1,r+1)]
    for pp in product(pairs,repeat=4):
        r=tuple(p[0] for p in pp);s=tuple(p[1] for p in pp);budget=r+s
        best=max(out for st,out in candidates if all(a<=b for a,b in zip(st,budget)))
        bound=u12(r,s);ratio=bound/best**12;cnt+=1
        if ratio>worst:worst=ratio;arg=(r,s,best,bound)
        assert (16*best)**12>bound
    print('INTEGER_ARC_GRID',M,'statistics',cnt,'feasible_stat_vectors',len(states),'worst_ratio12',str(worst),'witness',arg,flush=True)

if __name__=='__main__':
    modes=sys.argv[1:] or ['dual','small','random','arcs','grid']
    if 'dual' in modes:verify_dual()
    if 'small' in modes:exhaustive22()
    if 'random' in modes:random_checks()
    if 'arcs' in modes:arc_tests()
    if 'grid' in modes:
        integer_arc_grid(3);integer_arc_grid(4)
