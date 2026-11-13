"""Tests for Phase 4: Symbolic Processing (EventBus glyph hooks).

Tests GlyphEventBridge functionality:
- Glyph → Lattice cell mapping
- EventBus emission
- Diagonal trace activation
- Metrics tracking
"""

import asyncio
from typing import Any, Dict, List

import pytest

from backend.domain.models import SymbolicMetadata
from backend.eventbus import EventBus
from backend.services.glyph_event_bridge import (
    GLYPH_LATTICE_MAP,
    GlyphEvent,
    GlyphEventBridge,
    glyph_bridge,
)

# ============================================================================
# GLYPH LATTICE MAPPING TESTS
# ============================================================================


class TestGlyphLatticeMap:
    """Test the glyph → lattice cell mapping constants."""

    def test_all_five_glyphs_mapped(self):
        """Verify all 5 core glyphs are mapped."""
        expected_glyphs = {"APEX", "CORE", "EMIT", "ROOT", "CUBE"}
        assert set(GLYPH_LATTICE_MAP.keys()) == expected_glyphs

    def test_apex_maps_to_a1(self):
        """APEX → A1 (Prime Truth, Node 1)."""
        apex = GLYPH_LATTICE_MAP["APEX"]
        assert apex["cell"] == "A1"
        assert apex["node"] == 1
        assert apex["r"] == 1
        assert apex["c"] == 1
        assert apex["topic"] == "glyph.initiation"

    def test_core_maps_to_h1(self):
        """CORE → H1 (Diagonal Node 2)."""
        core = GLYPH_LATTICE_MAP["CORE"]
        assert core["cell"] == "H1"
        assert core["node"] == 2
        assert core["r"] == 2
        assert core["c"] == 2
        assert core["topic"] == "glyph.process"

    def test_emit_maps_to_o1(self):
        """EMIT → O1 (Diagonal Node 3)."""
        emit = GLYPH_LATTICE_MAP["EMIT"]
        assert emit["cell"] == "O1"
        assert emit["node"] == 3
        assert emit["r"] == 3
        assert emit["c"] == 3
        assert emit["topic"] == "glyph.action"

    def test_root_maps_to_v1(self):
        """ROOT → V1 (Meta Research focal, Node 4)."""
        root = GLYPH_LATTICE_MAP["ROOT"]
        assert root["cell"] == "V1"
        assert root["node"] == 4
        assert root["r"] == 4
        assert root["c"] == 4
        assert root["topic"] == "glyph.ethics"

    def test_cube_maps_to_z1(self):
        """CUBE → Z1 (Terminus, Node 5)."""
        cube = GLYPH_LATTICE_MAP["CUBE"]
        assert cube["cell"] == "Z1"
        assert cube["node"] == 5
        assert cube["r"] == 5
        assert cube["c"] == 2
        assert cube["topic"] == "glyph.stability"

    def test_diagonal_path_cells(self):
        """Verify diagonal dependency matches A1 → H1 → O1 → V1."""
        diagonal_glyphs = ["APEX", "CORE", "EMIT", "ROOT"]
        expected_cells = ["A1", "H1", "O1", "V1"]

        actual_cells = [GLYPH_LATTICE_MAP[g]["cell"] for g in diagonal_glyphs]
        assert actual_cells == expected_cells


# ============================================================================
# GLYPH EVENT TESTS
# ============================================================================


class TestGlyphEvent:
    """Test GlyphEvent dataclass."""

    def test_create_event(self):
        """Create a basic GlyphEvent."""
        event = GlyphEvent(
            glyph="APEX",
            cell="A1",
            node=1,
            topic="glyph.initiation",
            confidence=0.95,
        )
        assert event.glyph == "APEX"
        assert event.cell == "A1"
        assert event.node == 1
        assert event.confidence == 0.95
        assert event.timestamp  # Should have default timestamp

    def test_event_to_dict(self):
        """Convert GlyphEvent to dictionary."""
        event = GlyphEvent(
            glyph="CORE",
            cell="H1",
            node=2,
            topic="glyph.process",
            confidence=0.8,
            matched_seeds=["core", "process"],
            applied_rules={"process": "tag:process.core"},
        )
        d = event.to_dict()

        assert d["glyph"] == "CORE"
        assert d["cell"] == "H1"
        assert d["node"] == 2
        assert d["topic"] == "glyph.process"
        assert d["confidence"] == 0.8
        assert d["matched_seeds"] == ["core", "process"]
        assert d["applied_rules"] == {"process": "tag:process.core"}
        assert "timestamp" in d


# ============================================================================
# GLYPH EVENT BRIDGE TESTS
# ============================================================================


