#!/usr/bin/env python3
"""Bounded fresh audit. Standard library; no imports from the earlier solver.

Two exact routes for H: a two-state centered formula and Cramer's rule.
No matrix-exponential sampling, no rerun of the old 776 checks.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from datetime import datetime, timezone
import json
import math

ROOT = Path(__file__).resolve().parent


def mat(rows):
    return [[F(str(x)) for x in row] for row in rows]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    assert len(a) == len(b) and len(a[0]) == len(b[0])
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, s):
    return [[x * s for x in row] for row in a]


def subtract(a, b):
    return add(a, scale(b, -1))


def product(a, b):
    assert len(a[0]) == len(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def power(a, k):
    out = identity(len(a))
    for _ in range(k):
        out = product(out, a)
    return out


def determinant(a):
    n = len(a)
    assert all(len(row) == n for row in a)
    total = F(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F((-1) ** inversions)
        for i, j in enumerate(perm):
            term *= a[i][j]
        total += term
    return total


def cramer(a, b):
    """Deliberately different from the earlier Gaussian elimination."""
    d = determinant(a)
    if not d:
        raise ValueError('singular matrix')
    out = [[F(0) for _ in b[0]] for _ in a]
    for col in range(len(b[0])):
        for variable in range(len(a)):
            replaced = [row[:] for row in a]
            for i in range(len(a)):
                replaced[i][variable] = b[i][col]
            out[variable][col] = determinant(replaced) / d
    assert product(a, out) == b
    return out


def norm(a):
    return max(sum(abs(x) for x in row) for row in a)


def zero(a):
    return all(x == 0 for row in a for x in row)


def serial(a):
    return [[str(x) for x in row] for row in a]


def is_subgenerator(a):
    return all(sum(row) <= 0 and all(x >= 0 for j, x in enumerate(row) if j != i)
               for i, row in enumerate(a))


def two_environment(a0, a1, forward=F(1), backward=F(2)):
    a0, a1 = mat(a0), mat(a1)
    m, n = len(a0), 2 * len(a0)
    k = [[F(0) for _ in range(n)] for _ in range(n)]
    l = [[F(0) for _ in range(n)] for _ in range(n)]
    j = [[F(0) for _ in range(m)] for _ in range(n)]
    p = [[F(0) for _ in range(n)] for _ in range(m)]
    total = forward + backward
    env = [[-forward, forward], [backward, -backward]]
    pi = [backward / total, forward / total]
    for x in range(m):
        for e in range(2):
            i = 2 * x + e
            j[i][x], p[x][i] = F(1), pi[e]
            for f in range(2):
                k[i][2 * x + f] = env[e][f]
            for y in range(m):
                l[i][2 * y + e] = (a0, a1)[e][x][y]
    a = product(product(p, l), j)
    d = subtract(product(l, j), product(j, a))
    h = scale(d, 1 / total)  # On centered two-state vectors, K acts as -(a+b)I.
    assert h == cramer(add(k, product(j, p)), scale(d, -1))
    return k, l, j, p, a, d, h


def analyze(a0, a1):
    k, l, j, p, a, d, h = two_environment(a0, a1)
    one = [[F(1)] for _ in a]
    r = subtract(product(l, h), product(h, a))
    mean = cramer(scale(a, -1), one)
    assert all(row[0] > 0 for row in mean)
    assert is_subgenerator(k) and all(sum(row) == 0 for row in k)
    assert is_subgenerator(l) and is_subgenerator(a)
    identities = {
        'KJ=0': zero(product(k, j)), 'PK=0': zero(product(p, k)),
        'PJ=I': product(p, j) == identity(len(a)), 'PD=0': zero(product(p, d)),
        'KH=-D': product(k, h) == scale(d, -1), 'PH=0': zero(product(p, h)),
    }
    assert all(identities.values())
    endpoints = norm(product(h, one)) + norm(h)
    kappa = min(-row[0] for row in product(a, one))
    column = endpoints + sum(max(abs(row[z]) for row in r) * mean[z][0] for z in range(len(a)))
    kill = endpoints + norm(r) / kappa if kappa > 0 else None
    gate = [zero(product(d, product(power(a, z), one))) for z in range(len(a))]
    nu = F(3)
    q = add(scale(k, nu), l)
    checks = []
    for degree in range(5):
        lhs = subtract(product(power(q, degree), j), product(j, power(a, degree)))
        rhs = add(scale(product(power(q, degree), h), -1), product(h, power(a, degree)))
        for left_degree in range(degree):
            rhs = add(rhs, product(product(power(q, left_degree), r), power(a, degree - 1 - left_degree)))
        checks.append(lhs == scale(rhs, 1 / nu))
    assert all(checks)
    return {
        'A': serial(a), 'D': serial(d), 'H': serial(h), 'R': serial(r),
        'norm_H': str(norm(h)), 'norm_H1': str(norm(product(h, one))),
        'norm_R': str(norm(r)), 'kappa': str(kappa), 'mean_averaged': serial(mean),
        'constant_kill': str(kill) if kill is not None else None,
        'constant_column': str(column), 'strong_exact': zero(d),
        'survival_exact': all(gate), 'krylov_zero_tests': gate,
        'identities': identities, 'duhamel_taylor_degrees_0_to_4': checks,
    }


def main():
    models = {
        'main': ([[-2, 1], [2, -3]], [[-5, 3], [1, -4]]),
        'zero_direct_kill': ([[-1, 1], [1, -2]], [[-3, 3], [2, -4]]),
        'survival_exact_not_lumpable': ([[-2, 1], [2, -3]], [[-4, 3], [1, -2]]),
    }
    results = {name: analyze(*spec) for name, spec in models.items()}
    assert F(results['main']['constant_kill']) == F(49, 18)
    assert F(results['main']['constant_kill']) / F(1, 100) == F(2450, 9)
    assert results['zero_direct_kill']['constant_column'] == '21/5'
    negatives = {}
    q = mat([[-1, 1], [0, -2]])
    one = mat([[1], [1]])
    qt = [list(row) for row in zip(*q)]
    assert product(q, one) != product(qt, one)
    negatives['orientation'] = {'Q1': serial(product(q, one)), 'QT1': serial(product(qt, one))}
    m = mat([[1, -1], [0, 0]])
    assert norm(m) == 2 and max(abs(x) for row in m for x in row) == 1
    assert norm(product(m, mat([[1], [-1]]))) == 2
    negatives['norm'] = {'induced_infinity': '2', 'max_absolute_entry': '1'}
    assert not is_subgenerator(mat([[1]]))
    negatives['non_subgenerator'] = 'Q=[1] has exp(Qt)=exp(t)>1; contraction is false'
    assert not zero(product(mat([[-1]]), mat([[1]])))
    negatives['split_target'] = 'Killed K=[-1], hence KJ=-1, incompatible'
    jp = mat([['1/2', '1/2'], ['1/2', '1/2']])
    assert determinant(jp) == 0
    negatives['reducible_block'] = 'K=0 on two states and one coarse block: K+JP singular, KH=-D impossible for nonzero D'
    assert determinant(mat([[0]])) == 0
    negatives['nontransient_average'] = 'A=[0]: -A*m=1 has no solution'
    k, l, j, p, a, d, h = two_environment([[-2, 1], [1, -3]], [[-4, 3], [2, -4]])
    assert zero(product(d, one)) and not zero(product(d, product(a, one)))
    negatives['only_D1'] = {'D1': serial(product(d, one)), 'DA1': serial(product(d, product(a, one))),
                            'conclusion': 'equal initial hazards do not imply equal survival distributions'}
    # All rates <=2. h1=exp(-t), h2=exp(-2t)*(1+2t), h3=exp(-2t).
    a_cross = mat([[-1, 0, 0], [0, -2, 2], [0, 0, -2]])
    means = cramer(scale(a_cross, -1), mat([[1], [1], [1]]))
    assert means == mat([[1], [1], ['1/2']])
    negatives['max_integral_swap'] = {
        'A': serial(a_cross), 'mean': serial(means), 'max_integral': '1',
        'integral_of_max_lower_bound': '1+exp(-1)-2*exp(-2)>1, since exp(1)>2',
        'lower_bound_approx': 1 + math.exp(-1) - 2 * math.exp(-2),
    }
    eps = F(1, 10**13)
    _, _, _, _, _, tiny_d, _ = two_environment([[-1]], [[-1 - 2 * eps]], F(1), F(1))
    assert tiny_d == [[eps], [-eps]] and not zero(tiny_d)
    negatives['tiny_nonzero'] = {
        'epsilon': str(eps), 'D': serial(tiny_d), 'exact_survival': False,
        'survival_derivative_difference_at_zero': serial(tiny_d),
        'expected_float_gate_misclassification': 'original tolerance 1e-12 treats nonzero D1 as zero',
    }
    out = {'computed_at_utc': datetime.now(timezone.utc).isoformat(),
           'implementation': 'fresh Fraction Cramer determinants + analytic centered two-state formula',
           'no_old_grid_or_776_rerun': True, 'public_edition': '1.0.0',
           'models': results, 'negative_controls': negatives,
           'main_1percent_threshold_exact': '2450/9',
           'status': 'mathematical certificate passed bounded audit; float-only zero gate unsafe for generalized reuse',
           'novelty': 'not established', 'peer_review': False}
    (ROOT / 'results/audit_exact.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    for name, result in results.items():
        print(name, 'Ckill=', result['constant_kill'], 'Ccol=', result['constant_column'],
              'strong_exact=', result['strong_exact'], 'survival_exact=', result['survival_exact'])
    print('main 1% threshold = 2450/9; exact audit passed; negative controls =', len(negatives))


if __name__ == '__main__':
    main()
