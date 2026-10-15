#!/usr/bin/env python3
"""Exact mean/tail certificate on the frozen six small cases; standard library.

Reuses only this review's fresh Fraction/Cramer helpers, never the old solvers.
The reference full mean is computed independently of the corrector via -Qm=1.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_exact import (two_environment, product, add, scale, subtract, cramer,
                         zero, serial, is_subgenerator)

ROOT = Path(__file__).resolve().parent


def main():
    protocol = json.loads((ROOT / 'mean_protocol.json').read_text())
    output = {'computed_at_utc': datetime.now(timezone.utc).isoformat(),
              'implementation': 'B: Fraction, centered two-state formula, Cramer determinants',
              'cases': {}, 'pair_count': 0, 'pointwise_CDF_evaluations': 0}
    for name, spec in protocol['models'].items():
        assert spec['K_environment'] == [[-1, 1], [2, -2]]  # Explicit frozen scope.
        k, l, j, p, a, d, h = two_environment(spec['A_env0'], spec['A_env1'])
        one = [[F(1)] for _ in a]
        one_full = [[F(1)] for _ in k]
        mean_average = cramer(scale(a, -1), one)
        z = product(j, mean_average)
        c = product(h, mean_average)
        r = product(l, c)
        assert zero(add(product(k, c), product(d, mean_average)))
        assert zero(product(p, c))
        cstar = max(abs(c[i][0]) / z[i][0] for i in range(len(z)))
        rstar = max(abs(row[0]) for row in r)
        threshold = rstar + 100 * (cstar + rstar)
        rows = []
        for speed in protocol['speeds'][name]:
            nu = F(speed)
            assert nu > 0
            q = add(scale(k, nu), l)
            assert is_subgenerator(q)
            v = add(z, scale(c, 1 / nu))
            g = subtract(one_full, scale(r, 1 / nu))
            assert product(q, v) == scale(g, -1)
            exact_mean = cramer(scale(q, -1), one_full)
            assert all(row[0] > 0 for row in exact_mean)
            gmin, gmax = min(row[0] for row in g), max(row[0] for row in g)
            vmin, vmax = min(row[0] for row in v), max(row[0] for row in v)
            valid = vmin > 0 and gmin > 0
            row = {'nu': speed, 'z': serial(z), 'c': serial(c), 'r': serial(r),
                   'v': serial(v), 'g': serial(g), 'vmin': str(vmin), 'gmin': str(gmin),
                   'certificate_applicable': valid,
                   'exact_full_mean': serial(exact_mean),
                   'observed_exact_relative_mean_error': str(max(abs(exact_mean[i][0] - z[i][0]) / z[i][0] for i in range(len(z))))}
            if valid:
                lower, upper = scale(v, 1 / gmax), scale(v, 1 / gmin)
                assert all(lower[i][0] <= exact_mean[i][0] <= upper[i][0] for i in range(len(z)))
                bound = max(max(abs(lower[i][0] - z[i][0]), abs(upper[i][0] - z[i][0])) / z[i][0] for i in range(len(z)))
                beta = gmin / vmax
                prefactor = scale(v, 1 / vmin)
                assert all(row[0] >= 1 for row in prefactor)
                assert all(product(q, v)[i][0] <= -beta * v[i][0] for i in range(len(v)))
                row.update({'lower_mean': serial(lower), 'upper_mean': serial(upper),
                            'relative_mean_error_bound': str(bound),
                            'mean_admitted_at_1percent': bound <= F(1, 100),
                            'tail_beta': str(beta), 'tail_prefactor_by_microstate': serial(prefactor)})
            else:
                row.update({'rejection_reasons': [reason for yes, reason in ((vmin <= 0, 'v is not strictly positive'), (gmin <= 0, 'g=-Qv is not strictly positive')) if yes],
                            'mean_admitted_at_1percent': False})
            if nu > max(cstar, rstar):
                crude = (cstar + rstar) / (nu - rstar)
                assert F(row['observed_exact_relative_mean_error']) <= crude
                if valid:
                    assert F(row['relative_mean_error_bound']) <= crude
                row['simple_relative_mean_error_bound'] = str(crude)
            rows.append(row)
            output['pair_count'] += 1
        output['cases'][name] = {'mean_averaged': serial(mean_average), 'c': serial(c), 'r': serial(r),
                                 'cstar': str(cstar), 'rstar': str(rstar),
                                 'simple_1percent_threshold': str(threshold), 'rows': rows}
    assert output['pair_count'] == 6
    output['all_exact_checks_passed'] = True
    (ROOT / 'results/mean_exact.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    for name, case in output['cases'].items():
        print(name, 'cstar=', case['cstar'], 'rstar=', case['rstar'], '1% threshold=', case['simple_1percent_threshold'])
        for row in case['rows']:
            print(' nu=', row['nu'], 'applicable=', row['certificate_applicable'],
                  'relative bound=', row.get('relative_mean_error_bound'),
                  'exact error=', row['observed_exact_relative_mean_error'])
    print('six exact model-speed pairs checked; no CDF evaluations')


if __name__ == '__main__':
    main()
