The main theorem survives the audit. I wrote the [complete verification report]( ./report.md) and a [paper-ready corrected statement](./paper_ready_statement.md).

| Claim | Verdict |
|---|---|
| T1, including Lambda, F, G, H | **Proved** |
| T2: arc formulas, 50 vertices, 38 necessary terms, factor 16 | **Proved** |
| T4: factor-8 obstruction | **Proved with corrected threshold** |
| T5 and Astra’s obstruction | **Proved** |
| Partial-norm clipping | **Proved** |
| Sharp constant | **Open-with-obstruction: [8,16]** |

Fresh exact checks covered **65,536** binary 2×2 quadruples, **2,120** random/adversarial instances, **119** rebuilt arc instances, and **11,296** rounding-grid vectors. No violations or undecided upper-bound comparisons remained. No supplied script was executed or imported.

The exact T4 correction is
\[
U_4=\min\{t^3,\sqrt{Lt^3}\}\qquad(L\ge t\ge1).
\]
Thus \(L\ge t^3\) is necessary and sufficient; **fixed \(L=8\)** works throughout \(1\le t<2\).

A new refutation concerns the rounding discussion: loss approaching **16 does not require \(n_{\rm full}\to2\)**—it can occur with \(n_{\rm full}=1\). Literal rounding of an arbitrary optimum therefore cannot establish factor 8.

The report includes every claim’s proof audit, exact outputs, certificates, reproduction commands, and the remaining notation/construction repairs.