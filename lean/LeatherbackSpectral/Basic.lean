import Mathlib

/-!
# Triangle-query model: relations, 0/1 incidence matrices, output size

Three finite vertex types `X Y Z`, three relations `R ⊆ X × Y`, `S ⊆ Y × Z`,
`T ⊆ Z × X` (as `Finset`s of pairs), their 0/1 real incidence matrices
`adj R : Matrix X Y ℝ`, and the triangle output size

  `out R S T = trace (adj R * adj S * adj T)`
            `= #{(x, y, z) | (x, y) ∈ R, (y, z) ∈ S, (z, x) ∈ T}`.
-/

open Finset Matrix

namespace LeatherbackSpectral

section Defs

variable {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]

/-- The 0/1 real incidence matrix of a relation. -/
def adj (R : Finset (X × Y)) : Matrix X Y ℝ := fun x y => if (x, y) ∈ R then 1 else 0

/-- Real-valued out-degree (row sum of the incidence matrix). -/
def rowDeg (R : Finset (X × Y)) (x : X) : ℝ := ∑ y, adj R x y

/-- Real-valued in-degree (column sum of the incidence matrix). -/
def colDeg (R : Finset (X × Y)) (y : Y) : ℝ := ∑ x, adj R x y

variable (R : Finset (X × Y))

lemma adj_apply (x : X) (y : Y) : adj R x y = if (x, y) ∈ R then 1 else 0 := rfl

lemma adj_nonneg (x : X) (y : Y) : 0 ≤ adj R x y := by
  unfold adj; split_ifs <;> norm_num

lemma adj_le_one (x : X) (y : Y) : adj R x y ≤ 1 := by
  unfold adj; split_ifs <;> norm_num

lemma adj_mul_self (x : X) (y : Y) : adj R x y * adj R x y = adj R x y := by
  unfold adj; split_ifs <;> norm_num

lemma adj_sq (x : X) (y : Y) : adj R x y ^ 2 = adj R x y := by
  rw [sq, adj_mul_self]

/-- The entries of a 0/1 incidence matrix sum to the number of pairs. -/
lemma sum_adj : ∑ x, ∑ y, adj R x y = (R.card : ℝ) := by
  rw [← Fintype.sum_prod_type' (f := fun x y => adj R x y)]
  simp [adj]

lemma sum_rowDeg : ∑ x, rowDeg R x = (R.card : ℝ) := sum_adj R

lemma sum_colDeg : ∑ y, colDeg R y = (R.card : ℝ) := by
  unfold colDeg; rw [Finset.sum_comm]; exact sum_adj R

lemma rowDeg_nonneg (x : X) : 0 ≤ rowDeg R x :=
  Finset.sum_nonneg fun _ _ => adj_nonneg R _ _

lemma colDeg_nonneg (y : Y) : 0 ≤ colDeg R y :=
  Finset.sum_nonneg fun _ _ => adj_nonneg R _ _

lemma rowDeg_le_card (x : X) : rowDeg R x ≤ R.card := by
  rw [← sum_rowDeg]
  exact Finset.single_le_sum (fun i _ => rowDeg_nonneg R i) (Finset.mem_univ x)

lemma colDeg_le_card (y : Y) : colDeg R y ≤ R.card := by
  rw [← sum_colDeg]
  exact Finset.single_le_sum (fun i _ => colDeg_nonneg R i) (Finset.mem_univ y)

/-- The row degree is the cardinality of the out-neighbourhood. -/
lemma rowDeg_eq_card (x : X) :
    rowDeg R x = ((univ.filter fun y => (x, y) ∈ R).card : ℝ) := by
  simp [rowDeg, adj, Finset.sum_boole]

/-- The column degree is the cardinality of the in-neighbourhood. -/
lemma colDeg_eq_card (y : Y) :
    colDeg R y = ((univ.filter fun x => (x, y) ∈ R).card : ℝ) := by
  simp [colDeg, adj, Finset.sum_boole]

end Defs

section Out

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

/-- Triangle output size `Out = tr (A_R A_S A_T)`. -/
def out (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)) : ℝ :=
  trace (adj R * adj S * adj T)

