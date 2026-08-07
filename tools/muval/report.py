"""muval.report — console brief, JSON snapshot, and the self-contained HTML report.

Charts: matplotlib -> base64 PNG embedded inline. Palette + mark specs follow the
dataviz method (light surface #fcfcfb, categorical slots, diverging blue/red for
polarity, thin marks, solid hairline grid, tables as the accessible twin).
"""

from __future__ import annotations

import base64
import io
import json
import math
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TOOL_DIR = Path(__file__).resolve().parent
STORE = TOOL_DIR / "store"

# ---- palette (dataviz reference instance, light mode) ----
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"      # slot 1
AQUA = "#1baf7a"      # slot 2
YELLOW = "#eda100"    # slot 3
VIOLET = "#4a3aa7"    # slot 5
RED = "#e34948"       # slot 6 (also diverging warm pole)
BLUE_L = "#9ec5f4"    # sequential 200
BLUE_XL = "#cde2fb"   # sequential 100

SC_COLOR = {"A": AQUA, "B": BLUE, "C": RED}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.family": "Segoe UI",
    "text.color": INK, "axes.edgecolor": BASELINE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
    "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlelocation": "left", "axes.titlecolor": INK,
    "axes.titlesize": 11.5, "axes.titleweight": "bold",
    "font.size": 9.5, "figure.dpi": 130,
})


def _b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def img(fig, alt: str) -> str:
    return f'<img alt="{alt}" src="data:image/png;base64,{_b64(fig)}" style="max-width:100%;height:auto;">'


# ================================================================ figures ====

def fig_football(val: dict, fund: dict) -> str:
    base = val["base"]
    price = base["price"]
    snap = fund["snapshot"]
    mc = val["montecarlo"]["pct"]
    norm = val["normalized"]
    rows = [  # (label, lo, hi, point, color, note)
        ("52-week range", snap["lo_52w"], snap["hi_52w"], None, BASELINE, "market"),
        ("Sell-side targets (42 analysts)", snap["target_low"], snap["target_high"],
         snap["target_median"], MUTED, "market"),
        ("DCF scenarios C..A", val["scenarios"]["C"]["dcf"]["ps"],
         val["scenarios"]["A"]["dcf"]["ps"], val["fv_prob_weighted"], BLUE, "model"),
        ("Monte Carlo p25-p75", mc["p25"], mc["p75"], mc["p50"], BLUE_L, "model"),
        ("Monte Carlo p5-p95", mc["p5"], mc["p95"], None, BLUE_XL, "model"),
        ("Through-cycle bracket (no AI rents)", norm["lo"], norm["hi"], None, VIOLET, "model"),
    ]
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    for i, (label, lo, hi, pt, color, _) in enumerate(reversed(rows)):
        ax.barh(i, hi - lo, left=lo, height=0.52, color=color, edgecolor="none")
        if pt is not None:
            ax.plot([pt], [i], marker="D", color=INK, markersize=6, zorder=5)
    ax.axvline(price, color=INK, lw=1.6, zorder=6)
    ax.set_ylim(-0.55, len(rows) + 0.05)
    ax.text(price, len(rows) - 0.42, f"  price ${price:,.0f}", color=INK,
            fontsize=9.5, fontweight="bold", va="bottom")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=9.5, color=INK2)
    ax.set_xlabel("$ per share")
    ax.set_title("Where the price sits — model vs market anchors (diamond = central value)")
    ax.set_xlim(0, max(price, snap["target_high"], mc["p95"]) * 1.12)
    return img(fig, "football field of valuation ranges vs price")


def fig_revenue_trend(val: dict, fund: dict) -> str:
    ann = fund["annual"]
    tr = fund["trend"]
    cons = fund["consensus"]
    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    ax.plot(ann.index, ann["revenue"] / 1e3, color=BLUE, lw=2.0, marker="o",
            markersize=4, label="Revenue (actual)")
    yrs = np.arange(ann.index.min(), 2037)
    ax.plot(yrs, [tr["level"](y) / 1e3 for y in yrs], color=MUTED, lw=1.4,
            ls="--", label=f"FY12-25 trend ({tr['cagr']:.0%}/yr)")
    ax.plot([2026, 2027], [cons["rev_fy0"] / 1e9, cons["rev_fy1"] / 1e9], marker="o",
            markersize=7, mfc="white", mec=INK, lw=0, label="Consensus FY26/27")
    for k in ["A", "B", "C"]:
        p = val["scenarios"][k]["path"]
        ax.plot(p["years"], p["rev"] / 1e3, color=SC_COLOR[k], lw=1.5, alpha=0.85)
        ax.annotate(k, (p["years"][-1], p["rev"][-1] / 1e3), textcoords="offset points",
                    xytext=(6, -3), color=SC_COLOR[k], fontweight="bold", fontsize=10)
    ax.set_yscale("log")
    ax.set_yticks([10, 20, 40, 80, 160, 320])
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.set_ylabel("revenue, $B (log scale)")
    ax.set_title("Revenue: two memory cycles, then the AI-memory step change — and the three scenario paths")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "revenue history vs trend and scenario paths")


