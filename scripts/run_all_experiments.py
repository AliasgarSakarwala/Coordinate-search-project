#!/usr/bin/env python3
"""
Main script to run the 500-evaluation experiment.

This script runs all three coordinate search algorithms on 30 problem instances,
then computes data profiles and saves everything to CSV files.
Plots are generated separately using generate_tau_plots.py.
"""

import sys
import os
import pandas as pd

# Need to add the project root to the path so we can import our experiments package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.experiment_runner import run_experiments
from experiments.profiles import (
    compute_best_known_value,
    compute_success,
    build_data_profile_evals,
    build_data_profile_time
)
from experiments.config import MAX_EVALS, EVAL_BUDGET_STEP


def main():
    """
    Main function that runs the whole experiment pipeline.
    
    The process is:
    1. Run all algorithms on all instances (this takes a while)
    2. Find the best solution we found (f*)
    3. Figure out which runs succeeded based on the success criterion
    4. Build data profiles showing how many problems each algorithm solved
    5. Save everything to CSV files
    """
    print("=" * 60)
    print("Coordinate Search Variants Benchmark on SOLAR10")
    print("=" * 60)
    
    # Make sure the results folder exists
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Step 1: Actually run the experiments
    # This calls all three algorithms on 30 instances, so we get 90 runs total
    print("\n[1/5] Running experiments...")
    df = run_experiments()
    print(f"   Completed {len(df)} runs across {df['instance_id'].nunique()} instances")
    
    # Step 2: Find the best solution across all runs
    # This is f* - the minimum final_f value we found
    print("\n[2/5] Computing best-known value...")
    f_star = compute_best_known_value(df)
    print(f"   f* = {f_star:.6e}")
    
    # Step 3: Check which runs succeeded
    # A run succeeds if: (final_f - f*) <= tau * (f0 - f*)
    # This tells us how close we got relative to where we started
    print("\n[3/5] Computing success criterion...")
    df['success'] = compute_success(df, f_star)
    success_rate = df['success'].mean()
    print(f"   Overall success rate: {success_rate:.2%}")
    
    # Step 4: Build the data profiles
    # These show what fraction of problems each algorithm solved at different budgets
    # One profile uses evaluation count, the other uses CPU time
    print("\n[4/5] Building data profiles...")
    profile_evals = build_data_profile_evals(df, f_star, max_evals=MAX_EVALS, eval_budget_step=EVAL_BUDGET_STEP)
    profile_time = build_data_profile_time(df, f_star)
    print("   Data profiles computed")
    
    # Step 5: Save everything to CSV files
    print("\n[5/5] Saving results...")
    
    # Save the raw data - all 90 runs with their results
    raw_runs_path = os.path.join(results_dir, 'raw_runs.csv')
    df.to_csv(raw_runs_path, index=False)
    print(f"   Saved: {raw_runs_path}")
    
    # Save the data profiles - these are what we use to make the plots
    profile_evals_path = os.path.join(results_dir, 'data_profile_evals.csv')
    profile_time_path = os.path.join(results_dir, 'data_profile_time.csv')
    profile_evals.to_csv(profile_evals_path, index=False)
    profile_time.to_csv(profile_time_path, index=False)
    print(f"   Saved: {profile_evals_path}")
    print(f"   Saved: {profile_time_path}")
    
    # Print some summary stats so we can see how things went
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(f"\nBest-known value (f*): {f_star:.6e}")
    
    # Show success rates for each algorithm
    print(f"\nSuccess rates by algorithm:")
    for algo in ['Complete', 'Ordered', 'Opportunistic']:
        algo_df = df[df['algo'] == algo]
        algo_success = algo_df['success'].mean()
        print(f"  {algo:15s}: {algo_success:.2%}")
    
    # Show how many evaluations each algorithm used on average
    print(f"\nAverage evaluations by algorithm:")
    for algo in ['Complete', 'Ordered', 'Opportunistic']:
        algo_df = df[df['algo'] == algo]
        avg_evals = algo_df['evals'].mean()
        print(f"  {algo:15s}: {avg_evals:.1f}")
    
    # Show CPU time for each algorithm
    print(f"\nAverage CPU time by algorithm:")
    for algo in ['Complete', 'Ordered', 'Opportunistic']:
        algo_df = df[df['algo'] == algo]
        avg_time = algo_df['cpu_time'].mean()
        print(f"  {algo:15s}: {avg_time:.4f} seconds")
    
    print("\n" + "=" * 60)
    print("All results saved to:", results_dir)
    print("=" * 60)


if __name__ == '__main__':
    main()


