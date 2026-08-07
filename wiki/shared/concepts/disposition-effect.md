---
type: concept
title: Disposition Effect
description: The tendency to sell winners too early and hold losers too long — large, real (even in pros), and costly (the winners sold beat the losers held by ~3.4%/yr). The behavioral reason underwater positions are mishandled.
tags: [systematic-trading, behavioral, risk]
timestamp: 2026-06-14T00:00:00Z
status: active
sources: [../../sources/deep-research-losing-position-management.md]
---

# Disposition Effect

The **disposition effect** is the tendency to **realize gains too readily and hold losses too long**
(Shefrin-Statman 1985). It is the behavioral core of why a losing position is mishandled — the felt
asymmetry between *booking* a loss (admitting a mistake) and booking a gain.

## The evidence
- **Real and large** ([Odean 1998](../../sources/deep-research-losing-position-management.md)):
  Proportion of Gains Realized **0.148** vs Losses **0.098** (t=35); account-level gap **0.21**.
- **Costly, not smart:** the winners investors sell **beat the losers they keep by ~3.4%/yr** — Odean
  rules out mean-reversion, taxes, and costs, so holding the loser and hoping is **on average wrong ex
  post**.
- **Afflicts pros and moves prices** (Frazzini 2006): a paper-loss "overhang" creates underreaction to
  bad news; the long-short spread earns **2.43%/mo alpha**. Strongest in the **worst-performing
  funds.** *(Caveat: ~30% of managers, not all.)*
- **Mechanism = loss aversion**, but its magnitude is unstable (pooled λ ≈ 1.3 to ~2 across 2024
  meta-analyses) — so the fix is structural, not "calibrate your willpower."

## Why it matters
Your instinct on an underwater position points the wrong way: it pulls you to **hold the loser** (to
avoid realizing the loss) and **cut the winner** — the exact opposite of what the data rewards. The
[stop / hold / add framework](stop-losses-and-exits.md) and **pre-commitment** exist precisely to
override this instinct.

## Relationships
- The behavioral driver behind [stop-losses & exits](stop-losses-and-exits.md); a specific case of the
  cost of [over-trading / behavioral error](who-wins-empirical-record.md); related to the sunk-cost
  fallacy and anchoring.

## Sources
- [Deep-research brief: managing a losing position (2026)](../../sources/deep-research-losing-position-management.md)
  — Odean (1998); Frazzini (2006); Shefrin & Statman (1985); Walasek et al. (2024).
