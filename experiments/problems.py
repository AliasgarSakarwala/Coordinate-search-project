"""Registry of every blackbox problem in the benchmark suite.

Each entry maps a problem name to (callable, known_global_minimum). The
classic test functions have a known minimum of 0.0, which lets the
success criterion and the significance tests use the real optimality gap
instead of an estimate. SOLAR10 and the portfolio problem don't have a
known closed-form optimum, so their entry is None and profiles.py falls
back to the best value any solver found for them.
"""

from .finance_problem import portfolio_neg_sharpe
from .solar_mock import solar10
from .test_functions import BENCHMARK_FUNCTIONS

PROBLEMS = {
    "SOLAR10": (solar10, None),
    "Portfolio": (portfolio_neg_sharpe, None),
}

for _name, (_func, _known_min) in BENCHMARK_FUNCTIONS.items():
    PROBLEMS[_name] = (_func, _known_min)
