---
type: concept
title: Implied vs. Realized Volatility
description: The gap between volatility priced into options and volatility the underlying actually delivers — the core of volatility trading.
tags: [derivatives, volatility, options]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Implied vs. Realized Volatility

- **Implied volatility (IV):** the volatility the market backs out of option prices via
  Black–Scholes–Merton — a forward-looking *price*.
- **Realized (historical) volatility (RV):** the volatility the underlying actually exhibits,
  estimated from returns — see [measurement & forecasting](volatility-measurement-forecasting.md).

Sinclair's central thesis: **the largest source of edge in options is trading your forecast of
future RV against the market's IV.** If forecast RV > IV, options look cheap (buy vol, delta-hedge);
if forecast RV < IV, options look rich (sell vol, delta-hedge).

## Key points
- The strategy that monetises an IV–RV gap is
  [volatility arbitrage](../strategies/volatility-arbitrage.md), realised through
  [dynamic hedging](dynamic-hedging.md).
- IV usually trades above RV on average — the [**volatility / variance risk premium**](volatility-risk-premium.md).
  Selling vol has a structural edge (large for the *index*, small for single names) but with negative
  skew / tail risk.
- A point RV forecast is insufficient; use the *distribution* (volatility cones) to judge
  risk/reward — see [measurement & forecasting](volatility-measurement-forecasting.md).

## Relationships
- IV's shape across strike / expiry is the [volatility smile](volatility-smile-dynamics.md).
- The deep evidence on the IV>RV gap lives in [volatility / variance risk premium](volatility-risk-premium.md).

## Open questions
- How much of the VRP is compensation for risk vs. behavioural mispricing? **Both** — academic
  evidence puts >½ on jump/crash-tail risk, with a real demand/behavioural component on top
  ([VRP](volatility-risk-premium.md)).
- *(Resolved 2026-06-14)* the VRP edge — flagged in 2026 as practitioner-only — is now backed by
  top-tier evidence via a [focused deep-research run](../../sources/deep-research-volatility-risk-premium.md);
  the remaining gap is **post-2010 / net-of-cost** magnitude.

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Introduction and Ch. 1–3.
