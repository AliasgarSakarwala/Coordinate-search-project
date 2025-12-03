"""
Configuration for 2000-evaluation experiments.
This extends the base config with MAX_EVALS = 2000.
"""

from .config import (
    DIM, N_INSTANCES, DOMAIN_LOW, DOMAIN_HIGH,
    DELTA_0, DELTA_REDUCTION, DELTA_MIN,
    MAX_CPU_TIME, TAU, GLOBAL_SEED, INSTANCE_SEED_OFFSET
)

# Override MAX_EVALS for 2000-eval experiments
MAX_EVALS = 2000

# Evaluation budget step for data profiles (to reduce file size)
# Use step=20: 1, 21, 41, ..., 1981, 2000
EVAL_BUDGET_STEP = 20

