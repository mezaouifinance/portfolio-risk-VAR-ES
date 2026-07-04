from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import chi2
from .risk_metrics import historical_var, parametric_var


def rolling_var_backtest(
    returns: pd.Series,
    window: int = 252,
    alpha: float = 0.95,
    method: str = "historical"
) -> pd.DataFrame:
    var_values = []
    realized_returns = []
    dates = []

    for i in range(window, len(returns)):
        train_sample = returns.iloc[i - window:i]
        realized = returns.iloc[i]

        if method == "historical":
            var_estimate = historical_var(train_sample, alpha=alpha)
        elif method == "parametric":
            var_estimate = parametric_var(train_sample, alpha=alpha)
        else:
            raise ValueError(f"Unknown method '{method}'. Use 'historical' or 'parametric'.")

        var_values.append(var_estimate)
        realized_returns.append(realized)
        dates.append(returns.index[i])

    results = pd.DataFrame(
        {
            "realized_return": realized_returns,
            "VaR": var_values,
        },
        index=dates
    )

    results["exception"] = -results["realized_return"] > results["VaR"]
    return results


def exception_rate(backtest_results: pd.DataFrame) -> float:
    return float(backtest_results["exception"].mean())


def kupiec_pof(n_exceptions: int, n_obs: int, alpha: float = 0.95) -> dict:
    p = 1 - alpha
    if n_exceptions == 0:
        return {"stat": np.nan, "p_value": np.nan, "reject_H0": False}
    p_hat = n_exceptions / n_obs
    lr = -2 * (
        n_exceptions * np.log(p / p_hat)
        + (n_obs - n_exceptions) * np.log((1 - p) / (1 - p_hat))
    )
    p_value = float(1 - chi2.cdf(lr, df=1))
    return {"stat": round(lr, 4), "p_value": round(p_value, 4), "reject_H0": p_value < 0.05}


def traffic_light(n_exceptions: int) -> str:
    """Basel II/III traffic light for 99% VaR on a 250-day window."""
    if n_exceptions <= 4:
        return "green"
    if n_exceptions <= 9:
        return "yellow"
    return "red"