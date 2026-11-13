"""ADHD Burst Lens - Rapid Context Switching for Cognitive Processing.

Implements ADHD-friendly processing mode with:
- Short attention bursts (50-word chunks)
- Bullet-point formatting for quick scanning
- Action-oriented language emphasis
- Visual anchors and emoji markers

Architecture:
    ADHDLens → CognitiveOrchestrator → AI Adapter
"""

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ADHDLens:
    """
    ADHD Burst Lens for rapid context switching and chunked processing.

    Transforms content into ADHD-friendly formats:
    - Breaks long text into 50-word bullet points
    - Adds visual anchors (emojis, symbols)
    - Emphasizes action-oriented language
    - Maintains core meaning while improving scannability
    """

    # Configuration
    CHUNK_SIZE_WORDS = 50
    MAX_SENTENCES_PER_CHUNK = 4
    BULLET_MARKERS = ["⚡", "💥", "🚀", "🔥", "⚡", "💫", "⭐", "🎯"]
    ACTION_WORDS = [
        "start",
        "begin",
        "launch",
        "create",
        "build",
        "run",
        "execute",
        "activate",
    ]

    # Odooe Lattice Integration
    ODOOE_LATTICE_ENABLED = True
    MIRROR_ID = "M6"  # Burst Processing

    def __init__(self):
        """Initialize ADHD lens with default settings."""
        self.chunk_size = self.CHUNK_SIZE_WORDS
        self.max_sentences_per_chunk = self.MAX_SENTENCES_PER_CHUNK
        self.bullet_markers = list(self.BULLET_MARKERS)
        self.action_words = list(self.ACTION_WORDS)
        self.bullet_index = 0
        logger.info("🧠 ADHD Burst Lens initialized (Odooe Lattice Active)")

    def transform_context(self, context: str) -> str:
        """
        Transform context into ADHD-friendly format.

        Args:
            context: Original context string

        Returns:
            Transformed context with bullet points and visual anchors
        """
        if not context or not context.strip():
            return context

        # Split into sentences for processing
        sentences = self._split_into_sentences(context)

        # Group sentences into chunks
        chunks = self._create_chunks(sentences)

        # Format as bullet points
        bullet_points = self._format_as_bullets(chunks)

        # Join with ADHD-friendly formatting
        transformed = "\n\n".join(bullet_points)

        logger.debug(
            f"🧠 ADHD lens transformed {len(sentences)} sentences into {len(chunks)} chunks"
        )
        return transformed

    def transform_response(self, response: str) -> str:
        """
        Transform AI response into ADHD-friendly format.

        Args:
            response: Raw AI response

        Returns:
            ADHD-formatted response
        """
        if not response or not response.strip():
            return response

        # Apply same transformation as context
        return self.transform_context(response)

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (can be enhanced)
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _create_chunks(self, sentences: List[str]) -> List[str]:
        """Group sentences into word-count-limited chunks."""
        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            sentence_words = len(sentence.split())

            # If adding this sentence would exceed chunk size, start new chunk
            if current_chunk and (
                current_word_count + sentence_words > self.chunk_size
                or len(current_chunk) >= self.max_sentences_per_chunk
            ):
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0

            current_chunk.append(sentence)
            current_word_count += sentence_words

        # Add remaining sentences
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _format_as_bullets(self, chunks: List[str]) -> List[str]:
        """Format chunks as bullet points with visual markers."""
        bullets = []

        for i, chunk in enumerate(chunks):
            marker = self.BULLET_MARKERS[i % len(self.BULLET_MARKERS)]

            # Enhance with action words if present
            enhanced_chunk = self._enhance_action_words(chunk)

            bullet = f"{marker} {enhanced_chunk}"
            bullets.append(bullet)

        return bullets

    def _enhance_action_words(self, text: str) -> str:
        """Enhance action-oriented words with emphasis."""
        enhanced = text

        for word in self.ACTION_WORDS:
            # Add emphasis to action words (case-insensitive)
            pattern = r"\b" + re.escape(word) + r"\b"
            enhanced = re.sub(
                pattern, f"**{word.upper()}**", enhanced, flags=re.IGNORECASE
            )

        return enhanced

    def reset(self) -> None:
        """Reset lens state for new processing session."""
        self.bullet_index = 0
        logger.debug("🧠 ADHD lens reset")

    def get_config(self) -> Dict[str, Any]:
        """Get current lens configuration."""
        return {
            "chunk_size_words": self.chunk_size,
            "bullet_markers": self.bullet_markers,
            "action_words": self.action_words,
        }


# --- Convenience Functions ---


def create_adhd_lens() -> ADHDLens:
    """Create and return a configured ADHD lens instance."""
    return ADHDLens()


def transform_with_adhd_lens(text: str) -> str:
    """Convenience function to transform text with ADHD lens."""
    lens = ADHDLens()
    return lens.transform_context(text)
