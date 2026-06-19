from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = PACKAGE_ROOT / "artifacts"
DEFAULT_SYMBOL = "XAUUSD"
DEFAULT_TIMEFRAMES = ("M5", "M15", "H1")
PRIMARY_TIMEFRAME = "M15"
TRIGGER_TIMEFRAME = "M5"
CONTEXT_TIMEFRAME = "H1"
MONITOR_ONLY = True


def artifact_paths(out_dir: str | Path | None = None) -> dict[str, Path]:
    root = Path(out_dir) if out_dir is not None else ARTIFACT_DIR
    return {
        "raw_scan": root / "xau_raw_scan.json",
        "data_quality": root / "xau_data_quality.json",
        "composite_ohlcv": root / "xau_composite_ohlcv.json",
        "session_context": root / "xau_session_context.json",
        "macro_pressure": root / "xau_macro_pressure.json",
        "event_risk": root / "xau_event_risk_state.json",
        "state": root / "xau_lfx_external_state.json",
        "user_insight": root / "xau_user_insight.json",
        "artifact_quality": root / "xau_artifact_quality.json",
        "market_context_report": root / "xau_market_context_report.md",
    }


ARTIFACTS = artifact_paths()
