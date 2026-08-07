---
type: strategy
title: Pairs Trading & Statistical Arbitrage
description: Trading mean-reverting spreads between related assets, modelled in continuous time.
tags: [systematic-trading, stat-arb, mean-reversion]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Pairs Trading & Statistical Arbitrage

Going long one asset and short a related one so the position depends on the **spread** rather than
market direction, betting the spread mean-reverts. Cartea–Jaimungal–Penalva Ch. 11.

## Key points
- Model the spread as a mean-reverting process (e.g. Ornstein–Uhlenbeck); enter when it deviates,
  exit as it reverts.
- Cast as an optimal entry/exit (timing) problem solved with
  [stochastic control & optimal stopping](../../shared/concepts/stochastic-optimal-control.md).
- Execution still pays [transaction costs / impact](../../shared/concepts/transaction-costs.md),
  which bound the profitable deviation band.

## Relationships
- Shares the control / stopping toolkit with [optimal execution](optimal-execution.md) and
  [market making](market-making.md).
- Mean reversion of the spread is the same statistical idea exploited by many systematic factors.

## Open questions
- How to detect cointegration breakdown / regime change before the spread stops reverting?

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Ch. 11.
