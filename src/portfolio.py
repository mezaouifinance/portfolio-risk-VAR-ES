import pandas as pd
import numpy as np


def portfolio_returns(asset_returns: pd.DataFrame, weights: list[float]) -> pd.Series:
    weights_array = np.array(weights)

    if len(weights_array) != asset_returns.shape[1]:
        raise ValueError("Number of weights must match number of assets.")

    if not np.isclose(weights_array.sum(), 1.0):
        raise ValueError("Weights must sum to 1.")

    return asset_returns.dot(weights_array)