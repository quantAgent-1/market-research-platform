---
type: index
title: Designs — Index
description: The library of design specs for tools to build — one buildable blueprint per tool, with build-status tracking and a backlog of designs still to write.
timestamp: 2026-07-06T00:00:00Z
---

# Designs — the tool blueprint library

One page per tool (`type: design`): a **buildable blueprint** — concrete enough that a build can
start from the page alone, honest enough that it can be killed by its own criteria. Distinct from
`synthesis/` (knowledge and programs) the way an architectural drawing is distinct from an essay
about buildings. Design pages are expected to be **superseded by the built artifact**: once a tool
is live, the repo's own docs become truth and the design page's `build:` field records the handoff.

## Conventions

- **Frontmatter:** `type: design` plus the extension field `build:` ∈
  `planned | building | live | killed | superseded` (update it as the tool moves; the page body
  says *why* on every transition).
- **Required sections** (the exit-sentry page is the reference example): Mission & doctrine
  compliance (rule zero: prints into the morning brief in ≤7 days; explicit kill criteria) ·
  Architecture · Data plan (per feed: source, cadence, automation level, failure mode → fallback) ·
  Core logic · Interfaces (brief block / dashboard / panel contract) · Ops (schedule, alerts,
  storage, git) · Build plan (hours, Day-1-live rep) · Honest limits · Open questions.
- **Doctrine inherited from the [present-state stack](../synthesis/present-state-stack.md):**
  engine-v3-first, anti-platform-trap, budget honesty (a new design that overlaps an existing
  planned build must state what it *replaces*).

## Designs

| Design | Build | One line |
|---|---|---|
| [Exit Sentry](exit-sentry.md) | **planned** | The tripwire-exit machine as one pipeline: T1–T8 pullers → state machine → order tickets → dashboard/brief → replay validation; behavioral layer enforced in software. Replaces 3 stack builds; ~24h, Day-1-live. |
| [Forced-Flow Calendar](forced-flow-calendar.md) | **building** — v0.1 live at [`tools/calendar/`](../../tools/calendar/README.md) (19/19 selftest; scrapers/KOFIA-join/panel pending) | Fifteen feeds of scheduled forced flow (US+KRX expiries, reconstitutions, month-end windows, buyback blackouts, lockups, macro clocks, 반대매매 day-after flags) → one event schema → the next-10-days "who is forced" brief block, density/pileup score, day-of KST T-schedules, attribution prior. Deterministic core = pure date math → Day-1-live; ~10h; absorbs the hand-curated July calendar and becomes Exit Sentry's date source. |
| [Market-Research Skill](market-research-skill.md) | **planned** | `.claude/skills/market-research/` — the operating procedure for research-agent fleets: six phases (own-lake-first → data/narrative packs → analysis → adversarial skeptic → file), five role cards with hard contracts (numbers enter only through pullers; skeptic gets fresh context and must attack), the ten-rule accuracy contract, six question-type playbooks, one output contract, `runs.csv` grading loop. ~5h/2 days; live reps = week-ahead Jul-13 + TSMC preview Jul-16; kill = beat the Jul-6 baseline (4 killed / 8 gaps) while re-deriving ≥3 numbers per note. |
| [Valuation Complex (muval)](valuation-complex.md) | **live** at [`tools/muval/`](../../tools/muval/README.md) — design written post-hoc (build ran under the documentation pause) | MU/NVDA/AMD valuation & risk models as one engine: 12-knob cycle-aware scenario paths (data-anchored, all judgment in `assumptions.toml`) → per-name DCF / **reverse DCF** (perpetuity read · priced-in margin · **price-implied bull-path WACC** — the cross-name comparable) / normalized no-break bracket / seeded 20k Monte Carlo / tornado; MU adds the full risk block (GARCH, YZ vol cone, NW factor decomposition, earnings study). Cross-name layers: `events.py` pre-earnings cards (forward-variance implied move ÷ median historical move = **richness verdict**; AMD Aug-4 / NVDA Aug-26 / MU Sep-23) + `complex.py` consistency panel (discount-rate gap ranked AMD>NVDA>MU; MU/NVDA implied steady revenue ratio ~0.42 in every tier = same-bet-not-diversification; joint-bull needs ~$1.02T/yr AI capex = 1.41× the 2026 pool; effective breadth 1.44 bets from 3 names). First full manager/builder run: 6 Sonnet delegations, 3 gates, bit-identical regression discipline. Absorbs the implied-move half of the implied-move-&-TCA backlog item. |
| [Semis Institutional-Flow Map](semis-institutional-flow-map.md) | **building** — P1-live slice live at [`tools/flowmap/`](../../tools/flowmap/README.md) (five-question flow read + dashboard: KR/TW measured anchors, US inference, LETF forced-flow arithmetic, KOFIA/FINRA live; EDGAR crowding + graded log + block scanner pending) | The cohort ledger & anomaly detector for the semis complex: **Korea + Taiwan measured anchors (live S3/S10; TWSE 三大法人 for TSMC 2330 — both keystones directly measured, daily, free) + US inference layer (13F *crowding* diffs, ETF flows as retail/passive gauge, borrow, ATS/non-ATS split, block prints, dealer gamma, buyback run-rates) + ffcal clock** → per-name cohort ledger, POSITIONING/FLOW sub-scores, false-positive-budgeted flags (|z|≥3 single or dual-group |z|≥2), breadth-test attribution (hypotheses, never "institutions bought"), two-level grading (flag verdicts ~6mo; IC verdicts = years, honestly). Absorbs backlog US-positioning-composite + Tool 6's Form-4 slice + Tool 4's block slice; consumes Tool 3. **16–21h in 4 phases**; P1 (13F crowding + ETF flows + TWSE puller, 6–8h) = M11's artifact. **Same-day critic pass in §10:** six findings amended inline, incl. the original IC kill gate failing its own power analysis (16 correlated names ≈ 4 effective bets/day residualized ⇒ IC 0.03–0.05 needs years, not 8 weeks). **Same-day amendment §11 (user sharpened: live data on NVDA/AMD/MU):** the five genuinely-live channels (tape aggression/big prints incl. real-time off-exchange · options sweeps + intraday gamma · closing-auction imbalances [~$15/mo add-on, M8] · computed LETF MOC flow — the only flow knowable *before* it trades · the Asia session as a ~12h-early lead) — identity traded for behavior; build order flipped to **P1-live (~8–12h, merges Tool 3/4 slices)** with EDGAR crowding demoted to P2-context; vendors' "dark pool / flow" products = repackaged L1+L2. |

