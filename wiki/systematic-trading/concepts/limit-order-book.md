---
type: concept
title: Limit Order Book (LOB)
description: The electronic record of resting buy/sell limit orders that defines price and liquidity in modern markets.
tags: [systematic-trading, microstructure]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Limit Order Book (LOB)

The central data structure of an electronic exchange: the set of outstanding **limit orders** to
buy (bids) and sell (asks) at each price level. The best bid and best ask define the **quoted
spread**; the **mid-price** is their average. Orders match by price–time priority.

## Key points
- Two order types drive everything: **limit orders** (post liquidity, join the book, earn the
  spread, risk non-execution) and **market orders** (take liquidity, cross the spread, pay it).
- **Depth** = volume resting at each level; thin books mean larger
  [market impact](../../shared/concepts/transaction-costs.md).
- The LOB is where [market making](../strategies/market-making.md) (posting) and
  [optimal execution](../strategies/optimal-execution.md) (a mix of posting and crossing) play out.
- Cartea–Jaimungal–Penalva Ch. 1 builds the LOB as the foundation for every model in the book.

## Relationships
- Governed by the rules studied in [market microstructure](market-microstructure.md).
- Order flow and order imbalance in the book carry short-term price information exploited by
  execution and market-making algos.

## Open questions
- How do queue position and cancellation dynamics change optimal posting? (Cartea et al. Ch. 8, 12)

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Ch. 1.
