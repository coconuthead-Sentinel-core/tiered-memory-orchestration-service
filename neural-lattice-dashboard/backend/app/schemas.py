from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class HealthResponse(BaseModel):
    status: str
    version: str


class ZoneClassifyRequest(BaseModel):
    cognitive_load: int = Field(..., ge=1, le=10)
    status: Optional[str] = None


class ZoneClassifyResponse(BaseModel):
    zone: str
    rationale: str


class ZoneMigrateRequest(BaseModel):
    doc_id: str
    target_zone: str


class ZoneMigrateResponse(BaseModel):
    success: bool
    guard_result: str
    action: Optional[str] = None


class ComponentBase(BaseModel):
    doc_id: str
    name: str
    zone: str
    cognitive_load: int
    status: str
    artifact_type: str
    version: Optional[str] = "1.0"


class ComponentCreate(ComponentBase):
    pass


class ComponentOut(ComponentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MetadataValidateRequest(BaseModel):
    metadata_block: dict[str, Any]


class MetadataValidateResponse(BaseModel):
    valid: bool
    errors: list[str]


class SessionCreate(BaseModel):
    objectives: str
    zone: str
    time_box: int = 25


class SessionOut(BaseModel):
    id: int
    objectives: str
    zone: str
    time_box_minutes: int
    started_at: datetime
    ended_at: Optional[datetime]
    state: str

    class Config:
        from_attributes = True
