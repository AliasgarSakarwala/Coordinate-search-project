"""
Experiment runner for 2000-evaluation experiments.
Uses config_2000 which overrides MAX_EVALS = 2000.
"""

import numpy as np
import pandas as pd
# Import the 2000-eval config (which overrides MAX_EVALS)
from .config_2000 import (
    DIM, N_INSTANCES, DOMAIN_LOW, DOMAIN_HIGH,
    GLOBAL_SEED, INSTANCE_SEED_OFFSET, MAX_EVALS, MAX_CPU_TIME
)
from .solar_wrapper import SolarWrapper
# Import algorithms and patch MAX_EVALS to use 2000
import experiments.algorithms as algo_module
from .config_2000 import MAX_EVALS as MAX_EVALS_2000, MAX_CPU_TIME as MAX_CPU_TIME_2000
# Temporarily override MAX_EVALS in algorithms module
_old_max_evals = algo_module.MAX_EVALS
_old_max_cpu_time = algo_module.MAX_CPU_TIME
algo_module.MAX_EVALS = MAX_EVALS_2000
algo_module.MAX_CPU_TIME = MAX_CPU_TIME_2000
from .algorithms import (
    complete_coordinate_search,
    ordered_coordinate_search,
    opportunistic_coordinate_search
)


def generate_starting_points():
    """
    Generate N_INSTANCES random starting points uniformly in [-1, 1]^DIM.
    
    Returns:
        numpy array of shape (N_INSTANCES, DIM)
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
    Run all experiments with MAX_EVALS = 2000: generate starting points and run all algorithms.
    
    Returns:
        pandas.DataFrame with columns: instance_id, algo, f0, final_f, evals, cpu_time
    """
    # Generate starting points
    starting_points = generate_starting_points()
    
    results = []
    
    for instance_id in range(N_INSTANCES):
        x0 = starting_points[instance_id]
        instance_seed = instance_id + INSTANCE_SEED_OFFSET
        
        # Set seed ONCE per instance - all algorithms on this instance start with same RNG state
        np.random.seed(instance_seed)
        
        # Create function wrapper for this instance
        func_wrapper = SolarWrapper(instance_id)
        
        # Evaluate initial point (uses current RNG state)
        f0 = func_wrapper.evaluate(x0)
        
        # Run Complete Coordinate Search
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
    
    df = pd.DataFrame(results)
    return df