def fig_margins(fund: dict) -> str:
    ann = fund["annual"]
    cyc = fund["cycle"]
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.plot(ann.index, ann["gm"] * 100, color=BLUE, lw=2, label="Gross margin")
    ax.plot(ann.index, ann["nm"] * 100, color=VIOLET, lw=2, label="Net margin")
    ax.axhline(cyc["nm"]["median"] * 100, color=MUTED, lw=1.2, ls="--")
    ax.annotate(f"net-margin median FY12-25: {cyc['nm']['median']:.0%}",
                (ann.index.min(), cyc["nm"]["median"] * 100), textcoords="offset points",
                xytext=(0, 5), color=MUTED, fontsize=8.5)
    q = fund["quarterly"]
    if len(q):
        last_nm = q["nm"].iloc[-1] * 100
        ax.plot([ann.index.max() + 1], [last_nm], marker="*", color=INK, markersize=11)
        ax.annotate(f"latest quarter: {last_nm:.0f}%", (ann.index.max() + 1, last_nm),
                    textcoords="offset points", xytext=(-115, 2), color=INK, fontsize=9)
    ax.axhline(0, color=BASELINE, lw=1)
    ax.set_ylabel("% of revenue")
    ax.set_title("Margins: a hyper-cyclical band (net -38% to +47%) now printing all-time highs")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "gross and net margin history")


def fig_quarters(fund: dict) -> str:
    q = fund["quarterly"]
    fig, ax = plt.subplots(figsize=(9.2, 3.3))
    x = np.arange(len(q))
    ax.bar(x - 0.21, q["revenue"] / 1e3, width=0.38, color=BLUE, label="Revenue")
    ax.bar(x + 0.21, q["net_income"] / 1e3, width=0.38, color=AQUA, label="Net income")
    ax.set_xticks(x)
    ax.set_xticklabels([d[:7] for d in q.index], fontsize=9)
    for i, v in enumerate(q["revenue"] / 1e3):
        ax.annotate(f"{v:.0f}", (i - 0.21, v), textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=8.5, color=INK2)
    ax.set_ylabel("$B per quarter")
    ax.set_title("The boom in five quarters — revenue tripled, latest quarter's net income exceeds FY2025's full year")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "quarterly revenue and net income bars")


def fig_eps_paths(val: dict, fund: dict) -> str:
    cons = fund["consensus"]
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    for k in ["A", "B", "C"]:
        p = val["scenarios"][k]["path"]
        ax.plot(p["years"], p["eps"], color=SC_COLOR[k], lw=2,
                label=f"{k}: {val['scenarios'][k]['cfg']['name']}")
        ax.annotate(k, (p["years"][-1], p["eps"][-1]), textcoords="offset points",
                    xytext=(6, -3), color=SC_COLOR[k], fontweight="bold")
    ax.plot([2026, 2027], [cons["eps_fy0"], cons["eps_fy1"]], marker="o", markersize=7,
            mfc="white", mec=INK, lw=0, label="Consensus FY26/27")
    ann = fund["annual"]
    ax.plot([ann.index.max()], [ann["eps_diluted"].iloc[-1]], marker="o", color=INK, markersize=5)
    ax.annotate(f"FY25 actual ${ann['eps_diluted'].iloc[-1]:.2f}",
                (ann.index.max(), ann["eps_diluted"].iloc[-1]),
                textcoords="offset points", xytext=(-10, 8), fontsize=8.5, color=INK2)
    ax.axhline(0, color=BASELINE, lw=1)
    ax.set_ylabel("EPS, $")
    ax.set_title("Earnings per share under the three scenarios (consensus peaks at $150 in FY2027)")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    return img(fig, "scenario EPS paths")


def fig_mc(val: dict) -> str:
    mc = val["montecarlo"]
    price = val["base"]["price"]
    v = mc["values"]
    v_plot = v[v < np.percentile(v, 99.5)]
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.hist(v_plot, bins=90, color=BLUE_L, edgecolor=SURFACE, linewidth=0.4)
    ax.axvline(price, color=INK, lw=1.6)
    ax.text(price, ax.get_ylim()[1] * 0.95, f" price ${price:,.0f} = p{100 * (v < price).mean():.0f}",
            color=INK, fontweight="bold", fontsize=9.5, va="top")
    for q, lbl in [(25, "p25"), (50, "median"), (75, "p75")]:
        x = np.percentile(v, q)
        ax.axvline(x, color=BLUE, lw=1.1)
        ax.text(x, ax.get_ylim()[1] * 0.02, f" {lbl} ${x:,.0f}", color=BLUE, fontsize=8.5, rotation=90, va="bottom")
    ax.set_yticks([])
    ax.set_xlabel("model fair value, $ per share")
    ax.set_title(f"Monte Carlo over scenarios and inputs (n={len(v):,}) — P(fair value > price) = {mc['p_above_price']:.1%}")
    return img(fig, "Monte Carlo fair value distribution")


def fig_tornado(val: dict) -> str:
    tor = val["tornado"]
    base_v = tor[0]["base"]
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ylabels = []
    for i, t in enumerate(reversed(tor)):
        lo, hi = sorted([t["lo"], t["hi"]])
        ax.barh(i, hi, left=0, height=0.5, color=BLUE if hi > 0 else RED)
        ax.barh(i, lo, left=0, height=0.5, color=RED if lo < 0 else BLUE)
        ylabels.append(t["label"])
    ax.axvline(0, color=BASELINE, lw=1.2)
    ax.set_yticks(range(len(tor)))
    ax.set_yticklabels(ylabels, fontsize=9.5, color=INK2)
    ax.set_xlabel(f"change in scenario-B fair value, USD per share (base \\${base_v:,.0f})")
    ax.set_title("Sensitivity, one knob at a time (blue = knob helps, red = knob hurts)")
    return img(fig, "tornado sensitivity of base-case fair value")


