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

    # Usuario responde servicios (con precios para pasar validación)
    response = handle_message(sender, "Corte $8000, barba $5000, afeitado $3000")

    # Verifica respuesta confirma datos
    assert "Barbería El Corte" in response
    assert "Lun-Vie 9-18hs" in response
    assert "Corte $8000, barba $5000, afeitado $3000" in response
    assert "✅" in response or "Listo" in response

    # Verifica estado completado
    conv = get_conversation(sender)
    assert conv.get("estado") == "completado"
    assert conv.get("nombre") == "Barbería El Corte"
    assert conv.get("horarios") == "Lun-Vie 9-18hs"
    assert conv.get("servicios") == "Corte $8000, barba $5000, afeitado $3000"


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

    # Paso 4: Servicios (con precios para pasar validación)
    response = handle_message(sender, "Café $1500, medialunas $800, desayuno $2500")
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

    # Usuario envía mensaje después de completar (sin keywords)
    response = handle_message(sender, "hola")

    # Debe recibir fallback message guiando a consultar servicios
    assert "servicios" in response.lower()
    assert "precios" in response.lower()


# ==================== VALIDATION INTEGRATION TESTS ====================

def test_nombre_invalid_too_short_stays_in_state():
    """
    Invalid nombre (too short) should NOT advance state, should re-ask.
    """
    sender = "777888999"

    # Setup: Start flow
    handle_message(sender, "setup")
    assert get_conversation(sender).get("estado") == "esperando_nombre"

    # Send invalid nombre (too short)
    response = handle_message(sender, "ab")

    # Should NOT advance to esperando_horarios
    assert get_conversation(sender).get("estado") == "esperando_nombre"

    # Should return error message
    assert "❌" in response
    assert "3 caracteres" in response
    assert "negocio" in response.lower()  # Re-ask question

    # Should NOT have saved invalid nombre
    assert "nombre" not in get_conversation(sender)


def test_nombre_invalid_only_numbers_returns_error():
    """
    Invalid nombre (only numbers) should return specific error.
    """
    sender = "888999000"

    # Setup: Start flow
    handle_message(sender, "setup")

    # Send invalid nombre (only numbers)
    response = handle_message(sender, "12345")

    # Should stay in esperando_nombre
    assert get_conversation(sender).get("estado") == "esperando_nombre"

    # Should return error about only numbers
    assert "❌" in response
    assert "solo números" in response.lower()


def test_horarios_invalid_no_numbers_stays_in_state():
    """
    Invalid horarios (no numbers) should NOT advance state.
    """
    sender = "111000111"

    # Setup: Valid nombre first
    update_conversation(sender, {
        "estado": "esperando_horarios",
        "nombre": "Test Business"
    })

    # Send invalid horarios (no numbers)
    response = handle_message(sender, "todo el día")

    # Should NOT advance to esperando_servicios
    assert get_conversation(sender).get("estado") == "esperando_horarios"

    # Should return error message
    assert "❌" in response
    assert "números" in response.lower()
    assert "horarios" in response.lower()  # Re-ask question

    # Should NOT have saved invalid horarios
    assert "horarios" not in get_conversation(sender)


def test_horarios_invalid_no_letters_stays_in_state():
    """
    Invalid horarios (no letters) should NOT advance state.
    """
    sender = "222000222"

    # Setup: Valid nombre first
    update_conversation(sender, {
        "estado": "esperando_horarios",
        "nombre": "Test Business"
    })

    # Send invalid horarios (no letters)
    response = handle_message(sender, "9-18")

    # Should NOT advance to esperando_servicios
    assert get_conversation(sender).get("estado") == "esperando_horarios"

    # Should return error message
    assert "❌" in response
    assert "letras" in response.lower()


def test_servicios_invalid_too_short_returns_error():
    """
    Invalid servicios (too short) should NOT complete setup.
    """
    sender = "333000333"

    # Setup: Valid nombre and horarios
    update_conversation(sender, {
        "estado": "esperando_servicios",
        "nombre": "Test Business",
        "horarios": "9-18hs"
    })

    # Send invalid servicios (too short)
    response = handle_message(sender, "ab")

    # Should NOT advance to completado
    assert get_conversation(sender).get("estado") == "esperando_servicios"

    # Should return error message
    assert "❌" in response
    assert "3 caracteres" in response
    assert "servicios" in response.lower()  # Re-ask question

    # Should NOT have saved invalid servicios
    assert "servicios" not in get_conversation(sender)


def test_servicios_invalid_no_prices_stays_in_state():
    """
    Invalid servicios (no numbers/prices) should NOT complete setup.
    """
    sender = "444000444"

    # Setup: Valid nombre and horarios
    update_conversation(sender, {
        "estado": "esperando_servicios",
        "nombre": "Test Business",
        "horarios": "9-18hs"
    })

    # Send invalid servicios (no prices)
    response = handle_message(sender, "corte y barba")

    # Should NOT advance to completado
    assert get_conversation(sender).get("estado") == "esperando_servicios"

    # Should return error message
    assert "❌" in response
    assert "precios" in response.lower()


def test_validation_flow_with_corrections():
    """
    User can correct invalid input and continue flow.
    """
    sender = "555000555"

    # Step 1: Setup
    handle_message(sender, "setup")

    # Step 2: Try invalid nombre → rejected
    response = handle_message(sender, "ab")
    assert get_conversation(sender).get("estado") == "esperando_nombre"
    assert "❌" in response

    # Step 3: Send valid nombre → accepted
    response = handle_message(sender, "Barbería OK")
    assert get_conversation(sender).get("estado") == "esperando_horarios"
    assert "horarios" in response.lower()

    # Step 4: Try invalid horarios → rejected
    response = handle_message(sender, "xx")
    assert get_conversation(sender).get("estado") == "esperando_horarios"
    assert "❌" in response

    # Step 5: Send valid horarios → accepted
    response = handle_message(sender, "9-18hs")
    assert get_conversation(sender).get("estado") == "esperando_servicios"

    # Step 6: Try invalid servicios → rejected
    response = handle_message(sender, "x")
    assert get_conversation(sender).get("estado") == "esperando_servicios"
    assert "❌" in response

    # Step 7: Send valid servicios → complete
    response = handle_message(sender, "Corte $5000")
    assert get_conversation(sender).get("estado") == "completado"
    assert "✅" in response


