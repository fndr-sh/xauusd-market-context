from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

MonitorState = Literal[
    "WATCH",
    "CONTEXT",
    "NO_TRADE",
    "CAUTION",
    "INSUFFICIENT_SOURCE_COVERAGE",
    "RESEARCH_ONLY",
]


class QualityBlock(BaseModel):
    quality_flags: list[str] = Field(default_factory=list)
    confidence_cap: float = 0.0
    source_count: int = 0
    missing_field_count: int = 0


class RawScan(BaseModel):
    ts_utc: str
    symbol: str = "XAUUSD"
    monitor_only: bool = True
    source_payloads: list[dict[str, Any]] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)


class DataQuality(BaseModel):
    ts_utc: str
    symbol: str = "XAUUSD"
    monitor_only: bool = True
    freshness_score: float = 0.0
    coverage_score: float = 0.0
    schema_score: float = 0.0
    source_count: int = 0
    missing_field_count: int = 0
    dispersion_score: float = 0.0
    session_completeness: float = 0.0
    spread_stability: float = 0.0
    news_risk_flag: bool = False
    confidence_cap: float = 0.0
    present_timeframes: list[str] = Field(default_factory=list)
    event_count: int = 0
    errors: list[str] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)


class ExternalState(BaseModel):
    ts_utc: str
    symbol: str = "XAUUSD"
    monitor_only: bool = True
    state: MonitorState
    summary: str
    evidence: list[str] = Field(default_factory=list)
    quality: QualityBlock


class ArtifactQuality(BaseModel):
    ts_utc: str
    symbol: str = "XAUUSD"
    monitor_only: bool = True
    status: Literal["OK", "WARN", "ERROR"]
    quality_score: float
    quality_grade: Literal["A", "B", "C", "D", "F"]
    freshness_score: float
    coverage_score: float
    schema_score: float
    session_score: float
    spread_score: float
    event_score: float
    source_count: int
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
