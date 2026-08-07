---
type: concept
title: Volatility Measurement & Forecasting
description: Estimators of realized volatility, GARCH-family forecasts, and volatility cones for the distribution of future vol.
tags: [derivatives, volatility, statistics, forecasting]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Volatility Measurement & Forecasting

How to *measure* realized volatility and *forecast* it over a trade's life. Sinclair Ch. 2.

## Estimators of realized volatility
- **Close-to-close** — standard, but noisy (one price per day).
- **Parkinson** — uses the high–low range; more efficient, but ignores gaps and drift.
- **Garman–Klass** — uses OHLC; more efficient still.
- **Rogers–Satchell** — handles non-zero drift.
- **Yang–Zhang** — combines overnight + intraday; handles gaps and drift; most efficient.

Each is biased differently by **trends, opening gaps, fat tails, and microstructure noise**.
Higher-frequency data improves efficiency but reintroduces microstructure noise.

## Forecasting
- Simple moving windows, **EWMA**, and the **GARCH** family (captures vol clustering and mean
  reversion).
- For trading you need more than a point estimate: **volatility cones** give the sampling
  distribution of realized vol by horizon, so you can judge whether current
  [IV](implied-vs-realized-volatility.md) is high or low *relative to the plausible range* of RV.

## Relationships
- Supplies the RV forecast that [implied vs. realized volatility](implied-vs-realized-volatility.md)
  and [volatility arbitrage](../strategies/volatility-arbitrage.md) trade against.
- The forecasting-and-uses side of the same object — HAR-RV, asymmetric GARCH, vol targeting,
  event pre-staging, honest limits: [volatility forecasting](../../ml-stats/concepts/volatility-forecasting.md)
  (division of labor: estimators + cones live here; models + uses live there).

## Open questions
- Which estimator / forecast combination is most robust for the products you actually trade?

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Ch. 2.
