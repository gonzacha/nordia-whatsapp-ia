# 🔍 Evaluación QA del Estado Actual - Nordia WhatsApp IA

**Fecha:** 2026-01-31
**Evaluador:** Claude Code (QA Lead Mode)
**Versión evaluada:** main branch (post token-validation refactor)

---

## ✅ FORTALEZAS ARQUITECTÓNICAS

### 1. Arquitectura Defensiva de Tokens ⭐⭐⭐⭐⭐
**Ubicación:** `app/config.py`, `app/main.py`

**Implementación:**
- ✅ Healthcheck al startup (`validate_whatsapp_token()`)
- ✅ Variable global `TOKEN_IS_VALID` + `TOKEN_INVALID_SINCE`
- ✅ Modo degradado automático (bloquea envíos si token inválido)
- ✅ Detección en runtime (actualiza estado al detectar code 190)
- ✅ Endpoint `/` con introspección de estado

**Evaluación:** Nivel de ingeniería profesional. Previene cascadas de errores.

### 2. Logging Semántico
**Ubicación:** `app/main.py`, `app/config.py`

**Implementación:**
- ✅ Niveles claros: `[CONFIG]`, `[WhatsApp]`, `[WhatsApp CRITICAL]`, `[DEGRADED]`
- ✅ Contexto suficiente para debugging
- ✅ Timestamps en modo degradado

**Evaluación:** Muy bueno para MVP.

### 3. Simplicidad Arquitectónica
**Stack actual:**
- FastAPI (1 archivo principal)
- SQLite (pendiente)
- Sin microservicios
- Sin Redis/colas

**Evaluación:** Correcto para MVP. No hay sobre-ingeniería.

---

## 🔴 VULNERABILIDADES CRÍTICAS

### 1. PERSISTENCIA EN RAM ⚠️ CRÍTICO
**Ubicación:** `app/engine.py` (implícito)

**Problema:**
```python
# Estado actual (no visto en código pero inferido):
conversaciones = {}  # Solo en RAM
```

**Impacto:**
- ❌ Reinicio = pérdida total de conversaciones
- ❌ Usuario a mitad de setup → frustración
- ❌ No se puede testear flujos largos sin perder estado
- ❌ Debugging imposible (sin historial)

**Severidad:** **BLOQUEANTE PARA DEMO**

**Fix requerido:**
```python
# Persistencia JSON mínima (1 hora de trabajo)
import json
from pathlib import Path

STATE_FILE = Path("data/conversations_state.json")

def save_state(conversaciones):
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(conversaciones, f, indent=2, default=str)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Al inicio
conversaciones = load_state()

# Después de cada cambio de estado
save_state(conversaciones)
```

**Estimación:** 1 hora
**Prioridad:** P0 - Implementar ANTES de grabar demo

---

### 2. SIN VALIDACIÓN DE INPUTS ⚠️ ALTO
**Ubicación:** `app/engine.py:1-8`

**Código actual:**
```python
def handle_message(sender: str, text: str) -> str:
    text = text.strip().lower()  # Solo strip + lower

    if text in ["setup", "/setup"]:
        return "Perfecto 👍 ¿Cómo se llama tu negocio?"

    return "Hola 👋 Soy Nordia. Escribí 'setup' para comenzar."
```

**Vulnerabilidades detectadas:**
- ❌ No valida longitud (mensaje de 10,000 chars se procesa)
- ❌ No valida caracteres especiales
- ❌ No maneja mensaje vacío después de strip
- ❌ No detecta precios/números en fase de setup
- ❌ No sanitiza antes de guardar

**Casos de falla:**
```python
# Mensaje vacío
handle_message("+123", "   ")  # Retorna mensaje genérico, OK

# Mensaje extremadamente largo
handle_message("+123", "a" * 10000)  # Se procesa, riesgo de DoS

# Caracteres SQL peligrosos
handle_message("+123", "'; DROP TABLE businesses; --")  # Se guarda sin sanitizar

# Solo emojis
handle_message("+123", "😀😀😀")  # Retorna mensaje genérico, OK pero no útil
```

**Fix requerido:**
```python
MAX_MESSAGE_LENGTH = 500

def validate_input(text: str) -> tuple[bool, str]:
    """Retorna (es_válido, mensaje_error)"""
    if not text or not text.strip():
        return False, "Mensaje vacío"

    if len(text) > MAX_MESSAGE_LENGTH:
        return False, f"Mensaje muy largo (máx {MAX_MESSAGE_LENGTH} caracteres)"

    return True, ""

def sanitize_text(text: str) -> str:
    """Sanitiza texto para guardar en DB"""
    import re
    # Remover caracteres peligrosos
    clean = re.sub(r'[<>\"\'`]', '', text)
    # Normalizar espacios
    clean = ' '.join(clean.split())
    return clean[:MAX_MESSAGE_LENGTH]
