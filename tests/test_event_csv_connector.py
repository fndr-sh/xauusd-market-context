from pathlib import Path

import pytest

from xau_lfx.connectors.event_csv import EventCsvValidationError, parse_event_csv


def test_event_csv_parses_allowed_impacts():
    events = parse_event_csv(Path("examples/sample-data/usd_events.csv"))
    assert {event["impact"] for event in events} <= {"LOW", "MEDIUM", "HIGH"}
    assert events[0]["currency"] == "USD"


def test_invalid_event_impact_fails(tmp_path):
    path = tmp_path / "events.csv"
    path.write_text("ts_utc,currency,impact,title\n2026-01-01T00:00:00Z,USD,CRITICAL,Invalid\n", encoding="utf-8")
    with pytest.raises(EventCsvValidationError):
        parse_event_csv(path)
