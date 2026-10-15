# When can an averaged Markov model predict first-passage times?

[中文](README.md) | English

This is a reproducible research and teaching unit.
It studies finite-state continuous-time Markov chains with a rapidly switching environment.
The question is whether averaging out the environment preserves first-passage times accurately enough.
All examples are synthetic.
Public edition: 1.0.0.
Preparation date: 2026-10-15.

## Start here

The detailed tutorials and verification report are in Chinese.

- [Intuition, assumptions, CDF proof, counterexamples and exercises](TUTORIAL.zh-CN.md)
- [Exact review, floating-point zero-test correction, mean and tail proofs, and complete minimal code](TUTORIAL_REVIEW.zh-CN.md)
- [Literature and historical reading scope](literature_notes.zh-CN.md)
- [What was actually rerun for this public edition](VERIFICATION.md)

## Main results: assess each error metric separately

The main example has two positions and two environments.
The bounds cover every initial microstate.
The CDF bound covers all times.

- The absolute error in the first-passage-time CDF is at most min(1, 49/(18ν)). A sufficient threshold for error at most 1% is ν ≥ 2450/9 ≈ 272.2222.
- The relative error in the mean first-passage time has a separate certificate. It is at most 1% when ν ≥ 608458/4095 ≈ 148.5856. This threshold does not replace the CDF threshold.
- At ν=300, the certified relative mean error bound is 10201/2448684 ≈ 0.00416591. The exponential decay rate in the survival-tail bound is 58302/40517. The result files give the prefactor for each initial microstate.
- Failure of a sufficient certificate means “uncertified.” It does not establish that averaging fails or that the true mean is infinite.

The CDF theorem requires finite, homogeneous, conservative and irreducible fast blocks.
The target must consist of whole fast blocks.
The killed generators must be valid.
The selected all-time bound also requires its stated transience or decay conditions.
The mean certificate additionally requires every entry of the corrector vectors v and g to be strictly positive.
The executable exact interface covers only one or two slow states.
Each slow state has two environments with common positive environment-switching rates.

These are teaching applications of existing averaging, lumpability, Poisson-corrector and Lyapunov-comparison methods.
Novelty is not established.
Algorithmic cross-checks are not independent peer review.

## Reproduce with the Python standard library

Run these commands from this directory.
Do not use Python's `-O` option.
It disables the assertion checks.

```sh
python3 -B mean_minimal.py
python3 -B cdf_certificate_exact.py
python3 -B audit_exact.py
python3 -B repair_probes.py
python3 -B mean_exact.py
python3 -B validate_mean.py
```

The minimal example is self-contained.
The other exact scripts share the Fraction/Cramer helpers in `audit_exact.py`.
The audit cross-checks a centered two-environment formula against Cramer's rule.
The minimal example uses Gaussian elimination.
The final comparison script compares freshly recomputed exact means with the included historical floating-point results.
It does not rerun the floating-point solver.

Optional: `mean_float.py` independently constructs and solves the six mean cases using NumPy/SciPy.
The historical versions were NumPy 2.3.5 and SciPy 1.17.0.
Run it before `validate_mean.py` to regenerate and compare both routes.
No dependencies were installed for this public edition.
The floating-point solver was not rerun during preparation.

## Evidence and known correction

`results/` contains the current exact audit, exact means, regression probes and execution logs.
It also contains historical floating-point means, the CDF grid summary and extracted exact algebraic certificates.
Rerunning a script overwrites its corresponding result files.

An old floating-point demonstration treated residuals below 1e-12 as exact zero.
That rule is unsafe for general strict certification.
The public CDF interface uses exact rational arithmetic.
It rejects floating-point inputs.
It preserves a tiny but nonzero error bound in the regression example.
Historical rational certificates for the original models independently support the quoted main constants.
They do not rely on the faulty tolerance-based zero test.

This compact edition omits dense CDF curves, images and the full historical 776-point rational probability enclosure grid.
It therefore does not provide a complete rerun entry point for that historical grid.
The complete mathematical derivations are included.
All code dependencies needed for the public reproduction commands above are included.
