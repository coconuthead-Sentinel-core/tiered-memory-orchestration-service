import asyncio
import random
import sys
import time
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from backend.services.nexus_bridge import NexusBridge


async def run_load_test():
    print("💠 INITIATING TRINITY CONSENSUS LOAD TEST...")
    print("⚙️  Simulating High-Volume Query Traffic...")

    bridge = NexusBridge()

    # Simulate 50 concurrent requests
    tasks = []
    print("\n🚀 LAUNCHING 50 CONCURRENT VECTORS...")

    start_time = time.time()

    for i in range(50):
        # Generate random vectors
        # Most should be high clarity (low variance) to simulate stable system
        # Some outliers to test drift detection
        if random.random() > 0.1:
            # Stable vector
            base = random.random()
            vector = [base, base + 0.01, base - 0.01]
        else:
            # Drifting vector
            vector = [0.1, 0.9, 0.5]

        tasks.append(bridge.verify_trinity_consensus(vector))

    results = await asyncio.gather(*tasks)
    end_time = time.time()

    # Analyze Results
    locked = 0
    drifting = 0

    print("\n📊 ANALYZING CONSENSUS METRICS...")
    for i, res in enumerate(results):
        status = "✅ LOCKED" if res["consensus_reached"] else "❌ DRIFTING"
        if res["consensus_reached"]:
            locked += 1
        else:
            drifting += 1

        # Print sample of results
        if i % 10 == 0:
            print(f"   Query {i:02d}: Clarity {res['clarity_score']:.4f} | {status}")

    duration = end_time - start_time
    tps = 50 / duration

    print(f"\n⏱️  Execution Time: {duration:.4f}s")
    print(f"⚡ Throughput: {tps:.2f} TPS")
    print(f"🔒 Triangulation Lock Rate: {(locked/50)*100:.1f}%")

    if locked >= 45:  # 90% success rate target
        print("\n✅ TRINITY CONSENSUS STABLE UNDER LOAD.")
        print("   The L2 Cerebellum is holding the line.")
    else:
        print("\n⚠️  WARNING: CONSENSUS DRIFT DETECTED.")


if __name__ == "__main__":
    asyncio.run(run_load_test())
