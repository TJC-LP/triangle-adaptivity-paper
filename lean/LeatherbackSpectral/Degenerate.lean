import LeatherbackSpectral.Lower
import LeatherbackSpectral.Kernel

/-!
# The degenerate regime, and a limit of Lemma 1

* `theoremB_degenerate`: outside the regular regime (some `r_i < 1` or some `σ_i < 1`),
  every admissible instance has `Out = 0`, i.e. `W = 0`. Together with `theoremB` this
  covers all statistics.
* Nonnegativity convention: `admissible_exists_iff_nonneg` shows some instance is
  admissible iff all six statistics are `≥ 0`. With a negative bound the admissible class
  is empty, `theoremB_degenerate` holds vacuously, and `W = 0` is the convention
  `sup ∅ = 0`. With nonnegative statistics `theoremB_degenerate_attained` shows the class
  is nonempty, so `W = 0` is attained (by the empty instance).
* `theoremB_cases`: the universal upper bound `Out ≤ U`, together with the regular /
  degenerate dichotomy.
* `nestS_can_raise_opNorm`: nesting (Lemma 1) preserves `S`'s out-degree vector and its
  size but NOT its operator norm (nor, in general, its in-degree vector). A 2×2 matching (`‖·‖ ≤ 1`) nests to a relation with `‖·‖² ≥ 2`.
  This is why Lemma 1 is only combined with the terms `H_R` and the degree terms, never
  with `σ_S` or `σ_T` for the nested relations.
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

section Empty

variable {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]

/-- A relation whose size is bounded by some `r < 1` is empty. -/
lemma eq_empty_of_card_le_of_lt_one {R : Finset (X × Y)} {r : ℝ} (h : (R.card : ℝ) ≤ r)
    (hr : r < 1) : R = ∅ := by
  have : (R.card : ℝ) < 1 := h.trans_lt hr
  exact Finset.card_eq_zero.1 (by exact_mod_cast Nat.lt_one_iff.1 (by exact_mod_cast this))

/-- A relation whose operator norm is bounded by some `σ < 1` is empty (by N5). -/
lemma eq_empty_of_opNorm_le_of_lt_one {R : Finset (X × Y)} {σ : ℝ} (h : ‖adj R‖ ≤ σ)
    (hσ : σ < 1) : R = ∅ := by
  by_contra hne
  obtain ⟨⟨x, y⟩, hm⟩ := Finset.nonempty_iff_ne_empty.2 hne
  linarith [one_le_opNorm_adj R hm]

end Empty

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

lemma out_empty_left (S : Finset (Y × Z)) (T : Finset (Z × X)) :
    out (∅ : Finset (X × Y)) S T = 0 := by
  have h := out_le_card_mul_opNorm_sq_S (∅ : Finset (X × Y)) S T
  simp only [Finset.card_empty, Nat.cast_zero, zero_mul] at h
  exact le_antisymm h (out_nonneg _ _ _)

