# Assistant API Router
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Scheme
from app.schemas.scheme import AssistantMessageInput, AssistantMessageResponse, ProfileData
from app.assistant.service import AssistantService

router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.post("/message", response_model=AssistantMessageResponse)
def handle_assistant_message(payload: AssistantMessageInput, db: Session = Depends(get_db)):
    schemes = db.query(Scheme).all()
    scheme_dicts = [s.to_dict() for s in schemes]
    
    current_prof = payload.current_profile or ProfileData()
    response = AssistantService.process_message(
        message=payload.message,
        current_profile=current_prof,
        all_schemes=scheme_dicts
    )
    return response
