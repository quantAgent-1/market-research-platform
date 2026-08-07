# Markets Research Lab

**Hyunsuk Yang** · Systematic trading · Research engineering · Semiconductor / AI markets · AI-agent research ops

Public **working system**: a structured knowledge base, research tooling in Python, and a documented workflow for using AI agents without treating them as a source of truth.

| | |
|---|---|
| **Looking for** | Quant research, research engineering / market-data tooling, or markets roles where **process quality + build skill** both matter |
| **Not claiming** | Audited trading performance, live desk P&L, or “alpha for sale” |
| **Language** | English (research writing) · Korean market microstructure literacy (KRX / flow data) |

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](alpaca-data/)

---

## 1. Interests (what I spend depth on)

I care about problems where **naive prediction fails** and **structure, costs, and verification** decide outcomes.

### A. How edges are found, killed, and sized

- Statistical existence vs **tradeability after costs**
- Multiple testing, trial budgets, pre-registered kill criteria
- Naming the **payer** (mistake / service / constraint / premium) before naming the signal

*Examples in-repo:*  
[How strategies are discovered & validated](wiki/synthesis/how-strategies-are-discovered-and-validated.md) ·  
[Is quant research a science?](wiki/synthesis/is-quant-research-a-science.md) ·  
[Who pays you](wiki/shared/concepts/who-pays-you.md) ·  
[Alpha map](wiki/synthesis/alpha-map.md)

### B. Market structure and forced flow

- Cascades, margin / session clocks, leveraged-ETF rebalance math
- Cohort flow (especially Asia-session structure) as *condition recognition*, not crystal-ball forecasting
- Calendars of who is **forced** to trade

*Examples in-repo:*  
[Forced-flow calendar (tool)](tools/calendar/README.md) ·  
[Semis flow map (tool)](tools/flowmap/README.md) ·  
[Liquidity cascades](wiki/shared/concepts/liquidity-cascades-and-v-reversals.md) ·  
[KRX session clocks](wiki/shared/concepts/krx-session-clocks-and-forced-liquidation.md)

### C. Semiconductor / AI industry mechanics

- Memory / HBM cycle, hyperscaler capex, financing topology
- Second-derivative cycle logic (equities can top while earnings rise)
- Reverse-DCF style “what does price already assume?”

*Examples in-repo:*  
[AI capex financing](wiki/shared/concepts/ai-capex-war-financing.md) ·  
[Semis / AI state of play](wiki/market-research/semis-ai-state-of-play-2026-07-09.md) ·  
[Valuation complex — muval](tools/muval/README.md)

### D. Making research compound (with agents)

- Persistent knowledge base instead of one-off chat answers
- Agent fleets for breadth; **human + adversarial verify** for load-bearing facts
- Tools agents can call (data lake, calendars, models) instead of raw web search alone

*Examples in-repo:*  
§3 below · [Research accuracy stack](wiki/synthesis/research-accuracy-stack.md) · [LLM-wiki pattern](meta/llm-wiki.md)

---

## 2. Skills (what I can do — with evidence)

Recruiters: this is not a keyword list. Each row has a place to click.

