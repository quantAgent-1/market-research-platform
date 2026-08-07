---
type: design
title: "Market-Research Skill — the operating procedure that makes agent research primary-sourced, adversarial, and gradable"
description: Buildable blueprint for .claude/skills/market-research/ — a six-phase procedure, five role cards with hard contracts (data enters only through pullers, skeptic pass mandatory), six question-type playbooks, one output contract, and a grading loop benchmarked against the Jul-6 deep-research baseline.
tags: [systematic-trading, tooling, agents, research-process, market-research]
timestamp: 2026-07-07T00:00:00Z
status: active
build: planned
sources: []
---

# Market-Research Skill (design)

The [research accuracy stack](../synthesis/research-accuracy-stack.md) named procedure-as-skills
its Layer 3; this page is the buildable blueprint for the centerpiece: **one skill that any agent
fleet loads before doing market research for this wiki.** The design goal, stated plainly: an
Opus subagent that has never seen this repo should be able to load the skill, receive a research
question, and produce a market-note that survives the desk's own audit — because the skill, not
the agent's judgment, carries the source discipline, the analytical frames, the output shape,
and the verification step.

## 1. Mission & doctrine compliance

- **What:** `.claude/skills/market-research/` — a SKILL.md plus reference files, versioned in
  this repo, discoverable by the lead session and injectable into subagent prompts.
- **Why a skill and not a wiki page:** wiki pages are knowledge for the human-in-the-loop;
  a skill is *procedure that executes* — the mechanism that makes N disposable subagents behave
  like one trained analyst, run after run. The wiki stays the source of truth; the skill is the
  operational distillation with links back.
- **Rule zero:** the skill is exercised on a real, filed market-note within 7 days of build
  start — the calendar supplies the reps (week-ahead Mon Jul-13; TSMC preview Jul-16).
- **Kill criteria:** pre-registered in §11. Benchmark = the Jul-6 deep-research run
  (4 killed claims, 8 declared gaps, 0 numbers re-derived from Tier-0).
- **Replaces/absorbs:** the house-style conventions currently scattered across individual
  market-notes (as-of banners, ✅/◐/⚠️, killed-claims sections) become one written contract.

## 2. Package architecture

```
.claude/skills/market-research/
├── SKILL.md                 # the lean core (~300 lines): trigger, phases, role cards,
│                            #   accuracy contract, output contract — self-contained
├── references/
│   ├── source-ladder.md     # tier table + per-source endpoints/commands + the 7 traps,
│   │                        #   in operational form (checkable, not essayistic)
│   ├── frames.md            # the six analytical frames as run-the-list checklists,
│   │                        #   each linking to its wiki source page
│   ├── playbooks.md         # the six question-type playbooks (§7)
│   └── templates.md         # market-note skeletons per question type
└── scripts/                 # empty at v0 — pullers hit raw endpoints; thin wrappers
                             #   land here only when the accuracy-stack CLIs get built
```

Progressive disclosure: SKILL.md alone is sufficient to run a degraded-but-honest pass;
references load on demand. **Self-containment rule:** SKILL.md defines every symbol it uses
(◐, tier numbers, pack, falsifier) — a subagent must never need conversation context to
comply.

## 3. Core logic — the six-phase procedure

