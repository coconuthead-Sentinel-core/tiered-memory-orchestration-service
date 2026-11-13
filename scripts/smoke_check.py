"""
Lightweight smoke test for the FastAPI app.

Usage:
    python scripts/smoke_check.py http://localhost:8000/api
"""

import sys
import time

import httpx


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/smoke_check.py <base_url>")
        return 1

    base = sys.argv[1].rstrip("/")
    endpoints = [
        "/metrics/prom",
        "/sync/snapshot",
        "/notes",
        "/dashboard/metrics",
        "/dashboard/activity",
        "/dashboard/sentinel",
    ]

    ok = True
    with httpx.Client(timeout=10.0) as client:
        for path in endpoints:
            url = f"{base}{path}"
            try:
                start = time.time()
                res = client.get(url)
                elapsed = (time.time() - start) * 1000
                status = res.status_code
                if status >= 400:
                    ok = False
                preview = res.text[:200].replace("\n", "\\n")
                print(f"{status:3d} {elapsed:7.1f}ms {url} -> {preview}")
            except Exception as exc:
                ok = False
                print(f"ERR   ------ {url} -> {exc}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
