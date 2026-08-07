"""Command-line entry points. Run from the alpaca-data/ directory, e.g.:

    python -m alpaca_data.scripts.smoke_test
    python -m alpaca_data.scripts.backfill_stocks --universe default:ai_semis --timeframe 1Day
    python -m alpaca_data.scripts.query "SELECT count(*) FROM stocks_bars"
"""
