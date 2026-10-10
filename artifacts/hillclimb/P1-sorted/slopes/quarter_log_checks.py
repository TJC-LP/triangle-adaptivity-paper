from fractions import Fraction
from math import comb

def fields(h):
    L=2**h
    u=2**L
    n=u**8; a=u**6; p=u**7; q=u**8
    k=p*L; d=u**5//L; c=u**10*L**2
    assert d*L==u**5 and c*d==n*k
    assert c*a==u**16*L**2
    S0=u**14+u**13+u**16*L**2+u**15*L+u**16
    N=3*S0
    A=3*u**20+u**16*(L**2+1)
    Ar=u**24+2*u**23*L+u**22*(1+2*L**2)+u**19
    lower=u**21*L//2
    depth=p*L//2
    programs=3*u**14
    # Avoid constructing 2**depth: bit lengths certify programs<2**depth.
    assert programs.bit_length()<=depth
    assert Ar>A and 3*u**16*L**2<=N<=15*u**16*L**2
    assert A<=4*u**20
    assert N.bit_length()<=20*L
    # Exact eighth-power ratio to the spectral monomial S0^(3/8)*A^(3/4).
    ratio8=Fraction(lower**8,S0**3*A**6)
    return L,u,N,A,Ar,lower,depth,programs.bit_length(),ratio8

for h in (1,2,3):
    L,u,N,A,Ar,lower,depth,prog_bits,ratio8=fields(h)
    print('h=',h,'L=',L,'u=',u)
    print('N=',N,'B2=',A,'reverse=',Ar)
    print('comparison_lower=',lower,'R_call_depth_lower=',depth,'program_count_bit_length=',prog_bits)
    print('lower_eighth_over_spectral_eighth=',ratio8)

# Finite exact certificate count for a small analogue, unrelated to huge graphs.
for p,q in [(2,4),(3,9),(4,16),(8,64)]:
    M=comb(p+q,p)
    assert M*p**p>=q**p
    print('shuffle_count',p,q,M,'elementary_lower',Fraction(q,p)**p)