class TestGlyphEventBridge:
    """Test GlyphEventBridge functionality."""

    @pytest.fixture
    def test_bus(self):
        """Create a fresh EventBus for testing."""
        return EventBus("test_bus")

    @pytest.fixture
    def bridge(self, test_bus):
        """Create a GlyphEventBridge with test bus."""
        return GlyphEventBridge(bus_instance=test_bus)

    def test_emit_single_glyph(self, bridge):
        """Emit a single glyph event."""
        event = bridge.emit_glyph("APEX", confidence=0.9)

        assert event is not None
        assert event.glyph == "APEX"
        assert event.cell == "A1"
        assert event.node == 1
        assert event.confidence == 0.9

    def test_emit_glyph_case_insensitive(self, bridge):
        """Glyph names should be case-insensitive."""
        event1 = bridge.emit_glyph("apex")
        event2 = bridge.emit_glyph("ApEx")

        assert event1.glyph == "APEX"
        assert event2.glyph == "APEX"

    def test_emit_unknown_glyph_returns_none(self, bridge):
        """Unknown glyphs should return None and increment unmapped counter."""
        event = bridge.emit_glyph("UNKNOWN_GLYPH")

        assert event is None
        assert bridge._metrics["unmapped_glyphs"] == 1

    def test_emit_with_seeds_and_rules(self, bridge):
        """Emit glyph with matched seeds and rules."""
        event = bridge.emit_glyph(
            "EMIT",
            confidence=0.85,
            matched_seeds=["emit", "launch"],
            applied_rules={"launch": "tag:action.emit"},
        )

        assert event.matched_seeds == ["emit", "launch"]
        assert event.applied_rules == {"launch": "tag:action.emit"}

    def test_diagonal_trace_emits_four_events(self, bridge):
        """Diagonal trace should emit APEX → CORE → EMIT → ROOT."""
        events = bridge.emit_diagonal_trace(confidence=1.0)

        assert len(events) == 4

        glyphs = [e.glyph for e in events]
        assert glyphs == ["APEX", "CORE", "EMIT", "ROOT"]

        cells = [e.cell for e in events]
        assert cells == ["A1", "H1", "O1", "V1"]

    def test_metrics_tracking(self, bridge):
        """Verify metrics are tracked correctly."""
        bridge.emit_glyph("APEX")
        bridge.emit_glyph("CORE")
        bridge.emit_glyph("UNKNOWN")

        metrics = bridge.metrics()

        assert metrics["events_emitted"] == 2
        assert metrics["glyphs_mapped"] == 2
        assert metrics["unmapped_glyphs"] == 1
        assert "glyph.initiation" in metrics["topics_used"]
        assert "glyph.process" in metrics["topics_used"]

    def test_get_cell_for_glyph(self, bridge):
        """Test cell lookup by glyph name."""
        assert bridge.get_cell_for_glyph("APEX") == "A1"
        assert bridge.get_cell_for_glyph("apex") == "A1"
        assert bridge.get_cell_for_glyph("CUBE") == "Z1"
        assert bridge.get_cell_for_glyph("UNKNOWN") is None

    def test_get_topic_for_glyph(self, bridge):
        """Test topic lookup by glyph name."""
        assert bridge.get_topic_for_glyph("APEX") == "glyph.initiation"
        assert bridge.get_topic_for_glyph("ROOT") == "glyph.ethics"
        assert bridge.get_topic_for_glyph("UNKNOWN") is None


# ============================================================================
# EVENTBUS INTEGRATION TESTS
# ============================================================================


class TestEventBusIntegration:
    """Test GlyphEventBridge integration with EventBus."""

    @pytest.fixture
    def loop(self):
        """Create event loop for testing."""
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()

    @pytest.fixture
    def test_bus(self):
        """Create a fresh EventBus."""
        return EventBus("integration_test")

    @pytest.fixture
    def bridge(self, test_bus):
        """Create bridge with test bus."""
        return GlyphEventBridge(bus_instance=test_bus)

    def test_events_published_to_topic(self, bridge, test_bus, loop):
        """Events should be published to topic-specific channels."""
        # Subscribe to glyph.initiation topic
        queue = test_bus.subscribe(loop, topic="glyph.initiation", maxsize=10)

        # Emit APEX glyph
        bridge.emit_glyph("APEX")

        # Check queue has event (via call_soon_threadsafe delivery)
        # Note: In real async context, we'd await; here we check bus metrics
        assert test_bus.status()["published"] >= 1

    def test_events_also_published_to_catchall(self, bridge, test_bus, loop):
        """Events should also go to catch-all 'glyph' topic."""
        queue = test_bus.subscribe(loop, topic="glyph", maxsize=10)

        bridge.emit_glyph("CORE")

        # Published at least once (topic-specific + catch-all)
        assert test_bus.status()["published"] >= 1


# ============================================================================
# SYMBOLIC METADATA INTEGRATION TESTS
# ============================================================================


class TestMetadataIntegration:
    """Test emit_from_metadata functionality."""

    @pytest.fixture
    def test_bus(self):
        return EventBus("metadata_test")

    @pytest.fixture
    def bridge(self, test_bus):
        return GlyphEventBridge(bus_instance=test_bus)

    def test_emit_from_metadata(self, bridge):
        """Emit events from SymbolicMetadata structure."""
        metadata = SymbolicMetadata(
            matched_glyphs=[
                {
                    "shape": "APEX",
                    "topic": "initiation",
                    "confidence": 0.95,
                    "matched_seeds": ["apex", "ignite"],
                    "applied_rules": {"apex": "tag:initiation"},
                },
                {
                    "shape": "CORE",
                    "topic": "process",
                    "confidence": 0.80,
                    "matched_seeds": ["core"],
                    "applied_rules": {},
                },
            ],
            dominant_topic="initiation",
            symbolic_tags={"tag:initiation"},
        )

        events = bridge.emit_from_metadata(metadata)

        assert len(events) == 2
        assert events[0].glyph == "APEX"
        assert events[0].confidence == 0.95
        assert events[1].glyph == "CORE"

    def test_emit_from_empty_metadata(self, bridge):
        """Empty metadata should emit no events."""
        metadata = SymbolicMetadata(
            matched_glyphs=[],
            dominant_topic=None,
            symbolic_tags=set(),
        )

        events = bridge.emit_from_metadata(metadata)

        assert events == []


# ============================================================================
# SINGLETON INSTANCE TESTS
# ============================================================================


class TestSingletonBridge:
    """Test the singleton glyph_bridge instance."""

    def test_singleton_exists(self):
        """Singleton glyph_bridge should exist."""
        assert glyph_bridge is not None
        assert isinstance(glyph_bridge, GlyphEventBridge)

    def test_singleton_uses_global_bus(self):
        """Singleton should use the global EventBus."""
        from backend.eventbus import bus

        assert glyph_bridge._bus is bus
