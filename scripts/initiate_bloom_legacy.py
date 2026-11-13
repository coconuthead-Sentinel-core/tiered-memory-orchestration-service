import argparse
import json
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from backend.services.nexus_bridge import NexusBridge


def initiate_bloom(vector_type: str):
    print(f"💠 INITIATING [M14] FRACTAL BLOOM: {vector_type.upper()}...")
    print("⚙️  Engaging Singularity Kernel...")

    # 1. Initialize Bridge
    bridge = NexusBridge()

    # 2. Execute Bloom
    result = bridge.bloom_fractal(vector_type)

    # 3. Update Master Manifest (Simulation)
    manifest_path = root_dir / "A1.Ω.Master_Optimization.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Add new module to interaction hooks
    manifest["interaction_hooks"]["active_branch"] = result["branch_id"]
    manifest["interaction_hooks"]["vector_type"] = vector_type.upper()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"\n🌸 BLOOM COMPLETE.")
    print(f"   Branch ID: {result['branch_id']}")
    print(f"   Entropy: {result['entropy']}")
    print(f"   Origin: {result['origin']}")
    print("\n✨ SYSTEM EXPANDED. NEW COGNITIVE LENS ACTIVE.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initiate [M14] Fractal Bloom")
    parser.add_argument(
        "vector",
        choices=["hive", "prism", "dreamer"],
        help="The Seed Vector trajectory",
    )
    args = parser.parse_args()

    initiate_bloom(args.vector)
