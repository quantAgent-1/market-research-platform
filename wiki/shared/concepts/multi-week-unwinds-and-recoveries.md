---
type: concept
title: Multi-Week Unwinds & Recoveries — The Cascade on a Days-to-Weeks Clock
description: The days-to-weeks version of the liquidity cascade. The same first principle (flow moves end at a quantity; the move lasts as long as the constraint lasts) applied to slower, overlapping constraints — the cohort clocks (leveraged ETFs intraday, CTAs trigger-based over days, vol-control vol-gated, calendar rebalancers in-window, hedge-fund de-grossing over weeks, redemptions over months). Why the move stretches (square-root slicing, cohort sequencing, the braid with genuine repricing), why crowded complexes sell off on thesis-ambiguous headlines (information sets direction, crowding sets magnitude), why recoveries print a W more often than a V (sequenced re-entry, the vol-control re-leverage clock), the boundary conditions, and what is predictable at this horizon. Worked example: the June–July 2026 memory tape, including the Jul-2 soft-jobs/record-Dow/SOX −6.7% controlled experiment.
tags: [systematic-trading, market-research, derivatives, positioning, flows, tail-risk]
timestamp: 2026-07-07T15:30:00Z
status: active
sources: []
---

# Multi-Week Unwinds & Recoveries — The Cascade on a Days-to-Weeks Clock

The [intraday cascade page](liquidity-cascades-and-v-reversals.md) explains why a huge straight
move can round-trip inside a single session. This page is its companion for the horizon most
selloffs actually live on: **days to weeks**. The physics does not change — flow moves still end
at a quantity, and the move still lasts exactly as long as the constraint lasts — but at this
horizon the constraints are slower, there are several of them overlapping, and the flow is
always braided with genuine repricing. Those three differences produce a recognizably different
shape: a grinding, multi-session decline instead of a straight line, and a retest-prone W
instead of a clean V. Graduated from the 2026-07-03 query thread; the June–July 2026 memory
tape is the worked example throughout.

## The same first principle, on slower clocks

A multi-week selloff is almost never one seller. It is a **sequence of finite programs firing in
order**, each belonging to a cohort with its own clock and its own termination condition. The
reason the move takes weeks is not that anyone chooses to sell slowly out of patience — it is
that each cohort *cannot* finish faster, or is not *triggered* until the one before it has
already moved the price.

| Cohort | What forces the selling | Clock |
|---|---|---|
| **Leveraged / single-stock ETFs** | daily rebalance is mechanical and pro-cyclical | intraday — amplifies the front of the move, never the tail ([leveraged-ETF decay](leveraged-etf-decay.md)) |
| **CTAs / systematic trend** | trend thresholds breach → front-loaded selling programs | a few sessions to ~2 weeks once a trigger trips |
| **Vol-control / risk parity** | exposure is a function of realized volatility | vol-gated — sells while realized vol is elevated, re-levers as it decays |
| **Calendar rebalancers** (pensions, index recon) | mandated weights at month/quarter-end | clears in-window at known dates |
| **Hedge-fund discretionary de-grossing** | losses, VaR, and prime-broker pressure | "weeks, not days" — the slow tail |
| **Fund redemptions** | client withdrawals | monthly to quarterly — the slowest cohort (Coval–Stafford 2007: fire-sale pressure at fund scale takes quarters to build and revert) |

The June 2026 unwind was this table measured live: two amplifiers (leveraged ETFs, vol-control)
front-loaded the move, the calendar leg cleared at the June-30 quarter-end exactly as called, and
the hedge-fund de-gross ran as the multi-week tail
([unwind duration & flows, 2026-06-30](../../market-research/positioning/unwind-duration-and-flows-2026-06-30.md)).
Korea adds a cohort of its own with a literal overnight clock: margin shortfalls are measured at
each day's close and force-sold at the *next morning's* opening auction, so a crash day
manufactures the following morning's supply
([KRX session clocks & forced liquidation](krx-session-clocks-and-forced-liquidation.md)).

## Why it stretches to weeks: slicing, sequencing, and the braid

**Slicing.** The square-root impact law makes it ruinously expensive to exit a large book
quickly, so institutional parent orders are sliced across days — a fund that must cut billions
physically cannot be done in a session
([price formation](price-formation-and-the-float-identity.md), §4). The selling has a cadence
because impact cost imposes one.

