#!/usr/bin/env python3
"""Entry point for the whole benchmark: runs the experiments across the
full problem suite, builds the data profiles + plots, for both the
500-eval and 2000-eval budgets.

    python3 scripts/run_all.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.config import EVAL_BUDGET_STEP as EVAL_BUDGET_STEP_500
from experiments.config import MAX_EVALS as MAX_EVALS_500
from experiments.config import TAU as DEFAULT_TAU
from experiments.experiment_runner import run_experiments
from experiments.plots import plot_data_profile_evals, plot_data_profile_time
from experiments.profiles import (
    build_data_profile_evals,
    build_data_profile_time,
    compute_star_per_problem,
    compute_success,
)

MAX_EVALS_2000 = 2000
EVAL_BUDGET_STEP_2000 = 20

TAU_VALUES = [1e-3, 1e-2, 1e-1]


def run_single_experiment(max_evals):
    print(f"\n{'=' * 60}\nRunning {max_evals}-evaluation experiment\n{'=' * 60}")

    print(f"\n[1/2] Running experiments (MAX_EVALS = {max_evals})...")
    df = run_experiments(max_evals=max_evals)
    print(f"   completed {len(df)} runs across {df['instance_id'].nunique()} instances "
          f"({df['problem'].nunique()} problems)")

    print("\n[2/2] Computing best-known values and success criterion...")
    f_star_by_problem = compute_star_per_problem(df)
    df["success"] = compute_success(df, f_star_by_problem)
    print(f"   overall success rate: {df['success'].mean():.2%}")

    return df, f_star_by_problem


def generate_profiles_and_plots(df, f_star_by_problem, max_evals, eval_budget_step, results_dir):
    print(f"\n{'=' * 60}\nGenerating profiles and plots for {max_evals}-eval experiment\n{'=' * 60}")

    for tau in TAU_VALUES:
        print(f"\n--- tau = {tau:.0e} ---")

        tau_str = f"tau{tau:.0e}".replace("e-0", "e-").replace("e+0", "e+")
        exp_folder = os.path.join(results_dir, f"N{max_evals}_{tau_str}")
        os.makedirs(exp_folder, exist_ok=True)

        df_tau = df.copy()
        df_tau["success"] = compute_success(df_tau, f_star_by_problem, tau=tau)

        profile_evals = build_data_profile_evals(
            df_tau, f_star_by_problem, max_evals=max_evals, eval_budget_step=eval_budget_step, tau=tau
        )
        profile_time = build_data_profile_time(df_tau, f_star_by_problem, tau=tau)

        profile_evals.to_csv(os.path.join(exp_folder, "data_profile_evals.csv"), index=False)
        profile_time.to_csv(os.path.join(exp_folder, "data_profile_time.csv"), index=False)

        # raw data is the same across tau values, so only write it once
        if tau == DEFAULT_TAU:
            df_tau.to_csv(os.path.join(exp_folder, "raw_runs.csv"), index=False)

        plot_data_profile_evals(profile_evals, os.path.join(exp_folder, "data_profile_evals.png"))
        plot_data_profile_time(profile_time, os.path.join(exp_folder, "data_profile_time.png"))
        print(f"   saved results to {exp_folder}")


def main():
    print("=" * 60)
    print("Coordinate Search / MADS Benchmark - Full Pipeline")
    print("=" * 60)

    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)

    df_500, f_star_500 = run_single_experiment(MAX_EVALS_500)
    df_2000, f_star_2000 = run_single_experiment(MAX_EVALS_2000)

    generate_profiles_and_plots(df_500, f_star_500, MAX_EVALS_500, EVAL_BUDGET_STEP_500, results_dir)
    generate_profiles_and_plots(df_2000, f_star_2000, MAX_EVALS_2000, EVAL_BUDGET_STEP_2000, results_dir)

    print("\n" + "=" * 60)
    print(f"Done. Results are in: {results_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
