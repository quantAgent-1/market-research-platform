"""Configuration: load settings from the .env file and expose a Settings object.

Real OS environment variables take precedence over the .env file, so the same
code runs in CI / containers without a .env present.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# alpaca_data/ package dir -> alpaca-data/ project root (one level up).
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent

# Load alpaca-data/.env if present. override=False => real env vars win.
load_dotenv(PROJECT_ROOT / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_secret: str
    data_url: str
    trading_url: str
    stream_url_stocks: str
    stream_url_options: str
    stock_feed: str        # "sip" | "iex" | "delayed_sip" | ...
    options_feed: str      # "opra" | "indicative"
    store_root: Path
    max_requests_per_min: int

    @property
    def auth_headers(self) -> dict:
        return {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
        }

    @property
    def is_paper_key(self) -> bool:
        return self.api_key.upper().startswith("PK")


def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(
            f"Missing required env var {name!r}. "
            f"Copy .env.example to .env in the alpaca-data/ folder and fill it in."
        )
    return val


def load_settings() -> Settings:
    store_root = Path(os.getenv("STORE_ROOT", "store"))
    if not store_root.is_absolute():
        store_root = PROJECT_ROOT / store_root
    return Settings(
        api_key=_require("ALPACA_API_KEY"),
        api_secret=_require("ALPACA_API_SECRET"),
        data_url=os.getenv("ALPACA_DATA_URL", "https://data.alpaca.markets").rstrip("/"),
        trading_url=os.getenv("ALPACA_TRADING_URL", "https://paper-api.alpaca.markets").rstrip("/"),
        stream_url_stocks=os.getenv(
            "ALPACA_STREAM_URL_STOCKS", "wss://stream.data.alpaca.markets/v2/{feed}"
        ),
        stream_url_options=os.getenv(
            "ALPACA_STREAM_URL_OPTIONS", "wss://stream.data.alpaca.markets/v1beta1/{feed}"
        ),
        stock_feed=os.getenv("DATA_FEED_TYPE", "sip").strip().lower(),
        options_feed=os.getenv("OPTIONS_FEED_TYPE", "opra").strip().lower(),
        store_root=store_root,
        max_requests_per_min=int(os.getenv("ALPACA_MAX_REQUESTS_PER_MIN", "9000")),
    )


_SETTINGS: Settings | None = None


def get_settings() -> Settings:
    """Cached settings singleton."""
    global _SETTINGS
    if _SETTINGS is None:
        _SETTINGS = load_settings()
    return _SETTINGS
