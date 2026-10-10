"""Exponent profile f(kappa) of the per-binding cost C (Section "Per-binding choice"); the code calls the slope beta, the paper and figure kappa.

Usage: python3 -I make_fbeta_figure.py [out.svg]   (default: fbeta.svg next to this script)

Standard library only. Every plotted exponent is an exact Fraction derived from
the closed forms in the paper; the asserts tie the points to the curves.

Instances with B2 = N^beta. Exponents are "C = N^e":
  upper(beta)  = min(3/2, max(1, min((10 beta - 1)/8, 3/8 + 3 beta/4)))
                 from C <= N + 3^{1/8} N^{-1/8} B2^{5/4}   (thm-pb-upper2)
                 and  C <= N + (N/3)^{3/8} B2^{3/4}        (thm-pb-upper)
                 and  C <= N + sqrt(|R||S||T|) <= N + (N/3)^{3/2}  (lem-sum).
                 The two l2 bounds cross at beta = 1; the second-moment bound
                 is the smaller one exactly when B2 < N/3, so it governs beta < 1.
  target(beta) = max(1, beta), the exponent of N + B2.
  The worst-case exponent equals upper(beta) for every real beta in [9/10, 3/2]:
  D_{p,q} (thm-pb-asym) for 9/10 <= beta < 1 (rational p/q, and every real
  beta by p = floor(beta q)); F_{i,j} (thm-pb-slopes, cor-real-slopes) for every
  real beta in [1, 3/2); K_{s,s,s} at 3/2. For beta < 9/10 only the upper bound
  C <= (1 + 3^{1/8}) N is plotted (gap 0 against N + B2).
  F_{i,j}(u), i >= j >= 1: C >= u^{12i-3j}, N = Theta(u^{8i}),
                 B2 = Theta(u^{12i-4j}), so beta = 3/2 - j/(2i), e = 3/2 - 3j/(8i).
  D_{p,q}(u), 9/10 <= p/q <= 1: N = Theta(u^{8q}), B2 = 4u^{8p}, C = Theta(u^{10p-q}),
                 so beta = p/q, e = (10p - q)/(8q) = (10 beta - 1)/8.
  G8(m) union (thm-pb-lower): C = Theta(m^9), N, B2 = Theta(m^8): beta = 1, e = 9/8.
  K_{s,s,s}: N = 3 s^2, B2 = s^3, C = s^2 (1 + s): beta = 3/2, e = 3/2.
"""
import os, sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fbeta.svg")


def upper(b):
    return min(Fr(3, 2), max(Fr(1), min((10 * b - 1) / 8, Fr(3, 8) + Fr(3, 4) * b)))


def old_upper(b):  # thm-pb-upper alone (the curve of revision 2)
    return min(Fr(3, 2), max(Fr(1), Fr(3, 8) + Fr(3, 4) * b))


def target(b):
    return max(Fr(1), b)


EXACT_LO, EXACT_HI = Fr(9, 10), Fr(3, 2)  # worst-case exponent known exactly on this closed interval

# (i, j) with j/i in lowest terms, so every beta appears once.
PAIRS = [(1, 1), (6, 5), (5, 4), (4, 3), (3, 2), (5, 3), (2, 1), (5, 2), (3, 1), (4, 1), (6, 1)]
# (p, q) of the asymmetric family D1-D3, 9/10 <= p/q < 1, lowest terms.
DPAIRS = [(9, 10), (11, 12), (14, 15), (19, 20), (39, 40)]
POINTS = []  # (label, kind, beta, exponent of C)
for i, j in PAIRS:
    b = Fr(3, 2) - Fr(j, 2 * i)
    e = Fr(12 * i - 3 * j, 8 * i)
    assert b == Fr(12 * i - 4 * j, 8 * i)
    assert e == upper(b), (i, j)  # matched: the lower family meets the upper bound
    POINTS.append((f"F({i},{j})", "F", b, e))
for p, q in DPAIRS:
    assert 9 * q <= 10 * p and p < q
    b = Fr(p, q)
    e = Fr(10 * p - q, 8 * q)
    assert e == (10 * b - 1) / 8 == upper(b), (p, q)
    assert e < old_upper(b)  # strictly below the revision-2 curve
    POINTS.append((f"D({p},{q})", "D", b, e))
POINTS.append(("G8", "G8", Fr(1), Fr(9, 8)))
POINTS.append(("K(s,s,s)", "K", Fr(3, 2), Fr(3, 2)))
for _, _, b, e in POINTS:
    assert e == upper(b) and target(b) <= e and EXACT_LO <= b <= EXACT_HI