variable (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X))

/-- `Out` as a triple sum of indicator products. -/
lemma out_eq_sum : out R S T = ∑ x, ∑ y, ∑ z, adj R x y * adj S y z * adj T z x := by
  simp only [out, Matrix.trace, Matrix.diag, mul_apply, Finset.sum_mul]
  exact Finset.sum_congr rfl fun x _ => Finset.sum_comm

/-- `Out` counts triangles. -/
lemma out_eq_card :
    out R S T = ((univ.filter fun t : X × Y × Z =>
      (t.1, t.2.1) ∈ R ∧ (t.2.1, t.2.2) ∈ S ∧ (t.2.2, t.1) ∈ T).card : ℝ) := by
  rw [out_eq_sum, Finset.card_filter, Nat.cast_sum, Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun y _ => Finset.sum_congr rfl fun z _ => ?_
  simp only [adj]
  split_ifs <;> simp_all

/-- Cyclic relabelling (cyclicity of the trace). -/
lemma out_rotate : out R S T = out T R S := by
  unfold out
  rw [Matrix.trace_mul_comm, Matrix.mul_assoc]

lemma out_rotate' : out R S T = out S T R := by
  rw [out_rotate, out_rotate]

lemma out_nonneg : 0 ≤ out R S T := by
  rw [out_eq_sum]
  exact Finset.sum_nonneg fun _ _ => Finset.sum_nonneg fun _ _ => Finset.sum_nonneg
    fun _ _ => mul_nonneg (mul_nonneg (adj_nonneg _ _ _) (adj_nonneg _ _ _)) (adj_nonneg _ _ _)

/-- **(D), first form.** If every out-degree of `S` is at most `Δ` then `Out ≤ |R| Δ`. -/
theorem out_le_card_mul_of_rowDeg_le {Δ : ℝ} (hΔ : ∀ y, rowDeg S y ≤ Δ) :
    out R S T ≤ R.card * Δ := by
  rw [out_eq_sum, ← sum_adj R, Finset.sum_mul]
  refine Finset.sum_le_sum fun x _ => ?_
  rw [Finset.sum_mul]
  refine Finset.sum_le_sum fun y _ => ?_
  calc ∑ z, adj R x y * adj S y z * adj T z x ≤ ∑ z, adj R x y * adj S y z :=
        Finset.sum_le_sum fun z _ => mul_le_of_le_one_right
          (mul_nonneg (adj_nonneg _ _ _) (adj_nonneg _ _ _)) (adj_le_one _ _ _)
    _ = adj R x y * rowDeg S y := by rw [rowDeg, Finset.mul_sum]
    _ ≤ adj R x y * Δ := mul_le_mul_of_nonneg_left (hΔ y) (adj_nonneg _ _ _)

/-- **(D), second form.** If every in-degree of `T` is at most `Δ` then `Out ≤ |R| Δ`. -/
theorem out_le_card_mul_of_colDeg_le {Δ : ℝ} (hΔ : ∀ x, colDeg T x ≤ Δ) :
    out R S T ≤ R.card * Δ := by
  rw [out_eq_sum, ← sum_adj R, Finset.sum_mul]
  refine Finset.sum_le_sum fun x _ => ?_
  rw [Finset.sum_mul]
  refine Finset.sum_le_sum fun y _ => ?_
  calc ∑ z, adj R x y * adj S y z * adj T z x ≤ ∑ z, adj R x y * adj T z x :=
        Finset.sum_le_sum fun z _ => by
          rw [mul_right_comm]
          exact mul_le_of_le_one_right
            (mul_nonneg (adj_nonneg _ _ _) (adj_nonneg _ _ _)) (adj_le_one _ _ _)
    _ = adj R x y * colDeg T x := by rw [colDeg, Finset.mul_sum]
    _ ≤ adj R x y * Δ := mul_le_mul_of_nonneg_left (hΔ x) (adj_nonneg _ _ _)

end Out

end LeatherbackSpectral
