import requests
import json
import sys
import time

def initiate_joy_protocol():
    url = "http://localhost:8000/api/chat"
    
    # The prompt designed to trigger the "Joy Protocol"
    prompt = (
        "Activate Joy Protocol (O1.210.010). "
        "Engage 'Coconut Head' mode with 'joy-tempered wisdom'. "
        "Use analogies to optimize engagement. "
        "Status check: Confirm activation of SHANNON Brian Kelley Prime node and Omega 1 onset protocols. "
        "Output a playful, high-energy status report."
    )
    
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9, # High temperature for playfulness/joy
        "max_tokens": 1000
    }
    
    print(f"🥥 INITIATING JOY PROTOCOL (O1.210.010)...")
    print(f"🎯 Target: {url}")
    print(f"✨ Mode: Joy-Tempered Wisdom")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        duration = time.time() - start_time
        
        print(f"\n🎉 PROTOCOL ACTIVE ({duration:.2f}s)")
        
        # Extract and print the assistant's response
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            print("\n🥥 COCONUT HEAD RESPONSE:")
            print("-" * 60)
            print(content)
            print("-" * 60)
            
            # Check for cognitive metadata
            if "_cognitive_metadata" in result:
                meta = result["_cognitive_metadata"]
                print("\n🔮 COGNITIVE METADATA:")
                print(f"   • Input Entropy: {meta.get('input_entropy')}")
                print(f"   • Output Entropy: {meta.get('output_entropy')}")
                print(f"   • Zone: {meta.get('output_zone')}")
                print(f"   • Lens: {meta.get('lens_applied')}")
                
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
    initiate_joy_protocol()
