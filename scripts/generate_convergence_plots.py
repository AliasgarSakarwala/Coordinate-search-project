#!/usr/bin/env python3
"""One-off script that produces the convergence figures used in the
README (docs/assets/). Not part of the main benchmark run - this just
picks one starting point per problem and plots optimality gap vs.
evaluations for every algorithm, on a log axis.

    python3 scripts/generate_convergence_plots.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

import experiments.algorithms as algo_module
import experiments.mads as mads_module
from experiments.algorithms import (
    complete_coordinate_search,
    ordered_coordinate_search,
    opportunistic_coordinate_search,
)
from experiments.blackbox import Blackbox
from experiments.config import DIM, DOMAIN_LOW, DOMAIN_HIGH
from experiments.mads import mesh_adaptive_search
from experiments.plots import plot_convergence
from experiments.problems import PROBLEMS

ALGORITHMS = {
    "Complete": complete_coordinate_search,
    "Ordered": ordered_coordinate_search,
    "Opportunistic": opportunistic_coordinate_search,
    "MADS": mesh_adaptive_search,
}

EVAL_BUDGET = 2000
PROBLEMS_TO_PLOT = ["Rastrigin", "Rosenbrock"]
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "assets")


def trace_to_gap(trace, f_star):
    evals = np.array([t[0] for t in trace])
    best_f = np.array([t[1] for t in trace])
    gap = np.maximum(best_f - f_star, 1e-12)  # keep it plottable on a log axis
    return evals, gap


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    algo_module.MAX_EVALS = EVAL_BUDGET
    mads_module.MAX_EVALS = EVAL_BUDGET

    np.random.seed(2024)

    for problem_name in PROBLEMS_TO_PLOT:
        func, known_min = PROBLEMS[problem_name]
        f_star = known_min if known_min is not None else 0.0
        x0 = np.random.uniform(DOMAIN_LOW, DOMAIN_HIGH, size=DIM)

        traces = {}
        for algo_name, algo_fn in ALGORITHMS.items():
            np.random.seed(7)
            blackbox = Blackbox(func, record_trace=True)
            algo_fn(blackbox, x0)
            traces[algo_name] = trace_to_gap(blackbox.trace, f_star)

        out_path = os.path.join(OUT_DIR, f"convergence_{problem_name.lower()}.png")
        plot_convergence(traces, out_path, title=f"Convergence on {problem_name}")
        print(f"saved {out_path}")


if __name__ == "__main__":
    main()
