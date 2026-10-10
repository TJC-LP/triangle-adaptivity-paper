import LeatherbackSpectral.Upper

/-!
# Lemma 1 (nested neighbourhoods) and the adaptive-kernel corollary

The adaptive kernel driven by `R` probes, for every `(x, y) ∈ R`, the smaller of the
two neighbourhoods `S_y` and `T⁻_x`; its work is

  `M_R = ∑_{(x,y) ∈ R} min(d⁺_S(y), d⁻_T(x))`   (`kernelWork R S T`).

**Lemma 1.** Fix an ordering `e : Z ≃ Fin |Z|`. Let `S'` give `y` the first `d⁺_S(y)`
elements of `Z` and `T'` give `x` the first `d⁻_T(x)` elements. Then the neighbourhoods
are nested, so `|S'_y ∩ T'⁻_x| = min(d⁺_S(y), d⁻_T(x))` and `M_R = Out(R, S', T')`
(`kernelWork_eq_out_nest`). `S'` has the same out-degree vector as `S`
(`rowDeg_nestS`) and `T'` the same in-degree vector as `T` (`colDeg_nestT`), and
`|S'| = |S|`, `|T'| = |T|` (`card_nestS`, `card_nestT`). Only these one-sided degree vectors
and the sizes are preserved: the in-degrees of `S'`, the out-degrees of `T'` and the operator
norms can change (`nestS_can_raise_opNorm`: the 2×2 matching has column degrees `(1, 1)`, its
nested version `(2, 0)`). Theorem B's upper-bound lemmas applied to `(R, S', T')`
then bound `M_R` (Proposition 5.1), and the best rotation is `≤ U` (Corollary 5.2).
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

section Count

variable {Z : Type*} [Fintype Z]

/-- The first `k` elements of `Z` under `Fintype.equivFin` number exactly `k`. -/
lemma sum_ite_equivFin_lt {k : ℕ} (hk : k ≤ Fintype.card Z) :
    ∑ z : Z, (if ((Fintype.equivFin Z z : Fin _) : ℕ) < k then (1 : ℝ) else 0) = k := by
  rw [Equiv.sum_comp (Fintype.equivFin Z) (fun i => if (i : ℕ) < k then (1 : ℝ) else 0),
    Finset.sum_boole, Fin.card_filter_val_lt, min_eq_right hk]

end Count

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

/-- Out-degree of `y` in `S`, as a natural number. -/
def outN (S : Finset (Y × Z)) (y : Y) : ℕ := (univ.filter fun z => (y, z) ∈ S).card

/-- In-degree of `x` in `T`, as a natural number. -/
def inN (T : Finset (Z × X)) (x : X) : ℕ := (univ.filter fun z => (z, x) ∈ T).card

lemma outN_le (S : Finset (Y × Z)) (y : Y) : outN S y ≤ Fintype.card Z :=
  Finset.card_le_univ _

lemma inN_le (T : Finset (Z × X)) (x : X) : inN T x ≤ Fintype.card Z :=
  Finset.card_le_univ _

lemma rowDeg_eq_outN (S : Finset (Y × Z)) (y : Y) : rowDeg S y = outN S y :=
  rowDeg_eq_card S y

lemma colDeg_eq_inN (T : Finset (Z × X)) (x : X) : colDeg T x = inN T x :=
  colDeg_eq_card T x

/-- `S'`: `y` is joined to the first `d⁺_S(y)` elements of `Z`. -/
noncomputable def nestS (S : Finset (Y × Z)) : Finset (Y × Z) :=
  univ.filter fun p => ((Fintype.equivFin Z p.2 : Fin _) : ℕ) < outN S p.1

/-- `T'`: `x` is joined from the first `d⁻_T(x)` elements of `Z`. -/
noncomputable def nestT (T : Finset (Z × X)) : Finset (Z × X) :=
  univ.filter fun p => ((Fintype.equivFin Z p.1 : Fin _) : ℕ) < inN T p.2

lemma adj_nestS (S : Finset (Y × Z)) (y : Y) (z : Z) :
    adj (nestS S) y z = if ((Fintype.equivFin Z z : Fin _) : ℕ) < outN S y then 1 else 0 := by
  simp [adj, nestS]

lemma adj_nestT (T : Finset (Z × X)) (z : Z) (x : X) :
    adj (nestT T) z x = if ((Fintype.equivFin Z z : Fin _) : ℕ) < inN T x then 1 else 0 := by
  simp [adj, nestT]

/-- `S'` has the same out-degrees as `S`. -/
lemma rowDeg_nestS (S : Finset (Y × Z)) (y : Y) : rowDeg (nestS S) y = rowDeg S y := by
  rw [rowDeg_eq_outN S y, rowDeg]
  simp_rw [adj_nestS]
  exact sum_ite_equivFin_lt (outN_le S y)

/-- `T'` has the same in-degrees as `T`. -/
lemma colDeg_nestT (T : Finset (Z × X)) (x : X) : colDeg (nestT T) x = colDeg T x := by
  rw [colDeg_eq_inN T x, colDeg]
  simp_rw [adj_nestT]
  exact sum_ite_equivFin_lt (inN_le T x)

