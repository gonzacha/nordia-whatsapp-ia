# Activation Flow Guardrails Spec

## activation_awaiting_name

**Estado**
- activation_awaiting_name

**Inputs invalidos comunes**
- Mensaje vacio
- Solo emojis
- Solo espacios
- Texto muy corto sin nombre

**Regla minima de validacion**
- El texto no puede estar vacio y debe tener al menos 2 caracteres utiles.

**Respuesta sugerida cuando falla validacion**
- "Necesito el nombre del cliente. Escribilo en una sola palabra o frase."

---

## activation_awaiting_intent

**Estado**
- activation_awaiting_intent

**Inputs invalidos comunes**
- Mensaje vacio
- Una o dos palabras sin contexto
- Solo emojis
- Solo signos

**Regla minima de validacion**
- El texto debe tener al menos 3 palabras.

**Respuesta sugerida cuando falla validacion**
- "Escribi una frase corta con el motivo. Ej: recordar turno o ofrecer lentes nuevos."

---

## activation_showing_draft

**Estado**
- activation_showing_draft

**Inputs invalidos comunes**
- Mensajes distintos de enviar o cancelar
- Confirmaciones ambiguas como "ok" o "dale" si no se aceptan
- Respuestas vacias

**Regla minima de validacion**
- Solo se acepta "enviar" para confirmar o "cancelar" para descartar.

**Respuesta sugerida cuando falla validacion**
- "No entendi. Escribi ENVIAR para guardar o CANCELAR para descartar."

---

# Current Engine Validation Map

## activation_awaiting_name

**Estado**
- activation_awaiting_name

**Aceptado (actual)**
- Cualquier texto no vacio
- Nombres con una o mas palabras

**Rechazado (actual)**
- Mensaje vacio
- Solo espacios
- "cancelar", "salir", "no" (cancela el flujo)

**Regla minima de validacion (actual)**
- El texto debe tener al menos 1 caracter no vacio.
- `if not text.strip():`

**Validacion faltante**
- Missing validation: no hay validacion de formato o longitud minima.

---

## activation_awaiting_intent

**Estado**
- activation_awaiting_intent

**Aceptado (actual)**
- Texto con 3 o mas palabras

**Rechazado (actual)**
- Mensaje vacio
- Texto con menos de 3 palabras
- "cancelar", "salir" (cancela el flujo)

**Regla minima de validacion (actual)**
- El texto debe tener al menos 3 palabras.
- `word_count = len(text.strip().split())`
- `if word_count < 3:`

**Validacion faltante**
- Missing validation: no hay validacion de contenido mas alla del conteo de palabras.

---

## activation_showing_draft

**Estado**
- activation_showing_draft

**Aceptado (actual)**
- Confirmar: "enviar", "si", "sí", "ok", "dale", "confirmar"
- Cancelar: "cancelar", "no", "salir"

**Rechazado (actual)**
- Cualquier otro texto
- Mensaje vacio

**Regla minima de validacion (actual)**
- Solo se aceptan confirmaciones o cancelaciones de la lista.
- `if normalized_input in ["enviar", "si", "sí", "ok", "dale", "confirmar"]:`
- `if normalized_input in ["cancelar", "no", "salir"]:`

**Validacion faltante**
- Missing validation: no hay manejo explicito de respuestas alternativas fuera de la lista.
