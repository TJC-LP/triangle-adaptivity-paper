"""Self-test of the exact eigenvalue bracket against numpy on random 0/1 matrices (floats only as a sanity
cross-check; the bracket itself is exact)."""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import numpy as np
from v2lib import gram_small, lambda_max_bracket, charpoly, poly_eval, simplex_max

rng = random.Random(5)
worst = 0.0
nint = 0
for t in range(600):
    a, b = rng.randint(1, 8), rng.randint(1, 8)
    p = rng.random()
    A = [[1 if rng.random() < p else 0 for _ in range(b)] for _ in range(a)]
    if sum(map(sum, A)) == 0:
        continue
    G = gram_small(A)
    lo, hi, ex = lambda_max_bracket(G, 60)
    lam = float(np.linalg.eigvalsh(np.array(G, dtype=float)).max())
    assert float(lo) - 1e-7 <= lam <= float(hi) + 1e-7, (A, lo, hi, lam)
    assert hi - lo <= F(max(sum(r) for r in G) + 1) / 2 ** 59
    if ex:
        nint += 1
        assert poly_eval(charpoly(G), lo) == 0
    worst = max(worst, abs(lam - float(lo)))
print(f"600 random matrices: exact bracket always contains numpy's lambda_max (max |lam - lo| = {worst:.2e}); {nint} integer roots pinned exactly")

# simplex smoke tests
x, v = simplex_max([1, 1], [[1, 2], [3, 1]], [4, 6])
assert v == F(14, 5) and x == [F(8, 5), F(6, 5)], (x, v)
x, v = simplex_max([3, 2, 1], [[1, 1, 1], [2, 0, 1]], [5, 4])
# brute-force check on a grid of vertices: max 3a+2b+c s.t. a+b+c<=5, 2a+c<=4 -> a=2,b=3,c=0 -> 12
assert v == 12, (x, v)
print("simplex smoke tests passed")
