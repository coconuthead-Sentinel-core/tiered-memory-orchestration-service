import pytest
from types import SimpleNamespace

from app.services.zone_engine import ZoneEngine, Zone


@pytest.mark.parametrize("load,expected", [
    (10, Zone.GREEN), (8, Zone.GREEN), (7, Zone.GREEN),
    (6, Zone.YELLOW), (5, Zone.YELLOW), (4, Zone.YELLOW),
    (3, Zone.RED), (2, Zone.RED), (1, Zone.RED),
])
def test_classify_load_ranges(load, expected):
    assert ZoneEngine.classify(load) == expected


def test_green_to_yellow_guard_allows_when_load_drops_and_not_draft():
    doc = SimpleNamespace(zone="GREEN", cognitive_load=5, status="ACTIVE", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.YELLOW)
    assert ok


def test_green_to_yellow_guard_blocks_draft():
    doc = SimpleNamespace(zone="GREEN", cognitive_load=5, status="DRAFT", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.YELLOW)
    assert not ok


def test_green_to_yellow_blocks_high_load():
    doc = SimpleNamespace(zone="GREEN", cognitive_load=8, status="ACTIVE", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.YELLOW)
    assert not ok


def test_yellow_to_red_guard_allows_low_load_versioned():
    doc = SimpleNamespace(zone="YELLOW", cognitive_load=2, status="ACTIVE", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.RED)
    assert ok


def test_yellow_to_red_blocks_high_load():
    doc = SimpleNamespace(zone="YELLOW", cognitive_load=5, status="ACTIVE", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.RED)
    assert not ok


def test_red_to_yellow_manual_allowed():
    doc = SimpleNamespace(zone="RED", cognitive_load=2, status="ARCHIVED", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.YELLOW)
    assert ok


def test_red_to_green_scope_change_allowed():
    doc = SimpleNamespace(zone="RED", cognitive_load=2, status="ARCHIVED", version="1.0")
    ok, _ = ZoneEngine.can_migrate(doc, Zone.GREEN)
    assert ok


def test_invalid_transition_rejected():
    doc = SimpleNamespace(zone="YELLOW", cognitive_load=8, status="ACTIVE", version="1.0")
    ok, msg = ZoneEngine.can_migrate(doc, Zone.GREEN)
    assert not ok
    assert "No transition" in msg


def test_apply_migration_archives_yellow_to_red():
    doc = SimpleNamespace(zone="YELLOW", cognitive_load=2, status="ACTIVE", version="1.0", updated_at=None)
    result = ZoneEngine.apply_migration(doc, Zone.RED)
    assert result["success"]
    assert doc.zone == "RED"
    assert doc.status == "ARCHIVED"
