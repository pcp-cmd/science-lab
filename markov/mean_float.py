#!/usr/bin/env python3
"""Implementation A: independent NumPy/SciPy matrix construction and solves."""
import json
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import numpy as np
import scipy
from scipy.linalg import solve

ROOT = Path(__file__).resolve().parent


def main():
    protocol = json.loads((ROOT / 'mean_protocol.json').read_text())
    output = {'computed_at_utc': datetime.now(timezone.utc).isoformat(),
              'implementation': 'A: NumPy/SciPy, independent construction and dense solves',
              'numpy': np.__version__, 'scipy': scipy.__version__, 'cases': {}}
    for name, spec in protocol['models'].items():
        env = np.asarray(spec['K_environment'], dtype=float)
        environments = [np.asarray(spec[f'A_env{e}'], dtype=float) for e in range(2)]
        m = len(environments[0])
        k = np.kron(np.eye(m), env)
        l = np.zeros((2 * m, 2 * m))
        for e in range(2):
            l[e::2, e::2] = environments[e]
        pi_system = env.T.copy()
        pi_system[-1] = 1.
        pi_rhs = np.zeros(2)
        pi_rhs[-1] = 1.
        pi = solve(pi_system, pi_rhs)
        j = np.repeat(np.eye(m), 2, axis=0)
        p = np.kron(np.eye(m), pi.reshape(1, 2))
        a = p @ l @ j
        ma = solve(-a, np.ones(m))
        d = l @ j - j @ a
        h = solve(k + j @ p, -d)
        z, c = j @ ma, h @ ma
        r = l @ c
        cstar, rstar = float(np.max(np.abs(c) / z)), float(np.max(np.abs(r)))
        rows = []
        for speed in protocol['speeds'][name]:
            nu = float(Fraction(speed))
            q = nu * k + l
            v, g = z + c / nu, 1. - r / nu
            mean = solve(-q, np.ones(2 * m))
            valid = bool(np.min(v) > 0 and np.min(g) > 0)
            row = {'nu': speed, 'z': z.tolist(), 'c': c.tolist(), 'r': r.tolist(),
                   'v': v.tolist(), 'g': g.tolist(), 'certificate_applicable': valid,
                   'full_mean': mean.tolist(),
                   'observed_relative_mean_error': float(np.max(np.abs(mean - z) / z)),
                   'residual_max': float(np.max(np.abs(q @ v + g)))}
            if valid:
                lower, upper = v / np.max(g), v / np.min(g)
                bound = float(np.max(np.maximum(np.abs(lower - z), np.abs(upper - z)) / z))
                row.update({'lower_mean': lower.tolist(), 'upper_mean': upper.tolist(),
                            'relative_mean_error_bound': bound,
                            'tail_beta': float(np.min(g) / np.max(v)),
                            'tail_prefactor_by_microstate': (v / np.min(v)).tolist()})
            rows.append(row)
        output['cases'][name] = {'mean_averaged': ma.tolist(), 'c': c.tolist(), 'r': r.tolist(),
                                 'cstar': cstar, 'rstar': rstar,
                                 'simple_1percent_threshold': rstar + 100 * (cstar + rstar), 'rows': rows}
    (ROOT / 'results/mean_float.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print('Independent floating mean implementation: six pairs saved, zero matrix exponentials.')


if __name__ == '__main__':
    main()
