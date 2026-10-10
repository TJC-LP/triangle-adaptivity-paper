"""Fresh verifier. Standard library only; no solver imports. Run python3 -I live_audit.py.

Relations use integer vertex identifiers local to their domains and row adjacency
sets. The evaluator calculates all edge prices before taking binding minima.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from random import Random
import json
import sys


def invert(rows, n):
    back = [set() for _ in range(n)]
    for a, row in enumerate(rows):
        for b in row:
            back[b].add(a)
    return back


def measure(relations, support=True):
    R, S, T = relations
    forward = [list(map(len, e)) for e in relations]
    incoming = [invert(e, len(relations[(i + 1) % 3]))
                for i, e in enumerate(relations)]
    backward = [list(map(len, e)) for e in incoming]
    # Each relation's price contributes one option at each of its endpoints.
    leave = [[0]*len(e) for e in relations]
    enter = [[0]*len(e) for e in relations]
    work = []
    for i, e in enumerate(relations):
        j, k = (i+1) % 3, (i+2) % 3
        m = 0
        for a, row in enumerate(e):
            for b in row:
                price = 1 + min(forward[j][b], backward[k][a])
                leave[i][a] += price
                enter[j][b] += price
                m += price-1
        work.append(m)
    costs = [sum(min(a,b) for a,b in zip(leave[i],enter[i])) for i in range(3)]
    sizes = [sum(v) for v in forward]
    f = [sum(x*x for x in v) for v in forward]
    b = [sum(x*x for x in v) for v in backward]
    out = sum(len(S[y] & incoming[2][x]) for x,row in enumerate(R) for y in row)
    dead = []
    if support:
        for i, e in enumerate(relations):
            j, k = (i+1) % 3, (i+2) % 3
            dead.append(sum(relations[j][b].isdisjoint(incoming[k][a])
                            for a,row in enumerate(e) for b in row))
    return dict(sizes=sizes, N=sum(sizes), costs=costs, C=min(costs),
                fwd=f, rev=b, B2cube=min(f[0]*f[1]*f[2],b[0]*b[1]*b[2]),
                M=work, Out=out, dead=dead)


def live(p,q,t,g,k,w):
    assert min(p,q,t,g,k,w)>=1
    assert p%t == 0 and p*t%g == 0 and g<=p and q%k==0
    z=p*t//g
    assert z%q==0 and z%w==0
    blocks=z//w
    helpers=blocks*(q//k)
    R=[set() for _ in range(p+helpers)]
    S=[set() for _ in range(q+blocks*q)]
    T=[set() for _ in range(2*t+z)]
    # Index Z1 first, witness Zw second, grouped Z2 last.
    for x in range(p):
        R[x].update(range(q))
    for y in range(q):
        S[y].update(range(2*t))
    for a in range(t):
        T[a].add(a)
        T[t+a].update(range(a*(p//t),(a+1)*(p//t)))
    for a in range(z):
        zz=2*t+a
        T[zz].update((a*g+d)%p for d in range(g))
        S[a%q].add(zz)
        block=a//w
        for yy in range(q):
            S[q+block*q+yy].add(zz)
        for h in range(q//k):
            T[zz].add(p+block*(q//k)+h)
    for b in range(blocks):
        for yy in range(q):
            R[p+b*(q//k)+yy//k].add(q+b*q+yy)
    return R,S,T


def live_formula(p,q,t,g,k,w):
    z=p*t//g
    h=z*q//(w*k)
    sizes=[p*q+z*q//w, 2*q*t+z*(q+1), p*t+p+t+z*q//k]
    f=[p*q*q+z*q*k//w, q*(2*t+z//q)**2+z*q*w,
       z*(g+q//k)**2+p*p//t+t]
    b=[q*p*p+z*q//w, 2*t*q*q+z*(q+1)**2,
       (p-t)*(t+1)**2+t*(t+2)**2+h*w*w]
    cx=(p-t)*(q*(t+1)+min(q,t+1))+t*(q*(t+2)+min(q,t+2))+h*(k*w+min(k,w))
    cy=q*min(p*(t+2)+t,3*t+p+(z//q)*(1+min(p,g+q//k)))+(z*q//w)*(w+1)
    cz=t*(q+1)+p*q+t*min(q,p//t)+z*min(1+min(p,g+q//k)+2*q,g*(q+1)+(q//k)*(k+1))
    out=t*q+p*q+p*t+z*q
    return dict(sizes=sizes,N=sum(sizes),fwd=f,rev=b,costs=[cx,cy,cz],C=min(cx,cy,cz),Out=out)


def disjoint_rotations(instances):
    """Explicitly unite three independently constructed components; rotate by index."""
    result=[[],[],[]]
    for turn,inst in enumerate(instances):
        rotated=inst[turn:]+inst[:turn]
        offsets=list(map(len,result))
        for i,rows in enumerate(rotated):
            result[i].extend({b+offsets[(i+1)%3] for b in row} for row in rows)
    return result


def symmetrize(v):
    return dict(N=3*v['N'],C=sum(v['costs']),Out=3*v['Out'],
                B2=min(sum(v['fwd']),sum(v['rev'])),
                fwd=sum(v['fwd']),rev=sum(v['rev']),base_costs=v['costs'])


def old_gadget(v):
    # Compress a coordinate tuple into its mixed-radix integer. X=(A,B).
    a_count=v**3
    p=v**6
    y0=v**4
    z1=v**5
    R=[set() for _ in range(p)]
    S=[set() for _ in range(y0+v**10)]
    T=[set() for _ in range(z1+v**8)]
    for x in range(p):
        a,b=divmod(x,a_count)
        R[x].update(range(y0))
        T[a*v*v+b//v].add(x)
        for ee in range(a_count):
            base=y0+((x*a_count+ee)*v)
            zs=range(z1+(a*a_count+ee)*v*v,z1+(a*a_count+ee+1)*v*v)
            for e in range(v):
                R[x].add(base+e)
                S[base+e].update(zs)
            for z in zs:
                T[z].add(x)
    for y in range(y0):
        S[y].update(range(z1))
    return R,S,T


def old_formula(v):
    return dict(sizes=[2*v**10,v**12+v**9,v**11+v**6],
                costs=[v**15+v**11+v**10+v**6,v**12+2*v**10+v**9,2*v**12+v**10+v**6],
                fwd=[4*v**14,2*v**14,v**14+v**7],
                rev=[v**16+v**10,v**16+v**13,v**16+2*v**11+v**6],
                Out=v**10+v**12,N=v**12+v**11+2*v**10+v**9+v**6)


def verify_formula(params):
    got=measure(live(*params))
    expected=live_formula(*params)
    for key,value in expected.items():
        assert got[key]==value,(params,key,got[key],value)
    assert got['dead']==[0,0,0]
    return got


def bound_checks(v):
    n=v['N']; c=v['C']; b=v['B2cube']; r,s,t=v['sizes']
    excess=max(c-n,0)
    assert excess**8<=r*s*t*b*b
    assert n**3*excess**24<=27*b**10
    assert min(v['M'])**5<=r*s*t*b
    assert v['Out']**3<=b
    if v['dead']==[0,0,0]:
        assert v['Out']>=max(v['sizes'])
    # Degree-three products from the forward orientation and its reflection.
    a,d,g=v['fwd']; ap,dp,gp=v['rev']
    for m,rr,tt,aa,bb in ((v['M'][0],r,t,a,d),(v['M'][1],s,r,d,g),(v['M'][2],t,s,g,a),
                         (v['M'][0],r,s,ap,gp),(v['M'][1],s,t,dp,ap),(v['M'][2],t,r,gp,dp)):
        assert m**4<=rr*tt*tt*aa*bb


def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'small'
    if mode=='small':
        count=0
        tuples=[]
        for p,q,t,g,k,w in product(range(1,9),range(1,7),range(1,5),range(1,7),range(1,5),range(1,5)):
            if p%t or g>p or p*t%g or q%k: continue
            z=p*t//g
            if z%q or z%w: continue
            par=(p,q,t,g,k,w)
            got=verify_formula(par)
            bound_checks(got)
            tuples.append(par)
            count+=1
        print('LIVE_PARAMETER_TUPLES',count,flush=True)
        rng=Random(817221)
        for rep in range(100):
            pars=[rng.choice(tuples) for _ in range(3)]
            got=measure(disjoint_rotations([live(*p) for p in pars]))
            fs=[live_formula(*p) for p in pars]
            for key in ('sizes','fwd','rev','costs'):
                expected=[sum(f[key][(i+j)%3] for j,f in enumerate(fs)) for i in range(3)]
                assert got[key]==expected,(pars,key,got[key],expected)
            assert got['Out']==sum(f['Out'] for f in fs)
            assert got['dead']==[0,0,0]
            bound_checks(got)
        print('UNRELATED_ROTATED_TRIPLES',100,flush=True)
        for v in (1,2,3):
            got=measure(old_gadget(v))
            for key,value in old_formula(v).items(): assert got[key]==value,(v,key,got[key],value)
            assert got['dead']==[0,0,0]
            print('OLD_LITERAL',v,json.dumps(got),flush=True)
        for v in (1,2,3,4,8,16):
            s=symmetrize(old_formula(v));s['ratio']=str(Fraction(s['C'],s['N']+s['B2']))
            print('OLD_FORMULA',v,json.dumps(s),flush=True)
        for v in (1,2,3,4,8,16,32):
            f=live_formula(v**5,v**3,v**4,v**2,v**2,v)
            s=symmetrize(f)
            assert s['N']==3*(v**10+2*v**9+2*v**8+3*v**7+v**5+v**4)
            assert s['fwd']==13*v**11+2*v**10+v**9+v**6+v**4
            assert s['rev']>=s['fwd']
            assert f['costs'][0]==v**12+v**10+3*v**8+v**7
            if v>=2:
                assert s['N']<=9*v**10 and s['B2']<=15*v**11
                assert 24*s['C']>=v*(s['N']+s['B2'])
            s['ratio']=str(Fraction(s['C'],s['N']+s['B2']))
            print('LIVE_FORMULA',v,json.dumps(s),flush=True)
    elif mode=='literal':
        for v in (1,2,3,4):
            got=verify_formula((v**5,v**3,v**4,v**2,v**2,v))
            bound_checks(got)
            s=symmetrize(got)
            s['ratio']=str(Fraction(s['C'],s['N']+s['B2']))
            print('LIVE_LITERAL_BASE',v,json.dumps(got),flush=True)
            print('LIVE_LITERAL_ROTATION_SUM',v,json.dumps(s),flush=True)
            if v<=3:
                union=measure(disjoint_rotations([live(v**5,v**3,v**4,v**2,v**2,v) for _ in range(3)]))
                assert union['C']==s['C'] and union['N']==s['N'] and union['Out']==s['Out']
                assert union['dead']==[0,0,0] and union['fwd']==[s['B2']]*3
                print('LIVE_LITERAL_FULL_UNION',v,json.dumps(union),flush=True)
        pars=(2**8,2**6,2**7,2**5,2,1)
        got=verify_formula(pars)
        print('GENERAL_LITERAL',pars,json.dumps(got),json.dumps(symmetrize(got)),flush=True)
    elif mode=='random':
        rng=Random(492033)
        n=0;full=0
        for dimensions in product(range(1,4),repeat=3):
            if sum(dimensions[i]*dimensions[(i+1)%3] for i in range(3))>12:continue
            offsets=[0]
            for i in range(3): offsets.append(offsets[-1]+dimensions[i]*dimensions[(i+1)%3])
            for mask in range(1<<offsets[-1]):
                rel=[ [set() for _ in range(dimensions[i])] for i in range(3)]
                for i in range(3):
                    b=dimensions[(i+1)%3]
                    for a in range(dimensions[i]):
                        rel[i][a].update(c for c in range(b) if mask>>(offsets[i]+a*b+c)&1)
                got=measure(rel);bound_checks(got);n+=1
                full+=got['dead']==[0,0,0]
        print('EXHAUSTIVE',n,'fully_reduced',full,flush=True)
        maxratio=Fraction(0)
        for trial in range(10000):
            dims=[rng.randrange(1,11) for _ in range(3)]
            rel=[]
            for i in range(3):
                # Include sparse, dense, and skewed correlated row thresholds.
                threshold=rng.randrange(1,101)
                rel.append([{b for b in range(dims[(i+1)%3]) if rng.randrange(100)<(threshold if trial%2 else rng.randrange(101))} for a in range(dims[i])])
            got=measure(rel);bound_checks(got)
            if got['B2cube']:
                maxratio=max(maxratio,Fraction(max(0,got['C']-got['N'])**8,
                                             got['sizes'][0]*got['sizes'][1]*got['sizes'][2]*got['B2cube']**2))
        print('RANDOM',10000,'max_original_bound_eighth_power_ratio',str(maxratio),flush=True)
    elif mode=='extended':
        count=0
        for t,m,q,g,k,w in product(range(1,5),(1,2,3,4,6),(1,2,3,4,6),(1,2,3,4,6),(1,2,3),range(1,5)):
            p=m*t
            if g>p or p*t%g or q%k: continue
            z=p*t//g
            if z%q or z%w: continue
            verify_formula((p,q,t,g,k,w));count+=1
        print('EXTENDED_PARAMETER_TUPLES',count,flush=True)
        count=0
        for u in (2,3,5):
            for i in range(1,41):
                for j in range(0,(4*i)//5+1):
                    p,q,t,g,k,w=u**(4*i),u**(4*i-2*j),u**(4*i-j),u**(4*i-3*j),u**j,1
                    f=live_formula(p,q,t,g,k,w);s=symmetrize(f)
                    assert s['N']>=3*u**(8*i) and s['N']<=33*u**(8*i)
                    assert s['C']>=u**(12*i-3*j)
                    assert s['fwd']>=u**(12*i-4*j) and s['fwd']<=18*u**(12*i-4*j)
                    assert s['rev']>=u**(12*i-4*j)
                    count+=1
                    if (u,i,j) in ((2,1,0),(2,2,1),(2,5,4),(3,2,1),(5,2,1)):
                        s['ratio']=str(Fraction(s['C'],s['N']+s['B2']))
                        print('GENERAL_FORMULA',(u,i,j),json.dumps(s),flush=True)
        print('GENERAL_EXPONENT_GRID',count,flush=True)
        for v in range(2,101):
            f=live_formula(v**5,v**3,v**4,v**2,v**2,v);s=symmetrize(f)
            assert s['C']==v**12+4*v**10+3*v**9+7*v**8+7*v**7+v**5+v**4
            assert s['rev']==3*v**13+4*v**10+4*v**9+2*v**8+v**7+v**5+3*v**4
            assert s['Out']==3*(v**10+v**9+v**8+v**7)
        print('ADDITIONAL_POLYNOMIALS_v2_through_v100',99,flush=True)


if __name__=='__main__': main()
