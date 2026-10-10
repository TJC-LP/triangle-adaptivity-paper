"""Numbers for the revised engine section, recomputed from raw CSVs with exact
Fractions for the ratios (medians/quantiles via the artifact's linear-interp q()).

usage: engine_numbers.py <old_dir> <new_dir>
  old_dir: engine-kg/raw (run A, build P, exact = argmin M)
  new_dir: engine-kg/raw-rescue (run B, build R1, exact = argmin 2n+M, rescue stage)
"""
import csv
import math
import sys
from fractions import Fraction as F

FORCED = ["forced:0", "forced:1", "forced:2"]


def q(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * F(p)
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def load(path):
    by = {}
    for r in csv.DictReader(open(path)):
        by.setdefault(r["query_id"], {})[r["policy"]] = r
    return by


def t(r):
    return None if r["outcome"] == "timeout" or not r["median_ns"] else int(r["median_ns"])


def f3(x):
    return f"{float(x):.3g}"


def per_query(pol):
    s, e, g = pol["sampled"], pol["exact"], pol["greedy"]
    fm = [t(pol[f]) for f in FORCED]
    fpick = [int(pol[f]["pick"]) for f in FORCED]
    by_pick = {fpick[i]: fm[i] for i in range(3)}
    M = [int(s[f"M_{i}"]) for i in range(3)]
    n = [int(s[f"n_{i}"]) for i in range(3)]
    return s, e, g, fm, by_pick, M, n


def analyze(name, path, new):
    by = load(path)
    out = {}
    e2e, gain, dpick, s_fast, e_fast, m_fast, c_fast = [], [], 0, 0, 0, 0, 0
    e_is_cost_argmin = e_is_M_argmin = 0
    st1 = {"sampled": 0, "exact": 0}
    fin = {"sampled": 0, "exact": 0}
    nog_ratio, nog_cnt, oracle_ratio, oracle_cnt, ndecl = [], 0, [], 0, 0
    left_s, left_o, left_cnt_s, left_cnt_o = [], [], 0, 0
    resc_vs_best = []
    for qid, pol in by.items():
        s, e, g, fm, by_pick, M, n = per_query(pol)
        cost = [2 * n[i] + M[i] for i in range(3)]
        tg = t(g)
        ts, te = t(s), t(e)
        e2e.append(F(te, ts))
        gain.append(F(by_pick[int(s["pick"])], by_pick[int(e["pick"])]))
        dpick += s["pick"] != e["pick"]
        best = fm.index(min(fm))
        bestpick = int(pol[FORCED[best]]["pick"])
        s_fast += int(s["pick"]) == bestpick
        e_fast += int(e["pick"]) == bestpick
        m_fast += M[bestpick] == min(M)
        c_fast += cost[bestpick] == min(cost)
        e_is_cost_argmin += cost[int(e["pick"])] == min(cost)
        e_is_M_argmin += M[int(e["pick"])] == min(M)
        for p, r in (("sampled", s), ("exact", e)):
            st1[p] += r["outcome"] in ("gate", "rescued")
            fin[p] += r["outcome"] == "gate"
        # stage-1 declines: sampled choice without the gate vs oracle
        if s["outcome"] in ("gate", "rescued") and tg is not None:
            ndecl += 1
            r1 = F(tg, by_pick[int(s["pick"])])
            r2 = F(tg, min(fm))
            nog_ratio.append(r1); nog_cnt += r1 > F(3, 2)
            oracle_ratio.append(r2); oracle_cnt += r2 > F(3, 2)
        if new and s["outcome"] == "gate" and tg is not None:
            r1 = F(tg, by_pick[int(s["pick"])]); r2 = F(tg, min(fm))
            left_s.append(r1); left_o.append(r2)
            left_cnt_s += r1 > F(3, 2); left_cnt_o += r2 > F(3, 2)
        if new and s["outcome"] == "rescued":
            resc_vs_best.append(F(ts, min(fm)))
    N = len(by)
    print(f"## {name} ({'new R1' if new else 'old P'}), {N} queries")
    print(f"exact/sampled e2e median / p10: {f3(q(e2e,.5))} / {f3(q(e2e,.1))}")
    print(f"kernel-only gain (forced[s pick]/forced[e pick]) median / p90 / min / max: "
          f"{f3(q(gain,.5))} / {f3(q(gain,.9))} / {f3(min(gain))} / {f3(max(gain))}")
    print(f"exact pick != sampled pick: {dpick} ({100*dpick/N:.1f}%)")
    print(f"exact pick is argmin 2n+M: {e_is_cost_argmin}/{N}; is argmin M: {e_is_M_argmin}/{N}")
    print(f"fastest forced = argmin M / argmin 2n+M: {m_fast} / {c_fast}")
    print(f"fastest forced = sampled / exact pick: {s_fast} / {e_fast}")
    print(f"stage-1 declines sampled / exact: {st1['sampled']} / {st1['exact']}")
    print(f"final declines (gate) sampled / exact: {fin['sampled']} / {fin['exact']}")
    print(f"stage-1 declined ({ndecl} w/ greedy timing): greedy/forced[sampled pick] median / p90: "
          f"{f3(q(nog_ratio,.5))} / {f3(q(nog_ratio,.9))}; >1.5x: {nog_cnt}")
    print(f"   oracle greedy/best forced median / p90: {f3(q(oracle_ratio,.5))} / {f3(q(oracle_ratio,.9))}; >1.5x: {oracle_cnt}")
    if new:
        print(f"still declined after rescue ({len(left_s)}): greedy/forced[sampled pick] median / p90: "
              f"{f3(q(left_s,.5))} / {f3(q(left_s,.9))}; >1.5x {left_cnt_s};  oracle median / p90 "
              f"{f3(q(left_o,.5))} / {f3(q(left_o,.9))}; >1.5x {left_cnt_o}")
        print(f"rescued ({len(resc_vs_best)}): t_sampled / best forced median / p90 / max: "
              f"{f3(q(resc_vs_best,.5))} / {f3(q(resc_vs_best,.9))} / {f3(max(resc_vs_best))}")
    print()


old_dir, new_dir = sys.argv[1], sys.argv[2]
for nm in ("codex-l", "sci50", "w5m"):
    analyze(nm, f"{old_dir}/{nm}.csv", False)
    analyze(nm, f"{new_dir}/{nm}.csv", True)
