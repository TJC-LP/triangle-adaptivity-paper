"""Exact determination of which dual vertices are needed in U_4 = min over vertices.

A vertex v is needed iff there is a statistics vector c = (rho, varsigma) with
rho_e >= varsigma_e >= 0 (i.e. 1 <= s_e <= r_e in logs) at which v is the UNIQUE minimiser.
LP: max t  s.t. (u - v).c >= t for all other vertices u,  rho_e - varsigma_e >= 0,
varsigma_e >= 0, sum_e rho_e = 1.  Needed iff t* > 0.  All arithmetic exact.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from lp_vertices import vertices, monomial_str
from exact_lp import solve_lp

k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
names = {3: ["R", "S", "T"], 4: ["R", "S", "T", "Q"]}[k]
A, E, verts = vertices(k)
print(f"k={k}: {len(verts)} dual vertices")
needed = []
for v in verts:
    others = [u for u in verts if u != v]
    nvar = 2 * k + 1  # c (2k) and t
    c_obj = [0] * (2 * k) + [-1]  # maximise t  == minimise -t
    A_ub, b_ub = [], []
    for u in others:
        # (u - v).c - t >= 0  ->  -(u-v).c + t <= 0
        row = [-(u[i] - v[i]) for i in range(2 * k)] + [1]
        A_ub.append(row)
        b_ub.append(0)
    for e in range(k):
        # varsigma_e - rho_e <= 0
        row = [0] * nvar
        row[e] = -1
        row[k + e] = 1
        A_ub.append(row)
        b_ub.append(0)
    A_eq = [[1] * k + [0] * k + [0]]
    b_eq = [1]
    bounds = [(0, None)] * (2 * k) + [(None, None)]
    st, x, val = solve_lp(c_obj, A_ub, b_ub, A_eq, b_eq, bounds)
    assert st == 'optimal', st
    t = -val
    tag = "NEEDED" if t > 0 else "redundant"
    if t > 0:
        needed.append(v)
    print(f"{tag:9s} t*={str(t):8s} {monomial_str(v, k, names)}   witness c={[str(a) for a in x[:2*k]]}" if t > 0 else f"{tag:9s} t*={str(t):8s} {monomial_str(v, k, names)}")
print(f"needed: {len(needed)} of {len(verts)}")
