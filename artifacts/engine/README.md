# Engine A/B: the triangle operator against main's greedy plan

This directory reproduces the engine table (`tab-engine`, Appendix B; Section 9 in revision 3) of
`spectral_agm.typ`. The measurements are of the sampled-driver triangle
operator only.

## Builds

| Label | What it is |
|---|---|
| A (greedy) | Leatherback's main line at the time of the run (left-deep greedy plan) |
| N (operator) | the development branch with the triangle operator |

Leatherback is not yet public. The builds are named by label here; once
Leatherback is open-sourced, `../README.md` will give the commit of each
label (see "Leatherback builds" there).

Each side was exported with `git archive <commit>` into its own directory and
built with Zig 0.16.0 in ReleaseFast with ONNX disabled. Each used a private
cache: `ZIG_LOCAL_CACHE_DIR=<tree>/.zig-cache`, never shared between trees.
Both builds exited 0 (`logs/build.rc`), and both binaries report
`leatherback 0.2.1+unknown (onnx: disabled)`.

```sh
for side in A:$REV_A N:$REV_N; do      # the commits of builds A and N
  d=${side%%:*}; rev=${side#*:}
  mkdir -p $d && git archive $rev | tar -x -C $d
  python3 -I scripts/patch_bench.py $d/src/bench/benchmark.zig
  (cd $d && ZIG_LOCAL_CACHE_DIR=$PWD/.zig-cache zig build -Doptimize=ReleaseFast -Denable-onnx=false)
done
```

The same patch, `scripts/patch_bench.py`, went into both trees before the
build. It adds the eight `vf_*` query cases to `query_bench_suite`, and it
prints one `VFTIME,<case>,<exec_ns>,<rows>` line per run, giving the
in-process execution time of every run rather than only the best.

The exact `zig build` flags were not logged (`build_A.log` and `build_N.log`
are empty). The flags above are reconstructed from the verifier's report
("ReleaseFast", "own private cache") and from the binaries' version line.

## Data

The generator is `bench/generate_data.zig` in build N; the `triangles`
mode exists only on the branch. The graphs:

```sh
zig build gen-data -- triangles 1000000 skew.ttl 7 1.5   # Zipf(1.5) hubs, seed 7
zig build gen-data -- triangles 1000000 uni.ttl  7 0     # alpha 0 (uniform), seed 7
zig build gen-data -- 100000 medium.ttl 42               # the 100k synthetic set, seed 42
```

The generator printed (`logs/gen{1,2,3}.log`):
`Generated ~1000000 triangle-workload edges to …/skew.ttl (seed=7, alpha=1.50)`,
the same line for `uni.ttl` with `alpha=0.00`, and
`Generated 100000 triples to …/medium.ttl (seed=42)`. The logs named
the workspace by an absolute scratch path; revision 3 replaced it by
`$V`, the variable `scripts/ab.sh` now takes from the environment.

| File | sha256 | Statements written | Distinct triples loaded |
|---|---|---:|---:|
| `skew.ttl` | `887859868f302bcb2c02345a55e7cb466e9a7f88eaf1420b7515d2caf942e666` | 1,000,000 | 101,411 |
| `uni.ttl` | `b8034341712152aa349ca7de8ef3a19393eb4596d5436b6b405e457b26c91d71` | 1,000,000 | 999,983 |
| `medium.ttl` | `d6e52e83720caa8fb88bdec0a783c3e0a91b35e02563a02b5f9718a1e23d9345` | 105,224 | 101,210 |

The counts come from `logs/store_build_*.log`. **The skewed graph has 1M
generated edge statements, but they deduplicate to 101,411 distinct
triples.** The Zipf(1.5) sampler repeats hub pairs. The first version's phrase
"1M-edge generated graph" referred to the statements written, not to the
distinct edges stored; the revised paper gives both counts.

The `.lb` stores were built with A's (main's) binary. The command below is
reconstructed: the `leatherback build` output is in `logs/store_build_*.log`,
but the command line itself was not logged. The same goes for the
`gen-data` lines above, which are reconstructed from the generator's usage
string and its logged seed and alpha.

