from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_recommendations_and_assistant():
    payload = {
        "age": 28,
        "gender": "Female",
        "state": "West Bengal",
        "district": "Kolkata",
        "annual_income": 250000,
        "business_type": "Dairy & Animal Husbandry",
        "business_status": "New / Proposed",
        "loan_required": 200000
    }
    
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    recs = response.json()
    assert isinstance(recs, list)
    assert len(recs) > 0
    top = recs[0]
    assert top['mandatory_eligible'] is True
    assert top['match_score'] >= 70
    assert len(top['why_this_scheme']) > 0

    # Test Assistant endpoint
    assistant_payload = {
        "message": "I want a loan of ₹2 Lakh to start a dairy unit in West Bengal",
        "current_profile": payload
    }
    ast_res = client.post("/api/assistant/message", json=assistant_payload)
    assert ast_res.status_code == 200
    ast_json = ast_res.json()
    assert "reply" in ast_json
    assert len(ast_json['recommended_schemes']) > 0

    # Test Tracker endpoint
    tracker_res = client.get("/api/tracker/PMEGP-2026-WB-8921")
    assert tracker_res.status_code == 200
    tracker_data = tracker_res.json()
    assert tracker_data['tracking_id'] == "PMEGP-2026-WB-8921"
    assert tracker_data['overall_status'] == "UNDER_REVIEW"
