"""
Conversational engine with state machine for WhatsApp setup flow.

States:
- inicial: New user or no setup started
- esperando_nombre: Waiting for business name
- esperando_horarios: Waiting for business hours
- esperando_servicios: Waiting for services list
- completado: Setup completed
- activation_awaiting_name: Waiting for customer name (activation flow)
- activation_awaiting_intent: Waiting for commercial intent (activation flow)
- activation_showing_draft: Showing message draft for confirmation (activation flow)
"""

import unicodedata
from app.state import get_conversation, update_conversation
from app.validators import validate_nombre, validate_horarios, validate_servicios
from app.message_generator import generate_commercial_message
from app.persistence import save_message_draft


ESTADOS = {
    "inicial": "Usuario nuevo o sin setup",
    "esperando_nombre": "Esperando nombre del negocio",
    "esperando_horarios": "Esperando horarios de atención",
    "esperando_servicios": "Esperando lista de servicios",
    "completado": "Setup finalizado",
    "esperando_fecha_turno": "Esperando día para turno",
    "esperando_hora_turno": "Esperando hora para turno",
    "activation_awaiting_name": "Esperando nombre del cliente (activación)",
    "activation_awaiting_intent": "Esperando intención comercial (activación)",
    "activation_showing_draft": "Mostrando borrador de mensaje (activación)"
}


def normalize_text(text: str) -> str:
    """
    Normalize text for keyword matching: lowercase + remove accents.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text (lowercase, no accents)

    Examples:
        >>> normalize_text("CUÁNTO")
        'cuanto'
        >>> normalize_text("Precio")
        'precio'
    """
    # Remove accents using Unicode normalization
    nfkd = unicodedata.normalize('NFKD', text)
    without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    return without_accents.lower()


def contains_service_query_keyword(text: str) -> bool:
    """
    Check if text contains keywords for service/price query.

    Keywords: precio, servicios, cuanto, cuesta, sale
    Case-insensitive and accent-insensitive.

    Args:
        text: User message to check

    Returns:
        True if contains any service query keyword

    Examples:
        >>> contains_service_query_keyword("cuanto cuesta?")
        True
        >>> contains_service_query_keyword("hola")
        False
    """
    normalized = normalize_text(text)
    keywords = [
        'precio', 'precios',
        'servicio', 'servicios',
        'cuanto',
        'cuesta', 'cuestan',
        'sale', 'salen'
    ]

    return any(keyword in normalized for keyword in keywords)


def contains_appointment_keyword(text: str) -> bool:
    """
    Check if text contains keywords for appointment request.

    Keywords: turno, reserva, cita
    Case-insensitive and accent-insensitive.

    Args:
        text: User message to check

    Returns:
        True if contains any appointment keyword

    Examples:
        >>> contains_appointment_keyword("quiero un turno")
        True
        >>> contains_appointment_keyword("hola")
        False
    """
    normalized = normalize_text(text)
    keywords = ['turno', 'turnos', 'reserva', 'reservar', 'cita']
    return any(keyword in normalized for keyword in keywords)


