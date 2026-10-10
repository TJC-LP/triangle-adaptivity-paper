import Leatherback.Cost.TriangleCharge

/-!
# The triangle replica's searches and walk meter

Proofs about the executable replica `Leatherback.Cost.TriangleCharge`:

* `lowerBoundBy_isLB`, `upperBoundBy_isUB`, `gallop_isLB`, `runEnd_isUB`: on a
  non-decreasing column every search answers the exact lower / upper bound, whatever its
  linear, exponential and bisection phases did, provided the start cursor is below the
  bound;
* `seekKey_span`: `seekKey` answers the run `[LB(key), UB(key))` and leaves the cursor at
  `LB(key)`;
* `run_model_eq`: on relations whose key columns are non-decreasing, a run that ends
  `done` has candidate budget `model = kernelWorkNat E1 E2 E3` — the Std mirror of
  `LeatherbackSpectral.kernelWork` (identified with it in
  `LeatherbackSpectral.KernelBridge`);
* `run_walked_le_model`: the entries actually walked never exceed the budget, and
  `walked_lt_model_example` shows the inequality can be strict (`model = 3`, `walked = 1`),
  so `kernelWorkNat` is an upper bound on actual reads, not their count.
-/

namespace Leatherback.Cost.TriangleCharge

open Leatherback.Join.TriangleBag

/-- A non-decreasing column. -/
def Mono (c : Array Nat) : Prop := ∀ i j, i ≤ j → j < c.size → rd c i ≤ rd c j

/-- `r` is the first index whose value is `≥ key`. -/
def IsLB (c : Array Nat) (key r : Nat) : Prop :=
  r ≤ c.size ∧ (∀ i, i < r → rd c i < key) ∧ (∀ i, r ≤ i → i < c.size → key ≤ rd c i)

/-- `r` is the first index whose value is `> key`. -/
def IsUB (c : Array Nat) (key r : Nat) : Prop :=
  r ≤ c.size ∧ (∀ i, i < r → rd c i ≤ key) ∧ (∀ i, r ≤ i → i < c.size → key < rd c i)

section Searches

variable {c : Array Nat} {key : Nat}

