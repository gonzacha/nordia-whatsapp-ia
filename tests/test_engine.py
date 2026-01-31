"""
Tests for state machine in app/engine.py

Tests conversational flow:
- Initial state (no setup)
- Setup keyword triggers flow
- State transitions (nombre → horarios → servicios → completado)
- Persistence between messages
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

# Import functions to test
from app.engine import handle_message
from app.state import conversaciones, update_conversation, get_conversation, delete_conversation
from app.persistence import save_state, load_state


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


def test_initial_state_returns_welcome():
    """
    Usuario sin estado previo recibe mensaje de bienvenida
    """
    sender = "123456789"
    response = handle_message(sender, "hola")

    assert "Hola" in response
    assert "setup" in response.lower()
    assert get_conversation(sender) == {}  # No state created


def test_setup_keyword_triggers_flow():
    """
    'setup' inicia flujo y cambia estado a esperando_nombre
    """
    sender = "123456789"
    response = handle_message(sender, "setup")

    # Verifica respuesta
    assert "negocio" in response.lower()

    # Verifica estado guardado
    conv = get_conversation(sender)
    assert conv.get("estado") == "esperando_nombre"


def test_setup_keyword_case_insensitive():
    """
    'SETUP', '/setup', etc. también funcionan
    """
    sender = "123456789"

    # Test uppercase
    response = handle_message(sender, "SETUP")
    assert "negocio" in response.lower()

    # Cleanup para próximo test
    delete_conversation(sender)

    # Test con slash
    response = handle_message(sender, "/setup")
    assert "negocio" in response.lower()


def test_nombre_transition():
    """
    Respuesta en esperando_nombre → guarda nombre y pide horarios
    """
    sender = "123456789"

    # Setup inicial
    update_conversation(sender, {"estado": "esperando_nombre"})

    # Usuario responde nombre
    response = handle_message(sender, "Barbería El Corte")

    # Verifica respuesta
    assert "horarios" in response.lower()
    assert "Barbería El Corte" in response or "barbería el corte" in response.lower()

    # Verifica estado
    conv = get_conversation(sender)
    assert conv.get("estado") == "esperando_horarios"
    assert conv.get("nombre") == "Barbería El Corte"


def test_horarios_transition():
    """
    Respuesta en esperando_horarios → guarda horarios y pide servicios
    """
    sender = "123456789"

    # Setup inicial con nombre ya guardado
    update_conversation(sender, {
        "estado": "esperando_horarios",
        "nombre": "Barbería El Corte"
    })

    # Usuario responde horarios
    response = handle_message(sender, "Lun-Vie 9-18hs")

    # Verifica respuesta
    assert "servicios" in response.lower()

    # Verifica estado
    conv = get_conversation(sender)
    assert conv.get("estado") == "esperando_servicios"
    assert conv.get("nombre") == "Barbería El Corte"  # Preserva dato anterior
    assert conv.get("horarios") == "Lun-Vie 9-18hs"


def test_servicios_completes_flow():
    """
    Respuesta en esperando_servicios → marca completado y confirma
    """
    sender = "123456789"

    # Setup inicial con datos previos
    update_conversation(sender, {
        "estado": "esperando_servicios",
        "nombre": "Barbería El Corte",
        "horarios": "Lun-Vie 9-18hs"
    })

    # Usuario responde servicios
    response = handle_message(sender, "Corte, barba, afeitado")

    # Verifica respuesta confirma datos
    assert "Barbería El Corte" in response
    assert "Lun-Vie 9-18hs" in response
    assert "Corte, barba, afeitado" in response
    assert "✅" in response or "Listo" in response

    # Verifica estado completado
    conv = get_conversation(sender)
    assert conv.get("estado") == "completado"
    assert conv.get("nombre") == "Barbería El Corte"
    assert conv.get("horarios") == "Lun-Vie 9-18hs"
    assert conv.get("servicios") == "Corte, barba, afeitado"


def test_full_flow_end_to_end():
    """
    Flujo completo desde setup hasta completado
    """
    sender = "987654321"

    # Paso 1: Setup keyword
    response = handle_message(sender, "setup")
    assert "negocio" in response.lower()
    assert get_conversation(sender).get("estado") == "esperando_nombre"

    # Paso 2: Nombre
    response = handle_message(sender, "Café Molido")
    assert "horarios" in response.lower()
    assert get_conversation(sender).get("estado") == "esperando_horarios"
    assert get_conversation(sender).get("nombre") == "Café Molido"

    # Paso 3: Horarios
    response = handle_message(sender, "7-22hs todos los días")
    assert "servicios" in response.lower()
    assert get_conversation(sender).get("estado") == "esperando_servicios"

    # Paso 4: Servicios
    response = handle_message(sender, "Café, medialunas, desayuno")
    assert "Café Molido" in response
    assert "completado" in get_conversation(sender).get("estado")


def test_state_persists_between_messages():
    """
    Estado se guarda correctamente usando app.state
    """
    sender = "111222333"

    # Mensaje 1: Setup
    handle_message(sender, "setup")
    estado_1 = get_conversation(sender)
    assert estado_1.get("estado") == "esperando_nombre"

    # Mensaje 2: Nombre (simula mensaje nuevo, estado debe persistir)
    handle_message(sender, "Pizzería Napoli")
    estado_2 = get_conversation(sender)
    assert estado_2.get("estado") == "esperando_horarios"
    assert estado_2.get("nombre") == "Pizzería Napoli"

    # Mensaje 3: Horarios
    handle_message(sender, "19-00hs")
    estado_3 = get_conversation(sender)
    assert estado_3.get("estado") == "esperando_servicios"
    assert estado_3.get("nombre") == "Pizzería Napoli"  # Persiste
    assert estado_3.get("horarios") == "19-00hs"


def test_completado_state_response():
    """
    Usuario en estado completado recibe mensaje apropiado
    """
    sender = "444555666"

    # Setup: Usuario ya completó setup
    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Gym Fitness",
        "horarios": "6-22hs",
        "servicios": "Musculación, cardio"
    })

    # Usuario envía mensaje después de completar
    response = handle_message(sender, "hola")

    # Debe indicar que ya completó setup
    assert "completaste" in response.lower() or "listo" in response.lower()
