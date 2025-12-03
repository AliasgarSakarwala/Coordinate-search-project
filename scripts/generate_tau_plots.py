#!/usr/bin/env python3
"""
Generate data profile plots with different tau (tolerance) values.
Reads existing raw_runs.csv files and generates plots for specified tau values.
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
from experiments.plots import (
    plot_data_profile_evals,
    plot_data_profile_time
)
from experiments.config import MAX_EVALS as MAX_EVALS_500, EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_500
from experiments.config_2000 import MAX_EVALS as MAX_EVALS_2000, EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_2000


def generate_tau_plots(raw_runs_path, max_evals, eval_budget_step, suffix, tau_values):
    """
    Generate plots for different tau values.
    
    Args:
        raw_runs_path: Path to raw_runs.csv file
        max_evals: Maximum evaluation budget
        eval_budget_step: Step size for evaluation budgets
        suffix: Suffix for output files (e.g., '', '_2000')
        tau_values: List of tau values to process
    """
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    plots_dir = os.path.join(results_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
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
        # For tau=1e-3 (original), use no suffix to match original naming
        if tau == 1e-3:
            tau_suffix = ""
        else:
            tau_suffix = f"tau{tau:.0e}".replace('e-0', 'e-').replace('e+0', 'e+')
        
        # Generate plots
        # Handle naming: if tau_suffix is empty (tau=1e-3), don't add underscore
        if tau_suffix:
            plot_evals_path = os.path.join(plots_dir, f'data_profile_evals{suffix}_{tau_suffix}.png')
            plot_time_path = os.path.join(plots_dir, f'data_profile_time{suffix}_{tau_suffix}.png')
        else:
            plot_evals_path = os.path.join(plots_dir, f'data_profile_evals{suffix}.png')
            plot_time_path = os.path.join(plots_dir, f'data_profile_time{suffix}.png')
        
        plot_data_profile_evals(profile_evals, plot_evals_path)
        plot_data_profile_time(profile_time, plot_time_path)
        print(f"  Saved: {plot_evals_path}")
        print(f"  Saved: {plot_time_path}")


def main():
    """Generate plots for both 500-eval and 2000-eval experiments with different tau values."""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    
    # Tau values to process
    tau_values = [1e-3, 1e-2, 1e-1]
    
    print("=" * 60)
    print("Generating Data Profile Plots with Different Tau Values")
    print("=" * 60)
    
    # Process 500-eval experiment
    raw_runs_500 = os.path.join(results_dir, 'raw_runs.csv')
    generate_tau_plots(
        raw_runs_500,
        max_evals=MAX_EVALS_500,
        eval_budget_step=EVAL_BUDGET_STEP_500,
        suffix='',
        tau_values=tau_values
    )
    
    # Process 2000-eval experiment
    raw_runs_2000 = os.path.join(results_dir, 'raw_runs_2000.csv')
    generate_tau_plots(
        raw_runs_2000,
        max_evals=MAX_EVALS_2000,
        eval_budget_step=EVAL_BUDGET_STEP_2000,
        suffix='_2000',
        tau_values=tau_values
    )
    
    print("\n" + "=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()

