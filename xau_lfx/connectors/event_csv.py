from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from xau_lfx.connectors.base import SourceRequest
from xau_lfx.utils import utc_now_iso

EVENT_REQUIRED_COLUMNS = ("ts_utc", "currency", "impact", "title")
ALLOWED_IMPACTS = {"LOW", "MEDIUM", "HIGH"}


class EventCsvValidationError(ValueError):
    pass


def _parse_utc(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise EventCsvValidationError("ts_utc is empty")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EventCsvValidationError(f"ts_utc is not ISO-8601: {value}") from exc
    if parsed.tzinfo is None:
        raise EventCsvValidationError(f"ts_utc has no timezone: {value}")
    return parsed.astimezone(timezone.utc).isoformat()


def parse_event_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = [column for column in EVENT_REQUIRED_COLUMNS if column not in fieldnames]
        if missing:
            raise EventCsvValidationError(f"missing required columns in {path.name}: {missing}")
        events: list[dict[str, Any]] = []
        for index, row in enumerate(reader, start=2):
            impact = row["impact"].strip().upper()
            if impact not in ALLOWED_IMPACTS:
                raise EventCsvValidationError(f"{path.name}: row {index}: invalid impact: {row['impact']}")
            currency = row["currency"].strip().upper()
            title = row["title"].strip()
            if not currency:
                raise EventCsvValidationError(f"{path.name}: row {index}: currency is empty")
            if not title:
                raise EventCsvValidationError(f"{path.name}: row {index}: title is empty")
            events.append(
                {
                    "ts_utc": _parse_utc(row["ts_utc"]),
                    "currency": currency,
                    "impact": impact,
                    "title": title,
                    "event_policy": "risk_context_only_no_direction_prediction",
                }
            )
    return events


class EventCsvConnector:
    source_id = "EVENT_CSV"

    def __init__(self, event_file: str | Path) -> None:
        self.event_file = Path(event_file)

    def fetch(self, request: SourceRequest) -> dict[str, Any]:
        errors: list[str] = []
        quality_flags: list[str] = []
        events: list[dict[str, Any]] = []
        try:
            events = parse_event_csv(self.event_file)
            if not events:
                quality_flags.append("EVENT_CSV_EMPTY")
        except FileNotFoundError:
            errors.append(f"missing file: {self.event_file.name}")
            quality_flags.append("EVENT_CSV_MISSING")
        except EventCsvValidationError as exc:
            errors.append(str(exc))
            quality_flags.append("EVENT_CSV_INVALID")

        return {
            "ts_utc": utc_now_iso(),
            "source_id": self.source_id,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "status": "OK" if not errors else "ERROR",
            "payload": events,
            "row_count": len(events),
            "errors": errors,
            "quality_flags": sorted(set(quality_flags)),
        }
