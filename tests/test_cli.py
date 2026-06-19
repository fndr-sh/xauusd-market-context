from pathlib import Path
import sys

from xau_lfx.forbidden_language import assert_clean_language
from xau_lfx.pipeline import main


ROOT = Path(__file__).resolve().parents[1]


def test_demo_command_generates_artifacts_report_and_site(tmp_path, monkeypatch, capsys):
    artifact_dir = tmp_path / "artifacts"
    site_dir = tmp_path / "site"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xau-lfx",
            "demo",
            "--out-dir",
            str(artifact_dir),
            "--site-dir",
            str(site_dir),
        ],
    )

    main()

    output = capsys.readouterr().out
    assert "monitor_state: CONTEXT" in output
    assert "artifact.context_summary:" in output
    assert str((artifact_dir / "xau_context_summary.json").resolve()) in output
    assert str((artifact_dir / "xau_market_context_report.md").resolve()) in output
    assert str((site_dir / "index.html").resolve()) in output
    assert (artifact_dir / "xau_context_summary.json").exists()
    assert (artifact_dir / "xau_market_context_report.md").exists()
    assert (site_dir / "index.html").exists()


def test_run_once_command_prints_generated_artifact_paths(tmp_path, monkeypatch, capsys):
    artifact_dir = tmp_path / "artifacts"
    sample_dir = ROOT / "examples" / "sample-data"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xau-lfx",
            "run-once",
            "--input-dir",
            str(sample_dir),
            "--event-file",
            str(sample_dir / "usd_events.csv"),
            "--out-dir",
            str(artifact_dir),
        ],
    )

    main()

    output = capsys.readouterr().out
    assert output.splitlines()[0] == "CONTEXT"
    assert "artifact.raw_scan:" in output
    assert str((artifact_dir / "xau_raw_scan.json").resolve()) in output
    assert str((artifact_dir / "xau_context_summary.json").resolve()) in output


def test_cli_usage_documents_demo_and_existing_commands():
    text = (ROOT / "docs" / "CLI_USAGE.md").read_text(encoding="utf-8")
    for command in ["demo", "validate-sources", "run-once", "report", "site"]:
        assert f"xau-lfx {command}" in text
    assert "synthetic" in text.lower()
    assert "monitor-only" in text.lower()
    assert_clean_language(text)
