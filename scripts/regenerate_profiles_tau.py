#!/usr/bin/env python3
"""
Regenerate data profiles and plots with different tau (tolerance) values.
Reads existing raw_runs.csv files and recomputes success criteria.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path to import experiments package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.profiles import (
    compute_best_known_value,
    compute_success,
    build_data_profile_evals,
    build_data_profile_time
)
from experiments.config import MAX_EVALS as MAX_EVALS_500, EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_500
from experiments.config_2000 import MAX_EVALS as MAX_EVALS_2000, EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_2000, MAX_CPU_TIME


def process_experiment(raw_runs_path, max_evals, eval_budget_step, suffix, tau_values):
    """
    Process an experiment with different tau values.
    
    Args:
        raw_runs_path: Path to raw_runs.csv file
        max_evals: Maximum evaluation budget
        eval_budget_step: Step size for evaluation budgets
        suffix: Suffix for output files (e.g., '', '_2000')
        tau_values: List of tau values to process
    """
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    
    print(f"\n{'='*60}")
    print(f"Processing experiment: {raw_runs_path}")
    print(f"{'='*60}")
    
    # Read raw runs
    if not os.path.exists(raw_runs_path):
        print(f"Warning: {raw_runs_path} not found, skipping...")
        return
    
    df = pd.read_csv(raw_runs_path)
    print(f"Loaded {len(df)} runs from {raw_runs_path}")
    
    # Compute best-known value (same for all tau values)
    f_star = compute_best_known_value(df)
    print(f"Best-known value (f*): {f_star:.6e}")
    
    # Process each tau value
    for tau in tau_values:
        print(f"\n--- Processing tau = {tau:.0e} ---")
        
        # Recompute success with new tau using the function
        df_copy = df.copy()
        df_copy['success'] = compute_success(df_copy, f_star, tau=tau)
        
        success_rate = df_copy['success'].mean()
        print(f"Overall success rate: {success_rate:.2%}")
        
        # Print success counts per algorithm
        success_counts = df_copy.groupby('algo')['success'].sum()
        for algo in ['Complete', 'Ordered', 'Opportunistic']:
            count = success_counts.get(algo, 0)
            print(f"  {algo:15s}: {count}/30 ({count/30*100:.2f}%)")
        
        # Build data profiles (pass tau to ensure correct computation)
        profile_evals = build_data_profile_evals(df_copy, f_star, max_evals=max_evals, eval_budget_step=eval_budget_step, tau=tau)
        profile_time = build_data_profile_time(df_copy, f_star, tau=tau)
        
        # Create tau suffix for filenames
        tau_suffix = f"tau{tau:.0e}".replace('e-0', 'e-').replace('e+0', 'e+')
        
        # Save data profiles
        profile_evals_path = os.path.join(results_dir, f'data_profiles_eval{suffix}_{tau_suffix}.csv')
        profile_time_path = os.path.join(results_dir, f'data_profiles_time{suffix}_{tau_suffix}.csv')
        profile_evals.to_csv(profile_evals_path, index=False)
        profile_time.to_csv(profile_time_path, index=False)
        print(f"  Saved: {profile_evals_path}")
        print(f"  Saved: {profile_time_path}")


def main():
    """Process both 500-eval and 2000-eval experiments with different tau values."""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    
    # Tau values to process (only non-default tau values)
    tau_values = [1e-2, 1e-1]
    
    print("=" * 60)
    print("Regenerating Data Profiles with Different Tau Values")
    print("=" * 60)
    
    # Process 500-eval experiment
    raw_runs_500 = os.path.join(results_dir, 'raw_runs.csv')
    process_experiment(
        raw_runs_500,
        max_evals=MAX_EVALS_500,
        eval_budget_step=EVAL_BUDGET_STEP_500,
        suffix='',
        tau_values=tau_values
    )
    
    # Process 2000-eval experiment
    raw_runs_2000 = os.path.join(results_dir, 'raw_runs_2000.csv')
    process_experiment(
        raw_runs_2000,
        max_evals=MAX_EVALS_2000,
        eval_budget_step=EVAL_BUDGET_STEP_2000,
        suffix='_2000',
        tau_values=tau_values
    )
    
    print("\n" + "=" * 60)
    print("All profiles regenerated successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()

