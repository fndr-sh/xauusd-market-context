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


def test_ohlcv_high_below_close_fails(tmp_path):
    path = tmp_path / "bad_high.csv"
    path.write_text(
        "ts_utc,open,high,low,close,tick_volume\n"
        "2026-01-01T00:00:00Z,100,101,99,102,10\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="high is below open/close"):
        parse_ohlcv_csv(path)


def test_ohlcv_low_above_open_fails(tmp_path):
    path = tmp_path / "bad_low.csv"
    path.write_text(
        "ts_utc,open,high,low,close,tick_volume\n"
        "2026-01-01T00:00:00Z,100,103,101,102,10\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="low is above open/close"):
        parse_ohlcv_csv(path)


def test_ohlcv_duplicate_timestamp_fails(tmp_path):
    path = tmp_path / "duplicate_ts.csv"
    path.write_text(
        "ts_utc,open,high,low,close,tick_volume\n"
        "2026-01-01T00:00:00Z,100,101,99,100.5,10\n"
        "2026-01-01T00:00:00Z,100,101,99,100.5,11\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="duplicate ts_utc"):
        parse_ohlcv_csv(path)


def test_ohlcv_non_increasing_timestamp_fails(tmp_path):
    path = tmp_path / "non_increasing_ts.csv"
    path.write_text(
        "ts_utc,open,high,low,close,tick_volume\n"
        "2026-01-01T00:05:00Z,100,101,99,100.5,10\n"
        "2026-01-01T00:00:00Z,100,101,99,100.5,11\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="strictly increasing"):
        parse_ohlcv_csv(path)


def test_ohlcv_negative_tick_volume_fails(tmp_path):
    path = tmp_path / "negative_volume.csv"
    path.write_text(
        "ts_utc,open,high,low,close,tick_volume\n"
        "2026-01-01T00:00:00Z,100,101,99,100.5,-1\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="tick_volume is negative"):
        parse_ohlcv_csv(path)


def test_spread_csv_parses_and_keeps_broker_policy():
    rows = parse_spread_csv(Path("examples/sample-data/XAUUSD_spread.csv"))
    assert rows
    assert rows[0]["spread_policy"] == "BROKER_SPECIFIC_SPREAD"


def test_spread_ask_below_bid_fails(tmp_path):
    path = tmp_path / "bad_spread.csv"
    path.write_text(
        "ts_utc,bid,ask,spread_points\n"
        "2026-01-01T00:00:00Z,2000.10,2000.00,10\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="ask is below bid"):
        parse_spread_csv(path)


def test_spread_negative_points_fails(tmp_path):
    path = tmp_path / "negative_spread.csv"
    path.write_text(
        "ts_utc,bid,ask,spread_points\n"
        "2026-01-01T00:00:00Z,2000.00,2000.10,-1\n",
        encoding="utf-8",
    )
    with pytest.raises(CsvValidationError, match="spread_points is negative"):
        parse_spread_csv(path)
