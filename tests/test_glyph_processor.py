"""Tests for Glyph Processor - Symbolic Pattern Recognition.

Validates:
1. Glyph loading from JSON
2. Fuzzy pattern matching algorithms
3. Symbolic metadata generation
4. Confidence scoring and rule application
"""

import json
import tempfile
from pathlib import Path

import pytest

from backend.services.glyph_processor import (
    GlyphProcessor,
    SymbolicMetadata,
    get_glyph_processor,
)

# --- Test Data ---

SAMPLE_GLYPHS = {
    "shapes": {
        "TEST_INIT": {
            "topic": "initiation",
            "seeds": ["start", "begin", "initiate", "launch"],
            "rules": {"start": "tag:init.begin"},
        },
        "TEST_PROCESS": {
            "topic": "process",
            "seeds": ["process", "handle", "execute", "run"],
            "rules": {"process": "tag:process.core"},
        },
        "TEST_END": {
            "topic": "completion",
            "seeds": ["finish", "complete", "end", "done"],
            "rules": {"complete": "tag:completion.done"},
        },
    }
}


# --- Glyph Loading Tests ---


def test_glyph_processor_initialization():
    """Test GlyphProcessor initializes with default or custom path."""
    processor = GlyphProcessor()
    assert len(processor.glyphs) > 0  # Should load sample glyphs
    assert "APEX" in processor.glyphs  # From sample data


def test_glyph_processor_custom_path():
    """Test loading glyphs from custom JSON file."""
    # Create temporary JSON file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GLYPHS, f)
        temp_path = f.name

    try:
        processor = GlyphProcessor(temp_path)
        assert len(processor.glyphs) == 3
        assert "TEST_INIT" in processor.glyphs
        assert "TEST_PROCESS" in processor.glyphs
        assert "TEST_END" in processor.glyphs
    finally:
        Path(temp_path).unlink()


def test_glyph_processor_missing_file():
    """Test graceful handling of missing glyph file."""
    processor = GlyphProcessor("/nonexistent/path/glyphs.json")
    # Should create sample glyphs
    assert len(processor.glyphs) > 0
    assert "APEX" in processor.glyphs


def test_get_available_shapes():
    """Test retrieving list of available glyph shapes."""
    processor = GlyphProcessor()
    shapes = processor.get_available_shapes()
    assert isinstance(shapes, list)
    assert len(shapes) > 0
    assert "APEX" in shapes


def test_get_shape_info():
    """Test retrieving information about specific glyph shapes."""
    processor = GlyphProcessor()
    apex_info = processor.get_shape_info("APEX")
    assert apex_info is not None
    assert apex_info["topic"] == "initiation"
    assert "apex" in apex_info["seeds"]

    nonexistent = processor.get_shape_info("NONEXISTENT")
    assert nonexistent is None


# --- Pattern Matching Tests ---


def test_process_text_empty():
    """Test processing empty or whitespace-only text."""
    processor = GlyphProcessor()
    result = processor.process_text("")
    assert isinstance(result, SymbolicMetadata)
    assert len(result.matched_glyphs) == 0
    assert result.dominant_topic is None
    assert len(result.symbolic_tags) == 0


def test_process_text_no_matches():
    """Test processing text with no glyph matches."""
    processor = GlyphProcessor()
    result = processor.process_text("This text has no matching patterns whatsoever")
    assert len(result.matched_glyphs) == 0


def test_process_text_exact_match():
    """Test processing text with exact glyph seed matches."""
    # Create processor with test glyphs
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GLYPHS, f)
        temp_path = f.name

    try:
        processor = GlyphProcessor(temp_path)

        # Test exact match
        result = processor.process_text("Let's start the process now")
        assert (
            len(result.matched_glyphs) == 2
        )  # Should match TEST_INIT and TEST_PROCESS

        # Check first match (TEST_INIT)
        init_match = next(
            (m for m in result.matched_glyphs if m.shape == "TEST_INIT"), None
        )
        assert init_match is not None
        assert init_match.topic == "initiation"
        assert "start" in init_match.matched_seeds
        assert init_match.confidence == 1.0  # Exact match
        assert "tag:init.begin" in init_match.applied_rules.values()

        # Check second match (TEST_PROCESS)
        process_match = next(
            (m for m in result.matched_glyphs if m.shape == "TEST_PROCESS"), None
        )
        assert process_match is not None
        assert process_match.topic == "process"
        assert "process" in process_match.matched_seeds

        # Check metadata
        assert result.dominant_topic == "initiation"  # First match
        assert "tag:init.begin" in result.symbolic_tags
        assert "tag:process.core" in result.symbolic_tags

    finally:
        Path(temp_path).unlink()


