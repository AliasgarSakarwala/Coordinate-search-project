"""Success criterion and data profile construction.

A data profile answers "what fraction of problems did this algorithm solve
within budget X", swept over a range of budgets (evaluations or CPU time).
It's the standard way to compare derivative-free solvers across a batch of
problem instances (Moré & Wild, 2009).

Now that the suite has several different problems in it (not 30 restarts
of the same function), f* has to be computed per problem rather than once
globally - see compute_star_per_problem below.
"""

import numpy as np
import pandas as pd

from .config import TAU, MAX_CPU_TIME

ALGO_NAMES = ["Complete", "Ordered", "Opportunistic", "MADS"]


def compute_star_per_problem(df):
    """Best-known objective value for each problem in df.

    Uses the analytic global minimum when we have one (the classic test
    functions), otherwise falls back to the best final_f any solver found
    for that problem.
    """
    empirical = df.groupby("problem")["final_f"].min()
    known = df.groupby("problem")["known_min"].first()
    return known.where(known.notna(), empirical)


def compute_success(df, f_star_by_problem=None, tau=None):
    """A run counts as a success once it gets within tau of the way from
    its starting value f0 down to that problem's best known value f*:

        final_f - f* <= tau * (f0 - f*)

    which rearranges to the threshold used below.
    """
    if tau is None:
        tau = TAU
    if f_star_by_problem is None:
        f_star_by_problem = compute_star_per_problem(df)

    f_star = df["problem"].map(f_star_by_problem)
    threshold = tau * df["f0"] + (1 - tau) * f_star
    return df["final_f"] <= threshold


def _with_success(df, f_star_by_problem, tau):
    out = df.copy()
    if "success" not in out.columns or tau is not None:
        out["success"] = compute_success(df, f_star_by_problem, tau=tau)
    return out


def build_data_profile_evals(df, f_star_by_problem, max_evals, eval_budget_step=1, tau=None):
    """Fraction of the 35 problem instances solved vs. evaluation budget,
    one curve per algorithm.
    """
    df = _with_success(df, f_star_by_problem, tau)

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


def build_data_profile_time(df, f_star_by_problem, tau=None):
    """Same idea as build_data_profile_evals, but swept over CPU time.

    Log-spaced budgets since run times span several orders of magnitude.
    """
    df = _with_success(df, f_star_by_problem, tau)
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