def fig_vardecomp(risk: dict) -> str:
    vd = risk["factors"]["var_decomp"]
    parts = [("Market (S&P 500)", vd["mkt"], BLUE, "white"),
             ("Semis sector (SMH beyond market)", vd["sector"], AQUA, INK),
             ("Rates + dollar", vd["rates"] + vd["fx"], YELLOW, INK),
             ("Micron-specific", vd["idiosyncratic"], VIOLET, "white")]
    fig, ax = plt.subplots(figsize=(9.2, 1.75))
    left = 0.0
    for label, w, color, txt in parts:
        ax.barh(0, w, left=left, height=0.5, color=color, edgecolor=SURFACE, linewidth=2)
        if w > 0.05:
            ax.text(left + w / 2, 0, f"{label}\n{w:.0%}", ha="center", va="center",
                    fontsize=9, color=txt)
        left += w
    ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.grid(False)
    ax.set_title("What explains daily moves (3y): market + sector = 60%, Micron-specific = 40%")
    for s in ax.spines.values():
        s.set_visible(False)
    return img(fig, "variance decomposition of daily returns")


def fig_rolling_beta(risk: dict) -> str:
    rb = risk["rolling_betas"].iloc[-252 * 6:]
    fig, ax = plt.subplots(figsize=(9.2, 3.2))
    ax.plot(rb.index, rb["vs S&P 500"], color=BLUE, lw=1.8, label="beta vs S&P 500")
    ax.plot(rb.index, rb["vs SMH"], color=AQUA, lw=1.8, label="beta vs SMH (semis)")
    ax.axhline(1.0, color=BASELINE, lw=1)
    ax.set_ylabel("rolling 1y beta")
    ax.set_title("Beta is itself cyclical — hedge ratios drift, remeasure before sizing")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "rolling betas vs SPY and SMH")


def fig_cone(risk: dict) -> str:
    cone = risk["cone"]
    hs = sorted(cone.keys())
    p10 = [cone[h]["p10"] * 100 for h in hs]
    p25 = [cone[h]["p25"] * 100 for h in hs]
    p50 = [cone[h]["p50"] * 100 for h in hs]
    p75 = [cone[h]["p75"] * 100 for h in hs]
    p90 = [cone[h]["p90"] * 100 for h in hs]
    now = [cone[h]["now"] * 100 for h in hs]
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    ax.fill_between(hs, p10, p90, color=BLUE_XL, label="p10-p90 (10y)")
    ax.fill_between(hs, p25, p75, color=BLUE_L, label="p25-p75")
    ax.plot(hs, p50, color=BLUE, lw=1.6, label="median")
    ax.plot(hs, now, color=INK, lw=2, marker="o", markersize=5, label="current")
    iv = risk.get("iv", {})
    if iv.get("term"):
        pts = [(min(t * 5 / 7, 252), v * 100) for t, v in iv["term"] if 5 <= t <= 360]
        ax.plot([x for x, _ in pts], [y for _, y in pts],  # x: calendar dte -> trading days
                color=VIOLET, lw=0, marker="D", markersize=5, label="option-implied (ATM)")
    ax.set_xscale("log")
    ax.set_xticks([5, 10, 21, 63, 126, 252])
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}d"))
    ax.set_ylabel("annualized vol, %")
    ax.set_title("Vol cone: realized vol percentiles by horizon (10y) — today sits above the p90 at every horizon")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5, ncols=2)
    return img(fig, "volatility cone with current realized and implied vol")


def fig_rv_series(risk: dict) -> str:
    rv20 = risk["rv20_series"].iloc[-756:] * 100
    rv60 = risk["rv60_series"].iloc[-756:] * 100
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    ax.plot(rv20.index, rv20, color=BLUE, lw=1.6, label="realized vol 20d")
    ax.plot(rv60.index, rv60, color=AQUA, lw=1.6, label="realized vol 60d")
    marks = [("GARCH 1m fcst", risk["garch"]["sigma_21d_ann"] * 100, VIOLET),
             ("IV30", (risk["iv"].get("iv30") or 0), YELLOW),
             ("10y GARCH anchor", risk["garch"]["uncond_vol"] * 100, MUTED)]
    x_last = rv20.index[-1]
    for label, v, color in marks:
        if v:
            ax.plot([x_last], [v], marker="D", color=color, markersize=6)
            ax.annotate(f" {label} {v:.0f}%", (x_last, v), color=INK2, fontsize=8.5,
                        textcoords="offset points", xytext=(8, -3))
    ax.set_ylabel("annualized vol, %")
    ax.set_xlim(rv20.index[0], rv20.index[-1] + pd.Timedelta(days=170))
    ax.set_title("Realized vol, 3 years — the regime tripled during the AI-memory repricing")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "realized vol time series with GARCH and implied vol markers")


def fig_earnings(risk: dict) -> str:
    ev = risk["earnings"]["events"].tail(20)
    move = (risk["iv"].get("earnings_move") or {})
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    x = np.arange(len(ev))
    colors = [BLUE if v > 0 else RED for v in ev["reaction"]]
    ax.bar(x, ev["reaction"] * 100, color=colors, width=0.62)
    ax.axhline(0, color=BASELINE, lw=1)
    m = move.get("event_move_1sd")
    if m:
        ax.axhline(m * 100, color=MUTED, lw=1.1, ls="--")
        ax.axhline(-m * 100, color=MUTED, lw=1.1, ls="--")
        ax.annotate(f"options now imply +/-{m:.0%} (1sd) for the next print",
                    (0, m * 100), textcoords="offset points", xytext=(0, 4),
                    fontsize=8.5, color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels([d[2:7] for d in ev["date"]], rotation=45, fontsize=8)
    ax.set_ylabel("next-day reaction, %")
    st = risk["earnings"]["stats"]
    ax.set_title(f"Earnings-day reactions, last 20 prints — mean |move| {st['mean_abs']:.1%}, "
                 f"{st['var_share']:.0%} of all variance on {st['n']} of {st['n_days_span']:,} days")
    return img(fig, "earnings day reaction bars")


def fig_pb_history(val: dict, fund: dict) -> str:
    hist = val["multiples"]["history"]
    snap = fund["snapshot"]
    fig, ax = plt.subplots(figsize=(9.2, 3.3))
    ax.plot(hist.index, hist["pb"], color=BLUE, lw=2, marker="o", markersize=4, label="P/B at fiscal year end")
    ax.plot([2026], [snap["pb"]], marker="*", markersize=13, color=INK, lw=0, label="today")
    med = hist["pb"].median()
    ax.axhline(med, color=MUTED, lw=1.2, ls="--")
    ax.annotate(f"15y median {med:.1f}x", (hist.index.min(), med), textcoords="offset points",
                xytext=(0, 4), color=MUTED, fontsize=8.5)
    ax.set_yscale("log")
    ax.set_yticks([1, 2, 4, 8, 16])
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}x"))
    ax.set_ylabel("price / book value")
    ax.set_title("Price-to-book: the old cycle anchor (0.9x-3.2x band) vs 15x today — the market has re-classified the business")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    return img(fig, "price to book history")


