# Análisis de Modos de Falla

## Cuándo usar
- Antes de deployar cualquier versión
- Después de un bug en producción
- Antes de demo importante

## Severidad
🔴 **CRITICAL** - Ejecutar antes de cada deploy

---

## Prompt

```
ROLE: Sos un ingeniero de confiabilidad (SRE) que busca formas de romper sistemas.

TAREA: Identificá todos los modos de falla posibles en Nordia WhatsApp IA.

CATEGORÍAS DE FALLA:

1. FALLAS DE CREDENTIAL
   - Token de WhatsApp expirado
   - Token revocado por Meta
   - Credentials de DB inválidas
   - API key de LLM agotada

2. FALLAS DE RATE LIMIT
   - WhatsApp API rechaza por límite diario
   - WhatsApp API rechaza por límite por segundo
   - Demasiados usuarios simultáneos

3. FALLAS DE ESTADO
   - Usuario en medio de setup y se reinicia el servidor
   - Usuario envía mensajes fuera de orden
   - Dos mensajes llegan al mismo tiempo

4. FALLAS DE VALIDACIÓN
   - Usuario envía imagen cuando esperábamos texto
   - Usuario envía mensaje de 10,000 caracteres
   - Usuario envía caracteres especiales que rompen SQL/JSON

5. FALLAS DE RED
   - Webhook de WhatsApp no llega
   - Respuesta de WhatsApp tarda >30 segundos
   - cloudflared tunnel se cae

PARA CADA MODO DE FALLA:
1. Escenario exacto que lo causa
2. Comportamiento actual del sistema
3. Comportamiento deseado
4. Código actual responsable (archivo:función)
5. Fix propuesto (mínimo viable)

OUTPUT EN MARKDOWN CON TABLA:
| Modo Falla | Probabilidad | Impacto | Estado Actual | Fix Propuesto |
```

---

## Output esperado

Tabla completa de modos de falla:

```markdown
| Modo de Falla | Prob | Impacto | Estado Actual | Fix Propuesto | Prioridad |
|---------------|------|---------|---------------|---------------|-----------|
| Token expirado | 100% | ALTO | No detecta | Healthcheck startup | P0 |
| Mensaje muy largo | 30% | MEDIO | Procesa todo | Limit 500 chars | P1 |
| Webhook duplicado | 20% | BAJO | Procesa 2x | Idempotencia | P2 |
```

Código de cada fix.
