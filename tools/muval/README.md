# muval — valuation & risk models for the AI-silicon complex (MU / NVDA / AMD)

muval started as a Micron-only model and has grown into a small three-name complex: Micron (MU),
Nvidia (NVDA), and AMD. For each name it answers two questions: what the stock is actually worth,
and what today's price already assumes has to be true about the future. For Micron — the original
and still the most fully built-out name — it answers a third: what is likely to move the price
from here, in which direction, and how violently. Two companion scripts extend the same machinery
across names: `events.py` builds pre-earnings cards for all three, and `complex.py` builds the
cross-name report that treats the trio as one trade.

Everything runs off the same pulled data and the same assumptions file, so changing one input
updates everything consistently instead of leaving separate spreadsheets out of sync. Every
valuation lever — each name's scenario revenue and margin paths, the discount-rate inputs, the
terminal growth rate, the Monte Carlo jitter widths — lives in one file, `assumptions.toml`, with
each number commented against the historical data point it is anchored to. The file is namespaced
per name: `[names.<TICKER>]` holds each company's fiscal calendar (Micron's fiscal year ends in
late August; Nvidia's ends in late January, so its "current" fiscal year is FY2027; AMD reports on
the calendar year), and `[scenarios.<TICKER>.A/B/C]`, `[cash_mechanics.<TICKER>]`, and
`[normalized.<TICKER>]` hold the per-name assumptions, while the global sections (WACC inputs,
terminal value, Monte Carlo settings) apply to all names. Nothing is hardcoded in the Python: edit
a number, re-run offline, and the model reprices with no new data pull.

## Running it

```
python tools/muval/muval.py               # MU: pull (cached), model, report, open in browser
python tools/muval/muval.py --offline     # caches only, no network
python tools/muval/muval.py --refresh     # force re-pull all feeds
python tools/muval/muval.py --no-open     # skip opening the browser
python tools/muval/muval.py --name NVDA   # valuation-only brief + JSON for NVDA (or --name AMD)
python tools/muval/muval.py selftest      # offline arithmetic checks (DCF vs closed form, GARCH recovery, Yang-Zhang)

python tools/muval/events.py              # pre-earnings cards, all three names (cached-first)
python tools/muval/complex.py             # cross-name complex report, all three names
```

Plain `python tools/muval/muval.py` runs Micron end to end: it pulls each feed only if its on-disk
cache has gone stale (see the freshness column below), builds the model, writes the full HTML
report, and opens it in the default browser. `--offline` refuses to touch the network at all and
fails if a required cache file is missing — use it once the caches are warm, to iterate on
`assumptions.toml` without waiting on data pulls. `--refresh` ignores cache freshness and re-pulls
everything. `--no-open` skips the browser step, for scripted runs.

`--name NVDA` (or `--name AMD`) runs the same scenario-DCF, reverse-DCF, and Monte Carlo machinery
for that name instead. These runs are valuation-only: they print a console brief and write
`store/valuation-<TICKER>-<date>.json`, but the volatility/factor risk block and the full HTML
report remain Micron-only for now. `events.py` and `complex.py` accept the same `--offline` and
`--refresh` flags as `muval.py` and are cached-first by default.

`selftest` runs a handful of offline arithmetic checks — does the DCF collapse to the textbook
closed-form answer for a flat perpetuity, does a GARCH fit recover known parameters from synthetic
data, does the Yang-Zhang volatility estimator recover the true volatility of a simulated price
path — and prints `PASS` or `FAIL` with no network access and no cache required.

A first pull against a cold cache takes roughly one to two minutes per name. Most of that time is
macrotrends.net, which is rate-limited: the tool pulls thirteen separate pages of annual history
per name (revenue, margins, capex, equity, shares, and so on) with a 1.5-second pause between
requests to stay polite to the site. Once the caches are warm, an offline valuation run takes
about thirty to sixty seconds per name, dominated by the Monte Carlo step, which reprices the
model twenty thousand times to build a fair-value distribution rather than a single point
estimate.

