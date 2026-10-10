import csv, sys, statistics as st
from fractions import Fraction as F
for p in sys.argv[1:]:
    by = {}
    for r in csv.DictReader(open(p)): by.setdefault(r['query_id'], {})[r['policy']] = r
    g = {}
    for k, pol in by.items():
        s, o = pol['sampled'], pol['stage1']
        if not s['median_ns'] or not o['median_ns']: continue
        g.setdefault(s['outcome'], []).append((F(int(s['median_ns']), int(o['median_ns'])), int(o['median_ns']), int(s['median_ns'])))
    print(p.split('/')[-2] + '/' + p.split('/')[-1])
    for oc, xs in g.items():
        rs = sorted(x[0] for x in xs)
        so = sum(x[1] for x in xs); sn = sum(x[2] for x in xs)
        print(f"  {oc:9s} n={len(xs):4d} sampled/stage1 median {float(st.median(rs)):.4f} max {float(rs[-1]):.3f} >1.2: {sum(r > F(6,5) for r in rs)}  totals {so/1e6:.3f} -> {sn/1e6:.3f} ms ({float(F(sn,so)):.4f})")
