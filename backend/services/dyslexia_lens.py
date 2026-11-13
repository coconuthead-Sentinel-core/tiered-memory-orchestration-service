"""Dyslexia Spatial Lens - Multi-dimensional Processing for Cognitive Enhancement.

Implements Dyslexia-friendly processing mode with:
- Visual anchors and spatial organization
- Symbol-rich representations
- Chunking with color-coded sections
- Alternative pathways for information flow

Architecture:
    DyslexiaLens → CognitiveOrchestrator → AI Adapter
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DyslexiaLens:
    """
    Dyslexia Spatial Lens for multi-dimensional, visually-anchored processing.
    """

    SPATIAL_ANCHORS = ["🌟", "🔮", "🎨", "🌈", "🎭", "🎪", "🎨", "🌟"]
    CHUNK_MARKERS = ["📦", "🎁", "🗂️", "📚", "🎯", "🧭"]
    NAVIGATION_SYMBOLS = ["⬆️", "⬇️", "⬅️", "➡️", "🔄", "🔀"]
    COLOR_INDICATORS = ["🟡", "🟠", "🟣", "🟢", "🔵", "🟤"]

    ODOOE_LATTICE_ENABLED = True
    MIRROR_ID = "M5"

    def __init__(self):
        self.anchor_index = 0
        self.chunk_index = 0
        self.color_index = 0
        logger.info("🧠 Dyslexia Spatial Lens initialized (Odooe Lattice Active)")

    def transform_context(self, context: str) -> str:
        """
        Transform context into a Dyslexia-friendly format using spatial layout and symbols.
        """
        if not context or not context.strip():
            return context

        sentences = [
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+", context.strip())
            if part.strip()
        ]
        if not sentences:
            return ""

        central_idea = sentences[0]
        concept_source = " ".join(sentences[1:]) if len(sentences) > 1 else sentences[0]
        words = re.findall(r"\b\w{4,}\b", concept_source.lower())
        key_concepts = sorted(set(words))[:5]
        symbols = ["💡", "⚙️", "🔗", "🎯", "📊"]
        symbol_map = {concept: symbol for concept, symbol in zip(key_concepts, symbols)}

        transformed_parts = [
            "--- Spatial Map ---",
            "      [ 🧠 Central Idea ]",
            "              |",
            f'      " {central_idea} "',
            "              |",
            "     /        |        \\",
            "    /         |         \\",
        ]

        if key_concepts:
            concept_lines = [
                f"{symbol_map.get(concept, '🔹')} {concept}" for concept in key_concepts
            ]
            transformed_parts.append(f"  {concept_lines[0]:<15}")
            if len(concept_lines) > 1:
                transformed_parts[-1] += f"--- [ {concept_lines[1]} ]"
            if len(concept_lines) > 2:
                transformed_parts.append("    /         |         \\")
                transformed_parts.append(f"  [ {concept_lines[2]} ]")
            if len(concept_lines) > 3:
                transformed_parts[-1] += f" --- {concept_lines[3]} 🔹"
            if len(concept_lines) > 4:
                transformed_parts.append("              |")
                transformed_parts.append(f"        🔹 {concept_lines[4]}")

        transformed_parts.append("\n--- End Map ---")

        logger.debug(
            "🧠 Dyslexia lens transformed text into a spatial map with %s concepts.",
            len(key_concepts),
        )
        return "\n".join(transformed_parts)

    def get_transformation_stats(self) -> Dict[str, Any]:
        return {
            "lens_type": "dyslexia_spatial",
            "anchors_used": self.anchor_index,
            "chunks_processed": self.chunk_index,
            "colors_used": self.color_index,
            "spatial_anchors": self.SPATIAL_ANCHORS,
            "navigation_symbols": self.NAVIGATION_SYMBOLS,
        }


def create_dyslexia_lens() -> DyslexiaLens:
    return DyslexiaLens()


def transform_with_dyslexia_lens(text: str) -> str:
    lens = DyslexiaLens()
    return lens.transform_context(text)
