# All load-bearing checks use exact integers. No enormous graph is materialized.
from fractions import Fraction

def evaluate(i,j,h):
    M=2**h; L=M**4; u=2**L
    n=u**(4*i)//M**4
    a=u**(4*i-2*j)*M**2
    p=u**(4*i-j)//M
    q=u**(4*i)*M**4
    k=p*L
    d=u**(4*i-3*j)*M
    c=u**(4*i+2*j)//M**2
    assert n*M**4==u**(4*i) and p*M==u**(4*i-j)
    assert c*M**2==u**(4*i+2*j)
    assert n%d==0 and c%k==0 and n//d==c//k
    assert c*d==n*k and c*a==n*q==u**(8*i)
    R=n*a; S=a*p+c*a; T=c*d+n*q
    N=3*(R+S+T)
    alpha=n*a*a
    beta=a*p*p+c*a
    gamma=c*d*d+n*q
    A=alpha+beta+gamma
    assert alpha==u**(12*i-4*j)
    assert beta==gamma==alpha+u**(8*i)
    assert A==3*u**(12*i-4*j)+2*u**(8*i)
    Ar=a*n*n+p*a*a+c*a*a+n*(q+k)**2
    Ar_closed=(u**(12*i)*M**4+2*u**(12*i-j)*M**3
               +2*u**(12*i-2*j)*M**2+u**(12*i-2*j)//M**6
               +u**(12*i-5*j)*M**3)
    assert Ar==Ar_closed and Ar>A
    D=p*L//2
    lower=n*a*D
    assert lower==u**(12*i-3*j)*M//2
    programs=3*n*a
    assert programs.bit_length()<=D
    assert 6*u**(8*i)<=N<=15*u**(8*i)
    assert 3*u**(12*i-4*j)<=A<=5*u**(12*i-4*j)
    assert q>=u*p
    return M,L,u,N,A,Ar,lower,D,programs.bit_length()

for i,j,h in [(1,1,1),(2,1,1),(2,2,1)]:
    M,L,u,N,A,Ar,lower,D,pbits=evaluate(i,j,h)
    print('parameters i,j,h=',i,j,h,'M,L,u=',M,L,u)
    print('N=',N,'B2=',A,'reverse=',Ar)
    print('comparison_lower=',lower,'per_call_depth=',D,'program_count_bit_length=',pbits)
    print('kappa=',Fraction(3,2)-Fraction(j,2*i),'polynomial_exponent=',Fraction(3,2)-Fraction(3*j,8*i))

# Larger parameters are checked exactly and summarized without giant decimals.
for i,j,h in [(1,1,2),(2,1,2),(1,1,3)]:
    M,L,u,N,A,Ar,lower,D,pbits=evaluate(i,j,h)
    print('parameters i,j,h=',i,j,h,'M,L=',M,L,
          'bit_lengths N,B2,lower=',N.bit_length(),A.bit_length(),lower.bit_length(),
          'program_count_bit_length=',pbits,'per_call_depth_bit_length=',D.bit_length())
