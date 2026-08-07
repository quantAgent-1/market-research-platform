---
type: concept
title: Backtesting Rigor & Overfitting
description: How to tell a real edge from a curve fit — multiple-testing/p-hacking inflate backtests, so require high t-stat hurdles, out-of-sample/walk-forward validation, realistic costs, and bias-free data.
tags: [ml-stats, systematic-trading, methodology, backtesting]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/deep-research-long-term-profitability.md]
---

# Backtesting Rigor & Overfitting

A backtest's job is to *try to falsify* a candidate edge, not to flatter it. The dominant failure
mode is **overfitting via multiple testing**: try enough strategies and some will look profitable by
chance alone.

## The multiple-testing problem
- The anomaly literature is "infested with widespread p-hacking"
  ([Hou, Xue & Zhang 2020](https://www.nber.org/system/files/working_papers/w23394/w23394.pdf)).
  **Verified from the RFS paper (2026-07-20):** with microcaps handled properly (NYSE breakpoints,
  value-weighted returns), **65% of 452 anomalies fail to clear even t ≥ 1.96** — 96% of the
  trading-frictions category — and at the multiple-testing hurdle t ≥ 2.78 the failure rate rises to
  **82%**. Their verdict: "capital markets are more efficient than previously recognized." *(This
  page previously said "300+ factors"; 452 is the paper's actual library size.)*
  [Harvey, Liu & Zhu (2016)](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF)
  recommend **t ≥ 3** for new factors (others push to ~3.8).
- **The bar is unaffordable, and that is the real finding.** Since t ≈ SR·√T, clearing t = 2 on a
  Sharpe-0.5 strategy takes 16 years — and ~37 if you tried 100 variants first (T ≈ 2·ln N / SR²).
  The industry does not run on statistically validated backtests; it runs on evidence imported from
  outside the return series (mechanism, cross-sample replication, breadth, forward tracking). Full
  derivation + the canonical factors re-measured through 2026:
  [Is Quant Research a Science?](../../synthesis/is-quant-research-a-science.md).
- More strategies tested ⇒ higher chance the *best* is luck. The **deflated Sharpe ratio** (Bailey &
  López de Prado) explicitly discounts for the number of trials and for non-normal returns.
- **Canonical real-world case:** technical trading rules that look profitable in-sample on US
  large-cap indices *vanish* once you correct for the ~8,000 rules searched (Sullivan-Timmermann-
  White) — see [swing trading](../../systematic-trading/strategies/swing-trading.md).

## The non-negotiables
- **Out-of-sample / walk-forward** validation; never tune and judge on the same data.
- **An economic rationale** as a prior — the first defense against mining noise (an edge with no
  cause is a red flag, not a discovery). Ties to [factor premia](../../shared/concepts/factor-premia-and-alpha-decay.md).
- **Realistic costs and fills** in the simulation — many gross edges are negative net of
  [transaction costs](../../shared/concepts/transaction-costs.md).
- **Bias-free, point-in-time data** — see [data integrity](data-integrity.md) (look-ahead and
  survivorship bias silently manufacture edge).
- **Expect decay:** even real edges shrink ~⅓ once known
  ([alpha decay](../../shared/concepts/factor-premia-and-alpha-decay.md)), so a thin backtested
  margin will not survive live. **Measured on the canonical five through May-2026** (Ken French data,
  each factor split at its own publication date): decay of **48–106%, averaging ~73%** — and *not one
  of SMB/HML/Mom/CMA/RMW clears t = 2 in its own post-publication sample*
  ([the computation](../../synthesis/is-quant-research-a-science.md#2-the-playbook-re-measured)).
- ⚠️ **Vintage trap — McLean & Pontiff:** the 2013 working paper reports 82 characteristics,
  ~10% out-of-sample / ~35% post-publication decay; the published JF (2016) version reports 97
  characteristics, **26% / 58%**. Both circulate. Cite the published pair.

## Relationships
- The implementation pillar of
  [Edge × Risk × Implementation](../../synthesis/trading-system-fundamentals.md); the methodological
  complement to [factor premia & alpha decay](../../shared/concepts/factor-premia-and-alpha-decay.md).
- The full evaluation scorecard — Sharpe's gameability, CVaR vs VaR, and the **Deflated Sharpe Ratio**
  gate — is in [trading-system performance metrics](performance-metrics.md) (the metric side of this
  page's multiple-testing argument: a backtest Sharpe is uninterpretable without the number of trials N).

## Open questions
- Practical deflated-Sharpe / multiple-testing workflows for a single researcher running many
  configurations.

## Sources
- [Deep-research brief (2026)](../../sources/deep-research-long-term-profitability.md) —
  Hou-Xue-Zhang (2020); Harvey-Liu-Zhu (2016). Background: Bailey & López de Prado, "The Deflated
  Sharpe Ratio" (2014) and "Pseudo-Mathematics and Financial Charlatanism" (*AMS Notices*, 2014).
