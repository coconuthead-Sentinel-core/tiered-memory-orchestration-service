from __future__ import annotations

import logging
import socket
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import httpx

from backend.adapters.azure_openai import (
    AIO_TIMEOUT,
    AzureCognitiveTokenProvider,
    AzureOpenAIAdapter,
)
from backend.core.config import settings
from backend.mock_adapter import MockOpenAIAdapter

logger = logging.getLogger(__name__)


class AIRuntime:
    """Select the active AI adapter and report whether live scoring is verified."""

    def __init__(self) -> None:
        self._adapter: Any = None
        self._http_client: Optional[httpx.AsyncClient] = None
        self._token_provider: Optional[AzureCognitiveTokenProvider] = None
        self._selected_provider = "mock"
        self._auth_method = "mock"
        self._auth_ready: Optional[bool] = False
        self._auth_detail = "Mock mode selected."
        self._endpoint_host = ""
        self._endpoint_dns_resolves: Optional[bool] = None
        self._configure()

    def _configure(self) -> None:
        live_mode_requested = not settings.MOCK_AI

        if not live_mode_requested:
            logger.warning("Running in mock AI mode because MOCK_AI=true.")
            self._adapter = MockOpenAIAdapter()
            self._selected_provider = "mock"
            self._auth_method = "mock"
            self._auth_ready = False
            self._auth_detail = "MOCK_AI=true."
            return

        if not settings.AOAI_ENDPOINT:
            logger.warning("AOAI endpoint missing. Falling back to mock AI mode.")
            self._adapter = MockOpenAIAdapter()
            self._selected_provider = "mock"
            self._auth_method = "mock"
            self._auth_ready = False
            self._auth_detail = (
                "AOAI_ENDPOINT is missing, so live Azure scoring is unavailable."
            )
            return

        self._http_client = httpx.AsyncClient(timeout=AIO_TIMEOUT)
        self._selected_provider = "azure_openai"
        self._endpoint_host = urlparse(settings.AOAI_ENDPOINT).netloc

        if settings.AOAI_KEY:
            self._adapter = AzureOpenAIAdapter(
                self._http_client, api_key=settings.AOAI_KEY
            )
            self._auth_method = "api_key"
            self._auth_ready = None
            self._auth_detail = "Azure OpenAI API key configured. A model request is required to validate the key."
            logger.info("Azure OpenAI adapter configured with API key authentication.")
            return

        self._token_provider = AzureCognitiveTokenProvider()
        self._adapter = AzureOpenAIAdapter(
            self._http_client, token_provider=self._token_provider
        )
        self._auth_method = "aad"
        self._auth_ready = None
        self._auth_detail = "Azure OpenAI AAD mode selected. Run a readiness probe to validate credentials."
        logger.info("Azure OpenAI adapter configured with AAD authentication.")

    @property
    def adapter(self) -> Any:
        return self._adapter

    async def probe(self) -> Dict[str, Any]:
        if self._selected_provider != "azure_openai":
            return self.get_status()

        self._endpoint_dns_resolves = _host_resolves(self._endpoint_host)

        if self._auth_method == "api_key":
            self._auth_ready = None
            self._auth_detail = "Azure OpenAI API key is configured. A successful model request is still required to prove live access."
            return self.get_status()

        if self._token_provider is None:
            self._auth_ready = False
            self._auth_detail = "Azure OpenAI token provider was not initialized."
            return self.get_status()

        try:
            await self._token_provider.get_token()
        except Exception as exc:
            self._auth_ready = False
            self._auth_detail = _summarize_auth_error(exc)
        else:
            self._auth_ready = True
            self._auth_detail = "AAD token acquisition succeeded."

        return self.get_status()

    def get_status(self) -> Dict[str, Any]:
        live_mode_requested = not settings.MOCK_AI
        live_provider_selected = self._selected_provider == "azure_openai"
        verified_live_access = live_provider_selected and self._auth_ready is True
        return {
            "requested_mode": "live" if live_mode_requested else "mock",
            "selected_provider": self._selected_provider,
            "auth_method": self._auth_method,
            "chat_deployment": settings.AOAI_CHAT_DEPLOYMENT,
            "azure_endpoint_configured": bool(settings.AOAI_ENDPOINT),
            "endpoint_host": self._endpoint_host,
            "endpoint_dns_resolves": self._endpoint_dns_resolves,
            "live_mode_requested": live_mode_requested,
            "live_provider_selected": live_provider_selected,
            "verified_live_access": verified_live_access,
            "auth_ready": self._auth_ready,
            "auth_detail": self._auth_detail,
        }

    async def aclose(self) -> None:
        if self._token_provider is not None:
            await self._token_provider.aclose()
        if self._http_client is not None:
            await self._http_client.aclose()


def _summarize_auth_error(exc: Exception) -> str:
    first_line = (
        str(exc).strip().splitlines()[0] if str(exc).strip() else type(exc).__name__
    )
    return first_line


def _host_resolves(host: str) -> bool:
    if not host:
        return False
    try:
        socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    return True


ai_runtime = AIRuntime()
