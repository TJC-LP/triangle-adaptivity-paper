import Std

/-!
# Degree-adaptive triangle joins

An executable reference kernel for `R(x,y) ⋈ S(y,z) ⋈ T(x,z)`. For each row of
`R`, inspect the shorter of the two `z` adjacency lists and retain exactly the
members of the other list. The proofs establish result membership, absence of
duplicates under explicit hypotheses, and the exact number of candidate probes.

`probes` counts calls to the membership predicate, **not** equality comparisons,
CPU instructions, allocations, or wall-clock time. In this list implementation,
membership and degree calculation are linear. A production implementation needs
an independently verified index refinement and a measured physical cost model.

Set membership is specified; output is a list and duplicate-free only under
`Nodup` hypotheses. Membership correctness does not require distinct input rows.
SQL/SPARQL bag multiplicities are not modeled.
-/

namespace Leatherback.Join

variable {X Y Z : Type}

/-- A result paired with the number of candidate-membership predicate calls. -/
structure ScanResult (α : Type) where
  values : List α
  probes : Nat
  deriving Repr, DecidableEq

/-- Executable instrumented filter: one predicate call for each input element. -/
def probeFilter {α : Type} (p : α → Bool) : List α → ScanResult α
  | [] => ⟨[], 0⟩
  | a :: rest =>
    let tail := probeFilter p rest
    ⟨if p a then a :: tail.values else tail.values, tail.probes + 1⟩

@[simp] theorem probeFilter_values {α : Type} (p : α → Bool) (xs : List α) :
    (probeFilter p xs).values = xs.filter p := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp only [probeFilter, List.filter_cons, ih]

@[simp] theorem probeFilter_probes {α : Type} (p : α → Bool) (xs : List α) :
    (probeFilter p xs).probes = xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp only [probeFilter, ih, List.length_cons]

/-- Enumerate the shorter list, using membership in the longer list as oracle. -/
def intersect [DecidableEq Z] (left right : List Z) : ScanResult Z :=
  if left.length ≤ right.length then
    probeFilter (fun z => decide (z ∈ right)) left
  else
    probeFilter (fun z => decide (z ∈ left)) right

/-- Exact set semantics, valid even when the inputs contain duplicate values. -/
@[simp] theorem mem_intersect [DecidableEq Z] (left right : List Z) (z : Z) :
    z ∈ (intersect left right).values ↔ z ∈ left ∧ z ∈ right := by
  unfold intersect
  split <;> simp [and_comm]

/-- Exact predicate-call count. This is not a bound on the cost of each call. -/
@[simp] theorem intersect_probes [DecidableEq Z] (left right : List Z) :
    (intersect left right).probes = min left.length right.length := by
  unfold intersect
  split
  · rename_i h
    simp [Nat.min_eq_left h]
  · rename_i h
    simp [Nat.min_eq_right (Nat.le_of_lt (Nat.lt_of_not_ge h))]

theorem intersect_nodup [DecidableEq Z] (left right : List Z)
    (hleft : left.Nodup) (hright : right.Nodup) :
    (intersect left right).values.Nodup := by
  unfold intersect
  split
  · simpa [List.Nodup] using hleft.filter (fun z => decide (z ∈ right))
  · simpa [List.Nodup] using hright.filter (fun z => decide (z ∈ left))

theorem intersect_output_le_probes [DecidableEq Z] (left right : List Z) :
    (intersect left right).values.length ≤ (intersect left right).probes := by
  unfold intersect
  split <;> simp only [probeFilter_values, probeFilter_probes]
  · exact List.length_filter_le _ _
  · exact List.length_filter_le _ _

/-- Join each `R` row with its exact local intersection and accumulate the meter. -/
def triangle [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) : ScanResult (X × Y × Z) :=
  match r with
  | [] => ⟨[], 0⟩
  | (x, y) :: rest =>
    let slice := intersect (s y) (t x)
    let tail := triangle rest s t
    ⟨slice.values.map (fun z => (x, y, z)) ++ tail.values,
      slice.probes + tail.probes⟩

/-- The relational specification is derived from the executable implementation. -/
@[simp] theorem mem_triangle [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) (x : X) (y : Y) (z : Z) :
    (x, y, z) ∈ (triangle r s t).values ↔
      (x, y) ∈ r ∧ z ∈ s y ∧ z ∈ t x := by
  induction r with
  | nil => simp [triangle]
  | cons edge rest ih =>
    rcases edge with ⟨a, b⟩
    simp only [triangle, List.mem_append, List.mem_map, mem_intersect, ih,
      List.mem_cons, Prod.mk.injEq]
    constructor
    · intro h
      rcases h with ⟨w, ⟨hs, ht⟩, ha, hb, hz⟩ | ⟨hr, hs, ht⟩
      · subst x; subst y; subst z
        exact ⟨Or.inl ⟨rfl, rfl⟩, hs, ht⟩
      · exact ⟨Or.inr hr, hs, ht⟩
    · rintro ⟨h | h, hs, ht⟩
      · rcases h with ⟨ha, hb⟩
        subst x; subst y
        exact Or.inl ⟨z, ⟨hs, ht⟩, rfl, rfl, rfl⟩
      · exact Or.inr ⟨h, hs, ht⟩

