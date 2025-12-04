# Coordinate Search Variants Benchmark on SOLAR10

**MATH462 Final Project**

This project implements and benchmarks three variants of Coordinate Search (CS) algorithms on the SOLAR10 optimization problem.

## Project Overview

The project compares three Coordinate Search variants:
1. **Complete Coordinate Search**: Evaluates all ±eᵢ directions each iteration and chooses the best improving direction
2. **Ordered Coordinate Search**: Evaluates directions in fixed order and accepts the first improving direction
3. **Opportunistic Coordinate Search**: Same acceptance rule as Ordered CS, but directions are shuffled each iteration

All algorithms are tested on 30 randomized SOLAR10 instances with identical experimental conditions.

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- `numpy` - for numerical operations
- `pandas` - for data handling
- `matplotlib` - for plotting

**Note:** This project uses a mock implementation of SOLAR10 (`experiments/solar_mock.py`) since the real SOLAR package is not easily available. The mock is based on the real SOLAR simulator structure and provides a challenging optimization test function.

## Detailed Execution Instructions

### Running All Experiments

Simply run the unified script that executes everything:

```bash
python scripts/run_all.py
```

**What this script does:**
1. Runs the 500-evaluation experiment (all 3 algorithms on 30 instances)
2. Runs the 2000-evaluation experiment (all 3 algorithms on 30 instances)
3. Generates all data profiles (CSV files) for both experiments with τ = 1e-3, 1e-2, and 1e-1
4. Generates all plots (PNG files) for both experiments with all three tolerance values

**Expected output:**
```
============================================================
Coordinate Search Variants Benchmark - Complete Pipeline
============================================================

============================================================
Running 500-evaluation experiment
============================================================
[1/3] Running experiments (MAX_EVALS = 500)...
   Completed 90 runs across 30 instances
[2/3] Computing best-known value and success criterion...
   f* = 4.205723e+01
   Overall success rate: 100.00%
[3/3] Saving raw data...
   Saved: results/raw_runs.csv

============================================================
Running 2000-evaluation experiment
============================================================
[... similar output ...]

============================================================
Generating profiles and plots for 500-eval experiment
============================================================
--- Processing tau = 1e-03 ---
  Saved CSV: results/data_profile_evals.csv
  Saved CSV: results/data_profile_time.csv
  Saved plot: results/plots/data_profile_evals.png
  Saved plot: results/plots/data_profile_time.png
[... continues for all tau values and both experiments ...]

All experiments completed successfully!
```

**Total runtime:** This will take a few minutes as it runs 180 total algorithm runs (90 for 500-evals + 90 for 2000-evals).

### Complete File Structure After Running

After running `scripts/run_all.py`, your `results/` directory will contain:

```
results/
├── raw_runs.csv                          # 500-eval raw data (90 runs)
├── raw_runs_2000.csv                     # 2000-eval raw data (90 runs)
├── data_profile_evals.csv                # 500-eval profile (τ=1e-3)
├── data_profile_time.csv                 # 500-eval time profile (τ=1e-3)
├── data_profiles_eval_tau1e-2.csv        # 500-eval profile (τ=1e-2)
├── data_profiles_eval_tau1e-1.csv        # 500-eval profile (τ=1e-1)
├── data_profiles_time_tau1e-2.csv        # 500-eval time profile (τ=1e-2)
├── data_profiles_time_tau1e-1.csv        # 500-eval time profile (τ=1e-1)
├── data_profiles_eval_2000.csv           # 2000-eval profile (τ=1e-3)
├── data_profiles_time_2000.csv           # 2000-eval time profile (τ=1e-3)
├── data_profiles_eval_2000_tau1e-2.csv   # 2000-eval profile (τ=1e-2)
├── data_profiles_eval_2000_tau1e-1.csv   # 2000-eval profile (τ=1e-1)
├── data_profiles_time_2000_tau1e-2.csv   # 2000-eval time profile (τ=1e-2)
├── data_profiles_time_2000_tau1e-1.csv   # 2000-eval time profile (τ=1e-1)
└── plots/
    ├── data_profile_evals.png            # 500-eval plot (τ=1e-3)
    ├── data_profile_time.png              # 500-eval time plot (τ=1e-3)
    ├── data_profile_evals_tau1e-2.png    # 500-eval plot (τ=1e-2)
    ├── data_profile_time_tau1e-2.png     # 500-eval time plot (τ=1e-2)
    ├── data_profile_evals_tau1e-1.png    # 500-eval plot (τ=1e-1)
    ├── data_profile_time_tau1e-1.png     # 500-eval time plot (τ=1e-1)
    ├── data_profile_evals_2000.png       # 2000-eval plot (τ=1e-3)
    ├── data_profile_time_2000.png        # 2000-eval time plot (τ=1e-3)
    ├── data_profile_evals_2000_tau1e-2.png  # 2000-eval plot (τ=1e-2)
    ├── data_profile_time_2000_tau1e-2.png   # 2000-eval time plot (τ=1e-2)
    ├── data_profile_evals_2000_tau1e-1.png  # 2000-eval plot (τ=1e-1)
    └── data_profile_time_2000_tau1e-1.png   # 2000-eval time plot (τ=1e-1)
```

