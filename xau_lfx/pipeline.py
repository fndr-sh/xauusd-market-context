from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from xau_lfx.config import ARTIFACTS, DEFAULT_SYMBOL, PACKAGE_ROOT, artifact_paths
from xau_lfx.connectors.base import SourceRequest
from xau_lfx.connectors.event_calendar import EventCalendarConnector
from xau_lfx.connectors.event_csv import EventCsvConnector
from xau_lfx.connectors.mt5_csv import MT5CsvConnector
from xau_lfx.connectors.mt5_feed import MT5FeedConnector
from xau_lfx.connectors.public_market import PublicMarketConnector
from xau_lfx.engines.artifact_quality import build_artifact_quality
from xau_lfx.engines.composite_ohlcv import build_composite_ohlcv
from xau_lfx.engines.context_summary import build_context_summary
from xau_lfx.engines.data_quality import build_data_quality
from xau_lfx.engines.event_risk import build_event_risk
from xau_lfx.engines.lfx_state_adapter import build_external_state
from xau_lfx.engines.macro_pressure import build_macro_pressure
from xau_lfx.engines.normalizer import normalize_raw_scan
from xau_lfx.engines.session_context import build_session_context
from xau_lfx.engines.user_insight import build_user_insight
from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.reports.market_context_report import write_market_context_report
from xau_lfx.reports.static_site import write_static_site
from xau_lfx.utils import write_json


RUN_ARTIFACT_KEYS = (
    "raw_scan",
    "data_quality",
    "composite_ohlcv",
    "session_context",
    "macro_pressure",
    "event_risk",
    "state",
    "user_insight",
    "artifact_quality",
    "context_summary",
)


def _build_connectors(input_dir: str | Path | None, event_file: str | Path | None) -> list[Any]:
    if input_dir is None:
        connectors: list[Any] = [MT5FeedConnector(), PublicMarketConnector()]
        connectors.append(EventCsvConnector(event_file) if event_file else EventCalendarConnector())
        return connectors
    connectors = [MT5CsvConnector(input_dir)]
    connectors.append(EventCsvConnector(event_file) if event_file else EventCalendarConnector())
    return connectors


def run_once(
    symbol: str = DEFAULT_SYMBOL,
    input_dir: str | Path | None = None,
    event_file: str | Path | None = None,
    out_dir: str | Path | None = None,
) -> dict:
    paths = artifact_paths(out_dir) if out_dir is not None else ARTIFACTS
    request = SourceRequest(source_id="PHASE3", symbol=symbol, timeframe="M15", limit=300)
    connectors = _build_connectors(input_dir=input_dir, event_file=event_file)
    source_payloads = [connector.fetch(request) for connector in connectors]

    raw_scan = normalize_raw_scan(source_payloads, symbol=symbol)
    data_quality = build_data_quality(raw_scan)
    composite = build_composite_ohlcv(raw_scan, data_quality)
    session = build_session_context(data_quality, composite)
    macro = build_macro_pressure(data_quality)
    event = build_event_risk(data_quality, raw_scan)
    state = build_external_state(data_quality, composite, session, macro, event)
    user_insight = build_user_insight(data_quality, composite, session, macro, event, state)
    artifact_quality = build_artifact_quality(data_quality, composite, session, event)
    context_summary = build_context_summary(data_quality, composite, session, event, artifact_quality)

    for payload in [
        raw_scan,
        data_quality,
        composite,
        session,
        macro,
        event,
        state,
        user_insight,
        artifact_quality,
        context_summary,
    ]:
        assert_clean_language(payload)

    write_json(paths["raw_scan"], raw_scan)
    write_json(paths["data_quality"], data_quality)
    write_json(paths["composite_ohlcv"], composite)
    write_json(paths["session_context"], session)
    write_json(paths["macro_pressure"], macro)
    write_json(paths["event_risk"], event)
    write_json(paths["state"], state)
    write_json(paths["user_insight"], user_insight)
    write_json(paths["artifact_quality"], artifact_quality)
    write_json(paths["context_summary"], context_summary)
    return state


