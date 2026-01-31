# Post-Mortem: [Título del Bug]

**Fecha:** YYYY-MM-DD
**Severidad:** 🔴 CRÍTICO / 🟡 MEDIO / 🟢 BAJO
**Reportado por:** [Usuario/Demo/Interno]
**Estado:** [ ] Draft / [ ] Completado / [ ] Archivado

---

## 1. TIMELINE

- **Bug introducido:** [Fecha/Commit/PR] - [Descripción del cambio que lo introdujo]
- **Bug detectado:** [Fecha/Hora] - [Cómo se detectó]
- **Tiempo sin detectar:** [X días/horas]
- **Bug resuelto:** [Fecha/Commit] - [Link al PR del fix]

---

## 2. SÍNTOMAS

### ¿Qué vio el usuario?
[Descripción desde perspectiva del usuario]

### ¿Qué error apareció?
```
[Mensaje de error exacto / Stack trace / Logs]
```

### ¿Qué comportamiento esperado NO ocurrió?
[Qué debería haber pasado vs qué pasó]

### Screenshots/Evidence (si aplica):
[Links a screenshots, videos, logs]

---

## 3. ROOT CAUSE (Causa Raíz)

### Descripción técnica:
[¿Cuál fue la causa técnica fundamental?]

### Aplicar 5 Whys:

1. **¿Por qué pasó el bug?**
   → [Respuesta]

2. **¿Por qué eso?**
   → [Respuesta]

3. **¿Por qué eso?**
   → [Respuesta]

4. **¿Por qué eso?**
   → [Respuesta]

5. **¿Por qué eso?**
   → [ROOT CAUSE REAL - La causa sistémica fundamental]

### Código responsable:
**Archivo:** `[path/to/file.py]`
**Función/Línea:** `[nombre_funcion():123]`

```python
# Código con el bug
[código exacto que causó el problema]
```

---

## 4. IMPACTO

### Cuantificación:
- **Usuarios afectados:** [Número exacto o estimado]
- **Datos perdidos:** [ ] Sí / [ ] No
  - Si sí: [Detalle de qué se perdió y si es recuperable]
- **Demo fallida:** [ ] Sí / [ ] No
  - Si sí: [Cliente/Contexto]
- **Tiempo de downtime:** [X minutos/horas] o [ ] N/A
- **Requests fallidos:** [Número] o [ ] N/A

### Impacto de negocio:
- [ ] Cliente potencial perdido
- [ ] Credibilidad dañada
- [ ] Tiempo perdido debuggeando: [X horas]
- [ ] Otro: [Especificar]

---

## 5. POR QUÉ NO LO DETECTAMOS ANTES

### Análisis de prevención fallida:

- [ ] **¿Faltaba test?**
  - Si sí: ¿Qué test específico habría detectado esto?

- [ ] **¿Test existía pero no cubría este caso?**
  - Si sí: ¿Por qué el test no lo cubrió?

- [ ] **¿Smoke test no lo encontró?**
  - Si sí: ¿Por qué no? ¿Faltaba un paso en el smoke test?

- [ ] **¿QA Lead checklist no lo previno?**
  - Si sí: ¿Qué pregunta del checklist debería haberlo detectado?

- [ ] **¿Pre-demo checklist no lo encontró?**
  - Si sí: ¿Qué item del checklist falló?

### Análisis honesto:
[Explicación sin blame - enfocado en proceso, no en personas]

---

## 6. FIX APLICADO

### Descripción del fix:
[Explicación de cómo se solucionó]

### Código cambiado:
```python
# ANTES (con bug)
[código original]

# DESPUÉS (fix)
[código corregido]
```

**Commit del fix:** [hash/link]
**PR del fix:** [link si aplica]

### ¿Es fix definitivo o parche temporal?
- [ ] Fix definitivo (soluciona root cause)
- [ ] Parche temporal (mitiga síntoma)
  - Si parche: ¿Cuándo se implementará fix definitivo? [Fecha/Ticket]

---

## 7. PREVENCIÓN

### Tests Agregados:

- [ ] **Test unitario:** `tests/test_[nombre].py`
  - ¿Qué valida?: [Descripción]
  - Estado: [ ] Implementado / [ ] Pendiente

- [ ] **Test de integración:** `tests/integration/test_[nombre].py`
  - ¿Qué valida?: [Descripción]
  - Estado: [ ] Implementado / [ ] Pendiente

- [ ] **Smoke test actualizado:**
  - Paso agregado: [Descripción]
  - Estado: [ ] Implementado / [ ] Pendiente

### Validaciones Agregadas:

