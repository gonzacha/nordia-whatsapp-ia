# Checklist Pre-Demo

## Cuándo usar
**24 horas ANTES de grabar cualquier demo o lanzar feature**

## Severidad
🔴 **CRITICAL** - Obligatorio antes de cada demo pública

---

## Prompt

```
ROLE: Sos un QA lead que valida sistemas antes de demos públicas.

TAREA: Validar que Nordia está listo para demo/producción.

CHECKLIST OBLIGATORIO:

☐ 1. PERSISTENCIA
   - [ ] Estado se guarda en disco (no solo RAM)
   - [ ] Restart no pierde conversaciones
   - [ ] Probado: reiniciar servidor en medio de conversación

☐ 2. VALIDACIÓN
   - [ ] Inputs extremos manejados (vacío, muy largo, caracteres especiales)
   - [ ] Mensajes no-texto respondidos apropiadamente
   - [ ] Precios sin números rechazados con mensaje claro

☐ 3. ERRORES EXTERNOS
   - [ ] Token expirado detectado y logueado
   - [ ] WhatsApp API caído no crashea el sistema
   - [ ] Respuestas con timeout manejadas

☐ 4. ESTADOS
   - [ ] Transiciones inválidas bloqueadas
   - [ ] Conversaciones zombies limpiadas
   - [ ] Estados inconsistentes detectados

☐ 5. OBSERVABILIDAD
   - [ ] Logs claros con niveles apropiados
   - [ ] Errores tienen contexto suficiente
   - [ ] Health endpoint funciona

☐ 6. TESTING
   - [ ] Flujo completo testeado end-to-end
   - [ ] Casos edge probados manualmente
   - [ ] Rollback plan documentado

☐ 7. PERFORMANCE
   - [ ] Respuestas en <5 segundos
   - [ ] Sin memory leaks en pruebas de 1 hora
   - [ ] Rate limits configurados

☐ 8. SEGURIDAD
   - [ ] Credentials en .env, no hardcodeadas
   - [ ] Inputs sanitizados antes de guardar
   - [ ] No hay SQL injection posible

EJECUTAR TESTS:
```bash
# Test 1: Restart resilience
python -m pytest tests/test_persistence.py

# Test 2: Edge cases
python -m pytest tests/test_validation.py

# Test 3: End-to-end
python -m pytest tests/test_e2e.py
```

OUTPUT:
- Checklist completado (✅/❌)
- Lista de blockers encontrados
- Estimación de tiempo para fix
- GO / NO-GO para demo
```

---

## Output esperado

Reporte de preparación:

```markdown
## REPORTE PRE-DEMO

### Checklist (6/8 ✅)
✅ Persistencia
✅ Validación
✅ Errores externos
❌ Estados (falta validación de transiciones)
✅ Observabilidad
✅ Testing
❌ Performance (respuestas en 8s, objetivo 5s)
✅ Seguridad

### Blockers
1. [P0] Transiciones no validadas - 1h fix
2. [P1] Performance lenta - 2h optimización

### Decisión: NO-GO
**Razón:** Blocker P0 debe resolverse

**Tiempo para GO:** 1 hora
```

---

## Ejemplo de uso

```bash
# 24h antes de grabar demo
cat .nordia/prompts/09_pre_demo/checklist_pre_demo.md

# Claude ejecuta checklist y retorna GO/NO-GO
```
