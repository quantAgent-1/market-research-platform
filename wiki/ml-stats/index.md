---
type: index
title: ML & Stats for Markets — Index
description: Time-series models, ML pipelines, feature engineering, regime detection.
tags: [ml-stats]
timestamp: 2026-07-07T00:00:00Z
---

# ML & Statistics for Markets

> Time-series models, ML pipelines, feature engineering, regime detection.

Conventional subfolders (create on demand): `models/`, `concepts/`, `pipelines/`.

## Models
_None yet._

## Concepts
- [Backtesting Rigor & Overfitting](concepts/backtesting-overfitting.md) — telling a real edge from a curve fit; multiple-testing, t≥3, deflated Sharpe, OOS/walk-forward.
- [Trading-System Performance Metrics](concepts/performance-metrics.md) — the scorecard for system strength (risk-adjusted return + drawdown/tail + a deflation gate); Sharpe is gameable, CVaR > VaR, the Deflated Sharpe Ratio separates edge from overfit.
- [Data Integrity (Survivorship & Look-Ahead Bias)](concepts/data-integrity.md) — bias-free, point-in-time data as the precondition for a trustworthy backtest.
- [Regime Detection](concepts/regime-detection.md) — trend filters, breadth, and the momentum-crash danger in high-beta names; verified Daniel-Moskowitz crash magnitudes + vol-targeting evidence.
- [Volatility Forecasting](concepts/volatility-forecasting.md) — the predictable second moment: clustering / leverage effect / mean reversion / long memory; EWMA → GARCH(1,1) → EGARCH/GJR, **HAR-RV** (the production standard; range-proxy route for daily-only data), IV net of the vol-risk premium, regime models (naive-gate caveat); the uses — **vol targeting** (Harvey 2018), vol-managed momentum (~2×, Daniel-Moskowitz), ruin/Kelly sizing, event pre-staging, the vol-control flow clock; limits — dispersion not direction, jumps untimed, crash-timing (LPPL genre) fails OOS. Division of labor with the derivatives *measurement* page (estimators + cones live there).
