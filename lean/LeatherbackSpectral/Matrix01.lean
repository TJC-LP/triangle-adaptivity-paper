import LeatherbackSpectral.Lower

/-!
# Bridge: arbitrary 0/1 real matrices

Theorem B is stated for relations (`Finset`s of pairs) and their incidence matrices
`adj R`. Every real matrix with entries in `{0, 1}` is such an incidence matrix
(`adj_ones`), with `|R|` = the number of ones (`ones A`). This file restates the main
upper bounds directly for 0/1 matrices `A_R : Matrix X Y ℝ`, `A_S : Matrix Y Z ℝ`,
`A_T : Matrix Z X ℝ` and `Out = trace (A_R * A_S * A_T)`.
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

/-- Entries in `{0, 1}`. -/
def IsZeroOne {X' Y' : Type*} (A : Matrix X' Y' ℝ) : Prop := ∀ x y, A x y = 0 ∨ A x y = 1

/-- The positions of the ones of a matrix (so `(ones A).card` = number of ones). -/
noncomputable def ones {X' Y' : Type*} [Fintype X'] [Fintype Y'] (A : Matrix X' Y' ℝ) :
    Finset (X' × Y') :=
  univ.filter fun p => A p.1 p.2 = 1

lemma adj_ones {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X'] [DecidableEq Y']
    {A : Matrix X' Y' ℝ} (hA : IsZeroOne A) : adj (ones A) = A := by
  ext x y
  rcases hA x y with h | h <;> simp [adj, ones, h]

/-- The number of ones is the squared Frobenius norm. -/
lemma card_ones_eq_sum_sq {X' Y' : Type*} [Fintype X'] [Fintype Y'] [DecidableEq X']
    [DecidableEq Y'] {A : Matrix X' Y' ℝ} (hA : IsZeroOne A) :
    ((ones A).card : ℝ) = ∑ x, ∑ y, A x y ^ 2 := by
  conv_rhs => rw [← adj_ones hA]
  simp_rw [adj_sq]
  rw [sum_adj]

variable {A : Matrix X Y ℝ} {B : Matrix Y Z ℝ} {C : Matrix Z X ℝ}

/-- **Theorem B, Hölder term, matrix form.** For 0/1 matrices,
`tr(A_R A_S A_T) ≤ ‖A_R‖₂ √(|S| |T|)`. -/
theorem trace_le_opNorm_mul_sqrt (hA : IsZeroOne A) (hB : IsZeroOne B) (hC : IsZeroOne C) :
    trace (A * B * C) ≤ ‖A‖ * √(((ones B).card : ℝ) * (ones C).card) := by
  have h := out_le_opNorm_mul_sqrt (ones A) (ones B) (ones C)
  rwa [out, adj_ones hA, adj_ones hB, adj_ones hC] at h

/-- **Degree term, matrix form.** `tr(A_R A_S A_T) ≤ |R| ‖A_S‖²`. -/
theorem trace_le_card_mul_opNorm_sq (hA : IsZeroOne A) (hB : IsZeroOne B)
    (hC : IsZeroOne C) : trace (A * B * C) ≤ (ones A).card * ‖B‖ ^ 2 := by
  have h := out_le_card_mul_opNorm_sq_S (ones A) (ones B) (ones C)
  rwa [out, adj_ones hA, adj_ones hB, adj_ones hC] at h

/-- **Degree term `D_{R,T}`, matrix form.** `tr(A_R A_S A_T) ≤ |R| ‖A_T‖²`. -/
theorem trace_le_card_mul_opNorm_sq_T (hA : IsZeroOne A) (hB : IsZeroOne B)
    (hC : IsZeroOne C) : trace (A * B * C) ≤ (ones A).card * ‖C‖ ^ 2 := by
  have h := out_le_card_mul_opNorm_sq_T (ones A) (ones B) (ones C)
  rwa [out, adj_ones hA, adj_ones hB, adj_ones hC] at h

/-- **Lemma 3.1, matrix form.** Every row and column sum of a 0/1 matrix is `≤ ‖A‖²`. -/
theorem rowSum_le_opNorm_sq (hA : IsZeroOne A) (x : X) : ∑ y, A x y ≤ ‖A‖ ^ 2 := by
  have h := rowDeg_le_opNorm_sq (ones A) x
  rwa [rowDeg, adj_ones hA] at h

theorem colSum_le_opNorm_sq (hA : IsZeroOne A) (y : Y) : ∑ x, A x y ≤ ‖A‖ ^ 2 := by
  have h := colDeg_le_opNorm_sq (ones A) y
  rwa [colDeg, adj_ones hA] at h

/-- **Theorem B (upper bound), matrix form.** -/
theorem theoremB_upper_matrix (st : Stats) (hA : IsZeroOne A) (hB : IsZeroOne B)
    (hC : IsZeroOne C) (hR : ((ones A).card : ℝ) ≤ st.rR) (hS : ((ones B).card : ℝ) ≤ st.rS)
    (hT : ((ones C).card : ℝ) ≤ st.rT) (hσR : ‖A‖ ≤ st.σR) (hσS : ‖B‖ ≤ st.σS)
    (hσT : ‖C‖ ≤ st.σT) : trace (A * B * C) ≤ st.U := by
  have h := theoremB_upper st (ones A) (ones B) (ones C)
    ⟨hR, hS, hT, by rwa [adj_ones hA], by rwa [adj_ones hB], by rwa [adj_ones hC]⟩
  rwa [out, adj_ones hA, adj_ones hB, adj_ones hC] at h

end LeatherbackSpectral
