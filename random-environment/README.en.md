# Random environments, extinction risk, and a local root certificate

[中文](README.md) | English

Can average weather represent a population's average fate? These examples compare extinction risk in a switching environment with risk in an averaged environment.

The [full Chinese tutorial](TUTORIAL.zh-CN.md) contains intuition, model definitions, proofs, exercises, and answers. This page is an English entry point, not a full tutorial translation.

## Run the examples

Run these commands from this directory:

- E01: `python minimal_example.py`. It needs NumPy and SciPy. It computes a floating-point approximation using a matrix exponential.
- E02: `python minimal_e02.py`. It uses only the Python standard library. It certifies the existence of a root with rational arithmetic.

For the main E01 example, the extinction probabilities are approximately 0.433281434244 in the switching environment and 0.215104042216 in the averaged environment.

E02 returns the root interval [6.8707275390625, 6.871337890625]. The minimal program proves existence. It does not prove uniqueness. The tutorial gives a separate local uniqueness derivation. Its independent verification program is not included here.

Saved output and software versions are in [results/](results/). These records cover the minimal programs. They do not represent a rerun of the full historical experiments.

## What the examples establish

These are teaching and verification materials for finite models. They are not predictions for a real species. The original full experiment package, exact logs, parameter grids, and independent proof-audit scripts are absent. The minimal programs are therefore not a complete reproduction of the original work.

Methodological novelty and external academic recognition have not been established.
