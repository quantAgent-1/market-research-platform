---
type: design
build: planned
title: "Exit Sentry — Design Spec & Build Plan (the Tripwire Machine as One Pipeline)"
description: "Full design spec for the personal dashboard tool that runs the entire tripwire-exit pipeline: pull → evaluate → state machine → order tickets → brief/dashboard → calibration → replay, with the behavioral layer enforced in software (escalating confirms, config freeze during live signals, breach ledger, fail-closed staleness). Local-first Python, nightly KST run, Day-1-live build plan (~24h total) that replaces three overlapping present-state-stack builds."
tags: [systematic-trading, market-research, memory, tooling, engine, risk, exits]
timestamp: 2026-07-06T00:00:00Z
status: active
sources: [../systematic-trading/checklists/tripwire-exit-execution.md, ../synthesis/present-state-stack.md, ../synthesis/semiconductor-monitoring-system.md]
---

# Exit Sentry — Design Spec & Build Plan

**Mission.** One pipeline that runs the entire [Tripwire Exit Machine](../systematic-trading/checklists/tripwire-exit-execution.md)
end-to-end: *pull data → evaluate T1–T8 → run the state machine → emit order tickets and alerts →
render the dashboard + morning-brief section → log everything for calibration → replay-validate on
2018/2021.* The software's real job is not display — it is **enforcing the behavioral layer**: the
machine nags, escalates, freezes config mid-signal, and logs breaches, so the weakest component
(the operator at flip time) is never load-bearing.

**Doctrine compliance, up front.** Rule zero ([present-state stack](../synthesis/present-state-stack.md)): this
prints into the morning brief on **Day 1** — the pipeline goes live immediately with the operator
as every data-puller (manual CLI entry), and automation replaces pullers incrementally. It is
engine-v3-first: a self-contained module that rides the engine's nightly KST scheduling, with a
hard no-imports rule from H6 signal code. And it **replaces, not adds to,** three planned stack
builds (the expectations-tracker's revision half = T1; the calibration ledger's panel = Layer 6;
the flagged spot-vs-contract gap = T5), so it fits the July tool budget by consolidation.

---

## 1. Architecture

Local-first Python. No server, no database engine, no cloud. Files are the database (CSV/JSONL,
git-committed nightly = free audit trail + versioning); a static self-contained HTML file is the
dashboard (inline CSS/JS, opens from disk, zero ops); a markdown block is injected into the
morning brief. One scheduled process; everything else is a pure function of the files.

```
sentry/
├── run.py               # CLI: nightly | read | confirm | ticket | replay | review
├── config.yaml          # the constitution, encoded (thresholds, sizes, tickers, paths)
├── pullers/
│   ├── prices.py        #   daily bars: MU, SOXX, 005930.KS, 000660.KS, ^KS11 (yfinance)
│   ├── t1_revisions.py  #   FY26/FY27 consensus + eps_trend 30/60/90d-ago (yfinance)
│   ├── t5_spot.py       #   DRAM spot index scrape (requests+bs4), manual fallback
│   ├── t6_flush.py      #   flush/bounce episode detector (pure computation on bars)
│   └── t8_news.py       #   keyword news scan → candidate queue (never auto-flips)
├── model/
│   ├── tripwires.py     #   evaluators: raw values → {GREEN, SOFT, HARD, STALE} per tripwire
│   ├── machine.py       #   the state machine (pure, deterministic, replayable)
│   └── actions.py       #   ticket generator: state change → tranche schedule with deadlines
├── render/
│   ├── brief_md.py      #   morning-brief block (markdown)
│   └── dashboard_html.py#   single-file HTML dashboard (jinja2)
├── store/               # THE database (git-committed)
│   ├── tripwires.csv    #   every read: date,tripwire,value,state,source,method,note
│   ├── state_log.jsonl  #   every transition: ts,prior,new,trigger,inputs_hash,config_hash,ack
│   ├── episodes.csv     #   flush/bounce log: start,trough,retrace_pct,days,verdict
│   ├── tickets.jsonl    #   order tickets + fills + deadlines + breach flags
│   ├── breaches.jsonl   #   every rule violation, append-only
│   ├── queue.jsonl      #   pending human confirmations (escalating)
│   └── panels/*.json    #   drop-box: other stack tools publish panels here (see §5)
└── replay/
    ├── replay.py        #   runs machine.py over historical fixtures
    └── fixtures/        #   2018.csv, 2021.csv (hand-dated tripwire histories)
```

