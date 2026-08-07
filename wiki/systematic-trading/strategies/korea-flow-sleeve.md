---
type: strategy
title: The Korea Flow Sleeve — Lane 1, Specced to Registration
description: The alpha map's highest-prior lane turned into a testable strategy — a long-only KOSPI sleeve built from per-name investor-flow signals (foreign-flow persistence as the core, retail-extreme exclusion, margin-flush and LETF-close conditionals), with the sell-tax cost wall driving the design, exact pre-registered constants, and a one-week falsification plan on data the engine already pulls. VERDICT FILED 2026-07-11 — F (flagship) dead, R validated as a negative signal, M/L unrun; the registered book would have lost ~7.8%/yr net; 2-quarter forward clock running.
tags: [systematic-trading, korea, factor, flow, small-account]
timestamp: 2026-07-11T00:00:00Z
status: active
sources: []
---

# The Korea Flow Sleeve — Lane 1, Specced to Registration

> **What this page is.** The [alpha map](../../synthesis/alpha-map.md) ranked five lanes where
> this desk plausibly has positive expectancy and ordered the harness queue 1 → 3 → 2 → 4. Lane 1
> (the Korea flow & crowding family) has the highest prior but existed only as five named
> hypotheses. This page takes it the rest of the way: exact signal definitions with pre-registered
> constants, the cost arithmetic that dictates the shape, the portfolio form, the validation
> protocol, and kill tests written *before* the first backtest run. Under the wiki's own doctrine
> ("models don't have alpha; situations do"), **"finding a profitable strategy" is not picking a
> model — it is registering the best-priored payer-plus-barrier situation and trying to kill it.**
> This is that registration. Nothing here is validated yet; the point of the page is that the
> verdict, either way, will be trustworthy.
>
> ⚠️ marks from-training claims (literature, tax rates, data availability) that must be verified
> at Tier-0 before live money touches any rule — per the
> [research accuracy stack](../../synthesis/research-accuracy-stack.md) ladder.
>
> **✅ VERDICT FILED 2026-07-11 — see [the verdict note](#verdict-2026-07-11--the-first-full-data-run) below.**
> The flagship signal (F, foreign-flow persistence) is **dead**; the exclusion filter (R,
> retail-attention extremes) is **validated as a negative signal**; M and L stayed unrun on named
> blocked feeds. The registered book would have lost ~7.8%/yr net. This is the desk's first
> falsification run carried end-to-end — the verdict machine did its job before a won was risked.

## Verdict (2026-07-11) — the first full-data run

*Filed by the maintainer after the first full-data run of the falsification harness. The
constants below were pre-registered on 2026-07-08 (in git, on this page) and were **not touched**
at any point; this was a single untuned pass over 2016-03 → 2026-07 — roughly 2,520 daily
cross-sections, 633 names, the as-of top-150 universe (2,828 sessions, flow coverage 99.8%).
Point-in-time integrity was independently checked: deleting the last 40 sessions changed zero
derived values on earlier dates (14/14 columns). Full machine record:
`enginev3/research/sleeve/out/verdict.md`; trials registered in `research/experiments.jsonl` under
family `sleeve_lane1`, run `sleeve-20260711`.*

**Component F — foreign-flow persistence (the flagship): DEAD.** The pre-registered test demanded
the momentum/reversal/size-purged *residual* IC be positive with Newey–West t ≥ 2. It failed in
the strongest way the data can fail a hypothesis — the residual IC is **negative** (h=5: −0.0068,
t = −2.05; h=10: −0.0045, t = −1.04). Three things about the anatomy are worth keeping:

- **Where the negative sign lives:** the small-ADV tercile (−0.0161, t = −3.06); large caps are
  flat-dead (−0.0026, t = −0.49). Visible foreign "persistence" in illiquid names is *adversely
  selected*, not merely arbitraged away — you're the liquidity the informed schedule is picking off.
- **The era structure is textbook anticipation-decay:** 2016–19 IC −0.013 (t −4.1), 2020–22 −0.024
  (t −5.9), and 2023–26 **+0.005 after the purge** while raw is +0.015 — i.e. the only recent
  positive years are momentum wearing a flow costume, which is *exactly* the pre-registered
  falsification, not an escape from it.
- **The P&L agrees:** the registered long book ran gross CAGR −0.20% against the universe's +10.2%
  (it loses *before* costs), −7.8%/yr net, DSR 0.00.

The 1990s–2000s literature edge (Froot–O'Connell–Seasholes, Richards) is not merely gone from this
market at weekly horizons — *following it has been mildly toxic.* The sign-flipped variant ("buy
what foreigners persistently sell") was **not** registered and **not** evaluated as a strategy; it
is noted only as a hypothesis the 2016–22 data would have supported and the 2023–26 data kills, so
it is dead on arrival and stays off the book. Long-side F does not come back without the forward
clock (kill 5) flipping the recent era to significance first.

**Component R — the retail-attention exclusion: VALIDATED as a negative signal.** IC −0.0126
(NW t = −2.84) at h=5 and −0.0105 (t = −2.00) at h=10; **negative in every era**, including
2023–26 and 2026 YTD; non-overlapping robustness holds at the one-week horizon (−0.0195, t = −2.46)
and the effect is front-loaded in the first week (the h=10 non-overlap read collapses to zero — so
use it at 1-week, not two). The sharpest and most operationally lucky finding: the edge is
**largest in the top-ADV (most liquid) tercile** (−0.0231, t = −2.93) — attention extremes in the
biggest, most tradeable names are the fade-worthy ones, which is precisely where single-stock
futures, borrow, and the desk's discretionary lanes live. R is firing at record intensity in the
current tape (430 name-days in 2026 H1; active in 86% of sessions). Live roles, in order: (1) a
validated **exclusion/veto** on any KR long entry; (2) a **fade/short input** where SSF access
exists (an unresolved ops item); (3) an **entry-timing veto** for the discretionary July-campaign
reps. R's forward IC is now tracked by the same clock as F.

**The provision leg (diagnostic, not a kill row): right sign, underpowered.** Retail z ≥ +2
arriving on a ≤ −10% five-day flush — the Kaniel–Saar–Titman channel, defined verbatim above —
earns +27bp mean forward-5d residual against a −10bp universe baseline (+37bp relative), but at
t = +1.42 over 1,247 decade-events it is not deployable standalone. It is, however, direct evidence
*for* Component M's design: M adds the credit-balance condition and the intraday-exhaustion trigger
precisely to fatten this per-event edge. M stays the queue's best long-side episodic candidate.

**Components M and L — NA, feeds named honestly.** M needs the per-name credit-balance feed (S12,
a half-day build) — but KRX's portal is now login-gated end to end, and Naver/Daum were verified to
lack per-name credit, so the endpoint hunt is unresolved. L needs per-fund AUM *history* for the
Korean single-stock 2× complex (confirmed large — one SK Hynix 2× fund alone ~₩3.9T), which no free
endpoint serves historically; the engine's S5 archive accumulates it daily, so the event study
becomes runnable on live-collected data in ~1–2 quarters. Neither was run; neither is killed.

**Kill 5 — the 2-quarter out-of-registration forward test: RUNNING.** `signals.py` logged its
first live book (as-of 2026-07-10) to `forward_log.jsonl` on 2026-07-11. The clock adjudicates
around 2027-01 — era-3's F sign, R's persistence, and the provision leg's power all get free
out-of-sample evidence from the same log.

**Addendum (same day, on the "keep working" directive) — two more pre-specced families run to
verdict on the same panel:**

- **M-lite** (Component M's buildable daily-bar proxy; gates pre-stated): **DEAD.** Buy a name
  after a ≤ −5% day with retail z ≥ +2 and the KOFIA credit belt loaded (belt history extended to
  a decade, 2015–26, in one call); at the registered T+3 exit it grosses +14bp/event against a
  ~46bp round trip — **net −35bp** (t = −2.31, 1,727 events). Single-day −5% crashes are
  news-dominated *falling knives*, not mechanical flushes; the registered form's intraday-exhaustion
  trigger and information-tail guard were load-bearing exactly as this page argued. True per-name M
  stays paper (S12 blocked), prior lowered.
- **Lane 3** (the solution sheet's H2 cross-sectional residual reversal; IC-first): **DEAD at the
  gate** (h=3 IC +0.0081, t +1.90; h=5 +0.0060, t +1.21). It is real and significant at 1–2 days
  (h=1 t +2.90), mid-cap concentrated, and alive 2016–2022 — but **dead-to-negative in 2023–26**
  (−0.0030, t −0.56), and unharvestable long-only at KR retail costs even when it was alive.

**The cross-family finding (the run's most important number-free result).** Every daily-frequency
public-data cross-sectional signal tested — foreign-flow persistence, flush-buying, short-term
reversal — was alive *somewhere* in 2016–2022 and is **dead or inverted in 2023–2026**, while the
one *behavioral* signal (R, attention-extreme fade) survives all eras including 2026. The
six-layers public-data ceiling
and the anticipation-decay doctrine are no longer priors on this desk — they are now **measured
properties** of this market's current era. What remains retail-reachable in KR equities, as of this
run: behavioral extremes (the fade side), episodic mechanical forms that need gated feeds (true M,
L), weeks-horizon cohort positioning (untestable without KRX credentials), the discretionary event
lanes — and verification itself, which this run used to convert three would-be strategies into two
cheap kills and one asset.

**What ships, and what does not.** Ships: `signals.py` (the daily generator — now known dead and
kept *only* as the forward-clock instrument, plus the validated EXCLUDED list and exit flags), the
falsification harness itself (reusable for every next lane on this panel), and this verdict. Does
not ship: any claim that the registered long sleeve makes money — it would have lost ~7.8%/yr net.
**Next lanes, ranked by what this data says:** (1) S12 + Component M (provision sign confirmed, the
episodic form clears the cost wall by construction); (2) an R-fade feasibility check at a Korean retail broker (SSF
access tiers — R is the only validated signal with a direct harvest path); (3) the L event study
once the S5 archive matures; (4) a free KRX account (`data.krx.co.kr`) unlocks exact per-cohort
flows *and* removes this run's two data caveats — worth the five minutes.

## The strategy in one paragraph

A **long-only sleeve on the ~150 most liquid KOSPI names** that holds, for two to four weeks at a
time, the names that foreign institutions are *persistently accumulating* — because a large
foreign mandate cannot buy its position in one day, and the visible start of its buying predicts
the rest of its own schedule. Around that slow core sit three sharpeners: an **exclusion filter**
that refuses to hold names retail investors are piling into after a big run-up (the one retail
behavior that reliably precedes underperformance), a **margin-flush conditional buy** that
purchases the mechanical forced-selling exhaustion on the morning after a hard down day in
high-credit names (the belt from the
[forced-liquidation machinery](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md),
weaponized per-name), and a **leveraged-ETF close-pressure fade** that trades against the
deterministic rebalance distortion the Korean single-stock 2× complex imprints on big-move
closes. The whole sleeve sits behind the engine's regime gate and the
[H6 crowding state](../../synthesis/engine-v3/h6-crowding-defector-module.md). Every input is
public, daily, and already flowing through engine-v3's fetchers; what protects the lane is not
the data but **capacity floors and attention** — the trades are too small for institutions and
require a KST-native operator ([alpha-map Lane-1 correction](../../synthesis/alpha-map.md)).

## Why this candidate, and not something else

Three filters pick it. First, the [Phase-1 kill list](../../synthesis/retail-capital-edge-map.md)
stands — the generic US retail menu (intraday, large-cap PEAD, seasonality, overnight drift,
LETF "tactics") is not re-mined. Second, among the alpha map's lanes, Lane 1 is the only one
whose *entire data plane is already live in production*: S3 (per-name investor-type flows,
point-in-time clean, free), S5 (ETF AUM/shares-outstanding archive with the leveraged registry),
S10 (KOFIA margin credit) run nightly in engine-v3. Lane 3 (residual reversal) is already specced
as H2 in the [solution sheet](../../synthesis/institution-grade-solution-sheet.md) and queued;
Lane 2 rides on ffcal and shares this page's cohort-print evidence; Lane 4 needs the event-study
harness first. Third, the barrier fits this desk exactly: per-name flush and LETF trades are
capacity-tiny, the tape reads in Korean, and the clock is KST — the three advantages the
[operating doctrine](../../synthesis/institution-grade-quant-system.md) says we actually have.
The honest statement of the prior: **this is the best payer-plus-barrier situation this desk can
currently reach with data it already owns.** That is what "found" means before a backtest.

## The design boss: Korea's sell-side tax wall

Every design choice below is downstream of one number, so it goes first. Korea charges a
**securities transaction tax on every sale** — ⚠️ from-training: ~0.15% (15 bp) for KOSPI names
as of 2025–26, after the step-down schedule 0.23% → 0.20% (2023) → 0.18% (2024) → 0.15% (2025);
the backtest must apply the year-correct rate, and the current rate must be re-verified at Tier-0
(NTS/KRX notice) before registration. Add commission (~1–3 bp per side at a domestic broker;
measure our own), half the bid–ask spread per side (KRX tick bands put liquid mid-priced names at
roughly 5–20 bp spreads ⚠️), and market impact ≈ 0 at our size. A completed round trip therefore
costs **≈ 25–30 bp**, dominated by the tax.

Walk through what that does to turnover. A signal refreshed weekly that replaces the whole
portfolio each week completes ~50 round trips a year on every won of book: 50 × 27 bp ≈ **13% a
year in friction** — several times the entire expected gross edge. Hold the same signal for three
weeks on average and turn over only what the no-trade band forces (~17 book-turns a year), and
friction drops to ≈ 4–5%. Push holding toward a month with bands and it's ~3%. The conclusion is
structural, not tunable: **in Korea, a daily-rebalanced cross-sectional book is dead on arrival
at retail cost; the only viable forms are (a) slow signals held for weeks behind no-trade bands
and (b) episodic conditional trades whose per-event edge is a multiple of 27 bp.** The sleeve has
exactly those two forms and nothing else. (General framework:
[cost-aware trading](../../synthesis/cost-aware-trading.md); the long-only handicap TC ≈ 0.3–0.6:
[alpha model book](../models/alpha-model-book.md).)

## Component F — foreign-flow persistence (the core)

**Mechanism and payer.** A foreign institution rebuilding a Korea allocation must trade for days
or weeks — the √-impact schedule-slicing arithmetic in the
[model book](../models/production-model-book.md) — and KRX publishes each name's foreign net
purchase value **daily**. Day one of a large program is visible by day two; the signal front-runs
*the remainder of the buyer's own schedule*. Payer: **Constraint** — the institution pays impact
to demand liquidity on a deadline; we are on the supplying side of its remaining days. ⚠️
From-training evidence, all pointing the same way at this horizon: Froot–O'Connell–Seasholes
(2001, JFE) — cross-border institutional flows are strongly persistent (autocorrelation
half-lives measured in weeks) and *forecast* emerging-market equity returns at daily-to-weekly
horizons; Richards (2005, JFQA) — in six Asian markets including Korea, foreign flows are
positively autocorrelated and returns follow them; Choe–Kho–Stulz (1999 JFE; 2005 RFS) — Korean
data specifically: foreigners positive-feedback trade and, critically for the mechanism, **pay
worse execution prices when trading aggressively** — i.e., they demonstrably demand liquidity and
pay impact. The continuation channel is what we harvest; the long-run "who wins" debate in that
literature is irrelevant to a 2–4 week holding.

**Signal, exactly.** For name *i* on day *t*, on the S3 feed:

- Intensity: `f(i,t) = foreign_net_value(i,t) / ADV20_value(i,t)`, winsorized at ±3σ — net buying
  scaled by what the name normally trades, so ₩10B into a sleepy name outranks ₩10B into Samsung.
- Smoothed intensity: `F(i,t) = decay_linear(f(i,·), 10)` — a 10-day linearly-decaying weighted
  sum (today weighs most, ten days ago least; the
  [operator toolbox](../models/production-model-book-plain.md) explains why this is the standard
  turnover-controlling smoother).
- Streak: `s(i,t)` = consecutive sessions with foreign net value > 0 (strict, no gap allowance
  in v1).
- **Entry set:** rank names by `F`; a name qualifies when `s ≥ 3` **and** `F` is in the top
  quintile of the universe **and** `f`-intensity that day ≥ its own 60th percentile (one strong
  day plus persistence, not three trivially-positive days).
- **Exit:** foreign net value < 0 for 2 consecutive sessions (the schedule looks finished), or
  20 sessions elapsed, whichever first. **No-trade band:** once held, keep while the name stays
  in the top 40% by `F` — the band is the turnover governor that the tax wall demands.

**The falsification that matters most.** Foreign flows chase price momentum (Richards ⚠️), so a
naive backtest of F will partly rediscover momentum wearing a costume — the
[orthogonality doctrine](../models/production-model-book-plain.md) case in point. The registered
test is therefore *incremental*: residualize the F-rank against {12-1 momentum rank, 1-month
reversal rank, size, turnover} cross-sectionally, and demand the **residual** IC be positive with
t ≥ 2. ⚠️ Honest prior from the literature: something like half the raw continuation is price
momentum; the flow-specific residual is the part worth having. If the residual IC is zero, Lane
1's flagship sub-signal is a story, and the page says so in the verdict note.

## Component R — the retail-extreme exclusion (a filter, not a fade)

The naive version — "retail buys, so short it" — is **wrong at short horizons**, and the design
must encode why. ⚠️ From-training: Kaniel–Saar–Titman (2008, JF) show individual net buying
*positively* predicts weekly returns (individuals passively provide liquidity — they buy dips
that bounce); meanwhile Barber–Odean attention studies, Hvidkjaer (2008, RFS), and
Barber–Lee–Liu–Odean (2009, RFS — Taiwan's complete tape: individual investors lose ~2% of GDP a
year, transferred to institutions) show retail buying predicts *negative* returns at
weeks-to-months horizons **when it is attention-driven** — chasing after price has already run.
Same cohort, two opposite flows. The separator is the price path the buying arrives on:

- **Attention flow (fade-worthy):** retail net-buy z ≥ +2 (vs the name's own 1-year history)
  **and** trailing 20d return ≥ +15% **and** turnover z ≥ +1. Buying *into strength* after the
  move — the lottery/theme-stock (테마주) pattern.
- **Provision flow (leave it alone):** the same z ≥ +2 arriving on a −10% five-day flush. That's
  the Kaniel–Saar–Titman channel — and it points the same direction as component M below, so
  fading it would fight our own trade.

Since retail shorting is not honestly available to this desk, R's live role is an **exclusion
and underweight rule on the long book**: a name in the attention-flow state cannot be entered or
held, whatever F says. (In the IC harness R is still tested two-sided on paper, to know its
standalone strength; single-stock futures on the top names are the only realistic short channel
if it ever earns one ⚠️ — see the hedging note.)

**The cohort rule that applies to everything on this page:** never use the aggregate 기관
(institutional) row. It nets together the pension fund (연기금 — a *mechanical contrarian*: NPS
band rebalancing buys dips by mandate, the alpha map's Lane 2), discretionary asset managers
(투신/사모), and proprietary desks (금융투자) — cohorts that trade *against each other*. S3's
detailed split exists per name (⚠️ confirm 연기금 granularity per-name at build; the
market-level split is certain). Every signal here specifies its exact cohort; any variant built
on the aggregate row is unregistered by definition.

## Component M — the margin-flush conditional buy (episodic)

The [session-clocks page](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md)
documents the machine: margin loans (신용융자) against a name build up in a rally; a hard down
day triggers next-morning **broker forced liquidation that is price-insensitive and
front-loaded** — reverse-margin-call supply hits the open and exhausts by roughly 10:00 KST.
Payer: **Constraint** (the borrower must sell; the broker's algo doesn't negotiate). The engine
already runs the *market-level* version as H6's belt-load/armed-morning state (live since S10
landed). The alpha version is per-name:

- **Arm** name *i* into tomorrow when: credit balance ratio high vs its own history (per-name
  신용잔고 z ≥ +1.5 — needs the S12 feed, below) **and** today closed ≤ −5% **and** H6's
  market-level belt is loaded (aggregate credit z from S10 ≥ +1).
- **Trigger:** tomorrow, buy in the 09:50–10:10 KST window *only if* the tape shows the
  exhaustion signature (price above the 09:30 low; the flush is drying, per the
  [V-day checklist](../checklists/catching-the-v-day-checklist.md) trigger logic — this is the
  same trade, mechanized).
- **Exit:** T+3 close at the latest; earlier on +4% gain or −3% stop. Per-event edge must be a
  multiple of the 27 bp friction, and at these constants it is or the trade doesn't exist.
- **The information-tail guard:** if the down day came with a *named fundamental* (guidance cut,
  regulatory action — not "the market fell"), stand down; forced supply is only mispriced when
  the seller's reason isn't information. This is the breadth test from the alpha map, made a
  hard rule.

**Missing feed, named honestly:** per-name 신용잔고 is published daily (KOFIA/KRX, short lag ⚠️
endpoint and lag to confirm) but not yet ingested — call it **S12, a half-day build**. Until S12
lands, M runs market-level only inside H6 (already live) and the per-name rule stays paper.
Expected frequency: a handful of qualifying name-events per quarter; this is a rifle, not a
conveyor.

## Component L — the leveraged-ETF close-pressure fade (episodic, deterministic)

Korea's single-stock 2× ETFs (the Samsung/SKH complex is ~14% of those names' turnover, per the
[LETF-decay page](../../shared/concepts/leveraged-etf-decay.md)) must rebalance **daily, in the
direction of the day's move, at or near the close** — a fund holding 2× exposure needs its hedge
adjusted by `(L² − L) × AUM × r_day = 2 × AUM × r_day` for L = 2 (⚠️ Cheng–Madhavan 2009
mechanics; Ben-David–Franzoni–Moussawi 2018 on the volatility imprint). With S5's AUM archive
live, tomorrow's forced close flow is **computable at 15:00 KST today**:

- `N(i,t) = Σ_funds 2 × AUM(fund,t−1) × r(i,t)` — predicted rebalance notional for name *i*.
- **Event:** `|N(i,t)| / ADV(i,t) ≥ 3%` (threshold to be set from the S5 archive's actual
  distribution before registration — marked TBD, the one constant this page can't pre-set).
- **Trade:** the close auction overshoots in the rebalance direction; fade it — enter at next
  morning's open against yesterday's close-push direction, exit by 10:30 KST or flat by the
  close. Payer: **Constraint** (the fund rebalances regardless of price).
- **Gate before any trade rule:** an event study on the S5 archive must first show the
  close→open reversion is real and larger than 27 bp on qualifying events. If it isn't, L stays
  what it already is — an H6 execution-timing overlay (don't *place our own* MOC orders into an
  amplified close) — which is worth keeping and costs nothing.

## Universe, portfolio, and the hedging honesty

**Universe (survivorship-clean by construction):** top 150 names by trailing 60-day median traded
value, recomputed monthly, *as of each historical date* from the full-market S1/S3 panel — no
index-membership history needed, so the known KOSPI200-membership-history gap never touches the
backtest. Liquidity floor: ADV ≥ ₩5B. Foreigners concentrate in exactly this set, which is also
where our fills are frictionless.

**Book:** long-only, 10–20 names, equal-weight with a 10% single-name cap, F picks the names, R
excludes, M and L trade as bracketed conditional orders beside the core book. Weekly refresh
respecting the no-trade bands; expected average holding 2–4 weeks. The whole sleeve sits behind
the H1 regime gate (gate off ⇒ sleeve flat; the gate is
[not alpha, it's survivability](../../synthesis/alpha-map.md)) and inherits the
[risk constitution](../checklists/trading-risk-constitution.md) limits unchanged.

**Hedging, honestly:** beta-neutralizing this sleeve needs KOSPI200 futures; even the mini
contract (⚠️ ₩50,000/point vs the standard ₩250,000/point) is roughly a ₩50M notional unit —
hedge granularity binds until the sleeve is several times that. Single-stock futures exist and
are liquid in the top names (⚠️ 10-share multiplier) and are the only realistic short channel,
but derivatives access has retail prerequisites (education/deposit tiers — an ops item to check
at a Korean retail broker, not a design item). **v1 therefore runs long-only + regime-gated**, and the IC tests
are run in residual space anyway, so the *verdict* about the signals doesn't wait for the hedge.

## Validation protocol and pre-registered kills

The machinery is the [solution sheet](../../synthesis/institution-grade-solution-sheet.md)'s,
unchanged: daily rank-IC against 5d and 10d forward **residual** returns (WLS shrunk-beta
residualization), Newey–West errors, IC-decay curves 1–20d, purged walk-forward with a 20-session
embargo, costs at the year-correct tax schedule and again at **2×** as the stress hurdle, DSR ≥
0.95 with the trial registry counting **all four components and every variant** (the registry
remembers; this page registers F, R, M, L and the F-residualization as trials 1–5). Backfill: S3
history to the feed's honest depth (⚠️ expect ≥5–8 years; confirm at build), which at 150 names
is a few-hundred-thousand-row panel — trivial compute on the existing harness.

The kills, written before the first run:

1. **F dies** if the momentum-residualized IC is ≤ 0 or t < 2 over the panel, or if it fails the
   2× cost stress at band-governed turnover. (Raw-IC success with residual failure = momentum in
   a costume = dead.)
2. **R dies** as a signal if the attention-flow state shows no negative forward residual return
   monotone in z; it can survive as a cheap exclusion even at weak significance, but then it is
   labeled hygiene, not alpha.
3. **M's per-name form doesn't exist** until S12 lands; it dies if, on the backfillable events,
   the 09:50–10:10 entry doesn't clear 2× friction net, or if the information-tail guard can't
   be encoded (i.e., we can't distinguish flushes from news mechanically).
4. **L dies as a trade** if the event study shows reversion ≤ 27 bp on qualifying events; it
   then remains an execution overlay only.
5. **The lane dies** per the alpha map's standing test: each surviving signal must show IC > 0
   **out-of-registration within 2 quarters of forward data** or it retires. No signal, no sleeve
   — the book stays paper and the page gets a dated verdict note either way.

## What to honestly expect (pre-registered expectations)

Run the chain: per-signal IC in the 0.02–0.05 class (the alpha map's own stated band); one
country and one factor family cut effective breadth to the low hundreds of quasi-independent bets
a year; the long-only transfer-coefficient handicap ≈ 0.3–0.6
([model book](../models/alpha-model-book.md)); friction ≈ 3–5%/yr at band-governed turnover.
Net expectation for the F+R core: **roughly +2–4%/yr over the gated benchmark on sleeve capital**
— which independently reproduces the
six-layers note's public-data ceiling (~+2–3.5%/yr),
a consistency check that the arithmetic isn't being romanced. M and L add lumpy, episodic
per-event chunks (their per-trade edge is larger precisely because they fire rarely). Standalone
sleeve Sharpe in the 0.3–0.6 class; its job in the
[stack](../../synthesis/alpha-map.md) is to be one of the 2–3 modestly-correlated small edges
that together run 0.7–1.2.

**What this strategy is not:** it cannot produce the
campaign's 2:1 asymmetric chunks — that remains Lane
5's job, firewalled, gated, and graded separately. And at the current denominator the sleeve's
annual dollar output at small scale is secondary. Its primary product is **a
validated, registered, forward-tracked systematic alpha** — a verdict machine and a portable
research artifact (signal family + write-up), whose economic value scales with capital later.
Verdict → record → capital, in that order.

## The build-and-falsify plan (compressed; slots into the engine research block)

Five working blocks, no new infrastructure, no displacement of the sprint/campaign/W1 items:

- **Block 1 — panel.** Backfill S3 per-name investor values to full depth; build the
  trailing-ADV as-of universe constructor. (The fetcher exists; this is a loop and a table.)
- **Block 2 — F and R through the harness.** Signal library (`f`, `F`, streak, R-state), rank-IC
  + decay + residualized-IC runs, cost grid at scheduled tax rates. **This block alone settles
  Lane 1's flagship question.**
- **Block 3 — L event study** on the S5 archive (distribution of `|N|/ADV`, threshold choice,
  close→open reversion measurement). **S12 feed built** (half-day) and M's historical events
  assembled to whatever depth per-name credit history allows.
- **Block 4 — walk-forward + DSR + orthogonality vs H1/H3**, the 2× stress, and the verdict
  note appended to this page (survivors registered with final constants; corpses recorded with
  their trial counts).
- **Block 5 — paper.** Survivors wire into engine-v3 as registered signals (the
  [execution layer](../../synthesis/engine-v3/execution-layer.md)'s shadow state), forward IC
  clock starts for the 2-quarter out-of-registration test.

Live reps already on this week's calendar double as evidence: **Jul-9 (만기 + BOK)** — watch the
연기금 and program prints do or not do what Lane 2 predicts (the cohort-print kill test is
*observable that day*); **Jul-10 (SKH ADR debut)** — the ADR-parity monitor the
[model book §7](../models/production-model-book.md) specced starts collecting Lane-4 data. Both
feed this page's neighbors without costing the sleeve any build time.

## Relationships

- Parent ranking + kill doctrine: [The Alpha Map](../../synthesis/alpha-map.md) (this page = Lane 1 registered; Lane-2 evidence shared)
- The mathematics library behind the signals: [Alpha Model Book](../models/alpha-model-book.md) · [Production Model Book](../models/production-model-book.md) (+ [plain-language version](../models/production-model-book-plain.md))
- Machinery this page mechanizes: [KRX session clocks & forced liquidation](../../shared/concepts/krx-session-clocks-and-forced-liquidation.md) · [KRX program trading](../../shared/concepts/krx-program-trading.md) · [Leveraged-ETF decay](../../shared/concepts/leveraged-etf-decay.md) · [V-day checklist](../checklists/catching-the-v-day-checklist.md)
- Harness + process: [Institution-Grade Solution Sheet](../../synthesis/institution-grade-solution-sheet.md) · [Institution-Grade Quant System](../../synthesis/institution-grade-quant-system.md) · [Execution Layer](../../synthesis/engine-v3/execution-layer.md) · [H6 crowding module](../../synthesis/engine-v3/h6-crowding-defector-module.md)
- Cost doctrine: [Cost-Aware Trading](../../synthesis/cost-aware-trading.md) · [Transaction Costs](../../shared/concepts/transaction-costs.md)
- What it must not touch: firewalled discretionary campaign capital (separate risk book) · [Risk Constitution](../checklists/trading-risk-constitution.md)
- Payer taxonomy: [Who Pays You](../../shared/concepts/who-pays-you.md)

## Open questions

- ⚠️ Verify at build: current STT rate at Tier-0; pykrx per-name *detailed* cohort granularity
  (연기금 per name); S3 backfill depth; per-name 신용잔고 endpoint + publication lag (S12); SSF
  access prerequisites at a Korean retail broker.
- Does the F signal's residual IC concentrate in mid-liquidity names (where foreign schedules
  run longest) — i.e., should the universe tilt below the mega-caps?
- Is the L threshold better set on close-auction volume share than day-ADV share?
  (F is the natural candidate — pure expression-language material)?
