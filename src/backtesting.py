import pandas as pd
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
            raise ValueError("Méthode non reconnue. Utilisez 'historical' ou 'parametric'.")

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
    return backtest_results["exception"].mean()