/-- `|S'| = |S|`. -/
lemma card_nestS (S : Finset (Y × Z)) : (nestS S).card = S.card := by
  have h : ((nestS S).card : ℝ) = S.card := by
    rw [← sum_rowDeg, ← sum_rowDeg S]
    exact Finset.sum_congr rfl fun y _ => rowDeg_nestS S y
  exact_mod_cast h

/-- `|T'| = |T|`. -/
lemma card_nestT (T : Finset (Z × X)) : (nestT T).card = T.card := by
  have h : ((nestT T).card : ℝ) = T.card := by
    rw [← sum_colDeg, ← sum_colDeg T]
    exact Finset.sum_congr rfl fun x _ => colDeg_nestT T x
  exact_mod_cast h

/-- Probe work of the adaptive kernel driven by `R`:
`M_R = ∑_{(x,y) ∈ R} min(d⁺_S(y), d⁻_T(x))`. -/
def kernelWork (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)) : ℝ :=
  ∑ x, ∑ y, adj R x y * min (rowDeg S y) (colDeg T x)

/-- **Lemma 1 (nested neighbourhoods).** `M_R = Out(R, S', T')`. -/
theorem kernelWork_eq_out_nest (R : Finset (X × Y)) (S : Finset (Y × Z))
    (T : Finset (Z × X)) : kernelWork R S T = out R (nestS S) (nestT T) := by
  rw [out_eq_sum, kernelWork]
  refine Finset.sum_congr rfl fun x _ => Finset.sum_congr rfl fun y _ => ?_
  have hcount : ∑ z, adj (nestS S) y z * adj (nestT T) z x =
      ((min (outN S y) (inN T x) : ℕ) : ℝ) := by
    rw [← sum_ite_equivFin_lt (min_le_of_left_le (outN_le S y))]
    refine Finset.sum_congr rfl fun z _ => ?_
    rw [adj_nestS, adj_nestT]
    by_cases h1 : ((Fintype.equivFin Z z : Fin _) : ℕ) < outN S y <;>
      by_cases h2 : ((Fintype.equivFin Z z : Fin _) : ℕ) < inN T x <;>
      simp [h1, h2]
  simp_rw [mul_assoc, ← Finset.mul_sum]
  rw [hcount, rowDeg_eq_outN, colDeg_eq_inN, Nat.cast_min]

/-- The kernel never does less work than the output: `Out ≤ M_R`. -/
theorem out_le_kernelWork (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)) :
    out R S T ≤ kernelWork R S T := by
  rw [out_eq_sum, kernelWork]
  refine Finset.sum_le_sum fun x _ => Finset.sum_le_sum fun y _ => ?_
  rw [mul_min_of_nonneg _ _ (adj_nonneg R x y)]
  refine le_min ?_ ?_
  · calc ∑ z, adj R x y * adj S y z * adj T z x ≤ ∑ z, adj R x y * adj S y z :=
          Finset.sum_le_sum fun z _ => mul_le_of_le_one_right
            (mul_nonneg (adj_nonneg _ _ _) (adj_nonneg _ _ _)) (adj_le_one _ _ _)
      _ = adj R x y * rowDeg S y := by rw [rowDeg, Finset.mul_sum]
  · calc ∑ z, adj R x y * adj S y z * adj T z x ≤ ∑ z, adj R x y * adj T z x :=
          Finset.sum_le_sum fun z _ => by
            rw [mul_right_comm]
            exact mul_le_of_le_one_right
              (mul_nonneg (adj_nonneg _ _ _) (adj_nonneg _ _ _)) (adj_le_one _ _ _)
      _ = adj R x y * colDeg T x := by rw [colDeg, Finset.mul_sum]

section Bounds

variable (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X))

/-- **Lemma 1 ⇒ Hölder term.** `M_R ≤ ‖A_R‖₂ √(|S| |T|)`. -/
theorem kernelWork_le_opNorm_mul_sqrt :
    kernelWork R S T ≤ ‖adj R‖ * √((S.card : ℝ) * T.card) := by
  rw [kernelWork_eq_out_nest, ← card_nestS S, ← card_nestT T]
  exact out_le_opNorm_mul_sqrt R _ _

/-- `M_R ≤ |R| Δ` when all out-degrees of `S` are `≤ Δ` (term `D_{R,S}`). -/
theorem kernelWork_le_of_rowDeg_le {Δ : ℝ} (hΔ : ∀ y, rowDeg S y ≤ Δ) :
    kernelWork R S T ≤ R.card * Δ := by
  rw [kernelWork_eq_out_nest]
  exact out_le_card_mul_of_rowDeg_le R _ _ fun y => (rowDeg_nestS S y).trans_le (hΔ y)