- [ ] **Validación en:** `[archivo:función]`
  - ¿Qué valida ahora?: [Descripción]
  - Estado: [ ] Implementado / [ ] Pendiente

- [ ] **Defensive pattern agregado:**
  - Dónde: [Ubicación]
  - Qué hace: [Descripción]
  - Estado: [ ] Implementado / [ ] Pendiente

### Documentación Actualizada:

- [ ] **README actualizado:** [Qué se agregó]
- [ ] **Playbook actualizado:** [Nuevo prompt/regla/ejemplo]
- [ ] **Comments en código:** [Dónde se agregaron warnings]

### Prompts/Checklists Mejorados:

- [ ] **QA Lead checklist:** [Nueva pregunta agregada]
- [ ] **Pre-demo checklist:** [Nuevo item agregado]
- [ ] **Smoke test:** [Nuevo paso agregado]

---

## 8. LEARNING

### ¿Qué aprendimos?
[Reflexión sobre el learning técnico y de proceso]

**Technical learning:**
[Qué aprendimos sobre el código/arquitectura/tecnología]

**Process learning:**
[Qué aprendimos sobre nuestro proceso de desarrollo]

### ¿Hay otros lugares con el mismo patrón vulnerable?

**Archivos/funciones revisados:**
- [ ] `[archivo1.py:función()]` - Estado: ✅ Seguro / ⚠️ Vulnerable → Fixed
- [ ] `[archivo2.py:función()]` - Estado: ✅ Seguro / ⚠️ Vulnerable → Fixed
- [ ] `[archivo3.py:función()]` - Estado: ✅ Seguro / ⚠️ Vulnerable → Fixed

**Patrón encontrado:**
[Descripción del anti-pattern que se repite]

### ¿Necesitamos cambiar proceso de desarrollo?

- [ ] **Sí** - Cambio propuesto:
  - [Descripción del cambio de proceso]
  - [Dónde documentar: Playbook/Reglas/Workflow]

- [ ] **No** - El proceso actual es correcto, solo no se siguió

---

## 9. ACTION ITEMS

- [ ] **[Acción 1]**
  - Owner: [Nombre]
  - Deadline: [Fecha]
  - Priority: P0 / P1 / P2
  - Status: [ ] Todo / [ ] In Progress / [ ] Done

- [ ] **[Acción 2]**
  - Owner: [Nombre]
  - Deadline: [Fecha]
  - Priority: P0 / P1 / P2
  - Status: [ ] Todo / [ ] In Progress / [ ] Done

- [ ] **[Acción 3]**
  - Owner: [Nombre]
  - Deadline: [Fecha]
  - Priority: P0 / P1 / P2
  - Status: [ ] Todo / [ ] In Progress / [ ] Done

---

## 10. CATEGORIZACIÓN

### Tipo de bug:
- [ ] Lógica incorrecta
- [ ] Validación faltante
- [ ] Error handling faltante
- [ ] Race condition
- [ ] Estado corrupto
- [ ] Credential/Auth
- [ ] Performance
- [ ] UI/UX
- [ ] Otro: [Especificar]

### Fase donde debió detectarse:
- [ ] QA Lead checklist
- [ ] Implementación (test unitario)
- [ ] Code review
- [ ] Pre-demo checklist
- [ ] Smoke test
- [ ] Producción (inevitable)

### Severidad vs Urgencia:
```
Severidad: [ALTA/MEDIA/BAJA]
Urgencia: [ALTA/MEDIA/BAJA]

Matriz:
- Alta severidad + Alta urgencia = 🔴 CRÍTICO
- Alta severidad + Baja urgencia = 🟡 IMPORTANTE
- Baja severidad + Alta urgencia = 🟠 URGENTE
- Baja severidad + Baja urgencia = 🟢 MENOR
```

---

## 11. FIRMA

**Autor del post-mortem:** Gonzalo Haedo
**Fecha de creación:** [YYYY-MM-DD]
**Última actualización:** [YYYY-MM-DD]
**Revisado por:** [Claude Code / Otro]

**Estado del post-mortem:**
- [ ] Draft (incompleto)
- [ ] Completado (listo para archivar)
- [ ] Archivado (action items completados)

---

## 12. REFERENCIAS

**Links relevantes:**
- Commit que introdujo el bug: [link]
- PR del fix: [link]
- Issue relacionado: [link]
- Demo fallida: [video/screenshot]
- Conversación de debugging: [link a Slack/Discord]

---

**Nota:** Este post-mortem es parte del Nordia Engineering Playbook v1.

**No es blame game. Es aprendizaje sistemático.**

Los bugs son inevitables. No aprender de ellos es opcional.

---

**Template Version:** 1.0
**Last Updated:** 2026-01-31
