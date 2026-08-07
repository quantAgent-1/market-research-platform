"""muval.valuation — WACC, scenario DCF, reverse DCF, normalized bracket, multiples,
Monte Carlo, tornado. Per-name (MU / NVDA / AMD): every entry point takes a `ticker`
(default "MU") and looks up that name's fiscal calendar via
`name_cfg = cfg["names"][ticker]` (`{"fy0": int, "fye_month": int}`), and its
scenario/cash-mechanics/normalized assumptions via `cfg[...][ticker]`.

Units: $ millions everywhere inside this module; per-share values in $.
Fiscal timing: fy_end(fy, fye_month) approximates a fiscal year's end date as the
28th of that month; fy_mid = fy_end - 183 days is the mid-year cash-timing
convention used to discount each explicit forecast year's flow (matches the old
MU-only "Mar-1" convention when fye_month=8). The current (stub) fiscal year's
partial-year flow is handled separately: discounted to the midpoint between the
valuation date and that year's fy_end, since the balance-sheet net cash and the
consensus anchors are as of "today," not a fiscal year boundary.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd


# --------------------------------------------------------------- fiscal calendar --

def fy_end(fy: int, fye_month: int) -> date:
    """Approximate fiscal-year-end date: the 28th of the FYE month."""
    return date(fy, fye_month, 28)


def fy_mid(fy: int, fye_month: int) -> date:
    """Mid-year cash-timing convention for a full fiscal year's flow."""
    return fy_end(fy, fye_month) - timedelta(days=183)


# ------------------------------------------------------------------- WACC ----

def wacc_build(fund: dict, data: dict, cfg: dict, ticker: str = "MU") -> dict:
    c = cfg["wacc"]
    rf = (data["riskfree"].get("rate") or 4.5) / 100.0

    px = data["prices"]
    t_w = px[ticker]["Adj Close"].resample("W-FRI").last().pct_change().dropna()
    spy_w = px["SPY"]["Adj Close"].resample("W-FRI").last().pct_change().dropna()
    joined = pd.concat([t_w, spy_w], axis=1, keys=["t", "spy"]).dropna()
    joined = joined.iloc[-int(52 * c["beta_window_years"]):]
    beta_raw = float(np.polyfit(joined["spy"], joined["t"], 1)[0])
    beta = c["beta_shrink"] * beta_raw + (1 - c["beta_shrink"]) * 1.0
    beta = min(max(beta, c["beta_floor"]), c["beta_cap"])

    ke = rf + beta * c["erp"]
    kd = (rf + c["kd_spread"]) * (1 - c["tax_rate"])
    snap = fund["snapshot"]
    e = snap["mcap"]
    d = snap["debt"]
    wacc = (e * ke + d * kd) / (e + d)
    return {"rf": rf, "beta_raw": beta_raw, "beta": beta, "erp": c["erp"],
            "ke": ke, "kd": kd, "w_debt": d / (e + d), "wacc": wacc,
            "beta_yf": snap.get("beta_yf")}


# --------------------------------------------------------------- scenarios ----

def _fy0_reported_eps(fund: dict, name_cfg: dict) -> float:
    """Sum of actual EPS (street basis -- same accounting basis as the consensus
    estimate) for FY0 quarters already reported.

    fund["eps_quarters"] is indexed by earnings ANNOUNCE date, not fiscal period
    end. Announces lag the quarter they report on by several weeks, so the first
    announce after fy_end(fy0-1) is structurally always the trailing Q4/FY print
    of FY(fy0-1) itself (it reports on the year that just closed, even though it
    is dated a few weeks into FY0) -- every fiscal calendar has this leak, so drop
    that one entry and keep the rest through fy_end(fy0).
    """
    eq = fund.get("eps_quarters")
    if eq is None or eq.empty:
        return 0.0
    fy0, fye_month = name_cfg["fy0"], name_cfg["fye_month"]
    lo, hi = fy_end(fy0 - 1, fye_month), fy_end(fy0, fye_month)
    idx_date = eq.index.date
    win = eq[(idx_date > lo) & (idx_date <= hi)]
    if win.empty:
        return 0.0
    win = win.iloc[1:]  # drop the trailing FY(fy0-1) Q4/FY print (see docstring)
    return float(win["eps_act"].sum()) if not win.empty else 0.0


