import LeatherbackSpectral.Kernel
import Leatherback.Cost.TriangleChargeProofs

/-!
# Bridge: the kernel's candidate budget is `kernelWork`

The Std-only side defines `kernelWorkNat E1 E2 E3 = Σ_{(x,y) ∈ E1} min(|N2(y)|, |N3(x)|)` over
keyed edge lists in the Zig kernel's orientation (`Leatherback.Join.TriangleBag`), and proves
that the executable replica of the Leatherback triangle kernel accumulates exactly that in its `model`
field (`Leatherback.Cost.TriangleCharge.run_model_eq_sorted`). This file identifies it with the
spectral development's `kernelWork` (Lemma 1's quantity) and transfers the bounds that survive
nesting (Proposition 5.1) to it.

What `model` is: the **ideal precharged candidate budget** — `min(|N2(y)|, |N3(x)|)` added per
`E1` row before that row's intersection runs. It is *not* the number of neighbour entries the
replica reads. That number is the `walked` field, and the replica proves only
`walked ≤ model` (`run_walked_le_model`); the inequality can be strict
(`walked_lt_model_example`: `model = 3`, `walked = 1`). So the statements below bound actual
walked entries by `kernelWork` (`run_walked_le_kernelWork_real`, `run_walked_le_terms`) and
identify `kernelWork` only with the budget. Nothing here bounds `charged`, which also counts
galloping and seeks.

Orientation: the kernel keys `E3` by `x` with values `z`; here `T ⊆ Z × X`, so `T` is
`E3.map Prod.swap`.

Only the five `R`-driven terms transfer (`kernelWork_le_terms`): `nestS_can_raise_opNorm`
shows the `H_S`/`H_T` terms of Theorem B's `U` need not bound `kernelWork`.
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

open Leatherback.Join.TriangleBag

section Generic

variable {X Y Z : Type} [Fintype X] [Fintype Y] [Fintype Z]
  [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

lemma outN_toFinset (E : List (Y × Z)) (hE : E.Nodup) (y : Y) :
    outN E.toFinset y = (nbr E y).length := by
  unfold outN
  rw [← List.toFinset_card_of_nodup (nbr_nodup E y hE)]
  congr 1
  ext z
  simp [mem_nbr]

lemma inN_swap (E : List (X × Z)) (hE : E.Nodup) (x : X) :
    inN (E.map Prod.swap).toFinset x = (nbr E x).length := by
  unfold inN
  rw [← List.toFinset_card_of_nodup (nbr_nodup E x hE)]
  congr 1
  ext z
  simp [mem_nbr]

/-- **`kernelWorkNat = kernelWork`** on duplicate-free edge lists. -/
theorem kernelWorkNat_eq_kernelWork (E1 : List (X × Y)) (E2 : List (Y × Z)) (E3 : List (X × Z))
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) :
    (kernelWorkNat E1 E2 E3 : ℝ) =
      kernelWork E1.toFinset E2.toFinset (E3.map Prod.swap).toFinset := by
  rw [kernelWork]
  simp_rw [rowDeg_eq_outN, colDeg_eq_inN, outN_toFinset E2 h2, inN_swap E3 h3, adj_apply,
    ite_mul, one_mul, zero_mul]
  rw [← Finset.sum_product' (f := fun x y =>
    if (x, y) ∈ E1.toFinset then
      (min ((nbr E2 y).length : ℝ) ((nbr E3 x).length : ℝ)) else 0)]
  rw [Finset.sum_ite_mem, Finset.univ_product_univ, Finset.univ_inter, List.sum_toFinset _ h1,
    kernelWorkNat]
  simp [Nat.cast_list_sum, List.map_map, Function.comp_def, Nat.cast_min]

end Generic

section Relabel

/-- Ids `≤ N` as `Fin (N + 1)`. -/
def toFin (N a : Nat) : Fin (N + 1) := ⟨min a N, by omega⟩

/-- An edge list over `Fin (N + 1)`. -/
def finEdges (N : Nat) (E : List (Nat × Nat)) : List (Fin (N + 1) × Fin (N + 1)) :=
  E.map fun e => (toFin N e.1, toFin N e.2)

/-- Every id of `E` is `≤ N`. -/
def Bounded (N : Nat) (E : List (Nat × Nat)) : Prop := ∀ e ∈ E, e.1 ≤ N ∧ e.2 ≤ N

lemma toFin_inj {N a b : Nat} (ha : a ≤ N) (hb : b ≤ N) : toFin N a = toFin N b ↔ a = b := by
  simp only [toFin, Fin.mk.injEq]
  omega