def contains_activation_keyword(text: str) -> bool:
    """
    Check if text contains keywords for customer activation flow.

    Keywords: activar cliente, activar contacto, contactar cliente, etc.
    Case-insensitive and accent-insensitive.

    Args:
        text: User message to check

    Returns:
        True if contains any activation keyword

    Examples:
        >>> contains_activation_keyword("activar cliente")
        True
        >>> contains_activation_keyword("contactar cliente")
        True
        >>> contains_activation_keyword("hola")
        False
    """
    normalized = normalize_text(text)

    # Multi-word triggers
    multi_word_triggers = [
        'activar cliente',
        'activar contacto',
        'contactar cliente',
        'enviar mensaje a cliente',
        'mensaje a cliente',
        'escribirle a'
    ]

    return any(trigger in normalized for trigger in multi_word_triggers)


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
        # Check for activation keyword first (before setup)
        if contains_activation_keyword(text):
            # Initialize activation context
            update_conversation(sender, {
                "estado": "activation_awaiting_name",
                "activation_context": {
                    "active": True,
                    "customer_name": None,
                    "commercial_intent": None,
                    "generated_message": None
                }
            })
            return "¿Nombre del cliente?"

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
        # Check for appointment request (priority over services)
        if contains_appointment_keyword(text):
            update_conversation(sender, {
                **conv,  # Preserve existing data
                "estado": "esperando_fecha_turno"
            })
            return "Perfecto 👍 ¿Para qué día?"

        # Check if user is querying for services/prices
        if contains_service_query_keyword(text):
            servicios = conv.get("servicios", "")

            if servicios:
                return f"Estos son nuestros servicios:\n{servicios}"
            else:
                # Edge case: completed setup but no services saved
                return "Todavía no tenemos servicios configurados."

        # Fallback: guide user on what they can do
        return "¡Hola! Escribí SERVICIOS para ver precios o TURNO para reservar."

    elif estado_actual == "esperando_fecha_turno":
        # Save appointment date temporarily
        conv["turno_temp"] = {"fecha": text}
        conv["estado"] = "esperando_hora_turno"
        update_conversation(sender, conv)
        return "¿A qué hora?"

    elif estado_actual == "esperando_hora_turno":
        # Save complete appointment to list
        fecha = conv.get("turno_temp", {}).get("fecha", "")
        turno = {"fecha": fecha, "hora": text}

        # Add to appointments list
        if "turnos" not in conv:
            conv["turnos"] = []
        conv["turnos"].append(turno)

        # Clean temporary data and return to completado
        if "turno_temp" in conv:
            del conv["turno_temp"]
        conv["estado"] = "completado"
        update_conversation(sender, conv)

        return f"✅ Turno reservado para {fecha} a las {text}"

    elif estado_actual == "activation_awaiting_name":
        # Normalize input
        normalized_input = text.strip().lower()

        # Check for cancellation
        if normalized_input in ["cancelar", "salir", "no"]:
            # Clear activation context and return to inicial
            update_conversation(sender, {"estado": "inicial"})
            return "Activación cancelada."

        # Validate customer name
        if not text.strip():
            # Empty input - stay in same state
            return "Por favor decime el nombre del cliente."

        # Valid name - save and advance
        customer_name = text.strip()
        activation_ctx = conv.get("activation_context", {})
        activation_ctx["customer_name"] = customer_name

        conv["estado"] = "activation_awaiting_intent"
        conv["activation_context"] = activation_ctx
        update_conversation(sender, conv)

        return f"Perfecto. ¿Qué te gustaría decirle a {customer_name}?"

    elif estado_actual == "activation_awaiting_intent":
        # Normalize input
        normalized_input = text.strip().lower()

        # Check for cancellation
        if normalized_input in ["cancelar", "salir"]:
            # Clear activation context and return to inicial
            update_conversation(sender, {"estado": "inicial"})
            return "Activación cancelada."

        # Validate intent
        if not text.strip():
            # Empty input
            return "Contame qué querés decirle."

        # Check word count (need at least 3 words)
        word_count = len(text.strip().split())
        if word_count < 3:
            return "¿Podrías ser un poco más específico? Ej: 'ofrecer lentes nuevos', 'recordar turno'"

        # Valid intent - generate message and show draft
        commercial_intent = text.strip()
        activation_ctx = conv.get("activation_context", {})
        customer_name = activation_ctx.get("customer_name", "Cliente")

        # Generate message
        generated_message = generate_commercial_message(customer_name, commercial_intent)

        # Save to context
        activation_ctx["commercial_intent"] = commercial_intent
        activation_ctx["generated_message"] = generated_message

        conv["estado"] = "activation_showing_draft"
        conv["activation_context"] = activation_ctx
        update_conversation(sender, conv)

        # Show draft with options
        return (
            f"Te sugiero este mensaje:\n\n"
            f"\"{generated_message}\"\n\n"
            f"📤 Escribí \"enviar\" para confirmar\n"
            f"❌ Escribí \"cancelar\" para descartar"
        )

    elif estado_actual == "activation_showing_draft":
        # Normalize input
        normalized_input = text.strip().lower()

        # Check for confirmation
        if normalized_input in ["enviar", "si", "sí", "ok", "dale", "confirmar"]:
            # Save to database
            activation_ctx = conv.get("activation_context", {})
            customer_name = activation_ctx.get("customer_name", "")
            commercial_intent = activation_ctx.get("commercial_intent", "")
            generated_message = activation_ctx.get("generated_message", "")

            # Save message draft to DB
            draft_id = save_message_draft(customer_name, commercial_intent, generated_message)

            # Clear activation context and return to inicial
            update_conversation(sender, {"estado": "inicial"})

            # Success message
            return (
                f"✅ Listo. Mensaje preparado para {customer_name}.\n\n"
                f"El mensaje quedó guardado. Cuando conectemos WhatsApp, "
                f"se enviará automáticamente."
            )

        # Check for cancellation
        if normalized_input in ["cancelar", "no", "salir"]:
            # Clear activation context and return to inicial
            update_conversation(sender, {"estado": "inicial"})
            return "Activación cancelada."

        # Unknown command - repeat options
        return "No entendí. Escribí 'enviar' para confirmar o 'cancelar' para descartar."

    # Fallback (should never reach here)
    return "Hola 👋 Soy Nordia. Escribí 'setup' para comenzar."
