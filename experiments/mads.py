"""A simplified Mesh Adaptive Direct Search (MADS) solver.

This is the natural extension of the coordinate search variants in
algorithms.py: instead of always polling along the fixed +/-e_i axes, MADS
polls along a *random* positive spanning set that gets regenerated every
iteration, and separates the mesh size (controls where trial points can
land) from the poll size (controls how far it looks). Points are still
mesh-conforming, they just aren't restricted to the coordinate directions
- see Audet & Hare, "Derivative-Free and Blackbox Optimization" for the
general framework this is based on.

Two things distinguish this from a textbook GPS/MADS implementation:

1. The poll directions come from a random Householder reflection each
   iteration rather than a deterministic (Halton-based) construction like
   OrthoMADS. It's cheaper and still guarantees a positive spanning set,
   at the cost of losing OrthoMADS's nice deterministic coverage
   properties.
2. Before polling, there's a cheap "search step" that fits a local
   diagonal quadratic model to nearby evaluated points and jumps straight
   to that model's minimizer. When the model is any good this skips
   several iterations of blind polling for free (well, for one extra
   evaluation).
"""

import numpy as np

from .config import DELTA_0, DELTA_MIN, MAX_EVALS, MAX_CPU_TIME

MESH_EXPANSION = 4.0
MESH_CONTRACTION = 4.0
SEARCH_MIN_HISTORY_FACTOR = 2  # need at least 2n + 1 points before fitting


def _random_poll_directions(n, poll_size, mesh_size):
    """One random positive spanning set, snapped onto the current mesh.

    Reflecting the identity matrix through a random unit vector gives an
    orthogonal matrix; its columns (plus their negatives) positively span
    R^n no matter which unit vector was used, so this is cheap to sample
    fresh every iteration instead of reusing the coordinate axes.
    """
    u = np.random.normal(size=n)
    norm = np.linalg.norm(u)
    u = u / norm if norm > 1e-12 else np.eye(n)[0]
    reflection = np.eye(n) - 2.0 * np.outer(u, u)

    directions = []
    for col in reflection.T:
        d = np.round(col * poll_size / mesh_size) * mesh_size
        if np.linalg.norm(d) < 1e-12:
            continue
        directions.append(d)
        directions.append(-d)

    np.random.shuffle(directions)
    return directions


def _quadratic_surrogate_point(history_x, history_f, x_center, poll_size, n):
    """Fit f(x_center + y) ~= c + g.y + 0.5 * y.(h*y) on nearby points and
    return the model's minimizer inside the trust neighborhood, or None if
    there isn't enough nearby data yet (or the fit is degenerate).

    The Hessian is kept diagonal on purpose - with only a handful of local
    samples a full n x n Hessian is not identifiable, but n curvature
    terms plus n gradient terms plus a constant usually is.
    """
    n_params = 2 * n + 1
    if len(history_x) < SEARCH_MIN_HISTORY_FACTOR * n_params:
        return None

    X = np.asarray(history_x)
    F = np.asarray(history_f)
    dist = np.linalg.norm(X - x_center, axis=1)
    n_use = min(len(dist), max(n_params + n, 6 * n))
    nearest = np.argsort(dist)[:n_use]

    Y = X[nearest] - x_center
    design = np.hstack([np.ones((len(nearest), 1)), Y, Y ** 2])
    try:
        coeffs, *_ = np.linalg.lstsq(design, F[nearest], rcond=None)
    except np.linalg.LinAlgError:
        return None

    g = coeffs[1:n + 1]
    curvature = 2.0 * coeffs[n + 1:]

    step = np.zeros(n)
    for j in range(n):
        if curvature[j] > 1e-8:
            step[j] = np.clip(-g[j] / curvature[j], -poll_size, poll_size)
        elif g[j] != 0.0:
            step[j] = -poll_size * np.sign(g[j])

    if not np.any(np.abs(step) > 1e-12):
        return None

    return np.clip(x_center + step, -1.0, 1.0)


def mesh_adaptive_search(func, x0):
    """MADS with a diagonal-quadratic search step. Same call signature and
    stopping rules as the coordinate search variants, so it drops straight
    into the existing experiment runner.
    """
    func.reset()
    x = x0.copy()
    n = x0.shape[0]
    f_current = func.evaluate(x)

    history_x = [x.copy()]
    history_f = [f_current]

    mesh_size = DELTA_0
    poll_size = np.sqrt(mesh_size)

    while mesh_size >= DELTA_MIN and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
        improved = False

        candidate = _quadratic_surrogate_point(history_x, history_f, x, poll_size, n)
        if candidate is not None and func.eval_count < MAX_EVALS and func.cpu_time < MAX_CPU_TIME:
            f_candidate = func.evaluate(candidate)
            history_x.append(candidate.copy())
            history_f.append(f_candidate)
            if f_candidate < f_current:
                x, f_current = candidate, f_candidate
                improved = True

        if not improved:
            for d in _random_poll_directions(n, poll_size, mesh_size):
                if func.eval_count >= MAX_EVALS or func.cpu_time >= MAX_CPU_TIME:
                    break
                x_trial = np.clip(x + d, -1.0, 1.0)
                f_trial = func.evaluate(x_trial)
                history_x.append(x_trial.copy())
                history_f.append(f_trial)
                if f_trial < f_current:
                    x, f_current = x_trial, f_trial
                    improved = True
                    break

        if improved:
            mesh_size = min(mesh_size * MESH_EXPANSION, 1.0)
        else:
            mesh_size /= MESH_CONTRACTION
        poll_size = np.sqrt(mesh_size)

    return x, f_current, func.eval_count, func.cpu_time
