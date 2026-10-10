# Constants behind the exactness of the design-space LP: non-designated roots of a live gadget cost O(N(L)),
# and the designated root costs pqt + O(N(L)); so C(union) is within [min_v p_v q_v t_v, min_v p_v q_v t_v + c0 N].
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from fractions import Fraction as Fr
from live_gadget import params_ok, closed_live
worst = {'Cy/N': Fr(0), 'Cz/N': Fr(0), '(Cx-pqt)/N': Fr(0), 'Cx/pqt': Fr(0)}
cnt = 0
for p in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128):
    for q in (1, 2, 3, 4, 6, 8, 16, 32, 64):
        for t in (1, 2, 3, 4, 6, 8, 16, 32):
            for g in (1, 2, 3, 4, 6, 8, 16, 32, 64):
                for k in (1, 2, 4, 8, 16):
                    for w in (1, 2, 4, 8, 16):
                        if params_ok(p, q, t, g, k, w):
                            c = closed_live(p, q, t, g, k, w); N = c['N']; pqt = p * q * t
                            worst['Cy/N'] = max(worst['Cy/N'], Fr(c['Cy'], N)); worst['Cz/N'] = max(worst['Cz/N'], Fr(c['Cz'], N))
                            worst['(Cx-pqt)/N'] = max(worst['(Cx-pqt)/N'], Fr(c['Cx'] - pqt, N)); worst['Cx/pqt'] = max(worst['Cx/pqt'], Fr(c['Cx'], pqt))
                            assert c['Cx'] >= pqt
                            cnt += 1
print(cnt, "tuples; worst", {k: f"{float(v):.4f}" for k, v in worst.items()})