**Sequencing.** The cohorts arm each other. Selling marks prices down; falling prices raise
realized volatility, which makes vol-control sell; the combined pressure breaks a trend
threshold, which makes CTAs sell; the marks breach VaR limits and margin, which forces
hedge-fund de-grossing. Each cohort's finite program is the next cohort's trigger. This chain is
the multi-day analogue of the intraday feedback loops, and its canonical print is the August
2007 quant quake: three days of factor unwind as leveraged equity-neutral books de-grossed in
sequence, then a violent snapback on the fourth day (Khandani and Lo). Note what the chain
implies: the *order* of selling is somewhat predictable even when the start date is not —
amplifiers first, calendar flows at their dates, discretionary de-grossing last.

**The braid.** Unlike a single-session cascade, a multi-week move cannot be pure flow, because
real information keeps arriving — earnings, macro prints, headlines — and every new datum
re-sorts the crowd. The honest taxonomy therefore needs three boxes, not two: mechanical flow,
genuine repricing, and the hybrid that dominates in practice — **an expectations repricing on
genuinely new information, transmitted through still-fragile positioning. Information sets the
direction; crowding sets the magnitude**
(the Jul-1/2 selloff note).
The June–July 2026 tape shows the braid in one arc: the Jun-23 flush was mostly flow (a
Korea-led leveraged-ETF unwind); the quarter-end calendar leg cleared into a record Jun-30
close; and then Meta Compute — a real but thesis-ambiguous piece of information — landed on
positioning that was still fragile and started a second leg that no flow calendar could have
scheduled.

## Crowding is latent supply — why there is a selloff with "no thesis-breaking news"

Decompose price as **P = E × multiple**. News does not have to cut anyone's earnings to compress
the multiple, because the multiple is where positioning, narrative, and the distribution of
far-out scenarios live. A headline like Meta selling surplus compute changed no 2026 contract
and flipped no tripwire — it changed the market's *distribution* of 2027+ demand, and a crowded
complex was positioned for the old distribution. After a huge run, **everyone who could be long
already is**: the marginal buyer is exhausted, elastic demand is thin, and the crowd itself is
latent supply waiting for a trigger
(crowded longs & repricing mechanics).
That is why small headlines produce outsized moves in a crowded wing: the headline is the spark,
never the energy.

The evidence that distinguishes this from a genuine demand downgrade is **cross-sectional**. On
July 1, 2026 the ordering was SK Hynix (most re-rated) −14.6% > Micron −10.4% > Samsung
(diversified) −9.1% ≫ NVDA flat, Meta +10%, S&P −0.2% — de-grossing sells *the basket, not a
thesis*, so the most crowded expressions fall most while the index barely notices. The next
session provided something close to a controlled experiment: the June jobs print came in **soft**
(+57k vs ~113k consensus), removing the pre-registered "hot macro re-arms the systematic leg"
branch — and the SOX still fell another **6.7%** (after roughly doubling in the quarter) **while
the Dow closed at an all-time record**. A macro selloff does not print a record Dow; a dead
thesis does not leave the index untouched; a crowded momentum wing being de-grossed into
rotation does exactly this. The regime verdict stays with the pre-registered dashboard — the
tripwires read 0-of-8 flipped through the entire episode
(H2-2026 navigation playbook) —
never with the tape.

## The recovery: sequenced re-entry, and why it prints a W more often than a V

The buy-side flows return in roughly the mirror order of the selling, and the sequence is worth
memorizing because parts of it are schedulable:

1. **Short-covering and intraday mean-reversion systems** arrive first, at exhaustion prints.
2. **Vol-control re-leveraging** follows as realized volatility decays — this is the most
   schedulable buy flow in the market, because vol-target exposure is a near-deterministic
   function of the realized-vol path ([volatility forecasting](../../ml-stats/concepts/volatility-forecasting.md)).
3. **CTAs re-flip** when trend thresholds recover — trigger-based, like their exit.
4. **Corporate buybacks** resume when earnings blackouts end — a calendar flow.
5. **Slow money** re-rates last, at valuation floors, on fundamentals
   ([who sets price](who-sets-price.md)).

