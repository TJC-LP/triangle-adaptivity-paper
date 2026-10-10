"""Shared helpers for 4-cycle instances: exact Out, sizes, rigorous rational bounds on sigma^2.

Instance = (AR, AS, AT, AQ) as lists of lists of 0/1 ints with shapes
  AR: X x Y, AS: Y x Z, AT: Z x W, AQ: W x X.
Out = tr(AR AS AT AQ).
"""
from fractions import Fraction


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0]) if B else 0
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        oi = out[i]
        for t in range(k):
            a = Ai[t]
            if a:
                Bt = B[t]
                for j in range(m):
                    oi[j] += a * Bt[j]
    return out


def transpose(A):
    return [list(col) for col in zip(*A)] if A else []


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def out4(AR, AS, AT, AQ):
    return trace(matmul(matmul(AR, AS), matmul(AT, AQ)))


def size(A):
    return sum(map(sum, A))


def gram(A):
    """A^T A as integer matrix."""
    return matmul(transpose(A), A)


def sigma2_upper(A, iters=30):
    """Rigorous rational upper bound on ||A||_2^2 via Collatz-Wielandt on G = A^T A:
    for any positive vector v, lambda_max(G) <= max_i (Gv)_i / v_i.  Also min(max row sum of G).
    G is nonnegative; if G is reducible the CW bound still holds (it is an upper bound for any
    positive v because lambda_max <= ||G||_{v-weighted inf-norm}).  Returns a Fraction."""
    G = gram(A)
    n = len(G)
    if n == 0:
        return Fraction(0)
    best = Fraction(max(sum(row) for row in G))  # row-sum bound
    # power iterate from all-ones with +1 smoothing (keeps v positive); integer arithmetic
    v = [1] * n
    for _ in range(iters):
        w = [sum(G[i][j] * v[j] for j in range(n)) + 1 for i in range(n)]  # +1 keeps positivity
        # normalise to avoid blow-up: divide by gcd-ish (keep integers by scaling down)
        mx = max(w)
        if mx > 10 ** 30:
            w = [max(1, x // (mx // 10 ** 12)) for x in w]
        v = w
        cw = max(Fraction(sum(G[i][j] * v[j] for j in range(n)), v[i]) for i in range(n))
        if cw < best:
            best = cw
    return best


def _rayleigh_power(G, iters):
    """Largest Rayleigh quotient of the symmetric nonnegative integer matrix G along integer power
    iterates started from 1, from each unit vector's neighbourhood, and the diagonal.  Exact Fractions."""
    n = len(G)
    best = Fraction(0)
    if n == 0:
        return best
    starts = [[1] * n]
    for j in range(n):
        if G[j][j] > best:
            best = Fraction(G[j][j])
        starts.append([G[i][j] for i in range(n)])  # column j of G as a start vector
    for v in starts:
        for _ in range(iters):
            den = sum(x * x for x in v)
            if den == 0:
                break
            num = sum(v[i] * G[i][j] * v[j] for i in range(n) for j in range(n))
            rq = Fraction(num, den)
            if rq > best:
                best = rq
            w = [sum(G[i][j] * v[j] for j in range(n)) for i in range(n)]
            mx = max(w)
            if mx == 0:
                break
            if mx > 10 ** 40:
                w = [x // (mx // 10 ** 20) for x in w]
            v = w
    return best


def sigma2_lower(A, iters=30):
    """Rigorous rational lower bound on ||A||_2^2: Rayleigh quotients of A^T A and of A A^T at exact
    integer vectors (power iterates, columns of the Gram matrices, unit vectors).  Row and column
    degrees are included through the diagonals (||A||^2 >= max degree)."""
    if not A or not A[0]:
        return Fraction(0)
    G1 = gram(A)                 # A^T A
    G2 = matmul(A, transpose(A))  # A A^T
    return max(_rayleigh_power(G1, iters), _rayleigh_power(G2, iters))


def stats_bounds(AR, AS, AT, AQ, iters=30):
    """Return (r, s_lo, s_hi): sizes, rigorous lower and upper bounds on s_e = min(sigma_e^2, r_e)."""
    mats = (AR, AS, AT, AQ)
    r = [size(A) for A in mats]
    s_lo = [min(sigma2_lower(A, iters), Fraction(re)) for A, re in zip(mats, r)]
    s_hi = [min(sigma2_upper(A, iters), Fraction(re)) for A, re in zip(mats, r)]
    return r, s_lo, s_hi


def mono_pow(r, s, lam, mu, denom):
    """prod r_e^(lam_e) s_e^(mu_e) where lam, mu are integers over common denominator `denom`
    -> returns the exact value of (monomial)^denom as a Fraction."""
    val = Fraction(1)
    for e in range(4):
        val *= Fraction(r[e]) ** lam[e] * Fraction(s[e]) ** mu[e]
    return val


def kron(A, B):
    """Kronecker product of 0/1 matrices."""
    n, m = len(A), len(A[0])
    p, q = len(B), len(B[0])
    out = [[0] * (m * q) for _ in range(n * p)]
    for i in range(n):
        for j in range(m):
            if A[i][j]:
                for k in range(p):
                    for l in range(q):
                        if B[k][l]:
                            out[i * p + k][j * q + l] = 1
    return out


def ones(n, m):
    return [[1] * m for _ in range(n)]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def arc_instance(n):
    """Arc-blowup instance from a dict n: arc(frozenset) -> multiplicity.
    Vertices 0=X,1=Y,2=Z,3=W; edges R=(0,1), S=(1,2), T=(2,3), Q=(3,0).
    Returns (AR, AS, AT, AQ)."""
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    mats = []
    for (u, v) in edges:
        M = [[1]]
        for arc, mult in n.items():
            if mult <= 1:
                continue
            inu, inv = u in arc, v in arc
            if inu and inv:
                M = kron(M, eye(mult))
            elif inu:
                M = kron(M, ones(mult, 1))
            elif inv:
                M = kron(M, ones(1, mult))
        mats.append(M)
    # shapes must be consistent: rows of edge (u,v) index vertex u = prod_{A∋u} n_A ; we built in
    # dict order for every edge, so the index sets agree.
    return tuple(mats)


def all_arcs(k=4):
    out = []
    for length in range(1, k):
        for start in range(k):
            out.append(frozenset((start + i) % k for i in range(length)))
    out.append(frozenset(range(k)))
    return out
