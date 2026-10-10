import LeatherbackSpectral.OpNorm

/-!
# Theorem B, upper bound: `Out ≤ U(r, σ)`, instance by instance, constant 1

* `out_le_opNorm_mul_sqrt` (Hölder term, §3 (H)): `Out ≤ ‖A_R‖ √(|S| |T|)`.
* `out_le_card_mul_opNorm_sq_*` (degree terms, §3 (D)).
* `Stats`, `Stats.U` (the nine-term minimum with clipped `s_i = min(σ_i², r_i)`),
  `Admissible`, and `theoremB_upper : Admissible st R S T → out R S T ≤ st.U`.
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

/-- **Theorem B, Hölder term `H_R` (N6).** `Out ≤ ‖A_R‖₂ √(|S| |T|)`. -/
theorem out_le_opNorm_mul_sqrt (R : Finset (X × Y)) (S : Finset (Y × Z))
    (T : Finset (Z × X)) :
    out R S T ≤ ‖adj R‖ * √((S.card : ℝ) * T.card) := by
  rw [out_rotate, out_eq_sum]
  -- `out T R S = ∑ z, ∑ x, ∑ y, A_T z x * A_R x y * A_S y z`
  have hz : ∀ z, ∑ x, ∑ y, adj T z x * adj R x y * adj S y z ≤
      ‖adj R‖ * (√(rowDeg T z) * √(colDeg S z)) := by
    intro z
    have h := bilinear_le (adj R) (fun x => adj T z x) (fun y => adj S y z)
    have hu : ∑ x, adj T z x ^ 2 = rowDeg T z := by simp [rowDeg, adj_sq]
    have hv : ∑ y, adj S y z ^ 2 = colDeg S z := by simp [colDeg, adj_sq]
    rw [hu, hv] at h
    linarith
  calc ∑ z, ∑ x, ∑ y, adj T z x * adj R x y * adj S y z
      ≤ ∑ z, ‖adj R‖ * (√(rowDeg T z) * √(colDeg S z)) := Finset.sum_le_sum fun z _ => hz z
    _ = ‖adj R‖ * ∑ z, √(rowDeg T z) * √(colDeg S z) := by rw [Finset.mul_sum]
    _ ≤ ‖adj R‖ * (√(∑ z, rowDeg T z) * √(∑ z, colDeg S z)) :=
        mul_le_mul_of_nonneg_left
          (Real.sum_sqrt_mul_sqrt_le _ (rowDeg_nonneg T) (colDeg_nonneg S)) (norm_nonneg _)
    _ = ‖adj R‖ * √((S.card : ℝ) * T.card) := by
        rw [sum_rowDeg, sum_colDeg, ← Real.sqrt_mul (Nat.cast_nonneg _), mul_comm (T.card : ℝ)]

/-- **Degree term `D_{R,S}` in operator-norm form.** `Out ≤ |R| ‖A_S‖²`. -/
theorem out_le_card_mul_opNorm_sq_S (R : Finset (X × Y)) (S : Finset (Y × Z))
    (T : Finset (Z × X)) : out R S T ≤ R.card * ‖adj S‖ ^ 2 :=
  out_le_card_mul_of_rowDeg_le R S T (rowDeg_le_opNorm_sq S)

/-- **Degree term `D_{R,T}` in operator-norm form.** `Out ≤ |R| ‖A_T‖²`. -/
theorem out_le_card_mul_opNorm_sq_T (R : Finset (X × Y)) (S : Finset (Y × Z))
    (T : Finset (Z × X)) : out R S T ≤ R.card * ‖adj T‖ ^ 2 :=
  out_le_card_mul_of_colDeg_le R S T (colDeg_le_opNorm_sq T)

/-! ### Statistics and the nine-term bound -/

/-- Statistics: size bounds `r_i` and operator-norm bounds `σ_i`. -/
structure Stats where
  rR : ℝ
  rS : ℝ
  rT : ℝ
  σR : ℝ
  σS : ℝ
  σT : ℝ

namespace Stats

variable (st : Stats)

/-- Clipped squared norms `s_i = min(σ_i², r_i)`. -/
noncomputable def sR : ℝ := min (st.σR ^ 2) st.rR
noncomputable def sS : ℝ := min (st.σS ^ 2) st.rS
noncomputable def sT : ℝ := min (st.σT ^ 2) st.rT