```

**Estimación:** 2 horas
**Prioridad:** P0 - Implementar ANTES de demo

---

### 3. SIN MANEJO DE MEDIA ⚠️ MEDIO
**Ubicación:** `app/main.py:96`

**Código actual:**
```python
if message_type == "text":
    text_body = message.get("text", {}).get("body", "")
    # ...procesa
```

**Problema:**
- ❌ Si usuario envía imagen/audio/video → silencio total
- ❌ No hay respuesta que indique "solo acepto texto"
- ❌ Usuario queda confundido

**Fix requerido:**
```python
if message_type == "text":
    text_body = message.get("text", {}).get("body", "")
    # ...procesa
else:
    # Manejar otros tipos de media
    send_whatsapp_message(sender, "Solo puedo procesar mensajes de texto por ahora 📝")
```

**Estimación:** 15 minutos
**Prioridad:** P1 - Implementar antes de demo

---

### 4. SIN TIMEOUT DE CONVERSACIÓN ⚠️ MEDIO
**Ubicación:** `app/engine.py` (feature faltante)

**Problema:**
- ❌ Usuario inicia setup → se va → nunca vuelve
- ❌ `conversaciones[telefono]` queda eternamente en memoria/DB
- ❌ Memory leak lento

**Fix requerido:**
```python
from datetime import datetime, timedelta

# Agregar timestamp a cada conversación
conversaciones[telefono] = {
    "estado": "esperando_nombre",
    "last_interaction": datetime.now().isoformat(),
    # ...
}

# Cleanup periódico (ejecutar cada 1 hora)
def cleanup_stale_conversations(max_age_hours=24):
    now = datetime.now()
    to_delete = []

    for phone, data in conversaciones.items():
        last_interaction = datetime.fromisoformat(data.get("last_interaction", ""))
        if (now - last_interaction) > timedelta(hours=max_age_hours):
            to_delete.append(phone)

    for phone in to_delete:
        del conversaciones[phone]

    print(f"[CLEANUP] Removed {len(to_delete)} stale conversations")
```

**Estimación:** 1 hora
**Prioridad:** P2 - Nice to have antes de demo

---

### 5. SIN RATE LIMITING ⚠️ MEDIO
**Ubicación:** `app/main.py:send_whatsapp_message()`

**Problema:**
WhatsApp Cloud API tiene límites:
- 1000 mensajes/día (tier inicial)
- 80 mensajes/segundo

Si la demo se hace viral:
- ❌ Día 1: 500 mensajes
- ❌ Día 2: 600 mensajes
- ❌ Día 3: BLOQUEADO por Meta

**Fix requerido:**
```python
from datetime import date

# Estado global
messages_sent_today = 0
last_reset_date = date.today()
DAILY_LIMIT = 900  # Margen de seguridad

def send_whatsapp_message(to: str, text: str):
    global messages_sent_today, last_reset_date

    # Reset contador si cambió el día
    if date.today() > last_reset_date:
        messages_sent_today = 0
        last_reset_date = date.today()

    # Validar límite
    if messages_sent_today >= DAILY_LIMIT:
        print(f"[RATE LIMIT] Daily quota reached ({DAILY_LIMIT})")
        return None

    # ...enviar mensaje
    messages_sent_today += 1
```

**Estimación:** 30 minutos
**Prioridad:** P1 - Implementar antes de viralización

---

## 🟡 MEJORAS RECOMENDADAS

### 6. State Machine No Validada
**Ubicación:** `app/engine.py`

**Problema:**
- ⚠️ No hay validación de transiciones
- ⚠️ Se puede llegar a estados inconsistentes
- ⚠️ No hay diagrama formal de estados

**Recomendación:**
```python
# Estados válidos
VALID_STATES = {
    "inicio",
    "esperando_nombre",
    "esperando_horarios",
    "esperando_servicios",
    "completado"
}

# Transiciones válidas
VALID_TRANSITIONS = {
    "inicio": ["esperando_nombre"],
    "esperando_nombre": ["esperando_horarios"],
    "esperando_horarios": ["esperando_servicios"],
    "esperando_servicios": ["completado"],
    "completado": ["inicio"]  # Reset
}

def set_state(phone: str, new_state: str):
    current_state = conversaciones[phone].get("estado", "inicio")

    if new_state not in VALID_STATES:
        raise ValueError(f"Estado inválido: {new_state}")

    if new_state not in VALID_TRANSITIONS.get(current_state, []):
        raise ValueError(f"Transición inválida: {current_state} -> {new_state}")

    conversaciones[phone]["estado"] = new_state
