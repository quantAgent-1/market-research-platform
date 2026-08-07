---
type: overview
title: The Alpha Map — Where This Desk's Actual Edge Lives, Ranked
description: The alpha-side answer to the institution-grade thread — five ranked hunting lanes with a named payer, a barrier, an implementation, an honest size, and a kill test each. Lane 1 = the Korea flow & crowding family (the real data moat, five sub-signals); then constraint-flow anticipation, cross-sectional residual reversal, the Asia→US information chain, and the gated discretionary event edge. Plus what is deliberately NOT re-mined (the Phase-1 killed menu) and the honest stacking arithmetic.
tags: [systematic-trading, market-research, korea, factor, process, small-account]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# The Alpha Map — Where This Desk's Actual Edge Lives

> Companion to [Institution-Grade, Profitable](institution-grade-quant-system.md) (process) and
> the [Phase-1 edge map](retail-capital-edge-map.md) (what's already been tested and mostly
> killed). This page is the alpha side only: **where positive expectancy plausibly exists for
> this specific desk**, ranked by prior × data advantage × barrier. Every lane states who pays,
> why it isn't competed away, and what kills it. From-training receipts are flagged; nothing here
> is validated until it survives the IC harness.

## The premise, in three sentences

Alpha is a **named payer plus a barrier**: someone predictably transferring money to you, and a
reason better-capitalized players don't take it first. The Phase-1 survey proved the generic US
retail menu is mostly barren — the honest conclusion was "risk control survives, alpha is
marginal." But that survey covered the *standard menu*; it did not cover the lanes where this
desk holds actual comparative advantages: **Korean flow data, the KST clock, Korean-native
context, and capacity so small that institutional competitors are structurally absent.** Those
are the lanes below.

## Lane 1 — The Korea flow & crowding family (the data moat) · highest prior

**Why this is the flagship lane:** KRX publishes **daily, per-name net flows by investor type**
(foreign / pension / investment-trust / insurance / private-fund / retail) — the most granular
public cohort-flow data of any major market. KOFIA publishes daily margin-loan balances. The
[program-trading page](../shared/concepts/krx-program-trading.md) adds the basket-flow lens.
Most of this is barely exploited in English-language quant tooling, and the engine's S-fetchers
already pull it nightly. The H6 module uses this data as a *risk overlay* (crowding state); the
unmined part is the **cross-sectional, per-name alpha versions**. Five registered-hypothesis
candidates:

1. **Retail-extreme contrarian.** Korean and international literature (Barber–Odean family;
   Korean-market studies ⚠️ from-training) consistently finds intense retail net *buying*
   negatively predicts short-horizon returns — lottery preference and dip-catching against
   informed flow. Signal: z-score of retail net-buy intensity (value / ADV) per name; fade the
   extremes at days–weeks horizon. **Payer: Mistake.** Barrier: capacity-tiny per name, needs
   daily Korean data plumbing.
2. **Foreign-flow persistence.** Foreign net flows are autocorrelated (large mandates execute
   over days — the √-impact slicing mechanics) and positively predict continuation while a
   streak runs. Signal: streak length × intensity, entered *with* the streak, exited on the
   first break. **Payer: Constraint** (the foreign institution pays impact to demand liquidity
   over days; you front-run the remainder of its own schedule). Barrier: requires daily
   monitoring; decays fast at longer horizons.