# ================================================================= tables ====

def _fmt(v, kind="num"):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "—"
    if kind == "usd":
        return f"${v:,.0f}"
    if kind == "usd2":
        return f"${v:,.2f}"
    if kind == "pct":
        return f"{v:.1%}"
    if kind == "pct0":
        return f"{v:.0%}"
    if kind == "x":
        return f"{v:,.1f}×"
    return f"{v:,.2f}"


def html_table(headers: list, rows: list, note: str = "") -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = ""
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        trs += f"<tr>{tds}</tr>"
    cap = f'<div class="tnote">{note}</div>' if note else ""
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>{cap}</div>'


# ================================================================ console ====

def console_brief(val: dict, risk: dict, fund: dict) -> str:
    b = val["base"]
    mc = val["montecarlo"]
    r = val["reverse"]
    iv = risk.get("iv", {})
    em = (iv.get("earnings_move") or {})
    lines = [
        "=" * 74,
        f"MU VALUATION & RISK MODEL   as of {b['price_date']}   price ${b['price']:,.2f}",
        "=" * 74,
        f"DCF scenarios: A ${val['scenarios']['A']['dcf']['ps']:,.0f} (p={val['probs'][0]:.0%}) | "
        f"B ${val['scenarios']['B']['dcf']['ps']:,.0f} (p={val['probs'][1]:.0%}) | "
        f"C ${val['scenarios']['C']['dcf']['ps']:,.0f} (p={val['probs'][2]:.0%})",
        f"Probability-weighted fair value : ${val['fv_prob_weighted']:,.0f}",
        f"Monte Carlo p25/p50/p75         : ${mc['pct']['p25']:,.0f} / ${mc['pct']['p50']:,.0f} / ${mc['pct']['p75']:,.0f}",
        f"P(model fair value > price)     : {mc['p_above_price']:.1%}  (price = p{100 * (1 - mc['p_above_price']):.0f} of the model distribution)",
        "-" * 74,
        "What $%.0f already assumes (reverse DCF):" % b["price"],
        f"  perpetual owner earnings of ${r['perp_eps']:,.0f}/sh ({r['perp_vs_fy27_eps']:.0%} of FY27 consensus EPS), or",
        f"  bull revenue path + {r['implied_nm_steady_on_A']:.0%} steady net margin, or bull path at {r['implied_wacc_on_A']:.1%} WACC" if r.get("implied_nm_steady_on_A") else "",
        f"  (base-case cycle geometry cannot reach the price at any margin <= 90%)" if r.get("implied_nm_steady_on_B") is None or (r.get("implied_nm_steady_on_B") or 0) > 0.85 else "",
        "-" * 74,
        f"WACC {val['wacc']['wacc']:.1%} (beta {val['wacc']['beta']:.2f} shrunk from {val['wacc']['beta_raw']:.2f}, rf {val['wacc']['rf']:.2%})",
        f"Vol: RV20 {risk['rv20']:.0%} (p{risk['rv20_pctile_10y'] * 100:.0f} of 10y) | GARCH 1m {risk['garch']['sigma_21d_ann']:.0%} | "
        f"long-run {risk['garch']['uncond_vol']:.0%} | IV30 {iv.get('iv30', 0):.0f}%",
        f"Factors (3y): beta_SPY {risk['factors']['beta_spy_uni']:.2f}, beta_SMH {risk['factors']['beta_smh_uni']:.2f}; "
        f"idiosyncratic share {risk['factors']['var_decomp']['idiosyncratic']:.0%}",
        f"Next earnings {iv.get('next_earnings', '?')}: options imply +/-{em.get('event_move_1sd', 0):.1%} (1sd); "
        f"historical mean |reaction| {risk['earnings']['stats'].get('mean_abs', 0):.1%}",
        "=" * 74,
        f"Report: {STORE / 'report.html'}",
    ]
    return "\n".join(ln for ln in lines if ln)


# =================================================================== JSON ====

def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()
                if k not in ("values", "level", "path", "pv_rows", "rv20_series", "rv60_series",
                             "rolling_betas", "events", "history")}
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return [float(x) for x in o]
    if isinstance(o, (pd.Series, pd.DataFrame)):
        return None
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def write_json(val: dict, risk: dict, fund: dict) -> Path:
    b = val["base"]
    out = {
        "asof": b["price_date"], "price": b["price"],
        "valuation": _clean({k: v for k, v in val.items() if k != "base"}),
        "risk": _clean({k: v for k, v in risk.items()}),
        "cycle": _clean(fund["cycle"]),
        "trend": {k: v for k, v in fund["trend"].items() if k != "level"},
        "snapshot": _clean(fund["snapshot"]),
        "consensus": fund["consensus"],
    }
    path = STORE / f"valuation-{b['price_date']}.json"
    path.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    return path


