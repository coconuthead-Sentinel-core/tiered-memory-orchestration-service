"""Sentinel Forge pre-flight check.

Validates environment keys and basic reachability for Azure OpenAI and Cosmos DB
before launching the main server.
"""

from __future__ import annotations

import os
import socket
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import requests
except ImportError:  # pragma: no cover
    print("[FAIL] requests is not installed. Run: python -m pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    print("[WARN] python-dotenv not installed; continuing without .env auto-load.")

    def load_dotenv(path: str) -> None:  # type: ignore
        return None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
REQUIRED_VARS = [
    "API_KEY",
    "AOAI_ENDPOINT",
    "AOAI_CHAT_DEPLOYMENT",
    "AOAI_EMBED_DEPLOYMENT",
    "COSMOS_ENDPOINT",
    "COSMOS_KEY",
]


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def ok(msg: str) -> None:
    print(f"[PASS] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def check_tcp(host: str, port: int, timeout: float = 3.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            return sock.connect_ex((host, port)) == 0
        except OSError:
            return False


def http_ping(
    url: str, headers: Optional[Dict[str, str]] = None, verify: bool = True
) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        resp = requests.get(url, headers=headers, timeout=5, verify=verify)
        return True, resp.status_code, resp.reason
    except requests.RequestException as exc:
        return False, None, str(exc)


def load_env() -> None:
    if ENV_PATH.exists():
        load_dotenv(str(ENV_PATH))
        ok(f"Loaded environment from {ENV_PATH}")
    else:
        warn(f".env not found at {ENV_PATH}; relying on current environment")


def require_env() -> bool:
    missing: list[str] = []
    for var in REQUIRED_VARS:
        val = os.getenv(var, "").strip()
        if not val or "replace-with" in val:
            missing.append(var)
            fail(f"Environment variable {var} is missing or placeholder")
        else:
            ok(f"{var} present")
    if missing:
        fail("Critical environment values missing; update .env before launch")
    return not missing


def check_aoai() -> bool:
    endpoint = os.getenv("AOAI_ENDPOINT", "").rstrip("/")
    api_version = os.getenv("AOAI_API_VERSION", "2024-08-01-preview")
    api_key = os.getenv("API_KEY", "")
    if not endpoint:
        fail("AOAI_ENDPOINT not set")
        return False
    url = f"{endpoint}/openai/deployments?api-version={api_version}"
    headers = {"api-key": api_key} if api_key else None
    reachable, status, reason = http_ping(url, headers=headers)
    if reachable:
        ok(f"Azure OpenAI endpoint reachable (status {status or '?'} {reason or ''})")
        return True
    fail(f"Azure OpenAI endpoint not reachable: {reason or 'no response'}")
    return False


def check_cosmos() -> bool:
    endpoint = os.getenv("COSMOS_ENDPOINT", "").strip()
    key_present = bool(os.getenv("COSMOS_KEY", "").strip())
    if not endpoint:
        fail("COSMOS_ENDPOINT not set")
        return False
    if not key_present:
        fail("COSMOS_KEY not set")
        return False

    # For localhost emulator, probe TCP 8081; otherwise try HTTP ping.
    if "localhost" in endpoint or "127.0.0.1" in endpoint:
        port = 8081
        host = "127.0.0.1"
        reachable = check_tcp(host, port)
        if reachable:
            ok(f"Cosmos Emulator reachable on {host}:{port}")
        else:
            fail(f"Cosmos Emulator not reachable on {host}:{port}")
        return reachable

    # Remote Cosmos: attempt HTTPS request (401/403 counts as reachable).
    reachable, status, reason = http_ping(endpoint, verify=False)
    if reachable:
        ok(f"Cosmos endpoint reachable (status {status or '?'} {reason or ''})")
        return True
    fail(f"Cosmos endpoint not reachable: {reason or 'no response'}")
    return False


def main() -> int:
    info("Sentinel Forge pre-flight check starting...")
    load_env()

    env_ok = require_env()
    aoai_ok = check_aoai()
    cosmos_ok = check_cosmos()

    if env_ok and aoai_ok and cosmos_ok:
        ok("Pre-flight complete. Ready to launch server.")
        return 0
    fail("Pre-flight failed. Resolve issues above before launching the server.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
