import numpy as np
import pandas as pd
import pytest
from src.risk_metrics import historical_var, parametric_var, mc_var, expected_shortfall
from src.portfolio import portfolio_returns
from src.backtesting import rolling_var_backtest, exception_rate

rng = np.random.default_rng(0)
RETURNS = pd.Series(rng.normal(-0.0005, 0.015, 1000))


def test_var_positive():
    assert historical_var(RETURNS) > 0
    assert parametric_var(RETURNS) > 0
    assert mc_var(RETURNS, seed=42) > 0


def test_higher_confidence_higher_var():
    assert historical_var(RETURNS, 0.99) >= historical_var(RETURNS, 0.95)
    assert parametric_var(RETURNS, 0.99) >= parametric_var(RETURNS, 0.95)


def test_es_exceeds_var():
    var = historical_var(RETURNS, 0.95)
    es = expected_shortfall(RETURNS, 0.95)
    assert es >= var - 1e-10


def test_mc_var_deterministic_with_seed():
    assert mc_var(RETURNS, seed=7) == mc_var(RETURNS, seed=7)


def test_portfolio_returns_shape():
    asset_returns = pd.DataFrame({"A": RETURNS, "B": RETURNS * 0.5})
    pf = portfolio_returns(asset_returns, weights=[0.6, 0.4])
    assert len(pf) == len(RETURNS)


def test_portfolio_weights_must_sum_to_one():
    asset_returns = pd.DataFrame({"A": RETURNS, "B": RETURNS})
    with pytest.raises(ValueError):
        portfolio_returns(asset_returns, weights=[0.5, 0.3])


def test_backtest_exception_rate_in_range():
    backtest = rolling_var_backtest(RETURNS, window=100, alpha=0.95, method="historical")
    rate = exception_rate(backtest)
    assert 0.0 <= rate <= 0.20
