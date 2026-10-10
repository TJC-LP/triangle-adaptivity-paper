"""Fresh exact audit of C4 arc dual; no solver modules are imported."""
from fractions import Fraction as F
from itertools import combinations, product
from random import Random
import json
from pathlib import Path

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def square(a,b):
    # Rational forward elimination followed by back substitution.
    z=[[F(t) for t in row]+[F(v)] for row,v in zip(a,b)]
    d=len(b)
    for j in range(d):
        p=next((i for i in range(j,d) if z[i][j]),None)
        if p is None:return None
        z[j],z[p]=z[p],z[j]
        for i in range(j+1,d):
            if z[i][j]:
                q=z[i][j]/z[j][j]
                for k in range(j+1,d+1):z[i][k]-=q*z[j][k]
                z[i][j]=F(0)
    x=[F(0)]*d
    for j in range(d-1,-1,-1):x[j]=(z[j][d]-dot(z[j][j+1:d],x[j+1:]))/z[j][j]
    return tuple(x)

def arcs(k,triples=True):
    lens=range(1,k) if triples else range(1,min(k,3))
    return [frozenset((i+j)%k for j in range(t)) for t in lens for i in range(k)]+[frozenset(range(k))]

def rows(k,aa):
    ee=[{i,(i+1)%k} for i in range(k)]
    return [tuple(int(bool(a&e)) for e in ee)+tuple(int(len(a&e)==1) for e in ee) for a in aa]

def enum(k,aa):
    rr=rows(k,aa); vs=set(); bases=0
    # A vertex with m positive entries has m independent active arc rows.
    for m in range(1,2*k+1):
        for supp in combinations(range(2*k),m):
            for active in combinations(rr,m):
                bases+=1
                a=[[r[j] for j in supp] for r in active]
                y=square(a,[1]*m)
                if y is None or min(y)<=0:continue
                x=[F(0)]*(2*k)
                for j,t in zip(supp,y):x[j]=t
                if all(dot(r,x)>=1 for r in rr):vs.add(tuple(x))
    return sorted(vs),bases

def transformed(v,k): return v[:k]+tuple(v[i]+v[k+i] for i in range(k))

def classify(vs,k):
    transformed_vs=[transformed(v,k) for v in vs]
    domination={}
    for i,v in enumerate(transformed_vs):
        for j,w in enumerate(transformed_vs):
            if i!=j and all(a>=b for a,b in zip(v,w)):
                domination[i]=j;break
    needed=[i for i in range(len(vs)) if i not in domination]
    rng=Random(463921+k)
    witnesses={}
    vscaled=[[int(x*12) for x in v] for v in vs]
    for it in range(2000000):
        if len(witnesses)==len(needed):break
        ss=[rng.randrange(0,16) for _ in range(k)]
        c=[s+rng.randrange(0,20) for s in ss]+ss
        vals=[dot(v,c) for v in vscaled]
        best=min(vals); inds=[i for i,x in enumerate(vals) if x==best]
        if len(inds)==1:
            i=inds[0]
            if i not in witnesses:witnesses[i]=(c,F(min(x for j,x in enumerate(vals) if j!=i)-best,12))
    assert set(witnesses)==set(needed),(needed,witnesses.keys())
    return needed,domination,witnesses,it

def terms():
    d={}
    def add(name,rr,ss):
        v=tuple(F(rr.get(i,0)) for i in range(4))+tuple(F(ss.get(i,0)) for i in range(4));d[v]=name
    for i in range(4):
        other=[j for j in range(4) if j!=i]
        for j,k in combinations(other,2):add('A',{i:1},{j:1,k:1})
        add('B',{i:1},{j:F(1,2) for j in other})
    for i,j in combinations(range(4),2):
        add('C' if (i-j)%4==2 else 'Cprime',{i:F(1,2),j:F(1,2)},{k:F(1,2) for k in range(4) if k not in (i,j)})
    for i in range(2):
        add('D',{i:1,i+2:1},{})
        add('H',{i:F(1,2),i+2:F(1,2)},{j:F(1,4) for j in range(4)})
    for j in range(4):
        i,k=(j-1)%4,(j+1)%4
        add('E',{i:F(1,2),k:F(1,2)},{i:F(1,2),j:F(1,2),k:F(1,2)})
    for i in range(4):
        j=(i+2)%4
        add('F',{i:F(1,3),j:F(2,3)},{k:F(1,3) for k in range(4) if k!=j})
        add('G',{k:F(1,3) for k in range(4) if k!=i},{k:F(1,3) for k in range(4) if k!=j})
    return d

def orbit(v):
    z=set()
    for sign in (-1,1):
        for shift in range(4):
            p=[(sign*i+shift)%4 for i in range(4)]
            z.add(tuple(v[p[i]] for i in range(4))+tuple(v[4+p[i]] for i in range(4)))
    return z

