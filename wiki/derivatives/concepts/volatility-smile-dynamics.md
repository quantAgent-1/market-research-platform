---
type: concept
title: Volatility Smile Dynamics
description: How the implied-volatility surface is shaped across strike and expiry, and how it moves.
tags: [derivatives, volatility, options, skew]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Volatility Smile Dynamics

Black–Scholes assumes a single volatility, but the market prices a different
[implied vol](implied-vs-realized-volatility.md) at each strike and expiry — the **smile / skew**
(the surface). Sinclair Ch. 3 covers its normal shapes and how it moves over time and by strike.

## Key points
- **Level dynamics:** how the whole surface shifts up/down (often anti-correlated with the
  underlying for equity indices).
- **Smile / skew dynamics:** equity-index skew (puts richer than calls) arises from
  credit/leverage, actual return skewness, put buying as hedges, call buying as takeover hedges,
  and index skew from implied correlation.
- Sinclair extends BSM with **skewness and kurtosis** terms and gives rules of thumb for comparing
  vols across time and product.

## Trading use
- Understanding surface dynamics improves **execution and timing** even when the core trade is an
  [IV–RV](implied-vs-realized-volatility.md) bet, and informs which strikes to
  [hedge](dynamic-hedging.md) with.

## Relationships
- The surface prices the gap that [IV–RV](implied-vs-realized-volatility.md) trades and the
  [volatility risk premium](volatility-risk-premium.md) harvests; skew steepness is one of the
  crowd-positioning tells in [distribution & pullback tells](../../shared/concepts/distribution-and-pullback-tells.md).
- Execution side: which strikes to [hedge](dynamic-hedging.md) and how
  [smile-aware measurement](volatility-measurement-forecasting.md) feeds the forecast.

## Open questions
- How to separate genuine skew signal from supply/demand noise in thin option markets?

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Ch. 3.
