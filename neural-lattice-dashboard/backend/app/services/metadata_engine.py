import re
from datetime import datetime
from .zone_engine import ZoneEngine


ARTIFACT_TYPES = {
    "SYS_ARCH", "BLUEPRINT", "INT_GUIDE", "REF_SCHEMA",
    "CHARTER", "DIAGNOSTIC", "PROTOCOL", "TEST", "CONFIG",
}

VALID_PROTOCOLS = {"Onset_Omega_1", "Joy_Protocol", "Coconut_Head", "Combined"}

VALID_STATUSES = {"DRAFT", "ACTIVE", "TESTING", "ARCHIVED", "REFERENCE", "PRODUCTION"}


def _is_iso8601(v) -> bool:
    if not isinstance(v, str):
        return False
    try:
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return True
    except (ValueError, TypeError):
        return False


REQUIRED_FIELDS = {
    "doc_id": r"^[A-Z]{2,5}-[A-Z0-9]{2,8}(-[A-Z0-9]{1,8})?-[0-9]{3}$",
    "title": lambda v: isinstance(v, str) and 0 < len(v) <= 200,
    "zone": lambda v: v in ("GREEN", "YELLOW", "RED"),
    "protocol": lambda v: v in VALID_PROTOCOLS,
    "artifact_type": lambda v: v in ARTIFACT_TYPES,
    "cognitive_load": lambda v: isinstance(v, int) and 1 <= v <= 10,
    "timestamp": lambda v: _is_iso8601(v),
    "dependencies": lambda v: isinstance(v, list),
    "tags": lambda v: isinstance(v, list) and all(isinstance(t, str) and re.match(r"^[a-z_]+$", t) for t in v),
    "status": lambda v: v in VALID_STATUSES,
}


class MetadataEngine:
    def validate(self, block: dict) -> dict:
        errors = []
        if not isinstance(block, dict):
            return {"valid": False, "errors": ["metadata_block must be an object"]}
        for field, rule in REQUIRED_FIELDS.items():
            if field not in block:
                errors.append(f"Missing required field: {field}")
                continue
            value = block[field]
            if isinstance(rule, str):
                if not isinstance(value, str) or not re.match(rule, value):
                    errors.append(f"{field}: does not match pattern {rule}")
            elif callable(rule):
                try:
                    if not rule(value):
                        errors.append(f"{field}: validation failed")
                except Exception:
                    errors.append(f"{field}: validation failed")
        if "zone" in block and "cognitive_load" in block:
            try:
                expected = ZoneEngine.classify(block["cognitive_load"])
                if block["zone"] != expected.value:
                    errors.append(
                        f"zone {block['zone']} mismatches load {block['cognitive_load']}"
                    )
            except Exception:
                pass
        return {"valid": len(errors) == 0, "errors": errors}
