import numpy as np
import pandas as pd
import pytest
from src.risk_metrics import historical_var, parametric_var, expected_shortfall
from src.portfolio import portfolio_returns
from src.backtesting import rolling_var_backtest, exception_rate

rng = np.random.default_rng(42)
RETURNS = pd.Series(rng.normal(0, 0.01, 500))


def test_historical_var_positive():
    assert historical_var(RETURNS, alpha=0.95) > 0

def test_parametric_var_positive():
    assert parametric_var(RETURNS, alpha=0.95) > 0

def test_es_ge_var():
    var = historical_var(RETURNS, alpha=0.95)
    es  = expected_shortfall(RETURNS, alpha=0.95)
    assert es >= var - 1e-10  # ES is always >= VaR by definition

def test_higher_confidence_higher_var():
    var_95 = historical_var(RETURNS, alpha=0.95)
    var_99 = historical_var(RETURNS, alpha=0.99)
    assert var_99 >= var_95

def test_portfolio_returns_shape():
    asset_returns = pd.DataFrame({"A": RETURNS, "B": RETURNS * 0.5})
    pf = portfolio_returns(asset_returns, weights=[0.6, 0.4])
    assert len(pf) == len(RETURNS)

def test_portfolio_weights_must_sum_to_one():
    asset_returns = pd.DataFrame({"A": RETURNS, "B": RETURNS})
    with pytest.raises(ValueError):
        portfolio_returns(asset_returns, weights=[0.5, 0.3])

def test_backtest_exception_rate_near_expected():
    backtest = rolling_var_backtest(RETURNS, window=100, alpha=0.95, method="historical")
    rate = exception_rate(backtest)
    assert 0.0 <= rate <= 0.20  # should be near 5%; allow wide tolerance for small sample
