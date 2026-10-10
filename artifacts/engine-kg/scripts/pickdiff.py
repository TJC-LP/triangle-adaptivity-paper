"""Run B: where do sampled and exact (2n+M) final drivers differ, by outcome pair."""
import csv, sys
from collections import Counter
for nm in ("codex-l", "sci50", "w5m"):
    by = {}
    for r in csv.DictReader(open(f"{sys.argv[1]}/{nm}.csv")):
        by.setdefault(r["query_id"], {})[r["policy"]] = r
    c = Counter()
    for qid, p in by.items():
        s, e = p["sampled"], p["exact"]
        c[(s["outcome"], e["outcome"], s["pick"] != e["pick"])] += 1
    nonresc = sum(v for (a, b, d), v in c.items() if d and a != "rescued" and b != "rescued")
    nonresc_n = sum(v for (a, b, d), v in c.items() if a != "rescued" and b != "rescued")
    print(nm, "diff where neither rescued: %d/%d" % (nonresc, nonresc_n), sorted(c.items()))
