---
type: overview
title: Engine v3 — H6-First Build Handoff (for the coding agent)
description: The self-contained instruction document for building the H6 crowding/defector module as the FIRST vertical slice of enginev3 — scope table, stack pins, repo tree, free-tier data endpoints with the bitemporal schema, milestones A–C with definitions of done, engineering non-negotiables, and out-of-scope guardrails.
resource: h6-crowding-defector-module.md
tags: [systematic-trading, engineering, positioning, crowding, handoff]
timestamp: 2026-07-03T00:00:00Z
status: active
sources: []
---

# Engine v3 — H6-First Build Handoff

**Audience: the coding agent** (Claude Opus / Claude Code session) that will write the software.
This document is the entry point and the contract. Read order: **this file → the
[H6 module spec](h6-crowding-defector-module.md) (what to compute, exactly) → the
[project outline](project-outline.md) (repo conventions, PROTOCOL v3.0) → the
[design brief](design-brief.md) (mission context, optional).** Where documents disagree, this
handoff wins (it is newest); flag the conflict rather than silently resolving it.

## 0. What you are building, in one paragraph

The first vertical slice of `enginev3`: a **nightly market-positioning dashboard** that ingests
free public data, computes fourteen crowding gauges (A1–A14), eight defector detectors (B1–B8),
**three overshoot gauges (O1–O3) and five exhaustion detectors (C1–C5)** for a configured stock
complex, runs them through a CROWD state machine, a family-vote DEFECT trigger, **and the
CASCADE/EXHAUST extension (spec §5b)**, and publishes an auto-generated report page plus alerts.
**It moves no money, computes no backtest, and trades nothing.** It is the H6 module's Phases 1–2
(dashboard-only) riding on a minimal engine spine. Decisions already locked: **H6-first** (module
before engine) and **free-data-first** (no paid feeds; two sources are self-collected forward
archives). *(Signal C added to scope 2026-07-03 — it is dashboard math on the same free sources,
not a scope expansion into money.)*

## 1. Scope table

| Build now | Deferred (do NOT build) |
|---|---|
| Repo scaffold: uv, ruff, mypy --strict, pytest+hypothesis, pre-commit, Dockerfile, GH-Actions CI | IC/quantile evaluation core (`evaluation/ic.py` etc.) |
| Parquet lake + quality gates + universe config | Signals H1–H5 |
| 10 free-tier ingestors + `positioning_registry.py` (bitemporal, watermarked, fail-soft) | Portfolio construction, paper trading, live sleeve, tickets |
| `features/crowding.py` (A1–A14) + `features/defectors.py` (B1–B8) + `features/overshoot.py` (O1–O3) + `features/exhaustion.py` (belt-load meter, C1–C5) | Episode library & conditional evaluation (next handoff — O3 prints anchor-only until then) |
| `signals/h6_fragility.py` (composite, state machine incl. CASCADE/EXHAUST, DEFECT + EXHAUST votes) | Paid data feeds (ORATS/FMP etc.) |
| Nightly DAG (cron 22:30 UTC) + report page (GitHub Pages) + webhook alerts | Any order routing, options trading, ML |
| `evaluation/ledger.py` + `research/experiments.jsonl` (governance spine only) | The 17:30-KST intraday mini-run (documented, deferred) |

## 2. Stack pins (from the outline — do not re-litigate)

Python **3.13+** · **uv** · **ruff** (lint+format) · **mypy strict on `src/`** · **pytest +
hypothesis** · **pre-commit** · **Docker** slim · **GitHub Actions** (CI + nightly cron 22:30 UTC
= 07:30 KST) · **GitHub Pages** for the report · **pandas + pyarrow parquet** lake (DuckDB
optional) · **MIT license** · repo is **public from day 1** with a public-engine/private-config
split: `config/settings.local.yml` is gitignored (API keys, webhook tokens); CI uses repo
secrets. Footer on every published page: *education, not investment advice.* No secrets, account
sizes, or live positions in git — ever.

## 3. Repo tree for this slice

