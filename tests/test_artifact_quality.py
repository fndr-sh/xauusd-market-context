from xau_lfx.engines.artifact_quality import build_artifact_quality, quality_grade
from xau_lfx.pipeline import run_once
from xau_lfx.config import artifact_paths
from xau_lfx.utils import read_json


def test_quality_grade_thresholds():
    assert quality_grade(90) == "A"
    assert quality_grade(80) == "B"
    assert quality_grade(65) == "C"
    assert quality_grade(50) == "D"
    assert quality_grade(49.9) == "F"


def test_artifact_quality_warns_for_missing_sources():
    quality = build_artifact_quality(
        {"source_count": 0, "freshness_score": 0, "coverage_score": 0, "schema_score": 1, "spread_stability": 0, "quality_flags": []},
        {"quality_flags": []},
        {"quality_flags": [], "session_ranges": {}},
        {"quality_flags": [], "event_count": 0},
    )
    assert quality["status"] in {"WARN", "ERROR"}
    assert quality["quality_score"] <= 35


def test_artifact_quality_nonzero_for_sample_fixtures(tmp_path):
    run_once(input_dir="examples/sample-data", event_file="examples/sample-data/usd_events.csv", out_dir=tmp_path)
    quality = read_json(artifact_paths(tmp_path)["artifact_quality"])
    assert quality["quality_score"] > 0
    assert quality["schema_score"] == 100.0
    assert quality["source_count"] >= 2
