import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ev import ev,B2,Q,rotate,biregular
def V(t,n,k): return [(t,n,i) for i in range(k)]
def comp(A,B): return {(u,v) for u in A for v in B}
def fam2a(a):
    X=V(0,'x',a);Y=V(0,'y',a);Z=[(0,'z',i,k) for i in range(a) for k in range(a)]
    return comp(X,Y),{(Y[i],(0,'z',i,k)) for i in range(a) for k in range(a)},{(X[i],(0,'z',i,k)) for i in range(a) for k in range(a)}
def GMIN(m):
    x0,x1,x2,x3=V(0,'x0',m**3),V(0,'x1',m**5),V(0,'x2',m**2),V(0,'x3',m)
    y0,y1,y2,y3=V(0,'y0',m),V(0,'y1',m**3),V(0,'y2',m**2),V(0,'y3',m**5)
    z0,z1,z2,z3=V(0,'z0',m**5),V(0,'z1',m**2),V(0,'z2',m),V(0,'z3',m**3)
    R=comp(x0,y0)|biregular(x1,y1,1)|comp(x3,y2)
    S=comp(y0,z1)|comp(y1,z2)|biregular(y3,z3,1)
    T=biregular(x0,z0,m**2)|comp(x2,z2)|comp(x3,z3)
    return R,S,T
def GMR(m):
    X,Y,Z0,Z1=V(0,'x',m**3),V(0,'y',m),V(0,'z0',m**4),V(0,'z1',m)
    return comp(X,Y),comp(Y,Z1),biregular(X,Z0,m)
def pad(R,S,T):
    R,S,T=set(R),set(S),set(T);k=[0]
    def f(): k[0]+=1; return ('pad',k[0])
    Xr={x for x,_ in R};Xt={x for x,_ in T};Yr={y for _,y in R};Ys={y for y,_ in S};Zs={z for _,z in S};Zt={z for _,z in T}
    for x in Xr^Xt: y,z=f(),f(); R.add((x,y));T.add((x,z));S.add((y,z))
    for y in Yr^Ys: x,z=f(),f(); R.add((x,y));S.add((y,z));T.add((x,z))
    for z in Zs^Zt: x,y=f(),f(); S.add((y,z));T.add((x,z));R.add((x,y))
    return R,S,T
def ferrers(m):
    r=[(0,0,0),(0,0,1),(0,1,1)]; s=[(0,0,0),(0,1,1),(0,0,1)]; t=[(0,0,0),(1,1,0),(1,0,0)]
    bl=lambda B,p,q:{((p,i,u),(q,j,v)) for i in range(3) for j in range(3) if B[i][j] for u in range(m) for v in range(m)}
    return bl(r,'x','y'),bl(s,'y','z'),bl(t,'x','z')
def rep(tag,e,q=True):
    b=B2(e);mM=min(e['MR'],e['MS'],e['MT'])
    print(f"{tag}: N={e['N']} B2={b:.0f} A={e['A']} (Ax,Ay,Az)=({e['Ax']},{e['Ay']},{e['Az']}) M=({e['MR']},{e['MS']},{e['MT']}) "
          f"A/(N+B2)={e['A']/(e['N']+b):.3f} minM/(N+B2)={mM/(e['N']+b):.3f} MR/(N+B2)={e['MR']/(e['N']+b):.3f}"+(f" Q={Q(e)}" if q else ""),flush=True)
w=sys.argv[1]; ms=list(map(int,sys.argv[2:]))
for m in ms:
    if w=='2a':
        e=ev(*fam2a(m)); rep(f'2a a={m}',e)
        assert e['MR']==m**3 and e['MS']==m*m and e['MT']==m*m and e['Ax']==2*m*m and Q(e)==m*m
        assert e['al']==e['be']==m**3 and e['ga']==m**2
    if w=='min':
        e=ev(*GMIN(m)); rep(f'GMIN m={m}',e)
        assert e['MR']==e['MS']==e['MT']==m**6 and e['Ax']==e['Ay']==e['Az']==m**5+m**3
        assert e['N']==3*(m**5+m**4+m**3) and e['al']==e['be']==e['ga']==3*m**5
        rep(f'GMIN m={m} padded',ev(*pad(*GMIN(m))))
    if w=='mr':
        e=ev(*GMR(m)); rep(f'GMR m={m}',e)
        assert e['MR']==m**5 and e['MS']==0 and e['MT']==0 and e['Ax']==m**4 and e['al']==m**5 and e['be']==m**3 and e['ga']==m**4
        rep(f'GMR m={m} padded',ev(*pad(*GMR(m))))
    if w=='G8pad':
        from fams import union3,G8
    if w=='fer':
        e=ev(*ferrers(m)); rep(f'Ferrers m={m}',e)
