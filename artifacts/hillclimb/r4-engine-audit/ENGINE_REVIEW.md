# Independent second review of the engine counterexample

**Verdict: the floor-skipping counterexample in `ENGINE_REPORT.md` is valid against the actual source control flow, with the ordinary warm-view assumptions.** This is an independent source-level verification and fresh Python reconstruction, not an executed Zig integration test. No engine code was changed.

I read `triangle_join.zig` and `reorder.zig` in a checkout of the rescue-stage branch of the engine repository. I did not execute or import `engine_audit.py`. The fresh `engine_review_exact.py` uses integer/Fraction arithmetic, constructs all relations itself, and was run with `python3 -I`.

## Reachability in the actual planner

- `reorder.zig:87` and `orderRun` order a connected pattern run by cardinality, with original position only as a tie-breaker. Cardinalities 1000,10000,20000 therefore produce the intended order E0=(x,y),E1=(x,z),E2=(y,z), assuming no prebound seed variables.
- The ordinary threshold is `triangle_min_run_triples=2048` (`reorder.zig:744`). `trianglePlan` compares this with **the sum** returned by `triangleRunTriples` (`reorder.zig:974`), not the seed or chosen-driver length. The witness total is **31000**, so seed length 1000 does not cause an early decline.
- The source accepts this three-variable, three-predicate triangle shape. A row-capable unmerged `.view`, available PSO/POS indexes, valid positive term IDs below the transient bit, and already certified ranges satisfy the source/proof preconditions. The second reconstruction shifts every numeric ID by one, so every ID is positive and all sorting, degrees and decisions are unchanged.
- `triangle_gain_ratio=1` and `triangle_rescue_min_driver=16384` are the defaults (`reorder.zig:756,764`). No custom testing knob is needed.
- `Plan.init` maps seed driver 0 to e2=2 and e3=1. Therefore `estimate` sets `probe_first=false` and uses the seed's **right** budget, corresponding to the real first greedy join on x. Its value is 15000.
- `estimateCandidate` reads exactly k=min(64,n) positions `s*n/k`, then uses integer `n*sum/k`, precisely as in the rebuild. It samples predicate PSO order. No alternative sampler or sorting assumption was substituted.
- `estimate` prices greedy at n0+path=16000; seed kernel cost is 2n0+A0=17000. It leaves drivers 1 and 2 unsampled because their stage-1 floors are 20000 and 40000. `costedTrianglePlan` therefore reaches rescue after the stage-1 decline, provided proof price is zero.
- `rescuedTrianglePlan` permits precisely the warm `.view` arm. This is a realizable premise; pre-certifying all PSO/POS ranges is sufficient. The counterexample does not purport to run on a cold view or the graph arm.

## Independently reproduced arithmetic

The positive-ID reconstruction gives:

| Driver | n | n2 | n3 | adaptive | left | right | large cost | structural cost |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1000 | 20000 | 10000 | 15000 | 15000 | 15000 | 317000 | 484000 |
| 1 | 10000 | 20000 | 1000 | 0 | 0 | 1093 | 50000 | 100000 |
| 2 | 20000 | 10000 | 1000 | 0 | 0 | 1250 | 80000 | 160000 |

All computations use the source's `seekDepth(other,n)=floor(log2(floor(other/n)))` when other>n. This equals floor(log2(other/n)) here and gives the reported coefficients 17,5,4. Large budget `2G_L=798000`; structural budget `G_S=9000`.

The exact source predicate at `triangle_join.zig:345` skips driver 1 because its size is below 16384 and structural floor 100000 exceeds 9000. Driver 2 is sampled because its large floor passes. The remaining large-cost argmin is driver 2 and `3*80000=240000≤798000`, so source semantics accept.

If all three candidates are sampled, driver 1 is the large-cost argmin at 50000. The source's **post-argmin** size threshold then rejects it. Structural argmin 100000 exceeds 9000, so the all-candidate searched rule declines. The fresh exact output is:

```
SOURCE_PRUNING ([True, False, True], ('large', 2))
ALL_CANDIDATES ([True, True, True], None)
```

Thus the issue is genuinely the incompatible size-threshold placement and pruning, not a mistaken candidate mapping, an early floor check, a different default gain ratio or numerical rounding. The report's conservative repair—remove `c.n < min_driver` from the pruning predicate but preserve the searched post-argmin threshold—is sound. If an omitted candidate could beat an accepted large candidate, its actual large cost and hence its zero-walk large floor would pass that budget, so this corrected predicate would sample it.

## Independent fixed-stride adversary

I also rebuilt the paper's complete R plus interleaved-neighborhood adversary for m=64,128,256. Relations use distinct positive-ID intervals and are sorted by actual subject/object pairs. Padding consists of fresh matching edges. For all three sizes the 64 stride positions have residue set J={0}, so j=1. The execution order is R(x,y),T(z,x),S(y,z), matching the paper and `Plan.init`.

| m | N | M_R | M_T=M_S=Out | sampled M_R,M_T,M_S | walked-entry lower bound | chosen/exact-best objective ratio |
|---:|---:|---:|---:|---|---:|---|
| 64 | 12290 | 258048 | 4032 | (0,4032,258111) | 254016 | 133120/6113 |
| 128 | 49154 | 2080768 | 16256 | (0,32513,2097280) | 2064512 | 352256/8171 |
| 256 | 196610 | 16711680 | 65280 | (0,261123,16777472) | 16646400 | 8421376/98177 |

Here the objective is 2|E|+M_E. The sampled rule chooses R in all cases. The first greedy join has sampled path m³; the stage-1 gate admits R for gain ratio at most (m+1)/2, respectively **65/2,129/2,257/2**, including the default ratio 1. N exceeds 2048 in every case, and rescue is never reached because stage 1 already accepts. The literal m=64 construction works even though the proposition's general sufficient hypothesis m>k=64 is strict; its specific j=1 is still less than m.

The data, exact outputs and assertions are in `engine_review_exact.py` and `engine_review_exact.out`.