# Breakpoints of the curves.
assert (10 * Fr(9, 10) - 1) / 8 == 1                      # gap opens at 9/10
assert (10 * Fr(1) - 1) / 8 == Fr(3, 8) + Fr(3, 4) * 1     # the two l2 bounds agree at 1
assert Fr(3, 8) + Fr(3, 4) * Fr(5, 6) == 1 and Fr(3, 8) + Fr(3, 4) * Fr(3, 2) == Fr(3, 2)
assert upper(Fr(1)) - target(Fr(1)) == Fr(1, 8)
assert all(upper(b) == 1 for b in (Fr(1, 2), Fr(5, 6), Fr(7, 8), Fr(9, 10)))
assert (old_upper(Fr(19, 20)) - upper(Fr(19, 20))) == (1 - Fr(19, 20)) / 2  # improvement (1 - kappa)/2 on (5/6, 1)

# ---------------------------------------------------------------- SVG
W, H = 640, 540
L, R = 64, 22
T1, B1 = 92, 360  # top panel: exponents
T2, B2p = 390, 490  # bottom panel: gap
XLO, XHI = 0.5, 1.6
Y1LO, Y1HI = 0.9, 1.65
Y2LO, Y2HI = -0.04, 0.15
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
C_UP, C_TGT, C_PT, C_OLD = "#2a78d6", "#eb6834", "#0b0b0b", "#9a9890"


def X(b):
    return L + (float(b) - XLO) / (XHI - XLO) * (W - L - R)


def Y1(e):
    return B1 - (float(e) - Y1LO) / (Y1HI - Y1LO) * (B1 - T1)


def Y2(g):
    return B2p - (float(g) - Y2LO) / (Y2HI - Y2LO) * (B2p - T2)



def sub(base, idx, rest=""):
    """Math-style subscript as SVG tspans (no Unicode subscript glyphs); `rest` follows on the baseline."""
    return f'{base}<tspan dy="3" font-size="8">{idx}</tspan><tspan dy="-3">{rest}</tspan>'


# The script ell is taken from the math font, which has the glyph; the text font may not.
ELL = '<tspan font-family="New Computer Modern Math">ℓ</tspan>'


def ell2(rest):
    return sub(ELL, "2", rest)


# Every kappa is the math-italic kappa of the math font, as in the paper's
# text; the text font's upright Greek kappa has a different shape.
KAPPA = '<tspan font-family="New Computer Modern Math">\U0001D705</tspan>'

s = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    'font-family="New Computer Modern, STIX Two Text, Times, serif" font-size="11">',
    f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
    f'<defs><clipPath id="p1"><rect x="{L}" y="{T1}" width="{W-L-R}" height="{B1-T1}"/></clipPath>'
    f'<clipPath id="p2"><rect x="{L}" y="{T2}" width="{W-L-R}" height="{B2p-T2}"/></clipPath></defs>',
]

XT = [(Fr(1, 2), "1/2"), (Fr(2, 3), "2/3"), (Fr(5, 6), "5/6"), (Fr(9, 10), "9/10"), (Fr(1), "1"),
      (Fr(7, 6), "7/6"), (Fr(4, 3), "4/3"), (Fr(3, 2), "3/2")]
for b, lab in XT:
    x = X(b)
    for top, bot in ((T1, B1), (T2, B2p)):
        s.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bot}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="{x:.1f}" y="{B2p+16}" text-anchor="middle" fill="{MUTED}">{lab}</text>')
for e, lab in ((Fr(1), "1"), (Fr(9, 8), "9/8"), (Fr(5, 4), "5/4"), (Fr(11, 8), "11/8"), (Fr(3, 2), "3/2")):
    y = Y1(e)
    s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="{L-6}" y="{y+4:.1f}" text-anchor="end" fill="{MUTED}">{lab}</text>')
for g, lab in ((Fr(0), "0"), (Fr(1, 16), "1/16"), (Fr(1, 8), "1/8")):
    y = Y2(g)
    s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="{L-6}" y="{y+4:.1f}" text-anchor="end" fill="{MUTED}">{lab}</text>')
for top, bot in ((T1, B1), (T2, B2p)):
    s.append(f'<rect x="{L}" y="{top}" width="{W-L-R}" height="{bot-top}" fill="none" stroke="{MUTED}" stroke-width="0.8"/>')


