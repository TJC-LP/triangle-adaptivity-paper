import LeatherbackSpectral.Lower
import LeatherbackSpectral.Degenerate

/-!
# The factor 4 of Theorem B is sharp: `inf W/U = 1/4`

Theorem B (`theoremB`) gives `U/4 < W ≤ U` in the regular regime. This file shows that the
factor `4` cannot be improved: there are regular statistics with `W = 1` and `U` arbitrarily
close to `4`.

**The family** (`sharpStats t`, `1 ≤ t < 2`):

  `r_R = r_T = t²`, `r_S = t`, `σ_R = σ_T = √t`, `σ_S = 1`,

so `s_R = s_T = t`, `s_S = 1`, the three Hölder terms and four of the degree terms equal
`t²`, and `U = t²` (`sharpStats_U`). But every admissible instance has `|S| ≤ t < 2`, so
`|S| ≤ 1`, and every out-degree of `T` is at most `‖A_T‖² ≤ t < 2`, so at most `1`; hence
`Out ≤ 1` (`sharpStats_out_le_one`). A single triangle is admissible (`sharpStats_witness`),
so `W = 1` while `U = t² → 4` as `t → 2`.

The referee's rational Pell choice `t = p²/q²` with `p² - 2q² = -1` is the special case
that keeps every statistic rational; over `ℝ` any `t ∈ [1, 2)` works.

* `sharp_family`: the family's five facts for one `t`.
* `factor_four_sharp`: `∀ ε > 0, ∃` regular statistics with every admissible `Out ≤ 1`, an
  admissible instance with `Out = 1`, and `4 - ε < U`.
* `theoremB_constant_sharp`: `inf W/U = 1/4`, two-sided, without forming `W`: every regular
  `st` has an admissible instance with `U/4 < Out`, and for every `c > 1/4` some regular
  `st` has `Out ≤ c · U` on every admissible instance.
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

/-- The sharp family: `r = (t², t, t²)`, `σ = (√t, 1, √t)`. -/
noncomputable def sharpStats (t : ℝ) : Stats where
  rR := t ^ 2
  rS := t
  rT := t ^ 2
  σR := √t
  σS := 1
  σT := √t

variable {t : ℝ}

/-- For `t ≥ 1` the family is regular. -/
lemma sharpStats_regular (h1 : 1 ≤ t) : (sharpStats t).Regular :=
  ⟨one_le_pow₀ h1, h1, one_le_pow₀ h1, Real.one_le_sqrt.2 h1, le_rfl, Real.one_le_sqrt.2 h1⟩

/-- For `t ≥ 1`, `U = t²`. -/
theorem sharpStats_U (h1 : 1 ≤ t) : (sharpStats t).U = t ^ 2 := by
  have ht0 : 0 ≤ t := by linarith
  have hsq : √t ^ 2 = t := Real.sq_sqrt ht0
  have htt : t ≤ t ^ 2 := by nlinarith
  have hsR : (sharpStats t).sR = t := by
    simp only [Stats.sR, sharpStats, hsq]; exact min_eq_left htt
  have hsS : (sharpStats t).sS = 1 := by
    simp only [Stats.sS, sharpStats, one_pow]; exact min_eq_left h1
  have hsT : (sharpStats t).sT = t := by
    simp only [Stats.sT, sharpStats, hsq]; exact min_eq_left htt
  have h4 : √(t ^ 4) = t ^ 2 := by
    rw [show t ^ 4 = (t ^ 2) ^ 2 by ring]; exact Real.sqrt_sq (by positivity)
  have h4' : ∀ P : ℝ, P = t ^ 4 → √P = t ^ 2 := fun P hP => hP ▸ h4
  have hHR : (sharpStats t).HR = t ^ 2 := by
    rw [Stats.HR, hsR]; simp only [sharpStats]; exact h4' _ (by ring)
  have hHS : (sharpStats t).HS = t ^ 2 := by
    rw [Stats.HS, hsS]; simp only [sharpStats]; exact h4' _ (by ring)
  have hHT : (sharpStats t).HT = t ^ 2 := by
    rw [Stats.HT, hsT]; simp only [sharpStats]; exact h4' _ (by ring)
  have ht3 : t ^ 2 ≤ t ^ 2 * t := le_mul_of_one_le_right (sq_nonneg t) h1
  apply le_antisymm
  · refine (sharpStats t).U_le_DRS.trans ?_
    rw [Stats.DRS, hsS]; simp [sharpStats]
  · refine (sharpStats t).le_U hHR.ge hHS.ge hHT.ge ?_ ?_ ?_ ?_ ?_ ?_
    · rw [Stats.DRS, hsS]; simp [sharpStats]
    · rw [Stats.DRT, hsT]; exact ht3
    · rw [Stats.DSR, hsR]; simp [sharpStats, sq]
    · rw [Stats.DST, hsT]; simp [sharpStats, sq]
    · rw [Stats.DTR, hsR]; exact ht3
    · rw [Stats.DTS, hsS]; simp [sharpStats]

