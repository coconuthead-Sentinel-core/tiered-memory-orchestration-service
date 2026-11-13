import json
import os
import threading
from typing import Any, Dict


class JSONStore:
    """Thread-safe JSON persistence for minimal state (rules, memory, etc.)."""

    def __init__(self, path: str = "data/state.json") -> None:
        self.path = path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def load(self) -> Dict[str, Any]:
        with self._lock:
            if not os.path.exists(self.path):
                return {}
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}

    def save(self, payload: Dict[str, Any]) -> None:
        with self._lock:
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
