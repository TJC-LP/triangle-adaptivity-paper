import Leatherback.Join.AdaptiveTriangle

/-!
# Bag triangle rows and the Nat kernel-work meter

Reference semantics for the Leatherback triangle kernel (`src/query/triangle_join.zig`)
over keyed edge lists, in the orientation the kernel reads them:

* `E1` rows `(x, y)` (keyed by `x`),
* `E2` rows `(y, z)` (keyed by `y`),
* `E3` rows `(x, z)` (keyed by `x`; the mathlib side's `T ⊆ Z × X` holds `(z, x)`).

`bagRows` is the bag answer the kernel hands its sink, in the kernel's order: `E1` row
order (x-ascending on a sorted `E1`), then `z` ascending, each distinct `z` once with
multiplicity `count_{N2(y)} z * count_{N3(x)} z`. `kernelWorkNat` is the Std-only `Nat`
mirror of `LeatherbackSpectral.kernelWork`: `Σ_{(x,y) ∈ E1} min(|N2(y)|, |N3(x)|)`, the
quantity the kernel's walked-side meter (`noteWalk`) accumulates.

The executable replica of the Zig charges is `Leatherback.Cost.TriangleCharge`; the mathlib
identification `kernelWorkNat = kernelWork` is `LeatherbackSpectral.KernelBridge`.
-/

namespace Leatherback.Join.TriangleBag

open Leatherback.Join

section Generic

variable {K V : Type} [DecidableEq K]

/-- The values of key `k` in a keyed relation, in list order, with multiplicity. -/
def nbr (E : List (K × V)) (k : K) : List V :=
  (E.filter (fun e => decide (e.1 = k))).map Prod.snd

@[simp] theorem nbr_nil (k : K) : nbr ([] : List (K × V)) k = [] := rfl

theorem nbr_cons (a : K × V) (E : List (K × V)) (k : K) :
    nbr (a :: E) k = if a.1 = k then a.2 :: nbr E k else nbr E k := by
  unfold nbr
  by_cases h : a.1 = k <;> simp [h]

@[simp] theorem mem_nbr (E : List (K × V)) (k : K) (v : V) : v ∈ nbr E k ↔ (k, v) ∈ E := by
  unfold nbr
  simp only [List.mem_map, List.mem_filter, decide_eq_true_eq]
  constructor
  · rintro ⟨⟨a, b⟩, ⟨hm, rfl⟩, rfl⟩
    exact hm
  · intro h
    exact ⟨(k, v), ⟨h, rfl⟩, rfl⟩

theorem nbr_nodup (E : List (K × V)) (k : K) (h : E.Nodup) : (nbr E k).Nodup := by
  unfold nbr
  apply List.pairwise_map.mpr
  apply (h.filter (fun e => decide (e.1 = k))).imp_of_mem
  intro a b ha hb hab heq
  simp only [List.mem_filter, decide_eq_true_eq] at ha hb
  apply hab
  rcases a with ⟨a1, a2⟩
  rcases b with ⟨b1, b2⟩
  simp only at ha hb heq
  rw [ha.2, hb.2, heq]

end Generic

section Work

variable {X Y Z : Type} [DecidableEq X] [DecidableEq Y]

/-- Std-only `Nat` mirror of `LeatherbackSpectral.kernelWork`, over keyed edge lists:
`Σ_{(x,y) ∈ E1} min(d⁺_{E2}(y), d_{E3}(x))`. Repeated `E1` rows are counted repeatedly,
exactly as the kernel's walk meter counts them. -/
def kernelWorkNat (E1 : List (X × Y)) (E2 : List (Y × Z)) (E3 : List (X × Z)) : Nat :=
  (E1.map fun e => min (nbr E2 e.2).length (nbr E3 e.1).length).sum

/-- The meter is the adaptive kernel's probe budget on the list neighbourhoods. -/
theorem kernelWorkNat_eq_adaptiveBudget (E1 : List (X × Y)) (E2 : List (Y × Z))
    (E3 : List (X × Z)) : kernelWorkNat E1 E2 E3 = adaptiveBudget E1 (nbr E2) (nbr E3) := rfl

/-- ... and the exact probe count of the reference kernel `AdaptiveTriangle.triangle`. -/
theorem kernelWorkNat_eq_probes [DecidableEq Z] (E1 : List (X × Y)) (E2 : List (Y × Z))
    (E3 : List (X × Z)) :
    kernelWorkNat E1 E2 E3 = (triangle E1 (nbr E2) (nbr E3)).probes :=
  (triangle_probes E1 (nbr E2) (nbr E3)).symm

/-- Output never exceeds the meter (`out ≤ kernelWork`, list form). -/
theorem triangle_length_le_kernelWorkNat [DecidableEq Z] (E1 : List (X × Y))
    (E2 : List (Y × Z)) (E3 : List (X × Z)) :
    (triangle E1 (nbr E2) (nbr E3)).values.length ≤ kernelWorkNat E1 E2 E3 := by
  rw [kernelWorkNat_eq_probes]
  exact triangle_output_le_probes _ _ _

@[simp] theorem kernelWorkNat_nil (E2 : List (Y × Z)) (E3 : List (X × Z)) :
    kernelWorkNat ([] : List (X × Y)) E2 E3 = 0 := rfl

theorem kernelWorkNat_cons (e : X × Y) (E1 : List (X × Y)) (E2 : List (Y × Z))
    (E3 : List (X × Z)) :
    kernelWorkNat (e :: E1) E2 E3 =
      min (nbr E2 e.2).length (nbr E3 e.1).length + kernelWorkNat E1 E2 E3 := by
  simp [kernelWorkNat, List.sum_cons]

theorem kernelWorkNat_append (A B : List (X × Y)) (E2 : List (Y × Z)) (E3 : List (X × Z)) :
    kernelWorkNat (A ++ B) E2 E3 = kernelWorkNat A E2 E3 + kernelWorkNat B E2 E3 := by
  simp [kernelWorkNat]

end Work

section Distinct

/-- Insert into a strictly increasing list, dropping a duplicate. -/
def insertAsc (z : Nat) : List Nat → List Nat
  | [] => [z]
  | a :: rest => if z < a then z :: a :: rest else if z = a then a :: rest else a :: insertAsc z rest

/-- The distinct values of a list, ascending. -/
def ascDistinct (l : List Nat) : List Nat := l.foldr insertAsc []

theorem mem_insertAsc (z x : Nat) (l : List Nat) : x ∈ insertAsc z l ↔ x = z ∨ x ∈ l := by
  induction l with
  | nil => simp [insertAsc]
  | cons a rest ih =>
    unfold insertAsc
    by_cases h1 : z < a
    · simp [h1]
    · by_cases h2 : z = a
      · subst h2; simp [h1]
      · simp only [h1, h2, if_false, List.mem_cons, ih]
        constructor
        · rintro (h | h | h) <;> simp [h]
        · rintro (h | h | h) <;> simp [h]

theorem mem_ascDistinct (l : List Nat) (x : Nat) : x ∈ ascDistinct l ↔ x ∈ l := by
  induction l with
  | nil => simp [ascDistinct]
  | cons a rest ih =>
    simp only [ascDistinct, List.foldr_cons] at *
    rw [mem_insertAsc, ih, List.mem_cons]

theorem insertAsc_sorted (z : Nat) (l : List Nat) (h : l.Pairwise (· < ·)) :
    (insertAsc z l).Pairwise (· < ·) := by
  induction l with
  | nil => simp [insertAsc]
  | cons a rest ih =>
    obtain ⟨ha, hrest⟩ := List.pairwise_cons.mp h
    unfold insertAsc
    by_cases h1 : z < a
    · simp only [h1, if_true]
      refine List.pairwise_cons.mpr ⟨?_, h⟩
      intro b hb
      rcases List.mem_cons.mp hb with rfl | hb
      · exact h1
      · exact Nat.lt_trans h1 (ha b hb)
    · by_cases h2 : z = a
      · subst h2
        simp only [Nat.lt_irrefl, if_false, if_true]
        exact h
      · simp only [h1, h2, if_false]
        refine List.pairwise_cons.mpr ⟨?_, ih hrest⟩
        intro b hb
        rcases (mem_insertAsc z b rest).mp hb with rfl | hb
        · omega
        · exact ha b hb

theorem ascDistinct_sorted (l : List Nat) : (ascDistinct l).Pairwise (· < ·) := by
  induction l with
  | nil => simp [ascDistinct]
  | cons a rest ih => exact insertAsc_sorted a _ ih

theorem ascDistinct_nodup (l : List Nat) : (ascDistinct l).Nodup :=
  (ascDistinct_sorted l).imp (fun h => Nat.ne_of_lt h)

/-- A duplicate-free list contained in another is no longer than it. -/
theorem length_le_of_nodup_subset {α : Type} [DecidableEq α] :
    ∀ (l₁ l₂ : List α), l₁.Nodup → (∀ a ∈ l₁, a ∈ l₂) → l₁.length ≤ l₂.length
  | [], _, _, _ => Nat.zero_le _
  | a :: t, l₂, hn, hs => by
    obtain ⟨hat, ht⟩ := List.nodup_cons.mp hn
    have ha : a ∈ l₂ := hs a (List.mem_cons_self ..)
    have hsub : ∀ b ∈ t, b ∈ l₂.erase a := by
      intro b hb
      have hba : b ≠ a := fun e => hat (e ▸ hb)
      exact (List.mem_erase_of_ne hba).mpr (hs b (List.mem_cons_of_mem _ hb))
    have := length_le_of_nodup_subset t (l₂.erase a) ht hsub
    rw [List.length_erase_of_mem ha] at this
    have hpos : 0 < l₂.length := List.length_pos_of_mem ha
    simp only [List.length_cons]
    omega

theorem ascDistinct_length_le (l : List Nat) : (ascDistinct l).length ≤ l.length := by
  induction l with
  | nil => simp [ascDistinct]
  | cons a rest ih =>
    have hn := ascDistinct_nodup (a :: rest)
    apply length_le_of_nodup_subset _ _ hn
    intro b hb
    exact (mem_ascDistinct _ b).mp hb

end Distinct

section Bag

/-- A sink row: `(x, y, z, multiplicity)`. -/
abbrev Row := Nat × Nat × Nat × Nat

/-- The `z` values of row `(x, y)`: the distinct common values of `N2(y)` and `N3(x)`,
ascending (the order `intersectEachBy` visits them). -/
def rowZs (E2 E3 : List (Nat × Nat)) (x y : Nat) : List Nat :=
  (ascDistinct (nbr E2 y)).filter (fun z => decide (z ∈ nbr E3 x))

/-- The rows the kernel hands its sink for one `E1` row. -/
def rowsOf (E2 E3 : List (Nat × Nat)) (e : Nat × Nat) : List Row :=
  (rowZs E2 E3 e.1 e.2).map fun z => (e.1, e.2, z, (nbr E2 e.2).count z * (nbr E3 e.1).count z)

/-- **Bag triangle reference.** `E1` row order, then `z` ascending, run-length-product
multiplicities. -/
def bagRows (E1 E2 E3 : List (Nat × Nat)) : List Row := E1.flatMap (rowsOf E2 E3)

/-- The bag's size: what `CountSink` accumulates. -/
def bagCount (E1 E2 E3 : List (Nat × Nat)) : Nat := ((bagRows E1 E2 E3).map (·.2.2.2)).sum

theorem mem_rowZs (E2 E3 : List (Nat × Nat)) (x y z : Nat) :
    z ∈ rowZs E2 E3 x y ↔ (y, z) ∈ E2 ∧ (x, z) ∈ E3 := by
  simp [rowZs, mem_ascDistinct]

theorem rowZs_nodup (E2 E3 : List (Nat × Nat)) (x y : Nat) : (rowZs E2 E3 x y).Nodup :=
  (ascDistinct_nodup _).sublist (List.filter_sublist)

theorem rowZs_sorted (E2 E3 : List (Nat × Nat)) (x y : Nat) :
    (rowZs E2 E3 x y).Pairwise (· < ·) :=
  (ascDistinct_sorted _).sublist (List.filter_sublist)

theorem rowZs_length_le (E2 E3 : List (Nat × Nat)) (x y : Nat) :
    (rowZs E2 E3 x y).length ≤ min (nbr E2 y).length (nbr E3 x).length := by
  apply Nat.le_min.mpr
  constructor
  · exact Nat.le_trans (List.length_filter_le _ _) (ascDistinct_length_le _)
  · apply length_le_of_nodup_subset _ _ (rowZs_nodup E2 E3 x y)
    intro z hz
    exact (mem_nbr _ _ _).mpr ((mem_rowZs E2 E3 x y z).mp hz).2

/-- Membership in the bag reference: the triangle relation with its multiplicity. -/
theorem mem_bagRows (E1 E2 E3 : List (Nat × Nat)) (x y z m : Nat) :
    (x, y, z, m) ∈ bagRows E1 E2 E3 ↔
      (x, y) ∈ E1 ∧ (y, z) ∈ E2 ∧ (x, z) ∈ E3 ∧
        m = (nbr E2 y).count z * (nbr E3 x).count z := by
  simp only [bagRows, rowsOf, List.mem_flatMap, List.mem_map, mem_rowZs, Prod.mk.injEq]
  constructor
  · rintro ⟨⟨a, b⟩, he, w, ⟨h2, h3⟩, rfl, rfl, rfl, rfl⟩
    exact ⟨he, h2, h3, rfl⟩
  · rintro ⟨he, h2, h3, rfl⟩
    exact ⟨(x, y), he, z, ⟨h2, h3⟩, rfl, rfl, rfl, rfl⟩

theorem count_eq_one_of_nodup {l : List Nat} {z : Nat} (h : l.Nodup) (hz : z ∈ l) :
    l.count z = 1 := by
  rw [h.count]; simp [hz]

/-- On sets every multiplicity is one. -/
theorem bagRows_mult_one (E1 E2 E3 : List (Nat × Nat)) (h2 : E2.Nodup) (h3 : E3.Nodup)
    (r : Row) (hr : r ∈ bagRows E1 E2 E3) : r.2.2.2 = 1 := by
  rcases r with ⟨x, y, z, m⟩
  obtain ⟨_, hy, hx, rfl⟩ := (mem_bagRows E1 E2 E3 x y z m).mp hr
  simp only
  rw [count_eq_one_of_nodup (nbr_nodup E2 y h2) ((mem_nbr _ _ _).mpr hy),
    count_eq_one_of_nodup (nbr_nodup E3 x h3) ((mem_nbr _ _ _).mpr hx)]

/-- The `(x, y, z)` support of a bag row list. -/
def support (rows : List Row) : List (Nat × Nat × Nat) := rows.map fun r => (r.1, r.2.1, r.2.2.1)

theorem support_rowsOf_nodup (E2 E3 : List (Nat × Nat)) (e : Nat × Nat) :
    (support (rowsOf E2 E3 e)).Nodup := by
  unfold support rowsOf
  rw [List.map_map]
  apply List.pairwise_map.mpr
  apply (rowZs_nodup E2 E3 e.1 e.2).imp
  intro a b hab heq
  exact hab (congrArg (fun t => t.2.2) heq)

theorem support_rowsOf_key (E2 E3 : List (Nat × Nat)) (e : Nat × Nat)
    (t : Nat × Nat × Nat) (ht : t ∈ support (rowsOf E2 E3 e)) : (t.1, t.2.1) = e := by
  simp only [support, rowsOf, List.map_map, List.mem_map, Function.comp] at ht
  obtain ⟨z, _, rfl⟩ := ht
  rfl

theorem support_bagRows_key (E1 E2 E3 : List (Nat × Nat)) (t : Nat × Nat × Nat)
    (ht : t ∈ support (bagRows E1 E2 E3)) : (t.1, t.2.1) ∈ E1 := by
  rcases t with ⟨x, y, z⟩
  simp only [support, List.mem_map] at ht
  obtain ⟨⟨a, b, c, m⟩, hr, heq⟩ := ht
  simp only [Prod.mk.injEq] at heq
  obtain ⟨rfl, rfl, rfl⟩ := heq
  exact ((mem_bagRows E1 E2 E3 a b c m).mp hr).1

theorem sum_mult_eq_length (rows : List Row) (h : ∀ r ∈ rows, r.2.2.2 = 1) :
    (rows.map (·.2.2.2)).sum = rows.length := by
  induction rows with
  | nil => rfl
  | cons r rs ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    rw [h r List.mem_cons_self, ih (fun r' h' => h r' (List.mem_cons_of_mem _ h'))]
    omega

