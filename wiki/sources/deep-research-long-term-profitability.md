---
type: research-brief
title: "Fundamentals of Consistent Long-Term Profitability in Equities & Options (Deep-Research Brief, 2026)"
description: Fact-checked academic & empirical evidence on what separates the minority of consistent long-term market winners from the majority — edge, decay, limits to arbitrage, costs, survival, and skill.
tags: [systematic-trading, derivatives, ml-stats, factor, market-efficiency, evidence]
timestamp: 2026-06-13T00:00:00Z
status: active
sources: []
---

# Fundamentals of Consistent Long-Term Profitability — Deep-Research Brief

**Source:** Claude Code `deep-research` workflow, run `wf_c6420d23-34e` (2026-06-13).
**Method:** 6 search angles → 28 sources fetched → 137 falsifiable claims extracted → 25 adversarially
verified (3-vote; ≥2/3 refutes kills a claim) → **7 confirmed findings, 5 refuted.** Nearly all
confirmed claims rest on top-tier primary sources (*Journal of Finance*, *RFS*, NBER, S&P DJI).

## The one-paragraph answer
Durable edge in equities and equity-options markets is **real but scarce, decays once it is known,
and is bounded by the limits of arbitrage** — so survival, cost control, and process discipline
matter more than any single signal. Genuine cross-sectional factor premia exist and mostly
replicate, yet publication shrinks them by roughly a third as informed capital crowds in. On the
participant side the record is brutal: >80% of day traders and ~92% of active equity funds (20-yr)
lose to a passive benchmark, with essentially no persistence among past winners — *yet a small (~1%)
genuinely skilled minority does persist.* Skill exists; it is rare; and the dominant destroyers of
the majority are **costs and over-trading**, not bad stock-picking.

## Confirmed findings (each verified ≥2/3)

### 1. Edges decay once published — but don't vanish (alpha decay / crowding)
[McLean & Pontiff (2016, *J. Finance*)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623):
the average anomaly's return falls ~35% post-publication (net of statistical bias; 58% raw in the
published version), and the data statistically **reject both 0% decay and 100% decay** — a residual
premium survives. Pure data-mining explains only ~10% of in-sample returns (an insignificant upper
bound), so most published predictability is real, not spurious. Mechanism: post-publication, anomaly
stocks show higher turnover, volume, variance, and short interest — sophisticated investors trading
the signal *toward* (not to) zero. → [Factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md)