Stack: Python 3.11+, pandas, yfinance, requests+bs4, jinja2, PyYAML. Zero paid dependencies —
v1 needs no Alpaca (daily bars from yfinance suffice; the options/gamma panels come later from
their own stack tools via the panel contract).

## 2. The data plan, tripwire by tripwire (the crux)

Design rule: **quantitative tripwires are fully automated; anything news/judgment-shaped is
machine-nagged, human-confirmed.** A false hard flip fires a 50% de-gross, so hard flips from
scraped text are forbidden — but human confirmation is about *data validity only*, and an ignored
confirmation **escalates** (it cannot be waited out; see §3).

| TW | What | Method | Cadence | Automation | Failure mode → fallback |
|---|---|---|---|---|---|
| T1 | FY26/FY27 consensus EPS Δ4wk (MU; later SKH/Samsung) | `yfinance` `eps_trend` — Yahoo publishes current vs 7/30/60/90-days-ago consensus directly; snapshot weekly Friday | weekly, auto | **Full** | Yahoo schema drift → staleness flag + manual entry prompt |
| T2 | DRAM/NAND contract price m/m | TrendForce monthly press headlines; **manual entry via guided CLI** (`sentry read --monthly`), scraper-drafted in v2 | monthly | Nag + manual (2 min/month) | Operator skips → escalation ladder (§3) |
| T3 | Hyperscaler capex guides | Calendar-driven: tool schedules the 4 earnings dates, opens a Y/N/value prompt within 24h of each | quarterly ×4 | Nag + manual | Same ladder |
| T4 | Customer inventory (weeks) | Per MU/SKH/Samsung print, from call commentary; prompted like T3 | quarterly ×3 | Nag + manual | Same ladder |
| T5 | Spot vs contract spread | Scrape DRAMeXchange/TrendForce spot index page weekly; spread vs last contract print; 4-wk spot trend | weekly | **Semi** (scrape + manual fallback) | Scrape breaks → grey gauge + prompt |
| T6 | Bounce strength | Pure computation on daily bars: flush = basket peak-to-trough ≤ −7% within ≤3 sessions; measure % retraced by session 5; log episode | daily, auto | **Full** | None (data = prices) |
| T7 | Supplier capex (3 makers) | Prompted per maker guide event (calendar-driven) | quarterly ×3 | Nag + manual | Same ladder |
| T8 | HBM LTA/allocation break | `t8_news.py` scans feeds for {HBM, LTA, allocation, reprice, renegotiat*, walk*} → pushes **candidates** to queue with source link; human confirms validity | daily scan | Candidate-only | Missed story → also covered by T1/T2 within weeks (defense in depth; stated limit) |

Basket for T6 (config): MU 40%, SOXX 20%, 000660.KS 20%, 005930.KS 20%; KOSPI index logged as
context. Two runs per day cover both tapes: **06:30 KST** (after US close, before Seoul open —
the main run) and **15:40 KST** (after KRX close — T6 Korea episodes only).

## 3. The state machine and its enforcement (where the behavioral layer becomes code)

`machine.py` is a **pure function**: `(tripwire_states, prior_state, config) → (new_state,
required_actions)`. Deterministic, no clock reads, no network — which is exactly what makes the
2018/2021 replay (§8) run through the *identical* code path as live.

States and transitions implement the [checklist](../systematic-trading/checklists/tripwire-exit-execution.md)
verbatim: GREEN → YELLOW on 1 hard or ≥2 soft (action: 50%C ticket, 5-session deadline, place-GTC
reminder); → RED on 2 hard (action: ≤20%C ticket, 10-session deadline). Enforcement details that
make it denial-proof:

