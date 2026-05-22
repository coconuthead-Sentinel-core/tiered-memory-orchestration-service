from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Session as SessionModel
from ..services.protocol_engine import ProtocolEngine

router = APIRouter(prefix="/api/protocols", tags=["protocols"])


@router.get("")
def list_protocols(cognitive_load: int = 5, db: Session = Depends(get_db)):
    session_active = db.query(SessionModel).filter(SessionModel.state == "ACTIVE").count() > 0
    protos = ProtocolEngine.evaluate(cognitive_load=cognitive_load, session_active=session_active)
    return {"protocols": protos, "session_active": session_active}
