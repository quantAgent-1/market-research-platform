"""Pure helpers: OCC option-symbol parsing, date chunking, time formatting.

No network or filesystem access here, so this module is trivially unit-testable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable, Iterator

# OCC 21-char option symbol: ROOT(1-6) + YYMMDD + C|P + strike*1000 (8 digits)
# e.g. AAPL250117C00150000 = AAPL 2025-01-17 $150.00 Call
_OCC_RE = re.compile(r"^(?P<root>[A-Z]{1,6})(?P<exp>\d{6})(?P<cp>[CP])(?P<strike>\d{8})$")


@dataclass(frozen=True)
class OptionContract:
    symbol: str
    underlying: str
    expiration: date
    type: str          # "call" | "put"
    strike: float


def is_occ(symbol: str) -> bool:
    return bool(_OCC_RE.match(symbol.strip().upper()))


def parse_occ(symbol: str) -> OptionContract:
    m = _OCC_RE.match(symbol.strip().upper())
    if not m:
        raise ValueError(f"Not a valid OCC option symbol: {symbol!r}")
    exp = m.group("exp")
    return OptionContract(
        symbol=symbol.strip().upper(),
        underlying=m.group("root"),
        expiration=date(2000 + int(exp[:2]), int(exp[2:4]), int(exp[4:6])),
        type="call" if m.group("cp") == "C" else "put",
        strike=int(m.group("strike")) / 1000.0,
    )


def underlying_of(symbol: str) -> str:
    """Underlying root of an OCC symbol, or the symbol itself if it isn't one."""
    return parse_occ(symbol).underlying if is_occ(symbol) else symbol.strip().upper()


def to_rfc3339(value: datetime | date | str) -> str:
    """Normalize a datetime/date/string to an Alpaca-acceptable RFC-3339 string."""
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return value.isoformat()  # plain date


def parse_date(value: str | date | datetime) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def day_start(d: date) -> datetime:
    return datetime.combine(d, time.min, tzinfo=timezone.utc)


def day_end(d: date) -> datetime:
    return datetime.combine(d, time.max, tzinfo=timezone.utc)


def daterange_chunks(start: date, end: date, by: str) -> Iterator[tuple[date, date]]:
    """Yield inclusive (chunk_start, chunk_end) spans covering [start, end].

    `by` in {"day", "month", "year"}. Chunks align to calendar boundaries so each
    chunk maps to exactly one partition file (idempotent re-runs).
    """
    if start > end:
        return
    cur = start
    while cur <= end:
        if by == "day":
            nxt = cur
        elif by == "month":
            nxt = (date(cur.year + (cur.month == 12), (cur.month % 12) + 1, 1) - timedelta(days=1))
        elif by == "year":
            nxt = date(cur.year, 12, 31)
        else:
            raise ValueError(f"Unknown chunk unit: {by!r}")
        yield cur, min(nxt, end)
        cur = nxt + timedelta(days=1)


def batched(items: Iterable, n: int) -> Iterator[list]:
    """Yield successive n-sized batches from an iterable."""
    buf: list = []
    for it in items:
        buf.append(it)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf
