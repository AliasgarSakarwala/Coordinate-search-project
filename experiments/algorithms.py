"""
Three variants of Coordinate Search for comparison.

The main difference is how they choose which direction to move in:
- Complete: tries all directions, picks the best one
- Ordered: tries directions in a fixed order, takes the first improvement
- Opportunistic: same as ordered but shuffles the order each iteration
"""

import numpy as np
from .config import DIM, DELTA_0, DELTA_REDUCTION, DELTA_MIN, MAX_EVALS, MAX_CPU_TIME


def complete_coordinate_search(func, x0):
    """
    Complete Coordinate Search.
    
    This is the most thorough version - it evaluates all 2*DIM directions
    (positive and negative for each coordinate) and picks whichever one
    gives the best improvement. This uses the most evaluations but should
    make the best progress per iteration.
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0  # Start with the initial step size
    
    # Build the list of coordinate directions
    # For 10D, we have +e0, -e0, +e1, -e1, ..., +e9, -e9 (20 directions total)
    directions = []
    for i in range(DIM):
        directions.append(np.eye(DIM)[i])   # +e_i
        directions.append(-np.eye(DIM)[i])  # -e_i
    
    # Main loop: keep going until we hit a stopping condition
    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        # Track the best direction we find this iteration
        best_x = x.copy()
        best_f = f_current
        improved = False
        
        # Try every direction and see which one is best
        for d in directions:
            # Check if we've hit our limits
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            
            # Move in this direction by delta
            x_candidate = x + delta * d
            # Make sure we stay in bounds [-1, 1]
            x_candidate = np.clip(x_candidate, -1.0, 1.0)
            f_candidate = func.evaluate(x_candidate)
            
            # If this is better than what we've seen so far, remember it
            if f_candidate < best_f:
                best_f = f_candidate
                best_x = x_candidate.copy()
                improved = True
        
        # If we found an improvement, move to the best point
        if improved:
            x = best_x
            f_current = best_f
        else:
            # No improvement means we need a smaller step size
            delta *= DELTA_REDUCTION
            # If delta gets too small, we're done
            if delta < DELTA_MIN:
                break
    
    return x, f_current, func.eval_count, func.cpu_time


def ordered_coordinate_search(func, x0):
    """
    Ordered Coordinate Search.
    
    This version goes through directions in a fixed order (+e0, -e0, +e1, -e1, ...)
    and takes the FIRST direction that gives an improvement. This means it might
    not pick the best direction, but it uses fewer evaluations since it stops
    as soon as it finds something better.
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0
    
    # Same directions as complete, but we'll go through them in order
    directions = []
    for i in range(DIM):
        directions.append(np.eye(DIM)[i])   # +e_i
        directions.append(-np.eye(DIM)[i])  # -e_i
    
    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        improved = False
        
        # Go through directions in order, stop at the first improvement
        for d in directions:
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            
            x_candidate = x + delta * d
            x_candidate = np.clip(x_candidate, -1.0, 1.0)
            f_candidate = func.evaluate(x_candidate)
            
            # As soon as we find something better, take it and stop looking
            if f_candidate < f_current:
                x = x_candidate
                f_current = f_candidate
                improved = True
                break  # Found improvement, no need to check other directions
        
        if not improved:
            # Nothing worked, shrink the step size
            delta *= DELTA_REDUCTION
            if delta < DELTA_MIN:
                break
    
    return x, f_current, func.eval_count, func.cpu_time


def opportunistic_coordinate_search(func, x0):
    """
    Opportunistic Coordinate Search.
    
    This is basically the same as ordered, but we shuffle the directions
    randomly each iteration. The idea is that this makes the algorithm
    less biased toward always checking coordinates in the same order.
    Sometimes this helps, sometimes it doesn't - that's why we test it!
    """
    func.reset()
    x = x0.copy()
    f_current = func.evaluate(x)
    delta = DELTA_0
    
    # Start with the same base set of directions
    base_directions = []
    for i in range(DIM):
        base_directions.append(np.eye(DIM)[i])   # +e_i
        base_directions.append(-np.eye(DIM)[i])  # -e_i
    
    while delta >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        improved = False
        
        # Shuffle the directions each iteration - this is the key difference
        directions = base_directions.copy()
        np.random.shuffle(directions)
        
        # Now try them in the shuffled order, take first improvement
        for d in directions:
            if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                break
            
            x_candidate = x + delta * d
            x_candidate = np.clip(x_candidate, -1.0, 1.0)
            f_candidate = func.evaluate(x_candidate)
            
            if f_candidate < f_current:
                x = x_candidate
                f_current = f_candidate
                improved = True
                break  # Found one, stop looking
        
        if not improved:
            delta *= DELTA_REDUCTION
            if delta < DELTA_MIN:
                break
    
    return x, f_current, func.eval_count, func.cpu_time

