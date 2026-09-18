"""Thin wrapper around an objective function that counts evaluations and
tracks wall-clock time spent inside the function itself.

Both numbers are needed for the data profiles later, since we care about
"how many evaluations did it take" and "how much CPU time did it take"
separately.
"""

import time

from .solar_mock import solar10


class SolarWrapper:
    """Counts calls and timing for the mock SOLAR10 function.

    instance_id isn't used by solar10 itself right now (the mock is
    deterministic) - it's kept around so callers can tag results by
    instance without having to pass it through separately.
    """

    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.eval_count = 0
        self.cpu_time = 0.0

    def evaluate(self, x):
        t0 = time.perf_counter()
        f_val = solar10(x)
        self.cpu_time += time.perf_counter() - t0
        self.eval_count += 1
        return float(f_val)

    def reset(self):
        self.eval_count = 0
        self.cpu_time = 0.0
