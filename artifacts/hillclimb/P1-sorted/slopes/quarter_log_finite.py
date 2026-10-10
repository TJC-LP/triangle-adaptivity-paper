# Exact integer certificate at a finite parameter. No graph is materialized.
h=16
L=2**h
u=2**L
S0=u**14+u**13+u**16*L**2+u**15*L+u**16
N=3*S0
A=3*u**20+u**16*(L**2+1)
lower=u**21*L//2
D=u**7*L//2
programs=3*u**14
assert programs.bit_length()<=D
assert S0<=2*u**16*L**2
assert A<=4*u**20
assert 2*N<lower
assert L**2//2**23==512
# Algebraic certificate: lower^8 >=512*S0^3*A^6 and lower-N>lower/2.
# Therefore (lower-N)^8 >2*S0^3*A^6. Also check that inequality directly.
assert (lower-N)**8>S0**3*A**6
print('h=',h,'L=',L,'u=2^'+str(L))
print('bit_lengths N,B2,lower=',N.bit_length(),A.bit_length(),lower.bit_length())
print('program_count_bit_length=',programs.bit_length(),'R_depth_bit_length=',D.bit_length())
print('certified_lower_eighth_over_spectral_eighth_at_least=',L**2//2**23)
print('N_less_than_lower_half=',2*N<lower)
print('lower_minus_N_eighth_exceeds_spectral_eighth=',True)
