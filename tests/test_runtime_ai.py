import asyncio

from backend.core.config import settings
from backend.runtime_ai import AIRuntime


def _close_runtime(runtime: AIRuntime) -> None:
    asyncio.run(runtime.aclose())


def test_runtime_uses_mock_when_mock_mode_is_enabled(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_AI", True, raising=False)
    monkeypatch.setattr(
        settings, "AOAI_ENDPOINT", "https://example.openai.azure.com", raising=False
    )
    monkeypatch.setattr(settings, "AOAI_KEY", "", raising=False)

    runtime = AIRuntime()
    try:
        status = runtime.get_status()
        assert status["selected_provider"] == "mock"
        assert status["live_mode_requested"] is False
        assert status["verified_live_access"] is False
    finally:
        _close_runtime(runtime)


def test_runtime_falls_back_to_mock_when_live_endpoint_is_missing(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_AI", False, raising=False)
    monkeypatch.setattr(settings, "AOAI_ENDPOINT", "", raising=False)
    monkeypatch.setattr(settings, "AOAI_KEY", "", raising=False)

    runtime = AIRuntime()
    try:
        status = runtime.get_status()
        assert status["selected_provider"] == "mock"
        assert status["live_mode_requested"] is True
        assert status["verified_live_access"] is False
        assert "AOAI_ENDPOINT" in status["auth_detail"]
    finally:
        _close_runtime(runtime)


def test_runtime_selects_azure_when_api_key_is_configured(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_AI", False, raising=False)
    monkeypatch.setattr(
        settings, "AOAI_ENDPOINT", "https://example.openai.azure.com", raising=False
    )
    monkeypatch.setattr(settings, "AOAI_KEY", "test-key", raising=False)

    runtime = AIRuntime()
    try:
        status = runtime.get_status()
        assert status["selected_provider"] == "azure_openai"
        assert status["auth_method"] == "api_key"
        assert status["live_provider_selected"] is True
        assert status["verified_live_access"] is False
    finally:
        _close_runtime(runtime)