lemma nbr_finEdges_length (N : Nat) (E : List (Nat × Nat)) (hE : Bounded N E) (k : Nat)
    (hk : k ≤ N) : (nbr (finEdges N E) (toFin N k)).length = (nbr E k).length := by
  simp only [nbr, finEdges, List.length_map, List.filter_map]
  congr 1
  apply List.filter_congr
  intro e he
  simp [Function.comp, toFin_inj (hE e he).1 hk]

lemma kernelWorkNat_finEdges (N : Nat) (E1 E2 E3 : List (Nat × Nat)) (h1 : Bounded N E1)
    (h2 : Bounded N E2) (h3 : Bounded N E3) :
    kernelWorkNat (finEdges N E1) (finEdges N E2) (finEdges N E3) = kernelWorkNat E1 E2 E3 := by
  unfold kernelWorkNat
  rw [show finEdges N E1 = E1.map (fun e => (toFin N e.1, toFin N e.2)) from rfl, List.map_map]
  congr 1
  apply List.map_congr_left
  intro e he
  simp only [Function.comp]
  rw [nbr_finEdges_length N E2 h2 e.2 (h1 e he).2, nbr_finEdges_length N E3 h3 e.1 (h1 e he).1]

lemma finEdges_nodup (N : Nat) (E : List (Nat × Nat)) (hE : Bounded N E) (h : E.Nodup) :
    (finEdges N E).Nodup := by
  apply h.map_on
  intro a ha b hb hab
  simp only [Prod.mk.injEq] at hab
  have e1 := (toFin_inj (hE a ha).1 (hE b hb).1).mp hab.1
  have e2 := (toFin_inj (hE a ha).2 (hE b hb).2).mp hab.2
  exact Prod.ext e1 e2

/-- The finite relations a bounded instance denotes. -/
def finR (N : Nat) (E : List (Nat × Nat)) : Finset (Fin (N + 1) × Fin (N + 1)) :=
  (finEdges N E).toFinset

/-- `T ⊆ Z × X` from the kernel's `x`-keyed `E3`. -/
def finT (N : Nat) (E : List (Nat × Nat)) : Finset (Fin (N + 1) × Fin (N + 1)) :=
  ((finEdges N E).map Prod.swap).toFinset

/-- **`kernelWorkNat = kernelWork` on a bounded `Nat` instance.** -/
theorem kernelWorkNat_eq_kernelWork_fin (N : Nat) (E1 E2 E3 : List (Nat × Nat))
    (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) :
    (kernelWorkNat E1 E2 E3 : ℝ) = kernelWork (finR N E1) (finR N E2) (finT N E3) := by
  rw [← kernelWorkNat_finEdges N E1 E2 E3 b1 b2 b3]
  exact kernelWorkNat_eq_kernelWork _ _ _ (finEdges_nodup N E1 b1 h1)
    (finEdges_nodup N E2 b2 h2) (finEdges_nodup N E3 b3 h3)

end Relabel

section Meter

open Leatherback.Cost.TriangleCharge

variable {σ : Type} (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)

