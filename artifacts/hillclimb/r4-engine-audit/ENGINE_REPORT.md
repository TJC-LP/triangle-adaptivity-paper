# Independent engine audit

`engine_audit.py` was written independently and run as `python3 -I engine_audit.py`; `engine_audit.out` contains exact integer/Fraction results. Existing scripts were read, never run or imported. This audit did not build or run the Zig engine, did not run tests, and did not change engine code or external PRs.

## Verdicts

- **Proved from the supplied CSVs:** the KG summary table, timeout exclusion, reconstructed old-gate totals, zero regressions above 1.2 under that baseline, and all stored medians.
- **Proved from code inspection:** stage 2 follows a stage-1 decline, is restricted to the view arm with proof price zero, applies the signal guard, uses the stated arithmetic, and applies the 16,384 threshold after the large-cost argmin.
- **Refuted:** floor skipping preserves the all-candidate rescue decision. A literal, realizable 31,000-tuple graph causes the implementation to accept while the fully sampled rule declines.
- **Refuted:** synthetic slowdowns above 1.05 occur only on 8–180 microsecond queries. Uniform `vf_tri_count` takes 54,444,667 ns before and 57,613,750 ns after, a factor `57613750/54444667 = 1.0582074090011424`.
- **Historical evidence, not newly rerun:** five local gate exit codes and ReleaseFast build are zero; the red test log explicitly records exit 1; the historical synthetic answer log contains 21 equal hash records. The stored `green.log` is empty. The aggregate successful unit-test log/exit status is the available positive evidence.
- **Open with obstruction in this audit:** full `test-all` on the stack tip, out-of-sample performance, full independent replay of the 7,056-configuration selection, and any post-fix benchmark results were not supplied by this fresh execution. These are not claimed as newly verified here.

## Exact recomputation of the KG table

The baseline is a **within-run reconstruction**: on rescued queries it uses greedy's median multiplied by the median sampled/greedy ratio among declined queries; on other queries it reuses the new sampled-policy median. It is not a fresh old-binary timing for every query. This distinction matters when interpreting “zero regressions.”

| Dataset | Timed queries | Old reconstructed total, ms | New total, ms | p90 speedup | Maximum speedup | Old/new declines | Answer flags |
|---|---:|---:|---:|---:|---:|---|---|
| CoDEx-L | 871 | 189.863500303 | 144.771133 | 5.4419534894 | 16.4651637362 | 571 / 354 | 5226/5226 |
| sci50 | 120 | 1003.95605567 | 546.727088 | 7.50637813766 | 18.8001702727 | 87 / 35 | 720/720 |
| Wikidata5M | 249 | 1839.36789141 | 1270.166988 | 4.22067355991 | 104.639564598 | 166 / 123 | 1500/1500 |

All medians of speedup are 1. All three adjusted and raw baseline regression counts above 1.2 are zero. Exact old totals are respectively

- `25821288042666513977/135999220500000000` ms;
- `3730700702879/3716000000` ms;
- `373085427202569/202833500000` ms.

The exact overhead factors are `139752537931/135999220500`, `10715/11148`, and `374417/405667`. The raw-baseline p90 speedups are `302083/57042`, `638460594829/81752092040`, and `27700147835347/6057399285000`, approximately 5.29579958627, 7.80971567696, and 4.57294401971.

`w5m-1393` is the sole timed-comparison exclusion because its greedy row says timeout. The file nevertheless marks that row's answer as equal; therefore “1500/1500” is the number of stored successful answer flags, not 1500 newly repeated complete timing runs. Every nonblank median equals the independent exact median of its recorded `runs_ns` samples.

The available `raw-old2` reruns reproduce stage-1 outcomes **and accepted-driver picks** on 871/871 CoDEx-L and 120/120 sci50 queries. There is no Wikidata5M `raw-old2` file at that location, so this lane does not independently certify the separate 250/250 historical comparison.

## Literal refutation of decision-preserving floor skipping

The source has two incompatible facts:

1. `triangle_join.zig:319–326` specifies a large-cost argmin over **all sampled candidates**, then applies the minimum-driver threshold.
2. At line 345, an unsampled candidate is declared unable to pass the large branch whenever `n<min_driver`, even if its cost is low enough to win the argmin and veto a larger driver.

