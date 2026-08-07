---
type: thesis
title: "Cost-Aware Trading: Execution and Hedging as the Same Problem"
description: A synthesis connecting optimal execution (Cartea et al.) and dynamic hedging (Sinclair) as cost-vs-risk control problems.
tags: [systematic-trading, derivatives, execution, hedging, synthesis]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../sources/cartea-jaimungal-penalva-2015-algo-hft.md, ../sources/sinclair-volatility-trading.md]
---

# Cost-Aware Trading: Execution and Hedging as the Same Problem

The first two ingested books come from different worlds — equity microstructure vs. options
volatility trading — yet they pose **the same problem**: act repeatedly in the market to achieve an
objective while paying [transaction costs](../shared/concepts/transaction-costs.md) and bearing risk
from *not* acting fast enough.

## The shared structure

| | [Optimal execution](../systematic-trading/strategies/optimal-execution.md) (Cartea et al.) | [Dynamic hedging](../derivatives/concepts/dynamic-hedging.md) (Sinclair) |
|---|---|---|
| Goal | Liquidate / acquire a position | Keep delta ≈ 0 to isolate the vol bet |
| Cost of acting | [Market impact](../shared/concepts/transaction-costs.md) + spread | Hedge transaction costs |
| Cost of waiting | Price / timing risk | Path-dependent P&L drift |
| Lever | Trade rate / order type | Hedge frequency / band |

## The connection
- Both are, at heart, **trade-frequency vs. cost-vs-risk** trade-offs. Cartea et al. solve theirs
  formally with [stochastic optimal control](../shared/concepts/stochastic-optimal-control.md);
  Sinclair solves his with utility-based and ad hoc rules — but the economic structure is identical.
- Natural cross-pollination: apply the book's control machinery to the **optimal hedging-band**
  problem, or apply Sinclair's cost-estimation pragmatism to execution.
- Sizing ties them together too: the [Kelly criterion](../shared/concepts/kelly-criterion.md) sizes
  the *bet*; execution / hedging controls the *cost of expressing it*.

## Open threads
- Formal optimal-hedging-band model via HJB (bridge Sinclair ↔ Cartea et al.).
- Add a microstructure-aware cost model to the vol-arb workflow.

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../sources/cartea-jaimungal-penalva-2015-algo-hft.md)
- [Volatility Trading (Sinclair 2008)](../sources/sinclair-volatility-trading.md)
