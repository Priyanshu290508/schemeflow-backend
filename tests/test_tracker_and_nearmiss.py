import pytest
from app.schemas.scheme import ProfileData, RuleCriterionResult
from app.ranking.ranker import RecommendationEngine
from app.api.tracker import get_application_status

def test_near_miss_income_guidance():
    # User income is ₹2,80,000, rule max is ₹2,50,000 (delta is ₹30,000 which is within 35%)
    scheme = {"id": "pmegp_001", "name": "PMEGP"}
    profile = ProfileData(
        age=25,
        annual_income=280000,
        state="West Bengal",
        business_type="Manufacturing",
        business_status="New / Proposed",
        loan_required=300000,
        category="General"
    )
    failed_income_crit = RuleCriterionResult(
        field="annual_income",
        operator="LTE",
        required_value=250000,
        actual_value=280000,
        status="FAIL",
        required=True,
        label="Annual Income Limit",
        reason="Reported annual income ₹280,000 exceeds limit ₹250,000"
    )

    tips = RecommendationEngine.generate_near_miss_tips(scheme, profile, [failed_income_crit])
    assert len(tips) >= 1
    assert any("₹30,000 lower" in tip for tip in tips)

def test_application_tracker_endpoint():
    status = get_application_status("PMEGP-2026-WB-8921")
    assert status.tracking_id == "PMEGP-2026-WB-8921"
    assert status.applicant_name == "Priyanka Mondal"
    assert status.overall_status == "UNDER_REVIEW"
    assert len(status.steps) == 5
    assert status.progress_percentage == 65

def test_application_tracker_dynamic_generation():
    status = get_application_status("CUSTOM-REF-9999")
    assert status.tracking_id == "CUSTOM-REF-9999"
    assert len(status.steps) >= 3
    assert status.progress_percentage > 0
