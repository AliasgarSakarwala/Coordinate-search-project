"""
Wrapper for SOLAR10 function with evaluation counting and CPU time tracking.

We use a mock implementation of SOLAR10 since the real package isn't easily available.
The mock is based on the real SOLAR simulator structure - see solar_mock.py for details.
"""

import time
import numpy as np
from .solar_mock import solar10


class SolarWrapper:
    """
    Wraps the SOLAR10 function to track how many times we call it and how long it takes.
    This is important for our experiments since we need to count evaluations and measure CPU time.
    """
    
    def __init__(self, instance_id):
        """
        Set up a new wrapper for tracking evaluations.
        
        The seed is set in experiment_runner.py before creating this wrapper,
        so we don't need to worry about it here.
        """
        self.instance_id = instance_id
        self.eval_count = 0  # How many times we've called the function
        self.cpu_time = 0.0  # Total time spent evaluating
        self.start_time = None
    
    def evaluate(self, x):
        """
        Call SOLAR10 at point x and track the evaluation.
        
        We measure the time for each call and add it to our total.
        This gives us accurate CPU time even if the function is fast.
        """
        if self.start_time is None:
            self.start_time = time.perf_counter()
        
        # Time this specific evaluation
        eval_start = time.perf_counter()
        f_val = solar10(x)
        eval_end = time.perf_counter()
        
        # Keep track of everything
        self.eval_count += 1
        self.cpu_time += (eval_end - eval_start)
        
        return float(f_val)
    
    def reset(self):
        """Reset counters when starting a new algorithm run."""
        self.eval_count = 0
        self.cpu_time = 0.0
        self.start_time = None


