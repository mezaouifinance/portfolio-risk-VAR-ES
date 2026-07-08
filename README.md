![CI](https://github.com/mezaouifinance/portfolio-risk-VAR-ES/actions/workflows/ci.yml/badge.svg)

# Portfolio Risk – VaR, Expected Shortfall and Backtesting

Projet Python de mesure du risque de marché appliqué à un portefeuille financier diversifié.

## Objectif

Comparer plusieurs mesures de risque sur un portefeuille d'actifs financiers et valider leur robustesse statistique :
- Historical Value at Risk (VaR)
- Parametric Value at Risk (VaR)
- Monte Carlo Value at Risk (VaR)
- Expected Shortfall (ES / CVaR)

Backtesting sur fenêtre glissante avec test statistique de Kupiec et feux tricolores Bâle II.

## Univers étudié

Portefeuille de quatre ETF représentatifs de différentes classes d'actifs :

| Ticker | Classe | Poids |
|--------|--------|-------|
| SPY | Actions US | 40 % |
| QQQ | Tech US | 30 % |
| TLT | Obligations LT | 20 % |
| GLD | Or | 10 % |

## Méthodologie

### 1. Préparation des données
- téléchargement des prix historiques via `yfinance`
- rendements journaliers log
- construction des rendements pondérés du portefeuille

### 2. Mesures de risque

| Méthode | Description |
|---------|-------------|
| VaR historique | quantile empirique des pertes |
| VaR paramétrique | hypothèse de normalité (μ, σ) |
| VaR Monte Carlo | simulation sous distribution historique |
| Expected Shortfall | perte moyenne au-delà du seuil de VaR |

### 3. Backtesting

- VaR estimée sur fenêtre glissante de 252 jours
- comparaison avec les pertes réalisées
- **test de Kupiec (POF)** : test du chi² sur le taux d'exceptions observé
- **feux tricolores Bâle II** : classification sur fenêtre de 250 jours

```
Vert  : 0–4 exceptions   → modèle vraisemblablement correct
Jaune : 5–9 exceptions   → zone d'incertitude
Rouge : ≥ 10 exceptions  → modèle rejeté
```

## Structure du projet

```
portfoliorisk/
├── src/
│   ├── data_loader.py     # téléchargement via yfinance
│   ├── portfolio.py       # construction des rendements pondérés
│   ├── risk_metrics.py    # VaR (hist, param, MC), ES
│   └── backtesting.py     # rolling backtest, Kupiec, traffic light
├── tests/
│   ├── test_risk_metrics.py
│   └── test_backtesting.py
├── notebook/
│   └── risk_analysis.ipynb
├── figures/
├── requirements.txt
└── .github/workflows/ci.yml
```

## Installation

```bash
git clone https://github.com/mezaouifinance/portfolio-risk-VAR-ES.git
cd portfolio-risk-VAR-ES
pip install -r requirements.txt
```

## Usage

```python
from src.data_loader import load_prices, compute_returns
from src.portfolio import portfolio_returns
from src.risk_metrics import historical_var, parametric_var, mc_var, expected_shortfall
from src.backtesting import rolling_var_backtest, kupiec_pof, traffic_light

prices = load_prices(["SPY", "QQQ", "TLT", "GLD"], start="2018-01-01")
returns = compute_returns(prices)
pf = portfolio_returns(returns, weights=[0.4, 0.3, 0.2, 0.1])

var_h  = historical_var(pf, alpha=0.99)
var_p  = parametric_var(pf, alpha=0.99)
var_mc = mc_var(pf, alpha=0.99, seed=42)
es     = expected_shortfall(pf, alpha=0.99)

backtest = rolling_var_backtest(pf, window=252, alpha=0.99)
n_exc = backtest["exception"].sum()
print(kupiec_pof(n_exc, len(backtest), alpha=0.99))
print(traffic_light(n_exc))
```

## Tests

```bash
pytest tests/ -q
```