/-- A natural number below `2` is at most `1`, read off a real bound `n ≤ t < 2`. -/
lemma natCast_le_one_of_le_lt_two {n : ℕ} (hn : (n : ℝ) ≤ t) (h2 : t < 2) : (n : ℝ) ≤ 1 := by
  have : n < 2 := by exact_mod_cast hn.trans_lt h2
  exact_mod_cast Nat.lt_succ_iff.1 this

/-- **`W ≤ 1`.** For `1 ≤ t < 2`, every admissible instance of the family has `Out ≤ 1`. -/
theorem sharpStats_out_le_one (h1 : 1 ≤ t) (h2 : t < 2) {X Y Z : Type*} [Fintype X]
    [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y] [DecidableEq Z]
    (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X))
    (h : Admissible (sharpStats t) R S T) : out R S T ≤ 1 := by
  obtain ⟨-, hS, -, -, -, hσT⟩ := h
  have hS1 : (S.card : ℝ) ≤ 1 := natCast_le_one_of_le_lt_two hS h2
  have hT1 : ∀ z, rowDeg T z ≤ 1 := fun z => by
    have hd := rowDeg_le_opNorm_sq T z
    have hn : ‖adj T‖ ^ 2 ≤ t :=
      (pow_le_pow_left₀ (norm_nonneg _) hσT 2).trans_eq (Real.sq_sqrt (by linarith))
    rw [rowDeg_eq_card] at hd ⊢
    exact natCast_le_one_of_le_lt_two (hd.trans hn) h2
  calc out R S T = out S T R := out_rotate' R S T
    _ ≤ S.card * 1 := out_le_card_mul_of_rowDeg_le S T R hT1
    _ ≤ 1 := by linarith

/-- **`W ≥ 1`.** For `t ≥ 1`, a single triangle (`blk 1 1 1` three times) is admissible
and has `Out = 1`. -/
theorem sharpStats_witness (h1 : 1 ≤ t) :
    Admissible (sharpStats t) (blk 1 1 1) (blk 1 1 1) (blk 1 1 1) ∧
      out (blk 1 1 1) (blk 1 1 1) (blk 1 1 1) = 1 := by
  have hc : ((blk 1 1 1).card : ℝ) = 1 := by rw [card_blk]; norm_num
  have hn : ‖adj (blk 1 1 1)‖ ≤ 1 := opNorm_blk_le.trans_eq (by norm_num)
  have hst : (1 : ℝ) ≤ √t := Real.one_le_sqrt.2 h1
  have ht2 : (1 : ℝ) ≤ t ^ 2 := one_le_pow₀ h1
  refine ⟨⟨?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩
  · rw [hc]; exact ht2
  · rw [hc]; exact h1
  · rw [hc]; exact ht2
  · exact hn.trans hst
  · exact hn
  · exact hn.trans hst
  · rw [out_blk]; norm_num

