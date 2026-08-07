"""Pure-logic unit tests (no network, no credentials).

Run either with pytest, or directly:
    python tests/test_units.py      # from the alpaca-data/ directory
"""
from __future__ import annotations

import sys
from datetime import date

from alpaca_data.frames import normalize
from alpaca_data.ratelimit import TokenBucket
from alpaca_data.utils import (batched, daterange_chunks, is_occ, parse_date,
                               parse_occ, to_rfc3339, underlying_of)


def test_parse_occ():
    c = parse_occ("AAPL250117C00150000")
    assert c.underlying == "AAPL"
    assert c.expiration == date(2025, 1, 17)
    assert c.type == "call"
    assert abs(c.strike - 150.0) < 1e-9
    assert is_occ("AAPL250117C00150000")
    assert not is_occ("AAPL")
    assert underlying_of("AAPL250117P00150000") == "AAPL"
    assert underlying_of("nvda") == "NVDA"


def test_daterange_chunks_year():
    yr = list(daterange_chunks(date(2023, 3, 5), date(2025, 2, 1), "year"))
    assert yr[0] == (date(2023, 3, 5), date(2023, 12, 31))
    assert yr[1] == (date(2024, 1, 1), date(2024, 12, 31))
    assert yr[-1] == (date(2025, 1, 1), date(2025, 2, 1))


def test_daterange_chunks_month_leap():
    mo = list(daterange_chunks(date(2024, 1, 15), date(2024, 3, 2), "month"))
    assert mo[0] == (date(2024, 1, 15), date(2024, 1, 31))
    assert mo[1] == (date(2024, 2, 1), date(2024, 2, 29))  # leap February
    assert mo[2] == (date(2024, 3, 1), date(2024, 3, 2))


def test_daterange_chunks_day_and_empty():
    dd = list(daterange_chunks(date(2024, 1, 1), date(2024, 1, 3), "day"))
    assert dd == [(date(2024, 1, 1), date(2024, 1, 1)),
                  (date(2024, 1, 2), date(2024, 1, 2)),
                  (date(2024, 1, 3), date(2024, 1, 3))]
    assert list(daterange_chunks(date(2024, 2, 1), date(2024, 1, 1), "year")) == []


def test_batched():
    assert list(batched([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(batched([], 3)) == []


def test_normalize_bars():
    recs = [{"t": "2024-01-02T05:00:00Z", "o": 1, "h": 2, "l": 0.5,
             "c": 1.5, "v": 100, "n": 3, "vw": 1.4}]
    df = normalize(recs, "bars", symbol="AAPL")
    assert list(df.columns) == ["symbol", "timestamp", "open", "high", "low",
                                "close", "volume", "trade_count", "vwap"]
    assert df.loc[0, "symbol"] == "AAPL"
    assert str(df["timestamp"].dt.tz) == "UTC"
    empty = normalize([], "bars", symbol="AAPL")
    assert len(empty) == 0 and empty.columns[0] == "symbol"


def test_normalize_quotes_conditions_to_string():
    recs = [{"t": "2024-01-02T14:30:00Z", "ap": 1.0, "as": 2, "bp": 0.9, "bs": 3, "c": ["R"]}]
    df = normalize(recs, "quotes", symbol="AAPL")
    assert df.loc[0, "conditions"] == "R"
    assert df.loc[0, "ask_price"] == 1.0


def test_token_bucket_runs():
    tb = TokenBucket(60000)  # 1000/sec; a few acquires must not hang
    for _ in range(5):
        tb.acquire()


def test_time_helpers():
    assert to_rfc3339(date(2024, 1, 2)) == "2024-01-02"
    assert to_rfc3339("passthrough") == "passthrough"
    assert parse_date("2024-01-02T00:00:00Z") == date(2024, 1, 2)


def _run() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {t.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())
