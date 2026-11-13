#!/usr/bin/env python3
import argparse
import json
import os
import time
from typing import Any, Dict

import requests

API = os.getenv("QNF_API", "http://localhost:8000")
API_KEY = os.getenv("QNF_API_KEY")


def _headers() -> Dict[str, str]:
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h


def status() -> Dict[str, Any]:
    r = requests.get(f"{API}/api/status", headers=_headers(), timeout=10)
    r.raise_for_status()
    return r.json()


def stress(iterations: int, concurrent: bool) -> Dict[str, Any]:
    payload = {"iterations": iterations, "concurrent": concurrent, "async_mode": False}
    r = requests.post(
        f"{API}/api/stress", data=json.dumps(payload), headers=_headers(), timeout=120
    )
    r.raise_for_status()
    return r.json()


def seed_texts() -> None:
    texts = [
        "apex ignite core process launch",
        "flower grid coherence pattern lattice",
        "sphere field boundary rounding dial",
        "status help baseline",
        "quantum cognition load metrics",
    ]
    for t in texts:
        r = requests.post(
            f"{API}/api/cog/process",
            data=json.dumps({"data": t}),
            headers=_headers(),
            timeout=15,
        )
        r.raise_for_status()


def recent_events(limit: int = 20) -> Any:
    r = requests.get(
        f"{API}/api/events/history?limit={limit}", headers=_headers(), timeout=10
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser(description="QNF demo loader")
    ap.add_argument("--stress", type=int, default=0, help="Run stress iterations")
    ap.add_argument("--concurrent", action="store_true", help="Run stress concurrently")
    ap.add_argument("--seed-only", action="store_true", help="Only send seed texts")
    args = ap.parse_args()

    print("[load] checking status...")
    print(status())

    print("[load] sending seed texts...")
    seed_texts()

    if args.seed_only:
        print("[load] seeds done.")
        return

    if args.stress > 0:
        print(
            f"[load] running stress: iterations={args.stress} concurrent={args.concurrent}"
        )
        res = stress(args.stress, args.concurrent)
        print(json.dumps(res, indent=2))

    print("[load] pulling recent events...")
    time.sleep(1)
    ev = recent_events()
    print(json.dumps(ev, indent=2))


if __name__ == "__main__":
    main()
