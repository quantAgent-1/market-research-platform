---
type: checklist
title: "The Tripwire Exit Machine — Executing 'Sell on Evidence While Price Looks Fine'"
description: "The full execution framework for the cyclical exit problem: computable tripwire specs (source, formula, threshold, cadence), a GREEN/YELLOW/RED state machine with pre-mapped exposures and a one-way ratchet, tranche execution mechanics (sell strength, never flush lows), pre-commitment devices (the pre-mortem memo, act-then-adjudicate, GTC stops / collars, automation), the honest give-back arithmetic (~20–35% below the eventual peak is the price of avoiding the −50–75% round trip), and the 2018/2021 replay validation protocol."
tags: [systematic-trading, market-research, memory, risk, exits, checklist, behavioral]
timestamp: 2026-07-06T00:00:00Z
status: active
sources: [../../market-research/memory/regime-read-2026-07-06.md, ../../shared/concepts/second-derivative-cycle-trading.md]
---

# The Tripwire Exit Machine

**The problem this solves.** The [regime read](../../market-research/memory/regime-read-2026-07-06.md)
ends with an instruction that is easy to state and historically almost impossible to obey: *sell when
the checklist flips, while price still looks strong, the headlines still sound great, and selling
feels stupid.* In 2018 and 2021 the holders who "knew the rule" still round-tripped −50–75%, because
at the moment of decision the rule had to fight the feeling — and the feeling had record earnings,
a cheap P/E, and a raised price target on its side. The design principle, then: **the framework must
not rely on future-you agreeing with it.** Every component below exists to remove a discretionary
decision from the hot moment and relocate it to the cold present. Willpower is not a component.

The architecture in one line: **computable signals → a state machine with pre-mapped exposures → 
tranche execution with structural (not price) stops → pre-commitment devices that execute even if
you flinch → a monthly cadence with graded calibration → validated on the 2018/2021 replays before
being trusted live.** This page governs the **thesis book** (the memory-complex core); it is the
sell-side companion to the [trading risk constitution](trading-risk-constitution.md), which governs
overall risk, and it operationalizes the playbook's
two-tripwire rule and the [second-derivative clock](../../shared/concepts/second-derivative-cycle-trading.md).

---

## Layer 0 — the principle: signal, action, and feeling are separated

Three streams, never allowed to touch at execution time. **Signal** = states computed from logged
data by fixed formulas. **Action** = a lookup in a pre-written state→exposure table. **Feeling** =
journaled and graded (it gets its vote *now*, in the design, and again in the quarterly review —
never at a flip). The moment a feeling is allowed to modify a threshold mid-signal, the machine is
dead; that act is itself defined below as a breach.

## Layer 1 — the tripwires, made computable

A tripwire that is not reducible to *source + formula + threshold + cadence + logged history* is a
vibe, and vibes lose to headlines. The specs (thresholds inherit the
playbook and
[regime-read](../../market-research/memory/regime-read-2026-07-06.md) values; tune only at
quarterly reviews):

| # | Tripwire | Source / cadence | Formula | Flip rule |
|---|---|---|---|---|
| T1 | **Forward EPS revisions** *(master)* | FY27 (+FY26) consensus, Koyfin/Yahoo; **weekly Friday snapshot → CSV** | Δ4wk = E_now/E_−4wk − 1 | FLAT (soft): Δ4wk < +0.5% two consecutive weeks · DOWN (**hard**): Δ4wk < −1% |
| T2 | **Contract price m/m** | TrendForce monthly headlines | sign of blended DRAM contract m/m; NAND separately | first m/m ≤ 0 = **hard** · decel to < +2% m/m = soft |
| T3 | **Hyperscaler capex guide** | MSFT/META/GOOGL/AMZN calls (late Jul, late Oct) | any one guides FY capex below prior guide | one guide-down = **hard** |
| T4 | **Customer inventory** | quarterly commentary / sell-side | weeks of inventory | > 8 weeks = **hard** |
| T5 | **Spot leads contract** *(early warning; the flagged dashboard gap)* | DRAMeXchange/TrendForce spot indices, weekly | spot premium vs contract + spot 4-wk trend | premium < 0 **and** spot falling 4wk = soft (arms the system) |
| T6 | **Bounce strength** *(structure; from the regime read)* | own episode log | % of each ≥7% flush retraced within 5 sessions | two successive bounces < 50% retrace = soft |
| T7 | **Supplier capex discipline** | the 3 makers' guides | all three raise within ~2 quarters | soft (classic cycle-killer arming) |
| T8 | **HBM contract-side break** *(this cycle's migrated signal)* | LTA/allocation news flow | any LTA repriced down / allocation walked / prepayment renegotiated | **hard** (counts as a T2-equivalent — the [rule page's](../../shared/concepts/second-derivative-cycle-trading.md) signal migration) |