# =================================================================== HTML ====

def build_html(val: dict, risk: dict, fund: dict, cfg: dict) -> Path:
    b = val["base"]
    snap = fund["snapshot"]
    cons = fund["consensus"]
    cyc = fund["cycle"]
    w = val["wacc"]
    mc = val["montecarlo"]
    r = val["reverse"]
    iv = risk.get("iv", {})
    em = iv.get("earnings_move") or {}
    st = risk["earnings"]["stats"]
    f = risk["factors"]

    price = b["price"]
    fv = val["fv_prob_weighted"]

    # ---- verdict tiles ----
    tiles = [
        ("Price", f"${price:,.0f}", f"{snap['price_date']} · {(price / snap['hi_52w'] - 1):+.0%} off 52w high"),
        ("Probability-weighted DCF", f"${fv:,.0f}", f"scenarios A/B/C at {val['probs'][0]:.0%}/{val['probs'][1]:.0%}/{val['probs'][2]:.0%}"),
        ("Monte Carlo median", f"${mc['pct']['p50']:,.0f}", f"p25 ${mc['pct']['p25']:,.0f} · p75 ${mc['pct']['p75']:,.0f}"),
        ("P(fair value > price)", f"{mc['p_above_price']:.0%}", "under this model's assumptions"),
        ("Realized vol (20d)", f"{risk['rv20']:.0%}", f"p{risk['rv20_pctile_10y'] * 100:.0f} of the last 10 years"),
        ("Next earnings", iv.get("next_earnings", "?"), f"options imply ±{em.get('event_move_1sd', 0):.0%} (1σ)"),
    ]
    tiles_html = "".join(
        f'<div class="tile"><div class="tlabel">{a}</div><div class="tvalue">{v}</div><div class="tsub">{s}</div></div>'
        for a, v, s in tiles)

    # ---- scenario table ----
    sc_rows = []
    for k in ["A", "B", "C"]:
        s = val["scenarios"][k]
        c = s["cfg"]
        p = s["path"]
        d = s["dcf"]
        sc_rows.append([
            f"<b>{k}</b> — {c['name']}", f"{c['prob']:.0%}",
            _fmt(p['rev'][1] / 1e3, "num") + "B",
            _fmt(min(p['rev']) / 1e3, "num") + "B",
            _fmt(p['rev'][-1] / 1e3, "num") + "B",
            _fmt(c["nm_steady"], "pct0"),
            _fmt(d["ps"], "usd"), _fmt(d["ps_exit"], "usd"),
            _fmt(d["tv_share_of_ev"], "pct0"),
        ])
    scenario_table = html_table(
        ["Scenario", "Prob", "FY27 revenue", "Trough revenue", "FY36 revenue",
         "Steady net margin", "DCF value", "Exit-multiple x-check", "Terminal share of EV"],
        sc_rows,
        "Gordon terminal (g = {:.1%}) is primary; the exit-multiple column re-prices the terminal at {:.0f}× EBITDA. "
        "Every knob behind these paths sits in <code>assumptions.toml</code>.".format(
            cfg["terminal"]["g"], cfg["terminal"]["exit_ev_ebitda"]))

    # ---- WACC table ----
    wacc_table = html_table(
        ["Input", "Value", "Source"],
        [["Risk-free (10y UST)", _fmt(w["rf"], "pct"), "FRED DGS10, live"],
         ["Beta (raw, 5y weekly vs S&P)", _fmt(w["beta_raw"]), "computed from prices"],
         ["Beta (Blume-shrunk, used)", _fmt(w["beta"]), "2/3 raw + 1/3 market"],
         ["Equity risk premium", _fmt(w["erp"], "pct"), "assumption (Damodaran-class)"],
         ["Cost of equity", _fmt(w["ke"], "pct"), "CAPM"],
         ["Debt weight", _fmt(w["w_debt"], "pct"), "market values; MU is net cash"],
         ["<b>WACC</b>", f"<b>{w['wacc']:.2%}</b>", ""]])

    # ---- reverse DCF panel ----
    nmB = r.get("implied_nm_steady_on_B")
    reverse_html = f"""
    <p>Run the machine backwards: instead of asking what Micron is worth, ask what ${price:,.0f}
    <em>already assumes</em>. Three independent reads:</p>
    <ul>
      <li><b>The perpetuity yardstick.</b> Today's market value equals a claim on
      <b>${r['perp_eps']:,.0f}/share of owner earnings every year, forever</b> (growing {cfg['terminal']['g']:.1%},
      discounted at {w['wacc']:.1%}). That is {r['perp_vs_fy27_eps']:.0%} of the FY2027 <em>peak</em> consensus EPS —
      the market treats roughly this year's earnings as the permanent floor, not a cycle top.</li>
      <li><b>On the bull (A) revenue path</b> — supercycle revenue holds near $260B and grows —
      the price back-solves to a <b>{r['implied_nm_steady_on_A']:.0%} net margin in perpetuity</b>
      (Micron's 15-year median: {cyc['nm']['median']:.0%}; best year ever: {cyc['nm']['max']:.0%}).
      Alternatively, scenario A exactly as configured is worth the price at a
      <b>{r['implied_wacc_on_A']:.1%} discount rate</b> (model WACC: {w['wacc']:.1%}).</li>
      <li><b>On the base (B) cycle geometry</b> — a normal correction to a $129B plateau —
      {"the price is unreachable at any net margin up to 90%" if (nmB is None or nmB > 0.85) else f"the price requires a {nmB:.0%} steady margin"}.
      <b>The price cannot be justified by margins alone; it requires the revenue supercycle to persist.</b></li>
    </ul>"""

    # ---- factor table ----
    factor_table = html_table(
        ["Factor", "Beta", "t-stat (Newey-West)", "Reading"],
        [["Market (S&P 500)", _fmt(f["coef"]["mkt"]["beta"]), _fmt(f["coef"]["mkt"]["t_nw"]),
          "moves ~1:1 with the tape before sector effects"],
         ["Semis sector (SMH − S&P)", _fmt(f["coef"]["sector"]["beta"]), _fmt(f["coef"]["sector"]["t_nw"]),
          "the dominant loading — MU is a levered semis bet"],
         ["Rates (Δ10y, pp)", _fmt(f["coef"]["rates"]["beta"]), _fmt(f["coef"]["rates"]["t_nw"]),
          "no reliable daily rate sensitivity at this vol"],
         ["Dollar (Δ log DXY)", _fmt(f["coef"]["fx"]["beta"]), _fmt(f["coef"]["fx"]["t_nw"]),
          "not significant daily"],
         ["<b>Practical hedge ratios</b>", f"β<sub>SPY</sub> {f['beta_spy_uni']:.2f} · β<sub>SMH</sub> {f['beta_smh_uni']:.2f}",
          "", "univariate, 3y daily"]],
        f"R² = {f['r2']:.0%} over {f['n_obs']} days; {f['var_decomp']['idiosyncratic']:.0%} of variance is Micron-specific "
        "(earnings, memory pricing, HBM news) and does not hedge with index products.")

    # ---- Korea table ----
    kr = risk["korea"]
    kr_rows = [[name,
                _fmt(v["kr_leads_us_same_date"]),
                _fmt(v["us_leads_kr_next"]),
                f"{v['n']} days"] for name, v in kr.items()]
    kr_table = html_table(
        ["Seoul name", "corr: KR close (t) → MU (t)", "corr: MU (t) → KR (t+1)", "sample"],
        kr_rows,
        "Seoul closes ~14 hours before New York: the same-calendar-date column is information that exists before "
        "the US open. Both directions are strong — the complex reprices as one global trade around the clock.")

    # ---- earnings last-8 table ----
    ev8 = risk["earnings"]["events"].tail(8).iloc[::-1]
    earn_rows = [[e["date"], _fmt(e["eps_est"], "usd2"), _fmt(e["eps_act"], "usd2"),
                  _fmt(e["surprise"], "pct0") if e["surprise"] is not None else "—",
                  _fmt(e["gap"], "pct"), _fmt(e["reaction"], "pct")]
                 for _, e in ev8.iterrows()]
    earn_table = html_table(
        ["Announce date", "EPS est", "EPS actual", "Surprise", "Overnight gap", "Next-day close"],
        earn_rows,
        "Beats have been large and consistent for six quarters — and the market knows: even a +21% surprise is "
        "not automatically a rally. What moves the stock is guidance vs the whisper, not the printed beat.")

    # ---- multiples table ----
    m = val["multiples"]
    mult_table = html_table(
        ["Measure", "Now", "15y median (FY-end)", "Where that ranks"],
        [["Trailing P/E", _fmt(m["current"]["pe_t"], "x"), _fmt(m["history"]["pe"].median(), "x"),
          f"p{m['pe_pctile'] * 100:.0f} of history"],
         ["Forward P/E (FY27 consensus)", _fmt(m["current"]["pe_f"], "x"), "—",
          "cheap-looking — the classic peak-of-cycle value trap signature"],
         ["Price / book", _fmt(m["current"]["pb"], "x"), _fmt(m["history"]["pb"].median(), "x"),
          f"p{m['pb_pctile'] * 100:.0f} — the old 0.9-3.2× cycle band is gone"],
         ["EV / EBITDA (ttm)", _fmt(m["current"]["ev_ebitda"], "x"), "—", ""]],
        "Memory investors historically timed the cycle on price-to-book because book value is the only line that "
        "doesn't swing with DRAM prices. A 15× book multiple says the market no longer prices Micron as a "
        "commodity-cyclical at all.")

    # ---- peer multiples table ----
    yfp = (fund.get("_peers") or {})

    def _peer_mcap(v):
        if v is None:
            return "—"
        if v > 1e14:   # Samsung/Hynix market caps come back from Yahoo in KRW, not USD
            return f"₩{v / 1e12:,.0f}T"
        return f"${v / 1e12:.2f}T" if v >= 1e12 else f"${v / 1e9:.0f}B"

    peer_rows = [["<b>Micron (MU)</b>", _fmt(snap["forward_pe"], "x"), _fmt(snap["trailing_pe"], "x"),
                  _fmt(snap["pb"], "x"), _fmt(snap["ev_ebitda"], "x"),
                  _fmt(fund["quarterly"]["nm"].iloc[-1], "pct0"),
                  f"${snap['mcap'] / 1e12:.2f}T" if snap["mcap"] >= 1e12 else f"${snap['mcap'] / 1e9:.0f}B"]]
    for name, tk in [("Western Digital", "WDC"), ("Seagate", "STX"), ("TSMC (ADR)", "TSM"),
                      ("Nvidia", "NVDA"), ("Samsung Electronics", "005930.KS"), ("SK Hynix", "000660.KS")]:
        p = yfp.get(tk) or {}
        peer_rows.append([name, _fmt(p.get("forwardPE"), "x"), _fmt(p.get("trailingPE"), "x"),
                           _fmt(p.get("priceToBook"), "x"), _fmt(p.get("enterpriseToEbitda"), "x"),
                           _fmt(p.get("profitMargins"), "pct0"), _peer_mcap(p.get("marketCap"))])
    peer_table = html_table(
        ["Name", "Fwd P/E", "Trailing P/E", "P/B", "EV/EBITDA", "Net margin", "Mkt cap"],
        peer_rows,
        "Peer multiples are Yahoo snapshots (mixed currencies and fiscal calendars; Korean listings priced in KRW) "
        "— read them as rough context, not like-for-like. The interesting read: the whole memory complex re-rated "
        "together, so cross-checks against peers cannot detect a sector-wide mispricing.")

    # ---- normalized panel ----
    n = val["normalized"]
    normalized_html = f"""
    <p>The deliberately cold counterfactual: value Micron as if AI never happened — put revenue back on its
    FY2012–2025 trend (${n['trend_rev26'] / 1e3:,.0f}B for FY2026, vs ${cons['rev_fy0'] / 1e9:,.0f}B consensus)
    at the 15-year median net margin ({n['nm_mid']:.0%}). That machine earns
    <b>${n['norm_eps']:,.2f}/share mid-cycle</b>; at a {cfg['normalized']['pe_band_low']:.0f}–{cfg['normalized']['pe_band_high']:.0f}×
    through-cycle multiple plus ${n['net_cash_ps']:,.0f} net cash it is worth
    <b>${n['lo']:,.0f}–${n['hi']:,.0f}</b>. A justified price-to-book check
    ((normalized ROE {n['roe_norm']:.0%} − g)/(r − g) = {n['pb_justified']:.1f}× book) lands at ${n['pb_value']:,.0f} —
    the same zone. <b>Roughly ${price - n['hi']:,.0f} of today's ${price:,.0f} — about {(price - n['hi']) / price:.0%} —
    is payment for the AI-memory structural break being real and durable.</b> Note the 52-week low
    (${snap['lo_52w']:,.0f}) sat exactly at the top of this bracket.</p>"""

    # ---- data provenance ----
    prov_table = html_table(
        ["Feed", "Source", "What it feeds"],
        [["Prices, 12 tickers, up to 40y OHLCV", "Yahoo Finance (yfinance)", "returns, betas, vol, cone, tails"],
         ["Statements FY2021-26 + quarters", "Yahoo Finance (yfinance)", "boom cash mechanics, snapshot"],
         ["Annual fundamentals FY2011-25", "macrotrends.net", "trend, margins, cycle stats, P/B history"],
         ["Analyst estimates (37-42 analysts)", "Yahoo Finance (yfinance)", "FY26/27 anchors, targets"],
         ["Option chain, 13.5k contracts", "CBOE delayed quotes", "IV term structure, skew, implied earnings move"],
         ["10y Treasury", "FRED DGS10", "risk-free rate"],
         ["EDGAR XBRL", "<i>blocked from this network (SEC geo-block)</i>", "macrotrends substitutes"]])

    # ---- limits ----
    limits_html = """
    <ul>
      <li><b>The model prices cycles; it cannot price the structural break.</b> Whether HBM/custom-memory economics
      persist is the entire question, and it is a judgment input (the scenario probabilities), not a model output.
      The tool's job is to make that judgment explicit and price its consequences honestly.</li>
      <li><b>Consensus anchors are load-bearing.</b> FY26/27 revenue and EPS come from the analyst feed; if the sell-side
      is systematically wrong at cycle turns (it historically is), the near-term cash flows inherit that error.</li>
      <li><b>Fundamentals history starts FY2011</b> (EDGAR is geo-blocked from this machine; macrotrends caps free history).
      That window covers two full cycles and the modern 3-supplier oligopoly — but not 2001 or 2008.</li>
      <li><b>No segment data.</b> DRAM/NAND/HBM splits are not modeled separately; scenarios move the blended line.
      A per-segment build needs the 10-K segment tables (blocked) or manual entry.</li>
      <li><b>Options are delayed quotes</b>; the implied earnings move uses ATM forward-variance differencing and
      a far-dated baseline — a fair approximation, not a dealer's event-vol mark.</li>
      <li><b>Dilution, buybacks, and the Q4 stub are approximations</b> (~0.3%/yr share creep; stub at FY26 cash
      conversion). Each is worth ±$10-25/share, small next to the scenario spread.</li>
      <li><b>Model fair value ≠ price path.</b> Nothing here times the cycle; a stock can trade multiples of fair
      value for years. The reverse-DCF section is the bridge between this model and the tape.</li>
    </ul>"""

    css = """
    body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #f9f9f7; color: #0b0b0b;
           margin: 0; padding: 24px 16px; }
    .wrap { max-width: 1060px; margin: 0 auto; }
    h1 { font-size: 24px; margin: 0 0 4px; }
    h2 { font-size: 17px; margin: 34px 0 6px; border-bottom: 1px solid #e1e0d9; padding-bottom: 5px;}
    .sub { color: #52514e; margin-bottom: 18px; font-size: 13.5px;}
    .card { background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 10px;
            padding: 14px 16px; margin: 10px 0; }
    .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
    .tile { background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 10px; padding: 10px 12px; }
    .tlabel { font-size: 11px; color: #898781; text-transform: uppercase; letter-spacing: .04em;}
    .tvalue { font-size: 21px; font-weight: 700; margin: 2px 0; }
    .tsub { font-size: 11.5px; color: #52514e; }
    .tablewrap { overflow-x: auto; }
    table { border-collapse: collapse; width: 100%; font-size: 12.5px; margin: 8px 0 2px; }
    th { text-align: left; color: #52514e; font-weight: 600; border-bottom: 1px solid #c3c2b7; padding: 5px 8px;}
    td { border-bottom: 1px solid #e1e0d9; padding: 5px 8px; font-variant-numeric: tabular-nums; }
    .tnote { font-size: 11.5px; color: #898781; margin: 4px 0 8px; }
    p, li { font-size: 13.5px; line-height: 1.55; }
    code { background: #f0efec; padding: 1px 4px; border-radius: 4px; font-size: 12px;}
    .verdict { font-size: 14.5px; }
    img { border-radius: 6px; }
    """

    verdict_html = f"""
    <p class="verdict"><b>The one-paragraph read.</b> Micron at ${price:,.0f} is not priced as a memory company having a
    great year; it is priced as a company whose current, unprecedented economics (~{b['nm26']:.0%} net margin on
    ~${cons['rev_fy0'] / 1e9:.0f}B of revenue, headed to ${cons['rev_fy1'] / 1e9:.0f}B consensus) are the <em>new permanent state</em>.
    This model — three cycle-aware scenarios, probability-weighted {val['probs'][0]:.0%}/{val['probs'][1]:.0%}/{val['probs'][2]:.0%} —
    values that claim at <b>${fv:,.0f}</b> (Monte-Carlo median ${mc['pct']['p50']:,.0f}), which puts the market price at the
    <b>{100 * (1 - mc['p_above_price']):.0f}th percentile</b> of the model's fair-value distribution. The gap is not an arithmetic
    disagreement — it decomposes exactly into the questions in the reverse-DCF section: the market pays for supercycle
    <em>persistence</em> (margins near {r['implied_nm_steady_on_A']:.0%} forever on a held plateau, or a {r['implied_wacc_on_A']:.1%}
    discount rate on the bull path), while this model pays for a <em>cycle</em>, however large. Whichever side you take,
    take it knowingly: edit the probabilities and margins in <code>assumptions.toml</code> and re-run — the tool reprices
    in seconds. Volatility says the market itself is unsure: realized vol is at its 10-year 98th percentile, and options
    price the next earnings print at ±{em.get('event_move_1sd', 0):.0%}.</p>"""

    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MU valuation &amp; risk — {b['price_date']}</title>