def poly(f, Y, color, width, brk, dash="", clip="p1"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{X(b):.1f},{Y(f(b)):.1f}" for b in brk)
    s.append(f'<polyline clip-path="url(#{clip})" fill="none" stroke="{color}" stroke-width="{width}"{d} points="{pts}"/>')


# Curves: exact piecewise-linear, so the breakpoints are the vertices.
LOW = [Fr(1, 2), Fr(9, 10)]                       # upper bound only (C <= 2.15 N)
EXACT = [Fr(9, 10), Fr(1), Fr(3, 2)]              # exact worst-case exponent
poly(target, Y1, C_TGT, 2, [Fr(1, 2), Fr(1), Fr(3, 2), Fr(8, 5)], "6 3")
poly(old_upper, Y1, C_OLD, 1.2, [Fr(5, 6), Fr(1)], "2 2")   # thm-pb-upper alone on (5/6, 1)
poly(upper, Y1, C_UP, 1.4, LOW)
poly(upper, Y1, C_UP, 3.2, EXACT)
# Theorem's term alone beyond 3/2 (AGM caps it there).
s.append(f'<line x1="{X(Fr(3,2)):.1f}" y1="{Y1(Fr(3,2)):.1f}" x2="{X(Fr(8,5)):.1f}" '
         f'y2="{Y1(Fr(3,8)+Fr(3,4)*Fr(8,5)):.1f}" stroke="{C_UP}" stroke-width="1" stroke-dasharray="2 3"/>')
gap = lambda b: upper(b) - target(b)
s.append(f'<line x1="{L}" y1="{Y2(0):.1f}" x2="{W-R}" y2="{Y2(0):.1f}" stroke="{C_TGT}" stroke-width="2" stroke-dasharray="6 3"/>')
poly(lambda b: old_upper(b) - target(b), Y2, C_OLD, 1.2, [Fr(5, 6), Fr(1)], "2 2", clip="p2")
poly(gap, Y2, C_UP, 1.4, LOW, clip="p2")
poly(gap, Y2, C_UP, 3.2, EXACT, clip="p2")


def mark(kind, x, y):
    if kind == "F":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{C_PT}"/>'
    if kind == "D":
        return (f'<path d="M {x:.1f} {y-5:.1f} L {x+5:.1f} {y:.1f} L {x:.1f} {y+5:.1f} L {x-5:.1f} {y:.1f} Z" '
                f'fill="#ffffff" stroke="{C_PT}" stroke-width="1.3"/>')
    if kind == "G8":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="none" stroke="{C_PT}" stroke-width="1.3"/>'
    return f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="#ffffff" stroke="{C_PT}" stroke-width="1.4"/>'


for _, kind, b, e in POINTS:
    s.append(mark(kind, X(b), Y1(e)))
    s.append(mark(kind, X(b), Y2(e - target(b))))

# Legend: two columns of four above the top panel.
lx0, ly = L, 14
legend = [
    ("line", C_UP, "", 3.2, "exact exponent, every real κ ∈ [9/10, 3/2]"),
    ("line", C_UP, "", 1.4, "upper bound C ≤ 2.15 N for κ ≤ 9/10"),
    ("line", C_OLD, "2 2", 1.2, "first " + ell2(" bound alone, 3/8 + 3κ/4, on (5/6, 1)")),
    ("line", C_TGT, "6 3", 2.0, ell2(" target N + ") + sub("B", "2", ": max(1, κ)")),
    ("F", None, None, None, 'F<tspan dy="3" font-size="8">i,j</tspan><tspan dy="-3" dx="4">family, κ = 3/2 − j/(2i)</tspan>'),
    ("D", None, None, None, 'D<tspan dy="3" font-size="8">p,q</tspan><tspan dy="-3" dx="4">family, κ = p/q ∈ [9/10, 1)</tspan>'),
    ("G8", None, None, None, sub("G", "8", " rotation union, κ = 1")),
    ("K", None, None, None, 'K<tspan dy="3" font-size="8">s,s,s</tspan><tspan dy="-3">, κ = 3/2</tspan>'),
]
for k, (kind, color, dash, width, text) in enumerate(legend):
    lx = lx0 + (0 if k < 4 else 300)
    y = ly + 17 * (k % 4)
    if kind == "line":
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.append(f'<line x1="{lx}" y1="{y}" x2="{lx+24}" y2="{y}" stroke="{color}" stroke-width="{width}"{d}/>')
    else:
        s.append(mark(kind, lx + 12, y))
    s.append(f'<text x="{lx+32}" y="{y+4}" fill="{INK}">{text}</text>')

s.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-14}" text-anchor="middle" fill="{INK}">κ = log {sub("B", "2", " / log N")}</text>')
s.append(f'<text transform="translate(16,{(T1+B1)/2:.1f}) rotate(-90)" text-anchor="middle" fill="{INK}">exponent of C in N</text>')
s.append(f'<text transform="translate(16,{(T2+B2p)/2:.1f}) rotate(-90)" text-anchor="middle" fill="{INK}">gap over {ell2("")}</text>')
s.append("</svg>")
with open(OUT, "w") as fh:
    fh.write("\n".join(s).replace("κ", KAPPA) + "\n")

print("label      beta     e=exp(C)  target   gap")
for lab, _, b, e in POINTS:
    print(f"{lab:<10} {str(b):<8} {str(e):<9} {str(target(b)):<8} {e - target(b)}")
print("curve vertices (beta, upper, gap):",
      [(str(b), str(upper(b)), str(upper(b) - target(b))) for b in (Fr(1, 2), Fr(9, 10), Fr(1), Fr(3, 2))])
print(f"wrote {OUT}")
