"""Summarize bench --triangle-drivers CSVs against E2's bounds.

usage: analyze.py <meta.csv> <out.md> <name>=<bench.csv>...
"""
import csv
import math
import statistics
import sys


def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def fmt(x):
    if isinstance(x, float) and math.isnan(x):
        return "–"
    return f"{x:.3g}" if isinstance(x, float) else str(x)


def load(path):
    by = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            by.setdefault(r["query_id"], {})[r["policy"]] = r
    return by


def ms(r):
    return float(r["median_ns"]) if r["median_ns"] else float("nan")


def main():
    meta = {r["id"]: r for r in csv.DictReader(open(sys.argv[1]))}
    out = sys.stdout if sys.argv[2] == "-" else open(sys.argv[2], "w")
    forced = ["forced:0", "forced:1", "forced:2"]
    for spec in sys.argv[3:]:
        name, path = spec.split("=", 1)
        by = load(path)
        n = len(by)
        sp_exact, spread, greedy_over_op, greedy_over_op_acc, exact_vs_bestforced = [], [], [], [], []
        diff_pick = both_pick = 0
        gate = {"sampled": {}, "exact": {}}
        m_match = m_total = 0
        within_u = 0
        best_work_over_u = []
        timeouts = {}
        mismatch = 0
        best_forced_is_argmin = forced_cmp = 0
        sampled_picks_bestforced = exact_picks_bestforced = 0
        best_forced_is_cost_argmin = 0
        oracle = []  # t_forced[sampled pick] / t_forced[exact pick]
        big = big_m = big_cost = big_n = 0
        declined_overhead = []  # t_sampled / t_greedy where the gate declined
        missed = []  # t_greedy / t_best_forced where the gate declined
        accepted_regret = []  # t_sampled / t_greedy where accepted
        for qid, pol in by.items():
            mt = meta[qid]
            for p, r in pol.items():
                if r["outcome"] == "timeout":
                    timeouts[p] = timeouts.get(p, 0) + 1
                if r["answer_ok"] != "1":
                    mismatch += 1
            s, e, g = pol["sampled"], pol["exact"], pol["greedy"]
            for p in ("sampled", "exact"):
                o = pol[p]["outcome"]
                gate[p][o] = gate[p].get(o, 0) + 1
            if s["outcome"] != "timeout" and e["outcome"] != "timeout":
                sp_exact.append(ms(s) / ms(e))
            fm = [ms(pol[f]) for f in forced if pol[f]["outcome"] != "timeout"]
            if len(fm) == 3:
                spread.append(max(fm) / min(fm))
                # Engine M per text pattern; forced:k drives SHAPE edge k,
                # whose text pattern is that row's pick.
                fpick = [int(pol[f]["pick"]) for f in forced]
                best_f = fpick[fm.index(min(fm))]
                M = [int(s[f"M_{i}"]) for i in range(3)]
                forced_cmp += 1
                if M[best_f] == min(M):
                    best_forced_is_argmin += 1
                if int(s["pick"]) == best_f:
                    sampled_picks_bestforced += 1
                if int(e["pick"]) == best_f:
                    exact_picks_bestforced += 1
                if e["outcome"] == "accepted":
                    exact_vs_bestforced.append(ms(e) / min(fm))
                N = [int(s[f"n_{i}"]) for i in range(3)]
                cost = [2 * N[i] + M[i] for i in range(3)]
                if cost[best_f] == min(cost):
                    best_forced_is_cost_argmin += 1
                t_by_pick = {fpick[i]: fm[i] for i in range(3)}
                oracle.append(t_by_pick[int(s["pick"])] / t_by_pick[int(e["pick"])])
                if min(fm) >= 1e6:
                    big_n += 1
                    big_m += M[best_f] == min(M)
                    big_cost += cost[best_f] == min(cost)
            if s["outcome"] == "gate" and g["outcome"] != "timeout":
                declined_overhead.append(ms(s) / ms(g))
                if len(fm) == 3:
                    missed.append(ms(g) / min(fm))
            if s["outcome"] != "timeout" and g["outcome"] != "timeout":
                greedy_over_op.append(ms(g) / ms(s))
                if s["outcome"] == "accepted":
                    greedy_over_op_acc.append(ms(g) / ms(s))
            if s["pick"] != "-1" and e["pick"] != "-1":
                both_pick += 1
                diff_pick += s["pick"] != e["pick"]
            if s["M_0"]:
                M = [int(s[f"M_{i}"]) for i in range(3)]
                E2 = [round(float(mt[f"M{i+1}"])) for i in range(3)]
                m_total += 1
                m_match += M == E2
                U = float(mt["U"])
                bw = min(M)
                best_work_over_u.append(bw / U)
                within_u += bw <= U
        greedy_timeouts = timeouts.get("greedy", 0)
        print(f"## {name} (n = {n} queries)\n", file=out)
        rows = [
            ("answers identical across the six policies", f"{n * 6 - mismatch}/{n * 6} rows" + (f" ({mismatch} MISMATCH)" if mismatch else "")),
            ("speedup exact vs sampled (t_sampled / t_exact): median / p90 / min", f"{fmt(q(sp_exact, .5))} / {fmt(q(sp_exact, .9))} / {fmt(min(sp_exact) if sp_exact else float('nan'))}"),
            ("forced spread (worst / best forced driver): median / p90 / max", f"{fmt(q(spread, .5))} / {fmt(q(spread, .9))} / {fmt(max(spread) if spread else float('nan'))}"),
            ("fastest forced driver is the exact-M argmin", f"{best_forced_is_argmin}/{forced_cmp}"),
            ("fastest forced driver is the exact (2n + M) argmin", f"{best_forced_is_cost_argmin}/{forced_cmp}"),
            ("  same, queries whose fastest forced run ≥ 1 ms: M argmin / (2n+M) argmin", f"{big_m}/{big_n} / {big_cost}/{big_n}"),
            ("kernel-only gain of the exact pick: t_forced[sampled pick] / t_forced[exact pick], median / p90 / min / max", f"{fmt(q(oracle, .5))} / {fmt(q(oracle, .9))} / {fmt(min(oracle) if oracle else float('nan'))} / {fmt(max(oracle) if oracle else float('nan'))}"),
            ("sampled pick = fastest forced driver", f"{sampled_picks_bestforced}/{forced_cmp}"),
            ("exact pick = fastest forced driver", f"{exact_picks_bestforced}/{forced_cmp}"),
            ("exact-M picks a different driver than sampled", f"{diff_pick}/{both_pick} ({100 * diff_pick / max(both_pick, 1):.1f}%)"),
            ("sampled outcomes", ", ".join(f"{k} {v}" for k, v in sorted(gate['sampled'].items()))),
            ("exact outcomes", ", ".join(f"{k} {v}" for k, v in sorted(gate['exact'].items()))),
            ("greedy / operator (t_greedy / t_sampled), all: median / p90 / max", f"{fmt(q(greedy_over_op, .5))} / {fmt(q(greedy_over_op, .9))} / {fmt(max(greedy_over_op) if greedy_over_op else float('nan'))}"),
            ("greedy / operator where sampled accepted: n, median / p90 / min", f"{len(greedy_over_op_acc)}, {fmt(q(greedy_over_op_acc, .5))} / {fmt(q(greedy_over_op_acc, .9))} / {fmt(min(greedy_over_op_acc) if greedy_over_op_acc else float('nan'))}"),
            ("gate declined: t_sampled / t_greedy (planning overhead), median / p90", f"{fmt(q(declined_overhead, .5))} / {fmt(q(declined_overhead, .9))}"),
            ("gate declined: t_greedy / t_best_forced, median / p90 / max; count > 1.5", f"{fmt(q(missed, .5))} / {fmt(q(missed, .9))} / {fmt(max(missed) if missed else float('nan'))}; {sum(1 for x in missed if x > 1.5)}/{len(missed)}"),
            ("exact (accepted) / best forced: median / p90", f"{fmt(q(exact_vs_bestforced, .5))} / {fmt(q(exact_vs_bestforced, .9))}"),
            ("timeouts per policy", ", ".join(f"{k} {v}" for k, v in sorted(timeouts.items())) or "none"),
            ("engine exact M_π equals E2's M1..M3 (all three rotations)", f"{m_match}/{m_total}"),
            ("Cor 4.3 (cor-kernel): min_π M_π ≤ U", f"{within_u}/{m_total}"),
            ("min_π M_π / U: median / p90 / max", f"{fmt(q(best_work_over_u, .5))} / {fmt(q(best_work_over_u, .9))} / {fmt(max(best_work_over_u) if best_work_over_u else float('nan'))}"),
        ]
        print("| quantity | value |\n|---|---|", file=out)
        for k, v in rows:
            print(f"| {k} | {v} |", file=out)
        print(file=out)
    if out is not sys.stdout:
        out.close()
    if sys.argv[2] != "-":
        print(open(sys.argv[2]).read())


if __name__ == "__main__":
    main()
