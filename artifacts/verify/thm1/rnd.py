# Random checks: Theorem A (per-root + global), (Lam Lam')^{1/3} bound, M_E <= 2 sqrt(RST), Prop 3 scheduler.
import sys,os,random,math; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ev import ev
def terms(e):
    a,ap,b,bp,c,cp=e['deg']; Rf,Sf,Tf,Rb,Sb,Tb=e['Rf'],e['Sf'],e['Tf'],e['Rb'],e['Sb'],e['Tb']
    tx={x:([1+min(cp[x],b[y]) for y in Rf.get(x,())],[1+min(a[x],bp[z]) for z in Tf.get(x,())]) for x in set(Rf)|set(Tf)}
    ty={y:([1+min(b[y],cp[x]) for x in Rb.get(y,())],[1+min(ap[y],c[z]) for z in Sf.get(y,())]) for y in set(Rb)|set(Sf)}
    tz={z:([1+min(c[z],ap[y]) for y in Sb.get(z,())],[1+min(bp[z],a[x]) for x in Tb.get(z,())]) for z in set(Sb)|set(Tb)}
    return [tx,ty,tz]
class Pass:
    def __init__(s,T): s.vs=list(T.values()); s.k=0; s.done=0; s.steps=0; s.new()
    def new(s):
        s.steps+=3  # vertex transition + two root-degree reads
        s.p=[0,0]; s.i=[0,0]
    def L(s): return s.done+(min(s.p) if s.k<len(s.vs) else 0)
    def fin(s): return s.k>=len(s.vs)
    def step(s):
        L1,L2=s.vs[s.k]; side=0 if s.p[0]<=s.p[1] else 1; lst=(L1,L2)[side]
        if s.i[side]==len(lst):
            s.done+=s.p[side]; s.k+=1
            if not s.fin(): s.new()
            return
        s.p[side]+=lst[s.i[side]]; s.i[side]+=1; s.steps+=1
def schedule(e):
    P=[Pass(T) for T in terms(e)]
    while True:
        r=min(range(3),key=lambda i:(P[i].L(),not P[i].fin()))
        if P[r].fin(): return r,P
        P[r].step()
random.seed(int(sys.argv[1])); n_inst=int(sys.argv[2]); worst={'A':0,'root':0,'LL':0,'M':0,'P3':0}
def gen():
    n=random.choice([5,10,20,40,80]); out=[]
    for _ in range(3):
        mode=random.choice(['unif','pow','block','star'])
        m=random.randint(1,4*n*random.choice([1,2,4]))
        if mode=='unif': E={(random.randrange(n),random.randrange(n)) for _ in range(m)}
        elif mode=='pow':
            al=random.choice([0.5,1,1.5,2]); w=[(i+1)**-al for i in range(n)]
            E={(random.choices(range(n),w)[0],random.choices(range(n),w)[0] if random.random()<.5 else random.randrange(n)) for _ in range(m)}
        elif mode=='block':
            E=set()
            for _ in range(random.randint(1,4)):
                p,q=random.randint(1,n),random.randint(1,n); u,v=random.randrange(n),random.randrange(n)
                E|={((u+i)%n,(v+j)%n) for i in range(p) for j in range(q) if random.random()<random.choice([1,.5,.1])}
        else:
            h=random.randrange(n); E={(h,random.randrange(n)) for _ in range(m//2)}|{(random.randrange(n),h) for _ in range(m//2)}
        out.append(E or {(0,0)})
    return out
for it in range(n_inst):
    R,S,T=gen(); e=ev(R,S,T); N=e['N']; RST=e['R']*e['S']*e['T']
    al,be,ga,alp,bep,gap=e['al'],e['be'],e['ga'],e['alp'],e['bep'],e['gap']
    # per-root bounds, forward and reflected, in exact 8th-power integer form
    H={'x':e['Ax']-e['R']-e['T'],'y':e['Ay']-e['R']-e['S'],'z':e['Az']-e['S']-e['T']}
    fw={'x':al**2*be*ga**3*e['S']**3,'y':be**2*ga*al**3*e['T']**3,'z':ga**2*al*be**3*e['R']**3}
    rv={'x':gap**2*bep*alp**3*e['S']**3,'y':alp**2*gap*bep**3*e['T']**3,'z':bep**2*alp*gap**3*e['R']**3}
    for r in 'xyz':
        if H[r]>0:
            assert H[r]**8<=fw[r] and H[r]**8<=rv[r],(r,H[r],fw[r],rv[r])
            worst['root']=max(worst['root'],H[r]/min(fw[r],rv[r])**(1/8))
    hA=e['A']-N
    if hA>0:
        assert hA**8<=RST*min(al*be*ga,alp*bep*gap)**2
        worst['A']=max(worst['A'],hA/(RST**(1/8)*min(al*be*ga,alp*bep*gap)**0.25))
    mM=min(e['MR'],e['MS'],e['MT'])
    assert mM**6<=al*be*ga*alp*bep*gap; worst['LL']=max(worst['LL'],mM/(al*be*ga*alp*bep*gap)**(1/6) if mM else 0)
    for M in (e['MR'],e['MS'],e['MT']): assert M*M<=4*RST; worst['M']=max(worst['M'],M/(2*math.sqrt(RST)))
    r,P=schedule(e); A=e['A']
    assert [e['Ax'],e['Ay'],e['Az']][r]==A
    nv=sum(len(p.vs) for p in P); tot=sum(p.steps for p in P)
    assert tot<=6*A+4*nv+6,(tot,A,nv)
    worst['P3']=max(worst['P3'],(tot-4*nv)/(A or 1))
print(n_inst,'instances OK; worst ratios',{k:round(v,3) for k,v in worst.items()})
