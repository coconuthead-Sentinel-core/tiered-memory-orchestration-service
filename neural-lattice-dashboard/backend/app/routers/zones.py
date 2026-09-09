from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Component
from ..schemas import (
    ZoneClassifyRequest, ZoneClassifyResponse,
    ZoneMigrateRequest, ZoneMigrateResponse,
)
from ..services.zone_engine import ZoneEngine, Zone, ZONE_META

router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("")
def list_zones(db: Session = Depends(get_db)):
    zones = []
    for z in Zone:
        count = db.query(Component).filter(Component.zone == z.value).count()
        meta = ZONE_META[z]
        zones.append({
            "name": z.value,
            "load_range": meta["load_range"],
            "color": meta["color"],
            "access": meta["access"],
            "count": count,
        })
    return {"zones": zones}


@router.post("/classify", response_model=ZoneClassifyResponse)
def classify(req: ZoneClassifyRequest):
    zone = ZoneEngine.classify(req.cognitive_load)
    rationale = f"cognitive_load={req.cognitive_load} falls in range {ZONE_META[zone]['load_range']}"
    return ZoneClassifyResponse(zone=zone.value, rationale=rationale)


@router.post("/migrate", response_model=ZoneMigrateResponse)
def migrate(req: ZoneMigrateRequest, db: Session = Depends(get_db)):
    doc = db.query(Component).filter(Component.doc_id == req.doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Component {req.doc_id} not found")
    try:
        target = Zone(req.target_zone)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid target_zone: {req.target_zone}")
    result = ZoneEngine.apply_migration(doc, target)
    if result["success"]:
        db.commit()
    return ZoneMigrateResponse(**result)
