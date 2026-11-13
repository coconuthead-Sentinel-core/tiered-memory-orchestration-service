"""Chat service skeleton for handling chat interactions.

Persists user prompts as Notes via the Cosmos repository and delegates
response generation to the configured adapter (mock or Azure OpenAI).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from backend.domain.models import Note
from backend.infrastructure.cosmos_repo import cosmos_repo

logger = logging.getLogger(__name__)

try:  # Prefer Azure adapter if available/configured
    from backend.adapters.azure_openai import AzureOpenAIAdapter  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    AzureOpenAIAdapter = None  # type: ignore

try:
    from backend.mock_adapter import MockOpenAIAdapter  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    MockOpenAIAdapter = None  # type: ignore


class ChatService:
    """
    Orchestrates the Cognitive Chat Pipeline:
    1. Input Analysis
    2. Context Retrieval (Memory)
    3. AI Processing (Generation)
    4. Memory Consolidation (Storage)
    """

    def __init__(self, ai_adapter):
        self.ai_adapter = ai_adapter

    async def process_message(
        self, user_message: str, context: str = ""
    ) -> Dict[str, Any]:
        """
        Process a user message through the Sentinel pipeline.
        """
        # 1. Log Input (Short-term memory)
        # In a real system, we might save the user prompt immediately.

        # 2. AI Generation
        # Construct messages payload
        messages = [
            {"role": "system", "content": context or "You are Sentinel Forge."},
            {"role": "user", "content": user_message},
        ]

        try:
            # Call AI Adapter (Mock or Azure)
            response = await self.ai_adapter.chat(
                deployment="gpt-4",  # Config driven in real impl
                messages=messages,
                temperature=0.7,
            )
            # response = {
            #     "id": "test-id",
            #     "model": "test-model",
            #     "created": 1234567890,
            #     "choices": [{
            #         "index": 0,
            #         "message": {
            #             "role": "assistant",
            #             "content": f"Test response to: {user_message}"
            #         },
            #         "finish_reason": "stop"
            #     }],
            #     "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
            # }

            # Extract content safely
            choices = response.get("choices", [])
            if choices:
                ai_text = choices[0].get("message", {}).get("content", "")
            else:
                ai_text = ""

            # 3. Memory Consolidation (Save interaction)
            # We save the interaction as a Note in the Lattice
            if ai_text:
                note = Note(
                    text=f"User: {user_message}\nSentinel: {ai_text}",
                    tag="chat-history",
                    metadata={"type": "conversation"},
                )
                await cosmos_repo.upsert_note(note)

            return response

        except Exception as e:
            logger.error(f"Chat Pipeline Error: {e}")
            raise
