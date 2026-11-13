import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

import httpx
from azure.identity.aio import DefaultAzureCredential

from backend.core.config import settings

AIO_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
RETRIES = 2  # simple linear retry on 5xx/429


@dataclass
class CachedToken:
    token: str
    expires_at: float  # epoch seconds


class AzureCognitiveTokenProvider:
    """
    Uses AAD to obtain tokens for Azure OpenAI (Cognitive Services scope).
    Caches token until a safety window before expiry to avoid mid-request failures.
    """

    _scope = "https://cognitiveservices.azure.com/.default"
    _skew_seconds = 60

    def __init__(self) -> None:
        self._cred = DefaultAzureCredential()
        self._lock = asyncio.Lock()
        self._cache: Optional[CachedToken] = None

    async def get_token(self) -> str:
        now = time.time()
        if self._cache and now < (self._cache.expires_at - self._skew_seconds):
            return self._cache.token
        async with self._lock:
            # Double-check after acquiring the lock
            now = time.time()
            if self._cache and now < (self._cache.expires_at - self._skew_seconds):
                return self._cache.token
            tok = await self._cred.get_token(self._scope)
            self._cache = CachedToken(token=tok.token, expires_at=now + tok.expires_in)
            return self._cache.token

    async def aclose(self) -> None:
        await self._cred.close()


class AzureOpenAIAdapter:
    """
    Minimal Azure OpenAI adapter with Azure AD or API key authentication.
    """

    def __init__(
        self,
        http: httpx.AsyncClient,
        token_provider: Optional[AzureCognitiveTokenProvider] = None,
        api_key: str = "",
    ):
        self._http = http
        self._token_provider = token_provider
        self._api_key = api_key.strip()
        self._base = str(settings.AOAI_ENDPOINT)

    async def _headers(self) -> Dict[str, str]:
        if self._api_key:
            return {
                "api-key": self._api_key,
                "Content-Type": "application/json",
            }
        if self._token_provider is None:
            raise RuntimeError(
                "Azure OpenAI adapter is missing both API key and token provider."
            )
        token = await self._token_provider.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def _request_with_retries(
        self,
        method: str,
        url: str,
        json: Dict[str, Any],
        params: Dict[str, Any],
    ) -> httpx.Response:
        last_exc: Optional[Exception] = None
        for attempt in range(RETRIES + 1):
            try:
                resp = await self._http.request(
                    method, url, headers=await self._headers(), json=json, params=params
                )
                if resp.status_code in (429, 500, 502, 503, 504):
                    # Retry on transient server/backpressure conditions
                    await asyncio.sleep(0.5 * (attempt + 1))
                else:
                    return resp
            except (httpx.ConnectError, httpx.ReadTimeout) as exc:
                last_exc = exc
                await asyncio.sleep(0.5 * (attempt + 1))
        if last_exc:
            raise last_exc
        raise httpx.HTTPStatusError("Azure OpenAI request failed after retries", request=None, response=resp)  # type: ignore

    async def chat(
        self,
        deployment: str,
        messages: Sequence[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,  # ignored; deployment selects model
    ) -> Dict[str, Any]:
        url = f"{self._base}/openai/deployments/{deployment}/chat/completions"
        params = {"api-version": settings.AOAI_API_VERSION}
        body: Dict[str, Any] = {"messages": list(messages)}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_completion_tokens"] = (
                max_tokens  # required for o4-mini, GPT-5 models
            )
        if tools:
            body["tools"] = tools
        if tool_choice:
            body["tool_choice"] = tool_choice
        if response_format:
            body["response_format"] = response_format
        resp = await self._request_with_retries("POST", url, json=body, params=params)
        await _raise_if_azure_error(resp)
        return resp.json()

    async def embeddings(
        self,
        deployment: str,
        inputs: Union[str, List[str]],
        dimensions: Optional[int] = None,
    ) -> Dict[str, Any]:
        url = f"{self._base}/openai/deployments/{deployment}/embeddings"
        params = {"api-version": settings.AOAI_API_VERSION}
        body: Dict[str, Any] = {"input": inputs}
        if dimensions is not None:
            body["dimensions"] = dimensions
        resp = await self._request_with_retries("POST", url, json=body, params=params)
        await _raise_if_azure_error(resp)
        return resp.json()


async def _raise_if_azure_error(resp: httpx.Response) -> None:
    if 200 <= resp.status_code < 300:
        return
    # Azure returns structured error bodies; surface concise detail.
    try:
        data = resp.json()
        msg = data.get("error", {}).get("message") or data
    except Exception:
        msg = resp.text
    raise httpx.HTTPStatusError(
        f"Azure OpenAI error {resp.status_code}: {msg}",
        request=resp.request,
        response=resp,
    )
