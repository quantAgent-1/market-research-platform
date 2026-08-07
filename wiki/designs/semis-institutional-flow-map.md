---
type: design
title: "Semis Institutional-Flow Map — the Cohort Ledger & Anomaly Detector for the Semiconductor Complex"
description: One instrument answering "who is positioned how, and who is being forced, in semis" — Korea + Taiwan direct-measurement anchors (live S3/S10 prints; TWSE 三大法人 for TSMC 2330) + US inference layer (13F crowding diffs, ETF flows as retail/passive gauge, borrow, ATS/non-ATS split, block prints, dealer gamma, buyback run-rates) + the mechanical calendar (ffcal), fused into a daily per-name cohort ledger with POSITIONING/FLOW sub-scores, false-positive-budgeted anomaly flags, breadth-test attribution, and a two-level graded prediction log. Detects positioning and pressure, never intent. Same-day adversarial critic pass recorded in §10 (six findings amended inline, incl. the corrected kill-gate power analysis).
tags: [systematic-trading, market-structure, semiconductors, tooling, data, flow]
timestamp: 2026-07-11T00:00:00Z
status: active
build: building
sources: []
---

# Semis Institutional-Flow Map

**The ask (2026-07-10, S44):** "build an institutional flow tracker/detector on semiconductor
stocks." Per the Query protocol, the design-space map comes first, then the buildable spec.

> **🔨 Build status (2026-07-11): the P1-live slice is LIVE at
> [`tools/flowmap/`](../../tools/flowmap/README.md).** One integrated module + interactive
> dashboard answering the five-question flow read per name: (1) who owned the recent move —
> Korea (Naver investor trend, D+0) and Taiwan (TWSE 三大法人, D+0/D+1) *measured*, US names
> *inferred* (overnight/intraday split, FINRA short-volume mix); (2) forced seller vs informed
> distributor; (3) who is forced next — ffcal calendar + the leveraged-ETF arithmetic
> `(L²−L)×AUM×r` netted across the suite (the one flow knowable *before* it trades) + KR margin
> clock + a naive dealer-gamma state (LOW confidence); (4) where the crowd is — KOFIA margin
> (live), cohort accumulation, SI/IV-vs-RV, equal-weight pre-registered score; (5) what's already
> priced — straddle-implied vs realized moves, run-up vs SMH, 30d EPS drift. The identification
> contract holds in software: **positioning and pressure, never intent** — every attribution ships
> as hypothesis + confidence + falsifier (the MU 2026-06-23 lesson). This realizes §11's build-order
> flip (live intraday first). **Still pending** (later phases): the EDGAR 13F *crowding* diffs
> (P2-context), the two-level graded prediction log, and the block-print scanner (P4, Alpaca-gated).

## In plain language (read this first)

This tool answers one question every morning: **whose money moved in chip stocks yesterday,
and who will be forced to trade soon?** Not prices — people. The market is a handful of
distinct groups: big funds building or dumping positions, index funds that must trade on
known dates, companies buying back their own shares, options dealers who must hedge, and the
retail crowd. Each leaves different fingerprints, and this tool keeps a daily diary of all of
them, per stock.

The core trick: in America, nobody tells you who bought what — you can only infer it from
clues. But **Korea and Taiwan literally publish the answer**: every day, for every stock,
the exchange reports how much foreigners, local institutions, and retail bought and sold.
The two most important semiconductor companies on earth — Samsung/SK hynix (memory) and TSMC
(chip manufacturing) — happen to trade on exactly those two exchanges. So the design measures
Asia directly, infers the US from clues (quarterly fund filings, daily ETF money in and out,
the cost of borrowing shares, where trades print, options hedging pressure, buyback
schedules), and lays the known calendar of *forced* trading on top.

