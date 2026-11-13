import json
import os
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def verify_wcrp_calibration():
    print("💠 INITIATING WCRP RE-CALIBRATION...")
    print("⚙️  Checking Word Count Constraints...")

    master_path = root_dir / "A1.Ω.Master_Optimization.json"
    with open(master_path, "r", encoding="utf-8") as f:
        master_config = json.load(f)

    metrics = master_config["reporting_protocol"]["metrics"]
    max_count = metrics.get("max_word_count", 0)

    print(
        f"📏 Max Word Count: {max_count} | {'✅ LOCKED' if max_count == 450 else '❌ DRIFT'}"
    )

    if max_count == 450:
        print("\n✨ CALIBRATION COMPLETE. The Mountain is Respected.")
    else:
        print("\n❌ CALIBRATION FAILED. Adjusting...")


if __name__ == "__main__":
    verify_wcrp_calibration()
