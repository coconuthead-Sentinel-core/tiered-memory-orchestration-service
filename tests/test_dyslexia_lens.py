import pytest

from backend.services.dyslexia_lens import DyslexiaLens


@pytest.fixture
def lens():
    """Fixture for the DyslexiaLens."""
    return DyslexiaLens()


def test_transform_simple_sentence(lens):
    """Task 5.3 Test: Test a simple sentence is transformed into a spatial map."""
    text = "The system processes data."
    result = lens.transform_context(text)

    assert "--- Spatial Map ---" in result
    assert "[ 🧠 Central Idea ]" in result
    assert "The system processes data." in result
    assert "--- End Map ---" in result
    assert "processes" in result
    assert "system" in result


def test_transform_longer_sentence(lens):
    """Task 5.3 Test: Test that key concepts are extracted from a longer sentence."""
    text = "The quick brown fox jumps over the lazy dog and eats a snack."
    result = lens.transform_context(text)

    assert "[ 🧠 Central Idea ]" in result
    assert "The quick brown fox" in result
    assert "brown" in result
    assert "eats" in result
    assert "jumps" in result
    assert "over" in result


def test_transform_multiple_sentences(lens):
    """Task 5.3 Test: Test that only the first sentence becomes the central idea."""
    text = "First sentence is the main idea. Second sentence provides details. Third sentence adds more."
    result = lens.transform_context(text)

    assert "[ 🧠 Central Idea ]" in result
    assert "First sentence is the main idea." in result
    assert "Second sentence provides details." not in result
    assert "adds" in result
    assert "details" in result
    assert "more" in result
    assert "provides" in result


def test_transform_empty_and_whitespace_context(lens):
    """Task 5.3 Test: Test that empty or whitespace-only context is handled gracefully."""
    assert lens.transform_context("") == ""
    assert lens.transform_context("   \n\t   ") == "   \n\t   "


def test_no_key_concepts_found(lens):
    """Task 5.3 Test: Test that it handles cases with no extractable key concepts."""
    text = "A."
    result = lens.transform_context(text)

    assert "[ 🧠 Central Idea ]" in result
    assert "A." in result
    assert "--- [" not in result
    assert "💡" not in result
