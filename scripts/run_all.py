#!/usr/bin/env python3
"""
Main script to run all experiments and generate all outputs.

This single script:
1. Runs 500-evaluation experiment
2. Runs 2000-evaluation experiment  
3. Generates all data profiles (CSV files) for all tau values
4. Generates all plots for all tau values

Just run: python scripts/run_all.py
"""

import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.experiment_runner import run_experiments
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
from experiments.config import MAX_EVALS as MAX_EVALS_500, EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_500, TAU as DEFAULT_TAU

# 2000-eval experiment settings
MAX_EVALS_2000 = 2000
EVAL_BUDGET_STEP_2000 = 20


def run_single_experiment(run_experiments_func, max_evals, eval_budget_step, suffix, results_dir):
    """
    Run a single experiment (either 500 or 2000 evals) and save the raw data.
    
    Returns the DataFrame with results.
    """
    print(f"\n{'='*60}")
    print(f"Running {max_evals}-evaluation experiment")
    print(f"{'='*60}")
    
    # Run the experiments
    print(f"\n[1/3] Running experiments (MAX_EVALS = {max_evals})...")
    df = run_experiments_func()
    print(f"   Completed {len(df)} runs across {df['instance_id'].nunique()} instances")
    
    # Compute f* and success
    print(f"\n[2/3] Computing best-known value and success criterion...")
    f_star = compute_best_known_value(df)
    df['success'] = compute_success(df, f_star)
    print(f"   f* = {f_star:.6e}")
    print(f"   Overall success rate: {df['success'].mean():.2%}")
    
    # Note: Raw data will be saved in the tau=1e-3 folder later
    print(f"\n[3/3] Experiment complete")
    
    return df, f_star


def generate_profiles_and_plots(df, f_star, max_evals, eval_budget_step, suffix, results_dir, tau_values):
    """
    Generate all CSV profiles and plots for a given experiment.
    
    Results are organized into folders: N{max_evals}_tau{tau}
    """
    print(f"\n{'='*60}")
    print(f"Generating profiles and plots for {max_evals}-eval experiment")
    print(f"{'='*60}")
    
    for tau in tau_values:
        print(f"\n--- Processing tau = {tau:.0e} ---")
        
        # Create folder for this experiment configuration
        tau_str = f"tau{tau:.0e}".replace('e-0', 'e-').replace('e+0', 'e+')
        exp_folder = os.path.join(results_dir, f'N{max_evals}_{tau_str}')
        os.makedirs(exp_folder, exist_ok=True)
        
        # Recompute success with this tau
        df_copy = df.copy()
        df_copy['success'] = compute_success(df_copy, f_star, tau=tau)
        
        # Build data profiles
        profile_evals = build_data_profile_evals(df_copy, f_star, max_evals=max_evals, 
                                                 eval_budget_step=eval_budget_step, tau=tau)
        profile_time = build_data_profile_time(df_copy, f_star, tau=tau)
        
        # Save CSV profiles
        profile_evals_path = os.path.join(exp_folder, 'data_profile_evals.csv')
        profile_time_path = os.path.join(exp_folder, 'data_profile_time.csv')
        profile_evals.to_csv(profile_evals_path, index=False)
        profile_time.to_csv(profile_time_path, index=False)
        print(f"  Saved CSV: {profile_evals_path}")
        print(f"  Saved CSV: {profile_time_path}")
        
        # Save raw data only for tau=1e-3 (to avoid duplication)
        if tau == DEFAULT_TAU:
            raw_runs_path = os.path.join(exp_folder, 'raw_runs.csv')
            df_copy.to_csv(raw_runs_path, index=False)
            print(f"  Saved CSV: {raw_runs_path}")
        
        # Generate plots
        plot_evals_path = os.path.join(exp_folder, 'data_profile_evals.png')
        plot_time_path = os.path.join(exp_folder, 'data_profile_time.png')
        plot_data_profile_evals(profile_evals, plot_evals_path)
        plot_data_profile_time(profile_time, plot_time_path)
        print(f"  Saved plot: {plot_evals_path}")
        print(f"  Saved plot: {plot_time_path}")


def main():
    """
    Main function that runs everything.
    
    This does:
    1. Run 500-eval experiment
    2. Run 2000-eval experiment
    3. Generate all profiles and plots for both experiments
    """
    print("=" * 60)
    print("Coordinate Search Variants Benchmark - Complete Pipeline")
    print("=" * 60)
    
    # Set up directories
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Tau values to process
    tau_values = [1e-3, 1e-2, 1e-1]
    
    # Step 1: Run 500-eval experiment
    df_500, f_star_500 = run_single_experiment(
        lambda: run_experiments(max_evals=MAX_EVALS_500), 
        MAX_EVALS_500, EVAL_BUDGET_STEP_500, '', results_dir
    )
    
    # Step 2: Run 2000-eval experiment
    df_2000, f_star_2000 = run_single_experiment(
        lambda: run_experiments(max_evals=MAX_EVALS_2000),
        MAX_EVALS_2000, EVAL_BUDGET_STEP_2000, '_2000', results_dir
    )
    
    # Step 3: Generate all profiles and plots for 500-eval
    generate_profiles_and_plots(
        df_500, f_star_500, MAX_EVALS_500, EVAL_BUDGET_STEP_500, 
        '', results_dir, tau_values
    )
    
    # Step 4: Generate all profiles and plots for 2000-eval
    generate_profiles_and_plots(
        df_2000, f_star_2000, MAX_EVALS_2000, EVAL_BUDGET_STEP_2000,
        '_2000', results_dir, tau_values
    )
    
    # Final summary
    print("\n" + "=" * 60)
    print("All experiments completed successfully!")
    print("=" * 60)
    print(f"\nResults organized in: {results_dir}")
    print(f"\nGenerated folders:")
    for max_evals in [MAX_EVALS_500, MAX_EVALS_2000]:
        for tau in tau_values:
            tau_str = f"tau{tau:.0e}".replace('e-0', 'e-').replace('e+0', 'e+')
            print(f"  - N{max_evals}_{tau_str}/")
    print("=" * 60)


if __name__ == '__main__':
    main()

