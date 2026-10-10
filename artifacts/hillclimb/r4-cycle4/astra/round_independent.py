"""Independent exact verification of 4-cycle arc rounding and examples.

No solver/verifier code imported or executed. Run with python3 -I.
All load-bearing operations use integers or Fraction. In particular the LP
uses symbolic prime logarithms, compared by clearing denominators and integer
powers, and algebraic multiplicities are floored by integer binary search.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import prod, lcm
import sys
import random

EDGES = [frozenset((i, (i+1)%4)) for i in range(4)]
ARCS = [frozenset(((i+j)%4 for j in range(k)))
        for k in range(1,4) for i in range(4)] + [frozenset(range(4))]


def terms():
    ans = []
    def add(label, rr={}, ss={}):
        ans.append((label, tuple(F(rr.get(i,0)) for i in range(4)) +
                    tuple(F(ss.get(i,0)) for i in range(4))))
    for i in range(4):
        others = [j for j in range(4) if i != j]
        for j,k in combinations(others,2):
            add(f'A{i}{j}{k}', {i:1}, {j:1,k:1})
        add(f'B{i}', {i:1}, {j:F(1,2) for j in others})
    for i,j in combinations(range(4),2):
        add(f'C{i}{j}', {i:F(1,2),j:F(1,2)},
            {k:F(1,2) for k in range(4) if k not in (i,j)})
    for i,j in [(0,2),(1,3)]:
        add(f'D{i}{j}', {i:1,j:1})
        add(f'H{i}{j}', {i:F(1,2),j:F(1,2)}, {k:F(1,4) for k in range(4)})
    for i in range(4):
        j,k,l = (i+1)%4,(i+2)%4,(i+3)%4
        add(f'E{i}', {i:F(1,2),k:F(1,2)}, {i:F(1,2),j:F(1,2),k:F(1,2)})
        add(f'F{i}', {i:F(1,3),k:F(2,3)}, {i:F(1,3),j:F(1,3),l:F(1,3)})
        add(f'G{i}', {j:F(1,3),k:F(1,3),l:F(1,3)}, {i:F(1,3),j:F(1,3),l:F(1,3)})
    assert len(ans) == len(set(v for _,v in ans)) == 38
    return ans


TERMS = terms()


def u12(r,s):
    return min(prod(F(x)**int(12*a) for x,a in zip(r+s,v)) for _,v in TERMS)


def factor(n):
    out = {}
    d = 2
    while d*d <= n:
        while n%d == 0:
            out[d] = out.get(d,0)+1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n,0)+1
    return out


class Logs:
    """Exact real value sum(q_p log p); all comparisons are exact."""
    __slots__ = ('a',)
    def __init__(self, a=None):
        self.a = {p:F(q) for p,q in (a or {}).items() if q}
    @classmethod
    def log(cls,x):
        x = F(x)
        a = factor(x.numerator)
        for p,q in factor(x.denominator).items():
            a[p] = a.get(p,0)-q
        return cls(a)
    def __add__(self,other):
        a = self.a.copy()
        for p,q in other.a.items():
            a[p] = a.get(p,F(0))+q
        return Logs(a)
    def __sub__(self,other):
        return self + other * -1
    def __mul__(self,q):
        return Logs({p:a*q for p,a in self.a.items()})
    def __truediv__(self,q):
        return self * (1/F(q))
    def rational_power(self):
        d = lcm(*(q.denominator for q in self.a.values()))
        return prod((F(p)**int(q*d) for p,q in self.a.items()),start=F(1)), d
    def sign(self):
        x,d = self.rational_power()
        return (x>1)-(x<1)
    def __lt__(self,other):
        return (self-other).sign()<0
    def __eq__(self,other):
        return self.a == other.a
    def floor_exp(self):
        value,d = self.rational_power()
        assert value >= 1
        lo,hi = 1,2
        while hi**d * value.denominator <= value.numerator:
            lo,hi = hi,hi*2
        while hi-lo > 1:
            mid = (lo+hi)//2
            if mid**d*value.denominator <= value.numerator:
                lo = mid
            else:
                hi = mid
        return lo
    def __repr__(self):
        return repr(self.a)


def solve_arc(r,s, reduced=False):
    arcs = [a for a in ARCS if not reduced or len(a)!=3]
    n,m = len(arcs),8
    A = [[F(bool(a&e)) for a in arcs] for e in EDGES]
    A += [[F(len(a&e)==1) for a in arcs] for e in EDGES]
    for i in range(m):
        A[i] += [F(i==j) for j in range(m)]
    A += [[F(-1)]*n+[F(0)]*m]
    b = [Logs.log(x) for x in r+s]+[Logs()]
    basic = list(range(n,n+m))
    steps=0
    while True:
        entering = next((j for j,v in enumerate(A[-1]) if v<0),None)
        if entering is None:
            break
        candidates = [(b[i]/A[i][entering],basic[i],i) for i in range(m) if A[i][entering]>0]
        assert candidates
        _,_,leaving = min(candidates)
        f = A[leaving][entering]
        A[leaving] = [x/f for x in A[leaving]]
        b[leaving] = b[leaving]/f
        for i in range(m+1):
            if i == leaving:
                continue
            f = A[i][entering]
            if f:
                A[i] = [x-f*y for x,y in zip(A[i],A[leaving])]
                b[i] = b[i]-b[leaving]*f
        basic[leaving] = entering
        steps += 1
        assert steps < 500
    x = [Logs() for a in arcs]
    for i,j in enumerate(basic):
        assert b[i].sign() >= 0
        if j<n:
            x[j]=b[i]
    # Exact objective equality, all primal inequalities, and dual feasibility.
    target = Logs.log(u12(r,s))/12
    assert b[-1] == target, (r,s,b[-1],target)
    for e in range(8):
        lhs = Logs()
        for a,v in zip(arcs,x):
            if (bool(a&EDGES[e]) if e<4 else len(a&EDGES[e-4])==1):
                lhs = lhs+v
        assert not Logs.log((r+s)[e]) < lhs
    return dict(zip(arcs,x))


def round_arc(r,s,reduced=False):
    logs = solve_arc(r,s,reduced)
    ns = {a:v.floor_exp() for a,v in logs.items() if len(a)<4}
    m = min(F(r[i])/prod(n for a,n in ns.items() if a&EDGES[i]) for i in range(4))
    assert m>=1
    ns[ARCS[-1]] = m.numerator//m.denominator
    rr,ss,out = arc_stats(ns)
    assert all(x<=y for x,y in zip(rr+ss,r+s))
    assert (16*out)**12 > u12(r,s)
    return ns,out


def arc_stats(ns):
    return ([prod(n for a,n in ns.items() if a&e) for e in EDGES],
            [prod(n for a,n in ns.items() if len(a&e)==1) for e in EDGES],
            prod(ns.values()))


def arc_opt(r,s):
    # Triples are dominated by the full arc: same size incidence, no norms.
    arcs = [a for a in ARCS if len(a)!=3]
    limits = [[i for i,e in enumerate(EDGES) if a&e] +
              [i+4 for i,e in enumerate(EDGES) if len(a&e)==1] for a in arcs]
    def go(i,b):
        if i==len(arcs):
            return 1
        bound = min(b[j] for j in limits[i])
        ans = 0
        for n in range(1,bound+1):
            bb=b.copy()
            for j in limits[i]:
                bb[j] //= n
            ans=max(ans,n*go(i+1,bb))
        return ans
    return go(0,r+s)


def build_arc(ns):
    # Explicit vertex coordinate tuples and explicit 0/1 relation sets.
    active=[(a,n) for a,n in ns.items() if n>1]
    coords=[[k for k,(a,n) in enumerate(active) if v in a] for v in range(4)]
    verts=[list(product(*(range(active[k][1]) for k in ids))) for ids in coords]
    rels=[]
    for i in range(4):
        j=(i+1)%4
        shared=set(coords[i])&set(coords[j])
        pairs=[(coords[i].index(k),coords[j].index(k)) for k in shared]
        rels.append({(u,v) for u,x in enumerate(verts[i]) for v,y in enumerate(verts[j])
                     if all(x[a]==y[b] for a,b in pairs)})
    out=sum((x,y) in rels[0] and (y,z) in rels[1] and
            (z,w) in rels[2] and (w,x) in rels[3]
            for x,y,z,w in product(*(range(len(v)) for v in verts)))
    rr=[]; ss=[]
    for i,rel in enumerate(rels):
        row=[sum(x==u for x,y in rel) for u in range(len(verts[i]))]
        col=[sum(y==v for x,y in rel) for v in range(len(verts[(i+1)%4]))]
        assert len(set(row))==len(set(col))==1
        rr.append(len(rel))
        # Biregularity gives both a positive singular pair and matching Schur upper bound.
        ss.append(row[0]*col[0])
    assert (rr,ss,out)==arc_stats(ns)
    assert out**12<=u12(rr,ss)
    return [len(v) for v in verts],rr,ss,out


def examples():
    print('T4 monomials t^a L^b, and required L >= t^h:')
    threshold=F(0)
    for name,v in TERMS:
        a=sum(v[i] for i in [1,4,5,6]); b=sum(v[i] for i in [0,2,3,7])
        h=(3-a)/b if b else None
        if h is not None:
            assert a+b>=2 and b>=F(1,2)
            threshold=max(threshold,h)
        print(name, 'a=',a,'b=',b,'h=',h)
    assert threshold==3
    print('EXACT THRESHOLD',threshold)
    for t in map(F,['1','3/2','7/4','15/8','31/16','63/32']):
        for L in [t*t,t**3,F(10**6)]:
            val=u12([L,t,L,L],[t,t,t,L])
            assert val == min(t**36,(t**3*L)**6)
            print('T4',t,'L=',L,'U^12=',val,'t^36=',t**36,'equality=',val==t**36)
        L=(t**3).numerator//(t**3).denominator
        if F(L)<t**3:
            L+=1
        print('T4 smallest integral L >= t',t,':',L)
    for t in map(F,['3/2','7/4','15/8','31/16','63/32']):
        r=[t,t**3,t**4,t**3]; s=[F(1),t*t,t*t,t*t]
        # This real optimum is explicitly specified, independent of simplex tie breaking.
        nn={frozenset([2]):t,frozenset([3]):t,frozenset([2,3]):t,ARCS[-1]:t}
        assert arc_stats(nn)==(r,s,t**4)
        assert u12(r,s)==t**48
        rounded={a:1 for a in nn}
        assert arc_stats(rounded)[2]==1
        print('LITERAL FACTOR16',t,'r=',r,'s=',s,'U=',t**4,'roundedOut=1')
        nn={frozenset([0]):t,frozenset([2]):t,frozenset([3]):t,frozenset([2,3]):t,ARCS[-1]:F(1)}
        r=[t,t*t,t**3,t**3]; s=[t,t*t,t*t,t**3]
        assert arc_stats(nn)==(r,s,t**4)
        assert u12(r,s)==t**48
        print('FULL=1 FACTOR16',t,'r=',r,'s=',s,'U=',t**4,'roundedOut=1')
    # Five-edge P6 support: T rows [1,1,0], [0,1,1], [0,0,1].
    gram=[[F(1),F(1),F(0)],[F(1),F(2),F(1)],[F(0),F(1),F(2)]]
    b=F(27,8)
    h=[[b*int(i==j)-gram[i][j] for j in range(3)] for i in range(3)]
    minors=[h[0][0],h[0][0]*h[1][1]-h[0][1]*h[1][0],
            h[0][0]*(h[1][1]*h[2][2]-h[1][2]*h[2][1])-
            h[0][1]*(h[1][0]*h[2][2]-h[1][2]*h[2][0])+
            h[0][2]*(h[1][0]*h[2][1]-h[1][1]*h[2][0])]
    assert all(x>0 for x in minors)
    print('P6 Gram exact positive definite certificate at sigma² upper=27/8:',minors)
    for n in [1,2,3,5,7]:
        # X singleton blowup n; Y singleton n; ZW pair matching n.
        ns={frozenset([0]):n,frozenset([1]):n,frozenset([2,3]):n}
        rr,ss,out=arc_stats(ns)
        assert out**12==u12(rr,ss)
        print('T5 MATCHING',n,build_arc(ns),'best complete blocks=',n*n)
        # XYZ? Obstruction: R singleton edge; ZW pair n does the job.
        ns={frozenset([2,3]):n}
        rr,ss,out=arc_stats(ns)
        assert out**12==u12(rr,ss)
        print('T5 OBSTRUCTION',n,build_arc(ns))
    for ns in [
        {a:2 for a in ARCS if len(a)==1},
        {a:2 for a in ARCS if len(a)==2},
        {a:2 for a in ARCS if len(a)==3},
        {ARCS[-1]:3},
        {frozenset([0]):2,frozenset([1,2]):3,frozenset([3,0]):2,ARCS[-1]:2},
    ]:
        print('ARC REBUILD', {tuple(sorted(a)):n for a,n in ns.items()},build_arc(ns))
    for values in [(1,1,1,1,1,1,1),(2,2,2,2,2,2,2),(3,2,3,2,3,3,3),(2,1,3,2,2,3,1)]:
        aa,bb,cc,dd,p,q,m=values
        ns={frozenset([i]):v for i,v in enumerate((aa,bb,cc,dd))}
        ns.update({frozenset([1,2]):p,frozenset([0,3]):q,ARCS[-1]:m})
        dims,rr,ss,out=build_arc(ns)
        tight=[name for name,v in TERMS if prod(F(x)**int(12*a) for x,a in zip(rr+ss,v))==out**12]
        print('KITE',values,'stats=',(dims,rr,ss,out),'tight=',tight)
    for values in [(1,1,1,1,1,1),(2,2,2,2,2,2),(3,2,1,2,3,2),(1,3,2,1,4,3)]:
        aa,bb,cc,dd,p,m=values
        ns={frozenset([i]):v for i,v in enumerate((aa,bb,cc,dd))}
        ns.update({frozenset([1,2]):p,ARCS[-1]:m})
        dims,rr,ss,out=build_arc(ns)
        tight=[name for name,v in TERMS if prod(F(x)**int(12*a) for x,a in zip(rr+ss,v))==out**12]
        assert 'F1' in tight
        print('F FAMILY',values,'stats=',(dims,rr,ss,out),'tight=',tight)
    # Complete-block exact optimum brute force, small n.
    for n in [1,2,3,4,5]:
        best=0
        for a,b,c,d,m in product(range(1,n*n+1),range(1,n*n+1),[1],[1],range(1,n+1)):
            rr=[m*a*b,m*b*c,m*c*d,m*d*a]
            ss=[a*b,b*c,c*d,d*a]
            if all(x<=y for x,y in zip(rr+ss,[n*n,n*n,n,n*n,n*n,n*n,1,n*n])):
                best=max(best,m*a*b*c*d)
        assert best==n*n
        print('BLOCK EXACT ENUM',n,best)


def grid(n):
    points=[(r,s) for r in range(1,n+1) for s in range(1,r+1)]
    worst=(F(0),None); bestworst=(F(0),None)
    count=0
    for point in product(points,repeat=4):
        r=[x[0] for x in point]; s=[x[1] for x in point]
        ns,out=round_arc(r,s)
        ratio=F(u12(r,s),out**12)
        if ratio>worst[0]:
            worst=(ratio,(r,s,out,{tuple(sorted(a)):m for a,m in ns.items() if m>1}))
        opt=arc_opt(r,s)
        ratio=F(u12(r,s),opt**12)
        if ratio>bestworst[0]:
            bestworst=(ratio,(r,s,opt))
        count+=1
        if count%1000==0:
            print('progress',count,flush=True)
    print('GRID',n,'count',count,'zero violations, exact LP optimum equality at every point')
    print('WORST LITERAL ratio^12',worst)
    print('WORST OPTIMAL ratio^12',bestworst)


def random_stats(count):
    rng=random.Random(20261009)
    worst=(F(0),None)
    for k in range(count):
        r=[rng.randint(1,300) for i in range(4)]
        s=[rng.randint(1,x) for x in r]
        ns,out=round_arc(r,s)
        ratio=F(u12(r,s),out**12)
        if ratio>worst[0]:
            worst=(ratio,(r,s,out,{tuple(sorted(a)):m for a,m in ns.items() if m>1}))
    print('RANDOM',count,'seed20261009,maxr300,zero violations, exact LP optimum equality each point')
    print('WORST LITERAL ratio^12',worst)


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='grid':
        grid(int(sys.argv[2]))
    elif len(sys.argv)>1 and sys.argv[1]=='random':
        random_stats(int(sys.argv[2]))
    else:
        examples()
