# Hill-climb reports (revision 3 theory)

Three research reports and their consolidated verification, archived so that every
new theorem of revision 3 that cites them can be traced to a proof and to an exact
check. All scripts are standard-library Python, run as `python3 -I <script>` from
the directory that contains them; load-bearing arithmetic is integer or `Fraction`.

| Path | Content | Paper (revision 3) |
|---|---|---|
| `verified.md` | Verdicts (51 ACCEPT, 4 REPAIR, 0 REJECT) and paper-ready statements | all items below |
| `P1-sorted/report.md` | Sorted fresh-call comparison model: certificates, G8 / F_{i,j} / separations without log loss, the (log N)^{1/4} upper bound and its necessity, engine port | §"Sorted intersections" |
| `P1-sorted/engine/` | `gallop_port.py` (port of `intersectEachBy`/`intersectWalk`), `measure_g8.py` (rewrites `g8_counts.json`, about 1 s) | engine-port remark |
| `P1-sorted/slopes/` | `verify_families.py`, `log_normalized_checks.py`, `log_normalized_finite.py` (the h = 4 integer check) with recorded outputs; `log_normalized_proof.md` is the quarter-log proof (`quarter_log_*` is an earlier draft of the same argument) | quarter-log theorem |
| `P1-sorted/separations/` | `check.py` and `exact-output.txt` (F_a, GMR, GMIN, padded GMIN, H_a certificates) | sorted separations |
| `P2-exponents/report.md` | Second per-binding bound, slopes (9/10, 1), best of six 6/5, one order 5/4, fully reduced [1/12, 1/8] | §5.2-5.4 additions |
| `P2-exponents/*.py` | `verify_new_upper.py`, `verify_slopes.py`, `best_six_verify.py`, `verify_single_order.py`, `verify_fully_reduced.py` (the last enumerates v = 4 literally: about 30 s and 3 GB) | same |
| `P3-spectral/report.md` | Two measured norms, six-term irredundancy, planner corollary, 4-cycle obstruction | §3-4 additions |
| `P3-spectral/*.py` | `two_norms_exact.py`, `p3_independent_checks.py`, `cycle4_obstruction.py` | same |
| `checks/selfjoin_check.py` | Single-predicate embedding (G8, F_a, GMIN), symmetric predicate, the Theorem 5.3 signed-H counterexample | single-predicate section, proof of thm-pb-upper |
| `checks/selfjoin_connected.py` | Padded G8 as one predicate plus one X-to-X tuple: pairwise reduced, connected, (N, C, B2, Out) for m = 2, 3 | single-predicate section |
| `checks/d_gadget_check.py` | Literal D(L,a,h) statistics and the D1-D3 placement at p = q = 1 | thm-pb-asym |
| `checks/slopes_check.py` | Real-slope extension of F_{i,j}, D-family closed forms, sorted-model price identities, randomized-variant arithmetic | cor-real-slopes, thm-pb-asym |

Every script above was re-run from this layout before archiving; the P1 outputs match the
recorded `*_output.txt` / `exact-output.txt` byte for byte, and `measure_g8.py` reproduces
`g8_counts.json` exactly. The verifier lenses' own scripts are summarized in `verified.md`
and are not archived.

## Revision 4

Two results added in revision 4, the engine audit behind the revised §"Engine details
and measurements", and their independent verifications. Each result was rebuilt by two
verifiers who did not run or import the solvers' scripts; all load-bearing arithmetic is
integer or `Fraction`, run as `python3 -I`. Machine-local paths in the reports are replaced
by `./` or a placeholder.

| Path | Content | Paper (revision 4) |
|---|---|---|
| `r4-fullred/astra/REPORT.md`, `LP_REPORT.md` | Verifier A: the live gadget rebuilt literally (`live_audit.py`, `live_*.out`), the cost lemma, exact identities and dual certificates capping the live design at 1/10, the refutation of "1/11 at slope 1" as a normalization artifact and its repair by isolated-triangle padding (`lp_audit_*.py`, `.out`); `TRIANGLE_REPORT.md` and `triangle_audit_*` re-check the triangle two-norm and slope-profile statements; `reproduce.sh` runs every script | `thm-fullred`, `lem-live`, `rem-window` |
| `r4-fullred/fable/` | Verifier B: independent rebuild of the live gadget and of L(v) (`live_gadget.py`, `check_live.py`, `check_family.py`), the revision-3 gadget I_v (`check_iv.py`), the exact design-space LP (`lp_design.py`, `lp_near1.py`, `lp_profile_fine.py`) and random fuzzing of the upper bounds (`fuzz.py`); outputs in `out_*.txt`. See `README.md` there | same |
| `r4-fullred/editor/` | The editor's own literal rebuild of the gadget from the paper's description (L(2), L(3), the general family at (2,1,2), the padded family at v = 2, 3), the rotated-star two-norm example, and the 4-cycle sharpness family | `thm-fullred`, `rem-window`, `cor-planner2`, `prop-cycle4-sharp` |
| `r4-cycle4/astra/paper_ready_statement.md`, `proof_audit.md` | Verifier A for the 4-cycle: line-by-line proof audit (Lemma Λ, F, G, H), the corrected threshold L >= t^3, ten dihedral orbits, the rounding display; `lp_audit.md`, `rounding_audit.md`, scripts `proof_exact.py`, `lp_independent.py`, `round_independent.py`, `verify_independent.py` with outputs | `thm-cycle4`, `lem-lambda`, `prop-cycle4-sharp` |
| `r4-cycle4/astra-lane2/` | A second independent audit of the 4-cycle (fraction-free dual enumeration, exhaustive 2x2x2x2 instances, literal arc matrices) | same |
| `r4-cycle4/fable/` | Verifier B: exact dual enumeration (50 vertices, 38 needed, `s1_dual`), arc instances attaining every term (`s2_arcs`), exact certification of all terms on exhaustive and random 0/1 instances (`s3_*`), rounding grids (`s4_*`), the sharpness family (`s5_t4t5`), Lemma Λ annealing (`s6_*`), small-grid gaps (`s7_gap`) | same |
| `r4-cycle4/solver/` | The solver's scripts and outputs for the 4-cycle theorem | same |
| `r4-engine-audit/` | Independent audit of the rescue stage in build R1 (the first version of the rescue stage): exact re-aggregation of the run-B tables (imputed baseline made explicit), the 31,000-tuple counterexample to decision-preserving candidate pruning, the synthetic-control ratios, a second review of the counterexample against the source, and (`second-audit/`) the audit of the fix (build R2): a port matched against the full rule on 2.8M cases, sabotage controls, the witness failing on build R1, and run C's table recomputed | §"Engine details and measurements" |

All scripts in `r4-*` were re-run from this layout before archiving where they finish in
minutes; `proof_exact.py`, `s5_t4t5.py`, `check_live.py` and `lp_audit_general.py` reproduce
their recorded outputs byte for byte.
