from fastapi import APIRouter

from ..schemas import MetadataValidateRequest, MetadataValidateResponse
from ..services.metadata_engine import MetadataEngine

router = APIRouter(prefix="/api/metadata", tags=["metadata"])
engine = MetadataEngine()


@router.post("/validate", response_model=MetadataValidateResponse)
def validate(req: MetadataValidateRequest):
    result = engine.validate(req.metadata_block)
    return MetadataValidateResponse(**result)
