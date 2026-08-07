---
type: design
title: "Valuation Complex (muval) — MU / NVDA / AMD Valuation & Risk Models"
description: One engine answering three questions for each of Micron, Nvidia, and AMD — what is it worth (scenario DCF, probability-weighted, Monte-Carlo distributed), what does the price already assume (reverse DCF, three independent reads), and what moves it, how violently (factor decomposition, GARCH, vol cone, earnings-event study) — plus two cross-name layers no single-name model can produce, pre-earnings implied-move richness cards and the complex consistency panel (discount-rate gap, revenue-ratio yoking, the AI-capex pool the joint bull cases require, effective portfolio breadth). Written post-hoc for a live build; the build ran as the first full manager/builder delegation workflow (6 Sonnet builders, 3 verification gates).
resource: ../../tools/muval/README.md
tags: [systematic-trading, derivatives, semiconductors, valuation, volatility, tooling]
timestamp: 2026-07-11T00:00:00Z
status: active
build: live
sources: []
---

# Valuation Complex (muval) — MU / NVDA / AMD

**The ask (2026-07-11, three requests in sequence):** (1) "build a financial modeling tool to
get the valuation of Micron Technology and the variables that affect the price and volatility
... build it till the end"; (2) scope pinned to "nasdaq MU NVDA AMD" (no Korea-tape builds);
(3) go-ahead on the two chosen extensions — the three-name valuation complex with a cross-name
consistency panel, and the earnings-event engine — built under the new standing workflow:
Fable as manager/reviewer, Sonnet agents as builders.

This page is written **post-hoc for a live build** (the design-first rule was under the
documentation pause when construction started); it records the design as decided, not as
aspiration. The tool's user-facing documentation is
[`tools/muval/README.md`](../../tools/muval/README.md) — that file explains how to *use* it;
this page explains why it is *shaped* this way.

## In plain language (read this first)

The tool answers three questions about each of the three stocks, using only free data,
regenerated on demand:

**What is it worth?** Not as one number — as three explicit futures. For each company the
model writes down a bull, base, and bust scenario as a full year-by-year path of revenue,
profit margin, and cash out to ten years, then discounts the cash (a DCF — discounted cash
flow — the standard way of converting future cash into today's value). The three answers get
blended by probability weights you can edit, and a Monte Carlo simulation (twenty thousand
re-runs with the inputs jiggled) turns the blend into a full distribution, so the output is
honest about its own uncertainty.

**What does today's price already assume?** This is the reverse DCF — run the machine
backwards from the market price and solve for the assumption that would justify it. It turns
"this looks expensive" into a specific, checkable claim. Example finding: AMD at $558 equals
its bull-case revenue path discounted at 5.6% per year — against the 11.9% the standard
risk model says a stock this volatile should earn. That gap *is* the disagreement between
this model and the market, stated in one number.

**What moves the price, and how hard?** A statistical layer measures how much of each
stock's daily movement is the broad market, how much is the semiconductor sector, and how
much is company-specific news that no index hedge removes; how violent the stock is in
absolute terms (Micron's realized volatility was at its ten-year 98th percentile at build
time); and what earnings days specifically do (for Micron, 49 earnings days — 1.6% of
trading days — carried 10% of all price variance).

On top of the three single-name models sit the two things only a *set* of models can do.
The **pre-earnings cards** compare what the options market is paying for each company's next
earnings move against what that company's earnings days have actually done, and call the
event rich or cheap. The **complex report** checks the three models against each other:
whether the futures implied by the three prices can all be true at once (they require
~$1.02T/yr of sustained AI capex — 1.4× the 2026 pool), and whether owning all three is
diversification (it is not: one common factor is 69% of their joint daily variance, so three
positions are ~1.4 independent bets).

## 0. The design-space map — toy / professional / world-class

**Toy** is a single-point DCF on consensus numbers with a "fair value" headline — the
standard retail-site artifact. It fails on cyclicality (memory earnings swing from −38% to
+47% net margin; any point estimate is an accident of where you stand in the cycle) and it
hides the judgment inside the spreadsheet.

**Professional — this build** — makes the judgment explicit and prices its consequences:
cycle-aware scenario paths anchored to the company's own measured history (every default in
`assumptions.toml` cites the actual it came from), a reverse-DCF layer because *what's priced
in* is more decision-useful than *what I computed*, distribution over point estimate, and an
event/volatility layer because the desk trades these names around catalysts. Everything
regenerates from cached raw pulls; every run leaves a dated JSON for later grading.