Because the slow tail of sellers (hedge-fund de-grossing, redemptions) is still finishing when
the first bounce arrives, the first rally into residual supply frequently fails, and multi-week
bottoms print as a **W or a retest** rather than a clean V: the second low on lower volume,
narrower breadth, and visibly less panic is the exhaustion signature at this horizon. Korea
compressed the pattern into a single morning on July 3, 2026 — the overnight margin-liquidation
belt dumped its forced supply into the open, the KOSPI flushed to 7,378, a buy-sidecar fired,
and the index closed +5.37% — the fast, mechanical version of the same reload-and-exhaust logic
([KRX session clocks](krx-session-clocks-and-forced-liquidation.md)). Recovery *confirmation* at
the weeks horizon looks like: laggards keep leading while the crowded wing stops making new
lows, then fundamentals reassert at the dated prints. The malign tell is the mirror image — the
crowded wing making new lows on rising volume with the laggards also down.

## When the recovery doesn't come — boundary conditions

- **Accumulation kills theses.** No single headline breaks a bull thesis, but an accumulation of
  same-direction data points does — each one fattens the tail scenario until the tripwires
  actually flip. "No thesis-breaking news" is a claim to re-verify on the dashboard every week,
  not a standing assumption; the earliest-turning tells deserve the most weight (in the 2026
  memory case: GPU rental price direction and neocloud credit spreads before contract prices and
  capex guides). The E-side counterpart is the [second-derivative clock](second-derivative-cycle-trading.md) —
  cyclicals top on deceleration, while earnings still rise.
- **Constraint chains restart the clock.** Clearing one constraint does not immunize the market
  against the next shock: new information landing on still-fragile positioning starts a new
  braid, as Meta Compute did on July 1 immediately after the quarter-end leg had cleared. An
  unwind is finished when positioning is washed out, not when the first constraint clears.
- **Reflexive conversion works on weeks too.** A long unwind can manufacture real damage —
  funding stress, product deaths, credit events in the levered corners (the neocloud credit
  channel is the named watch item in the 2026 case) — converting temporary impact into permanent
  loss. Every extended flush is a race between constraint exhaustion and induced damage
  ([liquidity cascades](liquidity-cascades-and-v-reversals.md), boundary conditions).

**The archetypes.** August 2007: three days of quant-factor unwind, day-four snapback — pure
sequenced flow. August 2024: the yen-carry unwind — Nikkei −12.4% in a day, +10.2% the next,
global equities round-tripping over about two weeks as the levered carry cohort finished.
February 2018: a vol-control and short-vol unwind that took the S&P down ~10% in nine sessions
and *did* convert reflexively for the short-vol products (XIV terminated); the index needed
months, not days. And the routine case worth normalizing: 8–15% semiconductor-index corrections
inside intact up-cycles are a *feature* of a crowded, high-beta complex, not evidence the cycle
ended.

## Flush or top? The discriminator is the revision cycle

The dangerous seduction of the flows framework is the rule "indiscriminate selloff = mechanical =
buyable." The cross-sectional evidence (a whole complex down together, sub-sectors with unrelated
fundamentals in lockstep, index vol asleep) genuinely does identify the *selling* as basket flow
rather than stock-picking on news — but **"indiscriminate" describes the selling, not the setup**.
In a crowded complex the unwind is not noise obscuring fundamentals; it is the market discovering
how much of the price *was* positioning. The mechanics of a flush look identical at mid-cycle and
at the top; what separates the flushes that V-recovered from the flushes that started −60/−70%
derates is **where the earnings-revision cycle stood**:

| The flush looked mechanical | Revisions were | Outcome |
|---|---|---|
| Aug-2007 quake · Aug-2024 yen-carry · Apr-2025 tariff · Jun-2026 ×3 | still accelerating | V/W recovery, new highs |
| Mar-2000 · Nov-2021 growth liquidation · Oct-2018 semis | peak already behind | the flush was the first leg down |

