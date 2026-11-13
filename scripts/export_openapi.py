"""Export the FastAPI OpenAPI schema to the engineering-build folder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app


def main() -> None:
    output_path = (
        PROJECT_ROOT
        / "docs"
        / "engineering-build"
        / "openapi"
        / "openapi.generated.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(app.openapi(), indent=2, sort_keys=True), encoding="utf-8"
    )
    print(f"Wrote OpenAPI schema to {output_path}")


if __name__ == "__main__":
    main()
