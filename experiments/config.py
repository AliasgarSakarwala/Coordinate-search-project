"""Shared constants for the coordinate search experiments."""

# problem dimension
DIM = 10

# number of problem instances per benchmark run
N_INSTANCES = 30

# search domain bounds
DOMAIN_LOW = -1.0
DOMAIN_HIGH = 1.0

# step size schedule
DELTA_0 = 1.0
DELTA_REDUCTION = 0.5
DELTA_MIN = 1e-4

# budgets
MAX_EVALS = 500
MAX_CPU_TIME = 10.0

# step used when building the evaluation-budget data profile (keeps the
# 500-eval CSVs from having 500 rows each)
EVAL_BUDGET_STEP = 5

# success tolerance for the data profile
TAU = 1e-3

# seeds - fixed so results are reproducible across machines
GLOBAL_SEED = 12345
INSTANCE_SEED_OFFSET = 1000
