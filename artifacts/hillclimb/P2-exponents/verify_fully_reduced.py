"""Exact literal enumeration of a fully reduced coordinate construction."""
from fractions import Fraction

def instance(t):
 x=t**6; y0=t**4; y=y0+t**10; z1=t**5; z=z1+t**8
 R=[set() for _ in range(x)]; Ri=[set() for _ in range(y)]
 S=[set() for _ in range(y)]; Si=[set() for _ in range(z)]
 T=[set() for _ in range(z)]; Ti=[set() for _ in range(x)]
 def edge(F,B,a,b): F[a].add(b);B[b].add(a)
 for i in range(x):
  for j in range(y0):edge(R,Ri,i,j)
  edge(T,Ti,i//t,i)
 for j in range(y0):
  for k in range(z1):edge(S,Si,j,k)
 for A in range(t**3):
  for B in range(t**3):
   i=A*t**3+B
   for D in range(t**3):
    for E in range(t):
     j=y0+((A*t**3+B)*t**3+D)*t+E
     edge(R,Ri,i,j)
     for F in range(t**2):
      k=z1+(A*t**3+D)*t**2+F
      edge(S,Si,j,k)
  for D in range(t**3):
   for F in range(t**2):
    k=z1+(A*t**3+D)*t**2+F
    for B in range(t**3):edge(T,Ti,k,A*t**3+B)
 sizes=[sum(map(len,E)) for E in (R,S,T)]
 forward=[sum(len(a)**2 for a in E) for E in (R,S,T)]
 reverse=[sum(len(a)**2 for a in E) for E in (Ri,Si,Ti)]
 out=0
 for i,adj in enumerate(R):
  for j in adj:
   n=len(S[j]&Ti[i]);assert n>0;out+=n
 for j,adj in enumerate(S):
  for k in adj:assert Ri[j]&T[k]
 for k,adj in enumerate(T):
  for i in adj:assert R[i]&Si[k]
 Cx=sum(min(sum(1+min(len(S[j]),len(Ti[i])) for j in R[i]),sum(1+min(len(R[i]),len(Si[k])) for k in Ti[i])) for i in range(x))
 Cy=sum(min(sum(1+min(len(S[j]),len(Ti[i])) for i in Ri[j]),sum(1+min(len(Ri[j]),len(T[k])) for k in S[j])) for j in range(y))
 Cz=sum(min(sum(1+min(len(Ri[j]),len(T[k])) for j in Si[k]),sum(1+min(len(R[i]),len(Si[k])) for i in T[k])) for k in range(z))
 assert sizes==[2*t**10,t**12+t**9,t**11+t**6]
 assert forward==[4*t**14,2*t**14,t**14+t**7]
 assert reverse==[t**16+t**10,t**16+t**13,t**16+2*t**11+t**6]
 assert (Cx,Cy,Cz)==(t**15+t**11+t**10+t**6,t**12+2*t**10+t**9,2*t**12+t**10+t**6)
 assert out==t**12+t**10
 N=3*sum(sizes);B2=min(sum(forward),sum(reverse));C=Cx+Cy+Cz
 print(dict(t=t,sizes=sizes,forward=forward,reverse=reverse,root_costs=[Cx,Cy,Cz],Out_one=out,N_union=N,B2_union=B2,C_union=C,Out_union=3*out,ratio=str(Fraction(C,N+B2))),flush=True)
for t in (1,2,3,4):instance(t)
