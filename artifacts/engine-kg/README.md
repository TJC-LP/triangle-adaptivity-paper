# engine-kg: triangle driver policies on knowledge-graph triangles

The paper's knowledge-graph triangle workload (experiment E2's queries) is run
through the Leatherback engine as `COUNT(*)` under six driver policies.

- Engine: build P, the driver-policy development branch (on top of
  build N, the operator branch of `../engine/`), ReleaseFast, `-Denable-onnx=false`,
  on an Apple M4 Max with 128 GiB, one worker thread.
- Knob: `reorder.triangle_driver_policy`, a benchmarking-only variable. Only
  `bench --triangle-drivers` sets it. Its default `.sampled` is the
  product's planner, and the unit tests pin that the plan is unchanged.
- Harness:
  `leatherback bench --triangle-drivers --runs 5 --timeout-ms 30000 <store.lb> <queries.tsv>`.
  The harness opens the store once. For each query it does one untimed probe
  (`sampled`, with the planner's exact pass), one untimed warm-up per policy,
  then 5 timed rounds; each round runs every policy once, in turn. Times are
  the in-process `executeAstWithStoreContext` wall time, and every row
  reports the median of the 5. The answer of every run must equal the
  probe's, and the harness fails otherwise. All 7,446 (query, policy) rows
  agree.

## Policies

| policy | driver | floor and cost gate |
|---|---|---|
| `sampled` | argmin of the sampled kernel cost 2n + M̂, from 64 samples per candidate (the product) | yes |
| `exact` | argmin of the exact walk M_π, counted over every edge of each candidate, O(\|E₁\| log) degree reads, charged to the planning time | yes |
| `forced:k` | shape edge k (greedy's k-th pattern) | skipped |
| `greedy` | none: the operator is disabled, so the pairwise order runs | – |

M_π = Σ_{(x,y)∈E₁} min(|N₂(y)|, |N₃(x)|), the kernel's ideal precharged
candidate budget (`AdaptiveTriangle.triangle_probes`; the paper's
shorter-side cost model). It is not the number of entries the walk reads,
which can be smaller (the paper's §Mechanization gives a 3-versus-1
example), nor metered work. The engine's exact M_π equals E2's
`M1..M3` (computed independently with scipy) for every rotation of all
1,241 queries.

## Data and queries

- CoDEx-L: train, valid and test (612,437 triples), all 871 E2 queries.
- Wikidata5M (transductive): train, valid and test (20,624,575 triples). The
  sample is 250 of 1,781 queries, 25 per decile of log₁₀ M, seed 3313.
- sci50: `sci50.nt` (18,483,050 triples; see `../e2/README.md` for its rebuild recipe and digest). The sample
  is 120 of 456 queries, 12 per decile of log₁₀ M, seed 3313.
- Query i is `?x R ?y . ?y S ?z . ?z T ?x` from results.csv row i, with an
  edge reversed when d = 1. `queries/meta.csv` carries E2's U, AGM, ℓ2,
  Out and M1..M3 for every id.
- Entities and relations in the KG TSV files map to IRIs as
  `<http://wd/Q…>` and `<http://wd/P…>`.

## Files

- `raw/<dataset>.csv`: one row per (query, policy). The columns are listed
  at the top of `src/bench/triangle_drivers.zig`. In brief:
  - `outcome` is the planner's decision (`accepted` = the kernel ran,
    `gate` = the cost gate sent the query to greedy).
  - `pick` is the text-order pattern the policy chose as driver.
  - `runs_ns` holds the 5 timings.
  - `n_i` and `M_i` are the edge size and the exact walk, per text pattern.
  - `est_A_i` are the policy's estimated walks.
- `queries/`: the query files and `meta.csv`.
- `scripts/`: `tsv2nt.py`, `make_queries.py`, `analyze.py` and
  `run_all.sh`, which reproduces everything.
- `summary.md`: the output of `analyze.py`.
- `raw-rescue/<dataset>.csv`: run B (see below), same columns; `outcome`
  can also be `rescued`.
- `scripts/engine_numbers.py <raw> <raw-rescue>`: every number of the
  paper's Table 7 (`tab-engine-kg`) for runs A and B, in exact fractions;
  output in `logs/engine_numbers.log`.
- `scripts/compare.py codex-l=raw-rescue/codex-l.csv:raw/codex-l.csv ...`:
  the rescue-stage table (`tab-rescue`), old planner against new, with the
  stage-1 cross-check against run A.
- `scripts/pickdiff.py <raw-rescue>`: where the sampled and exact picks of
  run B differ, by outcome (`logs/pickdiff.log`).
- `scripts/adversary.py`: the sampled-planner adversary of the paper's
  `prop-sampler` for every data-independent position rule (stride,
  golden-ratio grid, fixed pseudo-random grids), exact integers
  (`logs/adversary.log`, ALL OK). `estimator_adversary.py` is the original
  stride-only construction (m = 64, 128, 256).

## Run B: exact objective 2n + M and the rescue stage

Run B repeats the same harness on the same stores and queries with
Leatherback build R1 (the first version of the rescue stage). Its `exact`
policy minimizes the planner's objective 2|E₁| + M_π (run A's minimized M_π
alone), and both `sampled` and `exact` go through the planner's second
admission stage (the rescue), which re-prices a declined triangle in
calibrated units on a warm stored view. The rescue rule was fitted offline
to run A's rows, so its gains in run B are in-sample; stage-1 decisions
agree with run A on every query. The w5m process peaked at a 91.7 GB
footprint in run B.

