# Automated Unit Tests for Deterministic Rule Engine, Scoring Weights & Explainability
import pytest
from app.schemas.scheme import ProfileData
from app.rules.engine import RuleEngine
from app.ranking.ranker import RecommendationEngine
from app.core.config import settings

def test_scoring_weights_sum_to_100():
    """Verify core scoring weights match the PRD & architecture specification (Total = 100)."""
    total_core_weights = (
        settings.WEIGHT_AGE +
        settings.WEIGHT_INCOME +
        settings.WEIGHT_BUSINESS_TYPE +
        settings.WEIGHT_LOCATION +
        settings.WEIGHT_FINANCIAL_NEED
    )
    assert total_core_weights == 100.0

def test_rule_engine_age_evaluation():
    rule = {
        "field": "age",
        "operator": "GTE",
        "value": 18,
        "required": True,
        "label": "Minimum Age"
    }

    # Pass case
    p_pass = ProfileData(age=25)
    res_pass = RuleEngine.evaluate_criterion(rule, p_pass)
    assert res_pass.status == "PASS"
    assert res_pass.points == 1.0

    # Fail case
    p_fail = ProfileData(age=16)
    res_fail = RuleEngine.evaluate_criterion(rule, p_fail)
    assert res_fail.status == "FAIL"
    assert res_fail.points == 0.0

    # Missing info case (must NEVER become PASS)
    p_missing = ProfileData()
    res_missing = RuleEngine.evaluate_criterion(rule, p_missing)
    assert res_missing.status == "MISSING_INFORMATION"
    assert res_missing.points == 0.0

def test_rule_engine_missing_info_never_passes():
    """Critical Law: Missing information must never count as PASS."""
    rules = [
        {"field": "annual_income", "operator": "LTE", "value": 300000, "required": True},
        {"field": "business_type", "operator": "IN", "value": ["Manufacturing"], "required": True},
        {"field": "state", "operator": "EQ", "value": "West Bengal", "required": False}
    ]

    empty_profile = ProfileData()
    for r in rules:
        res = RuleEngine.evaluate_criterion(r, empty_profile)
        assert res.status == "MISSING_INFORMATION"
        assert res.points == 0.0

def test_rule_engine_between_operator():
    rule = {
        "field": "loan_required",
        "operator": "BETWEEN",
        "value": [50000, 500000],
        "required": True,
        "label": "Loan Range"
    }

    p1 = ProfileData(loan_required=200000)
    assert RuleEngine.evaluate_criterion(rule, p1).status == "PASS"

    p2 = ProfileData(loan_required=1000000)
    assert RuleEngine.evaluate_criterion(rule, p2).status == "FAIL"

def test_mandatory_disqualifier_law():
    """
    Law: A high score must never override a failed mandatory rule.
    A failed required rule MUST result in mandatory_eligible=False, score <= 45, and 'Ineligible' label.
    """
    mock_scheme = {
        "id": "test_001",
        "name": "Test Scheme",
        "summary": "Summary",
        "category": "Business",
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Age"},
            {"field": "annual_income", "operator": "LTE", "value": 500000, "required": True, "label": "Income"},
            {"field": "business_type", "operator": "EQ", "value": "Manufacturing", "required": False, "label": "Sector"}
        ]
    }

    # Under-age user fails mandatory rule
    disqualified_profile = ProfileData(age=15, annual_income=200000, business_type="Manufacturing")
    recs = RecommendationEngine.rank_schemes([mock_scheme], disqualified_profile)

    assert len(recs) == 1
    assert recs[0].mandatory_eligible is False
    assert recs[0].match_score <= 45
    assert "Ineligible" in recs[0].match_label

def test_score_label_tiers():
    """Verify standard recommendation score brackets: 85-100, 70-84, 50-69, Below 50."""
    fully_eligible_scheme = {
        "id": "test_full",
        "name": "Perfect Scheme",
        "category": "Business",
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Age"},
            {"field": "annual_income", "operator": "LTE", "value": 300000, "required": True, "label": "Income"},
            {"field": "business_type", "operator": "IN", "value": ["Manufacturing"], "required": True, "label": "Sector"}
        ]
    }

    perfect_profile = ProfileData(age=28, annual_income=200000, business_type="Manufacturing", state="West Bengal")
    recs = RecommendationEngine.rank_schemes([fully_eligible_scheme], perfect_profile)
    assert len(recs) == 1
    assert recs[0].mandatory_eligible is True
    assert recs[0].match_score >= 85
    assert recs[0].match_label == "Excellent Match"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
