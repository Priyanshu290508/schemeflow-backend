# Schemes API Router
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Scheme
from app.retrieval.search import SearchEngine
from app.schemas.scheme import SearchQuery

router = APIRouter(prefix="/schemes", tags=["Schemes"])

@router.get("")
def list_schemes(
    category: Optional[str] = Query(None, description="Filter by category"),
    state: Optional[str] = Query(None, description="Filter by state coverage"),
    q: Optional[str] = Query(None, description="Search query"),
    db: Session = Depends(get_db)
):
    query = db.query(Scheme)
    if category and category.lower() not in ["all", "any", ""]:
        query = query.filter(Scheme.category == category)
    
    schemes = query.all()
    scheme_dicts = [s.to_dict() for s in schemes]

    if q:
        scheme_dicts = SearchEngine.search(
            schemes=scheme_dicts,
            query=q,
            category=category,
            state=state
        )

    return {"count": len(scheme_dicts), "schemes": scheme_dicts}

@router.get("/{scheme_id}")
def get_scheme(scheme_id: str, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter((Scheme.id == scheme_id) | (Scheme.slug == scheme_id)).first()
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme with ID '{scheme_id}' not found")
    return scheme.to_dict()

@router.post("/search")
def search_schemes(payload: SearchQuery, db: Session = Depends(get_db)):
    schemes = db.query(Scheme).all()
    scheme_dicts = [s.to_dict() for s in schemes]
    results = SearchEngine.search(
        schemes=scheme_dicts,
        query=payload.query,
        category=payload.category,
        state=payload.state
    )
    return {"count": len(results[:payload.limit]), "schemes": results[:payload.limit]}
