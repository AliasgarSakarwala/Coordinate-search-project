"""
Functions for computing success criteria and building data profiles.

Data profiles show what fraction of problems each algorithm solved
at different budgets (either evaluation count or CPU time).
"""

import numpy as np
import pandas as pd
from .config import TAU, MAX_EVALS, MAX_CPU_TIME


def compute_best_known_value(df):
    """
    Find the best solution we found across all runs.
    
    This is just the minimum final_f value. We use this as f* in
    the success criterion.
    """
    return df['final_f'].min()


def compute_success(df, f_star, tau=None):
    """
    Figure out which runs succeeded.
    
    A run succeeds if: (final_f - f*) <= tau * (f0 - f*)
    
    This means we got close enough to the best solution relative to
    where we started. If tau is small (like 1e-3), we need to get
    very close. If tau is larger, we're more lenient.
    
    We rearrange this to: final_f <= tau * f0 + (1 - tau) * f*
    which is easier to compute.
    """
    if tau is None:
        tau = TAU
    
    # Compute the threshold - if final_f is below this, we succeeded
    threshold = tau * df['f0'] + (1 - tau) * f_star
    
    # Check which runs succeeded
    success = df['final_f'] <= threshold
    
    return success


def build_data_profile_evals(df, f_star, max_evals=None, eval_budget_step=1, tau=None):
    """
    Build a data profile showing how many problems each algorithm solved
    at different evaluation budgets.
    
    For each budget (like 100, 200, 300 evaluations), we check how many
    instances each algorithm solved using that many or fewer evaluations.
    This gives us a curve showing performance vs. evaluation count.
    """
    if max_evals is None:
        max_evals = MAX_EVALS
    
    # Make sure we have success information
    df_with_success = df.copy()
    if 'success' not in df_with_success.columns or tau is not None:
        df_with_success['success'] = compute_success(df, f_star, tau=tau)
    
    # Create the list of budgets to check
    # For 500 evals with step 5, we check: 1, 6, 11, 16, ..., 500
    eval_budgets = np.arange(1, max_evals + 1, eval_budget_step)
    # Make sure we include the max (might not be in the range)
    if eval_budgets[-1] != max_evals:
        eval_budgets = np.append(eval_budgets, max_evals)
    
    profile_data = {'evals': eval_budgets}
    
    # For each algorithm, compute the fraction solved at each budget
    for algo in ['Complete', 'Ordered', 'Opportunistic']:
        algo_df = df_with_success[df_with_success['algo'] == algo]
        
        fractions = []
        for budget in eval_budgets:
            # Count how many instances this algorithm solved with <= budget evals
            solved = algo_df[
                (algo_df['evals'] <= budget) & (algo_df['success'])
            ]['instance_id'].nunique()
            total_instances = algo_df['instance_id'].nunique()
            fraction = solved / total_instances if total_instances > 0 else 0.0
            fractions.append(fraction)
        
        profile_data[algo] = fractions
    
    return pd.DataFrame(profile_data)


def build_data_profile_time(df, f_star, tau=None):
    """
    Build a data profile showing how many problems each algorithm solved
    at different CPU time budgets.
    
    Same idea as the evaluation profile, but using CPU time instead.
    We use logarithmic spacing for the time budgets since times can vary
    a lot (milliseconds to seconds).
    """
    # Make sure we have success information
    df_with_success = df.copy()
    if 'success' not in df_with_success.columns or tau is not None:
        df_with_success['success'] = compute_success(df, f_star, tau=tau)
    
    # Create time budgets from 0.001 seconds to MAX_CPU_TIME
    # Using log spacing gives us more points at small times where things change fast
    time_budgets = np.logspace(-3, np.log10(MAX_CPU_TIME), 100)
    
    profile_data = {'cpu_time': time_budgets}
    
    # For each algorithm, compute the fraction solved at each time budget
    for algo in ['Complete', 'Ordered', 'Opportunistic']:
        algo_df = df_with_success[df_with_success['algo'] == algo]
        
        fractions = []
        for budget in time_budgets:
            # Count how many instances this algorithm solved within this time
            solved = algo_df[
                (algo_df['cpu_time'] <= budget) & (algo_df['success'])
            ]['instance_id'].nunique()
            total_instances = algo_df['instance_id'].nunique()
            fraction = solved / total_instances if total_instances > 0 else 0.0
            fractions.append(fraction)
        
        profile_data[algo] = fractions
    
    return pd.DataFrame(profile_data)


