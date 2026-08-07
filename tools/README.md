# tools/ — the tool library

Two kinds of tools live here, one folder convention:

1. **Wiki-maintenance scripts** (repo plumbing, loose `.py` files):
   - `build_timeline.py` — regenerates `wiki/timeline.md` from git history (run on every ingest).
   - `pdf_extract.py` — PDF text/TOC extraction without poppler (PyMuPDF; ASCII-safe output).
   - `check_links.py` — relative-link checker for the wiki.

2. **Trading tools** (the present-state stack made real, **one subdirectory per tool**):
   - `position_size.py` — position sizing per the risk constitution (predates the folder rule).
   - `calendar/` — **Forced-Flow Calendar** (stack tool #2): who is forced to trade, when, on
     both tapes. Design spec: [`wiki/designs/forced-flow-calendar.md`](../wiki/designs/forced-flow-calendar.md).
   - `flowmap/` — **The Flow Read** (semis flow-map P1-live): the five-question habit as one
     module + dashboard (cohort attribution KR/TW measured + US inferred, forced-vs-informed
     tape, ffcal + LETF MOC arithmetic, crowd state, expectations bar). Design spec:
     [`wiki/designs/semis-institutional-flow-map.md`](../wiki/designs/semis-institutional-flow-map.md).
   - `muval/` — **Valuation & Risk Models (MU / NVDA / AMD)**: scenario DCF + reverse DCF
     ("what the price assumes") + Monte Carlo per name (`--name NVDA/AMD`); MU also gets the
     volatility/factor engine (GARCH, vol cone, earnings moves, betas). `events.py` =
     pre-earnings cards (implied-vs-historical move richness, all three names); `complex.py` =
     cross-name complex report; every assumption editable in `assumptions.toml`. Design spec:
     [`wiki/designs/valuation-complex.md`](../wiki/designs/valuation-complex.md) (post-hoc, `build: live`).

## Rules for trading tools (from the stack doctrine)

- **Design first:** each tool has a design page in `wiki/designs/` (`type: design`) with kill
  criteria; the `build:` field tracks `planned → building → live`.
- **Rule zero:** a tool prints into the morning brief within 7 days of build start and is cited
  in at least one graded call within 14 — or it gets cut.
- **Stdlib-first:** prefer zero-dependency Python (this machine: 3.13). Paid/API dependencies
  only where the design says so (Alpaca tools).
- **Files are the database:** outputs under the tool's `store/`, git-committed — the audit trail
  is the version history.
- Console is cp949: print ASCII-safe (`sys.stdout.reconfigure(errors="replace")`), write files
  as UTF-8.
