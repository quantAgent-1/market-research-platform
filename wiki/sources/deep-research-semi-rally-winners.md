---
type: research-brief
title: "Reverse-Engineering the AI-Semiconductor Rally Winners (Deep-Research Brief, 2026)"
description: How winners are actually compounding in the 2023-26 AI-semi rally — the live (April 2026) regime, the bull/bear fundamental case, and the durable mechanisms (low-turnover leader-riding, vol-based sizing, regime-aware exits) vs leveraged beta.
tags: [systematic-trading, semiconductors, momentum, regimes, evidence]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: []
---

# Reverse-Engineering the AI-Semiconductor Rally Winners — Deep-Research Brief

**Source:** Claude Code `deep-research` run `wf_15044bec-287` (2026-06-14; walled on the session quota
twice, **resumed** past each reset).
**Method:** 5 angles → 23 sources → 103 claims → 25 adversarially verified → **22 confirmed, 3
refuted → 9 findings.** Mechanism findings rest on top-tier peer-reviewed primary sources (JF, JFE,
FAJ, JPM); the live-regime numbers on multi-sourced financial press + NVDA's SEC filing.
**Purpose:** the sharper question — not "does momentum work on average" (a [prior brief](deep-research-swing-trading.md)
covered that) but **how the winners in *this* rally are actually winning**, with current data.

## The one-paragraph answer
The fundamental driver is **at least partly real** (NVDA Q3-FY2026 revenue $57.0B, +62% YoY; data
center $51.2B, +66%, ≈90% of revenue) — but the *magnitude* of single-name gains means most "winning"
through early 2026 was **concentrated long beta**, which is fragile and survivorship-laden. The
**durable, identifiable mechanisms** by which winners compound are narrow: **(1) ride the leaders
with LOW turnover** (1-2 orders of magnitude cheaper than active momentum), **(2) size by
volatility** (vol-targeting / dynamic momentum ~doubles risk-adjusted return and cuts the left tail),
and **(3) respect the turn** (momentum crashes are partly forecastable; concentrated high-beta is most
vulnerable to a sharp reversal after a run). And a real **2026 regime signal is already visible:
leadership broadened sharply off NVDA in April 2026.**

## Confirmed findings

### The live regime (2026) — leadership broadened off NVDA
2023-25 was NVDA-led (+239% / +171% / +39%). Then **April 2026: SOXX +40.4% (biggest month in its
25-year history), SMH +32.2% (best ever)** — but **NVDA was the *slowest* mega-cap chipmaker at
+21.9%**, while **Intel +119%, Credo +88%, Astera Labs +84%, AMD +75%, Marvell +65%, Micron +55%**
led (networking, memory/HBM, legacy). A near-complete *inversion* of the prior leaderboard (Micron
~+762% TTM, joined the $1T club). [3-0]

### Bull case — a verified earnings step-change
NVDA Q3 FY2026 (qtr ending Oct 2025): **revenue $57.0B (+62% YoY)**, **data center $51.2B (+66%)** ≈
90% of revenue, **Q4 guide $65.0B**. GAAP, not narrative. Hyperscaler capex ~$256B→$443B→$602B
(2024→26). [3-0]

### Bear case — a specific, contested accounting critique
Michael Burry (Nov 2025) accused hyperscalers of **understating depreciation** (extending chip
useful-life), ~$176B 2026-28, Oracle/Meta profits overstated ~27% / ~21%; disclosed bearish puts.
The dot-com parallel + $108B/yr hyperscaler debt. **Nvidia rebutted; CNBC couldn't confirm** — what's
established is that Burry *made* the claim, not that it is true. [3-0]

### Mechanism 1 — ride leaders with LOW turnover
Trading-cost dispersion is huge: low-turnover conviction strategies cost **~61-76 bps/yr** vs
high-turnover **momentum ~200-270 bps/yr** (Li et al., FAJ 2019). **Holding winners is the cheap edge;
flipping them is the expensive trap** — and the reason high-frequency technical trading mostly fails
net of costs. [3-0] *(Caveat: large-AUM market-impact figures, not retail spreads.)*

### Mechanism 2 — size by volatility
**Volatility targeting** improves risk-asset Sharpe and **cuts left-tail severity** across asset
classes (Harvey et al., JPM 2018); a dynamic mean/variance-scaled momentum overlay **~doubles** the
alpha/Sharpe of static momentum (Daniel-Moskowitz, JFE 2016). The most evidence-backed risk tool for
concentrated high-beta exposure. [3-0]

### Mechanism 3 / the turn — momentum crashes
Crashes are **partly forecastable** — they strike in **post-decline, high-vol "panic" states,
contemporaneous with rebounds** — driven by the loser-leg beta rising **above 3** (the book behaves
like a **written call**); loser deciles rebounded **+232% (1932), +163% (2009)**. *Transmission
caveat:* a **long-only** leader book lacks the written-call structure — it crashes via its own
valuation/earnings reversal (e.g. NVDA −$600B in a day, Jan 2025). The lesson holds: concentrated
high-beta is most fragile to a sharp reversal after a run. [3-0]

