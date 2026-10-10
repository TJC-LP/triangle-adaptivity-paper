import LeatherbackSpectral

/-!
# Axiom audit

Every main theorem of `LeatherbackSpectral` is checked here with `#print axioms`, wrapped in
`#guard_msgs` so that `lake build` FAILS if any of them ever depends on anything beyond the
three standard axioms `propext`, `Classical.choice`, `Quot.sound` (in particular `sorryAx`,
`Lean.ofReduceBool` from `native_decide`, or a custom axiom).
-/

/-- info: 'LeatherbackSpectral.out_eq_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_eq_sum

/-- info: 'LeatherbackSpectral.out_eq_card' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_eq_card

/-- info: 'LeatherbackSpectral.out_rotate' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_rotate

/-- info: 'LeatherbackSpectral.out_rotate'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_rotate'

/-- info: 'LeatherbackSpectral.out_le_card_mul_of_rowDeg_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_card_mul_of_rowDeg_le

/-- info: 'LeatherbackSpectral.out_le_card_mul_of_colDeg_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_card_mul_of_colDeg_le

/-- info: 'LeatherbackSpectral.bilinear_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.bilinear_le

/-- info: 'LeatherbackSpectral.l2_opNorm_le_of_sum_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.l2_opNorm_le_of_sum_sq

/-- info: 'LeatherbackSpectral.rowDeg_le_opNorm_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.rowDeg_le_opNorm_sq

/-- info: 'LeatherbackSpectral.colDeg_le_opNorm_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.colDeg_le_opNorm_sq

/-- info: 'LeatherbackSpectral.opNorm_adj_le_sqrt_card' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_adj_le_sqrt_card

/-- info: 'LeatherbackSpectral.opNorm_adj_sq_le_card' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_adj_sq_le_card

/-- info: 'LeatherbackSpectral.one_le_opNorm_adj' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.one_le_opNorm_adj

/-- info: 'LeatherbackSpectral.opNorm_adj_le_schur' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_adj_le_schur

/-- info: 'LeatherbackSpectral.out_le_opNorm_mul_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_opNorm_mul_sqrt

/-- info: 'LeatherbackSpectral.out_le_card_mul_opNorm_sq_S' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_card_mul_opNorm_sq_S

/-- info: 'LeatherbackSpectral.out_le_card_mul_opNorm_sq_T' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_card_mul_opNorm_sq_T

/-- info: 'LeatherbackSpectral.out_le_rotation_terms' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_rotation_terms

/-- info: 'LeatherbackSpectral.theoremB_upper' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_upper

/-- info: 'LeatherbackSpectral.kernelWork_eq_out_nest' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_eq_out_nest

/-- info: 'LeatherbackSpectral.rowDeg_nestS' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.rowDeg_nestS

/-- info: 'LeatherbackSpectral.colDeg_nestT' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.colDeg_nestT

/-- info: 'LeatherbackSpectral.card_nestS' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.card_nestS

/-- info: 'LeatherbackSpectral.card_nestT' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.card_nestT

/-- info: 'LeatherbackSpectral.out_le_kernelWork' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_le_kernelWork

/-- info: 'LeatherbackSpectral.kernelWork_le_opNorm_mul_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_opNorm_mul_sqrt

/-- info: 'LeatherbackSpectral.kernelWork_le_of_rowDeg_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_of_rowDeg_le

/-- info: 'LeatherbackSpectral.kernelWork_le_of_colDeg_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_of_colDeg_le

/-- info: 'LeatherbackSpectral.kernelWork_le_card_S_of_colDeg_R_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_card_S_of_colDeg_R_le

/-- info: 'LeatherbackSpectral.kernelWork_le_card_T_of_rowDeg_R_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_card_T_of_rowDeg_R_le

/-- info: 'LeatherbackSpectral.kernelWork_le_terms' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWork_le_terms

/-- info: 'LeatherbackSpectral.kernel_min_le_U' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernel_min_le_U

/-- info: 'LeatherbackSpectral.card_blk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.card_blk

/-- info: 'LeatherbackSpectral.rowDeg_blk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.rowDeg_blk

/-- info: 'LeatherbackSpectral.colDeg_blk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.colDeg_blk

/-- info: 'LeatherbackSpectral.opNorm_blk_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_blk_le

/-- info: 'LeatherbackSpectral.opNorm_blk_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_blk_eq

/-- info: 'LeatherbackSpectral.out_blk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_blk

/-- info: 'LeatherbackSpectral.floor_facts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.floor_facts

