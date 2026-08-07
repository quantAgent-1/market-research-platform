---
type: concept
title: Kelly Criterion
description: The bet-sizing rule that maximises long-run growth of capital; the foundation of money management.
tags: [derivatives, systematic-trading, money-management, risk]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/sinclair-volatility-trading.md]
---

# Kelly Criterion

The position-sizing rule that maximises the **long-run geometric growth rate** of capital. Sinclair
Ch. 6 argues sizing can matter more than selection, and that most option traders underuse it.

## Key points
- **Binary bet:** optimal fraction f* = p − q/b (edge over odds). **Continuous case** (the relevant
  one for trading): f* ≈ **expected excess return / variance**.
- **Full Kelly** maximises growth but with severe drawdowns; practitioners use **fractional Kelly**
  (e.g. half-Kelly) to cut variance at small growth cost — Sinclair's "alternatives to Kelly".
- Sinclair **extends Kelly** for a *continuum* of outcomes and for **mean-reverting** volatility,
  yielding simple scaling rules familiar to market makers.
- Watch **risk of ruin** and drawdowns; over-betting beyond f* lowers growth *and* raises risk.

## Relationships
- Provides the sizing step in
  [volatility arbitrage](../../derivatives/strategies/volatility-arbitrage.md) and applies to any
  positive-edge systematic strategy.
- Most Kelly research comes from gamblers (blackjack); the math is general.
- The survival counterpart is [risk of ruin](risk-of-ruin.md): over-betting past f* lowers growth
  *and* raises ruin probability.

## Open questions
- Estimating edge / variance robustly enough to trust the sizing (parameter uncertainty → shrink f).
- What fraction of Kelly do durable systematic traders actually use? Open item in the
  [2026 research brief](../../sources/deep-research-long-term-profitability.md) — assumed in theory,
  not yet evidenced.

## Sources
- [Volatility Trading (Sinclair 2008)](../../sources/sinclair-volatility-trading.md), Ch. 6.
