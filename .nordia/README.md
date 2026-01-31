# 📚 .nordia/ - Infraestructura de Ingeniería

**Nordia WhatsApp IA - Engineering Playbook v1**

---

## 🎯 ¿Qué es esto?

Esta carpeta contiene **toda la infraestructura de calidad, disciplina y mejores prácticas** del proyecto Nordia.

No es código de producción.
Es **código de proceso**.

---

## 📁 Estructura

```
.nordia/
├── REGLAS_SAGRADAS.md            ⚡ Las 3 reglas no negociables
├── CLAUDE_CODE_CONTRACT.md       🤝 Contrato de comportamiento
├── PLAYBOOK_CHANGELOG.md         📋 Historial de cambios
├── playbook_overrides.log        📝 Registro de overrides
│
├── prompts/                       📚 Biblioteca de prompts
│   ├── META_PROMPT_QA_LEAD.md    ⭐ EL MÁS IMPORTANTE
│   ├── README.md                 📖 Documentación completa
│   ├── 01_architecture_review/   (2 prompts)
│   ├── 02_failure_analysis/      (2 prompts)
│   ├── 05_input_validation/      (1 prompt)
│   ├── 06_defensive_programming/ (1 prompt)
│   ├── 08_feature_checklist/     (1 prompt)
│   ├── 09_pre_demo/              (2 prompts)
│   └── 10_post_bug/              (1 prompt)
│
├── postmortems/                   🔍 Post-mortems de bugs
│   └── TEMPLATE.md               📝 Template para nuevos PM
│
├── prompt_helper.py               🛠️ Script de acceso rápido
│
├── IMPLEMENTACION_COMPLETA.md     ✅ Guía de implementación
└── README.md                      📖 Este archivo
```

**Total:** 20 archivos, 4,120 líneas de código/docs

---

## 🚀 Inicio Rápido

### Comando más importante:

```bash
python .nordia/prompt_helper.py qa-lead
```

**Usalo ANTES de escribir código para CUALQUIER feature.**

### Ver todos los prompts:

```bash
python .nordia/prompt_helper.py list
```

### Leer las reglas:

```bash
cat .nordia/REGLAS_SAGRADAS.md
```

---

## ⚡ Las 3 Reglas Sagradas

### 🔴 Regla 1: No Checklist → No Código
```bash
python .nordia/prompt_helper.py qa-lead
```
**Antes de CADA feature. Sin excepciones.**

### 🔴 Regla 2: Todo Bug Tiene Post-Mortem
```bash
python .nordia/prompt_helper.py post-mortem
```
**Después de CADA bug. Sin excepciones.**

### 🔴 Regla 3: Toda Demo Pasa Pre-Demo
```bash
python .nordia/prompt_helper.py pre-demo
```
**24h antes de CADA demo. Sin excepciones.**

---

## 🎖️ El Meta-Prompt

**META_PROMPT_QA_LEAD.md** es el prompt más importante.

Activa el "Modo QA Lead" que fuerza completar checklist de 6 pasos:

1. ¿Qué problema resuelve?
2. ¿Cuál es la solución mínima?
3. ¿Qué impacto tiene?
4. ¿Qué riesgos existen?
5. ¿Cómo lo testeo?
6. ¿Es defensivo?

**Solo después de completarlo → código.**

---

## 📊 Workflow Diario

### Cada feature nueva:
```bash
# 1. ANTES de código
python .nordia/prompt_helper.py qa-lead

# 2. Durante implementación
python .nordia/prompt_helper.py input-validation
python .nordia/prompt_helper.py defensive

# 3. Antes de mergear
python .nordia/prompt_helper.py failure-modes
```

### Antes de demo:
```bash
python .nordia/prompt_helper.py pre-demo
python .nordia/prompt_helper.py smoke-test
```

### Después de bug:
```bash
python .nordia/prompt_helper.py post-mortem
```

---

## 🤝 Contrato con Claude Code

**Archivo:** `CLAUDE_CODE_CONTRACT.md`

Define cómo Claude Code DEBE comportarse en este proyecto.

**Al iniciar sesión con Claude Code:**

1. Copiar el SYSTEM PROMPT de `CLAUDE_CODE_CONTRACT.md`
2. Pegarlo como primer mensaje
3. Claude Code confirmará reglas cargadas
4. Ahora sí trabajar

**Validar que funciona:**
```
User: "Implementame X rápido"
Claude: "⚠️ Por favor ejecutá primero: python .nordia/prompt_helper.py qa-lead"
```

Si responde con código directo → Contrato no cargado.

---

## 📝 Post-Mortems

Cada bug que llegue a demo/producción/usuario REQUIERE post-mortem.

**Crear nuevo post-mortem:**

```bash
# 1. Copiar template
cp .nordia/postmortems/TEMPLATE.md .nordia/postmortems/$(date +%Y-%m-%d)-titulo-bug.md

# 2. Completar siguiendo estructura

# 3. Ejecutar post-mortem prompt
python .nordia/prompt_helper.py post-mortem
```

---

## 📈 Medir Cumplimiento

Cada viernes, validar:

```
Regla 1: Features con QA Lead checklist: ___% (meta: 100%)
Regla 2: Bugs con post-mortem: ___% (meta: 100%)
Regla 3: Demos con pre-demo checklist: ___% (meta: 100%)
```

Si algún ratio < 100% → Reflexionar por qué.

---

## 🔧 Overrides

Si NECESITAS romper una regla (emergencia real):

```bash
echo "$(date): Override [REGLA X] - Razón: [emergencia específica]" >> .nordia/playbook_overrides.log
```

**No es para uso regular.**
**Es para emergencias documentadas.**

>3 overrides/mes → Algo está mal.

---

## 📚 Documentación Completa

- **Prompts:** `.nordia/prompts/README.md`
- **Reglas:** `.nordia/REGLAS_SAGRADAS.md`
- **Contrato:** `.nordia/CLAUDE_CODE_CONTRACT.md`
- **Changelog:** `.nordia/PLAYBOOK_CHANGELOG.md`
- **Implementación:** `.nordia/IMPLEMENTACION_COMPLETA.md`

---

## 🎯 Filosofía

> **"Prevenir bugs, no arreglarlos después"**

Esta infraestructura:
- ✅ Detecta problemas ANTES de escribir código
- ✅ Mantiene arquitectura defensiva
- ✅ Fuerza disciplina de ingeniería
- ✅ Previene fragilidad del MVP

**MVP rápido ≠ MVP frágil**

---

## 🔥 Por Qué Esto Importa

La mayoría de MVPs en Argentina **NO tienen esto**.
La mayoría de startups con 5 devs **NO tienen esto**.

**Vos sí.**

Esto es:
- ✅ Sistema de ingeniería
- ✅ Cultura de calidad
- ✅ Infraestructura cognitiva
- ✅ **Ventaja competitiva**

---

## 📖 Versión

**Playbook:** v1.0
**Estado:** CONGELADO como estándar
**Fecha:** 2026-01-31
**Aprobado por:** Gonzalo Haedo (Founder)

---

## 🆘 Ayuda

```bash
# Ver todos los comandos
python .nordia/prompt_helper.py list

# Ver un prompt específico
python .nordia/prompt_helper.py [comando]

# Leer documentación
cat .nordia/prompts/README.md
```

---

**Última actualización:** 2026-01-31