```
enginev3/
├── pyproject.toml · uv.lock · .pre-commit-config.yaml · Dockerfile · LICENSE · README.md
├── PROTOCOL.md                    # v3.0 — port from outline §3; ASK the human for enginev2's
│                                  #   PROTOCOL.md to carry the verbatim base text
├── .github/workflows/{ci.yml, nightly.yml}
├── config/
│   ├── universe.yml               # v1 = the memory complex + references (see §4), NOT the 170-name set
│   ├── crowding.yml               # complexes, A/B params, thresholds, weights, hysteresis, k-of-n
│   ├── settings.yml               # public defaults
│   └── settings.local.yml         # GITIGNORED
├── src/enginev3/
│   ├── cli.py                     # click: ingest | quality | crowding | report | run-nightly | healthcheck
│   ├── data/
│   │   ├── ingest.py store.py quality.py universe.py          # S1 OHLCV spine
│   │   ├── ingest_options_free.py      # S2': yfinance/CBOE-delayed chains → IV30, 25Δ RR, P/C OI (forward archive)
│   │   ├── ingest_krx_flows.py         # S3: pykrx investor-type net flows + short-sale balance
│   │   ├── ingest_short_interest.py    # S4: FINRA/Nasdaq bi-monthly SI + DTC
│   │   ├── ingest_etf_flows.py         # S5: shares-outstanding/AUM deltas; leveraged-ETF registry
│   │   ├── ingest_cot.py               # S6: CFTC COT weekly (ES/NQ non-commercial net)
│   │   ├── ingest_estimates_free.py    # S7': yfinance analyst data + Finnhub free tier
│   │   ├── ingest_surveys.py           # S8: AAII, NAAIM weekly; S9 VIX/VIX3M lives in S1 ingest
│   │   ├── ingest_kofia_credit.py      # S10: KOFIA freesis 신용융자 daily balance (margin fuel)
│   │   ├── ingest_krx_events.py        # S11: sidecar/CB/VI event log from KRX notices
│   │   └── positioning_registry.py     # per-source contract: schema hash, SLA, forward_clean_from, fallback
│   ├── features/{core.py, market.py, crowding.py, defectors.py, overshoot.py, exhaustion.py}
│   ├── signals/{registry.py, h6_fragility.py}
│   ├── evaluation/ledger.py
│   ├── report/{build.py, templates/, publish.py}
│   └── ops/{runner.py, alerts.py, logging.py}
├── research/experiments.jsonl
├── tests/{unit, integration, protocol, fixtures}
└── docs/{DESIGN.md, H6-DESIGN.md, RUNBOOK.md, site/}   # copy outline → DESIGN, H6 spec → H6-DESIGN
```

## 4. Data: free tier, exact requirements

**The bitemporal rule (non-negotiable):** every row in every positioning table carries
`effective_date`, `observed_at`, `source`, `ingest_run_id`. All feature computation joins on
`observed_at ≤ decision time`. Sources whose history cannot be reconstructed point-in-time (S2′,
S5, S7′, S8) get `forward_clean_from: <go-live date>` in the registry — their archives begin at
go-live and only grow forward.

| Source | What to pull | Suggested access | Staleness SLA |
|---|---|---|---|
| S1 OHLCV + VIX/VIX3M | daily bars; ^VIX, ^VIX3M | yfinance, Stooq fallback | 1 session (fail-hard) |
| S2′ options (forward archive) | per-name: IV30, 25Δ RR skew, put/call OI & volume, 1m/3m term slope — computed in-house from chains | yfinance option chains / CBOE delayed | 2 sessions |
| S3 KRX cohort flows | foreign/institution/retail net ₩ per KR name; short-sale balance | pykrx | 2 sessions |
| S4 short interest | SI shares, % float, days-to-cover | FINRA/Nasdaq published files | 20 sessions (carry-forward) |
| S5 ETF flows/AUM | shares outstanding & AUM deltas for complex + leveraged ETFs | issuer pages / yfinance SO | 3 sessions |
| S6 COT | ES/NQ non-commercial net | CFTC weekly CSV (Fri, Tue data) | 10 sessions |
| S7′ estimates/ratings | consensus EPS + 30/90d revisions, ratings actions, targets, earnings surprises | yfinance + Finnhub free tier (key in settings.local) | 5 sessions |
| S8 surveys | AAII bull−bear, NAAIM exposure | published CSV/XLS | 10 sessions |
| S10 KOFIA margin credit | 신용융자 balance (total + by market), daily Δ | freesis.kofia.or.kr published series | 3 sessions |
| S11 KRX trading-curb events | sidecar (buy/sell) / CB / VI: timestamp + direction | KRX notice pages (scrape) | event-driven; stale after 1 missed check |