Two honesty rules run through everything. First, the tool reads pressure, not minds — a big
seller might know something, or might just need cash (the desk's own Micron June-23 lesson:
a drop that looked like insider selling was actually Korean leveraged-ETF funds forced to
sell). So every alert says *what happened, who most likely did it, and how confident that
guess is*. Second, every alert gets graded against what happened next, so within a few months
the tool's record tells us honestly whether it works.

## 0. The design-space map — toy / professional / world-class

**Toy (~1–2 days).** Pull 13F diffs + short interest + Form 4s for ten semis names into a
dashboard. Why it fails: the 45-day 13F lag dominates everything (you learn in mid-May what
funds held on March 31); no intraday or even daily cohort signal; no attribution logic — so it
emits "institutions are buying NVDA" narratives that are unfalsifiable and mostly stale. This
is what every retail "smart money tracker" website is, which is why none of them are edges.

**Professional (~14–19h phased — this design).** A multi-cohort **present-state map** at the
best cadence each data class permits: Korea prints daily (direct measurement — the anchor), ETF
flows and borrow daily, options positioning daily, dark share weekly-lagged, filings
quarterly-as-baseline — fused into one per-name cohort ledger with **pre-registered anomaly
flags**, attribution run through the [breadth test](../shared/concepts/informed-vs-uninformed-flow.md)
first, every flag logged and graded. The product is the retail replica of a prime broker's
positioning note for one sector, plus an honest scorecard of whether it predicts anything.

**World-class (structurally unbuyable — verified in [industrialization of edge](../synthesis/industrialization-of-edge.md)).**
Real internalization/PB flow visibility (private by construction), tick-level metaorder
attribution on full TAQ/OPRA history, client-order-book knowledge. Not reachable at any retail
price; the copyable part is the *process* (present-state map + forced-flow calendar +
calibration), which this desk already runs.

**The axes separating tiers:** latency (quarterly → daily → tick) · attribution confidence
(narrative → cohort-hypothesis → measured) · coverage (one name → complex-wide → cross-market)
· verification (none → graded flags) · cost ($0 → $99/mo → private-only).

**The desk's differentiator — design around it:** for the Korean half of the complex
(Samsung, SK hynix, 한미반도체), the desk already holds **actual per-name daily
institutional-flow prints** (S3, live; KOFIA margin S10, live; per-name credit S12 planned) —
direct measurement no US retail desk has, and the Jun-2026 unwind proved Korea cohort flow
**leads** US semis moves. The critic pass found the **second measured anchor**: Taiwan
discloses the same class of per-name daily cohort prints (三大法人 — foreign / investment
trust / dealer) for TSMC's home listing 2330 — so **both keystones of the global complex
(memory in Seoul, foundry in Taipei) are directly measurable, daily, free.** For US names, no
such prints exist; everything is inference from proxies. So the architecture is:
**Korea + Taiwan = measured anchors · US = inference layer · ffcal = the forced-flow clock ·
identification discipline = the breadth test.** A US-only 13F tracker is a commodity; an
Asia-anchored complex-wide map is differentiated and half-built.

## 1. Mission & doctrine compliance

**Mission.** Every morning, answer for the semis watchlist: *which cohorts moved yesterday,
who is positioned how, what forced flow is scheduled next, and did anything anomalous print* —
with attribution stated as graded hypotheses, never as fact.

**Rule zero.** Phase 1 prints into the morning brief ≤ 7 days from build start or the tool is
cut. Each later phase ships its own brief line the week it's built.

