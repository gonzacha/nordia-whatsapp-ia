"""Tests for customer handlers."""

import pytest

from app.customer_handlers import handle_customer_message
from app.state import conversaciones, get_conversation, update_conversation
from app.persistence import save_state


@pytest.fixture(autouse=True)
def clean_test_state(tmp_path, monkeypatch):
    """
    Clean state before each test and use temp directory for persistence.
    """
    conversaciones.clear()

    test_state_file = tmp_path / "test_conversations.json"
    monkeypatch.setattr("app.persistence.STATE_FILE", test_state_file)
    monkeypatch.setattr("app.state.save_state", lambda data: save_state(data))

    yield

    conversaciones.clear()


def test_customer_greeting_returns_hello():
    sender = "123456789"
    conv = get_conversation(sender)
    response = handle_customer_message(sender, "hola", conv)
    assert "hola" in response.lower()


def test_customer_services_returns_list_when_present():
    sender = "123456789"
    update_conversation(sender, {"estado": "completado", "servicios": "Corte $10"})
    conv = get_conversation(sender)
    response = handle_customer_message(sender, "precio", conv)
    assert "nuestros servicios son" in response.lower()
    assert "corte $10" in response.lower()


def test_customer_appointment_updates_state():
    sender = "123456789"
    conv = get_conversation(sender)
    response = handle_customer_message(sender, "quiero un turno", conv)
    assert "perfecto" in response.lower()
    assert get_conversation(sender)["estado"] == "esperando_fecha_turno"
