import Leatherback.Cost.TriangleChargeProofs

/-!
# Axiom audit of the Std-only triangle-kernel modules

The spectral library imports these four Std-only modules (reference semantics and a
line-by-line cost replica of Leatherback's triangle kernel). Each theorem below is
pinned to its exact axiom set with `#guard_msgs`, so `lake build` fails if any of them
gains an axiom (in particular `sorryAx`, `Lean.ofReduceBool`, or a custom axiom).
-/

/-- info: 'Leatherback.Join.TriangleBag.kernelWorkNat_eq_adaptiveBudget' does not depend on any axioms -/
#guard_msgs in
#print axioms Leatherback.Join.TriangleBag.kernelWorkNat_eq_adaptiveBudget

/-- info: 'Leatherback.Join.TriangleBag.bagRows_support_nodup' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Join.TriangleBag.bagRows_support_nodup

/-- info: 'Leatherback.Join.TriangleBag.bagCount_le_kernelWorkNat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Join.TriangleBag.bagCount_le_kernelWorkNat

/-- info: 'Leatherback.Join.TriangleBag.bagCount_eq_triangle_length' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Join.TriangleBag.bagCount_eq_triangle_length

/-- info: 'Leatherback.Cost.TriangleCharge.gallop_isLB' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.gallop_isLB

/-- info: 'Leatherback.Cost.TriangleCharge.runEnd_isUB' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.runEnd_isUB

/-- info: 'Leatherback.Cost.TriangleCharge.seekKey_span' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.seekKey_span

/-- info: 'Leatherback.Cost.TriangleCharge.run_model_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.run_model_eq

/-- info: 'Leatherback.Cost.TriangleCharge.run_done' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.run_done

/-- info: 'Leatherback.Cost.TriangleCharge.run_model_eq_sorted' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.run_model_eq_sorted

/-- info: 'Leatherback.Cost.TriangleCharge.run_walked_le_model' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.run_walked_le_model

/-- info: 'Leatherback.Cost.TriangleCharge.run_walked_le_kernelWork' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.run_walked_le_kernelWork

/-- info: 'Leatherback.Cost.TriangleCharge.walked_lt_model_example' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms Leatherback.Cost.TriangleCharge.walked_lt_model_example
