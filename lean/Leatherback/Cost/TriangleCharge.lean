import Leatherback.Join.TriangleBag

/-!
# Executable replica of the triangle kernel's work meter

A line-by-line, hand-written replica of the Leatherback triangle kernel's control flow and charges:

* `src/util/sorted_runs.zig`: `gallopLowerBoundBy`, `runEndBy`, `lowerBoundBy`,
  `upperBoundBy`, `equalRunEnd`, `dropsAt`, `intersectWalk`, `intersectEachBy`;
* `src/query/triangle_join.zig`: `seekKey`, `run`, `runGroup`, `Visit.visit`, `charge`.

Specialisation (the same one the extraction plan pins): `builtin.is_test = false`, every
`Sabotage` false, `Rel = SliceRel` with equal-length key and value columns,
`linear_steps = lanes = 16`, a total meter (deadline failure is not modelled), a sink that
never errors, and `usize`/`u64` arithmetic that never wraps (the gallop's `step *|= 2`
saturation and the `@min(n, maxInt(usize))` charge clamp are unreachable below `2^63`).
`GraphRel` reads the same `(key, value)` sequence through a permutation, so the replica
models both arms on the sequence the permutation presents.

This file is **not** generated from the Zig source: freshness against the shipped bytes is
established differentially (`bridge/triangle_check.py`, and the Zig bridge arms once the
kernel is merged), and later by extraction (`extract_triangle.py`, plan §1.3).

Every run reports, besides its end and sink, the three meter quantities of the contract:

* `model` (`M`): the **ideal precharged candidate budget**, the sum of the `noteWalk`
  arguments `Σ min(|N2(y)|, |N3(x)|)`. It is added *before* each intersection runs, so it
  is the number of shorter-side entries an intersection *may* read, not the number it does;
* `walked` (`W`): the walked-side entries `intersectWalk` actually consumed (`Σ ie - i`).
  The walk stops as soon as the galloped side is exhausted, so `W ≤ M` and the inequality
  can be strict (`walked_lt_model_example`: `M = 3`, `W = 1`);
* `charged` (`C`): the sum of every `n` passed to `meter.charge` by `run` (walked entries,
  galloping and seeks).

Theorems (`TriangleChargeProofs`): `lowerBoundBy_isLB`, `gallop_isLB`, `runEnd_isUB` (index characterisations on
non-decreasing columns), `seekKey_span` (the run of a key), `run_model_eq`: a completed
run over sorted inputs has `model = kernelWorkNat E1 E2 E3`, the Std mirror of
`LeatherbackSpectral.kernelWork`, and `run_walked_le_model`: `walked ≤ model` on every
input. Equality `model = kernelWorkNat` is about the candidate budget, not about the
entries actually read.
-/

namespace Leatherback.Cost.TriangleCharge

open Leatherback.Join.TriangleBag

/-- `sorted_runs.linear_steps = lanes = 16`. -/
def linearSteps : Nat := 16

/-- Bounds-checked read (`col.at(i)`; every read below is guarded by an index check). -/
def rd (c : Array Nat) (i : Nat) : Nat := c.getD i 0

/-! ## Searches (`sorted_runs.zig`) -/

/-- `lowerBoundBy`: bisection on `[lo, hi)`; one unit of work per probe. -/
def lowerBoundBy (c : Array Nat) (key lo hi work : Nat) : Nat × Nat :=
  if lo < hi then
    let mid := lo + (hi - lo) / 2
    if rd c mid < key then lowerBoundBy c key (mid + 1) hi (work + 1)
    else lowerBoundBy c key lo mid (work + 1)
  else (lo, work)
termination_by hi - lo

/-- `upperBoundBy`: bisection on `[lo, hi)` for the first value `> key`. -/
def upperBoundBy (c : Array Nat) (key lo hi work : Nat) : Nat × Nat :=
  if lo < hi then
    let mid := lo + (hi - lo) / 2
    if rd c mid ≤ key then upperBoundBy c key (mid + 1) hi (work + 1)
    else upperBoundBy c key lo mid (work + 1)
  else (lo, work)