**Flagship exception:** the [engine-v3 design set](../synthesis/engine-v3/index.md) (design brief,
project outline, H6 module plan, H6-first build handoff) predates this folder and **stays in place**
— the active coding-agent handoff pack references those paths mid-build. New tool designs go here;
engine-v3's docs migrate only if/when a build pause makes the path change free.

## Backlog — designs still to write

Sketches exist in the [present-state stack](../synthesis/present-state-stack.md); each gets a full
design page here when its build slot arrives (July slots first):

- ~~Forced-flow calendar~~ → **design filed 2026-07-06:** [forced-flow-calendar.md](forced-flow-calendar.md)
- **Dealer gamma & options map** — OPRA chains → net-dealer-gamma proxy, flip level, OI walls,
  straddle-implied moves. *(July slot; needs the Alpaca options sub decision.)*
- **Cascade sentinel (Signal-C runtime)** — the live SIP-tape runtime + lev-ETF MOC-pressure
  estimate by 15:00; partly exists in enginev3. *(July slot.)*
- **Breadth discriminator** — automated informed-vs-uninformed one-pager on any >2σ move.
  *(July slot.)*
- **~~Implied-move &~~ TCA remainder** — the implied-move half **absorbed 2026-07-11** by
  [valuation-complex.md](valuation-complex.md) (`events.py`: forward-variance event moves +
  richness verdicts for MU/NVDA/AMD). Remaining: slippage-vs-arrival TCA from fills. *(Aug.)*
- **Event-shock classifier** — LLM news→mechanism tagging ("who is now forced"), Form-4
  routine-vs-opportunistic filter. *(August.)*
- ~~US positioning composite~~ → **absorbed 2026-07-10** (semis-scoped, earlier) by
  [semis-institutional-flow-map.md](semis-institutional-flow-map.md); a market-wide version
  only if the semis version graduates its kill gate.
- **Tech/AI nowcaster** — Korean exports, TSMC monthlies, memory spot, LLM capex tracker → cycle
  dial. *(August.)*
- **Research-accuracy fetchers** — EDGAR CLI (XBRL companyfacts / full-text / Form-4), DART CLI
  (영업(잠정)실적 + S11 overlap), macro CLI (FRED/ALFRED vintages · ECOS · TreasuryDirect auctions)
  + the `research-data` catalog skill. Catalog + build order:
  [research-accuracy stack](../synthesis/research-accuracy-stack.md); design pages per fetcher when
  a slot arrives. *(Day-1 slice ~3h whenever a build block opens.)* ~~market-research +
  verify-numbers skills~~ → **design filed 2026-07-07:**
  [market-research-skill.md](market-research-skill.md) (skeptic role absorbs verify-numbers).

## Relationships

- Roadmap feeding this library: [the present-state stack](../synthesis/present-state-stack.md)
  (the ten-tool build list + sequencing + per-tool kill criteria).
- Integration shell: [Exit Sentry's](exit-sentry.md) `store/panels/*.json` drop-box contract —
  stack tools publish panels there and appear on the one dashboard.
- Frameworks the designs operationalize: [the tripwire exit machine](../systematic-trading/checklists/tripwire-exit-execution.md) ·
  [the monitoring system](../synthesis/semiconductor-monitoring-system.md) ·
  [the edge taxonomy](../synthesis/techniques-of-winning-trades.md).
