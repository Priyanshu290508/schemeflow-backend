# Recommendations API Router
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Scheme
from app.schemas.scheme import ProfileData, SchemeRecommendation
from app.ranking.ranker import RecommendationEngine
from app.rules.engine import RuleEngine

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("", response_model=list[SchemeRecommendation])
def get_recommendations(profile: ProfileData, db: Session = Depends(get_db)):
    """
    Evaluates the user's profile against all scheme eligibility rules
    and returns deterministic ranked recommendations with explainability summaries.
    """
    schemes = db.query(Scheme).all()
    scheme_dicts = [s.to_dict() for s in schemes]
    ranked = RecommendationEngine.rank_schemes(scheme_dicts, profile)
    return ranked

@router.post("/evaluate/{scheme_id}")
def evaluate_single_scheme(scheme_id: str, profile: ProfileData, db: Session = Depends(get_db)):
    """
    Evaluates a specific scheme against a user profile and returns detailed criteria breakdown.
    """
    scheme = db.query(Scheme).filter((Scheme.id == scheme_id) | (Scheme.slug == scheme_id)).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    scheme_dict = scheme.to_dict()
    mandatory_eligible, criteria_results = RuleEngine.evaluate_scheme(scheme_dict, profile)
    
    # Run full ranking single item
    ranked = RecommendationEngine.rank_schemes([scheme_dict], profile)
    return ranked[0]
