"""Tests for ADHD Burst Lens - Cognitive Processing Validation.

Validates:
1. ADHD lens chunking and bullet formatting
2. Action word enhancement
3. Integration with CognitiveOrchestrator
4. Edge cases and error handling
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.domain.models import CognitiveLens
from backend.services.adhd_lens import (
    ADHDLens,
    create_adhd_lens,
    transform_with_adhd_lens,
)
from backend.services.cognitive_orchestrator import CognitiveOrchestrator


def test_adhd_lens_initialization():
    lens = ADHDLens()
    assert lens.chunk_size == 50
    assert len(lens.BULLET_MARKERS) > 0
    assert "start" in lens.ACTION_WORDS


def test_adhd_lens_empty_context():
    lens = ADHDLens()
    result = lens.transform_context("")
    assert result == ""

    result = lens.transform_context("   ")
    assert result == "   "


def test_adhd_lens_simple_chunking():
    lens = ADHDLens()
    short_text = "This is a short message."
    result = lens.transform_context(short_text)
    assert "⚡" in result
    assert result.count("⚡") == 1


def test_adhd_lens_long_text_chunking():
    lens = ADHDLens()
    long_text = "This is the first sentence. " * 20
    result = lens.transform_context(long_text)
    bullet_count = result.count("⚡") + result.count("💥") + result.count("🚀")
    assert bullet_count > 1


def test_adhd_lens_action_word_enhancement():
    lens = ADHDLens()
    text = "You should start the process now."
    result = lens.transform_context(text)
    assert "**START**" in result


def test_adhd_lens_response_transformation():
    lens = ADHDLens()
    response = "Here is my response to your query."
    assert lens.transform_context(response) == lens.transform_response(response)


def test_adhd_lens_sentence_splitting():
    lens = ADHDLens()
    text = "First sentence. Second sentence! Third sentence?"
    sentences = lens._split_into_sentences(text)
    assert len(sentences) == 3
    assert "First sentence" in sentences[0]
    assert "Second sentence" in sentences[1]
    assert "Third sentence" in sentences[2]


def test_adhd_lens_chunk_creation():
    lens = ADHDLens()
    sentences = ["Short sentence."] * 10
    chunks = lens._create_chunks(sentences)
    assert len(chunks) > 1
    assert len(chunks) < len(sentences)


def test_adhd_lens_bullet_formatting():
    lens = ADHDLens()
    chunks = ["First chunk of text", "Second chunk of text"]
    bullets = lens._format_as_bullets(chunks)
    assert len(bullets) == 2
    assert bullets[0].startswith("⚡")
    assert bullets[1].startswith("💥")
    assert "First chunk" in bullets[0]
    assert "Second chunk" in bullets[1]


def test_adhd_lens_config():
    lens = ADHDLens()
    config = lens.get_config()
    assert "chunk_size_words" in config
    assert "bullet_markers" in config
    assert "action_words" in config


def test_create_adhd_lens():
    lens = create_adhd_lens()
    assert isinstance(lens, ADHDLens)


def test_transform_with_adhd_lens():
    text = "Transform this text."
    result = transform_with_adhd_lens(text)
    assert "⚡" in result
    assert "Transform this text" in result


@pytest.mark.asyncio
async def test_adhd_lens_integration():
    mock_adapter = MagicMock()
    mock_adapter.chat = AsyncMock(
        return_value={
            "id": "test-123",
            "choices": [
                {"message": {"content": "This is a test response from the AI."}}
            ],
        }
    )

    orchestrator = CognitiveOrchestrator(
        mock_adapter,
        default_lens=CognitiveLens.ADHD_BURST,
    )

    result = await orchestrator.process_message(
        "Please explain how this works.",
        lens=CognitiveLens.ADHD_BURST,
    )

    assert "_cognitive_metadata" in result
    assert result["_cognitive_metadata"]["lens_applied"] == "adhd"
    mock_adapter.chat.assert_called_once()


def test_adhd_lens_orchestrator_metadata():
    lens = ADHDLens()
    text = "This is a test message with start action."
    result = lens.transform_context(text)
    assert any(marker in result for marker in ["⚡", "💥", "🚀", "🔥"])
    assert "**START**" in result or "**ACTION**" in result


def test_adhd_lens_very_long_sentence():
    lens = ADHDLens()
    long_sentence = "This is a very long sentence " * 20
    result = lens.transform_context(long_sentence)
    assert "⚡" in result


def test_adhd_lens_special_characters():
    lens = ADHDLens()
    text = "Test with special chars: @#$%^&*()! And numbers: 12345."
    result = lens.transform_context(text)
    assert isinstance(result, str)
    assert len(result) > 0


def test_adhd_lens_unicode_content():
    lens = ADHDLens()
    text = "Unicode test: 🌟 ⭐ 📚 🎯"
    result = lens.transform_context(text)
    assert "🌟" in result
    assert "🎯" in result
