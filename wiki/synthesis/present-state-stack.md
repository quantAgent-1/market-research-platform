---
type: overview
title: "The Present-State Stack — Ten Tools That Recover the Institutional Map at Retail Cost"
description: The build list — ten pieces of software (public data + news + one ~$99/mo Alpaca market-data subscription) that recover the recoverable slices of the institutional present-state map for a tech/AI-focused KRX+US desk — flow visibility, the mechanical calendar, dealer gamma, expectations, cascade detection, nowcasting, and self-measurement — with July-sprint sequencing, per-tool kill criteria, and honest limits on what stays unbuyable.
tags: [systematic-trading, engineering, tooling, data, market-structure]
timestamp: 2026-07-06T00:00:00Z
status: active
sources: []
---

# The Present-State Stack — Ten Tools That Recover the Institutional Map at Retail Cost

Filed 2026-07-06 from a session Q&A. This page answers the open question left by
[what elite traders actually know](what-elite-traders-actually-know.md): institutions' real
edge is a **map of the present** — who is positioned how, who is forced to trade when — so
which slices of that map can a retail desk rebuild in software? The inputs allowed: public
data, news feeds, and one paid Alpaca market-data subscription (the ~$99/mo tier buys the
consolidated SIP equities tape, real-time OPRA options data — chains, Greeks, open interest —
and the Benzinga news stream; confirm plan inclusions at signup). Focus: the tech/AI complex
(semis and memory first) on a KRX + US footprint, at the days-to-weeks horizon.

