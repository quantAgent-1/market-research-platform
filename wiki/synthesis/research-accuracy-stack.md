---
type: overview
title: "The Research Accuracy Stack — Primary-Source Tools & Skills for Agent Market Research"
description: What to build so research agents stop depending on web search — a source-tier ladder, the seven transcription traps, four layers of tools (expose the own lake, Tier-0 fetchers, procedure-as-skills, gated paid feeds), with hours, kill criteria, and honest limits.
tags: [systematic-trading, tooling, data, research-process, agents]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# The Research Accuracy Stack — Primary-Source Tools & Skills for Agent Market Research

Filed 2026-07-07 from a session query: *"when I ask Claude agents to do market research, what
tools and skills can we set up for better, more accurate analysis — instead of relying on plain
web search and preloaded tools — so agents can use them repeatedly?"*

This is the sibling of [the present-state stack](present-state-stack.md), one level up the
pipeline. That page builds sensors for the **desk** (what prints into the morning brief). This
page equips the **research agents** — the ones that write the
[week-ahead briefs](../market-research/weekly/week-ahead-2026-07-06.md), earnings previews,
regime reads, and thesis checks in `market-research/`. The two stacks share most data sources;
they differ in consumer and failure mode. A desk tool that breaks misses a print. A research
agent without primary sources doesn't break — it **confidently files a wrong number**, which is
worse.

## Why web search fails, measured on our own tape

The Jul-6 deep-research run (104 agents, web search only) is the controlled experiment. Of 58
extracted claims, 25 were adversarially verified and **4 were killed — every kill was a date or
number fact**: a wrong ISM release date, a Jul-9 tariff-reversion catalyst refuted 0-3, a
mis-dated NFP print (57k vs 98k ambiguity), a stale EPS consensus. Meanwhile the brief declared
"the entire vol/positioning section is a gap" — VIX term structure, put/call, NAAIM, fund flows —
**data that enginev3's own lake now holds in S2′/S4/S5/S6/S8**. The agents didn't lack
intelligence; they lacked (a) access to our own instruments and (b) primary sources for facts
that journalism transcribes lossily.

