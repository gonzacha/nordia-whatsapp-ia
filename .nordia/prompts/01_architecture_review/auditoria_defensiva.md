# Auditoría de Arquitectura Defensiva

## Cuándo usar
- Antes de agregar cualquier feature nueva
- Después de 3+ días de desarrollo continuo
- Cuando sientas que el sistema se está volviendo frágil

## Severidad
🔴 **HIGH** - Ejecutar cada 2-3 features nuevas

---

## Prompt

```
ROLE: Sos un arquitecto de software senior especializado en sistemas resilientes.

TAREA: Auditá la arquitectura actual de Nordia WhatsApp IA con enfoque en ingeniería defensiva.

ANALIZAR:

1. PUNTOS DE FALLA ÚNICOS
   - ¿Qué componente, si falla, detiene todo el sistema?
   - ¿Hay algún archivo, token, o conexión crítica sin respaldo?

2. ESTADOS GLOBALES
   - ¿Qué estados del sistema están explícitamente modelados?
   - ¿Qué pasa si FastAPI se reinicia en medio de una conversación?

3. PERSISTENCIA
   - ¿Todos los datos críticos se guardan en disco?
   - ¿Hay algún estado solo en RAM que debería persistir?

4. VALIDACIÓN DE TRANSICIONES
   - ¿Las transiciones de estado están validadas?
   - ¿Se puede llegar a estados inconsistentes?

5. MANEJO DE ERRORES
   - ¿Los errores externos (WhatsApp API, LLM) se convierten en estados observables?
   - ¿O se loguean y se ignoran?

OUTPUT ESPERADO:
- Lista de Single Points of Failure con severidad (CRÍTICO/MEDIO/BAJO)
- Recomendaciones específicas con estimación de tiempo de implementación
- Priorización por impacto vs esfuerzo
```

---

## Output esperado

Informe estructurado con:

1. **Tabla de Single Points of Failure:**
   ```
   | Componente | Severidad | Impacto | Mitigación | Tiempo |
   ```

2. **Estados globales no persistidos:**
   - Lista de variables en RAM
   - Consecuencia de pérdida
   - Solución propuesta

3. **Recomendaciones priorizadas:**
   - P0: Crítico (hacer ya)
   - P1: Alto (siguiente sprint)
   - P2: Medio (backlog)

---

## Ejemplo de uso

```bash
# Después de implementar 3 features nuevas
cat .nordia/prompts/01_architecture_review/auditoria_defensiva.md

# Pegar prompt en Claude Code

# Claude analiza y retorna:
# SPOF DETECTADOS:
# 1. [CRÍTICO] WHATSAPP_TOKEN - Si expira, sistema no envía
#    Mitigación: Healthcheck + modo degradado (2h)
#
# 2. [CRÍTICO] conversaciones{} en RAM - Reinicio pierde todo
#    Mitigación: Persistencia JSON (1h)
#
# 3. [MEDIO] Sin backup de SQLite
#    Mitigación: Backup diario automático (30min)
```
