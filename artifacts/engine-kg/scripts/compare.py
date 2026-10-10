"""Old gate vs new gate from one run of the NEW binary's bench --triangle-drivers CSV.

Per query: new-gate time = the sampled policy's median; old-gate time = the same unless
the outcome is `rescued`, where the old gate ran greedy: t_greedy * overhead (overhead =
median t_sampled/t_greedy over the run's `gate` outcomes, the planner's own cost; also
reported raw). Cross-checked against the OLD binary's run (same queries): stage-1
decisions must agree.
usage: compare.py <name>=<new.csv>[:<old.csv>] ...
"""
import csv, math, sys, statistics

def q(xs, p):
    xs = sorted(xs)
    if not xs: return float('nan')
    k = (len(xs)-1)*p; lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi]-xs[lo])*(k-lo)

def load(path):
    by = {}
    for r in csv.DictReader(open(path)):
        by.setdefault(r['query_id'], {})[r['policy']] = r
    return by

def ms(r):
    return float(r['median_ns']) if r['median_ns'] else float('nan')

def table(name, new, old=None):
    recs = []
    overheads = []
    mism = 0
    for qid, pol in new.items():
        s, g = pol['sampled'], pol['greedy']
        for r in pol.values():
            if r['answer_ok'] != '1': mism += 1
        if s['outcome'] == 'timeout' or g['outcome'] == 'timeout':
            continue
        if s['outcome'] == 'gate':
            overheads.append(ms(s)/ms(g))
        recs.append((qid, s, g, pol))
    over = q(overheads, .5) if overheads else 1.0
    rows = []
    for qid, s, g, pol in recs:
        t_new = ms(s)
        if s['outcome'] == 'rescued':
            t_old = ms(g) * over
            t_old_raw = ms(g)
        else:
            t_old = t_old_raw = ms(s)
        rows.append(dict(qid=qid, t_new=t_new, t_old=t_old, t_old_raw=t_old_raw, outcome=s['outcome'], pick=s['pick'],
                         exact=pol['exact']['outcome'], tf={}, g=ms(g)))
    sp = [r['t_old']/r['t_new'] for r in rows]
    sp_raw = [r['t_old_raw']/r['t_new'] for r in rows]
    regs = sorted([r for r in rows if r['t_new'] > 1.2*r['t_old']], key=lambda r: -r['t_new']/r['t_old'])
    regs_raw = [r for r in rows if r['t_new'] > 1.2*r['t_old_raw']]
    n = len(rows)
    outcomes = {}
    for r in rows: outcomes[r['outcome']] = outcomes.get(r['outcome'], 0) + 1
    ex = {}
    for r in rows: ex[r['exact']] = ex.get(r['exact'], 0) + 1
    declined_new = outcomes.get('gate', 0)
    declined_old = outcomes.get('gate', 0) + outcomes.get('rescued', 0)
    tot_old = sum(r['t_old'] for r in rows); tot_new = sum(r['t_new'] for r in rows)
    print(f"## {name} (n = {n}; planner overhead on declines, median t_sampled/t_greedy: {over:.3f})")
    print(f"| speedup vs old gate: median / p90 / max | {q(sp,.5):.3g} / {q(sp,.9):.3g} / {max(sp):.3g} |")
    print(f"| same, old gate charged greedy's raw time (no planner overhead) | {q(sp_raw,.5):.3g} / {q(sp_raw,.9):.3g} / {max(sp_raw):.3g} |")
    print(f"| regressions > 1.2x: count; worst | {len(regs)}; {max((r['t_new']/r['t_old'] for r in regs), default=1):.3g}x ({regs[0]['qid'] if regs else '-'}) |")
    print(f"| same, raw greedy time | {len(regs_raw)} |")
    print(f"| decline rate old -> new | {declined_old}/{n} ({100*declined_old/n:.1f}%) -> {declined_new}/{n} ({100*declined_new/n:.1f}%) |")
    print(f"| sampled outcomes | {', '.join(f'{k} {v}' for k, v in sorted(outcomes.items()))} |")
    print(f"| exact outcomes | {', '.join(f'{k} {v}' for k, v in sorted(ex.items()))} |")
    print(f"| total ms old -> new | {tot_old/1e6:.1f} -> {tot_new/1e6:.1f} |")
    print(f"| answers identical across policies | {sum(len(p) for p in new.values()) - mism}/{sum(len(p) for p in new.values())} rows{' (MISMATCH ' + str(mism) + ')' if mism else ''} |")
    if old:
        # stage-1 agreement: old run's sampled outcome vs new run's (accepted stays accepted; gate -> gate or rescued)
        agree = dis = 0
        for qid, pol in new.items():
            if qid not in old: continue
            o = old[qid]['sampled']['outcome']; nn = pol['sampled']['outcome']
            ok = (o == 'accepted' and nn == 'accepted' and old[qid]['sampled']['pick'] == pol['sampled']['pick']) or (o == 'gate' and nn in ('gate', 'rescued')) or (o == nn)
            agree += ok; dis += not ok
        # drift: greedy medians old run vs new run
        drift = [ms(pol['greedy'])/ms(old[qid]['greedy']) for qid, pol in new.items() if qid in old and pol['greedy']['median_ns'] and old[qid]['greedy']['median_ns']]
        print(f"| stage-1 decisions vs the old binary's run | {agree} agree, {dis} differ |")
        print(f"| run drift, greedy median new/old: p10 / median / p90 | {q(drift,.1):.3g} / {q(drift,.5):.3g} / {q(drift,.9):.3g} |")
    for r in regs[:8]:
        print(f"    regression {r['qid']}: x{r['t_new']/r['t_old']:.2f} new {r['t_new']/1e3:.0f}us old {r['t_old']/1e3:.0f}us outcome {r['outcome']} pick {r['pick']}")
    print()

for spec in sys.argv[1:]:
    name, paths = spec.split('=', 1)
    parts = paths.split(':')
    new = load(parts[0]); old = load(parts[1]) if len(parts) > 1 else None
    table(name, new, old)
