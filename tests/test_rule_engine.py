# Automated Unit Tests for Deterministic Rule Engine & Ranking Model
import pytest
from app.schemas.scheme import ProfileData
from app.rules.engine import RuleEngine
from app.ranking.ranker import RecommendationEngine

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

    # Missing info case
    p_missing = ProfileData()
    res_missing = RuleEngine.evaluate_criterion(rule, p_missing)
    assert res_missing.status == "MISSING_INFORMATION"

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
    """
    mock_scheme = {
        "id": "test_001",
        "name": "Test Scheme",
        "summary": "Summary",
        "category": "Business",
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Age"},
            {"field": "business_type", "operator": "EQ", "value": "Manufacturing", "required": False, "label": "Sector"}
        ]
    }

    # Under-age user fails mandatory rule
    disqualified_profile = ProfileData(age=15, business_type="Manufacturing")
    recs = RecommendationEngine.rank_schemes([mock_scheme], disqualified_profile)

    assert len(recs) == 1
    assert recs[0].mandatory_eligible is False
    assert recs[0].match_score <= 45
    assert "Ineligible" in recs[0].match_label

if __name__ == "__main__":
    pytest.main(["-v", __file__])
