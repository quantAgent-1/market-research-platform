---
type: concept
title: Factor Premia & Alpha Decay
description: Cross-sectional risk premia (value, momentum, quality, low-vol) are largely real and globally replicated, but shrink ~a third once published as informed capital crowds in.
tags: [systematic-trading, ml-stats, factor, evidence]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: [../../sources/deep-research-long-term-profitability.md]
---

# Factor Premia & Alpha Decay

**Factor premia** are systematic, cross-sectional return differences (value, momentum, quality,
low-volatility, carry) that compensate for risk or exploit persistent behavioral mistakes. They are
the most-studied source of [edge](../../synthesis/trading-system-fundamentals.md) in equities — and
the cleanest case study in how edge decays.

## Are they real? (a genuinely two-sided debate)
- **Yes, mostly (the affirmative case).**
  [Jensen, Kelly & Pedersen (2023)](https://www.aqr.com/Insights/Research/Working-Paper/Is-There-a-Replication-Crisis-in-Finance):
  the majority of factors replicate, cluster into 13 themes, and validate out-of-sample across
  **93 countries (~82%)**; a hierarchical-Bayesian view has the *many correlated factors corroborate
  each other.* Even skeptic Campbell Harvey conceded "the results replicate."
- **With heavy caveats (the skeptical case).**
  [Hou, Xue & Zhang (2020)](https://www.nber.org/system/files/working_papers/w23394/w23394.pdf) call
  the literature "infested with widespread p-hacking";
  [Harvey, Liu & Zhu (2016)](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF)
  demand **t ≥ 3** for new factors.
- **The honest reading:** a real core replicates **and** the literature needs aggressive
  [multiple-testing discipline](../../ml-stats/concepts/backtesting-overfitting.md). The dispute is
  over *magnitude and method* (value- vs equal-weighting, NYSE breakpoints), not whether *any* edge
  exists. (The strong "most factors are insignificant" claim was specifically *refuted* in the
  [research run](../../sources/deep-research-long-term-profitability.md).)

## Alpha decay
- [McLean & Pontiff (2016)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623): the
  average anomaly return declines **~26% out-of-sample and ~58% post-publication**; the ~26pp visible
  already OOS is statistical bias, so **~32pp is attributable to publication-informed crowding** — but
  the data **reject** *both* zero decay and full disappearance. A residual premium survives.
- **Mechanism = crowding:** post-publication, anomaly stocks show higher turnover, volume, and short
  interest — informed capital trading the signal *toward* zero, exactly as the
  [limits to arbitrage](limits-to-arbitrage.md) predict.
- Pure data-mining explains only ~10% of in-sample returns — so decay is mostly *real arbitrage*,
  not the signal having been fake to begin with.

## Implications
- **Build for decay:** expect a published edge to shrink ~⅓; monitor live-vs-backtest and retire
  decayed signals.
- **The U.S. caveat:** Jacobs & Müller (2020) find the U.S. is the *only* market with reliable
  post-publication decay — crowding may be a U.S.-specific intensity.

## Relationships
- The flagship tradable factor is
  [momentum](../../systematic-trading/factors-signals/momentum.md) — whose contested net-of-cost
  survival and post-publication decay are the cleanest case study of these dynamics.
- Sized via the [Kelly criterion](kelly-criterion.md); eroded by
  [transaction costs](transaction-costs.md) and capacity limits; persists because of the
  [limits to arbitrage](limits-to-arbitrage.md).

## Sources
- [Deep-research brief (2026)](../../sources/deep-research-long-term-profitability.md) — McLean &
  Pontiff (2016); Jensen, Kelly & Pedersen (2023); Hou-Xue-Zhang (2020); Harvey-Liu-Zhu (2016).