# ==================== SERVICE QUERY TESTS ====================

def test_normalize_text_removes_accents():
    """normalize_text should remove accents and convert to lowercase."""
    from app.engine import normalize_text

    assert normalize_text("CUÁNTO") == "cuanto"
    assert normalize_text("Precio") == "precio"
    assert normalize_text("Servicios") == "servicios"
    assert normalize_text("¿Cuánto cuesta?") == "¿cuanto cuesta?"


def test_normalize_text_handles_special_chars():
    """normalize_text should preserve special characters except accents."""
    from app.engine import normalize_text

    assert normalize_text("Café $500") == "cafe $500"
    assert normalize_text("¿PRECIOS?") == "¿precios?"


def test_contains_service_query_keyword_detects_keywords():
    """Should detect service query keywords case-insensitively."""
    from app.engine import contains_service_query_keyword

    assert contains_service_query_keyword("cuanto cuesta?")
    assert contains_service_query_keyword("PRECIO")
    assert contains_service_query_keyword("servicios")
    assert contains_service_query_keyword("Cuánto sale?")
    assert contains_service_query_keyword("lista de precios por favor")
    assert contains_service_query_keyword("cuestan mucho?")


def test_contains_service_query_keyword_returns_false():
    """Should return False when no keywords present."""
    from app.engine import contains_service_query_keyword

    assert not contains_service_query_keyword("hola")
    assert not contains_service_query_keyword("buenos dias")
    assert not contains_service_query_keyword("gracias")
    assert not contains_service_query_keyword("chau")


def test_completado_returns_services_on_keyword():
    """
    Estado completado + keyword → muestra servicios.
    """
    sender = "777111222"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Barbería Test",
        "horarios": "Lun-Vie 9-18hs",
        "servicios": "Corte $5000, barba $3000"
    })

    response = handle_message(sender, "cuanto cuesta?")

    assert "servicios" in response.lower()
    assert "Corte $5000, barba $3000" in response


def test_completado_case_insensitive_keywords():
    """
    Keywords funcionan con mayúsculas/minúsculas y tildes.
    """
    sender = "777111223"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Test",
        "horarios": "9-18hs",
        "servicios": "Test $100"
    })

    # Mayúsculas
    response = handle_message(sender, "PRECIO")
    assert "Test $100" in response

    # Con tildes
    response = handle_message(sender, "¿Cuánto cuesta?")
    assert "Test $100" in response

    # Lowercase
    response = handle_message(sender, "servicios")
    assert "Test $100" in response


def test_completado_fallback_without_keywords():
    """
    Estado completado sin keywords → mensaje de ayuda.
    """
    sender = "777111224"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Test",
        "horarios": "9-18hs",
        "servicios": "Test $100"
    })

    response = handle_message(sender, "hola")

    assert "SERVICIOS" in response
    assert "precios" in response.lower()
    # NO debe mostrar los servicios todavía
    assert "Test $100" not in response


def test_completado_handles_empty_services():
    """
    Edge case: completado pero sin servicios guardados.
    """
    sender = "777111225"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Test",
        "horarios": "9-18hs",
        "servicios": ""  # Vacío
    })

    response = handle_message(sender, "precio")

    assert "no tenemos servicios" in response.lower() or "configurados" in response.lower()


def test_setup_not_affected_by_service_keywords():
    """
    CRÍTICO: Keywords NO deben afectar flujo de setup.
    Usuario en esperando_nombre escribe "cuanto" → debe seguir en setup.
    """
    sender = "777111226"

    # Setup inicial
    handle_message(sender, "setup")
    assert get_conversation(sender).get("estado") == "esperando_nombre"

    # Usuario escribe texto con keyword
    response = handle_message(sender, "Cuanto Cuesta Barbería")

    # Debe procesar como nombre (aunque tenga keyword)
    assert "horarios" in response.lower()  # Avanzó a esperando_horarios

    conv = get_conversation(sender)
    assert conv.get("estado") == "esperando_horarios"
    assert conv.get("nombre") == "Cuanto Cuesta Barbería"  # Guardó el texto con keyword


def test_multiple_service_query_keywords():
    """
    Múltiples keywords en mismo mensaje.
    """
    sender = "777111227"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Café Test",
        "horarios": "24hs",
        "servicios": "Café $1500, medialunas $800"
    })

    response = handle_message(sender, "cuanto cuestan los servicios?")

    assert "servicios" in response.lower()
    assert "Café $1500, medialunas $800" in response


def test_completado_preserves_state_on_query():
    """
    Consultar servicios NO debe modificar estado ni datos.
    """
    sender = "777111228"

    update_conversation(sender, {
        "estado": "completado",
        "nombre": "Test Business",
        "horarios": "Lun-Vie 9-18hs",
        "servicios": "Corte $5000"
    })

    # Query servicios
    response = handle_message(sender, "precio")

    # Verify state unchanged
    conv = get_conversation(sender)
    assert conv.get("estado") == "completado"
    assert conv.get("nombre") == "Test Business"
    assert conv.get("horarios") == "Lun-Vie 9-18hs"
    assert conv.get("servicios") == "Corte $5000"