termination_by hi - lo

/-- The linear prefix of `gallopLowerBoundBy`: `.inl i` at the first `col.at(i) >= key`,
`.inr stop` when the prefix is exhausted. -/
def linearLower (c : Array Nat) (key i stop work : Nat) : (Nat ⊕ Nat) × Nat :=
  if i < stop then
    if key ≤ rd c i then (.inl i, work + 1) else linearLower c key (i + 1) stop (work + 1)
  else (.inr i, work)
termination_by stop - i

/-- The exponential phase of `gallopLowerBoundBy` (`step ≥ 1` is invariant). -/
def expLower (c : Array Nat) (key n known step work : Nat) : Nat × Nat :=
  if 0 < step ∧ step < n - known then
    if key ≤ rd c (known + step) then lowerBoundBy c key (known + 1) (known + step) (work + 1)
    else expLower c key n (known + step) (2 * step) (work + 1)
  else lowerBoundBy c key (known + 1) n work
termination_by n - known

/-- `gallopLowerBoundBy(Col, col, from, key, work)`: `(index, work')`. -/
def gallop (c : Array Nat) (frm key work : Nat) : Nat × Nat :=
  if c.size ≤ frm then (c.size, work) else
  match linearLower c key frm (min c.size (frm + linearSteps)) work with
  | (.inl r, w) => (r, w)
  | (.inr i, w) => if c.size ≤ i then (c.size, w) else expLower c key c.size (i - 1) 1 w

/-- The linear prefix of `runEndBy`. -/
def linearRunEnd (c : Array Nat) (key j stop work : Nat) : (Nat ⊕ Nat) × Nat :=
  if j < stop then
    if rd c j ≠ key then (.inl j, work + 1) else linearRunEnd c key (j + 1) stop (work + 1)
  else (.inr j, work)
termination_by stop - j

/-- The exponential phase of `runEndBy`. -/
def expRunEnd (c : Array Nat) (key n known step work : Nat) : Nat × Nat :=
  if 0 < step ∧ step < n - known then
    if key < rd c (known + step) then upperBoundBy c key (known + 1) (known + step) (work + 1)
    else expRunEnd c key n (known + step) (2 * step) (work + 1)
  else upperBoundBy c key (known + 1) n work
termination_by n - known

/-- `runEndBy(Col, col, i, work)`: `(index, work')`. -/
def runEnd (c : Array Nat) (i work : Nat) : Nat × Nat :=
  if c.size ≤ i then (c.size, work) else
  match linearRunEnd c (rd c i) (i + 1) (min c.size (i + 1 + linearSteps)) work with
  | (.inl r, w) => (r, w)
  | (.inr j, w) => if c.size ≤ j then (c.size, w) else expRunEnd c (rd c i) c.size (j - 1) 1 w

/-- `equalRunEnd`: the first index at or after `e` whose value is not `v` (uncharged). -/
def equalRunEnd (c : Array Nat) (v e : Nat) : Nat :=
  if e < c.size ∧ rd c e = v then equalRunEnd c v (e + 1) else e
termination_by c.size - e

theorem equalRunEnd_ge (c : Array Nat) (v e : Nat) : e ≤ equalRunEnd c v e := by
  induction e using equalRunEnd.induct (c := c) (v := v) with
  | case1 e _ ih => rw [equalRunEnd]; simp only [*, and_self, if_true]; omega
  | case2 e h => rw [equalRunEnd]; simp [h]

/-- `dropsAt`: a decrease below `v` at index `i`. -/
def dropsAt (c : Array Nat) (i v : Nat) : Bool := decide (i < c.size) && decide (rd c i < v)

/-! ## Intersection (`intersectWalk`, `intersectEachBy`) -/

/-- How a walk or a run ended (`IntersectEnd`, `triangle_join.End`). -/
inductive End where
  | done
  | stopped
  | outOfOrder
  deriving DecidableEq, Repr

def End.name : End → String
  | .done => "done"
  | .stopped => "stopped"
  | .outOfOrder => "out_of_order"