Web search has three honest jobs in research: **discovery** (what happened, what's being said),
**narrative** (what the crowd believes — itself a positioning datum), and **finding the Tier-0
document**. It should never be the citation for a load-bearing number.

## The source-tier ladder (the doctrine in one table)

| Tier | Who | Examples | Use |
|---|---|---|---|
| **0 — the filer** | The reporting entity's own filing | SEC EDGAR/XBRL, DART 공시, central-bank releases, statistical agencies (BLS/BOK/customs) | Load-bearing numbers, verbatim |
| **1 — the venue/SRO** | Official aggregates of market activity | KRX, KOFIA, FINRA, CBOE, OCC, CFTC, TreasuryDirect | Load-bearing market/flow numbers |
| **2 — primary vendors** | Contractual-accuracy paid feeds | Alpaca/OPRA, FMP, Databento, Norgate | Where Tier 0/1 has no coverage (consensus, transcripts Q&A, clean tick data) |
| **3 — journalism & aggregators** | Everything web search returns | News, blogs, X, Yahoo-tier scrapes | Discovery + narrative only; never sole source for a number |

**The rule:** a number that a conclusion rests on is cited at Tier 0/1, or carried by two
independent Tier 2/3 sources **and marked ◐**. This is the
[verification-flags](../verification-flags-2026-06-22.md) discipline moved from post-hoc audit
to ingestion-time.

## The seven transcription traps (what "accuracy" concretely means)

These are the recurring ways secondhand financial data is wrong. Each one has already bitten
this desk or a named public failure; the tools below exist to make them structurally hard.

1. **The vintage trap (macro).** FRED shows today's *revised* series; the market traded the
   *initial* print. NFP revisions of ±100k are routine. ALFRED (same API, `realtime_start/end`
   parameters) serves what-was-known-when. The Jul-6 brief's 57k-vs-98k NFP confusion was this
   trap plus an ADP/BLS conflation.
2. **The consensus-provenance trap.** "Beat by 4%" depends on *whose* consensus — Refinitiv,
   FactSet, Zacks, and StreetAccount routinely differ, and free scrapes lag. Rule: name the
   consensus source and its as-of date, or mark ◐. (S7′'s Finnhub-free estimates are already
   flagged lower-confidence in the H6 spec for exactly this reason.)
3. **The adjusted-vs-GAAP trap.** Press releases headline "adjusted" figures; XBRL carries what
   was filed. Reconcile both and label which one a claim uses.
4. **The unit/scale trap.** Billions vs trillions, ₩조 vs ₩억, per-share vs total, split
   adjustments. The S10 KOFIA build hit the same genre (the tmpV40 unit-divisor trap). Rule:
   re-derive, never transcribe — growth rates get computed from the raw series, not quoted.
5. **The timezone/date-stamp trap.** KST vs ET turns "the 8th" into "the 7th"; period-ending vs
   published-on. (The dashboard's S2′/S5 age-off-by-one nit is this trap in miniature.)
6. **The recycled-news trap.** Old facts resurface as new catalysts. A GDELT volume timeline
   answers "did coverage actually spike, and when" in one call — the event-shock classifier's
   "new fact or recycled?" question, answerable today.
7. **The survivorship/lookahead trap.** Backtest-flavored claims in articles ("this signal
   returned X%") almost never state their universe or point-in-time hygiene. Treat as Tier-3
   narrative, never evidence.

Honest boundary: the ladder bounds **transcription error, not fraud**. Tier 0 tells you what was
*filed*, not what is *true* — Wirecard filed audited numbers. That risk is the analyst's, not
the pipeline's.

## Layer 1 — hand the agents what already exists (~3h, the single biggest win)

Nothing new gets fetched; the gap is that research agents can't *reach* the desk's own
instruments.

- **`.claude/skills/research-data/SKILL.md`** — a catalog skill: every callable data command in
  this repo and the engine, with exact command lines and output shapes. The enginev3 lake reads
  (S2′ options/IV archive, S4 short interest, S5 ETF AUM, S6 COT, S8 NAAIM, S10 KOFIA 신용융자,
  S3 pykrx investor-type flows), [`ffcal.py`](../../tools/calendar/README.md) `brief`/`events`,
  and `position_size.py`. Any subagent that loads the skill inherits the whole sensor suite.
- **A one-shot lake read CLI** if the engine doesn't already expose one (`enginev3 query
  <source> --last N` or a DuckDB view over the store) — agents should speak one command, never
  re-scrape their own data.
- **The calendar rule:** dates come from ffcal, never from web memory. Two of the Jul-6 kills
  (ISM date, tariff date) were calendar facts a local `ffcal.py brief` would have settled.

## Layer 2 — Tier-0/1 fetchers that don't exist yet (~10-12h total)

Each is a small CLI under `tools/` per the [library charter](../../tools/README.md)
(stdlib-first, files-as-database, ASCII-safe output, store/ committed).

- **EDGAR CLI (~4h).** The highest-value fetcher. SEC's free JSON APIs need only a User-Agent
  header (~10 req/s): `data.sec.gov/api/xbrl/companyfacts/` returns **every XBRL line item a
  company ever filed** (the full revenue/margin/capex history as filed — trend computation
  without a single web page); `data.sec.gov/submissions/` lists filings same-day;
  `efts.sec.gov` full-text-searches all filings since 2001; 13F holdings and Form 4 insider
  trades are structured. This also pre-builds the plumbing the present-state stack's Form-4
  filter (tool 6) and expectations tracker (tool 7) need. Python `edgartools` wraps all of it
  if a dependency is acceptable; raw REST + stdlib works too.
- **DART CLI (~3h).** OpenDART (free API key) serves Korean filings as filed: the
  영업(잠정)실적 disclosures (today's Samsung prelim is one), quarterly/annual statements,
  major-holder changes. This is the Tier-0 source for the book's core names — a Samsung number
  should never be cited from a news wire when the 공시 is a free API call. Overlaps the
  engine's deferred S11 (KRX events) hunt — likely the same endpoint family, so hours may
  amortize.
- **Macro CLI (~3h).** One `tools/macro/` fetcher covering: FRED **plus ALFRED vintages** (the
  honesty feature — "what did the market know on date X"); ECOS (Bank of Korea, free key) for
  Korean macro and BOK decisions; TreasuryDirect auction results (bid-to-cover, high yield,
  tail — the Jul-6 brief's auction-mechanics gap is literally one API call); the BLS release
  calendar for exact print dates/times. DBnomics (free, no key, 80+ official providers behind
  one REST shape) as the fallback aggregator.
- **Transcripts/IR (~2h + the honest limit).** Prepared remarks and guidance tables are free:
  8-K exhibits via the EDGAR CLI + IR PDFs through the existing `pdf_extract.py`. **Full Q&A
  transcripts are the one genuinely paid item** — FMP's starter tier (~$22–30/mo, verify
  current terms) or scraping Motley Fool (fragile, ToS-gray). The hyperscaler-capex tracker
  (stack tool 9) needs transcripts anyway, so one subscription serves both when that build
  slot arrives.
- **Attention/news-volume (~2h, optional).** GDELT DOC 2.0 (free, no key): coverage volume and
  tone timelines per entity — the recycled-news detector. Wikipedia pageviews REST (free,
  stable) as a retail-attention proxy. Google Trends via pytrends only with a fragility flag
  (unofficial, rate-limited, values are relative per query window — a classic trap-4 source).

## Layer 3 — the procedure as skills (what makes N agents repeatably accurate)

Tools give access; **skills give discipline**. A `.claude/skills/` file is versioned procedure —
the mechanism that makes a fleet of disposable subagents behave like one trained analyst. This
repo has none yet; these two are the highest-leverage first entries. *(Update 2026-07-07: the
buildable blueprint for this layer is now filed —
[the market-research skill design](../designs/market-research-skill.md), which absorbs the
`verify-numbers` sketch below as its skeptic role.)*

- **`market-research` skill.** Encodes the house method as instructions any agent inherits:
  the source-tier ladder and the ◐ rule; as-of stamps on every claim; derived numbers computed
  from raw series, never transcribed; the ✅/◐/⚠️ confidence markers; a **killed-claims
  section** in every brief (the Jul-6 convention, now standard — so downstream agents don't
  re-inherit dead facts); dates from ffcal; the post-mortem stub. Point the deep-research
  workflow's agents at this skill and the whole 104-agent fan-out inherits it at once.
- **`verify-numbers` pass.** Before a market-note files, one verifier agent re-derives the 3–5
  load-bearing numbers from Tier-0/1 APIs and attaches a pass/fail line per number. This is the
  deep-research harness's adversarial-verify pattern extended from web claims to data claims;
  output shape already exists as the wiki's `audit` type. Cost: one agent, minutes.
- **CLI over MCP, deliberately.** MCP servers for finance data exist (Polygon and Alpha Vantage
  official, OpenBB's server with its whole aggregator behind it) and are the fast-breadth
  option. But this repo's doctrine — stdlib-first, files-as-database, git-audited store,
  cp949-safe — favors small CLIs documented in a skill: versioned with the repo, no running
  processes, callable by any agent with Bash, outputs committed as the audit trail. Revisit
  only if fetcher maintenance starts eating real hours.

## Layer 4 — where money buys accuracy (gated, not Day-1)

| Feed | ~Cost | What it closes | Gate |
|---|---|---|---|
| FMP starter | $22–30/mo | Q&A transcripts + consensus estimates depth (trap 2) | Expectations tracker (stack 7) goes live |
| Alpaca $99 tier | already planned | OPRA options as-of snapshots for implied-move claims | Unchanged from present-state stack |
| Norgate | ~$30/mo | Survivorship-free US EOD universe | First filed claim that rests on a backtest |
| Databento | pay-as-you-go | Clean tick/intraday for adjudicating minute-level claims | Replay-gym episode needs it |

What stays unbuyable is unchanged from [the elite-traders map](what-elite-traders-actually-know.md):
IBES-grade revision history, dealer/internalizer flow, expert networks. The research layer's
answer is the same as the desk's — at days-to-weeks horizon, cite what's public, mark what
isn't, and never dress a Tier-3 number as a fact.

## Build order and kill criteria

Total ~8–11h of engine-block time; the sequence front-loads the free wins.

- **Day 1 (~3h):** `research-data` skill cataloging the existing lake + ffcal, and EDGAR CLI v0
  (companyfacts + submissions + full-text). Live rep: re-derive three numbers in the current
  week's market-note from Tier-0 and mark the diff.
- **Day 2 (~3h):** DART CLI + macro CLI (FRED/ALFRED, ECOS, TreasuryDirect). Live rep: the next
  BOK/auction day's call sheet cites an API pull, not a headline.
- **Day 3 (~2h):** `market-research` + `verify-numbers` skills; wire into the next week-ahead
  run.
- **Stop there.** Layer-4 subscriptions stay behind their gates; GDELT/pageviews only if a
  research question actually asks an attention question.

**Kill criteria (rule zero, research flavor):** each fetcher is cited in a *filed* market-note
within 7 days of build or it's cut; the skills must measurably cut the killed-claims and
gap-section counts across the next two deep-research runs versus the Jul-6 baseline (4 killed,
8 declared gaps) or they get rewritten.

## Honest limits

- **Primary sources bound transcription error, not truth.** Filings can lie; consensus can be
  stale even when named; the ladder makes errors *attributable*, which is the realistic goal.
- **This layer is deliberately not real-time.** Live sensing is the engine's job; research
  agents consume as-of snapshots. Mixing the two re-creates the platform trap.
- **Free-tier estimate data stays thin.** Until the FMP gate opens, "vs consensus" claims carry
  ◐ by construction. That is a feature (visible uncertainty), not a bug.
- **Scrapers rot silently.** pytrends and any HTML scrape need the engine's staleness-SLA
  pattern (freshness stamps + loud failure), or they become trap sources themselves.

## Relationships

- Sibling of [the present-state stack](present-state-stack.md) — same doctrine (rule zero,
  files-as-database, honest unbuyables), different consumer: research agents, not the morning
  brief. Tools 6/7/9 there share plumbing with the EDGAR/DART/transcript fetchers here.
- Exposes [Engine v3](engine-v3/index.md)'s lake to the research layer; the DART CLI likely
  subsumes the deferred S11 hunt.
- Enforces [the forced-flow calendar](../designs/forced-flow-calendar.md) as the single date
  source for research agents.
- Proof case and baseline: [week-ahead 2026-07-06](../market-research/weekly/week-ahead-2026-07-06.md)
  (4 killed claims, 8 declared gaps — the number the skills must beat).
- Moves the [verification-flags](../verification-flags-2026-06-22.md) audit discipline to
  ingestion time.
- Fetcher design pages, when build slots arrive, go to [Designs](../designs/index.md).

## Open questions

- Does OpenDART expose 영업(잠정)실적 disclosures via API same-day (prelims are the
  time-critical case), or only via KIND scraping?
- Which consensus source does the desk standardize on for "vs consensus" claims at free tier —
  Finnhub-free (current S7′), or scrape-and-name per note?
- Should the deep-research workflow get a finance-tuned variant with the `market-research`
  skill baked into every fan-out agent's prompt, rather than relying on skill discovery?
- Do the EDGAR/DART CLIs live in this repo's `tools/` or in enginev3 as feeders? (Lean: fetchers
  that only research agents use live here; anything the nightly DAG consumes lives in the
  engine.)
