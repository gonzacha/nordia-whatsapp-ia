"""
Tests for customer activation flow in app/engine.py

Tests activation flow:
- Happy path (full flow from trigger to confirmation)
- Cancellation at each step
- Validation rules (empty name, short intent, unknown commands)
- Message persistence to database
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import functions to test
from app.engine import handle_message
from app.state import conversaciones, update_conversation, get_conversation
from app.persistence import save_state, save_message_draft
from app.models import SessionLocal, MessageDraft


@pytest.fixture(autouse=True)
def clean_test_state(tmp_path, monkeypatch):
    """
    Clean state before each test and use temp directory for persistence.
    """
    # Clear global conversaciones dict
    conversaciones.clear()

    # Use temp directory for STATE_FILE
    test_state_file = tmp_path / "test_conversations.json"
    monkeypatch.setattr("app.persistence.STATE_FILE", test_state_file)
    monkeypatch.setattr("app.state.save_state", lambda data: save_state(data))

    yield

    # Cleanup after test
    conversaciones.clear()


@patch('app.engine.save_message_draft')
def test_activation_happy_path(mock_save_draft):
    """
    Flujo completo exitoso de activación de cliente
    """
    mock_save_draft.return_value = 1  # Mock draft ID
    sender = "123456789"

    # Step 1: Usuario escribe "activar cliente"
    response1 = handle_message(sender, "activar cliente")
    assert "¿nombre del cliente?" in response1.lower()
    assert get_conversation(sender)["estado"] == "activation_awaiting_name"

    # Step 2: Usuario escribe nombre del cliente
    response2 = handle_message(sender, "Juan")
    assert "perfecto" in response2.lower()
    assert "¿qué te gustaría decirle a juan?" in response2.lower()
    assert get_conversation(sender)["estado"] == "activation_awaiting_intent"
    assert get_conversation(sender)["activation_context"]["customer_name"] == "Juan"

    # Step 3: Usuario escribe intención comercial
    response3 = handle_message(sender, "ofrecer lentes nuevos")
    assert "te sugiero este mensaje" in response3.lower()
    assert "hola juan" in response3.lower()
    assert "enviar" in response3.lower()
    assert "cancelar" in response3.lower()
    assert get_conversation(sender)["estado"] == "activation_showing_draft"

    # Step 4: Usuario confirma con "enviar"
    response4 = handle_message(sender, "enviar")
    assert "listo" in response4.lower()
    assert "mensaje preparado para juan" in response4.lower()
    assert get_conversation(sender)["estado"] == "inicial"

    # Verify save_message_draft was called
    mock_save_draft.assert_called_once()
    call_args = mock_save_draft.call_args[0]
    assert call_args[0] == "Juan"  # customer_name
    assert call_args[1] == "ofrecer lentes nuevos"  # intent
    assert "Hola Juan" in call_args[2]  # generated_message


def test_activation_cancel_at_name():
    """
    Cancelar activación en primer paso (nombre)
    """
    sender = "123456789"

    # Step 1: Activar flujo
    handle_message(sender, "activar cliente")
    assert get_conversation(sender)["estado"] == "activation_awaiting_name"

    # Step 2: Cancelar
    response = handle_message(sender, "cancelar")
    assert "activación cancelada" in response.lower()
    assert get_conversation(sender)["estado"] == "inicial"


def test_activation_cancel_at_intent():
    """
    Cancelar activación en segundo paso (intent)
    """
    sender = "123456789"

    # Step 1: Activar flujo
    handle_message(sender, "activar cliente")

    # Step 2: Proveer nombre
    handle_message(sender, "Juan")
    assert get_conversation(sender)["estado"] == "activation_awaiting_intent"

    # Step 3: Cancelar
    response = handle_message(sender, "cancelar")
    assert "activación cancelada" in response.lower()
    assert get_conversation(sender)["estado"] == "inicial"


def test_activation_cancel_at_draft():
    """
    Cancelar activación en confirmación de draft
    """
    sender = "123456789"

    # Step 1: Activar flujo
    handle_message(sender, "activar cliente")

    # Step 2: Proveer nombre
    handle_message(sender, "Juan")

    # Step 3: Proveer intent
    handle_message(sender, "ofrecer lentes nuevos")
    assert get_conversation(sender)["estado"] == "activation_showing_draft"

    # Step 4: Cancelar
    response = handle_message(sender, "cancelar")
    assert "activación cancelada" in response.lower()
    assert get_conversation(sender)["estado"] == "inicial"


def test_activation_intent_too_short():
    """
    Intent muy corto es rechazado (menos de 3 palabras)
    """
    sender = "123456789"

    # Step 1: Activar flujo
    handle_message(sender, "activar cliente")

    # Step 2: Proveer nombre
    handle_message(sender, "Juan")

    # Step 3: Proveer intent muy corto
    response = handle_message(sender, "hola")
    assert "podrías ser un poco más específico" in response.lower()
    # Debe quedarse en el mismo estado
    assert get_conversation(sender)["estado"] == "activation_awaiting_intent"


def test_activation_unknown_command_at_draft():
    """
    Comando no reconocido en draft repite opciones
    """
    sender = "123456789"

    # Step 1: Activar flujo
    handle_message(sender, "activar cliente")

    # Step 2: Proveer nombre
    handle_message(sender, "Juan")

    # Step 3: Proveer intent
    handle_message(sender, "ofrecer lentes nuevos")

    # Step 4: Comando no reconocido
    response = handle_message(sender, "xyz random")
    assert "no entendí" in response.lower()
    assert "enviar" in response.lower()
    assert "cancelar" in response.lower()
    # Debe quedarse en el mismo estado
    assert get_conversation(sender)["estado"] == "activation_showing_draft"


def test_save_draft_creates_record():
    """
    Guardar draft crea registro en DB y retorna ID válido
    """
    # Save a draft
    draft_id = save_message_draft(
        customer_name="Juan Pérez",
        intent="ofrecer lentes nuevos",
        message="Hola Juan Pérez, llegaron nuevos lentes que te pueden interesar.\n¿Querés que te cuente más?"
    )

    # Verify ID is valid (not -1)
    assert draft_id > 0

    # Verify record exists in database
    db = SessionLocal()
    draft = db.query(MessageDraft).filter(MessageDraft.id == draft_id).first()

    assert draft is not None
    assert draft.customer_name == "Juan Pérez"
    assert draft.commercial_intent == "ofrecer lentes nuevos"
    assert "Hola Juan Pérez" in draft.generated_message
    assert draft.created_at is not None

    db.close()