A Micron run writes `store/report.html` (the full report, self-contained, every chart embedded as
an inline image so it opens fine straight from disk), `store/valuation-<date>.json` (a
machine-readable snapshot of that run's numbers, meant as the record to grade the model's calls
against later), and a console brief. NVDA/AMD runs write the console brief and their
`store/valuation-<TICKER>-<date>.json` snapshot. `events.py` writes `store/events-<date>.html` and
`store/events-<date>.json` plus console cards; `complex.py` writes `store/complex-report.html` and
`store/complex-<date>.json`.

## Where the data comes from

Everything muval pulls is free, and all of it is cached to disk per name, so a normal run only
re-downloads what has gone stale. The shared price panel covers twelve tickers: Micron itself; SMH
and SPY as the semiconductor-sector and broad-market benchmarks; the VIX (the market's own
volatility gauge) and the 10-year Treasury yield as macro context; the dollar index; Western
Digital and Seagate as the storage-peer comparison; Taiwan Semiconductor's US-listed shares and
Nvidia as supply-chain neighbors; and Samsung Electronics and SK Hynix, Micron's two direct
memory-chip competitors, both listed in Seoul. AMD's price history is pulled separately when
needed — thirteen price histories in all.

| feed | source | freshness | what it feeds |
|---|---|---|---|
| Prices, 13 tickers, up to 40 years of daily OHLCV (open/high/low/close/volume) | Yahoo Finance (`yfinance`) | cached 1 day | returns, betas, the volatility cone, tail statistics |
| Financial statements per name (5 years annual plus the last 5 quarters), analyst estimates (roughly 30-40 analysts per estimate line), ~50 past earnings dates | Yahoo Finance (`yfinance`) | cached 3 days | boom-year cash mechanics, the near-fiscal-year anchor numbers, the earnings-reaction studies |
| Annual fundamentals per name, FY2011 onward (revenue, margins, capex, equity, shares) | macrotrends.net | cached 14 days | the long-run revenue trend, mid-cycle margins, past cycle drawdowns, price-to-book history |
| Option chain per name (Micron's is roughly 13,500 contracts) | CBOE delayed quotes (JSON feed) | cached 1 day | at-the-money implied-volatility term structure, the 25-delta skew, the implied earnings-day move |
| 10-year Treasury yield | FRED, series DGS10 | cached 1 day | the risk-free rate used in the discount rate |

SEC EDGAR — normally the most authoritative source for financial statements — is geo-blocked from
this machine: its servers return an HTTP 403 to non-US IP addresses. That is why macrotrends.net's
scraped history stands in for it. Treat that long history as a good, but unofficial, substitute —
see honest limits below.

## The model, in brief

### Valuation (all three names): what it's worth, and what the price implies

For each name the model builds three explicit scenarios for revenue, margins, and cash flow, year
by year, out to ten fiscal years past the current one. The shape is always the same — A is the
bull case, B the base case, C the bear case — but the content is per name, set in
`assumptions.toml`. For Micron: A, the AI-driven memory rents persist and Micron keeps something
closer to a logic-chip company's margins; B (base), the supercycle is real but memory stays
cyclical underneath — a normal correction follows, landing at a plateau permanently higher than
the pre-AI era; C, competitors catch up and the premium collapses back toward commodity economics.
Nvidia's trio runs from "platform monopoly compounds" through "AI-capex digestion cycle" to a
"Cisco analog" unwind; AMD's from "credible second source at scale" through "structural #2, still
cyclical" to "squeezed between Nvidia and custom silicon." Each scenario carries a pre-set
probability weight (Micron 25/45/30 for A/B/C; Nvidia and AMD 30/45/25) so the three blend into
one probability-weighted fair value per name.

Each scenario's cash flow is discounted at the WACC — the weighted average cost of capital, the
blended required return of a company's equity and debt holders, and the standard discount rate for
a DCF (discounted cash flow model: the standard technique of projecting future free cash flow and
converting that stream into one value today). The cost-of-equity piece comes from CAPM, the capital
asset pricing model: the risk-free rate — here, the live 10-year Treasury yield — plus the name's
beta times the equity risk premium. Beta measures how much a stock swings relative to the overall
market; muval computes it per name from 5 years of weekly returns, then "Blume-shrinks" it
two-thirds of the way toward 1.0, a standard correction because raw historical betas tend to be
too extreme as predictors of future beta.

Cash flow beyond the explicit horizon is capitalized with a Gordon terminal value, the standard
formula for "this cash flow stream, growing at a constant modest rate, forever." That is
cross-checked against a second method — a fixed exit EV/EBITDA multiple (enterprise value to
EBITDA, a common trading multiple) applied to the terminal year — so the model doesn't rely on the
growing-perpetuity formula alone.

The reverse DCF runs the same machinery backwards. Instead of producing a fair value, it takes
today's actual price and solves for the assumption that would justify it, several independent
ways: as a perpetual owner-earnings yield (what constant, forever cash flow per share the market's
price is equivalent to); as the steady-state net margin the company would need to sustain forever,
layered on the bull-case (A) revenue path, for the DCF to equal the price; and as the discount
rate that would make the bull case worth exactly today's price at its own assumptions. Each solve
can also come back "unreachable" — no margin up to 90%, or no plausible discount rate, gets there —
and that is itself the informative answer: it says which kind of assumption the price is actually
resting on. A reverse DCF is usually the more useful direction in practice, because it turns a
vague feeling ("this looks expensive") into a specific, checkable claim about the future.

A single DCF number hides how much uncertainty is baked into the inputs, so muval also runs a Monte
Carlo simulation per name: twenty thousand simulated draws, each one randomly picking a scenario by
its probability weight and then jittering the key inputs (next-fiscal-year revenue, trough depth,
plateau level, steady-state margin, WACC, terminal growth) by a small random amount, and computing
the DCF fair value for that draw. The output is a distribution rather than a single number, which
is what lets the report state where today's actual price falls within the range of simulated fair
values — for example, above the 94th percentile of them, meaning expensive relative to almost
everything the model considers plausible — instead of implying false precision with one point
estimate.

Two more checks round out the valuation side. A normalized, through-cycle bracket answers "what is
this company worth if the AI structural break isn't real at all" — it puts revenue back on its
pre-AI trend line, applies a historical mid-cycle net margin, and (for Micron) adds a justified
price-to-book cross-check (a price-to-book ratio derived from normalized return on equity, growth,
and the discount rate), giving a deliberately cold floor-case value. And a tornado chart ranks
every input by how much it swings the base-case fair value when moved up or down one at a time —
the fastest way to see which two or three assumptions actually matter.

### Risk and volatility (Micron only, for now)

The risk engine estimates how much Micron actually moves using several realized-volatility
estimators, which differ in how much of each day's price action they use. The simplest,
close-to-close, only looks at the closing price each day. Yang-Zhang, the estimator used most in
the report, combines the open, high, low, and close and separately accounts for overnight jumps
versus intraday range — a more efficient, lower-noise estimate of true volatility than
close-to-close alone.

On top of that backward-looking measure, muval fits a GARCH(1,1) model — a standard time-series
model in which today's variance is a weighted combination of yesterday's variance and yesterday's
squared surprise, a compact way of capturing "volatility clusters: calm periods and turbulent
periods each tend to persist." Its three parameters are fit by maximum likelihood (the standard
statistical procedure for choosing the values that make the observed data most probable) on ten
years of daily returns, giving both a current one-month-ahead volatility forecast and a long-run
level the forecast decays toward. A ten-year vol cone then shows where today's realized volatility,
at several time horizons, sits against its own historical percentile range — the chart that answers
"is now unusually calm or unusually wild, compared to this stock's own history."

