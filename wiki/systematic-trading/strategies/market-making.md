---
type: strategy
title: Market Making
description: Quoting two-sided limit orders to earn the spread while managing inventory risk and adverse selection.
tags: [systematic-trading, market-making, stochastic-control]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Market Making

Continuously posting bid and ask [limit orders](../concepts/limit-order-book.md) to capture the
spread, while controlling **inventory risk** (unwanted directional exposure) and **adverse
selection** (being picked off by informed flow). Cartea–Jaimungal–Penalva Ch. 10.

## Key points
- The maker chooses how far from the mid to post each side; optimal quotes **skew** with current
  inventory to pull the position back toward zero.
- Trade-off: tighter quotes → more fills but more
  [adverse selection](../concepts/market-microstructure.md) and inventory risk; wider quotes →
  safer but fewer fills.
- Model drivers: inventory-risk aversion, adverse selection, and short-lived mid-price trends.
  Conceptually the Avellaneda–Stoikov / Cartea–Jaimungal line of work.
- A [stochastic optimal control](../../shared/concepts/stochastic-optimal-control.md) problem, dual
  in spirit to [optimal execution](optimal-execution.md) (posting vs. liquidating).

## Relationships
- Earns the spread defined by the [limit order book](../concepts/limit-order-book.md); exposed to
  the [microstructure](../concepts/market-microstructure.md) force of adverse selection.
- **Deep dive:** [prediction-first market making](../concepts/prediction-first-market-making.md) —
  the full mathematical reconstruction (fair-value engine, reservation price + alpha term, the
  GLFT skew formula, internalize-vs-hedge three-zone policy, toxicity pricing), reverse-engineered
  from the [XTX Markets](../../shared/people-firms/xtx-markets.md) record.

## Open questions
- How to set inventory limits when order-flow toxicity spikes?

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Ch. 10.