/-- Hölder terms `H_i = √(s_i r_j r_k)`. -/
noncomputable def HR : ℝ := √(st.sR * st.rS * st.rT)
noncomputable def HS : ℝ := √(st.sS * st.rT * st.rR)
noncomputable def HT : ℝ := √(st.sT * st.rR * st.rS)

/-- Degree terms `D_{i,j} = r_i s_j`. -/
noncomputable def DRS : ℝ := st.rR * st.sS
noncomputable def DRT : ℝ := st.rR * st.sT
noncomputable def DSR : ℝ := st.rS * st.sR
noncomputable def DST : ℝ := st.rS * st.sT
noncomputable def DTR : ℝ := st.rT * st.sR
noncomputable def DTS : ℝ := st.rT * st.sS

/-- `U(r, σ)`: the minimum of the nine terms. -/
noncomputable def U : ℝ :=
  min st.HR (min st.HS (min st.HT (min st.DRS (min st.DRT
    (min st.DSR (min st.DST (min st.DTR st.DTS)))))))

/-- A number below all nine terms is below `U`. -/
lemma le_U {v : ℝ} (h1 : v ≤ st.HR) (h2 : v ≤ st.HS) (h3 : v ≤ st.HT) (h4 : v ≤ st.DRS)
    (h5 : v ≤ st.DRT) (h6 : v ≤ st.DSR) (h7 : v ≤ st.DST) (h8 : v ≤ st.DTR)
    (h9 : v ≤ st.DTS) : v ≤ st.U := by
  unfold U
  simp only [le_min_iff]
  exact ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩

lemma U_le_HR : st.U ≤ st.HR := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_HS : st.U ≤ st.HS := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_HT : st.U ≤ st.HT := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DRS : st.U ≤ st.DRS := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DRT : st.U ≤ st.DRT := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DSR : st.U ≤ st.DSR := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DST : st.U ≤ st.DST := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DTR : st.U ≤ st.DTR := by unfold U; simp only [min_le_iff, le_refl]; tauto
lemma U_le_DTS : st.U ≤ st.DTS := by unfold U; simp only [min_le_iff, le_refl]; tauto

end Stats

/-- An instance is admissible for `st` when `|i| ≤ r_i` and `‖A_i‖₂ ≤ σ_i` for all three. -/
def Admissible (st : Stats) (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)) :
    Prop :=
  (R.card : ℝ) ≤ st.rR ∧ (S.card : ℝ) ≤ st.rS ∧ (T.card : ℝ) ≤ st.rT ∧
    ‖adj R‖ ≤ st.σR ∧ ‖adj S‖ ≤ st.σS ∧ ‖adj T‖ ≤ st.σT

