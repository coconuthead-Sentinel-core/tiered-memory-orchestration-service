from fastapi.testclient import TestClient  # type: ignore[reportMissingImports]

from backend.eventbus import bus
from backend.main import app


def test_ws_sync_receives_published_events(monkeypatch):
    client = TestClient(app)
    # Ensure no API key is required for this test
    monkeypatch.delenv("QNF_API_KEY", raising=False)
    monkeypatch.setenv("QNF_REQUIRE_API_KEY", "0")
    with client.websocket_connect("/ws/sync") as ws:
        # Publish an event and expect to receive it
        payload = {"type": "test.event", "data": {"hello": "world"}}
        bus.publish(payload)
        msg = ws.receive_text()
        assert "test.event" in msg
