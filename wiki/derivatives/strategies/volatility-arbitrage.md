---
type: strategy
title: Volatility Arbitrage
description: Monetising a gap between forecast realized volatility and option-implied volatility via a delta-hedged option position.
tags: [derivatives, volatility, options, relative-value]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Volatility Arbitrage

The core strategy of Sinclair's *Volatility Trading*: when your forecast of future **realized vol**
differs from the market's **[implied vol](../concepts/implied-vs-realized-volatility.md)**, take the
option side that is mispriced and [delta-hedge](../concepts/dynamic-hedging.md) so the P&L depends
on volatility, not direction.

## How it works
1. **Forecast RV** and its distribution —
   [measurement & forecasting](../concepts/volatility-measurement-forecasting.md) (estimators,
   GARCH, vol cones).
2. **Compare to IV.** Forecast RV > IV → buy options (long gamma); forecast RV < IV → sell options
   (short gamma).
3. **[Dynamic-hedge](../concepts/dynamic-hedging.md)** the delta; realised edge ≈ the difference
   between RV and the IV paid, minus
   [hedging costs](../../shared/concepts/transaction-costs.md).
4. **Size** with the [Kelly criterion](../../shared/concepts/kelly-criterion.md) and its safer
   variants.

## Key points
- Edge, variance, and **appropriate size** are the three pillars Sinclair insists on.
- Short-vol harvests the [volatility / variance risk premium](../concepts/volatility-risk-premium.md)
  but carries negative skew / tail risk; long-vol is the opposite.
- Discrete hedging makes realised P&L path-dependent, so the *expected* edge is not guaranteed on
  any single trade — diversify across products and time.

## Open questions
- Position sizing when vol is itself mean-reverting (Sinclair extends Kelly for exactly this).
- *(Resolved 2026-06-14)* the [volatility / variance risk premium](../concepts/volatility-risk-premium.md)
  is now verified against top-tier evidence ([brief](../../sources/deep-research-volatility-risk-premium.md)):
  the edge is **real but largely an *index* phenomenon**, **mostly crash-risk compensation**, and only
  **modest net of costs** (~0.68 Sharpe delta-hedged vs 0.32 for the S&P) with severe negative skew.
  Open: post-2010 magnitude; the unhedged-short-vol crash profile (2008 / Volmageddon / 2020).

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Ch. 1–6.
