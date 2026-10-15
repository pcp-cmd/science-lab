# Spatial validation: which prediction task does the error describe?

[中文](README.md) | [English](README.en.md)

This is a reproducible method demonstration using synthetic Gaussian fields. It also explores the conditions under which the results hold. **Novelty has not been established.** This is not a result-by-result replication of the cited papers' real-data experiments.

## Question and results

Random missing points, a contiguous interior gap, and an edge gap are different prediction tasks. Each task uses 160 observed points to predict 40 missing points.

The main example has 200 equally spaced points on a one-dimensional grid. The field has zero mean and unit variance. Its covariance is exponential, with no observation noise. The predictor knows the correct correlation length of 40.

- Random five-fold cross-validation has an exact mean squared error (MSE) of 0.029373. The contiguous interior-gap target has an exact MSE of 0.327692. Random cross-validation underestimates this target risk by 91.04%.
- Contiguous five-fold cross-validation includes edge blocks. Its exact MSE is 0.427970. It overestimates the interior target risk by 30.60%.
- Matching the nearest-observation distances to 1–20 does not remove the difference. One-sided and two-sided observations still give risks that differ by 17.05%. This percentage uses the two-sided risk as its denominator.
- Parameter misspecification can reverse the ordering. With a true correlation length of 2 and an assumed length of 10, the two-sided risk is 1.103229. It exceeds the one-sided risk of 1.100060. The model-reported variance also differs from the true MSE.

Define the deployment task and available information before designing validation splits. These numbers do not directly generalize to unknown hyperparameters, nonstationarity, observation noise, two dimensions, or real-world maps. The misspecification analysis is exploratory work performed after the main results.

## Read and run

Start with the [complete Chinese tutorial](TUTORIAL.zh-CN.md). It retains the background, step-by-step algebra, complete example code, references, negative controls, failure examples, misspecification boundaries, and exercises.

Two figures illustrate [validation geometry](figures/research_unit.png) and [misspecification boundaries](figures/misspecification_boundary.png).

Use a Python environment with NumPy already installed. Run these commands from this directory:

```sh
OPENBLAS_NUM_THREADS=1 python -B minimal.py
OPENBLAS_NUM_THREADS=1 python -B minimal_boundary.py
OPENBLAS_NUM_THREADS=1 python -B check_evidence.py
```

The scripts do not access the network or download data. The first two generate small teaching simulations. The third uses analytical formulas to check selected tables. These minimal scripts do not reconstruct the full original experiment.

## Evidence and verification scope

- The [36-row main summary](evidence/summary.csv) covers six correlation lengths and six scoring schemes. It includes MSE, standard errors, and intervals.
- The [45 misspecification cases](evidence/extension_grid.csv) and [nine secondary comparisons](evidence/extension_secondary.csv) include all cases, not just those supporting the conclusions.
- The [exploratory mechanism results](evidence/mechanism_summary.json) retain an interval example from the independent and identically distributed (iid) control. It does not establish a real mechanism effect.
- The [main configuration](evidence/protocol.json) and [misspecification configuration](evidence/extension_config.json) preserve scientific settings and random seeds.
- original_verification.json and original_extension_verification.json record checks from the original experiment. The same researcher implemented the independent algorithmic checks. These records are not external blind review.

During preparation on 2026-10-15, SHA-256 hashes were checked for 83 entries in the source package manifest. The two minimal scripts and this edition's check_evidence.py were then reviewed and executed. The environment used Python 3.12.14 and NumPy 2.3.5. No packages were installed.

The [main example output](validation/minimal-output.txt), [boundary output](validation/boundary-output.txt), and [analytical check results](validation/evidence-check.json) record the checks actually performed for this edition.

This edition rechecked endpoint true risks and model-reported variances for all 45 grid cases. It also rechecked deployment risks and mixture identities across six correlation lengths. It did not recheck the original large weight matrices or per-field arrays. It did not recompute every standard error from the original samples.

The full experiment runners and large raw arrays are not included. Historical verification records must not be read as fresh verification by this edition. The original full experiment also used SciPy 1.17.0 and Matplotlib 3.10.8. References are retained from the original tutorial. No new literature search was performed during preparation.
