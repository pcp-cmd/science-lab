"""Check selected aggregate evidence with scalar endpoint formulas; no new samples."""
import csv
import json
from pathlib import Path
import numpy as np
from minimal_boundary import point_risks

ROOT = Path(__file__).resolve().parent

def main():
    with (ROOT / 'evidence/extension_grid.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 45
    errors = []
    for row in rows:
        truth, model = float(row['true_ell']), float(row['assumed_ell'])
        one, both, *_ = point_risks(truth, model)
        reported_one, reported_both, *_ = point_risks(model, model)
        for key, value in [('edge20_true_mse', one.mean()), ('interior20_true_mse', both.mean()),
                           ('edge20_reported_variance', reported_one.mean()),
                           ('interior20_reported_variance', reported_both.mean())]:
            errors.append(abs(float(row[key]) - value))
    assert max(errors) < 1e-9
    with (ROOT / 'evidence/summary.csv').open() as handle:
        summary = list(csv.DictReader(handle))
    assert len(summary) == 36
    for ell in sorted({float(r['ell']) for r in summary}):
        values = {r['method']: float(r['exact_mse']) for r in summary if float(r['ell']) == ell}
        assert np.isclose(values['blocked_cv'], .6*values['interior_cv'] + .4*values['edge_cv'])
        if ell == 0:
            assert all(np.isclose(value, 1) for value in values.values())
        else:
            d = np.arange(1, 41)
            interior = np.mean((-np.expm1(-2*d/ell))*(-np.expm1(-2*(41-d)/ell))/(-np.expm1(-82/ell)))
            edge = np.mean(-np.expm1(-2*d/ell))
            assert abs(values['deploy_interior']-interior) < 1e-9
            assert abs(values['deploy_edge']-edge) < 1e-9
    print(json.dumps({'passed': True, 'extension_grid_rows': len(rows),
        'max_endpoint_risk_or_reported_variance_error': float(max(errors)),
        'primary_summary_rows': len(summary),
        'checks': ['all 45 grid true and reported risks', 'six-length primary mixture identity',
                   'iid primary control', 'six-length deployment endpoint risks'],
        'not_checked': ['original raw arrays', 'original Monte Carlo standard errors from raw samples',
                        'all original dense weight matrices', 'random-split exact risks across all lengths']}, indent=2))

if __name__ == '__main__':
    main()
