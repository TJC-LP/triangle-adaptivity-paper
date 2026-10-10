from fractions import Fraction as F
from itertools import product

# Independent two-phase tableau simplex. Variables are nonnegative; constraints
# are supplied as <= or =. All pivot and comparison arithmetic is exact.
def maximize(names, constraints, objective):
    n=len(names); lookup={s:i for i,s in enumerate(names)}
    rows=[]; basis=[]; artificial=[]; labels=[]; signs=[]; total=n
    for form,op,b,label in constraints:
        row={lookup[s]:F(v) for s,v in form.items() if v}
        b=F(b); signs.append(F(-1) if b<0 else F(1))
        if op=='<=':
            row[total]=F(1); basic=total; total+=1
        else:
            basic=None
        if b<0:
            row={j:-a for j,a in row.items()}; b=-b; basic=None
        if basic is None:
            row[total]=F(1); basic=total; artificial.append(total);total+=1
        rows.append((row,b));basis.append(basic);labels.append(label)
    tab=[[row.get(j,F(0)) for j in range(total)]+[b] for row,b in rows]
    transforms=[[F(i==j)*signs[i] for j in range(len(rows))] for i in range(len(rows))]
    def pivot(i,j,red):
        a=tab[i][j];tab[i]=[x/a for x in tab[i]];transforms[i]=[x/a for x in transforms[i]]
        rr=tab[i]
        for k in range(len(tab)):
            if k==i or not tab[k][j]:continue
            a=tab[k][j];tab[k]=[x-a*y for x,y in zip(tab[k],rr)];transforms[k]=[x-a*y for x,y in zip(transforms[k],transforms[i])]
        if red[j]:
            a=red[j];red[:]=[x-a*y for x,y in zip(red,rr)]
        basis[i]=j
    def phase(cost, permitted):
        red=[cost.get(j,F(0)) for j in range(total)]+[F(0)]
        for i,bv in enumerate(basis):
            c=cost.get(bv,F(0))
            if c:red=[x-c*y for x,y in zip(red,tab[i])]
        count=0
        while True:
            enter=next((j for j in permitted if red[j]>0),None)
            if enter is None:return red
            cand=[(row[-1]/row[enter],basis[i],i) for i,row in enumerate(tab) if row[enter]>0]
            if not cand:raise ValueError('unbounded')
            leave=min(cand)[2];pivot(leave,enter,red);count+=1
            if count>10000:raise ValueError('iterations')
    phase1=phase({j:F(-1) for j in artificial},range(total))
    if phase1[-1]!=0:return None
    art=set(artificial)
    for i in reversed(range(len(tab))):
        if basis[i] not in art:continue
        ent=next((j for j in range(total) if j not in art and tab[i][j]),None)
        if ent is None:del tab[i];del basis[i];del transforms[i]
        else:pivot(i,ent,phase1)
    red=phase({lookup[s]:F(v) for s,v in objective.items()},[j for j in range(total) if j not in art])
    x=[F(0)]*total
    for i,j in enumerate(basis):x[j]=tab[i][-1]
    xx=dict(zip(names,x))
    for f,op,b,label in constraints:
        got=sum(F(v)*xx[s] for s,v in f.items())
        assert got<=F(b) if op=='<=' else got==F(b),(label,got,b)
    val=sum(F(v)*xx[s] for s,v in objective.items())
    assert val==-red[-1]
    dual=[F(0)]*len(constraints)
    co={lookup[s]:F(v) for s,v in objective.items()}
    for i,j in enumerate(basis):
        dual=[x+co.get(j,F(0))*y for x,y in zip(dual,transforms[i])]
    assert all(y>=0 or con[1]=='=' for y,con in zip(dual,constraints))
    for name in names:
        assert sum(y*F(con[0].get(name,0)) for y,con in zip(dual,constraints))>=F(objective.get(name,0))
    assert sum(y*F(con[2]) for y,con in zip(dual,constraints))==val
    return val,xx,dual

