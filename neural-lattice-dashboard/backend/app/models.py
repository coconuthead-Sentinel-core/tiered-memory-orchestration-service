from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from datetime import datetime, timezone
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    zone = Column(String, nullable=False)
    cognitive_load = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    artifact_type = Column(String, nullable=False)
    version = Column(String, default="1.0")
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)


class DiagnosticRun(Base):
    __tablename__ = "diagnostic_runs"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=utcnow)
    results = Column(JSON, nullable=False)
    pass_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    objectives = Column(String, nullable=False)
    zone = Column(String, nullable=False)
    time_box_minutes = Column(Integer, default=25)
    started_at = Column(DateTime, default=utcnow)
    ended_at = Column(DateTime, nullable=True)
    state = Column(String, default="ACTIVE")
