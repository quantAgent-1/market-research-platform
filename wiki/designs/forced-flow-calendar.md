---
type: design
build: building
title: "Forced-Flow Calendar — Design Spec & Build Plan (the Mechanical Calendar as Software)"
description: "Full design for stack tool #2: fifteen feeds of scheduled forced flow (US + KRX expiries, index reconstitutions, month/quarter-end windows, buyback blackouts, lockups, macro clocks, 반대매매 day-after flags) normalized into one event schema, rendered as a next-10-days 'who is forced' brief block, a density/pileup score, day-of T-schedules in KST, and an attribution prior for the breadth discriminator. Deterministic core is pure date math → Day-1-live; ~10h total."
tags: [systematic-trading, market-research, tooling, market-structure, flows]
timestamp: 2026-07-06T00:00:00Z
status: active
sources: [../synthesis/present-state-stack.md, ../market-research/july-2026-event-calendar.md, ../shared/concepts/who-pays-you.md]
---

# Forced-Flow Calendar — Design Spec & Build Plan

**Mission.** Constraint flow is the only alpha with a timestamp. Every other payer in
[who pays you](../shared/concepts/who-pays-you.md) must be detected; the Constraint payer
*publishes a schedule* — expiries, reconstitutions, rebalance windows, blackout periods, margin
clocks. Institutions all run this calendar as a desk function; retail runs on vibes, which is why
"random" month-end pops, post-expiry volatility expansions, and blackout-window air pockets keep
reading as mysteries. This tool computes, for every trading day on both tapes, **who is forced to
trade (or forced to stand aside), in which direction, at roughly what size, and at what KST clock
time** — and prints the next ten days into the morning brief.

**Three uses, stated up front — because the honest evidence says most calendar *price* effects
have decayed** (index-add pop ≈ 0 since the 2010s, pre-FOMC drift faded post-publication — see
[what elite traders actually know](../synthesis/what-elite-traders-actually-know.md)):

1. **Risk timing.** Exposure and sizing keyed to event density: know before Sunday night that
   SK hynix + META + FOMC + AAPL land inside 48 hours, and size Monday accordingly. The calendar
   is a *when-not-to-be-big* instrument first.
2. **Execution.** Trade *with* the liquidity events (reconstitution closes are the deepest MOC
   prints of the year), never be the forced side, and never place naive market orders into a
   thin post-holiday or expiry-morning tape.
3. **Attribution.** A mechanical prior for the
   [breadth discriminator](../synthesis/present-state-stack.md): a 2% move on month-end T-1 with
   4× closing volume is plumbing until proven otherwise. This prior is half of "reading the tape
   like an institution."