theorem lowerBoundBy_isLB (hm : Mono c) (lo hi w : Nat) (hlh : lo ≤ hi) (hhi : hi ≤ c.size)
    (hlo : ∀ i, i < lo → rd c i < key) (hup : ∀ i, hi ≤ i → i < c.size → key ≤ rd c i) :
    IsLB c key (lowerBoundBy c key lo hi w).1 := by
  fun_induction lowerBoundBy c key lo hi w with
  | case1 lo hi w hlt mid hmid ih =>
    apply ih (by omega) hhi _ hup
    intro i hi'
    exact Nat.lt_of_le_of_lt (hm i mid (by omega) (by omega)) hmid
  | case2 lo hi w hlt mid hmid ih =>
    apply ih (by omega) (by omega) hlo
    intro i hi' hic
    exact Nat.le_trans (Nat.le_of_not_lt hmid) (hm mid i hi' hic)
  | case3 lo hi w hlt =>
    have : lo = hi := by omega
    subst this
    exact ⟨hhi, hlo, hup⟩

theorem upperBoundBy_isUB (hm : Mono c) (lo hi w : Nat) (hlh : lo ≤ hi) (hhi : hi ≤ c.size)
    (hlo : ∀ i, i < lo → rd c i ≤ key) (hup : ∀ i, hi ≤ i → i < c.size → key < rd c i) :
    IsUB c key (upperBoundBy c key lo hi w).1 := by
  fun_induction upperBoundBy c key lo hi w with
  | case1 lo hi w hlt mid hmid ih =>
    apply ih (by omega) hhi _ hup
    intro i hi'
    exact Nat.le_trans (hm i mid (by omega) (by omega)) hmid
  | case2 lo hi w hlt mid hmid ih =>
    apply ih (by omega) (by omega) hlo
    intro i hi' hic
    exact Nat.lt_of_lt_of_le (Nat.lt_of_not_le hmid) (hm mid i hi' hic)
  | case3 lo hi w hlt =>
    have : lo = hi := by omega
    subst this
    exact ⟨hhi, hlo, hup⟩

theorem expLower_isLB (hm : Mono c) (known step w : Nat) (hk : known < c.size)
    (hkey : rd c known < key) :
    IsLB c key (expLower c key c.size known step w).1 := by
  fun_induction expLower c key c.size known step w with
  | case1 known step w hcond hge =>
    apply lowerBoundBy_isLB hm _ _ _ (by omega) (by omega)
    · intro i hi
      exact Nat.lt_of_le_of_lt (hm i known (by omega) hk) hkey
    · intro i hi hic
      exact Nat.le_trans hge (hm _ i hi hic)
  | case2 known step w hcond hlt ih =>
    exact ih (by omega) (Nat.lt_of_not_le hlt)
  | case3 known step w hcond =>
    apply lowerBoundBy_isLB hm _ _ _ (by omega) (Nat.le_refl _)
    · intro i hi
      exact Nat.lt_of_le_of_lt (hm i known (by omega) hk) hkey
    · intro i hi hic
      omega

theorem linearLower_spec (i stop w : Nat) (hstop : stop ≤ c.size) (his : i ≤ stop)
    (hlo : ∀ j, j < i → rd c j < key) :
    match (linearLower c key i stop w).1 with
    | .inl r => IsLB c key r ∨ ¬ Mono c
    | .inr e => (∀ j, j < e → rd c j < key) ∧ e = stop := by
  fun_induction linearLower c key i stop w with
  | case1 i w hlt hge =>
    by_cases hm : Mono c
    · left
      refine ⟨by omega, hlo, ?_⟩
      intro j hj hjc
      exact Nat.le_trans hge (hm i j hj hjc)
    · exact Or.inr hm
  | case2 i w hlt hge ih =>
    apply ih (by omega)
    intro j hj
    rcases Nat.lt_succ_iff_lt_or_eq.mp hj with h | h
    · exact hlo j h
    · subst h; exact Nat.lt_of_not_le hge
  | case3 i w hlt =>
    exact ⟨hlo, by omega⟩

/-- **Gallop correctness.** From any cursor below the bound, `gallopLowerBoundBy` answers the
lower bound of `key` on a non-decreasing column. -/
theorem gallop_isLB (hm : Mono c) (frm w : Nat) (hlo : ∀ j, j < frm → rd c j < key) :
    IsLB c key (gallop c frm key w).1 := by
  unfold gallop
  by_cases hsz : c.size ≤ frm
  · simp only [hsz, if_true]
    refine ⟨Nat.le_refl _, fun i hi => hlo i (by omega), fun i hi hic => by omega⟩
  · simp only [hsz, if_false]
    have hspec := linearLower_spec (c := c) (key := key) frm (min c.size (frm + linearSteps)) w
      (Nat.min_le_left _ _) (by simp [linearSteps]; omega) hlo
    split
    · rename_i r w' heq
      rw [heq] at hspec
      simpa [hm] using hspec
    · rename_i e w' heq
      rw [heq] at hspec
      obtain ⟨hall, heq'⟩ := hspec
      have he : e = min c.size (frm + linearSteps) := heq'
      by_cases hes : c.size ≤ e
      · simp only [hes, if_true]
        exact ⟨Nat.le_refl _, fun i hi => hall i (by omega), fun i hi hic => by omega⟩
      · simp only [hes, if_false]
        have hpos : 0 < e := by rw [he]; simp [linearSteps]; omega
        exact expLower_isLB hm (e - 1) 1 w' (by omega) (hall _ (by omega))

theorem expRunEnd_isUB (hm : Mono c) (known step w : Nat) (hk : known < c.size)
    (hkey : rd c known ≤ key) :
    IsUB c key (expRunEnd c key c.size known step w).1 := by
  fun_induction expRunEnd c key c.size known step w with
  | case1 known step w hcond hgt =>
    apply upperBoundBy_isUB hm _ _ _ (by omega) (by omega)
    · intro i hi
      exact Nat.le_trans (hm i known (by omega) hk) hkey
    · intro i hi hic
      exact Nat.lt_of_lt_of_le hgt (hm _ i hi hic)
  | case2 known step w hcond hle ih =>
    exact ih (by omega) (Nat.le_of_not_lt hle)
  | case3 known step w hcond =>
    apply upperBoundBy_isUB hm _ _ _ (by omega) (Nat.le_refl _)
    · intro i hi
      exact Nat.le_trans (hm i known (by omega) hk) hkey
    · intro i hi hic
      omega

theorem linearRunEnd_spec (hm : Mono c) (j stop w : Nat) (hstop : stop ≤ c.size) (hjs : j ≤ stop)
    (hlo : ∀ i, i < j → rd c i ≤ key) (hj : 0 < j) (hjc : j ≤ c.size)
    (hkey : rd c (j - 1) = key) :
    match (linearRunEnd c key j stop w).1 with
    | .inl r => IsUB c key r
    | .inr e => (∀ i, i < e → rd c i ≤ key) ∧ e = stop ∧ 0 < e ∧
        (e ≤ c.size → rd c (e - 1) = key) := by
  fun_induction linearRunEnd c key j stop w with
  | case1 j w hlt hne =>
    refine ⟨by omega, hlo, ?_⟩
    intro i hi hic
    have h1 : key ≤ rd c j := hkey ▸ hm (j - 1) j (by omega) (by omega)
    exact Nat.lt_of_lt_of_le (Nat.lt_of_le_of_ne h1 (Ne.symm hne)) (hm j i hi hic)
  | case2 j w hlt heq ih =>
    have heq' : rd c j = key := Classical.not_not.mp heq
    apply ih (by omega)
    · intro i hi
      rcases Nat.lt_succ_iff_lt_or_eq.mp hi with h | h
      · exact hlo i h
      · subst h; exact Nat.le_of_eq heq'
    · omega
    · omega
    · simpa using heq'
  | case3 j w hlt =>
    exact ⟨hlo, by omega, hj, fun _ => hkey⟩

/-- **Run end correctness.** On a non-decreasing column, `runEndBy` from a position `i`
answers the upper bound of the value at `i`. -/
theorem runEnd_isUB (hm : Mono c) (i w : Nat) (hi : i < c.size) :
    IsUB c (rd c i) (runEnd c i w).1 := by
  unfold runEnd
  have hsz : ¬ c.size ≤ i := by omega
  simp only [hsz, if_false]
  have hspec := linearRunEnd_spec (c := c) (key := rd c i) hm (i + 1)
    (min c.size (i + 1 + linearSteps)) w (Nat.min_le_left _ _) (by simp [linearSteps]; omega)
    (fun j hj => hm j i (by omega) hi) (by omega) (by omega) (by simp)
  split
  · rename_i r w' heq
    rw [heq] at hspec
    exact hspec
  · rename_i e w' heq
    rw [heq] at hspec
    obtain ⟨hall, heq', hpos, hlast⟩ := hspec
    have he : e = min c.size (i + 1 + linearSteps) := heq'
    by_cases hes : c.size ≤ e
    · simp only [hes, if_true]
      exact ⟨Nat.le_refl _, fun j hj => hall j (by omega), fun j hj hjc => by omega⟩
    · simp only [hes, if_false]
      exact expRunEnd_isUB hm (e - 1) 1 w' (by omega) (Nat.le_of_eq (hlast (by omega)))

theorem isLB_le_isUB {lo hi : Nat} (hl : IsLB c key lo) (hu : IsUB c key hi) : lo ≤ hi := by
  obtain ⟨hlc, hl1, hl2⟩ := hl
  obtain ⟨huc, hu1, hu2⟩ := hu
  rcases Nat.lt_or_ge hi lo with h | h
  · have := hl1 hi h
    have := hu2 hi (Nat.le_refl _) (by omega)
    omega
  · exact h

theorem isLB_mono {k k' a b : Nat} (hkk : k ≤ k') (ha : IsLB c k a) (hb : IsLB c k' b) :
    a ≤ b := by
  obtain ⟨hac, ha1, _⟩ := ha
  obtain ⟨_, _, hb2⟩ := hb
  rcases Nat.lt_or_ge b a with h | h
  · have h4 := hb2 b (Nat.le_refl _) (by omega)
    have h5 := ha1 b h
    omega
  · exact h

/-- **`seekKey`.** From a cursor below the bound, the returned span is
`[LB(key), UB(key))` (empty when the key is absent) and the cursor moves to `LB(key)`. -/
theorem seekKey_span (hm : Mono c) (cursor w : Nat) (hcur : ∀ j, j < cursor → rd c j < key) :
    IsLB c key (seekKey c cursor key w).1.1 ∧ IsUB c key (seekKey c cursor key w).1.2 ∧
      (seekKey c cursor key w).2.1 = (seekKey c cursor key w).1.1 := by
  have hlb := gallop_isLB hm cursor w hcur
  by_cases habs : c.size ≤ (gallop c cursor key w).1 ∨ rd c (gallop c cursor key w).1 ≠ key
  · simp only [seekKey, habs, if_true]
    refine ⟨hlb, ?_, trivial⟩
    obtain ⟨hc, h1, h2⟩ := hlb
    refine ⟨hc, fun i hi => Nat.le_of_lt (h1 i hi), ?_⟩
    intro i hi hic
    have hlt : (gallop c cursor key w).1 < c.size := by omega
    have hne : rd c (gallop c cursor key w).1 ≠ key := by
      rcases habs with h | h
      · omega
      · exact h
    have hge := h2 _ (Nat.le_refl _) hlt
    exact Nat.lt_of_lt_of_le (Nat.lt_of_le_of_ne hge (Ne.symm hne)) (hm _ i hi hic)
  · simp only [seekKey, habs, if_false]
    simp only [not_or, Classical.not_not, Nat.not_le] at habs
    refine ⟨hlb, ?_, trivial⟩
    have := runEnd_isUB hm (gallop c cursor key w).1 (gallop c cursor key w).2 habs.1
    rw [habs.2] at this
    exact this

end Searches

section Counting

theorem length_filter_prefix (p : Nat → Bool) :
    ∀ (L : List Nat) (r : Nat), r ≤ L.length → (∀ i (h : i < L.length), i < r → p L[i] = true) →
      (∀ i (h : i < L.length), r ≤ i → p L[i] = false) → (L.filter p).length = r
  | [], r, hr, _, _ => by simp at hr; simp [hr]
  | a :: t, 0, _, _, h2 => by
    have ha : p a = false := h2 0 (by simp) (Nat.le_refl _)
    have := length_filter_prefix p t 0 (Nat.zero_le _) (fun i _ hi => absurd hi (Nat.not_lt_zero _))
      (fun i h _ => h2 (i + 1) (by simp; omega) (Nat.zero_le _))
    simp [ha, this]
  | a :: t, r + 1, hr, h1, h2 => by
    have ha : p a = true := h1 0 (by simp) (Nat.zero_lt_succ _)
    have := length_filter_prefix p t r (by simp at hr; omega)
      (fun i h hi => h1 (i + 1) (by simp; omega) (by omega))
      (fun i h hi => h2 (i + 1) (by simp; omega) (by omega))
    simp [ha, this]

theorem length_filter_le_eq (L : List Nat) (k : Nat) :
    (L.filter (fun v => decide (v ≤ k))).length =
      (L.filter (fun v => decide (v < k))).length + (L.filter (fun v => decide (v = k))).length := by
  induction L with
  | nil => rfl
  | cons a t ih =>
    simp only [List.filter_cons]
    by_cases h1 : a < k
    · have h2 : a ≤ k := Nat.le_of_lt h1
      have h3 : a ≠ k := Nat.ne_of_lt h1
      simp [h1, h2, h3, ih]; omega
    · by_cases h3 : a = k
      · subst h3; simp [ih]; omega
      · have h2 : ¬ a ≤ k := by omega
        simp [h1, h2, h3, ih]

theorem rd_toArray (L : List Nat) (i : Nat) (h : i < L.length) : rd L.toArray i = L[i] := by
  simp [rd, Array.getD, h]

/-- The span between the bounds of `k` in a key column is the number of rows keyed `k`. -/
theorem span_eq_count (L : List Nat) (k lo hi : Nat) (hl : IsLB L.toArray k lo)
    (hu : IsUB L.toArray k hi) : hi - lo = (L.filter (fun v => decide (v = k))).length := by
  obtain ⟨hlc, hl1, hl2⟩ := hl
  obtain ⟨huc, hu1, hu2⟩ := hu
  simp only [List.size_toArray] at hlc huc hl2 hu2
  have hlo : (L.filter (fun v => decide (v < k))).length = lo := by
    apply length_filter_prefix _ L lo hlc
    · intro i h hi; have := hl1 i hi; rw [rd_toArray L i h] at this; simp [this]
    · intro i h hi; have := hl2 i hi h; rw [rd_toArray L i h] at this; simp; omega
  have hhi : (L.filter (fun v => decide (v ≤ k))).length = hi := by
    apply length_filter_prefix _ L hi huc
    · intro i h hi'; have := hu1 i hi'; rw [rd_toArray L i h] at this; simp [this]
    · intro i h hi'; have := hu2 i hi' h; rw [rd_toArray L i h] at this; simp; omega
  have := length_filter_le_eq L k
  omega

theorem nbr_length_eq (E : List (Nat × Nat)) (k : Nat) :
    (nbr E k).length = ((E.map Prod.fst).filter (fun v => decide (v = k))).length := by
  simp only [nbr, List.length_map, List.filter_map, Function.comp_def]

end Counting

section Run

variable {σ : Type} (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)

theorem rd_keys (E : List (Nat × Nat)) (r : Nat) (h : r < E.length) :
    rd (Rel.ofPairs E).keys r = E[r].1 := by
  simp [Rel.ofPairs, rd, Array.getD, h]

theorem rd_vals (E : List (Nat × Nat)) (r : Nat) (h : r < E.length) :
    rd (Rel.ofPairs E).vals r = E[r].2 := by
  simp [Rel.ofPairs, rd, Array.getD, h]

theorem keys_size (E : List (Nat × Nat)) : (Rel.ofPairs E).keys.size = E.length := by
  simp [Rel.ofPairs]

theorem valCol_size (E : List (Nat × Nat)) (lo hi : Nat) (h : hi ≤ E.length) :
    ((Rel.ofPairs E).valCol lo hi).size = hi - lo := by
  simp [Rel.valCol, Rel.ofPairs]
  omega

theorem span_nbr (E : List (Nat × Nat)) (k lo hi : Nat) (hl : IsLB (Rel.ofPairs E).keys k lo)
    (hu : IsUB (Rel.ofPairs E).keys k hi) : hi - lo = (nbr E k).length := by
  rw [nbr_length_eq]
  exact span_eq_count _ _ _ _ hl hu

theorem take_drop_cons {α : Type} (E : List α) (r j : Nat) (h : r < j) (hj : j ≤ E.length) :
    (E.drop r).take (j - r) = E[r] :: (E.drop (r + 1)).take (j - (r + 1)) := by
  rw [List.drop_eq_getElem_cons (by omega)]
  have : j - r = (j - (r + 1)) + 1 := by omega
  rw [this, List.take_succ_cons]

theorem groupLoop_model (E1 E2 E3 : List (Nat × Nat)) (hm2 : Mono (Rel.ofPairs E2).keys)
    (x i j : Nat) (n3 : Array Nat) (hn3 : n3.size = (nbr E3 x).length) (hj : j ≤ E1.length) :
    ∀ (n r prevY k2 : Nat) (acc : Acc σ), j - r = n → i ≤ r →
      (∀ idx, idx < k2 → i < r ∧ rd (Rel.ofPairs E2).keys idx < prevY) →
      (groupLoop visit (Rel.ofPairs E1) (Rel.ofPairs E2) x i j n3 r prevY k2 acc).1 = .done →
      (groupLoop visit (Rel.ofPairs E1) (Rel.ofPairs E2) x i j n3 r prevY k2 acc).2.model =
        acc.model + kernelWorkNat ((E1.drop r).take (j - r)) E2 E3 := by
  intro n
  induction n with
  | zero =>
    intro r prevY k2 acc hn _ _ _
    rw [groupLoop]
    have : ¬ r < j := by omega
    simp [this, hn]
  | succ n ih =>
    intro r prevY k2 acc hn hir hinv hdone
    have hrj : r < j := by omega
    rw [groupLoop] at hdone ⊢
    simp only [hrj, if_true] at hdone ⊢
    have hrE : r < E1.length := by omega
    have hx : E1[r].1 = x := by
      by_cases hk : rd (Rel.ofPairs E1).keys r = x
      · rw [← rd_keys E1 r hrE]; exact hk
      · simp [hk] at hdone
    have hk : ¬ rd (Rel.ofPairs E1).keys r ≠ x := by rw [rd_keys E1 r hrE, hx]; simp
    simp only [hk, if_false] at hdone ⊢
    have hy : ¬ (i < r ∧ rd (Rel.ofPairs E1).vals r < prevY) := by
      intro hy
      simp [hy] at hdone
    simp only [hy, if_false] at hdone ⊢
    have hyv : rd (Rel.ofPairs E1).vals r = E1[r].2 := rd_vals E1 r hrE
    have hcur : ∀ idx, idx < k2 → rd (Rel.ofPairs E2).keys idx < rd (Rel.ofPairs E1).vals r := by
      intro idx hidx
      obtain ⟨hir, hlt⟩ := hinv idx hidx
      have : prevY ≤ rd (Rel.ofPairs E1).vals r := by omega
      omega
    have hspec := seekKey_span hm2 k2 1 hcur
    have hspan := span_nbr E2 _ _ _ hspec.1 hspec.2.1
    have hhiE : (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.2 ≤ E2.length := by
      have := hspec.2.1.1; rwa [keys_size] at this
    have hsize := valCol_size E2
      (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.1 _ hhiE
    have hinv' : ∀ idx, idx < (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).2.1 →
        i < r + 1 ∧ rd (Rel.ofPairs E2).keys idx < rd (Rel.ofPairs E1).vals r := by
      intro idx hidx
      rw [hspec.2.2] at hidx
      exact ⟨by omega, hspec.1.2.1 idx hidx⟩
    rw [take_drop_cons E1 r j hrj hj, kernelWorkNat_cons, hx, ← hyv]
    by_cases hne : (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.1 =
        (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.2
    · simp only [hne, ne_eq, not_true_eq_false, if_false] at hdone ⊢
      rw [ih (r + 1) _ _ _ (by omega) (by omega) hinv' hdone]
      rw [← hspan, hne, Nat.sub_self, Nat.zero_min]
      simp
    · simp only [ne_eq, hne, not_false_eq_true, if_true] at hdone ⊢
      split
      · rename_i hW
        simp only [hW] at hdone
        rw [ih (r + 1) _ _ _ (by omega) (by omega) hinv' hdone]
        simp only [hsize, hn3, hspan]
        omega
      · rename_i hW
        simp [hW] at hdone
      · rename_i hW
        simp [hW] at hdone

theorem kernelWorkNat_eq_zero (l E2 E3 : List (Nat × Nat))
    (h : ∀ e ∈ l, (nbr E3 e.1).length = 0) : kernelWorkNat l E2 E3 = 0 := by
  induction l with
  | nil => rfl
  | cons e t ih =>
    rw [kernelWorkNat_cons, h e List.mem_cons_self,
      ih (fun e' he' => h e' (List.mem_cons_of_mem _ he'))]
    simp

theorem kernelWorkNat_drop_split (E1 E2 E3 : List (Nat × Nat)) (i j : Nat) (hij : i ≤ j) :
    kernelWorkNat (E1.drop i) E2 E3 =
      kernelWorkNat ((E1.drop i).take (j - i)) E2 E3 + kernelWorkNat (E1.drop j) E2 E3 := by
  conv => lhs; rw [← List.take_append_drop (j - i) (E1.drop i)]
  rw [kernelWorkNat_append, List.drop_drop]
  congr 3
  omega

theorem mem_group (E1 : List (Nat × Nat)) (i j : Nat) (e : Nat × Nat)
    (he : e ∈ (E1.drop i).take (j - i)) : ∃ r, ∃ h : r < E1.length, i ≤ r ∧ r < j ∧ E1[r] = e := by
  obtain ⟨t, ht, rfl⟩ := List.getElem_of_mem he
  simp only [List.length_take, List.length_drop] at ht
  refine ⟨i + t, by omega, by omega, by omega, ?_⟩
  simp [List.getElem_take, List.getElem_drop]

/-- The outer loop: from row `i`, a completed run adds `kernelWorkNat (E1.drop i)`. -/
theorem outer_model (E1 E2 E3 : List (Nat × Nat)) (hm1 : Mono (Rel.ofPairs E1).keys)
    (hm2 : Mono (Rel.ofPairs E2).keys) (hm3 : Mono (Rel.ofPairs E3).keys)
    (i k3 : Nat) (acc : Acc σ)
    (hinv : ∀ idx, idx < k3 → i < E1.length →
      rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys i)
    (hdone : (outer visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) i k3 acc).1 = .done) :
    (outer visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) i k3 acc).2.model =
      acc.model + kernelWorkNat (E1.drop i) E2 E3 := by
  rw [outer] at hdone ⊢
  by_cases hi : i < (Rel.ofPairs E1).keys.size
  · simp only [hi, if_true] at hdone ⊢
    have hiE : i < E1.length := by rwa [keys_size] at hi
    have hub := runEnd_isUB hm1 i 1 hi
    generalize hg : runEnd (Rel.ofPairs E1).keys i 1 = g at hub hdone ⊢
    by_cases hbad : g.1 ≤ i ∨ (g.1 < (Rel.ofPairs E1).keys.size ∧
        rd (Rel.ofPairs E1).keys g.1 < rd (Rel.ofPairs E1).keys i)
    · simp [hbad] at hdone
    rw [dif_neg hbad] at hdone ⊢
    have hlt : i < g.1 := by omega
    have hgE : g.1 ≤ E1.length := by have := hub.1; rwa [keys_size] at this
    -- every row of the group [i, g.1) is keyed x
    have hkeyed : ∀ e ∈ (E1.drop i).take (g.1 - i), e.1 = rd (Rel.ofPairs E1).keys i := by
      intro e he
      obtain ⟨r, hr, hir, hrj, rfl⟩ := mem_group E1 i g.1 e he
      rw [← rd_keys E1 r hr]
      have h1 := hub.2.1 r hrj
      have h2 := hm1 i r hir (by rw [keys_size]; exact hr)
      omega
    have hcur : ∀ idx, idx < k3 → rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys i :=
      fun idx h => hinv idx h hiE
    have hsk := seekKey_span hm3 k3 g.2 hcur
    have hspan := span_nbr E3 _ _ _ hsk.1 hsk.2.1
    generalize hs : seekKey (Rel.ofPairs E3).keys k3 (rd (Rel.ofPairs E1).keys i) g.2 = sk
      at hsk hspan hdone ⊢
    have hinv' : ∀ idx, idx < sk.2.1 → g.1 < E1.length →
        rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys g.1 := by
      intro idx hidx hgl
      rw [hsk.2.2] at hidx
      have h1 := hsk.1.2.1 idx hidx
      have h2 := hub.2.2 g.1 (Nat.le_refl _) (by rw [keys_size]; exact hgl)
      omega
    rw [kernelWorkNat_drop_split E1 E2 E3 i g.1 (Nat.le_of_lt hlt)]
    by_cases hempty : sk.1.1 = sk.1.2
    · simp only [hempty, if_true] at hdone ⊢
      rw [outer_model E1 E2 E3 hm1 hm2 hm3 g.1 sk.2.1 _ hinv' hdone]
      have hz : kernelWorkNat ((E1.drop i).take (g.1 - i)) E2 E3 = 0 := by
        apply kernelWorkNat_eq_zero
        intro e he
        rw [hkeyed e he, ← hspan, hempty, Nat.sub_self]
      simp only [hz]
      omega
    · simp only [hempty, if_false] at hdone ⊢
      have hn3 : ((Rel.ofPairs E3).valCol sk.1.1 sk.1.2).size =
          (nbr E3 (rd (Rel.ofPairs E1).keys i)).length := by
        rw [valCol_size E3 _ _ (by have := hsk.2.1.1; rwa [keys_size] at this), hspan]
      have hgroup := groupLoop_model visit E1 E2 E3 hm2 (rd (Rel.ofPairs E1).keys i) i g.1
        ((Rel.ofPairs E3).valCol sk.1.1 sk.1.2) hn3 hgE (g.1 - i) i 0 0
        { acc with charged := acc.charged + sk.2.2 } rfl (Nat.le_refl _)
        (fun idx h => absurd h (Nat.not_lt_zero _))
      split
      · rename_i acc' hG
        rw [hG] at hdone hgroup
        simp only at hdone
        rw [outer_model E1 E2 E3 hm1 hm2 hm3 g.1 sk.2.1 acc' hinv' hdone]
        have := hgroup rfl
        simp only at this
        rw [this]
        omega
      · rename_i acc' hG
        rw [hG] at hdone
        simp at hdone
      · rename_i acc' hG
        rw [hG] at hdone
        simp at hdone
  · simp only [hi, if_false]
    have : E1.length ≤ i := by rw [keys_size] at hi; omega
    simp [List.drop_eq_nil_of_le this]
termination_by E1.length - i

theorem mono_ofPairs (E : List (Nat × Nat)) (h : (E.map Prod.fst).Pairwise (· ≤ ·)) :
    Mono (Rel.ofPairs E).keys := by
  intro i j hij hj
  rw [keys_size] at hj
  rcases Nat.lt_or_eq_of_le hij with h' | h'
  · rw [rd_keys E i (by omega), rd_keys E j hj]
    have := List.pairwise_iff_getElem.mp h i j (by simp; omega) (by simp; omega) h'
    simpa using this
  · subst h'
    exact Nat.le_refl _

/-- **The walk meter is `kernelWork`.** On relations whose key columns are non-decreasing,
a run of the replica that completes (`done`) has accumulated exactly
`model = Σ_{(x,y) ∈ E1} min(|N2(y)|, |N3(x)|) = kernelWorkNat E1 E2 E3`, whatever the sink. -/
theorem run_model_eq (E1 E2 E3 : List (Nat × Nat)) (h1 : (E1.map Prod.fst).Pairwise (· ≤ ·))
    (h2 : (E2.map Prod.fst).Pairwise (· ≤ ·)) (h3 : (E3.map Prod.fst).Pairwise (· ≤ ·)) (sink : σ)
    (hdone : (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).1 = .done) :
    (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model =
      kernelWorkNat E1 E2 E3 := by
  have := outer_model visit E1 E2 E3 (mono_ofPairs E1 h1) (mono_ofPairs E2 h2) (mono_ofPairs E3 h3)
    0 0 ⟨sink, 0, 0, 0⟩ (fun idx h => absurd h (Nat.not_lt_zero _)) hdone
  simpa [run] using this

/-- ... equivalently the adaptive reference kernel's exact probe count. -/
theorem run_model_eq_probes (E1 E2 E3 : List (Nat × Nat)) (h1 : (E1.map Prod.fst).Pairwise (· ≤ ·))
    (h2 : (E2.map Prod.fst).Pairwise (· ≤ ·)) (h3 : (E3.map Prod.fst).Pairwise (· ≤ ·)) (sink : σ)
    (hdone : (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).1 = .done) :
    (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model =
      (Leatherback.Join.triangle E1 (nbr E2) (nbr E3)).probes := by
  rw [run_model_eq visit E1 E2 E3 h1 h2 h3 sink hdone, kernelWorkNat_eq_probes]

/-- On sets, the bag a completed run's sink can see never exceeds the walk meter. -/
theorem bagCount_le_run_model (E1 E2 E3 : List (Nat × Nat))
    (h1 : (E1.map Prod.fst).Pairwise (· ≤ ·)) (h2 : (E2.map Prod.fst).Pairwise (· ≤ ·))
    (h3 : (E3.map Prod.fst).Pairwise (· ≤ ·)) (n2 : E2.Nodup) (n3 : E3.Nodup) (sink : σ)
    (hdone : (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).1 = .done) :
    bagCount E1 E2 E3 ≤
      (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model := by
  rw [run_model_eq visit E1 E2 E3 h1 h2 h3 sink hdone]
  exact bagCount_le_kernelWorkNat E1 E2 E3 n2 n3

section Completion

theorem equalRunEnd_spec (c : Array Nat) (v e : Nat) :
    (∀ k, e ≤ k → k < equalRunEnd c v e → k < c.size ∧ rd c k = v) ∧
      (equalRunEnd c v e < c.size → rd c (equalRunEnd c v e) ≠ v) := by
  induction e using equalRunEnd.induct (c := c) (v := v) with
  | case1 e h ih =>
    rw [equalRunEnd, if_pos h]
    refine ⟨?_, ih.2⟩
    intro k hk hlt
    rcases Nat.lt_or_eq_of_le hk with hk | rfl
    · exact ih.1 k hk hlt
    · exact h
  | case2 e h =>
    rw [equalRunEnd, if_neg h]
    refine ⟨fun k hk hlt => absurd hlt (by omega), ?_⟩
    intro hlt heq
    exact h ⟨hlt, heq⟩

/-- **No false decline in a walk.** On non-decreasing columns, with a visitor that never
stops, `intersectWalk` ends `done` from any cursor state below the walked value. -/
theorem walkLoop_done {τ : Type} (visit : Nat → Nat → τ → Bool × τ)
    (htot : ∀ v m st, (visit v m st).1 = true) (s l : Array Nat) (hs : Mono s) (hl : Mono l)
    (i lo : Nat) (acc : Walk τ) (hinv : i < s.size → ∀ idx, idx < lo → rd l idx < rd s i) :
    (walkLoop visit s l i lo acc).1 = .done := by
  rw [walkLoop]
  by_cases hi : i < s.size
  · rw [dif_pos hi]
    simp only []
    have hinv := hinv hi
    have hge := equalRunEnd_ge s (rd s i) (i + 1)
    have hrun := equalRunEnd_spec s (rd s i) (i + 1)
    generalize hie : equalRunEnd s (rd s i) (i + 1) = ie at hge hrun ⊢
    -- the walked side's next distinct value is strictly larger
    have hnext : ie < s.size → rd s i < rd s ie := by
      intro h
      have := hs i ie (by omega) h
      have := hrun.2 h
      omega
    have hds : dropsAt s ie (rd s i) = false := by
      unfold dropsAt
      by_cases h : ie < s.size
      · have := hnext h; simp; omega
      · simp [h]
    simp only [hds, Bool.false_eq_true, if_false]
    have hg := gallop_isLB hl lo (acc.work + (ie - i)) hinv
    generalize hgal : gallop l lo (rd s i) (acc.work + (ie - i)) = g at hg ⊢
    by_cases hend : l.size ≤ g.1
    · simp [hend]
    simp only [hend, if_false]
    have hgv : rd s i ≤ rd l g.1 := hg.2.2 g.1 (Nat.le_refl _) (by omega)
    have hdl : dropsAt l g.1 (rd s i) = false := by unfold dropsAt; simp; omega
    simp only [hdl, Bool.false_eq_true, if_false]
    by_cases hmatch : rd l g.1 = rd s i
    · simp only [hmatch, if_true]
      have hrl := equalRunEnd_spec l (rd s i) (g.1 + 1)
      have hgel := equalRunEnd_ge l (rd s i) (g.1 + 1)
      generalize hhe : equalRunEnd l (rd s i) (g.1 + 1) = he at hrl hgel ⊢
      have hdh : dropsAt l he (rd s i) = false := by
        unfold dropsAt
        by_cases h : he < l.size
        · have := hl g.1 he (by omega) h; simp; omega
        · simp [h]
      simp only [hdh, Bool.false_eq_true, if_false, htot, if_true]
      apply walkLoop_done visit htot s l hs hl
      intro hie' idx hidx
      have hv := hnext hie'
      by_cases hlt : idx < g.1
      · have := hg.2.1 idx hlt; omega
      · rcases Nat.lt_or_eq_of_le (Nat.le_of_not_lt hlt) with h | h
        · have := (hrl.1 idx (by omega) hidx).2; omega
        · subst h; omega
    · simp only [hmatch, if_false]
      apply walkLoop_done visit htot s l hs hl
      intro hie' idx hidx
      have := hg.2.1 idx hidx
      have := hnext hie'
      omega
  · rw [dif_neg hi]
termination_by s.size - i
decreasing_by all_goals omega

theorem intersectEach_done {τ : Type} (visit : Nat → Nat → τ → Bool × τ)
    (htot : ∀ v m st, (visit v m st).1 = true) (a b : Array Nat) (ha : Mono a) (hb : Mono b)
    (acc : Walk τ) : (intersectEach visit a b acc).1 = .done := by
  unfold intersectEach
  split
  · exact walkLoop_done visit htot a b ha hb 0 0 acc (fun _ idx h => absurd h (Nat.not_lt_zero _))
  · exact walkLoop_done visit htot b a hb ha 0 0 acc (fun _ idx h => absurd h (Nat.not_lt_zero _))

/-- Rows sorted by `(key, value)`, the order `presorted` bridge fixtures, certified `.lb`
ranges and graph permutations present. -/
def LexSorted (E : List (Nat × Nat)) : Prop :=
  E.Pairwise (fun a b => a.1 < b.1 ∨ (a.1 = b.1 ∧ a.2 ≤ b.2))

theorem LexSorted.keys {E : List (Nat × Nat)} (h : LexSorted E) :
    (E.map Prod.fst).Pairwise (· ≤ ·) :=
  List.pairwise_map.mpr (h.imp (fun h => by rcases h with h | ⟨h, _⟩ <;> omega))

theorem LexSorted.vals {E : List (Nat × Nat)} (h : LexSorted E) (a b : Nat) (hab : a ≤ b)
    (hb : b < E.length) (heq : E[a].1 = E[b].1) : E[a].2 ≤ E[b].2 := by
  rcases Nat.lt_or_eq_of_le hab with hab | rfl
  · have := List.pairwise_iff_getElem.mp h a b (by omega) hb hab
    omega
  · exact Nat.le_refl _

theorem rd_valCol (E : List (Nat × Nat)) (lo hi a : Nat) (hhi : hi ≤ E.length) (ha : a < hi - lo) :
    rd ((Rel.ofPairs E).valCol lo hi) a = E[lo + a].2 := by
  have h1 : a < ((Rel.ofPairs E).valCol lo hi).size := by rw [valCol_size E lo hi hhi]; exact ha
  simp only [rd, Array.getD, h1, dif_pos]
  simp [Rel.valCol, Rel.ofPairs]

theorem mono_valCol (E : List (Nat × Nat)) (h : LexSorted E) (k lo hi : Nat)
    (hl : IsLB (Rel.ofPairs E).keys k lo) (hu : IsUB (Rel.ofPairs E).keys k hi) :
    Mono ((Rel.ofPairs E).valCol lo hi) := by
  have hhi : hi ≤ E.length := by have := hu.1; rwa [keys_size] at this
  intro a b hab hb
  rw [valCol_size E lo hi hhi] at hb
  rw [rd_valCol E lo hi a hhi (by omega), rd_valCol E lo hi b hhi hb]
  apply h.vals _ _ (by omega) (by omega)
  have ka := hl.2.2 (lo + a) (by omega) (by rw [keys_size]; omega)
  have ka' := hu.2.1 (lo + a) (by omega)
  have kb := hl.2.2 (lo + b) (by omega) (by rw [keys_size]; omega)
  have kb' := hu.2.1 (lo + b) (by omega)
  rw [rd_keys E _ (by omega)] at ka ka' kb kb'
  omega

theorem groupLoop_done (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)
    (htot : ∀ x y z m st, (visit x y z m st).1 = true) (E1 E2 : List (Nat × Nat))
    (hs1 : LexSorted E1) (hs2 : LexSorted E2) (x i j : Nat) (n3 : Array Nat) (hn3 : Mono n3)
    (hj : j ≤ E1.length) (hkeys : ∀ r, i ≤ r → r < j → rd (Rel.ofPairs E1).keys r = x) :
    ∀ (n r prevY k2 : Nat) (acc : Acc σ), j - r = n → i ≤ r →
      (i < r → prevY = rd (Rel.ofPairs E1).vals (r - 1)) →
      (∀ idx, idx < k2 → i < r ∧ rd (Rel.ofPairs E2).keys idx < prevY) →
      (groupLoop visit (Rel.ofPairs E1) (Rel.ofPairs E2) x i j n3 r prevY k2 acc).1 = .done := by
  intro n
  induction n with
  | zero =>
    intro r prevY k2 acc hn _ _ _
    rw [groupLoop]
    have : ¬ r < j := by omega
    simp [this]
  | succ n ih =>
    intro r prevY k2 acc hn hir hprev hinv
    have hrj : r < j := by omega
    have hrE : r < E1.length := by omega
    rw [groupLoop]
    simp only [hrj, if_true]
    have hk : ¬ rd (Rel.ofPairs E1).keys r ≠ x := by simp [hkeys r hir hrj]
    simp only [hk, if_false]
    have hy : ¬ (i < r ∧ rd (Rel.ofPairs E1).vals r < prevY) := by
      rintro ⟨hlt, hlt'⟩
      rw [hprev hlt, rd_vals E1 (r - 1) (by omega), rd_vals E1 r hrE] at hlt'
      have := hs1.vals (r - 1) r (by omega) hrE (by
        have a := hkeys (r - 1) (by omega) (by omega)
        have b := hkeys r hir hrj
        rw [rd_keys E1 _ (by omega)] at a
        rw [rd_keys E1 _ hrE] at b
        rw [a, b])
      omega
    simp only [hy, if_false]
    have hcur : ∀ idx, idx < k2 → rd (Rel.ofPairs E2).keys idx < rd (Rel.ofPairs E1).vals r := by
      intro idx hidx
      obtain ⟨hir', hlt⟩ := hinv idx hidx
      by_cases hc : i < r ∧ rd (Rel.ofPairs E1).vals r < prevY
      · exact absurd hc hy
      · omega
    have hspec := seekKey_span (mono_ofPairs E2 hs2.keys) k2 1 hcur
    have hinv' : ∀ idx, idx < (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).2.1 →
        i < r + 1 ∧ rd (Rel.ofPairs E2).keys idx < rd (Rel.ofPairs E1).vals r := by
      intro idx hidx
      rw [hspec.2.2] at hidx
      exact ⟨by omega, hspec.1.2.1 idx hidx⟩
    have hprev' : i < r + 1 → rd (Rel.ofPairs E1).vals r = rd (Rel.ofPairs E1).vals (r + 1 - 1) :=
      fun _ => by simp
    by_cases hne : (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.1 =
        (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).1.2
    · simp only [hne, ne_eq, not_true_eq_false, if_false]
      exact ih (r + 1) _ _ _ (by omega) (by omega) hprev' hinv'
    · simp only [ne_eq, hne, not_false_eq_true, if_true]
      have hW := intersectEach_done (fun z m st => visit x (rd (Rel.ofPairs E1).vals r) z m st)
        (fun v m st => htot _ _ _ _ _) _ n3
        (mono_valCol E2 hs2 _ _ _ hspec.1 hspec.2.1) hn3
        ⟨acc.sink, (seekKey (Rel.ofPairs E2).keys k2 (rd (Rel.ofPairs E1).vals r) 1).2.2, acc.walked⟩
      split
      · exact ih (r + 1) _ _ _ (by omega) (by omega) hprev' hinv'
      · rename_i hW'
        rw [hW] at hW'
        cases hW'
      · rename_i hW'
        rw [hW] at hW'
        cases hW'

theorem outer_done (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)
    (htot : ∀ x y z m st, (visit x y z m st).1 = true) (E1 E2 E3 : List (Nat × Nat))
    (hs1 : LexSorted E1) (hs2 : LexSorted E2) (hs3 : LexSorted E3)
    (i k3 : Nat) (acc : Acc σ)
    (hinv : ∀ idx, idx < k3 → i < E1.length →
      rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys i) :
    (outer visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) i k3 acc).1 = .done := by
  have hm1 := mono_ofPairs E1 hs1.keys
  have hm3 := mono_ofPairs E3 hs3.keys
  rw [outer]
  by_cases hi : i < (Rel.ofPairs E1).keys.size
  · simp only [hi, if_true]
    have hiE : i < E1.length := by rwa [keys_size] at hi
    have hub := runEnd_isUB hm1 i 1 hi
    generalize hg : runEnd (Rel.ofPairs E1).keys i 1 = g at hub ⊢
    have hbad : ¬ (g.1 ≤ i ∨ (g.1 < (Rel.ofPairs E1).keys.size ∧
        rd (Rel.ofPairs E1).keys g.1 < rd (Rel.ofPairs E1).keys i)) := by
      rintro (h | ⟨h1, h2⟩)
      · have := hub.2.2 i h hi
        omega
      · have := hub.2.2 g.1 (Nat.le_refl _) h1
        omega
    rw [dif_neg hbad]
    have hlt : i < g.1 := by omega
    have hgE : g.1 ≤ E1.length := by have := hub.1; rwa [keys_size] at this
    have hcur : ∀ idx, idx < k3 → rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys i :=
      fun idx h => hinv idx h hiE
    have hsk := seekKey_span hm3 k3 g.2 hcur
    generalize hs : seekKey (Rel.ofPairs E3).keys k3 (rd (Rel.ofPairs E1).keys i) g.2 = sk at hsk ⊢
    have hinv' : ∀ idx, idx < sk.2.1 → g.1 < E1.length →
        rd (Rel.ofPairs E3).keys idx < rd (Rel.ofPairs E1).keys g.1 := by
      intro idx hidx hgl
      rw [hsk.2.2] at hidx
      have h1 := hsk.1.2.1 idx hidx
      have h2 := hub.2.2 g.1 (Nat.le_refl _) (by rw [keys_size]; exact hgl)
      omega
    by_cases hempty : sk.1.1 = sk.1.2
    · simp only [hempty, if_true]
      exact outer_done visit htot E1 E2 E3 hs1 hs2 hs3 g.1 sk.2.1 _ hinv'
    · simp only [hempty, if_false]
      have hkeys : ∀ r, i ≤ r → r < g.1 → rd (Rel.ofPairs E1).keys r = rd (Rel.ofPairs E1).keys i := by
        intro r hir hrj
        have h1 := hub.2.1 r hrj
        have h2 := hm1 i r hir (by rw [keys_size]; omega)
        omega
      have hG := groupLoop_done visit htot E1 E2 hs1 hs2 (rd (Rel.ofPairs E1).keys i) i g.1
        ((Rel.ofPairs E3).valCol sk.1.1 sk.1.2) (mono_valCol E3 hs3 _ _ _ hsk.1 hsk.2.1) hgE hkeys
        (g.1 - i) i 0 0 { acc with charged := acc.charged + sk.2.2 } rfl (Nat.le_refl _)
        (fun h => absurd h (Nat.lt_irrefl _)) (fun idx h => absurd h (Nat.not_lt_zero _))
      split
      · exact outer_done visit htot E1 E2 E3 hs1 hs2 hs3 g.1 sk.2.1 _ hinv'
      · rename_i acc' hG'
        rw [hG'] at hG
        cases hG
      · rename_i acc' hG'
        rw [hG'] at hG
        cases hG
  · simp only [hi, if_false]
termination_by E1.length - i

/-- **No false decline.** On `(key, value)`-sorted relations, with a sink that never stops,
the replica completes. -/
theorem run_done (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)
    (htot : ∀ x y z m st, (visit x y z m st).1 = true) (E1 E2 E3 : List (Nat × Nat))
    (hs1 : LexSorted E1) (hs2 : LexSorted E2) (hs3 : LexSorted E3) (sink : σ) :
    (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).1 = .done :=
  outer_done visit htot E1 E2 E3 hs1 hs2 hs3 0 0 _ (fun _ h => absurd h (Nat.not_lt_zero _))

/-- **The candidate budget is `kernelWork`, unconditionally on sorted input.** For
`(key,value)`-sorted relations and a total sink, the replica's `model` budget (the ideal
precharged candidate count, an upper bound on `walked`) is `kernelWorkNat E1 E2 E3`. -/
theorem run_model_eq_sorted (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)
    (htot : ∀ x y z m st, (visit x y z m st).1 = true) (E1 E2 E3 : List (Nat × Nat))
    (hs1 : LexSorted E1) (hs2 : LexSorted E2) (hs3 : LexSorted E3) (sink : σ) :
    (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.model =
      kernelWorkNat E1 E2 E3 :=
  run_model_eq visit E1 E2 E3 hs1.keys hs2.keys hs3.keys sink
    (run_done visit htot E1 E2 E3 hs1 hs2 hs3 sink)

end Completion

section Walked

theorem equalRunEnd_le (c : Array Nat) (v e : Nat) (h : e ≤ c.size) : equalRunEnd c v e ≤ c.size := by
  induction e using equalRunEnd.induct (c := c) (v := v) with
  | case1 e hc ih => rw [equalRunEnd, if_pos hc]; exact ih (by omega)
  | case2 e hc => rw [equalRunEnd, if_neg hc]; exact h

/-- A walk consumes at most the rest of its walked column. -/
theorem walkLoop_walked_le {τ : Type} (visit : Nat → Nat → τ → Bool × τ) (s l : Array Nat)
    (i lo : Nat) (acc : Walk τ) :
    (walkLoop visit s l i lo acc).2.walked ≤ acc.walked + (s.size - i) := by
  rw [walkLoop]
  by_cases hi : i < s.size
  · rw [dif_pos hi]
    simp only []
    have hle := equalRunEnd_le s (rd s i) (i + 1) (by omega)
    have hge := equalRunEnd_ge s (rd s i) (i + 1)
    generalize equalRunEnd s (rd s i) (i + 1) = ie at hle hge ⊢
    split
    · simp only; omega
    split
    · simp only; omega
    split
    · simp only; omega
    split
    · split
      · simp only; omega
      split
      · refine Nat.le_trans (walkLoop_walked_le visit s l ie _ _) ?_
        simp only
        omega
      · simp only; omega
    · refine Nat.le_trans (walkLoop_walked_le visit s l ie _ _) ?_
      simp only
      omega
  · rw [dif_neg hi]
    simp
termination_by s.size - i
decreasing_by all_goals omega

theorem intersectEach_walked_le {τ : Type} (visit : Nat → Nat → τ → Bool × τ) (a b : Array Nat)
    (acc : Walk τ) :
    (intersectEach visit a b acc).2.walked ≤ acc.walked + min a.size b.size := by
  unfold intersectEach
  split
  · have := walkLoop_walked_le visit a b 0 0 acc
    omega
  · have := walkLoop_walked_le visit b a 0 0 acc
    omega

theorem shift_le {a b m w m' w' : Nat} (h : a + m' ≤ b + w') (h' : w' + m ≤ m' + w) :
    a + m ≤ b + w := by omega

theorem groupLoop_walked_le (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 : Rel)
    (x i j : Nat) (n3 : Array Nat) :
    ∀ (n r prevY k2 : Nat) (acc : Acc σ), j - r = n →
      (groupLoop visit r1 r2 x i j n3 r prevY k2 acc).2.walked + acc.model ≤
        (groupLoop visit r1 r2 x i j n3 r prevY k2 acc).2.model + acc.walked := by
  intro n
  induction n with
  | zero =>
    intro r prevY k2 acc hn
    rw [groupLoop]
    have : ¬ r < j := by omega
    simp only [this, if_false]
    omega
  | succ n ih =>
    intro r prevY k2 acc hn
    rw [groupLoop]
    have hrj : r < j := by omega
    simp only [hrj, if_true]
    split
    · simp only; omega
    split
    · simp only; omega
    split
    · have hw := intersectEach_walked_le
        (fun z m st => visit x (rd r1.vals r) z m st)
        (r2.valCol (seekKey r2.keys k2 (rd r1.vals r) 1).1.1 (seekKey r2.keys k2 (rd r1.vals r) 1).1.2)
        n3 ⟨acc.sink, (seekKey r2.keys k2 (rd r1.vals r) 1).2.2, acc.walked⟩
      simp only at hw
      split
      · refine shift_le (ih (r + 1) _ _ _ (by omega)) ?_
        simp only
        omega
      · simp only; omega
      · simp only; omega
    · refine shift_le (ih (r + 1) _ _ _ (by omega)) ?_
      simp only
      omega

theorem outer_walked_le (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 r3 : Rel)
    (i k3 : Nat) (acc : Acc σ) :
    (outer visit r1 r2 r3 i k3 acc).2.walked + acc.model ≤
      (outer visit r1 r2 r3 i k3 acc).2.model + acc.walked := by
  rw [outer]
  by_cases hi : i < r1.keys.size
  · simp only [hi, if_true]
    split
    · simp only; omega
    · rename_i hbad
      have hlt : i < (runEnd r1.keys i 1).1 := by omega
      split
      · refine shift_le (outer_walked_le visit r1 r2 r3 (runEnd r1.keys i 1).1 _ _) ?_
        simp only
        omega
      · have hg := groupLoop_walked_le visit r1 r2 (rd r1.keys i) i (runEnd r1.keys i 1).1
          (r3.valCol (seekKey r3.keys k3 (rd r1.keys i) (runEnd r1.keys i 1).2).1.1
            (seekKey r3.keys k3 (rd r1.keys i) (runEnd r1.keys i 1).2).1.2) _ i 0 0
          { acc with charged := acc.charged +
              (seekKey r3.keys k3 (rd r1.keys i) (runEnd r1.keys i 1).2).2.2 } rfl
        split
        · rename_i acc' hG
          rw [hG] at hg
          refine shift_le (outer_walked_le visit r1 r2 r3 (runEnd r1.keys i 1).1 _ acc') ?_
          simp only at hg
          omega
        · rename_i acc' hG
          rw [hG] at hg
          simp only at hg ⊢
          omega
        · rename_i acc' hG
          rw [hG] at hg
          simp only at hg ⊢
          omega
  · simp only [hi, if_false]
    omega
termination_by r1.keys.size - i

/-- **`W ≤ M`.** On every input, sorted or not and whatever the sink does, the entries a run
walks never exceed its walk meter `model`. -/
theorem run_walked_le_model (visit : Nat → Nat → Nat → Nat → σ → Bool × σ) (r1 r2 r3 : Rel)
    (sink : σ) : (run visit r1 r2 r3 sink).2.walked ≤ (run visit r1 r2 r3 sink).2.model := by
  have := outer_walked_le visit r1 r2 r3 0 0 ⟨sink, 0, 0, 0⟩
  simp only [run] at this ⊢
  omega

/-- On sorted input, `W ≤ kernelWorkNat`. -/
theorem run_walked_le_kernelWork (visit : Nat → Nat → Nat → Nat → σ → Bool × σ)
    (htot : ∀ x y z m st, (visit x y z m st).1 = true) (E1 E2 E3 : List (Nat × Nat))
    (hs1 : LexSorted E1) (hs2 : LexSorted E2) (hs3 : LexSorted E3) (sink : σ) :
    (run visit (Rel.ofPairs E1) (Rel.ofPairs E2) (Rel.ofPairs E3) sink).2.walked ≤
      kernelWorkNat E1 E2 E3 := by
  rw [← run_model_eq_sorted visit htot E1 E2 E3 hs1 hs2 hs3 sink]
  exact run_walked_le_model visit _ _ _ sink

end Walked

/-- **`walked < model` can happen.** `E1 = [(0,0)]`, `N2(0) = [100,101,102]`,
`N3(0) = [1,2,3]`: sorted and duplicate-free. The budget precharges `min(3, 3) = 3`, but the
tie rule walks `N2(0)`, reads `100`, gallops `N3(0)` to its end and stops: `walked = 1`.
So `model = kernelWorkNat` is a conservative candidate budget, not the number of neighbour
reads. (Checked by kernel reduction; no `native_decide`.) -/
theorem walked_lt_model_example :
    let r := run countVisit (Rel.ofPairs [(0, 0)]) (Rel.ofPairs [(0, 100), (0, 101), (0, 102)])
      (Rel.ofPairs [(0, 1), (0, 2), (0, 3)]) 0
    r.1 = .done ∧ r.2.model = 3 ∧ r.2.walked = 1 ∧
      kernelWorkNat [(0, 0)] [(0, 100), (0, 101), (0, 102)] [(0, 1), (0, 2), (0, 3)] = 3 := by
  decide +kernel

end Run

end Leatherback.Cost.TriangleCharge