def _base_inputs(fund: dict, name_cfg: dict) -> dict:
    cons, snap = fund["consensus"], fund["snapshot"]
    shares_m = snap["shares"] / 1e6
    rev_fy0 = cons["rev_fy0"] / 1e6
    ni_fy0 = cons["eps_fy0"] * shares_m
    rev_fy1_cons = cons["rev_fy1"] / 1e6
    rev_prior = float(fund["annual"]["revenue"].dropna().iloc[-1])
    stub_eps = max(cons["eps_fy0"] - _fy0_reported_eps(fund, name_cfg), 0.0)
    return {"shares_m": shares_m, "rev26": rev_fy0, "nm26": ni_fy0 / rev_fy0,
            "rev27_cons": rev_fy1_cons, "rev_prior": rev_prior, "stub_eps": stub_eps,
            "net_cash": snap["net_cash"] / 1e6, "price": snap["price"],
            "price_date": snap["price_date"]}


def scenario_path(base: dict, sc: dict, mech: dict, last_fy: int, name_cfg: dict) -> dict:
    """Revenue / margin / cash path FY(fy0)..last_fy as numpy arrays (MC-fast).

    fy27_rev_vs_consensus / peak_extra_* anchor to calendar-2027 as these
    scenarios' shared first genuinely-open forecast year (authored 2026-07-11
    off each name's FY26/27/28 consensus). Which analyst-consensus figure that
    maps to depends on the ticker's own fy0: for MU/AMD (fy0=2026) it's fy0+1,
    scaling consensus rev_fy1, with fy0 itself left at unscaled consensus; for
    NVDA (fy0=2027 already) it's fy0 itself, scaling consensus rev_fy0 directly,
    with peak/trough/steady extending from there. A re-run once every name's fy0
    has rolled past 2027 needs this pivot (and the scenario knobs themselves)
    re-anchored -- an honest limit of a hand-built, dated scenario set, not a
    permanent formula.
    """
    fy0 = name_cfg["fy0"]
    years = np.arange(fy0, last_fy + 1)
    n = len(years)
    rev = np.zeros(n)
    rev[0] = base["rev26"]

    anchor_fy = fy0 if fy0 >= 2027 else fy0 + 1
    anchor_idx = anchor_fy - fy0
    anchor_cons = base["rev26"] if anchor_idx == 0 else base["rev27_cons"]
    anchor_rev = sc["fy27_rev_vs_consensus"] * anchor_cons
    rev[anchor_idx] = anchor_rev

    peak_fy = anchor_fy + int(sc["peak_extra_years"])
    peak_rev = anchor_rev * (1 + sc["peak_extra_growth"]) ** sc["peak_extra_years"]
    trough_fy = peak_fy + 2
    steady_fy = peak_fy + 4
    trough_rev = sc["trough_frac_of_peak"] * peak_rev
    steady_rev = sc["steady_frac_of_peak"] * peak_rev

    for i, y in enumerate(years):
        if y <= anchor_fy:
            continue
        if y <= peak_fy:                      # extra boom year(s)
            rev[i] = rev[i - 1] * (1 + sc["peak_extra_growth"])
        elif y <= trough_fy:                  # geometric slide to trough
            step = (trough_rev / peak_rev) ** (1.0 / (trough_fy - peak_fy))
            rev[i] = rev[i - 1] * step
        elif y <= steady_fy:                  # geometric recovery to plateau
            step = (steady_rev / trough_rev) ** (1.0 / (steady_fy - trough_fy))
            rev[i] = rev[i - 1] * step
        else:                                 # steady growth
            rev[i] = rev[i - 1] * (1 + sc["steady_growth"])

    # net margin path: pre-anchor years at the (unscaled) consensus-implied margin,
    # FY(anchor)..peak at nm_peak, linear to nm_trough, recover linear to nm_steady,
    # flat after
    nm = np.zeros(n)
    for i, y in enumerate(years):
        if y < anchor_fy:
            nm[i] = base["nm26"]
        elif y <= peak_fy:
            nm[i] = sc["nm_peak"]
        elif y <= trough_fy:
            f = (y - peak_fy) / (trough_fy - peak_fy)
            nm[i] = sc["nm_peak"] + f * (sc["nm_trough"] - sc["nm_peak"])
        elif y <= steady_fy:
            f = (y - trough_fy) / (steady_fy - trough_fy)
            nm[i] = sc["nm_trough"] + f * (sc["nm_steady"] - sc["nm_trough"])
        else:
            nm[i] = sc["nm_steady"]

    capex = np.where(years <= peak_fy, sc["capex_boom"],
                     np.where(years <= steady_fy, sc["capex_trough"], sc["capex_steady"]))

    # D&A % of revenue converges from today's level toward steady capex
    dna = np.zeros(n)
    dna_target = mech["dna_vs_capex_steady"] * sc["capex_steady"]
    for i in range(n):
        f = min(1.0, i / mech["dna_converge_years"])
        dna[i] = mech["dna_start"] + f * (dna_target - mech["dna_start"])

    ni = nm * rev
    delta_rev = np.diff(rev, prepend=base["rev_prior"])  # last actual FY vs FY(fy0)
    nwc_flow = -mech["nwc_pct_of_delta_rev"] * delta_rev
    fcf = ni + dna * rev - capex * rev + nwc_flow

    shares = base["shares_m"] * (1 + mech["dilution_per_year"]) ** (years - fy0)
    eps = ni / shares
    return {"years": years, "rev": rev, "nm": nm, "ni": ni, "eps": eps,
            "capex_pct": capex, "dna_pct": dna, "nwc_flow": nwc_flow,
            "fcf": fcf, "shares": shares,
            "peak_fy": peak_fy, "trough_fy": trough_fy, "steady_fy": steady_fy}