3. **Margin-flush mean reversion (the belt, weaponized per-name).** The
   [reverse-margin-call machinery](../shared/concepts/krx-session-clocks-and-forced-liquidation.md)
   is already documented: high margin-loan z-score + a hard down close ⇒ next-morning forced
   supply at the open, exhausting ~10:00 KST. The overlay version is live in H6; the alpha
   version is a *conditional per-name buy rule* at the flush. **Payer: Constraint** (the margin
   borrower is forced; the broker's liquidation algo is price-insensitive). Barrier: episodic
   (fires a few times a year), stomach-dependent, and the tail case (real information) must be
   handled by the breadth test.
4. **Leveraged-ETF close pressure.** Korea's single-stock 2× ETFs are ~14% of Samsung/SKH
   turnover; daily-rebalanced leverage must trade *in the direction of the day's move at the
   close* — computable **deterministically** from AUM × daily return (⚠️ from-training: the
   Cheng–Madhavan LETF-rebalance mechanics, applied to the Korean single-stock complex).
   Signal: predicted rebalance notional vs. ADV → fade the close-auction distortion next
   morning, or time entries away from amplified closes. **Payer: Constraint** (the ETF must
   rebalance regardless of price). Barrier: only matters on big-move days; requires the AUM
   archive (S5 — already live).
5. **The passive tide (비차익 streaks).** Multi-day one-way non-arbitrage program flow = the
   foreign passive allocation tide ([program trading](../shared/concepts/krx-program-trading.md)).
   Not a per-name signal (index flow is name-level noise) but a **market-level regime input**:
   the tide gauge behind lane-1 signals — fade retail against the tide, not into it.

*Honest size for the lane:* per-signal IC in the 0.02–0.05 class at best, with the flush and
LETF signals episodic rather than daily. The moat is real but the market is one country; treat
Korea as one sleeve, not the whole book.

> **Correction (2026-07-08, first-principles verification pass):** "data moat" overstated the
> barrier. KRX cohort flows are **public data**, actively used by domestic Korean quant desks
> and a large Korean academic literature — data *access* protects nothing here. What actually
> protects this lane: **capacity floors** (the per-name flush/LETF trades are institutionally
> too small), **attention/integration** (KST-native + fused with the discretionary sector book;
> scarce among English-language systematic operators — the honest meaning of "underexploited"),
> and the fact that competing local users are largely capacity-constrained too. Prior unchanged,
> reasons corrected: **a capacity-and-attention rent on public data, not an exclusivity rent.**
> Full derivation: [production model book, verification note 3](../systematic-trading/models/production-model-book.md).

> **Specced 2026-07-08:** Lane 1 is now registered as a testable strategy —
> [the Korea Flow Sleeve](../systematic-trading/strategies/korea-flow-sleeve.md): exact signal
> constants for all five sub-signals (the tide as gate), the sell-tax turnover arithmetic, kill
> tests pre-committed, and the five-block falsification plan on the live S3/S5/S10 feeds.
>
> **✅ Verdict 2026-07-11 — the falsification ran end-to-end** ([verdict note](../systematic-trading/strategies/korea-flow-sleeve.md#verdict-2026-07-11--the-first-full-data-run);
> single untuned pass, pre-registered constants, 633 names × 2016–2026). The flagship candidate
> here — **sub-signal #2, foreign-flow persistence — is DEAD** (momentum-purged residual IC
> *negative*: h=5 −0.0068, t −2.05; adversely selected in illiquid names, textbook
> anticipation-decay by era; the registered book lost before costs). **Sub-signal #1,
> retail-extreme contrarian, is VALIDATED as a negative signal** (IC −0.0126, t −2.84; negative in
> every era including 2026; strongest in the *most liquid* names) — its honest live role is
> exclusion/veto plus a fade where SSF access exists. #3 (margin-flush) shows the **right sign but
> is underpowered** as a daily-bar proxy and its true per-name form is feed-blocked (S12,
> KRX-login-gated); #4 (LETF close) is unrun pending AUM history (S5 archive accreting). **Net
> read: the lane's one durable edge is behavioral (retail-fade), not the flow-persistence core** —
> and the [cross-family finding](../systematic-trading/strategies/korea-flow-sleeve.md#verdict-2026-07-11--the-first-full-data-run)
> (every daily public-data signal alive 2016–22, dead/inverted 2023–26; only the behavioral one
> survives) turns the whole page's anticipation-decay prior into a *measured* property of this
> market. A 2-quarter forward clock is running (adjudicates ~2027-01).

## Lane 2 — Constraint-flow anticipation (the calendar knows) · high prior, low capacity

Mandated flow is calendar-known or trigger-known, and the desk already built the calendar
(ffcal). The tradeable Korean subset is less arbitraged than the US equivalents:

- **NPS band rebalancing:** the pension's target allocation bands are public; when equities
  drift outside them, the 연기금 row of the daily flow data shows the mechanical response —
  a predictable, slow, price-insensitive counterparty visible *daily* (US equivalents are
  quarter-end estimates; Korea publishes the actual cohort's prints).
- **만기/expiry unwinds:** the arb-balance unwind into expiry closing auctions
  ([program trading](../shared/concepts/krx-program-trading.md)) — risk-timing at minimum,
  fade-the-distortion at best.
- **Index reviews** (KOSPI200 June/December, MSCI): the *add-effect* is decayed (the ffcal
  design's honesty flag stands); the residual edge is providing liquidity against the forced
  tracker flow in the effective-day auction, not front-running the announcement.

**Payer: Constraint.** Barrier: each event is small and episodic — institutions can't scale it,
which is precisely why it's still there. Kill test: each event-type must show the predicted flow
in the actual cohort/program prints (measurable!) before any trade rule is registered.

## Lane 3 — Cross-sectional residual reversal (H2) · the statistical workhorse

Distinct from the Phase-1 survey's *time-series* index mean reversion (SPY RSI-2 — tested,
marginal): this is the **cross-sectional** version across 100–300 names — long the losers /
short-or-underweight the winners *in residual space*, harvesting the liquidity-provision
premium. ⚠️ From-training: Nagel (2012) shows reversal P&L behaves like compensation for
supplying liquidity, spiking in stress; gross profitability compressed since the 1990s but the
residualized weekly form persists; cost control decides the net. **Payer: Service** (impatient
flow pays for immediacy). Barrier: costs and infrastructure discipline — which is exactly what
the solution sheet builds. This lane is where **breadth** does the work the survey's single-index
version couldn't: same skill, √200 more bets. Status: next through the IC harness; the honest
expectation stays IC 0.02–0.05.

## Lane 4 — The Asia→US information chain (the timezone edge) · underexploited, natively yours

The desk is awake, Korean-native, and reading Asia's tape **before the US open prices it**:
Samsung prelim (8 quarters a year of memory-complex information), Korea's 1st/11th/21st export
prints, TSMC monthly sales, DRAM spot/contract fixings, Taiwan supply-chain monthlies. The US
memory/semis complex (MU, the SOX names) reprices much of this at 22:30 KST — hours after it was
legible in Seoul. ⚠️ From-training: the economic-linkage lag literature (Cohen–Frazzini
customer–supplier momentum; cross-listed lead–lag) documents that cross-border, cross-language
information diffuses slowly because attention is finite. **Payer: Mistake/limits-of-attention.**
Barrier: language + timezone + domain depth — the three things this desk has and a Connecticut
pod doesn't wake up for at 8:30 KST. Implementation: event-study first (did Seoul's reaction
predict the US open gap? — the desk literally graded a live rep of this today with the Samsung
prelim call sheet), then a scoped registered signal. This lane's discretionary form is already
the sprint; the quant form is unmined.

## Lane 5 — The discretionary event edge (in measurement) · highest ceiling, gated

The July sprint + campaign structure *is* an alpha lane: pre-registered event distributions on a
sector the desk knows deeply, graded rep by rep, with pre-committed gates before size. It is the
only lane that can plausibly pay 2:1 asymmetric chunks near-term — and the only one with a
formal ~1-in-5 honest odds statement attached. It stays firewalled from the quant book; its
*measurement discipline* is what makes it a lane rather than a hope.

## What is deliberately NOT re-mined

The Phase-1 kills stand: naive intraday (−EV even gross), PEAD in liquid US large-caps (dead
since ~2006; the residue is cost-eaten), calendar/seasonality standalone, overnight-drift
standalone (the NightShares liquidation is the real-money tombstone), leveraged-ETF "tactics,"
microcap "hidden alpha." Re-opening any of these requires new *mechanism* evidence, not a new
backtest — the registry remembers the trial count.

## The stacking arithmetic (honest)

Wrappers first: H1 regime gating and H3 momentum ballast are **not alpha** — they are what keeps
the alpha investable (drawdown control ⇒ the compounding survives to collect). On top of them,
the realistic stack is: lane 3 as the daily statistical base (breadth), lane 1 as the Korea
sleeve (data moat), lane 2 as episodic constraint capture, lane 4 as the event-window
sharpener — four *modestly correlated* small edges. If two or three validate at IC 0.02–0.04
with controlled costs, the stack plausibly runs **Sharpe ~0.7–1.2 unlevered** — a real system,
and still one whose dollar output scales with the denominator, not with wishing. The binding
constraint is unchanged: **hypothesis quality per experiment** — this page exists to feed the
IC harness better candidates, in this order: 1 → 3 → 2 → 4 (5 runs in parallel under its own
gates).

## Kill tests (pre-stated, one per lane)

1. Korea flow signals: each sub-signal must show IC > 0 out-of-registration on the daily flow
   panel within 2 quarters of data, or it's a story.
2. Constraint flows: the predicted mechanical flow must be *visible in the published cohort or
   program prints* on the predicted dates, or the mechanism is wrong.
3. Residual reversal: must survive 2× modeled costs and the orthogonality bar vs. H1/H3.
4. Asia→US chain: the event study must show the US-open gap is predictable from the Seoul
   session *beyond* what US futures already moved — if futures fully price it by 09:00 KST,
   there is no edge, only a story about one.
5. Discretionary: the campaign gates (already filed) — no gate, no size.

## Relationships

- **The mathematics for each lane: [the Alpha Model Book](../systematic-trading/models/alpha-model-book.md)** — full model specifications (eigenportfolio s-scores for lane 3, OFI/flow math behind lane 1, lead–lag estimators for lane 4).
- Process side: [Institution-Grade, Profitable](institution-grade-quant-system.md) · [the Solution Sheet](institution-grade-solution-sheet.md) · [execution layer](engine-v3/execution-layer.md)
- What was already tested and killed: [Small-Account Edge Map](retail-capital-edge-map.md) — this page extends it beyond the generic US menu
- The payer doctrine: [Who Pays You](../shared/concepts/who-pays-you.md) · [Techniques of Winning Trades](techniques-of-winning-trades.md) (the six counterparty families)
- The Korea machinery: [KRX Program Trading](../shared/concepts/krx-program-trading.md) · [KRX Session Clocks & Forced Liquidation](../shared/concepts/krx-session-clocks-and-forced-liquidation.md) · [H6 crowding module](engine-v3/h6-crowding-defector-module.md)
- The live measurement lane: July-2026 Sprint · the a small retail account→a multi-week return target campaign
