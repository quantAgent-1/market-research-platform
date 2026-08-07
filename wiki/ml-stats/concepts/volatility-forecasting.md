---
type: concept
title: Volatility Forecasting — The Predictable Second Moment
description: Direction is close to unforecastable at most horizons; volatility is the exception — clustering is the most robust stylized fact in financial econometrics. The stylized facts (persistence, the leverage effect, mean reversion, long memory); the model canon (EWMA/GARCH(1,1), asymmetric EGARCH/GJR, HAR-RV as the practical standard, implied vol as a biased-high forecast net of the volatility risk premium, regime models with the naive-gate caveat); what the forecast is actually FOR (vol targeting, vol-managed momentum, sizing, event pre-staging, the vol-control re-leverage clock); and the honest limits (no direction, no jump timing, quiet-body calibration understates regime shifts, crash-timing models fail out of sample). Division of labor: RV estimators and vol cones live on the derivatives measurement page.
tags: [ml-stats, systematic-trading, derivatives, volatility, risk, forecasting]
timestamp: 2026-07-07T00:00:00Z
status: active
sources: []
---

# Volatility Forecasting — The Predictable Second Moment

Almost nothing about future returns is reliably forecastable, but volatility is the standing
exception. Volatility **clusters**: quiet days follow quiet days, violent days follow violent
days, and today's realized volatility predicts next week's with real statistical power. This is
arguably the most robust stylized fact in financial econometrics, and it is the reason a
disciplined system can say "expect 3–5% daily ranges for the next two weeks" with confidence
while remaining honestly agnostic about direction. This page covers the facts, the standard
models, what the forecast is actually *for*, and the limits that keep it honest.

**Division of labor:** this page is the *forecasting-and-uses* side. The *measurement* side —
the realized-vol estimator zoo (close-to-close, Parkinson, Garman–Klass, Rogers–Satchell,
Yang–Zhang) and volatility cones — lives on
[volatility measurement & forecasting](../../derivatives/concepts/volatility-measurement-forecasting.md)
(Sinclair Ch. 2) and is not duplicated here.

## The stylized facts the models exploit

- **Persistence (clustering).** Volatility is strongly autocorrelated at daily-to-monthly lags —
  first noted by Mandelbrot (1963): "large changes tend to be followed by large changes, of
  either sign." The *sign* is what stays unpredictable.
- **The leverage effect (asymmetry).** Negative returns raise future volatility more than
  positive returns of the same size (Black 1976). Down moves are vol events; melt-ups usually
  are not.
- **Mean reversion on weeks-to-months.** Vol spikes decay toward a long-run level; the decay
  rate is estimable, which is what makes the vol-control re-leverage clock schedulable
  ([multi-week unwinds & recoveries](../../shared/concepts/multi-week-unwinds-and-recoveries.md)).
- **Long memory.** The autocorrelation decays slowly — daily, weekly, and monthly components
  all carry information, which is precisely the structure HAR exploits.
- **Fat tails and jumps.** Returns standardized by *forecast* vol are much closer to normal than
  raw returns, but jumps remain: the models forecast the diffusion well and the spark poorly.

## The model canon