**Phase 0 — Scope & classify.** Restate the question verbatim; classify into one of the six
playbook types (§7); stamp the as-of (date *and* timezone — KST vs ET is trap #5); pull the
matching template. If the question is forward-looking, note now that a pre-registered scenario
table (Phase 4) is mandatory.

**Phase 1 — Own instruments first.** Before any web call: `ffcal.py brief` for the event/date
skeleton (dates never come from web memory — two of the four Jul-6 kills were calendar facts);
the enginev3 lake for positioning/vol/flow state; the wiki indexes for priors (existing pages
are sources, cited like any other — and flagged as *priors*, not independent evidence).

**Phase 2 — Data pack assembly (pullers).** Mechanical agents run the playbook's pull list and
return **the data pack**: a table where every row is `claim · value · as-of · source ·
tier · fetch method`. Pullers do not interpret. This is the load-bearing anti-hallucination
contract: **a number exists in the research only if it entered through the pack.** An analyst
needing a number not in the pack requests another pull; it never types one from memory.

**Phase 3 — Narrative pack assembly (scouts).** Web search/fetch agents sweep what happened
and what is being said — each claim tagged Tier-3 with URL and publication date. Narrative is
a *positioning datum* (what the crowd believes), never a source of numbers. Scouts also do the
recycled-news check (trap #6): for each catalyst claim, when did coverage actually start?

**Phase 4 — Analysis (analyst, Opus).** Takes both packs plus wiki priors, runs the frames
checklist (§6) — only the frames the playbook marks relevant — and produces: the verdict, the
frame-by-frame findings, and for forward-looking questions the **pre-registered scenario
table**: exhaustive numeric buckets, probabilities summing to 1, one falsifier/tell per row,
timestamped *before* the skeptic pass. Buckets must be machine-gradable ("gap +3% to +6%:
p=0.30"), never vibes ("could bounce").

**Phase 5 — Adversarial verification (skeptic, Opus, fresh context).** A separate agent that
receives packs + draft and **must attack** (a pass with zero findings on a first draft is
itself a red flag). Mandate, in order: (a) re-derive the 3–5 most load-bearing numbers from
Tier-0/1 independently; (b) date-check every catalyst (recycled?); (c) the counterparty test —
who is on the other side of this conclusion and why are they wrong? if unnamed, the edge is
narrative; (d) the priced-check — what do consensus/implied move already embed?; (e) the
anchoring check — does the conclusion merely restate wiki priors? name what *independent*
evidence supports it; (f) the counterexample search — name one historical episode where this
exact setup failed (the Aug-5-2024 discipline). Verdict per claim: CONFIRMED / CORRECTED /
KILLED / UNVERIFIABLE→◐.

**Phase 6 — File & wire (synthesizer = the lead).** Merge into the output contract (§8);
killed claims and declared gaps get their sections even when empty ("none" is information);
file to the right `market-research/` subfolder; wire indexes, log, timeline per CLAUDE.md;
append the run's scorecard row (§11).

## 4. Role cards (the subagent fleet)

| Role | Model | Tools | Input | Output | Forbidden |
|---|---|---|---|---|---|
| **Puller** | Haiku/Sonnet | Bash, Read | pull list from playbook | data-pack rows (JSON/table, one row per number) | interpretation; omitting as-of/source |
| **Scout** | Sonnet | WebSearch, WebFetch | question + entities | narrative-pack claims (`claim · url · pub-date · tier-3`) | stating any number as fact; un-dated claims |
| **Analyst** | **Opus** | Read (packs only) | data pack + narrative pack + wiki priors | frame findings + verdict + scenario table | introducing numbers not in the pack; skipping pre-registration |
| **Skeptic** | **Opus** (fresh context) | Bash, WebFetch, Read | packs + draft | per-claim verdicts + re-derived numbers + attack findings | rubber-stamping; sharing analyst's context |
| **Synthesizer** | lead session | Write, Edit | everything above | the filed page per contract + scorecard row | new claims at synthesis time |

Independence note: the skeptic gets a *fresh* context (packs + draft only, not the analyst's
reasoning) — redundant reasoning is worthless; independent re-derivation is the product.

## 5. The accuracy contract (ten hard rules, testable per note)

1. A load-bearing number is cited Tier 0/1, **or** two independent Tier 2/3 sources **and ◐**.
2. Dates come from ffcal; a date ffcal lacks gets added to `overrides.toml`, not free-typed.
3. Every number carries as-of + source inline (in the data-pack table, not a footnote).
4. Derived figures (growth rates, spreads, multiples) are computed from raw series in the
   pack — never transcribed from an article.
5. "Vs consensus" claims name the consensus source and its as-of date, or carry ◐.
6. Every catalyst claim passes the new-vs-recycled check with a coverage start date.
7. Forward-looking notes carry a pre-registered scenario table: exhaustive numeric buckets,
   Σp = 1, a falsifier per row, timestamped before the skeptic pass.
8. Killed-claims and declared-gaps sections are mandatory, even when empty.
9. The skeptic pass runs before filing; ≥3 numbers re-derived from Tier-0/1; findings are
   incorporated, not appended.
10. Every note ends with a post-mortem stub naming its grade date and what gets graded.

## 6. The frames (references/frames.md — the wiki's doctrine as a checklist)

Run only the rows the playbook marks; each links to its source page (wiki = truth, skill =
distillation):

| # | Frame | The question, operationally | Source page |
|---|---|---|---|
| F1 | **What's priced?** | consensus + whisper + straddle-implied move + price-vs-target-wall gap → state *the bar*, not the outcome | [who sets price](../shared/concepts/who-sets-price.md) |
| F2 | **Who's positioned how?** | lake gauges (CROWD state, SI, COT, NAAIM, KOFIA fuel z, cohort flows) → which side is crowded, what's the asymmetry | [H6 module](../synthesis/engine-v3/h6-crowding-defector-module.md) |
| F3 | **Who's forced, when?** | ffcal window scan: opex/만기/rebalances/blackout bands/lockups/반대매매 state inside the question's horizon | [forced-flow calendar](forced-flow-calendar.md) · [KRX clocks](../shared/concepts/krx-session-clocks-and-forced-liquidation.md) |
| F4 | **Information or flow?** | breadth test: name vs true peers vs sector vs tape; skew steepening beyond the normal ramp? → idiosyncratic vs shared | [informed vs uninformed flow](../shared/concepts/informed-vs-uninformed-flow.md) |
| F5 | **Where's the cycle clock?** (cyclicals) | second-derivative state (increments peaked?), spot-vs-contract, the 5-phase checklist score | [second-derivative cycle trading](../shared/concepts/second-derivative-cycle-trading.md) |
| F6 | **Who pays you?** | name the counterparty of the conclusion and why they transact anyway; unnamed → narrative, not edge | [who pays you](../shared/concepts/who-pays-you.md) · [edge taxonomy](../synthesis/techniques-of-winning-trades.md) |

## 7. The six playbooks (references/playbooks.md)

Each playbook = required pulls · required frames · template deltas · grading hook.

1. **Earnings/event preview** (the call-sheet feeder). Pulls: consensus (named + ◐), implied
   move from the S2′ archive, positioning gauges, filed-history trend (EDGAR/DART), ffcal
   window. Frames F1–F4 (+F5 if cyclical). Output adds the 3-question card and the
   pre-registered reaction distribution. Grade: at print +1 day.
2. **Event postmortem.** Pulls: actuals as filed (Tier-0), the pre-registered table from the
   preview note. Frames F3/F4 for attribution (who was forced/who paid). Output = grade of
   each bucket + lessons + prior updates. Grade: immediate (it *is* the grading).
3. **Week-ahead brief** (the Jul-6 format, now instrumented). Pulls: ffcal 10-day, full lake
   sweep (the vol/positioning section can never again be "a gap"), macro calendar with exact
   date/time/timezone per print. Frames F1–F3. Grade: Friday close vs the scenario rows.
4. **Regime read.** Pulls: lake gauges' 60-session history, cycle variables (spot-vs-contract,
   increments), cohort flows. Frames F2/F3/F5 → the three-axis composite (fundamental clock ×
   positioning × macro). Grade: at the next tripwire flip, either direction.
5. **Thesis/claim check** (the viral-post pattern). Decompose to checkable claims; every claim
   gets a pack row + a verdict; then F6 — if the thesis is right, who loses, and is that
   already priced? Grade: the thesis's own nearest falsifiable date.
6. **Name deep-dive.** Pulls: full XBRL/DART filed history, holders/insiders (13F/Form-4 or
   지분공시), positioning, expectations. Frames F1/F2/F5/F6. Grade: next print.

## 8. Output contract (references/templates.md)

One skeleton, per-playbook deltas. Frontmatter: `type: market-note`, as-of in the title,
`status: active`, sources listing packs' provenance. Body, in order: **as-of banner**
(date·timezone·question verbatim·one-sentence verdict with confidence) → **the data pack
table** (every load-bearing number with tier + as-of) → **frame findings** (only the frames
run) → **scenario table** (pre-registered stamp visible) → **levels & tells** → **killed
claims** → **declared gaps** (each gap names the Tier-0 source that *would* close it) →
**post-mortem stub** (grade date + what gets graded) → **sources**. Confidence marks: ✅
Tier-0/1-verified · ◐ single-source or Tier-2/3 · ⚠️ contested/stale. House prose rule:
full sentences, reader-friendly, no headers-for-their-own-sake.

## 9. v0 pull inventory (works today, before the accuracy-stack CLIs)

| Source | v0 method | Covers |
|---|---|---|
| Event calendar | `python tools/calendar/ffcal.py brief` (v0.2 live) | F3, all dates |
| Engine lake | read `../enginev3/data/{options,short_interest,etf_flows,cot,surveys,kofia_credit,krx_flows,ohlcv,estimates}` directly (files-as-database; `uv run enginev3 report` refreshes) | F2 gauges, IV/implied move, fuel |
| US filings | `data.sec.gov` JSON (companyfacts/submissions) via python urllib with UA header — works today without the CLI | filed numbers, 8-K, Form 4 |
| KR filings | KIND/DART via WebFetch at v0 (OpenDART key + CLI = the upgrade) | 공시, 잠정실적 |
| KR flows | pykrx (already an engine dependency) | cohort flows by name |
| Macro | FRED/ECOS need free keys (2-min signups) — until then, declared gaps | vintages, BOK |
| Consensus | Finnhub-free (key exists in engine config) — always ◐ | F1's bar |
| Narrative | WebSearch/WebFetch (scouts only) | Tier-3 |

The [research-data catalog skill](../synthesis/research-accuracy-stack.md) (Layer 1) pins exact
commands as they harden; this table is the honest v0.

## 10. Orchestration patterns (how the lead runs it)

- **Small question (playbooks 1/2/5/6):** lead loads the skill, spawns 1–2 pullers + 1 scout in
  parallel, one Opus analyst, one Opus skeptic, synthesizes. ~5–8 agents.
- **Week-ahead scale (playbook 3):** the deep-research harness with this skill's role cards and
  accuracy contract injected into every fan-out prompt — **inline the contract sections into
  subagent prompts rather than relying on skill auto-discovery** (reliability over elegance;
  a subagent that never loads the skill silently reverts to web-search habits).
- **Phase barriers that matter:** packs complete before analyst starts; scenario table stamped
  before skeptic starts; skeptic returns before any filing. Everything else runs parallel.
- **Cost sanity:** pullers/scouts are cheap models; Opus spends only where judgment lives
  (analyst, skeptic). A full week-ahead should cost a fraction of the Jul-6 run's 104 agents
  — the lake replaces a whole fan-out wing.

## 11. Grading loop & kill criteria (pre-registered)

Every run appends one row to `store/runs.csv` inside the skill dir (files-as-database):
`date · playbook · killed-claims · declared-gaps · numbers-rederived · skeptic-findings ·
post-event-grade (when due)`.

- **Beat the baseline:** across the first two graded runs (target: week-ahead Jul-13, TSMC
  preview Jul-16), killed-claims and declared-gaps must land **at or below** the Jul-6
  baseline (4 killed / 8 gaps) *while* numbers-rederived goes from 0 to ≥3 per note — fewer
  errors while checking harder, not fewer errors by checking less.
- **Skeptic liveness:** if the skeptic reports zero findings on two consecutive first drafts
  *and* post-event grading later finds errors, the skeptic prompt is broken → rewrite before
  the next run.
- **Rule zero:** not exercised on a filed note within 7 days of build start → cut.
- **Scenario calibration** accrues to the desk's existing calls.csv/Brier machinery (stack
  tool 10), not to this skill — the skill's job is that gradable tables *exist*.

## 12. Build plan (~5h total)

- **Day 1 (~2.5–3h):** SKILL.md core (phases, role cards, accuracy contract, output contract,
  self-containment pass) + `source-ladder.md` + templates for playbooks 1 and 3 (the sprint's
  two live reps). Live rep booked: **Monday Jul-13 week-ahead**, run through the skill,
  scorecard row #1 vs the Jul-6 baseline.
- **Day 2 (~2h):** `frames.md` distillation (six checklists with wiki links) + playbooks
  2/4/5/6 + the skeptic prompt hardened (attack mandate + counterexample search) + `runs.csv`.
  Live rep #2: **TSMC preview Jul-16** (playbook 1, with the print itself as the grader).
- **Not in scope:** building the EDGAR/DART/macro CLIs (that's the accuracy stack's Layer 2,
  separately slotted); auto-triggering hooks; any real-time anything.

## 13. Honest limits

- **A skill bounds procedure, not intelligence.** It guarantees numbers have provenance, claims
  have dates, scenarios are gradable, and a skeptic ran — it cannot make the analysis *right*.
  Post-event grading is where right/wrong shows up, and that loop lives outside the skill.
- **Contracts hold only if the lead enforces sequencing.** Subagents follow their role cards
  well; the phase barriers (packs → analyst → stamp → skeptic → file) are the orchestrator's
  responsibility. The skill states them; it cannot execute them.
- **v0 data coverage is uneven:** FRED/ECOS keys don't exist yet, consensus is structurally ◐,
  DART is WebFetch-grade until the CLI. The declared-gaps section makes this visible instead
  of hidden — that's the design working, not failing.
- **Anchoring on wiki priors is a real risk** (the wiki is large and confident). The skeptic's
  anchoring check is the counter, and priors are labeled as priors in the packs.
- **Skill/wiki drift:** frames.md can drift from its source pages. Mitigation: every reference
  file opens with "the wiki page is truth; regenerate this distillation when the source page's
  timestamp is newer."

## 14. Relationships

- Operationalizes [the research accuracy stack](../synthesis/research-accuracy-stack.md)
  Layer 3 (and folds its `verify-numbers` sketch in as the skeptic role — one skill, not two).
- Consumes: [Engine v3](../synthesis/engine-v3/index.md)'s lake ·
  [the forced-flow calendar](forced-flow-calendar.md) (single date source) · the wiki's frame
  pages (§6 table).
- Feeds: every `market-research/` page type; the call-sheet ritual; calls.csv calibration.
- Baseline it must beat: [week-ahead 2026-07-06](../market-research/weekly/week-ahead-2026-07-06.md).

## 15. Open questions

- Auto-trigger wording: how aggressive should the SKILL.md description be about claiming
  general "research X" requests vs only explicit market-research asks?
- Does the deep-research harness get a persistent finance variant (role cards baked into the
  workflow script), or does the lead keep injecting per run?
- OpenDART key + FRED/ECOS keys: create at Day-1 build (10 minutes total) or defer to the
  accuracy-stack Layer-2 slot? (Lean: create at build — keys are free and unblock pullers.)
- Should postmortem notes (playbook 2) auto-diff the preview's scenario table, or stay
  hand-graded? (Lean: hand-graded until two reps show the shape is stable.)