theorem triangle_sound [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) (x : X) (y : Y) (z : Z)
    (h : (x, y, z) ∈ (triangle r s t).values) :
    (x, y) ∈ r ∧ z ∈ s y ∧ z ∈ t x :=
  (mem_triangle r s t x y z).mp h

theorem triangle_complete [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) (x : X) (y : Y) (z : Z)
    (h : (x, y) ∈ r ∧ z ∈ s y ∧ z ∈ t x) :
    (x, y, z) ∈ (triangle r s t).values :=
  (mem_triangle r s t x y z).mpr h

/-- Degree-adaptive candidate budget; repeated rows of `R` are charged repeatedly. -/
def adaptiveBudget (r : List (X × Y)) (s : Y → List Z) (t : X → List Z) : Nat :=
  (r.map (fun edge => min (s edge.2).length (t edge.1).length)).sum

/-- Fixed choice of enumerating `S` for every row of `R`. -/
def leftBudget (r : List (X × Y)) (s : Y → List Z) : Nat :=
  (r.map (fun edge => (s edge.2).length)).sum

/-- Fixed choice of enumerating `T` for every row of `R`. -/
def rightBudget (r : List (X × Y)) (t : X → List Z) : Nat :=
  (r.map (fun edge => (t edge.1).length)).sum

@[simp] theorem triangle_probes [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) :
    (triangle r s t).probes = adaptiveBudget r s t := by
  induction r with
  | nil => rfl
  | cons edge rest ih =>
    rcases edge with ⟨x, y⟩
    simp [triangle, adaptiveBudget, ih]

theorem adaptiveBudget_le_left (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) :
    adaptiveBudget r s t ≤ leftBudget r s := by
  induction r with
  | nil => exact Nat.le_refl 0
  | cons edge rest ih =>
    simp only [adaptiveBudget, leftBudget, List.map_cons, List.sum_cons] at *
    exact Nat.add_le_add (Nat.min_le_left _ _) ih

theorem adaptiveBudget_le_right (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) :
    adaptiveBudget r s t ≤ rightBudget r t := by
  induction r with
  | nil => exact Nat.le_refl 0
  | cons edge rest ih =>
    simp only [adaptiveBudget, rightBudget, List.map_cons, List.sum_cons] at *
    exact Nat.add_le_add (Nat.min_le_right _ _) ih

/-- Local adaptation never exceeds either fixed orientation in this probe model. -/
theorem adaptiveBudget_le_best_fixed (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) :
    adaptiveBudget r s t ≤ min (leftBudget r s) (rightBudget r t) :=
  Nat.le_min.mpr ⟨adaptiveBudget_le_left r s t, adaptiveBudget_le_right r s t⟩

theorem triangle_output_le_probes [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) :
    (triangle r s t).values.length ≤ (triangle r s t).probes := by
  induction r with
  | nil => exact Nat.le_refl 0
  | cons edge rest ih =>
    rcases edge with ⟨x, y⟩
    simp only [triangle, List.length_append, List.length_map]
    exact Nat.add_le_add (intersect_output_le_probes (s y) (t x)) ih

/-- Distinct base rows and distinct adjacency values suffice for distinct triples. -/
theorem triangle_nodup [DecidableEq Z] (r : List (X × Y))
    (s : Y → List Z) (t : X → List Z) (hr : r.Nodup)
    (hs : ∀ y, (s y).Nodup) (ht : ∀ x, (t x).Nodup) :
    (triangle r s t).values.Nodup := by
  induction r with
  | nil => exact List.nodup_nil
  | cons edge rest ih =>
    rcases edge with ⟨x, y⟩
    obtain ⟨hnotmem, hrest⟩ := List.nodup_cons.mp hr
    simp only [triangle]
    apply List.nodup_append.mpr
    refine ⟨?_, ih hrest, ?_⟩
    · apply List.Pairwise.map (fun z => (x, y, z)) ?_
        (intersect_nodup (s y) (t x) (hs y) (ht x))
      intro a b hab heq
      exact hab (congrArg (fun triple => triple.2.2) heq)
    · intro a ha b hb hab
      obtain ⟨z, _, rfl⟩ := List.mem_map.mp ha
      subst b
      exact hnotmem ((mem_triangle rest s t x y z).mp hb).1

end Leatherback.Join
