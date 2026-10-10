"""Synthetic controls: (a) per store, stage1 vs sampled in one process, 10 shuffled rounds;
(b) uniform vf_tri_count, old binary (build P) and new binary alternated in 10 process pairs.
usage: python3 -I run_c_controls.py controls-run-c"""
import csv, glob, sys, statistics as st
from fractions import Fraction as F
E = sys.argv[1]
def load(p):
    by = {}
    for r in csv.DictReader(open(p)):
        by.setdefault(r['query_id'], {})[r['policy']] = r
    return by
def runs(r): return [int(x) for x in r['runs_ns'].split(';') if x]
for d in ('skew', 'uni', 'medium'):
    by = load(f'{E}/shuffled/{d}.csv')
    print(f'## {d}')
    for qid, pol in by.items():
        s, o = pol['sampled'], pol['stage1']
        if not s['median_ns']: print(qid, s['outcome']); continue
        rs, ro = runs(s), runs(o)
        ok = all(r['answer_ok'] == '1' for r in pol.values())
        print(f"{qid}: sampled {s['outcome']}/{s['pick']} {int(s['median_ns'])/1e3:.1f}us [{min(rs)/1e3:.1f}-{max(rs)/1e3:.1f}] n={len(rs)}; stage1 {o['outcome']}/{o['pick']} {int(o['median_ns'])/1e3:.1f}us [{min(ro)/1e3:.1f}-{max(ro)/1e3:.1f}]; sampled/stage1 {float(F(int(s['median_ns']), int(o['median_ns']))):.4f}; answer_ok all {ok}")
print('## uniform vf_tri_count, alternated old/new processes')
pairs = []; allold = []; allnew = []; alls1 = []; outs = set()
for i in range(1, 11):
    o = load(f'{E}/pairs/alt_old_{i}.csv')['vf_tri_count']; n = load(f'{E}/pairs/alt_new_{i}.csv')['vf_tri_count']
    mo, mn, ms = int(o['sampled']['median_ns']), int(n['sampled']['median_ns']), int(n['stage1']['median_ns'])
    outs.add((o['sampled']['outcome'], o['sampled']['pick'], n['sampled']['outcome'], n['sampled']['pick'], n['stage1']['outcome'], n['stage1']['pick']))
    allold += runs(o['sampled']); allnew += runs(n['sampled']); alls1 += runs(n['stage1'])
    pairs.append(F(mn, mo))
    print(f'pair {i}: old {mo/1e6:.3f} ms, new sampled {mn/1e6:.3f} ms, new stage1 {ms/1e6:.3f} ms, new/old {float(F(mn,mo)):.4f}, new sampled/stage1 {float(F(mn,ms)):.4f}')
print('decisions (old sampled, new sampled, new stage1):', outs)
pr = sorted(pairs)
print(f'new/old per-pair: median {float(st.median(pr)):.4f} min {float(pr[0]):.4f} max {float(pr[-1]):.4f}; pairs > 1: {sum(p > 1 for p in pr)}/10')
for name, xs in (('old sampled', allold), ('new sampled', allnew), ('new stage1', alls1)):
    print(f'{name}: {len(xs)} runs median {st.median(xs)/1e6:.3f} ms mean {st.mean(xs)/1e6:.3f} sd {st.pstdev(xs)/1e6:.3f} min {min(xs)/1e6:.3f} max {max(xs)/1e6:.3f}')
print(f'pooled median new/old {st.median(allnew)/st.median(allold):.4f}')
