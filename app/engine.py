"""
Conversational engine with state machine for WhatsApp setup flow.

States:
- inicial: New user or no setup started
- esperando_nombre: Waiting for business name
- esperando_horarios: Waiting for business hours
- esperando_servicios: Waiting for services list
- completado: Setup completed
"""

from app.state import get_conversation, update_conversation
from app.validators import validate_nombre, validate_horarios, validate_servicios


ESTADOS = {
    "inicial": "Usuario nuevo o sin setup",
    "esperando_nombre": "Esperando nombre del negocio",
    "esperando_horarios": "Esperando horarios de atención",
    "esperando_servicios": "Esperando lista de servicios",
    "completado": "Setup finalizado"
}


def handle_message(sender: str, text: str) -> str:
    """
    Process incoming WhatsApp message with state machine.

    Args:
        sender: Phone number of sender
        text: Message text from user

    Returns:
        Reply message to send back
    """
    # Get current conversation state
    conv = get_conversation(sender)
    estado_actual = conv.get("estado", "inicial")

    print(f"[ENGINE] {sender} | Estado: {estado_actual} | Mensaje: {text[:50]}")

    # State machine transitions
    if estado_actual == "inicial":
        # Waiting for setup keyword
        if text.strip().lower() in ["setup", "/setup"]:
            update_conversation(sender, {"estado": "esperando_nombre"})
            return "Perfecto 👍 ¿Cómo se llama tu negocio?"
        return "Hola 👋 Soy Nordia. Escribí 'setup' para comenzar."

    elif estado_actual == "esperando_nombre":
        # Validate business name before saving
        is_valid, error_msg = validate_nombre(text)
        if not is_valid:
            # Validation failed - stay in same state and return error
            return f"❌ {error_msg}\n\n¿Cómo se llama tu negocio?"

        # Valid - save and advance to next state
        update_conversation(sender, {
            "estado": "esperando_horarios",
            "nombre": text
        })
        return f"Perfecto, {text}. ¿Cuáles son tus horarios de atención?"

    elif estado_actual == "esperando_horarios":
        # Validate business hours before saving
        is_valid, error_msg = validate_horarios(text)
        if not is_valid:
            # Validation failed - stay in same state and return error
            return f"❌ {error_msg}\n\n¿Cuáles son tus horarios?"

        # Valid - save and advance to next state
        conv["estado"] = "esperando_servicios"
        conv["horarios"] = text
        update_conversation(sender, conv)
        return "Genial. ¿Qué servicios ofreces?"

    elif estado_actual == "esperando_servicios":
        # Validate services before completing setup
        is_valid, error_msg = validate_servicios(text)
        if not is_valid:
            # Validation failed - stay in same state and return error
            return f"❌ {error_msg}\n\n¿Qué servicios ofreces?"

        # Valid - save and complete setup
        conv["estado"] = "completado"
        conv["servicios"] = text
        update_conversation(sender, conv)
        return (
            f"✅ Listo! Guardé:\n"
            f"- Negocio: {conv['nombre']}\n"
            f"- Horarios: {conv['horarios']}\n"
            f"- Servicios: {text}"
        )

    elif estado_actual == "completado":
        # User already completed setup
        return "Ya completaste el setup. Próximamente más funciones!"

    # Fallback (should never reach here)
    return "Hola 👋 Soy Nordia. Escribí 'setup' para comenzar."
