from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import norm


def historical_var(returns: pd.Series, alpha: float = 0.95) -> float:
    return float(-np.quantile(returns, 1 - alpha))


def parametric_var(returns: pd.Series, alpha: float = 0.95) -> float:
    mu = returns.mean()
    sigma = returns.std(ddof=1)
    z = norm.ppf(1 - alpha)
    return float(-(mu + z * sigma))


def mc_var(
    returns: pd.Series,
    alpha: float = 0.95,
    n_sims: int = 10_000,
    seed: int | None = None,
) -> float:
    rng = np.random.default_rng(seed)
    mu, sigma = returns.mean(), returns.std(ddof=1)
    simulated = rng.normal(mu, sigma, n_sims)
    return float(-np.quantile(simulated, 1 - alpha))


def expected_shortfall(returns: pd.Series, alpha: float = 0.95) -> float:
    var_threshold = np.quantile(returns, 1 - alpha)
    tail_losses = returns[returns <= var_threshold]
    return float(-tail_losses.mean())