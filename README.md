# Coordinate Search Variants Benchmark on SOLAR10

**MATH462 Final Project**

This project benchmarks three Coordinate Search variants (Complete, Ordered, Opportunistic) on the SOLAR10 optimization problem.

## Getting Started

### Option 1: Clone from GitHub

**Mac / Linux:**
```bash
git clone https://github.com/AliasgarSakarwala/Math462-Coordinate-search-project.git
cd Math462-Coordinate-search-project
```

**Windows:**
```bash
git clone <https://github.com/AliasgarSakarwala/Math462-Coordinate-search-project.git
cd Math462-Coordinate-search-project
```

### Option 2: Download from GitHub

1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

### Project Structure

After cloning/downloading, your project should look like:
```
Math462-Coordinate-search-project/
├── experiments/          # Core implementation
│   ├── algorithms.py     # Three CS variants
│   ├── experiment_runner.py
│   ├── profiles.py       # Data profile computation
│   └── plots.py          # Plot generation
├── scripts/
│   └── run_all.py        # Main entry point
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

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

## How CSV Files Are Created

The CSV files are generated in `scripts/run_all.py`:

1. **Raw Data Collection** (`experiments/experiment_runner.py`):
   - Runs all three algorithms on 30 instances
   - Collects: `instance_id`, `algo`, `f0`, `final_f`, `evals`, `cpu_time`
   - Returns a pandas DataFrame with 90 rows (30 instances × 3 algorithms)

2. **Success Evaluation** (`experiments/profiles.py` - `compute_success()` function):
   - Computes best-known value: `f* = min(final_f)` across all runs
   - For each run, checks: `(final_f - f*) ≤ τ × (f0 - f*)`
   - Adds a `success` column (True/False) to the DataFrame
   - **Location in code:** `experiments/profiles.py`, lines 23-45

3. **Data Profile Creation** (`experiments/profiles.py`):
   - `build_data_profile_evals()`: Creates evaluation budget profile
   - `build_data_profile_time()`: Creates CPU time profile
   - For each budget, counts how many instances each algorithm solved

4. **CSV File Generation** (`scripts/run_all.py`):
   - Saves raw data: `df.to_csv('raw_runs.csv')` (line 105)
   - Saves profiles: `profile_evals.to_csv('data_profile_evals.csv')` (line 97)
   - Saves time profiles: `profile_time.to_csv('data_profile_time.csv')` (line 98)

## Success Criterion

A run succeeds if: `(final_f - f*) ≤ τ × (f0 - f*)`

**Where this is evaluated:**
- Function: `experiments/profiles.py` → `compute_success()` (lines 23-45)
- Called from: `scripts/run_all.py` (line 57 for initial computation, line 87 for each tau value)

**How it works:**
1. Find best solution: `f* = min(final_f)` across all runs
2. For each run, compute threshold: `threshold = τ × f0 + (1 - τ) × f*`
3. Check if: `final_f ≤ threshold`
4. If true, the run succeeded; otherwise it failed

where f* is the best-known value across all runs.
