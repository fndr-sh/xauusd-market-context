from __future__ import annotations

from xau_lfx.utils import utc_now_iso


def build_macro_pressure(data_quality: dict) -> dict:
    return {
        "ts_utc": utc_now_iso(),
        "symbol": data_quality.get("symbol", "XAUUSD"),
        "monitor_only": True,
        "pressure_state": "CONTEXT",
        "drivers": [],
        "note": "Macro pressure disabled until explicit sources are configured.",
        "confidence_cap": data_quality.get("confidence_cap", 0.0),
        "quality_flags": sorted(set(data_quality.get("quality_flags", []) + ["MACRO_SOURCES_NOT_CONFIGURED"])),
    }
