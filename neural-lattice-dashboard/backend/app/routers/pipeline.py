from fastapi import APIRouter

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

PIPELINE_STAGES = [
    {"id": "S1", "name": "Input Ingestion", "description": "Query reception, intent parsing", "output": "Parsed intent object"},
    {"id": "S2", "name": "Context Assembly", "description": "Load memory threads L0-L3", "output": "Assembled context"},
    {"id": "S3", "name": "Protocol Synthesis", "description": "Determine active protocols", "output": "Protocol config object"},
    {"id": "S4", "name": "Zone Classification", "description": "Evaluate load, assign zone", "output": "Zone + load rating"},
    {"id": "S5", "name": "Metadata Generation", "description": "Auto-generate doc_id, tags, timestamps", "output": "YAML metadata block"},
    {"id": "S6", "name": "Content Structuring", "description": "Apply hierarchy, chunk for ND", "output": "Formatted content"},
    {"id": "S7", "name": "Quality Assurance", "description": "Verify compliance, validate", "output": "Pass/fail report"},
    {"id": "S8", "name": "Persistent Storage", "description": "Write to file, update graph", "output": "Stored artifact"},
]


@router.get("")
def get_pipeline():
    return {"stages": PIPELINE_STAGES}