- **The escalation ladder (no signal can be waited out).** A candidate flip or an overdue manual
  read enters `queue.jsonl`. Day 0: dashboard banner turns amber + Telegram ping. Day 1–2: daily
  re-ping, brief header shows "PENDING CONFIRM: T2 (age 2d)". Day 3: auto-logged breach line
  ("pending flip, operator non-response") + the dashboard state renders as `GREEN*` (asterisked =
  contested) and **dip-buy permission revokes** (the flush protocol reads state `GREEN*` as
  not-green). You may confirm or refute-with-a-source; you may not ignore.
- **Fail-closed staleness.** Every tripwire has `max_age` (T1 10d · T2 40d · T5 12d · T6 2d ·
  T3/T4/T7 100d). A stale gauge is grey, not green, and a stale *master* (T1) or T2 degrades the
  banner to `GREEN (UNVERIFIED)` — which also revokes dip-buy permission. Staleness is operator
  failure, not market signal, so it never auto-escalates state; it removes privileges instead.
- **Config freeze during live signals.** Every `state_log.jsonl` entry records
  `config_hash`. While state ≠ GREEN, `run.py` **refuses to run with a changed config hash**
  (exits with the breach message and logs it) unless invoked with `--quarterly-review "rationale"`,
  which requires state == GREEN or a cooling-off elapsed. Mid-signal threshold edits — the classic
  denial move — are now a *mechanical impossibility*, not a resolution.
- **The ratchet in code.** De-escalation transitions exist only via `monthly_full_green_count >= 2`,
  a counter that increments only on monthly reads with zero flips and resets on any flip. Re-entry
  emits a *new-trade ticket* at the next monthly boundary; there is no "undo cut" transition in
  the graph at all.
