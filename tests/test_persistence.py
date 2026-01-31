"""
Tests for conversation state persistence.

Following TDD approach: tests written before implementation.
"""

import json
import pytest
from pathlib import Path
from app.persistence import save_state, load_state, STATE_FILE


@pytest.fixture
def clean_state():
    """Fixture to ensure clean state before each test."""
    # Remove state file if exists
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    yield
    # Cleanup after test
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def test_save_and_load_state(clean_state):
    """Test 1: Happy path - save and load state successfully."""
    # Setup
    state = {
        "123456789": {
            "estado": "esperando_nombre",
            "nombre": "Barbería Los Andes"
        }
    }

    # Save
    save_state(state)

    # Verify file exists
    assert STATE_FILE.exists()

    # Load
    loaded = load_state()

    # Assert
    assert loaded == state
    assert loaded["123456789"]["estado"] == "esperando_nombre"
    assert loaded["123456789"]["nombre"] == "Barbería Los Andes"


def test_load_state_when_no_file(clean_state):
    """Test 2: Load state when file doesn't exist (first run)."""
    # Ensure file doesn't exist
    assert not STATE_FILE.exists()

    # Load
    loaded = load_state()

    # Assert returns empty dict
    assert loaded == {}
    assert isinstance(loaded, dict)


def test_load_state_corrupted_json(clean_state):
    """Test 3: Load state when JSON is corrupted."""
    # Setup: write invalid JSON
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text("{invalid json content", encoding='utf-8')

    # Load (should not crash)
    loaded = load_state()

    # Assert returns empty dict on error
    assert loaded == {}


def test_multiple_conversations(clean_state):
    """Test 4: Save and load multiple conversations."""
    # Setup
    state = {
        "111": {"estado": "esperando_nombre"},
        "222": {"estado": "completado", "nombre": "Peluquería X"},
        "333": {"estado": "esperando_horarios", "nombre": "Barbería Y"}
    }

    # Save
    save_state(state)

    # Load
    loaded = load_state()

    # Assert
    assert len(loaded) == 3
    assert loaded["222"]["nombre"] == "Peluquería X"
    assert loaded["333"]["estado"] == "esperando_horarios"


def test_save_state_creates_directory(clean_state):
    """Test 5: save_state creates data/ directory if it doesn't exist."""
    # This test validates that save_state can create directory if needed
    # Note: In real scenario, data/ might already exist from other files

    # Just verify that if we save, directory exists
    state = {"test": {"estado": "test"}}
    save_state(state)

    # Assert directory and file created
    assert STATE_FILE.parent.exists()
    assert STATE_FILE.exists()


def test_save_state_with_unicode(clean_state):
    """Test 6: Save state with unicode/emoji characters."""
    # Setup
    state = {
        "123": {
            "estado": "esperando_nombre",
            "mensaje": "Hola 👋 ¿Cómo se llama tu negocio?"
        }
    }

    # Save
    save_state(state)

    # Load
    loaded = load_state()

    # Assert unicode preserved
    assert loaded["123"]["mensaje"] == "Hola 👋 ¿Cómo se llama tu negocio?"


def test_save_state_empty_dict(clean_state):
    """Test 7: Save empty state (edge case)."""
    # Save empty dict
    save_state({})

    # Load
    loaded = load_state()

    # Assert
    assert loaded == {}


def test_save_state_handles_datetime_serialization(clean_state):
    """Test 8: save_state handles datetime objects (using default=str)."""
    from datetime import datetime

    # Setup with datetime (will be converted to string)
    state = {
        "123": {
            "estado": "esperando_nombre",
            "timestamp": datetime.now()
        }
    }

    # Save (should not crash)
    save_state(state)

    # Load
    loaded = load_state()

    # Assert saved successfully (timestamp converted to string)
    assert "123" in loaded
    assert loaded["123"]["estado"] == "esperando_nombre"
    # Timestamp will be string after JSON serialization
    assert isinstance(loaded["123"]["timestamp"], str)
