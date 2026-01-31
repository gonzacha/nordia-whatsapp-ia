# 📚 Quality Assurance Library - Nordia WhatsApp IA

Biblioteca de prompts estructurados para asegurar calidad, arquitectura defensiva y prevención de bugs.

## 📁 Estructura

```
quality/
├── 00_META_QA_LEAD_MODE.json          # ⭐ USAR ANTES DE CUALQUIER FEATURE
├── 01_architecture_review.json         # Auditorías de arquitectura
├── 02_failure_mode_analysis.json       # Análisis de modos de falla
├── 03_persistence_data_integrity.json  # Validación de persistencia
├── 04_state_machine_design.json        # Diseño de máquina de estados
├── 05_input_validation.json            # Validación y sanitización
├── 06_defensive_programming.json       # Patrones defensivos
├── 07_refactor_safety.json             # Seguridad en refactors
├── 08_feature_addition.json            # Checklist de features
├── 09_pre_demo_hardening.json          # Validación pre-demo
└── 10_post_bug_autopsy.json            # Post-mortem de bugs
```

## 🎯 Workflow Recomendado

### ANTES de cualquier feature
1. **Activar QA Lead Mode** (`00_META_QA_LEAD_MODE.json`)
2. Completar checklist obligatorio
3. Si pasa → Continuar | Si no → Redefinir

### DURANTE implementación
4. **Input Validation** (`05_input_validation.json`)
5. **Defensive Programming** (`06_defensive_programming.json`)
6. **State Machine** (`04_state_machine_design.json` - si aplica)

### ANTES de mergear
7. **Failure Mode Analysis** (`02_failure_mode_analysis.json`)
8. **Persistence Audit** (`03_persistence_data_integrity.json` - si tocó datos)
9. **Refactor Safety** (`07_refactor_safety.json` - si refactor grande)

### ANTES de demo/deploy
10. **Pre-Demo Checklist** (`09_pre_demo_hardening.json`)
11. **Smoke Test Manual** (`09_pre_demo_hardening.json`)
12. **Chaos Simulation** (`02_failure_mode_analysis.json` - features críticas)

### DESPUÉS de cualquier bug
13. **Post-Mortem** (`10_post_bug_autopsy.json`)
14. **Proactive Prevention** (`10_post_bug_autopsy.json`)

## 🚀 Cómo Usar

### Método 1: Claude Code CLI
```bash
# Leer el prompt que necesitas
cat quality/00_META_QA_LEAD_MODE.json | jq -r '.prompt.role'

# Copiar y pegar el contenido en conversación con Claude Code
```

### Método 2: Python Script
```python
import json

# Cargar prompt
with open('quality/09_pre_demo_hardening.json') as f:
    data = json.load(f)

# Obtener prompt específico
checklist = data['prompts'][0]  # Pre-Demo Checklist
print(checklist['prompt'])
```

### Método 3: Integración en Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validar que se completó QA checklist antes de commit
python scripts/validate_qa_checklist.py
```

## 📊 Severidades

- **CRITICAL**: Bloqueante, ejecutar SIEMPRE
- **HIGH**: Muy recomendado, ejecutar en features importantes
- **MEDIUM**: Recomendado, ejecutar periódicamente

## 🎖️ Regla de Oro

> **Nunca escribir código sin completar el checklist del QA Lead Mode**

Si el checklist no se puede completar → la feature no está bien definida.

## 📝 Ejemplo de Uso

```bash
# Quiero agregar feature "Notificaciones al dueño"

# 1. Activar QA Lead Mode
cat quality/00_META_QA_LEAD_MODE.json

# 2. Responder checklist:
# ✅ Problema: Dueño no sabe cuándo hay nuevo turno
# ✅ Solución mínima: WhatsApp message al dueño
# ✅ Archivos: app/engine.py, app/main.py
# ✅ Tests: 5 casos definidos
# ✅ Rollback: Feature flag NOTIFICATIONS_ENABLED

# 3. Implementar con defensive programming
cat quality/06_defensive_programming.json

# 4. Antes de demo, validar
cat quality/09_pre_demo_hardening.json
```

## 🔥 Estado Actual del Sistema

Para generar reporte del estado actual, ejecutar:

```bash
python scripts/generate_qa_report.py
```

---

**Última actualización:** 2026-01-31
**Versión:** 1.0.0
