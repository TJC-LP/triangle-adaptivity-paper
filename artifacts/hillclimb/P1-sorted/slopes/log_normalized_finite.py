# Direct exact finite check at the slope B2=Theta(N), using integers only.
M=16
L=M**4
u=2**L
S0=2*u**8+u**7//M+u**6//M**2+M*u**5
N=3*S0
B2=5*u**8
lower=M*u**9//2
D=u**3*M**3//2
programs=3*u**6//M**2
assert programs.bit_length()<D
assert (lower-N)**8>S0**3*B2**6
print('i=j=1 h=4 M=16 L=65536 u=2^65536')
print('N=3*(2^524289+2^458748+2^393208+2^327684)')
print('B2=5*2^524288 lower=2^589827 D=2^196619 programs=3*2^393208')
print('bit_lengths N,B2,lower=',N.bit_length(),B2.bit_length(),lower.bit_length())
print('program_count_bit_length=',programs.bit_length(),'per_call_depth_bit_length=',D.bit_length())
print('lower_minus_N_eighth_exceeds_spectral_eighth=',True)