### 2. Most factor premia replicate and validate out-of-sample
[Jensen, Kelly & Pedersen (2023, *J. Finance*)](https://www.aqr.com/Insights/Research/Working-Paper/Is-There-a-Replication-Crisis-in-Finance):
the majority of asset-pricing factors replicate, cluster into 13 themes, and work out of sample
across **93 countries (~82% global replication)**; under a hierarchical Bayesian prior the *large
number of correlated factors strengthens* the evidence rather than inflating false discoveries. Even
factor-zoo skeptic Campbell Harvey conceded "the results replicate." **Contested** — see finding 3.
→ [Factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md)

### 3. The anomaly literature is p-hacked → demand a high bar (t ≥ 3)
[Hou, Xue & Zhang (2020, *RFS* / NBER w23394)](https://www.nber.org/system/files/working_papers/w23394/w23394.pdf)
call the literature "infested with widespread p-hacking";
[Harvey, Liu & Zhu (2016, *RFS*)](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF)
argue the usual t > 2.0 no longer makes sense across 300+ tested factors and recommend **t > 3.0**
for new factors (Chordia-Goyal-Saretto push to ~3.8). Note: the *strong* "most factors are
insignificant / microcaps inflate them" claims were **refuted** in this run (see below); the
defensible takeaway is methodological rigor, not factor nihilism.
→ [Backtesting rigor & overfitting](../ml-stats/concepts/backtesting-overfitting.md)

### 4. Why inefficiency persists: the limits of arbitrage
[Shleifer & Vishny (1997, *J. Finance*)](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1997.tb03807.x):
real arbitrage is done not by many diversified traders but by "a relatively small number of highly
specialized investors using other people's money." Because of that agency structure, arbitrage
"becomes ineffective in extreme circumstances, when prices diverge far from fundamental value" —
capital is pulled *exactly when expected returns are highest* (LTCM 1998; the 2007 quant quake).
This is the theoretical bridge between EMH's limits and the persistence of edge.
→ [Market efficiency & limits to arbitrage](../shared/concepts/limits-to-arbitrage.md)

### 5. Consistent discretionary profit is achievable but empirically rare
[Barber, Lee, Liu & Odean (2014, *RFS*)](https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf),
a **complete census** of the Taiwan market 1995–99: in a typical 6-month window >80% of day traders
lose money net of costs; under favorable cost assumptions <20% profit. *Yet* there is "strong
evidence of persistent ability for a relatively small group" — the stocks the skilled cohort buys
beat those they sell by **62 bp/day**, and the persistently skilled are ~1%. Population census, so
the base rate is trustworthy: skill is real but the exception.
→ [Who actually wins](../shared/concepts/who-wins-empirical-record.md)

### 6. Over-trading is hazardous; costs and overconfidence (not stock-picking) do the damage
[Barber & Odean (2000, *J. Finance*)](http://faculty.haas.berkeley.edu/odean/papers/returns/individual_investor_performance_final.pdf),
66,465 households 1991–96: the highest-turnover households earned **11.4% net** vs 17.9% for the
market and 18.5% for the least-active — a ~710 bp gap. **Gross** returns ≈ the market while **net**
fell below — so the penalty is trading cost, not bad selection. The pattern fits overconfidence
models, not rational trading.
→ [Transaction costs & market impact](../shared/concepts/transaction-costs.md) · [Who actually wins](../shared/concepts/who-wins-empirical-record.md)

### 7. Most active managers lose, and winners don't persist (not a survivorship artifact)
[SPIVA U.S. Year-End 2024 (S&P DJI)](https://www.spglobal.com/spdji/en/spiva/article/spiva-us/):
65% of active large-cap funds trailed the S&P 500 in 2024 (~64% on the 20-yr average); over 15 years
**zero of 22 U.S. equity categories** had a majority of active managers beat their benchmark; ~92%
trailed over 20 years.
[Persistence Scorecard](https://www.spglobal.com/spdji/en/documents/spiva/persistence-scorecard-year-end-2024.pdf):
**0.00%** of top-quartile domestic funds (Dec-2020) stayed top-quartile through 2024 — persistence
*below* chance, i.e. past winners look lucky. SPIVA keeps liquidated funds in the denominator (~64%
died over 20 yr), so this is **not** survivorship bias.
→ [Who actually wins](../shared/concepts/who-wins-empirical-record.md)

## What got refuted (did NOT survive verification)
- **"64% of 447 anomalies are insignificant (85% at t≥3)"** — killed 0-3. The strong factor-nihilist
  reading is *not* supported.
- **"Replication failures are mostly a microcap-overweighting artifact"** — killed 1-2.
- **"Heavy day traders are positive gross and lose only on costs"** — killed 0-3. So *skill* (not just
  costs) separates the winners.
- **"Only 2.4% of funds stay top-half 5 yrs, below chance"** — killed 1-2 (the broad no-persistence
  result still holds via finding 7).
- **"Systematic CTAs survive longer than discretionary"** — killed 0-3. *No support here for "rules
  beat human emotion for survival."*

## Caveats (read before trusting any single number)
- **Coverage gaps — treat as open, not established:** the **options volatility-risk-premium /
  implied-vs-realized edge you specifically asked about had _no_ surviving verified claim** in this
  run (sources were fetched — AQR, SSRN, Fed — but none cleared verification within budget).
  Likewise **Kelly / fractional-Kelly sizing and risk-of-ruin math** were only *indirectly* supported
  (via the over-trading evidence), with no direct verified source; and **capacity / market-impact
  scaling laws** were touched only through the crowding mechanism. The wiki's existing
  Sinclair-sourced VRP and Kelly pages stand on a *practitioner* source, not on this run's academic
  verification.
- **The factor core is genuinely two-sided:** JKP (replicate) vs HXZ/Harvey (p-hacking) is a live
  dispute over *magnitude and method* (value- vs equal-weighting, NYSE breakpoints, Bayesian vs
  frequentist hurdles) — **not** over whether *any* edge exists. Both "a real core of factors
  replicates" and "the literature needs aggressive multiple-testing discipline" are true.
- **Metric precision:** McLean-Pontiff's 35% (net of bias) and 58% (raw) are different metrics — not
  interchangeable. The ~10% data-mining figure is an *insignificant upper bound*.
- **Time/scope:** SPIVA is point-in-time (YE-2024) and the U.S. is special — Jacobs & Müller (2020)
  find the U.S. is the *only* market with reliable post-publication decay, so crowding/decay may not
  generalize. Barber-Odean datasets (Taiwan 1995-99; U.S. 1991-96) predate zero-commission trading —
  the *lessons* (costs + overconfidence dominate) are durable; the *magnitudes* reflect a
  higher-cost era.

## Open questions (worth a focused follow-up run)
1. **Options edge:** *(addressed 2026-06-14 — see the [VRP brief](deep-research-volatility-risk-premium.md))*
   the equity-**index** VRP is verified as real and large but mostly crash-risk compensation and only
   modest net of costs; single-name VRP is small. Still open: post-2010 magnitude, the unhedged crash
   profile, and crowding/capacity.
2. **Sizing math:** the Kelly / fractional-Kelly and risk-of-ruin record — what fraction of Kelly do
   durable systematic traders actually use?
3. **Capacity & impact:** square-root impact law; the AUM at which value/momentum alpha decays to
   zero net of costs; crowding vs capacity as the driver of decay.
4. **Identifying the skilled minority ex ante:** what observable traits (process, costs, holding
   period, edge source) separate the ~1% durable winners from survivorship noise *before* the fact?

## Feeds into the wiki
- New thesis: [Fundamentals of a profitable, well-engineered trading system](../synthesis/trading-system-fundamentals.md)
- New concepts: [Limits to arbitrage](../shared/concepts/limits-to-arbitrage.md) ·
  [Factor premia & alpha decay](../shared/concepts/factor-premia-and-alpha-decay.md) ·
  [Who actually wins](../shared/concepts/who-wins-empirical-record.md) ·
  [Risk of ruin](../shared/concepts/risk-of-ruin.md) ·
  [Backtesting rigor & overfitting](../ml-stats/concepts/backtesting-overfitting.md) ·
  [Data integrity](../ml-stats/concepts/data-integrity.md)
- Strengthens: [Transaction costs](../shared/concepts/transaction-costs.md) ·
  [Kelly criterion](../shared/concepts/kelly-criterion.md) ·
  [Implied vs realized vol](../derivatives/concepts/implied-vs-realized-volatility.md) ·
  [Volatility arbitrage](../derivatives/strategies/volatility-arbitrage.md)

## Primary sources (verified)
- McLean & Pontiff (2016) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623
- Jensen, Kelly & Pedersen (2023) — https://www.aqr.com/Insights/Research/Working-Paper/Is-There-a-Replication-Crisis-in-Finance
- Hou, Xue & Zhang (2020) — https://www.nber.org/system/files/working_papers/w23394/w23394.pdf
- Harvey, Liu & Zhu (2016) — https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF
- Shleifer & Vishny (1997) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1997.tb03807.x
- Barber, Lee, Liu & Odean (2014) — https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf
- Barber & Odean (2000) — http://faculty.haas.berkeley.edu/odean/papers/returns/individual_investor_performance_final.pdf
- SPIVA U.S. & Persistence Scorecard YE-2024 — https://www.spglobal.com/spdji/en/spiva/article/spiva-us/

## Leads fetched but not verified this run (for a follow-up)
- **VRP / options:** AQR "Understanding the Volatility Risk Premium"; SSRN 3819342, 3229719; Fed FEDS 2015-020.
- **Backtest overfitting:** Bailey & López de Prado, "The Deflated Sharpe Ratio" (SSRN 2460551) and
  "Pseudo-Mathematics and Financial Charlatanism" (*AMS Notices*, 2014).
- **Kelly / sizing:** MacLean, Thorp & Ziemba, *The Kelly Capital Growth Investment Criterion* (2011);
  Thorp, "Understanding the Kelly Criterion."
