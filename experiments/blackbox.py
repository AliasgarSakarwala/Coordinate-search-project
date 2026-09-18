"""Generic evaluation-counting wrapper for a plain objective function.

Used to be SOLAR10-specific (see git history), but once the benchmark
suite grew past one function it made more sense to have a single wrapper
that works for anything with the signature f(x) -> float.
"""

import time


class Blackbox:
    """Wraps func(x) -> float and tracks call count + wall time spent
    inside func. instance_id is just a label for bookkeeping upstream.
    """

    def __init__(self, func, instance_id=None):
        self.func = func
        self.instance_id = instance_id
        self.eval_count = 0
        self.cpu_time = 0.0

    def evaluate(self, x):
        t0 = time.perf_counter()
        f_val = self.func(x)
        self.cpu_time += time.perf_counter() - t0
        self.eval_count += 1
        return float(f_val)

    def reset(self):
        self.eval_count = 0
        self.cpu_time = 0.0
