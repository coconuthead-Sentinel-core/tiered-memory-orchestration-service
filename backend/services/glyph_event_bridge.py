"""Glyph Event Bridge - Phase 4 Symbolic Processing.

Bridges GlyphProcessor output to EventBus with Quantum Nexus lattice coordinates.
Each glyph shape maps to a cell in the lattice, enabling symbolic event routing.

Architecture:
    GlyphProcessor → GlyphEventBridge → EventBus[topic=glyph.*] → WebSocket/Dashboard

Lattice Mapping:
    APEX  → A1 (Node 1: Technical Arsenal) - Initiation/Query start
    CORE  → H1 (Node 2: Core Frameworks)   - Processing/Logic
    EMIT  → O1 (Node 3: Skill Forge)       - Action/Output
    ROOT  → V1 (Node 4: Meta Research)     - Ethics/Memory binding
    CUBE  → Z1 (Node 5: Career)            - Stability/Grounding
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from backend.domain.models import SymbolicMetadata
from backend.eventbus import bus

logger = logging.getLogger(__name__)

# Glyph → Lattice Cell mapping (Phase 4 coordinate binding)
GLYPH_LATTICE_MAP: Dict[str, Dict[str, Any]] = {
    "APEX": {
        "cell": "A1",
        "node": 1,
        "topic": "glyph.initiation",
        "r": 1,
        "c": 1,
        "label": "Initiation Point (Prime Truth)",
    },
    "CORE": {
        "cell": "H1",
        "node": 2,
        "topic": "glyph.process",
        "r": 2,
        "c": 2,
        "label": "Processing Core (Diagonal Node 2)",
    },
    "EMIT": {
        "cell": "O1",
        "node": 3,
        "topic": "glyph.action",
        "r": 3,
        "c": 3,
        "label": "Action Emitter (Diagonal Node 3)",
    },
    "ROOT": {
        "cell": "V1",
        "node": 4,
        "topic": "glyph.ethics",
        "r": 4,
        "c": 4,
        "label": "Ethics Root (Meta Research focal)",
    },
    "CUBE": {
        "cell": "Z1",
        "node": 5,
        "topic": "glyph.stability",
        "r": 5,
        "c": 2,
        "label": "Stability Terminus (Career)",
    },
}


@dataclass
class GlyphEvent:
    """Event payload for glyph processing results."""

    glyph: str
    cell: str
    node: int
    topic: str
    confidence: float
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    matched_seeds: List[str] = field(default_factory=list)
    applied_rules: Dict[str, str] = field(default_factory=dict)
    source_text_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "glyph": self.glyph,
            "cell": self.cell,
            "node": self.node,
            "topic": self.topic,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "matched_seeds": self.matched_seeds,
            "applied_rules": self.applied_rules,
            "source_text_hash": self.source_text_hash,
        }


class GlyphEventBridge:
    """
    Bridges glyph processing results to EventBus with lattice coordinates.

    Responsibilities:
    1. Accept SymbolicMetadata from GlyphProcessor
    2. Map matched glyphs to Quantum Nexus cells
    3. Emit events to topic-specific channels (glyph.initiation, glyph.process, etc.)
    4. Track event flow metrics for dashboard
    """

    def __init__(self, bus_instance=None):
        """
        Initialize bridge with optional custom EventBus.

        Args:
            bus_instance: Custom EventBus, defaults to global singleton
        """
        self._bus = bus_instance or bus
        self._metrics = {
            "events_emitted": 0,
            "glyphs_mapped": 0,
            "unmapped_glyphs": 0,
            "topics_used": set(),
        }
        logger.info("🌉 GlyphEventBridge initialized")

    def emit_from_metadata(
        self, metadata: SymbolicMetadata, source_text_hash: Optional[str] = None
    ) -> List[GlyphEvent]:
        """
        Emit events for all matched glyphs in metadata.

        Args:
            metadata: SymbolicMetadata from GlyphProcessor
            source_text_hash: Optional hash of source text for correlation

        Returns:
            List of GlyphEvent objects that were emitted
        """
        events: List[GlyphEvent] = []

        for match in metadata.matched_glyphs:
            if hasattr(match, "shape"):
                glyph_name = match.shape.upper()
                confidence = match.confidence
                matched_seeds = match.matched_seeds
                applied_rules = match.applied_rules
            else:
                glyph_name = str(match.get("shape", "")).upper()
                confidence = float(match.get("confidence", 0.0))
                matched_seeds = list(match.get("matched_seeds", []))
                applied_rules = dict(match.get("applied_rules", {}))

            event = self.emit_glyph(
                glyph_name=glyph_name,
                confidence=confidence,
                matched_seeds=matched_seeds,
                applied_rules=applied_rules,
                source_text_hash=source_text_hash,
            )
            if event:
                events.append(event)

        return events

    def emit_glyph(
        self,
        glyph_name: str,
        confidence: float = 1.0,
        matched_seeds: Optional[List[str]] = None,
        applied_rules: Optional[Dict[str, str]] = None,
        source_text_hash: Optional[str] = None,
    ) -> Optional[GlyphEvent]:
        """
        Emit a single glyph event to EventBus.

        Args:
            glyph_name: Name of glyph (APEX, CORE, EMIT, ROOT, CUBE)
            confidence: Match confidence 0.0-1.0
            matched_seeds: List of matched seed words
            applied_rules: Dict of applied transformation rules
            source_text_hash: Optional correlation hash

        Returns:
            GlyphEvent if mapped successfully, None otherwise
        """
        glyph_upper = glyph_name.upper()
        mapping = GLYPH_LATTICE_MAP.get(glyph_upper)

        if not mapping:
            self._metrics["unmapped_glyphs"] += 1
            logger.warning(f"⚠️ Unmapped glyph: {glyph_name}")
            return None

        event = GlyphEvent(
            glyph=glyph_upper,
            cell=mapping["cell"],
            node=mapping["node"],
            topic=mapping["topic"],
            confidence=confidence,
            matched_seeds=matched_seeds or [],
            applied_rules=applied_rules or {},
            source_text_hash=source_text_hash,
        )

        # Publish to topic-specific channel
        self._bus.publish(event.to_dict(), topic=event.topic)

        # Also publish to catch-all glyph channel
        self._bus.publish(event.to_dict(), topic="glyph")

        # Update metrics
        self._metrics["events_emitted"] += 1
        self._metrics["glyphs_mapped"] += 1
        self._metrics["topics_used"].add(event.topic)

        logger.debug(f"🜂 Emitted {glyph_upper} → {event.cell} (Node {event.node})")

        return event

    def emit_diagonal_trace(self, confidence: float = 1.0) -> List[GlyphEvent]:
        """
        Emit events along the diagonal dependency path (A1 → H1 → O1 → V1).

        This represents the dep_A1_to_V1 flow from Prime Truth to Meta Research.
        Useful for full-pipeline symbolic activation.

        Returns:
            List of emitted GlyphEvents along diagonal
        """
        diagonal_glyphs = ["APEX", "CORE", "EMIT", "ROOT"]
        events = []

        for glyph in diagonal_glyphs:
            event = self.emit_glyph(glyph, confidence=confidence)
            if event:
                events.append(event)

        logger.info(f"🔀 Diagonal trace emitted: {len(events)} events")
        return events

    def get_cell_for_glyph(self, glyph_name: str) -> Optional[str]:
        """Get lattice cell for a glyph name."""
        mapping = GLYPH_LATTICE_MAP.get(glyph_name.upper())
        return mapping["cell"] if mapping else None

    def get_topic_for_glyph(self, glyph_name: str) -> Optional[str]:
        """Get EventBus topic for a glyph name."""
        mapping = GLYPH_LATTICE_MAP.get(glyph_name.upper())
        return mapping["topic"] if mapping else None

    def metrics(self) -> Dict[str, Any]:
        """Get bridge metrics for dashboard."""
        return {
            "events_emitted": self._metrics["events_emitted"],
            "glyphs_mapped": self._metrics["glyphs_mapped"],
            "unmapped_glyphs": self._metrics["unmapped_glyphs"],
            "topics_used": list(self._metrics["topics_used"]),
            "bus_status": self._bus.status(),
        }


# Singleton instance for app-wide use
glyph_bridge = GlyphEventBridge()
