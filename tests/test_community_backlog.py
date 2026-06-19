import re
from pathlib import Path

from xau_lfx.forbidden_language import assert_clean_language


ROOT = Path(__file__).resolve().parents[1]


def test_phase_e_community_files_exist():
    required = [
        "ROADMAP.md",
        "MAINTAINERS.md",
        "docs/LFX_EXTERNAL_BASELINE.md",
        ".github/ISSUE_TEMPLATE/user_feedback.md",
        ".github/workflows/issue-triage.yml",
    ]
    for relative_path in required:
        assert (ROOT / relative_path).exists(), relative_path


def test_issue_seed_meets_phase_e_acceptance():
    text = (ROOT / "docs" / "ISSUE_BACKLOG_SEED.md").read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^### ", text)[1:]
    assert 10 <= len(blocks) <= 20
    assert sum("`good first issue`" in block for block in blocks) >= 5
    assert sum("`docs`" in block or "`demo`" in block for block in blocks) >= 3
    for label in ["good first issue", "help wanted", "docs", "validation", "demo", "research", "schema"]:
        assert f"`{label}`" in text


def test_phase_e_docs_preserve_lfx_external_contract():
    files = [
        "ROADMAP.md",
        "MAINTAINERS.md",
        "docs/LFX_EXTERNAL_BASELINE.md",
        "docs/ISSUE_BACKLOG_SEED.md",
        ".github/ISSUE_TEMPLATE/user_feedback.md",
    ]
    text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in files)
    assert "monitor-only" in text.lower()
    assert "reference only" in text.lower()
    assert "not centralized traded volume" in text.lower()
    assert_clean_language(text)


def test_issue_triage_workflow_is_narrowly_scoped():
    text = (ROOT / ".github" / "workflows" / "issue-triage.yml").read_text(encoding="utf-8")
    assert "issues: write" in text
    assert "contents: read" in text
    assert "needs triage" in text
    assert "pull-requests: write" not in text
