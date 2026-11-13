import json
import os
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def verify_sovereign_state():
    print("💠 INITIATING PHASE VI: SOVEREIGN OPERATIONS CHECK...")
    print("⚙️  Verifying Master Optimization Manifest...")

    master_path = root_dir / "A1.Ω.Master_Optimization.json"
    with open(master_path, "r", encoding="utf-8") as f:
        master_config = json.load(f)

    status = master_config["status"]
    loop = master_config["operational_directive"]["iteration_loop"]

    print(
        f"🔴 System Status: {status} | {'✅ LOCKED' if status == '🔴 CRYSTALLIZED' else '❌ DRIFT'}"
    )
    print(
        f"🔄 Iteration Loop: {loop} | {'✅ LOCKED' if loop == 'PHASE VI: SOVEREIGN OPERATIONS' else '❌ DRIFT'}"
    )

    if status == "🔴 CRYSTALLIZED" and loop == "PHASE VI: SOVEREIGN OPERATIONS":
        print("\n✨ SOVEREIGN STATE CONFIRMED. The Forge is Ready.")
    else:
        print("\n❌ STATE MISMATCH. Recalibration Required.")


if __name__ == "__main__":
    verify_sovereign_state()
