"""Success criterion and data profile construction.

A data profile answers "what fraction of problems did this algorithm solve
within budget X", swept over a range of budgets (evaluations or CPU time).
It's the standard way to compare derivative-free solvers across a batch of
problem instances (Moré & Wild, 2009).
"""

import numpy as np
import pandas as pd

from .config import TAU, MAX_EVALS, MAX_CPU_TIME

ALGO_NAMES = ["Complete", "Ordered", "Opportunistic"]


def compute_best_known_value(df):
    """f* - the best objective value seen across every run in df."""
    return df["final_f"].min()


def compute_success(df, f_star, tau=None):
    """A run counts as a success once it gets within tau of the way from
    its starting value f0 down to the best known value f*:

        final_f - f* <= tau * (f0 - f*)

    which rearranges to the threshold used below.
    """
    if tau is None:
        tau = TAU
    threshold = tau * df["f0"] + (1 - tau) * f_star
    return df["final_f"] <= threshold


def _with_success(df, f_star, tau):
    out = df.copy()
    if "success" not in out.columns or tau is not None:
        out["success"] = compute_success(df, f_star, tau=tau)
    return out


def build_data_profile_evals(df, f_star, max_evals=None, eval_budget_step=1, tau=None):
    """Fraction of instances solved vs. evaluation budget, per algorithm."""
    if max_evals is None:
        max_evals = MAX_EVALS

    df = _with_success(df, f_star, tau)

    budgets = np.arange(1, max_evals + 1, eval_budget_step)
    if budgets[-1] != max_evals:
        budgets = np.append(budgets, max_evals)

    profile = {"evals": budgets}
    for algo in ALGO_NAMES:
        algo_df = df[df["algo"] == algo]
        total = algo_df["instance_id"].nunique()
        profile[algo] = [
            (algo_df[(algo_df["evals"] <= b) & algo_df["success"]]["instance_id"].nunique() / total)
            if total else 0.0
            for b in budgets
        ]

    return pd.DataFrame(profile)


def build_data_profile_time(df, f_star, tau=None):
    """Same idea as build_data_profile_evals, but swept over CPU time.

    Log-spaced budgets since run times span several orders of magnitude.
    """
    df = _with_success(df, f_star, tau)
    budgets = np.logspace(-3, np.log10(MAX_CPU_TIME), 100)

    profile = {"cpu_time": budgets}
    for algo in ALGO_NAMES:
        algo_df = df[df["algo"] == algo]
        total = algo_df["instance_id"].nunique()
        profile[algo] = [
            (algo_df[(algo_df["cpu_time"] <= b) & algo_df["success"]]["instance_id"].nunique() / total)
            if total else 0.0
            for b in budgets
        ]

    return pd.DataFrame(profile)
