from xau_lfx.config import ARTIFACTS
from xau_lfx.pipeline import run_once
from xau_lfx.utils import read_json


def test_user_insight_is_created_and_useful_in_no_source_mode():
    run_once()
    insight = read_json(ARTIFACTS["user_insight"])
    assert insight["monitor_only"] is True
    assert "headline" in insight
    assert len(insight["operator_focus"]) >= 3
    assert len(insight["upgrade_requirements"]) >= 3
    assert "External XAU context is not decision-grade yet" in insight["headline"]
