import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.domain.models import CognitiveLens, GlyphMatch, SymbolicMetadata
from backend.eventbus import bus
from backend.services.cognitive_orchestrator import CognitiveOrchestrator

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_ai_adapter():
    """Fixture for a mock AI adapter."""
    return AsyncMock()


@pytest.fixture
def mock_glyph_processor():
    """Fixture for a mock GlyphProcessor."""
    processor = MagicMock()
    processor.process_event = MagicMock()
    return processor


@pytest.fixture
def orchestrator(mock_ai_adapter, mock_glyph_processor):
    """Fixture for a CognitiveOrchestrator with a mock glyph processor."""
    return CognitiveOrchestrator(
        ai_adapter=mock_ai_adapter, glyph_processor=mock_glyph_processor
    )


async def test_event_processing_triggers_glyph_processor(
    orchestrator, mock_glyph_processor
):
    """
    Task 4.5 Test: Verify that a raw event published to the bus triggers the
    GlyphProcessor's process_event method.
    """
    # Arrange
    raw_event = {"type": "user_login", "text": "User 'test' logged in successfully."}

    # Start the listener
    orchestrator.start_event_listener()
    await asyncio.sleep(0.01)  # Allow the listener task to start

    # Act
    bus.publish(raw_event, topic="raw_events")
    await asyncio.sleep(0.01)  # Allow the event to be processed

    # Assert
    mock_glyph_processor.process_event.assert_called_once_with(raw_event)

    # Cleanup
    orchestrator.stop_event_listener()


async def test_glyph_match_triggers_reaction(orchestrator, mock_glyph_processor):
    """
    Task 4.5 Test: Verify that when the GlyphProcessor finds a match, the
    _react_to_glyphs method is called.
    """
    # Arrange
    raw_event = {"text": "An ethics violation was detected."}
    glyph_match = GlyphMatch(
        shape="ROOT",
        topic="ethics",
        confidence=0.9,
        matched_seeds=["ethics"],
        applied_rules={},
    )
    symbolic_metadata = SymbolicMetadata(
        matched_glyphs=[glyph_match], dominant_topic="ethics"
    )
    mock_glyph_processor.process_event.return_value = symbolic_metadata

    # Patch the _react_to_glyphs method to monitor its calls
    with patch.object(
        orchestrator, "_react_to_glyphs", new_callable=AsyncMock
    ) as mock_react:
        # Start the listener
        orchestrator.start_event_listener()
        await asyncio.sleep(0.01)

        # Act
        bus.publish(raw_event, topic="raw_events")
        await asyncio.sleep(0.01)

        # Assert
        mock_glyph_processor.process_event.assert_called_once_with(raw_event)
        mock_react.assert_awaited_once_with(symbolic_metadata)

        # Cleanup
        orchestrator.stop_event_listener()


async def test_reaction_logic_triggers_process_message(orchestrator, mock_ai_adapter):
    """
    Task 4.5 Test: Verify that the reaction logic in _react_to_glyphs
    correctly calls process_message with the right parameters.
    """
    # Arrange
    glyph_match = GlyphMatch(
        shape="ROOT",
        topic="ethics",
        confidence=0.9,
        matched_seeds=["ethics"],
        applied_rules={},
    )
    symbolic_metadata = SymbolicMetadata(
        matched_glyphs=[glyph_match], dominant_topic="ethics"
    )

    # Mock the parent process_message to prevent actual AI calls
    with patch.object(
        orchestrator, "process_message", new_callable=AsyncMock
    ) as mock_process_message:
        # Act
        # Directly call the reaction method to isolate the logic
        await orchestrator._react_to_glyphs(symbolic_metadata)
        await asyncio.sleep(0.01)  # Allow the created task to run

        # Assert
        mock_process_message.assert_awaited_once()
        # Check that it was called with the expected lens for the "ethics" topic
        call_args = mock_process_message.call_args
        assert call_args.kwargs["lens"] == CognitiveLens.AUTISM_PRECISION
