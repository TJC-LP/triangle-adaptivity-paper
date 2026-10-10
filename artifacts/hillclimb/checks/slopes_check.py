"""Exact checks: real-slope extension of F_{i,j} (floor parameters), D-family formulas,
sorted-model helper inequalities. python3 -I, integers/Fractions only."""
from fractions import Fraction as Fr
from math import isqrt

# ---- F_{i,j}(u) three-rotation union, closed forms (paper Thm 5.9 / referee 2.5)
def F(i, j, u):
    N = 3 * (u**(8*i) + u**(8*i-j) + u**(8*i-2*j) + u**(8*i-3*j))
    C = u**(12*i-3*j) + u**(8*i) + u**(8*i-2*j) + u**(8*i-3*j)
    fw = 3 * u**(12*i-4*j) + u**(8*i); rv = 3 * u**(12*i-2*j) + u**(12*i-5*j)
    assert rv > fw
    return N, fw, C   # B2 = fw exactly (all three forward sums equal)

assert F(1, 1, 2) == (1440, 1024, 864) and F(1, 1, 3) == (29160, 26244, 27216)
assert F(2, 1, 2) == (368640, 3211264, 2187264) and F(2, 2, 2) == (261120, 262144, 332800)

# Uniform constants for every i >= j >= 1, u = 2:  3*2^{8i} <= N <= 12*2^{8i};
# 3*2^{12i-4j} <= B2 <= 4*2^{12i-4j};  C >= 2^{12i-3j};  C^8 * 12^3 * 4^6 >= N^3 * B2^6.
for i in range(1, 41):
    for j in range(1, i + 1):
        N, B2, C = F(i, j, 2)
        assert 3 * 2**(8*i) <= N <= 12 * 2**(8*i)
        assert 3 * 2**(12*i-4*j) <= B2 <= 4 * 2**(12*i-4*j)
        assert C >= 2**(12*i-3*j) and C <= 4 * 2**(12*i-3*j)
        assert C**8 * 12**3 * 4**6 >= N**3 * B2**6      # C >= N^{3/8} B2^{3/4} / (12^{3/8} 4^{3/4})
print("F_{i,j}: uniform constants hold for 1 <= j <= i <= 40")

# kappa = sqrt 2: theta = 3 - 2 sqrt 2, j_n = floor(theta n) = 3n - isqrt(8 n^2) - 1 (sqrt(8) n irrational)
rows = []
for n in range(1, 200):
    j = 3*n - isqrt(8*n*n) - 1
    if j < 1: continue
    # floor check: j <= (3 - 2 sqrt2) n < j + 1  <=>  (3n - j)^2 >= 8n^2 > (3n - j - 1)^2
    assert (3*n - j)**2 > 8*n*n > (3*n - j - 1)**2
    N, B2, C = F(n, j, 2)
    # B2 / 2^{8 kappa n} in [3, 64):  2^{12n-4j} >= 2^{8 sqrt2 n}  <=> 12n-4j >= 8 sqrt2 n <=> (12n - 4j)^2 >= 128 n^2 (both >= 0)
    assert (12*n - 4*j)**2 >= 128*n*n and (12*n - 4*j - 4)**2 < 128*n*n
    rows.append((n, j))
print("kappa = sqrt2: first (n, j_n):", rows[:6], "... and (20,%d), (40,%d)" % (dict(rows)[20], dict(rows)[40]))

# ---- D(L,a,h) family (P2.3-P2.6), closed forms from the report, at u = 2
def Dfam(u, p, q):
    assert 9*q <= 10*p and p <= q
    a_ = 4 * u**(8*q); b_ = 4 * u**(8*p); g_ = 4 * u**(16*p - 8*q)
    ap = 2*u**(12*p-2*q) + u**(9*p-2*q) + u**(6*p+4*q)
    bp = u**(9*q-2*p) + 2*u**(4*p+6*q) + u**(12*q-2*p)
    gp = 2*u**(20*p-10*q) + u**(14*p-7*q) + u**(14*p-4*q)
    assert ap >= a_ and bp >= b_ and gp >= g_
    Cx = u**(10*p-q) + u**(4*p+2*q) + u**(16*p-8*q) + u**(3*p+2*q)
    Cy = u**(10*p-q) + u**(4*p+2*q) + u**(8*q) + u**(2*p+3*q)
    Cz = u**(7*p+2*q) + u**(10*p-4*q) + u**(8*p) + u**(10*p-5*q)
    C = min(Cx, Cy, Cz); assert C == Cx
    N = (2*u**(4*p+2*q) + u**(2*p+3*q) + u**(8*p) + u**(14*p-7*q) + u**(10*p-5*q) + u**(16*p-8*q)
         + u**(6*p+q) + u**(10*p-4*q) + u**(3*p+2*q) + u**(8*q) + u**(p+6*q))
    assert u**(8*q) <= N <= 12 * u**(8*q) and u**(10*p-q) <= C <= 4 * u**(10*p-q)
    return N, b_, C   # B2 = 4 u^{8p}