/-- **Set support.** On duplicate-free inputs the bag reference's support is duplicate-free
and is exactly the adaptive reference kernel's output set (`AdaptiveTriangle.triangle`). -/
theorem bagRows_support_nodup (E1 E2 E3 : List (Nat × Nat)) (h1 : E1.Nodup) :
    (support (bagRows E1 E2 E3)).Nodup ∧
      ∀ t, t ∈ support (bagRows E1 E2 E3) ↔ t ∈ (triangle E1 (nbr E2) (nbr E3)).values := by
  constructor
  · induction E1 with
    | nil => simp [support, bagRows]
    | cons e rest ih =>
      obtain ⟨hnot, hrest⟩ := List.nodup_cons.mp h1
      simp only [bagRows, List.flatMap_cons, support, List.map_append] at ih ⊢
      apply List.nodup_append.mpr
      refine ⟨support_rowsOf_nodup E2 E3 e, ih hrest, ?_⟩
      intro a ha b hb hab
      subst hab
      have hk := support_rowsOf_key E2 E3 e a ha
      have hk' := support_bagRows_key rest E2 E3 a hb
      exact hnot (hk ▸ hk')
  · rintro ⟨x, y, z⟩
    simp only [support, List.mem_map, mem_triangle, mem_nbr]
    constructor
    · rintro ⟨⟨a, b, c, m⟩, hr, heq⟩
      simp only [Prod.mk.injEq] at heq
      obtain ⟨rfl, rfl, rfl⟩ := heq
      obtain ⟨h1, h2, h3, _⟩ := (mem_bagRows E1 E2 E3 a b c m).mp hr
      exact ⟨h1, h2, h3⟩
    · rintro ⟨h1, h2, h3⟩
      exact ⟨(x, y, z, _), (mem_bagRows E1 E2 E3 x y z _).mpr ⟨h1, h2, h3, rfl⟩, rfl⟩

theorem bagCount_cons (e : Nat × Nat) (E1 E2 E3 : List (Nat × Nat)) :
    bagCount (e :: E1) E2 E3 =
      ((rowsOf E2 E3 e).map (·.2.2.2)).sum + bagCount E1 E2 E3 := by
  simp [bagCount, bagRows, List.flatMap_cons, List.map_append]

/-- **Output ≤ meter on sets.** The bag count of a duplicate-free instance never exceeds the
kernel-work meter. -/
theorem bagCount_le_kernelWorkNat (E1 E2 E3 : List (Nat × Nat)) (h2 : E2.Nodup) (h3 : E3.Nodup) :
    bagCount E1 E2 E3 ≤ kernelWorkNat E1 E2 E3 := by
  induction E1 with
  | nil => simp [bagCount, bagRows]
  | cons e rest ih =>
    rw [bagCount_cons, kernelWorkNat_cons]
    apply Nat.add_le_add _ ih
    have hone : ∀ r ∈ rowsOf E2 E3 e, r.2.2.2 = 1 := fun r hr =>
      bagRows_mult_one [e] E2 E3 h2 h3 r (by simpa [bagRows] using hr)
    have hsum := sum_mult_eq_length (rowsOf E2 E3 e) hone
    rw [hsum]
    simp only [rowsOf, List.length_map]
    exact rowZs_length_le E2 E3 e.1 e.2

/-- On sets the bag count is the reference kernel's output size. -/
theorem bagCount_eq_triangle_length (E1 E2 E3 : List (Nat × Nat)) (h1 : E1.Nodup)
    (h2 : E2.Nodup) (h3 : E3.Nodup) :
    bagCount E1 E2 E3 = (triangle E1 (nbr E2) (nbr E3)).values.length := by
  have hsum : bagCount E1 E2 E3 = (bagRows E1 E2 E3).length :=
    sum_mult_eq_length _ (bagRows_mult_one E1 E2 E3 h2 h3)
  obtain ⟨hnd, hmem⟩ := bagRows_support_nodup E1 E2 E3 h1
  have htri : (triangle E1 (nbr E2) (nbr E3)).values.Nodup :=
    triangle_nodup E1 (nbr E2) (nbr E3) h1 (fun y => nbr_nodup E2 y h2) (fun x => nbr_nodup E3 x h3)
  have hle := length_le_of_nodup_subset _ _ hnd (fun t ht => (hmem t).mp ht)
  have hge := length_le_of_nodup_subset _ _ htri (fun t ht => (hmem t).mpr ht)
  rw [hsum]
  simp only [support, List.length_map] at hle hge
  omega

end Bag

end Leatherback.Join.TriangleBag
