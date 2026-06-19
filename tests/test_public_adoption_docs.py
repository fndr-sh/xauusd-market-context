from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_adoption_docs_exist():
    required = [
        "docs/MT5_EXPORT_GUIDE.md",
        "docs/ADOPTION_GUIDE.md",
        "docs/ISSUE_BACKLOG_SEED.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_readme_has_public_badges_and_use_cases():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "actions/workflows/tests.yml/badge.svg" in readme
    assert "actions/workflows/pages.yml/badge.svg" in readme
    assert "## Use cases" in readme
    assert "## GitHub adoption resources" in readme


def test_adoption_docs_preserve_monitor_only_language():
    text = "\n".join(
        (ROOT / rel).read_text(encoding="utf-8").lower()
        for rel in [
            "docs/MT5_EXPORT_GUIDE.md",
            "docs/ADOPTION_GUIDE.md",
            "docs/ISSUE_BACKLOG_SEED.md",
        ]
    )
    assert "monitor-only" in text
    assert "no directional trade-call" in text
    assert "no execution" in text
    assert "profitability" in text
