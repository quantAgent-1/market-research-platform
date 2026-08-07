---
type: checklist
title: Trading Risk Constitution
description: Written risk rules for live practice trading — two-book firewall, practice-book sizing, loss/tilt protocols, and breach handling. Generalized template; parameters are examples, not a personal account.
tags: [systematic-trading, risk, sizing, checklist]
timestamp: 2026-08-07T00:00:00Z
status: active
sources: []
---

# Trading Risk Constitution

A **written rulebook** so sizing and process are not improvised under stress. Grounded in [risk of ruin](../../shared/concepts/risk-of-ruin.md) and the [Kelly criterion](../../shared/concepts/kelly-criterion.md).

**Template for research/education.** Replace the example parameter table with your own numbers before any live use. Not investment advice.

## Article 1 — Two books that never mix

- **Thesis book:** multi-week to multi-month positions driven by a written research thesis and pre-committed invalidation ([conviction-swing](../strategies/conviction-swing-on-institutional-accumulation.md), [new-high checklist](new-high-trade-checklist.md)). Changes only through that process — never “fixed” mid-session from short-term P&L.
- **Practice book:** separate capital (or hard notional cap) used for short-horizon skill reps and process measurement.

Averaging a practice loss into “long-term conviction” is the named blowup mode this constitution exists to prevent.

## Article 2 — Practice-book sizing (example defaults)

| Rule | Example default |
|---|---|
| Per-trade risk (entry → falsifier) | 0.5% of practice equity (1% hard max) |
| Risk through a binary event (earnings, FOMC) | 0.25% max |
| Concurrent practice positions | ≤ 2, preferably one per market |
| Period loss wall | Pre-set % of practice equity; when hit, live practice stops — study continues |

Conviction is expressed by **taking the trade under the rules**, not by increasing size.

## Article 3 — Instruments

- Cash equities/ETFs unless a separate, written leverage policy exists.
- No margin that can force liquidation in the practice book.
- No overnight leverage products unless explicitly allowed and sized under Article 2.
- Never knowingly be the **forced** side of a cascade (see [KRX forced liquidation](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md), [liquidity cascades](../../shared/concepts/liquidity-cascades-and-v-reversals.md)).

## Article 4 — Entry discipline

No live practice fill without a completed [morning call sheet](morning-call-sheet.md): claim, confidence, falsifier, exit — **before** entry. A trade without a falsifier is a breach even if it wins.

## Article 5 — Loss protocols

- Two consecutive red practice days → next day **half size**.
- Three consecutive red days → **flat 24h** + written incident note.
- Period loss wall → live practice closed for the period (no renegotiation).

## Article 6 — Tilt tripwires (mechanical)

Flatten practice book and stop trading if any occur:

- Falsifier/stop deleted or widened after entry
- Size increased immediately after a loss
- Re-entry within minutes of a stop-out in the same name
- Compulsive P&L checking with no decision pending

## Article 7 — Biology as data quality

Sleep floor (example: 6 hours). Below the floor → paper only. Tired trading poisons calibration data.

## Article 8 — Measurement

Log fills vs decision price (slippage). Score **process** (pre-committed calls, checklist adherence, zero breaches). Short-window P&L is recorded but is not the primary grade when samples are small.

## Article 9 — Breach protocol

Any article breached → halt live practice 24h + same-day incident note. Second breach in the period ends live practice for that period. Losing money **while following the rules** is variance, not failure; breaking rules for a win is failure.

## Example parameter block (fill in; do not leave blank in live use)

```text
practice_equity_unit: <set>
per_trade_risk_pct: 0.5
event_risk_pct: 0.25
period_loss_wall_pct: 10
max_positions: 2
instruments: cash equities/ETFs
```

## Related

- [Morning call sheet](morning-call-sheet.md) · [Tripwire exit machine](tripwire-exit-execution.md)
- [Who is selling? diagnostic](who-is-selling-diagnostic.md) · [Retail-capital edge program](../../synthesis/retail-capital-edge-program.md)