lemma out_empty_mid (R : Finset (X × Y)) (T : Finset (Z × X)) :
    out R (∅ : Finset (Y × Z)) T = 0 := by
  rw [out_rotate']; exact out_empty_left _ _

lemma out_empty_right (R : Finset (X × Y)) (S : Finset (Y × Z)) :
    out R S (∅ : Finset (Z × X)) = 0 := by
  rw [out_rotate]; exact out_empty_left _ _

/-- **Theorem B, degenerate regime.** If the statistics are not regular (some `r_i < 1` or
some `σ_i < 1`), every admissible instance has `Out = 0`; hence `W = 0` there.

No sign condition is assumed. If some statistic is negative, no instance is admissible
(`admissible_exists_iff_nonneg`) and the statement is vacuous; reading it as `W = 0` then
uses the convention `sup ∅ = 0`. For nonnegative statistics the admissible class is
nonempty and `W = 0` is attained (`theoremB_degenerate_attained`). -/
theorem theoremB_degenerate (st : Stats) (hreg : ¬ st.Regular) (R : Finset (X × Y))
    (S : Finset (Y × Z)) (T : Finset (Z × X)) (h : Admissible st R S T) : out R S T = 0 := by
  obtain ⟨hR, hS, hT, hσR, hσS, hσT⟩ := h
  have hcases : st.rR < 1 ∨ st.rS < 1 ∨ st.rT < 1 ∨ st.σR < 1 ∨ st.σS < 1 ∨ st.σT < 1 := by
    by_contra hc
    simp only [not_or, not_lt] at hc
    obtain ⟨h1, h2, h3, h4, h5, h6⟩ := hc
    exact hreg ⟨h1, h2, h3, h4, h5, h6⟩
  rcases hcases with h | h | h | h | h | h
  · rw [eq_empty_of_card_le_of_lt_one hR h]; exact out_empty_left _ _
  · rw [eq_empty_of_card_le_of_lt_one hS h]; exact out_empty_mid _ _
  · rw [eq_empty_of_card_le_of_lt_one hT h]; exact out_empty_right _ _
  · rw [eq_empty_of_opNorm_le_of_lt_one hσR h]; exact out_empty_left _ _
  · rw [eq_empty_of_opNorm_le_of_lt_one hσS h]; exact out_empty_mid _ _
  · rw [eq_empty_of_opNorm_le_of_lt_one hσT h]; exact out_empty_right _ _

/-- **Theorem B, all statistics.** Every admissible instance has `Out ≤ U`; in the regular
regime some admissible instance has `4 · Out > U`, and otherwise every admissible instance
has `Out = 0`. -/
theorem theoremB_cases (st : Stats) :
    (∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
        [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
        Admissible st R S T → out R S T ≤ st.U) ∧
    ((st.Regular ∧ ∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z)
        (_ : DecidableEq X) (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y))
        (S : Finset (Y × Z)) (T : Finset (Z × X)), Admissible st R S T ∧ st.U < 4 * out R S T) ∨
      (¬ st.Regular ∧ ∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X]
        [DecidableEq Y] [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T → out R S T = 0)) := by
  refine ⟨fun X Y Z _ _ _ _ _ _ R S T hadm => theoremB_upper st R S T hadm, ?_⟩
  by_cases h : st.Regular
  · exact Or.inl ⟨h, (theoremB st h).2⟩
  · exact Or.inr ⟨h, fun X Y Z _ _ _ _ _ _ R S T hadm => theoremB_degenerate st h R S T hadm⟩

/-! ### Nonnegativity: when the admissible class is nonempty -/

