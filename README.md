# Nordia WhatsApp IA

Sistema conversacional determinístico para activación y reactivación de clientes vía WhatsApp.

Nordia permite que un administrador genere mensajes comerciales personalizados para clientes inactivos. El sistema gestiona la conversación de forma estructurada, sin LLMs, usando una máquina de estados.

## Caso Principal

**Activación de Cliente Inactivo:**

1. Admin envía: `activar cliente`
2. Sistema pregunta: `¿Nombre del cliente?`
3. Admin responde: `Juan Pérez`
4. Sistema pregunta: `¿Qué te gustaría decirle a Juan Pérez?`
5. Admin responde: `ofrecer lentes nuevos con descuento`
6. Sistema genera borrador y muestra para confirmación
7. Admin confirma: `enviar`
8. Sistema guarda mensaje para envío automático

**Resultado:** Mensaje personalizado creado sin escribirlo manualmente, listo para enviar cuando el cliente esté disponible.

## Filosofía

- **Determinismo sobre IA**: State machine explícito, sin LLMs en runtime
- **Separación de planos**: Admin plane vs Customer plane desde Layer 0 (Signal Dispatcher)
- **Observabilidad**: Logs estructurados en cada transición
- **Testing first**: 88 tests unitarios garantizan estabilidad

## Arquitectura

```
Webhook (WhatsApp Cloud API)
    ↓
Handler (FastAPI)
    ↓
Dispatcher (Layer 0) ← Clasifica: ADMIN o CUSTOMER
    ↓
Engine (State Machine)
    ↓
Persistence (JSON + SQLite)
```

**Estados:**
- **Admin flow**: setup, activation
- **Customer flow**: servicios, turnos

**Storage:**
- Conversaciones: `data/conversations_state.json`
- Message drafts: `data/nordia.db`

## Cómo Correr

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar WHATSAPP_TOKEN, PHONE_ID, etc.

# Correr servidor
uvicorn app.main:app --reload

# Endpoint webhook
POST http://localhost:8000/webhook
```

## Cómo Correr Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_engine.py -v
pytest tests/test_dispatcher.py -v
pytest tests/test_activation_flow.py -v

# Con cobertura
pytest tests/ --cov=app
```

## Estructura del Proyecto

```
app/
├── main.py              # FastAPI app, webhook handler
├── engine.py            # State machine principal
├── dispatcher.py        # Signal Dispatcher (Layer 0)
├── state.py             # State management wrapper
├── persistence.py       # JSON + SQLite storage
├── validators.py        # Input validation
└── message_generator.py # Message drafting

tests/
├── test_engine.py       # 37 tests
├── test_dispatcher.py   # 7 tests
├── test_activation_flow.py # 7 tests
└── ...                  # 88 tests totales

data/
├── conversations_state.json  # Estado conversacional
└── nordia.db                 # Message drafts (SQLite)
```

## Configuración Admin

Editar `app/dispatcher.py`:

```python
ADMIN_WHITELIST = [
    "5493794281273"  # Agregar número admin
]
```

## Licencia

MIT
