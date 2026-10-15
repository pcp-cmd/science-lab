"""Compare already-saved outputs only; no rerun of either calculation."""
from fractions import Fraction
from pathlib import Path
import json

p = Path(__file__).resolve().parent
exact = json.loads((p / 'results/mean_exact.json').read_text())
floating = json.loads((p / 'results/mean_float.json').read_text())
errors = []


def compare(x, y):
    value = float(Fraction(x))
    discrepancy = abs(value - y)
    errors.append(discrepancy)
    assert discrepancy <= 1e-10 * max(1, abs(value)), (x, y)


def compare_vector(x, y):
    assert len(x) == len(y)
    for xr, yr in zip(x, y):
        compare(xr[0], yr)


for name, b in exact['cases'].items():
    a = floating['cases'][name]
    for field in ('cstar', 'rstar', 'simple_1percent_threshold'):
        compare(b[field], a[field])
    for field in ('mean_averaged', 'c', 'r'):
        compare_vector(b[field], a[field])
    for br, ar in zip(b['rows'], a['rows']):
        assert br['nu'] == ar['nu']
        assert br['certificate_applicable'] == ar['certificate_applicable']
        for field in ('z', 'c', 'r', 'v', 'g'):
            compare_vector(br[field], ar[field])
        compare_vector(br['exact_full_mean'], ar['full_mean'])
        compare(br['observed_exact_relative_mean_error'], ar['observed_relative_mean_error'])
        if br['certificate_applicable']:
            for field in ('lower_mean', 'upper_mean', 'tail_prefactor_by_microstate'):
                compare_vector(br[field], ar[field])
            for field in ('relative_mean_error_bound', 'tail_beta'):
                compare(br[field], ar[field])
report = {'all_checks_passed': True, 'scalar_comparisons': len(errors),
          'max_absolute_discrepancy': max(errors), 'relative_tolerance': 1e-10,
          'new_CDF_evaluations': 0, 'model_speed_pairs': 6,
          'independence_scope': 'Independent algorithms and construction in the same model/session; not independent peer review.'}
(p / 'results/mean_crosscheck.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
