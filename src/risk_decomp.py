from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import norm
from .portfolio import portfolio_returns


def correlation_matrix(asset_returns: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation matrix of asset returns."""
    return asset_returns.corr()


def component_var(
    asset_returns: pd.DataFrame,
    weights: list[float],
    alpha: float = 0.95,
) -> pd.Series:
    """
    Component VaR: contribution of each asset to portfolio parametric VaR.

    Uses the covariance decomposition:
        ComponentVaR_i = w_i * (Sigma @ w)_i / sigma_p * z_alpha

    Sum of component VaRs equals the total parametric portfolio VaR.
    """
    w = np.array(weights)
    mu = asset_returns.mean().values
    cov = asset_returns.cov().values
    sigma_p = float(np.sqrt(w @ cov @ w))
    z = norm.ppf(alpha)

    # Vol contribution + mean contribution (matches parametric_var formula)
    marginal_vol = cov @ w / sigma_p
    component = w * marginal_vol * z - w * mu

    return pd.Series(component, index=asset_returns.columns, name="component_var")


def diversification_ratio(
    asset_returns: pd.DataFrame,
    weights: list[float],
) -> float:
    """
    Diversification ratio = weighted avg vol / portfolio vol.
    DR > 1 means diversification benefit. DR = 1 means perfect correlation.
    """
    w = np.array(weights)
    vols = asset_returns.std(ddof=1).values
    cov = asset_returns.cov().values
    sigma_p = float(np.sqrt(w @ cov @ w))
    weighted_avg_vol = float(w @ vols)
    return weighted_avg_vol / sigma_p