Universe v1 (`config/universe.yml`): **memory complex** — US: MU, WDC, SNDK; KR: 005930, 000660;
reference: NVDA; **xmarket_reference: 2330.TW, ^TWII (Signal C's cross-market confirm — pulled
through the ordinary S1 ingest)**; ETFs: SMH, SOXX; leveraged registry: SOXL + the KR 2×
single-stock ETFs; market overlay: SPY, QQQ. Keep every ingestor universe-generic — the later ~170-name expansion must be a
config change only.

**If an endpoint turns out dead/unscrapeable:** mark the component deferred in the registry and
report it — do **not** silently substitute a different source (ask-before-deviating, §7).

## 5. What to compute

Implement **exactly** the definitions in the [H6 spec](h6-crowding-defector-module.md) §4–§5b:
A1–A14 each emitting (rolling 3y percentile, 20d slope) → coverage-weighted vote composite
**CROWD 0–100** → NORMAL/ELEVATED/EXTREME with hysteresis and the 2-consecutive-session rule;
B1–B8 emitting dated events with evidence payloads → **DEFECT = ≥3 distinct families within 10
sessions while EXTREME** (≥4 if ELEVATED), cool-down + re-arm rules; **O1–O3 (revision-anchored
gap, de-rating z, retracement anchor — O3 anchor-only in this slice) + the belt-load meter +
C1–C5 → CASCADE (DEFECT active + drawdown ≥ 8%) → EXHAUST = ≥2 of C1–C5 from ≥2 families within
3 sessions, only while CASCADE with the O-gate open (O1 ≥ p80 + anchor-staleness veto); a new
complex ≤ −3% down-close resets the C-window.** The armed-morning alert (belt-load ≥ p90 at the
close) links the human's [V-day checklist](../../systematic-trading/checklists/catching-the-v-day-checklist.md)
— intraday execution is deliberately out of engine scope. Coverage < 8/14 →
`INSUFFICIENT_DATA` (publish, never trigger). Every threshold comes from `config/crowding.yml` —
no magic numbers in code. Where a spec parameter says "calibrate," ship the stated default and log
it as a registered default in the ledger; calibration is a later phase.

## 6. Milestones & definitions of done

**A — spine (target ~1.5 wks):** scaffold + CI green + Dockerfile; S1 lake + quality gates;
S3 + S9 ingestors with the bitemporal schema; `nightly.yml` running ingest+quality on schedule
with a webhook alert; freshness table in a stub report.
*DoD: 3 consecutive green scheduled runs; bitemporal columns on every table; the chaos test
(delete one source dir → degrade path + alert, run halts nothing) passes for S3.*

**B — gauges (target ~1.5 wks):** remaining ingestors (S2′, S4, S5, S6, S7′, S8, **S10, S11**);
A1–A14 **+ O1–O3 + the belt-load meter**; composite + state machine; hypothesis property tests
(score bounded; missing data can never *raise* the score; no state flapping on constant input;
**O1 = 0 when price and estimates move together; belt-load monotone in fuel percentile**).
*DoD: state vector computes over a ≥3y backfill of the clean-history sources; `INSUFFICIENT_DATA`
path demonstrated; unit fixtures with hand-computed percentiles pass (incl. an O1/O3 fixture with
a hand-built estimate path).*