### Skill vs beta — most "winning" is hard to distinguish from luck
Fama-French (JF 2010): aggregate active funds have ~**zero gross alpha** and **negative net alpha
(−0.81% to −1.00%/yr)**; bootstraps show **~90% of even 90th-percentile track records are consistent
with zero skill** net of costs. In a +several-hundred-percent run, the prior is that most "winning" is
**leveraged long beta + luck**; survivorship bias dominates any individual story. [3-0]

### Relative strength / 52-week-high — a real signal, but not dominant
The 52-week-high strategy earns ~0.45%/mo (~1.2% ex-Jan; George-Hwang) — a documented relative-
strength signal. **But the claim that it *dominates* ordinary momentum was refuted** (in-sample,
small-stock-concentrated, contested OOS — Du 2008, Barroso-Wang 2021). [descriptive 3-0; dominance 1-2]

## The defensible "how winners win" playbook (synthesis)
1. **Regime ID** — 200-day-MA trend + breadth; watch *who leads* (broadening off the generals is a
   late-stage tell).
2. **Ride leaders, low turnover** — hold the genuine winners cheaply.
3. **Conviction on *real* fundamentals** — the verified earnings step-change, not the chart.
4. **Volatility-based sizing & stops** — ~doubles risk-adjusted return, cuts the tail.
5. **Regime-aware exit/hedging** — the crash is partly forecastable; the drawdown is inevitable.

**The honest catch:** the edge is the *risk/regime discipline*, not the gains — leveraged beta + luck
mimic skill perfectly in a bull run, and a deep drawdown (dot-com −80%+, 2022 −35%) is effectively
certain.

## What got refuted
- 52-week-high *dominates* momentum (1-2 — limited to small stocks, contested OOS).
- Two re-derivations of momentum's ~270 bps cost / linear cost-scaling ("refuted" only as duplicate
  derivations — the underlying numbers were rated credible, not contradicted).

## Caveats
- **Time-sensitive:** regime numbers are **April-2026 month-end** — one month of dispersion is a data
  point, not a proven regime change (though trailing data corroborate the broadening).
- **Source tiers:** regime/Burry = secondary press (multi-sourced); NVDA fundamentals = primary SEC;
  mechanisms = top-tier peer-reviewed.
- **Transmission:** long-only ≠ the written-call crash mechanism (different mechanics, same fragility).
- **Generalization:** factor costs are large-AUM impact, not retail; Fama-French is a mutual-fund
  *prior* for individual traders.
- **Survivorship is the overarching caveat** — no single track record from this rally proves edge.

## Open questions
1. Documented **net-of-cost track records** of named growth systems (O'Neil CANSLIM, Minervini SEPA)
   through full cycles — not verified here.
2. **Quantified SOXL** volatility-drag/decay over 2023-26 and past drawdowns.
3. Has the regime **turned** since April 2026 (capex-guidance cuts, GPU/HBM softening, TSMC
   utilization, a 200-day-MA break)?
4. **Valuation-vs-history** (forward P/E, EV/sales) and realized/implied vol for the named semis.

## Feeds into the wiki
- Fleshed out: [Semiconductors](../shared/instruments/semiconductors.md) ·
  [Regime detection](../ml-stats/concepts/regime-detection.md)
- Playbook added to: [Swing trading](../systematic-trading/strategies/swing-trading.md)
- Connects: [Momentum](../systematic-trading/factors-signals/momentum.md) ·
  [Transaction costs](../shared/concepts/transaction-costs.md) ·
  [Risk of ruin](../shared/concepts/risk-of-ruin.md) ·
  [Who actually wins](../shared/concepts/who-wins-empirical-record.md)

## Primary / key sources
- NVDA Q3 FY2026 results — https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2026
- Daniel & Moskowitz, "Momentum Crashes" (JFE 2016) — https://www.nber.org/system/files/working_papers/w20439/w20439.pdf
- Harvey et al., "The Impact of Volatility Targeting" (JPM 2018) — https://www.man.com/insights/the-impact-of-volatility-targeting
- Li, Chow, Pickard & Garg, "Transaction Costs of Factor-Investing Strategies" (FAJ 2019) — https://www.tandfonline.com/doi/full/10.1080/0015198X.2019.1567190
- Fama & French, "Luck versus Skill in the Cross Section of Mutual Fund Returns" (JF 2010) — https://mba.tuck.dartmouth.edu/bespeneckbo/default/AFA611-Eckbo%20web%20site/AFA611-S8C-FamaFrench-LuckvSkill-JF10.pdf
- George & Hwang, "The 52-Week High and Momentum Investing" (JF 2004) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x
- April-2026 regime — Benzinga / Sahm Capital / Motley Fool / CNBC (see run sources)
- Burry critique — CNBC (2025-11-11) / Burry's X post & 13F
