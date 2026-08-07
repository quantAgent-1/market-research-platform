---
type: concept
title: Stochastic Optimal Control & Stopping
description: The mathematical engine for deriving trading strategies as solutions to dynamic optimisation problems (HJB equations).
tags: [systematic-trading, stochastic-control, mathematics]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/cartea-jaimungal-penalva-2015-algo-hft.md]
---

# Stochastic Optimal Control & Stopping

The toolkit for choosing a *strategy* (a control — e.g. trading rate or quote placement) that
optimises an objective under uncertainty over time. Cartea–Jaimungal–Penalva Ch. 5 + Appendix A
teach it from scratch so the strategy chapters can be *derived* rather than asserted.

## Key points
- **Value function + HJB equation:** dynamic programming yields a Hamilton–Jacobi–Bellman PDE whose
  solution gives the optimal control as a feedback rule on the state (time, inventory, price).
- **Optimal stopping:** choose *when* to act (enter / exit / liquidate) — the basis for timing
  trades.
- States typically include **inventory** and **time remaining**; controls are trade rate or quote
  offsets; objectives trade expected cost / PnL against risk.

## Where it's used (this wiki)
- [Optimal execution](../../systematic-trading/strategies/optimal-execution.md) — control = trading speed.
- [Market making](../../systematic-trading/strategies/market-making.md) — control = bid/ask offsets.
- [Pairs trading & stat-arb](../../systematic-trading/strategies/pairs-trading-statarb.md) — optimal entry/exit (stopping).

## Open questions
- Robust control under model uncertainty when impact and dynamics are mis-specified.

## Sources
- [Algorithmic and High-Frequency Trading (Cartea et al. 2015)](../../sources/cartea-jaimungal-penalva-2015-algo-hft.md), Ch. 5 and Appendix A.
