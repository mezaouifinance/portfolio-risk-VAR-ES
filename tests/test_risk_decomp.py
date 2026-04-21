import numpy as np
import pandas as pd
from src.risk_decomp import correlation_matrix, component_var, diversification_ratio

rng = np.random.default_rng(42)
N = 500
RETURNS = pd.DataFrame({
    "SPY": rng.normal(0.0004, 0.012, N),
    "QQQ": rng.normal(0.0005, 0.015, N),
    "TLT": rng.normal(0.0001, 0.008, N),
    "GLD": rng.normal(0.0002, 0.007, N),
})
WEIGHTS = [0.4, 0.3, 0.2, 0.1]


def test_correlation_matrix_shape_and_diagonal():
    corr = correlation_matrix(RETURNS)
    assert corr.shape == (4, 4)
    assert np.allclose(np.diag(corr.values), 1.0)


def test_correlation_matrix_symmetric():
    corr = correlation_matrix(RETURNS)
    assert np.allclose(corr.values, corr.values.T)


def test_component_var_sums_to_portfolio_var():
    from src.risk_metrics import parametric_var
    from src.portfolio import portfolio_returns
    pf = portfolio_returns(RETURNS, WEIGHTS)
    total_pvar = parametric_var(pf, alpha=0.95)
    comp = component_var(RETURNS, WEIGHTS, alpha=0.95)
    assert abs(comp.sum() - total_pvar) < 1e-6


def test_component_var_length():
    comp = component_var(RETURNS, WEIGHTS)
    assert len(comp) == 4


def test_diversification_ratio_above_one():
    dr = diversification_ratio(RETURNS, WEIGHTS)
    assert dr >= 1.0
