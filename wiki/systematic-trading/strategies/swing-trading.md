---
type: strategy
title: Swing Trading
description: Multi-day-to-multi-week discretionary trading of liquid stocks. The honest evidence verdict — a real but fragile edge that mostly lives in the momentum factor, fails as technical rules in mature large-caps, and is governed by costs, decay, and risk discipline.
tags: [systematic-trading, swing-trading, momentum, equities]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: [../../sources/deep-research-swing-trading.md]
---

# Swing Trading

**Swing trading** holds positions for a few days to a few weeks to capture a "swing" in price —
between day-trading and long-horizon investing. The common archetypes: **breakout / momentum**
(incl. [52-week-high](../factors-signals/momentum.md)), **pullback / mean-reversion** to a moving
average (RSI-2, Bollinger), **single-name trend-following**, and **gap / earnings-catalyst** swings.

## The honest verdict (what the evidence supports)
Swing trading is **active trading**, and the
[base rate is unforgiving](../../shared/concepts/who-wins-empirical-record.md) (>80% of day traders
lose net of costs). On top of that, the
[2026 evidence review](../../sources/deep-research-swing-trading.md) finds:

- **The only serious edge is [momentum](../factors-signals/momentum.md)** — and it is fragile,
  cost-sensitive, capacity-limited, and
  [decaying](../../shared/concepts/factor-premia-and-alpha-decay.md), and strongest in *small/illiquid*
  stocks, not megacaps.
- **Technical price-action rules fail where it matters.** Moving-average / breakout rules that look
  great in-sample **vanish out-of-sample and on tradable S&P futures** once you correct for the
  thousands of rules searched (Sullivan-Timmermann-White) — and show **no surviving edge in mature
  US large-cap indices** (Hsu-Kuan). That is exactly where megacap semis trade.
- **Backtested/marketed "systems" are a
  [data-snooping](../../ml-stats/concepts/backtesting-overfitting.md) minefield** — a beautiful equity
  curve is the *expected* result of trying enough rules.

## What actually distinguishes the durable minority
Not a magic setup — **process and risk control**: a genuine (momentum-grounded) edge, ruthless
[cost awareness](../../shared/concepts/transaction-costs.md) (turnover kills short-hold returns),
disciplined [position sizing and survival](../../shared/concepts/risk-of-ruin.md) (volatility-based
stops, max-risk-per-trade, fractional-[Kelly](../../shared/concepts/kelly-criterion.md)), and trading
*with* the [regime](../../ml-stats/concepts/regime-detection.md) rather than against it. The
evidence-based exit side is [stop-losses & exit management](../../shared/concepts/stop-losses-and-exits.md)
(stops are regime-dependent — good for trend, bad for mean-reversion — and work best wide &
volatility-scaled), and the bias it counters is the
[disposition effect](../../shared/concepts/disposition-effect.md).

## How the winners actually win in megacap semis (reverse-engineered)
A [focused 2026 run](../../sources/deep-research-semi-rally-winners.md) reverse-engineered the
*durable* mechanisms (vs. luck). The defensible playbook:
1. **Identify the regime** — 200-day-MA trend + breadth; note *who leads* (the semi tape **broadened
   off NVDA in April 2026** — a late-stage tell). See [semiconductors](../../shared/instruments/semiconductors.md).
2. **Ride leaders with LOW turnover** — low-turnover conviction exposure costs **~3-4× less** than
   high-turnover momentum (≈61-76 vs 200-270 bps/yr); *holding* winners is the
   cheap edge, *flipping* them is the expensive trap.
3. **Anchor conviction to *real* fundamentals**, not price — e.g. NVDA's verified +62% revenue /
   ~90%-datacenter step-change, not just an up-chart.
4. **Size by volatility** — vol-targeting / dynamic sizing ~doubles momentum's risk-adjusted return
   and cuts the left tail ([regime detection](../../ml-stats/concepts/regime-detection.md)).
5. **Exit / hedge by regime** — momentum crashes are partly forecastable; concentrated high-beta semis
   carry severe earnings-gap / drawdown risk (NVDA −$600B in a day, Jan 2025).

**The honest catch:** in a sector up several hundred percent, **leveraged long beta + luck perfectly
mimic skill** — Fama-French show even ~90th-percentile track records are mostly consistent with zero
skill net of costs. So the durable edge is the *risk/regime discipline above*, not the gains
themselves; survivorship bias dominates any single winner's story, and a deep drawdown is effectively
inevitable.

## Open questions
- Net-of-cost performance of pullback/mean-reversion (RSI-2) and earnings-catalyst swings in liquid
  large-caps today (not verified in 2026).
- The single-name earnings-gap tail risk for semiconductor catalyst swings.

## Sources
- [Deep-research brief: swing trading & momentum (2026)](../../sources/deep-research-swing-trading.md).