def validate_sources(
    symbol: str = DEFAULT_SYMBOL,
    input_dir: str | Path | None = None,
    event_file: str | Path | None = None,
) -> dict[str, Any]:
    request = SourceRequest(source_id="VALIDATE_SOURCES", symbol=symbol, timeframe="M15", limit=300)
    connectors = _build_connectors(input_dir=input_dir, event_file=event_file)
    source_payloads = [connector.fetch(request) for connector in connectors]
    raw_scan = normalize_raw_scan(source_payloads, symbol=symbol)
    data_quality = build_data_quality(raw_scan)
    status = "ERROR" if data_quality.get("errors") else "OK"
    result = {
        "status": status,
        "symbol": symbol,
        "source_count": data_quality.get("source_count", 0),
        "present_timeframes": data_quality.get("present_timeframes", []),
        "errors": data_quality.get("errors", []),
        "quality_flags": data_quality.get("quality_flags", []),
    }
    assert_clean_language(result)
    return result


def run_demo(out_dir: str | Path, site_dir: str | Path) -> dict[str, Any]:
    sample_dir = PACKAGE_ROOT / "examples" / "sample-data"
    event_file = sample_dir / "usd_events.csv"
    required_files = [
        sample_dir / "XAUUSD_M5.csv",
        sample_dir / "XAUUSD_M15.csv",
        sample_dir / "XAUUSD_H1.csv",
        sample_dir / "XAUUSD_spread.csv",
        event_file,
    ]
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing synthetic demo files: " + ", ".join(missing))

    validation = validate_sources(input_dir=sample_dir, event_file=event_file)
    if validation["status"] != "OK":
        raise ValueError("Synthetic demo validation failed: " + json.dumps(validation, ensure_ascii=False))

    state = run_once(input_dir=sample_dir, event_file=event_file, out_dir=out_dir)
    paths = artifact_paths(out_dir)
    write_market_context_report(out_dir, write_md=True)
    site_index = write_static_site(artifact_dir=out_dir, out_dir=site_dir)
    return {
        "state": state["state"],
        "artifact_paths": paths,
        "site_index": site_index,
    }


def _print_generated_paths(paths: dict[str, Path], keys: tuple[str, ...]) -> None:
    for key in keys:
        print(f"artifact.{key}: {paths[key].resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="XAU-LFX External Data Foundation")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run-once")
    run_parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    run_parser.add_argument("--input-dir")
    run_parser.add_argument("--event-file")
    run_parser.add_argument("--out-dir", default=None)

    validate_parser = sub.add_parser("validate-sources")
    validate_parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    validate_parser.add_argument("--input-dir")
    validate_parser.add_argument("--event-file")

    report_parser = sub.add_parser("report")
    report_parser.add_argument("--artifact-dir", default="artifacts")
    report_parser.add_argument("--write-md", action="store_true")

    site_parser = sub.add_parser("site")
    site_parser.add_argument("--artifact-dir", default="artifacts")
    site_parser.add_argument("--out-dir", default="site")

    demo_parser = sub.add_parser("demo", help="Build synthetic artifacts, Markdown report, and static site.")
    demo_parser.add_argument("--out-dir", default="artifacts")
    demo_parser.add_argument("--site-dir", default="site")

    args = parser.parse_args()
    if args.command == "run-once":
        state = run_once(
            symbol=args.symbol,
            input_dir=args.input_dir,
            event_file=args.event_file,
            out_dir=args.out_dir,
        )
        print(state["state"])
        paths = artifact_paths(args.out_dir) if args.out_dir is not None else ARTIFACTS
        _print_generated_paths(paths, RUN_ARTIFACT_KEYS)
    elif args.command == "validate-sources":
        result = validate_sources(symbol=args.symbol, input_dir=args.input_dir, event_file=args.event_file)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if result["status"] == "ERROR":
            raise SystemExit(1)
    elif args.command == "report":
        report = write_market_context_report(args.artifact_dir, write_md=args.write_md)
        print(report if not args.write_md else str(artifact_paths(args.artifact_dir)["market_context_report"]))
    elif args.command == "site":
        index_path = write_static_site(artifact_dir=args.artifact_dir, out_dir=args.out_dir)
        print(str(index_path))
    elif args.command == "demo":
        try:
            result = run_demo(out_dir=args.out_dir, site_dir=args.site_dir)
        except (FileNotFoundError, ValueError) as exc:
            parser.exit(1, f"demo failed: {exc}\n")
        print(f"monitor_state: {result['state']}")
        _print_generated_paths(
            result["artifact_paths"],
            RUN_ARTIFACT_KEYS + ("market_context_report",),
        )
        print(f"site: {result['site_index'].resolve()}")


if __name__ == "__main__":
    main()
