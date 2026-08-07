---
type: checklist
title: Morning Call Sheet — Daily Pre-Registration & Grading
description: The daily form that turns every session into calibration data — one pre-registered call per market per day, graded at the close, logged to calls.csv for the weekly calibration curve.
tags: [systematic-trading, checklist, calibration, process]
timestamp: 2026-07-04T00:00:00Z
status: active
sources: []
---

# Morning Call Sheet — Daily Pre-Registration & Grading

The second-highest-ROI artifact of the sprint, because it
is what makes the other ~11 hours of each day count. Without it, a month of screen time produces
anecdotes. With it, the month produces a measured answer to the only question that matters:
**how good are my reads, actually?**

The rule: **one call per market per day, written before the session, graded at the close.**
A day with no trade still gets a call (graded as paper). A trade without a call sheet is a
[constitution](trading-risk-constitution.md) breach.

## The form

Copy this block into the day's journal entry each morning:

```
## Call — YYYY-MM-DD — [KRX / US]
Setup:        (which condition? which checklist page? "none — observation call" is valid)
Claim type:   direction / day / minute / magnitude   (pick ONE per call)
Claim:        (one falsifiable sentence with a number and a deadline)
Confidence:   55 / 65 / 75 / 85 %
Falsifier:    (what kills the call before the deadline)
Action:       PAPER  |  live (size per constitution: __ )
--- graded at the close ---
Outcome:      HIT / MISS / VOID
Notes:        (one line: what the tape said vs what I said)
```

Rules that keep the data honest:

- **One claim type per call.** "Direction, day, minute, magnitude" are separate claims with
  separate evidence, per the [V-day checklist](catching-the-v-day-checklist.md). Grading them
  together hides which skill you actually have.
- **A claim needs a number and a deadline.** "SK hynix looks strong" is not gradable.
  "005660 closes above yesterday's high today" is.
- **Confidence comes in four buckets only** (55/65/75/85). Finer precision is fake at this
  sample size.
- **VOID is for setups that never armed** (the condition didn't occur, the event was postponed).
  A call that armed and went nowhere is a MISS, not a VOID. When in doubt, grade against
  yourself.

## The event variant (implied-move sheet)

For scheduled events (earnings, CPI, FOMC), written the evening before:

```
## Event sheet — YYYY-MM-DD — [ticker/event]
Implied move:     (US: ATM straddle / spot, front expiry. KRX: use the base-rate table below)
Base rate:        (last 8 analogous events: median |move|, % up)
My distribution:  p10: __   p50: __   p90: __   (next-session close vs pre-event)
What's priced in: (one sentence — what outcome would NOT move it)
Plan:             PASS | position (0.25% max per constitution)
--- graded after ---
Actual:           __%   | my p50 error: __   | inside my p10-p90? Y/N
Lesson:           (one line)
```

For KRX names without liquid single-stock options, the implied move is replaced by a base-rate
table: pull the last 8 reaction days for the same event type (e.g. Samsung preliminary
guidance days) and use median absolute move and direction split. Building that table is part of
the event prep.

## The log — `calls.csv`

Every call also appends one row to a flat file (the engine can consume it later):

```
date,market,claim_type,statement,confidence,outcome,live_or_paper,notes
2026-07-06,KRX,day,"...",65,1,paper,"..."
```

`outcome`: 1 = HIT, 0 = MISS, blank = VOID. Brier score per call = (confidence/100 − outcome)².

## The weekly calibration curve

Every Monday morning, before the session:

1. Bin the graded calls by confidence bucket (55/65/75/85).
2. For each bucket: hit rate vs stated confidence, and mean Brier.
3. One sentence of diagnosis: overconfident where? Underconfident where? Which claim type is
   weakest?

That table, accumulated over the month, is the sprint's most valuable single output — the
Aug-2 exit criteria grade it. Expect the first week's
curve to be embarrassing; that is the point of measuring.

## Relationships

- Enforced by [the risk constitution](trading-risk-constitution.md) (Article 4).
- Claim structure from [catching the V-day](catching-the-v-day-checklist.md); exit-side tells
  from [the new-high checklist](new-high-trade-checklist.md).
- Event targets come from the [July-2026 event calendar](../../market-research/july-2026-event-calendar.md).
