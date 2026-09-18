"""Stand-in for the SOLAR10 benchmark.

SOLAR10 is normally distributed as a compiled C++ simulator (see the
NOMAD/SOLAR benchmark suite), which isn't practical to build for this
project. This module reproduces its rough shape instead: five inputs with
the real function's physical bounds (collector temperature, storage sizes,
etc.), a minimum around 42, and a roughly bowl-shaped cost surface with a
couple of cross-terms so the coordinates aren't fully separable. The other
five dimensions are along for the ride so the problem matches DIM = 10.

None of this is meant to be a faithful physical model - it's just something
deterministic and reasonably interesting to optimize against.
"""

import numpy as np

# bounds used by the real SOLAR10 simulator for its five inputs
_LB = np.array([793.0, 2.0, 2.0, 0.01, 0.01])
_UB = np.array([995.0, 50.0, 30.0, 5.00, 5.00])

_BASE_COST = 42.0
_SCALE = 15.0


def solar10(x):
    """Evaluate the mock SOLAR10 cost at a 10-d point in [-1, 1]^10."""
    x = np.asarray(x)
    if x.shape != (10,):
        raise ValueError(f"expected a length-10 vector, got shape {x.shape}")

    x_solar = _LB + (x[:5] + 1.0) / 2.0 * (_UB - _LB)
    x_norm = (x_solar - _LB) / (_UB - _LB)

    cost = 10.0 * np.sum((x_norm - 0.5) ** 2)
    cost += 5.0 * (x_norm[0] - x_norm[1]) ** 2
    cost += 3.0 * (x_norm[2] - x_norm[3]) ** 2
    cost += 2.0 * np.exp(-5.0 * np.sum(x_norm ** 2))

    result = _BASE_COST + cost * _SCALE
    result += 0.3 * np.sum(x[5:] ** 2)

    # keep it from dipping meaningfully below the known SOLAR10 floor
    if result < 40.0:
        result = 40.0 + (40.0 - result) * 0.1

    return float(result)
