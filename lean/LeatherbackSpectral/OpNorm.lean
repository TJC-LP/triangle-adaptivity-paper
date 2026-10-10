import LeatherbackSpectral.Basic

/-!
# The L2 operator norm of a (0/1) matrix

We use mathlib's L2 operator norm on rectangular matrices
(`open scoped Matrix.Norms.L2Operator`, `Matrix.instL2OpNormedAddCommGroup`):
`‖A‖ = ‖toEuclideanLin A‖` as a continuous linear map
`EuclideanSpace ℝ Y →L[ℝ] EuclideanSpace ℝ X`, i.e. the largest singular value.

The only interfaces to the norm used downstream are

* `bilinear_le` (N1): `∑ u_x A_xy v_y ≤ ‖A‖ ‖u‖ ‖v‖`, a consequence of
  `Matrix.l2_opNorm_mulVec`;
* `l2_opNorm_le_of_sum_sq`: an upper bound on `‖A‖` from a bound on `‖A v‖²`,
  a consequence of `ContinuousLinearMap.opNorm_le_bound`.

From these: degree ≤ ‖A‖² (N2), Frobenius `‖A‖² ≤ |R|` (N4),
nonzero ⇒ `‖A‖ ≥ 1` (N5) and the Schur test (N3).
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

variable {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]

/-- `‖A v‖₂ ≤ ‖A‖ ‖v‖₂` written with coordinates. -/
lemma sqrt_sum_sq_mulVec_le (A : Matrix X Y ℝ) (v : Y → ℝ) :
    √(∑ x, (A *ᵥ v) x ^ 2) ≤ ‖A‖ * √(∑ y, v y ^ 2) := by
  have h := A.l2_opNorm_mulVec (WithLp.toLp 2 v)
  simpa [EuclideanSpace.norm_eq] using h

/-- **N1 (bilinear bound).** `∑ₓ ∑ᵧ uₓ Aₓᵧ vᵧ ≤ ‖A‖ ‖u‖₂ ‖v‖₂`. -/
theorem bilinear_le (A : Matrix X Y ℝ) (u : X → ℝ) (v : Y → ℝ) :
    ∑ x, ∑ y, u x * A x y * v y ≤ ‖A‖ * √(∑ x, u x ^ 2) * √(∑ y, v y ^ 2) := by
  have h1 : ∑ x, ∑ y, u x * A x y * v y = ∑ x, u x * (A *ᵥ v) x := by
    simp [mulVec, dotProduct, Finset.mul_sum, mul_assoc]
  rw [h1]
  calc ∑ x, u x * (A *ᵥ v) x ≤ √(∑ x, u x ^ 2) * √(∑ x, (A *ᵥ v) x ^ 2) :=
        Real.sum_mul_le_sqrt_mul_sqrt _ _ _
    _ ≤ √(∑ x, u x ^ 2) * (‖A‖ * √(∑ y, v y ^ 2)) :=
        mul_le_mul_of_nonneg_left (sqrt_sum_sq_mulVec_le A v) (Real.sqrt_nonneg _)
    _ = ‖A‖ * √(∑ x, u x ^ 2) * √(∑ y, v y ^ 2) := by ring

/-- Upper bound on the operator norm from a bound on `‖A v‖²`. -/
theorem l2_opNorm_le_of_sum_sq {A : Matrix X Y ℝ} {C : ℝ} (hC : 0 ≤ C)
    (h : ∀ v : Y → ℝ, ∑ x, (A *ᵥ v) x ^ 2 ≤ C ^ 2 * ∑ y, v y ^ 2) : ‖A‖ ≤ C := by
  rw [Matrix.l2_opNorm_def]
  refine ContinuousLinearMap.opNorm_le_bound _ hC fun v => ?_
  have key : √(∑ x, (A *ᵥ v.ofLp) x ^ 2) ≤ C * √(∑ y, v.ofLp y ^ 2) := by
    rw [← Real.sqrt_sq hC, ← Real.sqrt_mul (sq_nonneg _)]
    exact Real.sqrt_le_sqrt (h _)
  simpa [EuclideanSpace.norm_eq] using key

/-- An elementary step: `d ≤ n √d` with `d, n ≥ 0` gives `d ≤ n²`. -/
lemma le_sq_of_le_mul_sqrt {d n : ℝ} (hd : 0 ≤ d) (hn : 0 ≤ n) (h : d ≤ n * √d) :
    d ≤ n ^ 2 := by
  rcases (Real.sqrt_nonneg d).eq_or_lt with h0 | hpos
  · have hd0 : d = 0 := by rw [← Real.sq_sqrt hd, ← h0]; norm_num
    rw [hd0]; positivity
  · have hs : √d * √d = d := Real.mul_self_sqrt hd
    have : √d ≤ n := by nlinarith
    nlinarith [Real.sqrt_nonneg d]

variable (R : Finset (X × Y))

/-- **N2 / Lemma 3.1 (rows).** Every out-degree of a 0/1 matrix is at most `‖A‖²`. -/
theorem rowDeg_le_opNorm_sq (x : X) : rowDeg R x ≤ ‖adj R‖ ^ 2 := by
  have h := bilinear_le (adj R) (fun x' => if x' = x then 1 else 0) (fun y => adj R x y)
  have hl : ∑ x', ∑ y, (if x' = x then (1 : ℝ) else 0) * adj R x' y * adj R x y = rowDeg R x := by
    simp [rowDeg, adj_mul_self]
  have hu : ∑ x', (if x' = x then (1 : ℝ) else 0) ^ 2 = 1 := by simp
  have hv : ∑ y, adj R x y ^ 2 = rowDeg R x := by simp [rowDeg, adj_sq]
  rw [hl, hu, hv, Real.sqrt_one, mul_one] at h
  exact le_sq_of_le_mul_sqrt (rowDeg_nonneg R x) (norm_nonneg _) h