| Skill | What it means in practice | Evidence |
|-------|---------------------------|----------|
| **Validation literacy** | Separate replication from implementable edge; respect trial counts and costs | [Discovery & validation](wiki/synthesis/how-strategies-are-discovered-and-validated.md), [retail-capital edge map](wiki/synthesis/retail-capital-edge-map.md) |
| **Mechanism-level strategy design** | Spec signals with payer, barrier, constants, and kill tests *before* mining | [Korea flow sleeve](wiki/systematic-trading/strategies/korea-flow-sleeve.md), [edge taxonomy](wiki/synthesis/techniques-of-winning-trades.md) |
| **Financial modeling** | Scenario / reverse DCF, assumption registries, Monte Carlo, event-move framing | [muval](tools/muval/README.md), [design](wiki/designs/valuation-complex.md) |
| **Research engineering** | Python packages, CLIs, caching, selftests, Parquet/DuckDB-shaped data work | [alpaca-data](alpaca-data/README.md), `tools/*` |
| **Market-structure tooling** | Forced-flow calendars, flow-read dashboards, design docs with kill criteria | [ffcal](tools/calendar/README.md), [flowmap](tools/flowmap/README.md), [designs](wiki/designs/index.md) |
| **Sector research (semis/AI)** | Tripwires, financing, cycle phase — not tip sheets | [market-research](wiki/market-research/index.md) |
| **Risk / process design** | Written constitutions, tripwire exits, practice vs thesis firewall (templates) | [risk constitution](wiki/systematic-trading/checklists/trading-risk-constitution.md), [tripwire exits](wiki/systematic-trading/checklists/tripwire-exit-execution.md) |
| **AI-agent research ops** | Schema-driven wiki maintenance, multi-agent research with verification gates | §3 · [CLAUDE.md](CLAUDE.md) · [accuracy stack](wiki/synthesis/research-accuracy-stack.md) |

**Stack (typical):** Python 3.11+ · pandas / scientific stack as needed · Parquet + DuckDB · REST/WebSocket market data · markdown knowledge systems · multi-agent coding/research assistants (Claude / similar) under written procedures.

---

## 3. How I work with AI agents

This is the part that is easy to fake in a sentence and hard to run for months. Here is the actual system.

### The principle

> **Agents expand search and drafting bandwidth.  
> They do not own truth.**  
> Load-bearing numbers need primary sources or independent verification. Chat is ephemeral; the wiki and tools are the durable product.

I do **not** treat “the model said so” as research. I treat agents as **junior analysts + junior engineers** with a strict filing and verification protocol.

### Architecture (three layers)

```text
┌─────────────────────────────────────────────────────────────┐
│  HUMAN                                                      │
│  · sets questions & priorities                              │
│  · owns kill criteria and final judgment                    │
│  · supplies sources; never lets agents invent “raw” truth   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT LAYER (breadth)                                      │
│  · read / summarize / cross-link / draft code & designs     │
│  · multi-agent research runs (search → extract → verify)    │
│  · constrained by schema (CLAUDE.md) and tool contracts     │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│  WIKI (compiled knowledge)│  │  TOOLS (executable research) │
│  wiki/ — interlinked md   │  │  muval · flowmap · ffcal     │
│  sources/ briefs          │  │  alpaca-data lake client     │
│  synthesis / designs      │  │  assumptions on disk         │
└──────────────────────────┘  └──────────────────────────────┘
```

- **Raw sources** (private): papers, filings, deep-research outputs — immutable when held; **not redistributed** in this public repo.  
- **Wiki** (this repo): LLM-maintained, human-directed knowledge — concepts, strategies, market notes, designs.  
- **Tools** (this repo): Python systems agents and I both use so answers are computed, not only narrated.

Pattern write-up: [meta/llm-wiki.md](meta/llm-wiki.md). Operating schema: [CLAUDE.md](CLAUDE.md).

### Workflow A — Ingest (source → knowledge)

```text
source lands  →  agent reads  →  discuss emphasis with me
      →  source summary page (wiki/sources/)
      →  update concept / market / synthesis pages
      →  cross-links + index
      →  contradictions flagged, not silently overwritten
```

One serious source typically touches many pages. The point is **compilation**, not chat that evaporates.

### Workflow B — Query (question → answer → file-back)

```text
question  →  agent searches wiki first (compounding context)
      →  answers at practitioner depth when the topic warrants it
      →  surfaces adjacent questions and gaps
      →  durable answers get filed back into wiki/synthesis or domains
```

So exploration **compounds**. The next session does not start from zero.

### Workflow C — Deep research with adversarial verification

For high-stakes questions I run multi-agent research, then **do not trust the first synthesis**:

```text
decompose question
    → parallel fetch / extract (agents)
    → adversarial verify claims (fresh context; attack numbers & dates)
    → grade: confirmed / refuted / unresolved
    → human reads the ledger; only then file a brief + fold into wiki
```

