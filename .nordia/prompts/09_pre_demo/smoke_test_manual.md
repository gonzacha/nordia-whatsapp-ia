# Smoke Test Manual

## Cuándo usar
- Después de deployar
- Antes de demo importante
- Después de fix de bug crítico

## Severidad
🔴 **HIGH** - Ejecutar antes de cada demo

---

## Prompt

```
ROLE: Sos un tester manual meticuloso.

TAREA: Ejecutar smoke test completo de Nordia.

PROCEDIMIENTO:

1. SETUP LIMPIO
   ```bash
   # Limpiar estado
   rm -f data/conversations_state.json
   rm -f data/nordia.db

   # Reiniciar servidor
   pkill -f uvicorn
   uvicorn app.main:app --reload
   ```

2. FLUJO FELIZ (SETUP)
   - WhatsApp: Enviar "Hola"
   - Esperar respuesta: "Hola 👋 Soy Nordia..."
   - Enviar: "setup"
   - Esperar: "¿Cómo se llama tu negocio?"
   - Enviar: "Barbería Test"
   - Esperar: "¿Cuáles son tus horarios?"
   - Enviar: "Lun-Vie 9-19"
   - Esperar: "¿Qué servicios ofrecés?"
   - Enviar: "Corte 8000, Barba 5000"
   - Esperar: "✅ Tu negocio quedó configurado"

   VALIDAR:
   - Todas las respuestas llegaron
   - Orden correcto
   - Latencia <5s cada una
   - JSON guardado en data/

3. RESTART RESILIENCE
   - En medio del flujo anterior, después de "Lun-Vie 9-19"
   - Reiniciar uvicorn
   - Enviar: "Corte 8000, Barba 5000"
   - DEBE recuperar contexto y completar setup

4. EDGE CASES
   - Enviar mensaje vacío → respuesta apropiada
   - Enviar imagen → "Solo texto por ahora"
   - Enviar mensaje de 1000 chars → truncado o rechazado
   - Enviar "asdfghjkl" en servicios → error claro

5. ERROR STATES
   - Simular token expirado (cambiar WHATSAPP_TOKEN a inválido)
   - Enviar mensaje
   - DEBE loguear error y no crashear
   - Health endpoint debe reportar degraded

PARA CADA PASO:
- ✅ PASS / ❌ FAIL
- Screenshot si falla
- Logs relevantes

OUTPUT:
- Reporte con % de tests pasados
- Lista de bugs encontrados
- Severidad de cada bug
```

---

## Output esperado

Reporte de smoke test:

```markdown
## SMOKE TEST - Nordia WhatsApp IA

**Fecha:** 2026-01-31
**Tester:** Gonza

### Resultados: 12/15 ✅ (80%)

#### 1. Setup Limpio ✅
- Estado borrado correctamente
- Servidor inició sin errores

#### 2. Flujo Feliz ✅ (7/7)
- Todas las respuestas llegaron
- Latencia promedio: 2.3s

#### 3. Restart Resilience ❌
- **BUG:** Contexto perdido después de restart
- Usuario tuvo que reiniciar setup
- **Severidad:** CRÍTICO

#### 4. Edge Cases ✅ (3/4)
- Mensaje vacío: OK
- Imagen: OK
- 1000 chars: OK
- "asdfghjkl" en servicios: ❌ Aceptó input inválido

#### 5. Error States ✅
- Token expirado: Detectado
- Sistema: No crasheó
- Health: degraded ✅

### Bugs Encontrados
1. [CRÍTICO] Restart pierde contexto
2. [MEDIO] Validación de precios falta

### Score: 80% - NO-GO
**Razón:** Bug crítico de persistencia
```
