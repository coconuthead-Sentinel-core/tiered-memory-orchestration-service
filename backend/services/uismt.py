import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class UISMT:
    """
    Universal Input Stream Memory Threading (UISMT)
    Node 8 Ingestion Protocol.
    Auto-threads every query, image, or document into seven color-coded categories.
    """

    # Color-coded categories
    CATEGORIES = {
        "GOLDEN": "Framework",  # Core architecture, rules
        "NEURAL": "Processing",  # Active thought, logic
        "BLUE": "Data",  # Raw facts, inputs
        "RED": "Critical",  # Errors, alerts, crystallized truths
        "GREEN": "Growth",  # New ideas, expansion
        "PURPLE": "Creative",  # Dreams, metaphors
        "GREY": "Archive",  # Old logs, history
    }

    def __init__(self):
        self.threads: Dict[str, List[Any]] = {k: [] for k in self.CATEGORIES.keys()}

    def thread_input(self, input_data: Any, input_type: str = "text") -> Dict[str, Any]:
        """
        Ingest and thread input into the appropriate category.
        """
        category = self._determine_category(input_data, input_type)

        # Thread the data
        self.threads[category].append(
            {"type": input_type, "data": input_data, "status": "ingested"}
        )

        logger.info(
            f"🧵 UISMT: Threaded input into {category} ({self.CATEGORIES[category]})"
        )

        return {
            "category": category,
            "description": self.CATEGORIES[category],
            "thread_id": f"{category}_{len(self.threads[category])}",
        }

    def _determine_category(self, data: Any, input_type: str) -> str:
        """
        Heuristic to determine the category.
        """
        # Simple keyword-based heuristic for now
        text = str(data).lower()

        if "error" in text or "critical" in text or "fail" in text:
            return "RED"
        elif "dream" in text or "imagine" in text or "creative" in text:
            return "PURPLE"
        elif "framework" in text or "rule" in text or "protocol" in text:
            return "GOLDEN"
        elif "learn" in text or "grow" in text or "new" in text:
            return "GREEN"
        elif input_type == "image":
            return "BLUE"
        else:
            return "NEURAL"  # Default processing


uismt = UISMT()
