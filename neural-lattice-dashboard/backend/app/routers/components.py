from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Component
from ..schemas import ComponentCreate, ComponentOut

router = APIRouter(prefix="/api/components", tags=["components"])


@router.get("")
def list_components(zone: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Component)
    if zone:
        q = q.filter(Component.zone == zone.upper())
    rows = q.order_by(Component.doc_id).all()
    return {"components": [ComponentOut.model_validate(r).model_dump(mode="json") for r in rows]}


@router.post("", response_model=ComponentOut)
def create_component(payload: ComponentCreate, db: Session = Depends(get_db)):
    existing = db.query(Component).filter(Component.doc_id == payload.doc_id).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"doc_id {payload.doc_id} exists")
    row = Component(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