/-- **N2 / Lemma 3.1 (columns).** Every in-degree of a 0/1 matrix is at most `‖A‖²`. -/
theorem colDeg_le_opNorm_sq (y : Y) : colDeg R y ≤ ‖adj R‖ ^ 2 := by
  have h := bilinear_le (adj R) (fun x => adj R x y) (fun y' => if y' = y then 1 else 0)
  have hl : ∑ x, ∑ y', adj R x y * adj R x y' * (if y' = y then (1 : ℝ) else 0) = colDeg R y := by
    simp [colDeg, adj_mul_self]
  have hu : ∑ y', (if y' = y then (1 : ℝ) else 0) ^ 2 = 1 := by simp
  have hv : ∑ x, adj R x y ^ 2 = colDeg R y := by simp [colDeg, adj_sq]
  rw [hl, hu, hv, Real.sqrt_one, mul_one, mul_comm ‖adj R‖] at h
  exact le_sq_of_le_mul_sqrt (colDeg_nonneg R y) (norm_nonneg _) (by linarith)

/-- **N4 (Frobenius).** `‖A_R‖ ≤ √|R|`, i.e. `‖A_R‖² ≤ ‖A_R‖_F² = |R|`. -/
theorem opNorm_adj_le_sqrt_card : ‖adj R‖ ≤ √(R.card : ℝ) := by
  refine l2_opNorm_le_of_sum_sq (Real.sqrt_nonneg _) fun v => ?_
  rw [Real.sq_sqrt (Nat.cast_nonneg _), ← sum_adj R, Finset.sum_mul]
  refine Finset.sum_le_sum fun x _ => ?_
  have := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (fun y => adj R x y) v
  simpa [mulVec, dotProduct, adj_sq] using this

theorem opNorm_adj_sq_le_card : ‖adj R‖ ^ 2 ≤ R.card := by
  have h := opNorm_adj_le_sqrt_card R
  calc ‖adj R‖ ^ 2 ≤ √(R.card : ℝ) ^ 2 := pow_le_pow_left₀ (norm_nonneg _) h 2
    _ = R.card := Real.sq_sqrt (Nat.cast_nonneg _)

/-- **N5.** A nonempty relation has `‖A_R‖ ≥ 1`. -/
theorem one_le_opNorm_adj {x : X} {y : Y} (h : (x, y) ∈ R) : 1 ≤ ‖adj R‖ := by
  have hd := rowDeg_le_opNorm_sq R x
  have h1 : 1 ≤ rowDeg R x := by
    calc (1 : ℝ) = adj R x y := by simp [adj, h]
      _ ≤ rowDeg R x := Finset.single_le_sum (fun i _ => adj_nonneg R x i) (Finset.mem_univ y)
  nlinarith [norm_nonneg (adj R)]

/-- **N3 (Schur test, 0/1 case).** If all out-degrees are `≤ p` and all in-degrees are `≤ q`
then `‖A_R‖ ≤ √(p q)`. -/
theorem opNorm_adj_le_schur {p q : ℝ} (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hrow : ∀ x, rowDeg R x ≤ p) (hcol : ∀ y, colDeg R y ≤ q) :
    ‖adj R‖ ≤ √(p * q) := by
  refine l2_opNorm_le_of_sum_sq (Real.sqrt_nonneg _) fun v => ?_
  rw [Real.sq_sqrt (mul_nonneg hp hq)]
  have step1 : ∀ x, (adj R *ᵥ v) x ^ 2 ≤ p * ∑ y, adj R x y * v y ^ 2 := by
    intro x
    have cs := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (fun y => adj R x y)
      (fun y => adj R x y * v y)
    have e1 : (adj R *ᵥ v) x = ∑ y, adj R x y * (adj R x y * v y) := by
      simp [mulVec, dotProduct, ← mul_assoc, adj_mul_self]
    have e2 : ∑ y, (adj R x y * v y) ^ 2 = ∑ y, adj R x y * v y ^ 2 := by
      refine Finset.sum_congr rfl fun y _ => ?_
      rw [mul_pow, adj_sq]
    have e3 : ∑ y, adj R x y ^ 2 = rowDeg R x := by simp [rowDeg, adj_sq]
    rw [e1]
    calc (∑ y, adj R x y * (adj R x y * v y)) ^ 2
        ≤ (∑ y, adj R x y ^ 2) * ∑ y, (adj R x y * v y) ^ 2 := cs
      _ = rowDeg R x * ∑ y, adj R x y * v y ^ 2 := by rw [e2, e3]
      _ ≤ p * ∑ y, adj R x y * v y ^ 2 :=
          mul_le_mul_of_nonneg_right (hrow x)
            (Finset.sum_nonneg fun y _ => mul_nonneg (adj_nonneg _ _ _) (sq_nonneg _))
  calc ∑ x, (adj R *ᵥ v) x ^ 2 ≤ ∑ x, p * ∑ y, adj R x y * v y ^ 2 :=
        Finset.sum_le_sum fun x _ => step1 x
    _ = p * ∑ y, colDeg R y * v y ^ 2 := by
        rw [← Finset.mul_sum, Finset.sum_comm]
        congr 1
        refine Finset.sum_congr rfl fun y _ => ?_
        rw [colDeg, Finset.sum_mul]
    _ ≤ p * ∑ y, q * v y ^ 2 :=
        mul_le_mul_of_nonneg_left
          (Finset.sum_le_sum fun y _ => mul_le_mul_of_nonneg_right (hcol y) (sq_nonneg _)) hp
    _ = p * q * ∑ y, v y ^ 2 := by rw [← Finset.mul_sum, mul_assoc]

end LeatherbackSpectral
