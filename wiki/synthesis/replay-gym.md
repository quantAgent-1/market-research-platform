---
type: overview
title: The Replay Gym — Blind Historical Reps
description: Training protocol for graded market-history reps — blind day-stepping, call sheet integration, and a starter episode list ordered by learning ROI.
tags: [systematic-trading, ml-stats, training, market-history]
timestamp: 2026-08-07T00:00:00Z
status: active
sources: []
---

# The Replay Gym — Blind Historical Reps

The rate limiter on trader development is **graded feedback cycles**, not information. Live markets issue roughly one meaningful rep per day; history issues as many as you can process — **if** you step through it blind.

Pairs with the [quant trader curriculum](quant-trader-curriculum.md) and the [morning call sheet](../systematic-trading/checklists/morning-call-sheet.md).

## Protocol

1. **Load a window** with warm-up days before the event so the turn date is not obvious.
2. **Step one day at a time.** Observe only data ≤ T.
3. **Write a call before revealing T+1** when the tape demands one (large move, new extreme, gap): claim type + confidence as on the call sheet. Log with `market=replay`.
4. **Grade on reveal.** No rewinds. A skipped grade voids the episode.
5. **Close with a one-pager:** setup (crowding/leverage), spark, who was forced, propagation, floor formation, false lessons. File it as a pattern library entry.

**Honesty rule:** episodes you already know cold are study reps, not graded calibration data.

## Minimal stepper (~100 lines)

CLI sketch (`tools/replay.py` or engine research harness):

- Input: tickers, start/end, warm-up days; cache OHLCV once.
- Loop: show frame through T → optional call → append log → reveal T+1 → grade numeric claims when possible.
- No look-ahead: the served frame is sliced before the prompt.

## Starter episode list (learning ROI)

| # | Episode | Load window (approx.) | Instruments (examples) | One-pager question |
|---|---|---|---|---|
| 1 | Aug-2024 yen-carry unwind | 2024-07 → 2024-08 | Nikkei, USDJPY, VIX, QQQ, KOSPI, SK Hynix | Cross-border margin cascade vs local clocks |
| 2 | Feb-2018 Volmageddon | 2018-01 → 2018-02 | SPY, VIX, short-vol ETPs | Mechanical vol buyer into a close |
| 3 | Oct-1987 | 1987-09 → 1987-11 | S&P | Portfolio insurance as vol-target ancestor |
| 4 | KOSPI options crash (2010) | 2010-11 | KOSPI + public post-mortems | Expiry auction under one large seller |
| 5 | 2010 flash crash | 2010-04 → 2010-05 | SPY + official report | Conditional liquidity |
| 6 | Mar-2020 COVID crash/V | 2020-02 → 2020-04 | SPY, VIX, HY credit | Constraint stack + policy backstop |
| 7 | 2018 memory cycle top | 2018 | MU, SOXX, Samsung/SKH | Second-derivative topping while earnings rise |
| 8 | 2021–22 growth de-rate | 2021-11 → 2022-10 | QQQ, high-duration names | Duration compression without “bad earnings” first |

Extend with sector-specific episodes relevant to your research book; keep **pre-current-year** episodes for graded work if concurrent live trading uses the same complex (avoid contaminating the live process with hindsight on the same tape).

## Related

- [Navigating nonlinear markets](navigating-nonlinear-markets.md)
- [Liquidity cascades](../shared/concepts/liquidity-cascades-and-v-reversals.md)
- [Multi-week unwinds](../shared/concepts/multi-week-unwinds-and-recoveries.md)
