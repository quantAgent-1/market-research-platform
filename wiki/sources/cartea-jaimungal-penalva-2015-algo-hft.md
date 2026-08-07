---
type: book
title: "Algorithmic and High-Frequency Trading (Cartea, Jaimungal & Penalva, 2015)"
description: Graduate text deriving stochastic-control models for execution, market making, and stat-arb, grounded in market microstructure.
resource: # primary source not redistributed
tags: [systematic-trading, microstructure, optimal-execution, market-making, stochastic-control, book]
timestamp: 2026-06-13T00:00:00Z
status: active
---

# Algorithmic and High-Frequency Trading

**Authors:** Álvaro Cartea (UCL), Sebastian Jaimungal (U. Toronto), José Penalva (U. Carlos III de Madrid)
**Publisher:** Cambridge University Press, 2015 · ISBN 978-1-107-09114-6 · 360 pp.
**Companion:** algorithmic-trading.org (datasets + MATLAB code)
**Source file:** `(primary source on file privately — not redistributed)`

## What it is
The first textbook to combine rigorous stochastic-control modelling, empirical microstructure
facts, and financial economics for algorithmic trading. It takes the reader from how electronic
exchanges work to research-grade models for execution, market making, and statistical arbitrage.
Assumes basic continuous-time finance; teaches stochastic optimal control from scratch (Ch. 5 +
Appendix A). US equities are the running empirical example.

## Structure
- **Part I — Microstructure & empirical facts (Ch. 1–4):** the [limit order book](../systematic-trading/concepts/limit-order-book.md),
  market participants and [microstructure](../systematic-trading/concepts/market-microstructure.md)
  (adverse selection, informed vs. liquidity traders), and stylised statistical facts of prices,
  returns, volume, and market quality.
- **Part II — Measurement tools (Ch. 5):** [stochastic optimal control and stopping](../shared/concepts/stochastic-optimal-control.md)
  — the mathematical engine for the rest of the book.
- **Part III — Strategies (Ch. 6–12):** [optimal execution](../systematic-trading/strategies/optimal-execution.md)
  (continuous; limit + market orders; VWAP/POV targeting; lit + dark venues),
  [market making](../systematic-trading/strategies/market-making.md),
  [pairs trading & stat-arb](../systematic-trading/strategies/pairs-trading-statarb.md), and
  order-imbalance–based execution.

## Why it matters here
The canonical reference for the *model-based* approach to execution and market making — strategies
derived as solutions to control problems (HJB equations) rather than heuristics. Robert Almgren (of
Almgren–Chriss) is acknowledged; the book generalises that line of work.

## Key takeaways
- Microstructure (the LOB, adverse selection, order flow) determines the fate of any algorithm.
- Execution, market making, and stat-arb can all be posed as stochastic control problems trading
  off [transaction costs / market impact](../shared/concepts/transaction-costs.md) against
  timing/inventory risk.
- Empirical regularities (intraday volume/volatility/spread patterns) motivate model design.

## Caveats & limitations
- Published 2015 — the empirical microstructure snapshots (venue landscape, spreads, HFT share)
  predate the current market; the *control-theoretic framework* is the durable content.
- Models assume parameter knowledge (arrival rates, impact coefficients) that must be estimated
  from noisy data in practice; execution results are highly sensitive to those estimates.
- Institutional in orientation — the latency/queue-position games it models are largely
  inaccessible (and irrelevant) at retail scale, where the takeaway is cost-awareness, not HFT.

## Links into the wiki
Feeds: [Limit order book](../systematic-trading/concepts/limit-order-book.md) ·
[Market microstructure](../systematic-trading/concepts/market-microstructure.md) ·
[Optimal execution](../systematic-trading/strategies/optimal-execution.md) ·
[Market making](../systematic-trading/strategies/market-making.md) ·
[Pairs trading & stat-arb](../systematic-trading/strategies/pairs-trading-statarb.md) ·
[Stochastic optimal control](../shared/concepts/stochastic-optimal-control.md) ·
[Transaction costs & market impact](../shared/concepts/transaction-costs.md)
