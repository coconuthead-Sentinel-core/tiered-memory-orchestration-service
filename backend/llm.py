import os
from typing import Any, Dict, List, Optional

try:
    # OpenAI SDK v1+
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class LLMError(RuntimeError):
    pass


class LLMClient:
    """Thin wrapper around OpenAI to decouple provider details.

    Reads credentials from env:
      - OPENAI_API_KEY (required)
      - OPENAI_BASE_URL (optional; for Azure/OpenRouter, etc.)
    """

    def __init__(self) -> None:
        if OpenAI is None:
            raise LLMError(
                "OpenAI SDK not installed. Run: pip install -r requirements.txt"
            )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMError("OPENAI_API_KEY not set in environment.")
        base_url = os.getenv("OPENAI_BASE_URL")
        self.client = (
            OpenAI(api_key=api_key, base_url=base_url)
            if base_url
            else OpenAI(api_key=api_key)
        )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.4,
    ) -> Dict[str, Any]:
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        try:
            # Use Chat Completions API for widest compatibility
            resp = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as exc:  # pragma: no cover
            raise LLMError(str(exc))
        msg = resp.choices[0].message
        return {
            "id": resp.id,
            "model": resp.model,
            "role": msg.role,
            "content": msg.content,
            "usage": getattr(resp, "usage", None) and resp.usage.dict(),
        }

    def embeddings(
        self, input: List[str], model: Optional[str] = None
    ) -> Dict[str, Any]:
        model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        try:
            resp = self.client.embeddings.create(model=model, input=input)
        except Exception as exc:  # pragma: no cover
            raise LLMError(str(exc))
        return {"model": resp.model, "vectors": [row.embedding for row in resp.data]}


# Lazy singleton accessor
_singleton: Optional[LLMClient] = None


def get_llm() -> LLMClient:
    global _singleton
    if _singleton is None:
        _singleton = LLMClient()
    return _singleton
