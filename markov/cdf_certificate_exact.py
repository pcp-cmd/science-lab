#!/usr/bin/env python3
"""Strict replacement example for the old FLOAT-ONLY zero gate.

Scope: one/two slow states, two retained environments per block, common positive
environment rates, rational killed generators. The target is external to these
whole blocks. This is a small exact example, not a general CTMC parser.
"""
from fractions import Fraction as F
from audit_exact import (mat, two_environment, is_subgenerator, product, subtract,
                         scale, cramer, norm, zero)


def certificate(a0, a1, nu, delta='1/100', forward=1, backward=2, horizon=5):
    raw = [v for rows in (a0, a1) for row in rows for v in row]
    raw += [nu, delta, forward, backward, horizon]
    if any(isinstance(v, float) for v in raw):
        raise TypeError('Use int, rational strings, or Fraction; float tolerance is not exact zero.')
    nu, delta, forward, backward, horizon = map(F, (nu, delta, forward, backward, horizon))
    if nu <= 0 or forward <= 0 or backward <= 0 or horizon < 0 or not 0 < delta < 1:
        raise ValueError('Require nu, forward, backward>0, horizon>=0 and 0<delta<1.')
    m = len(a0)
    if m not in (1, 2) or len(a1) != m or any(len(row) != m for rows in (a0, a1) for row in rows):
        raise ValueError('This reviewed example supports square one/two slow-state generators only.')
    if not all(is_subgenerator(mat(rows)) for rows in (a0, a1)):
        raise ValueError('Each environment generator must be a killed subgenerator.')
    k, l, j, p, a, d, h = two_environment(a0, a1, forward, backward)
    one = [[F(1)] for _ in a]
    v = one
    exact = True
    for _ in range(m):
        exact = exact and zero(product(d, v))
        v = product(a, v)
    r = subtract(product(l, h), product(h, a))
    b = norm(product(h, one)) + norm(h)
    finite_constant = b + horizon * norm(r)
    candidates = []
    if exact:
        candidates = [F(0)]
        finite_constant = F(0)
    else:
        kappa = min(-row[0] for row in product(a, one))
        if kappa > 0:
            candidates.append(b + norm(r) / kappa)
        try:
            mean = cramer(scale(a, -1), one)
        except ValueError:
            mean = None
        if mean is not None and all(row[0] > 0 for row in mean):
            candidates.append(b + sum(max(abs(row[z]) for row in r) * mean[z][0] for z in range(m)))
    constant = min(candidates) if candidates else None
    bound = min(F(1), constant / nu) if constant is not None else None
    return {'exact_survival': exact, 'constant_all_time': constant, 'bound_all_time': bound,
            'admitted_all_time': bound is not None and bound <= delta,
            'bound_finite_horizon': min(F(1), finite_constant / nu), 'horizon': horizon}


if __name__ == '__main__':
    print(certificate([[-2, 1], [2, -3]], [[-5, 3], [1, -4]], 300))
