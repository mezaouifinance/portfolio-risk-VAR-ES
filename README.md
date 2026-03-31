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

### Distribution des rendements du portefeuille

![Distribution des rendements du portefeuille](figures/returns_distribution.png)

La distribution des rendements est centrée autour de 0, ce qui signifie que les variations journalières du portefeuille sont le plus souvent modestes.  
La majorité des observations se concentre près de 0, mais quelques valeurs plus extrêmes apparaissent dans les queues de distribution.  
Cela justifie l’utilisation de mesures comme la VaR et l’Expected Shortfall pour quantifier le risque de pertes extrêmes.

### Backtesting de la VaR historique

![Backtesting de la VaR historique](figures/backtest_historical_var.png)

Ce graphique compare les pertes réalisées à la VaR historique estimée sur fenêtre glissante.  
Les points d’exception correspondent aux jours où la perte réalisée dépasse le seuil de VaR.  
Leur fréquence restant proche du niveau théorique attendu, la VaR historique fournit ici une estimation globalement cohérente du risque.

### Backtesting de la VaR paramétrique

![Backtesting de la VaR paramétrique](figures/backtest_parametric_var.png)

Ce graphique montre le backtesting de la VaR paramétrique sous hypothèse de normalité.  
Comme son niveau est proche de celui de la VaR historique, les deux approches donnent ici des résultats voisins sur l’échantillon étudié.  
Le taux d’exceptions observé suggère que cette approche fournit elle aussi une estimation globalement acceptable du risque.

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