# -------------------------------------------------------------------- DCF ----

def _yearfrac(d0: date, d1: date) -> float:
    return (d1 - d0).days / 365.25


def dcf(path: dict, base: dict, wacc: float, cfg: dict, name_cfg: dict) -> dict:
    """PV of the current-FY (FY0) stub + FY(fy0+1)..last FCF + terminal, plus net cash."""
    g = cfg["terminal"]["g"]
    fy0, fye_month = name_cfg["fy0"], name_cfg["fye_month"]
    val_date = datetime.strptime(base["price_date"], "%Y-%m-%d").date()

    years, fcf = path["years"], path["fcf"]
    pv_sum, pv_rows = 0.0, []

    # FY0 stub: consensus-minus-actuals residual EPS (see _fy0_reported_eps) at the
    # FY0 cash-conversion ratio, discounted to the midpoint of the remaining stub period
    conv0 = path["fcf"][0] / max(path["ni"][0], 1e-9)
    stub_fcf = base["stub_eps"] * base["shares_m"] * min(max(conv0, 0.0), 1.0)
    fy0_end = fy_end(fy0, fye_month)
    stub_mid = val_date + (fy0_end - val_date) / 2
    t_stub = max(_yearfrac(val_date, stub_mid), 0.02)
    pv_stub = stub_fcf / (1 + wacc) ** t_stub
    pv_sum += pv_stub

    for i, y in enumerate(years):
        if y <= fy0:
            continue
        t = _yearfrac(val_date, fy_mid(int(y), fye_month))
        pv = fcf[i] / (1 + wacc) ** t
        pv_rows.append((int(y), float(fcf[i]), float(pv)))
        pv_sum += pv

    t_term = _yearfrac(val_date, fy_mid(int(years[-1]), fye_month))
    fcf_term = fcf[-1] * (1 + g)
    tv = fcf_term / (wacc - g)
    pv_tv = tv / (1 + wacc) ** t_term

    # exit-multiple cross-check on terminal-year EBITDA
    tax = cfg["wacc"]["tax_rate"]
    ebitda_term = path["ni"][-1] / (1 - tax) + path["dna_pct"][-1] * path["rev"][-1]
    tv_exit = cfg["terminal"]["exit_ev_ebitda"] * ebitda_term
    pv_tv_exit = tv_exit / (1 + wacc) ** t_term

    ev = pv_sum + pv_tv
    equity = ev + base["net_cash"]
    ps = equity / base["shares_m"]
    ev_exit = pv_sum + pv_tv_exit
    ps_exit = (ev_exit + base["net_cash"]) / base["shares_m"]
    return {"pv_stub": pv_stub, "pv_explicit": pv_sum - pv_stub, "pv_tv": pv_tv,
            "tv_share_of_ev": pv_tv / ev if ev > 0 else float("nan"),
            "ev": ev, "equity": equity, "ps": ps, "ps_exit": ps_exit,
            "pv_rows": pv_rows}