def mat_instance(aa,nn):
    # Construct finite endpoint tuples and relations independently of stats formulas.
    coord=[[i for i,a in enumerate(aa) if v in a] for v in range(4)]
    spaces=[list(product(*(range(nn[i]) for i in ids))) for ids in coord]
    edges=[]
    for e in range(4):
        f=(e+1)%4
        common=[(coord[e].index(i),coord[f].index(i)) for i in coord[e] if i in coord[f]]
        edges.append([{b for b,y in enumerate(spaces[f]) if all(x[i]==y[j] for i,j in common)} for x in spaces[e]])
    r=[];s=[]
    for e,adj in enumerate(edges):
        outdeg=[len(a) for a in adj]
        indeg=[sum(j in a for a in adj) for j in range(len(spaces[(e+1)%4]))]
        assert len(set(outdeg))==len(set(indeg))==1
        r.append(sum(outdeg));s.append(outdeg[0]*indeg[0])
    # Pair of length-two path count matrices: Out=sum_{x,z} RS[x,z] TQ[z,x].
    paths=[]
    for e in (0,2):
        p=[]
        for adj in edges[e]:
            counts={}
            for y in adj:
                for z in edges[e+1][y]:counts[z]=counts.get(z,0)+1
            p.append(counts)
        paths.append(p)
    out=sum(n*paths[1][z].get(x,0) for x,dd in enumerate(paths[0]) for z,n in dd.items())
    return [len(t) for t in spaces],r,s,out

def primal_witness(c,v,rr):
    tight=[i for i,a in enumerate(rr) if dot(a,v)==1]
    target=dot(c,v)
    for m in range(min(len(tight),len(c)),0,-1):
        for support in combinations(tight,m):
            for active in combinations(range(len(c)),m):
                x=square([[rr[j][i] for j in support] for i in active],[c[i] for i in active])
                if x is None or min(x)<0 or sum(x)!=target:continue
                if all(sum(rr[j][i]*t for j,t in zip(support,x))<=c[i] for i in range(len(c))):
                    result=[F(0)]*len(rr)
                    for j,t in zip(support,x):result[j]=t
                    return result
    raise AssertionError(('no primal witness',c,v))

def run():
    report={}
    for k in (3,4):
        aa=arcs(k,False);vs,bases=enum(k,aa)
        keep,dom,ws,it=classify(vs,k)
        print('ENUM',k,'arcs',len(aa),'bases',bases,'vertices',len(vs),'needed',len(keep),'redundant',len(dom),'strict_witness_draws',it,flush=True)
        if k==4:
            full,fullbases=enum(4,arcs(4,True))
            assert full==vs
            print('FULL13',len(full),'vertices',fullbases,'bases; exactly equal to reduced9',flush=True)
        allrows=rows(k,arcs(k))
        assert all(dot(v,r)>=1 for v in vs for r in allrows)
        report[str(k)]={'vertices':[[str(t) for t in v] for v in vs],'needed':keep,'domination':dom,'separation':{str(i):{'c':c,'gap':str(gap)} for i,(c,gap) in ws.items()},'bases':bases}
        if k==4:
            tt=terms();assert len(tt)==38 and set(tt)=={vs[i] for i in keep}
            orbit_sizes=[];done=set()
            for v in tt:
                if v in done:continue
                orb=orbit(v);done|=orb;orbit_sizes.append((tt[v],len(orb)))
            print('ORBITS',orbit_sizes,flush=True)
            report['orbits']=orbit_sizes
            pw={}
            for i in keep:
                c,gap=ws[i]
                p=primal_witness(c,vs[i],rows(4,aa))
                pw[str(i)]={'arc_log_multiplicities':[str(t) for t in p],'objective':str(sum(p))}
            report['primal_witnesses']=pw
            print('PRIMAL_STRICT_WITNESSES',len(pw),'exact equalities and feasibility certified',flush=True)
            rebuilt=[]
            for n in (2,3,4):
                for i in keep:
                    v=vs[i];nn=[n if dot(row,v)==1 else 1 for row in rows(4,aa)]
                    dims,r,s,out=mat_instance(aa,nn)
                    ep=[int(t*12) for t in v]
                    rhs=1
                    for a,b in zip(r+s,ep):rhs*=a**b
                    assert out**12==rhs
                    expected=1
                    for a in nn:expected*=a
                    assert out==expected
                    for e in range(4):
                        rr=ss=1
                        for a,m in zip(aa,nn):
                            meet=len(a&{e,(e+1)%4})
                            if meet:rr*=m
                            if meet==1:ss*=m
                        assert rr==r[e] and ss==s[e]
                    rebuilt.append({'vertex':i,'family':tt[v],'n':n,'tight_arcs':[j for j,m in enumerate(nn) if m>1],'dimensions':dims,'r':r,'s':s,'out':out})
                print('MATRIX_WITNESSES n',n,'count',len(keep),'outputs',sorted({z['out'] for z in rebuilt if z['n']==n}),flush=True)
            report['rebuilt']=rebuilt
            fullaa=arcs(4,True)
            fullcases=[('all13_twos',[2]*13)]+[(f'triples_{n}',[1]*8+[n]*4+[1]) for n in (2,3,4)]+[('mixed',[2,3,1,2,1,2,3,1,2,1,3,2,2])]
            fullrecords=[]
            for label,nn in fullcases:
                dims,r,s,out=mat_instance(fullaa,nn)
                expected=1
                for n in nn:expected*=n
                assert out==expected
                for e in range(4):
                    rr=ss=1
                    for a,m in zip(fullaa,nn):
                        meet=len(a&{e,(e+1)%4})
                        if meet:rr*=m
                        if meet==1:ss*=m
                    assert (rr,ss)==(r[e],s[e])
                record={'case':label,'n':nn,'dimensions':dims,'r':r,'s':s,'out':out}
                fullrecords.append(record)
                print('FULL13_MATRIX',record,flush=True)
            report['full13_rebuilt']=fullrecords
    Path('lp_independent.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':run()