**World-class** — what this build deliberately is not — adds what money buys: consensus
*revision history* (the drift of estimates, not just their level — the single most useful
missing feed), segment-level models (DRAM/NAND/HBM bit-price-cost curves; HBM contract-book
tracking), dealer event-vol marks instead of delayed-quote approximations, and an
institutional-grade capex-tracker for the pool bridge instead of one parametric number. None
of these change the architecture; they upgrade feeds and granularity. The copyable part —
scenario discipline, reverse-DCF framing, pre-registered assumptions, grading substrate — is
all here.

## 1. Mission & doctrine compliance

The tool exists to make the desk's AI-silicon views *quantified, editable, and gradeable*:
a standing answer to "what would I have to believe to hold this name here," refreshed from
live data in under a minute, with the judgment isolated into one editable file rather than
smeared through code.

- **Rule zero:** the tool prints decision-usable output immediately (console briefs + three
  HTML reports on day one), and the earnings calendar gives it a natural graded rep within
  weeks — AMD prints Aug-4, NVDA Aug-26, MU Sep-23; the pre-earnings cards are built to be
  cited in those pre-registrations. Kill criteria in §13.
- **Anti-platform-trap / budget honesty:** absorbed the "implied-move" half of the stack's
  implied-move & TCA backlog item (straddle-implied event moves now live here); zero new
  spend — every feed is free; no new standing pipeline (pull-on-run with caches, not a
  scheduler).
- **Identification discipline (house rule inherited from the flow-map):** the model never
  claims to *know* the structural-break question. The scenario probabilities are labeled
  judgment inputs; the reverse-DCF section exists precisely so the market's implied answer
  and the model's assumed answer face each other in one table.

## 2. Architecture — five layers over one cache

```
data.py          fetch + cache (files are the database; per-ticker, TTL'd, offline-first)
fundamentals.py  frames + cycle analytics (trend fit, margin percentiles, drawdowns, consensus)
valuation.py     the engine: scenario paths -> DCF -> reverse DCF -> normalized -> MC -> tornado
riskvol.py       vol estimators, GARCH, cone, factor decomposition, earnings study, IV extraction
report.py        MU full report (13 figures, dataviz-conformant), console brief, JSON snapshot
events.py        pre-earnings cards for the three names (consumes riskvol's event extraction)
complex.py       the three-name consistency panel (consumes valuation runs for all names)
assumptions.toml the judgment file: per-name fiscal calendars, scenario sets, cash mechanics
muval.py         CLI orchestrator (--name MU|NVDA|AMD, --offline/--refresh/--no-open, selftest)
```

The dependency direction is strictly downward: `events.py` and `complex.py` import the lower
layers as libraries and add nothing to them. The MU pipeline (`muval.py` bare) is the
reference path and carries the full risk block + HTML report; NVDA/AMD run valuation-only
briefs + JSONs; the cross-name artifacts are separate commands. One deliberate asymmetry:
the risk/volatility block stays MU-only for now (MU is the desk's active name; the event
engine covers the risk facts that matter pre-print for the other two).

## 3. Data plan (per feed: source · cadence · automation · failure mode → fallback)

| Feed | Source | TTL | Feeds | Failure mode → fallback |
|---|---|---|---|---|
| Prices, 13 tickers, up to 40y OHLCV | yfinance | 1d | returns, betas, cone, tails, P/B join | per-ticker try/except; MU missing = hard stop, others warn |
| Statements (5y ann + quarters), info, estimates, ~50 earnings dates | yfinance | 3d | boom cash mechanics, consensus anchors, earnings study | offline mode reads last cache; estimate tables may be sparse per name → `None`-safe consensus dict |
| Annual fundamentals FY2011+ (13 metrics; capex = CFO − FCF) | macrotrends.net | 14d | trend, mid-cycle margins, drawdowns, multiples history | 429 retry ×3 w/ backoff; slug 404 → redirect-discovery probe (verified against an unseeded ticker); page loss = that metric NaN, engine degrades |
| Option chain (~13.5k contracts/name) | CBOE delayed-quotes JSON | 1d | IV term structure, 25Δ skew, event-move extraction | absent/stale → IV sections empty, valuation unaffected |
| 10y Treasury (DGS10) | FRED | 1d | risk-free rate | stale cache → last print with as-of stamp |
| EDGAR XBRL | — **geo-blocked** (SEC 403s non-US IPs, verified from both sandbox and real IP) | — | — | macrotrends substitutes for long history; segment tables remain out of reach (limit §14) |

