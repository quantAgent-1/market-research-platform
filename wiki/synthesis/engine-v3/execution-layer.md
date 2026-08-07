---
type: design
title: Engine v3 — Execution Layer (OMS) — from Signals + Manual Tickets to Automated Fills
description: The design that closes enginev2's named gap — an order-management/execution layer that turns v3's nightly target portfolio into broker fills with zero human latency, bounded worst-case damage, and full auditability. Alpaca adapter, diff engine, 8-check pre-trade risk gate, order state machine with idempotent IDs, reconciliation, kill switch, the KST session daemon, and a pre-registered shadow → paper → live-small → full promotion ladder. Amends (does not delete) the v2/v3 "tickets-only" guardrail: code may route orders only downstream of gates.
tags: [systematic-trading, engineering, process, small-account]
timestamp: 2026-07-07T00:00:00Z
status: active
build: planned
sources: []
---

# Engine v3 — Execution Layer (OMS)

> **The amendment, stated up front.** v2 and the v3 design brief carried a hard guardrail: *signal
> only, no order routing by code, human executes tickets.* That guardrail existed for three
> reasons — unvalidated signals, an unmeasured operator, and safety. It was right. This design
> does not delete it; it **re-scopes it as a state machine of trust**: code may route orders only
> after pre-registered promotion gates pass, and the guardrail remains binding at every rung
> below. The change is registered here rather than silently overwritten (the brief's exclusion
> list should point to this page).
>
> Why the layer is worth building at all: enginev2's production gap was exactly this — full
> research infrastructure, signals, and then a human at 22:30 KST clicking. The one measured live
> leak was the human (−$39.76 of −$44 from un-signaled trades). Automation is how **adherence
> becomes structural instead of aspirational**, and it is the only way a 20–40-name nightly book
> is tradeable at all from KST. What automation does *not* do is create edge: it is a faithful
> amplifier — a positive-expectancy book realizes its expectancy; a zero-expectancy book realizes
> zero minus costs, faster. The signal layer's verdicts still gate everything.

## 1. Mission

Convert the nightly target portfolio (produced by the already-specced DAG at 07:30 KST) into
fills at the next US open (22:30 KST) with: **zero human latency** (runs while the operator
sleeps), **bounded worst-case damage** (pre-trade gate + kill switch + caps), and **full
auditability** (every order transition timestamped; every fill lands in the TCA ledger).

Three measurable profit contributions, none of them "alpha": (1) the operator leak goes to zero
by construction — adherence-% is replaced by uptime-%; (2) **breadth unlocks** — Grinold's lever,
impossible manually at this clock; (3) intended prices get captured and measured (TCA), so the
live-vs-paper gap becomes diagnosable.

## 2. Architecture (modules under `src/enginev3/exec/`)

| module | responsibility |
|---|---|
| `broker.py` | Alpaca adapter: REST for orders/positions/account, websocket `trade_updates` for fills; **paper and live are the same code path** — different base URL + keys. All calls timeout-wrapped, retries with backoff on idempotent reads only. |
| `diff.py` | target weights × NAV → integer share targets → deltas vs **broker** positions (broker is truth, not the local book) → order list. No-trade band \|Δw\| < 0.5% [inherited]; min order notional $50 [default]. |
| `risk_gate.py` | the 8 pre-trade checks (§4). Pure function: (order list, account state, config) → (approved, rejected+reasons). Any rejection is logged with its named check. |
| `oms.py` | order state machine (§3); idempotent `client_order_id = v3-{date}-{symbol}-{side}-{hash(qty,px)}` so a crashed-and-restarted session can never double-submit; ambiguous states resolved by status query, never by blind resubmit. |
| `daemon.py` | the session runner (§5): wake → reconcile → gate → submit window → monitor → book → report → sleep. |
| `reconcile.py` | broker-truth reconciliation at session start and end: positions, open orders, cash vs local expectations. Any mismatch → **halt new submissions + alert**; trading resumes only after a written explanation. |
| `kill.py` | kill switch: a `KILL` flag file checked before every submission batch + a cancel-all-open-orders command + a flatten-all script (**drilled in paper before Gate B** — an untested kill switch is decoration). |

