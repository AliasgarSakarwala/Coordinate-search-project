"""
This module handles running all the experiments.

We generate 30 random starting points, then run all three algorithms
on each one. That gives us 90 runs total (30 instances × 3 algorithms).

Can run with different max_evals values (500 or 2000) by passing a parameter.
"""

import numpy as np
import pandas as pd
from .config import (
    DIM, N_INSTANCES, DOMAIN_LOW, DOMAIN_HIGH,
    GLOBAL_SEED, INSTANCE_SEED_OFFSET, MAX_EVALS as DEFAULT_MAX_EVALS,
    MAX_CPU_TIME as DEFAULT_MAX_CPU_TIME, EVAL_BUDGET_STEP as DEFAULT_EVAL_BUDGET_STEP
)
from .solar_wrapper import SolarWrapper
# Import algorithms module so we can temporarily override MAX_EVALS if needed
import experiments.algorithms as algo_module
from .algorithms import (
    complete_coordinate_search,
    ordered_coordinate_search,
    opportunistic_coordinate_search
)


def generate_starting_points():
    """
    Generate 30 random starting points in [-1, 1]^10.
    
    We use a fixed seed so we always get the same 30 points.
    This makes experiments reproducible.
    """
    np.random.seed(GLOBAL_SEED)
    starting_points = np.random.uniform(
        low=DOMAIN_LOW,
        high=DOMAIN_HIGH,
        size=(N_INSTANCES, DIM)
    )
    return starting_points


def run_experiments(max_evals=None, eval_budget_step=None):
    """
    Run all three algorithms on all 30 instances.
    
    For each instance:
    1. Get the starting point
    2. Run Complete CS
    3. Run Ordered CS
    4. Run Opportunistic CS
    
    We reset the random seed before each algorithm so they all start
    with the same RNG state. This makes the comparison fair.
    
    Args:
        max_evals: Maximum evaluations (defaults to config.MAX_EVALS)
        eval_budget_step: Step size for evaluation budgets (defaults to config.EVAL_BUDGET_STEP)
    
    Returns a DataFrame with all the results.
    """
    # If max_evals is different from default, temporarily override it in algorithms module
    if max_evals is None:
        max_evals = DEFAULT_MAX_EVALS
    
    # Temporarily override MAX_EVALS in algorithms if needed
    old_max_evals = None
    if max_evals != DEFAULT_MAX_EVALS:
        old_max_evals = algo_module.MAX_EVALS
        algo_module.MAX_EVALS = max_evals
    # Generate all starting points at once
    starting_points = generate_starting_points()
    
    results = []
    
    # Loop through each of the 30 instances
    for instance_id in range(N_INSTANCES):
        x0 = starting_points[instance_id]
        
        # Each instance gets its own seed based on its ID
        # This ensures reproducibility while allowing variation between instances
        instance_seed = instance_id + INSTANCE_SEED_OFFSET
        
        # Set the seed for this instance
        # We'll reset it before each algorithm so they all start the same
        np.random.seed(instance_seed)
        
        # Create a wrapper to track evaluations for this instance
        func_wrapper = SolarWrapper(instance_id)
        
        # Evaluate the starting point - this is f0
        f0 = func_wrapper.evaluate(x0)
        
        # Run Complete Coordinate Search
        # Reset seed and wrapper so this algorithm starts fresh
        np.random.seed(instance_seed)
        func_wrapper.reset()
        final_x_cs, final_f_cs, evals_cs, cpu_time_cs = complete_coordinate_search(
            func_wrapper, x0
        )
        results.append({
            'instance_id': instance_id,
            'algo': 'Complete',
            'f0': f0,
            'final_f': final_f_cs,
            'evals': evals_cs,
            'cpu_time': cpu_time_cs
        })
        
        # Run Ordered Coordinate Search
        # Reset everything again so it's a fair comparison
        np.random.seed(instance_seed)
        func_wrapper.reset()
        final_x_ocs, final_f_ocs, evals_ocs, cpu_time_ocs = ordered_coordinate_search(
            func_wrapper, x0
        )
        results.append({
            'instance_id': instance_id,
            'algo': 'Ordered',
            'f0': f0,
            'final_f': final_f_ocs,
            'evals': evals_ocs,
            'cpu_time': cpu_time_ocs
        })
        
        # Run Opportunistic Coordinate Search
        # Same reset process
        np.random.seed(instance_seed)
        func_wrapper.reset()
        final_x_opcs, final_f_opcs, evals_opcs, cpu_time_opcs = opportunistic_coordinate_search(
            func_wrapper, x0
        )
        results.append({
            'instance_id': instance_id,
            'algo': 'Opportunistic',
            'f0': f0,
            'final_f': final_f_opcs,
            'evals': evals_opcs,
            'cpu_time': cpu_time_opcs
        })
    
    # Restore original MAX_EVALS if we changed it
    if old_max_evals is not None:
        algo_module.MAX_EVALS = old_max_evals
    
    # Convert to DataFrame and return
    df = pd.DataFrame(results)
    return df

