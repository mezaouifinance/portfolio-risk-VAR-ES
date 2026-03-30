import pandas as pd
import numpy as np


def portfolio_returns(asset_returns: pd.DataFrame, weights: list[float]) -> pd.Series:
    weights_array = np.array(weights)

    if len(weights_array) != asset_returns.shape[1]:
        raise ValueError("Le nombre de poids doit correspondre au nombre d'actifs.")

    if not np.isclose(weights_array.sum(), 1.0):
        raise ValueError("La somme des poids doit être égale à 1.")

    return asset_returns.dot(weights_array)