/-- The state a walk threads: the visitor's world, the caller's `work` cell and `W`. -/
structure Walk (σ : Type) where
  state : σ
  work : Nat
  walked : Nat

/-- `intersectWalk(Col, s, l, ctx, visit, work)` from cursor state `(i, lo)`. -/
def walkLoop {σ : Type} (visit : Nat → Nat → σ → Bool × σ) (s l : Array Nat) (i lo : Nat)
    (acc : Walk σ) : End × Walk σ :=
  if _hi : i < s.size then
    let v := rd s i
    let ie := equalRunEnd s v (i + 1)
    let acc := { acc with work := acc.work + (ie - i), walked := acc.walked + (ie - i) }
    if dropsAt s ie v then (.outOfOrder, acc) else
    let g := gallop l lo v acc.work
    let acc := { acc with work := g.2 }
    if l.size ≤ g.1 then (.done, acc) else
    if dropsAt l g.1 v then (.outOfOrder, acc) else
    if rd l g.1 = v then
      let he := equalRunEnd l v (g.1 + 1)
      let acc := { acc with work := acc.work + (he - g.1) }
      if dropsAt l he v then (.outOfOrder, acc) else
      let r := visit v ((ie - i) * (he - g.1)) acc.state
      let acc := { acc with state := r.2 }
      if r.1 then walkLoop visit s l ie he acc else (.stopped, acc)
    else walkLoop visit s l ie g.1 acc
  else (.done, acc)
termination_by s.size - i
decreasing_by
  all_goals
    have := equalRunEnd_ge s (rd s i) (i + 1)
    omega

/-- `intersectEachBy`: walk the shorter column (ties walk `a`). -/
def intersectEach {σ : Type} (visit : Nat → Nat → σ → Bool × σ) (a b : Array Nat)
    (acc : Walk σ) : End × Walk σ :=
  if a.size ≤ b.size then walkLoop visit a b 0 0 acc else walkLoop visit b a 0 0 acc

/-! ## The kernel (`triangle_join.zig`) -/

/-- A `SliceRel`: equal-length key and value columns. -/
structure Rel where
  keys : Array Nat
  vals : Array Nat
  size_eq : keys.size = vals.size

/-- `SliceRel` over a list of `(key, value)` rows, in the given order. -/
def Rel.ofPairs (E : List (Nat × Nat)) : Rel :=
  ⟨(E.map Prod.fst).toArray, (E.map Prod.snd).toArray, by simp⟩

/-- `rel.valCol(lo, hi)`. -/
def Rel.valCol (r : Rel) (lo hi : Nat) : Array Nat := r.vals.extract lo hi

/-- `seekKey`: `((lo, hi), cursor', work')`, the run of `key` searched from `cursor`. -/
def seekKey (keys : Array Nat) (cursor key work : Nat) : (Nat × Nat) × Nat × Nat :=
  let g := gallop keys cursor key work
  if keys.size ≤ g.1 ∨ rd keys g.1 ≠ key then ((g.1, g.1), g.1, g.2)
  else
    let e := runEnd keys g.1 g.2
    ((g.1, e.1), g.1, e.2)

/-- The meter quantities and the sink, threaded through `run`. -/
structure Acc (σ : Type) where
  /-- The visitor's world. -/
  sink : σ
  /-- `C`: every unit passed to `meter.charge` (walks, gallops, seeks). -/
  charged : Nat
  /-- `M`: the ideal precharged candidate budget, `min(|N2(y)|, |N3(x)|)` added per `E1` row
  before its intersection runs. An upper bound on `walked`, not a count of reads. -/
  model : Nat
  /-- `W`: walked-side entries actually consumed; `walked ≤ model` (`run_walked_le_model`). -/
  walked : Nat