/-- info: 'LeatherbackSpectral.max_mul_max_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.max_mul_max_le

/-- info: 'LeatherbackSpectral.Stats.real_shape_feasible' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.Stats.real_shape_feasible

/-- info: 'LeatherbackSpectral.Stats.Regular.min_r_le_U' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.Stats.Regular.min_r_le_U

/-- info: 'LeatherbackSpectral.Stats.real_shape_value' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.Stats.real_shape_value

/-- info: 'LeatherbackSpectral.Stats.real_shape_attains_U' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.Stats.real_shape_attains_U

/-- info: 'LeatherbackSpectral.Stats.block_params' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.Stats.block_params

/-- info: 'LeatherbackSpectral.theoremB_lower' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_lower

/-- info: 'LeatherbackSpectral.theoremB' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB

/-- info: 'LeatherbackSpectral.trace_le_opNorm_mul_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.trace_le_opNorm_mul_sqrt

/-- info: 'LeatherbackSpectral.trace_le_card_mul_opNorm_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.trace_le_card_mul_opNorm_sq

/-- info: 'LeatherbackSpectral.rowSum_le_opNorm_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.rowSum_le_opNorm_sq

/-- info: 'LeatherbackSpectral.colSum_le_opNorm_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.colSum_le_opNorm_sq

/-- info: 'LeatherbackSpectral.theoremB_upper_matrix' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_upper_matrix

/-- info: 'LeatherbackSpectral.trace_le_card_mul_opNorm_sq_T' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.trace_le_card_mul_opNorm_sq_T

/-- info: 'LeatherbackSpectral.eq_empty_of_card_le_of_lt_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.eq_empty_of_card_le_of_lt_one

/-- info: 'LeatherbackSpectral.eq_empty_of_opNorm_le_of_lt_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.eq_empty_of_opNorm_le_of_lt_one

/-- info: 'LeatherbackSpectral.out_empty_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_empty_left

/-- info: 'LeatherbackSpectral.out_empty_mid' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_empty_mid

/-- info: 'LeatherbackSpectral.out_empty_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.out_empty_right

/-- info: 'LeatherbackSpectral.theoremB_degenerate' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_degenerate

/-- info: 'LeatherbackSpectral.theoremB_cases' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_cases

/-- info: 'LeatherbackSpectral.opNorm_adj_diag2_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_adj_diag2_le

/-- info: 'LeatherbackSpectral.two_le_opNorm_sq_nestS_diag2' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.two_le_opNorm_sq_nestS_diag2

/-- info: 'LeatherbackSpectral.nestS_can_raise_opNorm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.nestS_can_raise_opNorm

/-- info: 'LeatherbackSpectral.kernelWorkNat_eq_kernelWork' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWorkNat_eq_kernelWork

/-- info: 'LeatherbackSpectral.kernelWorkNat_eq_kernelWork_fin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.kernelWorkNat_eq_kernelWork_fin

/-- info: 'LeatherbackSpectral.run_model_eq_kernelWork' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.run_model_eq_kernelWork

/-- info: 'LeatherbackSpectral.run_model_le_terms' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.run_model_le_terms

/-- info: 'LeatherbackSpectral.run_model_le_opNorm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.run_model_le_opNorm

/-- info: 'LeatherbackSpectral.opNorm_adj_empty' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.opNorm_adj_empty

/-- info: 'LeatherbackSpectral.admissible_exists_iff_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.admissible_exists_iff_nonneg

/-- info: 'LeatherbackSpectral.theoremB_degenerate_attained' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_degenerate_attained

/-- info: 'LeatherbackSpectral.run_walked_le_kernelWork_real' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.run_walked_le_kernelWork_real

/-- info: 'LeatherbackSpectral.run_walked_le_terms' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.run_walked_le_terms

/-- info: 'LeatherbackSpectral.sharpStats_regular' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.sharpStats_regular

/-- info: 'LeatherbackSpectral.sharpStats_U' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.sharpStats_U

/-- info: 'LeatherbackSpectral.sharpStats_out_le_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.sharpStats_out_le_one

/-- info: 'LeatherbackSpectral.sharpStats_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.sharpStats_witness

/-- info: 'LeatherbackSpectral.sharp_family' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.sharp_family

/-- info: 'LeatherbackSpectral.factor_four_sharp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.factor_four_sharp

/-- info: 'LeatherbackSpectral.theoremB_constant_sharp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms LeatherbackSpectral.theoremB_constant_sharp