# ------------------------------------------------------------ reverse DCF ----

def reverse_dcf(fund: dict, wacc: float, cfg: dict, ticker: str, name_cfg: dict) -> dict:
    """Two reads of what $price already assumes."""
    base = _base_inputs(fund, name_cfg)
    g = cfg["terminal"]["g"]
    mech = cfg["cash_mechanics"][ticker]
    last_fy = name_cfg["fy0"] + 10
    price = base["price"]

    # read 1: the perpetuity yardstick
    perp_fcf = (price * base["shares_m"] - base["net_cash"]) * (wacc - g)
    perp_eps = perp_fcf / base["shares_m"]

    def solve(key, lo, hi, sc_base, transform=None):
        """Bisect a scenario knob so DCF == price; None if outside [lo, hi]."""
        def v_at(x):
            s = dict(sc_base)
            s[key] = x
            if transform:
                s = transform(s)
            p = scenario_path(base, s, mech, last_fy, name_cfg)
            return dcf(p, base, wacc, cfg, name_cfg)["ps"]
        v_lo, v_hi = v_at(lo), v_at(hi)
        if not (min(v_lo, v_hi) <= price <= max(v_lo, v_hi)):
            return None
        for _ in range(60):
            mid = (lo + hi) / 2
            if (v_at(mid) < price) == (v_lo < price):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    # read 2: on the BULL (A) revenue geometry, what steady net margin is priced in?
    sc_a = dict(cfg["scenarios"][ticker]["A"])
    nm_star_a = solve("nm_steady", 0.0, 0.9, sc_a)

    # read 3: on A's full assumption set, what discount rate makes it worth price?
    p_a = scenario_path(base, sc_a, mech, last_fy, name_cfg)
    w_lo, w_hi = 0.055, 0.25
    implied_wacc = None
    v_lo = dcf(p_a, base, w_lo, cfg, name_cfg)["ps"]
    v_hi = dcf(p_a, base, w_hi, cfg, name_cfg)["ps"]
    if min(v_lo, v_hi) <= price <= max(v_lo, v_hi):
        lo, hi = w_lo, w_hi
        for _ in range(60):
            mid = (lo + hi) / 2
            if (dcf(p_a, base, mid, cfg, name_cfg)["ps"] < price) == (v_lo < price):
                lo = mid
            else:
                hi = mid
        implied_wacc = (lo + hi) / 2

    # read 4: on the base (B) geometry, is price reachable at any margin? (usually no)
    sc_b = dict(cfg["scenarios"][ticker]["B"])
    nm_star_b = solve("nm_steady", 0.0, 0.9, sc_b)

    return {"perp_fcf": perp_fcf, "perp_eps": perp_eps,
            "perp_vs_fy27_eps": perp_eps / fund["consensus"]["eps_fy1"],
            "implied_nm_steady_on_A": nm_star_a,
            "implied_wacc_on_A": implied_wacc,
            "implied_nm_steady_on_B": nm_star_b}


# ----------------------------------------------------- normalized bracket ----

def normalized_value(fund: dict, wacc: float, cfg: dict, ticker: str, name_cfg: dict) -> dict:
    """The 'no structural break' limiting case: pre-boom trend revenue at mid-cycle
    margins, plus today's net cash. Deliberately ignores the current growth boom."""
    c = cfg["normalized"][ticker]
    base = _base_inputs(fund, name_cfg)
    trend, cyc, snap = fund["trend"], fund["cycle"], fund["snapshot"]
    trend_rev26 = trend["level"](name_cfg["fy0"]) / 1  # $M already
    nm_mid = cyc["nm"]["median"]
    norm_eps = trend_rev26 * nm_mid / base["shares_m"]
    ncps = base["net_cash"] / base["shares_m"]
    lo = norm_eps * c["pe_band_low"] + ncps
    hi = norm_eps * c["pe_band_high"] + ncps

    roe_norm = cyc["roe"]["median"]
    g = c["pb_roe_g"]
    pb_just = max((roe_norm - g) / max(wacc - g, 1e-6), 0.0)
    pb_value = pb_just * (snap.get("book_value_ps") or 0.0)
    return {"trend_rev26": trend_rev26, "nm_mid": nm_mid, "norm_eps": norm_eps,
            "net_cash_ps": ncps, "lo": lo, "hi": hi,
            "roe_norm": roe_norm, "pb_justified": pb_just, "pb_value": pb_value}