/-- `M_R ≤ |R| Δ` when all in-degrees of `T` are `≤ Δ` (term `D_{R,T}`). -/
theorem kernelWork_le_of_colDeg_le {Δ : ℝ} (hΔ : ∀ x, colDeg T x ≤ Δ) :
    kernelWork R S T ≤ R.card * Δ := by
  rw [kernelWork_eq_out_nest]
  exact out_le_card_mul_of_colDeg_le R _ _ fun x => (colDeg_nestT T x).trans_le (hΔ x)

/-- `M_R ≤ |S| Δ` when all in-degrees of `R` are `≤ Δ` (term `D_{S,R}`). -/
theorem kernelWork_le_card_S_of_colDeg_R_le {Δ : ℝ} (hΔ : ∀ y, colDeg R y ≤ Δ) :
    kernelWork R S T ≤ S.card * Δ := by
  rw [kernelWork_eq_out_nest, out_rotate', ← card_nestS S]
  exact out_le_card_mul_of_colDeg_le _ _ R hΔ

/-- `M_R ≤ |T| Δ` when all out-degrees of `R` are `≤ Δ` (term `D_{T,R}`). -/
theorem kernelWork_le_card_T_of_rowDeg_R_le {Δ : ℝ} (hΔ : ∀ x, rowDeg R x ≤ Δ) :
    kernelWork R S T ≤ T.card * Δ := by
  rw [kernelWork_eq_out_nest, out_rotate, ← card_nestT T]
  exact out_le_card_mul_of_rowDeg_le _ R _ hΔ

/-- **Proposition 5.1.** Under the statistics, `M_R ≤ min(H_R, D_{R,S}, D_{R,T}, D_{S,R}, D_{T,R})`. -/
theorem kernelWork_le_terms {rR rS rT σR σS σT : ℝ}
    (hR : (R.card : ℝ) ≤ rR) (hS : (S.card : ℝ) ≤ rS) (hT : (T.card : ℝ) ≤ rT)
    (hσR : ‖adj R‖ ≤ σR) (hσS : ‖adj S‖ ≤ σS) (hσT : ‖adj T‖ ≤ σT) :
    kernelWork R S T ≤ √(min (σR ^ 2) rR * rS * rT) ∧
      kernelWork R S T ≤ rR * min (σS ^ 2) rS ∧
      kernelWork R S T ≤ rR * min (σT ^ 2) rT ∧
      kernelWork R S T ≤ rS * min (σR ^ 2) rR ∧
      kernelWork R S T ≤ rT * min (σR ^ 2) rR := by
  refine ⟨le_holder_clip R hR hS hT hσR (kernelWork_le_opNorm_mul_sqrt R S T), ?_, ?_, ?_, ?_⟩
  · exact (kernelWork_le_of_rowDeg_le R S T (rowDeg_le_clip S hσS hS)).trans
      (mul_le_mul_of_nonneg_right hR (clip_nonneg S hS))
  · exact (kernelWork_le_of_colDeg_le R S T (colDeg_le_clip T hσT hT)).trans
      (mul_le_mul_of_nonneg_right hR (clip_nonneg T hT))
  · exact (kernelWork_le_card_S_of_colDeg_R_le R S T (colDeg_le_clip R hσR hR)).trans
      (mul_le_mul_of_nonneg_right hS (clip_nonneg R hR))
  · exact (kernelWork_le_card_T_of_rowDeg_R_le R S T (rowDeg_le_clip R hσR hR)).trans
      (mul_le_mul_of_nonneg_right hT (clip_nonneg R hR))

/-- **Corollary 5.2 (adaptive rotation is worst-case optimal).** The best of the three
rotations does work `min(M_R, M_S, M_T) ≤ U(r, σ)` on every admissible instance. -/
theorem kernel_min_le_U (st : Stats) (h : Admissible st R S T) :
    min (kernelWork R S T) (min (kernelWork S T R) (kernelWork T R S)) ≤ st.U := by
  obtain ⟨hR, hS, hT, hσR, hσS, hσT⟩ := h
  obtain ⟨r1, r2, r3, r4, r5⟩ := kernelWork_le_terms R S T hR hS hT hσR hσS hσT
  obtain ⟨s1, s2, -, s4, -⟩ := kernelWork_le_terms S T R hS hT hR hσS hσT hσR
  obtain ⟨t1, -, -, -, -⟩ := kernelWork_le_terms T R S hT hR hS hσT hσR hσS
  have mR : min (kernelWork R S T) (min (kernelWork S T R) (kernelWork T R S)) ≤
      kernelWork R S T := min_le_left _ _
  have mS : min (kernelWork R S T) (min (kernelWork S T R) (kernelWork T R S)) ≤
      kernelWork S T R := (min_le_right _ _).trans (min_le_left _ _)
  have mT : min (kernelWork R S T) (min (kernelWork S T R) (kernelWork T R S)) ≤
      kernelWork T R S := (min_le_right _ _).trans (min_le_right _ _)
  exact st.le_U (mR.trans r1) (mS.trans s1) (mT.trans t1) (mR.trans r2) (mR.trans r3)
    (mR.trans r4) (mS.trans s2) (mR.trans r5) (mS.trans s4)

end Bounds

end LeatherbackSpectral
