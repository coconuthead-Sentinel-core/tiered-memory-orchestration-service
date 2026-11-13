import random
import uuid
from typing import Any, Dict, List


class MockOpenAIAdapter:
    """
    Simulates Azure OpenAI responses for development without API keys.
    """

    def __init__(self, http_client=None, token_provider=None):
        pass

    async def chat(
        self, deployment: str, messages: List[Dict[str, str]], **kwargs
    ) -> Dict[str, Any]:
        """Returns a simulated chat completion."""
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), "..."
        )

        # varied responses to make it feel alive
        if "DREAMER" in last_user_msg:
            content = (
                "🌌 [M14-DREAMER] Visualizing Cognitive Load as a 4D Weather System...\n\n"
                "1. **The Storm Front (Red Zone):** High cognitive load manifests as swirling thunderclouds. "
                "Heavy rain indicates 'Information Overload'.\n"
                "2. **The Clear Sky (Green Zone):** Low load is a serene, starlit void. "
                "Shooting stars represent 'Flow State' insights.\n"
                "3. **The Fog (Yellow Zone):** Ambiguity appears as a shifting mist. "
                "Requires 'Lighthouse' glyphs to navigate.\n\n"
                "✨ *Concept generated via Metatron's Cube lattice.*"
            )
        else:
            responses = [
                f"[MOCK] I received your data: '{last_user_msg[:20]}...'. Processing complete.",
                f"[MOCK] The Sentinel system is online. Simulated response to: '{last_user_msg[:20]}...'",
                f"[MOCK] Analysis: Nominal. Input '{last_user_msg[:20]}...' recorded in memory lattice.",
                f"[MOCK] Shannon Prime acknowledges your query: '{last_user_msg[:20]}...'",
            ]
            content = random.choice(responses)

        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "created": 1677652288,
            "model": "mock-gpt-4",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        }

    async def embeddings(
        self, deployment: str, inputs: List[str], dimensions: int = 1536
    ) -> Dict[str, Any]:
        """Returns random vectors to simulate embeddings."""
        if isinstance(inputs, str):
            inputs = [inputs]

        data = []
        for i, _ in enumerate(inputs):
            # Generate a random normalized vector
            vec = [random.random() for _ in range(dimensions)]
            data.append({"object": "embedding", "index": i, "embedding": vec})

        return {
            "object": "list",
            "data": data,
            "model": "mock-embedding-ada-002",
            "usage": {"prompt_tokens": 5, "total_tokens": 5},
        }