/-- **The sharp family.** For `1 ≤ t < 2`, `sharpStats t` is regular, `U = t²`, every
admissible instance has `Out ≤ 1`, and a single triangle is admissible with `Out = 1`:
so `W = 1` and `U / W = t²`. -/
theorem sharp_family (h1 : 1 ≤ t) (h2 : t < 2) :
    (sharpStats t).Regular ∧ (sharpStats t).U = t ^ 2 ∧
      (∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
        [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
        Admissible (sharpStats t) R S T → out R S T ≤ 1) ∧
      Admissible (sharpStats t) (blk 1 1 1) (blk 1 1 1) (blk 1 1 1) ∧
      out (blk 1 1 1) (blk 1 1 1) (blk 1 1 1) = 1 :=
  ⟨sharpStats_regular h1, sharpStats_U h1,
    fun _ _ _ _ _ _ _ _ _ R S T h => sharpStats_out_le_one h1 h2 R S T h,
    (sharpStats_witness h1).1, (sharpStats_witness h1).2⟩

/-- **The factor 4 is sharp.** For every `ε > 0` there are regular statistics whose every
admissible instance has `Out ≤ 1`, with an admissible instance of `Out = 1` (so `W = 1`),
and `U > 4 - ε`. -/
theorem factor_four_sharp (ε : ℝ) (hε : 0 < ε) :
    ∃ st : Stats, st.Regular ∧
      (∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
        [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
        Admissible st R S T → out R S T ≤ 1) ∧
      (∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z) (_ : DecidableEq X)
        (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T ∧ out R S T = 1) ∧
      4 - ε < st.U := by
  set δ := min (1 / 2 : ℝ) (ε / 5) with hδ
  have hδpos : 0 < δ := lt_min (by norm_num) (by linarith)
  have hδh : δ ≤ 1 / 2 := min_le_left _ _
  have hδε : δ ≤ ε / 5 := min_le_right _ _
  have h1 : (1 : ℝ) ≤ 2 - δ := by linarith
  have h2 : 2 - δ < 2 := by linarith
  obtain ⟨hreg, hU, hle, hadm, hout⟩ := sharp_family h1 h2
  refine ⟨sharpStats (2 - δ), hreg, hle, ⟨_, _, _, inferInstance, inferInstance, inferInstance,
    inferInstance, inferInstance, inferInstance, _, _, _, hadm, hout⟩, ?_⟩
  rw [hU]
  nlinarith

/-- **`inf W/U = 1/4`**, stated two-sidedly since `W` is not a Lean object.
(i) Every regular `st` has an admissible instance with `U/4 < Out`, so `W/U > 1/4`
(`theoremB`). (ii) For every `c > 1/4` there are regular statistics with `Out ≤ c · U` on
every admissible instance, so `W/U ≤ c`. -/
theorem theoremB_constant_sharp :
    (∀ st : Stats, st.Regular →
      ∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z) (_ : DecidableEq X)
        (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T ∧ st.U / 4 < out R S T) ∧
      ∀ c : ℝ, 1 / 4 < c → ∃ st : Stats, st.Regular ∧
        ∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
          [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
          Admissible st R S T → out R S T ≤ c * st.U := by
  refine ⟨fun st h => ?_, fun c hc => ?_⟩
  · obtain ⟨X, Y, Z, i1, i2, i3, i4, i5, i6, R, S, T, hadm, hlt⟩ := (theoremB st h).2
    exact ⟨X, Y, Z, i1, i2, i3, i4, i5, i6, R, S, T, hadm, by linarith⟩
  · have hc0 : 0 < c := by linarith
    have hinv : 1 / c < 4 := by
      rw [div_lt_iff₀ hc0]; linarith
    obtain ⟨st, hreg, hle, -, hU⟩ := factor_four_sharp (4 - 1 / c) (by linarith)
    refine ⟨st, hreg, fun X Y Z _ _ _ _ _ _ R S T hadm => (hle X Y Z R S T hadm).trans ?_⟩
    have : 1 / c < st.U := by linarith
    rw [div_lt_iff₀ hc0] at this
    linarith

end LeatherbackSpectral