Doctrine for numbers: **source-tier ladder** (filer / venue / vendor / journalism).  
Web search = discovery and narrative, **not** the sole citation for a load-bearing figure.  
Full write-up: [Research accuracy stack](wiki/synthesis/research-accuracy-stack.md).

Examples of filed research briefs: [`wiki/sources/`](wiki/sources/index.md).

### Workflow D — Build tools (design → code → kill criteria)

```text
mission + doctrine  →  design page (wiki/designs/) with kill criteria
    →  implement under tools/ or alpaca-data/
    →  assumptions in config (e.g. assumptions.toml), not magic constants
    →  selftest / README; mark build: planned | building | live
```

Agents draft and refactor; I own architecture choices and what “done” means.  
Examples: [valuation complex design](wiki/designs/valuation-complex.md) → [muval](tools/muval/README.md).

### What I do myself vs what agents do

| Human (me) | Agents |
|------------|--------|
| Problem selection and research agenda | Breadth search, first drafts, cross-linking |
| Accept / reject kill criteria | Scaffold code, tests, docs |
| Final call on contradictions and risk | Multi-file wiki maintenance under schema |
| “Would I stake a decision on this number?” | Format, indexes, mechanical consistency |
| Primary-source retrieval decisions | Parallel extraction and adversarial passes |

### What I refuse to outsource to agents

- Inventing market data or “remembered” filings  
- Shipping a number into a conclusion without a tiered source or recompute  
- Silent overwrite of a prior claim when a new source conflicts  
- Performance or “guaranteed edge” marketing copy  

---

## 4. If you have five minutes

| Time | Open |
|-----:|------|
| 1 min | This page (§1–§3) |
| 2 min | One judgment sample: [Discovery & validation](wiki/synthesis/how-strategies-are-discovered-and-validated.md) |
| 2 min | One build sample: [muval README](tools/muval/README.md) **or** [alpaca-data](alpaca-data/README.md) |

Deeper map (optional): [SHOWCASE.md](SHOWCASE.md) · full catalog [wiki/index.md](wiki/index.md).

---

## 5. Repository map

```text
.
├── README.md                 ← landing page (you are here)
├── SHOWCASE.md               ← optional skills ↔ artifacts matrix
├── CLAUDE.md                 ← agent schema: how the wiki is maintained
├── wiki/                     ← knowledge base (OKF-style markdown)
│   ├── synthesis/            ← flagship overviews
│   ├── systematic-trading/   ← strategies, models, checklists
│   ├── market-research/      ← semis / AI / memory (time-stamped)
│   ├── shared/               ← cross-cutting concepts
│   ├── designs/              ← tool blueprints + kill criteria
│   └── sources/              ← research-brief summaries
├── tools/                    ← runnable research tools
│   ├── muval/                ← MU / NVDA / AMD valuation complex
│   ├── flowmap/              ← semis institutional-flow read
│   └── calendar/             ← forced-flow calendar
├── alpaca-data/              ← market-data client (code only; no secrets)
└── meta/                     ← LLM-wiki pattern notes
```

### Quick start (tools)

```powershell
python tools/muval/muval.py selftest
python tools/calendar/ffcal.py --help
python tools/flowmap/flowmap.py --help

cd alpaca-data
python -m pip install -e .
# API keys only in local .env — never commit
```

---

## 6. Honest limits

- **Solo portfolio**, not a production trading firm stack.  
- Some designs are deeper than the shipped slice; statuses are marked on design pages.  
- Market notes are **research**, time-stamped, and can go stale.  
- **No performance claims** from this repository.  
- Copyrighted primary PDFs are **not** redistributed; summaries point to public references.

**Not investment advice.** Nothing here is a recommendation to buy, sell, or hold any security.

---

## 7. License & contact

**License:** [MIT](LICENSE) for original code and markdown © 2026 Hyunsuk Yang.

**Author:** Hyunsuk Yang  

Open to conversations on quant research, research engineering, and markets-technology roles.  
If you are hiring: the highest signal path is **this README → one synthesis page → one tool**. I am happy to walk through the agent workflow or any single artifact on a short call.
