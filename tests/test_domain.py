from datetime import datetime, timezone

import pytest

from backend.domain.models import Entity, MemorySnapshot, Note


def test_entity_defaults():
    """Ensure ID and created_at are auto-generated."""
    e = Entity()
    assert e.id is not None
    assert len(e.id) > 0
    assert e.created_at is not None


def test_note_creation():
    """Test Note creation and field assignments."""
    note = Note(text="Test content", tag="test-tag")
    assert note.text == "Test content"
    assert note.tag == "test-tag"
    assert note.vector is None
    assert note.metadata == {}


def test_note_strict_config():
    """Ensure we cannot pass arbitrary database fields to the domain model."""
    # This should ignore 'partitionKey' because of model_config = ConfigDict(extra="ignore")
    note = Note(text="Test", tag="tag", partitionKey="should_be_ignored")

    # It won't be in the model fields
    assert not hasattr(note, "partitionKey")

    # It won't be in the dump
    data = note.model_dump()
    assert "partitionKey" not in data


def test_memory_snapshot():
    """Test MemorySnapshot structure."""
    snap = MemorySnapshot(
        summary="System stable",
        active_nodes=5,
        entropy_level=0.12,
    )
    assert snap.summary == "System stable"
    assert snap.active_nodes == 5


def test_note_auto_fields_and_aliases():
    note = Note(text="hello lattice", tag="test")
    assert isinstance(note.id, str) and note.id
    assert note.created_at.tzinfo is not None
    dumped = note.model_dump()
    assert dumped["text"] == "hello lattice"
    assert dumped["tag"] == "test"


def test_note_ignores_extra_fields():
    note = Note(text="extra", tag="meta", unexpected="ignored")
    dumped = note.model_dump()
    assert "unexpected" not in dumped


def test_memory_snapshot_auto_fields():
    """Verify MemorySnapshot auto-generates id and created_at fields."""
    snap = MemorySnapshot(summary="state", active_nodes=3, entropy_level=0.12)
    assert isinstance(snap.id, str) and snap.id
    assert snap.created_at.tzinfo is not None
    # Note: timestamp is NOT a field on MemorySnapshot - removed invalid assertion


def test_memory_snapshot_ignores_extra_fields():
    """Verify MemorySnapshot ignores unknown fields (ConfigDict(extra='ignore'))."""
    snap = MemorySnapshot(
        summary="entropy",
        active_nodes=1,
        entropy_level=0.01,
        extraneous="dropme",
        timestamp="also_ignored",  # Not a real field - should be ignored
    )
    dumped = snap.model_dump()
    assert "extraneous" not in dumped
    assert "timestamp" not in dumped
