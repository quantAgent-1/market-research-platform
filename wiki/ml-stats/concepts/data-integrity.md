---
type: concept
title: "Data Integrity (Survivorship & Look-Ahead Bias)"
description: Garbage-in edge — survivorship, look-ahead, and non-point-in-time data silently manufacture backtest profits that don't exist live.
tags: [ml-stats, methodology, data]
timestamp: 2026-06-13T00:00:00Z
status: stub
sources: [../../sources/deep-research-long-term-profitability.md]
---

# Data Integrity (Survivorship & Look-Ahead Bias)

Every downstream number inherits the flaws of its data. Three biases manufacture phantom edge:

## The three classic biases
- **Survivorship bias:** dropping dead/delisted names inflates returns. The credibility of
  [SPIVA's](../../shared/concepts/who-wins-empirical-record.md) damning active-management verdict
  rests precisely on *keeping liquidated funds in the denominator* — most casual datasets don't.
- **Look-ahead bias:** using information not knowable at decision time (restated fundamentals;
  trading "today's close" on a signal computed from that same close). The subtlest and most common
  killer.
- **Point-in-time failure:** judging the past with today's index membership, today's adjusted
  prices, or today's corporate-action data.

## The non-negotiable
- Use **point-in-time, bias-free** data, with delisted names retained and timestamps that reflect
  *availability*, not publication. Without it, [backtest rigor](backtesting-overfitting.md) is moot —
  the inputs already lie.

## Relationships
- Precondition for [backtesting & overfitting](backtesting-overfitting.md) control; the data half of
  the [implementation pillar](../../synthesis/trading-system-fundamentals.md).

## Open questions
- Practical point-in-time data sources and reconstruction for an independent equities/options
  researcher.

## Sources
- [Deep-research brief (2026)](../../sources/deep-research-long-term-profitability.md).
