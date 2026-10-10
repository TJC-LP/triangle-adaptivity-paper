"""Run E2 on one prepared dataset.

usage: run.py <prep.npz> <dataset-label> <out.csv> [--top K] [--min-edges N] [--sym] [--max-M X]
"""
import argparse
import csv
import itertools
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bounds as B  # noqa: E402

FIELDS = ["dataset", "variant", "query", "pattern", "p1", "d1", "p2", "d2", "p3", "d3",
          "r1", "r2", "r3", "sigma1", "sigma2", "sigma3", "s1", "s2", "s3",
          "sig_cert1", "sig_cert2", "sig_cert3",
          "U", "U_term", "U_schur", "U_cw", "U_cert", "U_hi", "U_lo", "agm", "deg_bound",
          "l2", "l2_fwd", "l2_rev", "out", "M", "M1", "M2", "M3", "matmul_check", "count_secs"]


def canon(q):
    """q = ((p,d),(p,d),(p,d)); orbit under rotation and reversal (flip all directions)."""
    rev = tuple((p, 1 - d) for (p, d) in reversed(q))
    orbit = []
    for s in (q, rev):
        for k in range(3):
            orbit.append(s[k:] + s[:k])
    return min(orbit)


def pattern_name(ds):
    # cyclic if all three edges run the same way around the cycle; else "transitive" (acyclic)
    return "cyclic" if len(set(ds)) == 1 else "acyclic"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz")
    ap.add_argument("label")
    ap.add_argument("out")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--min-edges", type=int, default=0)
    ap.add_argument("--sym", action="store_true", help="also run the symmetrised graph (single-pred)")
    ap.add_argument("--max-M", type=float, default=2e10)
    ap.add_argument("--preds", default="", help="comma-separated predicate names to restrict to")
    ap.add_argument("--keep-zero", action="store_true")
    a = ap.parse_args()

    z = np.load(a.npz)
    n = int(z["n"][0])
    names = list(z["preds"])
    sizes = [len(z[f"s_{i}"]) for i in range(len(names))]
    order = sorted(range(len(names)), key=lambda i: -sizes[i])
    order = [i for i in order if sizes[i] >= a.min_edges]
    if a.preds:
        want = a.preds.split(",")
        order = [i for i in order if names[i] in want or names[i].rsplit("/", 1)[-1].strip("<>") in want]
    if a.top:
        order = order[: a.top]
    print(f"[{a.label}] n={n} preds selected={len(order)}", flush=True)

    rels = {}
    sig = {}
    spec_rows = []
    variants = ["dir"] + (["sym"] if a.sym else [])
    for i in order:
        s, o = z[f"s_{i}"], z[f"o_{i}"]
        for var in variants:
            if var == "sym":
                s2 = np.concatenate([s, o])
                o2 = np.concatenate([o, s])
                m = B.csr_from_edges(s2, o2, n)
            else:
                m = B.csr_from_edges(s, o, n)
            rels[(var, i)] = B.Rel(m)
            t0 = time.time()
            sp = B.spectral(m)
            sig[(var, i)] = sp
            spec_rows.append(dict(dataset=a.label, variant=var, pred=names[i], r=m.nnz, **sp))
            print(f"  {var} {names[i]} r={m.nnz} sigma={sp['sigma']:.6g} [{sp['sigma_lo']:.8g},"
                  f"{sp['sigma_hi']:.8g}] svds={sp['svds']:.8g} schur={sp['schur']:.6g} "
                  f"cw5={sp['cw_few']:.6g} it={sp['iters']} rel_width={sp['rel_width']:.2e}"
                  f"{'' if sp['converged'] else ' NOT-CONVERGED'} {time.time()-t0:.1f}s", flush=True)

    rows = []
    for var in variants:
        queries = set()
        for p in itertools.product(order, repeat=3):
            for d in itertools.product((0, 1), repeat=3):
                queries.add(canon(tuple(zip(p, d))))
        queries = sorted(queries)
        print(f"[{a.label}/{var}] canonical queries: {len(queries)}", flush=True)
        if var == "sym":
            # symmetric relations: direction irrelevant; keep only d=(0,0,0)
            queries = sorted({canon(tuple((p, 0) for p, _ in q)) for q in queries})
        skipped_support = skipped_M = zero = 0
        t0 = time.time()
        # support table: column 2j = subjects of order[j], 2j+1 = objects of order[j]
        import scipy.sparse as sps
        cols = []
        for j, p in enumerate(order):
            r = rels[(var, p)]
            cols.append(np.flatnonzero(r.rd))
            cols.append(np.flatnonzero(r.cd))
        zi = np.concatenate(cols)
        zj = np.concatenate([np.full(len(c), k) for k, c in enumerate(cols)])
        zm = sps.csr_matrix((np.ones(len(zi)), (zi, zj)), shape=(n, len(cols)))
        inter = (zm.T @ zm).toarray() > 0
        pos = {p: j for j, p in enumerate(order)}

        def side(p, d, head):  # head=True: the variable the edge points to
            j = pos[p]
            obj = head != bool(d)
            return 2 * j + (1 if obj else 0)

        flipped = {}
        for qi, q in enumerate(queries):
            ok = all(inter[side(*q[k], True), side(*q[(k + 1) % 3], False)] for k in range(3))
            if not ok:
                skipped_support += 1
                continue
            rv = []
            for p, d in q:
                r = rels[(var, p)]
                if d:
                    if (var, p) not in flipped:
                        flipped[(var, p)] = r.flipped()
                    r = flipped[(var, p)]
                rv.append(r)
            mt = B.kernel_M(rv)
            if min(mt) > a.max_M:
                skipped_M += 1
                print(f"  skip (M={min(mt):.3g}) {q}", flush=True)
                continue
            res = B.triangle(rv, [sig[(var, p)] for p, _ in q], mt=mt)
            if res["out"] == 0 and not a.keep_zero:
                zero += 1
                continue
            row = dict(dataset=a.label, variant=var,
                       query=" . ".join(f"{names[p]}{'^T' if d else ''}" for p, d in q),
                       pattern=pattern_name([d for _, d in q]))
            for k, (p, d) in enumerate(q, 1):
                row[f"p{k}"] = names[p]
                row[f"d{k}"] = d
                sp = sig[(var, p)]
                row[f"sigma{k}"] = sp["sigma"]
                row[f"sig_cert{k}"] = sp["sig_cert"]  # exact min(Schur, CW_5), rounded up
            row.update({k: res[k] for k in FIELDS if k in res})
            rows.append(row)
            if len(rows) % 200 == 0:
                print(f"  {qi}/{len(queries)} kept={len(rows)} {time.time()-t0:.0f}s", flush=True)
        print(f"[{a.label}/{var}] rows-so-far={len(rows)} zero={zero} support-skip={skipped_support} "
              f"M-skip={skipped_M} {time.time()-t0:.0f}s", flush=True)

    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    with open(a.out.replace(".csv", ".spectral.json"), "w") as f:
        json.dump(spec_rows, f, indent=1, default=float)


if __name__ == "__main__":
    main()
