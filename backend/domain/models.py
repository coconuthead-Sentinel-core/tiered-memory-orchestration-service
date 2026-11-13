import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    """Base class for all domain entities."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Strict mode: ignore extra fields passed during initialization
    model_config = ConfigDict(extra="ignore")


# --- Cognitive Zone Enums (Three-Zone Memory System) ---


class MemoryZone(str, Enum):
    """
    Three-zone memory classification based on entropy thresholds.

    🟢 ACTIVE: High entropy (>0.7) - Real-time processing, novel content
    🟡 PATTERN: Mid entropy (0.3-0.7) - Pattern emergence, semi-stable
    🔴 CRYSTALLIZED: Low entropy (<0.3) - Stable storage, well-known patterns
    """

    ACTIVE = "active"  # 🟢 High entropy - real-time
    PATTERN = "pattern"  # 🟡 Mid entropy - emerging patterns
    CRYSTALLIZED = "crystal"  # 🔴 Low entropy - stable memory


class CognitiveLens(str, Enum):
    """
    Neurodivergent processing modes for adaptive AI responses.

    Each lens adjusts how information is processed and presented.
    """

    NEUROTYPICAL = "neurotypical"  # Baseline processing
    ADHD_BURST = "adhd"  # Rapid context-switching, shorter chunks
    AUTISM_PRECISION = "autism"  # Detail focus, explicit structure
    DYSLEXIA_SPATIAL = "dyslexia"  # Multi-dimensional, symbol-rich


class Glyph(Entity):
    """
    A symbolic pattern representing a concept or event type.
    Glyphs are used by the CognitiveOrchestrator to identify and categorize
    incoming information based on pattern matching.
    """

    shape: str = Field(
        ...,
        description="A unique identifier for the glyph's pattern, e.g., 'event:user_login:success'",
    )
    topic: str = Field(
        ...,
        description="The general topic this glyph relates to, e.g., 'user_authentication'",
    )
    description: str = Field(
        ..., description="A human-readable description of what this glyph represents."
    )
    rules: Dict[str, Any] = Field(
        default_factory=dict,
        description="A set of rules used for matching this glyph pattern.",
    )
    seed_keywords: Set[str] = Field(
        default_factory=set,
        description="A set of seed keywords to initiate a pattern match.",
    )


class GlyphMatch(BaseModel):
    """Represents a matched glyph pattern."""

    shape: str
    topic: str
    confidence: float
    matched_seeds: List[str]
    applied_rules: Dict[str, str]
    model_config = ConfigDict(extra="ignore")


class SymbolicMetadata(BaseModel):
    """Metadata generated from symbolic processing."""

    matched_glyphs: List[GlyphMatch]
    dominant_topic: Optional[str] = None
    symbolic_tags: Set[str] = Field(default_factory=set)
    model_config = ConfigDict(extra="ignore")


class Note(Entity):
    """
    A discrete unit of information stored in the Memory Lattice.
    Pure domain model: No database aliases here.
    """

    text: str
    tag: str
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ZonedNote(Note):
    """
    A Note enhanced with three-zone memory classification.

    Extends Note with:
    - zone: Which memory zone this note belongs to (active/pattern/crystal)
    - entropy: Information entropy score (0.0-1.0)
    - lens_applied: Which cognitive lens was used during processing
    - symbolic_metadata: Results from glyph pattern matching

    Pure domain model: No database aliases. ConfigDict inherited from Entity.
    """

    zone: MemoryZone = MemoryZone.ACTIVE
    entropy: float = Field(default=0.5, ge=0.0, le=1.0)
    lens_applied: Optional[CognitiveLens] = None
    symbolic_metadata: Optional[SymbolicMetadata] = None

    # Inherits model_config = ConfigDict(extra="ignore") from Entity


class ZoneMetrics(BaseModel):
    """
    Aggregated metrics for memory zone distribution.
    Used for real-time dashboard updates.
    """

    active_count: int = 0
    pattern_count: int = 0
    crystal_count: int = 0
    avg_entropy: float = 0.0
    last_transition: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class MemorySnapshot(Entity):
    """A snapshot of the system's cognitive state."""

    summary: str
    active_nodes: int
    entropy_level: float