The rescue-stage totals of run B in `compare.py` use a reconstructed
stage-1 time on rescued queries (greedy's time times a median planning
overhead). Run C below measures that baseline instead and supersedes them
in the paper's `tab-rescue`.

## Run C: the stage-1 planner measured in the same run

Run C uses build R2s of the rescue stage: build R2, which makes the rescue's
candidate pruning decision-preserving, plus a commit that adds a bench-only
`stage1` policy: the same sampled estimate and stage-1 gate with no rescue.
The harness is as above with `--runs 6`, and the order of the seven
policies is shuffled in every timed round, seeded by the query id (a
fixed-order run showed a 5–8% position bias in favour of `stage1`).

- `raw-run-c/<dataset>.csv`: the rows (all 250 w5m queries; `w5m-1393`'s
  greedy row is again a timeout). The w5m process peaked at a 116 GB
  footprint.
- `python3 -I scripts/run_c_analyze.py raw-run-c/<dataset>.csv`: totals,
  speedups, regressions and answer flags of `tab-rescue`, exact fractions.
  `scripts/run_c_split.py raw-run-c/*.csv` splits them by outcome
  (rescued / unchanged plan); `scripts/run_c_rows.py raw-run-c/*.csv` gives
  the exact policy's counts.
- `controls-run-c/shuffled/`: the three synthetic stores, 10 shuffled
  rounds. `controls-run-c/pairs/`: uniform `vf_tri_count` run as 10
  alternating process pairs of the pre-rescue binary (build P,
  `alt_old_*`) and the fixed binary (build R2, before the bench-only shuffle commit; `alt_new_*`), 5 runs each; `answers.log`
  compares sorted-output hashes, old against new, for all 21 (store,
  query) pairs. `python3 -I scripts/run_c_controls.py controls-run-c`
  prints both.
- The bench exits 1 (`AnswerMismatch`) on the synthetic stores, in run C
  and with the pre-rescue binary alike: its answer check compares the
  first cell of a row-returning query, and the `*_rows` and `vf_tri_sel`
  queries have no `ORDER BY`, so the first row depends on the driver. The
  sorted-output hashes in `answers.log` are identical. The knowledge-graph
  runs are `COUNT(*)` and exit 0.

## Caveats

- In this experiment the `exact` policy's planning is real work: three full
  O(|E| log |E|) passes per query. Its end-to-end time is therefore
  dominated by planning, and it is meant to say which driver is right, not
  to be fast. "Forced-time gain" (called "kernel-only gain" in revision 2)
  reads the `forced` timing of each policy's pick, which separates the
  choice from its planning cost. A forced time is the elapsed time of the
  whole run with that driver forced, not metered kernel work; the "oracle"
  (best forced driver) is chosen after seeing all three forced times and
  is not a deployable policy.
- Most CoDEx-L runs take 0.1–1 ms, which is noisy at the scale of driver
  choice. The "≥ 1 ms" rows restrict to queries whose fastest forced run
  takes at least 1 ms.
- One greedy run passed the 30 s timeout (`w5m-1393`,
  `P31 . P17 . P17^T`; sampled operator 9.4 ms). It is left out of every
  greedy ratio, so those ratios understate the gap. The w5m process peaked
  at an 85.6 GB memory footprint, from greedy's materialized 2-paths.
