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

### Step 1: Run the 500-Evaluation Experiment

Execute the main experiment script:

```bash
python scripts/run_all_experiments.py
```

**What this does:**
- Generates 30 random starting points in [-1, 1]¹⁰
- Runs all three CS variants (Complete, Ordered, Opportunistic) on each instance
- Computes the best-known objective value f* (minimum across all runs)
- Applies the success criterion to determine which runs succeeded
- Builds data profiles showing performance at different evaluation budgets
- Saves results to CSV files

**Expected output:**
```
============================================================
Coordinate Search Variants Benchmark on SOLAR10
============================================================

[1/5] Running experiments...
   Completed 90 runs across 30 instances

[2/5] Computing best-known value...
   f* = 4.205724e+01

[3/5] Computing success criterion...
   Overall success rate: 75.56%

[4/5] Building data profiles...
   Data profiles computed

[5/5] Saving results...
   Saved: results/raw_runs.csv
   Saved: results/data_profile_evals.csv
   Saved: results/data_profile_time.csv

[Summary statistics printed here]
```

**Files created:**
- `results/raw_runs.csv` - All 90 runs (30 instances × 3 algorithms) with their results
- `results/data_profile_evals.csv` - Data profile by evaluation budget (τ=1e-3)
- `results/data_profile_time.csv` - Data profile by CPU time (τ=1e-3)

### Step 2: Run the 2000-Evaluation Experiment (Optional)

For comparison, you can run the same experiment with a larger evaluation budget:

```bash
python scripts/run_experiments_2000.py
```

This does the same thing as Step 1 but with MAX_EVALS=2000 instead of 500.

**Files created:**
- `results/raw_runs_2000.csv`
- `results/data_profiles_eval_2000.csv`
- `results/data_profiles_time_2000.csv`

### Step 3: Generate Plots

Generate plots for different tolerance values (τ):

```bash
python scripts/generate_tau_plots.py
```

**What this does:**
- Reads the raw run data from Step 1 (and Step 2 if you ran it)
- Recomputes success criteria for τ = 1e-3, 1e-2, and 1e-1
- Generates data profile plots for each tolerance value
- Saves plots as PNG files

**Expected output:**
```
============================================================
Generating Data Profile Plots with Different Tau Values
============================================================

[Processing for each tau value and experiment]
  Saved: results/plots/data_profile_evals.png
  Saved: results/plots/data_profile_time.png
  [etc...]
```

**Files created:**
- `results/plots/data_profile_evals.png` - Evaluation profile (τ=1e-3)
- `results/plots/data_profile_time.png` - Time profile (τ=1e-3)
- `results/plots/data_profile_evals_tau1e-2.png` - Evaluation profile (τ=1e-2)
- `results/plots/data_profile_time_tau1e-2.png` - Time profile (τ=1e-2)
- `results/plots/data_profile_evals_tau1e-1.png` - Evaluation profile (τ=1e-1)
- `results/plots/data_profile_time_tau1e-1.png` - Time profile (τ=1e-1)
- Plus corresponding `_2000` versions if Step 2 was run

### Step 4: Generate Additional Data Profiles (Optional)

If you want CSV files for the other tolerance values:

```bash
python scripts/regenerate_profiles_tau.py
```

**What this does:**
- Recomputes success criteria for τ = 1e-2 and 1e-1
- Generates data profile CSV files for these tolerance values
- Does NOT generate plots (use Step 3 for that)

**Files created:**
- `results/data_profiles_eval_tau1e-2.csv`
- `results/data_profiles_time_tau1e-2.csv`
- `results/data_profiles_eval_tau1e-1.csv`
- `results/data_profiles_time_tau1e-1.csv`
- Plus `_2000` versions if Step 2 was run

### Complete File Structure After Running All Steps

After running all steps, your `results/` directory should contain:

```
results/
├── raw_runs.csv                          # 500-eval raw data
├── raw_runs_2000.csv                     # 2000-eval raw data (if Step 2 run)
├── data_profile_evals.csv                # 500-eval profile (τ=1e-3)
├── data_profile_time.csv                 # 500-eval time profile (τ=1e-3)
├── data_profiles_eval_tau1e-2.csv        # 500-eval profile (τ=1e-2)
├── data_profiles_eval_tau1e-1.csv        # 500-eval profile (τ=1e-1)
├── data_profiles_time_tau1e-2.csv        # 500-eval time profile (τ=1e-2)
├── data_profiles_time_tau1e-1.csv        # 500-eval time profile (τ=1e-1)
├── data_profiles_eval_2000.csv           # 2000-eval profile (τ=1e-3, if Step 2 run)
├── data_profiles_time_2000.csv           # 2000-eval time profile (τ=1e-3, if Step 2 run)
├── data_profiles_eval_2000_tau1e-2.csv   # 2000-eval profile (τ=1e-2, if Step 2 run)
├── data_profiles_eval_2000_tau1e-1.csv   # 2000-eval profile (τ=1e-1, if Step 2 run)
├── data_profiles_time_2000_tau1e-2.csv   # 2000-eval time profile (τ=1e-2, if Step 2 run)
└── data_profiles_time_2000_tau1e-1.csv   # 2000-eval time profile (τ=1e-1, if Step 2 run)
└── plots/
    ├── data_profile_evals.png            # 500-eval plot (τ=1e-3)
    ├── data_profile_time.png              # 500-eval time plot (τ=1e-3)
    ├── data_profile_evals_tau1e-2.png    # 500-eval plot (τ=1e-2)
    ├── data_profile_time_tau1e-2.png     # 500-eval time plot (τ=1e-2)
    ├── data_profile_evals_tau1e-1.png    # 500-eval plot (τ=1e-1)
    ├── data_profile_time_tau1e-1.png     # 500-eval time plot (τ=1e-1)
    ├── data_profile_evals_2000.png       # 2000-eval plot (τ=1e-3, if Step 2 run)
    ├── data_profile_time_2000.png        # 2000-eval time plot (τ=1e-3, if Step 2 run)
    ├── data_profile_evals_2000_tau1e-2.png  # 2000-eval plot (τ=1e-2, if Step 2 run)
    ├── data_profile_time_2000_tau1e-2.png   # 2000-eval time plot (τ=1e-2, if Step 2 run)
    ├── data_profile_evals_2000_tau1e-1.png  # 2000-eval plot (τ=1e-1, if Step 2 run)
    └── data_profile_time_2000_tau1e-1.png   # 2000-eval time plot (τ=1e-1, if Step 2 run)
```

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
│   ├── run_all_experiments.py      # Main entry point (500 evals)
│   ├── run_experiments_2000.py    # 2000-eval experiment
│   ├── generate_tau_plots.py      # Generate plots for different tau values
│   └── regenerate_profiles_tau.py  # Generate CSV profiles for different tau values
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


