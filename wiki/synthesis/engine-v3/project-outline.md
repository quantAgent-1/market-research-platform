---
type: overview
title: Engine v3 — Full Project Outline (Repo Blueprint)
description: The complete, file-by-file blueprint for enginev3 — the production-grade cross-sectional daily signal platform. Stack decisions (Python 3.13+/uv/pandas+pyarrow, ruff/mypy/pytest+hypothesis, Docker, GH-Actions CI + nightly cron → GitHub-Pages report); the full directory tree with module responsibilities across the five layers (data → features → signals → evaluation → portfolio/live/report/ops); the nightly DAG on the KST clock with idempotency rules; PROTOCOL v3.0 amendments (new data splits, survivorship rule, v2 trial-count import); the testing strategy incl. protocol-enforcement tests; what's reused from v2 vs deliberately dropped; week-by-week deliverables mapped to concrete files; defaults chosen + the open decisions. Companion to the engine-v3 design brief (the why/what); this page is the exactly-what.
tags: [systematic-trading, ml-stats, engineering, small-account, process]
timestamp: 2026-07-03T00:00:00Z
status: active
sources: []
---

# Engine v3 — Full Project Outline (Repo Blueprint)

*Companion to the [design brief](design-brief.md) (mission, constraints, hypotheses,
metrics). This page is the buildable blueprint: every directory, module, and week-one-to-four
deliverable. Kept current as the repo evolves; a copy seeds `docs/DESIGN.md` in the repo itself.*

## 0. Identity & stack (defaults chosen — flag disagreement before Week 1)

- **Working name:** `enginev3` (rename optional before public launch; the repo is **public from
  day 1**, with a public-engine / private-config split — no secrets, account sizes, or live
  positions in git).
- **Language/tooling:** Python **3.13+** · **uv** (deps + lock) · **ruff** (lint+format) ·
  **mypy** (strict on `src/`) · **pytest + hypothesis** · **pre-commit** · **Docker** (slim
  runtime) · **GitHub Actions** (CI + nightly cron) · **GitHub Pages** (the published report).
