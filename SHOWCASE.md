# Showcase — extended skills ↔ artifacts map

**Author:** Hyunsuk Yang  

> **Recruiters / hiring managers:** start with the **Markets Research Lab** landing page **[README.md](README.md)**  
> (interests, skills, and **AI-agent workflow**). This file is an optional deeper matrix.

This is not a claim of trading performance. It is a map of **process quality, technical build skill, and domain judgment** under explicit honesty constraints.

---

## The hiring problem this repo solves

Recruiters and technical interviewers cannot easily tell “watched YouTube / ran tutorials” from “can do the job.” They look for short, checkable evidence of:

| Signal | What “good” looks like | Where to verify it here |
|--------|------------------------|-------------------------|
| **Epistemic honesty** | States limits, kills bad claims, separates existence from tradeability | [Strategy discovery & validation](wiki/synthesis/how-strategies-are-discovered-and-validated.md), [Is quant research a science?](wiki/synthesis/is-quant-research-a-science.md) |
| **Mechanism thinking** | Names *who pays* for an edge; not black-box “alpha” | [Edge taxonomy](wiki/synthesis/techniques-of-winning-trades.md), [Who pays you](wiki/shared/concepts/who-pays-you.md) |
| **Math → product** | Models become runnable tools with assumptions externalized | [muval](tools/muval/README.md) + [design](wiki/designs/valuation-complex.md) |
| **Market structure literacy** | Forced flow, cascades, cohort data, calendars | [flowmap](tools/flowmap/README.md), [ffcal](tools/calendar/README.md), KRX / LETF concepts |
| **Research ops / AI-native work** | Adversarial verification, primary-source discipline, knowledge systems | [Research accuracy stack](wiki/synthesis/research-accuracy-stack.md), deep-research briefs in `wiki/sources/` |
| **Engineering hygiene** | Packages, CLIs, caches, selftests, design kill criteria | `alpaca-data/`, tool READMEs, [designs index](wiki/designs/index.md) |
| **Sector depth (semis/AI)** | Capex, memory cycle, financing topology — not price-prediction cosplay | [AI capex financing](wiki/shared/concepts/ai-capex-war-financing.md), state-of-play market notes |

---

## Role tracks — pick the story that matches the job

### A. Quant researcher / systematic research associate

**Sell:** validation literacy + edge taxonomy + ability to pre-register kills.

**Lead with (in order):**
1. [How strategies are discovered and validated](wiki/synthesis/how-strategies-are-discovered-and-validated.md)  
2. [Is quant research a science?](wiki/synthesis/is-quant-research-a-science.md)  
3. [Alpha map](wiki/synthesis/alpha-map.md) + [Korea flow sleeve](wiki/systematic-trading/strategies/korea-flow-sleeve.md) (registration-style strategy spec)  
4. [Retail-capital edge map](wiki/synthesis/retail-capital-edge-map.md) (cost-first survey honesty)  
5. [Production model book (plain)](wiki/systematic-trading/models/production-model-book-plain.md)

**Interview line:**  
> “I treat published factors as statistically real and usually economically dead after costs. My work focuses on naming the payer, measuring multiple testing, and only promoting ideas that survive a pre-registered kill list.”

---

### B. Quant engineer / research engineer / data engineer (markets)

**Sell:** data pipelines, tooling that ships, design docs with failure modes.

**Lead with:**
1. [`alpaca-data/`](alpaca-data/README.md) — Parquet/DuckDB research lake client  
2. [`tools/muval/`](tools/muval/README.md) — multi-name valuation engine + selftest  
3. [`tools/flowmap/`](tools/flowmap/README.md) + [`tools/calendar/`](tools/calendar/README.md)  
4. Design specs: [valuation complex](wiki/designs/valuation-complex.md), [flow map](wiki/designs/semis-institutional-flow-map.md), [forced-flow calendar](wiki/designs/forced-flow-calendar.md)  
5. [Institution-grade solution sheet](wiki/synthesis/institution-grade-solution-sheet.md) (schemas, IC, DSR, TCA shape)

**Interview line:**  
> “I build research systems where assumptions live in config, data is cached and refreshable, and every tool has a written kill criterion. Design docs and code stay in the same repo so review is possible.”

---

### C. Markets / sector research (semis–AI) or research analyst track

