# 📚 Biblioteca de Prompts - Nordia WhatsApp IA

Colección de prompts de ingeniería diseñados para prevenir bugs y mantener disciplina de calidad.

---

## 🎯 Filosofía

> **"Prevenir bugs, no arreglarlos después"**

Esta biblioteca te ayuda a:
- ✅ Detectar problemas ANTES de escribir código
- ✅ Mantener arquitectura defensiva
- ✅ Forzar disciplina de ingeniería
- ✅ Prevenir fragilidad en el MVP

---

## 🚀 Inicio Rápido

### Usar script helper (recomendado)

```bash
# Listar todos los prompts disponibles
python .nordia/prompt_helper.py list

# Activar QA Lead Mode (el más importante)
python .nordia/prompt_helper.py qa-lead

# Checklist antes de demo
python .nordia/prompt_helper.py pre-demo

# Análisis post-bug
python .nordia/prompt_helper.py post-mortem
```

### Uso manual

```bash
# Leer prompt directamente
cat .nordia/prompts/META_PROMPT_QA_LEAD.md

# Copiar y pegar en Claude Code
```

---

## 📁 Estructura

```
.nordia/prompts/
├── META_PROMPT_QA_LEAD.md           ⭐ MÁS IMPORTANTE - USAR SIEMPRE
├── 01_architecture_review/
│   ├── auditoria_defensiva.md
│   └── validacion_kiss.md
├── 02_failure_analysis/
│   ├── modos_de_falla.md
│   └── simulacion_caos.md
├── 05_input_validation/
│   └── hardening_validacion.md
├── 06_defensive_programming/
│   └── patrones_defensivos.md
├── 08_feature_checklist/
│   └── pre_feature_checklist.md
├── 09_pre_demo/
│   ├── checklist_pre_demo.md
│   └── smoke_test_manual.md
├── 10_post_bug/
│   └── post_mortem.md
└── README.md (este archivo)
```

---

## 🎖️ El Prompt Más Importante

### META_PROMPT_QA_LEAD.md

**Úsalo ANTES de escribir código para CUALQUIER feature.**

Este prompt activa el "Modo QA Lead" que te obliga a completar un checklist de 6 pasos:

1. ¿Qué problema resuelve?
2. ¿Cuál es la solución mínima?
3. ¿Qué impacto tiene?
4. ¿Qué riesgos existen?
5. ¿Cómo lo testeo?
6. ¿Es defensivo?

**Regla de Oro:** Si no podés completar el checklist → la feature no está bien definida → NO escribir código.

```bash
python .nordia/prompt_helper.py qa-lead
```

---

## 📊 Workflow Recomendado

```
┌────────────────────────────────────┐
│ ANTES DE CUALQUIER FEATURE         │
├────────────────────────────────────┤
│ 1. QA Lead Mode ⭐                 │
│ 2. Completar checklist             │
│ 3. Si pasa → Continuar             │
│ 4. Si no → Redefinir               │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ DURANTE IMPLEMENTACIÓN             │
├────────────────────────────────────┤
│ 5. Input Validation                │
│ 6. Defensive Programming           │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ ANTES DE MERGEAR                   │
├────────────────────────────────────┤
│ 7. Failure Mode Analysis           │
│ 8. Architecture Audit              │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ ANTES DE DEMO/DEPLOY               │
├────────────────────────────────────┤
│ 9. Pre-Demo Checklist              │
│ 10. Smoke Test Manual              │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ DESPUÉS DE BUG                     │
├────────────────────────────────────┤
│ 11. Post-Mortem                    │
└────────────────────────────────────┘
```

---

## 📖 Catálogo de Prompts

### 🎖️ Meta

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `qa-lead` | `META_PROMPT_QA_LEAD.md` | ⭐ ANTES de cualquier feature |

### 🏗️ Architecture Review

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `arch-audit` | `auditoria_defensiva.md` | Cada 2-3 features nuevas |
| `kiss` | `validacion_kiss.md` | Cuando código se complica |

### 💥 Failure Analysis

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `failure-modes` | `modos_de_falla.md` | Antes de cada deploy |
| `chaos` | `simulacion_caos.md` | Features críticas |

### ✅ Input Validation

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `input-validation` | `hardening_validacion.md` | Antes de release |

### 🛡️ Defensive Programming

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `defensive` | `patrones_defensivos.md` | En code reviews |

### ➕ Feature Addition

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `pre-feature` | `pre_feature_checklist.md` | Antes de implementar |

### 🎬 Pre-Demo

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `pre-demo` | `checklist_pre_demo.md` | 24h antes de demo |
| `smoke-test` | `smoke_test_manual.md` | Después de deploy |

### 🔍 Post-Bug

