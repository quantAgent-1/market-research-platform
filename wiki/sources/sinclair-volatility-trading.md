---
type: book
title: "Volatility Trading (Euan Sinclair, 2008)"
description: Practitioner guide to trading the spread between implied and realized volatility — measurement, forecasting, hedging, and money management.
resource: # primary source not redistributed
tags: [derivatives, volatility, options, hedging, kelly, book]
timestamp: 2026-06-13T00:00:00Z
status: active
---

# Volatility Trading

**Author:** Euan Sinclair (b. 1969), option trader
**Publisher:** John Wiley & Sons, 2008 (1st ed., Wiley Trading series) · ISBN 978-0-470-18199-7 · ~220 pp.
**Source file:** `(primary source on file privately — not redistributed)`

## What it is
A pragmatic, data-driven manual for trading volatility with options — making trades that depend on
the *range* of the underlying rather than its direction. Sinclair writes as a working trader: "My
success is measured in profits. The tools I use... need only be useful." He uses Black–Scholes–
Merton as a deliberately simple, well-understood lens, then trades against its inadequacies.

## The trading process (the book's spine)
Sinclair splits trading into three areas, each a section of the book:
1. **Finding edge** — option pricing (Ch. 1, informal BSM derivation),
   [volatility measurement & forecasting](../derivatives/concepts/volatility-measurement-forecasting.md)
   (Ch. 2), [implied-vol / smile dynamics](../derivatives/concepts/volatility-smile-dynamics.md)
   (Ch. 3), [hedging](../derivatives/concepts/dynamic-hedging.md) (Ch. 4–5). Core thesis: trade
   your forecast of realized vol against the market's
   [implied vol](../derivatives/concepts/implied-vs-realized-volatility.md) — see
   [volatility arbitrage](../derivatives/strategies/volatility-arbitrage.md).
2. **Managing risk & bankroll** — [money management / Kelly criterion](../shared/concepts/kelly-criterion.md)
   (Ch. 6); trade evaluation with risk-adjusted metrics (Ch. 7: Sharpe, Sortino, Calmar, omega).
3. **Psychology** — behavioural biases to defend against and exploit (Ch. 8); life cycle of a
   trade (Ch. 9).

## Key takeaways
- The largest source of edge in options is trading forecast realized vol vs. market implied vol.
- A point forecast isn't enough — use **volatility cones** for the *distribution* of future vol.
- Estimator choice matters (close-to-close, Parkinson, Garman–Klass, Rogers–Satchell, Yang–Zhang);
  each is biased differently by trends, gaps, and microstructure noise.
- Position sizing (Kelly and safer variants) can matter more than trade selection.

## Caveats & limitations
- First edition 2008 — pre-dates the post-2010 compression of the
  [volatility risk premium](../derivatives/concepts/volatility-risk-premium.md) (the wiki's VRP
  brief found the premium mostly an index phenomenon and only modest net of costs); the 2nd edition
  remains an open reading item.
- Written for an options market-maker/prop context: assumes execution quality and vega scale a
  retail account cannot match — the sizing/psychology chapters travel better than the
  trade-structuring ones.

## Links into the wiki
Feeds: [Implied vs. realized volatility](../derivatives/concepts/implied-vs-realized-volatility.md) ·
[Volatility measurement & forecasting](../derivatives/concepts/volatility-measurement-forecasting.md) ·
[Volatility smile dynamics](../derivatives/concepts/volatility-smile-dynamics.md) ·
[Dynamic hedging](../derivatives/concepts/dynamic-hedging.md) ·
[Volatility arbitrage](../derivatives/strategies/volatility-arbitrage.md) ·
[Kelly criterion](../shared/concepts/kelly-criterion.md) ·
[Euan Sinclair](../shared/people-firms/euan-sinclair.md)
