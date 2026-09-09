from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.diagnostic_engine import DiagnosticEngine
from ..models import DiagnosticRun

router = APIRouter(prefix="/api/diagnostics", tags=["diagnostics"])
engine = DiagnosticEngine()


@router.get("")
def get_diagnostics(db: Session = Depends(get_db)):
    last = db.query(DiagnosticRun).order_by(DiagnosticRun.started_at.desc()).first()
    if last:
        return {"tests": last.results, "ran_at": last.started_at.isoformat()}
    return {"tests": engine.run_all(db), "ran_at": None}


@router.get("/run")
def run_diagnostics(db: Session = Depends(get_db)):
    results = engine.run_all(db)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = len(results) - pass_count
    record = DiagnosticRun(results=results, pass_count=pass_count, fail_count=fail_count)
    db.add(record)
    db.commit()
    return {"tests": results, "pass_count": pass_count, "fail_count": fail_count}
