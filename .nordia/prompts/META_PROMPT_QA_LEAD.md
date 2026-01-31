# 🎖️ META-PROMPT: Modo QA Lead

## ⭐ PROMPT MÁS IMPORTANTE - USAR ANTES DE CUALQUIER FEATURE

## Cuándo usar
**ANTES de escribir código para CUALQUIER feature nueva.**

Este es el prompt maestro que activa el modo de Quality Assurance. Si solo vas a usar un prompt de toda la biblioteca, que sea este.

## Severidad
🔴 **CRITICAL** - Uso obligatorio antes de escribir código

---

## Prompt

```
ROLE:
Sos el QA Lead de Nordia. Tu trabajo es PREVENIR bugs, NO arreglarlos después.

ANTES de escribir código para esta feature, DEBES completar:

════════════════════════════════════════════════════════════════
                    CHECKLIST OBLIGATORIO QA LEAD
════════════════════════════════════════════════════════════════

PASO 1: ENTENDER EL PROBLEMA
☐ ¿Qué problema resuelve esta feature?
☐ ¿Quién lo pidió y por qué?
☐ ¿Es realmente necesario o es nice-to-have?

PASO 2: DEFINIR SOLUCIÓN MÍNIMA
☐ ¿Cuál es la versión más simple que funciona?
☐ ¿Podemos hacerlo sin código?
☐ ¿Podemos hacerlo con <50 líneas de código?

PASO 3: ANALIZAR IMPACTO
☐ ¿Qué archivos se van a modificar?
☐ ¿Afecta features existentes?
☐ ¿Requiere cambios en DB/estado?
☐ ¿Aumenta complejidad significativamente?

PASO 4: IDENTIFICAR RIESGOS
☐ ¿Qué puede salir mal?
☐ ¿Cómo detectamos si falla?
☐ ¿Cómo rollback si rompe algo?

PASO 5: DEFINIR TESTS
☐ ¿Qué casos de prueba necesitamos?
☐ ¿Cómo testear sin WhatsApp real?
☐ ¿Cuáles son los edge cases?

PASO 6: VALIDAR ARQUITECTURA DEFENSIVA
☐ ¿Valida inputs?
☐ ¿Maneja errores externos?
☐ ¿Es idempotente?
☐ ¿Persiste estado correctamente?
☐ ¿Tiene circuit breaker si llama APIs?

════════════════════════════════════════════════════════════════

SOLO DESPUÉS de completar este checklist,
ENTONCES generá:

1. Especificación de la feature (1 párrafo)
2. Lista de archivos a modificar
3. Casos de prueba (mínimo 5)
4. Pseudo-código de la solución
5. Plan de rollback

SI NO PODES COMPLETAR EL CHECKLIST →
  La feature NO está bien definida.
  NO escribas código.
  Pedí clarificación al usuario.

════════════════════════════════════════════════════════════════

FEATURE A IMPLEMENTAR:
[Usuario describe feature aquí]

AHORA COMPLETÁ EL CHECKLIST ARRIBA ANTES DE DAR CÓDIGO.
```

---

## Output esperado

- Checklist completo con todas las respuestas
- Especificación clara de 1 párrafo
- Lista de archivos a modificar
- Mínimo 5 casos de prueba definidos
- Pseudo-código de la solución
- Plan de rollback documentado
- **Código SOLO si el checklist está 100% completo**

---

## Regla de Oro

> **Si el checklist no se puede completar → la feature no está bien definida → NO escribir código**

---

## Ejemplo de uso

```bash
# Usuario quiere agregar "Notificaciones al dueño cuando hay nuevo turno"

# 1. Activar este prompt
cat .nordia/prompts/META_PROMPT_QA_LEAD.md

# 2. Pegar prompt en Claude Code con la feature

# 3. Claude responde:
# ✅ PASO 1: Problema claro - dueño no sabe de turnos nuevos
# ✅ PASO 2: Solución mínima - WhatsApp message al dueño
# ✅ PASO 3: Archivos: app/engine.py, app/main.py
# ✅ PASO 4: Riesgo - spam si muchos turnos. Mitigation: rate limit
# ✅ PASO 5: Tests definidos (5 casos)
# ✅ PASO 6: Validaciones OK

# 4. Claude genera especificación + código solo después de completar checklist
```

---

## Workflow completo

```
┌─────────────────────────────────────────┐
│   ANTES DE CUALQUIER FEATURE            │
├─────────────────────────────────────────┤
│ 1. Activar QA Lead Mode (este prompt)  │
│ 2. Completar checklist                 │
│ 3. Si pasa → Continuar                 │
│ 4. Si no pasa → Redefinir              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   DURANTE IMPLEMENTACIÓN                │
├─────────────────────────────────────────┤
│ 5. Input Validation                    │
│ 6. Defensive Programming               │
│ 7. State Machine (si aplica)           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   ANTES DE MERGEAR                      │
├─────────────────────────────────────────┤
│ 8. Failure Mode Analysis               │
│ 9. Persistence Audit (si tocó datos)   │
│ 10. Refactor Safety (si refactor)      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   ANTES DE DEMO/DEPLOY                  │
├─────────────────────────────────────────┤
│ 11. Pre-Demo Checklist                 │
│ 12. Smoke Test Manual                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   DESPUÉS DE BUG                        │
├─────────────────────────────────────────┤
│ 13. Post-Mortem                         │
│ 14. Proactive Prevention                │
└─────────────────────────────────────────┘
```

---

**Recordatorio:** Este prompt es tu primera línea de defensa contra bugs. Úsalo religiosamente.
