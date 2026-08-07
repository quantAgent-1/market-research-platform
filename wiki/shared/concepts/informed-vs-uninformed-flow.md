---
type: concept
title: Informed vs. Uninformed Flow & the Identification Problem
description: Why you usually cannot tell informed (private-information) selling apart from uninformed liquidity/de-risking flow ex-ante — the tells (breadth, options skew, short interest, insider Form 4, turnover) are all ambiguous, PIN/VPIN are contested, and pre-earnings drift predicts reversal, not the surprise direction. The breadth test is the cheapest decisive tell.
tags: [systematic-trading, market-research, microstructure, behavioral]
timestamp: 2026-06-24T00:00:00Z
status: active
sources: [../../sources/deep-research-memory-drawdown-flow-2026.md]
---

# Informed vs. Uninformed Flow & the Identification Problem

When a stock sells off into a catalyst (e.g. earnings), two very different stories produce the *same* tape:

- **Informed flow** — someone trading on a genuine edge about the upcoming outcome (private information, or
  faster processing of public information: channel checks, supply-chain reads, whisper numbers). The dramatic
  version is **insider trading** on material non-public information (MNPI).
- **Uninformed flow** — selling for reasons unrelated to the outcome: **de-risking** ahead of a binary event,
  **profit-taking** after a run, **forced de-grossing** (margin, risk limits, leveraged-ETF rebalancing),
  index/factor **rebalancing**, **tax** selling, or plain liquidity demand.

**The identification problem:** ex-ante, on the tape, these are **very hard to separate.** Both push price down,
bid up puts, and lift volume. Anyone who claims to *read* "informed flow" off a pre-catalyst chart is usually
**pattern-matching in hindsight** — after the outcome is known, the prior selling looks prescient.

## Why the standard tells are all ambiguous
| Tell | Informed reading | Why it's also consistent with uninformed flow |
|---|---|---|
| **Price weakness into the event** | Smart money positioning for a miss | De-risking / profit-taking after a run does the same; see base rate below |
| **Elevated turnover / order-flow imbalance** | Information being traded | Turnover spikes for disagreement, rebalancing, taxation, coordination — **PIN is "no more useful than checking whether turnover is above average"** (Duarte-Hu-Young, *JFE* 2020; turnover + turnover² ≈ 65% of its power) |
| **Bid-up puts / higher IV** | Hedging known downside | A **routine pre-earnings IV ramp** bids puts for *every* name; only **skew *steepening beyond* the ramp** is suggestive |
| **Rising short interest** | Informed shorts | Hedging, basis trades, and factor shorts also raise it; reported with a lag |
| **Insider Form 4 selling** | Insiders know something | **Blackout windows** bar pre-print insider trades; 10b5-1 plans are pre-scheduled; insider activity clusters *after* prints |

The one genuinely **cheap, decisive** tell is **breadth** (next section).

## The breadth test — the most decisive cheap discriminator
**Is the weakness idiosyncratic to the name, or shared by its peers / sector / the macro tape?**
- **Broad, correlated weakness** (the whole complex + sector ETFs + long-duration tech falling together,
  especially on an exogenous trigger) ⇒ **macro/sector de-risking** — by construction *not* name-specific private
  information.
- **Idiosyncratic underperformance** (the name falling materially *more* than its true peers, with no shared
  catalyst) is the **precondition** for a name-specific informed-flow read — necessary, not sufficient.

