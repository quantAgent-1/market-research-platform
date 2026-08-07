"""Alpaca market-data engine.

A small, robust toolkit for pulling Alpaca historical + streaming market data
(stocks, options, news, corporate actions) into a local DuckDB/Parquet research
lake for backtesting and theory verification.

Quick start (from the alpaca-data/ directory):
    python -m alpaca_data.scripts.smoke_test
    python -m alpaca_data.scripts.backfill_stocks --universe default --timeframe 1Day
"""
from .config import get_settings, load_settings, Settings

__all__ = ["get_settings", "load_settings", "Settings"]
__version__ = "0.1.0"
