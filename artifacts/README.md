# Reproducibility artifacts for `spectral_agm.typ`

| Directory | What it reproduces |
|---|---|
| [`e2/`](e2/README.md) | Experiment E2 (Appendix A): code, `results.csv`, `summary.md`, logs, dataset URLs and sha256 digests, exact commands, Python environment |
| [`verify/`](verify/README.md) | Verification scripts for Theorem B and the per-binding results, with recorded outputs (`verify/OUTPUTS.md`), including an exact-arithmetic Theorem B check |
| [`engine/`](engine/README.md) | Engine A/B (Section 6 and Appendix B): build labels, build and data-generation commands, seeds, data hashes, raw timing samples, answer comparisons, machine |
| [`engine-kg/`](engine-kg/README.md) | Driver-policy runs on the knowledge-graph triangles (Appendix B, `tab-engine-kg`, `tab-rescue`): query files, raw per-(query, policy) rows of runs A, B and C, per-query bounds, scripts, summary, and the sampled-planner adversary (`prop-sampler`) |
| [`hillclimb/`](hillclimb/README.md) | Results added in revisions 3 and 4 (Sections 3--4, Appendix G), including the revision-4 fully reduced and 4-cycle theorems and the engine audit (`r4-*`): reports, exact-arithmetic rebuild scripts, recorded outputs, and `verified.md` with the consolidated verdicts |
| Lean (below) | The `LeatherbackSpectral` formalization (Appendix D) |

The raw datasets and generated graphs are not committed. Each README gives
the commands to download or regenerate them, and their SHA-256 digests.

## Leatherback builds

Leatherback, the engine of the measurements, is not yet public, so the
engine artifacts name its builds by label. Once it is open-sourced, this
table will give the commit of each label.

| Label | What it is | Used by |
|---|---|---|
| A | the main line at the time of the A/B (left-deep greedy plan) | `engine/` |
| N | the development branch with the triangle operator | `engine/` |
| P | the driver-policy branch, on top of N | `engine-kg/` run A; pre-rescue binary of `engine-kg/controls-run-c/pairs/` |
| R1 | the first version of the rescue (second admission) stage | `engine-kg/` run B; `hillclimb/r4-engine-audit/` |
| R2 | R1 with decision-preserving candidate pruning | `engine-kg/controls-run-c/pairs/`; `hillclimb/r4-engine-audit/second-audit/` |
| R2s | R2 plus a bench-only `stage1` policy and per-round shuffled policy order | `engine-kg/` run C |

## Lean: building the formalization

In this public repository the formalization is the standalone Lake package
in [`../lean/`](../lean/README.md). It contains the `LeatherbackSpectral`
library, its axiom audit `LeatherbackSpectralAudit`, and the four Std-only
Leatherback modules the spectral library imports (the reference semantics
and cost replica of the triangle kernel). It pins Lean `v4.32.2` and
mathlib `v4.32.2` (commit `905b95818eb32af7874a58b427f50c1711a5e96c`)
through `lean-toolchain` and `lake-manifest.json`.

```sh
cd lean
lake exe cache get    # mathlib's prebuilt .olean files (network)
lake build            # kernel-checks every module and the axiom audit
```

The audit file wraps each main theorem's `#print axioms` in `#guard_msgs`,
so the build fails if any of them depends on anything beyond `propext`,
`Classical.choice` and `Quot.sound`. That catches `sorryAx`,
`native_decide` (`Lean.ofReduceBool`) and custom axioms.

The package also builds `LeatherbackAudit`, which pins the axiom sets of
the 13 kernel-replica theorems the same way. The Lean sources are
byte-identical to the engine repository's Lean workspace except for three
doc comments that named an internal ticket; see `../lean/README.md`.
