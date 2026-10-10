"""KG re-run: measured stage1 (old gate) vs sampled (new gate) in one interleaved run.
usage: python3 -I analyze.py <new.csv> [<previous run's sampled csv>]
Exact arithmetic (Fraction) for totals and ratios; medians as stored by the harness."""
import csv, sys
from fractions import Fraction as F

def load(p):
    by = {}
    for r in csv.DictReader(open(p)):
        by.setdefault(r['query_id'], {})[r['policy']] = r
    return by

def q(xs, p):  # nearest-rank quantile on sorted list
    xs = sorted(xs); import math
    return xs[max(0, math.ceil(p * len(xs)) - 1)]

def med(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

new = load(sys.argv[1])
prev = load(sys.argv[2]) if len(sys.argv) > 2 else None
tot_old = tot_new = F(0); ratios = []; regs = []; excluded = []
outc = {}; s1 = {}; answers_ok = answers_all = 0; incons = []
resc_ratios = []; same_ratios = []
for qid, pol in new.items():
    s, o = pol['sampled'], pol['stage1']
    outc[s['outcome']] = outc.get(s['outcome'], 0) + 1
    s1[o['outcome']] = s1.get(o['outcome'], 0) + 1
    for r in pol.values():
        answers_all += 1; answers_ok += r['answer_ok'] == '1'
    # stage1 must be sampled's stage-1 decision
    if not ((s['outcome'] in ('gate', 'rescued') and o['outcome'] == 'gate') or (s['outcome'] == o['outcome'] and s['pick'] == o['pick'])):
        incons.append((qid, s['outcome'], o['outcome']))
    if not s['median_ns'] or not o['median_ns'] or 'timeout' in (s['outcome'], o['outcome']):
        excluded.append(qid); continue
    tn, to = F(int(s['median_ns'])), F(int(o['median_ns']))
    tot_old += to; tot_new += tn
    r = to / tn; ratios.append(r)
    (resc_ratios if s['outcome'] == 'rescued' else same_ratios).append(r)
    if tn / to > F(6, 5): regs.append((qid, s['outcome'], float(tn / to), int(o['median_ns']), int(s['median_ns'])))
print(f"queries {len(new)}, timed {len(ratios)}, excluded {excluded}")
print(f"sampled outcomes {outc}; stage1 outcomes {s1}; stage1/sampled inconsistencies {incons}")
print(f"answers ok {answers_ok}/{answers_all} (all policies)")
print(f"total stage1 {float(tot_old)/1e6:.3f} ms -> sampled {float(tot_new)/1e6:.3f} ms; ratio new/old exact {tot_new/tot_old} = {float(tot_new/tot_old):.6f}")
print(f"speedup stage1/sampled: median {float(med(ratios)):.4f} p90 {float(q(ratios,0.9)):.4f} max {float(max(ratios)):.4f} min {float(min(ratios)):.4f}")
if resc_ratios: print(f"  rescued ({len(resc_ratios)}): median {float(med(resc_ratios)):.3f} p10 {float(q(resc_ratios,0.1)):.3f} p90 {float(q(resc_ratios,0.9)):.3f} min {float(min(resc_ratios)):.3f} max {float(max(resc_ratios)):.3f}")
print(f"  same plan ({len(same_ratios)}): median {float(med(same_ratios)):.3f} p5 {float(q(same_ratios,0.05)):.3f} p95 {float(q(same_ratios,0.95)):.3f} min {float(min(same_ratios)):.3f} max {float(max(same_ratios)):.3f}")
print(f"regressions sampled/stage1 > 1.2: {len(regs)}")
for r in sorted(regs, key=lambda x: -x[2]): print("   ", r)
if prev:
    diff = [(k, prev[k]['sampled']['outcome'], prev[k]['sampled']['pick'], new[k]['sampled']['outcome'], new[k]['sampled']['pick']) for k in new if k in prev and (prev[k]['sampled']['outcome'], prev[k]['sampled']['pick']) != (new[k]['sampled']['outcome'], new[k]['sampled']['pick'])]
    print(f"sampled decision changes vs previous (build R1) run: {len(diff)}")
    for d in diff: print("   ", d)
    # timing drift on sampled, same decision
    dr = [F(int(new[k]['sampled']['median_ns']), int(prev[k]['sampled']['median_ns'])) for k in new if k in prev and new[k]['sampled']['median_ns'] and prev[k]['sampled']['median_ns'] and (prev[k]['sampled']['outcome'], prev[k]['sampled']['pick']) == (new[k]['sampled']['outcome'], new[k]['sampled']['pick'])]
    print(f"sampled timing drift new/prev, same decision ({len(dr)}): median {float(med(dr)):.3f} p10 {float(q(dr,0.1)):.3f} p90 {float(q(dr,0.9)):.3f}")
    pt = sum(F(int(prev[k]['sampled']['median_ns'])) for k in new if k in prev and new[k]['sampled']['median_ns'] and prev[k]['sampled']['median_ns'] and k not in excluded)
    print(f"previous run sampled total over the same timed queries {float(pt)/1e6:.3f} ms")
