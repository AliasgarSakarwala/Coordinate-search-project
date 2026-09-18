"""Standard derivative-free optimization test functions.

The SOLAR10 mock is a fine real-world-flavored blackbox, but on its own
it's a single arbitrary problem with no known optimum - hard to say
anything rigorous about "how close to optimal did we get". These five are
the opposite: textbook non-convex test functions with a known global
minimizer, so we can report a real optimality gap instead of just ranking
algorithms against each other.

Every function here is defined generically for any dimension n and takes
x in [-1, 1]^n, same convention as the rest of the project. Internally each
one rescales x into the range it's normally tested on and shifts things so
the global minimum always sits at x = 0 with f(x*) = 0 - that keeps the
"random starting point in [-1, 1]^n" setup from experiment_runner.py
meaningful across every problem in the suite, and keeps the classic
Rosenbrock minimizer (normally at all-ones) off the domain boundary.
"""

import numpy as np


def sphere(x):
    """Convex bowl, separable. About as easy as DFO problems get."""
    y = np.asarray(x)
    return float(np.sum(y ** 2))


def rosenbrock(x, scale=2.0):
    """The banana function. Narrow curved valley - hard for methods that
    only move along fixed coordinate axes, since the valley cuts diagonally
    across them.
    """
    y = np.asarray(x) * scale + 1.0  # shift so x=0 -> y=(1,...,1) -> f=0
    return float(np.sum(100.0 * (y[1:] - y[:-1] ** 2) ** 2 + (1.0 - y[:-1]) ** 2))


def rastrigin(x, scale=5.12):
    """Sphere with a cosine ripple layered on top - lots of local minima
    surrounding the global one at the origin.
    """
    y = np.asarray(x) * scale
    n = len(y)
    return float(10.0 * n + np.sum(y ** 2 - 10.0 * np.cos(2.0 * np.pi * y)))


def ackley(x, scale=32.768):
    """Nearly flat outside a steep central well - easy to make progress far
    from the optimum, easy to get lost once you're close to it.
    """
    y = np.asarray(x) * scale
    n = len(y)
    term1 = -20.0 * np.exp(-0.2 * np.sqrt(np.sum(y ** 2) / n))
    term2 = -np.exp(np.sum(np.cos(2.0 * np.pi * y)) / n)
    return float(term1 + term2 + 20.0 + np.e)


def levy(x, scale=10.0):
    """Multimodal, minimizer at the all-ones vector before our shift."""
    y = np.asarray(x) * scale + 1.0
    w = 1.0 + (y - 1.0) / 4.0
    term1 = np.sin(np.pi * w[0]) ** 2
    term3 = (w[-1] - 1.0) ** 2 * (1.0 + np.sin(2.0 * np.pi * w[-1]) ** 2)
    mid = (w[:-1] - 1.0) ** 2 * (1.0 + 10.0 * np.sin(np.pi * w[:-1] + 1.0) ** 2)
    return float(term1 + np.sum(mid) + term3)


# name -> (callable, known global minimum value)
BENCHMARK_FUNCTIONS = {
    "Sphere": (sphere, 0.0),
    "Rosenbrock": (rosenbrock, 0.0),
    "Rastrigin": (rastrigin, 0.0),
    "Ackley": (ackley, 0.0),
    "Levy": (levy, 0.0),
}
