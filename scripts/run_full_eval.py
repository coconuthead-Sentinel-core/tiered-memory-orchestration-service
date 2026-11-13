import os
import socket
import subprocess
import sys
import time
from pathlib import Path

# --- Unicode Patch for Windows Consoles ---
# Ensures emojis (🚀, ✅, etc.) don't crash the script on legacy terminals.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        # Fallback for older Python versions or environments
        pass


def wait_for_port(port, timeout=30):
    """Wait until the port is open."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(("127.0.0.1", port))
            if result == 0:
                return True
        time.sleep(1)
    return False


def main():
    # Ensure we are in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🚀 Starting Sentinel Forge Evaluation Pipeline...")
    print("=" * 60)

    # 1. Use TestClient for in-process testing
    print("\n[1/3] Using TestClient for in-process testing...")
    print("      ✅ TestClient ready (no server needed)")

    try:
        # 2. Run the Collection Script (now uses TestClient)
        print("\n[2/3] Collecting Responses...")
        collect_result = subprocess.run(
            [sys.executable, "evaluation/collect_responses.py"], capture_output=False
        )

        if collect_result.returncode != 0:
            print("❌ Collection failed.")
            return
        else:
            # 3. Run the Evaluation Script
            print("\n[3/3] Running Evaluation...")
            eval_result = subprocess.run(
                [sys.executable, "evaluation/run_evaluation.py"], capture_output=False
            )
            if eval_result.returncode != 0:
                print("❌ Evaluation failed.")
            else:
                print("✅ Pipeline Complete.")

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")


if __name__ == "__main__":
    main()