# ---------------------------------------------------------------- multiples ----

def multiples_history(fund: dict, px: pd.DataFrame, name_cfg: dict) -> dict:
    """FY-end trailing P/E, P/B, P/S from the long annual frame + price history."""
    ann = fund["annual"]
    rows = []
    for fy, r in ann.iterrows():
        if pd.isna(r["eps_diluted"]) or pd.isna(r["bvps"]):
            continue
        fy_end_ts = pd.Timestamp(fy_end(int(fy), name_cfg["fye_month"]))
        px_win = px.loc[:fy_end_ts, "Close"]
        if px_win.empty:
            continue
        price = float(px_win.iloc[-1])
        pe = price / r["eps_diluted"] if r["eps_diluted"] > 0 else np.nan
        ps = price * r["shares_outstanding"] / r["revenue"]
        rows.append({"fy": int(fy), "price": price, "pe": pe,
                     "pb": price / r["bvps"], "ps": ps})
    hist = pd.DataFrame(rows).set_index("fy")

    snap = fund["snapshot"]
    def pctile(series, x):
        s = series.dropna()
        return float((s < x).mean()) if len(s) else float("nan")
    return {"history": hist,
            "current": {"pe_t": snap["trailing_pe"], "pe_f": snap["forward_pe"],
                        "pb": snap["pb"], "ev_ebitda": snap["ev_ebitda"]},
            "pb_pctile": pctile(hist["pb"], snap["pb"] or np.nan),
            "pe_pctile": pctile(hist["pe"], snap["trailing_pe"] or np.nan)}


# -------------------------------------------------------------- Monte Carlo ----

def monte_carlo(fund: dict, wacc: float, cfg: dict, ticker: str, name_cfg: dict) -> dict:
    mc = cfg["montecarlo"]
    mech = cfg["cash_mechanics"][ticker]
    last_fy = name_cfg["fy0"] + 10
    base = _base_inputs(fund, name_cfg)
    rng = np.random.default_rng(int(mc["seed"]))
    names = ["A", "B", "C"]
    probs = np.array([cfg["scenarios"][ticker][k]["prob"] for k in names], dtype=float)
    probs = probs / probs.sum()
    n = int(mc["n"])
    draws_sc = rng.choice(3, size=n, p=probs)
    z = rng.standard_normal((n, 6))
    out = np.empty(n)
    for i in range(n):
        sc = dict(cfg["scenarios"][ticker][names[draws_sc[i]]])
        sc["fy27_rev_vs_consensus"] = max(0.2, sc["fy27_rev_vs_consensus"] * (1 + mc["sd_fy27_rev"] * z[i, 0]))
        sc["trough_frac_of_peak"] = float(np.clip(sc["trough_frac_of_peak"] + mc["sd_trough_frac"] * z[i, 1], 0.15, 0.98))
        sc["steady_frac_of_peak"] = float(np.clip(sc["steady_frac_of_peak"] + mc["sd_steady_frac"] * z[i, 2], 0.2, 1.5))
        sc["nm_steady"] = float(np.clip(sc["nm_steady"] + mc["sd_nm_steady"] * z[i, 3], -0.05, 0.55))
        w = float(np.clip(wacc + mc["sd_wacc"] * z[i, 4], 0.07, 0.20))
        cfg_t = {"terminal": {"g": float(np.clip(cfg["terminal"]["g"] + mc["sd_g"] * z[i, 5], 0.0, w - 0.02)),
                              "exit_ev_ebitda": cfg["terminal"]["exit_ev_ebitda"]},
                 "wacc": cfg["wacc"]}
        p = scenario_path(base, sc, mech, last_fy, name_cfg)
        out[i] = dcf(p, base, w, cfg_t, name_cfg)["ps"]
    pct = {f"p{q}": float(np.percentile(out, q)) for q in [5, 10, 25, 50, 75, 90, 95]}
    return {"values": out, "pct": pct,
            "p_above_price": float((out > base["price"]).mean()),
            "mean": float(out.mean()), "probs_used": probs.tolist()}


