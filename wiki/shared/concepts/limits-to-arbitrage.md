---
type: concept
title: Market Efficiency & the Limits to Arbitrage
description: Why public markets are neither perfectly efficient nor freely beatable — arbitrage is scarce, leveraged, and flees when mispricing is widest, so edges persist without being free.
tags: [systematic-trading, derivatives, market-efficiency, behavioral]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/deep-research-long-term-profitability.md]
---

# Market Efficiency & the Limits to Arbitrage

The efficient-market hypothesis (EMH) says prices reflect available information, so consistent edge
should be competed away. The empirical record says edges **persist** — and the reconciliation is the
*limits to arbitrage*.

## The core mechanism (Shleifer & Vishny 1997)
Textbook arbitrage assumes many diversified investors each take small corrective positions. In
reality, arbitrage is performed by **"a relatively small number of highly specialized investors
using other people's money."** Because they run leveraged client capital judged on short-horizon
performance, their arbitrage **"becomes ineffective in extreme circumstances, when prices diverge
far from fundamental value"** — they are forced to *withdraw* capital exactly when mispricing (and
expected return) is greatest. So mispricing is bounded but not eliminated.

## Key points
- **Edges neither vanish nor stay free.** Arbitrage pushes prices *toward* fair value, not *to* it —
  leaving a residual, [decaying premium](factor-premia-and-alpha-decay.md).
- **Crowding and forced deleveraging are real risks**, not tail abstractions: LTCM (1998) and the
  August 2007 "quant quake" are the canonical realizations.
- **Implication for a trader:** an edge survives *because* of structural/behavioral frictions — so
  understanding *who is forced to trade against you, and when,* is itself part of the edge.

## Relationships
- Explains why [factor premia](factor-premia-and-alpha-decay.md) persist yet decay once crowded.
- The flip side of [transaction costs & market impact](transaction-costs.md): frictions both
  *create* and *cap* opportunity.
- Behavioral mistakes (overconfidence, the [disposition effect](disposition-effect.md)) supply the
  mispricing — see [who actually wins](who-wins-empirical-record.md).

## Open questions
- How wide can mispricing get before arbitrage capital returns — and can that boundary be traded?

## Sources
- [Deep-research brief (2026)](../../sources/deep-research-long-term-profitability.md) — Shleifer &
  Vishny (1997, *J. Finance*), "The Limits of Arbitrage."
