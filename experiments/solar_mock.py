"""
Mock implementation of the SOLAR10 function.

The real SOLAR10 is a C++ program that's hard to install, so we use a mock instead.
I looked at the real SOLAR code on GitHub to understand what it does:
- It's a cost minimization problem (lower is better)
- The real version has 5 inputs, but our project needs 10 dimensions
- It's deterministic (same input always gives same output)
- The best known value is around 42.4

This mock tries to capture the same behavior but works with 10D inputs.
"""

import numpy as np


def solar10(x):
    """
    Mock SOLAR10 function that takes a 10D point and returns a cost value.
    
    The real SOLAR10 has 5 inputs with specific physical meanings (temperature,
    storage dimensions, etc.), but we need 10D for this project. So we:
    1. Take the first 5 dimensions and map them to the real SOLAR10 bounds
    2. Use the remaining 5 dimensions to add some extra complexity
    3. Return a cost value that's in a similar range to the real function
    """
    x = np.asarray(x)
    if x.shape != (10,):
        raise ValueError(f"Expected shape (10,), got {x.shape}")
    
    # The real SOLAR10 uses these bounds for its 5 inputs
    # We map our [-1, 1]^10 to these bounds for the first 5 dimensions
    lb = np.array([793.0, 2.0, 2.0, 0.01, 0.01])  # Lower bounds
    ub = np.array([995.0, 50.0, 30.0, 5.00, 5.00])  # Upper bounds
    
    # Transform first 5 dimensions from [-1, 1] to the real SOLAR10 bounds
    x_solar = lb + (x[:5] + 1) / 2.0 * (ub - lb)
    
    # Normalize to [0, 1] to make the math easier
    x_norm = (x_solar - lb) / (ub - lb)
    
    # Build a cost function that has some structure
    # I'm using a mix of quadratic and exponential terms to make it interesting
    result = 0.0
    
    # Quadratic penalties - being away from the center costs more
    for i in range(5):
        center = 0.5
        result += 10.0 * (x_norm[i] - center)**2
    
    # Cross-terms - variables interact with each other
    result += 5.0 * (x_norm[0] - x_norm[1])**2
    result += 3.0 * (x_norm[2] - x_norm[3])**2
    
    # Exponential term to create a sharp minimum
    result += 2.0 * np.exp(-5.0 * np.sum(x_norm**2))
    
    # Do some extra computation to make timing realistic
    # (the real function does actual physics calculations)
    _ = np.sum(np.sin(x_norm) * np.cos(x_norm))
    _ = np.sum(np.exp(-0.1 * x_norm))
    
    # Scale the result to match the real SOLAR10's value range
    # Real function has minimum around 42, typical values 40-200+
    base_cost = 42.0
    scaled_result = base_cost + result * 15.0
    
    # Use the remaining 5 dimensions (x[5:]) to add some extra cost
    # They don't affect things as much as the main 5 dimensions
    x_extra = x[5:]
    extra_term = 0.3 * np.sum(x_extra**2)
    scaled_result += extra_term
    
    # Make sure we don't go below the minimum we expect
    if scaled_result < 40.0:
        scaled_result = 40.0 + (40.0 - scaled_result) * 0.1
    
    return float(scaled_result)