class Model:
    def __init__(self):self.names=[];self.rows=[]
    def var(self,s):
        if s not in self.names:self.names.append(s)
        return {s:F(1)}
    def le(self,a,b=0,name=''):
        for x in a:self.var(x)
        self.rows.append((a,'<=',F(b),name))
    def eq(self,a,b=0,name=''):
        for x in a:self.var(x)
        self.rows.append((a,'=',F(b),name))
    def solve(self,obj):return maximize(self.names,self.rows,obj)
def add(*forms):
    ans={}
    for f in forms:
        for k,v in f.items():ans[k]=ans.get(k,F(0))+v
    return {k:v for k,v in ans.items() if v}
def mul(f,a):return {k:v*F(a) for k,v in f.items()}

def model(branch='fwd',slope=None,size_equal=None,symmetric=False):
    m=Model(); norms=[m.var(x) for x in ('a','b','d')]; cost=m.var('c');den=m.var('m')
    main=[];params=[]
    for i in range(3):
        P,Q,T,G,K,W=[m.var(v+str(i)) for v in 'PQTGKW'];params.append((P,Q,T,G,K,W))
        Z=add(P,T,mul(G,-1)); C=add(P,Q,T)
        sizes=[add(P,Q),add(P,T),add(Z,Q)]
        main.append(sizes)
        for f in sizes:m.le(f,1,'size')
        # Remaining size monomials are dominated because K,W>=0.
        m.le(add(cost,mul(C,-1)),name='designated cost')
        for a,b in [(T,P),(G,P),(Q,Z),(K,Q),(W,Z)]:m.le(add(a,mul(b,-1)))
        if branch=='fwd':
            forms=[ [add(P,mul(Q,2)),add(Z,Q,K,mul(W,-1))],
                    [add(Q,mul(T,2)),add(mul(Z,2),mul(Q,-1)),add(Z,Q,W)],
                    [add(P,T,G),add(Z,mul(Q,2),mul(K,-2)),add(mul(P,2),mul(T,-1)),T] ]
        else:
            forms=[ [add(mul(P,2),Q),add(Z,Q,mul(W,-1))],
                    [add(T,mul(Q,2)),add(Z,mul(Q,2))],
                    [add(P,mul(T,2)),add(Z,Q,W,mul(K,-1))] ]
        for j,ff in enumerate(forms):
            for f in ff:m.le(add(f,mul(norms[(i+j)%3],-1)),name='norm')
    m.le(add(*norms,mul(den,-3)),name='norm budget');m.le(mul(den,-1),-1,'linear budget')
    if slope is not None:m.eq(den,slope,'slope cap')
    if size_equal is not None:m.eq(main[0][size_equal],1,'actual N')
    if symmetric:
        for i in (1,2):
            for a,b in zip(params[0],params[i]):m.eq(add(a,mul(b,-1)))
    return m

if __name__=='__main__':
    # Two known LP sanity checks.
    a=Model();a.le({'x':1,'y':1},3);a.le({'x':1},2)
    assert a.solve({'x':2,'y':1})[0]==5
    b=Model();b.le({'x':-1},-2);b.le({'x':1},3)
    assert b.solve({'x':1})[0]==3
    print('exact simplex sanity PASS',flush=True)
    for br in ('fwd','bwd'):
        ans=model(br).solve({'c':1,'m':-1})
        print('global',br,ans,flush=True)
    for kap in [F(1),F(21,20),F(11,10),F(23,20),F(6,5),F(5,4),F(13,10),F(7,5),F(3,2)]:
        out=[]
        for br in ('fwd','bwd'):
            relaxed=model(br,kap).solve({'c':1,'m':-1})
            exact=[model(br,kap,sz).solve({'c':1,'m':-1}) for sz in range(3)]
            best=max((x[0] for x in exact if x is not None),default=None)
            out.append((br,relaxed[0] if relaxed else None,best))
            if kap==1:
                for sz,ans in enumerate(exact):print('slope1 exact',br,'size',sz,ans,flush=True)
        print('slope',kap,'branch/relaxed/exact',out,flush=True)
