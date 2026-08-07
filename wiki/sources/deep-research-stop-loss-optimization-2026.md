---
type: research-brief
title: "Stop-Loss Optimization — When Stops Work, by Regime, Frequency & Granularity (Deep-Research Brief, June 2026)"
description: Deepens the stop-loss evidence — Kaminski-Lo's analytic regime-dependence (random-walk negative, momentum positive), the frequency/granularity split (index monthly+ helps; individual-stock tight stops lose on costs), a 10% momentum stop that halves crash risk and doubles Sharpe (gross), and the strong behavioral case (disposition effect; stops *associated with* a reduced disposition effect — mechanism vs self-selection contested). NOTE: the companion "system-strength metrics" half was not covered by this run.
tags: [systematic-trading, risk, stop-losses, position-management, evidence]
timestamp: 2026-06-21T00:00:00Z
status: active
sources: []
---

# Stop-Loss Optimization — When Stops Work (Deep-Research Brief)

**Source:** Claude Code `deep-research` run `wf_5bb20ac8-e78` (2026-06-21). The backgrounded run **stalled
~6h on the overnight quota wall** (status "running", empty output) → **TaskStop'd + resumed past the
reset** → clean.
**Method:** 6 angles → 28 sources → 113 claims → 25 adversarially verified → **21 confirmed, 4 refuted →
10 findings.** Part-A core rests on primary academic sources (Kaminski-Lo MIT/ScienceDirect, Lo-Remorov,
Han-Zhou-Zhu, Odean, Richards, Locke-Mann, Barberis-Xiong).
**⚠️ Scope:** this run answered **Part A (stop-losses) + the behavioral question only**. The companion
**Part B — trading-system strength metrics (Sharpe/Sortino/Calmar/expectancy/DSR/PBO/drawdown)** — got
**zero verified claims** (the 25-claim budget was consumed by Part A) and is being researched separately.
**Evidence/education, not investment advice.** Extends [Stop-Losses & Exit Management](../shared/concepts/stop-losses-and-exits.md).

## The one-paragraph answer
**There is no universal optimal stop.** Whether a stop helps is governed by **(1) the return process
(regime), (2) the sampling frequency, and (3) the asset granularity** — and the *behavioral* case is the
single strongest-evidenced reason to use one. Kaminski-Lo prove a stop *always lowers* expected return
under a random walk and *helps only under momentum*; stops add value for **index/asset-allocation at
monthly+ frequency** but **tight stops on individual stocks lose to transaction costs**; a **10% stop
halves momentum's crash risk and doubles its Sharpe — gross of costs** (net survival was *refuted*); and
a stop's most robust benefit is as **discipline against the costly disposition effect.**

## Confirmed findings

### Regime-dependence — at the level of proof
- **Random walk (i.i.d.): a simple 0/1 stop ALWAYS reduces expected return**, by exactly the risk premium
  (Δ = −pₒ·π, π = μ−r_f ≥ 0) — it merely ejects you from a higher-yielding asset, no informational
  benefit. *No* conditions make a simple stop add value to an i.i.d. positive-premium portfolio.
  [Kaminski-Lo 2014; 3-0] *(Caveat: conditional on μ>r_f; applies to the simple heuristic on gross returns.)*
- **The "stopping premium" turns POSITIVE under momentum / positive serial correlation** (∝ persistence),
  and **stops HURT under mean-reversion.** [3-0]

### Frequency & granularity — the practical split
- **Index / asset-allocation, low frequency: stops ADD value.** On daily US index futures (S&P vs bond
  futures, 1993-2011), monthly+ stops raised return & cut vol (one calibration: **+~1.5% return, −5% vol,
  +20% Sharpe**); on monthly 1950-2004 data, certain stops added **+50-100 bps/month during stop-out
  periods**. **High-frequency stops give NEGATIVE stopping premiums.** [Kaminski-Lo; 3-0]
- **Individual stocks, tight stops: UNDERPERFORM buy-and-hold** in mean-variance terms, **mainly from
  transaction costs** ("death by a thousand cuts") — outperform *only* for stocks with high (positive)
  serial correlation. [Lo-Remorov 2017; 3-0]

### The standout result — taming momentum crashes
- A **10% intra-month stop on US momentum (WML)** cut the worst monthly loss **−49.79% → −11.36%**
  (equal-weighted) and raised EW return 0.99%→1.69%/mo while cutting vol 6.01%→4.58% — **more than
  doubling the Sharpe (~0.17→0.37 EW per the paper; an independent CXO review reports up to ~0.50 by stop level)** (Han-Zhou-Zhu, 1926-2013). [3-0 in-sample]
- **BUT this is GROSS:** the claim that the edge **survives transaction costs** (it raises trading ~40%;
  ~32% of losers / ~30% of winners stopped per month) was **REFUTED 0-3**; CXO flags **data-snooping**
  across stop thresholds and possible dependence on a few crash months (Aug/Sep 1932). Crash-taming &
  Sharpe-doubling are robust in-sample facts; **real-world net profitability is not established.**
- **Lottery stocks:** stop-loss rules raise *risk-adjusted* returns for lottery-type stocks; popular
  technical sell rules (MA, trailing stops) act like stops and add FF-alpha, especially in down markets
  (Dai et al. 2023). [medium; cost-survival only 2-1, thin in-sample break-even]

