"""
AUTONOMOUS FIX: backend/api.py Syntax Error Repair
Quantum Nexus Forge - Neurodivergent-Optimized Workflow

SAFETY FEATURES:
- Creates backup before modification (.backup extension)
- Validates Python syntax after fix
- Rollback capability if validation fails
- Detailed logging of all changes
"""

import ast
import shutil
from pathlib import Path


def fix_api_file():
    """Fix syntax errors in backend/api.py with full safety checks."""

    # Paths
    project_root = Path(__file__).parent.parent
    api_file = project_root / "backend" / "api.py"
    backup_file = api_file.with_suffix(".py.backup")

    print("🛠️  Quantum Nexus Forge - Auto-Repair Tool")
    print("=" * 60)

    # Step 1: Create backup
    print(f"\n📦 Creating backup: {backup_file.name}")
    shutil.copy2(api_file, backup_file)
    print("   ✅ Backup created successfully")

    # Step 2: Read current content
    print(f"\n📖 Reading {api_file.name}...")
    with open(api_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 3: Apply fixes
    print("\n🔧 Applying fixes...")
    fixes_applied = []

    # Fix 1: Replace REM with # on line 1
    if content.startswith("REM filepath:"):
        content = content.replace("REM filepath:", "# filepath:", 1)
        fixes_applied.append("✓ Changed 'REM' to '#' on line 1")

    # Fix 2: Add missing imports
    import_section = """from typing import Any
import logging

from fastapi import APIRouter, HTTPException, Depends, Body, Response, status, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse
import json"""

    if "from fastapi import APIRouter, HTTPException\n" in content:
        # Replace incomplete import with full import
        content = content.replace(
            "from fastapi import APIRouter, HTTPException\n",
            "from fastapi import APIRouter, HTTPException, Depends, Body, Response, status, Request\n",
        )
        fixes_applied.append("✓ Added missing FastAPI imports")

    if "import logging" not in content[:500]:  # Check first 500 chars
        # Add logging import after typing
        content = content.replace(
            "from typing import Any\n", "from typing import Any\nimport logging\n"
        )
        fixes_applied.append("✓ Added logging import")

    # Step 4: Write fixed content
    print("\n💾 Writing fixes to file...")
    with open(api_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Step 5: Validate Python syntax
    print("\n✅ Validating Python syntax...")
    try:
        ast.parse(content)
        print("   ✅ Syntax validation PASSED")
    except SyntaxError as e:
        print(f"   ❌ Syntax validation FAILED: {e}")
        print("\n🔄 Rolling back changes...")
        shutil.copy2(backup_file, api_file)
        print("   ✅ Rollback complete - original file restored")
        return False

    # Step 6: Summary
    print("\n" + "=" * 60)
    print("✅ REPAIR COMPLETE")
    print("\nFixes applied:")
    for fix in fixes_applied:
        print(f"  {fix}")
    print(f"\n📦 Backup saved: {backup_file}")
    print("\n🚀 Next step: Start server with 'uvicorn main:app --reload'")
    return True


if __name__ == "__main__":
    success = fix_api_file()
    exit(0 if success else 1)
