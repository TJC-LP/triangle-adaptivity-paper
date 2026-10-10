"""Write the triangle COUNT(*) queries of E2's results.csv as bench query files.

usage: make_queries.py <results.csv> <outdir> [--seed S] [--w5m N] [--sci50 N]

Every CoDEx-L query; a sample of Wikidata5M and sci50 stratified by the
decile of log10(M) (E2's min-rotation walk), equal count per decile, seeded.
Writes <outdir>/<dataset>.tsv (id<TAB>SPARQL) and <outdir>/meta.csv (the E2
columns each id came from).
Query i of results.csv is  ?x R ?y . ?y S ?z . ?z T ?x  with R = p1 (d1 = 1:
reversed), S = p2, T = p3 — the patterns written in that order.
"""
import argparse
import csv
import math
import os
import random

DATASETS = {"codex-l": "codex-l", "wikidata5m": "w5m", "sci50": "sci50"}


def iri(p):
    return p if p.startswith("<") else f"<http://wd/{p}>"


def pattern(p, d, a, b):
    s, o = (b, a) if d == "1" else (a, b)
    return f"?{s} {iri(p)} ?{o} ."


def sparql(row):
    pats = [pattern(row["p1"], row["d1"], "x", "y"),
            pattern(row["p2"], row["d2"], "y", "z"),
            pattern(row["p3"], row["d3"], "z", "x")]
    return "SELECT (COUNT(*) AS ?n) WHERE { " + " ".join(pats) + " }"


def stratified(rows, n, rng, bins=10):
    keyed = sorted(rows, key=lambda r: (math.log10(max(float(r["M"]), 1.0)), r["_id"]))
    per = n // bins
    extra = n - per * bins
    out = []
    for b in range(bins):
        lo = len(keyed) * b // bins
        hi = len(keyed) * (b + 1) // bins
        chunk = keyed[lo:hi]
        k = min(len(chunk), per + (1 if b < extra else 0))
        out.extend(rng.sample(chunk, k))
    return sorted(out, key=lambda r: r["_id"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("outdir")
    ap.add_argument("--seed", type=int, default=3313)
    ap.add_argument("--w5m", type=int, default=250)
    ap.add_argument("--sci50", type=int, default=120)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    by = {k: [] for k in DATASETS}
    with open(a.results) as f:
        for i, row in enumerate(csv.DictReader(f)):
            if row["dataset"] in by and row["variant"] == "dir":
                row["_id"] = f"{DATASETS[row['dataset']]}-{i:04d}"
                by[row["dataset"]].append(row)
    pick = {
        "codex-l": by["codex-l"],
        "wikidata5m": stratified(by["wikidata5m"], a.w5m, rng),
        "sci50": stratified(by["sci50"], a.sci50, rng),
    }
    os.makedirs(a.outdir, exist_ok=True)
    meta_cols = ["id", "dataset", "query", "pattern", "p1", "d1", "p2", "d2", "p3", "d3",
                 "r1", "r2", "r3", "U", "U_cert", "agm", "l2", "out", "M", "M1", "M2", "M3"]
    with open(os.path.join(a.outdir, "meta.csv"), "w", newline="") as mf:
        mw = csv.writer(mf)
        mw.writerow(meta_cols)
        for ds, rows in pick.items():
            with open(os.path.join(a.outdir, f"{DATASETS[ds]}.tsv"), "w") as qf:
                for r in rows:
                    qf.write(f"{r['_id']}\t{sparql(r)}\n")
                    mw.writerow([r["_id"]] + [r[c] for c in meta_cols[1:]])
            print(ds, "of", len(by[ds]), "->", len(rows))


if __name__ == "__main__":
    main()
