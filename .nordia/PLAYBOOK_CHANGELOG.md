# Nordia Engineering Playbook - Changelog

## Regla de Cambios

Todo cambio al Playbook requiere:
1. **Mini-postmortem:** ¿Por qué cambiar? ¿Qué falló del playbook anterior?
2. **Incremento de versión:** v1 → v1.1 (minor) o v2 (major)
3. **Documentación en este archivo:** Fecha, razón, cambios específicos

---

## v1.0 - 2026-01-31

**VERSIÓN INICIAL CANÓNICA**

### Componentes:
- Sistema de 11 prompts de ingeniería
- Meta-Prompt QA Lead (crítico)
- Script helper Python (`prompt_helper.py`)
- Workflow de 5 fases (pre-feature → implementación → pre-merge → pre-demo → post-bug)
- Biblioteca completa en `.nordia/prompts/`

### Filosofía fundacional:
- **No checklist → No código**
- **Todo bug tiene post-mortem**
- **Toda demo pasa pre-demo**

### Estructura:
```
.nordia/
├── prompts/              # 11 prompts Markdown
├── prompt_helper.py      # Script de acceso rápido
├── PLAYBOOK_CHANGELOG.md # Este archivo
├── REGLAS_SAGRADAS.md    # 3 reglas no negociables
└── CLAUDE_CODE_CONTRACT.md # Contrato de comportamiento
```

### Aprobado por:
**Gonzalo Haedo** (Founder)

### Estado:
**CONGELADO** como estándar v1

### Próximos cambios esperados:
- v1.1: Agregar prompts faltantes (persistence, state machine, refactor safety)
- v1.2: Integración con pre-commit hooks
- v2.0: Solo si falla algo fundamental del v1

---

## Reglas de Versionado

**Minor (v1.0 → v1.1):**
- Agregar nuevos prompts
- Mejorar documentación
- Agregar ejemplos
- No rompe workflow existente

**Major (v1.0 → v2.0):**
- Cambiar workflow fundamental
- Eliminar reglas sagradas
- Modificar filosofía core
- Requiere aprobación explícita

---

**Última actualización:** 2026-01-31
