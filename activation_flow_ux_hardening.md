# Activation Flow UX Hardening

## activation_awaiting_name

**Estado actual**
- activation_awaiting_name

**Mensaje actual**
- "¿Nombre del cliente?"
- "Por favor decime el nombre del cliente."

**Problema detectado**
- Es abrupto. No recuerda el contexto de activacion.
- No indica opcion de cancelar.
- No da ejemplo de formato.

**Propuesta de nuevo copy**
- "Necesito el nombre del cliente."
- "Podes escribir solo el nombre. Ej: Juan Perez."
- "Si queres salir, escribi CANCELAR."

---

## activation_awaiting_intent

**Estado actual**
- activation_awaiting_intent

**Mensaje actual**
- "Perfecto. ¿Qué te gustaría decirle a {customer_name}?"
- "Contame qué querés decirle."
- "¿Podrías ser un poco más específico? Ej: 'ofrecer lentes nuevos', 'recordar turno'"

**Problema detectado**
- La pregunta es larga y puede sonar vaga.
- El pedido de detalle aparece tarde y en un solo mensaje largo.
- No aclara el objetivo: crear un mensaje comercial corto.

**Propuesta de nuevo copy**
- "¿Que mensaje queres enviarle a {customer_name}?"
- "Escribi la idea en una frase corta."
- "Ejemplos: ofrecer lentes nuevos. Recordar un turno."

---

## activation_showing_draft

**Estado actual**
- activation_showing_draft

**Mensaje actual**
- "Te sugiero este mensaje:\n\n\"{generated_message}\"\n\n📤 Escribí \"enviar\" para confirmar\n❌ Escribí \"cancelar\" para descartar"
- "No entendí. Escribí 'enviar' para confirmar o 'cancelar' para descartar."

**Problema detectado**
- Instrucciones mezcladas con el borrador.
- El CTA esta en una sola linea larga.
- El fallback repite pero no aclara que el borrador se mantiene.

**Propuesta de nuevo copy**
- "Borrador listo:"
- "\"{generated_message}\""
- "Escribi ENVIAR para guardar."
- "Escribi CANCELAR para descartar."
- "Si escribis otra cosa, mantengo este borrador."
