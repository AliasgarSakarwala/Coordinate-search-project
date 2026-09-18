"""A portfolio construction blackbox - the problem in this suite that's
closest to why you'd actually reach for a derivative-free method at work
instead of a classic test function.

The setup: K synthetic assets whose returns come from a small factor model
(fixed seed, so the "market data" is the same every run), and we're
choosing portfolio weights to maximize a risk-adjusted return net of
trading costs. The objective wraps a sort (for CVaR) and an L1 turnover
penalty, so there's no clean closed-form gradient to hand to a solver even
though the weight mapping itself is smooth - which is exactly the kind of
pipeline DFO methods get used on in practice: you can call the backtest as
a function, you just can't differentiate through it.
"""

import numpy as np

N_ASSETS = 10  # matches the project's DIM so it drops into the same pipeline
_N_FACTORS = 3
_N_DAYS = 500

_TRANSACTION_COST_RATE = 0.0015
_CVAR_LEVEL = 0.95
_RISK_AVERSION = 0.5
_TRADING_DAYS = 252

_rng = np.random.RandomState(20240917)
_factor_loadings = _rng.normal(0.6, 0.3, size=(N_ASSETS, _N_FACTORS))
_factor_vol = np.array([0.015, 0.010, 0.008])
_idio_vol = _rng.uniform(0.008, 0.02, size=N_ASSETS)
_asset_drift = _rng.uniform(0.0002, 0.0006, size=N_ASSETS)

_factor_returns = _rng.normal(size=(_N_DAYS, _N_FACTORS)) * _factor_vol
_idio_returns = _rng.normal(size=(_N_DAYS, N_ASSETS)) * _idio_vol
ASSET_RETURNS = _asset_drift + _factor_returns @ _factor_loadings.T + _idio_returns

_EQUAL_WEIGHT = np.full(N_ASSETS, 1.0 / N_ASSETS)


def weights_from_x(x):
    """Map an unconstrained point in [-1, 1]^N_ASSETS to long-only weights
    that sum to one, via softmax. Smooth on purpose - the kinks in the
    objective come from the cost and risk terms, not from this.
    """
    z = np.asarray(x)
    shifted = np.exp(z - np.max(z))
    return shifted / np.sum(shifted)


def _cvar(losses, level):
    """Historical CVaR: average loss over the worst (1 - level) fraction
    of days. Sorting makes this non-smooth in the weights.
    """
    tail_size = max(1, int(np.ceil((1.0 - level) * len(losses))))
    worst = np.sort(losses)[::-1][:tail_size]
    return float(np.mean(worst))


def portfolio_neg_sharpe(x):
    """Objective to minimize: -annualized Sharpe, plus a turnover cost
    penalty and a CVaR risk penalty. Starting from equal weight (x = 0)
    gives some baseline Sharpe; the point of running a solver here is to
    see how much of that can be improved once costs and tail risk are
    accounted for.
    """
    w = weights_from_x(x)
    port_returns = ASSET_RETURNS @ w

    mean_ret = np.mean(port_returns)
    std_ret = np.std(port_returns)
    sharpe = (mean_ret / std_ret) * np.sqrt(_TRADING_DAYS) if std_ret > 1e-10 else 0.0

    turnover = np.sum(np.abs(w - _EQUAL_WEIGHT))
    cost_penalty = _TRANSACTION_COST_RATE * turnover * _TRADING_DAYS

    tail_risk = _cvar(-port_returns, _CVAR_LEVEL) * np.sqrt(_TRADING_DAYS)

    return float(-sharpe + cost_penalty + _RISK_AVERSION * tail_risk)
