"""Runs every algorithm against every problem in the benchmark suite and
collects everything into one DataFrame.
"""

import numpy as np
import pandas as pd

import experiments.algorithms as algo_module
import experiments.mads as mads_module
from .algorithms import (
    complete_coordinate_search,
    ordered_coordinate_search,
    opportunistic_coordinate_search,
)
from .blackbox import Blackbox
from .config import (
    DIM, STARTS_PER_PROBLEM, DOMAIN_LOW, DOMAIN_HIGH,
    GLOBAL_SEED, INSTANCE_SEED_OFFSET,
    MAX_EVALS as DEFAULT_MAX_EVALS,
)
from .mads import mesh_adaptive_search
from .problems import PROBLEMS

ALGORITHMS = {
    "Complete": complete_coordinate_search,
    "Ordered": ordered_coordinate_search,
    "Opportunistic": opportunistic_coordinate_search,
    "MADS": mesh_adaptive_search,
}


def generate_starting_points():
    """STARTS_PER_PROBLEM random starts per problem, all in [-1, 1]^DIM.

    Seeded once up front so the whole batch of starting points is fixed
    across runs, regardless of eval budget.
    """
    np.random.seed(GLOBAL_SEED)
    n_problems = len(PROBLEMS)
    return np.random.uniform(
        DOMAIN_LOW, DOMAIN_HIGH, size=(n_problems, STARTS_PER_PROBLEM, DIM)
    )


def run_experiments(max_evals=None):
    """Returns a DataFrame with one row per (problem, start, algorithm).

    Reseeds the RNG right before every algorithm call so all four solvers
    see identical randomness on a given instance - matters for MADS's
    random poll directions and opportunistic's shuffles.
    """
    if max_evals is None:
        max_evals = DEFAULT_MAX_EVALS

    # both algorithms.py and mads.py read their eval budget as a module
    # constant, so bump it there for the duration of this run
    old_algo_budget = algo_module.MAX_EVALS
    old_mads_budget = mads_module.MAX_EVALS
    algo_module.MAX_EVALS = max_evals
    mads_module.MAX_EVALS = max_evals

    starting_points = generate_starting_points()
    rows = []
    instance_id = 0

    try:
        for problem_idx, (problem_name, (func, known_min)) in enumerate(PROBLEMS.items()):
            for start_idx in range(STARTS_PER_PROBLEM):
                x0 = starting_points[problem_idx, start_idx]
                instance_seed = instance_id + INSTANCE_SEED_OFFSET

                blackbox = Blackbox(func, instance_id)
                f0 = blackbox.evaluate(x0)

                for algo_name, algo_fn in ALGORITHMS.items():
                    np.random.seed(instance_seed)
                    blackbox.reset()
                    _, final_f, evals, cpu_time = algo_fn(blackbox, x0)
                    rows.append({
                        "instance_id": instance_id,
                        "problem": problem_name,
                        "algo": algo_name,
                        "f0": f0,
                        "final_f": final_f,
                        "known_min": known_min,
                        "evals": evals,
                        "cpu_time": cpu_time,
                    })

                instance_id += 1
    finally:
        algo_module.MAX_EVALS = old_algo_budget
        mads_module.MAX_EVALS = old_mads_budget

    return pd.DataFrame(rows)
