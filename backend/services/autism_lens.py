"""Autism Precision Lens - Detail Focus for Cognitive Processing.

Implements Autism-friendly processing mode with:
- Explicit structure and categorization
- Detail emphasis and pattern recognition
- Logical sequencing and hierarchical organization
- Clear boundaries and explicit relationships

Architecture:
    AutismLens → CognitiveOrchestrator → AI Adapter
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AutismLens:
    """
    Autism Precision Lens for detail-focused, structured processing.

    Transforms content into Autism-friendly formats:
    - Adds explicit categorization and labeling
    - Emphasizes logical relationships and hierarchies
    - Provides clear boundaries and structure
    - Highlights patterns and details
    """

    CATEGORY_MARKERS = ["📂", "🏷️", "🔍", "📊", "🔗"]
    RELATIONSHIP_INDICATORS = ["→", "↔", "⊂", "⊃", "∋"]
    NON_DEFINITION_TERMS = {"first", "second", "third", "next", "then", "finally"}
    STRUCTURE_PATTERNS = [
        r"^(\d+\.|\-|\•)\s*",
        r"^(First|Second|Third|Next|Then|Finally)\b",
        r"^(Because|Therefore|However|Although|Since)\b",
    ]

    ODOOE_LATTICE_ENABLED = True
    MIRROR_ID = "M3"

    def __init__(self):
        self.category_index = 0
        logger.info("🧠 Autism Precision Lens initialized (Odooe Lattice Active)")

    def transform_context(self, context: str) -> str:
        """
        Transform context into an Autism-friendly format with explicit structure.
        """
        if not context or not context.strip():
            return context

        normalized = re.sub(r"\s+(?=[*-]\s)", "\n", context.strip())
        lines = [line.strip() for line in normalized.splitlines() if line.strip()]
        first_line_sentences = self._split_into_sentences(lines[0]) if lines else []
        main_point = first_line_sentences[0] if first_line_sentences else ""

        definitions = self._extract_definitions(normalized)
        definition_sentences = {
            item["source_sentence"] for item in definitions.values()
        }

        details: List[str] = []
        for sentence in first_line_sentences[1:]:
            if sentence not in definition_sentences:
                details.append(sentence)

        for line in lines[1:]:
            if line.startswith(("- ", "* ")):
                details.append(line)
                continue
            for sentence in self._split_into_sentences(line):
                if sentence not in definition_sentences:
                    details.append(sentence)

        if len(details) > 3:
            details = details[:3]

        transformed_parts = [
            "### 🎯 Main Point",
            main_point,
            "\n---",
        ]

        if details:
            transformed_parts.append("### 🔢 Key Details")
            for index, detail in enumerate(details, 1):
                transformed_parts.append(f"{index}. {detail}")
            transformed_parts.append("\n---")

        if definitions:
            transformed_parts.append("### 📚 Definitions")
            for definition in definitions.values():
                transformed_parts.append(
                    f"- **{definition['term'].strip()}**: {definition['definition'].strip()}."
                )
            transformed_parts.append("\n---")

        transformed_parts.append(
            f"### 🏁 Conclusion\nThe text covers the main point about '{main_point[:30]}...' "
            f"with {len(details)} supporting detail(s) and {len(definitions)} definition(s)."
        )

        logger.debug(
            "🧠 Autism lens transformed text into %s structured parts.",
            len(transformed_parts),
        )
        return "\n\n".join(transformed_parts)

    def _split_into_sentences(self, text: str) -> List[str]:
        return [
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+", text.strip())
            if part.strip()
        ]

    def _extract_definitions(self, text: str) -> Dict[str, Dict[str, str]]:
        pattern = re.compile(
            r"(?P<sentence>(?:^|(?<=[.!?])\s*)(?:A|An|The)?\s*(?P<term>[A-Za-z][A-Za-z0-9_]*)\s+"
            r"(?P<verb>is|means)\s+(?P<definition>[^.]+)\.)",
            re.IGNORECASE,
        )
        definitions: Dict[str, Dict[str, str]] = {}
        for match in pattern.finditer(text):
            term = match.group("term")
            if term.lower() in self.NON_DEFINITION_TERMS:
                continue
            definitions[term.lower()] = {
                "term": term,
                "definition": match.group("definition"),
                "source_sentence": match.group("sentence").strip(),
            }
        return definitions

    def get_transformation_stats(self) -> Dict[str, Any]:
        return {
            "lens_type": "autism_precision",
            "category_markers_used": self.category_index,
            "structure_patterns": self.STRUCTURE_PATTERNS,
            "relationship_indicators": self.RELATIONSHIP_INDICATORS,
        }


def create_autism_lens() -> AutismLens:
    return AutismLens()


def transform_with_autism_lens(text: str) -> str:
    lens = AutismLens()
    return lens.transform_context(text)
