from pathlib import Path

from xau_lfx.forbidden_language import assert_clean_language


ROOT = Path(__file__).resolve().parents[1]


def test_adoption_guide_covers_current_live_dashboard_path():
    text = (ROOT / "docs" / "ADOPTION_GUIDE.md").read_text(encoding="utf-8")

    assert "OANDA_LIVE_DASHBOARD.md" in text
    assert "serve-oanda" in text
    assert "same private network" in text
    for topic in ["dashboard", "fastapi", "oanda"]:
        assert topic in text
    assert_clean_language(text)


def test_claude_positioning_uses_current_progression_gates():
    text = (ROOT / "docs" / "CLAUDE_FOR_OSS_POSITIONING.md").read_text(encoding="utf-8")

    assert "`v2.4.x`" in text
    assert "`v2.5.0`" in text
    assert "`v3.0.0`" in text
    assert "v1.4.0: public publish pack" not in text
    assert "official program criteria" in text
    assert_clean_language(text)