Take shape edges `E0=(x,y)`, `E1=(x,z)`, `E2=(y,z)` with sizes `(1000,10000,20000)` and the default `min_driver=16384`. Let `E0={(i,i):0<=i<1000}`. At the 64 indices `floor(1000s/64)`, give both the associated `x` in E1 and the associated `y` in E2 degree 15. Use disjoint z-value sets in E1 and E2, and fill the remaining rows with unrelated matching edges. There are no triangles.

The independently constructed actual sets give these **literal** stride-sampling results:

| Driver | n | n2 | n3 | sampled adaptive | Large cost | Structural cost |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1000 | 20000 | 10000 | 15000 | 317000 | 484000 |
| 1 | 10000 | 20000 | 1000 | 0 | 50000 | 100000 |
| 2 | 20000 | 10000 | 1000 | 0 | 80000 | 160000 |

The seed's E2 edge is relation 2, so `probe_first=false`. Its sampled path is 15000. Stage 1 prices greedy at 16000 and the seed kernel at 17000, hence declines. Both other drivers were left unsampled because their `2n` floors exceed 16000.

The rescue's large comparison budget `2G_L` is 798000; its structural budget is 9000. Candidate 1's floors are `(50000,100000)`. It is skipped because `10000<16384` and its structural floor exceeds 9000. Candidate 2 is sampled, and accepted because `3*80000=240000<=798000`.

If candidate 1 is sampled, however, it wins the large-cost argmin at 50000 and then fails the minimum-size threshold. The structural argmin costs 100000, exceeding 9000. The all-candidate rule therefore declines.

Exact Python output:

```
floor_filtered ([True, False, True], ('large', 2))
all_sampled ([True, True, True], None)
```

This is a decision counterexample, not a query-answer correctness counterexample. It directly refutes the source comment and report's universal claim that the pruning can neither undercut an accepted candidate nor change a decision. It also prevents interpreting every difference between exact and sampled policies as solely a numerical sampling error: their candidate-availability states can differ, which changes this rule's decisions even with candidate costs held fixed.

A conservative repair retaining the searched post-argmin semantics is to remove `c.n < min_driver` from `large_floor_fails`. Skip only when both actual price floors fail their budgets:

```
3 * rescueFloor(.large) > large_budget
and rescueFloor(.structural) > structural_budget
```

Then any skipped candidate is too expensive to undercut an accepted candidate in either branch. Retain the minimum-size test after the large argmin. This would require a regression test with the literal witness and fresh benchmark measurements; no code was changed by this audit.

## Synthetic controls and historical gates

All 18 sampled-policy outcomes and picks in `ctl/old_*.csv` versus `ctl/new_*.csv` agree. The exact new/old range is `163166/194459` through `8583/7708`, approximately 0.8390766177 through 1.1135184224. Exactly three controls exceed 1.05:

| Control | Old ns | New ns | Exact ratio |
|---|---:|---:|---:|
| skew `vf_tri_sel` | 168667 | 184084 | `184084/168667` |
| uniform `vf_tri_count` | 54444667 | 57613750 | `57613750/54444667` |
| uniform `vf_tri_sel` | 7708 | 8583 | `8583/7708` |

Calling these differences “noise” is a possible interpretation, not established by these single old/new sets alone. The precise defensible statement is that decisions and drivers were unchanged, timings ranged as above, and the historical answer-hash log reports 21/21 matches.

The stored gate status is `fmt=0,test-unit=0,lint=0,sparql=0,changelog=0`; build status is `rf=0`. No fresh Zig build, test run, or hash execution occurred in this audit.

## Paper-ready corrected statement

> On the supplied within-run reconstructed baseline, the rescue reduces aggregate median query times from 189.9 to 144.8 ms, 1004.0 to 546.7 ms, and 1839.4 to 1270.2 ms on the three measured datasets, with no slowdown exceeding 1.2 under that comparison. The supplied synthetic controls retain all measured plan decisions and driver choices; their new/old timing ratios range from 0.839 to 1.114, including a 1.058 ratio on the approximately 54 ms uniform count query. The implementation's threshold-aware candidate pruning is not equivalent to evaluating the searched rule on every candidate: a smaller candidate can win the large-cost argmin and then fail its post-selection threshold. Until this pruning is corrected and remeasured, the engine should be described as a variant of the searched rule, not as a universally decision-preserving implementation of it.
