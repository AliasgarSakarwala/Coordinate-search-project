"""Runs the three coordinate search variants across a batch of starting
points and collects the results into a single DataFrame.
"""

import numpy as np
import pandas as pd

import experiments.algorithms as algo_module
from .algorithms import (
    complete_coordinate_search,
    ordered_coordinate_search,
    opportunistic_coordinate_search,
)
from .config import (
    DIM, N_INSTANCES, DOMAIN_LOW, DOMAIN_HIGH,
    GLOBAL_SEED, INSTANCE_SEED_OFFSET,
    MAX_EVALS as DEFAULT_MAX_EVALS, MAX_CPU_TIME as DEFAULT_MAX_CPU_TIME,
)
from .solar_wrapper import SolarWrapper

ALGORITHMS = {
    "Complete": complete_coordinate_search,
    "Ordered": ordered_coordinate_search,
    "Opportunistic": opportunistic_coordinate_search,
}


def generate_starting_points():
    """N_INSTANCES random starts in [-1, 1]^DIM, seeded for reproducibility."""
    np.random.seed(GLOBAL_SEED)
    return np.random.uniform(DOMAIN_LOW, DOMAIN_HIGH, size=(N_INSTANCES, DIM))


def run_experiments(max_evals=None, eval_budget_step=None):
    """Run every algorithm on every starting point and return one DataFrame.

    eval_budget_step isn't actually needed to run the experiments - it only
    matters later when building the data profile - but it's accepted here
    too so callers can pass both budget params through in one place.
    """
    if max_evals is None:
        max_evals = DEFAULT_MAX_EVALS

    # algorithms.py reads MAX_EVALS as a module-level constant, so bump it
    # there for the duration of this run if a different budget was asked for
    old_max_evals = algo_module.MAX_EVALS
    algo_module.MAX_EVALS = max_evals

    starting_points = generate_starting_points()
    rows = []

    try:
        for instance_id in range(N_INSTANCES):
            x0 = starting_points[instance_id]
            instance_seed = instance_id + INSTANCE_SEED_OFFSET

            func = SolarWrapper(instance_id)
            f0 = func.evaluate(x0)

            for algo_name, algo_fn in ALGORITHMS.items():
                # reseed before every algorithm so each one sees the same
                # RNG state - matters for opportunistic's shuffles
                np.random.seed(instance_seed)
                func.reset()
                _, final_f, evals, cpu_time = algo_fn(func, x0)
                rows.append({
                    "instance_id": instance_id,
                    "algo": algo_name,
                    "f0": f0,
                    "final_f": final_f,
                    "evals": evals,
                    "cpu_time": cpu_time,
                })
    finally:
        algo_module.MAX_EVALS = old_max_evals

    return pd.DataFrame(rows)
