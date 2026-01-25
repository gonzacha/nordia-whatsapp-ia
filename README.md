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

Crear archivo .env (opcional):

```bash
cp .env.example .env
```

Ejecutar servidor:

```bash
uvicorn app.main:app --reload
```

El servidor estará corriendo en http://localhost:8000

## Uso

### Healthcheck

```bash
curl http://localhost:8000/
```

### Probar webhook

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"from": "5491112345678", "message": "hola"}'
```

## Flujo de Conversación

1. Cliente: "hola" → Sistema: "Hola 👋 ¿Querés sacar un turno? Respondé SI"
2. Cliente: "si" → Sistema: "¿Qué servicio te interesa?"
3. Cliente: "corte" → Sistema: "¿Qué día te gustaría?"
4. Cliente: "lunes" → Sistema: "¿A qué hora?"
5. Cliente: "10:00" → Sistema: "¿Cuál es tu nombre?"
6. Cliente: "Juan" → Sistema: "Listo, tu turno quedó agendado 👍"

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

## Notas

- Este es un MVP bootstrap, no un sistema de producción
- El cliente WhatsApp está simulado (stub)
- No incluye integración con OpenAI aún
- No incluye integración con WhatsApp real aún
