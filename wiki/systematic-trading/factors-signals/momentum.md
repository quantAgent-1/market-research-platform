---
type: factor
title: Momentum
description: Past winners keep winning over 3-12 months — the most-documented swing/trend edge in equities, but real net-of-cost profitability is contested, capacity-limited, and decaying.
tags: [systematic-trading, factor, momentum, equities]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: [../../sources/deep-research-swing-trading.md]
---

# Momentum

**Momentum** is the tendency of recent winners to keep outperforming recent losers over horizons of
~3-12 months. It is the academic backbone any breakout / trend / "swing" approach maps onto — and
the cleanest case study in how a real edge is qualified by costs and
[decay](../../shared/concepts/factor-premia-and-alpha-decay.md).

## The signal
The standard measure is **MOM2-12**: the past 12-month cumulative return **skipping the most recent
month** (to avoid 1-month return reversal). This convention defines Jegadeesh-Titman (1993),
Carhart (1997), and the Fama-French UMD factor (Asness-Moskowitz-Pedersen 2013).

## Variants with the best evidence
- **Cross-sectional momentum** (long past winners, short losers): Jegadeesh-Titman earns
  ~0.9-1%/mo gross.
- **52-week-high momentum** (George-Hwang 2004): rank by nearness to the 52-week high — W-L ~1.23%/mo
  (ex-Jan, 1963-2001) and it *statistically subsumes* JT momentum. This is the academic form of the
  classic **breakout** swing trade. *Caveat:* in-sample, US, gross — later work finds it small/
  insignificant for the US 1980-2014.
- **Time-series (trend) momentum** (own past return): *more contested* — Huang et al. (2020) find
  weak asset-level evidence, and where it pays it behaves like **net-long exposure**, not prediction
  (Goyal-Jegadeesh). AQR/D'Souza defend trend over 100+ years. Treat as a live debate.

## The catch: costs, capacity, decay
- **Net-of-cost survival is contested.** Equal-weighted momentum is *best gross, worst after costs*
  (it trades illiquid small caps). Liquidity-weighted momentum may survive to **~$5B capacity**
  (Korajczyk-Sadka 2004); Lesmond-Schill-Zhou (2004) call the standard strategy illusory after
  costs. Live-trade data (Frazzini et al. 2015) sides with implementability at scale.
- **It decays.** ~26% out-of-sample and ~58% post-publication
  ([alpha decay](../../shared/concepts/factor-premia-and-alpha-decay.md); McLean-Pontiff 2016).
- **It crashes.** Momentum has rare, severe crashes in sharp rebounds (Daniel-Moskowitz) — acute for
  high-beta names; see [regime detection](../../ml-stats/concepts/regime-detection.md), whose later
  run **verified the magnitudes** (loser-decile rebounds +232% in 1932 / +163% in 2009), and
  [stop-losses & exits](../../shared/concepts/stop-losses-and-exits.md) for the crash-taming evidence
  (a 10% stop cutting the worst month). *(Resolves the "magnitude not verified" flag from the 2026 run.)*

## So is it a swing-trading edge?
Real but **fragile, cost-sensitive, capacity-limited, and decaying** — and strongest in
small/illiquid stocks, *not* the megacap large-caps most swing traders actually trade. See
[swing trading](../strategies/swing-trading.md) for the practical verdict.

## Relationships
- A specific [factor premium](../../shared/concepts/factor-premia-and-alpha-decay.md); eroded by
  [transaction costs](../../shared/concepts/transaction-costs.md); its backtests are a minefield of
  [data-snooping](../../ml-stats/concepts/backtesting-overfitting.md).

## Sources
- [Deep-research brief: swing trading & momentum (2026)](../../sources/deep-research-swing-trading.md)
  — Jegadeesh-Titman; Asness-Moskowitz-Pedersen (2013); George-Hwang (2004); Korajczyk-Sadka (2004);
  Lesmond-Schill-Zhou (2004); Huang et al. (2020); McLean-Pontiff (2016).
