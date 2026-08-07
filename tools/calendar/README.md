# Forced-Flow Calendar (ffcal) — v0.1

Who is forced to trade, when, on both tapes (US + KRX), rendered in KST. Present-state stack
tool #2; design spec (feeds, doctrine, kill criteria):
[`wiki/designs/forced-flow-calendar.md`](../../wiki/designs/forced-flow-calendar.md).

Stdlib-only, Python 3.11+ (uses `tomllib`). No network calls — deterministic rules + the
hand-maintained `overrides.toml`.

## Daily use

```
python ffcal.py next 10              # the "who is forced" block (stdout)
python ffcal.py brief                # same, written to store/brief-YYYY-MM-DD.md
python ffcal.py day 2026-07-09       # day-of T-schedule (KST timeline) for big days
python ffcal.py ics --days 60        # store/ffcal.ics -> import to the phone calendar
python ffcal.py html --days 27       # store/dashboard.html -> open in any browser
python ffcal.py selftest             # 26 acceptance anchors (July-2026 hand calendar + sector feeds)
--asof YYYY-MM-DD                    # deterministic output for any date (testing/backfill)
```

**Dashboard:** `html` writes a self-contained `store/dashboard.html` (no network, light/dark,
works from disk): density-heat strip + corporate-bid bars on shared day columns, pins-needed
panel, filterable day cards (KR / US+global / L+XL / hide-plumbing) with embedded T-schedules.
`html --fragment` emits the body-only variant used for claude.ai artifact publishing
(current artifact: https://claude.ai/code/artifact/b1407abe-db7d-4549-9f1c-edd69afc2315 —
redeploy by regenerating the fragment and republishing to the same URL).

Line format: `[size|conf]` where size S/M/L/XL and conf `#`=rule-derived, `OK`=confirmed on a
primary source, `~`=estimated (pin before relying). `[plumbing, not signal]` marks events whose
famous *price* effect is decayed — they remain risk/execution/attribution events.

## Conventions that differ from the hand calendar

- **KST-native dates.** A US AMC print renders on its KST landing datetime: META "Jul 29 AMC"
  shows as **Thu Jul 30, 05:05** — when it actually hits this desk's tape.
- **Blackout windows are per-name merged bands** `[earnings − 35d, earnings + 2 trading days]`;
  the brief shows only enter/exit transitions plus the daily gauge
  (`corporate bid: N/M present`). Windows are proxies for private policies — bands, not lines.
- Weekend data releases (Korean exports on the 1st/11th/21st) stay on their calendar date with a
  "tape reacts next session" note.

## Weekly human pass (~10 min)

1. Pin `~` estimated dates as IR pages confirm them → flip `confirmed = true` in
   `overrides.toml` (MSFT Jul 28-vs-29 and SK hynix Jul 29 are the live ones).
2. Paste any published month-end/quarter-end rebalance estimates into `monthend_estimates`.
3. After a big KOSPI down day: add the date to `[f13] kospi_down_days` (+ set `margin_z`) so the
   next morning carries the 반대매매 forced-supply flag. (Automates when the flow engine lands.)
3b. Before each big print: refresh its `[watch_for]` questions (they render on the brief and
   dashboard — answer them on the call sheet). Add dated policy items to `policy = [...]` as
   they're announced (effective dates, comment deadlines, statutory clocks — dated items only).
4. Annually: verify `[krx_holidays]` (substitutes are best-effort) and the in-code FOMC/CPI
   tables against the published Fed/BLS schedules.

## Implemented vs pending (design §6)

- **v0.1 (Day 1-2, live):** F1 opex/witching · F2 VIX exp · F3 roll week · F4 month-end windows
  (+ estimate slots) · F5 FOMC/blackout/CPI/NFP (+ `macro_us` paste) · F6 US sessions/DST ·
  F7 recon effective dates · F8/F15 earnings (overrides) · F9 blackout transitions + gauge ·
  F11 KRX 만기 · F12 exports triplet/TSMC-monthly/BOK · F13 manual flags · F14 KR sessions ·
  brief/density/pileup · T-schedules · ICS · selftest · html dashboard.
- **v0.2 sector layer (design §1b items 1/2/3/5/8, live):** **F16** monthly sector prints —
  TrendForce contract-settlement window (**Sentry T2's date source**), Hon Hai ~5th, Aspeed +
  Taiwan ODM statutory deadline on the 10th, Korea IP semis shipments/inventory (~last KR bd,
  08:00) · **F18** policy dates (overrides paste; dated items only) · **F7+** SOXX/SOXL + SMH
  quarterly rebalances · **`watch_for`** pre-registered questions per print (`[watch_for]` table
  in overrides; keyed `"TICKER@date"` → `"TICKER"` → macro label), rendered as `?` lines in the
  brief and question checklists on the dashboard.
- **Pending:** F16 SIA/SEMI/SEAJ prints · tripwire chips (§1b item 4) · F17 conference/qual
  calendar (item 6) · chain tags + "this week in the chain" strip (item 7) · F7 announcement
  scrapers (S&P/MSCI RSS) · F8 earnings auto-confirm · F10 lockup scraper · F13 KOFIA auto-join
  (needs stack tool #1) · Exit-Sentry `store/panels/calendar.json` export · scheduler entry.

## Kill criteria (pre-registered, from the design page)

In the morning brief from Day 1 ✓. The **Jul-9 KRX 만기** and **Jul-17 US opex** T-schedules
must each be cited *before the fact* in a call sheet by D14 — or scrapers freeze and this
reverts to a static quarterly hand-page.
