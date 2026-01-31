# Checklist Pre-Feature

## Cuándo usar
**ANTES de escribir código para cualquier feature nueva**

(Este es el checklist que también está en META_PROMPT_QA_LEAD)

## Severidad
🔴 **CRITICAL** - Uso obligatorio

---

## Prompt

```
ROLE: Sos un product engineer que valida features antes de construirlas.

TAREA: Validar que la feature propuesta está bien definida.

FEATURE PROPUESTA:
[Describir feature]

VALIDAR:

☐ 1. PROBLEMA CLARO
   - ¿Qué problema resuelve?
   - ¿Quién tiene este problema?
   - ¿Cuántos usuarios lo pidieron?

☐ 2. SOLUCIÓN MÍNIMA
   - ¿Cuál es la versión más simple que resuelve el problema?
   - ¿Hay forma de hacerlo sin código?
   - ¿Hay forma de hacerlo con menos código?

☐ 3. SCOPE BIEN DEFINIDO
   - ¿Qué está incluido?
   - ¿Qué está explícitamente excluido?
   - ¿Cuándo está "terminado"?

☐ 4. NO ROMPE NADA
   - ¿Afecta features existentes?
   - ¿Cambia comportamiento actual?
   - ¿Requiere migración de datos?

☐ 5. OBSERVABLE
   - ¿Cómo sé si funciona?
   - ¿Qué métricas medir?
   - ¿Cómo debuggear si falla?

☐ 6. REVERSIBLE
   - ¿Puedo desactivarla fácil?
   - ¿Feature flag?
   - ¿Plan de rollback?

SI ALGUNA RESPUESTA ES "NO SÉ" → NO ESCRIBAS CÓDIGO TODAVÍA

OUTPUT:
- Checklist completado
- Estimación de tiempo: X horas
- Riesgo: BAJO/MEDIO/ALTO
- Recomendación: HACER / NO HACER / REDEFINIR
```

---

## Output esperado

```markdown
## FEATURE: Notificaciones al dueño

### Checklist ✅
1. Problema: Dueño no sabe cuándo hay turno nuevo
2. Solución mínima: WhatsApp al dueño
3. Scope: Solo WhatsApp, no email
4. No rompe: Feature aislada
5. Observable: Log de notificación enviada
6. Reversible: Flag NOTIFICATIONS_ENABLED

### Estimación: 2 horas
### Riesgo: BAJO
### Recomendación: HACER
```
