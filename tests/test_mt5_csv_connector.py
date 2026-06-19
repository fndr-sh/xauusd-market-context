from pathlib import Path

import pytest

from xau_lfx.connectors.mt5_csv import CsvValidationError, parse_ohlcv_csv, parse_spread_csv


def test_valid_mt5_ohlcv_csv_parses():
    rows = parse_ohlcv_csv(Path("examples/sample-data/XAUUSD_M15.csv"))
    assert rows
    assert rows[0]["volume_type"] == "tick_volume"
    assert isinstance(rows[0]["close"], float)


def test_missing_required_ohlcv_column_fails(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("ts_utc,open,high,low,close\n2026-01-01T00:00:00Z,1,2,0.5,1.5\n", encoding="utf-8")
    with pytest.raises(CsvValidationError):
        parse_ohlcv_csv(path)


def test_spread_csv_parses_and_keeps_broker_policy():
    rows = parse_spread_csv(Path("examples/sample-data/XAUUSD_spread.csv"))
    assert rows
    assert rows[0]["spread_policy"] == "BROKER_SPECIFIC_SPREAD"