def test_process_text_partial_match():
    """Test processing text with partial substring matches."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GLYPHS, f)
        temp_path = f.name

    try:
        processor = GlyphProcessor(temp_path)

        # Test partial match (word contains seed)
        result = processor.process_text("We need to initialize the system")
        assert len(result.matched_glyphs) == 1

        match = result.matched_glyphs[0]
        assert match.shape == "TEST_INIT"
        assert "initiate" in match.matched_seeds  # Partial match
        assert match.confidence == 0.7  # Partial match confidence

    finally:
        Path(temp_path).unlink()


def test_process_text_multiple_matches():
    """Test processing text that matches multiple seeds in one glyph."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GLYPHS, f)
        temp_path = f.name

    try:
        processor = GlyphProcessor(temp_path)

        # Text with multiple seeds from same glyph
        result = processor.process_text("begin the process and execute the plan")
        assert len(result.matched_glyphs) >= 1

        # Find TEST_PROCESS match
        process_match = next(
            (m for m in result.matched_glyphs if m.shape == "TEST_PROCESS"), None
        )
        assert process_match is not None
        assert (
            len(process_match.matched_seeds) >= 2
        )  # Should match "process" and "execute"
        assert process_match.confidence < 1.0  # Average of multiple matches

    finally:
        Path(temp_path).unlink()


def test_process_text_confidence_calculation():
    """Test confidence score calculation for matches."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GLYPHS, f)
        temp_path = f.name

    try:
        processor = GlyphProcessor(temp_path)

        # Single exact match
        result = processor.process_text("start")
        assert len(result.matched_glyphs) == 1
        assert result.matched_glyphs[0].confidence == 1.0

        # Single partial match
        result = processor.process_text("starting")
        assert len(result.matched_glyphs) == 1
        assert result.matched_glyphs[0].confidence == 0.7

        # Multiple matches (mixed exact/partial)
        result = processor.process_text("start the process")
        init_match = next(
            (m for m in result.matched_glyphs if m.shape == "TEST_INIT"), None
        )
        process_match = next(
            (m for m in result.matched_glyphs if m.shape == "TEST_PROCESS"), None
        )

        assert init_match.confidence == 1.0  # Exact "start"
        assert process_match.confidence == 1.0  # Exact "process"

    finally:
        Path(temp_path).unlink()


# --- Singleton Tests ---


def test_get_glyph_processor_singleton():
    """Test that get_glyph_processor returns singleton instance."""
    processor1 = get_glyph_processor()
    processor2 = get_glyph_processor()
    assert processor1 is processor2


def test_reload_glyphs():
    """Test reloading glyphs from file."""
    processor = GlyphProcessor()

    # Modify glyphs in memory
    original_count = len(processor.glyphs)
    processor.glyphs["TEST_NEW"] = {"topic": "test", "seeds": ["test"], "rules": {}}

    assert len(processor.glyphs) == original_count + 1

    # Reload should restore original
    processor.reload_glyphs()
    assert len(processor.glyphs) == original_count
    assert "TEST_NEW" not in processor.glyphs


# --- Integration Tests ---


def test_glyph_processor_with_real_sample():
    """Test glyph processor with the actual sample glyphs file."""
    # This test uses the real sample file in the data directory
    processor = GlyphProcessor()

    # Test with text that should match APEX patterns
    result = processor.process_text("Let's ignite the AI inference query")
    assert len(result.matched_glyphs) >= 1

    apex_match = next((m for m in result.matched_glyphs if m.shape == "APEX"), None)
    if apex_match:
        assert apex_match.topic == "initiation"
        assert any(
            seed in ["ignite", "ai_infer", "query"] for seed in apex_match.matched_seeds
        )