**Total files generated:** 14 CSV files + 12 PNG plots = 26 files

## Experimental Configuration

- **Dimension**: 10
- **Number of instances**: 30
- **Domain**: [-1, 1]¹⁰
- **Initial step size**: Δ₀ = 1
- **Step size reduction**: Δₖ₊₁ = 0.5 × Δₖ
- **Minimum step size**: Δ_min = 10⁻⁴
- **Maximum evaluations**: 500
- **Maximum CPU time**: 10 seconds per run
- **Success tolerance**: τ = 10⁻³
- **Global RNG seed**: 12345
- **Instance seed offset**: instance_id + 1000

## Project Structure

```
.
├── experiments/
│   ├── __init__.py
│   ├── config.py              # Global configuration constants (500 evals)
│   ├── config_2000.py         # Configuration for 2000-eval experiment
│   ├── solar_wrapper.py       # SOLAR10 wrapper with evaluation/time tracking
│   ├── solar_mock.py          # Mock SOLAR10 function implementation
│   ├── algorithms.py          # Three CS variant implementations
│   ├── experiment_runner.py   # Experiment execution (500 evals)
│   ├── experiment_runner_2000.py  # Experiment execution (2000 evals)
│   ├── profiles.py            # Data profile computation
│   └── plots.py               # Plot generation
├── scripts/
│   ├── run_all.py                  # Main entry point - runs everything
│   ├── run_all_experiments.py      # Legacy: 500-eval only (use run_all.py instead)
│   ├── run_experiments_2000.py     # Legacy: 2000-eval only (use run_all.py instead)
│   ├── generate_tau_plots.py       # Legacy: plots only (use run_all.py instead)
│   └── regenerate_profiles_tau.py   # Legacy: CSV profiles only (use run_all.py instead)
├── results/                   # Output directory (created automatically)
│   └── plots/                 # Plot files (created automatically)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Understanding the Results

### Raw Data Files

**raw_runs.csv** (and **raw_runs_2000.csv**): Contains all individual run results with columns:
- `instance_id`: Problem instance identifier (0-29)
- `algo`: Algorithm name (Complete, Ordered, Opportunistic)
- `f0`: Initial function value at the starting point
- `final_f`: Final function value after optimization
- `evals`: Number of function evaluations used
- `cpu_time`: CPU time in seconds
- `success`: Boolean indicating if run succeeded (computed using success criterion)

### Data Profile Files

**data_profile_evals.csv**: Shows what fraction of problems each algorithm solved at different evaluation budgets. Columns:
- `evals`: Evaluation budget (x-axis)
- `Complete`: Fraction of problems solved by Complete CS at this budget
- `Ordered`: Fraction of problems solved by Ordered CS at this budget
- `Opportunistic`: Fraction of problems solved by Opportunistic CS at this budget

**data_profile_time.csv**: Same as above but using CPU time as the budget (x-axis is `cpu_time`).

### Plot Files

The PNG files in `results/plots/` visualize the data profiles. Each plot shows three curves (one per algorithm) showing how the fraction of solved problems increases as the budget (evaluations or time) increases. Higher curves indicate better performance.

## Success Criterion

A run is considered successful if:
```
f(x_final) - f* ≤ τ × (f0 - f*)
```
where:
- f* is the best-known value (minimum final_f across all runs)
- τ = 10⁻³ is the tolerance parameter
- f0 is the initial function value for that instance

## Reference

This project is part of the MATH462 course final project requirements.


