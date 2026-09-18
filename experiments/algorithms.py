"""Three coordinate search variants that differ only in how they pick a
direction to move in during the poll step:

- complete: evaluates every direction, moves to the best one
- ordered: fixed direction order, takes the first improvement it finds
- opportunistic: same as ordered, but the order is reshuffled each pass
"""

import numpy as np

from .config import DIM, DELTA_0, DELTA_REDUCTION, DELTA_MIN, MAX_EVALS, MAX_CPU_TIME


def _coordinate_directions():
    """+e_i / -e_i for i = 0..DIM-1, i.e. the 2*DIM coordinate directions."""
    basis = np.eye(DIM)
    directions = []
    for i in range(DIM):
        directions.append(basis[i])
        directions.append(-basis[i])
    return directions


def complete_coordinate_search(func, x0):
    """Poll all 2*DIM coordinate directions and move to the best improvement.

    Most expensive per iteration of the three variants, but each step it
    does take is the best available one.
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0
    directions = _coordinate_directions()

    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        best_x = x.copy()
        best_f = f_current
        improved = False

        for d in directions:
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            x_trial = np.clip(x + delta * d, -1.0, 1.0)
            f_trial = func.evaluate(x_trial)
            if f_trial < best_f:
                best_f = f_trial
                best_x = x_trial.copy()
                improved = True

        if improved:
            x, f_current = best_x, best_f
        else:
            delta *= DELTA_REDUCTION
            if delta < DELTA_MIN:
                break

    return x, f_current, func.eval_count, func.cpu_time


def ordered_coordinate_search(func, x0):
    """Poll directions in a fixed order and stop at the first improvement.

    Cheaper per iteration than the complete variant since it doesn't need
    to check every direction, but the step it takes isn't guaranteed to be
    the best one available.
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0
    directions = _coordinate_directions()

    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        improved = False

        for d in directions:
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            x_trial = np.clip(x + delta * d, -1.0, 1.0)
            f_trial = func.evaluate(x_trial)
            if f_trial < f_current:
                x, f_current = x_trial, f_trial
                improved = True
                break

        if not improved:
            delta *= DELTA_REDUCTION
            if delta < DELTA_MIN:
                break

    return x, f_current, func.eval_count, func.cpu_time


def opportunistic_coordinate_search(func, x0):
    """Same rule as ordered search, but the polling order is shuffled every
    iteration instead of staying fixed. Removes the bias towards whichever
    coordinate happens to come first in the list.
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0
    base_directions = _coordinate_directions()

    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        improved = False
        directions = base_directions.copy()
        np.random.shuffle(directions)

        for d in directions:
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            x_trial = np.clip(x + delta * d, -1.0, 1.0)
            f_trial = func.evaluate(x_trial)
            if f_trial < f_current:
                x, f_current = x_trial, f_trial
                improved = True
                break

        if not improved:
            delta *= DELTA_REDUCTION
            if delta < DELTA_MIN:
                break

    return x, f_current, func.eval_count, func.cpu_time
