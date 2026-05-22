from enum import Enum
from datetime import datetime, timezone


class Zone(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


ZONE_META = {
    Zone.GREEN: {"load_range": "7-10", "color": "#4CAF50", "access": "FREQUENT", "css": "zone-green"},
    Zone.YELLOW: {"load_range": "4-6", "color": "#FFC107", "access": "OCCASIONAL", "css": "zone-yellow"},
    Zone.RED: {"load_range": "1-3", "color": "#F44336", "access": "RARE", "css": "zone-red"},
}


class ZoneEngine:
    TRANSITIONS = {
        (Zone.GREEN, Zone.YELLOW): lambda doc: doc.cognitive_load < 7 and doc.status != "DRAFT",
        (Zone.YELLOW, Zone.RED): lambda doc: doc.cognitive_load < 4 and str(doc.version) >= "1.0",
        (Zone.RED, Zone.YELLOW): lambda doc: True,
        (Zone.RED, Zone.GREEN): lambda doc: True,
    }

    TRANSITION_ACTIONS = {
        (Zone.GREEN, Zone.YELLOW): "Update zone, timestamp",
        (Zone.YELLOW, Zone.RED): "Set ARCHIVED, timestamp",
        (Zone.RED, Zone.YELLOW): "Set ACTIVE, timestamp",
        (Zone.RED, Zone.GREEN): "Set DRAFT, timestamp",
    }

    @classmethod
    def classify(cls, cognitive_load: int) -> Zone:
        if cognitive_load >= 7:
            return Zone.GREEN
        elif cognitive_load >= 4:
            return Zone.YELLOW
        return Zone.RED

    @classmethod
    def can_migrate(cls, doc, target_zone: Zone) -> tuple[bool, str]:
        current = Zone(doc.zone)
        key = (current, target_zone)
        guard = cls.TRANSITIONS.get(key)
        if guard is None:
            return False, f"No transition from {current.value} to {target_zone.value}"
        if not guard(doc):
            return False, f"Guard condition not met for {current.value} -> {target_zone.value}"
        return True, "Migration approved"

    @classmethod
    def apply_migration(cls, doc, target_zone: Zone) -> dict:
        ok, msg = cls.can_migrate(doc, target_zone)
        if not ok:
            return {"success": False, "guard_result": msg}
        action = cls.TRANSITION_ACTIONS.get((Zone(doc.zone), target_zone), "")
        doc.zone = target_zone.value
        if "ARCHIVED" in action:
            doc.status = "ARCHIVED"
        elif "ACTIVE" in action:
            doc.status = "ACTIVE"
        elif "DRAFT" in action:
            doc.status = "DRAFT"
        doc.updated_at = datetime.now(timezone.utc)
        return {"success": True, "guard_result": msg, "action": action}
