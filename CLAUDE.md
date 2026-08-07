# CLAUDE.md — Markets Research Lab Schema

This directory is the **Markets Research Lab** public knowledge base (LLM-wiki pattern; see `meta/llm-wiki.md`)
conformant with a lightweight **Open Knowledge Format** style: YAML frontmatter + interlinked markdown.

The maintainer is responsible for keeping pages atomic, cross-linked, and free of personal account data.

---

## Layers

1. **`wiki/`** — knowledge (OKF-style concept documents).
2. **`tools/`** — research/trading tooling (one subdirectory per tool + small wiki scripts).
3. **`alpaca-data/`** — market-data package (code only in public).
4. **`CLAUDE.md`** — this schema.

There is **no public `raw/` corpus** of copyrighted PDFs. Source summaries in `wiki/sources/` cite public
references; primary PDFs are not redistributed.

---

## Frontmatter

```yaml
---
type: concept          # see type vocabulary below
title: Human title
description: One-line summary
tags: [domain, theme]
timestamp: 2026-08-07T00:00:00Z
status: stub | active | stable
sources: []            # relative paths to source summaries when applicable
---
```

Design pages may include `build: planned | building | live | killed | superseded`.

---

## Type vocabulary

`concept` · `strategy` · `factor` · `model` · `instrument` · `dataset` · `person` · `firm` ·
`thesis` · `overview` · `market-note` · `audit` · `checklist` · `design` · `index` ·
`paper` · `book` · `article` · `code` · `research-brief`

---

## Rules for public content

- **No personal trading accounts:** no balances, share counts, personal fills, leverage on a private book,
  brokerage login product detail, or “what should I do with my position” coaching.
- **Market facts OK:** public prices, industry figures, and institutional disclosures used as research evidence.
- **Generalize process pages:** risk rules and edge surveys use example parameters, not private NAVs.
- **Cross-link with relative markdown links** to `.md` files (not Obsidian wikilinks alone).
- **Flag contradictions** rather than silently overwriting.
- **Never commit secrets** (`.env`, keys, parquet lakes).

---

## Indexing

- `wiki/index.md` — catalog (progressive disclosure).
- Section `index.md` files under each domain.
- Prefer updating indexes when adding pages.

---

## Tools doctrine

From the present-state stack: design pages in `wiki/designs/` with kill criteria; stdlib-first Python;
files under a tool’s local `store/` for runtime output (gitignored in public); ASCII-safe console on Windows.

---

When in doubt: keep pages atomic and linked, keep the public tree free of personal account detail, and treat
every trading-related page as **education/research**, not advice.
