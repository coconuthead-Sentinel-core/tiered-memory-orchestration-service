"""Glyph Parser for Symbolic Sequence Processing.

Parses symbolic glyph sequences and converts them to structured metadata
for the Cognitive Orchestrator. Provides mapping from visual symbols to
cognitive concepts and actions.

Architecture:
    glyph_parser.py → CognitiveOrchestrator → EventBus
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# --- Glyph Symbol Map ---

GLYPH_MAP = {
    # Meta-context symbols
    "🌐": "meta_context",
    "🔭": "observation_mode",
    "🌀": "cognitive_flow",
    # Action pulse symbols
    "🜂": "action_pulse",
    "⚙️": "processing_gear",
    "🔺": "initiation_triangle",
    # Memory zone symbols
    "🟢": "active_zone",
    "🟡": "pattern_zone",
    "🔴": "crystal_zone",
    # Cognitive lens symbols
    "🧠": "neurotypical_mode",
    "⚡": "adhd_burst",
    "🎯": "autism_precision",
    "🌊": "dyslexia_spatial",
}


def parse_glyph_sequence(sequence: str) -> Dict[str, Any]:
    """
    Parse a sequence of glyphs into structured metadata.

    Args:
        sequence: String containing glyph symbols

    Returns:
        Dict with parsed glyph information
    """
    if not sequence or not sequence.strip():
        return {"parsed": False, "glyphs": [], "concepts": []}

    parsed_glyphs = []
    concepts = []

    for char in sequence:
        if char in GLYPH_MAP:
            concept = GLYPH_MAP[char]
            parsed_glyphs.append({"symbol": char, "concept": concept})
            concepts.append(concept)
            logger.debug(f"🜂 Parsed glyph: {char} → {concept}")

    return {
        "parsed": len(parsed_glyphs) > 0,
        "glyphs": parsed_glyphs,
        "concepts": concepts,
        "sequence_length": len(sequence),
        "parsed_count": len(parsed_glyphs),
    }


def get_available_glyphs() -> Dict[str, str]:
    """Get the complete glyph symbol map."""
    return GLYPH_MAP.copy()


def add_glyph_mapping(symbol: str, concept: str) -> None:
    """
    Add a new glyph mapping dynamically.

    Args:
        symbol: The glyph symbol (emoji/character)
        concept: The cognitive concept it represents
    """
    GLYPH_MAP[symbol] = concept
    logger.info(f"🜂 Added glyph mapping: {symbol} → {concept}")


def get_concept_for_glyph(symbol: str) -> Optional[str]:
    """Get the concept for a specific glyph symbol."""
    return GLYPH_MAP.get(symbol)
