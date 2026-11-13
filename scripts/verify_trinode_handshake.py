import logging
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.validation_loop import validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trinode_verifier")


def verify_handshake():
    print("🤝 INITIATING TRINODE CONSENSUS HANDSHAKE...")
    print("=" * 50)

    test_content = "System initialization sequence complete. All systems nominal."

    print(f"📝 Input Content: '{test_content}'")
    print("🔄 Requesting consensus from Trinode Cluster (Claude, Gemini, ChatGPT)...")

    result = validator.validate_output(test_content)

    print("-" * 50)
    print(f"📊 Consensus Reached: {result['consensus']}")
    print(f"🎯 Average Clarity Score: {result['average_clarity']}")
    print(f"⚖️  Status: {result['status']}")
    print("-" * 50)

    print("🔍 Node Scores:")
    for node, score in result["scores"].items():
        status_icon = "✅" if score >= validator.TARGET_CLARITY else "❌"
        print(f"   {status_icon} {node}: {score}")

    print("=" * 50)

    if result["consensus"]:
        print("✅ HANDSHAKE SUCCESSFUL: VR Studios Environment Synchronized.")
    else:
        print("❌ HANDSHAKE FAILED: Consensus not reached.")


if __name__ == "__main__":
    verify_handshake()