So the rule needs its conditional restored: *buyable if the revision cycle is still accelerating*
— and that is a dashboard question ([second-derivative clock](second-derivative-cycle-trading.md),
the tripwires), never a tape question. Two tape tells do carry real information at this boundary:
**good-news-sold** (a record print sold hard reveals positioning saturation — no marginal buyer
at these prices even for the best number; the single most informational price action there is)
and the **bounce-strength sequence** (accumulation = flushes met by strong fast Vs; distribution
= progressively weaker bounces — the crowd's own de-leveraging can *be* the topping mechanism).
A further useful split: **pure margin cascades are price-insensitive and exhaust in hours-days**
(Aug-5-2024 bottomed intraday), while **discretionary de-grossing is price-sensitive and runs
weeks**, pausing on bounces — a tape where the anchor name is being *kept* (chosen, not dumped)
while the crowded expressions are cut is de-gross, not cascade, and its clock is the slow one.
Live application with both tells firing: the Jul-7-2026 SOXL scenario map
(Samsung's record beat sold −9%; strike one on the bounce detector).

## What is predictable at this horizon — and what is not

- **The dates are the most predictable object in the system**: quarter-ends, option expiries,
  index reconstitutions, buyback blackouts, earnings, macro prints. The calendar leg of any
  unwind can be written down in advance (operationalized in this repo as the forced-flow
  calendar tool, `tools/calendar/`).
- **Cadence and mechanism are durable; levels are always stale.** Which cohorts sell in what
  order, and on what clocks, is knowable; how much dry powder each has left at any moment is
  not. Trade the calendar and the thresholds, never the unobservable residual.
- **The second moment is genuinely forecastable** — elevated volatility for days-to-weeks after
  a shock is a high-confidence statistical forecast, and it feeds both sizing and the
  vol-control re-leverage clock ([volatility forecasting](../../ml-stats/concepts/volatility-forecasting.md)).
- **The spark, the direction, and the real-time flush-vs-break classification are not
  forecastable.** Only the tripwires resolve regime, with a lag. The honest ceiling of a good
  system is the [monitoring system's](../../synthesis/semiconductor-monitoring-system.md)
  no-hindsight output: *"violent two-way move probable this week; regime intact, lean buyable;
  size to survive both branches."* That is condition-recognition, and it is everything the
  gauges can deliver.

## What it means for trading

The days-to-weeks clock is where a small account's payer actually lives — the Constraint payer's
flows are large, scheduled or triggered, and too slow for the microstructure arms race to
harvest completely ([who pays you](who-pays-you.md)). The design consequences carry over from
the intraday page with one addition each way. Pre-commit plans at the *dated* catalysts, because
the dates are the forecastable part. Expect the W: the first bounce into a slow tail is the
lowest-quality entry, and the retest on drying volume is the highest. Size for the braid — some
component of every multi-week decline is genuine repricing, so the position must survive the
case where the multiple stays compressed. And keep the feedback loop: every read pre-registered
before its catalyst, graded after ([navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md)).

External sources for the July 2 session facts:
[Yahoo Finance — June payrolls +57k vs expectations](https://finance.yahoo.com/economy/article/june-jobs-report-us-payrolls-rose-by-57000-missing-expectations-190000748.html) ·
[Yahoo Finance live — Dow record, semis extend decline](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-2-223136955.html) ·
[TheStreet — July 2 close](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-2-2026).
Academic anchors: Khandani–Lo (2007); Coval–Stafford (2007); Brunnermeier–Pedersen (2009);
Daniel–Moskowitz (2016); Harvey et al. (2018).

## Relationships

- **The single-session version — same physics, faster constraint:**
  [liquidity cascades & V-reversals](liquidity-cascades-and-v-reversals.md).
- **The live measured instance of the cohort clocks:**
  [unwind duration & flows, 2026-06-30](../../market-research/positioning/unwind-duration-and-flows-2026-06-30.md);
  the braided second leg: the Jul-1/2 selloff note;
  the flush-vs-top boundary live: SOXL scenario map, Jul-7.
- **The Korea-specific overnight constraint clock:**
  [KRX session clocks & forced liquidation](krx-session-clocks-and-forced-liquidation.md).
- **Crowding as latent supply, in depth:**
  crowded longs & repricing mechanics ·
  [distribution & pullback tells](distribution-and-pullback-tells.md).
- **The instrument panel that watches all of this:**
  [semiconductor monitoring system](../../synthesis/semiconductor-monitoring-system.md) (fuel /
  spark / regime); the regime dashboard: H2-2026 navigation playbook.
- **The forecastable piece:** [volatility forecasting](../../ml-stats/concepts/volatility-forecasting.md) ·
  [regime detection](../../ml-stats/concepts/regime-detection.md).
- **The risk philosophy:** [navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md) ·
  [who pays you](who-pays-you.md) · [small-account edge map](../../synthesis/retail-capital-edge-map.md).

## Open questions

- Can cohort *completion* be measured live — CTA-model replication, vol-control exposure
  estimates from the realized-vol path, blackout calendars — well enough to time the W's second
  low, rather than merely recognize it afterward?
- What fraction of a multi-week drawdown's variance is flow versus repricing, measured ex post
  by how much reverts — and does that decomposition stabilize enough to be a usable prior?
- Korea's daily per-name cohort flows are the best free positioning data in the world: can they
  support an unwind-stage classifier (building / climaxing / exhausting) at the weeks horizon?
