"""
This module handles running all the experiments.

We generate 30 random starting points, then run all three algorithms
on each one. That gives us 90 runs total (30 instances × 3 algorithms).
"""

import numpy as np
import pandas as pd
from .config import (
    DIM, N_INSTANCES, DOMAIN_LOW, DOMAIN_HIGH,
    GLOBAL_SEED, INSTANCE_SEED_OFFSET
)
from .solar_wrapper import SolarWrapper
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


def run_experiments():
    """
    Run all three algorithms on all 30 instances.
    
    For each instance:
    1. Get the starting point
    2. Run Complete CS
    3. Run Ordered CS
    4. Run Opportunistic CS
    
    We reset the random seed before each algorithm so they all start
    with the same RNG state. This makes the comparison fair.
    
    Returns a DataFrame with all the results.
    """
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
    
    # Convert to DataFrame and return
    df = pd.DataFrame(results)
    return df

