"""
Integration test for admin activation happy path.

Pure integration test - no mocks, no monkeypatch.
Tests complete activation flow with real handle_message function.
"""

from app.engine import handle_message
from app.state import delete_conversation


def test_admin_activation_complete_happy_path():
    """
    Test complete admin activation flow from start to finish.

    Flow:
    1. Admin: "activar cliente"
    2. System: asks for customer name
    3. Admin: provides name
    4. System: asks for intent
    5. Admin: provides intent
    6. System: shows draft
    7. Admin: "enviar"
    8. System: confirms
    """
    # Use fresh test phone number (in TEST_PHONE_PATTERNS)
    admin_sender = "888111222"

    # Clean state before test
    delete_conversation(admin_sender)

    # Step 1: Trigger activation
    reply1 = handle_message(admin_sender, "activar cliente")
    assert "nombre" in reply1.lower()
    assert "cliente" in reply1.lower()

    # Step 2: Provide customer name
    reply2 = handle_message(admin_sender, "Carlos Martinez")
    assert "carlos" in reply2.lower()
    assert "mensaje" in reply2.lower()

    # Step 3: Provide commercial intent
    reply3 = handle_message(admin_sender, "recordar turno de mañana")
    assert "borrador" in reply3.lower()
    assert "carlos" in reply3.lower()
    assert "enviar" in reply3.lower()

    # Step 4: Confirm sending
    reply4 = handle_message(admin_sender, "enviar")
    assert "listo" in reply4.lower() or "✅" in reply4
    assert "carlos" in reply4.lower()
    assert "preparado" in reply4.lower() or "guardado" in reply4.lower()

    # Cleanup after test
    delete_conversation(admin_sender)
