---
type: index
title: Engine v3 — Index
description: All Engine v3 design documents in one place — mission brief, repo blueprint, the H6 module spec, and the active build handoff.
timestamp: 2026-07-03T00:00:00Z
---

# Engine v3

The design-doc set for `enginev3`, grouped. Read order for context: brief → outline → module spec
→ handoff. **The active build is the H6-first vertical slice** — module before engine (decision
2026-07-03); the coding agent starts from the handoff.

- [Design brief](design-brief.md) — the mission (a sensing instrument, not a money printer),
  constraints, hypotheses H1–H5, pre-committed success metrics (dollars not a KPI).
- [Full project outline (repo blueprint)](project-outline.md) — file-by-file directory tree, stack
  pins, the idempotent nightly DAG on the KST clock, PROTOCOL v3.0, week-by-week deliverables.
- [H6 — crowding & first-defector module (production plan)](h6-crowding-defector-module.md) —
  Signal A condition (A1–A14 → CROWD state machine) + Signal B trigger (B1–B8 → family-vote
  DEFECT) **+ Signal C re-entry (§5b: overshoot meter O1–O3 quantifying "fell more than the
  revisions" + exhaustion detectors C1–C5 → CASCADE/EXHAUST)** → tax-aware exposure overlay;
  bitemporal PIT data contracts; episode-library falsification; fail-soft ops; phase gates +
  binding kill criterion. **Amended 2026-07-03 (×2): free-data-first + H6-first sequencing;
  Signal C added from the Jul-1→3 cascade-and-V.**
- [H6-first build handoff](h6-first-build-handoff.md) — **the coding-agent entry point**: the
  scoped vertical slice, milestones A–C with definitions of done, free-tier data endpoints
  (now incl. S10 KOFIA margin credit + S11 KRX curb events), engineering non-negotiables,
  out-of-scope guardrails, and the human acceptance checklist. **Amended 2026-07-03: Signal C
  in scope (dashboard math on free sources; O3 anchor-only until the episodes handoff).**
- [Execution layer (OMS) design](execution-layer.md) — **(added 2026-07-07, build: planned)**
  the registered amendment to the tickets-only guardrail: Alpaca adapter + diff engine + 8-check
  pre-trade risk gate + idempotent order state machine + reconciliation + drilled kill switch +
  the 22:20-KST session daemon, promoted only through the pre-registered **shadow → paper-auto →
  live-small (≤20% NAV) → full** ladder with automatic demotion. ~14h to shadow; kill criterion:
  beat the manual-ticket baseline in 30 sessions or freeze.