```sh
A/zig-out/bin/leatherback build skew.ttl -o skew.lb     # and uni, medium
```

## Timing protocol (`scripts/ab.sh`)

There were three interleaved rounds, ordered dataset → side, A before N. In
each, `leatherback bench --query --runs 5 --filter vf_ <dataset>` was run on
`skew.lb`, `skew.ttl` (in-memory), `uni.lb`, `medium.lb` and `medium.ttl`.
That gives 15 samples per (dataset, case, side), and the table reports their
median. Every bench process exited 0 (`logs/ab.rc`).

```sh
zsh scripts/ab.sh                                    # writes ab.csv and ab.rc
python3 -I scripts/summ.py ab.csv > ab_summary.md    # medians, minima, N/A ratios
```

`ab.csv` columns: side, round, dataset, tag, case, exec_ns, rows.

## Answers (`scripts/answers.py`)

Both binaries ran 10 queries through `leatherback query` on the five
datasets: the eight `vf_*` cases plus an `ORDER BY … LIMIT 5` and a
`COUNT(DISTINCT ?a)` triangle. Each stdout was sorted and hashed with
SHA-256. All 50 pairs matched with exit 0 (`logs/answers.log`, `DIFFS 0`).
The line counts in that log include the result header lines.

## Gates on build N (`scripts/gates.sh`)

`logs/gates.rc` records `test-unit=0 lint=0 sparql=0 changelog=0 fmt=0`.
The summaries are in `logs/g_unit_summary.log`, where test-unit ran 6945
tests, passed them all and skipped 67, plus `logs/g_lint.log`,
`logs/g_sparql.log` and `logs/g_changelog.log`.

## Machine

```
hw.model: Mac16,5
hw.ncpu: 16
hw.memsize: 137438953472        (128 GiB)
machdep.cpu.brand_string: Apple M4 Max
macOS 26.7 (25G229); Zig 0.16.0
```

These values were read from `sysctl` and `sw_vers` on the machine that ran
the A/B, while these artifacts were assembled on 2026-10-09, the same day as
the run. No other load was controlled for. Runs were in-process (`bench`),
and there was no CPU pinning: macOS offers none.

## Files

| Path | Contents |
|---|---|
| `logs/ab.csv` | Every raw timing sample (1,200 rows = 3 rounds × 5 datasets × 2 sides × 8 cases × 5 runs) |
| `logs/ab_summary.md` | `summ.py` output: per (dataset, case) the row counts, n, A/N medians, N/A and minima. The paper's table is taken from this. |
| `logs/ab.rc` | Exit code of each bench process |
| `logs/answers.log` | 50 answer comparisons |
| `logs/probe_{A,N}_{skew,uni,medium}.log` | Single-run probes made before the A/B |
| `logs/gen{1,2,3}.log`, `logs/store_build_*.log`, `logs/data_sha256.txt` | Data generation, store builds and hashes |
| `logs/revs.txt`, `logs/build.rc`, `logs/gates.rc`, `logs/g_*.log` | Build labels (the commits are withheld until Leatherback is public), build exit codes and gate results |
| `scripts/*` | The verifier's scripts, unchanged. They hard-code the verifier's scratch directory, so edit `V=`/`S=`/`W=` before re-running. |

## Ratios quoted in the paper

The ratios below come from the medians in `logs/ab_summary.md`.

- Triangle rows: 878.50 ms / 27.28 ms = 32.2.
- Triangle `COUNT(*)`: 941.80 ms / 8.29 ms = 113.6. Taken from the
  displayed rounded medians, 94180/829 lies strictly between 113 and 114
  and rounds to 114.

## Not covered

The following were not measured: each forced driver, exact-M driver choice,
the per-binding scheduler (not implemented), the separation families at
scale, p99 latency, metered work split into pricing and execution, and the
knowledge-graph triangles of E2. Whether the gate "declined" is inferred from
timing, because the build has no counter to report it.
