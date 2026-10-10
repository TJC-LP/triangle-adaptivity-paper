# Second engine audit: the pruning fix of the rescue-stage pull request

Audit of build R2s (the pruning fix, build R2) against the searched rescue rule.

- `port.py`: a Python port (integer arithmetic, `python3 -I`) of
  `rescueDecide` / `rescueRule` / `unsettled` from
  `src/query/triangle_join.zig`, compared with the rule over every candidate
  on 2,800,002 cases: an exhaustive tie-heavy grid of 2.5M cases and 300k
  random wide cases, including the first audit's witness. No disagreement;
  in 673,734 cases the rule on the initially sampled candidates differs.
- `sab1.py` … `sab4.py`: sabotaged ports. `sab1` (restore the old
  `n >= min_driver` skip) and `sab4` (no index tie-break in the large
  undercut) produce counterexamples; `sab3` (drop the structural clause of
  `unsettled`) and `sab2` (that clause without its tie-break) still agree
  on every case: the structural clause is implied by the large one.
- `witness_block.zig.txt`: the witness test block (a fragment of `src/query/triangle_join_tests.zig`, not a standalone file), appended to the old tree
  (build R1); `old_witness.log` is its failure there ("pruned argmin:
  rescued driver 2 by large, the full rule declines").
  `new_filter.log` / `lazy.log`: the rescue tests passing on the fix, and
  the randomized test's statistics.
- `kg.py`: recomputes run C's table (totals, declines, p90/max speedups,
  regression counts, answers) from `engine-kg/raw-run-c/`; run it from a
  directory where `engine/kg2/` points at those rows.