### The behavioral core — the best-evidenced case for stops
- **Disposition effect is real and costly:** investors realize gains far more than losses (Odean 1998:
  PGR 0.148 vs PLR 0.098, t>35), and **held losers underperform sold winners by 3.4%/yr** — holding
  losers is a *mistake*, not justified by mean-reversion (at the ~1yr horizon). [3-0]
- **A stop is ASSOCIATED WITH a reduced disposition effect** (Richards et al., UK retail): when a stop
  triggers, loss-realization rises and gain-grabbing falls; the authors say stops "inoculate against" the
  bias. ⚠️ *Mechanism vs self-selection is contested* — an independent re-check (2026-06-21) found the
  paper also frames stop-users as a **self-selected, less-experienced** group, so the original "not
  selection" reading is **downgraded / not established**. [original run: mechanism 3-0 / reversal 2-1]
- **Skill-graded discipline:** among pro futures traders, the **least successful hold losers longest, the
  most successful cut quickest** (Locke-Mann 2005). [2-1; floor-futures, minutes-horizon caveat]
- **Why traders resist (Barberis-Xiong "realization utility"):** a documented model of utility from the
  *act* of realizing P&L. [attribution 3-0; the "explains the disposition effect" causal link refuted 1-2]

## What got refuted (do NOT cite)
- The 10% momentum stop **survives transaction costs** / beats standard momentum net of costs. [0-3]
- Floor futures traders exhibit the disposition effect (longer holds on losers). [1-2 — *contested* in that sample]
- Realization utility **explains** the disposition effect (causal). [1-2]
- Disposition-proneness **predicts** lower subsequent income / forecasts success. [1-2]

## Caveats
- **GROSS vs NET and IN-SAMPLE vs OOS are load-bearing:** most reported Sharpe/return gains are gross &
  in-sample. **Cost survival:** YES for low-frequency index allocation & high-autocorrelation/lottery
  stocks; **NO/unproven** for tight stops on ordinary single stocks.
- **No universal optimal stop** — value hinges on return process, frequency, granularity, and market state.
- **Single-source / split-vote items** (Lo-Remorov, Han-Zhou-Zhu, Dai, Locke-Mann, Richards-reversal)
  carry less weight than the Kaminski-Lo + Odean anchors.

## Open questions (what this run did NOT establish)
1. **How to SET stop WIDTH in practice** — a methods comparison (ATR/σ-multiples vs % vs chart/swing-low
   vs account-risk-% vs time-based) and the tight-vs-wide tradeoff. The run covered *whether/when* stops
   help, not the width-setting *method*.
2. **Dynamic-mechanics evidence** — Chandelier/ATR-trailing, Parabolic SAR, breakeven stops, vol-scaled
   widening, scaling-out, time-stops: which are *evidenced* vs folklore (only "technical sell rules
   resemble stops" surfaced).
3. **Stop ↔ position-sizing interaction** (fixed-fractional risk → size; ATR sizing; Kelly/risk-of-ruin)
   — requested but uncovered.
4. **PART B — system-strength metrics** — entirely unanswered; dedicated run in flight.

## Feeds into the wiki
- Strengthens [Stop-Losses & Exit Management](../shared/concepts/stop-losses-and-exits.md) (frequency/
  granularity split; momentum-crash-taming; the behavioral mechanism).
- Connects: [Disposition effect](../shared/concepts/disposition-effect.md) ·
  [Risk of ruin](../shared/concepts/risk-of-ruin.md) · [Momentum](../systematic-trading/factors-signals/momentum.md) ·
  [Transaction costs](../shared/concepts/transaction-costs.md) · [Regime detection](../ml-stats/concepts/regime-detection.md) ·
  `tools/position_size.py` (ATR-stop + risk-based sizer).

## Primary / key sources
- Kaminski & Lo, "When Do Stop-Loss Rules Stop Losses?" (J. Financial Markets 2014) — https://dspace.mit.edu/bitstream/handle/1721.1/114876/Lo_When%20Do%20Stop-Loss.pdf
- Lo & Remorov, "Stop-Loss Strategies with Serial Correlation, Regime Switching, and Transaction Costs" (2017) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2695383
- Han, Zhou & Zhu, "Taming Momentum Crashes: A Simple Stop-Loss Strategy" (2014/2024) — https://www.cicfconf.org/sites/default/files/paper_811.pdf
- Dai, Marshall, Nguyen & Visaltanachoti, "Lottery Stocks and Stop-Loss Rules" (Global Finance J. 2023) — https://www.sciencedirect.com/science/article/abs/pii/S1044028322000503
- Odean, "Are Investors Reluctant to Realize Their Losses?" (J. Finance 1998) — https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/areinvestorsreluctant.pdf
- Richards, Rutterford & Fenton-O'Creevy, "…stop losses and the disposition effect" (Eur. J. Finance 2017) — https://www.bayes.citystgeorges.ac.uk/__data/assets/pdf_file/0004/79960/Richards.pdf
- Locke & Mann, "Professional trader discipline and trade disposition" (JFE 2005) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X0400203X
- Barberis & Xiong, "Realization Utility" (NBER 2008 / JFE 2012) — https://www.nber.org/papers/w14440