- **One-way audit.** `state_log.jsonl` and `breaches.jsonl` are append-only; the nightly run
  re-verifies their hash chain (each line carries the previous line's hash) so retroactive edits
  are detectable. Git commit each run doubles the seal.

## 4. Tickets: the machine decides, the human executes — with a deadline

No auto-trading in v1 (deliberate: partly-Korean book, small US account, and a scraped-data hard
flip must never move money by itself). Instead `actions.py` renders an **order ticket** the moment
state changes:

```
TICKET #2026-07-31-A   (YELLOW: cut to 50%C)         deadline: 5 sessions (Aug 7)
  tranche 1/3: SELL 33% of excess — limit ≥ max(VWAP_today, prev_close) — place by Aug 1
  tranche 2/3: SELL 33% — same rule — by Aug 4
  tranche 3/3: SELL 34% — day-3-unfilled converts to MOC — by Aug 7
  also: place GTC stop-limit on remainder at [structural level from config] — confirm placement
  flush-mode override: if a ≥7% flush is in progress, switch to first-bounce limits (50% retrace), 5-session cap
```

Fills are confirmed manually (`sentry ticket fill A 1 --px 987.40`); an unfilled ticket past
deadline = automatic breach line + daily nag until resolved or explicitly marked
`--breach-accepted "reason"`. The pre-mortem memo (stored verbatim in config) renders at the top
of every YELLOW/RED brief and ticket — future-you cannot see the ticket without reading the memo.

## 5. The dashboard and the brief

**Morning-brief block (markdown, injected into the existing brief):** one banner line
(`STATE: GREEN · since 2026-05-02 · nearest flip: T2 needs m/m ≤ 0 · next read: Jul-31`), the
8-row tripwire table (value · threshold · distance-to-flip · age), open tickets/queue items, and
the phase-4 checklist score from the [regime read](../market-research/memory/regime-read-2026-07-06.md).

**Dashboard (single HTML file, regenerated nightly):**
- **State banner** with since-date, distance-to-nearest-flip, and — always visible — *what would
  change the state* (the two nearest flip conditions spelled out).
- **Tripwire board**: 8 gauges with 90-day sparklines, staleness greying, source links.
- **Clock panel**: quarters-since-increment-peak (1Q26), the 2018/2021 overlay (where each
  precedent topped relative to the clock), phase-4 score.
- **Episode log** (T6): every flush with retrace %, the bounce-strength trend line — the
  distribution detector made visible.
- **Actions panel**: open tickets, pending confirms with ages, breach ledger tail.
- **Calibration panel**: Brier curve from `calls.csv`, give-back-vs-budget tracker (peak-marking
  starts once YELLOW first arms), replay-validation status badge (§8).
- **Panel drop-box**: renders any `store/panels/*.json` matching a 20-line contract
  (`{title, asof, rows|series, footnote}`) — this is the integration socket by which the other
  [present-state-stack](../synthesis/present-state-stack.md) tools (gamma map, KRX flow engine, cascade
  sentinel) later appear on the same screen without touching sentry code. Sentry is the shell;
  the stack tools are plugins.

**Alerts:** Telegram bot (free, reaches the phone) — fired **only** on state change, new pending
confirm, deadline breach, or hash-chain failure. Never on price moves; the tool's silence is
itself the signal that nothing changed.

## 6. Config (the constitution, encoded) — sample

```yaml
core_size_C: {usd: <thesis_notional>, current_pct: 100}   # thesis-book definition, per risk constitution
thresholds:
  t1: {soft_flat_4wk: 0.005, hard_down_4wk: -0.01, consec_weeks: 2}
  t2: {hard_mm: 0.0, soft_decel_mm: 0.02}
  t4: {hard_weeks: 8}
  t5: {soft: {premium_lt: 0.0, spot_4wk_falling: true}}
  t6: {flush_pct: -0.07, flush_sessions: 3, bounce_sessions: 5, weak_retrace: 0.50, consec_weak: 2}
states:
  yellow: {cut_to_pct: 50, deadline_sessions: 5}
  red:    {cut_to_pct: 20, deadline_sessions: 10}
ratchet: {full_green_months_to_deescalate: 2}
tickers: {us: [MU, SOXX], kr: [000660.KS, 005930.KS], index: [^KS11]}
basket_weights: {MU: 0.4, SOXX: 0.2, "000660.KS": 0.2, "005930.KS": 0.2}
runs: {main_kst: "06:30", kr_close_kst: "15:40"}
memo: |
  On exit day the tape will show record earnings, sold-out headlines, a single-digit P/E,
  and a fresh target raise. I will want to wait one more print. After I sell, the stock may
  make a new high without me — Jan-2022 did, +40% above the exit — then it halved. I sell anyway.
```

Scheduling (Windows): `schtasks /create /tn sentry-nightly /tr "py -m sentry.run nightly" /sc daily /st 06:30`
(second task at 15:40). The nightly run ends with `git add store/ && git commit -m "sentry: <date> <state>"`.

## 7. Human workflows (all of them, timed)

- **Daily (0 min default):** read the brief block. Interact only if amber.
- **Weekly (2 min, Fri):** T1 auto-snapshots; glance the dashboard; T5 confirm if scrape flagged.
- **Monthly (15 min, first weekend after TrendForce):** `sentry read --monthly` — guided prompts
  for T2 (+T4/T7 if a print landed), shows last value beside each entry, validates ranges, appends,
  recomputes state, regenerates everything, prompts the Brier-scored 3-month regime call into `calls.csv`.
- **Event-driven (5 min within 24h):** T3/T4/T7 prompts on the four hyperscaler + three maker dates;
  T8 confirms as candidates arrive.
- **Quarterly (30 min):** `sentry review` — grades the machine (did softs lead hards? did T6 lead
  everything?), unlocks config with written rationale, re-runs replay against any threshold change.

## 8. The replay harness (validation gate, enforced)

`replay.py` feeds hand-dated fixture CSVs (weekly 2017–19 and 2020–22 tripwire values — building
these is the [checklist's](../systematic-trading/checklists/tripwire-exit-execution.md) open work
item, a [replay-gym](../synthesis/replay-gym.md) session) through the **same `machine.py`**, emitting: flip
dates, exit prices vs the eventual peak (the give-back), what holding cost instead, and the
Jan-2022 phantom-ATH sequence as a labeled artifact. Acceptance gate in software: the dashboard
shows **`UNVALIDATED (replay pending)`** on the state banner until both fixture runs exist and
are committed — the tool itself refuses to claim validation it doesn't have. Replay also answers
the standing question of whether T6 promotes to hard-flip status (if it led in both cycles).

## 9. Build plan (compressed, live-reps; ~24h total inside the July tool budget)

| Day | Hours | Ship | Live rep (rule zero) |
|---|---|---|---|
| **1** | 4 | Skeleton, config, `machine.py` + tests, manual `read` CLI for all 8, `tripwires.csv`, brief block | **Pipeline live in tomorrow's brief** — operator is every puller; first real state computed from real entries |
| **2–3** | 6 | T1 auto (yfinance eps_trend), prices+T6 detector, staleness/fail-closed, HTML dashboard v1 | First auto-detected T6 episode logged from the live tape |
| **4–5** | 6 | T5 scraper + fallback, T8 candidate queue, escalation ladder, ticket generator, Telegram | Fire a synthetic YELLOW in a sandbox store; execute the drill ticket end-to-end (place/fill/log) |
| **W2** | 8 | Replay harness + 2018/2021 fixtures (the data work is the bulk), calibration panel, config-freeze + hash chain | Replay artifacts committed → `UNVALIDATED` badge clears; give-back numbers firmed and written into the checklist page |

Kill criteria (per stack doctrine): if the brief block isn't being read daily by Day 7, or no
graded call references it by Day 14 → cut to the manual checklist and stop. Budget honesty: the
~24h **replaces** three planned builds (expectations-tracker revision half, calibration ledger,
spot-spread gap) rather than adding to the 70h.

## 10. Honest limits (v1)

No auto-trading (tickets + deadlines instead — deliberate). No Korean consensus automation (FnGuide
is manual paste; weekly). No intraday logic (two daily runs; the flush handler works on daily bars
+ the operator's [V-day checklist](../systematic-trading/checklists/catching-the-v-day-checklist.md)
for intraday execution). No options greeks (the gamma map is a separate stack tool that will plug
in via the panel contract). T8 news scan will miss stories — accepted because T1/T2 catch the same
break within weeks (defense in depth, stated). Single-operator, single-machine; the git remote is
the backup.

## Relationships

- Implements: [the Tripwire Exit Machine](../systematic-trading/checklists/tripwire-exit-execution.md)
  (every layer) · the H2-playbook's
  two-tripwire rule · [second-derivative clock](../shared/concepts/second-derivative-cycle-trading.md).
- Consolidates from the [present-state stack](../synthesis/present-state-stack.md): expectations-tracker (T1),
  calibration ledger (panel), the spot-spread gap (T5); provides the **panel contract** the other
  stack tools plug into.
- Regime context: [the regime read](../market-research/memory/regime-read-2026-07-06.md) ·
  [monitoring system](../synthesis/semiconductor-monitoring-system.md) (sentry is Layers 1–2 operationalized).
- Constitution: [trading risk constitution](../systematic-trading/checklists/trading-risk-constitution.md)
  (sizing inputs; breach culture) · [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md)
  (`calls.csv` integration).
- Build home: engine-v3 repo as an independent module (no H6 imports); see
  [engine-v3 docs](../synthesis/engine-v3/index.md).

## Open questions

- Fixture construction: best sources for weekly 2017–19 / 2020–22 consensus-revision histories
  (T1) — sell-side archives vs reconstructed from earnings-revision studies; affects replay fidelity.
- Telegram vs Windows-toast-only for the alert channel (Telegram chosen for phone reach; revisit
  if the bot token becomes a nuisance).
- When the Korean book grows: KRX single-stock options liquidity for the collar leg, and whether
  sentry should track a separate C for the KR thesis book.