**Broker decision [default]:** Alpaca — the account exists from v2, the API is production-grade,
paper/live parity is built in, US equities commission-free, MOO/MOC/limit/stop supported,
fractional shares available. The **a Korean retail broker book stays manual and discretionary** — no fragile
scraping automation against a retail HTS; the automated sleeve and the discretionary sprint book
stay firewalled (separate accounts, separate KPIs). Single-broker dependency is an accepted risk
at daily horizon: an API outage means orders go next session (see §6).

## 3. Order lifecycle

```
PENDING_NEW → SUBMITTED → {PARTIALLY_FILLED → FILLED} | REJECTED | CANCELED | EXPIRED
```

- **Order type policy [default]:** MOO (market-on-open) — the opening auction is the deepest
  print and *is* the simulator's fill-next-open convention, so sim and prod share a fill model.
  Post-open remainder (partial/rejected): one marketable-limit retry capped at quote + 10 bps,
  window T+5 → T+30 min; after T+30, unfilled remainder is **booked as opportunity cost in the
  TCA ledger — never chased**.
- Submission retries: ≤ 3 with exponential backoff, and only after a status query proves the
  prior attempt is not live (the idempotent ID makes this safe).
- Every transition appends to `exec/orders.parquet` (order_id, client_order_id, ts, state, px,
  qty, reason) — the audit trail that makes the monthly governance review possible.

## 4. The pre-trade risk gate (8 checks, all must pass per order)

| # | check | constant [default] | scope |
|---|---|---|---|
| 1 | kill switch clear | `KILL` file absent | session |
| 2 | market session valid | full trading day (holidays/half-days from the exchange calendar) | session |
| 3 | price collar | reference px within ±5% of prior close | order |
| 4 | per-order notional | ≤ 20% NAV | order |
| 5 | planned total notional | ≤ 0.95 × buying power (T+1 settlement aware) | session |
| 6 | post-trade position caps | name ≤ 5%, sector ≤ 25% (recheck at current prices) | order |
| 7 | order count sanity | ≤ 2 × expected N (a runaway diff = a bug, not a signal) | session |
| 8 | symbol whitelist | in the current universe file | order |

One failed check rejects the order; **two failed checks or any reconcile mismatch halts the
session** (the pattern of failures is itself information — a bug, not bad luck). Session halts
page the operator via Telegram; there is no auto-resume.

## 5. The session daemon on the KST clock

- **07:30 KST** — nightly DAG (already specced) produces `targets_{date}.parquet`.
- **22:20 KST (09:20 ET)** — daemon wakes: reconcile → diff → risk gate → stage orders.
- **22:25–22:28 KST** — submit MOO batch (before the 09:28 ET MOO cutoff).
- **22:30–23:00 KST** — monitor fills via websocket (poll fallback every 60s); limit retries per
  §3; write fills → TCA ledger as they land.
- **23:00 KST** — session close: end reconcile, orders/fills digest + SLA line to Telegram, sleep.
- **07:30 KST next day** — DAG's book-pending-fills step cross-checks the ledger (double-entry:
  daemon wrote what the DAG expects).

**Where it runs [decision]:** a $5/mo VPS with a systemd timer is the production home — the
daemon is a *trading-window process* and GH-Actions cron (±15 min jitter, no persistent process,
inactivity pauses) is explicitly rejected for it (fine for the nightly batch, wrong for a 5-minute
submission window). Through Gate B, the home PC + Task Scheduler is acceptable; the VPS move is a
Gate-C precondition. DST note: the KST wake time shifts with US clock changes — the daemon keys
off the **exchange calendar in ET**, never a fixed KST time.

## 6. Failure modes → responses (pre-decided, in the runbook)

| failure | response |
|---|---|
| daemon crash mid-window | systemd restart → status-query every staged `client_order_id` → resume; idempotent IDs make double-submit impossible |
| websocket drop | poll fallback; no state lives only in the stream |
| broker API outage | session skipped, alert fired; targets stand; orders go next session (daily horizon absorbs a one-day miss — this is the accepted single-broker cost) |
| order rejected by broker | log named reason, skip, include in digest; ≥ 3 rejects → session halt |
| flash move at the open | the ±5% collar rejects the order — accepted cost, never widened mid-session |
| reconcile mismatch | halt + page; written explanation required before resume (no exceptions — this is the failure that precedes every horror story) |
| stale targets file (DAG failed) | daemon refuses to trade yesterday's targets twice (date-stamp check) → no-op session + alert |

