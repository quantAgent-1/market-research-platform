"""muval.data — fetch + cache layer. Files are the database (store/cache/).

Sources (all free, all verified reachable from this machine 2026-07-11):
  - yfinance   : prices (40y OHLCV), statements (5y), analyst estimates, earnings dates, info
  - macrotrends: long annual fundamentals (revenue/margins/capex/equity/shares, ~20y)
  - CBOE       : delayed option chain -> ATM IV term structure, skew, implied earnings move
  - FRED       : DGS10 (risk-free anchor)

EDGAR companyfacts is geo-blocked from this machine (SEC 403s non-US IPs) -- macrotrends
is the long-history substitute; provenance is stamped on every cache file.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

TOOL_DIR = Path(__file__).resolve().parent
CACHE = TOOL_DIR / "store" / "cache"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) personal research"}

TICKERS = {
    "MU": "Micron",
    "SMH": "Semis ETF",
    "SPY": "S&P 500 ETF",
    "^VIX": "VIX",
    "^TNX": "US 10y yield x10",
    "DX-Y.NYB": "Dollar index",
    "WDC": "Western Digital",
    "STX": "Seagate",
    "TSM": "TSMC ADR",
    "NVDA": "Nvidia",
    "005930.KS": "Samsung Electronics",
    "000660.KS": "SK Hynix",
}

MACROTRENDS_SLUGS = {"MU": "micron-technology", "NVDA": "nvidia", "AMD": "amd"}

MACROTRENDS_PAGES = {
    "revenue": "revenue",
    "gross_profit": "gross-profit",
    "operating_income": "operating-income",
    "net_income": "net-income",
    "eps_diluted": "eps-earnings-per-share-diluted",
    "shares_outstanding": "shares-outstanding",
    "equity": "total-share-holder-equity",
    "dna": "total-depreciation-amortization-cash-flow",
    "rnd": "research-development-expenses",
    "cfo": "cash-flow-from-operating-activities",
    "fcf": "free-cash-flow",  # macrotrends FCF = CFO - capex, so capex = cfo - fcf
    "inventory": "inventory",
    "long_term_debt": "long-term-debt",
}
# per-share pages report dollars; everything else is $ millions
_PER_SHARE = {"eps_diluted"}


def _fresh(path: Path, max_age_hours: float) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < max_age_hours * 3600


def _stamp(payload: dict, source: str) -> dict:
    payload["_meta"] = {"source": source, "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    return payload


# ---------------------------------------------------------------- prices ----

def prices(ticker: str, offline: bool = False, refresh: bool = False) -> pd.DataFrame:
    """Daily OHLCV + Adj Close, full history, cached one day."""
    safe = ticker.replace("^", "_").replace(".", "_").replace("-", "_")
    path = CACHE / "prices" / f"{safe}.csv"
    if not refresh and (offline or _fresh(path, 24)):
        if path.exists():
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            return df
        if offline:
            raise FileNotFoundError(f"offline and no price cache for {ticker}")
    import yfinance as yf

    h = yf.Ticker(ticker).history(period="max", auto_adjust=False)
    if h.empty:
        raise RuntimeError(f"no price data for {ticker}")
    h.index = pd.to_datetime(h.index).tz_localize(None)
    h = h[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].dropna(how="all")
    path.parent.mkdir(parents=True, exist_ok=True)
    h.to_csv(path)
    return h


def all_prices(offline: bool = False, refresh: bool = False) -> dict[str, pd.DataFrame]:
    out = {}
    for tk in TICKERS:
        try:
            out[tk] = prices(tk, offline=offline, refresh=refresh)
        except Exception as e:  # non-core tickers may fail without sinking the run
            print(f"  [warn] prices {tk}: {e}")
    if "MU" not in out:
        raise RuntimeError("MU price history is required")
    return out


# ----------------------------------------------------------- yf bundles ----

def _migrate_legacy_yf_cache() -> None:
    """One-time migration: the pre-multi-ticker cache (yf_fundamentals.json, MU-only)
    becomes yf_fundamentals_MU.json under the new per-ticker naming. Old file is left
    in place (never deleted) so nothing downstream that still points at it breaks."""
    old = CACHE / "yf_fundamentals.json"
    new = CACHE / "yf_fundamentals_MU.json"
    if old.exists() and not new.exists():
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(old, new)
        print("  [data] migrated yf_fundamentals.json -> yf_fundamentals_MU.json")


def yf_fundamentals(ticker: str = "MU", offline: bool = False, refresh: bool = False) -> dict:
    """Statements (5y annual + quarterly), info snapshot, estimates, earnings dates."""
    _migrate_legacy_yf_cache()
    path = CACHE / f"yf_fundamentals_{ticker}.json"
    if not refresh and (offline or _fresh(path, 24 * 3)):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        if offline:
            raise FileNotFoundError(f"offline and no yf_fundamentals cache for {ticker}")
    import yfinance as yf

    t = yf.Ticker(ticker)
    out: dict = {}

    def df_pack(df: pd.DataFrame) -> dict:
        if df is None or df.empty:
            return {}
        d = {}
        for col in df.columns:
            key = str(pd.Timestamp(col).date())
            d[key] = {str(ix): (None if pd.isna(v) else float(v)) for ix, v in df[col].items()}
        return d

    out["income_annual"] = df_pack(t.get_income_stmt(freq="yearly"))
    out["income_quarterly"] = df_pack(t.get_income_stmt(freq="quarterly"))
    out["balance_annual"] = df_pack(t.get_balance_sheet(freq="yearly"))
    out["balance_quarterly"] = df_pack(t.get_balance_sheet(freq="quarterly"))
    out["cashflow_annual"] = df_pack(t.get_cashflow(freq="yearly"))
    out["cashflow_quarterly"] = df_pack(t.get_cashflow(freq="quarterly"))

    info = t.info or {}
    keep = [
        "currentPrice", "marketCap", "sharesOutstanding", "impliedSharesOutstanding",
        "beta", "trailingPE", "forwardPE", "priceToBook", "bookValue", "totalDebt",
        "totalCash", "freeCashflow", "operatingCashflow", "trailingEps", "forwardEps",
        "dividendYield", "earningsGrowth", "revenueGrowth", "grossMargins",
        "operatingMargins", "profitMargins", "enterpriseValue", "enterpriseToEbitda",
        "ebitda", "shortPercentOfFloat", "shortRatio", "heldPercentInstitutions",
        "targetMeanPrice", "targetHighPrice", "targetLowPrice", "targetMedianPrice",
        "numberOfAnalystOpinions", "recommendationKey",
    ]
    out["info"] = {k: info.get(k) for k in keep}

    def est_pack(df) -> dict:
        try:
            if df is None or len(df) == 0:
                return {}
            return {str(ix): {str(c): (None if pd.isna(v) else float(v)) for c, v in row.items()}
                    for ix, row in df.iterrows()}
        except Exception:
            return {}

    out["revenue_estimate"] = est_pack(t.revenue_estimate)
    out["earnings_estimate"] = est_pack(t.earnings_estimate)

    try:
        ed = t.get_earnings_dates(limit=50)
        out["earnings_dates"] = [
            {"date": str(pd.Timestamp(ix).date()),
             "eps_est": (None if pd.isna(r.get("EPS Estimate")) else float(r.get("EPS Estimate"))),
             "eps_act": (None if pd.isna(r.get("Reported EPS")) else float(r.get("Reported EPS")))}
            for ix, r in ed.iterrows()
        ]
    except Exception as e:
        print(f"  [warn] earnings dates: {e}")
        out["earnings_dates"] = []

    # peer snapshot for the multiples table (best effort) -- MU-only; other tickers
    # get an empty peers block (no defined peer set for them yet).
    if ticker == "MU":
        peers = {}
        for tk in ["WDC", "STX", "TSM", "NVDA", "005930.KS", "000660.KS"]:
            try:
                pi = yf.Ticker(tk).info or {}
                peers[tk] = {k: pi.get(k) for k in
                             ["forwardPE", "trailingPE", "priceToBook", "enterpriseToEbitda",
                              "marketCap", "profitMargins", "revenueGrowth"]}
            except Exception:
                peers[tk] = {}
        out["peers"] = peers
    else:
        out["peers"] = {}

    _stamp(out, "yfinance")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ---------------------------------------------------------- macrotrends ----

def _parse_macrotrends_annual(html: str) -> dict[int, float]:
    """First table whose col0 parses as 4-digit years; values '$37,378' in $M."""
    tables = pd.read_html(io.StringIO(html))
    for tb in tables:
        if tb.shape[1] < 2:
            continue
        c0 = tb.iloc[:, 0].astype(str).str.strip()
        years = c0.str.fullmatch(r"(19|20)\d{2}(\.0)?")
        if years.sum() >= 5:
            out = {}
            for _, row in tb[years.fillna(False)].iterrows():
                y = int(float(str(row.iloc[0]).strip()))
                raw = str(row.iloc[1]).replace("$", "").replace(",", "").strip()
                if raw in ("", "nan", "-", "N/A"):
                    continue
                try:
                    out[y] = float(raw)
                except ValueError:
                    continue
            if out:
                return out
    return {}


def _discover_macrotrends_slug(ticker: str) -> str | None:
    """Fetch the bare ticker chart URL; macrotrends 301s it to the canonical
    .../charts/{TICKER}/{slug}/... page -- read the slug off the post-redirect URL.
    Note: the bare-root redirect target itself 404s (macrotrends only serves actual
    metric pages, not the company root), so this deliberately does NOT raise_for_status;
    r.url is populated correctly by requests' redirect-following regardless of the
    final page's status code, and that's all this needs."""
    try:
        r = requests.get(f"https://www.macrotrends.net/stocks/charts/{ticker}/",
                         headers=UA, timeout=25)
        segs = [s for s in r.url.split("/") if s]
        if "charts" in segs:
            i = segs.index("charts")
            if i + 2 < len(segs) and segs[i + 1].upper() == ticker.upper():
                return segs[i + 2]
    except Exception as e:
        print(f"  [warn] macrotrends slug discovery for {ticker}: {e}")
    return None


def macrotrends_long(ticker: str = "MU", offline: bool = False, refresh: bool = False) -> dict:
    """Long annual fundamentals for one ticker, one dict {metric: {year: value}}. $ millions
    except per-share metrics. Cached 14 days (annual data moves quarterly)."""
    path = CACHE / f"macrotrends_{ticker.lower()}.json"
    if not refresh and (offline or _fresh(path, 24 * 14)):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        if offline:
            raise FileNotFoundError(f"offline and no macrotrends cache for {ticker}")
    slug = MACROTRENDS_SLUGS.get(ticker, "")
    slug_source = "known" if slug else "discovered"
    if not slug:
        discovered = _discover_macrotrends_slug(ticker)
        if discovered:
            slug = discovered
        else:
            print(f"  [warn] macrotrends: could not resolve a slug for {ticker}")
    out: dict = {}
    for metric, page in MACROTRENDS_PAGES.items():
        parsed = {}
        for attempt in range(3):
            try:
                base = f"https://www.macrotrends.net/stocks/charts/{ticker}/{slug}/"
                r = requests.get(base + page, headers=UA, timeout=25)
                if r.status_code == 429:
                    time.sleep(5 * (attempt + 1))
                    continue
                if r.status_code == 404:
                    discovered = _discover_macrotrends_slug(ticker)
                    if discovered and discovered != slug:
                        slug = discovered
                        slug_source = "discovered (redirect after 404)"
                        continue
                r.raise_for_status()
                parsed = _parse_macrotrends_annual(r.text)
                break
            except Exception as e:
                if attempt == 2:
                    print(f"  [warn] macrotrends {metric}: {e}")
        if not parsed:
            print(f"  [warn] macrotrends {metric}: no data")
        out[metric] = {str(y): v for y, v in sorted(parsed.items())}
        time.sleep(1.5)
    print(f"  [data] macrotrends slug for {ticker}: {slug or '?'} ({slug_source})")
    _stamp(out, "macrotrends.net (annual, $M except per-share)")
    out["_meta"]["slug"] = slug
    out["_meta"]["ticker"] = ticker
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ----------------------------------------------------------------- CBOE ----

def cboe_options(ticker: str = "MU", offline: bool = False, refresh: bool = False) -> dict:
    """Distilled option surface: spot, iv30, per-expiry ATM IV / OI / 25-delta skew,
    plus raw ATM quotes for the earnings-straddle calc. Cached 1 day."""
    path = CACHE / f"cboe_{ticker.lower()}.json"
    if not refresh and (offline or _fresh(path, 24)):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        if offline:
            return {}
    # anchored to the exact ticker root -- deliberately drops adjusted option roots
    # like "NVDA1" (fine: we only need clean ATM quotes).
    opt_re = re.compile(rf"^{ticker}(\d{{6}})([CP])(\d{{8}})$")
    try:
        r = requests.get(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{ticker}.json",
                         headers=UA, timeout=40)
        r.raise_for_status()
        j = r.json()
    except Exception as e:
        print(f"  [warn] CBOE options {ticker}: {e}")
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    d = j.get("data", {})
    spot = d.get("current_price") or d.get("close")
    rows = []
    for o in d.get("options", []):
        m = opt_re.match(o.get("option", ""))
        if not m:
            continue
        exp = datetime.strptime(m.group(1), "%y%m%d").date()
        rows.append({
            "expiry": str(exp), "cp": m.group(2), "strike": int(m.group(3)) / 1000.0,
            "bid": o.get("bid") or 0.0, "ask": o.get("ask") or 0.0,
            "iv": o.get("iv") or 0.0, "delta": o.get("delta") or 0.0,
            "oi": o.get("open_interest") or 0.0, "vol": o.get("volume") or 0.0,
            "theo": o.get("theo") or 0.0,
        })
    df = pd.DataFrame(rows)
    today = datetime.now().date()
    out: dict = {"spot": spot, "iv30": d.get("iv30"), "asof": str(today), "expiries": []}
    if not df.empty:
        for exp, g in df.groupby("expiry"):
            dte = (datetime.strptime(exp, "%Y-%m-%d").date() - today).days
            if dte <= 0 or dte > 550:
                continue
            g = g[g["iv"] > 0.01]
            if g.empty:
                continue
            k_atm = g.loc[(g["strike"] - spot).abs().idxmin(), "strike"]
            atm = g[g["strike"] == k_atm]
            atm_iv = float(atm["iv"].mean())
            calls, puts = g[g["cp"] == "C"], g[g["cp"] == "P"]
            skew = None
            if len(calls) and len(puts):
                c25 = calls.loc[(calls["delta"] - 0.25).abs().idxmin()]
                p25 = puts.loc[(puts["delta"] + 0.25).abs().idxmin()]
                if abs(c25["delta"] - 0.25) < 0.10 and abs(p25["delta"] + 0.25) < 0.10:
                    skew = float(p25["iv"] - c25["iv"])

            def mid(row) -> float:
                b, a = float(row["bid"]), float(row["ask"])
                if b > 0 and a > 0:
                    return (b + a) / 2
                return float(row["theo"]) if row["theo"] else 0.0

            call_atm = atm[atm["cp"] == "C"]
            put_atm = atm[atm["cp"] == "P"]
            straddle = None
            if len(call_atm) and len(put_atm):
                cm, pm = mid(call_atm.iloc[0]), mid(put_atm.iloc[0])
                if cm > 0 and pm > 0:
                    straddle = cm + pm
            out["expiries"].append({
                "expiry": exp, "dte": dte, "atm_strike": float(k_atm), "atm_iv": atm_iv,
                "skew_25d": skew, "oi": float(g["oi"].sum()), "volume": float(g["vol"].sum()),
                "atm_straddle": straddle,
            })
        out["expiries"].sort(key=lambda x: x["dte"])
    _stamp(out, "CBOE delayed quotes")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ----------------------------------------------------------------- FRED ----

def risk_free(offline: bool = False, refresh: bool = False) -> dict:
    """US 10y constant-maturity yield (DGS10), last print. Cached 1 day."""
    path = CACHE / "fred_dgs10.json"
    if not refresh and (offline or _fresh(path, 24)):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        if offline:
            return {"rate": None}
    try:
        r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10", timeout=25)
        r.raise_for_status()
        lines = [ln for ln in r.text.strip().splitlines()[1:] if "," in ln]
        rate, asof = None, None
        for ln in reversed(lines):
            dt, val = ln.split(",", 1)
            try:
                rate, asof = float(val), dt
                break
            except ValueError:
                continue
        out = _stamp({"rate": rate, "asof": asof}, "FRED DGS10")
    except Exception as e:
        print(f"  [warn] FRED DGS10: {e}")
        out = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"rate": None}
        return out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ------------------------------------------------------------ orchestrate --

def pull_all(offline: bool = False, refresh: bool = False, names: tuple[str, ...] = ("MU",)) -> dict:
    """Pull prices (shared, all TICKERS) + per-name fundamentals/macrotrends/cboe for
    every ticker in `names`. Back-compat: the top-level "yf"/"macrotrends"/"cboe" keys
    always mirror names[0] (byte-identical to the pre-multi-ticker shape when
    names==("MU",), the default); "by_name" additionally covers every requested name."""
    print("[data] prices ...")
    px = all_prices(offline=offline, refresh=refresh)
    print(f"[data] prices ok ({len(px)} tickers; MU {px['MU'].index[0].date()} -> {px['MU'].index[-1].date()})")

    by_name: dict[str, dict] = {}
    for name in names:
        print(f"[data] fundamentals (yfinance) {name} ...")
        yff = yf_fundamentals(name, offline=offline, refresh=refresh)
        print(f"[data] long history (macrotrends) {name} ...")
        mt = macrotrends_long(name, offline=offline, refresh=refresh)
        n_years = len(mt.get("revenue", {}))
        print(f"[data] macrotrends ok ({name}, {n_years} revenue years)")
        print(f"[data] options (CBOE) {name} ...")
        cb = cboe_options(name, offline=offline, refresh=refresh)
        print(f"[data] cboe ok ({name}, {len(cb.get('expiries', []))} expiries)" if cb
              else f"[data] cboe unavailable ({name})")
        by_name[name] = {"yf": yff, "macrotrends": mt, "cboe": cb}

    rf = risk_free(offline=offline, refresh=refresh)
    print(f"[data] risk-free 10y = {rf.get('rate')}% ({rf.get('asof')})")

    first = names[0]
    return {
        "prices": px,
        "yf": by_name[first]["yf"],
        "macrotrends": by_name[first]["macrotrends"],
        "cboe": by_name[first]["cboe"],
        "riskfree": rf,
        "by_name": by_name,
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    pull_all(refresh="--refresh" in sys.argv, offline="--offline" in sys.argv)