**C — detectors + report (target ~1.5 wks):** B1–B8 + DEFECT family vote; **C1–C5 + the
CASCADE/EXHAUST extension + the armed-morning alert**; the full report panel (state gauge + score
history, 14-component table with percentile bars/slopes/staleness, B-event timeline with evidence,
**overshoot dial + belt-load gauge + C-event timeline**, freshness table) published to GitHub
Pages; alert rules (state transition, DEFECT, **CASCADE, armed-morning, EXHAUST**, SLA breach,
quarantine).
*DoD: 5 consecutive green nightly runs publishing the panel; the scripted synthetic
rise→crowd→defect→crash episode runs end-to-end in the integration test and fires the alert —
**extended with an exhaustion tail (crash → belt-load spike → up-close + institutional turn →
EXHAUST fires; plus a counterexample leg where a new down-close correctly blocks it)**; the
June-2026 memory replay shows EXTREME by mid-June and a DEFECT vote by Jun-25/26, **and the
Jul-1→3-2026 replay shows CASCADE by the Jul-2 close, the armed-morning alert that evening, and
EXHAUST on the Jul-3 close** — as demos (both episodes are design-contaminated; they prove
plumbing, not edge).*

Then **stop**. The episode/falsification harness and anything money-adjacent is the next handoff.

## 7. Engineering non-negotiables

1. **PIT everywhere:** features may only read rows with `observed_at ≤` the run's decision time.
2. **Fail-soft/fail-closed:** S1 failure halts the run; any other source failure stales its
   components and re-weights the composite; below coverage the state freezes — never silently
   reset, never impute.
3. **Vendor-drift quarantine:** per batch — pinned schema hash, row-count z-score, KS-test on key
   fields; tripped → quarantine + alert, never auto-adapt.
4. **Idempotent, watermarked ingest:** re-running any night is safe; retries with backoff.
5. **Config-driven:** every threshold/weight/window in `config/crowding.yml`; changing one is a
   new registered variant in the ledger, not an edit.
6. **Tests ride along:** each milestone's tests land with its code, not after; mypy strict stays
   green; CI blocks merge.
7. **Ask before deviating** on: data-source substitutions, schema changes, threshold changes,
   scope additions, anything touching money, and the enginev2 PROTOCOL.md port. Small internal
   refactors: just do them.
8. **Public-repo hygiene:** no keys/tokens/account data; education-not-advice footer on the
   published site.

## 8. Things to ask the human before starting

GitHub repo name (default `enginev3`) and visibility (default public) · Finnhub API key + webhook
(Telegram vs Discord) into `settings.local.yml`/repo secrets · the path to **enginev2's
PROTOCOL.md** for the v3.0 port · confirm the KR leveraged-ETF ticker list for `config/crowding.yml`
· confirm SNDK/WDC belong in complex v1 and the SK Hynix ADR add date (~Jul-10).

## 9. Human acceptance checklist (per milestone)

- [ ] CI green + scheduled runs green (A: 3, C: 5 consecutive)
- [ ] Freshness table shows every source inside SLA (or honestly stale-marked)
- [ ] Chaos test demonstrably passes (A)
- [ ] Property tests + synthetic-episode integration test pass (B, C)
- [ ] Report page renders on Pages; alert received on the webhook (C)
- [ ] June-2026 replay demo reviewed (C) · Jul-1→3-2026 CASCADE/EXHAUST replay demo reviewed (C)
- [ ] No secrets in git history; ledger has a registration row per shipped component

## Relationships
- The spec this implements: [H6 crowding & first-defector module](h6-crowding-defector-module.md).
- Conventions/protocol inherited from: [project outline](project-outline.md) · mission:
  [design brief](design-brief.md).
- The manual precedent being automated: tripwire playbook ·
  [distribution & pullback tells](../../shared/concepts/distribution-and-pullback-tells.md).

---
**Refresh triggers:** each milestone completion (tick the checklist, update `status`); any
ask-before-deviating decision (record it here + in the repo ledger); the next handoff (episodes
harness) supersedes §1's deferred column.
