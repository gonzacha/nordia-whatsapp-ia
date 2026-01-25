sessions = {}

def process_message(phone: str, text: str) -> str:
    if phone not in sessions:
        sessions[phone] = {"estado": "inicio", "data": {}}

    session = sessions[phone]
    estado = session["estado"]
    text_lower = text.lower().strip()

    if estado == "inicio":
        sessions[phone]["estado"] = "esperando_servicio"
        return "Hola 👋 ¿Querés sacar un turno? Respondé SI"

    elif estado == "esperando_servicio":
        if "si" in text_lower:
            sessions[phone]["estado"] = "esperando_dia"
            return "¿Qué servicio te interesa?"
        else:
            sessions[phone]["estado"] = "inicio"
            return "Ok, cualquier cosa avisame"

    elif estado == "esperando_dia":
        sessions[phone]["data"]["servicio"] = text
        sessions[phone]["estado"] = "esperando_hora"
        return "¿Qué día te gustaría? (ej: lunes, martes)"

    elif estado == "esperando_hora":
        sessions[phone]["data"]["dia"] = text
        sessions[phone]["estado"] = "esperando_nombre"
        return "¿A qué hora? (ej: 10:00, 14:30)"

    elif estado == "esperando_nombre":
        sessions[phone]["data"]["hora"] = text
        sessions[phone]["estado"] = "confirmado"
        return "¿Cuál es tu nombre?"

    elif estado == "confirmado":
        sessions[phone]["data"]["nombre"] = text
        sessions[phone]["estado"] = "inicio"
        return "Listo, tu turno quedó agendado 👍"

    return "No entendí, escribí HOLA para empezar"
