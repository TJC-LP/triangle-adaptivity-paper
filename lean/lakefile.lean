import Lake
open Lake DSL

package leatherbackSpectral where
  leanOptions := #[⟨`autoImplicit, false⟩, ⟨`warningAsError, true⟩]

require mathlib from git "https://github.com/leanprover-community/mathlib4" @ "v4.32.2"

-- Std-only reference semantics and cost replica of Leatherback's triangle kernel.
-- `LeatherbackSpectral.KernelBridge` imports `Leatherback.Cost.TriangleChargeProofs`.
@[default_target]
lean_lib Leatherback where
  roots := #[`Leatherback.Join.AdaptiveTriangle, `Leatherback.Join.TriangleBag,
    `Leatherback.Cost.TriangleCharge, `Leatherback.Cost.TriangleChargeProofs]

@[default_target]
lean_lib LeatherbackSpectral where
  leanOptions := #[⟨`maxSynthPendingDepth, .ofNat 3⟩, ⟨`linter.unusedSectionVars, .ofBool false⟩]

@[default_target]
lean_lib LeatherbackSpectralAudit where

@[default_target]
lean_lib LeatherbackAudit where
