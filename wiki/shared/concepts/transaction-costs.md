---
type: concept
title: Transaction Costs & Market Impact
description: The frictions — spread, fees, and price impact — that every trading and hedging strategy must pay and model.
tags: [systematic-trading, derivatives, execution, costs]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md, ../../sources/sinclair-volatility-trading.md]
---

# Transaction Costs & Market Impact

The frictions that erode strategy returns: the **quoted spread**, exchange **fees / rebates**, and
**market impact** — the adverse price move your own trading causes. A page where both ingested books
meet.

## Key points
- **Impact decomposition:** *temporary* impact (transient, from demanding liquidity) vs.
  *permanent* impact (information your trade reveals). Cartea et al. model both.
- In [optimal execution](../../systematic-trading/strategies/optimal-execution.md), impact is the
  cost you trade slower to reduce — balanced against timing risk.
- In [market making](../../systematic-trading/strategies/market-making.md), you *earn* the spread
  but pay via adverse selection.
- In options, [dynamic hedging](../../derivatives/concepts/dynamic-hedging.md) pays costs on every
  rebalance; Sinclair (Ch. 4) estimates them and uses them to decide **when to hedge**.
- **Turnover is the multiplier:** at scale, low-turnover strategies cost ~61-76 bps/yr vs ~200-270 bps
  for high-turnover [momentum](../../systematic-trading/factors-signals/momentum.md) — the empirical
  reason *holding* winners beats *flipping* them (Li et al., FAJ 2019).

## Why it matters
Costs set the boundary of what is profitable: the deviation band for stat-arb, the hedge frequency
for options, the urgency for execution. Modelling them well is often the difference between a
backtest and a live edge — see the [cost-aware trading](../../synthesis/cost-aware-trading.md)
synthesis.

**Empirically the single largest destroyer of returns:** the most-active retail households
underperformed the least-active by ~710 bp/yr — almost entirely costs, not stock selection
([who actually wins](who-wins-empirical-record.md)). Costs and capacity also bound how much capital
a [factor edge](factor-premia-and-alpha-decay.md) can hold before alpha decays to zero.

## Sources
- [Cartea et al. 2015](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md) — impact models, execution.
- [Sinclair 2008](../../sources/sinclair-volatility-trading.md), Ch. 4 — hedging-cost estimation.
- [Deep-research brief (2026)](../../sources/deep-research-long-term-profitability.md) — Barber &
  Odean (2000), the empirical cost drag.
