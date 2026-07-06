import numpy as np
import pandas as pd
from src.backtesting import rolling_var_backtest, exception_rate, kupiec_pof, traffic_light

rng = np.random.default_rng(1)
RETURNS = pd.Series(rng.normal(-0.0005, 0.015, 500))


def test_rolling_backtest_length():
    window = 100
    result = rolling_var_backtest(RETURNS, window=window, alpha=0.95)
    assert len(result) == len(RETURNS) - window


def test_rolling_backtest_columns():
    result = rolling_var_backtest(RETURNS, window=100)
    assert {"realized_return", "VaR", "exception"}.issubset(result.columns)


def test_exception_rate_in_range():
    result = rolling_var_backtest(RETURNS, window=100, alpha=0.95)
    rate = exception_rate(result)
    assert 0.0 <= rate <= 1.0


def test_kupiec_accepts_correct_rate():
    # 50 exceptions / 1000 obs = 5%, consistent with alpha=0.95
    result = kupiec_pof(50, 1000, alpha=0.95)
    assert not result["reject_H0"]


def test_kupiec_rejects_excess_exceptions():
    result = kupiec_pof(150, 1000, alpha=0.95)
    assert result["reject_H0"]


def test_traffic_light_zones():
    assert traffic_light(0) == "green"
    assert traffic_light(4) == "green"
    assert traffic_light(5) == "yellow"
    assert traffic_light(9) == "yellow"
    assert traffic_light(10) == "red"