**Sell:** primary-source discipline, cycle mechanics, financing topology, falsification tripwires.

**Lead with:**
1. [Semis/AI state of play](wiki/market-research/semis-ai-state-of-play-2026-07-09.md) + source brief  
2. [AI capex war financing](wiki/shared/concepts/ai-capex-war-financing.md)  
3. [Equity duration & narrative regimes](wiki/shared/concepts/equity-duration-and-narrative-regimes.md)  
4. [After the earnings game](wiki/synthesis/after-the-earnings-game.md)  
5. muval reverse-DCF framing ([valuation complex design](wiki/designs/valuation-complex.md))

**Interview line:**  
> “I separate level vs second derivative in cyclicals, fund the difference between a beat and a re-rate, and keep explicit tripwires so a narrative can’t silently replace evidence.”

---

### D. AI-native / applied LLM roles adjacent to finance

**Sell:** multi-agent research process, verification gates, knowledge OS (not “chatbot demos”).

**Lead with:**
1. [Research accuracy stack](wiki/synthesis/research-accuracy-stack.md)  
2. Source briefs with claim ledgers in `wiki/sources/`  
3. Wiki architecture ([CLAUDE.md](CLAUDE.md), [meta/llm-wiki.md](meta/llm-wiki.md))  
4. Designs that encode adversarial review (e.g. market-research skill design)

**Interview line:**  
> “I use agents for breadth and force verification for truth. Numbers only enter through pullers or primary sources; synthesis is graded against falsifiers.”

---

## Flagship “show the screen” demos

If you get a 10-minute share-screen slot, run or walk through:

| Minutes | Demo | What it proves |
|--------:|------|----------------|
| 0–2 | Open [README](README.md) → this file → one synthesis page | You can structure knowledge for other people |
| 2–5 | `muval` design + assumptions.toml philosophy | Modeling judgment + engineering |
| 5–7 | `flowmap` / `ffcal` mission (forced flow vs information) | Market structure, not TA cosplay |
| 7–10 | One killed claim from a deep-research brief | You will say “no” to bad evidence |

Commands (see tool READMEs for env details):

```powershell
python tools/muval/muval.py selftest
python tools/calendar/ffcal.py --help
python tools/flowmap/flowmap.py --help
```

---

## What *not* to sell

| Avoid | Why |
|-------|-----|
| “I built a profitable system / beat the market” | You have no audited track record in this public repo; overclaiming destroys trust |
| Raw wiki size (“167 pages”) | Volume ≠ skill; signal density does |
| “I use AI a lot” | Everyone does; sell **verification discipline** |
| Personal account P&L or live position stories | Private by design; not in this repo |

---

## One-paragraph bio (copy/paste variants)

**Short (LinkedIn / GitHub):**  
> Quant research portfolio: systematic trading methodology, semiconductor/AI market research, and Python research tooling (valuation, flow maps, forced-flow calendars, market-data lake). Emphasis on cost-aware validation, mechanism-level edges, and design docs that ship.

**Medium (cover email):**  
> I maintain a public quant research knowledge base and tool library. The work spans (1) how strategies are actually discovered and falsified in the literature, (2) production-shaped model documentation and risk process design, and (3) runnable tools for multi-name valuation, institutional-flow reading, and forced-flow calendars—focused on the AI/semiconductor complex. I’m looking for roles where research rigor and build skill both matter.

**Technical (referral to a quant):**  
> Public artifacts include adversarial literature synthesis on replication/tradeability, pre-registered strategy specs (e.g. Korea flow sleeve), and a MU/NVDA/AMD valuation stack with reverse DCF, Monte Carlo, and cross-name consistency. Happy to walk through any design kill criterion or selftest.

---

## Suggested application package

For each application, send **three links max**:

1. This repo README (or a single flagship synthesis page)  
2. One **code** artifact (muval *or* alpaca-data *or* flowmap)  
3. One **domain** artifact matching the team (semis note *or* strategy discovery *or* model book)

Plus one sentence on **why those three** match *their* desk.

---

## Honest limits (say this out loud in interviews)

- This is a **solo research & tooling portfolio**, not a live production trading firm stack.  
- Some designs are deeper than the shipped vertical slice; designs mark `build: planned | building | live` honestly.  
- Sector notes are **time-stamped research**, not predictions you should trade.  
- No performance claims are made from this repository.
