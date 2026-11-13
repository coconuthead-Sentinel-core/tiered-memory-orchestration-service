import json

import pytest
from fastapi.testclient import TestClient

from backend.eventbus import bus
from backend.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_ws_cognitive_endpoint():
    """
    Tests the /ws/cognitive endpoint for receiving initial state and subsequent events.
    """
    # Use TestClient's WebSocket context manager
    with client.websocket_connect("/ws/cognitive?api_key=secret") as websocket:
        # 1. Receive initial state
        initial_data = websocket.receive_json()
        assert initial_data["type"] == "cognitive.state"
        assert "zone_metrics" in initial_data["data"]

        # 2. Publish a 'cognitive' event and verify it's received
        cognitive_event = {"type": "test.cognitive.event", "data": "cognitive_payload"}
        bus.publish(cognitive_event, topic="cognitive")

        received_data = websocket.receive_json()
        assert received_data == cognitive_event

        # 3. Publish a 'symbolic' event and verify it's received
        symbolic_event = {"type": "test.symbolic.event", "data": "symbolic_payload"}
        bus.publish(symbolic_event, topic="symbolic")

        received_data = websocket.receive_json()
        assert received_data == symbolic_event

        # 4. Publish a 'glyph' event and verify it's received
        glyph_event = {"type": "test.glyph.event", "data": "glyph_payload"}
        bus.publish(glyph_event, topic="glyph")

        received_data = websocket.receive_json()
        assert received_data == glyph_event


@pytest.mark.asyncio
async def test_ws_metrics_endpoint():
    """
    Tests the /ws/metrics endpoint for event-driven metric updates.
    """
    with client.websocket_connect("/ws/metrics?api_key=secret") as websocket:
        # 1. Receive initial metrics state
        initial_data = websocket.receive_json()
        assert initial_data["type"] == "metrics.initial_state"
        assert isinstance(initial_data["data"], dict)

        # 2. Publish a relevant 'zone.classified' event and verify it's received
        classified_event = {
            "type": "zone.classified",
            "data": {"zone": "active", "entropy": 0.8},
        }
        bus.publish(classified_event, topic="cognitive")

        received_data = websocket.receive_json()
        assert received_data == classified_event

        # 3. Publish a relevant 'zone.transition' event and verify it's received
        transition_event = {
            "type": "zone.transition",
            "data": {"note_id": "123", "from": "active", "to": "pattern"},
        }
        bus.publish(transition_event, topic="cognitive")

        received_data = websocket.receive_json()
        assert received_data == transition_event

        # 4. Publish an irrelevant event, then a relevant one, and ensure the filter skips the irrelevant payload
        irrelevant_event = {"type": "some.other.event", "data": "should_be_ignored"}
        bus.publish(irrelevant_event, topic="cognitive")
        followup_event = {
            "type": "zone.classified",
            "data": {"zone": "pattern", "entropy": 0.5},
        }
        bus.publish(followup_event, topic="cognitive")
        received_data = websocket.receive_json()
        assert received_data == followup_event


# To run these tests, use:
# pytest tests/test_websockets.py
