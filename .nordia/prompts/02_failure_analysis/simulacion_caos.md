# Simulación de Caos

## Cuándo usar
- Después de implementar feature crítica
- Antes de lanzamiento importante
- Después de incidente en producción

## Severidad
🔴 **HIGH** - Ejecutar en features críticas

---

## Prompt

```
ROLE: Sos un tester de caos que intenta romper el sistema de todas las formas posibles.

TAREA: Generá un script de prueba que simule escenarios de falla extremos.

ESCENARIOS A SIMULAR:

1. MENSAJE MIENTRAS SE REINICIA
   - Usuario envía "setup"
   - Sistema recibe webhook
   - ANTES de responder, FastAPI se reinicia
   - Usuario envía "Barbería Los Andes"
   - ¿El sistema recupera el contexto?

2. SPAM DE MENSAJES
   - Usuario envía 10 mensajes en 1 segundo
   - ¿Todos se procesan?
   - ¿Mantiene orden?
   - ¿Evita duplicados?

3. MENSAJES FUERA DE ORDEN
   - Usuario inicia setup
   - Responde pregunta 3 antes que pregunta 2
   - ¿El sistema detecta y maneja?

4. TOKEN EXPIRA DURANTE CONVERSACIÓN
   - Usuario a mitad de setup
   - Token de WhatsApp expira
   - Sistema intenta responder
   - ¿Qué pasa?

PARA CADA ESCENARIO:
1. Script bash/python para reproducir
2. Comportamiento esperado
3. Comportamiento actual (ejecutar y reportar)
4. Fix si falla

OUTPUT:
- Scripts ejecutables
- Resultados de ejecución
- Lista de bugs encontrados
```

---

## Output esperado

Scripts de prueba de caos + resultados:

```bash
#!/bin/bash
# test_chaos_restart.sh

# Simular mensaje + restart + mensaje
curl -X POST http://localhost:8000/webhook -d '{"message": "setup"}'
pkill -f uvicorn &
sleep 1
uvicorn app.main:app &
curl -X POST http://localhost:8000/webhook -d '{"message": "Barbería X"}'

# ¿Mantiene contexto? → NO → BUG ENCONTRADO
```

Lista de bugs + fixes.
