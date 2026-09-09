from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import Base, engine, SessionLocal
from .models import Component
from .routers import diagnostics, zones, protocols, components, metadata, pipeline, sessions

VERSION = "1.0.0"

SEED_COMPONENTS = [
    {"doc_id": "SENT-PROJ-A1-001", "name": "Sentinel Project A1", "zone": "RED", "cognitive_load": 8, "status": "ARCHIVED", "artifact_type": "SYS_ARCH"},
    {"doc_id": "COMP-FILE-001", "name": "Filing System Matrix", "zone": "RED", "cognitive_load": 7, "status": "ARCHIVED", "artifact_type": "BLUEPRINT"},
    {"doc_id": "COMP-MASTER-001", "name": "Master Integration", "zone": "RED", "cognitive_load": 6, "status": "ARCHIVED", "artifact_type": "INT_GUIDE"},
    {"doc_id": "CSTM-V30-FINAL-001", "name": "CSTM Lattice", "zone": "GREEN", "cognitive_load": 9, "status": "PRODUCTION", "artifact_type": "REF_SCHEMA"},
    {"doc_id": "SDLC-CHARTER-001", "name": "SDLC Charter", "zone": "GREEN", "cognitive_load": 8, "status": "ACTIVE", "artifact_type": "CHARTER"},
    {"doc_id": "NEURAL-LATTICE-001", "name": "Neural Lattice Matrix", "zone": "GREEN", "cognitive_load": 8, "status": "ACTIVE", "artifact_type": "SYS_ARCH"},
]


def seed_db():
    db = SessionLocal()
    try:
        for entry in SEED_COMPONENTS:
            existing = db.query(Component).filter(Component.doc_id == entry["doc_id"]).first()
            if not existing:
                db.add(Component(**entry, version="1.0"))
        db.commit()
    finally:
        db.close()


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    seed_db()

    app = FastAPI(title="Neural Lattice Diagnostic Dashboard", version=VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": VERSION}

    app.include_router(diagnostics.router)
    app.include_router(zones.router)
    app.include_router(protocols.router)
    app.include_router(components.router)
    app.include_router(metadata.router)
    app.include_router(pipeline.router)
    app.include_router(sessions.router)

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")
    static_dir = os.path.abspath(static_dir)
    if os.path.isdir(static_dir):
        app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

        @app.get("/")
        def root():
            return FileResponse(os.path.join(static_dir, "index.html"))

        @app.get("/{full_path:path}")
        def spa(full_path: str):
            target = os.path.join(static_dir, full_path)
            if os.path.isfile(target):
                return FileResponse(target)
            return FileResponse(os.path.join(static_dir, "index.html"))
    else:
        @app.get("/")
        def root():
            return {
                "message": "Neural Lattice Dashboard API",
                "docs": "/docs",
                "health": "/api/health",
            }

    return app


app = create_app()
