---
type: concept
title: Stop-Losses & Exit Management
description: When to stop, hold, or add to a losing position. Stops are regime-dependent (proven bad under random-walk/mean-reversion, good under momentum), are risk-control not alpha, and work best wide and volatility-scaled.
tags: [systematic-trading, derivatives, risk, position-management]
timestamp: 2026-06-21T00:00:00Z
status: active
sources: [../../sources/deep-research-losing-position-management.md, ../../sources/deep-research-stop-loss-optimization-2026.md]
---

# Stop-Losses & Exit Management

How to handle a position that has moved against you. The headline: **there is no universal rule — the
right action depends on your return process and whether your thesis still holds**, and a stop is a
*risk-control* tool, not a source of return.

## Stops are regime-dependent (proven)
[Kaminski & Lo (2014)](../../sources/deep-research-losing-position-management.md) prove the "stopping
premium" = −p₀·π:
- **Random walk (IID): a stop ALWAYS reduces expected return** (it just ejects you from a
  positive-return asset).
- **Mean-reversion: stops hurt** (they sell right before the bounce).
- **Momentum / positive autocorrelation: stops add value**, proportional to the persistence.

So the first question for any losing position is **"what process am I trading?"** — a price stop fits a
[momentum/trend](../../systematic-trading/factors-signals/momentum.md) trade and fights a
mean-reversion/value one.

## Tight stops whipsaw; wide stops work (net of costs)
- Lo & Remorov (2017): on individual US stocks, **tight stops underperform buy-and-hold** because of
  trading costs ("death by a thousand cuts") — they only beat it where serial correlation is high.
- Dai et al. (2021), 90 years of CRSP: trailing stops **cut risk, not return**; a **1% stop is worse
  than benchmark**, a **~20% trailing threshold** is optimal net of costs.
- **Lesson:** treat stops as downside insurance and place them **wide & volatility-scaled** (ATR-
  style), beyond normal noise — never at a tight round number or at your pain threshold.

## Deeper evidence (2026): frequency, granularity & the crash-taming case
A [follow-up brief](../../sources/deep-research-stop-loss-optimization-2026.md) sharpened the picture:
- **It's also a *frequency* and *granularity* question, not only regime.** Stops **add value for
  index/asset-allocation at monthly+ frequency** (Kaminski-Lo: one calibration **+~1.5% return / −5% vol /
  +20% Sharpe**; +50-100 bps/mo during stop-out periods) but give **negative** stopping premiums at high
  frequency — and on **individual stocks, tight stops lose to costs** (Lo-Remorov) unless the name is
  strongly autocorrelated.
- **Crash insurance is the clearest win:** a **10% stop on momentum** cut its worst month
  **−49.79% → −11.36%** and **more than doubled its Sharpe** (≈0.17→0.37 EW per the paper; an independent CXO review reports up to ~0.50 by stop level) (Han-Zhou-Zhu) — **but gross
  of costs**; the **net-of-cost survival claim was *refuted***, and the result may lean on a few crash
  months. Use stops to **cap the left tail**, not to add alpha net of costs.
- **The strongest case for a stop is behavioral discipline.** A stop is **associated with a reduced**
  [disposition effect](disposition-effect.md) — Richards et al. find stops "inoculate against" it (though
  stop-users are also a self-selected, less-experienced group, so *mechanism vs selection* is contested) —
  and the **least successful pros hold losers longest** (Locke-Mann). The value is in
  *overriding a costly bias*, not in the price level itself.

## The decision framework
1. **Decide the exit at entry** (thesis, invalidation condition, stop, size) — when calm.
2. **Action = edge type × thesis validity × sizing:**
   - momentum/trend → wide price stop (+ re-entry on a fresh signal);
   - mean-reversion/value, thesis intact → thesis-invalidation exit, add only if pre-planned with a
     **total-size cap**;
   - thesis broken or survival threatened → cut, regardless of the loss.
3. **Sizing is the master control** — see [risk of ruin](risk-of-ruin.md) / [Kelly](kelly-criterion.md);
   correct sizing is what makes a drawdown *boring*.
4. **Sunk-cost-free test:** "would I open this at this price today?"
5. **Pre-commit + score process** to neutralize the [disposition effect](disposition-effect.md) —
   willpower is unreliable.

## Relationships
- The exit half of [risk of ruin](risk-of-ruin.md); regime-conditioned by
  [regime detection](../../ml-stats/concepts/regime-detection.md); the antidote to the
  [disposition effect](disposition-effect.md); applied in
  [swing trading](../../systematic-trading/strategies/swing-trading.md).

## Open questions
- **Options-specific exits** (theta/gamma/vega, defined-risk, rolling) — the equity stop math doesn't
  transfer; unverified, flagged in the
  [brief](../../sources/deep-research-losing-position-management.md).
- Does systematic **re-entry / stop-and-reverse** recover whipsaw net of costs?
- **How to SET width in practice** — a head-to-head of ATR/σ-multiples vs % vs chart/swing-low vs
  account-risk-% vs time-based, and the tight-vs-wide tradeoff — remains thin (the evidence establishes
  *whether/when* stops help, less *how* to size them). Same for **dynamic mechanics** (Chandelier/SAR/
  breakeven/scale-out): evidence vs folklore unresolved.

## Sources
- [Deep-research brief: managing a losing position (2026)](../../sources/deep-research-losing-position-management.md)
  — Kaminski-Lo (2014); Lo-Remorov (2017); Dai et al. (2021).
- [Deep-research brief: stop-loss optimization — when stops work (2026)](../../sources/deep-research-stop-loss-optimization-2026.md)
  — frequency/granularity split; Han-Zhou-Zhu momentum-crash-taming (gross); Richards/Locke-Mann behavioral mechanism.
