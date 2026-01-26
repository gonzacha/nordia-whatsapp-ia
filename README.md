# Nordia WhatsApp IA

WhatsApp AI receptionist MVP para gestión de turnos de comercios.

## Descripción

Sistema simple de webhook que recibe mensajes de WhatsApp, detecta el comercio y ejecuta un motor de estados para gestionar reservas de turnos.

## Stack Tecnológico

- Python 3.11
- FastAPI
- SQLite
- SQLAlchemy
- Uvicorn

## Requisitos

- Python 3.11+
- pip

## Setup

Clonar el repositorio y crear entorno virtual:

```bash
git clone https://github.com/gonzacha/nordia-whatsapp-ia.git
cd nordia-whatsapp-ia
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar variables de entorno:

```bash
cp .env.example .env
```

Editar `.env` y agregar tu token de WhatsApp:

```
WHATSAPP_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=976165072250440
WHATSAPP_API_VERSION=v22.0
WHATSAPP_VERIFY_TOKEN=nordia_verify_token_123
```

Ejecutar servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará corriendo en http://localhost:8000

## Configuración de WhatsApp Cloud API

### 1. Verificar Webhook

Meta enviará una petición GET para verificar tu webhook:

```
GET /webhook?hub.mode=subscribe&hub.verify_token=nordia_verify_token_123&hub.challenge=CHALLENGE_STRING
```

El servidor responderá con el challenge si el verify_token coincide.

### 2. Configurar Webhook en Meta

1. Ve a https://developers.facebook.com/apps/
2. Selecciona tu app
3. WhatsApp > Configuration
4. Webhook URL: `https://tu-dominio.com/webhook`
5. Verify Token: `nordia_verify_token_123`
6. Suscribirse a: `messages`

### 3. Exponer el servidor local (desarrollo)

Usa ngrok para exponer tu servidor local:

```bash
ngrok http 8000
```

Copia la URL HTTPS que te da ngrok (ej: https://abc123.ngrok.io) y úsala como Webhook URL en Meta.

## Uso

### Healthcheck

```bash
curl http://localhost:8000/
```

### Enviar mensaje manualmente (testing)

```bash
curl -X POST https://graph.facebook.com/v22.0/976165072250440/messages \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5491112345678",
    "type": "text",
    "text": {
      "body": "Hola desde la API"
    }
  }'
```

## Comandos Disponibles

### Setup de Comercio
- `/setup` - Configura tu negocio (nombre, horarios, servicios)

### Gestión de Turnos
- `hola` - Inicia conversación para sacar turno
- `cancelar` - Cancela un turno existente
- `reprogramar` - Reprograma un turno existente

## Flujo de Conversación

### Sacar Turno
1. Cliente: "hola" → Sistema: "Hola, soy Nordia de [Negocio] 👋 ¿Querés sacar un turno? Respondé SI"
2. Cliente: "si" → Sistema: "¿Qué servicio te interesa?"
3. Cliente: "corte" → Sistema: "¿Qué día te gustaría?"
4. Cliente: "lunes" → Sistema: "¿A qué hora?"
5. Cliente: "10:00" → Sistema: "¿Cuál es tu nombre?" (valida disponibilidad)
6. Cliente: "Juan" → Sistema: "Listo, tu turno quedó agendado 👍"

### Cancelar Turno
1. Cliente: "cancelar" → Sistema: "Decime tu nombre por favor"
2. Cliente: "Juan" → Sistema: "Tu turno del lunes a las 10:00 fue cancelado ✅"

### Reprogramar Turno
1. Cliente: "reprogramar" → Sistema: "Decime tu nombre por favor"
2. Cliente: "Juan" → Sistema: "Perfecto 👍 ¿Qué día te gustaría ahora?"
3. (Continúa con flujo normal de reserva)

## Estructura del Proyecto

```
.
├── app/
│   ├── main.py       # FastAPI application
│   ├── config.py     # Configuración
│   ├── models.py     # Modelos SQLAlchemy
│   ├── engine.py     # State machine
│   ├── whatsapp.py   # WhatsApp stub
│   └── prompts.py    # System prompts
├── data/             # SQLite database
├── tests/
├── requirements.txt
└── README.md
```

## Características

- ✅ Integración con WhatsApp Cloud API
- ✅ Setup de comercio vía WhatsApp
- ✅ Gestión de turnos (crear, cancelar, reprogramar)
- ✅ Validación de disponibilidad de horarios
- ✅ Saludos personalizados con nombre del negocio
- ✅ State machine simple pero funcional
- ✅ Persistencia con SQLite

## Notas

- Este es un MVP funcional con WhatsApp Cloud API real
- No incluye autenticación de usuarios
- No incluye panel de administración
- No incluye integración con OpenAI (solo flujo hardcodeado)