| Comando | Archivo | Cuándo usar |
|---------|---------|-------------|
| `post-mortem` | `post_mortem.md` | Después de cada bug |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Agregar nueva feature

```bash
# Usuario quiere: "Notificaciones al dueño cuando hay turno"

# 1. Activar QA Lead Mode
python .nordia/prompt_helper.py qa-lead

# 2. Pegar en Claude Code
# Claude completa checklist:
# ✅ Problema claro
# ✅ Solución mínima definida
# ✅ Archivos a modificar: app/engine.py, app/main.py
# ✅ Riesgos identificados
# ✅ Tests definidos
# ✅ Defensivo

# 3. Claude genera código solo después de checklist completo
```

### Ejemplo 2: Antes de grabar demo

```bash
# 24 horas antes de demo

# 1. Ejecutar pre-demo checklist
python .nordia/prompt_helper.py pre-demo

# Claude valida:
# ✅ Persistencia
# ✅ Validación
# ❌ Performance lenta (8s, objetivo 5s)
# Decisión: NO-GO - Optimizar primero

# 2. Después de fix, smoke test
python .nordia/prompt_helper.py smoke-test

# Claude ejecuta flujo completo manualmente
# Resultado: 14/15 tests ✅ → GO
```

### Ejemplo 3: Bug en producción

```bash
# Bug: Token expirado durante demo

# 1. Post-mortem
python .nordia/prompt_helper.py post-mortem

# Claude genera:
# - Timeline del bug
# - Root cause analysis (5 Whys)
# - Impacto cuantificado
# - Fix implementado
# - Action items para prevenir
```

---

## 🎓 Mejores Prácticas

### ✅ DO

- **Usar QA Lead Mode SIEMPRE** antes de escribir código
- Completar checklist ANTES de implementar
- Ejecutar pre-demo 24h antes (no 1h antes)
- Hacer post-mortem de TODOS los bugs (no solo críticos)

### ❌ DON'T

- Saltar el checklist "porque es simple"
- Implementar features mal definidas
- Deployar sin smoke test
- Ignorar bugs "pequeños"

---

## 🔧 Integración con Workflow

### Git Hook (recomendado)

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "🎖️ Validando QA checklist..."
python .nordia/qa_validator.py

if [ $? -ne 0 ]; then
    echo "❌ QA checklist incompleto"
    echo "Ejecutá: python .nordia/prompt_helper.py qa-lead"
    exit 1
fi
```

### VS Code Snippet

```json
{
  "QA Lead Mode": {
    "prefix": "qalead",
    "body": [
      "# QA Lead Mode Checklist",
      "python .nordia/prompt_helper.py qa-lead"
    ]
  }
}
```

---

## 📈 Métricas de Éxito

Medir impacto de usar la biblioteca:

- **Bugs en producción:** Objetivo <1 por sprint
- **Demo failures:** Objetivo 0
- **Time to fix bug:** Objetivo <1h (gracias a post-mortem)
- **Code review time:** Reducción 30% (gracias a defensive patterns)

---

## 🆘 Ayuda

### ¿Qué prompt usar?

```bash
# Listar todos
python .nordia/prompt_helper.py list

# Ver contenido de uno
python .nordia/prompt_helper.py [comando]
```

### ¿Cuándo usar cada uno?

Ver tabla en sección **Catálogo de Prompts** arriba.

### ¿Cómo contribuir con nuevos prompts?

1. Crear archivo en categoría correspondiente
2. Seguir formato existente (ver cualquier .md)
3. Agregar a `PROMPT_MAP` en `prompt_helper.py`
4. Actualizar este README

---

## 📝 Formato de Prompt

Todos los prompts siguen este formato:

```markdown
# Título del Prompt

## Cuándo usar
[Descripción]

## Severidad
[CRITICAL/HIGH/MEDIUM/LOW]

---

## Prompt
```
[Texto completo listo para copiar]
```

---

## Output esperado
[Qué debe retornar Claude]

---

## Ejemplo de uso
[Ejemplo concreto]
```

---

## 🔗 Referencias

- **Quality directory:** `/quality/` - JSONs estructurados con evaluaciones
- **Current state assessment:** `/quality/CURRENT_STATE_ASSESSMENT.md`
- **Biblioteca original:** Ver conversación con ChatGPT/Claude

---

**Última actualización:** 2026-01-31
**Versión:** 1.0.0
**Mantenedor:** Gonza

---

## 🎯 Regla de Oro Final

> **Si solo vas a hacer UNA cosa de esta biblioteca:**
>
> **Usar QA Lead Mode antes de CADA feature**
>
> ```bash
> python .nordia/prompt_helper.py qa-lead
> ```

**Esto solo prevendrá el 80% de los bugs.**