Logging is not optional: each read appends a row (date, value, state) to a `tripwires.csv`. The
state must be **auditable** — at a flip you will be strongly motivated to re-litigate history, and
the log is what makes that impossible.

## Layer 2 — the state machine

| State | Definition | Pre-mapped action (no discretion) |
|---|---|---|
| **GREEN** | 0 hard flips, ≤ 1 soft | Hold 100% of core size **C**. Flush protocol active (below). No adds above plan. |
| **YELLOW / ARMED** | 1 hard flip **or** ≥ 2 soft | Within **5 sessions**: cut to **50% C**, selling strength per Layer 3. Place the commitment structure (GTC stops / collar). No new adds; stop reinvesting. Write nothing new into the thesis — the next change is either re-green or RED. |

**The one-way ratchet (anti-denial):** states only escalate intra-quarter. De-escalation requires
**two consecutive monthly full-GREEN reads**, and re-entry is a *new trade decision* at the next
monthly boundary — never a same-week reversal of a cut. Exception: the mirror-image *bottom*
framework (steepest-but-improving QoQ declines + the second capex cut — the
[rule page's](../../shared/concepts/second-derivative-cycle-trading.md) long side) may initiate the
*next* cycle's entry independently; that is a different trade, not an un-exit.

**The ambiguity handler (flush during a signal — the case that kills discretionary traders):**
a flows-flush while GREEN = the buyable-dislocation regime (deploy the pre-sized dip tranche if the
[exhaustion signature](../../synthesis/semiconductor-monitoring-system.md) confirms). A flush while
YELLOW/RED = treated as the break regardless of its mechanical appearance — but **never sell into
the flush low**: cascades overshoot ([taxonomy §7](../../synthesis/techniques-of-winning-trades.md) —
price stops are anti-edge in reversion conditions). The rule: sell the **first bounce**, limit
orders at ~50% retrace of the flush range, time-capped at 5 sessions (unfilled → MOC on day 5).

## Layer 3 — execution mechanics

- **Tranches:** each cut executes in **3 equal tranches over 3–7 sessions**, limit orders pegged
  near/above VWAP — you are selling *strength*, which exists precisely because the signal fires
  while price looks fine. Day-3 unfilled tranche converts to market-on-close. Never market orders
  at the open; never all-at-once except on discrete T8-type news.
- **The give-back budget (the honest number, pre-accepted):** replayed against history, this
  machine exits **~20–35% below the eventual peak**. 2018: T1 rolls Aug–Sep, T2 goes negative
  Oct–Nov → out around −25–30% from the May top, versus −50%+ by December for holders. 2021: out
  Oct–Nov ~−25–30% from the April peak — and then MU printed a **marginal new ATH in Jan-2022
  without you** (+~40% above the exit price) before halving. Write the number down: the product
  you are buying is *converting a −50–75% round trip into a −20–35% give-back*, and the price is
  never top-ticking plus occasionally watching a last spike from the sidelines.
- **Sizing (flush-survival, feeds the [constitution](trading-risk-constitution.md)):** choose core
  size C as the smaller of: (a) C × 20% (a routine reflexive flush) ≤ the weekly loss budget;
  (b) C × 35% (worst signal-to-flat path, 2021-style) ≤ the maximum cycle give-back you accept in
  NAV terms. In the current [regime](../../market-research/memory/regime-read-2026-07-06.md),
  (a) binds — size to the flush, not the average day.
- **Scale adaptation:** at small-account scale (sub-$10k; MU options are ~$100k notional per
  contract — unusable), the commitment structure is **GTC stop-limit orders placed at the
  structural level the moment YELLOW arms** (the *platform* holds the commitment, not you) plus
  the tranche schedule. At larger scale, YELLOW places a **zero-cost collar** (buy ~6-month
  ~10%-OTM put, finance with ~12–15%-OTM call): if future-you refuses to sell, the structure
  sells for you — a Ulysses contract with teeth.

## Layer 4 — behavioral hardening (what actually makes it fire)

1. **The pre-mortem memo, written now, in GREEN, signed.** Contents, verbatim-style: *"On exit day
   the tape will show record earnings, sold-out-through-202X headlines, a single-digit P/E, my P&L
   deeply green, and at least one fresh target raise. I will want to wait one more print. If I
   sell, the stock may make a new high without me — Jan-2022 did, +40% above the signal exit —
   and I will feel maximal regret; then it halved. I sell anyway because the alternative,
   replayed twice, is −50–75%."* Read it aloud at YELLOW. This memo is the single
   highest-leverage artifact on this page.
2. **Act-then-adjudicate.** At a flip, the cut executes first (inside its window); the debate
   about data quality happens *after, in writing*, and may only affect **re-entry** — it can never
   cancel an executed cut. The asymmetry is pre-decided: re-entry costs a spread; staying wrong
   costs the cycle.
3. **The denial tells, named in advance.** At flip time, catching yourself (a) shopping for a
   friendlier data source, (b) re-deriving the threshold, or (c) "waiting one more print to
   confirm" = the disposition effect arriving in uniform, on schedule
   ([taxonomy §6](../../synthesis/techniques-of-winning-trades.md)). The memo lists these so they
   are recognized as the enemy, not as your own reasoning. Any threshold edit while a signal is
   live = a constitution breach, logged as such.
4. **Automation removes the failure modes on both sides.** The nightly job (engine-v3 /
   [present-state stack](../../synthesis/present-state-stack.md) tools) snapshots the sources,
   computes T1–T8, prints a one-line state banner in the morning brief, and **alerts only on
   state change** — killing both "I didn't check" and "I checked hourly and re-litigated."
5. **Cadence.** The formal read is **monthly** (first weekend after the TrendForce print,
   30 minutes, log the row, one Brier-scored 3-month regime call into `calls.csv` per the
   [morning call sheet](morning-call-sheet.md)). Event overrides only for discrete T3/T8 news.
   Between reads, the file stays closed — checking daily invites the feeling to vote.
6. **Grade the machine, not just the market.** Quarterly review: did soft flips lead hard flips?
   Did T6 (bounce strength) lead everything? Threshold changes happen only here, with written
   rationale, never during a live signal.

## Layer 5 — replay validation (required before live trust)

Run 2016–18 and 2020–22 through the exact specs in the [replay gym](../../synthesis/replay-gym.md):
date each tripwire flip from historical data, compute exit prices, the realized give-back, and the
phantom-regret path (the Jan-2022 marginal ATH). This calibrates the thresholds, produces the two
numbers that make compliance psychologically possible (*expected give-back ~25–30%; expected
drawdown avoided ~30–50%*), and — most importantly — pre-loads the emotional sequence so that
living it feels like a rerun, not an ambush. An untrained exit rule is a rule that breaks on first
contact; the replay is the training.

## Relationships

- Governs the thesis book; companion to the [trading risk constitution](trading-risk-constitution.md)
  and the [morning call sheet](morning-call-sheet.md) (calibration vehicle).
- Executes: the H2-2026 playbook's
  two-tripwire rule · the [regime read's](../../market-research/memory/regime-read-2026-07-06.md)
  "exit on evidence while price looks strong" · the
  [second-derivative clock](../../shared/concepts/second-derivative-cycle-trading.md) (clock arms,
  tripwires fire).
- Mechanism grounding: [edge taxonomy](../../synthesis/techniques-of-winning-trades.md) §6
  (disposition effect — the counterparty this framework refuses to become) and §7
  (strategy-specific stops; sizing/survival).
- Tooling: T1/T5/T6 feeds belong in the [present-state stack](../../synthesis/present-state-stack.md)
  builds (expectations tracker, calibration ledger).

## Open questions

- Historical flip-dating for the 2018/2021 replays (exact weeks T1/T2 crossed their thresholds) —
  a replay-gym work item; needed to firm the give-back numbers beyond from-training estimates.
- Whether T6 (bounce strength) should be promoted to hard-flip status if the replays show it led
  the fundamental tripwires in both prior cycles.
- Korean-book adaptation: KRX instruments for the collar leg on Samsung/SKH (single-stock options
  liquidity; inverse-ETF sizing as the poor-man's put).
