import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sys
from ev import ev,B2,Q,rotate,biregular
def V(tag,n,k): return [(tag,n,i) for i in range(k)]
def G8(m,tag):
    X=V(tag,'x',m**4); Y0=V(tag,'y0',m**2); Y2=V(tag,'y2',m**8); Z0=V(tag,'z0',m**8); Z1=V(tag,'z1',m**3); Z2=V(tag,'z2',m**6)
    R={(x,y) for x in X for y in Y0}
    T=biregular(X,Z0,m**4)|biregular(X,Z2,m**3)
    S={(y,z) for y in Y0 for z in Z1}|biregular(Y2,Z2,1)
    return R,S,T
def union3(f,m):
    R0,S0,T0=f(m,0); R1,S1,T1=rotate(*f(m,1)); R2,S2,T2=rotate(*rotate(*f(m,2)))
    return R0|R1|R2,S0|S1|S2,T0|T1|T2
def Fij(i,j):
    def f(u,tag):
        X=V(tag,'x',u**(4*i)); Y0=V(tag,'y0',u**(4*i-2*j)); Y2=V(tag,'y2',u**(8*i)); Z1=V(tag,'z1',u**(4*i-j)); Z2=V(tag,'z2',u**(4*i+2*j))
        R={(x,y) for x in X for y in Y0}; S={(y,z) for y in Y0 for z in Z1}|biregular(Y2,Z2,1); T=biregular(X,Z2,u**(4*i-j))
        return R,S,T
    return f
which=sys.argv[1]
if which=='G8':
    for m in map(int,sys.argv[2:]):
        g=ev(*G8(m,0)); e=ev(*union3(G8,m))
        assert g['Ax']==m**9+m**6 and g['Ay']==m**5 and g['Az']==m**8, (g['Ax'],g['Ay'],g['Az'])
        assert g['al']==m**8 and g['be']==2*m**8 and g['ga']==2*m**8
        assert e['Ax']==e['Ay']==e['Az']==m**9+m**8+m**6+m**5
        assert e['N']==3*(2*m**8+m**7+m**6+m**5) and e['al']==e['be']==e['ga']==5*m**8
        assert e['alp']*e['bep']*e['gap']>=e['al']*e['be']*e['ga']
        b=B2(e); ub=e['N']+(e['R']*e['S']*e['T'])**(1/8)*b**0.75
        print(f"G8 m={m} single:Ax={g['Ax']} Ay={g['Ay']} Az={g['Az']} N={g['N']}  union: A={e['A']} N={e['N']} B2={b:.0f} A/(N+B2)={e['A']/(e['N']+b):.3f} A/ThmA={e['A']/ub:.3f} minM={min(e['MR'],e['MS'],e['MT'])}")
elif which=='F':
    i,j=int(sys.argv[2]),int(sys.argv[3])
    for u in map(int,sys.argv[4:]):
        e=ev(*union3(Fij(i,j),u)); b=B2(e)
        assert e['A']>=u**(12*i-3*j) and e['N']<=12*u**(8*i) and b<=4*u**(12*i-4*j)*1.0000001
        print(f"F({i},{j}) u={u} A={e['A']} N={e['N']} B2={b:.0f} A/(N+B2)={e['A']/(e['N']+b):.3f} A/(N^3/8 B2^3/4)={e['A']/(e['N']**.375*b**.75):.3f}")
