"""
Customer plane handlers.
"""

from app.state import update_conversation


def handle_customer_message(sender: str, text: str, conv: dict) -> str:
    """
    Maneja mensajes CUSTOMER cuando plane == CUSTOMER
    Retorna string de respuesta.
    No modifica estado salvo cuando explícito.
    """
    from app.engine import (
        normalize_text,
        contains_service_query_keyword,
        contains_appointment_keyword,
    )

    normalized = normalize_text(text).strip()
    greetings = ["hola", "buenas", "buen dia", "buenas tardes"]

    if normalized in greetings:
        return "Hola 👋 ¿En qué puedo ayudarte?"

    if contains_service_query_keyword(text):
        servicios = conv.get("servicios", "")
        if servicios:
            return f"Nuestros servicios son:\n{servicios}"
        return "Todavía no tengo cargados los servicios."

    if contains_appointment_keyword(text):
        update_conversation(sender, {"estado": "esperando_fecha_turno"})
        return "Perfecto 👍 ¿Para qué día te gustaría el turno?"

    return "Podes preguntarme por servicios, precios o sacar un turno."
