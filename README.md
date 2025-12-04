# Coordinate Search Variants Benchmark on SOLAR10

**MATH462 Final Project**

This project benchmarks three Coordinate Search variants (Complete, Ordered, Opportunistic) on the SOLAR10 optimization problem.

## Installation

### Mac / Linux
```bash
pip3 install -r requirements.txt
```

### Windows
```bash
python -m pip install -r requirements.txt
```

**Dependencies:** numpy, pandas, matplotlib

## Running the Experiments

### Mac / Linux
```bash
python3 scripts/run_all.py
```

### Windows
```bash
python scripts/run_all.py
```

This single command:
- Runs 500-evaluation experiment (90 runs: 30 instances × 3 algorithms)
- Runs 2000-evaluation experiment (90 runs)
- Generates all data profiles and plots for τ = 1e-3, 1e-2, 1e-1

**Runtime:** ~2-5 minutes (depends on your computer)

## Results Organization

Results are organized into folders by experiment configuration:

```
results/
├── N500_tau1e-3/
│   ├── raw_runs.csv
│   ├── data_profile_evals.csv
│   ├── data_profile_time.csv
│   ├── data_profile_evals.png
│   └── data_profile_time.png
├── N500_tau1e-2/
│   ├── data_profiles_eval_tau1e-2.csv
│   ├── data_profiles_time_tau1e-2.csv
│   ├── data_profile_evals_tau1e-2.png
│   └── data_profile_time_tau1e-2.png
├── N500_tau1e-1/
│   └── [similar files]
├── N2000_tau1e-3/
│   └── [similar files]
├── N2000_tau1e-2/
│   └── [similar files]
└── N2000_tau1e-1/
    └── [similar files]
```

Each folder contains:
- **raw_runs.csv**: Individual run results (only in tau1e-3 folders)
- **data_profile_evals.csv**: Evaluation budget data profile
- **data_profile_time.csv**: CPU time data profile
- **data_profile_*.png**: Visualization plots

## Project Structure

```
.
├── experiments/          # Core implementation
│   ├── algorithms.py     # Three CS variants
│   ├── experiment_runner.py
│   ├── profiles.py       # Data profile computation
│   └── plots.py          # Plot generation
├── scripts/
│   └── run_all.py       # Main entry point
└── results/              # Output directory (auto-created)
```

## Experimental Configuration

- **Dimension**: 10
- **Instances**: 30
- **Domain**: [-1, 1]¹⁰
- **Step size**: Δ₀ = 1, reduction = 0.5, min = 10⁻⁴
- **Max evaluations**: 500 or 2000
- **Success tolerance**: τ = 1e-3, 1e-2, or 1e-1

## Success Criterion

A run succeeds if: `(final_f - f*) ≤ τ × (f0 - f*)`

where f* is the best-known value across all runs.
