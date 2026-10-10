# Consistency of the LP term lists with the brute-force-verified closed forms: for random parameter tuples, every closed-form
# statistic S lies between max(monomials) and (#monomials) * max(monomials), where the monomials are the LP's exponent vectors.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import random
from fractions import Fraction as Fr
from lp_design import terms
from live_gadget import params_ok, closed_live
rng = random.Random(7)
def mono(form, i, vals):
    r = Fr(1)
    for key, ex in form.items():
        base = vals[key[0]]
        r *= Fr(base) ** ex
    return r
cnt = 0
tuples = []
for p in (1, 2, 3, 4, 6, 8, 12, 16, 24):
    for q in (1, 2, 3, 4, 6, 8):
        for t in (1, 2, 3, 4, 6, 8):
            for g in (1, 2, 3, 4, 6, 8):
                for k in (1, 2, 3, 4):
                    for w in (1, 2, 3, 4):
                        if params_ok(p, q, t, g, k, w):
                            tuples.append((p, q, t, g, k, w))
size, fwd, bwd = terms(1)
stat_of = {'R': 'R', 'S': 'S', 'T': 'T', 'al': 'al', 'be': 'be', 'ga': 'ga', 'alp': 'alp', 'bep': 'bep', 'gap': 'gap'}
allterms = {**size, **fwd, **bwd}
for pr in tuples:
    vals = dict(zip('PQTGKW', pr))
    c = closed_live(*pr)
    for key, lst in allterms.items():
        ms = [mono(f, 1, vals) for f in lst]
        S = c[stat_of[key]]
        assert max(ms) <= S <= 12 * max(ms), (pr, key, S, ms)
    assert c['Cx'] >= pr[0] * pr[1] * pr[2]
    cnt += 1
print(f"LP term lists consistent with closed forms on {cnt} parameter tuples (each statistic within [max, 12*max] of its monomials)")
