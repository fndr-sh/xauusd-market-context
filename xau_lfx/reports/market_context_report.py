from __future__ import annotations

from pathlib import Path
from typing import Any

from xau_lfx.config import artifact_paths
from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.utils import read_json, utc_now_iso, write_text


def _lines_for_sessions(session_ranges: dict[str, Any]) -> list[str]:
    if not session_ranges:
        return ["- No session range could be built from the current source set."]
    lines: list[str] = []
    for name, block in session_ranges.items():
        lines.append(
            f"- {name}: bars={block.get('bar_count', 0)}, high={block.get('high')}, "
            f"low={block.get('low')}, range={block.get('range_points')}"
        )
    return lines


def build_market_context_markdown(
    data_quality: dict[str, Any],
    composite: dict[str, Any],
    session: dict[str, Any],
    event: dict[str, Any],
    user_insight: dict[str, Any],
    artifact_quality: dict[str, Any],
) -> str:
    session_lines = _lines_for_sessions(session.get("session_ranges", {}))
    latest_close = composite.get("median_latest_close")
    warnings = artifact_quality.get("warnings", [])
    errors = artifact_quality.get("errors", [])

    report = f"""# XAUUSD Market Context Report

Generated: {utc_now_iso()}  
Mode: monitor-only research artifact  
Symbol: {data_quality.get('symbol', 'XAUUSD')}

## Artifact Quality

- Status: {artifact_quality.get('status')}
- Quality score: {artifact_quality.get('quality_score')} / 100
- Quality grade: {artifact_quality.get('quality_grade')}
- Confidence cap: {artifact_quality.get('confidence_cap')}
- Source count: {artifact_quality.get('source_count')}

## Source Coverage

- Present timeframes: {', '.join(data_quality.get('present_timeframes', [])) or 'none'}
- Freshness score: {artifact_quality.get('freshness_score')} / 100
- Coverage score: {artifact_quality.get('coverage_score')} / 100
- Schema score: {artifact_quality.get('schema_score')} / 100
- Spread score: {artifact_quality.get('spread_score')} / 100
- Event score: {artifact_quality.get('event_score')} / 100

## M15 Session Map

{chr(10).join(session_lines)}

## Event Risk Context

- Risk state: {event.get('risk_state')}
- Event count: {event.get('event_count', 0)}
- High-impact USD events: {len(event.get('high_impact_events', []))}
- Note: {event.get('note')}

## Current Read

- Latest cross-timeframe median close: {latest_close if latest_close is not None else 'not available'}
- Headline: {user_insight.get('headline')}
- Now: {user_insight.get('now_read')}

## What To Monitor

"""
    for item in user_insight.get("operator_focus", []):
        report += f"- {item}\n"

    report += "\n## What This Artifact Cannot Claim\n\n"
    cannot_claim = [
        "It cannot infer centralized spot-gold orderflow from broker CSV files.",
        "It cannot infer actual dealer inventory or actual retail-side positioning.",
        "It cannot provide execution instructions or profitability claims.",
        "It cannot treat broker tick activity as centralized traded volume.",
    ]
    for item in cannot_claim:
        report += f"- {item}\n"

    report += "\n## Warnings\n\n"
    if warnings:
        for item in warnings[:30]:
            report += f"- {item}\n"
    else:
        report += "- No warnings emitted by the artifact-quality gate.\n"

    report += "\n## Errors\n\n"
    if errors:
        for item in errors[:30]:
            report += f"- {item}\n"
    else:
        report += "- No schema or source errors were emitted.\n"

    assert_clean_language(report)
    return report


def write_market_context_report(artifact_dir: str | Path, write_md: bool = True) -> str:
    paths = artifact_paths(artifact_dir)
    report = build_market_context_markdown(
        data_quality=read_json(paths["data_quality"]),
        composite=read_json(paths["composite_ohlcv"]),
        session=read_json(paths["session_context"]),
        event=read_json(paths["event_risk"]),
        user_insight=read_json(paths["user_insight"]),
        artifact_quality=read_json(paths["artifact_quality"]),
    )
    if write_md:
        write_text(paths["market_context_report"], report)
    return report
