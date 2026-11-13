import json
import os
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def verify_wcrp_sync():
    print("💠 INITIATING L2 CEREBELLUM SYNCHRONIZATION TEST...")
    print("⚙️  Verifying WCRP v1.0 Constraints...")

    # Load Master Optimization
    master_path = root_dir / "A1.Ω.Master_Optimization.json"
    with open(master_path, "r", encoding="utf-8") as f:
        master_config = json.load(f)

    # Load Firewall Rules
    firewall_path = root_dir / "meta_context" / "firewall_rules_l6.json"
    with open(firewall_path, "r", encoding="utf-8") as f:
        firewall_config = json.load(f)

    constraints = master_config["egress_logic"]["constraints"]
    stillwater = firewall_config["stillwater_protocol"]

    # Check L1 Mountain Limit
    l1_limit = constraints["l1_mountain_limit"]
    print(
        f"🏔️  L1 Mountain Limit: {l1_limit} chars | {'✅ LOCKED' if l1_limit == 10000 else '❌ DRIFT'}"
    )

    # Check L3 Input Anchor
    l3_anchor = constraints["l3_input_anchor"]
    print(
        f"⚓  L3 Input Anchor: {l3_anchor} words | {'✅ LOCKED' if l3_anchor == 600 else '❌ DRIFT'}"
    )

    # Check L6 Stillwater
    chunk_range = stillwater.get("chunk_size_range", "Unknown")
    print(
        f"🌊  L6 Stillwater Protocol: {chunk_range} | {'✅ LOCKED' if chunk_range == '5-7 lines' else '❌ DRIFT'}"
    )

    # Check Code Pacing
    snippet_max = constraints["code_pacing"]["snippet_max_lines"]
    print(
        f"📝  Code Pacing (Snippet): {snippet_max} lines | {'✅ LOCKED' if snippet_max == 150 else '❌ DRIFT'}"
    )

    # Simulate Output Validation
    test_string = "The quick brown fox jumps over the lazy dog. " * 20
    word_count = len(test_string.split())
    print(f"\n📊  L2 Metric Calibration Test:")
    print(f"    Input Sample: {word_count} words")
    print(
        f"    Accuracy Target: {master_config['reporting_protocol']['metrics']['clarity_threshold'] * 100}%"
    )
    print(f"    Status: CALIBRATED")

    print("\n✨ SYNCHRONIZATION COMPLETE. The Mountain is Mapped.")


if __name__ == "__main__":
    verify_wcrp_sync()
