"""muval.riskvol — what moves the price, and how much it moves.

Realized-vol estimators (close-close, Parkinson, Garman-Klass, Yang-Zhang),
EWMA + GARCH(1,1) fitted by MLE (scipy), a 10y vol cone, factor regressions with
Newey-West errors + variance decomposition, the earnings-day study, implied vol
from the CBOE chain, Korea-complex lead-lag, and tail stats.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ANN = 252.0


# ------------------------------------------------------------- estimators ----

def log_returns(px: pd.DataFrame) -> pd.Series:
    return np.log(px["Adj Close"]).diff().dropna()


def realized_cc(r: pd.Series, window: int) -> pd.Series:
    return r.rolling(window).std() * math.sqrt(ANN)


def realized_parkinson(px: pd.DataFrame, window: int) -> pd.Series:
    hl = np.log(px["High"] / px["Low"]) ** 2
    return np.sqrt(hl.rolling(window).mean() / (4 * math.log(2))) * math.sqrt(ANN)


def realized_yang_zhang(px: pd.DataFrame, window: int) -> pd.Series:
    o = np.log(px["Open"] / px["Close"].shift(1))
    c = np.log(px["Close"] / px["Open"])
    u = np.log(px["High"] / px["Open"])
    d = np.log(px["Low"] / px["Open"])
    rs = u * (u - c) + d * (d - c)
    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    var_o = o.rolling(window).var()
    var_c = c.rolling(window).var()
    var_rs = rs.rolling(window).mean()
    return np.sqrt(var_o + k * var_c + (1 - k) * var_rs) * math.sqrt(ANN)


def ewma_vol(r: pd.Series, lam: float = 0.94) -> float:
    r2 = r.values ** 2
    v = r2[0]
    for x in r2[1:]:
        v = lam * v + (1 - lam) * x
    return math.sqrt(v * ANN)


# ------------------------------------------------------------ GARCH(1,1) ----

def garch11(r: pd.Series) -> dict:
    """MLE fit on demeaned daily log returns (in %); normal likelihood."""
    x = (r - r.mean()).values * 100.0
    var_u = np.var(x)

    def nll(params):
        w, a, b = params
        if w <= 0 or a < 0 or b < 0 or a + b >= 0.9999:
            return 1e9
        v = np.empty_like(x)
        v[0] = var_u
        for t in range(1, len(x)):
            v[t] = w + a * x[t - 1] ** 2 + b * v[t - 1]
        v = np.maximum(v, 1e-10)
        return 0.5 * np.sum(np.log(v) + x ** 2 / v)

    best = None
    for a0, b0 in [(0.08, 0.90), (0.05, 0.93), (0.15, 0.80)]:
        w0 = var_u * (1 - a0 - b0)
        res = minimize(nll, [w0, a0, b0], method="Nelder-Mead",
                       options={"maxiter": 4000, "xatol": 1e-8, "fatol": 1e-8})
        if best is None or res.fun < best.fun:
            best = res
    w, a, b = best.x
    persistence = a + b
    uncond = math.sqrt(w / max(1 - persistence, 1e-9) * ANN) / 100
    # current conditional variance
    v = var_u
    for t in range(1, len(x)):
        v = w + a * x[t - 1] ** 2 + b * v
    sigma_1d = math.sqrt(v) / 100
    # n-day-ahead integrated vol (annualized), h steps
    h = 21
    vs, vt = [], v
    for _ in range(h):
        vt = w + persistence * vt if False else w + (a + b) * vt
        vs.append(vt)
    sigma_21d = math.sqrt(np.mean(vs) * ANN) / 100
    halflife = math.log(0.5) / math.log(persistence) if 0 < persistence < 1 else float("inf")
    return {"omega": w, "alpha": a, "beta": b, "persistence": persistence,
            "uncond_vol": uncond, "sigma_1d_ann": sigma_1d * math.sqrt(ANN),
            "sigma_21d_ann": sigma_21d, "halflife_days": halflife,
            "n_obs": len(x), "converged": bool(best.success)}


# --------------------------------------------------------------- vol cone ----

def vol_cone(r: pd.Series, horizons=(5, 10, 21, 63, 126, 252)) -> dict:
    out = {}
    for h in horizons:
        rv = r.rolling(h).std() * math.sqrt(ANN)
        rv = rv.dropna()
        out[h] = {
            "p10": float(rv.quantile(.10)), "p25": float(rv.quantile(.25)),
            "p50": float(rv.quantile(.50)), "p75": float(rv.quantile(.75)),
            "p90": float(rv.quantile(.90)), "now": float(rv.iloc[-1]),
        }
    return out


# ------------------------------------------------------ factor regression ----

def _nw_se(X: np.ndarray, resid: np.ndarray, lags: int = 5) -> np.ndarray:
    n, k = X.shape
    xtx_inv = np.linalg.inv(X.T @ X)
    u = X * resid[:, None]
    S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1)
        G = u[l:].T @ u[:-l]
        S += w * (G + G.T)
    cov = xtx_inv @ S @ xtx_inv
    return np.sqrt(np.diag(cov))


def factor_model(px: dict, years: int = 3) -> dict:
    """MU daily returns on market (SPY), sector-ex-market (SMH-SPY), rates (d10y pp),
    dollar (dln DXY). OLS + Newey-West t-stats + sequential variance decomposition."""
    mu = log_returns(px["MU"])
    spy = log_returns(px["SPY"])
    smh = log_returns(px["SMH"])
    tnx = (px["^TNX"]["Close"] / 10.0).diff()      # yield change in pp
    dxy = np.log(px["DX-Y.NYB"]["Close"]).diff()
    df = pd.concat([mu, spy, smh - spy, tnx, dxy], axis=1,
                   keys=["mu", "mkt", "sector", "rates", "fx"]).dropna()
    df = df.iloc[-int(ANN * years):]

    y = df["mu"].values
    order = ["mkt", "sector", "rates", "fx"]
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in order])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    se = _nw_se(X, resid)
    r2 = 1 - resid.var() / y.var()

    # sequential R^2: market -> +sector -> +rates -> +fx
    seq, prev = {}, 0.0
    for i in range(1, len(order) + 1):
        Xi = np.column_stack([np.ones(len(df))] + [df[c].values for c in order[:i]])
        bi = np.linalg.lstsq(Xi, y, rcond=None)[0]
        ri = 1 - (y - Xi @ bi).var() / y.var()
        seq[order[i - 1]] = ri - prev
        prev = ri
    seq["idiosyncratic"] = 1 - prev

    # practical hedge betas (univariate)
    b_smh = float(np.polyfit(df["mkt"] + df["sector"], y, 1)[0])  # vs SMH itself
    b_spy = float(np.polyfit(df["mkt"], y, 1)[0])

    return {
        "coef": {name: {"beta": float(beta[i + 1]), "t_nw": float(beta[i + 1] / se[i + 1])}
                 for i, name in enumerate(order)},
        "alpha_daily": float(beta[0]), "r2": float(r2),
        "var_decomp": {k: float(v) for k, v in seq.items()},
        "beta_spy_uni": b_spy, "beta_smh_uni": b_smh,
        "n_obs": int(len(df)), "years": years,
    }


def rolling_betas(px: dict, window: int = 252) -> pd.DataFrame:
    mu = log_returns(px["MU"])
    out = {}
    for name, tk in [("vs S&P 500", "SPY"), ("vs SMH", "SMH")]:
        f = log_returns(px[tk])
        df = pd.concat([mu, f], axis=1, keys=["mu", "f"]).dropna()
        cov = df["mu"].rolling(window).cov(df["f"])
        var = df["f"].rolling(window).var()
        out[name] = (cov / var)
    return pd.DataFrame(out).dropna()


# --------------------------------------------------------- earnings study ----

def earnings_study(yf: dict, px_mu: pd.DataFrame) -> dict:
    events = [e for e in yf.get("earnings_dates", []) if e.get("eps_act") is not None]
    idx = px_mu.index
    rows = []
    for e in events:
        d = pd.Timestamp(e["date"])
        pos = idx.searchsorted(d, side="right") - 1   # trading day of the announce
        if pos < 1 or pos + 1 >= len(idx):
            continue
        c0 = float(px_mu["Close"].iloc[pos])
        c1 = float(px_mu["Close"].iloc[pos + 1])
        o1 = float(px_mu["Open"].iloc[pos + 1])
        rows.append({"date": str(idx[pos].date()), "eps_est": e["eps_est"],
                     "eps_act": e["eps_act"],
                     "surprise": (e["eps_act"] / e["eps_est"] - 1) if e.get("eps_est") else None,
                     "gap": o1 / c0 - 1, "reaction": c1 / c0 - 1})
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    if df.empty:
        return {"events": df, "stats": {}}
    r = df["reaction"]
    all_r = np.log(px_mu["Adj Close"]).diff().loc[df["date"].iloc[0]:].dropna()
    var_share = float((r ** 2).sum() / (all_r ** 2).sum()) if len(all_r) else float("nan")
    stats = {
        "n": int(len(df)),
        "mean_abs": float(r.abs().mean()), "median_abs": float(r.abs().median()),
        "max_abs": float(r.abs().max()),
        "pct_up": float((r > 0).mean()),
        "mean_up": float(r[r > 0].mean()) if (r > 0).any() else 0.0,
        "mean_dn": float(r[r < 0].mean()) if (r < 0).any() else 0.0,
        "var_share": var_share,
        "n_days_span": int(len(all_r)),
    }
    return {"events": df, "stats": stats}


# ------------------------------------------------------------ implied vol ----

def implied_view(cboe: dict, yf: dict) -> dict:
    if not cboe or not cboe.get("expiries"):
        return {}
    spot = cboe.get("spot")
    term = [(e["dte"], e["atm_iv"]) for e in cboe["expiries"] if e.get("atm_iv")]
    skews = [(e["dte"], e["skew_25d"]) for e in cboe["expiries"]
             if e.get("skew_25d") is not None and 20 <= e["dte"] <= 90]
    next_earn = None
    for e in yf.get("earnings_dates", []):
        if e.get("eps_act") is None:                      # future event
            d = pd.Timestamp(e["date"])
            if d >= pd.Timestamp.now() - pd.Timedelta(days=2):
                next_earn = d if next_earn is None or d < next_earn else next_earn
    move = None
    if next_earn is not None:
        exps = [e for e in cboe["expiries"] if e.get("atm_iv")]
        pre = [e for e in exps if pd.Timestamp(e["expiry"]) < next_earn]
        post = [e for e in exps if pd.Timestamp(e["expiry"]) >= next_earn]
        if pre and post:
            b, a = pre[-1], post[0]
            # forward variance between the bracketing expiries, minus baseline
            # (far-dated IV) variance on the non-event days = the event's variance
            fwd_var = a["atm_iv"] ** 2 * a["dte"] / 365 - b["atm_iv"] ** 2 * b["dte"] / 365
            far = [e["atm_iv"] for e in exps if e["dte"] >= 300]
            base_iv = float(np.mean(far)) if far else min(e["atm_iv"] for e in exps)
            n_trad = max((a["dte"] - b["dte"]) * 5 / 7 - 1, 1)
            event_var = fwd_var - (base_iv ** 2 / 252) * n_trad
            move = {"pre_expiry": b["expiry"], "post_expiry": a["expiry"],
                    "fwd_vol_ann": math.sqrt(max(fwd_var, 1e-9) / ((a["dte"] - b["dte"]) / 365)),
                    "base_iv": base_iv,
                    "event_move_1sd": math.sqrt(event_var) if event_var > 0 else 0.0,
                    "method": "forward-variance differencing, far-dated IV baseline"}
        elif post and post[0].get("atm_straddle"):
            e = post[0]
            move = {"post_expiry": e["expiry"], "dte": e["dte"],
                    "implied_move_total": e["atm_straddle"] / spot,
                    "method": "ATM straddle to first post-earnings expiry (includes baseline vol)"}
    return {"spot": spot, "iv30": cboe.get("iv30"), "term": term,
            "skew_25d_1to3m": float(np.mean([s for _, s in skews])) if skews else None,
            "next_earnings": str(next_earn.date()) if next_earn is not None else None,
            "earnings_move": move, "asof": cboe.get("asof")}


# ------------------------------------------------------------ Korea link ----

def korea_leadlag(px: dict, years: int = 3) -> dict:
    mu = log_returns(px["MU"])
    out = {}
    for name, tk in [("SK Hynix", "000660.KS"), ("Samsung", "005930.KS")]:
        if tk not in px:
            continue
        kr = log_returns(px[tk])
        df = pd.concat([mu, kr], axis=1, keys=["mu", "kr"]).dropna()
        df = df.iloc[-int(ANN * years):]
        same = float(df["mu"].corr(df["kr"]))                    # KR closes ~14h before US
        us_leads = float(df["mu"].corr(df["kr"].shift(-1)))      # MU(t) vs KR(t+1)
        out[name] = {"kr_leads_us_same_date": same, "us_leads_kr_next": us_leads,
                     "n": int(len(df))}
    return out


# ------------------------------------------------------------------ tails ----

def tail_stats(px: dict, years: int = 10) -> dict:
    r = log_returns(px["MU"]).iloc[-int(ANN * years):]
    eq = np.exp(r.cumsum())
    dd = eq / eq.cummax() - 1
    worst = r.nsmallest(5)
    best = r.nlargest(5)
    smh = log_returns(px["SMH"])
    j = pd.concat([r, smh], axis=1, keys=["mu", "smh"]).dropna().iloc[-int(ANN * 3):]
    dn = j[j["smh"] < 0]
    up = j[j["smh"] > 0]
    return {
        "skew": float(r.skew()), "ex_kurt": float(r.kurt()),
        "var95": float(-r.quantile(.05)), "var99": float(-r.quantile(.01)),
        "es95": float(-r[r <= r.quantile(.05)].mean()),
        "max_dd": float(dd.min()),
        "dd_now": float(eq.iloc[-1] / eq.max() - 1),
        "worst": [(str(d.date()), float(v)) for d, v in worst.items()],
        "best": [(str(d.date()), float(v)) for d, v in best.items()],
        "down_capture": float(dn["mu"].mean() / dn["smh"].mean()) if len(dn) else None,
        "up_capture": float(up["mu"].mean() / up["smh"].mean()) if len(up) else None,
    }


# -------------------------------------------------------------------- run ----

def run(data: dict, cfg: dict) -> dict:
    px = data["prices"]
    rc = cfg["riskvol"]
    r_mu = log_returns(px["MU"])
    r10 = r_mu.iloc[-int(ANN * rc["vol_cone_years"]):]

    px_mu_recent = px["MU"].iloc[-int(ANN * 12):]   # OHLC estimators on clean data
    rv20 = realized_cc(r_mu, 20)
    rv60 = realized_cc(r_mu, 60)
    yz21 = realized_yang_zhang(px_mu_recent, 21)
    rv20_pct = float((rv20.iloc[-int(ANN * 10):].dropna() < rv20.iloc[-1]).mean())

    garch = garch11(r_mu.iloc[-int(ANN * rc["garch_years"]):])
    cone = vol_cone(r10)
    factors = factor_model(px, years=int(rc["factor_years_daily"]))
    rbetas = rolling_betas(px)
    earn = earnings_study(data["yf"], px["MU"])
    iv = implied_view(data.get("cboe", {}), data["yf"])
    kr = korea_leadlag(px)
    tails = tail_stats(px)

    vix_now = float(px["^VIX"]["Close"].iloc[-1]) if "^VIX" in px else None

    return {
        "rv20": float(rv20.iloc[-1]), "rv60": float(rv60.iloc[-1]),
        "yz21": float(yz21.iloc[-1]), "rv20_pctile_10y": rv20_pct,
        "ewma": ewma_vol(r_mu.iloc[-int(ANN * 3):]),
        "rv20_series": rv20, "rv60_series": rv60,
        "garch": garch, "cone": cone, "factors": factors,
        "rolling_betas": rbetas, "earnings": earn, "iv": iv,
        "korea": kr, "tails": tails, "vix": vix_now,
    }
