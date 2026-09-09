from app.services.metadata_engine import MetadataEngine


VALID_BLOCK = {
    "doc_id": "QNF-DIAG-001",
    "title": "Live Diagnostic",
    "zone": "GREEN",
    "protocol": "Onset_Omega_1",
    "artifact_type": "DIAGNOSTIC",
    "cognitive_load": 8,
    "timestamp": "2026-05-21T00:00:00+00:00",
    "dependencies": ["CSTM-V30-FINAL-001"],
    "tags": ["diagnostic"],
    "status": "ACTIVE",
}


def test_valid_block_passes():
    result = MetadataEngine().validate(VALID_BLOCK)
    assert result["valid"], result["errors"]


def test_missing_all_fields_reports_all():
    result = MetadataEngine().validate({})
    assert not result["valid"]
    assert len(result["errors"]) >= 10


def test_each_required_field_missing_reported():
    for field in VALID_BLOCK.keys():
        block = {k: v for k, v in VALID_BLOCK.items() if k != field}
        result = MetadataEngine().validate(block)
        assert not result["valid"], f"{field} omission must fail"
        assert any(field in e for e in result["errors"]), f"Error for {field} missing"


def test_doc_id_pattern_enforced():
    block = {**VALID_BLOCK, "doc_id": "bad-id"}
    result = MetadataEngine().validate(block)
    assert not result["valid"]


def test_zone_load_cross_validation():
    block = {**VALID_BLOCK, "zone": "RED", "cognitive_load": 8}
    result = MetadataEngine().validate(block)
    assert not result["valid"]
    assert any("mismatches" in e for e in result["errors"])


def test_invalid_tag_format_rejected():
    block = {**VALID_BLOCK, "tags": ["BadTag"]}
    result = MetadataEngine().validate(block)
    assert not result["valid"]


def test_load_out_of_range():
    block = {**VALID_BLOCK, "cognitive_load": 15}
    result = MetadataEngine().validate(block)
    assert not result["valid"]


def test_bad_timestamp_rejected():
    block = {**VALID_BLOCK, "timestamp": "not-a-date"}
    result = MetadataEngine().validate(block)
    assert not result["valid"]
