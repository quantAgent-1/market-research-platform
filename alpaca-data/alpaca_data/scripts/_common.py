"""Shared CLI helpers: logging, client factory, universe resolution."""
from __future__ import annotations

import logging
import sys

import yaml

from ..config import PROJECT_ROOT, get_settings
from ..rest import AlpacaDataClient


def force_utf8() -> None:
    """Prevent UnicodeEncodeError when printing non-ASCII on legacy consoles (cp949)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def setup_logging(level: str = "INFO") -> None:
    force_utf8()
    logging.basicConfig(
        level=getattr(logging, str(level).upper(), logging.INFO),
        format="%(asctime)s %(levelname)-5s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def make_client() -> AlpacaDataClient:
    return AlpacaDataClient(get_settings())


def load_universe(spec: str) -> list[str]:
    """Resolve a symbol spec into a ticker list.

    Accepts: a comma list ("NVDA,AMD"), a universe file ("default"), a
    file:group ("default:ai_semis"), or a bare single symbol.
    """
    spec = spec.strip()
    if "," in spec:
        return [x.strip().upper() for x in spec.split(",") if x.strip()]
    file, _, group = spec.partition(":")
    path = PROJECT_ROOT / "universes" / f"{file}.yml"
    if not path.exists():
        return [spec.upper()]
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if group:
        syms = data.get(group) or []
    else:
        syms = sorted({s for lst in data.values() if isinstance(lst, list) for s in lst})
    return [str(s).upper() for s in syms]


def resolve_symbols(args, default: str = "default") -> list[str]:
    if getattr(args, "symbols", None):
        return load_universe(args.symbols)
    if getattr(args, "universe", None):
        return load_universe(args.universe)
    return load_universe(default)


def add_symbol_args(parser) -> None:
    parser.add_argument("--symbols", help="comma-separated tickers, e.g. NVDA,AMD")
    parser.add_argument("--universe", help="universe file[:group], e.g. default:ai_semis")
    parser.add_argument("--log", default="INFO", help="log level (DEBUG/INFO/WARNING)")