/-- **The replica's candidate budget is `kernelWork`.** For a sorted, duplicate-free,
bounded instance and a sink that never stops, the executable replica of the Leatherback triangle kernel
accumulates `model = kernelWork R S T` of the finite relations the instance denotes. `model`
is the ideal precharged candidate budget, not the count of entries read; that count,
`walked`, is only `≤ model` (`run_walked_le_kernelWork_real`). -/
theorem run_model_eq_kernelWork (htot : ∀ x y z m st, (visit x y z m st).1 = true) (N : Nat)
    (E1 E2 E3 : List (Nat × Nat)) (s1 : LexSorted E1) (s2 : LexSorted E2) (s3 : LexSorted E3)
    (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) (sink : σ) :
    ((run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model : ℝ) =
      kernelWork (finR N E1) (finR N E2) (finT N E3) := by
  rw [run_model_eq_sorted visit htot E1 E2 E3 s1 s2 s3 sink]
  exact kernelWorkNat_eq_kernelWork_fin N E1 E2 E3 b1 b2 b3 h1 h2 h3

/-- **Proposition 5.1 for the candidate budget.** Under the admissible statistics, the
replica's `model` budget is bounded by each of the five `R`-driven terms. -/
theorem run_model_le_terms (htot : ∀ x y z m st, (visit x y z m st).1 = true) (N : Nat)
    (E1 E2 E3 : List (Nat × Nat)) (s1 : LexSorted E1) (s2 : LexSorted E2) (s3 : LexSorted E3)
    (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) (sink : σ) {rR rS rT σR σS σT : ℝ}
    (hR : ((finR N E1).card : ℝ) ≤ rR) (hS : ((finR N E2).card : ℝ) ≤ rS)
    (hT : ((finT N E3).card : ℝ) ≤ rT)
    (hσR : ‖adj (finR N E1)‖ ≤ σR) (hσS : ‖adj (finR N E2)‖ ≤ σS)
    (hσT : ‖adj (finT N E3)‖ ≤ σT) :
    let M : ℝ := (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model
    M ≤ √(min (σR ^ 2) rR * rS * rT) ∧ M ≤ rR * min (σS ^ 2) rS ∧
      M ≤ rR * min (σT ^ 2) rT ∧ M ≤ rS * min (σR ^ 2) rR ∧ M ≤ rT * min (σR ^ 2) rR := by
  intro M
  have hM : M = kernelWork (finR N E1) (finR N E2) (finT N E3) :=
    run_model_eq_kernelWork visit htot N E1 E2 E3 s1 s2 s3 b1 b2 b3 h1 h2 h3 sink
  rw [hM]
  exact kernelWork_le_terms _ _ _ hR hS hT hσR hσS hσT

/-- The Hölder term without statistics: `M ≤ ‖A_R‖₂ √(|S| |T|)`. -/
theorem run_model_le_opNorm (htot : ∀ x y z m st, (visit x y z m st).1 = true) (N : Nat)
    (E1 E2 E3 : List (Nat × Nat)) (s1 : LexSorted E1) (s2 : LexSorted E2) (s3 : LexSorted E3)
    (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) (sink : σ) :
    ((run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model : ℝ) ≤
      ‖adj (finR N E1)‖ * √(((finR N E2).card : ℝ) * (finT N E3).card) := by
  rw [run_model_eq_kernelWork visit htot N E1 E2 E3 s1 s2 s3 b1 b2 b3 h1 h2 h3 sink]
  exact kernelWork_le_opNorm_mul_sqrt _ _ _

/-- **Actual walked entries are at most `kernelWork`.** On a sorted, duplicate-free, bounded
instance with a total sink, the replica's `walked` count is `≤ kernelWork R S T`
(`walked ≤ model = kernelWork`). The inequality can be strict (`walked_lt_model_example`). -/
theorem run_walked_le_kernelWork_real (htot : ∀ x y z m st, (visit x y z m st).1 = true)
    (N : Nat) (E1 E2 E3 : List (Nat × Nat)) (s1 : LexSorted E1) (s2 : LexSorted E2)
    (s3 : LexSorted E3) (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) (sink : σ) :
    ((run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.walked : ℝ) ≤
      kernelWork (finR N E1) (finR N E2) (finT N E3) := by
  rw [← run_model_eq_kernelWork visit htot N E1 E2 E3 s1 s2 s3 b1 b2 b3 h1 h2 h3 sink]
  exact_mod_cast run_walked_le_model visit _ _ _ sink

/-- **Proposition 5.1 for the actual walked entries.** Under the admissible statistics, the
replica's `walked` count is bounded by each of the five `R`-driven terms. -/
theorem run_walked_le_terms (htot : ∀ x y z m st, (visit x y z m st).1 = true) (N : Nat)
    (E1 E2 E3 : List (Nat × Nat)) (s1 : LexSorted E1) (s2 : LexSorted E2) (s3 : LexSorted E3)
    (b1 : Bounded N E1) (b2 : Bounded N E2) (b3 : Bounded N E3)
    (h1 : E1.Nodup) (h2 : E2.Nodup) (h3 : E3.Nodup) (sink : σ) {rR rS rT σR σS σT : ℝ}
    (hR : ((finR N E1).card : ℝ) ≤ rR) (hS : ((finR N E2).card : ℝ) ≤ rS)
    (hT : ((finT N E3).card : ℝ) ≤ rT)
    (hσR : ‖adj (finR N E1)‖ ≤ σR) (hσS : ‖adj (finR N E2)‖ ≤ σS)
    (hσT : ‖adj (finT N E3)‖ ≤ σT) :
    let W : ℝ := (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.walked
    W ≤ √(min (σR ^ 2) rR * rS * rT) ∧ W ≤ rR * min (σS ^ 2) rS ∧
      W ≤ rR * min (σT ^ 2) rT ∧ W ≤ rS * min (σR ^ 2) rR ∧ W ≤ rT * min (σR ^ 2) rR := by
  intro W
  have hW : W ≤ kernelWork (finR N E1) (finR N E2) (finT N E3) :=
    run_walked_le_kernelWork_real visit htot N E1 E2 E3 s1 s2 s3 b1 b2 b3 h1 h2 h3 sink
  obtain ⟨k1, k2, k3, k4, k5⟩ := kernelWork_le_terms _ _ _ hR hS hT hσR hσS hσT
  exact ⟨hW.trans k1, hW.trans k2, hW.trans k3, hW.trans k4, hW.trans k5⟩

end Meter

end LeatherbackSpectral
