# Levels of adaptivity and spectral worst-case bounds for labeled triangle joins

A. Richard Caputo III, TJC L.P.

This repository holds the paper, its figure scripts, the Lean 4
formalization, and the scripts, raw rows and recorded outputs behind every
computational claim. Paths in the paper of the form `artifacts/...` are
relative to this repository's root.

- Paper: [`paper/spectral_agm.pdf`](paper/spectral_agm.pdf) (Typst source [`paper/spectral_agm.typ`](paper/spectral_agm.typ))
- arXiv: _to be added_
- Leatherback (the RDF engine this work comes from): _to be open-sourced;
  link to be added here_. Until then the paper and the engine artifacts
  refer to its builds by label (`artifacts/README.md`, "Leatherback
  builds"); once it is public that table will give the commit of each
  label.

## What the paper proves

The paper asks how much adaptivity a variable-at-a-time join needs to be
worst-case optimal for the labeled triangle
`Q(x,y,z) = R(x,y) ∧ S(y,z) ∧ T(z,x)`, and for which statistics. It compares
a fixed attribute order, the best of the six orders per instance, a fixed
root with a per-binding choice of the next variable, and full per-binding
choice.

- **Per-binding choice and the cyclic ℓ2 bound.** For the cost `C` of the
  best per-binding choice (each intersection charged at its shorter run) and
  the cyclic ℓ2 bound `B2`:
  `C ≤ N + (N/3)^{3/8} B2^{3/4}` and `C ≤ N + 3^{1/8} N^{-1/8} B2^{5/4}`,
  and explicit families attain the minimum of the two up to a constant
  factor at every slope `B2 ≍ N^κ`, `κ ∈ [9/10, 3/2]`. So `C = O(N + B2)`
  fails even up to polylogarithmic factors (exponent 9/8 at `B2 ≍ N`): this
  unpartitioned kernel class cannot attain `O(N + B2)`, while known
  degree-partitioned algorithms can. When every tuple lies in a triangle
  the gap exponent lies in `[1/10, 1/8]`, exact for `κ ≥ 11/10`.
- **Separations between levels.** Against `N + B2`, one fixed order loses
  exactly `Θ(N^{1/4})`, the best of six orders `Θ(N^{1/5})`, and a fixed
  root between `N^{1/8}` and `N^{1/4}`. The lower bounds also hold for a
  single directed predicate and for fresh comparison-based sorted
  intersections under adversarial identifiers (where the worst case at
  `B2 ≍ N` is `Θ(N^{9/8} (log N)^{1/4})`).
- **Spectral bound.** Under relation sizes and operator norms of the 0/1
  incidence matrices, the worst-case triangle output lies in `(U/4, U]` for
  an explicit nine-term `U`, with a sharp factor 4, and the best driver of
  the kernel does work at most `U`. This part is machine-checked in Lean 4
  (see `lean/`). For the labeled 4-cycle an explicit 38-term `U4` gives
  `(U4/16, U4]`, with the best constant in `[8, 16]`.
- **Engine measurements.** On 1,241 knowledge-graph triangle queries the
  driver changes running time by up to 132×; a 64-row sample picks it about
  as often as exact counting, although no fixed sampling grid is within a
  constant factor in the worst case; and a calibrated second admission stage
  cuts total time by 21–49% against the stage-1 planner measured in the
  same run (in-sample).

The paper's "What is and is not new" and "What is not checked" passages
state exactly which results are proved on paper, which are formalized, and
which are measured.

## Layout

| Path | Contents |
|---|---|
| `paper/` | `spectral_agm.typ` and `spectral_agm.pdf`; figures `fbeta.svg`, `e2_ecdf.svg` and the scripts that draw them |
| `artifacts/` | Everything needed to check the computational claims; [`artifacts/README.md`](artifacts/README.md) indexes it |
| `lean/` | Standalone Lake package: the `LeatherbackSpectral` library, the Std-only kernel-replica modules it imports, and two axiom audits |
| `weaver-checks/` | Weaver's outside checks: five Python scripts written from the paper's definitions alone, and their recorded output (see its README) |
| `tools/scrub_check.py` | Fails if any file contains machine-local paths, internal ticket identifiers, tracker or session links, or e-mail addresses other than the author's; `--deny FILE` adds literal strings kept outside the repository |
| `CITATION.cff` | Citation metadata |
| `LICENSE` | MIT (code and data, copyright TJC L.P.); the paper text and figures are CC BY 4.0, see `paper/LICENSE` |

## Reproducing each artifact

All Python runs with `python3 -I` (Python 3.11). Unless a README says
otherwise, scripts use only the standard library and exact `fractions`
arithmetic.

**The paper.** Typst 0.15.1 with the New Computer Modern fonts:

```sh
cd paper
typst compile spectral_agm.typ spectral_agm.pdf
```

**The figures.**

```sh
python3 -I paper/make_fbeta_figure.py paper/fbeta.svg                           # exponent profile, exact Fractions
python3 -I paper/make_e2_figure.py artifacts/e2/results.csv paper/e2_ecdf.svg   # E2 ECDF from the raw results
```

Both regenerate the committed SVGs byte for byte.

**Exact-arithmetic checks of the theorems.** `artifacts/verify/` (the
spectral bound and its sharp family, the adaptivity families and the
scheduler; every command, exit code and output is recorded in
`artifacts/verify/OUTPUTS.md`), for example:

```sh
cd artifacts/verify
python3 -I chk_exact.py --max 15 --random 3000 --seed 7 --pell 6
```

`artifacts/hillclimb/` holds the solver and verifier reports, scripts and
recorded outputs for the results added in later drafts; `verified.md` has
the consolidated verdicts and each subdirectory's README the commands.

**Experiment E2 (spectral bound on real graphs).** `artifacts/e2/README.md`
gives the dataset URLs and SHA-256 digests, the Python environment (3.11.9,
numpy 2.4.6, scipy 1.17.1, numba 0.68.0) and the exact commands;
`check/csvcheck.py results.csv` audits the committed results for internal
consistency without the raw data; `check/rebuild_summary.py` runs
`src/summarize.py` on the committed `results.csv` and `spectral/` files
and checks that it reproduces `results.csv` and `summary.md` byte for
byte (on a fresh run `src/summarize.py` reads the uncommitted `out/`
directory instead); and `check/recompute.py` independently recomputes
sampled rows from the prepared data. All three need numpy.

**Engine runs.** `artifacts/engine/` (synthetic stores) and
`artifacts/engine-kg/` (knowledge-graph triangles, runs A, B and C) hold the
raw per-query rows, the query files, the summary scripts and the logs. The
tables in the paper rebuild from the committed rows with the scripts there.
Re-running the engine itself needs the Leatherback builds named in
`artifacts/README.md`, which becomes possible once Leatherback is
open-sourced.

**The Lean formalization.** With [`elan`](https://github.com/leanprover/elan)
installed:

```sh
cd lean
lake exe cache get
lake build
```

`lake build` kernel-checks every module and both audits
(`LeatherbackSpectralAudit`, `LeatherbackAudit`); it fails if any audited
theorem depends on an axiom beyond `propext`, `Classical.choice` and
`Quot.sound`. Lean `v4.32.2` and mathlib `v4.32.2` are pinned. See
[`lean/README.md`](lean/README.md).

**Scrub check.**

```sh
python3 -I tools/scrub_check.py    # exit 0 when clean
```

## Use of AI tools (summary)

Generative AI was used throughout this work: to search for and prove
theorems, to write and run the exact-arithmetic checks and the Lean proofs,
to implement and measure the engine operator, to draft and revise the text,
and to review it. Orchestration, implementation and drafting were done with
Claude Code (Claude Opus 5.5, Anthropic), with Claude subagents for theorem
search, proofs, internal refereeing, verification and audits; solvers and
verifiers for results added in later drafts were Claude Fable 5.1 agents
and Codex CLI agents (OpenAI, GPT-6-Astra). All reviews of the drafts were
model-based, including a final review by Weaver, TJC's internal work agent;
no human referee has reviewed this work. The author directed the work,
checked the results he relies on, and is responsible for every claim; no AI
system is an author. The paper's section "Use of AI tools" gives the full
statement and the provenance table of who produced and who checked each
result.

## Not included

- **Review reports.** The model-based review reports, including Weaver's
  review memo, are not published here: the memo is marked internal and
  confidential. The paper's "Use of AI tools" section and verification
  appendix summarize what each review checked and what changed.
- **Raw datasets and generated graphs.** Not committed; each
  `artifacts/*/README.md` gives the download or generation commands and the
  SHA-256 digests.
- **Internal working notes.** One internal status memo from the solver
  lanes (merge planning for the engine) and the response-to-referees letter
  are not included; neither is cited by the paper.

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

The MIT license in `LICENSE` covers the code and data in this repository (scripts,
the Lean sources under lean/, tools/, weaver-checks/ and artifacts/) except the
paper. The paper text and figures under paper/ are licensed separately under
CC BY 4.0; see paper/LICENSE. Third-party datasets referenced by the artifacts
(SNAP graphs, CoDEx, Wikidata5M) keep their own licenses, and the Lean package
depends on mathlib (Apache-2.0).