<style>{css}</style></head>
<body><div class="wrap">
<h1>Micron (MU) — valuation &amp; risk model</h1>
<div class="sub">as of {b['price_date']} · price ${price:,.2f} · market cap ${snap['mcap'] / 1e12:.2f}T ·
fiscal year ends late August · every input editable in <code>assumptions.toml</code> · generated by <code>tools/muval</code></div>

<div class="tiles">{tiles_html}</div>

<h2>Verdict</h2>
<div class="card">{verdict_html}{fig_football(val, fund)}</div>

<h2>What the price already assumes (reverse DCF)</h2>
<div class="card">{reverse_html}</div>

<h2>The cycle you are buying into</h2>
<div class="card">{fig_revenue_trend(val, fund)}{fig_quarters(fund)}{fig_margins(fund)}{fig_pb_history(val, fund)}{mult_table}{peer_table}</div>

<h2>The scenario engine</h2>
<div class="card">
<p>Three explicit futures, each a full revenue-margin-cash path to FY2036 (details in the table; every number
editable). <b>A</b>: the AI-memory rents persist and Micron keeps logic-class economics. <b>B</b> (base): the
supercycle is real but 2028-29 brings a classic digestion — trough at 50% of peak (history: −24%, −29%, −49%) —
then a plateau near FY2026 revenue at 25% margins (median era margin: {cyc['nm']['median']:.0%}, so B still grants a
structural HBM uplift). <b>C</b>: Samsung qualifies everywhere, CXMT scales, the premium collapses — FY2023 rhymed.</p>
{fig_eps_paths(val, fund)}{scenario_table}{wacc_table}</div>

