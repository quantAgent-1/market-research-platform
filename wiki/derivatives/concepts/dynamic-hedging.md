---
type: concept
title: Dynamic Hedging
description: Delta-hedging an option position so its P&L isolates the volatility bet, and the costs and path-dependency that introduces.
tags: [derivatives, volatility, options, hedging]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Dynamic Hedging

To turn an option position into a pure bet on
[realized volatility](volatility-measurement-forecasting.md), you continuously **delta-hedge** away
exposure to the underlying's direction and to rates. Sinclair Ch. 4–5.

## Key points
- **When to hedge** is a risk/reward problem: hedging reduces variance but incurs
  [transaction costs](../../shared/concepts/transaction-costs.md). Methods range from ad hoc
  (fixed time / fixed band) to **utility-based** rules (Ch. 4).
- **Discrete hedging** makes the P&L **path-dependent**: the realised outcome depends on the
  volatility used for delta estimation and the particular path the underlying takes (Ch. 5).
- Aggregating options across underlyings reduces the total hedging required.

## Relationships
- The mechanism that realises a [volatility arbitrage](../strategies/volatility-arbitrage.md) trade
  from an [IV–RV](implied-vs-realized-volatility.md) gap.
- Mirror image of execution: both manage
  [trading costs](../../shared/concepts/transaction-costs.md) under uncertainty — see the
  [cost-aware trading](../../synthesis/cost-aware-trading.md) synthesis.

## Open questions
- Optimal hedge bandwidth as a function of cost level and gamma?

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Ch. 4–5.
