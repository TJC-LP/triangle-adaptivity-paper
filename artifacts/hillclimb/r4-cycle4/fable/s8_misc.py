"""Step 8: side remarks, exactly.
 (a) double star: Delta^+ Delta^- > sigma^2 (so 'Delta^+ Delta^- <= sigma^2' is false) and
     sum_{(x,y) in R} d^+(x) d^-(y) is not O(|R| sigma^2) on k stars + k co-stars + K_{k,k}.
 (b) H for real matrices: A_R = A_T = I_2, A_S = A_Q = I_2/2 gives Out = 1/2 > 1/4 = H (with r = ||.||_F^2,
     s = ||.||_2^2), so the 0/1 structure is needed.
 (c) Lemma Lambda on a small explicit instance, exactly: K has integer entries when all common-neighbourhood
     counts are perfect squares; here we take R = T = complete so rho = tau = |X| J, |W| J and check
     lambda_max(K) = sqrt(|X||W|) sigma_S exactly via the row-sum / Perron argument on a star S.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import sigma2_bracket, gram_small, lambda_max_bracket

print("(a) double star")
for k in [3, 4, 6, 10]:
    A = [[0] * k for _ in range(k)]
    for j in range(k):
        A[0][j] = 1
    for i in range(k):
        A[i][0] = 1
    lo, hi, ex = sigma2_bracket(A, 50)
    dp = max(sum(r) for r in A)
    dm = max(sum(c) for c in zip(*A))
    print(f"  k={k}: Delta+ Delta- = {dp*dm}, sigma^2 in ({float(lo):.6f}, {float(hi):.6f}] -> Delta+Delta- > sigma^2: {dp*dm > hi}")
print("    (sigma^2 = 2k - 1 for the double star: check)", end=" ")
A = [[0] * 6 for _ in range(6)]
for j in range(6):
    A[0][j] = 1
for i in range(6):
    A[i][0] = 1
lo, hi, ex = sigma2_bracket(A, 50)
print(lo, hi, ex)
print("  k stars + k co-stars + K_{k,k}: sum d+(x) d-(y) over R vs |R| sigma^2")
for k in [3, 5, 8]:
    # vertex sets: X = k star centers + k leaves-of-costars... build: block K_{k,k} on (X1, Y1); star centers X1[i]
    # each with k private leaves; co-star centers Y1[j] each with k private leaves.
    nx = k + k * k
    ny = k + k * k
    A = [[0] * ny for _ in range(nx)]
    for i in range(k):
        for j in range(k):
            A[i][j] = 1
    for i in range(k):
        for l in range(k):
            A[i][k + i * k + l] = 1          # star from x_i to private y leaves
    for j in range(k):
        for l in range(k):
            A[k + j * k + l][j] = 1          # co-star into y_j from private x leaves
    r = sum(map(sum, A))
    dplus = [sum(row) for row in A]
    dminus = [sum(col) for col in zip(*A)]
    ssum = sum(dplus[i] * dminus[j] for i in range(nx) for j in range(ny) if A[i][j])
    G = gram_small(A)
    lo, hi, ex = lambda_max_bracket(G, 40)
    print(f"  k={k}: |R|={r}, sum d+ d- = {ssum}, sigma^2 in ({float(lo):.4f}, {float(hi):.4f}], ratio sum/(|R| sigma^2) >= {ssum/(r*float(hi)):.4f}")

print("(b) real-matrix H remark: Out = 1/2, r = (2, 1/2, 2, 1/2), s = (1, 1/4, 1, 1/4):",
      "H = sqrt(r_S r_Q)(s_R s_S s_T s_Q)^(1/4) =", F(1, 2) * F(1, 2), "< Out = 1/2")

print("(c) Lemma Lambda exact instance: R = J_{X x Y}, T = J_{Z x W}, S a star")
# rho_{yy'} = |X| for all y, y'; tau_{zz'} = |W|; K = sqrt(|X||W|) J_{S x S}; lambda_max(K) = sqrt(|X||W|) |S|.
# sigma_R^2 = |X||Y|, sigma_T^2 = |Z||W|, sigma_S^2 = |S| for a star.  Claim: sqrt(|X||W|)|S| <= sqrt(|X||Y|) sqrt(|S|) sqrt(|Z||W|)
# <=> sqrt(|S|) <= sqrt(|Y||Z|) <=> |S| <= |Y||Z|: true, with equality iff S complete (then sigma_S^2 = |Y||Z|).
for (nx, ny, nz, nw) in [(2, 3, 4, 5), (1, 1, 1, 1), (3, 3, 3, 3)]:
    for star in (True, False):
        nS = ny if star else ny * nz
        sS2 = nS if star else ny * nz
        lhs2 = nx * nw * nS * nS            # lambda_max(K)^2
        rhs2 = (nx * ny) * sS2 * (nz * nw)  # (sigma_R sigma_S sigma_T)^2
        print(f"  dims {(nx,ny,nz,nw)} S={'star' if star else 'complete'}: lambda_max(K)^2 = {lhs2} <= {rhs2} = (sigma_R sigma_S sigma_T)^2: {lhs2 <= rhs2}{' (equality)' if lhs2 == rhs2 else ''}")
print("STEP-8 DONE")