A name can still be the **biggest decliner** in a broad sell-off without it being informed: the **highest-beta**
member (most stretched, most leveraged, a binary catalyst next) leads a sector flush. Largest-mover ≠ informed.
*(Worked example: [Micron's −13% on 2026-06-23](../../market-research/memory/micron-fq3-2026-earnings.md) — the
biggest US decliner, but in line with Samsung/SK Hynix/SanDisk in a Korea-led leveraged-ETF panic.)*

## Why measured "informed trading" still isn't proof of private information
Even when microstructure models *do* flag informed trading, it's detected **both before AND after** public
announcements (Brennan-Huh-Subrahmanyam, *RFS* 2018) → "caution in interpreting trading on information as
trading on private information." Some traders just **process public news faster.** PIN's defect is specific to
PIN; OWR/GPIN models reportedly don't share it — so this is *not* a blanket dismissal of microstructure
detection, just of the naive reading.

## The base rate: pre-event drawdowns do NOT predict the outcome
"Smart money is selling, so the print must be bad" is **not a reliable inference.** Pre-earnings price drift in
stretched, high-flying names is largely **uninformed over-extrapolation that REVERSES** after the announcement
(Ertan-Karolyi-Kelly-Stoumbos, *RAS* 2022) — the predictive content is **mean-reversion, not the surprise
direction.** The drift tells you about **sentiment/positioning**, not the **fundamentals** about to be revealed.

## The asymmetry is conditional, not predictive — the "earnings torpedo"
A separate, real effect: growth/glamour names suffer an **asymmetrically large negative** price response to a
**miss**, while a beat isn't symmetrically rewarded (Skinner-Sloan, *RAS* 2002; Mashruwala 2014 → short-sale
constraints + disagreement). This is the **reaction *conditional* on a miss**, not the **probability** of one.
It's why a stretched, concentrated, **leveraged** book carries lopsided downside through a binary **regardless of
what any pre-print drawdown "means"** — the risk is the *payoff shape*, not a flow-reading edge.

## The literal-insider channel is the least likely mechanism
- **Blackout periods** generally run from ~2-4 weeks before quarter-end to 1-2 business days after the release →
  insiders are typically **barred** from trading into a print (Perkins Coie).
- **Rule 10b-5** bars trading on MNPI; **Rule 10b5-1** sell plans require a **cooling-off period** + a no-MNPI
  certification, so a freshly-timed pre-print sale can't easily/lawfully be arranged.
- Insider trading **concentrates *after* earnings** (day 0 to +5) and accompanies only **~5%** of announcements.
- ⇒ "**Informed flow**" in the *broad* sense (funds with channel checks / pricing reads) is the realistic
  version — but it's **diffuse, partly already in consensus/IV, and not a smoking gun.**

## Practical heuristic
1. **Run the breadth test first** (peers, sector ETFs, macro tape, the trigger) — it resolves most cases cheaply.
2. Only if the move is **idiosyncratic** do the harder tells (skew *steepening beyond* the ramp, unusual
   downside blocks, short-interest jumps) carry weight — and even then, **probabilistically, not definitively.**
   *(Worked example — semis, Jun 2026: when the harder tells were finally measured, they came back **mixed/benign** —
   the "fear-still-steep" skew claims were **refuted**, SOXL skew was modest (~1.05), and MU short interest was **low**
   (~3.7% float / 0.8 days-to-cover) — i.e. they pointed to a **passing de-risking flush**, not informed/structural-bear
   selling. See the [semis positioning brief](../../sources/deep-research-semis-positioning-unwind-2026-06-29.md).)*
3. **Don't trade the drawdown as a directional signal** — it predicts reversion, not the outcome.
4. **Manage the payoff shape**, not the omen: the torpedo asymmetry + leverage is the controllable risk.

## Relationships
- Behavioral cousin: the [disposition effect](disposition-effect.md) (why holders misread their own flow) and
  [regime-aware exits](stop-losses-and-exits.md).
- Payoff-shape risk amplifier: [leveraged-ETF decay](leveraged-etf-decay.md) (a 3×-daily book through a
  multi-day catalyst).
- Valuation backdrop for "stretched high-flyer": [fundamental valuation & re-rating](fundamental-valuation.md).
- Which pool is behind the flow — fast, slow, or mechanical — and why mechanical flow is plumbing, not a vote:
  [who sets price](who-sets-price.md).
- What uninformed *forced* flow does to price — straight legs, overshoot, and the same-day
  V-reversal: [liquidity cascades & V-reversals](liquidity-cascades-and-v-reversals.md).
- Worked example: [Micron FQ3-2026 earnings](../../market-research/memory/micron-fq3-2026-earnings.md) ·
  sector context [semiconductors](../instruments/semiconductors.md).

## Open questions
- Do **OWR/GPIN** (the models that reportedly lack PIN's turnover-conflation defect) give a usable real-time
  read, or do they fail out-of-sample like most microstructure signals?
- Is there a **net-of-cost** edge to *fading* uninformed pre-earnings drift (the reversion base rate), or is it
  eaten by the [vol-risk premium / IV crush](fundamental-valuation.md) and transaction costs?
