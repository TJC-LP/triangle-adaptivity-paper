"""Exact enumeration of the dual vertices of the arc-blowup LP for the k-cycle.

Cycle vertices 0..k-1, edge e = (e, e+1 mod k).  An arc is a nonempty
contiguous subset of Z_k (k singletons, k pairs, ..., k (k-1)-sets, 1 full).

Arc-blowup instance with multiplicities n_A >= 1 (integers):
  vertex v has index set prod_{A ∋ v} [n_A];
  edge e = (v, v') relates (i, i') iff i_A = i'_A for every arc A ⊇ e;
  the other coordinates are free.
Then (Kronecker products; all exact)
  |R_e|     = prod_{A ∩ e ≠ ∅} n_A
  ||A_e||^2 = prod_{|A ∩ e| = 1} n_A
  Out       = prod_A n_A.

Primal LP (log scale): max sum_A nu_A  s.t.
  sum_{A∩e≠∅} nu_A <= rho_e,  sum_{|A∩e|=1} nu_A <= varsigma_e,  nu >= 0.
Dual: min sum_e lambda_e rho_e + mu_e varsigma_e  s.t. for all arcs A:
  sum_{e: A∩e≠∅} lambda_e + sum_{e: |A∩e|=1} mu_e >= 1, lambda, mu >= 0.

The dual vertices are the candidate monomials  prod r_e^lambda_e s_e^mu_e.
Everything is in fractions.Fraction.
"""
import itertools
import sys
from fractions import Fraction


def arcs(k):
    out = []
    for length in range(1, k):
        for start in range(k):
            out.append(frozenset((start + i) % k for i in range(length)))
    out.append(frozenset(range(k)))
    return out


def edges(k):
    return [frozenset({e, (e + 1) % k}) for e in range(k)]


def dual_rows(k):
    """Rows of the dual constraint matrix, variables ordered (lambda_0..lambda_{k-1}, mu_0..mu_{k-1})."""
    A = arcs(k)
    E = edges(k)
    rows = []
    for arc in A:
        row = [Fraction(0)] * (2 * k)
        for e, edge in enumerate(E):
            inter = len(arc & edge)
            if inter >= 1:
                row[e] = Fraction(1)
            if inter == 1:
                row[k + e] = Fraction(1)
        rows.append(row)
    return A, E, rows


def solve_square(M, b):
    """Solve M x = b exactly (Gaussian elimination); return None if singular."""
    n = len(M)
    M = [row[:] + [b[i]] for i, row in enumerate(M)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        inv = 1 / M[col][col]
        M[col] = [v * inv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b_ for a, b_ in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def vertices(k):
    A, E, rows = dual_rows(k)
    nvar = 2 * k
    # constraints: rows (>= 1) and nonnegativity (x_i >= 0)
    cons = [(row, Fraction(1)) for row in rows]
    for i in range(nvar):
        row = [Fraction(0)] * nvar
        row[i] = Fraction(1)
        cons.append((row, Fraction(0)))
    verts = set()
    for subset in itertools.combinations(range(len(cons)), nvar):
        M = [cons[i][0] for i in subset]
        b = [cons[i][1] for i in subset]
        x = solve_square(M, b)
        if x is None:
            continue
        # feasibility
        ok = all(sum(c * v for c, v in zip(row, x)) >= rhs for row, rhs in cons)
        if ok:
            verts.add(tuple(x))
    return A, E, sorted(verts)


def monomial_str(x, k, names=None):
    if names is None:
        names = [chr(ord('a') + i) for i in range(k)]
    parts = []
    for e in range(k):
        if x[e] != 0:
            parts.append(f"r_{names[e]}^{x[e]}")
    for e in range(k):
        if x[k + e] != 0:
            parts.append(f"s_{names[e]}^{x[k + e]}")
    return " ".join(parts) if parts else "1"


def dominated(x, y, k):
    """True if monomial x >= monomial y for all 1 <= s_e <= r_e, i.e. y is at least as good as x.
    x dominated-by y iff for each e: lambda_x >= lambda_y and lambda_x + mu_x >= lambda_y + mu_y."""
    return all(x[e] >= y[e] and x[e] + x[k + e] >= y[e] + y[k + e] for e in range(k))


def prune(verts, k):
    keep = []
    for x in verts:
        if any(y != x and dominated(x, y, k) for y in verts):
            continue
        keep.append(x)
    return keep


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    names = {3: ["R", "S", "T"], 4: ["R", "S", "T", "Q"]}.get(k)
    A, E, verts = vertices(k)
    print(f"k={k}: {len(A)} arcs, {len(verts)} dual vertices")
    kept = prune(verts, k)
    print(f"after pairwise domination pruning: {len(kept)}")
    for x in kept:
        print("  ", monomial_str(x, k, names))
    # also show the pruned ones
    print("pruned (pairwise dominated):")
    for x in verts:
        if x not in kept:
            print("  ", monomial_str(x, k, names))