/-- `√(min(σ², r) · P) = min(σ, √r) · √P`-style bound: if `v ≤ σ √P` and `v ≤ √r √P`
then `v ≤ √(min(σ², r) P)`. -/
lemma le_sqrt_min_mul {v σ r P : ℝ} (hσ : 0 ≤ σ) (hP : 0 ≤ P)
    (h1 : v ≤ σ * √P) (h2 : v ≤ √r * √P) : v ≤ √(min (σ ^ 2) r * P) := by
  rcases min_cases (σ ^ 2) r with ⟨hm, _⟩ | ⟨hm, _⟩
  · rw [hm, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq hσ]; exact h1
  · rw [hm]
    rcases le_total 0 r with hr | hr
    · rw [Real.sqrt_mul hr]; exact h2
    · rw [Real.sqrt_eq_zero'.2 (mul_nonpos_of_nonpos_of_nonneg hr hP)]
      rw [Real.sqrt_eq_zero'.2 hr, zero_mul] at h2; exact h2

/-- Degree bound packaged with clipping: degrees are `≤ min(σ², r)`. -/
lemma rowDeg_le_clip {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X'] [DecidableEq Y']
    (Q : Finset (X' × Y')) {σ r : ℝ} (hσ : ‖adj Q‖ ≤ σ) (hr : (Q.card : ℝ) ≤ r) (x : X') :
    rowDeg Q x ≤ min (σ ^ 2) r :=
  le_min ((rowDeg_le_opNorm_sq Q x).trans (pow_le_pow_left₀ (norm_nonneg _) hσ 2))
    ((rowDeg_le_card Q x).trans hr)

lemma colDeg_le_clip {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X'] [DecidableEq Y']
    (Q : Finset (X' × Y')) {σ r : ℝ} (hσ : ‖adj Q‖ ≤ σ) (hr : (Q.card : ℝ) ≤ r) (y : Y') :
    colDeg Q y ≤ min (σ ^ 2) r :=
  le_min ((colDeg_le_opNorm_sq Q y).trans (pow_le_pow_left₀ (norm_nonneg _) hσ 2))
    ((colDeg_le_card Q y).trans hr)

lemma clip_nonneg {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X'] [DecidableEq Y']
    (Q : Finset (X' × Y')) {σ r : ℝ} (hr : (Q.card : ℝ) ≤ r) : 0 ≤ min (σ ^ 2) r :=
  le_min (sq_nonneg _) ((Nat.cast_nonneg _).trans hr)

/-- Clipped Hölder term from an operator-norm Hölder bound. -/
lemma le_holder_clip (R : Finset (X × Y)) {nS nT : ℕ} {v rR rS rT σR : ℝ}
    (hR : (R.card : ℝ) ≤ rR) (hS : (nS : ℝ) ≤ rS) (hT : (nT : ℝ) ≤ rT) (hσR : ‖adj R‖ ≤ σR)
    (hv : v ≤ ‖adj R‖ * √((nS : ℝ) * nT)) : v ≤ √(min (σR ^ 2) rR * rS * rT) := by
  have hS0 : 0 ≤ rS := (Nat.cast_nonneg _).trans hS
  have hT0 : 0 ≤ rT := (Nat.cast_nonneg _).trans hT
  have hST : √((nS : ℝ) * nT) ≤ √(rS * rT) :=
    Real.sqrt_le_sqrt (mul_le_mul hS hT (Nat.cast_nonneg _) hS0)
  rw [mul_assoc]
  refine le_sqrt_min_mul ((norm_nonneg _).trans hσR) (mul_nonneg hS0 hT0) ?_ ?_
  · exact hv.trans (mul_le_mul hσR hST (Real.sqrt_nonneg _) ((norm_nonneg _).trans hσR))
  · refine hv.trans (mul_le_mul ?_ hST (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
    exact (opNorm_adj_le_sqrt_card R).trans (Real.sqrt_le_sqrt hR)

/-- The three terms "owned" by the `R`-rotation: `H_R`, `D_{R,S}`, `D_{R,T}`. -/
theorem out_le_rotation_terms (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X))
    {rR rS rT σR σS σT : ℝ}
    (hR : (R.card : ℝ) ≤ rR) (hS : (S.card : ℝ) ≤ rS) (hT : (T.card : ℝ) ≤ rT)
    (hσR : ‖adj R‖ ≤ σR) (hσS : ‖adj S‖ ≤ σS) (hσT : ‖adj T‖ ≤ σT) :
    out R S T ≤ √(min (σR ^ 2) rR * rS * rT) ∧
      out R S T ≤ rR * min (σS ^ 2) rS ∧ out R S T ≤ rR * min (σT ^ 2) rT := by
  refine ⟨le_holder_clip R hR hS hT hσR (out_le_opNorm_mul_sqrt R S T), ?_, ?_⟩
  · exact (out_le_card_mul_of_rowDeg_le R S T (rowDeg_le_clip S hσS hS)).trans
      (mul_le_mul_of_nonneg_right hR (clip_nonneg S hS))
  · exact (out_le_card_mul_of_colDeg_le R S T (colDeg_le_clip T hσT hT)).trans
      (mul_le_mul_of_nonneg_right hR (clip_nonneg T hT))

/-- **Theorem B (upper bound).** Every admissible instance has `Out ≤ U(r, σ)`. -/
theorem theoremB_upper (st : Stats) (R : Finset (X × Y)) (S : Finset (Y × Z))
    (T : Finset (Z × X)) (h : Admissible st R S T) : out R S T ≤ st.U := by
  obtain ⟨hR, hS, hT, hσR, hσS, hσT⟩ := h
  obtain ⟨h1, h4, h5⟩ := out_le_rotation_terms R S T hR hS hT hσR hσS hσT
  obtain ⟨h2, h7, h6⟩ := out_le_rotation_terms S T R hS hT hR hσS hσT hσR
  obtain ⟨h3, h8, h9⟩ := out_le_rotation_terms T R S hT hR hS hσT hσR hσS
  rw [← out_rotate'] at h2 h7 h6
  rw [← out_rotate] at h3 h8 h9
  exact st.le_U h1 h2 h3 h4 h5 h6 h7 h8 h9

end LeatherbackSpectral
