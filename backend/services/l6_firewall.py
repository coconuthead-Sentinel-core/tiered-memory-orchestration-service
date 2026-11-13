import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class L6EthicalFirewall:
    """
    L6 Ethical Firewall - The "Ethical Mirror"
    Enforces constraints defined in A1.Ω.Master_Optimization.json
    """

    def __init__(self, config_path: str = "A1.Ω.Master_Optimization.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.firewall_config = self.config.get("ethical_firewall_l6", {})
        self.reporting_protocol = self.config.get("reporting_protocol", {})

        self.core_values = self.firewall_config.get("core_values", [])
        self.neurodivergent_constraints = self.firewall_config.get(
            "neurodivergent_constraints", {}
        )

        logger.info(f"L6 Ethical Firewall initialized. Values: {self.core_values}")

    def _load_config(self) -> Dict:
        try:
            if self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Fallback check for parent directory if running from backend/
                parent_path = Path("..") / self.config_path
                if parent_path.exists():
                    with open(parent_path, "r", encoding="utf-8") as f:
                        return json.load(f)

                logger.warning(f"L6 Config not found at {self.config_path}")
                return {}
        except Exception as e:
            logger.error(f"Failed to load L6 Config: {e}")
            return {}

    def validate_request(self, content: str) -> bool:
        """
        Validate incoming request against Ethical Mirror protocols.
        Returns True if allowed, False if blocked.
        """
        # TODO: Implement semantic analysis against core values
        # For now, we pass everything but log the check
        return True

    def apply_constraints(self, content: str, lens: str = "neurotypical") -> str:
        """
        Apply L6 constraints to the output content based on the active lens.
        """
        # 1. Word Count Check (Hard Limit)
        max_words = self.reporting_protocol.get("metrics", {}).get(
            "max_word_count", 450
        )
        words = content.split()
        if len(words) > max_words:
            logger.info(
                f"L6 Firewall: Truncating content from {len(words)} to {max_words} words."
            )
            truncation_marker = "[TRUNCATED BY L6 FIREWALL]"
            marker_word_count = len(truncation_marker.split())
            allowed_content_words = max(1, max_words - marker_word_count)
            content = " ".join(words[:allowed_content_words]) + f" {truncation_marker}"

        # 2. Neurodivergent Formatting (Lens-specific)
        # These are "soft" constraints applied as post-processing if the AI missed them

        if lens == "autism":
            # Constraint: Explicit Structure / Literal Language
            # Ensure no ambiguous metaphors (simple check)
            pass

        elif lens == "adhd":
            # Constraint: Block-based Pacing / Emoji Anchors
            # If the content is a wall of text, break it up
            if "\n\n" not in content and len(words) > 50:
                # Naive paragraph break
                sentences = content.split(". ")
                chunks = []
                current_chunk = []
                for s in sentences:
                    current_chunk.append(s)
                    if len(current_chunk) >= 3:
                        chunks.append(". ".join(current_chunk) + ".")
                        current_chunk = []
                if current_chunk:
                    chunks.append(". ".join(current_chunk))
                content = "\n\n".join(chunks)

        elif lens == "dyslexia":
            # Constraint: Visual Mapping / Color-Coded Blocks
            # Ensure key terms are highlighted (Markdown bold)
            # This is a simple heuristic
            pass

        return content


# Singleton instance
l6_firewall = L6EthicalFirewall()