Directional *trades* on calendar events are explicitly out of scope — that requires a validated
edge, which is [Engine v3 / H6's](../synthesis/engine-v3/index.md) job, not the calendar's.

**Doctrine compliance.** Rule zero: the deterministic core (feeds F1–F6, F11–F12, F14 below) is
pure date arithmetic — no scraping — so the ten-day block prints into **tomorrow's brief on
Day 1**. Engine-v3-first: a standalone module riding the nightly KST run; publishes a panel to
[Exit Sentry's](exit-sentry.md) `store/panels/` drop-box (the one-dashboard contract). Budget
honesty: this build **absorbs** the hand-curated
[July-2026 event calendar](../market-research/july-2026-event-calendar.md) (that page becomes
this tool's rendered July output + post-mortem home; reproducing it 100% is the acceptance test)
and becomes the **single date source** for Exit Sentry's calendar-driven prompts (T3/T4/T7
earnings-date nags read this store — one calendar, two consumers, no drift).

---

## 1. The feed catalog (the crux)

Fifteen feeds, each emitting normalized events. Per feed: the schedule rule, who is forced and
why, the size/effect status (with decay honesty), and automation level.

### US — deterministic (pure date math, Day-1)

| # | Feed | Rule | Who is forced, and how |
|---|---|---|---|
| F1 | **Monthly/quarterly opex** | 3rd Friday; triple witching Mar/Jun/Sep/Dec | Dealers' hedges concentrate then expire: pinning pressure toward large-OI strikes into Friday; the week *after* opex trades wider (gamma runoff until new OI builds). Persistent structural effect — it's hedging mechanics, not a published anomaly. OI-wall levels come from the gamma-map tool; the calendar owns the *dates*. |
| F2 | **VIX expiration** | Wednesday ~30 days before next monthly SPX opex | VIX ETP/structured-product roll flows; vol-complex plumbing day. |
| F3 | **Futures roll week** | ES/NQ volume migrates front→next starting ~8 days before quarterly expiry | Execution note only: basis/liquidity noise in index futures. |
| F4 | **Month-end / quarter-end window** | Last 3 + first 2 sessions | Pension/target-date/balanced mandates rebalance the stock-bond mix (sell the month's winner asset class); window dressing into quarter-end prints; bond-index duration extensions. Size: paste-slot for published bank estimates (the Jun-2026 JPM ~$165B is the archetype) — estimates are wide-error, displayed as ranges with provenance, never false precision. |
| F5 | **Macro clock** | FOMC (8/yr, published; decision 03:00 KST next-day, presser 03:30) + **Fed blackout start** (second Saturday before the meeting — Fedspeak goes silent); CPI (BLS schedule, 21:30/22:30 KST by DST); PCE, NFP (first Friday), GDP; **Treasury QRA** (quarterly) + 10y/30y auction dates (the long-end prints that long-duration tech trades off) | Nobody is "forced" but everyone is synchronized: vol sellers/buyers reposition around known variance events; the pre-FOMC drift window is logged for attribution only (faded post-publication). |
| F6 | **US session structure** | Holidays, half-days (early MOC cutoffs), **DST shifts** | The KST time of every US event moves twice a year — a real gotcha for this desk; the tool renders everything in KST natively. |

### US — scraped / semi-automated

| # | Feed | Rule / source | Who is forced, and how |
|---|---|---|---|
| F7 | **Index reconstitutions** | S&P quarterly: effective 3rd-Friday close Mar/Jun/Sep/Dec, announced ~1 week prior; ad-hoc adds on ~2–5 days notice (press-release RSS). Nasdaq-100: annual recon announced early-Dec, effective at Dec opex. **Russell recon**: ranked from end-April data, prelim lists through May–June, effective at the close of the last Friday of June — the largest MOC volume print of the year. MSCI: Feb/May/Aug/Nov reviews, announced ~2 weeks before, effective at month-end close (the KR leg moves Samsung/SKH weights). | Index funds *must* trade at the effective close — tracking error is their termination clause. **Decay honesty:** the add-day *price* pop is ≈0 now (Greenwood-Sammon), but the *liquidity* event is bigger than ever → use for execution timing and attribution, not direction. |
| F8 | **Watchlist earnings dates** | Public calendars, cross-confirmed against company IR (the only truth); AMC/BMO; `confirmed` vs `estimated` flag mandatory (estimated dates slip) | The anchor most other feeds key off (F9 windows, implied-move joins, Exit Sentry prompts). |
| F9 | **Buyback blackout windows** (derived) | Default proxy per name: [earnings − 5 weeks, earnings + 2 trading days]; rendered as a shaded *band*, not a hard line (policies are private and vary) | The single largest steady demand source in US equities — the corporate bid — **steps aside** (discretionary portion; 10b5-1 autopilot continues) exactly when event risk peaks. Output includes the aggregate gauge: % of watchlist (and of S&P cap) in blackout per day — the "corporate bid presence" curve that troughs into peak earnings weeks. |
| F10 | **Lockup expirations** | IPO +180d default (90/365 and staged unlocks exist); S-1/424B4 filings; watchlist-scoped (recent AI/tech IPOs only) | Insiders + early holders *become able* to sell; supply event with a date. |

### Korea — deterministic

| # | Feed | Rule | Who is forced, and how |
|---|---|---|---|
| F11 | **KRX derivatives 만기** | KOSPI200 options monthly, 2nd Thursday; quadruple witching (동시만기) Mar/Jun/Sep/Dec | The flow lands in the **15:20–15:30 closing auction**; intraday program-trade balance disclosures telegraph direction hours ahead; KOSPI200 constituent changes take effect around the Jun/Dec 만기. Tail case on file: the 2010-11-11 option-expiry crash (replay-gym episode). |
| F12 | **KR macro clock** | BOK MPC (published schedule); Korean CPI; the **exports triplet** — full month on the 1st, 1–10-day print ~the 11th, 1–20-day ~the 21st, all KST mornings | The exports semis line is the global complex's best public leading indicator, published in this timezone before US traders wake — the desk's structural home advantage. |
| F13 | **반대매매 day-after flags** (computed, joins Tool 1) | After any watchlist/KOSPI down-day beyond threshold: flag next morning **09:00–10:00 KST** as a forced-supply window — T+2 미수 liquidations execute at the open, 신용융자 margin calls clear through the morning (the ~10:00 bottoming clock in [KRX session clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md)); flag intensity scaled by the KOFIA margin-balance z-score from the flow engine | The one feed that is *data-triggered* rather than date-fixed — the join point between calendar and flow engine, and the mechanical basis of Signal C's morning setups. |
| F14 | **KR session structure** | KRX holidays; the 15:20–15:30 auction; VI-halt mechanics note; **short-sale-ban regime state** (slow-changing flag) | Session-shape context for every other feed's KR leg. |

### Korea — semi-automated

| # | Feed | Rule / source | Who is forced, and how |
|---|---|---|---|
| F15 | **Korean complex earnings cadence** | Samsung *preliminary* ~5th–8th of Jan/Apr/Jul/Oct (BMO KST; the Jul-7 print is sprint Day 1), full results + call ~3 weeks later; SK hynix dates from IR | Anchors the whole memory complex including US sympathy (MU/NVDA supply-chain reads land on Korean prints, in Korean hours). |

## 1b. Sector extension — semis/AI catalyst feeds (spec'd 2026-07-06, build pending)

The v0.1 feeds are the market's plumbing — correct but generic. This extension makes the
calendar sector-native. Boundary unchanged: the calendar carries **dates + what to ask**;
values (prices, revisions, spot) belong to Exit Sentry and the nowcaster.

**Schema additions (all events):** `chain` tag (equipment | foundry | memory | hbm-chain |
server-odm | networking | hyperscaler | apex | policy | supply) · `tripwires` list (T1–T8 —
which Sentry reads this event feeds; renders as chips and makes the calendar Sentry's single
date source for T2/T3/T4/T7 prompts) · `watch_for` list (the 2–3 sector-critical questions per
print, rendered as a pre-event checklist in the day card) · optional `base_rate` paste field
(median/p10/p90 of the last analogous prints, from the call-sheet ledger).

**F16 — the monthly sector-data print calendar** (rule-based bands, all `estimated` until a
month's date is pinned):

| Print | When (rule) | Why it matters to this book |
|---|---|---|
| **TrendForce DRAM/NAND contract settlement** | last ~3 bd of month, band | THE cycle print — **Sentry T2's date source**; fixed-price m/m is the hard-flip input |
| **Taiwan statutory monthly revenue cluster** | by the 10th; Hon Hai ~5th | The highest-frequency public truth on AI-server demand: TSMC (capex pulse), **Hon Hai** (server assembly), **Aspeed** (BMC — purest server-unit nowcast), Quanta/Wistron ODM cluster |
| **Korea industrial production — semis shipments/inventory lines** | ~last bd, 08:00 KST | The earliest public *inventory-cycle* tell (T4-adjacent); complements the exports triplet |
| **SIA/WSTS global sales** | first week of month | Level-set for the cycle narrative |
| **Equipment billings window (SEMI NA + SEAJ Japan)** | ~3rd week | WFE direction between ASML/AMAT prints (T7-adjacent) |

**F17 — conference/product-qualification calendar** (overrides-driven; 2026 seeds): FMS (~Aug),
Hot Chips (~late Aug), Semicon Taiwan (Sep), **OCP Global Summit (Oct — hyperscaler infra
roadmaps; where custom-ASIC-vs-GPU and HBM-roadmap repricing risk lives)**, SC26 (Nov), Apple
fall event (Sep — device memory content), CES (Jan), GTC (Mar), Computex (Jun); Korea: SK AI
Summit (Nov), Samsung Memory Tech Day (fall), SEDEX (Oct). Plus announced qualification/ramp
milestones (HBM4 quals at NVDA, Rubin ramp windows) as dated entries with `chain: hbm-chain`.

**F18 — policy dates** (overrides-only; honesty note: most policy shocks are *undated* — this
feed captures the minority that carry real dates): announced effective dates of export rules,
comment-period deadlines, statutory merger-review clocks, VEU/license review windows,
tariff-decision deadlines.

**F7 extension:** ICE Semiconductor (SOXX/SOXL) and MarketVector (SMH) quarterly rebalance
effective dates (Mar/Jun/Sep/Dec, third-Friday aligned) — `decayed`, execution/attribution.

**Read-through rendering:** day cards group by `chain` and the dashboard gains a "this week in
the chain" strip (equipment → foundry → memory → hyperscaler), so a TSMC Thursday reads as the
*foundry link* of the same thesis the SK hynix print closes two weeks later.

**Out of scope, stated:** implied moves (gamma tool #3 joins later), consensus deltas (Sentry
T1), DRAM spot (Sentry T5), KIND disclosure scanning e.g. HBM bonder orders (event-shock
classifier #6). Build estimate: Tier A (F16 rules + tripwire/watch_for/chain schema + chips)
~4–6h; Tier B (F17/F18 seeds + F7 extension + chain strip) ~3–4h.

## 2. Architecture

A small module in the engine repo; files are the database, per the
[Exit Sentry](exit-sentry.md) house style.

```
calendar/
├── run.py             # CLI: nightly | next N | day YYYY-MM-DD | confirm | ics
├── rules/             # deterministic generators — each feed = pure fn(date_range) → events
│   ├── us_expiries.py · us_monthend.py · us_macro.py · us_sessions.py
│   └── kr_expiries.py · kr_macro.py · kr_sessions.py
├── scrapers/          # F7 index press-release RSS · F8/F15 earnings confirm · F10 lockups
├── joins/
│   ├── blackouts.py   # F9: windows derived from F8 + aggregate gauge
│   └── bandaemae.py   # F13: reads Tool-1 store (KOFIA z-scores); manual fallback
├── overrides.yaml     # paste-slots: bank rebalance estimates, unconfirmed dates, one-offs
├── store/
│   ├── events.parquet # the normalized event table (git-committed)
│   └── confirm_queue.jsonl
└── render/            # brief block (md) · panels/calendar.json · calendar.ics · t_schedules
```

**The event schema is the design's real decision** — one record shape for all fifteen feeds:

```
{id, feed, market, scope: macro|index|name:TICKER,
 t_kst, t_local, window: point|band,
 direction: buy|sell|two_way|vol|supply|demand_absent,
 size_class: S|M|L|XL (or $ estimate + provenance),
 confidence: deterministic|confirmed|estimated,
 mechanics: "<one line: who must do what>",
 decayed_price_effect: bool,
 uses: [risk|execution|attribution],
 source_url}
```

The `mechanics` one-liner and the `uses` tags are what turn a wall of dates into decisions; the
`decayed_price_effect` flag keeps the tool honest at render time (decayed events display with a
"plumbing, not signal" glyph).

## 3. Core logic — from events to decisions

- **The 10-day brief block** (the daily product): one line per relevant event — date · KST time ·
  event · *who is forced* · direction/size · the "so what" from `uses`. Filtered to watchlist ∪
  macro; XL events bolded.
- **Density score**: Σ(size-class weight × proximity decay) per day → a 0–100 congestion index.
  Flags **pileups** (the SKH+META+FOMC+AAPL 48h cluster the July page hand-flagged becomes a
  computed alert). Exposed as a number the
  [risk constitution](../systematic-trading/checklists/trading-risk-constitution.md) can key
  rules to (e.g. no new overnight adds when density > threshold while holding through ≥2 XL
  events) — advisory in July, mechanical only if it earns it.
- **Day-of T-schedules** for the four XL day-types, rendered as an ordered KST timeline:
  *US opex day*, *KRX 만기 Thursday* (08:30 program disclosures → 09:00–10:00 반대매매 window if
  flagged → intraday balance prints → 15:20 auction), *FOMC night* (03:00 decision → 03:30
  presser), *month-end T-1/T-0*.
- **Attribution prior export**: for any date, the active mechanical explanations as a list —
  consumed by the breadth discriminator to lower the informed-flow prior on plumbing days.
- **Blackout gauge**: the % -in-blackout series (watchlist and S&P-cap weighted) as a panel line.

## 4. Interfaces

Morning-brief markdown block (prepended by the nightly run) · `store/panels/calendar.json` per
the Exit Sentry panel contract (`{title, asof, rows, footnote}`) · `calendar.ics` export so the
XL events sit in the phone calendar · CLI (`cal next 10`, `cal day 2026-07-17`,
`cal confirm NVDA 2026-08-27 --source <IR url>`).

## 5. Ops

Runs inside the nightly KST DAG, before the brief renderer. Scraper failure **fails soft**: the
event degrades to `estimated`, enters the confirm queue, and never blocks the brief. Date
*changes* on confirmed events fire the only alerts this tool sends (plus: new XL event inside
10 days; density crossing the pileup threshold). `events.parquet` + `overrides.yaml`
git-committed nightly. Weekly 10-minute human pass: clear the confirm queue, paste any published
month-end estimates into `overrides.yaml`.

## 6. Build plan (~10h, Day-1-live)

| Day | Hours | Ship | Live rep (rule zero) |
|---|---|---|---|
| **1** | 3 | Schema + all deterministic generators (F1–F6, F11–F12, F14) + 10-day brief renderer | **Block in tomorrow's brief.** Acceptance: reproduces the hand-built [July calendar](../market-research/july-2026-event-calendar.md) 100% — and lists anything the hand version missed |
| **2** | 3 | F9 blackout derivation from hand-entered watchlist earnings + density score + ICS | Blackout gauge + pileup flags render for the Jul-28–31 cluster |
| **3** | 2 | Scrapers: F8/F15 earnings-confirm, F7 index-announcement RSS, F10 watchlist lockups; confirm queue; overrides paste-slots | First auto-confirmed date change logged |
| **4** | 2 | F13 반대매매 join (Tool-1 store read, manual KOFIA fallback) + the 4 day-of T-schedules + Exit Sentry panel | T-schedule fires live on the next KRX 만기 (Jul-9) |

**Kill criteria** (stack doctrine): in the brief Day 1 ✓ by construction; if no graded call or
post-mortem cites a calendar line within 14 days → freeze scrapers, revert to a static quarterly
hand-page, stop. Specific validation: the Jul-9 KRX expiry and Jul-17 US opex T-schedules must
each be *referenced before the fact* in a call sheet to count.

## 7. Honest limits

Size estimates are the weak layer: bank month-end/quarter-end numbers vary widely and carry wide
error bars — the tool shows ranges with provenance and refuses point estimates it doesn't have.
Several famous calendar *price* effects are decayed and flagged as such per feed (index-add pop,
pre-FOMC drift); the durable value is risk/execution/attribution, and the page says so wherever a
user might be tempted to trade the date naively. Blackout windows are proxies for private
policies (bands, not lines; 10b5-1 buying continues inside them). Estimated earnings dates slip
(hence the confirmed-flag discipline). The calendar knows *when* the spring releases — it does
not know how tightly it's wound: positioning size lives in the gamma map (US) and the flow
engine's margin z-scores (KR), which is why those three tools share one brief.

## Build log

- **2026-07-06 — planned → building.** Day-1/Day-2 core shipped same-day as
  [`tools/calendar/`](../../tools/calendar/README.md) (`ffcal.py`, stdlib-only): all
  deterministic feeds (F1–F7, F11, F12, F14), overrides-driven F8/F15 + F9 (merged blackout
  bands + daily corporate-bid gauge), manual F13, the brief/density/pileup renderer, four
  T-schedule templates, ICS export, and a **19-check selftest green** pinned to this page's
  acceptance anchors (Jul-9 만기, Jul-17 opex, CPI/FOMC KST renders, NFP holiday shift, META
  blackout window, gauntlet pileup — the hand-built July calendar reproduces). Bugs caught
  in-build: TOML array-after-table nesting; Samsung prelim/full overlapping blackout windows
  (transitions now fire on merged boundaries only); ICS crash on `time="close"`. Remaining per
  §6: F7 announcement + F8 earnings-confirm + F10 lockup scrapers, F13 KOFIA join (blocked on
  stack tool #1), Exit-Sentry panel export, scheduler entry. **Rule-zero clock is running.**
- **2026-07-06 (later still) — sector layer built (§1b items 1/2/3/5/8; user-selected).**
  New F16 (TrendForce settlement window = Sentry T2's date source; Hon Hai ~5th; Aspeed + ODM
  statutory deadline on the 10th; Korea IP semis inventory ~last KR bd 08:00), F18 policy paste
  feed, SOXX/SOXL+SMH quarterly rebalances in F7, and the `watch_for` question layer
  (`[watch_for]` overrides table, keyed print→ticker→label; rendered in brief `?` lines and
  dashboard checklists; July set seeded: Samsung ×2, SKH, ASML, TSM, MSFT/META/AAPL/AMZN, NVDA,
  MU, BOK, TrendForce, Korea-IP). Selftest 19 → **26 anchors, green**. Dashboard + artifact
  redeployed (same URL). Still pending from §1b: SIA/SEMI/SEAJ, tripwire chips (item 4), F17
  conferences (6), chain strip (7).
- **2026-07-06 (later) — HTML dashboard added** (`ffcal.py html`): self-contained
  `store/dashboard.html` — density-heat + corporate-bid strips on shared day columns,
  pins-needed panel, filterable day cards with embedded T-schedules; light/dark token themes;
  `--fragment` variant published as a claude.ai artifact
  (https://claude.ai/code/artifact/b1407abe-db7d-4549-9f1c-edd69afc2315). This partially
  pre-empts the Exit-Sentry panel item: the calendar now has its own surface; the panel-contract
  export remains for the one-dashboard integration.

## Relationships

- Operationalizes the **Constraint** row of [who pays you](../shared/concepts/who-pays-you.md)
  and the catalyst-calendar gauge of the
  [monitoring system](../synthesis/semiconductor-monitoring-system.md).
- Stack context: tool #2 of the [present-state stack](../synthesis/present-state-stack.md);
  supersedes hand-curation of the
  [July-2026 event calendar](../market-research/july-2026-event-calendar.md) (which becomes this
  tool's rendered output + post-mortem record).
- Consumers: the [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md)
  (brief block), [Exit Sentry](exit-sentry.md) (panel + the single date source for its T3/T4/T7
  prompts), the breadth discriminator (attribution prior), H6 context lanes.
- Mechanics referenced: [KRX session clocks & 반대매매](../shared/concepts/krx-session-clocks-and-forced-liquidation.md) ·
  [liquidity cascades](../shared/concepts/liquidity-cascades-and-v-reversals.md) ·
  decay evidence in [what elite traders actually know](../synthesis/what-elite-traders-actually-know.md).

## Open questions

- Is the KRX intraday program-trade balance feed scrapeable reliably enough to put *live*
  direction into the 만기 T-schedule, or does that stay a manual glance at 14:50?
- US buyback *execution* estimates (GS desk-style daily-bid numbers) circulate secondhand — worth
  a paste-slot, or noise?
- Korea value-up program dates (corporate disclosure deadlines, index events) as feed F16?
- Should density gate the constitution mechanically after July (auto size-caps on pileup days),
  or stay advisory? Decide from the July record.