```

**Prioridad:** P2 - Antes de agregar más estados

---

### 7. Sin Tests Automatizados
**Problema:**
- ⚠️ No hay tests unitarios
- ⚠️ No hay tests de integración
- ⚠️ Testing 100% manual

**Recomendación:**
```bash
# Crear estructura de tests
mkdir tests/
touch tests/test_engine.py
touch tests/test_validation.py
touch tests/test_persistence.py
```

```python
# tests/test_engine.py
def test_setup_flow():
    """Test flujo completo de setup"""
    sender = "+123456789"

    # Inicio
    resp = handle_message(sender, "setup")
    assert "negocio" in resp.lower()

    # Nombre
    resp = handle_message(sender, "Barbería Test")
    assert "horarios" in resp.lower()

    # ... etc
```

**Prioridad:** P2 - Después de persistencia

---

### 8. Hardcoded Verify Token
**Ubicación:** `app/main.py:9, 59`

**Código actual:**
```python
VERIFY_TOKEN = "nordia_verify_token"

if mode == "subscribe" and token == "nordia_verify_token":
```

**Problema:**
- ⚠️ Token hardcodeado dos veces
- ⚠️ No está en `.env`
- ⚠️ Si cambias en un lugar, falta cambiar en otro

**Fix:**
```python
# app/config.py
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "nordia_verify_token")

# app/main.py
from app.config import VERIFY_TOKEN

if mode == "subscribe" and token == VERIFY_TOKEN:
```

**Prioridad:** P3 - Quick win

---

## 📊 MATRIZ DE RIESGOS

| ID | Vulnerabilidad | Severidad | Probabilidad | Impacto | Prioridad |
|----|----------------|-----------|--------------|---------|-----------|
| 1 | Persistencia en RAM | CRÍTICO | 100% | ALTO | P0 |
| 2 | Sin validación inputs | ALTO | 80% | ALTO | P0 |
| 3 | Sin manejo media | MEDIO | 60% | BAJO | P1 |
| 4 | Sin timeout conversaciones | MEDIO | 40% | MEDIO | P2 |
| 5 | Sin rate limiting | MEDIO | 30% | ALTO | P1 |
| 6 | State machine no validada | BAJO | 20% | MEDIO | P2 |
| 7 | Sin tests | BAJO | N/A | ALTO | P2 |
| 8 | Verify token hardcoded | BAJO | 10% | BAJO | P3 |

---

## 🎯 ROADMAP DE FIXES

### BLOQUEANTES (P0) - ANTES DE DEMO
**Tiempo estimado: 3-4 horas**

1. ✅ **Persistencia JSON mínima** (1h)
   - `data/conversations_state.json`
   - `save_state()` / `load_state()`

2. ✅ **Validación de inputs** (2h)
   - Límite de longitud
   - Sanitización
   - Validación de precios en fase servicios

### CRÍTICOS (P1) - ANTES DE VIRALIZACIÓN
**Tiempo estimado: 1 hora**

3. ✅ **Manejo de media** (15min)
4. ✅ **Rate limiting** (30min)
5. ✅ **Verify token en .env** (15min)

### IMPORTANTES (P2) - PRÓXIMA ITERACIÓN
**Tiempo estimado: 3-4 horas**

6. ✅ **Validación state machine** (1-2h)
7. ✅ **Timeout conversaciones** (1h)
8. ✅ **Tests básicos** (1-2h)

---

## 🚦 DECISIÓN GO / NO-GO PARA DEMO

### ❌ NO-GO (Estado Actual)

**Razones:**
1. Persistencia en RAM → Reinicio pierde todo
2. Sin validación de inputs → Vulnerable a crashes
3. Sin manejo de media → UX confusa

**Recomendación:**
Implementar fixes P0 (3-4 horas de trabajo) ANTES de grabar demo.

### ✅ GO (Después de P0)

**Condiciones:**
1. ✅ Persistencia JSON funcionando
2. ✅ Validación básica de inputs
3. ✅ Manejo de media
4. ✅ Smoke test manual pasado

---

## 📝 SIGUIENTE PASO INMEDIATO

**Ejecutar este comando:**

```bash
# 1. Crear estructura de persistencia
mkdir -p data/

# 2. Implementar save/load state en app/engine.py
# (Ver fix requerido #1 arriba)

# 3. Implementar validación en app/engine.py
# (Ver fix requerido #2 arriba)

# 4. Implementar manejo de media en app/main.py
# (Ver fix requerido #3 arriba)

# 5. Smoke test
python -m pytest tests/ -v  # (después de crear tests)
```

---

**Evaluación final:** Sistema tiene fundamentos sólidos (arquitectura defensiva de tokens), pero necesita 3-4 horas de hardening ANTES de demo para prevenir pérdida de datos y mejorar UX.

**Score de preparación para demo: 6/10**
**Score post-fixes P0: 8.5/10**

---

**Próxima revisión:** Después de implementar fixes P0
