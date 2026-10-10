import LeatherbackSpectral.Kernel

/-!
# Theorem B, lower bound: the block instance `B(a, b, c, m)` and the rounding argument

* `blk m a b`: `m` vertex-disjoint complete blocks `K_{a,b}` on `Fin m × Fin a` and
  `Fin m × Fin b` (Kronecker `I_m ⊗ J_{a×b}`). Sizes `mab`, degrees `b` / `a`,
  `‖A‖₂ = √(ab)` (Schur test for `≤`, an explicit test pair for `≥`), and
  `Out(B(a,b,c,m)) = m a b c`.
* The statistic-driven parameters `a = ⌊max(1, U/r_S)⌋`, `b = ⌊max(1, U/r_T)⌋`,
  `c = ⌊max(1, U/r_R)⌋`, `m = ⌊min(r_R/ab, r_S/bc, r_T/ca)⌋` are admissible and give
  `4 · Out > U` (`theoremB_lower`).
* Over real parameters (no floors) the block shape attains exactly `U`
  (`real_shape_feasible`, `real_shape_value`).
-/

open Finset Matrix
open scoped Matrix.Norms.L2Operator

namespace LeatherbackSpectral

/-! ### The block instance -/

section Block

variable {m a b c : ℕ}

/-- `m` disjoint complete bipartite blocks `K_{a,b}`: `(i, ·) ~ (j, ·)` iff `i = j`. -/
def blk (m a b : ℕ) : Finset ((Fin m × Fin a) × (Fin m × Fin b)) :=
  univ.filter fun p => p.1.1 = p.2.1

lemma adj_blk (x : Fin m × Fin a) (y : Fin m × Fin b) :
    adj (blk m a b) x y = if x.1 = y.1 then 1 else 0 := by
  simp [adj, blk]

lemma rowDeg_blk (x : Fin m × Fin a) : rowDeg (blk m a b) x = b := by
  rw [rowDeg, Fintype.sum_prod_type, Finset.sum_eq_single x.1]
  · simp [adj_blk]
  · intro i _ hi; simp [adj_blk, Ne.symm hi]
  · simp

lemma colDeg_blk (y : Fin m × Fin b) : colDeg (blk m a b) y = a := by
  rw [colDeg, Fintype.sum_prod_type, Finset.sum_eq_single y.1]
  · simp [adj_blk]
  · intro i _ hi; simp [adj_blk, hi]
  · simp

/-- `|B_R| = m a b`. -/
lemma card_blk : ((blk m a b).card : ℝ) = m * a * b := by
  rw [← sum_rowDeg]
  simp [rowDeg_blk, mul_assoc]

/-- Schur-test bound: `‖I_m ⊗ J_{a×b}‖₂ ≤ √(ab)`. -/
lemma opNorm_blk_le : ‖adj (blk m a b)‖ ≤ √((a : ℝ) * b) := by
  rw [mul_comm]
  exact opNorm_adj_le_schur _ (Nat.cast_nonneg _) (Nat.cast_nonneg _)
    (fun x => (rowDeg_blk x).le) (fun y => (colDeg_blk y).le)

