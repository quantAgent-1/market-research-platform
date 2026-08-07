"""muval.fundamentals — assemble statements into analysis frames + cycle analytics.

Everything downstream (valuation scenarios, normalized earnings) keys off what this
module computes from data: the revenue trend, margin percentiles, cycle drawdowns,
capex intensity, FCF conversion. No hand-typed history.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def annual_frame(mt: dict, yf: dict) -> pd.DataFrame:
    """Long annual frame from macrotrends ($M), FY-indexed (MU fiscal year ends
    late Aug / early Sep; macrotrends year N = FY ending Aug N)."""
    metrics = ["revenue", "gross_profit", "operating_income", "net_income",
               "eps_diluted", "shares_outstanding", "equity", "dna", "rnd",
               "cfo", "fcf", "inventory", "long_term_debt"]
    years = sorted({int(y) for m in metrics for y in mt.get(m, {})})
    df = pd.DataFrame(index=years)
    for m in metrics:
        df[m] = [mt.get(m, {}).get(str(y), np.nan) for y in years]
    df["capex"] = df["cfo"] - df["fcf"]  # macrotrends FCF = CFO - capex
    df["gm"] = df["gross_profit"] / df["revenue"]
    df["om"] = df["operating_income"] / df["revenue"]
    df["nm"] = df["net_income"] / df["revenue"]
    df["fcf_margin"] = df["fcf"] / df["revenue"]
    df["capex_pct"] = df["capex"] / df["revenue"]
    df["dna_pct"] = df["dna"] / df["revenue"]
    df["bvps"] = df["equity"] / df["shares_outstanding"]
    df["roe"] = df["net_income"] / df["equity"]
    df["rev_yoy"] = df["revenue"].pct_change()
    df["inv_days"] = df["inventory"] / (df["revenue"] - df["gross_profit"]) * 365
    return df


def consensus(yf: dict) -> dict:
    """Analyst anchors: current + next FY revenue/EPS, next two quarters."""
    rev = yf.get("revenue_estimate", {})
    eps = yf.get("earnings_estimate", {})

    def g(d, period, field="avg"):
        row = d.get(period, {})
        v = row.get(field)
        return float(v) if v is not None else None

    out = {
        "rev_fy0": g(rev, "0y"), "rev_fy1": g(rev, "+1y"),
        "rev_fy0_low": g(rev, "0y", "low"), "rev_fy0_high": g(rev, "0y", "high"),
        "rev_fy1_low": g(rev, "+1y", "low"), "rev_fy1_high": g(rev, "+1y", "high"),
        "eps_fy0": g(eps, "0y"), "eps_fy1": g(eps, "+1y"),
        "eps_fy0_low": g(eps, "0y", "low"), "eps_fy0_high": g(eps, "0y", "high"),
        "eps_fy1_low": g(eps, "+1y", "low"), "eps_fy1_high": g(eps, "+1y", "high"),
        "rev_q0": g(rev, "0q"), "rev_q1": g(rev, "+1q"),
        "eps_q0": g(eps, "0q"), "eps_q1": g(eps, "+1q"),
        "n_analysts": g(eps, "+1y", "numberOfAnalysts"),
    }
    return out


def quarterly_frame(yf: dict) -> pd.DataFrame:
    """Recent quarterly income statement (5 quarters from yfinance)."""
    inc = yf.get("income_quarterly", {})
    rows = []
    for dt, d in sorted(inc.items()):
        rows.append({
            "qtr_end": dt,
            "revenue": d.get("TotalRevenue"),
            "gross_profit": d.get("GrossProfit"),
            "op_income": d.get("OperatingIncome"),
            "net_income": d.get("NetIncome"),
            "eps_diluted": d.get("DilutedEPS"),
        })
    df = pd.DataFrame(rows).set_index("qtr_end")
    for c in ["revenue", "gross_profit", "op_income", "net_income"]:
        df[c] = df[c] / 1e6  # $M, matching the annual frame
    df["nm"] = df["net_income"] / df["revenue"]
    df["gm"] = df["gross_profit"] / df["revenue"]
    return df


def eps_quarters(yf: dict) -> pd.DataFrame:
    """Reported quarterly EPS history from the earnings-dates feed (~6 years)."""
    rows = [r for r in yf.get("earnings_dates", []) if r.get("eps_act") is not None]
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").set_index("date")


def revenue_trend(ann: pd.DataFrame, fit_start: int, fit_end: int) -> dict:
    """Log-linear through-cycle revenue trend on actual FY data.

    Returns fitted CAGR, the trend level for any year, and the current deviation.
    """
    sub = ann.loc[(ann.index >= fit_start) & (ann.index <= fit_end), "revenue"].dropna()
    x = sub.index.values.astype(float)
    y = np.log(sub.values)
    slope, intercept = np.polyfit(x, y, 1)
    cagr = math.exp(slope) - 1
    resid = y - (slope * x + intercept)

    def level(year: float) -> float:
        return math.exp(slope * year + intercept)

    return {
        "fit_start": int(x[0]), "fit_end": int(x[-1]),
        "cagr": cagr, "slope": slope, "intercept": intercept,
        "level": level,
        "resid_sd": float(np.std(resid)),
        "dev_last": float(math.exp(resid[-1]) - 1),  # last fit-year vs trend
        "r2": float(1 - np.var(resid) / np.var(y)),
    }


def cycle_stats(ann: pd.DataFrame, window_start: int) -> dict:
    """Peak-to-trough drawdowns and margin/capex/FCF percentiles over the modern
    era (default FY2012+ = post-Elpida consolidation, the 3-supplier DRAM oligopoly)."""
    sub = ann.loc[ann.index >= window_start]
    rev = sub["revenue"].dropna()

    # revenue drawdowns: running peak, record each trough
    drawdowns = []
    peak, peak_y, trough, trough_y = -np.inf, None, np.inf, None
    in_dd = False
    for y, v in rev.items():
        if v >= peak:
            if in_dd and trough_y is not None:
                drawdowns.append({"peak_fy": int(peak_y), "trough_fy": int(trough_y),
                                  "dd": float(trough / peak - 1)})
            peak, peak_y, in_dd, trough = v, y, False, np.inf
        else:
            in_dd = True
            if v < trough:
                trough, trough_y = v, y
    if in_dd and trough_y is not None:
        drawdowns.append({"peak_fy": int(peak_y), "trough_fy": int(trough_y),
                          "dd": float(trough / peak - 1)})

    def pct(series: pd.Series) -> dict:
        s = series.dropna()
        return {"min": float(s.min()), "p25": float(s.quantile(.25)),
                "median": float(s.median()), "p75": float(s.quantile(.75)),
                "max": float(s.max())}

    return {
        "window_start": int(window_start),
        "rev_drawdowns": drawdowns,
        "gm": pct(sub["gm"]), "om": pct(sub["om"]), "nm": pct(sub["nm"]),
        "fcf_margin": pct(sub["fcf_margin"]),
        "capex_pct": pct(sub["capex_pct"]),
        "dna_pct": pct(sub["dna_pct"]),
        "roe": pct(sub["roe"]),
        "cum_fcf": float(sub["fcf"].sum()),
        "cum_ni": float(sub["net_income"].sum()),
        "fcf_conversion_cum": float(sub["fcf"].sum() / max(sub["net_income"].sum(), 1e-9)),
    }


def current_snapshot(yf: dict, px_mu: pd.DataFrame) -> dict:
    info = yf.get("info", {})
    balq = yf.get("balance_quarterly", {})
    last_bal = {}
    if balq:
        last_bal = balq[sorted(balq.keys())[-1]]
    cash = last_bal.get("CashCashEquivalentsAndShortTermInvestments") or info.get("totalCash") or 0.0
    debt = last_bal.get("TotalDebt") or info.get("totalDebt") or 0.0
    shares = info.get("impliedSharesOutstanding") or info.get("sharesOutstanding")
    price = float(px_mu["Close"].iloc[-1])
    return {
        "price": price,
        "price_date": str(px_mu.index[-1].date()),
        "shares": float(shares),
        "mcap": price * float(shares),
        "net_cash": float(cash) - float(debt),
        "cash": float(cash), "debt": float(debt),
        "book_value_ps": info.get("bookValue"),
        "trailing_eps": info.get("trailingEps"),
        "forward_eps": info.get("forwardEps"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb": info.get("priceToBook"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "target_low": info.get("targetLowPrice"),
        "target_mean": info.get("targetMeanPrice"),
        "target_high": info.get("targetHighPrice"),
        "target_median": info.get("targetMedianPrice"),
        "n_analysts": info.get("numberOfAnalystOpinions"),
        "beta_yf": info.get("beta"),
        "hi_52w": float(px_mu["Close"].iloc[-252:].max()),
        "lo_52w": float(px_mu["Close"].iloc[-252:].min()),
    }


def build(data: dict, cfg: dict, ticker: str = "MU") -> dict:
    # data["by_name"][ticker] is the multi-name shape (data.pull_all(names=...));
    # fall back to the top-level MU-shaped keys for back-compat with any caller
    # that still hands in a single-name-only data dict.
    src = data.get("by_name", {}).get(ticker) or data
    ann = annual_frame(src["macrotrends"], src["yf"])
    cons = consensus(src["yf"])
    ncfg = cfg["normalized"][ticker]
    fit_start = int(ncfg["trend_fit_start"])
    fit_end = int(ann.index.max())
    trend = revenue_trend(ann, fit_start, fit_end)
    cyc = cycle_stats(ann, int(ncfg["window_start"]))
    snap = current_snapshot(src["yf"], data["prices"][ticker])
    return {
        "annual": ann,
        "quarterly": quarterly_frame(src["yf"]),
        "eps_quarters": eps_quarters(src["yf"]),
        "consensus": cons,
        "trend": trend,
        "cycle": cyc,
        "snapshot": snap,
    }
