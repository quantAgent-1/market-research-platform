---
type: strategy
title: Optimal Execution
description: Liquidating or acquiring a large position over a window while balancing market impact against timing risk.
tags: [systematic-trading, optimal-execution, stochastic-control]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Optimal Execution

How to trade a large order over a fixed window so that aggressive trading (high
[market impact](../../shared/concepts/transaction-costs.md)) is balanced against slow trading
(exposure to price / **timing risk**). Posed as a
[stochastic optimal control](../../shared/concepts/stochastic-optimal-control.md) problem.
Cartea–Jaimungal–Penalva Part III (Ch. 6–9).

## Key points
- **Almgren–Chriss baseline:** with linear temporary + permanent impact and mean–variance
  preferences, the optimal schedule trades expected cost against variance — risk-neutral → uniform
  (TWAP-like), risk-averse → front-loaded. (Robert Almgren is acknowledged in the book.)
- **Cartea et al. extensions (Ch. 6–8):** continuous trading with urgency / inventory penalties;
  execution that stops at a critical price boundary; incorporating **order flow** to ride
  short-term trends; trading across a **lit venue and a dark pool**; and execution with **limit +
  market orders** rather than market orders only.
- **Schedule targeting (Ch. 9):** Percentage of Volume (POV), Percentage of Cumulative Volume, and
  **VWAP** — track market volume to minimise footprint.

## Relationships
- Operates on the [limit order book](../concepts/limit-order-book.md); shares impact modelling with
  [market making](market-making.md) and the
  [transaction-cost](../../shared/concepts/transaction-costs.md) page.
- Solved with the same [control machinery](../../shared/concepts/stochastic-optimal-control.md) as
  market making — see the [cost-aware trading](../../synthesis/cost-aware-trading.md) synthesis.

## Open questions
- How robust are impact-model parameters across regimes and assets?

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Ch. 6–9.