- **Data:** **pandas + pyarrow parquet** as the lake (yfinance-native, pragmatic); **DuckDB** as an
  optional query layer; *no Numba until profiling demands it* (daily-bar cross-section is
  vectorizable — v2's Numba pattern stays on the shelf).
- **License:** MIT. **Footer everywhere:** education, not investment advice.

## 1. Directory tree (the whole repo)

```
enginev3/
├── pyproject.toml              # uv-managed; deps; ruff/mypy/pytest config
├── uv.lock
├── Dockerfile                  # slim image used by CI and (later) the VPS
├── .pre-commit-config.yaml
├── .github/workflows/
│   ├── ci.yml                  # push/PR: ruff + mypy + pytest (3.13)
│   └── nightly.yml             # cron 22:30 UTC (= 07:30 KST): the nightly DAG + publish + alert
├── README.md                   # front door: mission, architecture diagram, live-report link, badges
├── PROTOCOL.md                 # v3.0 — binding research governance (amended from v2)
├── LICENSE
├── config/
│   ├── universe.yml            # tickers + liquidity-screen rules + re-selection cadence
│   ├── settings.yml            # public defaults: paths, cost-model params, report options
│   └── settings.local.yml     # GITIGNORED: live account size, alert tokens (CI uses repo secrets)
├── src/enginev3/
│   ├── cli.py                  # click: ingest|quality|signals|evaluate|paper|report|run-nightly|log-trade|healthcheck
│   ├── data/
│   │   ├── ingest.py           # yfinance batch OHLCV (Stooq fallback); incremental via per-ticker watermarks; retries
│   │   ├── store.py            # parquet lake I/O; DuckDB view helpers
│   │   ├── quality.py          # fail-loud gates: calendar alignment, NaN/gap/split sanity, volume outliers
│   │   └── universe.py         # membership + liquidity screen; PIT-caveat logging (forward-clean rule)
│   ├── features/
│   │   ├── core.py             # per-name: returns 1/5/10/21d, vol, gaps, RSI(2)/IBS, MA distances, 52w-high prox
│   │   ├── cross_section.py    # winsorize, cross-sectional z-scores, sector-relative residuals, neutralize utils
│   │   └── market.py           # breadth %>200DMA, advance/decline, dispersion, index trend, VIX (^VIX free)
│   ├── signals/
│   │   ├── registry.py         # Signal objects: id, params, hypothesis, NAMED PAYER, status; ledger hooks
│   │   ├── h1_overlay.py       # regime/vol + trend gate → exposure scalar 0–100% (gates everything)
│   │   ├── h2_reversal.py      # cross-sectional short-term reversal (residual z), regime-gated — flagship
│   │   ├── h3_momentum.py      # low-turnover 12-1 momentum ballast (monthly)
│   │   ├── h4_overnight.py     # overnight/intraday split as a filter
│   │   └── h5_calendar.py      # flow-calendar flags (quarter-end, index recon, OpEx) — DASHBOARD-ONLY
│   ├── evaluation/
│   │   ├── ic.py               # daily rank-IC vs 1/5/10/21d fwd returns; mean/t-stat; decay curves
│   │   ├── quantiles.py        # decile portfolios; Q10−Q1 net of costs; monotonicity
│   │   ├── turnover.py         # signal autocorrelation → implied turnover → cost hurdle
│   │   ├── neutralize.py       # factor regressions (beta/size/momentum/sector): alpha or disguised beta?
│   │   ├── robustness.py       # subperiod/regime/sector splits; parameter plateaus
│   │   ├── dsr.py              # deflated Sharpe; total trial count (v2 counts imported for overlapping families)
│   │   └── ledger.py           # append-only research/experiments.jsonl: registered-BEFORE-results
│   ├── portfolio/
│   │   ├── construct.py        # composite → long-only weights; vol targeting; H1 exposure gate
│   │   ├── costs.py            # spread+slippage model; fee ladder 0/5/10/25 bps (post-promo scenarios)
│   │   └── paper.py            # signal-on-close → NEXT-OPEN fills; positions/P&L state (parquet, run-date keyed)
│   ├── live/
│   │   ├── sleeve.py           # top-N candidates + sizing (2%-risk caps); human-readable order tickets
│   │   └── adherence.py        # planned-vs-executed log; adherence-% (a first-class metric)
│   ├── report/
│   │   ├── build.py            # nightly report: regime | breadth | dispersion | signals | flow calendar |
│   │   │                       #   paper P&L + tear sheet | live-vs-backtest IC | adherence
│   │   ├── templates/          # jinja2 (HTML + markdown)
│   │   └── publish.py          # write docs/site/ for GitHub Pages
│   └── ops/
│       ├── runner.py           # the nightly DAG (idempotent, resumable): book pending fills → ingest →
│       │                       #   quality → features → signals → new targets → report → publish
│       ├── alerts.py           # Telegram/Discord webhook: failure detail + nightly success summary
│       └── logging.py          # structlog config
├── research/
│   ├── experiments.jsonl       # THE append-only ledger (checked in; protocol-enforced)
│   ├── notebooks/              # exploration only — excluded from any rigor claim
│   └── reports/                # per-experiment REPORT.md + fresh-eyes AUDIT.md
├── tests/
│   ├── unit/                   # indicator math vs hand fixtures; hypothesis property tests (bounds, invariances)
│   ├── integration/            # 5-ticker × 2-yr fixture lake → full nightly DAG → snapshot the report
│   ├── protocol/               # ENFORCEMENT: evaluation code cannot touch holdout dates (boundary test,
│   │                           #   v2-style); ledger rows registered-before-result; append-only check
│   └── fixtures/
├── data/                       # GITIGNORED parquet lake
└── docs/
    ├── DESIGN.md               # this outline, kept current
    ├── ARCHITECTURE.md         # diagram + dataflow
    ├── RUNBOOK.md              # ops playbook: normal night, failure modes, recovery, re-run rules
    └── site/                   # generated report (Pages source)
```

## 2. The nightly DAG on the KST clock

US close 16:00 ET = 05:00 KST → **cron 22:30 UTC = 07:30 KST** (EOD data settled). Steps
(`ops/runner.py`, each idempotent, re-run-safe via run-date keys and ingest watermarks):
1. **Book pending fills** — yesterday's target portfolio fills at *today's* open (the
   signal-on-close → fill-next-open convention, inherited from v2 verbatim).
2. **Ingest** (incremental) → **quality gates** (fail-loud → alert; a failed gate halts the run
   rather than publishing garbage).
3. **Features → signals → new target portfolio** (H1 exposure gate applied).
4. **Report build + publish** (GitHub Pages) → **alert** (success summary or failure detail).
5. Human loop (evening KST): read the report; if trading the live sleeve, execute at the 22:30 KST
   US open and `cli log-trade` it → adherence updates next night.

## 3. PROTOCOL v3.0 (amendments to v2's binding doc)

- **Universe/horizon:** ~100–300 liquid US names + ETF set; daily bars; holds 1–21 days.
- **Splits (set once):** train ≤ 2023-12-31 · validate 2024-01-01 → 2026-05-31 · **holdout
  2026-06-01 → forward, never consumed, one shot** (the forward paper record is the living OOS).
- **Survivorship rule:** current-membership universes are *forward-clean* (re-selected each
  rebalance, decisions never backdated); historical backtests carry a mandatory PIT-caveat flag.
- **Carried verbatim:** registered-before-results ledger; ~10 variants → obituary; banned outputs;
  fee-ladder + perturbation + latency reruns; fresh-eyes gate (kill is final); DSR ≥ threshold with
  **v2 trial counts imported** for overlapping families; simulation rules (next-open fills,
  gap-through stops, no touching fills/costs/data once results exist).
- **New:** signal registration requires a **named payer** (who-pays-you test) before any backtest.

## 4. Reused from v2 vs deliberately dropped

**Reused:** PROTOCOL text (as base) · ledger format + trial counts · fresh-eyes checklist ·
cost-ladder rerun pattern · signal-on-close→next-open convention · 2%-risk sizing caps ·
signal-only guardrail (no order routing) · later: the OU MLE + BreakDetector (pairs/MR research).
**Dropped:** tick/order-book ingestion and the async hot loop · Numba kernels (until profiling
says otherwise) · Mongo/Postgres services (parquet + DuckDB suffice at this scale) · TSLA-only
anything.

## 5. Week-by-week deliverables (files, not vibes)

- **Wk 1 — scaffold + data:** pyproject/uv/ruff/mypy/pytest/pre-commit; `ci.yml` green + badge;
  Dockerfile; `data/` (ingest, store, quality, universe) + fixtures + unit tests; `nightly.yml`
  running ingest+quality on schedule with alerting. *Exit: 3 consecutive green scheduled runs.*
- **Wk 2 — evaluation core:** `features/*`, `evaluation/*` (ic, quantiles, turnover, neutralize,
  robustness, dsr, ledger); PROTOCOL.md v3.0 committed; H1+H2 registered (payer named) → first IC
  tables + decay curves into `research/reports/`. *Exit: 2 registered verdicts at the IC stage.*
- **Wk 3 — portfolio + report:** `portfolio/*` (construct, costs, paper); `report/*` + Pages
  publishing; tear sheet; the full DAG live end-to-end. *Exit: the nightly report auto-publishing
  with paper P&L.*
- **Wk 4 — polish + launch + live:** README/ARCHITECTURE/RUNBOOK; `live/*` (sleeve, adherence);
  launch write-up; live sleeve begins **only after ≥4 clean paper runs**; stretch: extract the
  rigor-harness OSS package (ledger + DSR gate + fresh-eyes checklist). *Exit: the program page's
  month-end metrics.*

## 6. Success metrics & guardrails (inherited, pre-committed)

≥15 consecutive automated runs, zero silent failures · adherence ≥95% on the live sleeve · paper
IC > 0 out-of-registration for anything shipped · ≥2 registered verdicts/month · report read daily
· **dollars not a KPI**. Guardrails: no order routing; no options; no ML combiner until ≥5
registered linear signals; H5 calendar flags never trade.

## 7. Open decisions / Phase-0 gates

- **Repo name** (default `enginev3`; rename before launch if desired).
- **a Korean retail broker:** fractional US shares? pre-placeable GTC exits? (shapes `live/sleeve.py` sizing).
- **Universe v1:** default = S&P-100 ∪ Nasdaq-100 ∪ ~20 sector/theme ETFs ∪ the semis complex
  (~170 names) — expand to ~300 after the pipeline is boring.
- **VPS graduation:** move `nightly.yml` → systemd timer + healthchecks.io once GH-Actions cron
  jitter/inactivity limits chafe (documented in RUNBOOK).
- KR compliance framing for public signals (education-not-advice footer — verify sufficiency).

## Relationships
- The why/what: [Engine v3 design brief](design-brief.md) · the career frame:
  proof-of-value program · the evidence base:
  [small-account edge map](../retail-capital-edge-map.md) · the methods:
  [algorithmic-trading landscape](../../systematic-trading/concepts/algorithmic-trading-landscape.md).
- Governance inherited from `enginev2/research_loop/PROTOCOL.md` (see the
  session note Q8b mapping).
