# Portfolio Risk – VaR, Expected Shortfall and Backtesting

Projet Python de mesure du risque de marché appliqué à un portefeuille financier diversifié.

## Objectif

L’objectif du projet est de comparer plusieurs mesures de risque sur un portefeuille d’actifs financiers :
- Historical Value at Risk (VaR)
- Parametric Value at Risk (VaR)
- Expected Shortfall (ES)

Le projet inclut également un backtesting sur fenêtre glissante afin d’évaluer la robustesse des estimations de VaR.

## Univers étudié

Le portefeuille est composé de quatre ETF représentatifs de différentes classes d’actifs :
- SPY
- QQQ
- TLT
- GLD

Exemple de pondération :
- 40 % SPY
- 30 % QQQ
- 20 % TLT
- 10 % GLD

## Méthodologie

### 1. Préparation des données
- téléchargement des prix historiques via `yfinance`
- calcul des rendements journaliers
- construction des rendements du portefeuille

### 2. Mesures de risque
- **VaR historique** : estimation empirique du quantile de perte
- **VaR paramétrique** : estimation sous hypothèse de normalité
- **Expected Shortfall** : perte moyenne au-delà du seuil de VaR

### 3. Backtesting
- estimation de la VaR sur fenêtre glissante de 252 jours
- comparaison avec les pertes réalisées
- calcul du taux d’exceptions

## Structure du projet

```text
portfolio-risk-var-backtesting/
│
├── notebooks/
│   └── risk_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── portfolio.py
│   ├── risk_metrics.py
│   └── backtesting.py
├── figures/
├── README.md
├── requirements.txt
└── .gitignore