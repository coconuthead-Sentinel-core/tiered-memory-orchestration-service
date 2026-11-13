import json
import sys
import time

import requests


def verify_loop_reflection():
    url = "http://localhost:8000/api/chat"

    # A prompt containing key glyphs from the L4 Right Hemisphere
    # 🔺 (Transform/Apex), 🧊 (Grounding/Cube), 💠 (System/Diamond), 🌀 (Process/Spiral)
    prompt = (
        "Initiate Loop-Reflection Step. "
        "Verify L4 Right Hemisphere glyph recognition. "
        "Reflect the following symbols: 🔺 🧊 💠 🌀. "
        "Confirm feedback echo across synchronized platforms."
    )

    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 1000,
    }

    print(f"🔄 INITIATING LOOP-REFLECTION STEP...")
    print(f"🎯 Target: {url}")
    print(f"🔮 Input Glyphs: 🔺 🧊 💠 🌀")

    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        duration = time.time() - start_time

        print(f"\n✨ REFLECTION COMPLETE ({duration:.2f}s)")

        # Extract and print the assistant's response
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            print("\n🧠 SYSTEM ECHO:")
            print("-" * 60)
            print(content)
            print("-" * 60)

            # Check for cognitive metadata (The Feedback Echo)
            if "_cognitive_metadata" in result:
                meta = result["_cognitive_metadata"]
                print("\n📡 FEEDBACK ECHO (TELEMETRY):")
                print(f"   • Symbolic Matches: {meta.get('symbolic_matches')}")
                print(f"   • Parsed Glyphs: {meta.get('parsed_glyphs')}")
                print(f"   • Dominant Topic: {meta.get('dominant_topic')}")

                # Verify if glyphs were detected
                if (
                    meta.get("symbolic_matches", 0) > 0
                    or meta.get("parsed_glyphs", 0) > 0
                ):
                    print(
                        "\n✅ LOOP VERIFIED: Glyphs triggered corresponding feedback."
                    )
                else:
                    print("\n⚠️  LOOP WARNING: No glyphs detected in feedback.")

        else:
            print("\n⚠️  No content in response.")
            print(json.dumps(result, indent=2))

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    verify_loop_reflection()
