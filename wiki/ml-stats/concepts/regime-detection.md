---
type: concept
title: Regime Detection
description: Identifying market states (trend vs mean-revert, calm vs crash) to decide which strategy to run and when to cut — anchored by the partly-forecastable, severe momentum crash in high-beta names.
tags: [ml-stats, systematic-trading, regimes, risk]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: [../../sources/deep-research-semi-rally-winners.md]
---

# Regime Detection

Strategy returns are **regime-dependent**: trend/momentum pays in persistent trends and blows up in
sharp reversals; mean-reversion is the opposite. Detecting the regime tells you which edge to run —
and, more importantly, when to **cut or hedge**.

## Filters (practitioner-standard)
- **Trend:** price vs the 200-day moving average; higher-highs / higher-lows.
- **Breadth & leadership:** how many names participate; a **leadership handoff away from the generals**
  (e.g. semis broadening off NVDA in April 2026) is a classic late-stage tell.
- **Volatility regime:** VIX level / term structure; realized-vol state.

## Momentum crashes — the verified core
[Momentum](../../systematic-trading/factors-signals/momentum.md) suffers infrequent but **severe
crashes** that are **partly forecastable** (Daniel-Moskowitz 2016): they strike in **"panic" states —
after market declines, when volatility is high — and coincide with sharp *rebounds*.** Mechanism:
after big declines the loser-leg beta rises **above 3** while winners fall **below 0.5**, so a
long-winner/short-loser book behaves like a **written call on the market**. Magnitudes are extreme:
the loser decile returned **+232% (1932)** and **+163% (2009)** vs winners +32% / +8%.
- **Transmission caveat:** the crash force lives in the *short* leg. A **long-only** leader book
  (e.g. just holding NVDA) doesn't have the written-call structure — it crashes via its *own*
  valuation/earnings reversal. The durable lesson is the same: concentrated high-beta is most
  vulnerable to a sharp reversal after a run, in a high-vol regime.

## The defensible response: volatility-based sizing
**Volatility targeting** (lever when vol is low, cut when high) improves the Sharpe of risk assets and
**reduces left-tail severity** across asset classes (Harvey et al. 2018) — because crashes hit in
high-vol states when a vol-targeted book already holds less. Applied to momentum, a dynamic
mean/variance-scaled overlay **~doubles** static momentum's alpha/Sharpe (Daniel-Moskowitz). The
most evidence-backed risk tool for high-beta
[semiconductor](../../shared/instruments/semiconductors.md) exposure.

## Relationships
- Governs which [swing](../../systematic-trading/strategies/swing-trading.md) /
  [momentum](../../systematic-trading/factors-signals/momentum.md) edge applies; a survival tool
  alongside [risk of ruin](../../shared/concepts/risk-of-ruin.md).
- The complementary crash-insurance evidence lives on
  [stop-losses & exits](../../shared/concepts/stop-losses-and-exits.md) (Han-Zhou-Zhu: a 10% stop
  taming the momentum-crash tail).
- The second-moment forecasting canon these filters coarsen — models, uses, limits:
  [volatility forecasting](volatility-forecasting.md).

## Sources
- [Deep-research brief: reverse-engineering the semi-rally winners (2026)](../../sources/deep-research-semi-rally-winners.md)
  — Daniel & Moskowitz, "Momentum Crashes" (JFE 2016); Harvey et al., "The Impact of Volatility
  Targeting" (JPM 2018).