**EWMA and GARCH(1,1) — the workhorses.** The ARCH family (Engle 1982; Bollerslev's GARCH 1986)
models conditional variance as a function of yesterday's shock and yesterday's variance.
GARCH(1,1) remains the baseline everything else is judged against; RiskMetrics-style EWMA is its
zero-intercept simplification. The **asymmetric variants** — EGARCH (Nelson 1991) and GJR-GARCH
(1993) — add the leverage effect and are the right default for equities.

**HAR-RV — the practical standard.** With a realized-vol series in hand, Corsi's (2009)
Heterogeneous AutoRegression forecasts tomorrow's RV from the averages of the last day, week,
and month of RV. It is embarrassingly simple — one OLS regression — and consistently hard to
beat; the [alpha model book](../../systematic-trading/models/alpha-model-book.md) grades it
production-as-is. True RV wants intraday data, but the HAR *structure* works on any decent vol
proxy: with daily OHLCV only, feed it a range-based estimator (Parkinson/Garman–Klass/Yang–Zhang
— see the [measurement page](../../derivatives/concepts/volatility-measurement-forecasting.md)),
which recovers much of the efficiency intraday data would provide. That combination is the
natural fit for a free-daily-data stack like enginev3's.

**Implied volatility — the market's forecast, biased high on purpose.** IV aggregates the
market's vol expectation *plus* the
[volatility risk premium](../../derivatives/concepts/volatility-risk-premium.md): implied
systematically exceeds subsequently realized vol because hedgers pay for insurance. So IV is a
strong but *biased-high* forecast — useful raw as a state variable (VIX level and term
structure), better calibrated net of the premium
([implied vs. realized volatility](../../derivatives/concepts/implied-vs-realized-volatility.md)).
The term structure also prices **known event dates** directly — earnings and macro prints show
up as bumps — which is the options market doing event-time vol forecasting for you.

**Regime models — persistence at the state level.** Markov-switching models (Hamilton 1989) and
HMMs classify calm-vs-stressed states that persist, which is a coarser but robust form of the
same persistence fact ([regime detection](regime-detection.md)). Carry the
[model book's](../../systematic-trading/models/alpha-model-book.md) verified caveat: as a
*classifier feeding sizing* the approach is sound; as a naive standalone trading gate it is
oversold.

**ML extensions.** Tree ensembles and neural forecasters add modest, real gains over HAR in
most horse races — mostly by exploiting the same persistence plus cross-asset spillovers. The
marginal value is small relative to getting the uses right, which is where the actual money is.

## What the forecast is for

The point of a vol forecast is almost never the number itself — it is the **dial it turns**:

- **Volatility targeting (the sizing dial).** Scale position size inversely to forecast vol.
  Harvey et al. (2018) show vol targeting improves Sharpe and, more importantly, cuts left-tail
  severity across risk assets — precisely because crashes cluster in high-vol states, when a
  vol-targeted book is already small. This is the most evidence-backed risk tool available for
  high-beta exposure ([regime detection](regime-detection.md)).
- **Vol-managed factor exposure.** The same scaling applied to momentum roughly doubles its
  alpha and Sharpe (Daniel–Moskowitz 2016), because momentum's crashes concentrate in
  post-decline, high-vol states.
- **Survival arithmetic.** Position sizing per [risk of ruin](../../shared/concepts/risk-of-ruin.md)
  and fractional [Kelly](../../shared/concepts/kelly-criterion.md) needs a vol input; a
  clustered-vol world means yesterday's estimate is materially better than a long-run average.
- **Event pre-staging.** The catalyst calendar plus the IV term structure tells you *when*
  ranges will be wide before they are — the "expect a violent two-way move this week" half of
  the [monitoring system's](../../synthesis/semiconductor-monitoring-system.md) output.
- **Reading the mechanical flows.** Vol-control and risk-parity exposure is a near-deterministic
  function of the realized-vol path, so a vol forecast doubles as a forecast of *their* buying
  and selling — the most schedulable flow in an unwind's recovery sequence
  ([multi-week unwinds & recoveries](../../shared/concepts/multi-week-unwinds-and-recoveries.md)).

## The limits (carry these, or the forecast lies to you)

1. **It forecasts dispersion, never direction.** The first moment is not in the model. A vol
   forecast is a conditional density width, not an event call.
2. **Jumps and sparks are not timed.** The models forecast the diffusive component well; the
   headline that starts the move (a Meta Compute, a false tweet) arrives unannounced. After the
   jump, the models catch up fast — that is the clustering — but the jump itself is the
   unforecastable part.
3. **Quiet-body calibration understates regime shifts.** A GARCH fit to calm data mechanically
   understates the tail regime — the Mandelbrot point that the tail is generated by a different
   process ([navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md)). Use
   the forecast as a *dial*, never as a guarantee of the worst case; survival is set at the
   sizing layer.
4. **Skill decays with horizon.** Days-to-weeks forecasts are good; quarterly forecasts revert
   to the unconditional mean and add little.
5. **A vol forecast is not a crash predictor.** Elevated vol raises the odds of large moves *in
   both directions* (crashes coincide with rebounds — the momentum-crash literature). The
   crash-*timing* genre (log-periodic/LPPL-style models) has not survived out of sample; treat
   it as history, not tooling.

## Worked anchor — July 2026 semis

After the July 1–2, 2026 sessions (SOX −6.3% then −6.7%, Samsung −9.1%, SK Hynix −14.6%), any
competent vol model said the same thing: elevated ranges in the complex for days to weeks, with
decay toward normal only as the tape calmed. That forecast could not say whether the next 5%
would be up or down — Korea's July 3 session answered *up*, violently — but it correctly set the
two things a trader controls: position size for the week (smaller), and the vol-control
re-leverage clock (buy-side flow returning as realized vol decayed). That is the entire promise
of this page in one episode: **the weather, not the lightning.**

## Relationships

- **Measurement side (estimators, cones):**
  [volatility measurement & forecasting](../../derivatives/concepts/volatility-measurement-forecasting.md) ·
  [implied vs. realized volatility](../../derivatives/concepts/implied-vs-realized-volatility.md) ·
  [volatility risk premium](../../derivatives/concepts/volatility-risk-premium.md).
- **State-level persistence:** [regime detection](regime-detection.md); production grading of
  HAR-RV and the Hamilton-gate caveat: [alpha model book](../../systematic-trading/models/alpha-model-book.md).
- **Where the forecast plugs into events:**
  [multi-week unwinds & recoveries](../../shared/concepts/multi-week-unwinds-and-recoveries.md) ·
  [liquidity cascades & V-reversals](../../shared/concepts/liquidity-cascades-and-v-reversals.md) ·
  [semiconductor monitoring system](../../synthesis/semiconductor-monitoring-system.md).
- **The sizing consumers:** [risk of ruin](../../shared/concepts/risk-of-ruin.md) ·
  [Kelly criterion](../../shared/concepts/kelly-criterion.md) ·
  [performance metrics](performance-metrics.md).
- **The philosophy of what may be forecast at all:**
  [navigating nonlinear markets](../../synthesis/navigating-nonlinear-markets.md).

## Open questions

- HAR on range-based vol proxies over the enginev3 universe: how much forecast accuracy is lost
  versus intraday RV, and does an asymmetric-GARCH baseline beat it on daily-only data?
- Does vol targeting survive transaction costs at small-account scale, and at what rebalance
  cadence (daily vs weekly) does the net benefit peak?
- Regime-conditional vol targets (different target vol per detected state): real improvement or
  double-counting the same persistence?
