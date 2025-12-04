# Coordinate Search Variants Benchmark on SOLAR10

**MATH462 Final Project**

This project benchmarks three Coordinate Search variants (Complete, Ordered, Opportunistic) on the SOLAR10 optimization problem.

## Getting Started

### Option 1: Clone from GitHub

In your terminal, run:

**Mac / Linux:**
```bash
git clone https://github.com/AliasgarSakarwala/Math462-Coordinate-search-project.git
cd Math462-Coordinate-search-project
```

**Windows:**
```bash
git clone https://github.com/AliasgarSakarwala/Math462-Coordinate-search-project.git
cd Math462-Coordinate-search-project
```

### Option 2: Download from GitHub

1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. In your terminal, navigate to the extracted folder:
   ```bash
   cd Math462-Coordinate-search-project
   ```

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

In your terminal, navigate to the project directory and install dependencies:

### Mac / Linux
```bash
cd Math462-Coordinate-search-project
pip3 install -r requirements.txt
```

### Windows
```bash
cd Math462-Coordinate-search-project
python -m pip install -r requirements.txt
```

**Dependencies:** numpy, pandas, matplotlib

## Running the Experiments

In your terminal, run the main script:

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

You should see progress messages as the experiments run, and the script will print a summary when complete.

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

## Viewing Results

In your terminal, you can view the generated files using the following commands:

### View CSV Files

**Mac / Linux:**
```bash
# View raw runs data (500 evaluations, tau=1e-3)
cat results/N500_tau1e-3/raw_runs.csv | head -20

# View evaluation data profile (500 evaluations, tau=1e-3)
cat results/N500_tau1e-3/data_profile_evals.csv | head -20

# View CPU time data profile (500 evaluations, tau=1e-3)
cat results/N500_tau1e-3/data_profile_time.csv | head -20

# View raw runs data (2000 evaluations, tau=1e-3)
cat results/N2000_tau1e-3/raw_runs.csv | head -20

# View evaluation data profile (2000 evaluations, tau=1e-3)
cat results/N2000_tau1e-3/data_profile_evals.csv | head -20

# View CPU time data profile (2000 evaluations, tau=1e-3)
cat results/N2000_tau1e-3/data_profile_time.csv | head -20

# View other tau values (example for tau=1e-2, 500 evaluations)
cat results/N500_tau1e-2/data_profile_evals.csv | head -20
cat results/N500_tau1e-2/data_profile_time.csv | head -20

# View tau=1e-1 (500 evaluations)
cat results/N500_tau1e-1/data_profile_evals.csv | head -20
cat results/N500_tau1e-1/data_profile_time.csv | head -20
```

**Windows:**
```bash
# View raw runs data (500 evaluations, tau=1e-3)
type results\N500_tau1e-3\raw_runs.csv | more

# View evaluation data profile (500 evaluations, tau=1e-3)
type results\N500_tau1e-3\data_profile_evals.csv | more

# View CPU time data profile (500 evaluations, tau=1e-3)
type results\N500_tau1e-3\data_profile_time.csv | more

# View raw runs data (2000 evaluations, tau=1e-3)
type results\N2000_tau1e-3\raw_runs.csv | more

# View evaluation data profile (2000 evaluations, tau=1e-3)
type results\N2000_tau1e-3\data_profile_evals.csv | more

# View CPU time data profile (2000 evaluations, tau=1e-3)
type results\N2000_tau1e-3\data_profile_time.csv | more
```

### Open Plot Images

**Mac / Linux:**
```bash
# Open evaluation profile plots
open results/N500_tau1e-3/data_profile_evals.png
open results/N500_tau1e-3/data_profile_time.png
open results/N2000_tau1e-3/data_profile_evals.png
open results/N2000_tau1e-3/data_profile_time.png

# Open plots for other tau values
open results/N500_tau1e-2/data_profile_evals.png
open results/N500_tau1e-2/data_profile_time.png
open results/N500_tau1e-1/data_profile_evals.png
open results/N500_tau1e-1/data_profile_time.png
open results/N2000_tau1e-2/data_profile_evals.png
open results/N2000_tau1e-2/data_profile_time.png
open results/N2000_tau1e-1/data_profile_evals.png
open results/N2000_tau1e-1/data_profile_time.png
```

**Windows:**
```bash
# Open evaluation profile plots
start results\N500_tau1e-3\data_profile_evals.png
start results\N500_tau1e-3\data_profile_time.png
start results\N2000_tau1e-3\data_profile_evals.png
start results\N2000_tau1e-3\data_profile_time.png

# Open plots for other tau values
start results\N500_tau1e-2\data_profile_evals.png
start results\N500_tau1e-2\data_profile_time.png
start results\N500_tau1e-1\data_profile_evals.png
start results\N500_tau1e-1\data_profile_time.png
start results\N2000_tau1e-2\data_profile_evals.png
start results\N2000_tau1e-2\data_profile_time.png
start results\N2000_tau1e-1\data_profile_evals.png
start results\N2000_tau1e-1\data_profile_time.png
```

### List All Results Folders

**Mac / Linux:**
```bash
ls -la results/
```

**Windows:**
```bash
dir results
```

### Navigate to Results Folder

**Mac / Linux:**
```bash
cd results
ls -la
```

**Windows:**
```bash
cd results
dir
```

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