N, B2, C = Dfam(2, 9, 10)
assert (N, B2, C) == (1214275593117998941995008, 18889465931478580854784, 1208944338557034410541056)
assert Fr(C, N + B2) == Fr(1099528470656, 1121557087617)
N, B2, C = Dfam(2, 10, 11); assert Fr(C, N + B2) == Fr(17592320393344, 8970241051009)
N, B2, C = Dfam(2, 19, 20); assert Fr(C, N + B2) == Fr(1208925837629027751297152, 1203668645819051934081)
for (p, q) in [(9, 10), (11, 12), (14, 15), (19, 20), (39, 40), (1, 1)]:
    Dfam(2, p, q); Dfam(3, p, q)
print("D family: report values reproduced; bounds (15) hold")

# P2.1 constant: C <= (1 + 3^{1/8}) N when B2 <= N^{9/10}:  3^{1/8} < 1.15 since 1.15^8 > 3
assert Fr(115, 100)**8 > 3
# P2.9 / P2.12 maxima: v^{3/5}/(1+v) max at v = 3/2; v^{3/4}/(1+v) max at v = 3 (derivative zero: 3/5(1+v) = v; 3/4(1+v) = v)
assert Fr(3, 5) * (1 + Fr(3, 2)) == Fr(3, 2) and Fr(3, 4) * (1 + 3) == 3
# GMIN ratio and GMR ratio
for m in range(2, 13):
    assert Fr(m**6, 3*(m**5+m**4+m**3) + 3*m**5) == Fr(m**3, 6*m*m + 3*m + 3)
    assert Fr(m**5, 2*m**4 + m*m + m**4) == Fr(m**3, 3*m*m + 1)
    assert 2*m**7 + m**4 - 3*m**5 == m**4 * (m - 1) * (2*m*m + 2*m - 1)
print("best-of-six / single-GAO ratios OK")

# ---- sorted model helpers (P1.7)
def h(p, q):
    if p == 0 or q == 0: return 0
    s, l = min(p, q), max(p, q)
    return s * (1 + ((l - 1) // s).bit_length())
for s in range(1, 300):
    for l in range(s, 2000):
        k = ((l - 1) // s).bit_length()
        assert (2**k * s >= l) and (k == 0 or 2**(k - 1) * s < l)        # k = ceil(log2(l/s))
        assert h(s, l)**2 <= 9 * s * l                                  # h <= 3 sqrt(pq)
for k in range(1, 200):
    assert (k + 1)**2 <= 9 * 2**(k - 1)
print("sorted-model price identities OK")

# P1.21 Markov/union-bound arithmetic: log2(6na) < 3 + 8iL <= 16 iL <= D = pL/2, for the smallest member (i=j=1,h=1)
for (i, j, hh) in [(1, 1, 1), (1, 1, 2), (2, 1, 1), (2, 2, 1), (3, 1, 1)]:
    M = 2**hh; L = M**4; ulog = L       # u = 2^L, keep exponents in log2
    n_l = 4*i*L - 4*hh; a_l = (4*i - 2*j)*L + 2*hh; p_l = (4*i - j)*L - hh
    assert 3 + n_l + a_l < 3 + 8*i*L     # log2(6na) = log2 6 + n_l + a_l < 3 + 8iL
    assert p_l >= 2*i*L and 2**(2*i*L) >= 32*i   # p >= u^{2i} >= 32 i
    D_l = None  # D = pL/2 >= 16 i L since p >= 32 i
print("randomized-variant arithmetic OK")