/-- The norm of the block instance is exactly `√(ab)` when it is nonempty. -/
lemma opNorm_blk_eq (hm : 0 < m) (ha : 0 < a) (hb : 0 < b) :
    ‖adj (blk m a b)‖ = √((a : ℝ) * b) := by
  refine le_antisymm opNorm_blk_le ?_
  set i0 : Fin m := ⟨0, hm⟩
  have h := bilinear_le (adj (blk m a b)) (fun x => if x.1 = i0 then 1 else 0)
    (fun y => if y.1 = i0 then 1 else 0)
  have hl : ∑ x : Fin m × Fin a, ∑ y : Fin m × Fin b,
      (if x.1 = i0 then (1 : ℝ) else 0) * adj (blk m a b) x y *
        (if y.1 = i0 then (1 : ℝ) else 0) = (a : ℝ) * b := by
    simp only [adj_blk, Fintype.sum_prod_type]
    simp [Finset.sum_ite_eq']
  have hu : ∑ x : Fin m × Fin a, (if x.1 = i0 then (1 : ℝ) else 0) ^ 2 = a := by
    simp only [Fintype.sum_prod_type]
    simp
  have hv : ∑ y : Fin m × Fin b, (if y.1 = i0 then (1 : ℝ) else 0) ^ 2 = b := by
    simp only [Fintype.sum_prod_type]
    simp
  rw [hl, hu, hv, mul_assoc, ← Real.sqrt_mul (Nat.cast_nonneg _)] at h
  have hP : 0 < (a : ℝ) * b := by positivity
  have hs : 0 < √((a : ℝ) * b) := Real.sqrt_pos.2 hP
  have hss : √((a : ℝ) * b) * √((a : ℝ) * b) = a * b := Real.mul_self_sqrt hP.le
  nlinarith

/-- `Out(B(a, b, c, m)) = m a b c`. -/
lemma out_blk : out (blk m a b) (blk m b c) (blk m c a) = m * a * b * c := by
  rw [out_eq_sum]
  have h : ∀ (x : Fin m × Fin a) (y : Fin m × Fin b),
      ∑ z, adj (blk m a b) x y * adj (blk m b c) y z * adj (blk m c a) z x =
        adj (blk m a b) x y * c := by
    intro x y
    rw [adj_blk]
    split_ifs with hxy
    · simp only [one_mul]
      simp only [adj_blk, Fintype.sum_prod_type, hxy]
      simp [eq_comm]
    · simp
  simp_rw [h, ← Finset.sum_mul]
  rw [sum_adj, card_blk]

end Block

/-! ### Real arithmetic for the rounding argument -/

/-- **R4.** For `x ≥ 1`: `1 ≤ ⌊x⌋`, `⌊x⌋ ≤ x` and `x < 2 ⌊x⌋`. -/
lemma floor_facts {x : ℝ} (hx : 1 ≤ x) :
    1 ≤ ⌊x⌋₊ ∧ (⌊x⌋₊ : ℝ) ≤ x ∧ x < 2 * ⌊x⌋₊ := by
  have h1 : 1 ≤ ⌊x⌋₊ := Nat.le_floor (by simpa using hx)
  have h2 : (⌊x⌋₊ : ℝ) ≤ x := Nat.floor_le (by linarith)
  have h3 : x < ⌊x⌋₊ + 1 := Nat.lt_floor_add_one x
  have h4 : (1 : ℝ) ≤ ⌊x⌋₊ := by exact_mod_cast h1
  exact ⟨h1, h2, by linarith⟩

/-- **R1 + R2 (feasibility of the real shape).** -/
lemma max_mul_max_le {s p q U : ℝ} (hs : 1 ≤ s) (hp : 0 < p) (hq : 0 < q)
    (h1 : U ≤ p * s) (h2 : U ≤ q * s) (h3 : U ^ 2 ≤ s * p * q) :
    max 1 (U / p) * max 1 (U / q) ≤ s := by
  rcases le_total 1 (U / p) with ha | ha <;> rcases le_total 1 (U / q) with hb | hb
  · rw [max_eq_right ha, max_eq_right hb, div_mul_div_comm, div_le_iff₀ (mul_pos hp hq)]
    nlinarith
  · rw [max_eq_right ha, max_eq_left hb, mul_one, div_le_iff₀ hp]; linarith
  · rw [max_eq_left ha, max_eq_right hb, one_mul, div_le_iff₀ hq]; linarith
  · rw [max_eq_left ha, max_eq_left hb]; linarith

namespace Stats

variable (st : Stats)

/-- The non-degenerate regime: all `r_i ≥ 1` and all `σ_i ≥ 1`. -/
structure Regular : Prop where
  rR : 1 ≤ st.rR
  rS : 1 ≤ st.rS
  rT : 1 ≤ st.rT
  σR : 1 ≤ st.σR
  σS : 1 ≤ st.σS
  σT : 1 ≤ st.σT

variable {st}

lemma Regular.one_le_sR (h : st.Regular) : 1 ≤ st.sR := le_min (one_le_pow₀ h.σR) h.rR
lemma Regular.one_le_sS (h : st.Regular) : 1 ≤ st.sS := le_min (one_le_pow₀ h.σS) h.rS
lemma Regular.one_le_sT (h : st.Regular) : 1 ≤ st.sT := le_min (one_le_pow₀ h.σT) h.rT

lemma one_le_sqrt3 {p q r : ℝ} (hp : 1 ≤ p) (hq : 1 ≤ q) (hr : 1 ≤ r) : 1 ≤ √(p * q * r) :=
  Real.one_le_sqrt.2 (one_le_mul_of_one_le_of_one_le (one_le_mul_of_one_le_of_one_le hp hq) hr)

lemma Regular.one_le_U (h : st.Regular) : 1 ≤ st.U :=
  st.le_U (one_le_sqrt3 h.one_le_sR h.rS h.rT) (one_le_sqrt3 h.one_le_sS h.rT h.rR)
    (one_le_sqrt3 h.one_le_sT h.rR h.rS)
    (one_le_mul_of_one_le_of_one_le h.rR h.one_le_sS)
    (one_le_mul_of_one_le_of_one_le h.rR h.one_le_sT)
    (one_le_mul_of_one_le_of_one_le h.rS h.one_le_sR)
    (one_le_mul_of_one_le_of_one_le h.rS h.one_le_sT)
    (one_le_mul_of_one_le_of_one_le h.rT h.one_le_sR)
    (one_le_mul_of_one_le_of_one_le h.rT h.one_le_sS)

lemma sq_le_of_le_sqrt {u P : ℝ} (hu : 0 ≤ u) (hP : 0 ≤ P) (h : u ≤ √P) : u ^ 2 ≤ P := by
  calc u ^ 2 ≤ √P ^ 2 := pow_le_pow_left₀ hu h 2
    _ = P := Real.sq_sqrt hP

/-- Shape parameters before flooring. -/
noncomputable def α (st : Stats) : ℝ := max 1 (st.U / st.rS)
noncomputable def β (st : Stats) : ℝ := max 1 (st.U / st.rT)
noncomputable def γ (st : Stats) : ℝ := max 1 (st.U / st.rR)

/-- **Lemma 4.2.** The real shape is feasible: `αβ ≤ s_R`, `βγ ≤ s_S`, `γα ≤ s_T`. -/
theorem real_shape_feasible (h : st.Regular) :
    st.α * st.β ≤ st.sR ∧ st.β * st.γ ≤ st.sS ∧ st.γ * st.α ≤ st.sT := by
  have hU0 : 0 ≤ st.U := zero_le_one.trans h.one_le_U
  have p1 : (0 : ℝ) ≤ 1 := zero_le_one
  refine ⟨?_, ?_, ?_⟩
  · refine max_mul_max_le h.one_le_sR (by linarith [h.rS]) (by linarith [h.rT])
      st.U_le_DSR st.U_le_DTR ?_
    exact sq_le_of_le_sqrt hU0 (mul_nonneg (mul_nonneg (by linarith [h.one_le_sR]) (by linarith [h.rS])) (by linarith [h.rT])) st.U_le_HR
  · refine max_mul_max_le h.one_le_sS (by linarith [h.rT]) (by linarith [h.rR])
      st.U_le_DTS st.U_le_DRS ?_
    exact sq_le_of_le_sqrt hU0 (mul_nonneg (mul_nonneg (by linarith [h.one_le_sS]) (by linarith [h.rT])) (by linarith [h.rR])) st.U_le_HS
  · refine max_mul_max_le h.one_le_sT (by linarith [h.rR]) (by linarith [h.rS])
      st.U_le_DRT st.U_le_DST ?_
    exact sq_le_of_le_sqrt hU0 (mul_nonneg (mul_nonneg (by linarith [h.one_le_sT]) (by linarith [h.rR])) (by linarith [h.rS])) st.U_le_HT

/-- `U ≥ min(r_R, r_S, r_T)`. -/
lemma Regular.min_r_le_U (h : st.Regular) : min st.rR (min st.rS st.rT) ≤ st.U := by
  set μ := min st.rR (min st.rS st.rT)
  have hμR : μ ≤ st.rR := min_le_left _ _
  have hμS : μ ≤ st.rS := (min_le_right _ _).trans (min_le_left _ _)
  have hμT : μ ≤ st.rT := (min_le_right _ _).trans (min_le_right _ _)
  have hμ1 : 1 ≤ μ := le_min h.rR (le_min h.rS h.rT)
  have hH : ∀ {s p q : ℝ}, 1 ≤ s → μ ≤ p → μ ≤ q → μ ≤ √(s * p * q) := by
    intro s p q hs hp hq
    refine Real.le_sqrt_of_sq_le ?_
    have hp0 : 0 ≤ p := by linarith
    have hq0 : 0 ≤ q := by linarith
    nlinarith [mul_le_mul hp hq (by linarith) hp0, mul_nonneg (sub_nonneg.2 hs) (mul_nonneg hp0 hq0)]
  have hD : ∀ {r s : ℝ}, 1 ≤ s → μ ≤ r → μ ≤ r * s := by
    intro r s hs hr; nlinarith
  exact st.le_U (hH h.one_le_sR hμS hμT) (hH h.one_le_sS hμT hμR) (hH h.one_le_sT hμR hμS)
    (hD h.one_le_sS hμR) (hD h.one_le_sT hμR) (hD h.one_le_sR hμS) (hD h.one_le_sT hμS)
    (hD h.one_le_sR hμT) (hD h.one_le_sS hμT)

lemma max_one_div_mul {U r : ℝ} (hr : 0 < r) : max 1 (U / r) * r = max r U := by
  rw [max_mul_of_nonneg _ _ hr.le, one_mul, div_mul_cancel₀ _ hr.ne']

/-- **Lemma 4.3 (the real value is `U`).** `min(γ r_R, α r_S, β r_T) = U`; with
`m* = min(r_R/αβ, r_S/βγ, r_T/γα)` this is `m* αβγ = U`. -/
theorem real_shape_value (h : st.Regular) :
    min (st.γ * st.rR) (min (st.α * st.rS) (st.β * st.rT)) = st.U := by
  have hR : 0 < st.rR := by linarith [h.rR]
  have hS : 0 < st.rS := by linarith [h.rS]
  have hT : 0 < st.rT := by linarith [h.rT]
  simp only [γ, α, β, max_one_div_mul hR, max_one_div_mul hS, max_one_div_mul hT]
  refine le_antisymm ?_ (le_min (le_max_right _ _) (le_min (le_max_right _ _) (le_max_right _ _)))
  have hm := h.min_r_le_U
  rcases min_choice st.rR (min st.rS st.rT) with e | e <;> rw [e] at hm
  · exact (min_le_left _ _).trans (max_le hm le_rfl)
  · rcases min_choice st.rS st.rT with e' | e' <;> rw [e'] at hm
    · exact (min_le_right _ _).trans ((min_le_left _ _).trans (max_le hm le_rfl))
    · exact (min_le_right _ _).trans ((min_le_right _ _).trans (max_le hm le_rfl))

/-- `m* := min(r_R/αβ, r_S/βγ, r_T/γα)` -/
noncomputable def mStar (st : Stats) : ℝ :=
  min (st.rR / (st.α * st.β)) (min (st.rS / (st.β * st.γ)) (st.rT / (st.γ * st.α)))

/-- Over real block parameters the shape `(α, β, γ, m*)` is feasible with `m* ≥ 1`
and attains exactly `U`: `m* · αβγ = U`. -/
theorem real_shape_attains_U (h : st.Regular) :
    1 ≤ st.mStar ∧ st.mStar * (st.α * st.β * st.γ) = st.U := by
  obtain ⟨f1, f2, f3⟩ := real_shape_feasible h
  have hα : 1 ≤ st.α := le_max_left _ _
  have hβ : 1 ≤ st.β := le_max_left _ _
  have hγ : 1 ≤ st.γ := le_max_left _ _
  have pab : 0 < st.α * st.β := by positivity
  have pbc : 0 < st.β * st.γ := by positivity
  have pca : 0 < st.γ * st.α := by positivity
  refine ⟨?_, ?_⟩
  · refine le_min ?_ (le_min ?_ ?_)
    · exact (one_le_div pab).2 (f1.trans (min_le_right _ _))
    · exact (one_le_div pbc).2 (f2.trans (min_le_right _ _))
    · exact (one_le_div pca).2 (f3.trans (min_le_right _ _))
  · rw [← real_shape_value h, mStar, min_mul_of_nonneg _ _ (by positivity),
      min_mul_of_nonneg _ _ (by positivity)]
    congr 1
    · field_simp
    · congr 1 <;> field_simp

/-! ### Integer parameters -/

/-- Floored shape parameters `a = ⌊α⌋`, `b = ⌊β⌋`, `c = ⌊γ⌋`. -/
noncomputable def a (st : Stats) : ℕ := ⌊st.α⌋₊
noncomputable def b (st : Stats) : ℕ := ⌊st.β⌋₊
noncomputable def c (st : Stats) : ℕ := ⌊st.γ⌋₊

/-- `μ = min(r_R/ab, r_S/bc, r_T/ca)` and `m = ⌊μ⌋`. -/
noncomputable def μ (st : Stats) : ℝ :=
  min (st.rR / ((st.a : ℝ) * st.b)) (min (st.rS / ((st.b : ℝ) * st.c)) (st.rT / ((st.c : ℝ) * st.a)))
noncomputable def m (st : Stats) : ℕ := ⌊st.μ⌋₊

/-- **R5 (rounding assembly).** The integer parameters are `≥ 1`, satisfy the norm
constraints `ab ≤ s_R`, `bc ≤ s_S`, `ca ≤ s_T` and the size constraints
`mab ≤ r_R`, `mbc ≤ r_S`, `mca ≤ r_T`, and `U < 4 mabc`. -/
theorem block_params (h : st.Regular) :
    1 ≤ st.a ∧ 1 ≤ st.b ∧ 1 ≤ st.c ∧ 1 ≤ st.m ∧
      (st.a : ℝ) * st.b ≤ st.sR ∧ (st.b : ℝ) * st.c ≤ st.sS ∧ (st.c : ℝ) * st.a ≤ st.sT ∧
      (st.m : ℝ) * st.a * st.b ≤ st.rR ∧ (st.m : ℝ) * st.b * st.c ≤ st.rS ∧
      (st.m : ℝ) * st.c * st.a ≤ st.rT ∧
      st.U < 4 * ((st.m : ℝ) * st.a * st.b * st.c) := by
  obtain ⟨f1, f2, f3⟩ := real_shape_feasible h
  have hα : 1 ≤ st.α := le_max_left _ _
  have hβ : 1 ≤ st.β := le_max_left _ _
  have hγ : 1 ≤ st.γ := le_max_left _ _
  obtain ⟨a1, a2, a3⟩ := floor_facts hα
  obtain ⟨b1, b2, b3⟩ := floor_facts hβ
  obtain ⟨c1, c2, c3⟩ := floor_facts hγ
  have ha : (1 : ℝ) ≤ st.a := by exact_mod_cast a1
  have hb : (1 : ℝ) ≤ st.b := by exact_mod_cast b1
  have hc : (1 : ℝ) ≤ st.c := by exact_mod_cast c1
  change (st.a : ℝ) ≤ st.α at a2
  change (st.b : ℝ) ≤ st.β at b2
  change (st.c : ℝ) ≤ st.γ at c2
  change st.α < 2 * (st.a : ℝ) at a3
  change st.β < 2 * (st.b : ℝ) at b3
  change st.γ < 2 * (st.c : ℝ) at c3
  have hR : 0 < st.rR := by linarith [h.rR]
  have hS : 0 < st.rS := by linarith [h.rS]
  have hT : 0 < st.rT := by linarith [h.rT]
  have ab : (st.a : ℝ) * st.b ≤ st.sR :=
    (mul_le_mul a2 b2 (by positivity) (by linarith)).trans f1
  have bc : (st.b : ℝ) * st.c ≤ st.sS :=
    (mul_le_mul b2 c2 (by positivity) (by linarith)).trans f2
  have ca : (st.c : ℝ) * st.a ≤ st.sT :=
    (mul_le_mul c2 a2 (by positivity) (by linarith)).trans f3
  have abR : (st.a : ℝ) * st.b ≤ st.rR := ab.trans (min_le_right _ _)
  have bcS : (st.b : ℝ) * st.c ≤ st.rS := bc.trans (min_le_right _ _)
  have caT : (st.c : ℝ) * st.a ≤ st.rT := ca.trans (min_le_right _ _)
  have pab : 0 < (st.a : ℝ) * st.b := by positivity
  have pbc : 0 < (st.b : ℝ) * st.c := by positivity
  have pca : 0 < (st.c : ℝ) * st.a := by positivity
  have hμ : 1 ≤ st.μ := by
    refine le_min ?_ (le_min ?_ ?_)
    · exact (one_le_div pab).2 abR
    · exact (one_le_div pbc).2 bcS
    · exact (one_le_div pca).2 caT
  obtain ⟨m1, m2, m3⟩ := floor_facts hμ
  change (st.m : ℝ) ≤ st.μ at m2
  change st.μ < 2 * (st.m : ℝ) at m3
  have hm0 : (0 : ℝ) ≤ st.m := Nat.cast_nonneg _
  -- size constraints
  have sizeR : (st.m : ℝ) * st.a * st.b ≤ st.rR := by
    have : st.μ ≤ st.rR / ((st.a : ℝ) * st.b) := min_le_left _ _
    have := mul_le_mul_of_nonneg_right (m2.trans this) pab.le
    rw [div_mul_cancel₀ _ pab.ne'] at this
    linarith [mul_assoc (st.m : ℝ) st.a st.b]
  have sizeS : (st.m : ℝ) * st.b * st.c ≤ st.rS := by
    have : st.μ ≤ st.rS / ((st.b : ℝ) * st.c) := (min_le_right _ _).trans (min_le_left _ _)
    have := mul_le_mul_of_nonneg_right (m2.trans this) pbc.le
    rw [div_mul_cancel₀ _ pbc.ne'] at this
    linarith [mul_assoc (st.m : ℝ) st.b st.c]
  have sizeT : (st.m : ℝ) * st.c * st.a ≤ st.rT := by
    have : st.μ ≤ st.rT / ((st.c : ℝ) * st.a) := (min_le_right _ _).trans (min_le_right _ _)
    have := mul_le_mul_of_nonneg_right (m2.trans this) pca.le
    rw [div_mul_cancel₀ _ pca.ne'] at this
    linarith [mul_assoc (st.m : ℝ) st.c st.a]
  -- output: each floored coordinate loses less than half
  have hγU : st.U ≤ st.γ * st.rR := by
    have := le_max_right 1 (st.U / st.rR)
    have := mul_le_mul_of_nonneg_right this hR.le
    rwa [div_mul_cancel₀ _ hR.ne'] at this
  have hαU : st.U ≤ st.α * st.rS := by
    have := le_max_right 1 (st.U / st.rS)
    have := mul_le_mul_of_nonneg_right this hS.le
    rwa [div_mul_cancel₀ _ hS.ne'] at this
  have hβU : st.U ≤ st.β * st.rT := by
    have := le_max_right 1 (st.U / st.rT)
    have := mul_le_mul_of_nonneg_right this hT.le
    rwa [div_mul_cancel₀ _ hT.ne'] at this
  have cR : st.U < 2 * st.c * st.rR :=
    lt_of_le_of_lt hγU (by have := mul_lt_mul_of_pos_right c3 hR; linarith)
  have aS : st.U < 2 * st.a * st.rS :=
    lt_of_le_of_lt hαU (by have := mul_lt_mul_of_pos_right a3 hS; linarith)
  have bT : st.U < 2 * st.b * st.rT :=
    lt_of_le_of_lt hβU (by have := mul_lt_mul_of_pos_right b3 hT; linarith)
  have habc : 0 < (st.a : ℝ) * st.b * st.c := by positivity
  have key : st.U < 2 * (st.μ * ((st.a : ℝ) * st.b * st.c)) := by
    unfold μ
    rcases min_choice (st.rR / ((st.a : ℝ) * st.b))
        (min (st.rS / ((st.b : ℝ) * st.c)) (st.rT / ((st.c : ℝ) * st.a))) with e | e <;>
      rw [e]
    · have : st.rR / ((st.a : ℝ) * st.b) * ((st.a : ℝ) * st.b * st.c) = st.c * st.rR := by
        field_simp
      rw [this]; linarith
    · rcases min_choice (st.rS / ((st.b : ℝ) * st.c)) (st.rT / ((st.c : ℝ) * st.a)) with e' | e' <;>
        rw [e']
      · have : st.rS / ((st.b : ℝ) * st.c) * ((st.a : ℝ) * st.b * st.c) = st.a * st.rS := by
          field_simp
        rw [this]; linarith
      · have : st.rT / ((st.c : ℝ) * st.a) * ((st.a : ℝ) * st.b * st.c) = st.b * st.rT := by
          field_simp
        rw [this]; linarith
  have out4 : st.U < 4 * ((st.m : ℝ) * st.a * st.b * st.c) := by
    have := mul_lt_mul_of_pos_right m3 habc
    linarith
  exact ⟨a1, b1, c1, m1, ab, bc, ca, sizeR, sizeS, sizeT, out4⟩

end Stats

/-! ### Theorem B, lower bound -/

lemma sqrt_le_of_le_clip {P σ r : ℝ} (hσ : 0 ≤ σ) (h : P ≤ min (σ ^ 2) r) : √P ≤ σ := by
  calc √P ≤ √(σ ^ 2) := Real.sqrt_le_sqrt (h.trans (min_le_left _ _))
    _ = σ := Real.sqrt_sq hσ

/-- **Theorem B (lower bound).** For `r_i ≥ 1`, `σ_i ≥ 1` the explicit block instance
`B(a, b, c, m)` with `a = ⌊max(1, U/r_S)⌋`, `b = ⌊max(1, U/r_T)⌋`, `c = ⌊max(1, U/r_R)⌋`,
`m = ⌊min(r_R/ab, r_S/bc, r_T/ca)⌋` is admissible and has `U < 4 · Out`. -/
theorem theoremB_lower (st : Stats) (h : st.Regular) :
    1 ≤ st.a ∧ 1 ≤ st.b ∧ 1 ≤ st.c ∧ 1 ≤ st.m ∧
      Admissible st (blk st.m st.a st.b) (blk st.m st.b st.c) (blk st.m st.c st.a) ∧
      st.U < 4 * out (blk st.m st.a st.b) (blk st.m st.b st.c) (blk st.m st.c st.a) := by
  obtain ⟨a1, b1, c1, m1, ab, bc, ca, sR, sS, sT, o4⟩ := Stats.block_params h
  refine ⟨a1, b1, c1, m1, ⟨?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩
  · rw [card_blk]; exact sR
  · rw [card_blk]; exact sS
  · rw [card_blk]; exact sT
  · exact opNorm_blk_le.trans (sqrt_le_of_le_clip (by linarith [h.σR]) ab)
  · exact opNorm_blk_le.trans (sqrt_le_of_le_clip (by linarith [h.σS]) bc)
  · exact opNorm_blk_le.trans (sqrt_le_of_le_clip (by linarith [h.σT]) ca)
  · rw [out_blk]; exact o4

/-- **Theorem B.** In the regular regime, `U/4 < W ≤ U`: every admissible instance has
`Out ≤ U`, and some admissible instance (on finite types) has `Out > U/4`. -/
theorem theoremB (st : Stats) (h : st.Regular) :
    (∀ (X Y Z : Type) [Fintype X] [Fintype Y] [Fintype Z] [DecidableEq X] [DecidableEq Y]
        [DecidableEq Z] (R : Finset (X × Y)) (S : Finset (Y × Z)) (T : Finset (Z × X)),
        Admissible st R S T → out R S T ≤ st.U) ∧
      ∃ (X Y Z : Type) (_ : Fintype X) (_ : Fintype Y) (_ : Fintype Z) (_ : DecidableEq X)
        (_ : DecidableEq Y) (_ : DecidableEq Z) (R : Finset (X × Y)) (S : Finset (Y × Z))
        (T : Finset (Z × X)), Admissible st R S T ∧ st.U < 4 * out R S T := by
  refine ⟨fun X Y Z _ _ _ _ _ _ R S T hadm => theoremB_upper st R S T hadm, ?_⟩
  obtain ⟨-, -, -, -, hadm, hout⟩ := theoremB_lower st h
  exact ⟨Fin st.m × Fin st.a, Fin st.m × Fin st.b, Fin st.m × Fin st.c, inferInstance,
    inferInstance, inferInstance, inferInstance, inferInstance, inferInstance,
    blk st.m st.a st.b, blk st.m st.b st.c, blk st.m st.c st.a, hadm, hout⟩

end LeatherbackSpectral
