# science-lab

[中文](README.md) | English

Start with a concrete question. Check the answer with a small program. Then explain the method.

This repository contains four sets of scientific computing and learning materials. Start with intuition. Run an example. Then read the derivation and evidence. The work mainly applies established methods to specific models. It includes conditional error bounds and teaching experiments. **Novel discoveries and external peer recognition have not been established.**

## Where to start

| Module and entry | Fields | Main content | Directory and materials |
|---|---|---|---|
| [Spatial prediction](spatial-validation/README.en.md) | Spatial statistics; machine-learning evaluation | Validation error for random missing points and contiguous gaps; effects of model misspecification | `spatial-validation/`: Chinese tutorial, minimal programs, `evidence/`, `figures/`, and `validation/` |
| [Random environments](random-environment/README.en.md) | Stochastic processes; theoretical ecology; numerical analysis | Extinction risk versus an averaged environment; local certificates for crossing risk curves | `random-environment/`: Chinese tutorial, E01/E02 minimal programs, and `results/` |
| [Markov error bounds](markov/README.en.md) | Probability; multiscale models; reliability methods | Conditional bounds for first-passage distributions, mean waiting times, and tails | `markov/`: two Chinese tutorials, exact computation and audit programs, `results/`, and verification notes |
| [Contact boundary](transit-boundary/README.en.md) | Numerical analysis; computational astronomy | Positive denominators, finite-precision enclosures, and rational certificates near contact | `transit-boundary/`: bilingual explanation, one standard-library program, and `results/` |

The table gives a suggested learning order. Basic Python knowledge is enough to start running examples. You can return to the derivations after reviewing the prerequisites.

## Four ideas to take away

1. Validation should match the prediction task. Random missing points, internal gaps, and extrapolation beyond an edge can have different errors.
2. Averaging parameters before calculating risk can differ from averaging the risks themselves. The direction of the bias is not universal.
3. A small distribution error and a small mean waiting-time error need separate guarantees. The mean also depends on the tail.
4. Failure to produce a certificate does not imply that the mathematical quantity is wrong. Finite precision can enclose a strictly positive number in an interval that includes zero.

The numerical results depend on the models and assumptions stated in each module. They are not direct predictions for real species, maps, or observations.

## How to use the materials

Each module's README gives commands and limitations. The full Chinese tutorials include derivations, references, and exercises. English entry points explain what to run and what the results mean. They are not full translations of the tutorials.

Run a minimal program first. Compare its output with the saved output. Then change one parameter and try to explain the difference.

- `random-environment/`: E01 needs NumPy and SciPy. E02 uses only the Python standard library.
- `markov/`: the listed exact verification commands use only the standard library. Optional floating-point programs need NumPy and SciPy.
- `spatial-validation/`: the minimal experiment needs NumPy.
- `transit-boundary/`: only the standard library is needed.

## Scope of this collection

The first collection is dated 2026-10-15. It contains reading guides, runnable examples, selected evidence, and verification notes for four modules. Each directory distinguishes current verification runs from historical results.

**This is not a complete archive of the original research.** Large per-sample arrays, full parameter grids, and some historical audit implementations are absent. In particular, the E02 minimal program certifies that a root exists. It does not recheck the tutorial's local uniqueness derivation. The contact-boundary example does not load or test PyTransit. Neither entry point is a complete software audit.

Passing a code check is not peer review of a theory. Reading an exercise or running a program does not establish mastery.

See each module for references and assumptions. Questions tied to a specific input, output, or derivation are welcome.

## Universal Gap A | Research progress

- **Completed:** A written proof for finite-dimensional elementary algebras with at most four vertices, with internal review after corrections.
- **Extended:** Additional cases with more vertices under established reduction conditions.
- **Ongoing:** The general case with no bound on the number of vertices. A complete proof has not yet been obtained.
- **Verification:** Independent peer review and formal verification of the full four-vertex result remain pending. Proofs and research details are withheld.