**The identification contract (the design's load-bearing honesty).** This tool detects
**positioning and pressure, not intent**. The desk's own worked example is the reason:
MU −13.18% (Jun-23) looked exactly like informed selling and was a Korea-led LETF cascade.
Every output passes the [informed-vs-uninformed](../shared/concepts/informed-vs-uninformed-flow.md)
discipline: breadth test first (complex-wide ⇒ flow; idiosyncratic ⇒ dig), attribution emitted
as hypothesis + confidence, and forward-graded.

**Budget honesty (designs-index convention — what this absorbs/replaces).** Absorbs the
backlog's **"US positioning composite"** (this is its semis-scoped, earlier version); takes the
**Form-4 filter slice** of the event-shock classifier (Tool 6) and the **block-print scanner
slice** of the cascade sentinel (Tool 4); **consumes** (does not duplicate) the dealer-gamma
map (Tool 3) when built; Layers A/B below are existing live/building systems (S3/S5/S10,
ffcal) — zero new build there. Cost cap: the already-planned ~$99/mo Alpaca subscription;
everything else free.

## 2. Architecture — three layers over one ledger

```
Layer A  ASIA DIRECT (measured)  KR (live): S3 per-name cohort prints · S10 margin · [S12 credit]
                                 TW (new — critic-pass find): TWSE 三大法人 daily for 2330/2454
Layer B  MECHANICAL CLOCK (live) ffcal: expiries/recon/blackouts/lockups · S5 LETF AUM → MOC estimate
Layer C  US INFERENCE (new)      C1 EDGAR filings (crowding read) · C2 ETF flows (retail/passive)
                                 C3 short/borrow · C4 ATS vs non-ATS split · C5 block prints
                                 C6 dealer gamma (from Tool 3) · C7 buyback cohort
                    ↓
         PER-NAME DAILY COHORT LEDGER (PIT lake, engine-v3 schema)
                    ↓
         POSITIONING state + FLOW pressure sub-scores + corrected anomaly-flag rules (§4)
                    ↓
         attribution decision tree (breadth test → cohort hypothesis + confidence)
                    ↓
         brief block · alerts · graded prediction log
```

**Watchlist v1.** US: NVDA, AMD, AVGO, MU, TSM, ASML, AMAT, LRCX, KLAC, INTC, MRVL, QCOM +
SMH, SOXX, SOXL/SOXS. KR: 005930, 000660, 042700. TW: 2330 (TSMC home listing — the complex's
keystone, directly measured via A3), 2454. (Extend later; capacity of the brief, not the code,
is the constraint.)

## 3. Data plan (per feed: source · cadence · automation · failure mode → fallback)

| # | Feed | Source | Cadence | Auto | Failure → fallback |
|---|------|--------|---------|------|--------------------|
| A1 | KR per-name cohort flows | KRX (S3, **live**) | daily D+0 | full | already in nightly SLA |
| A2 | KR margin/credit | KOFIA (S10 **live**; S12 planned) | daily | full | market-level only until S12 |
| A3 | **TW per-name cohort flows** *(added by the critic pass)* | TWSE/TPEx daily 三大法人 per-name buy/sell (foreign / investment trust / dealer) for 2330, 2454 | daily D+0 | full (~1–2h puller) | FINI market-level aggregates |
| B1 | Forced-flow calendar | ffcal (**live v0.2**) | daily | full | hand calendar |
| B2 | LETF rebalance estimate | S5 AUM (**live**) × day return | intraday 15:00 ET | full | skip line |
| C1a | 13F quarterly diffs — **read as crowding/fragility, not smart-money-following** (critic pass §10) | EDGAR structured 13F XML; panel of ~20 managers (active semis-heavy: Fidelity/Capital/T.Rowe/Wellington class + Coatue/Altimeter/Viking/Appaloosa class + specialists). Engineering contract: diff **shares not value**, split-adjust, treat call/put lines separately (exclude from crowding), latest amendment per period wins | quarterly (45d lag) | full | manual WhaleWisdom check |
| C1b | 13D/G crossings | EDGAR full-text daily | daily | full | *(honest note: ~irrelevant for megacaps — 5% of NVDA doesn't happen; matters for small/mid equipment names only)* |
| C1c | Form 4 insiders | EDGAR daily index; routine-vs-opportunistic flag (10b5-1 marker + regularity heuristic per Cohen–Malloy–Pomorski) | daily | full | weekly batch |
| C2 | ETF flows — **relabeled: retail/passive cohort gauge, NOT institutional** (critic pass §10) | Issuer daily SO/NAV files: SMH (VanEck), SOXX (iShares), SOXL/SOXS (Direxion — S5 extension) | daily D+1 | full | ETF.com weekly |
| C3 | Short interest + borrow | FINRA SI (S4 **live**, bi-monthly T+9) + IBKR shortable/fee API | SI bi-monthly; borrow daily | full | SI only |
| C4 | Off-exchange share — **must be split: ATS (institutional-block proxy) vs non-ATS OTC (wholesaler-internalized retail proxy)**; the two are *opposite* cohorts and their sum is uninterpretable (critic pass §10) | FINRA OTC Transparency weekly files, ATS and non-ATS published separately (~2wk lag Tier-1) | weekly | full | skip (lag noted on every print) |
| C5 | Block prints / auction share | Alpaca SIP trade stream: single prints ≥$2M or ≥0.05% ADV; closing-auction volume share | daily | full | **gated on the Alpaca sub decision** (same gate as Tool 3); v1 without it |
| C6 | Dealer gamma / OI walls | Tool 3 (dealer-gamma map) output; until built, S2′ archive slice (extend MU → NVDA/SMH) | daily | full | IV/OI deltas only |
| C7 | **Corporate buyback cohort** *(added by the critic pass — the largest single US equity buyer was missing)* | EDGAR XBRL companyfacts (quarterly repurchase $) ÷ trading days → daily run-rate bid estimate; blackout state from ffcal | quarterly rate, daily state | full (~1h) | blackout windows only |

*(MOC imbalance feeds are broker/paid-gated — explicitly out of v1; closing-auction volume
share is the free proxy. No SOX futures exist; COT (S6) stays a macro-tape overlay only.)*

## 4. Core logic

**The cohort ledger.** One row per name per day: KR cohort net-buys (A1, measured) · ETF share
flow (C2) · ΔOI/gamma state (C6) · Δborrow fee & utilization (C3) · dark share (C4, lagged
flag) · block-print $ share (C5) · insider net-30d with opportunistic flag (C1c) · 13F
baseline tilt & crowding count (C1a, quarterly) · scheduled forced flow next 5 sessions (B1/B2).

**Two sub-scores, not one (critic-pass correction).** Mixing quarterly levels with daily deltas
in one z-composite is statistically incoherent. Split: **POSITIONING state** (slow variables:
13F crowding/HF-ownership concentration, SI level, dealer-gamma regime, buyback run-rate —
updated at each variable's own cadence, read as *fragility context*) and **FLOW pressure** (fast
variables: KR/TW cohort net-buys, ETF share flow, Δborrow, ΔATS share, block share — daily
z-scores over trailing 60d). Weights within each sub-score pre-registered equal; **no fitting
until ≥60 graded days exist** (the [solution-sheet](../synthesis/institution-grade-solution-sheet.md)
machinery applies unchanged).

**Anomaly flags — thresholds set by false-positive arithmetic (critic-pass correction).** The
original |z| ≥ 2 single-feed rule fails multiple-testing trivially: ~8 daily feeds × ~18 names ≈
**150 tests/day → ~7 pure-noise flags/day** at |z| ≥ 2. Alert fatigue kills tools faster than
bad data. Pre-registered rule: a flag fires on **|z| ≥ 3 on a single feed (~0.4 noise
flags/day)**, or **|z| ≥ 2 confirmed on ≥2 feeds from different evidence groups** (groups:
Asia-prints / ETF-flows / options / short-borrow / off-exchange / filings — within-group
correlation makes same-group confirmation worthless), or the divergence tells (price ±2σ
*without* cohort confirmation; retail-accumulating-what-foreigners-distribute on KR names).
FLOW composite alert at mean-z ≥ 1.25 — under independence that's ~3.5σ; under a realistic
average cross-feed correlation ~0.3 it's nearer 2σ, stated so the alert's real rarity is honest.

**Attribution decision tree.** On any flag: (1) breadth test — complex-wide or idiosyncratic?
(2) if complex-wide → flow explanation; check B1/B2 for the scheduled suspect; Signal-C/H6
state. (3) if idiosyncratic → check C1c/C6/C3 for the informed-flow tells, emit "dig" with the
specific channel. (4) output = hypothesis + confidence + the falsifying observation. Never a
bare "institutions bought."

**Grading loop — two levels, with the power arithmetic stated (critic-pass correction).**
(1) **Flag-level** (the operational verdict): every flag logs hypothesis, confidence, and
1d/5d forward outcome **on SMH-residualized returns** (raw semis returns are ~0.7 cross-
correlated — grading on them mostly grades the sector). Power: detecting a ~0.3σ mean effect
per flag needs ~90 graded flags → at ~1–2 genuine flags/day, **flag-level verdicts arrive in
3–6 months.** (2) **IC-level** (the research verdict): daily rank-IC of the FLOW score vs
next-1–5d residualized returns, reported quarterly with CIs — but stated honestly: 16 names at
residual correlation ~0.2 is ~4 effective bets/day, so a professional-grade IC of 0.03–0.05
reaches t ≥ 2 only after **years, not weeks**. The IC number is tracked from day one and
*believed* only at that horizon.

## 5. Interfaces

Morning brief block (**"SEMIS FLOW MAP"**): 3–6 lines — per-name pressure scores that moved,
active flags with attribution hypotheses, next-5-day forced-flow lines, KR-cohort lead read.
Panel JSON to Exit Sentry's `store/panels/` drop-box (the stack's one-dashboard contract).
Alerts (composite ≥ 60 or breadth-test "idiosyncratic" verdicts) → the existing alert channel.

## 6. Ops

Nightly KST batch after the engine's existing DAG (A/C feeds); 15:00 ET intraday line for B2;
weekly C4 ingest. Storage: engine-v3 PIT lake conventions (raw + derived, as-of stamps).
Git: `tools/flowmap/` per the tools-README convention. Heartbeat into the nightly SLA table.

## 7. Build plan (phased; each phase ships a brief line the same week)

| Phase | Hours | Ships | Note |
|-------|-------|-------|------|
| P1 | 6–8h | EDGAR 13F puller + 2-quarter **crowding** table (20 managers × watchlist, shares-diffed/split-adjusted) + ETF-flow daily line (C2 = S5 extension) + **TWSE A3 puller (critic-pass addition — the second measured anchor ships first, not last)** → brief block v0 | **= ledger row M11's artifact**; Day-1-live rep |
| P2 | 4–5h | Form-4 opportunistic filter + daily borrow + FINRA **ATS/non-ATS split** ingest + **C7 buyback run-rates** → alerts v0 | absorbs Tool 6's Form-4 slice |
| P3 | 3–4h | Cohort ledger assembly + the two sub-scores + corrected flag rules + attribution tree (breadth test inline) | Tool 5's logic, wired to live feeds |
| P4 | 3–4h | Block-print scanner (with measured false-positive rate — M13's artifact) + prediction log + grading loop | gated on Alpaca sub (Tool 3's gate) |

Total **16–21h** to professional tier (was 14–19h; the critic pass added A3 + C7 and the
engineering contracts). Order chosen so the free, ungated, *measured* layers land first and the
paid-gated inference layer lands last.

## 8. Kill criteria (pre-committed)

1. Rule zero: P1 not in the brief within 7 days of build start → cut.
2. **(Corrected by the critic pass — the original gate failed its own power analysis:
   demanding IC t ≥ 2 in 8 weeks would kill a genuinely working tool with near-certainty.)**
   Split into two gates: **(2a) decision-use gate, 8 weeks** — the brief block influenced <1
   actual decision/week → demote to weekly digest. **(2b) flag-quality gate, ~6 months / ≥90
   graded flags** — flag-level hit rate on residualized 5d outcomes shows no edge over base
   rate (per the grading loop's power arithmetic) → stop calling flags signals; keep the
   cohort ledger as context. The IC-level research verdict runs on its own multi-year clock
   and never gates operations.
3. Any layer whose data lag makes its flags strictly reactive (fires only after the move) for
   3 consecutive graded events → drop the layer from the composite (keep as context line).
4. Cost creep beyond the Alpaca plan → out of scope, full stop.

## 9. Honest limits

- **Intent is unobservable.** The tool maps pressure and positioning; the informed/uninformed
  verdict is a graded hypothesis with a known failure mode (MU Jun-23). Anyone who sells a
  "smart money detector" without this caveat is selling the [lottery](../shared/concepts/leverage-lottery-arithmetic.md)'s
  research-tool costume.
- **US per-name daily cohort attribution is impossible from public data.** Only the KR names
  get true measurement; the US side is proxy inference, permanently hypothesis-grade. The
  wholesaler/PB layer is invisible by construction (verified:
  [industrialization](../synthesis/industrialization-of-edge.md) §3).
- **13F is a baseline, never timing** (45-day lag); 13D ~never fires on megacaps; dark-share
  data lags ~2 weeks; MOC imbalance feeds are out of reach in v1.
- **13F cannot see NET positioning — at all.** It reports long US-listed equity/option custody
  only: no shorts, no swaps, no futures; family offices are exempt entirely (Archegos held
  tens of billions in total-return swaps and filed *nothing*). A fund long NVDA in its 13F can
  be net short the name. This is why C1a is framed as gross-long **crowding/fragility** — the
  one reading that survives the limitation — and never as "smart money is bullish."
- **The passive giants dominate megacap 13F holdings** (Vanguard/BlackRock/SSGA class own
  ~20%+ of NVDA); their changes are index mechanics, not views — excluded from the crowding
  panel by construction (active managers only).
- **Anticipation-decay applies to this tool's own outputs**: any flag pattern that works and is
  publishable is on the same decay clock as the index effect — the durable part is the
  process + the KR data moat, not any single flag.

## 10. Critic pass (2026-07-10, same-day, on challenge — "are you sure? more rigorous?")

Adversarial pass per the Query protocol's build clause, run against the v1 spec. Structural
verdict: the three-layer architecture, rule zero, and the identification contract survive.
Six findings, all amended inline above:

1. **The IC kill gate failed its own power analysis (the most serious defect).** Sixteen ~0.7
   cross-correlated names ≈ 1–2 effective independent bets/day raw, ~4 residualized; a
   professional-grade IC of 0.03–0.05 cannot reach t ≥ 2 in 8 weeks under any honest math —
   the gate would have killed a *working* tool. Fixed: two-level grading (flag-level verdicts
   in 3–6 months at ~90 graded flags; IC-level on a multi-year research clock), evaluation on
   SMH-residualized returns, kill gate split into decision-use (8wk) + flag-quality (~6mo).
2. **The flag thresholds failed multiple-testing arithmetic.** ~150 tests/day at |z| ≥ 2 ⇒ ~7
   noise flags/day ⇒ alert-fatigue death. Fixed: |z| ≥ 3 single-feed (~0.4/day) or |z| ≥ 2
   cross-confirmed across independent evidence groups; composite threshold stated with its
   correlation-honest rarity.
3. **Two legs were mislabeled cohorts.** C2 ETF flows are a retail/passive gauge, not
   institutional (creation/redemption also carries MM inventory noise; flows chase returns);
   C4's raw off-exchange share sums wholesaler-internalized *retail* with institutional ATS
   *blocks* — opposite cohorts, uninterpretable summed. Fixed: relabel C2; split C4 into
   ATS / non-ATS.
4. **13F was over-read.** It shows long-only US-listed custody — no shorts, swaps, futures;
   family offices exempt (Archegos filed nothing); passive giants dominate megacap registers.
   Fixed: C1a reframed from "smart-money following" to **gross-long crowding/fragility**
   (the reading the quant-quake/de-gross literature actually supports — crowded names carry
   tail risk, which feeds H6/unwind machinery), active-manager panel only, shares-diffed and
   split-adjusted, option lines separated.
5. **A missing cohort: the corporate bid.** Buybacks are the largest single US equity buyer
   class and were absent except via blackout windows. Added C7 (XBRL repurchase run-rates +
   blackout state, ~1h).
6. **A missing measured anchor — the pass's best find:** TWSE's per-name daily 三大法人
   prints give TSMC 2330 (and 2454) Korea-grade direct cohort measurement. Layer A becomes
   two-anchor Asia-direct; the Jun-2026 "Korea leads US semis" hypothesis generalizes to a
   two-anchor Asia-leads-US test, graded for free by the tool itself. (Considered and
   rejected: Japan — weekly aggregate only, not per-name; India FII/DII — not semis-relevant.)
   C5 (block prints) is noted as the *weakest* leg — negotiated blocks print off-exchange,
   algo slicing hides the rest, and the sub-penny retail-identification literature (BJZZ) has
   a published accuracy critique — hence its false-positive rate is P4's own deliverable (M13).

Evidence grades now attached to each leg's predictive validity: opportunistic insiders [A,
82bp/mo] · crowding→tail-risk [A/B] · SI level [A theory, weak on megacaps — conditional
flag only] · ETF flow→vol [A] / flow→alpha [weak] · dealer gamma [B/C practitioner] ·
ATS share [C] · block prints [C, measured in P4]. The composite stays equal-weighted
(anti-overfit) but expectations per leg are now honest.

## 11. Amendment (2026-07-10, same day): the live intraday layer — user requirement sharpened

The user, correctly: *"I want higher-frequency live data, not quarterly reports that are stale
by the time the market has moved — specifically NVDA, AMD, MU."* The design's answer, stated
plainly first: **no one publishes live per-name "institutions bought $X of NVDA" data at any
price** — that information exists only inside brokers and is private by construction. What
high-frequency reality offers instead is a trade: **you give up identity and gain behavior.**
At intraday speed you cannot know *who* is trading, but you can measure live *how* the trading
behaves — urgency, size signatures, hedging pressure, and forced flows you can compute before
they execute. Five channels are genuinely live or same-day for NVDA/AMD/MU:

| # | Live channel | What it shows | Latency | Access/cost | Limit |
|---|---|---|---|---|---|
| L1 | **The live tape read** (consolidated feed of every trade) | Buyer-vs-seller aggression (share of volume trading at the offer = buyers paying up, vs at the bid), retail share via sub-penny-priced prints, and **big prints — including off-exchange/"dark" trades, which hit the public tape within seconds** (venue anonymized; the weekly FINRA files only add venue detail later) | seconds | Alpaca ~$99/mo (already planned — same gate as Tool 3) | behavior, not identity; algos slice most institutional orders into invisible children (M13) |
| L2 | **Live options flow + dealer pressure** | Urgent positioning leaks here first: large sweeps at the ask on short-dated contracts; plus the dealer-hedging state (long-gamma = dampens moves, short-gamma = amplifies) recomputed intraday | seconds–minutes | same Alpaca OPRA feed; = Tool 3 pulled forward | attribution is inference; heavy multiple-testing discipline per §4 |
| L3 | **Closing-auction imbalances** | The one scheduled moment institutional orders become semi-visible *before executing*: exchanges broadcast the net buy/sell imbalance for the 4pm auction starting ~3:50–3:55 ET | ~10 min before execution | small broker add-on (e.g. IBKR + Nasdaq TotalView, order ~$15/mo) — **the one new cost this amendment adds** | late-day only; re-surfaces ledger **M8** (US auction plumbing), no new row |
| L4 | **Computed forced flows** | The only flow knowable *before it trades*: leveraged-ETF rebalancing. SOXL must trade (L²−L)=6× its assets × the day's return at the close — with ~$26B AUM (live S5), a +2% semis day ⇒ **≈$3.1B of mechanical buying into the close, computable by ~3pm** | hours ahead | free (S5 live + arithmetic) | one cohort only; netting across the LETF suite required |
| L5 | **The Asia lead as live data** | Samsung/SKH (memory ⇒ MU's thesis twins) and TSMC 2330 (⇒ NVDA/AMD's supply chain) cohort prints arrive during the Asian session — **hours before the US open**. Daily data, but *earlier on the global clock*: effectively a pre-market institutional read for US semis | ~12h ahead of US open | free (S3 live + A3 puller) | cross-market inference, graded as the Asia-leads-US hypothesis |

Plus the daily-fresh (not intraday) upgrades already in the plan: FINRA **daily** short-sale
volume files (published same evening — far fresher than the bi-monthly SI), daily borrow fees,
daily ETF flows. The quarterly filings stay in the design *only* as crowding context (§10.4) —
they were never the engine.

**What the "live institutional flow" vendors sell (honesty note):** services in the
$50–150/mo range (unusual-options-activity and "dark pool print" platforms) are repackaging
exactly L1+L2 — public OPRA prints and TRF off-exchange prints that are on the tape for
anyone with the feed. Building L1+L2 in-house on the already-planned Alpaca subscription buys
the same data without the mystique, plus custom logic.

**Build-order consequence:** the live layer is no longer P4-last. Revised order for a
NVDA/AMD/MU-focused desk: **P1-live (~8–12h)** = L1 aggression/big-print monitor + L2 sweep
detector & intraday gamma state (merges the planned Tool 3/Tool 4 slices, scoped to
NVDA/AMD/MU + SMH) + L4 LETF MOC line (exists) + L5 TWSE puller, feeding a **live intraday
panel** in addition to the morning brief; the EDGAR/crowding work (old P1) becomes **P2-context
(~4–6h)**; L3 auction-imbalance feed decision rides with it. Grading discipline (§4's
false-positive budgets, two-level verdicts) applies unchanged — *more* strictly intraday,
since noise scales with frequency.

**Honest limit of the live layer:** at second-level latency you are reading the present, not
racing it — HFT firms win every race by microseconds, permanently. The live layer's use is
state-reading (is this a cascade or information? is the close about to amplify? who is forced?)
feeding the desk's existing checklists — never speed competition. High frequency also means
faster edge decay and weaker attribution; the flag thresholds tighten accordingly.

## Relationships

- Consumers: [conviction-swing on institutional accumulation](../systematic-trading/strategies/conviction-swing-on-institutional-accumulation.md)
  (its evidence layer, systematized) · the [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md) ·
  H6 (crowding spine) · the [semiconductor monitoring system](../synthesis/semiconductor-monitoring-system.md)
  (this is its positioning gauge, made per-name).
- Parents: [present-state stack](../synthesis/present-state-stack.md) (Tools 1/3/4/5/6 —
  absorption map in §1) · [ffcal](forced-flow-calendar.md) · engine-v3 feeds S2′–S10.
- Doctrine: [informed-vs-uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md) ·
  [what elite traders actually know](../synthesis/what-elite-traders-actually-know.md) (which
  slices are recoverable) · [industrialization of edge](../synthesis/industrialization-of-edge.md)
  (why the rest isn't).
- Ledger: **M11** (13F/13D/Form-4 plumbing — P1 is its artifact) · **M13** (trade-classification
  & metaorder inference — the methods under C5; new row).

## Open questions

- Alpaca sub timing (gates P4 + Tool 3 — one decision, two tools).
- S12 (per-name 신용잔고) build slot — upgrades A2 from market-level to per-name.
- Manager panel composition for C1a: which 20 filers actually move semis? (First 13F diff run
  answers this empirically — start broad, prune by observed position sizes.)
- Does the KR-cohort lead on US semis (Jun-2026 evidence, n=1 regime) hold across regimes? The
  grading loop answers this for free.
