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

    def __init__(self, func, instance_id=None, record_trace=False):
        self.func = func
        self.instance_id = instance_id
        self.eval_count = 0
        self.cpu_time = 0.0
        self.record_trace = record_trace
        self.trace = []
        self._best_f = None

    def evaluate(self, x):
        t0 = time.perf_counter()
        f_val = float(self.func(x))
        self.cpu_time += time.perf_counter() - t0
        self.eval_count += 1

        if self._best_f is None or f_val < self._best_f:
            self._best_f = f_val
        if self.record_trace:
            # (evals so far, best objective seen so far) - what a
            # convergence plot needs, tracked for free here instead of
            # threading it through every solver
            self.trace.append((self.eval_count, self._best_f))

        return f_val

    def reset(self):
        self.eval_count = 0
        self.cpu_time = 0.0
        self.trace = []
        self._best_f = None
