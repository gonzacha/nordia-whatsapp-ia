# Autopsia Post-Mortem

## Cuándo usar
**Después de CUALQUIER bug en producción o demo fallida**

## Severidad
🔴 **CRITICAL** - Obligatorio después de cada bug

---

## Prompt

```
ROLE: Sos un investigador forense de bugs.

TAREA: Analizar el bug a fondo y prevenir recurrencia.

BUG:
[Describir qué salió mal]

AUTOPSIA:

1. TIMELINE
   - ¿Cuándo se introdujo el bug? (commit, PR, fecha)
   - ¿Cuándo se detectó?
   - ¿Cuánto tiempo pasó sin detectarse?

2. ROOT CAUSE
   - ¿Cuál fue la causa raíz? (no síntoma)
   - ¿Por qué pasó? (5 Whys)
   - ¿Qué asumimos incorrectamente?

3. IMPACTO
   - ¿Cuántos usuarios afectados?
   - ¿Datos perdidos/corruptos?
   - ¿Demo/demo fallida?

4. DETECCIÓN
   - ¿Cómo se descubrió?
   - ¿Por qué los tests no lo detectaron?
   - ¿Por qué el smoke test no lo encontró?

5. FIX APLICADO
   - ¿Qué se cambió?
   - ¿Es fix definitivo o parche temporal?
   - ¿Código del fix?

6. PREVENCIÓN
   - ¿Qué test agregar para que no vuelva a pasar?
   - ¿Qué validación faltaba?
   - ¿Qué documentación agregar?

7. LEARNING
   - ¿Qué aprendimos?
   - ¿Hay otros lugares con el mismo patrón?
   - ¿Necesitamos cambiar proceso de desarrollo?

OUTPUT:
Documento markdown con:
- Título: "Post-Mortem: [Bug]"
- Secciones numeradas
- Action items concretos
- Owner de cada action item
- Timeline de implementación

EJEMPLO ACTION ITEMS:
- [ ] Agregar test test_empty_message_handling.py
- [ ] Documentar validaciones en VALIDATION.md
- [ ] Agregar pre-commit hook para validar inputs
```

---

## Output esperado

```markdown
# Post-Mortem: Token Expirado Durante Demo

## Timeline
- **Introducido:** 2026-01-28 (deploy sin healthcheck)
- **Detectado:** 2026-01-30 14:35 (demo en vivo)
- **Duración:** 48 horas sin detectar

## Root Cause
Token de WhatsApp expiró después de 60 días.
Sistema no validaba token al startup.

### 5 Whys:
1. ¿Por qué falló? → Token expirado
2. ¿Por qué expiró? → Duración 60 días
3. ¿Por qué no detectamos? → Sin healthcheck
4. ¿Por qué sin healthcheck? → No lo consideramos
5. ¿Por qué? → Falta de análisis de failure modes

## Impacto
- 1 usuario (demo)
- Demo fallida
- Sin datos perdidos

## Fix Aplicado
```python
# app/config.py
def validate_whatsapp_token():
    # Valida contra /me endpoint
    ...
```

## Prevención
- [x] Test de token inválido
- [x] Healthcheck en startup
- [ ] Monitoring de expiración
- [ ] Alert 7 días antes de expirar

## Learning
**Patrón:** Credential Liveness Failure
**Acción:** Agregar a biblioteca de failure modes
```
