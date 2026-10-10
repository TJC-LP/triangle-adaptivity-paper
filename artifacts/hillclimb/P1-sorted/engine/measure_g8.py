"""Exact G8 measurements, run with python3 -I engine/measure_g8.py.

Every distinct inner-run shape is actually passed through the port. Repeated
calls are aggregated with integer multiplicities only to avoid executing the
same benchmark invocation billions of times; the modeled executor receives
no cross-call cache, and pays independently for every invocation.
"""

import json
from fractions import Fraction
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
PORT = run_path(str(HERE / 'gallop_port.py'))
intersect = PORT['intersect']


def measure(m):
    a, b, c = m**4, m**2, m**3
    # X=(g,h), g<c,h<m; Z2=(g,t), g<c,t<c.
    # Layered order: Z1[t], Z2[0,t],...,Z2[c-1,t]. Then all Z0.
    z1 = [1 + t * (c + 1) for t in range(c)]
    z0_start = 1 + c * (c + 1)
    z_stats = []
    for g in range(c):
        for h in range(m):
            x = g * m + h
            tx = [2 + t * (c + 1) + g for t in range(c)]
            tx += list(range(z0_start + x * a, z0_start + (x + 1) * a))
            status, hits, meter = intersect(z1, tx)
            assert status == 'done' and not hits
            z_stats.append(meter.as_dict())
    # Y order: Y0[k], then Y2[z,k] for z in lexicographic Z2 order.
    z2_size = c * c
    y0 = [1 + k * (z2_size + 1) for k in range(b)]
    y_stats = []
    y_swapped_stats = []
    for z in range(z2_size):
        sy = [2 + k * (z2_size + 1) + z for k in range(b)]
        status, hits, meter = intersect(y0, sy)
        assert status == 'done' and not hits
        y_stats.append(meter.as_dict())
        status, hits, meter = intersect(sy, y0)
        assert status == 'done' and not hits
        y_swapped_stats.append(meter.as_dict())
    assert all(s == z_stats[0] for s in z_stats)
    assert all(s == y_stats[0] for s in y_stats)
    assert all(s == y_swapped_stats[0] for s in y_swapped_stats)
    Z, Y = z_stats[0], y_stats[0]
    Y_swapped = y_swapped_stats[0]
    assert Z['comparisons'] == 6*c-3 and Z['work'] == 3*c-1
    assert Y['comparisons'] == 6*b-3 and Y['work'] == 3*b-1
    assert Y_swapped['comparisons'] == 6*b-5 and Y_swapped['work'] == 3*b-1
    # Empty smaller side reads and compares nothing, as used at y/z roots.
    assert intersect([], y0)[2].as_dict() == dict(work=0,walked=0,comparisons=0,predicates={})

    # Costs include one unit per visited outer edge. The fields give the
    # actual minima for each metric, independently, across both root options.
    options = {}
    driver_options = {}
    for metric in ('comparisons', 'work', 'walked'):
        rx = b * (1 + Z[metric])
        tx = a + c * (1 + Y[metric])
        assert rx <= tx
        # y in Y0: S visits c empty intersections; R visits a hard ones.
        ry = a * (1 + Z[metric])
        sy = c
        # z in Z2: S visits b empty intersections; T visits m hard ones.
        sz = b
        tz = m * (1 + Y[metric])
        assert sy <= ry and sz <= tz
        one_root = a * min(rx, tx) + b * min(ry, sy) + z2_size * min(sz, tz)
        options[metric] = dict(x_option_R=rx, x_option_T=tx,
                               gadget_root_x=a*min(rx,tx),
                               gadget_root_y=b*min(ry,sy),
                               gadget_root_z=z2_size*min(sz,tz),
                               three_rotation_each_root=one_root,
                               normalized_by_m9=str(Fraction(one_root,m**9)))
        # Real runGroup calls intersectEachBy(n2,n3): on option T,
        # n2=S^-(z) and n3=R(x), hence the balanced Y pair is swapped.
        tx_driver = a + c * (1 + Y_swapped[metric])
        tz_driver = m * (1 + Y_swapped[metric])
        driver_root = a * min(rx, tx_driver) + b * min(ry, sy) + z2_size * min(sz, tz_driver)
        driver_options[metric] = dict(x_option_R=rx, x_option_T=tx_driver,
                                      x_selected='R' if rx <= tx_driver else 'T',
                                      gadget_root_x=a*min(rx,tx_driver),
                                      gadget_root_y=b*min(ry,sy),
                                      gadget_root_z=z2_size*min(sz,tz_driver),
                                      three_rotation_each_root=driver_root,
                                      normalized_by_m9=str(Fraction(driver_root,m**9)))
    C_cmp = options['comparisons']['three_rotation_each_root']
    C_work = options['work']['three_rotation_each_root']
    C_proxy = options['walked']['three_rotation_each_root']
    assert C_cmp == 6*m**9 + m**8 - 2*m**6 + m**5
    assert C_work == 3*m**9 + m**8 + m**5
    assert C_proxy == m**9 + m**8 + m**6 + m**5
    # Pure key comparison minimum excludes all outer-loop charges. This
    # reverses the preferred x option (T wins), so present it distinctly.
    pure_cmp = a * min(b * Z['comparisons'], c * Y['comparisons'])
    assert pure_cmp == 6*m**9 - 3*m**7
    driver_pure_cmp = a * min(b * Z['comparisons'], c * Y_swapped['comparisons'])
    assert driver_pure_cmp == 6*m**9 - 5*m**7
    N = 3 * (2*m**8 + m**7 + m**6 + m**5)
    forward_norm = 5*m**8
    reverse_norm = m**12 + 2*m**11 + 3*m**10 + m**7
    assert forward_norm <= reverse_norm
    driver_selected = driver_options['comparisons']['x_selected']
    driver_outer = a * (b if driver_selected == 'R' else a+c) + m**5 + m**8
    driver_total = driver_options['comparisons']['three_rotation_each_root']
    return dict(m=m, N=N, B2=5*m**8, m9=m**9,
                each_forward_norm=forward_norm, each_reverse_norm=reverse_norm,
                actual_port_calls=len(z_stats)+len(y_stats)+len(y_swapped_stats),
                Z1_vs_Tx=Z, Y0_vs_Sz=Y, Sz_vs_Y0=Y_swapped, options=options,
                actual_driver_argument_order_options=driver_options,
                pure_comparison_minimum_each_root=pure_cmp,
                actual_driver_argument_order_pure_comparison_minimum=driver_pure_cmp,
                actual_driver_chosen_plan_key_comparisons=driver_total-driver_outer,
                actual_driver_chosen_plan_outer_steps=driver_outer,
                actual_driver_comparison_cost_over_N_plus_B2=str(Fraction(driver_total,N+forward_norm)),
                optimal_ternary_comparisons_plus_outer=2*m**9+m**8+m**5,
                chosen_comparison_plus_outer_plan_key_comparisons=6*m**9-3*m**6,
                chosen_comparison_plus_outer_plan_outer_steps=m**6+m**8+m**5,
                comparison_cost_over_N_plus_B2=str(Fraction(C_cmp,N+5*m**8)))


if __name__ == '__main__':
    cases = [measure(m) for m in range(2,6)]
    c2,c4 = cases[0],cases[2]
    result = dict(self_test=PORT['self_test'](),
                  methodology='Exact independent-call costs with integer multiplicities; no executor caching',
                  cases=cases,
                  m2_to_m4_ratios=dict(
                    N=str(Fraction(c4['N'],c2['N'])),
                    canonical_comparison_cost=str(Fraction(c4['options']['comparisons']['three_rotation_each_root'],c2['options']['comparisons']['three_rotation_each_root'])),
                    driver_order_comparison_cost=str(Fraction(c4['actual_driver_argument_order_options']['comparisons']['three_rotation_each_root'],c2['actual_driver_argument_order_options']['comparisons']['three_rotation_each_root'])),
                    optimal_ternary_cost=str(Fraction(c4['optimal_ternary_comparisons_plus_outer'],c2['optimal_ternary_comparisons_plus_outer'])),
                    leading_m9='512'))
    out = HERE / 'g8_counts.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