To separate what kind of risk this is from how much risk it is, a factor regression decomposes
Micron's daily returns into a loading on the broad market (the S&P 500), a loading on the
semiconductor sector beyond the market, a loading on interest-rate changes, a loading on the
dollar, and whatever's left over — the Micron-specific piece that doesn't hedge away with any
index. The regression's standard errors use the Newey-West correction, which accounts for daily
stock-return noise not being perfectly independent day to day; without it, the t-statistics (a
signal-to-noise ratio: roughly, how many standard errors a coefficient sits away from zero) would
overstate how confident the model should be in each factor loading.

An earnings-day study measures the actual next-day price reaction across roughly the last 50
reports: the average size of the move, how often it's up versus down, and what share of the
stock's total variance over that whole span is concentrated into just those handful of days.
Alongside it, a read of the CBOE option chain backs out the market's own forecast for the next
earnings move: it takes the difference in variance priced into the at-the-money options (options
with a strike price closest to today's stock price) expiring just before versus just after the
report, nets out a baseline volatility level implied by far-dated options, and also reads the
25-delta skew — the gap in implied volatility between downside and upside options a set distance
from the money, which reflects how much extra the market pays for crash protection versus upside
calls. This is an approximation of the "pure event" volatility the market is pricing, not an exact
replica of how a market maker marks it.

Finally, a Korea lead-lag check correlates Micron's returns against Samsung Electronics and SK
Hynix in both directions. Seoul's market closes about fourteen hours before New York opens, so a
same-calendar-date correlation captures information that was already public before the US trading
day even began.

## Pre-earnings cards (`events.py`)

`events.py` takes the earnings-move slice of the risk engine and runs it for all three names at
once, producing one card per name ahead of its next report. Each card shows when the next print
lands and the consensus estimates for it; the options-implied plus-or-minus one-standard-deviation
move for the event, extracted by the forward-variance differencing described above (the variance
gap between the option expiries bracketing the print, with far-dated implied volatility as the
baseline for ordinary non-event days); and the name's actual historical earnings-day behavior —
mean, median, and worst next-day reactions, and the last eight prints in detail.

The card's verdict is a computed richness ratio: the implied event move divided by the median
historical absolute move. Below 0.8, the options market is pricing the event cheap against the
name's own history; between 0.8 and 1.25, in line; above 1.25, rich. The cards flag two situations
where that read deserves less trust: when no option expiry actually brackets the print, the tool
falls back to a plain straddle read (the combined price of the at-the-money call and put), which
bakes in ordinary background volatility and therefore biases the richness high; and when a name's
current realized volatility sits above its own ten-year 90th percentile, history itself may
understate what a "normal" move now looks like. Output goes to the console as ASCII cards, plus
`store/events-<date>.html` and `store/events-<date>.json`.

## The complex report (`complex.py`)

`complex.py` runs the valuation machinery for all three names and builds the cross-name analysis —
the layer where the three names stop being separate models and become one picture. It produces a
comparison table (each name's scenario fair values and probability-weighted value against its
price, and the price-implied discount rate on the bull path next to the CAPM-derived WACC — the
cleanest single number for "how much optimism is in this price"); mini football fields per name (a
football field is the standard valuation chart: each method's value range drawn as a horizontal
bar, with the current price as a line across them); a Micron-to-Nvidia revenue-ratio consistency
check, which asks whether the two names' scenario paths, taken together, imply a revenue
relationship the two companies have never actually exhibited; a parametric AI-capex-pool bridge,
which translates an assumed total AI-datacenter spending pool into what each name's scenario
revenue would claim as a share of it — labeled clearly as parametric context (the pool size is an
input you set, not data the tool pulls); and a correlation and effective-breadth block, which
measures how correlated the three names' returns actually are and therefore how many independent
bets the trio really represents — three names this correlated are closer to one bet than three.
Output: `store/complex-report.html` and `store/complex-<date>.json`.

## What a run looks like

Every number below regenerates on every run and will already have drifted since it was written;
read this as an illustration of what the tool produces, not a current valuation. As of 2026-07-10,
with Micron trading at $979.30:

The three Micron scenario DCFs came out at $866 (A), $314 (B), and $105 (C), blending to a
probability-weighted fair value of $389. The Monte Carlo simulation put the median simulated fair
value at $301: only 5.5% of the twenty thousand simulated fair-value draws came out above today's
actual price, so the price sat above roughly 95% of what the model considered a plausible fair
value.

The reverse DCF said the price was equivalent to any of: perpetual owner earnings of $88 per share,
forever; the bull (A) revenue path combined with a roughly 45% net margin held forever (versus a
15-year historical median of about 18%, and a best-ever single year of about 47%); or the bull path
at a 10.5% discount rate (versus the model's own computed WACC of about 11.7%). On the base-case
(B) revenue geometry, the price was unreachable at any economically plausible margin — it could
only be justified by the revenue supercycle itself persisting, not by margin assumptions on top of
a normal cycle correction.

The same machinery read the other two names as pricing in even more: Nvidia's scenarios came out
at $130 / $68 / $28 (probability-weighted $77) against a $210.96 price, which back-solves to the
bull path discounted at 8.8% versus a 12.4% model WACC — on the bull path's own margins, no margin
assumption alone reaches the price. AMD's came out at $173 / $76 / $34 (probability-weighted $95)
against $557.89, an implied bull-path discount rate of 5.6% versus 11.9% — the most optimism-laden
price of the three by this yardstick.

On the volatility side, Micron's 20-day realized volatility was 118% annualized — the 98th
percentile of its own 10-year range. The GARCH model's one-month-ahead forecast was 91%, below the
current realized level, implying some expected cooling even without new information. Implied
volatility (the 30-day point on the options curve) was around 94%, and the options market was
pricing roughly a plus-or-minus 11% one-standard-deviation move around the 2026-09-23 earnings
report — about twice Micron's median historical earnings-day move, which the events card called
rich.

## Honest limits

- **The model prices cycles; it cannot price the structural break itself.** Whether HBM
  (high-bandwidth memory, the chip stacked into AI accelerators), custom-memory economics, and the
  AI-capex boom are a permanent step-change or just an unusually long upswing is the entire
  question — and the model treats it as a judgment input (the scenario probabilities), not
  something it derives. The tool's job is to force that judgment to be explicit and price its
  consequences honestly, not to resolve it.
- **The near-term numbers lean on sell-side consensus.** The current and next fiscal year's revenue
  and EPS come from the analyst-estimate feed. Sell-side estimates are historically least reliable
  exactly at cycle turns, which is when they matter most — an error there flows straight into the
  model's anchor points.
- **The fundamentals history starts at FY2011.** SEC EDGAR, which would go back further, is
  geo-blocked from this machine, so macrotrends.net's scraped history is the substitute. FY2011
  onward covers two full memory cycles and the modern three-supplier oligopoly (Micron, Samsung, SK
  Hynix), but not the 2001 dot-com bust or the 2008 financial crisis.
- **No segment splits.** Micron's DRAM/NAND/HBM mix — and equally Nvidia's data-center versus
  everything else — is not modeled separately; scenarios move one blended revenue-and-margin line
  per name. A true per-segment build would need 10-K segment tables (blocked from this machine) or
  manual data entry.
- **AMD's consensus EPS is street-basis, not GAAP.** Analysts quote AMD's earnings excluding the
  large intangible-amortization charge from the Xilinx acquisition, so AMD's reported GAAP profits
  run well below the consensus the model anchors on. To avoid double-counting that add-back, the
  model uses tangible-only depreciation for AMD's cash mechanics — a documented approximation
  (flagged in `assumptions.toml`), and the GAAP-versus-street gap is a stated limit for this name.
- **The options data is delayed, and the earnings-move extraction is an approximation.** The CBOE
  feed is delayed, not live, and the implied earnings-day move is backed out algebraically rather
  than read directly off a market maker's own event-volatility mark.
- **A few cash-flow mechanics are simplified.** Annual share dilution, buybacks, and the
  current-fiscal-year stub are modeled with simple approximations rather than a full
  capital-structure build. Each is individually worth on the order of $10-25 per share — small next
  to the spread between scenarios, but not zero.
- **A fair-value estimate is not a price target or a timing signal.** Nothing in the model says
  when, or whether, a price will move toward its computed fair value; a stock can trade at
  multiples of fair value for years. The reverse-DCF section is the intended bridge between what the
  model says and what the tape is actually doing.

## A note on the console

This machine's Windows console uses the cp949 code page (a Korean-language encoding), which cannot
print every Unicode character — an em dash, for instance. muval prints ASCII-safe console output
for that reason, while every file it writes to disk (the HTML reports, the JSON snapshots) is UTF-8
regardless.
