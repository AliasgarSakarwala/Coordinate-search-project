"""
Global configuration constants for the Coordinate Search experiments.
"""

# Problem dimension
DIM = 10

# Number of problem instances
N_INSTANCES = 30

# Domain bounds
DOMAIN_LOW = -1.0
DOMAIN_HIGH = 1.0

# Initial step size
DELTA_0 = 1.0

# Step size reduction factor
DELTA_REDUCTION = 0.5

# Minimum step size
DELTA_MIN = 1e-4

# Maximum function evaluations
MAX_EVALS = 500

# Evaluation budget step for data profiles (to reduce file size for 500-eval)
# Use step=5: 1, 6, 11, ..., 496, 500
EVAL_BUDGET_STEP = 5

# Maximum CPU time (seconds)
MAX_CPU_TIME = 10.0

# Tolerance for success
TAU = 1e-3

# Random seeds
GLOBAL_SEED = 12345
INSTANCE_SEED_OFFSET = 1000