/-- The empty relation has incidence matrix `0`, hence operator norm `0`. -/
lemma opNorm_adj_empty {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X']
    [DecidableEq Y'] : ‖adj (∅ : Finset (X' × Y'))‖ = 0 := by
  have h : adj (∅ : Finset (X' × Y')) = 0 := by ext x y; simp [adj]
  rw [h, norm_zero]

/-- **Nonnegativity convention.** Some instance is admissible for `st` iff all six
statistics are nonnegative. With a negative bound the admissible class is empty. -/
theorem admissible_exists_iff_nonneg (st : Stats) :
    (∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z) (_ : DecidableEq X)
        (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T) ↔
      0 ≤ st.rR ∧ 0 ≤ st.rS ∧ 0 ≤ st.rT ∧ 0 ≤ st.σR ∧ 0 ≤ st.σS ∧ 0 ≤ st.σT := by
  constructor
  · rintro ⟨X, Y, Z, _, _, _, _, _, _, R, S, T, hR, hS, hT, hσR, hσS, hσT⟩
    exact ⟨(Nat.cast_nonneg _).trans hR, (Nat.cast_nonneg _).trans hS,
      (Nat.cast_nonneg _).trans hT, (norm_nonneg _).trans hσR, (norm_nonneg _).trans hσS,
      (norm_nonneg _).trans hσT⟩
  · rintro ⟨hR, hS, hT, hσR, hσS, hσT⟩
    refine ⟨Unit, Unit, Unit, inferInstance, inferInstance, inferInstance, inferInstance,
      inferInstance, inferInstance, ∅, ∅, ∅, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
      simp only [Finset.card_empty, Nat.cast_zero, opNorm_adj_empty] <;> assumption

/-- **Degenerate regime, attained.** For nonnegative, non-regular statistics the admissible
class is nonempty and every member has `Out = 0`: `W = 0` is a maximum, not a vacuous
supremum. -/
theorem theoremB_degenerate_attained (st : Stats) (hreg : ¬ st.Regular)
    (hnn : 0 ≤ st.rR ∧ 0 ≤ st.rS ∧ 0 ≤ st.rT ∧ 0 ≤ st.σR ∧ 0 ≤ st.σS ∧ 0 ≤ st.σT) :
    (∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z) (_ : DecidableEq X)
        (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T ∧ out R S T = 0) ∧
      ∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
        [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
        Admissible st R S T → out R S T = 0 := by
  refine ⟨?_, fun X Y Z _ _ _ _ _ _ R S T hadm => theoremB_degenerate st hreg R S T hadm⟩
  obtain ⟨X, Y, Z, i1, i2, i3, i4, i5, i6, R, S, T, hadm⟩ :=
    (admissible_exists_iff_nonneg st).2 hnn
  exact ⟨X, Y, Z, i1, i2, i3, i4, i5, i6, R, S, T, hadm, theoremB_degenerate st hreg R S T hadm⟩

/-! ### Nesting does not preserve operator norms -/

/-- The 2×2 matching (identity relation on `Fin 2`). -/
def diag2 : Finset (Fin 2 × Fin 2) := univ.filter fun p => p.1 = p.2

lemma outN_diag2 (y : Fin 2) : outN diag2 y = 1 := by
  fin_cases y <;> decide

lemma colN_diag2 (z : Fin 2) : (univ.filter fun y => (y, z) ∈ diag2).card = 1 := by
  fin_cases z <;> decide

/-- The matching has operator norm at most `1` (Schur test with `p = q = 1`). -/
theorem opNorm_adj_diag2_le : ‖adj diag2‖ ≤ 1 := by
  have h := opNorm_adj_le_schur diag2 zero_le_one zero_le_one
    (fun y => by rw [rowDeg_eq_card]; exact_mod_cast (outN_diag2 y).le)
    (fun z => by rw [colDeg_eq_card, colN_diag2]; norm_num)
  simpa using h

/-- Its nested version has a column of degree `2`, hence operator norm at least `√2`. -/
theorem two_le_opNorm_sq_nestS_diag2 : 2 ≤ ‖adj (nestS diag2)‖ ^ 2 := by
  set z0 : Fin 2 := (Fintype.equivFin (Fin 2)).symm ⟨0, by norm_num⟩
  have hz0 : ((Fintype.equivFin (Fin 2) z0 : Fin _) : ℕ) = 0 := by simp [z0]
  have hcol : colDeg (nestS diag2) z0 = 2 := by
    simp only [colDeg, adj_nestS, hz0, outN_diag2, Nat.lt_one_iff, if_true]
    simp
  have := colDeg_le_opNorm_sq (nestS diag2) z0
  linarith

/-- **Nesting can raise the operator norm.** `nestS` keeps the out-degree vector and the
size (`rowDeg_nestS`, `card_nestS`) — not the in-degree vector: here the column degrees go
from `(1, 1)` to `(2, 0)` — but here takes `‖A_S‖ ≤ 1` to `‖A_{S'}‖ ≥ √2`. -/
theorem nestS_can_raise_opNorm :
    ‖adj diag2‖ ≤ 1 ∧ 2 ≤ ‖adj (nestS diag2)‖ ^ 2 ∧ ‖adj diag2‖ < ‖adj (nestS diag2)‖ := by
  refine ⟨opNorm_adj_diag2_le, two_le_opNorm_sq_nestS_diag2, ?_⟩
  have h1 := opNorm_adj_diag2_le
  have h2 := two_le_opNorm_sq_nestS_diag2
  nlinarith [norm_nonneg (adj (nestS diag2)), norm_nonneg (adj diag2)]

end LeatherbackSpectral