# ------------------------------------------------------------------ tornado ----

def tornado(fund: dict, wacc: float, cfg: dict, ticker: str, name_cfg: dict) -> list:
    """One-at-a-time sensitivity of the base (B) fair value."""
    mech = cfg["cash_mechanics"][ticker]
    last_fy = name_cfg["fy0"] + 10
    base = _base_inputs(fund, name_cfg)
    sc0 = dict(cfg["scenarios"][ticker]["B"])

    def value(sc=None, w=None, g=None):
        s = dict(sc0 if sc is None else sc)
        ww = wacc if w is None else w
        cfg_t = {"terminal": {"g": cfg["terminal"]["g"] if g is None else g,
                              "exit_ev_ebitda": cfg["terminal"]["exit_ev_ebitda"]},
                 "wacc": cfg["wacc"]}
        return dcf(scenario_path(base, s, mech, last_fy, name_cfg), base, ww, cfg_t, name_cfg)["ps"]

    v0 = value()
    knobs = []

    def add(label, lo_kw, hi_kw):
        knobs.append({"label": label, "lo": value(**lo_kw) - v0, "hi": value(**hi_kw) - v0})

    def scv(k, dv):
        s = dict(sc0)
        s[k] = s[k] + dv
        return {"sc": s}

    add("WACC +/-1pp", {"w": wacc + 0.01}, {"w": wacc - 0.01})
    add("Terminal growth +/-0.5pp", {"g": cfg["terminal"]["g"] - 0.005}, {"g": cfg["terminal"]["g"] + 0.005})
    add("Steady net margin +/-5pp", scv("nm_steady", -0.05), scv("nm_steady", +0.05))
    add("Plateau level +/-10pp of peak", scv("steady_frac_of_peak", -0.10), scv("steady_frac_of_peak", +0.10))
    add("Trough depth +/-10pp of peak", scv("trough_frac_of_peak", -0.10), scv("trough_frac_of_peak", +0.10))
    add("FY27 revenue +/-10%", scv("fy27_rev_vs_consensus", -0.10), scv("fy27_rev_vs_consensus", +0.10))
    add("Steady capex +/-5pp of revenue", scv("capex_steady", +0.05), scv("capex_steady", -0.05))
    add("Steady growth +/-2pp", scv("steady_growth", -0.02), scv("steady_growth", +0.02))

    knobs.sort(key=lambda k: -(abs(k["hi"]) + abs(k["lo"])))
    return [{"label": k["label"], "lo": float(k["lo"]), "hi": float(k["hi"]), "base": float(v0)} for k in knobs]


# ---------------------------------------------------------------------- run ----

def run(data: dict, fund: dict, cfg: dict, ticker: str = "MU") -> dict:
    name_cfg = cfg["names"][ticker]
    base = _base_inputs(fund, name_cfg)
    w = wacc_build(fund, data, cfg, ticker)
    wacc = w["wacc"]
    mech = cfg["cash_mechanics"][ticker]
    last_fy = name_cfg["fy0"] + 10

    scenarios = {}
    for key in ["A", "B", "C"]:
        sc = cfg["scenarios"][ticker][key]
        p = scenario_path(base, sc, mech, last_fy, name_cfg)
        d = dcf(p, base, wacc, cfg, name_cfg)
        scenarios[key] = {"cfg": dict(sc), "path": p, "dcf": d}

    probs = np.array([cfg["scenarios"][ticker][k]["prob"] for k in ["A", "B", "C"]])
    probs = probs / probs.sum()
    fv_pw = float(sum(probs[i] * scenarios[k]["dcf"]["ps"] for i, k in enumerate(["A", "B", "C"])))

    rev = reverse_dcf(fund, wacc, cfg, ticker, name_cfg)
    norm = normalized_value(fund, wacc, cfg, ticker, name_cfg)
    mult = multiples_history(fund, data["prices"][ticker], name_cfg)
    mc = monte_carlo(fund, wacc, cfg, ticker, name_cfg)
    tor = tornado(fund, wacc, cfg, ticker, name_cfg)

    return {"base": base, "wacc": w, "scenarios": scenarios, "fv_prob_weighted": fv_pw,
            "probs": probs.tolist(), "reverse": rev, "normalized": norm,
            "multiples": mult, "montecarlo": mc, "tornado": tor}