The EDGAR block is the build's one forced substitution and its most consequential data
decision: fundamentals history starts FY2011 (macrotrends' free window) instead of ~1995,
which covers two full memory cycles and the post-Elpida three-supplier oligopoly but not
2001/2008. Anchors quoted in the toml are all from inside that window.

## 4. Core logic — the valuation engine

**Scenario paths.** Each scenario is twelve knobs, chosen so that each one is a claim a
human can argue about (nothing is a free regression coefficient): the first forecast year's
revenue as a fraction of consensus; optional extra boom years and their growth; the trough
as a fraction of peak (anchored to the name's measured drawdowns — MU: −24%, −29%, −49% in
the modern era); the post-correction plateau as a fraction of peak; steady growth thereafter;
net-margin at peak / trough / steady (anchored to the name's margin percentiles); and capex
intensity in boom / correction / steady phases. The path builder turns those into geometric
revenue segments (peak → trough → plateau → steady growth) and piecewise-linear margin paths
over a ten-year horizon. Margins are modeled *directly* (net margin, not a full P&L build):
with only ~15 annual observations per name, a line-item build would manufacture precision
the data cannot support — the margin path IS the argument, so it should be the knob.

**Cash conversion.** Free cash flow = net income + D&A − capex − working-capital build,
where D&A converges from today's level toward steady-state capex over five years (fab
depreciation lag — the mechanism that torpedoes memory margins in downturns), and working
capital consumes a fixed fraction (measured: ~12% for MU) of each year's revenue *change*,
releasing cash in contractions. This four-term identity is where memory economics live: MU's
FY2012–25 cumulative FCF was $19.5B on $52.1B of net income — conversion 0.37 — because
capex historically ran ~10pp of revenue above D&A forever. Scenario A vs C for MU is largely
a disagreement about whether that ends.

**Discounting and fiscal calendars.** Cost of equity via CAPM (risk-free = live 10y; beta =
5y weekly regression vs SPY, Blume-shrunk two-thirds toward 1, floored/capped), blended to a
WACC that is ~equity-only for all three (all net cash). Cash lands at fiscal mid-year, where
"fiscal" is per-name: MU's year ends late August, NVDA's late January (so NVDA's *current*
fiscal year is 2027), AMD's is the calendar year — `fy_end(fy) − 183 days` generalizes the
timing. The in-progress year enters as a stub: consensus full-year EPS minus already-reported
quarters (street basis on both sides), at the year's modeled cash conversion. Terminal value
is a Gordon growing perpetuity (g = 2.5%) cross-checked by an exit EV/EBITDA multiple —
two terminal readings shown side by side, disagreement visible.

**Reverse DCF — the layer the tool is really for.** Three independent solves per name:
(1) the perpetuity yardstick — market cap minus net cash as a constant-growth perpetuity,
expressed as owner earnings per share and as a fraction of next-FY consensus EPS; (2) on the
bull revenue path, the steady net margin that matches the price (frequently *unreachable* at
any margin ≤ 90% — the solver reporting "no solution" is itself the finding: the price
requires the revenue story, not a margin story); (3) the discount rate that makes the bull
case worth the price — the cleanest cross-name comparable (MU 10.5%, NVDA 8.8%, AMD 5.6% at
build time, vs CAPM WACCs of 11.7/12.4/11.9%).

**The normalized bracket (MU).** The deliberately cold counterfactual — trend revenue (log-
linear fit, FY2012–25) at the median net margin, banded by a through-cycle P/E plus net
cash, cross-checked by justified price-to-book ((normalized ROE − g)/(r − g) × book). It is
the "structural break never happened" limiting case, ~$76–106 against a $979 price — i.e. a
measured statement that ~90% of the market price is payment for the break being real.

**Monte Carlo and tornado.** The MC draws a scenario by its probability then jitters six
inputs (first-year revenue, trough, plateau, steady margin, WACC, terminal g) with fixed
seed — so runs are reproducible and cross-checkable bit-for-bit. The tornado moves one knob
at a time around the base case and ranks them; for all three names the plateau and steady
margin (the "is the break real" knobs) dominate the financial knobs.

## 5. Core logic — the risk engine (MU pipeline)

Realized volatility four ways (close-close, Parkinson, Garman-Klass, Yang-Zhang — the last
using open/high/low/close and separating overnight from intraday variance), rolling and as a
ten-year **vol cone** (percentile bands of realized vol by horizon, current values and the
option-implied curve overlaid). A **GARCH(1,1)** fitted by maximum likelihood on ten years of
daily returns gives the one-month forecast and the long-run anchor the current regime decays
toward (at build: 118% realized → 91% one-month forecast → 51% long-run). A **factor
regression** (market / sector-beyond-market / rates / dollar, Newey-West standard errors
because daily returns aren't independent) decomposes variance: at build, 33% market + 27%
sector + 40% Micron-specific-and-unhedgeable. The **earnings study** joins ~50 announcement
dates to next-session reactions (mean |move| 6.5%, and earnings days = 10% of total variance
from 1.6% of days). The **event-vol extraction** backs the market's implied earnings move
out of the option chain by forward-variance differencing: total variance to the first
post-earnings expiry minus variance to the last pre-earnings expiry, minus baseline (far-
dated IV) variance on the non-event days — an approximation of the dealer's event mark,
labeled as such.

## 6. Core logic — the pre-earnings cards (`events.py`)

The event engine runs the extraction plus the historical study for all three names and adds
the one line that makes it decision-shaped: **richness = implied ±1σ event move ÷ median
historical |reaction|**, bucketed (<0.8 cheap · 0.8–1.25 in line · >1.25 rich), with two
honesty guards — a flag when only the fallback (total-straddle) read is available, since that
bakes in background vol and biases richness high; and a regime caveat when current realized
vol is above the name's ten-year 90th percentile, since history then understates plausible
moves. At build: MU 2.08× (rich — and genuinely event-specific, since the method already
nets an ~87% baseline), NVDA 1.20× (in line), AMD 1.34× (marginally rich, soft call — its
history is fat-tailed enough that the median denominator is fragile).

## 7. Core logic — the consistency panel (`complex.py`)

The design idea: the three prices are claims on **one underlying object** — hyperscaler AI
capex flowing through NVDA/AMD accelerators into HBM orders at MU — so three independently
built models can be audited *jointly*. Four checks:

1. **The discount-rate gap.** Each name's price-implied WACC on its own bull path vs its
   CAPM WACC, in one table. The uniform sign (every implied rate below CAPM) with ranked
   magnitude (AMD 6.3pp > NVDA 3.6pp > MU 1.1pp) is the market's pricing of the complex made
   comparable. The panel states both admissible readings — a lower-than-CAPM risk premium
   for AI, or outcomes beyond the configured bull cases — and refuses to pick: the model
   measures the gap, the human owns the interpretation.
2. **Revenue-ratio yoking.** MU/NVDA scenario-implied steady-state revenue ratios per
   matched letter (A/A 0.42, B/B 0.40, C/C 0.44) against the measured history (3.5× in 2014
   → 0.17 for the last closed fiscal years). The tight implied cluster is the finding: the
   scenario sets are structurally yoked, so MU and NVDA exposure is the same macro bet at
   different points in the chain, not diversification.
3. **The AI-capex pool bridge** (labeled parametric, not data): joint-A requires
   accelerator revenue of ~$614B, i.e. a sustained ~$1,023B/yr AI-capex pool at a 60%
   accelerator share — 1.41× the 2026 pool. Joint-B ≈ 0.82×, joint-C ≈ 0.41×. The memory
   attach ratio (MU revenue per dollar of accelerator revenue) lands 36–39% in every tier —
   an internal-coherence check on the scenario sets themselves.
4. **One factor, owned three times.** 3y daily correlation matrix, first principal component
   (69% of joint variance), and effective breadth 3/(1+2ρ̄) = **1.44 independent bets** from
   three positions — the sizing consequence in one number.

## 8. Interfaces

- `python tools/muval/muval.py` — MU: console brief + `store/report.html` (13 figures, six
  sections) + `store/valuation-<date>.json`.
- `--name NVDA|AMD` — valuation-only brief + `store/valuation-<TICKER>-<date>.json`.
- `python tools/muval/events.py` — cross-name summary + three cards; `store/events-<date>.html/.json`.
- `python tools/muval/complex.py` — consistency panel; `store/complex-report.html` +
  `store/complex-<date>.json`.
- All support `--offline` (cache-only; the assumption-iteration mode) and `--refresh`.
- Every dated JSON is a grading substrate: assumptions + outputs frozen per run.

## 9. Ops

No scheduler and no standing jobs by design — this is a pull-on-run tool; the caches make
warm runs ~30–60s (Monte Carlo dominates) and `--offline` runs pure. Reports are
self-contained HTML (charts embedded base64; renders from disk; dataviz-method conformant —
light surface, categorical slots, diverging blue/red only for polarity, tables as the
accessible twin of every chart). Console output is ASCII-safe for the cp949 terminal; files
are UTF-8. `selftest` pins the arithmetic offline: DCF vs closed-form perpetuity, terminal-
value monotonicity, bisection inversion, GARCH parameter recovery on synthetic data,
Yang-Zhang vs known synthetic vol.

## 10. The judgment layer — scenario sets and their anchors

The per-name scenario sets live in `assumptions.toml` with the anchor for every number in a
comment. Summary of the shape (full numbers in the toml):

| | A (bull) | B (base) | C (bust) | probs |
|---|---|---|---|---|
| **MU** | AI-memory rents persist; 38% steady NM (logic-class) | supercycle then a −50% digestion to a plateau ≈ FY26 revenue at 25% NM | commoditization; trough −65%, 16% NM | 25/45/30 |
| **NVDA** | platform monopoly compounds; consensus path, 50% NM | capex-digestion cycle; −40% to trough, 42% NM | Cisco analog / circular-financing unwind; 30% NM | 30/45/25 |
| **AMD** | credible second source; ~$100B peak, 25% NM | structural #2, cyclical; 18% NM | squeezed by NVDA + custom silicon; 10% NM | 30/45/25 |

Two doctrine points. First, the probabilities are inputs, not outputs — the model's honest
claim is conditional ("if you believe 25/45/30, fair value is $389"), and the tornado shows
which beliefs are load-bearing. Second, one accounting wrinkle is handled explicitly rather
than silently: AMD's consensus EPS is street-basis (excludes Xilinx intangible amortization),
so its cash mechanics use tangible-only D&A to avoid double-counting the add-back — flagged
in the toml and in the README's limits.

## 11. Build record & verification (the manager/builder workflow's first full run)

Six Sonnet builder delegations, three hard gates, manager-verified at each: (D) data-layer
parameterization — gate: MU console brief byte-identical to a frozen baseline, verified
independently; the builder also found and fixed a real bug in the slug-discovery fallback
and proved the fix on an unseeded ticker. (V) engine generalization — gate: WACC/beta/vol
numbers identical, DCF drift ≤ ~1.5% and fully attributed; the builder reconstructed the old
code path to prove 100% of the drift came from the two *approved* correctness fixes (the
stub now uses residual consensus EPS; working capital keys off actual prior-year revenue —
correctness beat the frozen regression on both), and caught a fiscal-window leak in the stub
spec that would have silently dropped the trailing prior-year print. (E) event engine —
gate: the MU card must reproduce the main report's ±11.2% through the same code path (it
did). (C) complex report — gate: per-name values bit-identical (1e-6, same MC seed) to the
standing snapshots; the builder corrected the manager's wrong narrative guess about the
revenue-ratio history from the data. Plus two documentation rounds (README written, then
re-verified line-by-line against live runs — the doc builder caught four spec inaccuracies
and fixed the *spec's* claims, not the code). Manager-side chart QA per the dataviz method
found and fixed five rendering defects across the 13 MU figures (title collision, mathtext
corruption, grid-over-bars, two contrast violations). All arithmetic in the consistency
panel re-derived by hand at the final gate (breadth 1.444, PC1 69.3% — exactly consistent
with the equicorrelation identity (1+2ρ̄)/3 — pool $1,023B, ratio 0.419).

## 12. Results as of 2026-07-10/11 (perishable — regenerate before use)

| | Price | PW fair value | MC p50 | P(FV>price) | implied bull WACC vs CAPM |
|---|---|---|---|---|---|
| MU | $979.30 | $389 | $301 | 5.5% | 10.5% vs 11.7% |
| NVDA | $210.96 | $77 | $69 | 0.0% | 8.8% vs 12.4% |
| AMD | $557.89 | $95 | $78 | 0.0% | 5.6% vs 11.9% |

Event cards: AMD Aug-4 ±9.8% implied (1.34× history), NVDA Aug-26 ±6.4% (1.20×), MU Sep-23
±11.2% (2.08× — rich even after the elevated baseline). Complex: implied steady MU/NVDA
ratio ~0.42 in all tiers vs 0.17 last-closed-FY actual; joint-bull requires ~$1,023B/yr AI
capex; effective breadth 1.44. MU alone additionally carries: the normalized bracket $76–106,
P/B 15.2× vs a 1.45× fifteen-year median, RV20 118% (p98), 40% idiosyncratic variance.

## 13. Kill criteria (pre-committed)

1. **Rule zero:** cited in ≥1 graded pre-registration within 14 days of build — the AMD
   Aug-4 card is the natural first rep. Miss twice (AMD *and* NVDA prints pass uncited) →
   the tool is a museum piece; demote to on-demand and stop refreshing.
2. **Events engine calibration:** after 6 graded prints (two cycles of the three names),
   the richness verdict must show discrimination — RICH-flagged prints should realize below
   the implied move more often than IN-LINE ones. No discrimination → keep the implied-move
   line, kill the verdict line.
3. **Valuation layer:** scenario sets are re-anchored after each name's print (consensus
   moves are the trigger, not the calendar). If two consecutive re-anchors require rewriting
   the *geometry* (not the numbers) of the letters, the parameterization is wrong — redesign
   rather than patch.
4. **Complex panel:** if by Sep-30 the breadth/consistency numbers have not entered any
   sizing or hedging decision, fold `complex.py`'s table into the MU report and stop
   maintaining it separately.
5. **Hard time-bomb, flagged in code:** the scenario anchor pivot (NVDA's fy0=2027 anchors
   consensus `0y`, MU/AMD anchor `+1y`) is time-anchored to the July-2026 estimate tables
   and MUST be re-derived when any name's fiscal year rolls — first at NVDA's FY close
   (late Jan-2027). A stale pivot silently mis-anchors every NVDA scenario.

## 14. Honest limits

- **The model prices cycles; the structural break is a judgment input.** Whether HBM/custom-
  memory economics (or NVDA's platform rents, or AMD's share gains) persist is exactly what
  the scenario probabilities encode — the tool forces the judgment to be explicit; it cannot
  make it.
- **Consensus anchors are load-bearing** for the near years, and sell-side estimates are
  least reliable at cycle turns — which is when the tool matters most. The missing feed
  (estimate revision *history*) is the single highest-value upgrade.
- **CAPM cost of equity is contestable** at these betas; the whole verdict is WACC-sensitive
  (tornado shows it), which is why the reverse-DCF implied-WACC framing exists — it converts
  the dispute into one comparable number instead of hiding it in the discount rate.
- **History starts FY2011** (EDGAR geo-block; macrotrends free window): two full cycles, no
  2001/2008. **No segment split** (DRAM/NAND/HBM; DC vs client): blended lines only.
- **AMD mixes street-basis consensus with GAAP history** (handled via tangible-only D&A;
  residual imprecision acknowledged). **Options are delayed quotes** and the event
  extraction approximates a dealer's event mark. **Dilution/stub/NWC are one-parameter
  approximations** worth ±$10–25/share each — small next to scenario spread.
- **The capex-pool bridge is parametric context** (accelerator share, AMD DC share are
  assumptions; the $725B pool is a desk research figure as of Jul-2026), not measurement.
- **Fair value is not a price path.** Nothing here times anything; a stock can trade at
  multiples of model fair value for years. The bridge to the tape is the reverse-DCF and the
  event cards, deliberately.

## 15. Relationships

- Tool docs (how to run, plain-language model guide): [`tools/muval/README.md`](../../tools/muval/README.md)
- The same three names' *flow* instrument (positioning/pressure, vs this page's *value/vol*):
  [Semis Institutional-Flow Map](semis-institutional-flow-map.md) — §11 is the same
  MU/NVDA/AMD scoping decision, one day earlier.
- Where this sits in the desk's capability map: The Alpha Benchmark
  (verification-first doctrine; this build is a "verification asset," not a signal).
- Complex-wide fundamental state the scenarios lean on: [Semis/AI state of play 2026-07-09](../market-research/semis-ai-state-of-play-2026-07-09.md)
  (hyperscaler capex $725B; the circular-financing/Cisco-analog risk that became NVDA-C).
- Volatility methods background: [volatility forecasting](../ml-stats/concepts/volatility-forecasting.md).

## 16. Open questions

- **Estimate-revision history:** any free/cheap path to consensus *time series* (the
  "what's priced in" drift)? Without it, reverse-DCF is a snapshot, not a track.
- **Segment build:** if an EDGAR access path appears (proxy/mirror), the 10-K segment
  tables enable per-segment scenarios — the biggest single upgrade to MU's model.
- **Grading loop:** the queued next slice — grade each dated valuation/events JSON against
  realized outcomes (implied vs realized move per print; fair-value drift vs price). Small
  build, converts the tool from opinions to a track record.
- **Fourth column:** does SMH belong in the complex report as a benchmark column (the
  "just buy the ETF" alternative the breadth number implies)?
