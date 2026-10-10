# Verification scripts

These are independent numerical checks of the paper's theorems and families.
Each one exits 0 only if every assertion holds. `OUTPUTS.md` records the
command, exit code, wall time and full output of each run.

Environment: Python 3.11.9. `chk.py` needs `numpy`; the run used
`numpy==2.4.6` from the E2 venv (`../e2/README.md`). Every other script uses
only the standard library. Run everything with `python3 -I`.

## Internal names and paper numbering

The scripts, their comments and the run labels below use the internal names
of an earlier draft. This table maps them to the numbering of revision 2 of
`spectral_agm.typ` and to the paper's stable Typst labels.

| Internal name (scripts, outputs) | Paper, revision 2 | Typst label |
|---|---|---|
| Theorem B (spectral AGM) | Theorem 3.1 | `thm-main` |
| "the constant 4 is best possible", Pell family | Theorem 3.7 and the paragraph after it | `thm-sharp` |
| Lemma 1.2 (`M_i² ≤ 4|R||S||T|`, a weaker form of the last bound) | Lemma 5.1 (sum identities; `M_π ≤ √(|R||S||T|)`) | `lem-sum` |
| Prop. 1.3 (`min M ≤ (ΛΛ')^{1/3}`, checked as `min M⁶ ≤ αβγα'β'γ'`) | Corollary 5.4(3) | `cor-pb` |
| Lemma 1.4 (per-root bounds) | Lemma 5.2 | `lem-perroot` |
| Theorem A / Theorem 1.U (`A` = the per-binding cost `C`) | Theorem 5.3 | `thm-pb-upper` |
| Theorem 1.L (G₈ and its rotation union) | Theorem 5.5 (values in Table 4) | `thm-pb-lower`, `tab-g8-values` |
| Theorem 1.L' (F_{i,j} slope families) | Theorem 5.9 | `thm-pb-slopes` |
| Theorem 2(a) (family `2a` = 𝓕_a; GMR) | Theorem 5.10(1) | `thm-sep` |
| Theorem 2(b) (GMIN and padded GMIN) | Theorem 5.10(2) | `thm-sep` |
| padding | Lemma 5.7 | `lem-pad` |
| Proposition 3 (scheduler; statistic `P3`) | Proposition 5.14 and Remark 5.15 | `prop-ptr`, `rem-ptr` |
| Proposition 4 (Ferrers family `fer`) | Proposition 5.16 | `prop-ferrers` |

Result numbers can shift between revisions; the labels do not.

## Theorem B (spectral AGM)

| Script | Usage | Checks |
|---|---|---|
| `chk_exact.py` | `python3 -I chk_exact.py [--max 15] [--random 3000] [--seed 7] [--pell 6]` | **Exact arithmetic only** (integers and `Fraction`; U is carried as U², so there are no square roots). (1) Exhaustive grid `1 ≤ s_i ≤ r_i ≤ MAX`: the floored block (a, b, c, m) satisfies all six size and degree/norm feasibility inequalities with m ≥ 1, and `U < 4mabc`. The relaxed real shape is feasible, has m* ≥ 1, and has value exactly U. The script prints the exact maximum of U/(mabc). (2) Random 0/1 instances: `Out ≤ U` for the instance's own statistics, certified exactly. σ² is replaced by a rational lower bound ρ ≤ σ², the largest of several Rayleigh quotients of AᵀA (unit vectors, rows of A, and integer power iterates of 𝟙), and U is monotone in σ. (3) The Pell sharpness family (Theorem "the constant 4 is best possible", Section 4): `p² − 2q² = −1`, `U = t²` exactly, the construction is (1,1,1,1), and `U/W = t² → 4`. |
| `chk.py` | `python3 -I chk.py` (no arguments; needs numpy) | The original floating-point check: `Out/U` on 3,000 random instances, and the construction ratio `U/mabc` on 200,000 random log-uniform statistics. Superseded by `chk_exact.py` for every load-bearing claim and kept for provenance. |

## Per-binding results (Theorems 1.U, 1.L, 2; Propositions 3, 4)

| Script | Usage | Checks |
|---|---|---|
| `g8.py` | `python3 -I g8.py` (fixed m = 2, 3) | Independent check of the G₈ gadget and its rotation union, in cycle form. It asserts the closed forms `(C_x, C_y, C_z) = (m⁹+m⁶, m⁵, m⁸)`, N, the forward squared-degree sums, and the union's `C = m⁹+m⁸+m⁶+m⁵`. |
| `thm1/ev.py` | library | The literal per-binding evaluator, with the corrected root-z row: C_x, C_y, C_z, M_R, M_S, M_T, and all six squared-degree sums. |
| `thm1/fams.py` | `python3 -I thm1/fams.py G8 <m…>` and `python3 -I thm1/fams.py F <i> <j> <u…>` | Theorem 1.L (G₈ and its union) and the F_{i,j} slope families. Every closed form is asserted in integers. |
| `thm1/fams2.py` | `python3 -I thm1/fams2.py {2a\|min\|mr\|fer} <m…>` | Theorem 2(a): fixed order, family `2a`. GMR (`mr`) and GMIN (`min`), each with its semijoin-reduced padding. Proposition 4: the Ferrers family (`fer`). |
| `thm1/rnd.py` | `python3 -I thm1/rnd.py <seed> <n>` | n random instances drawn from uniform, power-law, block and star relations. Checked exactly as integer inequalities: Lemma 1.4 per root (forward and reflected, 8th-power form) and Theorem 1.U (8th-power form). Also checked: `min M ≤ (ΛΛ')^{1/3}` (as `min M^6 ≤ αβγ·α'β'γ'`), `M_i² ≤ 4|R||S||T|`, and Proposition 3's scheduler, which must pick an optimal root with total ≤ 6C + 4n + 6. |

Floats appear only in printed ratios (`B2`, `A/(N+B2)` and the like), never
in an assertion. The exception is `chk.py`, which `chk_exact.py` supersedes.

## What these scripts do not reproduce

Some numbers in the paper come from scripts that are **not** included here
and were not located when these artifacts were assembled:

- the "10⁴ random instances and adversarial hill-climbing, worst ratio 0.75"
  check of Theorem 1.U;
- the "2 × 10⁴ random instances and 40 hill-climb restarts" check of the
  price-then-run scheduler;
- the "worst measured (pricing − 4n)/C = 2.33 (2.83 under hill-climbing)" figure;
- the annealing and brute-force search behind "largest ratios C/(N+B₂)
  between 0.45 and 0.66".

`rnd.py` is a smaller random check, 4,500 instances. Its scheduler statistic
`P3 = (total steps − 4·#bindings)/C` reaches 3.5 at seed 1, and 3.0–3.2 at
seeds 0, 2, 3, 7 and 42. That exceeds the paper's quoted 2.33/2.83, though it
stays within the proved bound of 6. The step accounting in `rnd.py`
(3 units per binding for the vertex transition and two degree reads) may
differ from the one behind the quoted figure. The paper now cites `rnd.py`'s
statistic (between 3.0 and 3.5) and marks the earlier figures as coming from
a script that was not preserved.
