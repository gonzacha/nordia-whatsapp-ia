"""
Generación determinística de mensajes comerciales.

Este módulo genera mensajes comerciales basados en intent del usuario.
100% determinístico, sin LLM.
"""


def generate_commercial_message(customer_name: str, intent: str) -> str:
    """
    Genera mensaje comercial basado en intent detectado.
    100% determinístico, sin LLM.

    Args:
        customer_name: Nombre del cliente
        intent: Intención comercial del usuario (qué quiere decirle al cliente)

    Returns:
        Mensaje comercial generado

    Examples:
        >>> generate_commercial_message("Juan", "ofrecer lentes nuevos")
        'Hola Juan, llegaron nuevos lentes nuevos que te pueden interesar.\\n¿Querés que te cuente más?'

        >>> generate_commercial_message("María", "recordar turno del martes")
        'Hola María, quería recordarte turno del martes.\\n¿Querés que te cuente más?'

        >>> generate_commercial_message("Pedro", "invitar al evento")
        'Hola Pedro, te queremos invitar a evento.\\n¿Querés que te cuente más?'
    """
    intent_lower = intent.lower().strip()

    # Detectar verbo principal y extraer resto
    verb_mappings = [
        (["ofrecer", "mostrar", "presentar", "tenemos"],
            "llegaron nuevos {resto} que te pueden interesar"),
        (["recordar", "avisar", "acordar"],
            "quería recordarte {resto}"),
        (["invitar", "agendar", "programar", "reservar"],
            "te queremos invitar a {resto}"),
        (["preguntar", "consultar", "saber"],
            "quería preguntarte sobre {resto}"),
    ]

    phrase = None
    for verbs, template in verb_mappings:
        for verb in verbs:
            if verb in intent_lower:
                # Extraer el resto después del verbo
                parts = intent_lower.split(verb, 1)
                resto = parts[1].strip() if len(parts) > 1 else intent

                # Limpiar artículos comunes al inicio
                for prefix in ["le ", "te ", "los ", "las ", "un ", "una ", "el ", "la "]:
                    if resto.startswith(prefix):
                        resto = resto[len(prefix):]

                phrase = template.format(resto=resto if resto else intent)
                break
        if phrase:
            break

    # Fallback: usar intent tal cual
    if not phrase:
        phrase = intent

    # Construir mensaje final
    message = f"Hola {customer_name}, {phrase}.\n¿Querés que te cuente más?"

    return message
