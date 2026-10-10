"""Step 1: exact enumeration of the dual vertices of the arc LP (k = 3 sanity, k = 4), domination pruning,
D4-orbit classification, and exact 'needed' certificates.

needed(v): there is a statistics vector c = (rho, varsigma) with rho_e >= varsigma_e >= 0 at which v is the
UNIQUE minimiser among all dual vertices (then it is on an open set, by continuity).  Certificate: an explicit
rational c with (u - v).c > 0 for every other vertex u.  Found by random rational sampling, verified exactly.
redundant(v): some other vertex u dominates v on the whole cone (exact exponent test) -> v is never the unique
minimiser anywhere.
usage: python3 -I s1_dual.py
"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from v2lib import dual_vertices, dominated_by, mono_str, classify, d4_images

random.seed(12345)


def run(k):
    A, E, rows, verts = dual_vertices(k)
    print(f"k={k}: {len(A)} arcs, {len(verts)} dual vertices (exact basis enumeration)")
    nvar = 2 * k
    kept = [v for v in verts if not any(dominated_by(v, u, k) for u in verts)]
    pruned = [v for v in verts if v not in kept]
    print(f"  non-dominated: {len(kept)}; dominated: {len(pruned)}")
    # min over all vertices == min over kept, everywhere on the cone: each pruned vertex is >= some kept vertex
    for v in pruned:
        doms = [u for u in kept if dominated_by(v, u, k)]
        assert doms, ("pruned vertex not dominated by a kept one", v)
    # needed certificates for kept vertices
    needed = {}
    for v in kept:
        found = None
        for trial in range(20000):
            rho = [F(random.randint(0, 60)) for _ in range(k)]
            vs = [F(random.randint(0, int(rho[e]))) if rho[e] > 0 else F(0) for e in range(k)]
            c = rho + vs
            vc = sum(a * b for a, b in zip(v, c))
            if all(sum(a * b for a, b in zip(u, c)) > vc for u in verts if u != v):
                found = c
                break
        needed[v] = found
    n_needed = sum(1 for v in kept if needed[v] is not None)
    print(f"  needed (unique-minimiser certificate found): {n_needed} of {len(kept)}")
    for v in kept:
        if needed[v] is None:
            print("   NO certificate found for", mono_str(v, k))
    # redundant: every pruned vertex is dominated -> never a unique minimiser.  Also double-check by sampling
    # that no pruned vertex is ever a unique minimiser on 20000 random points.
    bad = 0
    for trial in range(20000):
        rho = [F(random.randint(0, 60)) for _ in range(k)]
        vs = [F(random.randint(0, int(rho[e]))) if rho[e] > 0 else F(0) for e in range(k)]
        c = rho + vs
        vals = [(sum(a * b for a, b in zip(u, c)), u) for u in verts]
        m = min(x[0] for x in vals)
        mins = [u for (x, u) in vals if x == m]
        if len(mins) == 1 and mins[0] in pruned:
            bad += 1
    print(f"  pruned vertex unique minimiser on random points: {bad} (expected 0)")
    return A, E, verts, kept, pruned, needed


if __name__ == "__main__":
    A3, E3, v3, k3, p3, n3 = run(3)
    print("  k=3 kept monomials:")
    for v in k3:
        print("    ", mono_str(v, 3, ["R", "S", "T"]))
    print("  k=3 pruned:")
    for v in p3:
        print("    ", mono_str(v, 3, ["R", "S", "T"]))

    A4, E4, v4, k4, p4, n4 = run(4)
    # orbit classification
    from collections import Counter
    cls = {v: classify(v) for v in k4}
    cnt = Counter(cls.values())
    print("  orbit class counts (kept):", dict(sorted(cnt.items())))
    # D4 orbits: kept set closed under D4?
    kept_set = set(k4)
    closed = all(img in kept_set for v in k4 for img in d4_images(v))
    print("  kept set closed under D4:", closed)
    orbits = []
    seen = set()
    for v in k4:
        if v in seen:
            continue
        orb = d4_images(v) & kept_set
        seen |= orb
        orbits.append((cls[v], len(orb), sorted(orb)))
    print("  number of D4-orbits among kept:", len(orbits))
    for name, sz, orb in sorted(orbits, key=lambda t: (t[0], -t[1])):
        print(f"    orbit {name:3s} size {sz}: " + "; ".join(mono_str(v, 4) for v in orb))
    print("  kept vertices with certificates:")
    for v in k4:
        c = n4[v]
        print(f"    {cls[v]:3s} {mono_str(v, 4):42s} witness c=rho{[str(x) for x in c[:4]]} vs{[str(x) for x in c[4:]]}" if c else f"    {cls[v]:3s} {mono_str(v,4)} NONE")
    print("  pruned (dominated) vertices and a dominating kept vertex:")
    for v in p4:
        u = next(u for u in k4 if dominated_by(v, u, 4))
        print(f"    {mono_str(v, 4):40s} >= {mono_str(u, 4)}")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vertices4.json"), "w") as f:
        json.dump({"all": [[str(x) for x in v] for v in v4], "kept": [[str(x) for x in v] for v in k4],
                   "class": {mono_str(v, 4): cls[v] for v in k4}}, f, indent=1)
    print("wrote vertices4.json")
