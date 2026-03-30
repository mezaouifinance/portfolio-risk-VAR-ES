import numpy as np
import pandas as pd
from scipy.stats import norm


def historical_var(returns: pd.Series, alpha: float = 0.95) -> float:
    return -np.quantile(returns, 1 - alpha)


def parametric_var(returns: pd.Series, alpha: float = 0.95) -> float:
    mu = returns.mean()
    sigma = returns.std(ddof=1)
    z = norm.ppf(1 - alpha)
    return -(mu + z * sigma)


def expected_shortfall(returns: pd.Series, alpha: float = 0.95) -> float:
    var_threshold = np.quantile(returns, 1 - alpha)
    tail_losses = returns[returns <= var_threshold]
    return -tail_losses.mean()