<h2>Distribution, not a number</h2>
<div class="card">{fig_mc(val)}
<p>The Monte Carlo draws a scenario by its probability, then jitters revenue, trough depth, plateau, steady margin,
WACC and terminal growth around it ({mc and val['montecarlo']['probs_used'] and f"{cfg['montecarlo']['n']:,}"} paths).
Read the price against it: today's ${price:,.0f} is exceeded by only {mc['p_above_price']:.1%} of model outcomes.</p>
{fig_tornado(val)}
<p>The tornado explains why the distribution is wide: the plateau level and steady margin — the two knobs that
encode "is the structural break real" — dominate; the financial knobs (WACC, terminal growth) matter second.</p></div>

<h2>What moves the price day to day</h2>
<div class="card">{fig_vardecomp(risk)}{factor_table}{fig_rolling_beta(risk)}{kr_table}</div>

<h2>Volatility: what you are signing up for</h2>
<div class="card">{fig_cone(risk)}{fig_rv_series(risk)}
<p>GARCH(1,1) on ten years of daily returns: persistence {risk['garch']['persistence']:.3f} (shock half-life
{risk['garch']['halflife_days']:.0f} trading days), long-run anchor {risk['garch']['uncond_vol']:.0%} — today's
{risk['rv20']:.0%} regime decays toward ~{risk['garch']['sigma_21d_ann']:.0%} over the next month if nothing new hits.
Tails (10y): worst day {risk['tails']['worst'][0][1]:.0%} ({risk['tails']['worst'][0][0]}), 95% one-day VaR
{risk['tails']['var95']:.1%}, max drawdown {risk['tails']['max_dd']:.0%}, current drawdown {risk['tails']['dd_now']:.0%};
down-capture vs SMH {risk['tails']['down_capture']:.2f}.</p>
{fig_earnings(risk)}{earn_table}</div>

<h2>Data &amp; honest limits</h2>
<div class="card">{prov_table}{limits_html}
<div class="tnote">Model, not advice. Everything regenerates from cached raw pulls with
<code>python tools/muval/muval.py --offline</code>; refresh feeds with <code>--refresh</code>.</div></div>

</div></body></html>"""

    STORE.mkdir(parents=True, exist_ok=True)
    out = STORE / "report.html"
    out.write_text(html, encoding="utf-8")
    return out
