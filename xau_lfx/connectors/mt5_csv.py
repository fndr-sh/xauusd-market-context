from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from xau_lfx.connectors.base import SourceRequest
from xau_lfx.utils import utc_now_iso

OHLCV_REQUIRED_COLUMNS = ("ts_utc", "open", "high", "low", "close", "tick_volume")
SPREAD_REQUIRED_COLUMNS = ("ts_utc", "bid", "ask", "spread_points")
DEFAULT_TIMEFRAMES = ("M5", "M15", "H1")


class CsvValidationError(ValueError):
    pass


def _parse_utc(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise CsvValidationError("ts_utc is empty")
    normalized = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise CsvValidationError(f"ts_utc is not ISO-8601: {value}") from exc
    if parsed.tzinfo is None:
        raise CsvValidationError(f"ts_utc has no timezone: {value}")
    return parsed.astimezone(timezone.utc).isoformat()


def _to_float(value: str, column: str) -> float:
    raw = str(value).strip()
    if raw == "":
        raise CsvValidationError(f"{column} is empty")
    try:
        return float(raw)
    except ValueError as exc:
        raise CsvValidationError(f"{column} is not numeric: {value}") from exc


def _read_csv_rows(path: Path, required_columns: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = [column for column in required_columns if column not in fieldnames]
        if missing:
            raise CsvValidationError(f"missing required columns in {path.name}: {missing}")
        return list(reader)


def parse_ohlcv_csv(path: Path) -> list[dict[str, Any]]:
    rows = _read_csv_rows(path, OHLCV_REQUIRED_COLUMNS)
    parsed: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        try:
            parsed.append(
                {
                    "ts_utc": _parse_utc(row["ts_utc"]),
                    "open": _to_float(row["open"], "open"),
                    "high": _to_float(row["high"], "high"),
                    "low": _to_float(row["low"], "low"),
                    "close": _to_float(row["close"], "close"),
                    "tick_volume": _to_float(row["tick_volume"], "tick_volume"),
                    "volume_type": "tick_volume",
                }
            )
        except CsvValidationError as exc:
            raise CsvValidationError(f"{path.name}: row {index}: {exc}") from exc
    return parsed


def parse_spread_csv(path: Path) -> list[dict[str, Any]]:
    rows = _read_csv_rows(path, SPREAD_REQUIRED_COLUMNS)
    parsed: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        try:
            parsed.append(
                {
                    "ts_utc": _parse_utc(row["ts_utc"]),
                    "bid": _to_float(row["bid"], "bid"),
                    "ask": _to_float(row["ask"], "ask"),
                    "spread_points": _to_float(row["spread_points"], "spread_points"),
                    "spread_policy": "BROKER_SPECIFIC_SPREAD",
                }
            )
        except CsvValidationError as exc:
            raise CsvValidationError(f"{path.name}: row {index}: {exc}") from exc
    return parsed


class MT5CsvConnector:
    source_id = "MT5_CSV"

    def __init__(self, input_dir: str | Path, timeframes: tuple[str, ...] = DEFAULT_TIMEFRAMES) -> None:
        self.input_dir = Path(input_dir)
        self.timeframes = timeframes

    def fetch(self, request: SourceRequest) -> dict[str, Any]:
        errors: list[str] = []
        quality_flags: list[str] = []
        ohlcv: dict[str, list[dict[str, Any]]] = {}

        for timeframe in self.timeframes:
            path = self.input_dir / f"{request.symbol}_{timeframe}.csv"
            try:
                rows = parse_ohlcv_csv(path)
                ohlcv[timeframe] = rows
                if not rows:
                    quality_flags.append(f"{timeframe}_CSV_EMPTY")
            except FileNotFoundError:
                errors.append(f"missing file: {path.name}")
                quality_flags.append(f"{timeframe}_CSV_MISSING")
            except CsvValidationError as exc:
                errors.append(str(exc))
                quality_flags.append(f"{timeframe}_CSV_INVALID")

        spread_path = self.input_dir / f"{request.symbol}_spread.csv"
        spread: list[dict[str, Any]] = []
        try:
            spread = parse_spread_csv(spread_path)
            if not spread:
                quality_flags.append("SPREAD_CSV_EMPTY")
        except FileNotFoundError:
            quality_flags.append("SPREAD_CSV_MISSING")
        except CsvValidationError as exc:
            errors.append(str(exc))
            quality_flags.append("SPREAD_CSV_INVALID")

        status = "OK" if not errors and ohlcv else "ERROR" if errors else "WARN"
        return {
            "ts_utc": utc_now_iso(),
            "source_id": self.source_id,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "status": status,
            "payload": {
                "ohlcv": ohlcv,
                "spread": spread,
                "volume_policy": "tick_volume is broker tick activity, not centralized real volume",
            },
            "row_counts": {
                "ohlcv": {timeframe: len(rows) for timeframe, rows in ohlcv.items()},
                "spread": len(spread),
            },
            "errors": errors,
            "quality_flags": sorted(set(quality_flags)),
        }
