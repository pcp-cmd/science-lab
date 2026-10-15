"""Small repair checks: no old grid, no matrix exponential."""
from fractions import Fraction as F
from pathlib import Path
import json
from cdf_certificate_exact import certificate

eps = F(1, 10**13)
tiny = certificate([[-1]], [[-1 - 2 * eps]], 1, forward=1, backward=1)
assert tiny['exact_survival'] is False
assert tiny['bound_all_time'] > 0
conservative = certificate([[0]], [[0]], 1, forward=1, backward=1)
assert conservative['exact_survival'] is True and conservative['bound_all_time'] == 0
partly_nonabsorbing = certificate([[-1, 0], [0, 0]], [[-2, 0], [0, 0]], 10)
assert partly_nonabsorbing['exact_survival'] is False
assert partly_nonabsorbing['bound_all_time'] is None
assert partly_nonabsorbing['bound_finite_horizon'] > 0
float_rejected = False
try:
    certificate([[-1.0]], [[-2.0]], 10)
except TypeError:
    float_rejected = True
assert float_rejected
output = {'tiny_nonzero': tiny, 'exact_nonabsorbing': conservative,
          'nonexact_nonabsorbing': partly_nonabsorbing, 'float_input_rejected': float_rejected,
          'all_checks_passed': True, 'CDF_evaluations': 0}
(Path(__file__).resolve().parent / 'results/repair_probes.json').write_text(json.dumps(output, default=str, indent=2) + '\n')
print(json.dumps(output, default=str, indent=2))
