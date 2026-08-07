---
type: concept
title: Market Microstructure
description: How market rules, participants, and information shape price formation, liquidity, and adverse selection.
tags: [systematic-trading, microstructure]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Market Microstructure

The study of how the *mechanics* of trading — order types, the
[limit order book](limit-order-book.md), participant behaviour, and information asymmetry —
determine prices, spreads, and liquidity at short horizons. Part I of Cartea–Jaimungal–Penalva.

## Key points
- **Participant types:** informed traders (trade on an informational edge), liquidity/noise
  traders, and [market makers](../strategies/market-making.md) who quote both sides.
- **Adverse selection:** market makers lose to better-informed counterparties; the spread is
  partly compensation for this risk. A central driver of market-making models.
- **Order imbalance / order flow:** one-sided pressure in the book predicts short-term mid-price
  moves (Cartea et al. Ch. 7, 12) and is used to improve execution.
- **Stylised empirical facts (Ch. 3–4):** fat-tailed returns, volatility clustering, intraday
  U-shaped volume/spread patterns, and the price impact of trades.

## Relationships
- Provides the assumptions behind [optimal execution](../strategies/optimal-execution.md),
  [market making](../strategies/market-making.md), and
  [transaction-cost / impact models](../../shared/concepts/transaction-costs.md).

## Open questions
- How stable are order-imbalance signals out-of-sample and across venues?

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Part I (Ch. 1–4) and Ch. 12.
