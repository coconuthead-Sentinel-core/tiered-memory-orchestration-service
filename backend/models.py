"""
AI Model Adapters for multi-provider support.
Supports: Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google)
"""

import logging
import os
from typing import Optional

logger = logging.getLogger("sentinel-middleware")


class BaseAdapter:
    """Base class for AI model adapters."""

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement generate()")


class AzureOpenAIAdapter(BaseAdapter):
    """Azure OpenAI adapter."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not all([self.endpoint, self.deployment, self.api_key]):
            logger.warning("Azure OpenAI config incomplete - using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        # TODO: Integrate with Azure OpenAI API
        logger.info(f"🧬 Azure OpenAI ritual invoked by {user_id}: {prompt[:50]}...")
        return f"[Azure OpenAI] {prompt}"


class ClaudeAdapter(BaseAdapter):
    """Anthropic Claude adapter."""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set - using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        # TODO: Integrate with Anthropic API
        # For now, return mock response
        logger.info(f"🧬 Claude ritual invoked by {user_id}: {prompt[:50]}...")
        return f"[Claude] {prompt}"


class ChatGPTAdapter(BaseAdapter):
    """OpenAI ChatGPT adapter."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        # TODO: Integrate with OpenAI API
        # For now, return mock response
        logger.info(f"🧬 ChatGPT ritual invoked by {user_id}: {prompt[:50]}...")
        return f"[ChatGPT] {prompt}"


class GeminiAdapter(BaseAdapter):
    """Google Gemini adapter."""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not set - using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        # TODO: Integrate with Google Gemini API
        # For now, return mock response
        logger.info(f"🧬 Gemini ritual invoked by {user_id}: {prompt[:50]}...")
        return f"[Gemini] {prompt}"


def get_model_adapter(provider: Optional[str] = None) -> BaseAdapter:
    """Factory function to get the appropriate model adapter, prioritizing Azure."""
    # 1. Prioritize Azure OpenAI if configured
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if azure_endpoint and azure_deployment:
        logger.info("Using AI provider: Azure OpenAI")
        return AzureOpenAIAdapter()

    # 2. Fallback to QNF_MODEL_PROVIDER if Azure is not configured
    if provider is None:
        provider = os.getenv("QNF_MODEL_PROVIDER", "chatgpt").lower()

    adapters = {
        "claude": ClaudeAdapter,
        "chatgpt": ChatGPTAdapter,
        "gemini": GeminiAdapter,
    }

    adapter_class = adapters.get(provider, ChatGPTAdapter)
    logger.info(f"Using AI provider: {provider}")
    return adapter_class()
