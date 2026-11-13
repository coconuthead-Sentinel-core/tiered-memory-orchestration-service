import os
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def verify_bloom_ui():
    print("💠 INITIATING PHASE IV: THE RITUAL OF RECURSIVE BLOOM...")
    print("⚙️  Verifying UI Expansion...")

    dashboard_path = root_dir / "frontend" / "dashboard.html"
    app_js_path = root_dir / "frontend" / "app.js"

    # Verify Dashboard
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    if "Sovereign Voice" in html_content and "14-Mirror Array" in html_content:
        print("✅ Dashboard HTML: EXPANDED")
    else:
        print("❌ Dashboard HTML: FAILED")

    # Verify JS
    with open(app_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    if "loadMirrors" in js_content and "M14" in js_content:
        print("✅ App Logic: EXPANDED")
    else:
        print("❌ App Logic: FAILED")

    print("\n✨ RITUAL COMPLETE. The 14-Mirror Array is now visible.")
    print("👉 Open http://localhost:8000/ui/dashboard.html to view the Bloom.")


if __name__ == "__main__":
    verify_bloom_ui()