**Rule zero — the anti-platform-trap contract.** The
[curriculum](quant-trader-curriculum.md) names over-engineering infrastructure before an edge
is validated as this desk's most seductive failure mode. So every tool below signs the same
contract: it must print into the **daily pre-market brief** (the
[morning call sheet](../systematic-trading/checklists/morning-call-sheet.md)'s data section)
within one week of build start, or it is cut. One brief, many sensors. And where a tool
overlaps [Engine v3](engine-v3/index.md), it is built *as an engine module*, not a new repo —
H6 (crowding → defector → Signal-C re-entry, with KOFIA margin and KRX event feeds already
specced) is the spine this stack hangs off.

## Tier 1 — the moat and the calendar (July must-builds)

### 1. KRX Flow & Fuel Engine *(finish what H6 started)*

The single most institutional dataset this desk can touch is free: KRX publishes **daily
per-name investor-type flows** (foreign / institutional subtypes / retail), short-sale volume
and balances, and program-trading stats; KOFIA publishes daily margin-loan balances (신용융자)
— the cascade fuel gauge. The tool: ingest all of it nightly, compute per-name 5/20/60-day
cumulative net-buy by cohort, foreign-flow persistence runs, cohort divergence (retail
accumulating what foreigners distribute is the wiki's distribution tell), margin-balance
z-scores per name, and a "who owned today's move" attribution line for every ±2% day on the
watchlist. This is the retail replica of a prime broker's positioning notes — and Korea is the
one market where the replica is nearly the real thing.
**Data:** KRX data portal, KOFIA freesis (both free; S10/S11 in the H6 handoff already point at
them). **Build:** ~15h beyond the H6 slice. **July:** yes — it is the moat.

### 2. Forced-Flow Calendar

The mechanical calendar as software, because constraint flow is the only *scheduled* alpha in
existence. One machine-readable calendar merging: US monthly/quarterly option expiries and the
KRX expiry Thursdays; index rebalance dates (S&P quarterly, MSCI reviews, KOSPI200 June/Dec);
month/quarter-end pension-rebalance windows; **per-name buyback blackout windows** derived from
earnings dates (the corporate bid vanishing exactly when event risk peaks); lockup expiries;
earnings dates; and the macro tape (CPI/FOMC/PCE, BOK, Korean 1st/10th/20th-of-month customs
exports, TSMC monthly revenue ~10th). Output: a "next 10 days — who is forced to trade, and
when" block auto-prepended to the morning brief. This tool is mostly knowledge, barely code —
the highest understanding-per-line on the list.
**Data:** all public (exchange notices, index-provider schedules, IR pages, release calendars).
**Build:** ~10h + light upkeep. **July:** yes — week 1.
**Design:** full buildable spec filed → [forced-flow calendar](../designs/forced-flow-calendar.md)
(15 feeds, event schema, density score, day-of T-schedules, Day-1-live plan).

### 3. Dealer Gamma & Options Positioning Map

For the watchlist plus QQQ/SMH/SOXX: pull full option chains daily (OI, volume, IV, Greeks) and
compute the standard dealer-positioning estimate — net dealer gamma by strike under the usual
customer-long-puts/short-calls sign conventions, the **gamma flip level**, the biggest OI walls
(pin candidates into expiry), 25Δ skew versus its own 1-year history, term-structure kinks
around events, and the **straddle-implied move for every known catalyst** (the number the
Micron post-mortem had
to derive by hand). Output: a per-name "dealer weather" line — amplifying (short gamma) vs
damping (long gamma) — plus levels that matter into opex. This is the retail clone of the
SpotGamma/SqueezeMetrics layer, which is itself the retail clone of a dealer's book.
**Data:** Alpaca OPRA (OI refreshes daily; IV/quotes intraday). **Build:** ~15–20h.
**July:** yes — before the Jul-17 opex.

### 4. Cascade Sentinel *(Signal C's live runtime)*

The live companion to H6: a websocket process on the SIP tape that watches the AI complex for
the cascade signature in real time — straight-line directional runs vs ATR, complex-wide
breadth collapse (everything down in lockstep = flow, not information), realized-vol spikes vs
the 20-day, volume-at-price anomalies, KRX VI-halt proximity on Korean mornings, and the
**leveraged-ETF close-rebalance estimate** (SOXL/TQQQ AUM × day's return → publishable MOC
pressure by ~15:00 ET). Output: the CASCADE/EXHAUST state machine as alerts, so the
[V-day checklist](../systematic-trading/checklists/catching-the-v-day-checklist.md) runs on
data instead of adrenaline.
**Data:** Alpaca SIP stream + public ETF AUM/shares-outstanding files + KRX. **Build:** ~20h,
but much of the state machine already exists as Signal C in `enginev3` — this is
productionizing, not inventing. **July:** yes — it is the sprint's live lab instrument.

### 5. Breadth Discriminator *(the informed-vs-uninformed one-pager, automated)*

On any >2σ move in a watchlist name, auto-run the
[breadth test](../shared/concepts/informed-vs-uninformed-flow.md): the name vs its true peers
vs sector ETFs vs the macro tape, across both markets; options confirmation (is skew steepening
*beyond* the normal pre-event ramp?); short-interest and borrow deltas; KRX cohort attribution
from Tool 1. Emit one verdict: **idiosyncratic** (dig — something may be known) or **shared**
(de-risking flow — reversion base rate applies, Signal C territory). This automates the page
this desk already runs by hand on every scary day.
**Data:** derived — sits on Tools 1, 3, 8. **Build:** ~6h once its parents exist. **July:** yes
— cheap and used weekly.

## Tier 2 — the expectations and news layer (start in July, finish in August)

### 6. Event-Shock Classifier *(news → mechanism, not news → feelings)*

A pipeline on the Benzinga stream + SEC EDGAR real-time feeds + watchlist IR/RSS that uses an
LLM to tag every item with the only questions that matter: **new fact or recycled?** which
mechanism (guidance / capex / pricing / supply / regulatory / macro)? and **who is now forced
to do what?** — the anti-curriculum's required lens. Its main output is silence: ~95% of items
marked noise, so news stops being a stimulus and becomes a structured delta feed. Second job:
a **Form 4 filter** implementing the routine-vs-opportunistic split (the
[82 bp/mo result](what-elite-traders-actually-know.md)) on watchlist insiders, with
cluster-buy detection. Honest purpose: you will never beat machines to the trade on news; the
goal is *correct classification within minutes*, so you are never late **and** wrong.
**Data:** Alpaca/Benzinga news, EDGAR (free), IR feeds; Claude API for extraction.
**Build:** ~15h. **July:** skeleton only (watchlist 8-K/Form-4 alerts); full version August.

### 7. Expectations & Implied-Move Tracker

The "what is priced in" card, generated before every known catalyst: consensus revision
direction and breadth over the last 4 weeks (scraped from public aggregators — cruder than
IBES, honestly so), the straddle-implied move from Tool 3, your own p10/p50/p90 written into
`calls.csv` before the print (the calibration rep), the post-print drift state, and the
**price-vs-target-wall gap** as the skepticism gauge from
[who sets price](../shared/concepts/who-sets-price.md). SK hynix Jul-29 and the megacap
gauntlet are the July test cases.
**Data:** public scraping + Tool 3. **Build:** ~12h. **July:** the implied-move + call-sheet
half (that part is sprint-critical); revisions half August.

## Tier 3 — the slow map (August; weekly cadence, not daily)

### 8. US Positioning Composite

The lag-honest US replica of Tool 1: weekly CFTC COT on NQ/ES, FINRA short interest
(twice-monthly) plus the daily Reg SHO short-volume ratio per name, ETF flow tracking from
shares-outstanding files (SMH/SOXX/QQQ + the leveraged complex), a 13F diff engine over ~20
relevant funds (45 days stale — trend information only), and CBOE put/call + skew composites.
Output: a weekly **crowding score** per name/sector that feeds H6's Signal-A condition.
Everything here lags — so it is a *condition*, never a trigger, exactly as H6 specs it.
**Data:** all public. **Build:** ~10h. **August.**

### 9. Tech/AI Fundamentals Nowcaster

The alt-data slice where this desk is genuinely competitive, because the world's best
semiconductor nowcast data is public and publishes in this timezone: Korean customs
1st/10th/20th-of-month exports (the semis line leads the global complex), TSMC monthly revenue,
memory spot-price headlines, an LLM-extracted hyperscaler-capex tracker from transcripts (capex
guidance is the sector's master variable), SIA/WSTS monthlies. Output: the
[semiconductor monitoring system](semiconductor-monitoring-system.md)'s regime gauge, automated
— a cycle dial that updates itself instead of being hand-curated.
**Data:** public; Claude API for transcript extraction. **Build:** ~12h. **August** (the manual
dashboard covers July).

### 10. Calibration & Execution Ledger *(smallest tool, non-negotiable)*

The institutional risk-and-TCA layer at desk scale: auto-grade every `calls.csv` entry (Brier
score by claim type, calibration curve by bucket — the Monday ritual, computed); pull every
live fill from the Alpaca account API and measure **slippage vs arrival and VWAP** (the "free
money" of the curriculum's execution topic); track tuition-budget burn against the
[risk constitution](../systematic-trading/checklists/trading-risk-constitution.md)'s caps; and
keep the per-setup expectancy ledger (Signal C shadow calls vs actual outcomes). Institutions
are elite in *process* before information — this tool is that process, and it must exist before
any size increase.
**Data:** own records + Alpaca account API. **Build:** ~8h. **July:** yes — week 1, alongside
Tool 2.

## The honest limits — what this stack does and does not buy

What it recovers well: **constraint flow** (Tools 1, 2, 4 — near-institutional grade, because
forced flows are public by nature and Korea publishes the fuel data daily); **dealer-positioning
weather** (Tool 3 — direction and levels, though the sign conventions are heuristics and a real
dealer's book is invisible); **the expectations interface** (Tool 7's implied-move core is
exactly what a desk uses); **the semis nowcast** (Tool 9 — competitive outright); and
**institutional process** (Tools 5, 10 — calibration, mechanism-tagging, TCA — available at any
account size, immediately).

What stays unbuyable at any retail price: internalizer and dealer client-flow visibility,
prime-broker crowding aggregates, millisecond speed, IBES-grade estimate depth, expert-network
access. The stack's answer is the horizon: at days-to-weeks on liquid tech names, those missing
slices are mostly someone else's game — which is precisely why the
[curriculum](quant-trader-curriculum.md) put arena choice above effort. "Elite institutional
decisions" here means decisions made *with the institutional checklist* — calendar-aware,
flow-attributed, expectations-anchored, mechanism-tagged, sized by rule, and scored — not
decisions made with institutional information, which no tool list can honestly promise.

Total running cost: ~$99/mo (Alpaca) + Claude API usage; everything else is free. A Bloomberg
seat is ~$30k/yr; the recoverable fraction of what this desk actually needs from one is most of
this list.

## Build order and the July reality check

July engine-block hours are finite (~2–3h/day inside the
sprint template ≈ 60–70h). The July set — finish Tool 1, build Tools 2,
3, 10, productionize Tool 4, add Tool 5, plus Tool 7's implied-move half — fits at ~70h only
because Tools 1 and 4 are partly built inside H6. Tools 6, 8, 9 and the rest of 7 are August.
Per-tool kill criterion, pre-registered: **printed into the morning brief within 7 days of
build start and referenced in at least one graded call within 14 — or cut.** The stack exists
to sharpen calls, not to exist.

## Relationships

- Sibling layer: [the research accuracy stack](research-accuracy-stack.md) — the same doctrine
  applied one level up, to the *research agents* that write the market-research pages (source-tier
  ladder, EDGAR/DART/macro fetchers, procedure-as-skills); tools 6/7/9 here share its plumbing.
- Answers the open question in
  [what elite traders actually know](what-elite-traders-actually-know.md) (which map slices are
  recoverable at retail cost).
- Extends [Engine v3](engine-v3/index.md) — Tools 1, 4, 8 are H6 modules or feeders, not new
  repos; the [H6 handoff](engine-v3/h6-first-build-handoff.md) already carries the S10/S11
  endpoints.
- Instruments the July-2026 sprint and the
  [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md); enforced by the
  [risk constitution](../systematic-trading/checklists/trading-risk-constitution.md).
- Operationalizes: [who pays you](../shared/concepts/who-pays-you.md) (Constraint harvesting),
  [informed vs. uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md) (Tool 5),
  [who sets price](../shared/concepts/who-sets-price.md) (Tool 7's skepticism gauge),
  [liquidity cascades](../shared/concepts/liquidity-cascades-and-v-reversals.md) +
  [KRX session clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md) (Tool 4),
  [the semiconductor monitoring system](semiconductor-monitoring-system.md) (Tool 9).

## Open questions

- Alpaca plan verification: does the current $99 tier include real-time OPRA with OI and
  Greeks, and are options websockets rate-limited enough to need EOD-batch fallbacks?
- Gamma-map validation: do the heuristic dealer-sign conventions reproduce the published
  SpotGamma-style flip levels closely enough to trade around, or only directionally?
- KRX short-sale and program-trading feeds: publication lags and revision behavior under the
  recurring short-sale-ban regimes — what exactly is available live in 2026?
- Which August tool earns promotion to July if a week frees up — the Form-4 filter (6) or the
  nowcaster (9)?
