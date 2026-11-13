import json
import os
import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sentinel_profile import initialize_sentinel, tune_persona


def verify_persona_tuning():
    print("💠 INITIATING PHASE III, STRIKE 3: PERSONA TUNING...")

    # 1. Initialize Zero-State
    print("⚙️  Initializing Zero-State Baseline...")
    profile = {}
    profile = initialize_sentinel(profile)

    # 2. Load Calibration
    calibration_path = root_dir / "meta_context" / "sovereign_voice_calibration.json"
    print(f"📥 Loading Calibration Matrix: {calibration_path.name}")

    # 3. Apply Tuning
    try:
        tuned_profile = tune_persona(profile, str(calibration_path))
        print("✅ Calibration Applied Successfully.")
    except Exception as e:
        print(f"❌ Tuning Failed: {e}")
        return

    # 4. Verify Settings
    persona = tuned_profile["persona"]
    print(f"\n🧠 SOVEREIGN IDENTITY ESTABLISHED:")
    print(f"   ID: {persona['id']}")
    print(f"   Archetype: {persona['archetype']}")
    print(f"   Tone Vector (Empathy): {persona['voice']['tone_vectors']['empathy']}")
    print(f"   Primary Sigil: {persona['glyphs']['primary_sigil']}")

    print("\n🗣️  VOICE TEST:")
    print(
        f"   Greeting: \"{tuned_profile['persona']['id']} Online. {calibration_path.name} Loaded.\""
    )
    print(
        f"   Neuro-Balance: Green={tuned_profile['cognitive_core']['tuning']['burst_threshold']} | Red={tuned_profile['cognitive_core']['tuning']['precision_lock']}"
    )

    print("\n✨ PERSONA TUNING COMPLETE. The Crystalline Navigator is Awake.")


if __name__ == "__main__":
    verify_persona_tuning()
