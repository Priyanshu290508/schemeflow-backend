# Profile and Saved Schemes Router
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import UserProfile, SavedScheme, Scheme
from app.schemas.scheme import ProfileData

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=ProfileData)
def get_user_profile(user_id: str = "default_user", db: Session = Depends(get_db)):
    prof = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not prof:
        return ProfileData()
    
    extra = {}
    try:
        if prof.extra_data:
            extra = json.loads(prof.extra_data)
    except Exception:
        pass

    return ProfileData(
        age=prof.age,
        gender=prof.gender,
        state=prof.state,
        district=prof.district,
        annual_income=prof.annual_income,
        employment_status=prof.employment_status,
        business_type=prof.business_type,
        business_status=prof.business_status,
        business_size=prof.business_size,
        investment_required=prof.investment_required,
        loan_required=prof.loan_required,
        category=prof.category,
        is_differently_abled=prof.is_differently_abled,
        extra_data=extra
    )

@router.post("")
def save_user_profile(profile_data: ProfileData, user_id: str = "default_user", db: Session = Depends(get_db)):
    prof = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not prof:
        prof = UserProfile(id=user_id)
        db.add(prof)

    prof.age = profile_data.age
    prof.gender = profile_data.gender
    prof.state = profile_data.state
    prof.district = profile_data.district
    prof.annual_income = profile_data.annual_income
    prof.employment_status = profile_data.employment_status
    prof.business_type = profile_data.business_type
    prof.business_status = profile_data.business_status
    prof.business_size = profile_data.business_size
    prof.investment_required = profile_data.investment_required
    prof.loan_required = profile_data.loan_required
    prof.category = profile_data.category
    prof.is_differently_abled = profile_data.is_differently_abled
    prof.extra_data = json.dumps(profile_data.extra_data or {})

    db.commit()
    return {"message": "Profile saved successfully", "profile": profile_data}

@router.get("/saved-schemes")
def get_saved_schemes(user_id: str = "default_user", db: Session = Depends(get_db)):
    saved = db.query(SavedScheme).filter(SavedScheme.user_id == user_id).all()
    scheme_ids = [s.scheme_id for s in saved]
    if not scheme_ids:
        return {"saved_schemes": []}
    
    schemes = db.query(Scheme).filter(Scheme.id.in_(scheme_ids)).all()
    return {"saved_schemes": [s.to_dict() for s in schemes]}

@router.post("/saved-schemes/{scheme_id}")
def save_scheme_bookmark(scheme_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    exists = db.query(SavedScheme).filter(SavedScheme.user_id == user_id, SavedScheme.scheme_id == scheme_id).first()
    if exists:
        return {"message": "Scheme already saved"}
    
    entry = SavedScheme(user_id=user_id, scheme_id=scheme_id)
    db.add(entry)
    db.commit()
    return {"message": "Scheme bookmarked successfully"}

@router.delete("/saved-schemes/{scheme_id}")
def remove_saved_scheme(scheme_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    db.query(SavedScheme).filter(SavedScheme.user_id == user_id, SavedScheme.scheme_id == scheme_id).delete()
    db.commit()
    return {"message": "Scheme removed from saved list"}
