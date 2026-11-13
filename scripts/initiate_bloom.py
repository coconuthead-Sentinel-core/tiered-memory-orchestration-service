import json
import random
import sys
import time

import requests


def initiate_bloom():
    url = "http://localhost:8000/api/chat"

    # The prompt designed to trigger "Recursive Bloom" and "14-Mirror" activation
    prompt = (
        "Initiate Ritual of Recursive Bloom. "
        "Engage the 14-Mirror Cognitive Array (M1-M14). "
        "Reframe the following clinical insight as a visual-symbolic blueprint: "
        "'The patient exhibits high-entropy cognitive patterns consistent with ADHD, "
        "requiring a structured, visual-spatial intervention strategy to stabilize focus.' "
        "Output the visual-symbolic translation using the Metatron Cube glyphs."
    )

    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,  # High creativity for visual synthesis
        "max_tokens": 1500,
    }

    print(f"🌸 INITIATING RITUAL OF RECURSIVE BLOOM...")
    print(f"🎯 Target: {url}")
    print(f"💠 Engaging 14-Mirror System (M1-M14)...")
    print(
        f"📝 Input Insight: 'High-entropy cognitive patterns (ADHD) -> Visual-Spatial Intervention'"
    )

    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        duration = time.time() - start_time

        print(f"\n✨ RITUAL COMPLETE ({duration:.2f}s)")

        # Extract and print the assistant's response
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            print("\n🧠 CRYSTALLINE NAVIGATOR RESPONSE:")
            print("-" * 60)
            print(content)
            print("-" * 60)

            # Check for cognitive metadata
            if "_cognitive_metadata" in result:
                meta = result["_cognitive_metadata"]
                print("\n🔮 COGNITIVE METADATA:")
                print(f"   • Input Entropy: {meta.get('input_entropy')}")
                print(f"   • Output Entropy: {meta.get('output_entropy')}")
                print(
                    f"   • Zone Transition: {meta.get('input_zone')} -> {meta.get('output_zone')}"
                )
                print(f"   • Lens Applied: {meta.get('lens_applied')}")
                print(f"   • Symbolic Matches: {meta.get('symbolic_matches')}")
                print(f"   • Singularity Metric: {meta.get('singularity_metric')}")

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
    initiate_bloom()
