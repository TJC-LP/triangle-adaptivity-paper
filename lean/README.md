# Lean formalization: `LeatherbackSpectral`

A standalone Lake package with the paper's Lean 4 / mathlib formalization
(Appendix D of `paper/spectral_agm.typ`) and every module it imports.

| Library | Modules | Depends on |
|---|---|---|
| `Leatherback` (Std-only) | `Leatherback.Join.AdaptiveTriangle`, `Leatherback.Join.TriangleBag`, `Leatherback.Cost.TriangleCharge`, `Leatherback.Cost.TriangleChargeProofs` | Lean core / `Std` only |
| `LeatherbackSpectral` | `Basic`, `OpNorm`, `Upper`, `Kernel`, `Lower`, `Matrix01`, `Degenerate`, `KernelBridge`, `Sharp` | mathlib; `KernelBridge` also imports `Leatherback.Cost.TriangleChargeProofs` |
| `LeatherbackSpectralAudit` | `#print axioms` of 80 main declarations, each under `#guard_msgs` | `LeatherbackSpectral` |
| `LeatherbackAudit` | `#print axioms` of the 13 kernel-replica theorems, each pinned to its exact axiom set under `#guard_msgs` | `Leatherback` |

The four `Leatherback.*` modules are the reference semantics and a
line-by-line cost replica of the triangle kernel of the Leatherback engine
(`src/query/triangle_join.zig` in the engine repository). They are the import
closure of `LeatherbackSpectral` outside mathlib; the engine's other Lean
libraries are not needed and are not included.

## Pins

- `lean-toolchain`: `leanprover/lean4:v4.32.2`
- `lakefile.lean`: `require mathlib from git "https://github.com/leanprover-community/mathlib4" @ "v4.32.2"`
- `lake-manifest.json`: mathlib `905b95818eb32af7874a58b427f50c1711a5e96c`
  (tag `v4.32.2`) and its dependencies (plausible, LeanSearchClient,
  importGraph, proofwidgets, aesop, Qq, batteries, Cli) at fixed commits.
- Options: `autoImplicit false` and `warningAsError true` package-wide.

## Build

Install [`elan`](https://github.com/leanprover/elan); it reads
`lean-toolchain` and fetches Lean 4.32.2. Then, from this directory:

```sh
lake exe cache get    # mathlib's prebuilt .olean files (network, about 5 GB unpacked)
lake build            # every default target: both libraries and both audits
```

`lake build` exits 0 only if every proof kernel-checks and every
`#guard_msgs` matches. The audits make the build fail if any audited theorem
depends on an axiom beyond `propext`, `Classical.choice` and `Quot.sound`;
that catches `sorryAx`, `native_decide` (`Lean.ofReduceBool`) and custom
axioms. No source file uses `sorry`, `native_decide` or `axiom`.

To build only the spectral development and its audit:

```sh
lake build LeatherbackSpectral LeatherbackSpectralAudit
```

## Provenance

The `.lean` sources are copied from the Lean workspace of the Leatherback
engine repository at the commit that produced the paper. They are
byte-identical except for three doc comments, where an internal ticket
identifier for the triangle kernel was replaced by "the Leatherback triangle
kernel". `lakefile.lean` and `LeatherbackAudit.lean` are new for this
standalone package; `LeatherbackAudit.lean` restates, with `#print axioms`
and `#guard_msgs`, the axiom pins the engine workspace checks with its own
audit command.