## 7. The promotion ladder (pre-registered gates — the guardrail's new form)

| rung | what routes | entry gate (all must hold) |
|---|---|---|
| **Shadow** | nothing — daemon logs *intended* orders against live opens | build done + unit/integration tests green |
| **Paper-auto** | orders to Alpaca **paper** | ≥ 10 consecutive clean shadow sessions · median intended-vs-sim fill gap < 10 bps · 0 crashes |
| **Live-small** | real orders, **≤ 20% of NAV** deployed | ≥ 20 clean paper sessions · 0 unexplained reconcile breaks · kill-switch + flatten drill executed in paper · VPS or equivalent uptime story |
| **Full** | the whole automated sleeve | ≥ 60 live-small sessions · realized TCA ≤ 2× modeled cost · uptime ≥ 99% · **zero manual overrides** · live-vs-paper IC gap reviewed in governance |

**Demotion is automatic:** any unexplained reconcile break → down one rung pending post-mortem;
any kill-switch use → post-mortem gate before re-promotion. Signals and execution promote
independently — a new signal enters at paper regardless of the OMS rung.

## 8. Build plan (compressed, ~14h to Gate-A entry)

- **Day 1 (~4h):** `broker.py` + `diff.py` + `risk_gate.py` + shadow mode wired end-to-end on
  paper keys — **first shadow session tonight 22:20 KST** (the live rep; it costs nothing and
  starts the Gate-A counter).
- **Day 2–3 (~6h):** `oms.py` state machine + `reconcile.py` + `kill.py` + the paper kill drill;
  orders.parquet audit trail; Telegram digest.
- **Week 2 (~4h):** TCA-ledger integration (the schema already exists in the
  [solution sheet](../institution-grade-solution-sheet.md) §L4) + failure-mode tests (crash
  mid-window, stale targets) + VPS move prep.

## 9. Kill criteria (for this tool itself)

If after 30 shadow+paper sessions the layer does not beat the manual-ticket baseline on its own
KPIs — fill capture (median gap to the open print), session reliability, and total operator time —
or if maintenance exceeds ~2h/week, **freeze it and stay manual**: at 1–3 live names, manual
tickets are genuinely adequate, and the layer's real payoff only arrives with breadth. Building it
ahead of validated breadth is a deliberate infrastructure bet; the kill criterion keeps the bet
honest.

## 10. Honest limits

- **Automation is not edge.** This layer realizes whatever expectancy the signal layer proves —
  including zero. The profitability chain is unchanged: validated IC × breadth × costs ×
  denominator. Nothing here shortcuts the IC harness.
- **Single broker, single venue.** Alpaca outage = missed session; acceptable at daily horizon,
  documented as such. No smart order routing — MOO into the auction *is* the routing decision at
  this size.
- **Small-size privilege:** zero market impact assumed and true at this NAV; the design does not
  pretend to institutional execution (no slicing, no participation caps needed until size makes
  the TCA ledger say otherwise).
- **Security basics, not theater:** keys in env/secrets only, never in the repo; VPS = SSH keys +
  fail2ban + no inbound ports beyond SSH; the flatten script is the incident response.
- **KR compliance:** the automated sleeve trades the operator's own US cash account — no client
  money, no public signal-following; the education-not-advice footer question stays open on the
  public-repo side (tracked in the outline's open decisions).

## Relationships

- Amends the exclusions in the [design brief](design-brief.md); slots into the
  [project outline](project-outline.md)'s repo tree as `src/enginev3/exec/` + a `session` CLI verb.
- Fill model + cost measurement: [the solution sheet](../institution-grade-solution-sheet.md)
  (§L4 TCA ledger, §L5 rulebook constants it enforces).
- Why this layer exists: [Institution-Grade, Profitable](../institution-grade-quant-system.md)
  (failure modes #7/#8 — skipped incubation, operational fragility, the human).
- The leak it closes: the enginev2 diagnosis (Q5/Q8 — the −$39.76 operator post-mortem).
