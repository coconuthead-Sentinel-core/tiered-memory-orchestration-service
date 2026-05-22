from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..database import get_db
from ..models import Session as SessionModel
from ..schemas import SessionCreate, SessionOut

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=SessionOut)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    db.query(SessionModel).filter(SessionModel.state == "ACTIVE").update({"state": "ENDED", "ended_at": datetime.now(timezone.utc)})
    row = SessionModel(
        objectives=payload.objectives,
        zone=payload.zone,
        time_box_minutes=payload.time_box,
        state="ACTIVE",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("")
def list_sessions(db: Session = Depends(get_db)):
    rows = db.query(SessionModel).order_by(SessionModel.started_at.desc()).limit(50).all()
    return {"sessions": [SessionOut.model_validate(r).model_dump(mode="json") for r in rows]}


@router.get("/current")
def current_session(db: Session = Depends(get_db)):
    row = db.query(SessionModel).filter(SessionModel.state == "ACTIVE").order_by(SessionModel.started_at.desc()).first()
    if not row:
        return {"active": False}
    elapsed_seconds = (datetime.now(timezone.utc) - row.started_at.replace(tzinfo=timezone.utc)).total_seconds()
    return {
        "active": True,
        "session": SessionOut.model_validate(row).model_dump(mode="json"),
        "elapsed_seconds": int(elapsed_seconds),
        "remaining_seconds": max(0, row.time_box_minutes * 60 - int(elapsed_seconds)),
    }