/-- `runGroup`: rows `[r, j)` of an `x` group against `N3(x)`. -/
def groupLoop {σ : Type} (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 : Rel)
    (x i j : Nat) (n3 : Array Nat) (r prevY k2 : Nat) (acc : Acc σ) : End × Acc σ :=
  if r < j then
    if rd r1.keys r ≠ x then (.outOfOrder, acc) else
    let y := rd r1.vals r
    if i < r ∧ y < prevY then (.outOfOrder, acc) else
    let sk := seekKey r2.keys k2 y 1
    if sk.1.1 ≠ sk.1.2 then
      let n2 := r2.valCol sk.1.1 sk.1.2
      let acc := { acc with model := acc.model + min n2.size n3.size }
      let w := intersectEach (fun z m st => visit x y z m st) n2 n3 ⟨acc.sink, sk.2.2, acc.walked⟩
      let acc := { acc with sink := w.2.state, walked := w.2.walked }
      match w.1 with
      | .done => groupLoop visit r1 r2 x i j n3 (r + 1) y sk.2.1
          { acc with charged := acc.charged + w.2.work }
      | .stopped => (.stopped, acc)
      | .outOfOrder => (.outOfOrder, acc)
    else groupLoop visit r1 r2 x i j n3 (r + 1) y sk.2.1
      { acc with charged := acc.charged + sk.2.2 }
  else (.done, acc)
termination_by j - r

/-- `run`'s outer loop over `x` groups from row `i` with `E3` cursor `k3`. -/
def outer {σ : Type} (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 r3 : Rel)
    (i k3 : Nat) (acc : Acc σ) : End × Acc σ :=
  if i < r1.keys.size then
    let x := rd r1.keys i
    let g := runEnd r1.keys i 1
    if hbad : g.1 ≤ i ∨ (g.1 < r1.keys.size ∧ rd r1.keys g.1 < x) then (.outOfOrder, acc) else
    have : i < (runEnd r1.keys i 1).1 := (by omega : i < g.1)
    let sk := seekKey r3.keys k3 x g.2
    if sk.1.1 = sk.1.2 then
      outer visit r1 r2 r3 g.1 sk.2.1 { acc with charged := acc.charged + (sk.2.2 + (g.1 - i)) }
    else
      let acc := { acc with charged := acc.charged + sk.2.2 }
      match groupLoop visit r1 r2 x i g.1 (r3.valCol sk.1.1 sk.1.2) i 0 0 acc with
      | (.done, acc) => outer visit r1 r2 r3 g.1 sk.2.1 acc
      | (.stopped, acc) => (.stopped, acc)
      | (.outOfOrder, acc) => (.outOfOrder, acc)
  else (.done, acc)
termination_by r1.keys.size - i

/-- `run(Rel, r1, r2, r3, sink, meter)` with sink world `σ`. -/
def run {σ : Type} (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 r3 : Rel) (sink : σ) :
    End × Acc σ :=
  outer visit r1 r2 r3 0 0 ⟨sink, 0, 0, 0⟩

/-! ## Sinks -/

/-- A recording sink that accepts the first `limit` matches and refuses the next one
(the bridge's `triangle_rows` with no limit, `triangle_stop` with one). -/
structure RowSink where
  rows : Array Row
  limit : Option Nat

def rowVisit (x y z m : Nat) (st : RowSink) : Bool × RowSink :=
  match st.limit with
  | some k => if k ≤ st.rows.size then (false, st) else (true, { st with rows := st.rows.push (x, y, z, m) })
  | none => (true, { st with rows := st.rows.push (x, y, z, m) })

/-- `CountSink`: `total +|= mult` on `u64`. -/
def countVisit (_x _y _z m : Nat) (total : Nat) : Bool × Nat :=
  (true, min (total + m) (2 ^ 64 - 1))

/-- The uniform per-call search bound `G(N) = linear_steps + 2·(⌊log₂ N⌋ + 1)`. -/
def searchBound (n : Nat) : Nat := linearSteps + 2 * (Nat.log2 n + 1)

/-- The contract's charge bound on sets:
`C ≤ (3 + 5·G(N))·|E1| + (2 + G(N))·M` with `N` the longest column. -/
def chargeBound (n1 n2 n3 model : Nat) : Nat :=
  let g := searchBound (max n1 (max n2 n3))
  (3 + 5 * g) * n1 + (2 + g) * model

end Leatherback.Cost.TriangleCharge
