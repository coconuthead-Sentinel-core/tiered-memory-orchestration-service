import os
import time
from typing import Callable, Dict, Optional

from fastapi import (  # type: ignore[reportMissingImports]
    Depends,
    Header,
    HTTPException,
    WebSocket,
)
from starlette.requests import Request


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """Simple API key guard.

    Behavior:
      - If QNF_API_KEY is set, require header X-API-Key to match.
      - Else if QNF_REQUIRE_API_KEY is truthy, reject all without a configured key.
      - Otherwise (dev), allow.
    """
    configured = os.getenv("QNF_API_KEY")
    require = str(os.getenv("QNF_REQUIRE_API_KEY", "0")).lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if configured:
        if not x_api_key or x_api_key != configured:
            raise HTTPException(status_code=401, detail="invalid api key")
        return
    if require:
        raise HTTPException(status_code=401, detail="api key required (not configured)")


def websocket_require_api_key(ws: WebSocket) -> None:
    """Enforce API key for WebSocket connections using header or query param.

    Header: X-API-Key
    Query:  api_key
    """
    configured = os.getenv("QNF_API_KEY")
    require = str(os.getenv("QNF_REQUIRE_API_KEY", "0")).lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if not configured and not require:
        return
    # Try header then query param
    header_val = ws.headers.get("x-api-key")
    query_val = ws.query_params.get("api_key")
    provided = header_val or query_val
    if not configured:
        # Require but not configured ⇒ reject
        raise HTTPException(status_code=401, detail="api key required (not configured)")
    if provided != configured:
        raise HTTPException(status_code=401, detail="invalid api key")


class RateLimiter:
    """Simple in-memory token bucket per client ip.

    Enabled if QNF_RATE_LIMIT_ENABLED is truthy.
    Configure with:
      - QNF_RATE_LIMIT_RPM (requests per minute)
      - QNF_RATE_LIMIT_BURST (max bucket size)
    """

    def __init__(self) -> None:
        self.enabled = str(os.getenv("QNF_RATE_LIMIT_ENABLED", "0")).lower() in (
            "1",
            "true",
            "yes",
            "on",
        )
        self.rpm = int(os.getenv("QNF_RATE_LIMIT_RPM", "600"))
        self.burst = int(os.getenv("QNF_RATE_LIMIT_BURST", "120"))
        self._buckets: Dict[str, Dict[str, float]] = {}

    def _key(self, request: Request) -> str:
        client = request.client.host if request.client else "unknown"
        return client

    def __call__(self, request: Request) -> None:
        if not self.enabled:
            return
        key = self._key(request)
        now = time.time()
        rate_per_sec = max(1.0, float(self.rpm)) / 60.0
        b = self._buckets.get(key)
        if b is None:
            b = {"tokens": float(self.burst), "ts": now}
        # Refill
        elapsed = max(0.0, now - float(b.get("ts", now)))
        tokens = min(
            float(b.get("tokens", 0.0)) + elapsed * rate_per_sec, float(self.burst)
        )
        if tokens < 1.0:
            raise HTTPException(status_code=429, detail="rate limit exceeded")
        tokens -= 1.0
        b["tokens"] = tokens
        b["ts"] = now
        self._buckets[key] = b
